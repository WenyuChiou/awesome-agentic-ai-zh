"""Regression tests for the post-build site contract."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parent.parent


def _load(name: str):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


audit = _load("check-rendered-site")
build_docs = _load("build-docs-tree")
hooks = _load("mkdocs_hooks")
SITE_URL = "https://example.test/docs/"


def _page(
    lang: str,
    *,
    href: str = "asset.txt",
    alternate_overrides: dict[str, str] | None = None,
) -> str:
    links = {
        "zh-TW": SITE_URL,
        "zh-Hans": SITE_URL + "zh-Hans/",
        "en": SITE_URL + "en/",
        "x-default": SITE_URL,
    }
    links.update(alternate_overrides or {})
    alternates = "".join(
        f'<link rel="alternate" hreflang="{item}" href="{destination}">'
        for item, destination in links.items()
    )
    return f'<html lang="{lang}"><head>{alternates}</head><body><a href="{href}">x</a></body></html>'


def _good_site(tmp_path: Path) -> Path:
    site = tmp_path / "site"
    for directory, lang in ((Path(), "zh-TW"), (Path("en"), "en"), (Path("zh-Hans"), "zh-Hans")):
        target = site / directory
        target.mkdir(parents=True)
        (target / "index.html").write_text(_page(lang), encoding="utf-8")
        (target / "asset.txt").write_text("ok", encoding="utf-8")
        search = target / "search"
        search.mkdir()
        (search / "search_index.json").write_text(json.dumps({"docs": []}), encoding="utf-8")
    return site


def test_good_rendered_site_passes(tmp_path: Path) -> None:
    assert audit.audit_site(
        _good_site(tmp_path), base_path="/docs/", site_url=SITE_URL
    ) == []


def test_broken_link_and_wrong_language_fail(tmp_path: Path) -> None:
    site = _good_site(tmp_path)
    (site / "en" / "index.html").write_text(
        _page("zh", href="missing.txt"), encoding="utf-8"
    )
    problems = audit.audit_site(site, base_path="/docs/", site_url=SITE_URL)
    assert any("html lang" in item for item in problems)
    assert any("broken rendered target" in item for item in problems)


def test_maintainer_plan_cannot_enter_site_or_search(tmp_path: Path) -> None:
    site = _good_site(tmp_path)
    plan = site / "docs" / "plans" / "draft" / "index.html"
    plan.parent.mkdir(parents=True)
    plan.write_text(_page("zh-TW", href="../../../../asset.txt"), encoding="utf-8")
    search = site / "search" / "search_index.json"
    search.write_text(json.dumps({"docs": [{"location": "docs/plans/draft/"}]}), encoding="utf-8")
    problems = audit.audit_site(site, base_path="/docs/", site_url=SITE_URL)
    assert any("maintainer-only page" in item for item in problems)
    assert any("leaked into search" in item for item in problems)


def test_search_text_may_name_maintainer_files_without_publishing_them(tmp_path: Path) -> None:
    site = _good_site(tmp_path)
    search = site / "search" / "search_index.json"
    search.write_text(
        json.dumps(
            {
                "docs": [
                    {
                        "location": "CHANGELOG/",
                        "text": "Historical note about docs/TESTING_PLAN.md",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    assert audit.audit_site(site, base_path="/docs/", site_url=SITE_URL) == []


def test_empty_site_and_missing_search_index_fail(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    assert any("no HTML pages" in item for item in audit.audit_site(empty))

    site = _good_site(tmp_path)
    for index in site.rglob("search_index.json"):
        index.unlink()
    problems = audit.audit_site(site, base_path="/docs/", site_url=SITE_URL)
    assert any("no search index" in item for item in problems)


def test_active_content_and_existing_escape_target_fail(tmp_path: Path) -> None:
    site = _good_site(tmp_path)
    (site / "index.html").write_text(
        _page("zh-TW", href="javascript:alert(1)"), encoding="utf-8"
    )
    problems = audit.audit_site(site, base_path="/docs/", site_url=SITE_URL)
    assert any("forbidden active-content" in item for item in problems)

    outside = tmp_path / "outside.txt"
    outside.write_text("not public", encoding="utf-8")
    (site / "index.html").write_text(
        _page("zh-TW", href="../outside.txt"), encoding="utf-8"
    )
    problems = audit.audit_site(site, base_path="/docs/", site_url=SITE_URL)
    assert any("escapes site root" in item for item in problems)


def test_dangerous_first_duplicate_href_cannot_hide_from_audit(tmp_path: Path) -> None:
    site = _good_site(tmp_path)
    unsafe = _page("zh-TW").replace(
        '<a href="asset.txt">',
        '<a href="javascript:alert(1)" href="#safe">',
    )
    (site / "index.html").write_text(unsafe, encoding="utf-8")

    problems = audit.audit_site(site, base_path="/docs/", site_url=SITE_URL)
    assert any("duplicate URL attribute on <a> href" in item for item in problems)
    assert any("forbidden active-content" in item for item in problems)


def test_hreflang_destination_and_x_default_must_match_page(tmp_path: Path) -> None:
    site = _good_site(tmp_path)
    (site / "index.html").write_text(
        _page(
            "zh-TW",
            alternate_overrides={
                "zh-Hans": SITE_URL + "en/",
                "x-default": "https://external.example/",
            },
        ),
        encoding="utf-8",
    )
    problems = audit.audit_site(site, base_path="/docs/", site_url=SITE_URL)
    assert any("hreflang 'zh-Hans'" in item for item in problems)
    assert any("hreflang 'x-default'" in item for item in problems)


def test_public_build_rejects_external_target_symlink(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "repo"
    public = repo / "public"
    public.mkdir(parents=True)
    (repo / "index.md").write_text("# Home", encoding="utf-8")
    outside = tmp_path / "private.txt"
    outside.write_text("private", encoding="utf-8")
    try:
        (public / "escape.txt").symlink_to(outside)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"symlinks unavailable: {exc}")

    monkeypatch.setattr(build_docs, "REPO", repo)
    monkeypatch.setattr(build_docs, "DEST", repo / "_build" / "docs")
    monkeypatch.setattr(build_docs, "CONTENT_DIRS", ["public"])
    monkeypatch.setattr(build_docs, "CONTENT_FILES", [])
    monkeypatch.setattr(build_docs, "ROOT_STEMS", ["index"])

    assert build_docs.main() == 1
    assert not build_docs.DEST.exists()


def test_hooks_strip_source_switcher_rewrite_links_and_add_metadata(tmp_path: Path) -> None:
    markdown = "# Title\n\n> **繁體中文** | [简体中文](./page.zh-Hans.md) | [English](./page.en.md)\n\nBody"
    assert "page.zh-Hans.md" not in hooks.strip_github_language_switcher(markdown)

    (tmp_path / "resources").mkdir()
    (tmp_path / "resources" / "guide.md").write_text("# guide", encoding="utf-8")
    rewritten = hooks.rewrite_local_html_links(
        '<a href="resources/guide.md">guide</a>',
        src_path="about.md",
        page_url="about/",
        repo_root=tmp_path,
    )
    assert 'href="../resources/guide/"' in rewritten

    (tmp_path / "CONTRIBUTORS.md").write_text("# contributors", encoding="utf-8")
    fallback = hooks.rewrite_local_html_links(
        '<a href="CONTRIBUTORS.en.md?view=full#people">contributors</a>',
        src_path="ROADMAP.en.md",
        page_url="en/ROADMAP/",
        repo_root=tmp_path,
    )
    assert 'href="../CONTRIBUTORS/?view=full#people"' in fallback

    output = hooks.add_locale_metadata(
        '<html lang="zh"><head></head><body></body></html>',
        src_path="stages/page.zh-Hans.md",
        site_url="https://example.test/docs/",
    )
    assert '<html lang="zh-Hans"' in output
    assert output.count('rel="alternate"') == 4


def test_hooks_keep_individual_language_badges() -> None:
    badges = (
        "[![繁體中文](badge.svg)](README.md)\n"
        "[![简体中文](badge.svg)](README.zh-Hans.md)\n"
        "[![English](badge.svg)](README.en.md)\n"
    )
    assert hooks.strip_github_language_switcher(badges) == badges


def test_only_theme_search_share_placeholder_is_sanitized() -> None:
    html = (
        '<a href="javascript:void(0)" data-md-component="search-share">share</a>'
        '<a href="javascript:alert(1)">unsafe</a>'
    )
    sanitized = hooks.sanitize_theme_placeholders(html)
    assert 'href="#" data-md-component="search-share"' in sanitized
    assert 'href="javascript:alert(1)"' in sanitized


@pytest.mark.parametrize(
    ("page_url", "label"),
    [
        ("en/branches/DESIGN/", "Open full-size image"),
        ("zh-Hans/branches/DESIGN/", "打开原图"),
    ],
)
def test_diagram_caption_uses_rendered_fallback_locale(page_url: str, label: str) -> None:
    page = SimpleNamespace(
        url=page_url,
        file=SimpleNamespace(src_path="branches/DESIGN.md"),
    )
    rendered = hooks.on_page_content(
        '<p><img src="../../resources/diagrams/example.png" alt="map"></p>',
        page=page,
        config=None,
        files=None,
    )
    assert label in rendered

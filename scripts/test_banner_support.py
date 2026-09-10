"""Focused contracts for site banner enhancement and static PDF images."""
from __future__ import annotations

import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]


def _load(filename: str):
    spec = importlib.util.spec_from_file_location(filename.replace("-", "_"), ROOT / "scripts" / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hooks = _load("mkdocs_hooks.py")
release = _load("release_manifest.py")
tree = _load("build-docs-tree.py")


class Tags(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.tags: list[tuple[str, dict[str, str | None]]] = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def of_type(self, tag):
        return [attrs for kind, attrs in self.tags if kind == tag]


@pytest.mark.parametrize("locale,suffix,play", [
    ("zh-TW", "", "播放動畫"),
    ("en", ".en", "Play animation"),
    ("zh-Hans", ".zh-Hans", "播放动画"),
])
def test_site_banner_is_one_eager_static_image_with_localized_controls(locale, suffix, play):
    src = f"../resources/diagrams/banner{suffix}.svg"
    source = f'<p><img alt="A &amp; B" src="{src}" loading="lazy" /></p>'
    rendered = hooks.enhance_diagram_html(source, locale=locale)
    tags = Tags(rendered)
    assert tags.of_type("img") == [{
        "alt": "A & B", "decoding": "async", "src": src.removesuffix(".svg") + ".png",
        "loading": "eager",
    }]
    wrapper = tags.of_type("div")[0]
    assert wrapper["class"] == "aaz-banner"
    assert wrapper["data-animated-src"] == src
    assert wrapper["data-static-src"] == src.removesuffix(".svg") + ".png"
    assert wrapper["data-play-label"] == play
    assert wrapper["data-reduced-label"]
    assert tags.of_type("button") == [{"class": "aaz-banner__toggle", "type": "button", "hidden": None}]
    assert tags.of_type("a")[0]["href"] == wrapper["data-static-src"]
    assert tags.of_type("a")[0]["target"] == "_blank"
    assert tags.of_type("a")[0]["rel"] == "noopener"
    assert hooks._FULL_SIZE_LABELS[locale] in rendered
    assert hooks._BANNER_ROUTE_HINTS[locale] in rendered
    assert not tags.of_type("figure")
    assert hooks.enhance_diagram_html(rendered, locale=locale) == rendered


def test_banner_url_query_is_preserved_and_html_escaped_once():
    source = '<p><img alt="Banner" src="../resources/diagrams/banner.svg?v=2&amp;x=3" /></p>'
    rendered = hooks.enhance_diagram_html(source, locale="en")
    tags = Tags(rendered)
    assert tags.of_type("img")[0]["src"] == "../resources/diagrams/banner.png?v=2&x=3"
    assert tags.of_type("div")[0]["data-animated-src"] == "../resources/diagrams/banner.svg?v=2&x=3"
    assert "&amp;amp;" not in rendered


def test_svg_banners_do_not_change_ordinary_figures_or_external_images():
    diagram = '<p><img src="../resources/diagrams/lesson.svg" alt="Lesson"></p>'
    rendered = hooks.enhance_diagram_html(diagram, locale="en")
    assert len(Tags(rendered).of_type("figure")) == 1
    assert Tags(rendered).of_type("img")[0]["loading"] == "lazy"
    external = '<p><img src="https://example.com/resources/diagrams/banner.svg" alt="External"></p>'
    assert hooks.enhance_diagram_html(external, locale="en") == external


@pytest.mark.parametrize("locale,suffix,hint", [
    ("zh-TW", "", "依需求選一條延伸路線，不必全部走完。"),
    ("en", ".en", "Choose one extension for your needs; you do not need to follow every path."),
    ("zh-Hans", ".zh-Hans", "依需求选一条延伸路线，不必全部走完。"),
])
def test_role_motion_keeps_a_lazy_figure_with_both_original_links(locale, suffix, hint):
    src = f"../resources/diagrams/branch-decision-tree{suffix}.svg"
    static = src.removesuffix(".svg") + ".png"
    rendered = hooks.enhance_diagram_html(f'<p><img src="{src}" alt="Roles &amp; choices"></p>', locale=locale)
    tags = Tags(rendered)
    assert tags.of_type("img") == [{
        "src": static, "alt": "Roles & choices", "decoding": "async", "loading": "lazy",
    }]
    figure, = tags.of_type("figure")
    assert set(figure["class"].split()) == {"aaz-diagram", "aaz-banner"}
    assert figure["data-static-src"] == static
    assert figure["data-animated-src"] == src
    assert figure["data-play-label"] == hooks._BANNER_MOTION_LABELS[locale][0]
    assert figure["data-reduced-label"] == hooks._BANNER_MOTION_LABELS[locale][2]
    image_link, fullsize_link = tags.of_type("a")
    assert image_link["class"] == "aaz-diagram__image-link"
    assert image_link["aria-label"] == f"{hooks._FULL_SIZE_LABELS[locale]}: Roles & choices"
    for link in (image_link, fullsize_link):
        assert link["href"] == static
        assert link["target"] == "_blank"
        assert link["rel"] == "noopener"
    assert tags.of_type("figcaption") == [{"class": "aaz-diagram__caption"}]
    assert tags.of_type("button")[0]["hidden"] is None
    assert hint in rendered
    assert hooks._BANNER_ROUTE_HINTS[locale] not in rendered
    assert hooks.enhance_diagram_html(rendered, locale=locale) == rendered


@pytest.mark.parametrize("src", [
    "https://example.com/resources/diagrams/branch-decision-tree.svg",
    "//example.com/resources/diagrams/branch-decision-tree.svg",
    "../resources/diagrams/branch-decision-tree-custom.svg",
    "../resources/diagrams/branch-decision-tree.fr.svg",
    "../resources/diagrams/branch-decision-tree.png",
])
def test_role_motion_does_not_expand_the_exact_local_svg_allowlist(src):
    rendered = hooks.enhance_diagram_html(f'<p><img src="{src}" alt="Other"></p>', locale="en")
    assert "data-animated-src" not in rendered
    assert "aaz-banner__toggle" not in rendered


@pytest.mark.parametrize("locale,suffix", [("zh-TW", ""), ("en", ".en"), ("zh-Hans", ".zh-Hans")])
@pytest.mark.parametrize("basename", ["banner", "branch-decision-tree"])
def test_pdf_assembly_replaces_only_exact_local_banner_embeds(tmp_path, monkeypatch, locale, suffix, basename):
    local = f"resources/diagrams/{basename}{suffix}"
    untouched = [
        "![Lesson](resources/diagrams/lesson.svg)",
        "![Other](resources/diagrams/banner-custom.svg)",
        "![Other role](resources/diagrams/branch-decision-tree-custom.svg)",
        f"[Original]({local}.svg)",
        f"![Elsewhere](other/{local}.svg)",
    ]
    (tmp_path / "README.md").write_text(
        f"# Example\n![Banner]({local}.svg)\n" + "\n".join(untouched), encoding="utf-8"
    )
    manifest = {
        "locales": {locale: {"title": "Example", "subtitle": "Example", "html_lang": locale}},
        "pages": [{"id": "readme", "localized": {locale: "README.md"}}],
    }
    monkeypatch.setattr(release, "ROOT", tmp_path)
    monkeypatch.setattr(release, "validate_pages_manifest", lambda: manifest)
    assembled = release.assemble_markdown(locale, "v2026.09.08")
    assert f"![Banner]({local}.png)" in assembled
    assert f"![Banner]({local}.svg)" not in assembled
    assert all(image in assembled for image in untouched)


def test_site_script_is_registered_and_staged():
    asset = "docs/javascripts/banner-motion.js"
    assert asset in tree.CONTENT_FILES
    assert f"extra_javascript:\n  - {asset}" in (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert ROOT / asset in tree._selected_public_sources()


@pytest.mark.parametrize("prefix", ["", "en/", "zh-Hans/"])
def test_release_url_parity_accepts_the_exact_localized_banner_controls_link(prefix):
    site = "https://wenyuchiou.github.io/awesome-agentic-ai-zh/"
    assert release._external_urls(f"[Controls]({site}{prefix}about/)", "README.md") == {f"{site}about/"}


@pytest.mark.parametrize("url", [
    "https://example.com/en/about/",
    "https://wenyuchiou.github.io/another-repository/en/about/",
    "https://wenyuchiou.github.io/awesome-agentic-ai-zh/en/resources/",
    "https://wenyuchiou.github.io/awesome-agentic-ai-zh/en/about/?mode=other",
    "https://wenyuchiou.github.io/awesome-agentic-ai-zh/en/about/#other",
    "https://wenyuchiou.github.io/awesome-agentic-ai-zh/fr/about/",
    "http://wenyuchiou.github.io/awesome-agentic-ai-zh/en/about/",
])
def test_release_url_parity_keeps_other_destinations_distinct(url):
    assert release._external_urls(f"[Other]({url})", "README.md") == {url}


def test_browser_state_contracts():
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is required for the banner browser-state tests")
    result = subprocess.run(
        [node, "--test", str(ROOT / "scripts" / "test_banner_motion.cjs")],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

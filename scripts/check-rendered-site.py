#!/usr/bin/env python3
"""Audit the built MkDocs site instead of assuming source links rendered well."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

DEFAULT_BASE_PATH = "/awesome-agentic-ai-zh/"
DEFAULT_SITE_URL = "https://wenyuchiou.github.io/awesome-agentic-ai-zh/"
EXPECTED_ALTERNATES = {"zh-TW", "zh-Hans", "en", "x-default"}
FORBIDDEN_SCHEMES = {"javascript", "vbscript"}


@dataclass
class PageData:
    lang: str | None = None
    refs: list[str] = field(default_factory=list)
    alternates: dict[str, str] = field(default_factory=dict)
    duplicate_alternates: set[str] = field(default_factory=set)
    duplicate_url_attributes: list[str] = field(default_factory=list)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.data = PageData()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values: dict[str, list[str]] = {}
        for name, value in attrs:
            if value is not None:
                values.setdefault(name, []).append(value)
        if tag == "html":
            self.data.lang = next(iter(values.get("lang", [])), None)
        for key in ("href", "src"):
            url_values = values.get(key, [])
            self.data.refs.extend(url_values)
            if len(url_values) > 1:
                self.data.duplicate_url_attributes.append(f"<{tag}> {key}")
        rel = next(iter(values.get("rel", [])), None)
        if tag == "link" and rel == "alternate":
            hreflang = next(iter(values.get("hreflang", [])), None)
            href = next(iter(values.get("href", [])), None)
            if hreflang and href:
                if hreflang in self.data.alternates:
                    self.data.duplicate_alternates.add(hreflang)
                self.data.alternates[hreflang] = href


def expected_lang(parts: tuple[str, ...]) -> str:
    if parts and parts[0] == "en":
        return "en"
    if parts and parts[0] == "zh-Hans":
        return "zh-Hans"
    return "zh-TW"


def parse_page(path: Path) -> PageData:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.data


def expected_alternates(relative: Path, site_url: str) -> dict[str, str]:
    """Return the exact page-equivalent locale URLs for one rendered page."""

    parts = list(relative.parts)  # abs-parts-ok: caller passes page.relative_to(site)
    if parts and parts[0] in {"en", "zh-Hans"}:
        parts.pop(0)
    if parts and parts[-1] == "index.html":
        parts.pop()
    elif parts and parts[-1].endswith(".html"):
        parts[-1] = parts[-1][: -len(".html")]
    route = "/".join(parts)
    if route:
        route += "/"
    base = site_url.rstrip("/") + "/"
    traditional = base + route
    return {
        "zh-TW": traditional,
        "zh-Hans": base + "zh-Hans/" + route,
        "en": base + "en/" + route,
        "x-default": traditional,
    }


def local_target(site: Path, page: Path, raw: str, base_path: str) -> Path | None:
    parsed = urlsplit(raw)
    if parsed.scheme or parsed.netloc or raw.startswith(("#", "mailto:", "tel:", "data:")):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    if path.startswith(base_path):
        return (site / path[len(base_path) :]).resolve()
    if path.startswith("/"):
        return (site / "__invalid_root_absolute__" / path.lstrip("/")).resolve()
    return (page.parent / path).resolve()


def target_exists(target: Path) -> bool:
    return (target.exists() and target.is_file()) or (target / "index.html").is_file()


def audit_site(
    site: Path,
    *,
    base_path: str = DEFAULT_BASE_PATH,
    site_url: str = DEFAULT_SITE_URL,
) -> list[str]:
    site = site.resolve()
    problems: list[str] = []
    if not site.is_dir():
        return [f"site directory does not exist: {site}"]

    html_pages = sorted(path for path in site.rglob("*.html") if path.name != "404.html")
    if not html_pages:
        problems.append("rendered site contains no HTML pages")
    for page in html_pages:
        relative = page.relative_to(site)
        data = parse_page(page)
        wanted_lang = expected_lang(page.relative_to(site).parts)
        if data.lang != wanted_lang:
            problems.append(f"{relative}: html lang={data.lang!r}, expected {wanted_lang!r}")
        for duplicate in data.duplicate_url_attributes:
            problems.append(f"{relative}: duplicate URL attribute on {duplicate}")
        expected = expected_alternates(relative, site_url)
        missing_alternates = EXPECTED_ALTERNATES - data.alternates.keys()
        if missing_alternates:
            problems.append(
                f"{relative}: missing hreflang alternates {sorted(missing_alternates)}"
            )
        extra_alternates = data.alternates.keys() - EXPECTED_ALTERNATES
        if extra_alternates:
            problems.append(
                f"{relative}: unexpected hreflang alternates {sorted(extra_alternates)}"
            )
        if data.duplicate_alternates:
            problems.append(
                f"{relative}: duplicate hreflang alternates "
                f"{sorted(data.duplicate_alternates)}"
            )
        for language, wanted_href in expected.items():
            actual_href = data.alternates.get(language)
            if actual_href is not None and actual_href != wanted_href:
                problems.append(
                    f"{relative}: hreflang {language!r} points to {actual_href!r}, "
                    f"expected {wanted_href!r}"
                )
        for raw in data.refs:
            scheme = urlsplit(raw).scheme.lower()
            if scheme in FORBIDDEN_SCHEMES:
                problems.append(
                    f"{relative}: forbidden active-content URL scheme in {raw!r}"
                )
                continue
            target = local_target(site, page, raw, base_path)
            if target is None:
                continue
            if not target.is_relative_to(site):
                problems.append(
                    f"{relative}: rendered target escapes site root {raw!r} -> {target}"
                )
                continue
            if target_exists(target):
                continue
            rendered_target = target.relative_to(site).as_posix()
            problems.append(f"{relative}: broken rendered target {raw!r} -> {rendered_target}")

    forbidden_pages = sorted(site.glob("**/docs/plans/**/*.html"))
    forbidden_pages += sorted(site.glob("**/docs/TESTING_PLAN/**/*.html"))
    for page in forbidden_pages:
        problems.append(f"maintainer-only page was published: {page.relative_to(site)}")

    search_indexes = sorted(site.glob("**/search/search_index.json"))
    if not search_indexes:
        problems.append("rendered site contains no search index")
    for index in search_indexes:
        try:
            payload = json.loads(index.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"{index.relative_to(site)}: unreadable search index: {exc}")
            continue
        locations = [
            str(item.get("location", "")).replace("\\", "/")
            for item in payload.get("docs", [])
            if isinstance(item, dict)
        ]
        if any(
            location.startswith("docs/plans/")
            or location.startswith("docs/TESTING_PLAN")
            for location in locations
        ):
            problems.append(f"{index.relative_to(site)}: maintainer plans leaked into search")

    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("_build/site"))
    parser.add_argument("--base-path", default=DEFAULT_BASE_PATH)
    parser.add_argument("--site-url", default=DEFAULT_SITE_URL)
    args = parser.parse_args(argv)
    problems = audit_site(
        args.site,
        base_path=args.base_path,
        site_url=args.site_url,
    )
    if problems:
        print(f"rendered-site audit failed with {len(problems)} problem(s):", file=sys.stderr)
        for problem in problems[:100]:
            print(f"- {problem}", file=sys.stderr)
        if len(problems) > 100:
            print(f"- ... {len(problems) - 100} more", file=sys.stderr)
        return 1
    print("rendered-site audit passed: links, locales, metadata, and public search")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

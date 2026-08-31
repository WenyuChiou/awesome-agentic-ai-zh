#!/usr/bin/env python3
"""Build and verify one trilingual release from two small YAML manifests."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from md_fences import strip_code_blocks


ROOT = Path(__file__).resolve().parent.parent
PAGES_MANIFEST = ROOT / "release" / "pages.yml"
NOTES_MANIFEST = ROOT / "release" / "notes.yml"
LOCALES = ("zh-TW", "zh-Hans", "en")
LOCALE_SUFFIX = {"zh-TW": "", "zh-Hans": ".zh-Hans", "en": ".en"}
REQUIRED_PAGE_IDS = {
    "readme",
    *(f"stage-{number:02d}" for number in range(9)),
    "stage-07-5",
    "cli-a1",
    "cli-a2",
    "cli-a3",
    "role-everyday-user",
    "role-developer",
    "role-researcher",
    "role-knowledge-worker",
    "role-teacher",
    "walkthrough-paper-bot",
    "capstone",
    "setup",
    "glossary",
    "resources-index",
    "advanced-rag",
    "agent-memory",
    "cli-agents-guide",
    "model-training-guide",
}
VERSION_RE = re.compile(r"^v(?P<year>\d{4})\.(?P<month>\d{2})\.(?P<day>\d{2})(?:-(?P<sequence>[2-9]\d*))?$")
URL_RE = re.compile(r"https?://[^\s<>\]\[\)\(\"'`，。；：！？、）]+")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
SUMMARY_RE = re.compile(r"<summary\b[^>]*>(.*?)</summary>", re.IGNORECASE | re.DOTALL)
DETAILS_TAG_RE = re.compile(r"</?details\b[^>]*>", re.IGNORECASE)
FRONT_MATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
REMOTE_MARKDOWN_IMAGE_RE = re.compile(
    r"!\[[^\]]*\]\(https?://[^\s)]+(?:\([^\s)]*\)[^\s)]*)?\)", re.IGNORECASE
)
REMOTE_HTML_IMAGE_RE = re.compile(
    r"<img\b[^>]*\bsrc\s*=\s*([\"'])https?://.*?\1[^>]*>",
    re.IGNORECASE | re.DOTALL,
)


class ReleaseManifestError(ValueError):
    """A release input violates the public release contract."""


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ReleaseManifestError(f"cannot read {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ReleaseManifestError(f"{path.relative_to(ROOT)} must contain a mapping")
    return payload


def validate_version(version: str, *, today: date | None = None) -> date:
    match = VERSION_RE.fullmatch(version)
    if not match:
        raise ReleaseManifestError(
            "version must look like vYYYY.MM.DD; use -2 or higher for another release that day"
        )
    try:
        release_date = date(
            int(match.group("year")), int(match.group("month")), int(match.group("day"))
        )
    except ValueError as exc:
        raise ReleaseManifestError(f"version contains an invalid calendar date: {version}") from exc
    if release_date > (today or date.today()):
        raise ReleaseManifestError(f"release date cannot be in the future: {version}")
    return release_date


def _safe_canonical_path(raw: object) -> PurePosixPath:
    if not isinstance(raw, str) or not raw:
        raise ReleaseManifestError("every page needs a non-empty path")
    if "\\" in raw:
        raise ReleaseManifestError(f"page path must use forward slashes: {raw}")
    path = PurePosixPath(raw)
    if path.is_absolute() or ".." in path.parts:  # abs-parts-ok: manifest path is repo-relative by contract
        raise ReleaseManifestError(f"page path must stay inside the repository: {raw}")
    if path.suffix != ".md" or path.name.endswith((".en.md", ".zh-Hans.md")):
        raise ReleaseManifestError(f"page path must be the canonical zh-TW .md file: {raw}")
    return path


def localized_path(canonical: PurePosixPath, locale: str) -> PurePosixPath:
    if locale not in LOCALE_SUFFIX:
        raise ReleaseManifestError(f"unsupported locale: {locale}")
    suffix = LOCALE_SUFFIX[locale]
    return canonical.with_name(f"{canonical.stem}{suffix}.md")


def _external_urls(text: str, source: str) -> set[str]:
    visible = strip_code_blocks(text, source=source)
    return {match.group(0).rstrip(".,;:!?") for match in URL_RE.finditer(visible)}


def _heading(text: str, source: str) -> str:
    match = H1_RE.search(text)
    if not match:
        raise ReleaseManifestError(f"release page has no H1 heading: {source}")
    return match.group(1).strip()


def _body_key_and_candidates(text: str, source: str) -> tuple[str, list[str]]:
    """Return normalized body prose and candidate snippets for PDF verification."""
    heading = H1_RE.search(text)
    if not heading:
        raise ReleaseManifestError(f"release page has no H1 heading: {source}")
    visible = strip_code_blocks(text[heading.end() :], source=source)
    body_key = _heading_key(visible)
    candidates: list[str] = []
    for raw_line in visible.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("#", "<", "![", "[", "---", "|")):
            continue
        marker = _heading_key(line)[:40]
        if len(marker) >= 16 and marker not in candidates:
            candidates.append(marker)
    if not candidates:
        raise ReleaseManifestError(f"release page has no extractable body marker: {source}")
    return body_key, candidates


def validate_pages_manifest(*, strict_urls: bool = False) -> dict[str, Any]:
    manifest = load_yaml(PAGES_MANIFEST)
    if manifest.get("schema_version") != 1:
        raise ReleaseManifestError("release/pages.yml schema_version must be 1")

    locales = manifest.get("locales")
    if not isinstance(locales, dict) or tuple(locales) != LOCALES:
        raise ReleaseManifestError(f"release locales must appear once in this order: {LOCALES}")
    for locale in LOCALES:
        config = locales[locale]
        if not isinstance(config, dict):
            raise ReleaseManifestError(f"locale {locale} must be a mapping")
        for field in ("html_lang", "title", "subtitle"):
            if not isinstance(config.get(field), str) or not config[field].strip():
                raise ReleaseManifestError(f"locale {locale} needs {field}")

    pages = manifest.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ReleaseManifestError("release/pages.yml needs an ordered pages list")
    ids: list[str] = []
    paths: list[str] = []
    normalized_pages: list[dict[str, Any]] = []
    body_keys: dict[tuple[str, str], str] = {}
    body_candidates: dict[tuple[str, str], list[str]] = {}
    for row in pages:
        if not isinstance(row, dict):
            raise ReleaseManifestError("every page entry must be a mapping")
        page_id = row.get("id")
        if not isinstance(page_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", page_id):
            raise ReleaseManifestError(f"invalid page id: {page_id!r}")
        canonical = _safe_canonical_path(row.get("path"))
        ids.append(page_id)
        paths.append(canonical.as_posix())
        localized: dict[str, str] = {}
        url_sets: dict[str, set[str]] = {}
        headings: dict[str, str] = {}
        for locale in LOCALES:
            relative = localized_path(canonical, locale)
            absolute = ROOT / relative
            if not absolute.is_file():
                raise ReleaseManifestError(f"missing {locale} release page: {relative}")
            text = absolute.read_text(encoding="utf-8")
            localized[locale] = relative.as_posix()
            headings[locale] = _heading(text, relative.as_posix())
            body_key, candidates = _body_key_and_candidates(text, relative.as_posix())
            body_keys[(page_id, locale)] = body_key
            body_candidates[(page_id, locale)] = candidates
            url_sets[locale] = _external_urls(text, relative.as_posix())
        if strict_urls:
            canonical_urls = url_sets["zh-TW"]
            for locale in LOCALES[1:]:
                if url_sets[locale] != canonical_urls:
                    missing = sorted(canonical_urls - url_sets[locale])
                    extra = sorted(url_sets[locale] - canonical_urls)
                    raise ReleaseManifestError(
                        f"external URL drift in {page_id} ({locale}); missing={missing}, extra={extra}"
                    )
        normalized_pages.append(
            {
                "id": page_id,
                "path": canonical.as_posix(),
                "localized": localized,
                "headings": headings,
            }
        )

    if len(ids) != len(set(ids)):
        raise ReleaseManifestError("release page ids must be unique")
    if len(paths) != len(set(paths)):
        raise ReleaseManifestError("release page paths must be unique")
    missing_ids = sorted(REQUIRED_PAGE_IDS - set(ids))
    if missing_ids:
        raise ReleaseManifestError(f"release page manifest is missing required ids: {missing_ids}")

    for page in normalized_pages:
        page_id = page["id"]
        page["body_markers"] = {}
        for locale in LOCALES:
            marker = next(
                (
                    candidate
                    for candidate in body_candidates[(page_id, locale)]
                    if all(
                        candidate not in body_keys[(other_id, locale)]
                        for other_id in ids
                        if other_id != page_id
                    )
                ),
                None,
            )
            if marker is None:
                raise ReleaseManifestError(
                    f"release page has no body marker unique to its page: {page_id} ({locale})"
                )
            page["body_markers"][locale] = marker

    manifest["pages"] = normalized_pages
    return manifest


def validate_notes_manifest(*, expected_version: str | None = None) -> dict[str, Any]:
    manifest = load_yaml(NOTES_MANIFEST)
    if manifest.get("schema_version") != 1:
        raise ReleaseManifestError("release/notes.yml schema_version must be 1")
    release_version = manifest.get("release_version")
    if not isinstance(release_version, str):
        raise ReleaseManifestError("release/notes.yml needs release_version")
    validate_version(release_version)
    if expected_version is not None and release_version != expected_version:
        raise ReleaseManifestError(
            f"release notes target {release_version}, not requested version {expected_version}"
        )
    changes = manifest.get("changes")
    if not isinstance(changes, list) or not changes:
        raise ReleaseManifestError("release/notes.yml needs at least one change")
    ids: list[str] = []
    for row in changes:
        if not isinstance(row, dict):
            raise ReleaseManifestError("every release change must be a mapping")
        change_id = row.get("id")
        if not isinstance(change_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", change_id):
            raise ReleaseManifestError(f"invalid release change id: {change_id!r}")
        ids.append(change_id)
        for field in ("category", *LOCALES):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ReleaseManifestError(f"release change {change_id} needs {field}")
        links = row.get("links")
        if not isinstance(links, list) or not links:
            raise ReleaseManifestError(f"release change {change_id} needs shared links")
        if any(not isinstance(link, str) or not link.startswith("https://") for link in links):
            raise ReleaseManifestError(f"release change {change_id} has an invalid shared link")
        if len(links) != len(set(links)):
            raise ReleaseManifestError(f"release change {change_id} repeats a shared link")
    if len(ids) != len(set(ids)):
        raise ReleaseManifestError("release change ids must be unique")
    return manifest


def asset_name(version: str, locale: str) -> str:
    validate_version(version)
    if locale not in LOCALES:
        raise ReleaseManifestError(f"unsupported locale: {locale}")
    return f"awesome-agentic-ai-zh-{version}-{locale}.pdf"


def _strip_front_matter(text: str) -> str:
    return FRONT_MATTER_RE.sub("", text, count=1)


def _expand_details(text: str) -> str:
    def summary(match: re.Match[str]) -> str:
        label = re.sub(r"\s+", " ", match.group(1)).strip()
        return f"\n### {label}\n"

    return DETAILS_TAG_RE.sub("", SUMMARY_RE.sub(summary, text))


def _strip_remote_images(text: str) -> str:
    """Keep release builds offline and omit badges or contributor mosaics."""
    return REMOTE_HTML_IMAGE_RE.sub("", REMOTE_MARKDOWN_IMAGE_RE.sub("", text))


def assemble_markdown(locale: str, version: str) -> str:
    validate_version(version)
    manifest = validate_pages_manifest()
    config = manifest["locales"][locale]
    title = str(config["title"]).replace('"', '\\"')
    cover_title = html.escape(str(config["title"]))
    cover_subtitle = html.escape(str(config["subtitle"]))
    lines = [
        "---",
        f'pagetitle: "{title} — {version}"',
        f'lang: "{config["html_lang"]}"',
        "toc: true",
        "toc-depth: 2",
        "---",
        "",
        '<div class="release-cover">',
        f"<h1>{cover_title}</h1>",
        f"<p>{cover_subtitle}</p>",
        f"<p><strong>{html.escape(version)}</strong></p>",
        '<span class="release-meta">@WenyuChiou</span>',
        "</div>",
        "",
    ]
    for page in manifest["pages"]:
        relative = page["localized"][locale]
        text = (ROOT / relative).read_text(encoding="utf-8")
        text = _strip_remote_images(_expand_details(_strip_front_matter(text))).strip()
        lines.extend(
            [
                '<div class="release-page-break"></div>',
                "",
                f"<!-- release-page:{page['id']} source:{relative} -->",
                "",
                text,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_notes(version: str, *, sha: str | None = None) -> str:
    validate_version(version)
    manifest = validate_notes_manifest(expected_version=version)
    labels = {
        "zh-TW": "繁體中文",
        "zh-Hans": "简体中文",
        "en": "English",
    }
    lines = [f"# {version} — 三語正式版 / Trilingual release", ""]
    for locale in LOCALES:
        lines.extend([f"## {labels[locale]}", ""])
        for change in manifest["changes"]:
            links = " · ".join(
                f"[來源 {index + 1}]({url})" if locale != "en" else f"[source {index + 1}]({url})"
                for index, url in enumerate(change["links"])
            )
            lines.append(
                f"- `{change['category']}` {change[locale]} {links}"
            )
        lines.append("")
    if sha:
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            raise ReleaseManifestError("release SHA must be a full lowercase 40-character commit")
        lines.extend(["---", "", f"Source commit: [`{sha}`](https://github.com/WenyuChiou/awesome-agentic-ai-zh/commit/{sha})", ""])
    return "\n".join(lines).rstrip() + "\n"


def _heading_key(value: str) -> str:
    # A PDF body can contain an unrelated `[` thousands of characters before a
    # later `](...)`. Never let Markdown cleanup swallow across line breaks.
    value = re.sub(r"!?\[([^\]\n]*)\]\([^\)\n]*\)", r"\1", value)
    value = re.sub(r"</?[A-Za-z][^>\n]*>", "", value)
    value = html.unescape(value)
    value = unicodedata.normalize("NFKC", value)
    return "".join(char.lower() for char in value if char.isalnum())


def validate_pdfs(version: str, dist: Path, *, pdftotext: str = "pdftotext") -> dict[str, Any]:
    manifest = validate_pages_manifest()
    binary = shutil.which(pdftotext)
    if not binary:
        raise ReleaseManifestError(f"cannot find PDF text extractor: {pdftotext}")
    result: dict[str, Any] = {"version": version, "assets": {}}
    for locale in LOCALES:
        name = asset_name(version, locale)
        path = dist / name
        if not path.is_file() or path.stat().st_size < 10_000:
            raise ReleaseManifestError(f"missing or implausibly small PDF: {path}")
        extracted = subprocess.run(
            [binary, "-layout", str(path), "-"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.decode("utf-8", errors="replace")
        extracted_key = _heading_key(extracted)
        missing: list[str] = []
        for page in manifest["pages"]:
            heading_marker = _heading_key(page["headings"][locale])[:24]
            body_marker = page["body_markers"][locale]
            if (
                len(heading_marker) < 4
                or heading_marker not in extracted_key
                or body_marker not in extracted_key
            ):
                missing.append(f"{page['id']}:{page['headings'][locale]}")
        if missing:
            raise ReleaseManifestError(f"{name} is missing page headings: {missing}")
        if locale == "en" and re.search(
            r"(?im)\b(?:Deskto[ \t]*\r?\n[ \t]*p|Recommen[ \t]*\r?\n[ \t]*dation)\b",
            extracted,
        ):
            raise ReleaseManifestError(
                f"{name} splits an English table label across lines"
            )
        cjk_count = len(CJK_RE.findall(extracted))
        if locale == "en" and cjk_count > max(200, len(extracted) // 100):
            raise ReleaseManifestError(
                f"{name} contains too much CJK text for the English edition: {cjk_count} characters"
            )
        result["assets"][locale] = {
            "name": name,
            "bytes": path.stat().st_size,
            "extracted_characters": len(extracted),
            "cjk_characters": cjk_count,
            "headings_verified": len(manifest["pages"]),
            "body_markers_verified": len(manifest["pages"]),
        }
    return result


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate both manifests and every locale path")
    validate.add_argument("--strict-urls", action="store_true")
    validate.add_argument("--version")

    version = sub.add_parser("validate-version", help="validate a calendar release tag")
    version.add_argument("--version", required=True)

    listing = sub.add_parser("list-pages", help="print ordered source paths for one locale")
    listing.add_argument("--locale", required=True, choices=LOCALES)

    asset = sub.add_parser("asset-name", help="print the contracted PDF filename")
    asset.add_argument("--version", required=True)
    asset.add_argument("--locale", required=True, choices=LOCALES)

    assemble = sub.add_parser("assemble", help="expand details and assemble one PDF source")
    assemble.add_argument("--version", required=True)
    assemble.add_argument("--locale", required=True, choices=LOCALES)
    assemble.add_argument("--output", required=True, type=Path)

    notes = sub.add_parser("render-notes", help="render all three release-note sections")
    notes.add_argument("--version", required=True)
    notes.add_argument("--sha")
    notes.add_argument("--output", required=True, type=Path)

    pdfs = sub.add_parser("validate-pdfs", help="verify all three named PDF assets")
    pdfs.add_argument("--version", required=True)
    pdfs.add_argument("--dist", default=ROOT / "dist", type=Path)
    pdfs.add_argument("--pdftotext", default="pdftotext")
    pdfs.add_argument("--json", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    try:
        if args.command == "validate":
            pages = validate_pages_manifest(strict_urls=args.strict_urls)
            notes = validate_notes_manifest(expected_version=args.version)
            print(
                f"Release manifests passed: {len(pages['pages'])} pages × 3 locales, "
                f"{len(notes['changes'])} trilingual changes."
            )
        elif args.command == "validate-version":
            validate_version(args.version)
            print(args.version)
        elif args.command == "list-pages":
            manifest = validate_pages_manifest()
            print("\n".join(page["localized"][args.locale] for page in manifest["pages"]))
        elif args.command == "asset-name":
            print(asset_name(args.version, args.locale))
        elif args.command == "assemble":
            _write(args.output, assemble_markdown(args.locale, args.version))
            print(args.output)
        elif args.command == "render-notes":
            _write(args.output, render_notes(args.version, sha=args.sha))
            print(args.output)
        elif args.command == "validate-pdfs":
            payload = validate_pdfs(args.version, args.dist, pdftotext=args.pdftotext)
            if args.json:
                _write(args.json, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
            print(json.dumps(payload, ensure_ascii=False))
        return 0
    except (ReleaseManifestError, OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

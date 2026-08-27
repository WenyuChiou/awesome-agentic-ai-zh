#!/usr/bin/env python3
"""Ratcheted reader-experience checks for migrated learning-map pages.

The checker deliberately covers only pages listed in reader-ux-pages.yml. A
chapter joins the list after its beginner path has been reviewed in all three
locales. This keeps old pages visible as migration work without letting a
finished page quietly grow another wall of text.

Usage:
    python scripts/check-reader-ux.py
    python scripts/check-reader-ux.py --config path/to/config.yml
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("❌ PyYAML required. Install: pip install pyyaml", file=sys.stderr)
    raise SystemExit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "scripts" / "reader-ux-pages.yml"
LOCALES = ("zh-TW", "en", "zh-Hans")
DETAILS_START_RE = re.compile(r"^\s*<details\b", re.IGNORECASE)
DETAILS_END_RE = re.compile(r"^\s*</details\s*>", re.IGNORECASE)
OPEN_ATTR_RE = re.compile(r"(?:^|\s)open(?:\s|=|>)", re.IGNORECASE)
SUMMARY_RE = re.compile(r"<summary\b[^>]*>(.*?)</summary>", re.IGNORECASE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
TAG_RE = re.compile(r"<[^>]+>")
TH_RE = re.compile(r"<th\b[^>]*>", re.IGNORECASE)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_fences import code_line_flags, strip_code_blocks  # noqa: E402

_ANCHOR_SPEC = importlib.util.spec_from_file_location(
    "check_anchors_for_reader_ux", Path(__file__).with_name("check-anchors.py")
)
_check_anchors = importlib.util.module_from_spec(_ANCHOR_SPEC)
_ANCHOR_SPEC.loader.exec_module(_check_anchors)
slugify = _check_anchors.slugify


@dataclass
class PageMetrics:
    visible_chars: int
    open_details_count: int
    open_summaries: list[str]
    visible_headings_outside_details: list[tuple[str, str]]


def _plain(text: str) -> str:
    """Remove HTML wrappers and lightweight Markdown decoration for matching."""
    text = TAG_RE.sub("", text)
    text = re.sub(r"\[([^]]+)]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_`~]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _without_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    """Remove non-rendered HTML comments while preserving text around them."""
    out: list[str] = []
    cursor = 0
    while cursor < len(line):
        if in_comment:
            end = line.find("-->", cursor)
            if end < 0:
                return "".join(out), True
            cursor = end + 3
            in_comment = False
            continue
        start = line.find("<!--", cursor)
        if start < 0:
            out.append(line[cursor:])
            break
        out.append(line[cursor:start])
        cursor = start + 4
        in_comment = True
    return "".join(out), in_comment


def _without_all_html_comments(text: str) -> str:
    """Strip HTML comments after fenced examples have already been blanked."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def analyze_markdown(text: str) -> tuple[PageMetrics, list[str]]:
    """Measure the visible Markdown source before the reader clicks anything.

    This is intentionally a conservative source-level proxy, not a browser DOM
    text-length claim. Markdown syntax and visible fenced code count. HTML
    comments and bodies of closed disclosures do not. Tags shown inside fenced
    examples are code, so they never open or close a real disclosure block.
    """
    stack: list[bool] = []
    visible_lines: list[str] = []
    open_summaries: list[str] = []
    outside_headings: list[tuple[str, str]] = []
    errors: list[str] = []
    open_details_count = 0
    in_comment = False
    lines = text.splitlines()
    code_flags = code_line_flags(text)

    for line_no, (line, in_code) in enumerate(zip(lines, code_flags), start=1):
        if in_comment:
            line, in_comment = _without_html_comments(line, in_comment)
            if not line:
                continue
        elif in_code:
            if not stack or all(stack):
                visible_lines.append(line)
            continue
        else:
            line, in_comment = _without_html_comments(line, False)
            if not line:
                continue

        if DETAILS_START_RE.match(line):
            is_open = bool(OPEN_ATTR_RE.search(line))
            stack.append(is_open)
            if is_open:
                open_details_count += 1
            continue

        if DETAILS_END_RE.match(line):
            if stack:
                stack.pop()
            else:
                errors.append(f"line {line_no}: closing </details> has no opener")
            continue

        summary = SUMMARY_RE.search(line)
        if summary:
            if not stack:
                errors.append(f"line {line_no}: <summary> is outside <details>")
                continue
            # A summary is visible only when every ancestor disclosure is open.
            if all(stack[:-1]):
                visible_lines.append(line)
            if stack[-1]:
                open_summaries.append(_plain(summary.group(1)))
            continue

        heading = HEADING_RE.match(line)
        if heading and not stack:
            raw_heading = heading.group(1)
            outside_headings.append((_plain(raw_heading), slugify(raw_heading)))

        if not stack or all(stack):
            visible_lines.append(line)

    if stack:
        errors.append(f"{len(stack)} unclosed <details> block(s)")
    if in_comment:
        errors.append("unclosed HTML comment")

    visible_chars = len(re.sub(r"\s+", "", "\n".join(visible_lines)))
    return PageMetrics(
        visible_chars, open_details_count, open_summaries, outside_headings
    ), errors


def _attr(tag: str, name: str) -> str | None:
    match = re.search(rf"\b{name}\s*=\s*(['\"])(.*?)\1", tag, re.IGNORECASE)
    return match.group(2) if match else None


def _resource_table_errors(text: str, expected: list[int]) -> list[str]:
    """Find one accessible grouped table matching the configured row spans."""
    structural_source = _without_all_html_comments(strip_code_blocks(text))
    candidates = re.findall(
        r"<table\b[^>]*>.*?</table>", structural_source, re.IGNORECASE | re.DOTALL
    )
    observed: list[list[int]] = []
    structural_errors: list[str] = []

    for table in candidates:
        thead_match = re.search(r"<thead\b[^>]*>(.*?)</thead>", table, re.IGNORECASE | re.DOTALL)
        if not thead_match:
            continue
        column_headers = TH_RE.findall(thead_match.group(1))
        groups = re.findall(r"<tbody\b[^>]*>(.*?)</tbody>", table, re.IGNORECASE | re.DOTALL)
        if len(groups) != len(expected):
            continue

        group_spans: list[int] = []
        group_errors: list[str] = []
        for index, (group, expected_rows) in enumerate(zip(groups, expected), start=1):
            rows = re.findall(r"<tr\b[^>]*>.*?</tr>", group, re.IGNORECASE | re.DOTALL)
            rowgroup_tags = [
                tag for tag in TH_RE.findall(group)
                if (_attr(tag, "scope") or "").lower() == "rowgroup"
            ]
            first_row_tags = [
                tag for tag in (TH_RE.findall(rows[0]) if rows else [])
                if (_attr(tag, "scope") or "").lower() == "rowgroup"
            ]
            if len(rowgroup_tags) != 1 or len(first_row_tags) != 1:
                group_errors.append(
                    f"resource <tbody> {index} must own exactly one rowgroup header in its first row"
                )
                group_spans.append(-1)
                continue
            raw_span = _attr(first_row_tags[0], "rowspan")
            span = int(raw_span) if raw_span and raw_span.isdigit() else -1
            group_spans.append(span)
            if len(rows) != expected_rows or span != expected_rows:
                group_errors.append(
                    f"resource <tbody> {index} has {len(rows)} row(s) and rowspan={raw_span!r}; "
                    f"expected {expected_rows}"
                )

        if group_spans != expected:
            structural_errors.extend(group_errors)
            if any(span >= 0 for span in group_spans):
                observed.append(group_spans)
            continue
        if not column_headers or any(
            (_attr(tag, "scope") or "").lower() != "col" for tag in column_headers
        ):
            group_errors.append('every resource column header must use scope="col"')
        if group_errors:
            structural_errors.extend(group_errors)
            continue
        return []

    if structural_errors:
        return structural_errors
    return [f"resource rowgroup spans are {observed or 'missing'}; expected {expected}"]


def _load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"config not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("reader UX config must use schema_version: 1")
    if not isinstance(data.get("pages"), list) or not data["pages"]:
        raise ValueError("reader UX config needs a non-empty pages list")
    terms = data.get("forbidden_open_summary_terms")
    if not isinstance(terms, dict) or set(terms) != set(LOCALES):
        raise ValueError("forbidden_open_summary_terms must define zh-TW, en, and zh-Hans")
    for locale, values in terms.items():
        if not isinstance(values, list) or not values or any(
            not isinstance(value, str) or not value.strip() for value in values
        ):
            raise ValueError(
                f"forbidden_open_summary_terms.{locale} must be a non-empty string list"
            )

    page_ids: set[str] = set()
    page_paths: set[str] = set()
    for index, page in enumerate(data["pages"], start=1):
        if not isinstance(page, dict):
            raise ValueError(f"pages[{index}] must be a mapping")
        page_id = page.get("id")
        if not isinstance(page_id, str) or not page_id.strip() or page_id in page_ids:
            raise ValueError(f"pages[{index}].id must be a unique non-empty string")
        page_ids.add(page_id)

        canonical = page.get("canonical")
        mirrors = page.get("mirrors")
        if not isinstance(canonical, str) or not canonical or Path(canonical).is_absolute():
            raise ValueError(f"{page_id}.canonical must be a relative path")
        if not isinstance(mirrors, dict) or set(mirrors) != {"en", "zh-Hans"} or any(
            not isinstance(value, str) or not value or Path(value).is_absolute()
            for value in mirrors.values()
        ):
            raise ValueError(f"{page_id}.mirrors must define relative en and zh-Hans paths")
        for rel in (canonical, mirrors["en"], mirrors["zh-Hans"]):
            if rel in page_paths:
                raise ValueError(f"page path is configured more than once: {rel}")
            page_paths.add(rel)

        limits = page.get("max_visible_chars")
        if not isinstance(limits, dict) or set(limits) != set(LOCALES) or any(
            not isinstance(value, int) or isinstance(value, bool) or value <= 0
            for value in limits.values()
        ):
            raise ValueError(f"{page_id}.max_visible_chars needs positive integers for all locales")
        max_open = page.get("max_open_details")
        if not isinstance(max_open, int) or isinstance(max_open, bool) or max_open < 0:
            raise ValueError(f"{page_id}.max_open_details must be a non-negative integer")

        sections = page.get("required_visible_sections")
        if not isinstance(sections, dict) or not sections:
            raise ValueError(f"{page_id}.required_visible_sections must be a non-empty mapping")
        for section_id, localized in sections.items():
            if not isinstance(section_id, str) or not section_id or not isinstance(localized, dict):
                raise ValueError(f"{page_id} has an invalid visible-section mapping")
            if set(localized) != set(LOCALES):
                raise ValueError(f"{page_id}.{section_id} must define all three locales")
            for locale, identity in localized.items():
                if not isinstance(identity, dict) or set(identity) != {"heading", "anchor"}:
                    raise ValueError(
                        f"{page_id}.{section_id}.{locale} needs exact heading and anchor"
                    )
                if any(
                    not isinstance(identity[key], str) or not identity[key].strip()
                    for key in ("heading", "anchor")
                ):
                    raise ValueError(
                        f"{page_id}.{section_id}.{locale} heading/anchor cannot be empty"
                    )

        groups = page.get("resource_group_rowspans")
        if groups is not None and (
            not isinstance(groups, list)
            or not groups
            or any(not isinstance(value, int) or isinstance(value, bool) or value <= 0 for value in groups)
        ):
            raise ValueError(f"{page_id}.resource_group_rowspans must be positive integers")
    return data


def check(config_path: Path) -> list[str]:
    config = _load_config(config_path)
    failures: list[str] = []
    ids: set[str] = set()

    for page in config["pages"]:
        page_id = page.get("id")
        if page_id in ids:
            failures.append(f"config: duplicate page id {page_id!r}")
            continue
        ids.add(page_id)

        mirrors = page.get("mirrors") or {}
        paths = {"zh-TW": page.get("canonical"), "en": mirrors.get("en"), "zh-Hans": mirrors.get("zh-Hans")}
        limits = page.get("max_visible_chars") or {}
        sections = page["required_visible_sections"]
        max_open = page.get("max_open_details")

        for locale, rel in paths.items():
            path = REPO_ROOT / rel
            label = f"{page_id}/{locale} ({rel})"
            if not path.exists():
                failures.append(f"{label}: missing page")
                continue
            text = path.read_text(encoding="utf-8")
            metrics, parse_errors = analyze_markdown(text)
            failures.extend(f"{label}: {item}" for item in parse_errors)

            if metrics.visible_chars > limits[locale]:
                failures.append(
                    f"{label}: {metrics.visible_chars} visible characters exceeds {limits[locale]}"
                )
            if metrics.open_details_count > max_open:
                failures.append(
                    f"{label}: {metrics.open_details_count} default-open details exceeds {max_open}"
                )

            terms = config["forbidden_open_summary_terms"][locale]
            for summary in metrics.open_summaries:
                lowered = summary.casefold()
                hits = [str(term) for term in terms if str(term).casefold() in lowered]
                if hits:
                    failures.append(
                        f"{label}: forbidden open summary {summary!r} contains {', '.join(hits)}"
                    )

            for section_id, localized in sections.items():
                wanted = _plain(localized[locale]["heading"])
                expected_anchor = localized[locale]["anchor"]
                exact_matches = [
                    anchor for heading, anchor in metrics.visible_headings_outside_details
                    if heading == wanted
                ]
                if not exact_matches:
                    failures.append(
                        f"{label}: required visible heading {section_id!r} ({wanted!r}) is missing or inside <details>"
                    )
                elif expected_anchor not in exact_matches:
                    failures.append(
                        f"{label}: heading {section_id!r} anchor is {exact_matches}; "
                        f"expected {expected_anchor!r}"
                    )

            expected_groups = page.get("resource_group_rowspans")
            if expected_groups:
                failures.extend(
                    f"{label}: {item}" for item in _resource_table_errors(text, expected_groups)
                )

    return failures


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args()
    try:
        failures = check(args.config.resolve())
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"❌ reader UX config error: {exc}")
        return 2
    if failures:
        print("❌ Reader UX ratchet failed:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    config = _load_config(args.config.resolve())
    print(f"✓ Reader UX ratchet passed for {len(config['pages'])} pages × 3 locales.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

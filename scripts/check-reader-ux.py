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
    details_count: int
    open_details_count: int
    open_summaries: list[str]
    visible_headings_outside_details: list[tuple[str, str]]
    visible_source: str


EXTERNAL_URL_RE = re.compile(r"https://[^\s<>)\"']+")
RATING_RE = re.compile(r"(?<!⭐)(⭐{1,5})(?!⭐)")


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
    details_count = 0
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
            details_count += 1
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
    visible_source = "\n".join(visible_lines)
    return PageMetrics(
        visible_chars,
        details_count,
        open_details_count,
        open_summaries,
        outside_headings,
        visible_source,
    ), errors


def _visible_heading_span(text: str, wanted: str) -> tuple[int, int, int] | None:
    """Return the exact visible heading span for one plain-text heading."""
    cursor = 0
    lines = text.splitlines(keepends=True)
    for line, in_code in zip(lines, code_line_flags(text), strict=True):
        if not in_code:
            heading = HEADING_RE.match(line.rstrip("\r\n"))
            if heading and _plain(heading.group(1)) == wanted:
                level = len(line) - len(line.lstrip("#"))
                return cursor, cursor + len(line), level
        cursor += len(line)
    return None


def _next_section_start(text: str, after: int, max_level: int) -> int:
    """Find the next visible heading that closes the current section."""
    cursor = 0
    lines = text.splitlines(keepends=True)
    for line, in_code in zip(lines, code_line_flags(text), strict=True):
        line_end = cursor + len(line)
        if cursor >= after and not in_code:
            heading = HEADING_RE.match(line.rstrip("\r\n"))
            if heading:
                level = len(line) - len(line.lstrip("#"))
                if level <= max_level:
                    return cursor
        cursor = line_end
    return len(text)


def _without_link_destinations(text: str) -> str:
    """Keep Markdown link labels while removing URL text from prose checks."""
    return re.sub(r"\[([^]]+)]\([^)]*\)", r"\1", text)


def _first_literal_span(text: str, literal: str) -> tuple[int, int] | None:
    escaped = re.escape(literal)
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 ._/-]*", literal):
        escaped = rf"(?<![A-Za-z0-9_-]){escaped}(?![A-Za-z0-9_-])"
    match = re.search(escaped, text, re.IGNORECASE)
    return match.span() if match else None


def _inside_bold_span(text: str, span: tuple[int, int]) -> bool:
    start, end = span
    for match in re.finditer(r"\*\*([^*\n]+)\*\*", text):
        if match.start(1) <= start and end <= match.end(1):
            return True
    return False


def _core_term_errors(
    text: str,
    metrics: PageMetrics,
    core_terms: dict[str, Any],
    sections: dict[str, Any],
    locale: str,
) -> list[str]:
    """Check the visible, ordered, bold core-term block for one locale."""
    errors: list[str] = []
    visible = metrics.visible_source
    section_id = core_terms["section_id"]
    exercise_id = core_terms["first_exercise_section_id"]
    core_heading = _plain(sections[section_id][locale]["heading"])
    exercise_heading = _plain(sections[exercise_id][locale]["heading"])
    core_span = _visible_heading_span(visible, core_heading)
    exercise_span = _visible_heading_span(visible, exercise_heading)
    if core_span is None or exercise_span is None:
        return errors  # The required-visible-section gate reports the missing heading.
    if core_span[0] >= exercise_span[0]:
        return ["core terms section must appear before the first exercise"]

    prose = TAG_RE.sub("", _without_link_destinations(strip_code_blocks(visible)))
    # The page title may name the chapter topic. It is navigation, not the first
    # explanatory use, so exclude only the H1 line from the first-use check.
    first_use_lines: list[str] = []
    page_title_removed = False
    for line in prose.splitlines():
        if not page_title_removed and re.match(r"^#\s+", line):
            page_title_removed = True
            continue
        first_use_lines.append(line)
    first_use_source = "\n".join(first_use_lines)

    section_end = _next_section_start(visible, core_span[1], core_span[2])
    core_end = min(section_end, exercise_span[0])
    core_block = visible[core_span[1] : core_end]
    ordered_spans: list[tuple[int, int, str]] = []

    for item in core_terms["terms"]:
        localized = item[locale]
        term = localized["term"]
        label = localized["label"]
        first_span = _first_literal_span(first_use_source, term)
        if first_span is None:
            errors.append(f"core term {term!r} is missing from visible prose")
        elif not _inside_bold_span(first_use_source, first_span):
            errors.append(f"first visible use of core term {term!r} must be bold")

        marker = f"**{label}**"
        starts = [match.start() for match in re.finditer(re.escape(marker), core_block)]
        if not starts:
            errors.append(
                f"core term {term!r} needs visible bold definition label {marker!r}"
            )
            continue
        ordered_spans.append((starts[0], starts[0] + len(marker), term))

    if len(ordered_spans) == len(core_terms["terms"]):
        starts = [item[0] for item in ordered_spans]
        if starts != sorted(starts):
            errors.append("core-term definition labels are not in configured order")
        else:
            minimum = core_terms["min_definition_chars"]
            for index, (_, end, term) in enumerate(ordered_spans):
                next_start = (
                    ordered_spans[index + 1][0]
                    if index + 1 < len(ordered_spans)
                    else len(core_block)
                )
                explanation = _plain(core_block[end:next_start])
                explanation_chars = len(re.sub(r"\s+", "", explanation))
                if explanation_chars < minimum:
                    errors.append(
                        f"core term {term!r} has only {explanation_chars} explanation "
                        f"characters; expected at least {minimum}"
                    )
    return errors


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


def _resource_url_rating_pairs(
    text: str, expected: list[int]
) -> tuple[list[tuple[str, str]], list[str]]:
    """Return each resource URL with its exact editorial rating.

    URL order and aggregate star counts are not enough: two translated rows can
    silently exchange ratings while both old checks stay green. This parser is
    intentionally limited to the same accessible grouped table shape already
    enforced by ``_resource_table_errors``.
    """
    structural_source = _without_all_html_comments(strip_code_blocks(text))
    candidates = re.findall(
        r"<table\b[^>]*>.*?</table>", structural_source, re.IGNORECASE | re.DOTALL
    )

    for table in candidates:
        groups = re.findall(r"<tbody\b[^>]*>(.*?)</tbody>", table, re.IGNORECASE | re.DOTALL)
        if len(groups) != len(expected):
            continue

        rows: list[str] = []
        matches_shape = True
        for group, expected_rows in zip(groups, expected):
            group_rows = re.findall(r"<tr\b[^>]*>.*?</tr>", group, re.IGNORECASE | re.DOTALL)
            first_row_headers = [
                tag for tag in (TH_RE.findall(group_rows[0]) if group_rows else [])
                if (_attr(tag, "scope") or "").lower() == "rowgroup"
            ]
            raw_span = _attr(first_row_headers[0], "rowspan") if len(first_row_headers) == 1 else None
            if (
                len(group_rows) != expected_rows
                or raw_span is None
                or not raw_span.isdigit()
                or int(raw_span) != expected_rows
            ):
                matches_shape = False
                break
            rows.extend(group_rows)

        if not matches_shape:
            continue

        pairs: list[tuple[str, str]] = []
        errors: list[str] = []
        for index, row in enumerate(rows, start=1):
            urls = EXTERNAL_URL_RE.findall(row)
            ratings = RATING_RE.findall(TAG_RE.sub(" ", row))
            if len(urls) != 1:
                errors.append(
                    f"resource row {index} must contain exactly one external URL; found {len(urls)}"
                )
            if len(ratings) != 1:
                errors.append(
                    f"resource row {index} must contain exactly one 1-to-5-star rating; "
                    f"found {len(ratings)}"
                )
            if len(urls) == 1 and len(ratings) == 1:
                pairs.append((urls[0], ratings[0]))
        return pairs, errors

    return [], ["could not find the configured grouped resource table for URL/rating parity"]


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
        required_details = page.get("required_details_count")
        if required_details is not None and (
            not isinstance(required_details, int)
            or isinstance(required_details, bool)
            or required_details < 0
        ):
            raise ValueError(
                f"{page_id}.required_details_count must be a non-negative integer"
            )

        forbidden = page.get("forbidden_terms")
        if forbidden is not None:
            if not isinstance(forbidden, dict) or set(forbidden) != set(LOCALES):
                raise ValueError(
                    f"{page_id}.forbidden_terms must define zh-TW, en, and zh-Hans"
                )
            for locale, values in forbidden.items():
                if not isinstance(values, list) or any(
                    not isinstance(value, str) or not value.strip() for value in values
                ):
                    raise ValueError(
                        f"{page_id}.forbidden_terms.{locale} must be a string list"
                    )
        include_code = page.get("forbidden_terms_include_code", False)
        if not isinstance(include_code, bool):
            raise ValueError(f"{page_id}.forbidden_terms_include_code must be a boolean")

        parity = page.get("parity")
        if parity is not None:
            if not isinstance(parity, dict) or not parity:
                raise ValueError(f"{page_id}.parity must be a non-empty mapping")
            unknown = set(parity) - {
                "ordered_external_urls",
                "literals",
                "resource_url_ratings",
            }
            if unknown:
                raise ValueError(f"{page_id}.parity has unknown keys: {sorted(unknown)}")
            ordered_urls = parity.get("ordered_external_urls", False)
            if not isinstance(ordered_urls, bool):
                raise ValueError(f"{page_id}.parity.ordered_external_urls must be a boolean")
            resource_ratings = parity.get("resource_url_ratings", False)
            if not isinstance(resource_ratings, bool):
                raise ValueError(f"{page_id}.parity.resource_url_ratings must be a boolean")
            literals = parity.get("literals", [])
            if not isinstance(literals, list) or any(
                not isinstance(value, str) or not value.strip() for value in literals
            ):
                raise ValueError(f"{page_id}.parity.literals must be a string list")
            if len(literals) != len(set(literals)):
                raise ValueError(f"{page_id}.parity.literals cannot contain duplicates")

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

        visible_order = page.get("visible_section_order")
        if visible_order is not None:
            if (
                not isinstance(visible_order, list)
                or len(visible_order) < 2
                or any(not isinstance(value, str) or not value for value in visible_order)
                or len(visible_order) != len(set(visible_order))
            ):
                raise ValueError(
                    f"{page_id}.visible_section_order must be a unique string list with at least two items"
                )
            unknown_sections = set(visible_order) - set(sections)
            if unknown_sections:
                raise ValueError(
                    f"{page_id}.visible_section_order has unknown section ids: "
                    f"{sorted(unknown_sections)}"
                )

        core_terms = page.get("core_terms")
        if core_terms is not None:
            if not isinstance(core_terms, dict) or set(core_terms) != {
                "section_id",
                "first_exercise_section_id",
                "min_definition_chars",
                "terms",
            }:
                raise ValueError(
                    f"{page_id}.core_terms needs section_id, first_exercise_section_id, "
                    "min_definition_chars, and terms"
                )
            for key in ("section_id", "first_exercise_section_id"):
                value = core_terms[key]
                if not isinstance(value, str) or value not in sections:
                    raise ValueError(
                        f"{page_id}.core_terms.{key} must name a required_visible_sections key"
                    )
            if core_terms["section_id"] == core_terms["first_exercise_section_id"]:
                raise ValueError(
                    f"{page_id}.core_terms section and first exercise must be different"
                )
            minimum = core_terms["min_definition_chars"]
            if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum <= 0:
                raise ValueError(
                    f"{page_id}.core_terms.min_definition_chars must be a positive integer"
                )
            configured_terms = core_terms["terms"]
            if not isinstance(configured_terms, list) or not configured_terms:
                raise ValueError(f"{page_id}.core_terms.terms must be a non-empty list")
            term_ids: set[str] = set()
            localized_terms: dict[str, set[str]] = {locale: set() for locale in LOCALES}
            for term_index, item in enumerate(configured_terms, start=1):
                if not isinstance(item, dict) or set(item) != {"id", *LOCALES}:
                    raise ValueError(
                        f"{page_id}.core_terms.terms[{term_index}] needs id and all three locales"
                    )
                term_id = item["id"]
                if (
                    not isinstance(term_id, str)
                    or not term_id.strip()
                    or term_id in term_ids
                ):
                    raise ValueError(
                        f"{page_id}.core_terms.terms[{term_index}].id must be unique and non-empty"
                    )
                term_ids.add(term_id)
                for locale in LOCALES:
                    localized = item[locale]
                    if not isinstance(localized, dict) or set(localized) != {"term", "label"}:
                        raise ValueError(
                            f"{page_id}.core_terms.terms[{term_index}].{locale} "
                            "needs term and label"
                        )
                    term = localized["term"]
                    label = localized["label"]
                    if any(
                        not isinstance(value, str) or not value.strip()
                        for value in (term, label)
                    ):
                        raise ValueError(
                            f"{page_id}.core_terms.terms[{term_index}].{locale} "
                            "term and label cannot be empty"
                        )
                    folded = term.casefold()
                    if folded in localized_terms[locale]:
                        raise ValueError(
                            f"{page_id}.core_terms has duplicate {locale} term {term!r}"
                        )
                    localized_terms[locale].add(folded)
                    if folded not in label.casefold():
                        raise ValueError(
                            f"{page_id}.core_terms label {label!r} must contain term {term!r}"
                        )

        groups = page.get("resource_group_rowspans")
        if groups is not None and (
            not isinstance(groups, list)
            or not groups
            or any(not isinstance(value, int) or isinstance(value, bool) or value <= 0 for value in groups)
        ):
            raise ValueError(f"{page_id}.resource_group_rowspans must be positive integers")
        if (page.get("parity") or {}).get("resource_url_ratings") and not groups:
            raise ValueError(
                f"{page_id}.parity.resource_url_ratings requires resource_group_rowspans"
            )
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
        localized_text: dict[str, str] = {}

        for locale, rel in paths.items():
            path = REPO_ROOT / rel
            label = f"{page_id}/{locale} ({rel})"
            if not path.exists():
                failures.append(f"{label}: missing page")
                continue
            text = path.read_text(encoding="utf-8")
            localized_text[locale] = text
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
            required_details = page.get("required_details_count")
            if required_details is not None and metrics.details_count != required_details:
                failures.append(
                    f"{label}: {metrics.details_count} details block(s); expected {required_details}"
                )

            forbidden_source = (
                text if page.get("forbidden_terms_include_code", False)
                else strip_code_blocks(text)
            )
            searchable = _without_all_html_comments(forbidden_source).casefold()
            for term in (page.get("forbidden_terms") or {}).get(locale, []):
                if term.casefold() in searchable:
                    failures.append(f"{label}: forbidden term {term!r} is present")

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

            visible_order = page.get("visible_section_order") or []
            if visible_order:
                ordered_positions: list[int] = []
                for section_id in visible_order:
                    identity = sections[section_id][locale]
                    wanted = _plain(identity["heading"])
                    expected_anchor = identity["anchor"]
                    position = next(
                        (
                            index
                            for index, (heading, anchor) in enumerate(
                                metrics.visible_headings_outside_details
                            )
                            if heading == wanted and anchor == expected_anchor
                        ),
                        None,
                    )
                    if position is None:
                        break
                    ordered_positions.append(position)
                if (
                    len(ordered_positions) == len(visible_order)
                    and ordered_positions != sorted(ordered_positions)
                ):
                    failures.append(
                        f"{label}: required visible sections are out of order; "
                        f"expected {' -> '.join(visible_order)}"
                    )

            core_terms = page.get("core_terms")
            if core_terms:
                failures.extend(
                    f"{label}: {item}"
                    for item in _core_term_errors(
                        text, metrics, core_terms, sections, locale
                    )
                )

            expected_groups = page.get("resource_group_rowspans")
            if expected_groups:
                failures.extend(
                    f"{label}: {item}" for item in _resource_table_errors(text, expected_groups)
                )

        parity = page.get("parity") or {}
        if len(localized_text) == len(LOCALES):
            canonical_text = _without_all_html_comments(localized_text["zh-TW"])
            if parity.get("ordered_external_urls"):
                expected_urls = EXTERNAL_URL_RE.findall(canonical_text)
                for locale in ("en", "zh-Hans"):
                    actual_urls = EXTERNAL_URL_RE.findall(
                        _without_all_html_comments(localized_text[locale])
                    )
                    if actual_urls != expected_urls:
                        failures.append(
                            f"{page_id}/{locale}: ordered external URLs differ from zh-TW"
                        )
            if parity.get("resource_url_ratings"):
                expected_groups = page["resource_group_rowspans"]
                expected_pairs, pair_errors = _resource_url_rating_pairs(
                    localized_text["zh-TW"], expected_groups
                )
                failures.extend(
                    f"{page_id}/zh-TW: {item}" for item in pair_errors
                )
                if not pair_errors:
                    for locale in ("en", "zh-Hans"):
                        actual_pairs, actual_errors = _resource_url_rating_pairs(
                            localized_text[locale], expected_groups
                        )
                        failures.extend(
                            f"{page_id}/{locale}: {item}" for item in actual_errors
                        )
                        if not actual_errors and actual_pairs != expected_pairs:
                            failures.append(
                                f"{page_id}/{locale}: resource URL/rating pairs differ from zh-TW"
                            )
            for literal in parity.get("literals", []):
                expected_count = canonical_text.count(literal)
                if expected_count == 0:
                    failures.append(
                        f"{page_id}/zh-TW: parity literal {literal!r} is missing"
                    )
                    continue
                for locale in ("en", "zh-Hans"):
                    actual_count = _without_all_html_comments(
                        localized_text[locale]
                    ).count(literal)
                    if actual_count != expected_count:
                        failures.append(
                            f"{page_id}/{locale}: parity literal {literal!r} occurs "
                            f"{actual_count} time(s); zh-TW has {expected_count}"
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

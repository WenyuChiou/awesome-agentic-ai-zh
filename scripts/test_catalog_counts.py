#!/usr/bin/env python3
"""Regression tests for the catalog entry and no-advertised-total gate."""

from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
from pathlib import Path


_SPEC = importlib.util.spec_from_file_location(
    "check_catalog_counts", Path(__file__).with_name("check-catalog-counts.py")
)
ccc = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ccc)


def _parse(body: str):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "catalog.md"
        path.write_text(body, encoding="utf-8")
        return ccc.parse_catalog(path)


def test_counts_entry_without_bracket_link() -> None:
    body = "## 1. Things\n\n### [a/b](https://x)\n\n### Hosted service\n"
    assert _parse(body) == {1: 2}


def test_not_an_entry_marker_excludes_heading() -> None:
    body = (
        "## 1. Things\n\n### [a/b](https://x)\n\n"
        "<!-- not-an-entry -->\n### How the tools compose\n"
    )
    assert _parse(body) == {1: 1}


def test_headings_outside_numbered_sections_are_ignored() -> None:
    body = "## Some prose\n\n### Help\n\n## 1. Things\n\n### [x/y](https://x)\n"
    assert _parse(body) == {1: 1}


def test_details_do_not_change_entry_counting() -> None:
    body = (
        "## 1. Things\n\n<details markdown=\"1\">\n<summary>Show entries</summary>\n\n"
        "### [x/y](https://x)\n\n### Hosted service\n\n</details>\n"
    )
    assert _parse(body) == {1: 2}


def test_finds_advertised_catalog_totals() -> None:
    lines = (
        "See resources/mcp-skills-catalog.md — 81+ integrations",
        "完整 MCP / Skills catalog（81 個 entry）",
        "Catalog includes 81 curated tools",
        "MCP, Skills, Plugins, with an 81+ entry integration catalog",
        "Plugins and 81+ integrations grouped by use case",
    )
    assert [ccc.advertised_catalog_totals(line) for line in lines] == [
        [81],
        [81],
        [81],
        [81],
        [81],
    ]


def test_finds_volatile_public_inventory_totals_in_prose_and_html() -> None:
    lines = (
        "A roadmap with 240+ curated resources and runnable examples",
        "目前 240+ curated 资源",
        "81+ entry integration catalog",
        '<span class="aaz-num">240+</span><span class="aaz-lbl">projects</span>',
        "術語決策影響 100+ 個 entry",
        "术语决策影响 100+ 个 entry",
        "It's MIT, ~240 curated projects with runnable examples",
        "integrations grouped by 16 use-case categories",
    )
    assert [ccc.advertised_public_inventory_totals(line) for line in lines] == [
        [240],
        [240],
        [81],
        [240],
        [100],
        [100],
        [240],
        [16],
    ]


def test_finds_stale_outreach_stage_counts_and_stage8_roles() -> None:
    stale = (
        "a 7-stage learning roadmap",
        "我們的 7 階段三語學習地圖",
        "8-" + "stage roadmap from Stage 0 to multi-agent production",
        "Stage 8 (multi-agent orchestration and sandboxes)",
        "Stage 8 (production)",
        "Stage 8 的多代理編排",
    )
    current = (
        "Stage 7 covers multi-agent production; Stage 8 covers Agent Interfaces.",
        "Stage 0 → Stage 8 learning roadmap",
    )
    assert all(ccc.has_stale_outreach_route(line) for line in stale)
    assert all(not ccc.has_stale_outreach_route(line) for line in current)


def test_finds_cached_outreach_popularity_and_traffic_metrics() -> None:
    frozen = (
        "★525 week 1",
        "⭐ ≈ **1.9k**",
        "1.9k stars",
        "525 stars",
        "120 stargazers",
        "3,185 views",
        "900 visitors",
        "50 forks",
        "1,099 clones",
        "408 unique cloners",
    )
    dynamic = (
        "![GitHub stars](https://img.shields.io/github/stars/example/repo)",
        "gh repo view example/repo --json stargazerCount",
        "Popularity metrics are intentionally omitted because they drift.",
    )
    assert all(ccc.has_outreach_popularity_metric(line) for line in frozen)
    assert all(not ccc.has_outreach_popularity_metric(line) for line in dynamic)


def test_ignores_versions_time_ranges_and_project_totals() -> None:
    lines = (
        "Use Python 3.11 and read this in 30-50 minutes",
        "Stage 05 links to mcp-skills-catalog.md",
        "The repository contains 240 projects",
    )
    assert all(not ccc.advertised_catalog_totals(line) for line in lines)
    assert all(not ccc.advertised_public_inventory_totals(line) for line in lines)


def test_repo_is_consistent_and_does_not_advertise_a_total() -> None:
    buffer, previous_stdout, previous_argv = io.StringIO(), sys.stdout, sys.argv
    sys.stdout = buffer
    try:
        sys.argv = ["check-catalog-counts.py", "--quiet"]
        assert ccc.main() == 0, buffer.getvalue()
    finally:
        sys.stdout = previous_stdout
        sys.argv = previous_argv


def _run_all() -> int:
    functions = [
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    failed = 0
    for function in functions:
        try:
            function()
            print(f"  PASS  {function.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"  FAIL  {function.__name__}: {exc!r}")
    print(f"\n{len(functions) - failed}/{len(functions)} passed")
    return failed


if __name__ == "__main__":
    raise SystemExit(1 if _run_all() else 0)

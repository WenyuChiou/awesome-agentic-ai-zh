#!/usr/bin/env python3
"""Regression tests for scripts/check-reader-ux.py.

Run with plain Python; pytest is optional:
    python scripts/test_reader_ux.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("check-reader-ux.py")


def _copy_checker(root: Path) -> None:
    (root / "scripts").mkdir()
    for name in (SCRIPT.name, "md_fences.py", "check-anchors.py"):
        source = SCRIPT.with_name(name)
        (root / "scripts" / name).write_text(
            source.read_text(encoding="utf-8"), encoding="utf-8"
        )


def _page(body: str) -> str:
    return "# Page\n\n## Start\n\n" + body


def _config(
    *,
    limit: int = 500,
    opens: int = 0,
    groups: str = "",
    heading: str = "Start",
    anchor: str = "start",
) -> str:
    group_line = f"    resource_group_rowspans: [{groups}]\n" if groups else ""
    return f"""\
schema_version: 1
forbidden_open_summary_terms:
  zh-TW: [時間, 選修]
  en: [time, optional]
  zh-Hans: [时间, 选修]
pages:
  - id: sample
    canonical: page.md
    mirrors:
      en: page.en.md
      zh-Hans: page.zh-Hans.md
    max_visible_chars:
      zh-TW: {limit}
      en: {limit}
      zh-Hans: {limit}
    max_open_details: {opens}
    required_visible_sections:
      start:
        zh-TW: {{heading: {heading}, anchor: {anchor}}}
        en: {{heading: {heading}, anchor: {anchor}}}
        zh-Hans: {{heading: {heading}, anchor: {anchor}}}
{group_line}"""


def _run(body: str, *, config: str | None = None) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _copy_checker(root)
        (root / "scripts" / "reader-ux-pages.yml").write_text(
            config or _config(), encoding="utf-8"
        )
        for name in ("page.md", "page.en.md", "page.zh-Hans.md"):
            (root / name).write_text(_page(body), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(root / "scripts" / SCRIPT.name)],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return result.returncode, result.stdout + result.stderr


def test_closed_body_is_not_counted_but_summary_is() -> None:
    body = "<details markdown=\"1\">\n<summary>short label</summary>\n" + "x" * 800 + "\n</details>\n"
    rc, out = _run(body, config=_config(limit=80))
    assert rc == 0, out


def test_open_body_counts_as_visible() -> None:
    body = "<details markdown=\"1\" open>\n<summary>do it now</summary>\n" + "x" * 800 + "\n</details>\n"
    rc, out = _run(body, config=_config(limit=80, opens=1))
    assert rc == 1 and "visible characters" in out, out


def test_open_details_without_summary_still_counts_as_open() -> None:
    body = "<details open>\nthis block has no summary\n</details>\n"
    rc, out = _run(body, config=_config(opens=0))
    assert rc == 1 and "default-open" in out, out


def test_fenced_details_example_is_visible_code_not_a_real_disclosure() -> None:
    body = "```html\n<details>\n" + "x" * 800 + "\n</details>\n```\n"
    rc, out = _run(body, config=_config(limit=80))
    assert rc == 1 and "visible characters" in out, out


def test_html_comments_do_not_count_as_visible() -> None:
    body = "<!--\n" + "x" * 800 + "\n-->\nvisible\n"
    rc, out = _run(body, config=_config(limit=80))
    assert rc == 0, out


def test_visible_limit_is_blocking() -> None:
    rc, out = _run("x" * 800, config=_config(limit=80))
    assert rc == 1 and "visible characters" in out, out


def test_default_open_allowance_is_blocking() -> None:
    body = "<details open>\n<summary>do it now</summary>\nok\n</details>\n"
    rc, out = _run(body, config=_config(opens=0))
    assert rc == 1 and "default-open" in out, out


def test_open_optional_or_setup_content_is_forbidden() -> None:
    body = "<details open>\n<summary>選修：有時間再做</summary>\nok\n</details>\n"
    rc, out = _run(body, config=_config(opens=1))
    assert rc == 1 and "forbidden open summary" in out, out


def test_required_heading_inside_closed_details_is_not_visible() -> None:
    body = "<details>\n<summary>more</summary>\n## Needle\n</details>\n"
    rc, out = _run(body, config=_config(heading="Needle", anchor="needle"))
    assert rc == 1 and "required visible heading" in out, out


def test_required_heading_match_is_exact_not_a_substring() -> None:
    body = "## Deprecated Needle\n"
    rc, out = _run(body, config=_config(heading="Needle", anchor="needle"))
    assert rc == 1 and "required visible heading" in out, out


def test_required_anchor_must_match_heading_slug() -> None:
    rc, out = _run("ok", config=_config(anchor="old-start-anchor"))
    assert rc == 1 and "anchor is" in out, out


def test_missing_mirror_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _copy_checker(root)
        (root / "scripts" / "reader-ux-pages.yml").write_text(_config(), encoding="utf-8")
        (root / "page.md").write_text(_page("ok"), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(root / "scripts" / SCRIPT.name)],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    assert result.returncode == 1 and "missing page" in result.stdout, result.stdout


def test_accessible_resource_groups_pass() -> None:
    body = """\
<table>
<thead><tr><th scope="col">Group</th><th scope="col">Item</th></tr></thead>
<tbody><tr><th scope="rowgroup" rowspan="2">A</th><td>1</td></tr><tr><td>2</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">B</th><td>3</td></tr></tbody>
</table>
"""
    rc, out = _run(body, config=_config(groups="2, 1"))
    assert rc == 0, out


def test_wrong_resource_rowspans_fail() -> None:
    body = """\
<table>
<thead><tr><th scope="col">Group</th><th scope="col">Item</th></tr></thead>
<tbody><tr><th scope="rowgroup" rowspan="3">A</th><td>1</td></tr></tbody>
</table>
"""
    rc, out = _run(body, config=_config(groups="2"))
    assert rc == 1 and "rowspan='3'; expected 2" in out, out


def test_each_tbody_must_own_its_rowgroup_header() -> None:
    body = """\
<table>
<thead><tr><th scope="col">Group</th><th scope="col">Item</th></tr></thead>
<tbody><tr><th scope="rowgroup" rowspan="1">A</th><th scope="rowgroup" rowspan="1">B</th><td>1</td></tr></tbody>
<tbody><tr><td>2</td></tr></tbody>
</table>
"""
    rc, out = _run(body, config=_config(groups="1, 1"))
    assert rc == 1 and "must own exactly one rowgroup header" in out, out


def test_resource_table_inside_fence_cannot_satisfy_gate() -> None:
    body = """\
```html
<table>
<thead><tr><th scope="col">Group</th><th scope="col">Item</th></tr></thead>
<tbody><tr><th scope="rowgroup" rowspan="1">A</th><td>1</td></tr></tbody>
</table>
```
"""
    rc, out = _run(body, config=_config(limit=1000, groups="1"))
    assert rc == 1 and "rowgroup spans" in out, out


def test_resource_table_needs_scoped_column_headers() -> None:
    body = """\
<table>
<thead><tr><th>Group</th><th>Item</th></tr></thead>
<tbody><tr><th scope="rowgroup" rowspan="1">A</th><td>1</td></tr></tbody>
</table>
"""
    rc, out = _run(body, config=_config(groups="1"))
    assert rc == 1 and 'scope="col"' in out, out


def test_empty_locale_term_list_is_a_config_error() -> None:
    bad = _config().replace("  en: [time, optional]", "  en: []")
    rc, out = _run("ok", config=bad)
    assert rc == 2 and "config error" in out and "non-empty string list" in out, out


def test_non_mapping_page_is_a_controlled_config_error() -> None:
    bad = """\
schema_version: 1
forbidden_open_summary_terms:
  zh-TW: [時間]
  en: [time]
  zh-Hans: [时间]
pages: [not-a-mapping]
"""
    rc, out = _run("ok", config=bad)
    assert rc == 2 and "config error" in out and "must be a mapping" in out, out


def test_repo_passes_committed_ratchet() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=SCRIPT.parent.parent,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0, result.stdout + result.stderr


def _run_all() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except Exception as exc:  # noqa: BLE001 - standalone test runner
            failed += 1
            print(f"  FAIL  {test.__name__}: {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return failed


if __name__ == "__main__":
    raise SystemExit(1 if _run_all() else 0)

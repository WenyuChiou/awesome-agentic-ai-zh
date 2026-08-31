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
    details: int | None = None,
    forbidden: str = "",
    forbidden_include_code: bool = False,
    parity_urls: bool = False,
    parity_literals: str = "",
    parity_resource_ratings: bool = False,
    core_terms: bool = False,
    section_order: str = "",
    visible_min_links: int = 0,
    visible_min_ratings: int = 0,
) -> str:
    group_line = f"    resource_group_rowspans: [{groups}]\n" if groups else ""
    details_line = f"    required_details_count: {details}\n" if details is not None else ""
    forbidden_lines = ""
    if forbidden:
        forbidden_lines = f"""\
    forbidden_terms:
      zh-TW: [{forbidden}]
      en: [{forbidden}]
      zh-Hans: [{forbidden}]
"""
    include_code_line = (
        "    forbidden_terms_include_code: true\n" if forbidden_include_code else ""
    )
    parity_lines = ""
    if parity_urls or parity_literals or parity_resource_ratings:
        parity_lines = f"""\
    parity:
      ordered_external_urls: {str(parity_urls).lower()}
      resource_url_ratings: {str(parity_resource_ratings).lower()}
      literals: [{parity_literals}]
"""
    core_sections = ""
    core_config = ""
    order_line = (
        f"    visible_section_order: [{section_order}]\n" if section_order else ""
    )
    visible_minimum_lines = ""
    if visible_min_links or visible_min_ratings:
        minimum_values = ""
        if visible_min_links:
            minimum_values += f"        min_links: {visible_min_links}\n"
        if visible_min_ratings:
            minimum_values += f"        min_ratings: {visible_min_ratings}\n"
        visible_minimum_lines = (
            "    visible_section_minimums:\n"
            "      start:\n"
            f"{minimum_values}"
        )
    if core_terms:
        core_sections = """\
      core-terms:
        zh-TW: {heading: Core Terms, anchor: core-terms}
        en: {heading: Core Terms, anchor: core-terms}
        zh-Hans: {heading: Core Terms, anchor: core-terms}
      exercise-1:
        zh-TW: {heading: Exercise 1, anchor: exercise-1}
        en: {heading: Exercise 1, anchor: exercise-1}
        zh-Hans: {heading: Exercise 1, anchor: exercise-1}
"""
        core_config = """\
    core_terms:
      section_id: core-terms
      first_exercise_section_id: exercise-1
      min_definition_chars: 12
      terms:
        - id: token
          zh-TW: {term: Token, label: Token}
          en: {term: Token, label: Token}
          zh-Hans: {term: Token, label: Token}
        - id: context-window
          zh-TW: {term: Context Window, label: Context Window}
          en: {term: Context Window, label: Context Window}
          zh-Hans: {term: Context Window, label: Context Window}
"""
    return f"""\
schema_version: 1
forbidden_open_summary_terms:
  zh-TW: [時間, 選修]
  en: [time, optional]
  zh-Hans: [时间, 选修]
forbidden_closed_summary_terms:
  zh-TW: [必修閱讀, 學習資源]
  en: [required reading, learning resources]
  zh-Hans: [必读, 学习资源]
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
{details_line}{forbidden_lines}{include_code_line}{parity_lines}{order_line}{visible_minimum_lines}    required_visible_sections:
      start:
        zh-TW: {{heading: {heading}, anchor: {anchor}}}
        en: {{heading: {heading}, anchor: {anchor}}}
        zh-Hans: {{heading: {heading}, anchor: {anchor}}}
{core_sections}{core_config}{group_line}"""


def _run_locales(
    bodies: dict[str, str], *, config: str | None = None
) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _copy_checker(root)
        (root / "scripts" / "reader-ux-pages.yml").write_text(
            config or _config(), encoding="utf-8"
        )
        for name, body in bodies.items():
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


def _run(body: str, *, config: str | None = None) -> tuple[int, str]:
    return _run_locales(
        {name: body for name in ("page.md", "page.en.md", "page.zh-Hans.md")},
        config=config,
    )


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


def test_empty_compatibility_anchors_do_not_count_as_visible_text() -> None:
    anchors = "\n".join(
        f'<a id="legacy-deep-link-{index:03d}"></a>' for index in range(100)
    )
    rc, out = _run(anchors, config=_config(limit=80))
    assert rc == 0, out


def test_empty_anchor_literal_inside_fenced_code_still_counts() -> None:
    body = "```html\n" + '<a id="visible-code"></a>\n' * 8 + "```\n"
    rc, out = _run(body, config=_config(limit=80))
    assert rc == 1 and "visible characters" in out, out


def test_empty_anchor_literal_inside_inline_code_still_counts() -> None:
    body = " ".join(f'`<a id="visible-inline-{index}"></a>`' for index in range(8))
    rc, out = _run(body, config=_config(limit=80))
    assert rc == 1 and "visible characters" in out, out


def test_anchor_text_that_readers_can_see_still_counts() -> None:
    body = '<a id="visible-link">' + "x" * 100 + "</a>"
    rc, out = _run(body, config=_config(limit=80))
    assert rc == 1 and "visible characters" in out, out


def test_visible_limit_is_blocking() -> None:
    rc, out = _run("x" * 800, config=_config(limit=80))
    assert rc == 1 and "visible characters" in out, out


def test_default_open_allowance_is_blocking() -> None:
    body = "<details open>\n<summary>do it now</summary>\nok\n</details>\n"
    rc, out = _run(body, config=_config(opens=0))
    assert rc == 1 and "default-open" in out, out


def test_required_details_count_is_blocking() -> None:
    body = "<details>\n<summary>one</summary>\nok\n</details>\n"
    rc, out = _run(body, config=_config(details=2))
    assert rc == 1 and "1 details block(s); expected 2" in out, out


def test_forbidden_page_term_is_blocking() -> None:
    rc, out = _run("obsolete-setting", config=_config(forbidden="obsolete-setting"))
    assert rc == 1 and "forbidden term" in out, out


def test_forbidden_term_inside_fenced_example_is_ignored() -> None:
    rc, out = _run(
        "```text\nobsolete-setting\n```\n",
        config=_config(forbidden="obsolete-setting", limit=1000),
    )
    assert rc == 0, out


def test_forbidden_term_inside_fenced_example_blocks_when_enabled() -> None:
    rc, out = _run(
        "```text\nobsolete-setting\n```\n",
        config=_config(
            forbidden="obsolete-setting", forbidden_include_code=True, limit=1000
        ),
    )
    assert rc == 1 and "forbidden term" in out, out


def test_ordered_external_url_parity_is_blocking() -> None:
    rc, out = _run_locales(
        {
            "page.md": "https://example.com/a https://example.com/b",
            "page.en.md": "https://example.com/b https://example.com/a",
            "page.zh-Hans.md": "https://example.com/a https://example.com/b",
        },
        config=_config(parity_urls=True),
    )
    assert rc == 1 and "ordered external URLs differ" in out, out


def test_exact_literal_parity_is_blocking() -> None:
    rc, out = _run_locales(
        {
            "page.md": "run --read-only",
            "page.en.md": "run --read-only",
            "page.zh-Hans.md": "run normally",
        },
        config=_config(parity_literals="--read-only"),
    )
    assert rc == 1 and "parity literal '--read-only'" in out, out


def _rated_resource_table(first_rating: str, second_rating: str) -> str:
    return f"""\
<table>
<thead><tr><th scope="col">Group</th><th scope="col">Resource</th><th scope="col">Rating</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="2">A</th><td><a href="https://example.com/a">A</a></td><td>{first_rating}</td></tr>
<tr><td><a href="https://example.com/b">B</a></td><td>{second_rating}</td></tr>
</tbody>
</table>
"""


def test_resource_url_rating_parity_passes() -> None:
    body = _rated_resource_table("⭐⭐⭐⭐", "⭐⭐⭐")
    rc, out = _run(
        body,
        config=_config(groups="2", parity_urls=True, parity_resource_ratings=True),
    )
    assert rc == 0, out


def test_swapped_resource_ratings_fail_even_when_urls_and_totals_match() -> None:
    rc, out = _run_locales(
        {
            "page.md": _rated_resource_table("⭐⭐⭐⭐", "⭐⭐⭐"),
            "page.en.md": _rated_resource_table("⭐⭐⭐", "⭐⭐⭐⭐"),
            "page.zh-Hans.md": _rated_resource_table("⭐⭐⭐⭐", "⭐⭐⭐"),
        },
        config=_config(groups="2", parity_urls=True, parity_resource_ratings=True),
    )
    assert rc == 1 and "resource URL/rating pairs differ" in out, out


def _core_terms_body(*, intro: str = "", swap: bool = False, short: bool = False) -> str:
    definitions = [
        "### **Token**\nA small text piece that the model reads and counts.",
        "### **Context Window**\nThe model's desk: everything for this turn must fit on it.",
    ]
    if swap:
        definitions.reverse()
    if short:
        definitions[0] = "### **Token**\ntiny"
    return (
        intro
        + "\n## Core Terms\n\n"
        + "\n\n".join(definitions)
        + "\n\n## Exercise 1\n\nRun the example.\n"
    )


def test_visible_bold_ordered_core_terms_pass() -> None:
    rc, out = _run(_core_terms_body(), config=_config(limit=2000, core_terms=True))
    assert rc == 0, out


def test_visible_html_strong_ordered_core_terms_pass() -> None:
    body = _core_terms_body().replace("**Token**", "<strong>Token</strong>").replace(
        "**Context Window**", "<strong>Context Window</strong>"
    )
    rc, out = _run(body, config=_config(limit=2000, core_terms=True))
    assert rc == 0, out


def test_fenced_heading_does_not_truncate_core_term_section() -> None:
    body = (
        "## Core Terms\n\n```markdown\n## Setup\n```\n\n"
        "### **Token**\nA small text piece that the model reads and counts.\n\n"
        "### **Context Window**\nThe model's desk: everything for this turn must fit on it.\n\n"
        "## Exercise 1\n\nRun the example.\n"
    )
    rc, out = _run(body, config=_config(limit=2000, core_terms=True))
    assert rc == 0, out


def test_fenced_configured_headings_do_not_shadow_real_sections() -> None:
    body = (
        "```markdown\n## Core Terms\n## Exercise 1\n```\n\n"
        "## Core Terms\n\n"
        "### **Token**\nA small text piece that the model reads and counts.\n\n"
        "### **Context Window**\nThe model's desk: everything for this turn must fit on it.\n\n"
        "## Exercise 1\n\nRun the example.\n"
    )
    rc, out = _run(body, config=_config(limit=2000, core_terms=True))
    assert rc == 0, out


def test_first_visible_core_term_use_must_be_bold() -> None:
    rc, out = _run(
        _core_terms_body(intro="Token is useful."),
        config=_config(limit=2000, core_terms=True),
    )
    assert rc == 1 and "first visible use of core term 'Token' must be bold" in out, out


def test_longer_word_does_not_count_as_core_term_first_use() -> None:
    rc, out = _run(
        _core_terms_body(intro="A Tokenizer splits text."),
        config=_config(limit=2000, core_terms=True),
    )
    assert rc == 0, out


def test_ascii_core_term_next_to_cjk_still_counts_as_first_use() -> None:
    rc, out = _run(
        _core_terms_body(intro="Token是模型讀寫文字的小單位。"),
        config=_config(limit=2000, core_terms=True),
    )
    assert rc == 1 and "first visible use of core term 'Token' must be bold" in out, out


def test_only_the_actual_page_title_h1_is_exempt() -> None:
    rc, out = _run(
        _core_terms_body(intro="# Token topic"),
        config=_config(limit=2000, core_terms=True),
    )
    assert rc == 1 and "first visible use of core term 'Token' must be bold" in out, out


def test_html_tag_attributes_do_not_count_as_visible_term_use() -> None:
    rc, out = _run(
        _core_terms_body(intro='<span data-name="Token">Open this panel.</span>'),
        config=_config(limit=2000, core_terms=True),
    )
    assert rc == 0, out


def test_core_term_definition_order_is_blocking() -> None:
    rc, out = _run(
        _core_terms_body(swap=True),
        config=_config(limit=2000, core_terms=True),
    )
    assert rc == 1 and "definition labels are not in configured order" in out, out


def test_core_term_needs_a_real_explanation() -> None:
    rc, out = _run(
        _core_terms_body(short=True),
        config=_config(limit=2000, core_terms=True),
    )
    assert rc == 1 and "explanation characters" in out, out


def test_empty_core_section_cannot_borrow_definitions_from_later_section() -> None:
    body = (
        "## Core Terms\n\n## Setup\n\n"
        "### **Token**\nA small text piece that the model reads and counts.\n\n"
        "### **Context Window**\nThe model's desk: everything for this turn must fit on it.\n\n"
        "## Exercise 1\n\nRun the example.\n"
    )
    rc, out = _run(body, config=_config(limit=2000, core_terms=True))
    assert rc == 1 and "needs visible bold definition label" in out, out


def test_final_core_term_cannot_borrow_explanation_from_setup_section() -> None:
    body = (
        "## Core Terms\n\n"
        "### **Token**\nA small text piece that the model reads and counts.\n\n"
        "### **Context Window**\n\n"
        "## Setup\n\nThis later setup paragraph is long but is not a definition.\n\n"
        "## Exercise 1\n\nRun the example.\n"
    )
    rc, out = _run(body, config=_config(limit=2000, core_terms=True))
    assert rc == 1 and "core term 'Context Window' has only 0 explanation" in out, out


def test_core_terms_must_appear_before_first_exercise() -> None:
    body = (
        "## Exercise 1\n\nRun the example.\n\n## Core Terms\n\n"
        "### **Token**\nA small text piece that the model reads and counts.\n\n"
        "### **Context Window**\nThe model's desk: everything for this turn must fit on it.\n"
    )
    rc, out = _run(body, config=_config(limit=2000, core_terms=True))
    assert rc == 1 and "core terms section must appear before the first exercise" in out, out


def test_core_terms_cannot_hide_inside_closed_details() -> None:
    body = (
        '<details markdown="1">\n<summary>More</summary>\n## Core Terms\n\n'
        "### **Token**\nA small text piece that the model reads and counts.\n\n"
        "### **Context Window**\nThe model's desk: everything for this turn must fit on it.\n"
        "</details>\n\n## Exercise 1\n\nRun the example.\n"
    )
    rc, out = _run(body, config=_config(limit=2000, core_terms=True))
    assert rc == 1 and "required visible heading 'core-terms'" in out, out


def test_one_locale_cannot_swap_core_term_order() -> None:
    rc, out = _run_locales(
        {
            "page.md": _core_terms_body(),
            "page.en.md": _core_terms_body(swap=True),
            "page.zh-Hans.md": _core_terms_body(),
        },
        config=_config(limit=2000, core_terms=True),
    )
    assert rc == 1 and "sample/en" in out and "definition labels" in out, out


def test_open_optional_or_setup_content_is_forbidden() -> None:
    body = "<details open>\n<summary>選修：有時間再做</summary>\nok\n</details>\n"
    rc, out = _run(body, config=_config(opens=1))
    assert rc == 1 and "forbidden open summary" in out, out


def test_required_learning_content_cannot_hide_in_closed_details() -> None:
    body = (
        "<details>\n"
        "<summary>Required reading and learning resources</summary>\n"
        "[Official guide](https://example.com)\n"
        "</details>\n"
    )
    rc, out = _run(body)
    assert rc == 1 and "forbidden closed summary" in out, out


def test_open_required_reading_inside_closed_parent_is_still_hidden() -> None:
    body = (
        "<details>\n"
        "<summary>More</summary>\n"
        "<details open>\n"
        "<summary>Required reading</summary>\n"
        "[Official guide](https://example.com)\n"
        "</details>\n"
        "</details>\n"
    )
    rc, out = _run(body)
    assert rc == 1 and "forbidden closed summary" in out, out


def test_schema_v1_config_without_closed_summary_terms_remains_compatible() -> None:
    config = _config().replace(
        "forbidden_closed_summary_terms:\n"
        "  zh-TW: [必修閱讀, 學習資源]\n"
        "  en: [required reading, learning resources]\n"
        "  zh-Hans: [必读, 学习资源]\n",
        "",
    )
    rc, out = _run("<details>\n<summary>Required reading</summary>\n</details>\n", config=config)
    assert rc == 0, out


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


def test_required_visible_section_order_is_blocking() -> None:
    body = (
        "## Exercise 1\n\nRun it.\n\n"
        "## Core Terms\n\n"
        "### **Token**\nA small text piece that the model reads and counts.\n\n"
        "### **Context Window**\nThe model's desk: everything for this turn must fit on it.\n"
    )
    rc, out = _run(
        body,
        config=_config(
            limit=2000,
            core_terms=True,
            section_order="start, core-terms, exercise-1",
        ),
    )
    assert rc == 1 and "required visible sections are out of order" in out, out


def test_visible_section_minimums_ignore_links_hidden_in_details() -> None:
    body = (
        '<details markdown="1">\n<summary>More sources</summary>\n'
        '[Hidden project](https://example.com) ⭐⭐⭐⭐⭐\n</details>\n'
    )
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out
    assert "visible section 'start' has 0 rating(s)" in out, out


def test_visible_section_minimums_accept_visible_link_and_rating() -> None:
    body = (
        '[Starter project](https://example.com) ⭐⭐⭐⭐⭐\n\n'
        '<details markdown="1">\n<summary>More sources</summary>\nHidden\n</details>\n'
    )
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 0, out


def test_visible_section_minimums_accept_code_style_link_label() -> None:
    body = "[`starter-project`](https://example.com) ⭐⭐⭐⭐⭐\n"
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 0, out


def test_visible_section_minimums_accept_visible_html_link_and_rating() -> None:
    body = '<table><tr><td><a href="https://example.com">Starter</a></td><td>⭐⭐⭐⭐⭐</td></tr></table>\n'
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 0, out


def test_visible_section_minimums_do_not_count_images_as_links() -> None:
    body = "![Project map ⭐⭐⭐⭐⭐](project-map.png)\n"
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out
    assert "visible section 'start' has 0 rating(s)" in out, out


def test_visible_section_minimums_ignore_fenced_code() -> None:
    body = (
        "```markdown\n"
        "[Fake project](https://example.com) ⭐⭐⭐⭐⭐\n"
        '<a href="https://example.com/html">Fake HTML project</a>\n'
        "```\n"
    )
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out
    assert "visible section 'start' has 0 rating(s)" in out, out


def test_visible_section_minimums_ignore_indented_code() -> None:
    body = "    [Fake project](https://example.com) ⭐⭐⭐⭐⭐\n"
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out
    assert "visible section 'start' has 0 rating(s)" in out, out


def test_visible_section_minimums_ignore_inline_code() -> None:
    body = "`[Fake project](https://example.com) ⭐⭐⭐⭐⭐`\n"
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out
    assert "visible section 'start' has 0 rating(s)" in out, out


def test_visible_section_minimums_ignore_raw_html_code() -> None:
    body = '<code><a href="https://example.com">Fake project</a> ⭐⭐⭐⭐⭐</code>\n'
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out
    assert "visible section 'start' has 0 rating(s)" in out, out


def test_visible_section_minimums_ignore_html_attributes() -> None:
    body = '<img alt="[Fake project](map.png) ⭐⭐⭐⭐⭐" src="map.png">\n'
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out
    assert "visible section 'start' has 0 rating(s)" in out, out


def test_visible_section_minimums_ignore_hidden_html_entry() -> None:
    body = '<span hidden><a href="https://example.com">Fake</a> ⭐⭐⭐⭐⭐</span>\n'
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out
    assert "visible section 'start' has 0 rating(s)" in out, out


def test_visible_section_minimums_keep_nested_hidden_stack_balanced() -> None:
    body = (
        '<span hidden><span>x</span><a href="https://example.com">Fake</a> '
        "⭐⭐⭐⭐⭐</span>\n"
    )
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out
    assert "visible section 'start' has 0 rating(s)" in out, out


def test_visible_section_minimums_hidden_void_does_not_hide_following_entry() -> None:
    body = '<input hidden><a href="https://example.com">Real</a> ⭐⭐⭐⭐⭐\n'
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 0, out


def test_visible_section_minimums_ignore_fragment_only_link() -> None:
    body = "[Jump to setup](#setup) ⭐⭐⭐⭐⭐\n"
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1),
    )
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out


def test_visible_section_minimums_ignore_escaped_link_syntax() -> None:
    body = r"\[Fake project](https://example.com)" + " ⭐⭐⭐⭐⭐\n"
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1),
    )
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out


def test_visible_section_minimums_ignore_rating_in_link_destination() -> None:
    body = "[Starter project](https://example.com/⭐⭐⭐⭐⭐)\n"
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 1 and "visible section 'start' has 0 rating(s)" in out, out
    assert "visible section 'start' has 0 link(s)" not in out, out


def test_visible_section_minimums_accept_reference_link() -> None:
    body = (
        "[Starter project][project] ⭐⭐⭐⭐⭐\n\n"
        "## Later section\n\n"
        "[project]: https://example.com\n"
    )
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 0, out


def test_visible_section_minimums_ignore_reference_definition_in_pre() -> None:
    body = (
        "[Starter project][project] ⭐⭐⭐⭐⭐\n\n"
        "## Later section\n\n"
        "<pre>\n[project]: https://example.com\n</pre>\n"
    )
    rc, out = _run(body, config=_config(limit=2000, visible_min_links=1))
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out


def test_visible_section_minimums_ignore_reference_definition_in_hidden_html() -> None:
    body = (
        "[Starter project][project] ⭐⭐⭐⭐⭐\n\n"
        "## Later section\n\n"
        '<div hidden>\n[project]: https://example.com\n</div>\n'
    )
    rc, out = _run(body, config=_config(limit=2000, visible_min_links=1))
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out


def test_visible_section_minimums_accept_autolink() -> None:
    body = "<https://example.com> ⭐⭐⭐⭐⭐\n"
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 0, out


def test_visible_section_minimums_avoid_existing_wrapper_id_collision() -> None:
    body = (
        "No resource here.\n\n"
        "## Later section\n\n"
        '<div id="reader-ux-visible-section">'
        '<a href="https://example.com">Fake</a> ⭐⭐⭐⭐⭐</div>\n'
    )
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out
    assert "visible section 'start' has 0 rating(s)" in out, out


def test_visible_section_minimums_avoid_entity_encoded_wrapper_id_collision() -> None:
    body = (
        "No resource here.\n\n"
        "## Later section\n\n"
        '<div id="reader-ux-visible&#45;section">'
        '<a href="https://example.com">Fake</a> ⭐⭐⭐⭐⭐</div>\n'
    )
    rc, out = _run(
        body,
        config=_config(limit=2000, visible_min_links=1, visible_min_ratings=1),
    )
    assert rc == 1 and "visible section 'start' has 0 link(s)" in out, out
    assert "visible section 'start' has 0 rating(s)" in out, out


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
forbidden_closed_summary_terms:
  zh-TW: [必修閱讀]
  en: [required reading]
  zh-Hans: [必读]
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

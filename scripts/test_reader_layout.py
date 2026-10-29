"""Keep compact catalogs complete and mobile field labels readable."""

from html import unescape
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("entry", "identity", "use", "status", "limits")
ROLE_LAYOUTS = {
    "developer": ((4, 6, 2, 2), ("entry", "identity", "surface", "use", "status")),
    "researcher": ((3, 4, 5, 2, 1), ("entry", "use", "status", "limits")),
    "teacher": ((3, 3, 3, 3), ("entry", "use", "status", "limits")),
    "knowledge-worker": ((4, 4, 2, 3, 2), ("entry", "use", "status", "limits")),
}


def compact_catalog(
    text: str,
    group_sizes: tuple[int, ...] = (4, 8, 4, 4, 2, 1),
    field_names: tuple[str, ...] = FIELDS,
) -> str:
    match = re.search(
        r'<div class="reader-resource-catalog" role="region" tabindex="0" '
        r'aria-label="[^"]+">\s*(<table align="center">.*?</table>)\s*</div>', text, re.S,
    )
    assert match, "Missing named, keyboard-focusable catalog region"
    table = match[1]
    assert len(re.findall(r'<th scope="col">', table)) == 5
    assert "<details" not in table, "Resource facts must stay visible"
    groups = re.findall(r"<tbody>(.*?)</tbody>", table, re.S)
    assert len(groups) == len(group_sizes)
    for group, count in zip(groups, group_sizes):
        assert f'scope="rowgroup" rowspan="{count}"' in group
        rows = re.findall(r"<tr>(.*?)</tr>", group, re.S)
        assert len(rows) == count
        for row in rows:
            assert len(re.findall(r"<td\b[^>]*>", row)) == 4
            fields = re.findall(r'<div data-field="([^"]+)">(.*?)</div>', row, re.S)
            assert tuple(name for name, _ in fields) == field_names
            for name, value in fields:
                if name != "entry":
                    assert "⭐" not in value, "Rating duplicated into resource facts"
                if name in ("identity", "surface") and "surface" in field_names:
                    assert re.match(r"<strong>[^<]+</strong>", value)
                    value = re.sub(r"^<strong>[^<]+</strong>\s*", "", value)
                assert re.sub(r"<[^>]+>", "", value).strip(), f"Empty {name}"
            entry = fields[0][1]
            assert "<strong><a href=" in entry
            assert re.search(r'<td\b[^>]*><span data-field="rating">⭐{3,5}</span></td>', row)
            label = re.search(r'<a href="https://github.com/[^"]+">(.*?)</a>', entry)
            if label and ("surface" in field_names or "identity" not in field_names):
                assert "/" not in label[1], "Repository labels must omit the owner prefix"
                assert "<br>" not in label[1], "Repository labels must not force a line break"
    return table


@pytest.mark.parametrize("role", ROLE_LAYOUTS)
@pytest.mark.parametrize("suffix", ("", ".en", ".zh-Hans"))
def test_role_catalogs_are_complete_grouped_and_visible(role: str, suffix: str) -> None:
    group_sizes, field_names = ROLE_LAYOUTS[role]
    text = (ROOT / f"branches/for-{role}{suffix}.md").read_text(encoding="utf-8")
    table = compact_catalog(text, group_sizes, field_names)
    assert len(re.findall(r'<div data-field="entry">', table)) == sum(group_sizes)
    assert len(re.findall(r'<a href="', table)) == sum(group_sizes)
    prefix = text[:text.index(table)]
    assert prefix.count("<details") == prefix.count("</details>")
    assert "## ⭐" in prefix
    visible = re.sub(r"<details\b.*?</details>", "", text, flags=re.S)
    assert table in visible, "Important resource fields were collapsed"


@pytest.mark.parametrize(
    ("role", "field"),
    [(role, field) for role, (_, fields) in ROLE_LAYOUTS.items() for field in fields[1:]],
)
def test_role_catalog_rejects_a_dropped_field(role: str, field: str) -> None:
    group_sizes, field_names = ROLE_LAYOUTS[role]
    text = (ROOT / f"branches/for-{role}.md").read_text(encoding="utf-8")
    changed, count = re.subn(rf'<div data-field="{field}">.*?</div>', "", text, count=1, flags=re.S)
    assert count == 1
    with pytest.raises(AssertionError):
        compact_catalog(changed, group_sizes, field_names)


@pytest.mark.parametrize("role", ROLE_LAYOUTS)
def test_role_catalog_rejects_a_rating_copied_into_status(role: str) -> None:
    group_sizes, field_names = ROLE_LAYOUTS[role]
    text = (ROOT / f"branches/for-{role}.md").read_text(encoding="utf-8")
    changed, count = re.subn(
        r'(<div data-field="status">.*?)</div>', r'\1 ⭐⭐⭐⭐⭐</div>', text, count=1, flags=re.S,
    )
    assert count == 1
    with pytest.raises(AssertionError, match="Rating duplicated"):
        compact_catalog(changed, group_sizes, field_names)


@pytest.mark.parametrize("role", ROLE_LAYOUTS)
@pytest.mark.parametrize("mutation", ("owner", "break"))
def test_role_catalog_rejects_owner_prefixes_and_forced_breaks(role: str, mutation: str) -> None:
    group_sizes, field_names = ROLE_LAYOUTS[role]
    text = (ROOT / f"branches/for-{role}.md").read_text(encoding="utf-8")
    pattern = r'(<div data-field="entry"><strong><a href="https://github.com/([^"/]+)/([^"/]+)">)([^<]+)(</a>)'
    def inject(match: re.Match[str]) -> str:
        label = f"{match[2]}/{match[4]}" if mutation == "owner" else f"{match[4]}<br>"
        return f"{match[1]}{label}{match[5]}"
    changed, count = re.subn(pattern, inject, text, count=1)
    assert count == 1
    error = "omit the owner prefix" if mutation == "owner" else "force a line break"
    with pytest.raises(AssertionError, match=error):
        compact_catalog(changed, group_sizes, field_names)


@pytest.mark.parametrize("role", ROLE_LAYOUTS)
def test_role_catalog_mirrors_keep_urls_ratings_and_group_order(role: str) -> None:
    group_sizes, field_names = ROLE_LAYOUTS[role]
    observations = []
    for suffix in ("", ".en", ".zh-Hans"):
        text = (ROOT / f"branches/for-{role}{suffix}.md").read_text(encoding="utf-8")
        table = compact_catalog(text, group_sizes, field_names)
        observations.append((
            re.findall(r'<a href="([^"]+)"', table),
            re.findall(r'<span data-field="rating">(⭐+)</span>', table),
            re.findall(r'rowspan="(\d+)"', table),
        ))
    assert observations[0] == observations[1] == observations[2]


@pytest.mark.parametrize(
    ("suffix", "identity", "surface"),
    (("", "核心身分：", "主要 Surface："),
     (".en", "Core identity:", "Main Surface:"),
     (".zh-Hans", "核心身份：", "主要 Surface：")),
)
def test_developer_identity_and_surface_are_visibly_distinct(
    suffix: str, identity: str, surface: str,
) -> None:
    text = (ROOT / f"branches/for-developer{suffix}.md").read_text(encoding="utf-8")
    assert text.count(f'<div data-field="identity"><strong>{identity}</strong>') == 14
    assert text.count(f'<div data-field="surface"><strong>{surface}</strong>') == 14


@pytest.mark.parametrize("suffix", ("", ".en", ".zh-Hans"))
def test_everyday_catalog_is_compact_complete_and_visible(suffix: str) -> None:
    text = (ROOT / f"branches/for-everyday-users{suffix}.md").read_text(encoding="utf-8")
    table = compact_catalog(text)
    assert len(re.findall(r'<div data-field="entry">', table)) == 23
    assert len(re.findall(r'<a href="', table)) == 23
    assert text.index("## ⭐") < text.index(table) < text.index("<details", text.index(table))


@pytest.mark.parametrize("field", ("identity", "use", "status", "limits"))
def test_compact_catalog_rejects_losing_an_original_field(field: str) -> None:
    text = (ROOT / "branches/for-everyday-users.md").read_text(encoding="utf-8")
    changed, count = re.subn(rf'<div data-field="{field}">.*?</div>', "", text, count=1, flags=re.S)
    assert count == 1
    with pytest.raises(AssertionError):
        compact_catalog(changed)


def test_english_researcher_category_keeps_short_equivalent_words() -> None:
    text = (ROOT / "branches/for-researcher.en.md").read_text(encoding="utf-8")
    table = compact_catalog(text, *ROLE_LAYOUTS["researcher"])
    assert 'rowspan="5" align="center" valign="middle" width="80">Repeatable research and evidence</th>' in table
    assert ">Reproducibility and evidence</th>" not in table


def test_english_model_labels_keep_short_equivalent_names() -> None:
    text = (ROOT / "stages/01-llm-basics.en.md").read_text(encoding="utf-8")
    tables = re.findall(r'<table data-model-family="[^"]+" align="center">(.*?)</table>', text, re.S)
    assert len(tables) == 18
    for table in tables:
        for field, label in (("models", "Models"), ("limits", "Limits")):
            body = re.search(rf'<tbody data-field="{field}">(.*?)</tbody>', table, re.S)
            assert body
            header = re.search(r"<th[^>]*>(.*?)</th>", body[1], re.S)
            assert header and unescape(header[1]) == label


def test_layout_rules_do_not_shrink_or_hide_important_content() -> None:
    css = (ROOT / "docs/stylesheets/extra.css").read_text(encoding="utf-8")
    assert '.md-typeset .reader-resource-catalog' in css
    assert 'table-layout: fixed' in css
    assert 'outline: 2px solid var(--md-accent-fg-color)' in css
    labels = re.findall(
        r'\.md-typeset details\.model-family table\[data-model-family\] th \{([^}]+)\}', css,
    )
    assert labels and "overflow-wrap: normal" in labels[-1]
    assert "word-break: normal" in labels[-1]
    assert ".reader-resource-catalog .md-typeset__scrollwrap" in css
    assert ".reader-resource-catalog .md-typeset__table" in css
    catalog_rules = css[css.index("/* Resource facts stay visible"):css.index("/* Stage 0: grouped definitions")]
    assert "display: none" not in catalog_rules
    assert catalog_rules.count("white-space: nowrap") == 1
    assert ".reader-resource-catalog td:nth-of-type(2)" in catalog_rules


def test_phone_catalogs_use_full_width_instead_of_a_category_column() -> None:
    css = (ROOT / "docs/stylesheets/extra.css").read_text(encoding="utf-8")
    phone = css[css.index("/* Phone catalogs: category heading, then full-width resources. */"):]
    assert "@media (max-width: 900px)" in phone
    for selector in ("table:not([class])", "tbody", "tr", 'th[scope="rowgroup"]', "td"):
        assert f".reader-resource-catalog {selector}" in phone
    assert "display: block" in phone and "inline-size: 100%" in phone
    assert "box-sizing: border-box" in phone
    assert "clip-path: inset(50%)" in phone  # column labels remain accessible
    assert 'div[data-field="identity"]' in phone and "font-size: inherit" in phone
    assert "width: 29%" not in phone
    assert "display: none" not in phone


def test_centered_markdown_table_renders_cells_links_and_alignment() -> None:
    """The docs renderer must parse wrapped Markdown and keep its content."""
    import xml.etree.ElementTree as ET

    import markdown

    source = (
        '<div align="center" markdown="1">\n\n'
        '| Description | Resource | Rating |\n'
        '|:---|---:|:---:|\n'
        '| Plain explanation | [Project](https://example.org/project) | ⭐⭐⭐⭐ |\n'
        '| Another explanation | Source | ⭐⭐⭐⭐⭐ |\n\n'
        '</div>\n'
    )
    rendered = markdown.markdown(source, extensions=["tables", "md_in_html"])
    root = ET.fromstring(rendered)
    assert root.tag == "div" and root.attrib["align"] == "center"
    table = root.find("table")
    assert table is not None and "| Description |" not in rendered
    headers = table.findall("./thead/tr/th")
    assert [h.text for h in headers] == ["Description", "Resource", "Rating"]
    assert [h.attrib.get("style") for h in headers] == [
        "text-align: left;", "text-align: right;", "text-align: center;",
    ]
    rows = table.findall("./tbody/tr")
    assert [["".join(c.itertext()) for c in row.findall("td")] for row in rows] == [
        ["Plain explanation", "Project", "⭐⭐⭐⭐"],
        ["Another explanation", "Source", "⭐⭐⭐⭐⭐"],
    ]
    assert rows[0].find("./td/a").attrib["href"] == "https://example.org/project"


@pytest.mark.parametrize("suffix", ("", ".en", ".zh-Hans"))
def test_stage07_explanations_are_left_aligned_and_deploy_is_bold(suffix: str) -> None:
    import markdown

    text = (ROOT / f"stages/07-multi-agent-production{suffix}.md").read_text(encoding="utf-8")
    # Preserve the reported Chinese flanking regression without guessing bold pairs.
    assert "**Deploy（部署）**是" not in text
    rendered = markdown.markdown(text, extensions=["extra"])
    assert re.search(r"<strong>Deploy(?:（部署）)?</strong>", rendered)
    assert "|---:|" not in text  # the stage order is explanatory text, not a numeric measure

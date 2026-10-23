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
        r'aria-label="[^"]+">\s*(<table>.*?</table>)\s*</div>', text, re.S,
    )
    assert match, "Missing named, keyboard-focusable catalog region"
    table = match[1]
    assert len(re.findall(r'<th scope="col">', table)) == 2
    assert "<details" not in table, "Resource facts must stay visible"
    groups = re.findall(r"<tbody>(.*?)</tbody>", table, re.S)
    assert len(groups) == len(group_sizes)
    for group, count in zip(groups, group_sizes):
        assert f'scope="rowgroup" rowspan="{count}"' in group
        rows = re.findall(r"<tr>(.*?)</tr>", group, re.S)
        assert len(rows) == count
        for row in rows:
            assert row.count("<td>") == 1
            fields = re.findall(r'<p data-field="([^"]+)">(.*?)</p>', row, re.S)
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
            assert re.search(r'<span data-field="rating">⭐{3,5}</span>', entry)
            label = re.search(r'<a href="https://github.com/[^"]+">(.*?)</a>', entry)
            if label and ("surface" in field_names or "identity" not in field_names):
                plain = label[1].replace("<br>", "")
                if len(plain) > 14 and re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", plain):
                    owner, repo = plain.split("/", 1)
                    assert label[1] == f"{owner}/<br>{repo}", "Long repository label needs a native line break"
    return table


@pytest.mark.parametrize("role", ROLE_LAYOUTS)
@pytest.mark.parametrize("suffix", ("", ".en", ".zh-Hans"))
def test_role_catalogs_are_complete_grouped_and_visible(role: str, suffix: str) -> None:
    group_sizes, field_names = ROLE_LAYOUTS[role]
    text = (ROOT / f"branches/for-{role}{suffix}.md").read_text(encoding="utf-8")
    table = compact_catalog(text, group_sizes, field_names)
    assert len(re.findall(r'<p data-field="entry">', table)) == sum(group_sizes)
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
    changed, count = re.subn(rf'<p data-field="{field}">.*?</p>', "", text, count=1, flags=re.S)
    assert count == 1
    with pytest.raises(AssertionError):
        compact_catalog(changed, group_sizes, field_names)


@pytest.mark.parametrize("role", ROLE_LAYOUTS)
def test_role_catalog_rejects_a_rating_copied_into_status(role: str) -> None:
    group_sizes, field_names = ROLE_LAYOUTS[role]
    text = (ROOT / f"branches/for-{role}.md").read_text(encoding="utf-8")
    changed, count = re.subn(
        r'(<p data-field="status">.*?)</p>', r'\1 ⭐⭐⭐⭐⭐</p>', text, count=1, flags=re.S,
    )
    assert count == 1
    with pytest.raises(AssertionError, match="Rating duplicated"):
        compact_catalog(changed, group_sizes, field_names)


@pytest.mark.parametrize("role", ROLE_LAYOUTS)
def test_role_catalog_rejects_removing_long_repo_name_break(role: str) -> None:
    group_sizes, field_names = ROLE_LAYOUTS[role]
    text = (ROOT / f"branches/for-{role}.md").read_text(encoding="utf-8")
    changed, count = re.subn(r"/<br>", "/", text, count=1)
    assert count == 1
    with pytest.raises(AssertionError, match="native line break"):
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
    assert text.count(f'<p data-field="identity"><strong>{identity}</strong>') == 14
    assert text.count(f'<p data-field="surface"><strong>{surface}</strong>') == 14


@pytest.mark.parametrize("suffix", ("", ".en", ".zh-Hans"))
def test_everyday_catalog_is_compact_complete_and_visible(suffix: str) -> None:
    text = (ROOT / f"branches/for-everyday-users{suffix}.md").read_text(encoding="utf-8")
    table = compact_catalog(text)
    assert len(re.findall(r'<p data-field="entry">', table)) == 23
    assert len(re.findall(r'<a href="', table)) == 23
    assert text.index("## ⭐") < text.index(table) < text.index("<details", text.index(table))


@pytest.mark.parametrize("field", ("identity", "use", "status", "limits"))
def test_compact_catalog_rejects_losing_an_original_field(field: str) -> None:
    text = (ROOT / "branches/for-everyday-users.md").read_text(encoding="utf-8")
    changed, count = re.subn(rf'<p data-field="{field}">.*?</p>', "", text, count=1, flags=re.S)
    assert count == 1
    with pytest.raises(AssertionError):
        compact_catalog(changed)


def test_english_researcher_category_keeps_short_equivalent_words() -> None:
    text = (ROOT / "branches/for-researcher.en.md").read_text(encoding="utf-8")
    table = compact_catalog(text, *ROLE_LAYOUTS["researcher"])
    assert 'rowspan="5">Repeatable research and evidence</th>' in table
    assert ">Reproducibility and evidence</th>" not in table


def test_english_model_labels_keep_short_equivalent_names() -> None:
    text = (ROOT / "stages/01-llm-basics.en.md").read_text(encoding="utf-8")
    tables = re.findall(r'<table data-model-family="[^"]+">(.*?)</table>', text, re.S)
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
    catalog_rules = css[css.index("/* Resource facts stay visible"):]
    assert "display: none" not in catalog_rules
    assert "white-space: nowrap" not in catalog_rules

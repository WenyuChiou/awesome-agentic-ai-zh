"""Keep compact catalogs complete and mobile field labels readable."""

from html import unescape
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("entry", "identity", "use", "status", "limits")


def compact_catalog(text: str) -> str:
    match = re.search(
        r'<div class="reader-resource-catalog" role="region" tabindex="0" '
        r'aria-label="[^"]+">\s*(<table>.*?</table>)\s*</div>', text, re.S,
    )
    assert match, "Missing named, keyboard-focusable catalog region"
    table = match[1]
    assert len(re.findall(r'<th scope="col">', table)) == 2
    assert "<details" not in table, "Resource facts must stay visible"
    groups = re.findall(r"<tbody>(.*?)</tbody>", table, re.S)
    assert len(groups) == 6
    for group, count in zip(groups, (4, 8, 4, 4, 2, 1)):
        assert f'scope="rowgroup" rowspan="{count}"' in group
        rows = re.findall(r"<tr>(.*?)</tr>", group, re.S)
        assert len(rows) == count
        for row in rows:
            assert row.count("<td>") == 1
            fields = re.findall(r'<p data-field="([^"]+)">(.*?)</p>', row, re.S)
            assert tuple(name for name, _ in fields) == FIELDS
            assert all(re.sub(r"<[^>]+>", "", value).strip() for _, value in fields)
            entry = fields[0][1]
            assert "<strong><a href=" in entry
            assert re.search(r'<span data-field="rating">⭐{3,5}</span>', entry)
    return table


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

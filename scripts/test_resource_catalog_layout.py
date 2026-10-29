"""Keep resource catalogs lossless, grouped, labeled and visible on every route."""

from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[1]
CATALOGS = {
    "resources/advanced-rag": ((4, 4, 4), ("entry", "audience", "learn", "status")),
    "resources/agent-memory": ((8, 3, 4), ("entry", "audience", "learn", "status")),
    "stages/06-memory-rag": ((3, 4, 2), ("entry", "audience", "learn", "status")),
    "resources/courses": ((3, 6, 2, 2), ("entry", "cost", "outcome", "limits")),
}
SUFFIXES = ("", ".en", ".zh-Hans")


def resource_catalog(text: str, stem: str) -> str:
    """Validate a complete catalog, not merely one matching paragraph."""
    groups, fields = CATALOGS[stem]
    matches = re.findall(
        r'<div class="reader-resource-catalog" role="region" tabindex="0" '
        r'aria-label="[^"]+">\s*(<table align="center">.*?</table>)\s*</div>', text, re.S,
    )
    assert len(matches) == 1, "Expected one named, keyboard-focusable catalog"
    table = matches[0]
    assert len(re.findall(r'<th scope="col">', table)) == 5
    visible = re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.S)
    assert table in visible, "Important resources must not be collapsed"
    assert "<details" not in table
    bodies = re.findall(r"<tbody>(.*?)</tbody>", table, re.S)
    assert len(bodies) == len(groups)
    for body, expected in zip(bodies, groups):
        categories = re.findall(r'<th scope="rowgroup" rowspan="(\d+)" align="center" valign="middle" width="80">[^<]+</th>', body)
        assert categories == [str(expected)], "Keep exactly one real merged category"
        rows = re.findall(r"<tr>(.*?)</tr>", body, re.S)
        assert len(rows) == expected
        for row in rows:
            assert len(re.findall(r"<td\b[^>]*>", row)) == row.count("</td>") == 4
            facts = re.findall(r'<div data-field="([^"]+)">(.*?)</div>', row, re.S)
            assert tuple(key for key, _ in facts) == fields, "Lost or reordered a resource field"
            entry = re.fullmatch(
                r'<strong>(.*?)</strong>', facts[0][1].strip(), re.S,
            )
            assert entry and re.search(r'<td\b[^>]*><span data-field="rating">⭐{3,5}[^<]*</span></td>', row), "Keep the original editorial rating"
            assert "<br" not in entry[1], "Do not force project-name line breaks"
            assert not re.search(r">[^<>]+/[^<>]+</a>", entry[1]), "Show project names, not owner/repo"
            for key, value in facts[1:]:
                label = re.match(r"<strong>[^<]+[：:]</strong>\s*(.+)", value, re.S)
                assert label and re.sub(r"<[^>]+>", "", label[1]).strip(), f"Missing labeled {key}"
                assert "⭐" not in value, "Do not mix ratings into resource facts"
    return table


@pytest.mark.parametrize("stem", CATALOGS)
@pytest.mark.parametrize("suffix", SUFFIXES)
def test_catalogs_keep_all_fields_visible_and_real_merged_categories(stem, suffix):
    resource_catalog((ROOT / f"{stem}{suffix}.md").read_text(encoding="utf-8"), stem)


@pytest.mark.parametrize("stem", CATALOGS)
def test_catalog_mirrors_keep_url_order_ratings_names_and_group_order(stem):
    observations = []
    for suffix in SUFFIXES:
        table = resource_catalog((ROOT / f"{stem}{suffix}.md").read_text(encoding="utf-8"), stem)
        observations.append((
            re.findall(r'href="([^"]+)"', table),
            re.findall(r'<span data-field="rating">(⭐+)', table),
            re.findall(r'rowspan="(\d+)"', table),
        ))
    assert observations[0] == observations[1] == observations[2]


@pytest.mark.parametrize("stem", CATALOGS)
@pytest.mark.parametrize("mutation", ("field", "rating", "category", "closed", "owner", "break"))
def test_catalog_validation_rejects_lost_or_hidden_information(stem, mutation):
    text = (ROOT / f"{stem}.md").read_text(encoding="utf-8")
    if mutation == "field":
        last_field = CATALOGS[stem][1][-1]
        changed = re.sub(rf'<div data-field="{last_field}">.*?</div>', "", text, count=1, flags=re.S)
    elif mutation == "rating":
        changed = re.sub(r'<span data-field="rating">.*?</span>', "", text, count=1, flags=re.S)
    elif mutation == "category":
        changed = re.sub(r'rowspan="\d+"', 'rowspan="999"', text, count=1)
    elif mutation == "closed":
        changed = text.replace('<div class="reader-resource-catalog"', '<details><div class="reader-resource-catalog"', 1)
        changed = changed.replace('</table>\n</div>', '</table>\n</div></details>', 1)
    elif mutation == "owner":
        changed = re.sub(r'(<div data-field="entry"><strong><a href="https://github.com/([^/\"]+)/[^\"]+">)([^<]+)', r'\1\2/\3', text, count=1)
    else:
        changed = re.sub(r'(<div data-field="entry"><strong>.*?)(</a>)', r'\1<br>\2', text, count=1)
    assert changed != text, "Mutation must exercise the intended guard"
    with pytest.raises(AssertionError):
        resource_catalog(changed, stem)


@pytest.mark.parametrize("suffix", SUFFIXES)
def test_course_cost_cannot_be_misplaced_as_a_rating(suffix):
    stem = "resources/courses"
    text = (ROOT / f"{stem}{suffix}.md").read_text(encoding="utf-8")
    cost = re.search(r'<div data-field="cost"><strong>[^<]+</strong> (.*?)</div>', text, re.S)
    assert cost
    changed = re.sub(r'(<span data-field="rating">).*?(</span>)',
                     lambda match: match[1] + cost[1] + match[2], text, count=1)
    assert changed != text
    with pytest.raises(AssertionError, match="editorial rating"):
        resource_catalog(changed, stem)

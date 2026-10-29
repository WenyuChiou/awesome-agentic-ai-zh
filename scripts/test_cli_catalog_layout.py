"""CLI catalogs keep the right label with each fact, without hiding resources."""
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
CATALOGS = {
    "resources/cli-agents-guide": ((4, 5), ("entry", "audience", "models", "auth", "safety", "status", "sources")),
    "tracks/cli/A2-cli-workflow": ((4, 4, 4, 2, 2), ("entry", "read", "when", "sources")),
    "tracks/cli/A3-cli-production": ((4, 5, 4, 3, 2), ("entry", "read", "when", "sources")),
}
LABELS = {
    "guide": {
        "": ("現在適合誰：", "模型／provider 選擇：", "登入方式：", "安全起手式：", "狀態：", "官方來源："),
        ".en": ("Who it currently suits:", "Model / provider choices:", "Sign-in method:", "Safe starting point:", "Status:", "Official sources:"),
        ".zh-Hans": ("现在适合谁：", "模型 / provider 选择：", "登录方式：", "安全起手式：", "状态：", "官方来源："),
    },
    "A2": {
        "": ("先看：", "適用：", "來源："),
        ".en": ("Read:", "Use for:", "Source:"),
        ".zh-Hans": ("先看：", "适用：", "来源："),
    },
    "A3": {
        "": ("先看什麼：", "何時使用：", "來源："),
        ".en": ("Read first:", "When to use:", "Source:"),
        ".zh-Hans": ("先看什么：", "何时使用：", "来源："),
    },
}
SUFFIXES = ("", ".en", ".zh-Hans")


def cli_catalog(text, stem, suffix):
    groups, names = CATALOGS[stem]
    guide = stem == "resources/cli-agents-guide"
    match = re.search(r'<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="[^"]+">\s*(<table align="center">.*?</table>)\s*</div>', text, re.S)
    assert match, "Missing focusable, named catalog"
    table = match[1]
    assert table in re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.S), "Important catalog is hidden"
    assert table.count('<th scope="col">') == 5
    bodies = re.findall(r"<tbody>(.*?)</tbody>", table, re.S)
    assert len(bodies) == len(groups)
    expected_labels = LABELS["guide" if guide else "A2" if "A2" in stem else "A3"][suffix]
    for body, count in zip(bodies, groups):
        assert re.findall(r'<th scope="rowgroup" rowspan="(\d+)" align="center" valign="middle" width="80">', body) == [str(count)]
        rows = re.findall(r"<tr>(.*?)</tr>", body, re.S)
        assert len(rows) == count
        for row in rows:
            assert len(re.findall(r"<td\b[^>]*>", row)) == row.count("</td>") == 4
            fields = re.findall(r'<div data-field="([^"]+)">(.*?)</div>', row, re.S)
            assert tuple(key for key, value in fields) == names
            entry = re.fullmatch(r'<strong>(.*?)</strong>', fields[0][1], re.S)
            assert entry and bool(re.search(r'<td\b[^>]*><span data-field="rating">⭐{3,5}</span></td>', row)) == (not guide), "Keep ratings only where originally provided"
            assert "<br" not in entry[1], "Do not force project names to break"
            for owner, repo in re.findall(r'https://github.com/([^/"<>]+)/([^/"<>]+)', row):
                assert f"{owner}/{repo}" not in re.sub(r"<[^>]+>", "", entry[1]), "Display the project name without its owner"
            for (key, value), label in zip(fields[1:], expected_labels):
                assert value.startswith(f'<strong>{label}</strong> '), f"Wrong label for {key}"
                assert re.sub(r"<[^>]+>", "", value.removeprefix(f'<strong>{label}</strong> ')).strip()
                assert "⭐" not in value
            assert len(re.findall(r'href="', fields[-1][1])) == (2 if guide else 1)
    return table


@pytest.mark.parametrize("stem", CATALOGS)
@pytest.mark.parametrize("suffix", SUFFIXES)
def test_cli_catalogs_have_all_correctly_labeled_visible_fields(stem, suffix):
    cli_catalog((ROOT / f"{stem}{suffix}.md").read_text(encoding="utf-8"), stem, suffix)


@pytest.mark.parametrize("stem", CATALOGS)
def test_cli_catalog_locales_share_urls_ratings_and_groups(stem):
    results = []
    for suffix in SUFFIXES:
        table = cli_catalog((ROOT / f"{stem}{suffix}.md").read_text(encoding="utf-8"), stem, suffix)
        results.append((re.findall(r'href="([^"]+)"', table), re.findall(r'<span data-field="rating">(⭐+)</span>', table), re.findall(r'rowspan="(\d+)"', table)))
    assert results[0] == results[1] == results[2]


@pytest.mark.parametrize("stem", CATALOGS)
@pytest.mark.parametrize("mutation", ("drop", "label", "hide", "owner"))
def test_cli_catalog_guards_reject_lost_mislabeled_or_hidden_fields(stem, mutation):
    text = (ROOT / f"{stem}.md").read_text(encoding="utf-8")
    table = cli_catalog(text, stem, "")
    if mutation == "drop":
        changed = re.sub(r'<div data-field="sources">.*?</div>', '', text, count=1, flags=re.S)
    elif mutation == "label":
        changed = re.sub(r'(<div data-field="(?:read|audience)"><strong>)[^<]+', r'\1Wrong:', text, count=1)
    elif mutation == "hide":
        changed = text.replace('<div class="reader-resource-catalog"', '<details><div class="reader-resource-catalog"', 1)
        changed = changed.replace('</table>\n</div>', '</table>\n</div></details>', 1)
    else:
        row = next(row for row in re.findall(r'<tr>.*?</tr>', table, re.S) if 'https://github.com/' in row)
        owner, repo = re.search(r'https://github.com/([^/"<>]+)/([^/"<>]+)', row).groups()
        changed_row = re.sub(r'(<div data-field="entry"><strong>).*?(</strong>)', lambda m: m[1]+owner+'/'+repo+m[2], row, count=1)
        changed = text.replace(row, changed_row, 1)
    assert changed != text
    with pytest.raises(AssertionError):
        cli_catalog(changed, stem, "")

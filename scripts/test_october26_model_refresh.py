"""Official-source model facts and readable, lossless three-locale references."""
from pathlib import Path
import re
from xml.etree import ElementTree

import pytest
import yaml

from model_reference_test_helpers import family_cells


ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("", ".en", ".zh-Hans")
TERRA = "https://developers.openai.com/api/docs/models/gpt-6.1-terra"
KIMI = "https://platform.kimi.ai/docs/guide/kimi-k3-1-pro-quickstart"


def page(locale: str) -> str:
    return (ROOT / f"stages/01-llm-basics{locale}.md").read_text(encoding="utf-8")


def family_table(text: str, family: str) -> ElementTree.Element:
    markup = re.search(rf'<table data-model-family="{family}">.*?</table>', text, re.S)
    assert markup is not None
    return ElementTree.fromstring(markup[0])


@pytest.mark.parametrize("locale", LOCALES)
def test_terra_exact_id_pricing_and_tool_boundary(locale: str) -> None:
    cells = family_cells(page(locale), "GPT")
    assert "`gpt-6.1-terra`" in cells[1] and TERRA in cells[7]
    assert "1.05M" in cells[3] and "128K" in cells[3]
    assert "$1/$0.05/$1.25/$5" in cells[4] and "$2.50" in cells[4]
    assert "30" in cells[4] and "12" in cells[4]
    assert "Terra 6.1" in cells[6] and "Responses API" in cells[6]
    assert "Chat Completions" in cells[6]
    assert "272K" in cells[6] and "1.5" in cells[6]
    assert "Batch" in cells[6] and "Fast" in cells[6]


@pytest.mark.parametrize("locale", LOCALES)
def test_kimi_api_is_not_a_completed_weights_release(locale: str) -> None:
    cells = family_cells(page(locale), "Kimi")
    assert "`kimi-k3.1-pro`" in cells[1]
    assert "`kimi-k3.1-pro-highspeed`" in cells[1]
    assert "`kimi-k3`" not in cells[1]
    assert "1,048,576" in cells[3]
    assert "US$1" in cells[2] and "2026-11-04" in cells[2]
    assert "預告" in cells[2] or "预告" in cells[2] or "announced" in cells[2]
    assert "$2/$0.20/$2/$10" in cells[4]
    assert "$4/$0.20/$4/$20" in cells[4]
    assert "US$" in cells[4] and "CNY" not in cells[4]
    assert "5" in cells[4] and "1" in cells[4] and "Kimi Code" in cells[4]
    assert "reasoning_effort" in cells[6]
    assert all(f"`{effort}`" in cells[6] for effort in ("low", "high", "max"))
    assert "2026-10-31" in cells[6] and "2026" in cells[6]
    assert KIMI in cells[7]
    assert "https://platform.kimi.ai/docs/models" in cells[7]
    assert "https://platform.kimi.ai/docs/guide/context-caching" in cells[7]


@pytest.mark.parametrize("locale", LOCALES)
@pytest.mark.parametrize("family,counts", (("GPT", {"models": 4, "pricing": 5}),
                                          ("Kimi", {"models": 2, "pricing": 4, "limits": 2})))
def test_long_fields_use_real_merged_labels(locale: str, family: str, counts: dict) -> None:
    table = family_table(page(locale), family)
    for field, count in counts.items():
        rows = table.find(f'./tbody[@data-field="{field}"]').findall("tr")
        assert len(rows) == count
        assert rows[0].find("th").attrib == {"scope": "rowgroup", "rowspan": str(count)}
        assert len(rows[0]) == 2
        assert all(len(row) == 1 and row[0].tag == "td" for row in rows[1:])


def test_model_numbers_ids_urls_and_groups_match_across_locales() -> None:
    for family in ("GPT", "Kimi"):
        signatures = []
        for locale in LOCALES:
            table = family_table(page(locale), family)
            signatures.append((
                [node.text for node in table.iter("code")],
                [node.attrib["href"] for node in table.iter("a")],
                # English spells the Chinese 每百萬 unit as "per 1M tokens".
                # Normalize only that unit, not actual prices, dates or limits.
                re.findall(r"\d+(?:[.,]\d+)*", " ".join(table.itertext()).replace("per 1M tokens", "per million tokens")),
                [(group.attrib["data-field"], len(group.findall("tr"))) for group in table.findall("tbody")],
            ))
        assert signatures[0] == signatures[1] == signatures[2], family


@pytest.mark.parametrize("locale", LOCALES)
def test_new_model_choices_stay_visible_without_redating_other_facts(locale: str) -> None:
    text = page(locale)
    visible = text.split("<details", maxsplit=1)[0]
    assert "**GPT-6.1 Sol" in visible and "Terra" in visible
    assert "Kimi K3.1 Pro**" in visible
    assert "verified_on=2026-09-22" in text
    dates = next(line for line in text.splitlines() if line.startswith("<small>") and "2026-09-22 UTC" in line)
    assert all(value in dates for value in ("2026-10-26 UTC", "2026-10-08 UTC", "2026-10-15 UTC", "2026-10-23 UTC"))
    assert "gemma4:e4b" in text


def test_fact_pack_tracks_only_this_scoped_refresh() -> None:
    config = yaml.safe_load((ROOT / "scripts/freshness-models.yml").read_text(encoding="utf-8"))
    pack = config["stage01_fact_pack"]
    assert pack["verified_on"] == "2026-09-22"
    assert pack["provider_updates"]["gpt"] == pack["provider_updates"]["kimi"] == "2026-10-26"
    assert pack["provider_updates"]["anthropic"] == "2026-10-08"
    assert pack["provider_updates"]["deepseek"] == "2026-10-23"
    assert pack["official_sources"]["gpt_terra"] == TERRA
    assert pack["official_sources"]["kimi"] == KIMI
    assert pack["pricing_sources"]["kimi"] == "https://platform.kimi.ai/"

"""Scoped weekly facts and reader-visible boundaries, not live product tests."""
from pathlib import Path
import re

import pytest
import yaml

from model_reference_test_helpers import family_cells


ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("", ".en", ".zh-Hans")
DUET = "https://support.claude.com/en/articles/17631495-get-started-with-claude-duet"
CLEF = "https://huggingface.co/Cloudflare/clef"
DEEPSEEK = "https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017"


def visible_text(text: str) -> str:
    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.S)


@pytest.mark.parametrize("locale", LOCALES)
def test_duet_access_and_memory_limits_are_visible(locale: str) -> None:
    text = (ROOT / f"branches/for-everyday-users{locale}.md").read_text(encoding="utf-8")
    visible = visible_text(text)
    row = next(row for row in re.findall(r"<tr>.*?</tr>", visible, re.S) if DUET in row)
    assert "Claude Duet" in row and row.count("⭐") == 3
    assert all(token in row for token in ("Pro", "Max", "Team", "Enterprise"))
    assert 'rowspan="8"' in visible
    assert "2026-10-23 UTC" in visible
    assert "2026-10-16 UTC" in visible  # Do not redate unchecked products.
    phrases = {
        "": ("研究預覽", "美國", "候補邀請", "記憶不會自動刪除"),
        ".en": ("research preview", "US", "waitlist invitation", "memory is not automatically deleted"),
        ".zh-Hans": ("研究预览", "美国", "候补邀请", "记忆不会自动删除"),
    }[locale]
    assert all(phrase in visible for phrase in phrases)


@pytest.mark.parametrize("locale", LOCALES)
def test_connector_questions_precede_first_connector_action(locale: str) -> None:
    text = (ROOT / f"branches/for-everyday-users{locale}.md").read_text(encoding="utf-8")
    visible = visible_text(text)
    block = re.search(r'<!-- connector-safety:start -->(.*?)<!-- connector-safety:end -->', visible, re.S)
    assert block is not None
    assert len(re.findall(r"^\d\. ", block[1], re.M)) == 4
    assert block.start() < visible.index("<table>")
    assert "Approval Gate" in block[1]


@pytest.mark.parametrize("locale", LOCALES)
def test_deepseek_exact_snapshot_aliases_and_price_conditions(locale: str) -> None:
    text = (ROOT / f"stages/01-llm-basics{locale}.md").read_text(encoding="utf-8")
    cells = family_cells(text, "DeepSeek")
    assert "1017" in cells[1] and "0813" in cells[1]
    assert "deepseek-flash" in cells[1]
    assert DEEPSEEK in cells[7] and "MIT" in cells[4]
    assert all(price in cells[4] for price in (
        "$0.30/$0.15", "$1.20/$0.60", "$0.006/$0.003",
        "$1.32/$0.66", "$3.96/$1.98", "$0.044/$0.022",
    ))
    assert "deepseek-v4-flash-vision-exp" in cells[6]
    assert "01:00" in cells[6] and "06:00" in cells[6]
    assert {"": "中國公眾假期", ".en": "Chinese public holidays", ".zh-Hans": "中国公众假期"}[locale] in cells[6]
    assert "verified_on=2026-09-22" in text
    date_note = next(note for note in re.findall(r"<small>(.*?)</small>", text, re.S) if "2026-09-22 UTC" in note)
    assert all(value in date_note for value in ("DeepSeek", "Decisions", "Clef", "2026-10-23 UTC"))


@pytest.mark.parametrize("locale", LOCALES)
def test_decision_electives_keep_model_action_and_hardware_boundaries(locale: str) -> None:
    text = (ROOT / f"stages/01-llm-basics{locale}.md").read_text(encoding="utf-8")
    elective = re.search(r'<!-- decision-electives:start -->(.*?)<!-- decision-electives:end -->', text, re.S)
    assert elective is not None
    assert "public beta" not in elective[1].lower()
    for token in ("gpt-6-luna", "400", "$0.10", "27B", "Apache-2.0", CLEF):
        assert token in elective[1]
    assert "Decisions API" in elective[1]
    assert "Clef" not in family_cells(text, "Jev (TypeSafe AI)" if locale == ".en" else "Jev（TypeSafe AI）")[1]
    assert "gemma4:e4b" in text
    visible = visible_text(text)
    assert {"": "判斷不是授權", ".en": "Deciding is not authorization", ".zh-Hans": "判断不是授权"}[locale] in visible


def test_scoped_facts_and_cross_locale_numbers_match() -> None:
    config = yaml.safe_load((ROOT / "scripts/freshness-models.yml").read_text(encoding="utf-8"))
    pack = config["stage01_fact_pack"]
    assert pack["verified_on"] == "2026-09-22"
    assert pack["provider_updates"]["deepseek"] == "2026-10-23"
    assert pack["provider_updates"]["gpt_decisions"] == "2026-10-23"
    assert pack["provider_updates"]["cloudflare_clef"] == "2026-10-23"
    assert pack["provider_updates"]["gpt_features"] == "2026-10-15"
    assert pack["official_sources"]["deepseek_weights"] == DEEPSEEK
    assert pack["official_sources"]["cloudflare_clef"] == CLEF
    for marker in ("decision-electives", "connector-safety"):
        signatures = []
        section = "stages/01-llm-basics" if marker == "decision-electives" else "branches/for-everyday-users"
        for locale in LOCALES:
            text = (ROOT / f"{section}{locale}.md").read_text(encoding="utf-8")
            block = re.search(rf"<!-- {marker}:start -->(.*?)<!-- {marker}:end -->", text, re.S)
            assert block is not None
            urls = re.findall(r"https://[^\s)>\"]+", block[1])
            numbers = re.findall(r"\d+(?:[.,]\d+)*", re.sub(r"https://[^\s)>\"]+", "", block[1]))
            signatures.append((urls, numbers))
        assert signatures[0] == signatures[1] == signatures[2], marker

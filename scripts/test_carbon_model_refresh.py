"""Keep an announced, restricted model distinct from a usable beginner API."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

from model_reference_test_helpers import family_cells, family_rows

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("", ".en", ".zh-Hans")
ANNOUNCEMENT = "https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/"


@pytest.mark.parametrize("locale", LOCALES)
def test_carbon_warning_is_visible_but_recommendations_are_available(locale: str) -> None:
    text = (ROOT / f"stages/01-llm-basics{locale}.md").read_text(encoding="utf-8")
    visible = re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.S)
    assert "**Gemini 4 Carbon**" in visible and ANNOUNCEMENT in visible
    boundary = {"": "一般開發者還不能直接用", ".en": "not yet available to general developers",
                ".zh-Hans": "一般开发者还不能直接用"}[locale]
    assert boundary in visible
    cells = family_cells(text, "Gemini")
    assert "Carbon" not in cells[1]
    assert "Gemini 3.8 Flash" in cells[1] and "gemini-4-argon" in cells[1]
    assert "Preview" in cells[2]
    assert len(family_rows(text)) == 18
    assert "<code>gemini-4-carbon</code>" not in text


@pytest.mark.parametrize("locale", LOCALES)
def test_carbon_does_not_inherit_argon_specs_or_promotion_end(locale: str) -> None:
    text = (ROOT / f"stages/01-llm-basics{locale}.md").read_text(encoding="utf-8")
    cells = family_cells(text, "Gemini")
    carbon_context = cells[3].split("Carbon", 1)[1]
    assert "1,048,576" not in carbon_context and "65,536" not in carbon_context
    carbon_prices = cells[4].split("Carbon", 1)[1]
    assert all(value in carbon_prices for value in ("$2/$10", "$4/$20", "5%", "$0.10"))
    assert "2026-11-30" not in carbon_prices and "2026-12-01" not in carbon_prices
    context_unknown, price_unknown = {
        "": ("官方未公布", "官方未公布"),
        ".en": ("not published", "not been published"),
        ".zh-Hans": ("官方未公布", "官方未公布"),
    }[locale]
    assert context_unknown in carbon_context and price_unknown in carbon_prices
    assert "API ID" in cells[6] and ANNOUNCEMENT in cells[7]


def test_carbon_fact_pack_keeps_unknown_fields_unknown_and_dates_scoped() -> None:
    config = yaml.safe_load((ROOT / "scripts/freshness-models.yml").read_text(encoding="utf-8"))
    pack = config["stage01_fact_pack"]
    assert pack["verified_on"] == "2026-09-22"
    assert pack["provider_updates"]["gemini"] == "2026-10-29"
    assert pack["provider_updates"]["muse"] == "2026-10-15"
    carbon = pack["announced_models"]["gemini_carbon"]
    assert carbon["status"] == "Preview" and carbon["public_api_available"] is False
    assert carbon["pricing_is_announcement"] is True
    for field in ("api_model_id", "input_context_tokens", "max_output_tokens",
                  "general_access_date", "tool_support", "introductory_end_date"):
        assert carbon[field] is None
    assert carbon["introductory_cached_input_calculated"] == pytest.approx(
        carbon["introductory_input"] * (1 - carbon["cached_input_discount_percent"] / 100)
    )
    assert ANNOUNCEMENT in carbon["official_sources"]


def test_manual_browser_record_is_not_a_scanner_override() -> None:
    audit = json.loads((ROOT / "docs/maintenance/link-browser-audit-20261029.json").read_text(encoding="utf-8"))
    assert audit["scanner_results_overridden"] is False
    records = audit["records"]
    assert len(records) == len({row["url"] for row in records}) == 10
    assert all(row["httpStatus"] == 200 for row in records)
    assert sum(row["classification"] == "valid" for row in records) == 9
    login = [row for row in records if row["classification"] != "valid"]
    assert len(login) == 1 and login[0]["finalUrl"] == "https://claude.ai/login"

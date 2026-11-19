"""Verify paid API access and model-specific pricing in all three locales."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

from model_reference_test_helpers import ModelReferenceParser, family_cells, family_rows

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("", ".en", ".zh-Hans")
ANNOUNCEMENT = "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/"


@pytest.mark.parametrize("locale", LOCALES)
def test_paid_gemini_access_is_visible_before_reference(locale: str) -> None:
    text = (ROOT / f"stages/01-llm-basics{locale}.md").read_text(encoding="utf-8")
    visible = re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.S)
    assert "**Gemini 4 Carbon**" in visible
    assert "**Gemini 4 Neon**" in visible
    boundary = {"": "付費 API", ".en": "paid API", ".zh-Hans": "付费 API"}[locale]
    assert boundary in next(line for line in visible.splitlines() if line.startswith("**Gemini 4 Carbon**"))
    cells = family_cells(text, "Gemini")
    assert "gemini-4-carbon" in cells[1] and "gemini-4-neon" in cells[1]
    assert "2026-11-10" in cells[2]
    assert len(family_rows(text)) == 18


def carbon_field_rows(text: str, field: str) -> list[str]:
    """Select Carbon's own data rows, not all text after its first mention."""
    parser = ModelReferenceParser()
    parser.feed(text)
    rows = [row for row in parser.records["Gemini"][field]
            if re.match(r"^Carbon(?=[:：\s])", row)]
    assert len(rows) == {"context": 1, "pricing": 2}[field]
    return rows


@pytest.mark.parametrize("locale", LOCALES)
def test_carbon_and_neon_have_separate_pricing_and_limits(locale: str) -> None:
    text = (ROOT / f"stages/01-llm-basics{locale}.md").read_text(encoding="utf-8")
    cells = family_cells(text, "Gemini")
    carbon_context = carbon_field_rows(text, "context")[0]
    context_separator = ": " if locale == ".en" else "："
    assert carbon_context.startswith(f"Carbon{context_separator}")
    assert all(value in carbon_context for value in ("1,048,576", "65,536"))
    introductory, current = carbon_field_rows(text, "pricing")
    assert "2026-11-30" in introductory and "$2/$0.10/$10" in introductory
    assert "2026-12-01" in current and "$4/$0.20/$20" in current
    parser = ModelReferenceParser()
    parser.feed(text)
    fields = parser.records["Gemini"]
    neon_context = [row for row in fields["context"] if row.startswith(f"Neon{context_separator}")]
    neon_pricing = [row for row in fields["pricing"] if re.match(r"^Neon[:：]", row)]
    assert len(neon_context) == len(neon_pricing) == 1
    assert all(value in neon_context[0] for value in ("1,048,576", "65,536"))
    assert "$3/$0.15/$15" in neon_pricing[0]
    assert ANNOUNCEMENT in cells[7]


def test_carbon_and_neon_fact_pack_updates_are_scoped() -> None:
    config = yaml.safe_load((ROOT / "scripts/freshness-models.yml").read_text(encoding="utf-8"))
    pack = config["stage01_fact_pack"]
    assert pack["verified_on"] == "2026-09-22"
    assert pack["provider_updates"]["gemini"] == "2026-10-29"
    assert pack["provider_updates"]["gemini_carbon"] == pack["provider_updates"]["gemini_neon"] == "2026-11-19"
    carbon = pack["model_updates"]["gemini_carbon"]
    assert carbon["status"] == "stable" and carbon["free_tier"] is False
    assert carbon["general_access_date"] == "2026-11-10"
    assert carbon["introductory_end_date"] == "2026-11-30"
    assert carbon["post_introductory_start_date"] == "2026-12-01"
    assert ANNOUNCEMENT == pack["official_sources"]["gemini_carbon_availability"]


def test_manual_browser_record_is_not_a_scanner_override() -> None:
    audit = json.loads((ROOT / "docs/maintenance/link-browser-audit-20261029.json").read_text(encoding="utf-8"))
    assert audit["scanner_results_overridden"] is False
    records = audit["records"]
    assert len(records) == len({row["url"] for row in records}) == 10
    assert all(row["httpStatus"] == 200 for row in records)
    assert sum(row["classification"] == "valid" for row in records) == 9
    login = [row for row in records if row["classification"] != "valid"]
    assert len(login) == 1 and login[0]["finalUrl"] == "https://claude.ai/login"


@pytest.mark.parametrize("hydrogen_first", (False, True))
def test_carbon_row_selection_excludes_hydrogen_but_preserves_carbon_facts(hydrogen_first: bool) -> None:
    carbon = '<tr><td>Carbon: not published</td></tr>'
    hydrogen = '<tr><td>Hydrogen: 1,048,576; 65,536</td></tr>'
    rows = hydrogen + carbon if hydrogen_first else carbon + hydrogen
    text = '<table data-model-family="Gemini"><tbody data-field="context">' + rows + '</tbody></table>'
    assert carbon_field_rows(text, "context") == ["Carbon: not published"]
    # A real Carbon contamination must remain visible to the existing assertions.
    contaminated = text.replace("Carbon: not published", "Carbon: 1,048,576; 65,536")
    assert all(value in carbon_field_rows(contaminated, "context")[0]
               for value in ("1,048,576", "65,536"))


def test_carbon_price_selection_keeps_both_rows_and_rejects_missing_rows() -> None:
    text = ('<table data-model-family="Gemini"><tbody data-field="pricing">'
            '<tr><td>Argon: 2026-11-30</td></tr>'
            '<tr><td>Carbon introductory: $2/$10; 5%; $0.10</td></tr>'
            '<tr><td>Carbon post-promotion: $4/$20; end not published</td></tr>'
            '<tr><td>Hydrogen: $1.50/$7.50; 2026-12-01</td></tr>'
            '</tbody></table>')
    rows = carbon_field_rows(text, "pricing")
    assert len(rows) == 2 and all(row.startswith("Carbon") for row in rows)
    assert "2026-11-30" not in "; ".join(rows) and "2026-12-01" not in "; ".join(rows)
    contaminated = text.replace("Carbon introductory:", "Carbon introductory: 2026-11-30")
    assert "2026-11-30" in "; ".join(carbon_field_rows(contaminated, "pricing"))
    with pytest.raises(AssertionError):
        carbon_field_rows(text.replace("Carbon post-promotion:", "Hydrogen post-promotion:"), "pricing")

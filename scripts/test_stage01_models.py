from __future__ import annotations

import re
from pathlib import Path
from xml.etree import ElementTree

import pytest

from model_reference_test_helpers import FIELDS, ModelReferenceParser, family_cells, family_rows


ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    (ROOT / "stages" / "01-llm-basics.md", "Fable／Opus／Sonnet／Haiku：正式可用", "Mythos：限核准使用者"),
    (ROOT / "stages" / "01-llm-basics.zh-Hans.md", "Fable／Opus／Sonnet／Haiku：正式可用", "Mythos：限核准用户"),
    (ROOT / "stages" / "01-llm-basics.en.md", "Fable/Opus/Sonnet/Haiku: generally available", "Mythos: vetted access only"),
)


@pytest.mark.parametrize(("page", "fable_status", "mythos_status"), PAGES)
def test_stage01_uses_current_fable_and_mythos_models(
    page: Path, fable_status: str, mythos_status: str
) -> None:
    text = page.read_text(encoding="utf-8")
    cells = family_cells(text, "Claude")

    assert len(cells) == 8
    assert "Fable 5.1" in cells[1]
    assert "Mythos 5.1" in cells[1]
    assert "claude-fable-5-1" in cells[1]
    assert "claude-mythos-5-1" in cells[1]
    assert fable_status in cells[2]
    assert mythos_status in cells[2]
    assert "1M" in cells[3]
    assert "128K" in cells[3]
    assert "$10/$50" in cells[4]
    assert "$0.25" in cells[4]
    assert "claude-opus-5-5" in cells[1]
    assert "claude-sonnet-5-5" in cells[1]
    assert "$4/$20" in cells[4]
    assert "$2/$10" in cells[4]
    assert "$0.20" in cells[4]
    assert "https://platform.claude.com/docs/en/models/opus-5-5/overview" in cells[7]
    assert "https://platform.claude.com/docs/en/models/sonnet-5-5/overview" in cells[7]
    assert "https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide" in cells[7]
    assert "claude-fable-5-1" in text
    assert "claude-mythos-5-1" in text
    assert not re.search(r"claude-(?:fable|mythos)-5(?!-1)", text)
    assert "verified_on=2026-09-22" in text


@pytest.mark.parametrize("page", [item[0] for item in PAGES])
def test_stage01_uses_current_gpt_family(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    cells = family_cells(text, "GPT")

    assert len(cells) == 8
    for model in ("gpt-6-astra", "gpt-6.1-sol", "gpt-6.1-terra", "gpt-6-luna"):
        assert model in cells[1]
        assert f"https://developers.openai.com/api/docs/models/{model}" in cells[7]
    assert "GPT-5.6" not in cells[1]
    assert "1.05M" in cells[3]
    assert "128K" in cells[3]
    assert "Standard" in cells[4]
    assert "$10/$1/$12.50/$50" in cells[4]
    assert "$2/$0.10/$2.50/$10" in cells[4]
    assert "$1/$0.05/$1.25/$5" in cells[4]
    assert "$0.10/$0.01/$0.125/$0.50" in cells[4]
    assert "272K" in cells[6]
    assert "1.5" in cells[6]
    assert "https://developers.openai.com/api/docs/pricing" in cells[7]
    assert "GPT-6.1 Sol" in text.split("<details", maxsplit=1)[0]
    assert "2026-10-26 UTC" in text
    assert "verified_on=2026-09-22" in text


def test_stage01_fact_pack_separates_full_table_and_gpt_update_dates() -> None:
    fact_pack = (ROOT / "scripts" / "freshness-models.yml").read_text(encoding="utf-8")
    assert "verified_on: '2026-09-22'" in fact_pack
    assert "gpt: '2026-10-26'" in fact_pack
    assert "kimi: '2026-10-26'" in fact_pack
    assert "gemini: '2026-10-15'" in fact_pack
    for provider in ("typesafe_jev", "muse", "mistral", "gpt_features"):
        assert f"{provider}: '2026-10-15'" in fact_pack
    assert "anthropic: '2026-10-08'" in fact_pack
    assert "claude_sonnet: 'https://platform.claude.com/docs/en/models/sonnet-5-5/overview'" in fact_pack
    assert "gpt: 'https://developers.openai.com/api/docs/pricing'" in fact_pack


@pytest.mark.parametrize("page", [item[0] for item in PAGES])
def test_stage01_explains_typesafe_jev_without_treating_it_as_a_chat_llm(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    cells = family_cells(text, "Jev")

    assert len(cells) == 8
    assert "early access" in cells[2].lower()
    assert "jev-1.13.0" in cells[1]
    assert "jev-latest" in cells[1]
    assert "TypeSafe direct" in cells[1]
    assert "Cloudflare route" in cells[1]
    assert "64K" in cells[3] and "32K" in cells[3]
    assert "TypeSafe direct" in cells[3] and "Cloudflare route" in cells[3]
    assert "$0.042" in cells[4]
    assert "TypeSafe direct" in cells[4] and "Cloudflare route" in cells[4]
    assert "unmetered" in cells[4] or "不計費" in cells[4] or "不计费" in cells[4]
    assert "free-form text" in cells[6] or "自由文字" in cells[6] or "自由文本" in cells[6]
    assert "https://docs.typesafe.ai/models" in cells[7]
    assert "https://docs.typesafe.ai/introduction" in cells[7]
    assert "https://typesafe.ai/blog/introducing-system-one-models-and-jev" in cells[7]
    assert "https://developers.cloudflare.com/ai/models/typesafe/jev/" in cells[7]
    assert "Jev" in text
    assert "Choice" in text and "Score" in text and "Noul" in text


@pytest.mark.parametrize("page", [item[0] for item in PAGES])
def test_stage01_current_model_table_corrections(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    rows = family_rows(text)

    assert "Gemini 3.8 Flash" in rows["Gemini"][1]
    assert "Gemini 3.7 Flash" not in rows["Gemini"][1]
    deepseek = rows["DeepSeek"]
    assert deepseek[3] in {
        "1M context／384K 最大輸出",
        "1M context／384K 最大输出",
        "1M context / 384K max output",
    }
    assert "deepseek-flash" in deepseek[1]
    assert "$0.30/$0.15" in deepseek[4]
    assert "$1.20/$0.60" in deepseek[4]
    assert "$1.32/$0.66" in deepseek[4]
    assert "$3.96/$1.98" in deepseek[4]

    hunyuan = rows["Hunyuan"]
    assert hunyuan[3] == "256K"
    assert "2026-08-31" in hunyuan[6]
    assert "https://cloud.tencent.com/document/product/1823/130051" in hunyuan[7]

    minimax = rows["MiniMax"]
    assert "permanent 50% off" not in minimax[4]
    assert "永久 50% 折扣" not in minimax[4]
    assert "$0.30/$0.06/$1.20" in minimax[4]
    assert "$0.60/$0.12/$2.40" in minimax[4]
    assert "MiniMax Community License" in minimax[4]
    assert "https://huggingface.co/MiniMaxAI/MiniMax-M3" in minimax[7]


@pytest.mark.parametrize("page", [item[0] for item in PAGES])
def test_stage01_has_eighteen_sourced_families_and_distinguishes_muse_products(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    rows = family_rows(text)
    families = {"Claude", "GPT", "Jev（TypeSafe AI）", "Jev (TypeSafe AI)", "Gemini", "DeepSeek", "Kimi", "Hunyuan", "MiniMax", "Qwen", "GLM", "Yi", "Llama", "Muse", "Grok", "MiMo", "Gemma", "Mistral", "Phi"}
    assert len(set(rows) & families) == 18
    assert "muse-spark-1.3" in rows["Muse"][1]
    assert "muse-spark-1.3-contributor" in rows["Muse"][1]
    assert "US$1.25/$0.15/$4.25" in rows["Muse"][4]
    assert "US$0.10/$0.002/$0.20" in rows["Muse"][4]
    assert "https://dev.meta.ai/docs/pricing-rate-limits" in rows["Muse"][7]
    assert "grok-4.7" in rows["Grok"][1]
    assert "US$2/$0.50/$6" in rows["Grok"][4]
    assert "https://docs.x.ai/developers/models/grok-4.7" in rows["Grok"][7]
    assert "mimo-v2.6-pro" in rows["MiMo"][1]
    assert "US$0.435/$0.0036/$0.87" in rows["MiMo"][4]
    assert "https://mimo.mi.com/models/en-US/mimo-v2.6-pro" in rows["MiMo"][7]
    assert "https://ai.google.dev/gemini-api/docs/models/gemini-3.8-live" in text
    assert all(len(cells) == 8 and all(cells) for cells in rows.values())


@pytest.mark.parametrize("page", [item[0] for item in PAGES])
def test_stage01_gpt61_has_exact_id_and_responses_tool_boundary(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    cells = family_cells(text, "GPT")
    assert "gpt-6.1-sol" in cells[1]
    assert "`gpt-6-sol`" not in cells[1]
    required_boundary = {
        "01-llm-basics.md": ("工具呼叫須用 Responses API", "Chat Completions 不支援工具呼叫"),
        "01-llm-basics.en.md": ("tool calling requires Responses API", "Chat Completions has no tool calling"),
        "01-llm-basics.zh-Hans.md": ("工具调用须用 Responses API", "Chat Completions 不支持工具调用"),
    }[page.name]
    assert all(token in cells[6] for token in required_boundary)
    assert "Sora" not in " ".join(cells)
    assert "https://developers.openai.com/api/docs/models/gpt-6.1-sol" in cells[7]


@pytest.mark.parametrize("page", [item[0] for item in PAGES])
def test_stage01_argon_is_available_with_scoped_context_and_pricing(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    cells = family_cells(text, "Gemini")
    assert "Gemini 3.8 Flash" in cells[1] and "Gemini 4 Argon" in cells[1]
    assert "`gemini-4-argon`" in cells[1]
    assert "Fairwind" not in " ".join(cells)
    assert any(label in cells[2] for label in ("正式可用", "generally available"))
    assert "1,048,576" in cells[3] and "65,536" in cells[3]
    assert "long decode" in cells[6] and "1M" in cells[6]
    assert "2026-11-30" in cells[4] and "2026-12-01" in cells[4]
    assert "$2/$0.10/$10" in cells[4] and "$4/$0.20/$20" in cells[4]
    assert any(label in cells[6] for label in ("無免費層", "无免费层", "no free tier"))
    assert "https://ai.google.dev/gemini-api/docs/models/gemini-4-argon" in cells[7]
    visible_selector = text.split("<details", maxsplit=1)[0]
    assert "Gemini 3.8 Flash" in visible_selector
    assert "Gemini 4 Argon" not in visible_selector


@pytest.mark.parametrize("page", [item[0] for item in PAGES])
def test_october_preview_and_product_boundaries(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    rows = family_rows(text)
    jev = next(cells for key, cells in rows.items() if key.startswith("Jev"))
    assert "jev-1.14.0" in jev[1] and "jev-preview" in jev[1]
    assert "jev-1.13.0" in jev[1] and "jev-latest" in jev[1]
    assert "Preview" in jev[2]
    assert "262K" not in jev[3] and "262K" in jev[6]
    assert "experimental" in jev[6]
    assert "muse-wonder-1.0" in rows["Muse"][1]
    assert "US$4/$0.20/$20" in rows["Muse"][4]
    assert "Wonder Full" in rows["Muse"][6] and "Muse Code" in rows["Muse"][6]
    mistral = rows["Mistral"]
    assert "mistral-large-4" in mistral[1] and "Public Preview" in mistral[2]
    assert "US$0.68/$0.07/$2.09" in mistral[4]
    assert "US$1.36/$0.14/$4.18" in mistral[4]
    assert "Modified MIT" in mistral[4]
    assert any(token in mistral[6] for token in ("權重尚未釋出", "权重尚未发布", "weights not yet released"))
    assert "https://developers.openai.com/api/docs/guides/ultrafast-mode" in text
    assert "https://developers.openai.com/api/docs/guides/decisions" in text
    decisions = re.search(r"<!-- decision-electives:start -->(.*?)<!-- decision-electives:end -->", text, re.S)
    assert decisions is not None and "gpt-6-luna" in decisions[1]
    assert "public beta" not in decisions[1].lower()


def test_october_model_rows_keep_identical_urls_and_numbers_across_locales() -> None:
    for family in ("Jev", "Gemini", "Muse", "Mistral"):
        signatures = []
        for page, *_ in PAGES:
            row = " ".join(family_cells(page.read_text(encoding="utf-8"), family))
            signatures.append((re.findall(r"https://\S+", row), sorted(re.findall(r"\d+(?:[.,]\d+)*", row))))
        assert signatures[0] == signatures[1] == signatures[2], family


@pytest.mark.parametrize("page", [item[0] for item in PAGES if item[0].suffix == ".md" and ".en." not in item[0].name])
def test_refreshed_model_row_sentences_fit_written_chinese_style(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    for family in ("GPT", "Gemini"):
        # Exclude model-name lists and official-link lists. For descriptive,
        # specification, and pricing cells count rendered text, not link URLs.
        for cell in family_cells(text, family)[2:7]:
            visible = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", cell)
            visible = visible.replace("**", "").replace("`", "")
            for sentence in re.split(r"(?<=[。！？])", visible):
                if sentence.strip():
                    assert len(sentence.strip()) <= 60, sentence


@pytest.mark.parametrize("page", [item[0] for item in PAGES if ".en." not in item[0].name])
def test_refreshed_model_review_date_sentences_fit_written_style(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    summary = next(line for line in text.splitlines() if line.startswith("<small>") and "2026-10-26 UTC" in line)
    visible = re.sub(r"<[^>]+>", "", summary)
    for sentence in re.split(r"(?<=[。！？])", visible):
        if sentence.strip():
            assert len(sentence.strip()) <= 60, sentence


def test_current_model_refresh_changelog_sentences_fit_written_style() -> None:
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    current = text.split("## 2026-10-02\n", 1)[1].split("\n## ", 1)[0]
    entry = next(line for line in current.splitlines() if "content / Stage 1 / model update" in line)
    prose = entry.split(" · ", 1)[1].replace("`", "")
    for sentence in re.split(r"(?<=[。！？])", prose):
        if sentence.strip():
            assert len(sentence.strip()) <= 60, sentence


@pytest.mark.parametrize("page", [item[0] for item in PAGES])
def test_model_reference_uses_closed_family_disclosures_and_two_columns(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    blocks = re.findall(
        r'<details class="model-family" markdown="1">\s*<summary>(.*?)</summary>\s*'
        r'(<table data-model-family=".*?</table>)\s*</details>', text, re.S,
    )
    assert len(blocks) == 18
    assert len(re.findall(r'<details\b[^>]*class="model-family"[^>]*>', text)) == 18
    for family, markup in blocks:
        table = ElementTree.fromstring(markup)
        assert table.attrib["data-model-family"] == family
        assert len(table.findall("./thead/tr/th")) == 2
        groups = table.findall("tbody")
        assert [group.attrib["data-field"] for group in groups] == list(FIELDS)
        models = groups[0].findall("tr")
        label = models[0].find("th")
        assert int(label.attrib.get("rowspan", "1")) == len(models)
        assert label.attrib["scope"] == ("rowgroup" if len(models) > 1 else "row")
        assert len(models[0]) == 2
        assert all(len(row) == 1 and row.find("td") is not None for row in models[1:])
        for group in groups[1:]:
            field_rows = group.findall("tr")
            assert field_rows and len(field_rows[0]) == 2
            field_label = field_rows[0].find("th")
            assert int(field_label.attrib.get("rowspan", "1")) == len(field_rows)
            assert field_label.attrib["scope"] == ("rowgroup" if len(field_rows) > 1 else "row")
            assert all(len(row) == 1 and row.find("td") is not None for row in field_rows[1:])
        assert all("".join(cell.itertext()).strip() for cell in table.iter("td"))
        assert not re.search(r"\[[^\]]+\]\(|`|\*\*", markup)
        assert all(link.attrib.get("href", "").startswith("https://") for link in table.iter("a"))
        if family == "Claude":
            assert len(models) == 5
            assert len(table.findall(".//code")) == 5


def test_all_model_reference_links_and_variant_ids_match_across_locales() -> None:
    signatures = []
    for page, *_ in PAGES:
        parser = ModelReferenceParser()
        parser.feed(page.read_text(encoding="utf-8"))
        signatures.append([
            (re.findall(r"`([^`]+)`", "; ".join(fields["models"])), parser.links[family])
            for family, fields in parser.records.items()
        ])
    assert signatures[0] == signatures[1] == signatures[2]


def test_reference_parser_rejects_missing_fields_and_duplicate_families() -> None:
    table = '<table data-model-family="Claude"><tbody data-field="models"><tr><td>Fable</td></tr></tbody></table>'
    with pytest.raises(AssertionError, match="missing or reordered fields"):
        family_rows(table)
    with pytest.raises(AssertionError, match="duplicate family table"):
        family_rows(table + table)

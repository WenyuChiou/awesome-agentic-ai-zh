from __future__ import annotations

import re
from pathlib import Path

import pytest


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
    row = next(line for line in text.splitlines() if line.startswith("| Claude |"))
    cells = [cell.strip() for cell in row.strip("|").split("|")]

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
    assert "$4/$20" in cells[4]
    assert "$0.20" in cells[4]
    assert "https://platform.claude.com/docs/en/models/opus-5-5/overview" in cells[7]
    assert "claude-fable-5-1" in text
    assert "claude-mythos-5-1" in text
    assert not re.search(r"claude-(?:fable|mythos)-5(?!-1)", text)
    assert "verified_on=2026-09-22" in text


@pytest.mark.parametrize(("page", "gpt_status"), (
    (ROOT / "stages" / "01-llm-basics.md", "Astra：正式發布、分批開放；Terra／Luna：正式可用"),
    (ROOT / "stages" / "01-llm-basics.zh-Hans.md", "Astra：正式发布、分批开放；Terra／Luna：正式可用"),
    (ROOT / "stages" / "01-llm-basics.en.md", "Astra: released, rolling out; Terra/Luna: generally available"),
))
def test_stage01_uses_current_gpt6_astra(page: Path, gpt_status: str) -> None:
    text = page.read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if line.startswith("| GPT |"))
    cells = [cell.strip() for cell in row.strip("|").split("|")]

    assert len(cells) == 8
    assert "GPT-6 Astra" in cells[1]
    assert "GPT-5.6 Terra" in cells[1]
    assert "Luna" in cells[1]
    assert "Sol" not in cells[1]
    assert gpt_status in cells[2]
    assert "1.05M" in cells[3]
    assert "128K" in cells[3]
    assert "$10/$50" in cells[4]
    assert "$2/$12" in cells[4]
    assert "$0.20/$1.20" in cells[4]
    assert "272K" in cells[6]
    assert "2×" in cells[6]
    assert "1.5×" in cells[6]
    assert "GPT-5.6 Sol" in cells[6]
    assert "https://developers.openai.com/api/docs/models/gpt-6-astra" in cells[7]
    assert "verified_on=2026-09-22" in text


@pytest.mark.parametrize("page", [item[0] for item in PAGES])
def test_stage01_explains_typesafe_jev_without_treating_it_as_a_chat_llm(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if line.startswith("| Jev (TypeSafe AI) |") or line.startswith("| Jev（TypeSafe AI） |"))
    cells = [cell.strip() for cell in row.strip("|").split("|")]

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
    rows = {
        line.split("|", 2)[1].strip(): line
        for line in text.splitlines()
        if line.startswith("|")
    }

    assert "Gemini 3.8 Flash" in rows["Gemini"]
    assert "Gemini 3.7 Flash" not in rows["Gemini"]
    deepseek = [cell.strip() for cell in rows["DeepSeek"].strip("|").split("|")]
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

    hunyuan = [cell.strip() for cell in rows["Hunyuan"].strip("|").split("|")]
    assert hunyuan[3] == "256K"
    assert "2026-08-31" in hunyuan[6]
    assert "https://cloud.tencent.com/document/product/1823/130051" in hunyuan[7]

    minimax = [cell.strip() for cell in rows["MiniMax"].strip("|").split("|")]
    assert "permanent 50% off" not in minimax[4]
    assert "永久 50% 折扣" not in minimax[4]
    assert "$0.30/$0.06/$1.20" in minimax[4]
    assert "$0.60/$0.12/$2.40" in minimax[4]
    assert "MiniMax Community License" in minimax[4]
    assert "https://huggingface.co/MiniMaxAI/MiniMax-M3" in minimax[7]


@pytest.mark.parametrize("page", [item[0] for item in PAGES])
def test_stage01_has_eighteen_sourced_families_and_distinguishes_muse_products(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    rows = {
        line.split("|", 2)[1].strip(): [cell.strip() for cell in line.strip("|").split("|")]
        for line in text.splitlines() if line.startswith("|")
    }
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
    table_region = text[text.index("| Claude |"):text.index("\n", text.index("| Phi |"))]
    assert all(line.startswith("|") for line in table_region.splitlines())

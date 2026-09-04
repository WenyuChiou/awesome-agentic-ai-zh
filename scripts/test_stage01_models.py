from __future__ import annotations

import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    (ROOT / "stages" / "01-llm-basics.md", "Fable 5.1：正式可用", "Mythos 5.1：限核准使用者"),
    (ROOT / "stages" / "01-llm-basics.zh-Hans.md", "Fable 5.1：正式可用", "Mythos 5.1：限核准用户"),
    (ROOT / "stages" / "01-llm-basics.en.md", "Fable 5.1: generally available", "Mythos 5.1: vetted access only"),
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
    assert "https://platform.claude.com/docs/en/models/fable-5-1/overview" in cells[7]
    assert "https://platform.claude.com/docs/en/models/mythos-5-1/overview" in cells[7]
    assert "claude-fable-5-1" in text
    assert "claude-mythos-5-1" in text
    assert not re.search(r"claude-(?:fable|mythos)-5(?!-1)", text)
    assert "verified_on=2026-09-04" in text


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
    assert "verified_on=2026-09-04" in text


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
    assert "$0.44/$0.22" in deepseek[4]
    assert "$1.32/$0.66" in deepseek[4]
    assert "$3.96/$1.98" in deepseek[4]

    hunyuan = [cell.strip() for cell in rows["Hunyuan"].strip("|").split("|")]
    assert hunyuan[3] == "256K"
    assert "2026-08-31" in hunyuan[6]
    assert "https://cloud.tencent.com/document/product/1823/130051" in hunyuan[7]

    minimax = [cell.strip() for cell in rows["MiniMax"].strip("|").split("|")]
    assert "permanent 50% off" in minimax[4] or "永久 50% 折扣" in minimax[4]
    assert "MiniMax Community License" in minimax[4]
    assert "https://huggingface.co/MiniMaxAI/MiniMax-M3" in minimax[7]

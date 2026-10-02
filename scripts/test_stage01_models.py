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
    row = next(line for line in text.splitlines() if line.startswith("| GPT |"))
    cells = [cell.strip() for cell in row.strip("|").split("|")]

    assert len(cells) == 8
    for model in ("gpt-6-astra", "gpt-6.1-sol", "gpt-6-luna"):
        assert model in cells[1]
        assert f"https://developers.openai.com/api/docs/models/{model}" in cells[7]
    assert "GPT-5.6" not in cells[1]
    assert "1.05M" in cells[3]
    assert "128K" in cells[3]
    assert "Standard" in cells[4]
    assert "$10/$1/$12.50/$50" in cells[4]
    assert "$2/$0.10/$2.50/$10" in cells[4]
    assert "$0.10/$0.01/$0.125/$0.50" in cells[4]
    assert "272K" in cells[6]
    assert "1.5" in cells[6]
    assert "https://developers.openai.com/api/docs/pricing" in cells[7]
    assert "GPT-6.1 Sol" in text.split("<details", maxsplit=1)[0]
    assert "2026-10-02 UTC" in text
    assert "verified_on=2026-09-22" in text


def test_stage01_fact_pack_separates_full_table_and_gpt_update_dates() -> None:
    fact_pack = (ROOT / "scripts" / "freshness-models.yml").read_text(encoding="utf-8")
    assert "verified_on: '2026-09-22'" in fact_pack
    assert "gpt: '2026-10-02'" in fact_pack
    assert "gemini: '2026-10-02'" in fact_pack
    assert "anthropic: '2026-09-28'" in fact_pack
    assert "claude_sonnet: 'https://platform.claude.com/docs/en/models/sonnet-5-5/overview'" in fact_pack
    assert "gpt: 'https://developers.openai.com/api/docs/pricing'" in fact_pack


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


@pytest.mark.parametrize("page", [item[0] for item in PAGES])
def test_stage01_gpt61_has_exact_id_and_responses_tool_boundary(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if line.startswith("| GPT |"))
    cells = [cell.strip() for cell in row.strip("|").split("|")]
    assert "gpt-6.1-sol" in cells[1]
    assert "`gpt-6-sol`" not in cells[1]
    required_boundary = {
        "01-llm-basics.md": ("工具呼叫須用 Responses API", "Chat Completions 不支援工具呼叫"),
        "01-llm-basics.en.md": ("tool calling requires Responses API", "Chat Completions has no tool calling"),
        "01-llm-basics.zh-Hans.md": ("工具调用须用 Responses API", "Chat Completions 不支持工具调用"),
    }[page.name]
    assert all(token in cells[6] for token in required_boundary)
    assert "Sora" not in row
    assert "https://developers.openai.com/api/docs/models/gpt-6.1-sol" in cells[7]


@pytest.mark.parametrize("page", [item[0] for item in PAGES])
def test_stage01_argon_is_restricted_and_not_a_guessed_api_default(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if line.startswith("| Gemini |"))
    cells = [cell.strip() for cell in row.strip("|").split("|")]
    assert "Gemini 3.8 Flash" in cells[1] and "Gemini 4 Argon" in cells[1]
    restricted, output_limit, no_context, forthcoming, no_id = {
        "01-llm-basics.md": (
            "Argon：限 Fairwind 可信資安防禦者", "Argon：公告 1M 輸出上限",
            "公開 API context 規格未公布", "一般 API／Google AI Ultra 開放仍待後續發布",
            "公開 API model ID 未公布",
        ),
        "01-llm-basics.en.md": (
            "Argon: trusted cyber defenders through Fairwind only", "Argon: announced 1M output limit",
            "public API context specification not announced", "API / Google AI Ultra access is still forthcoming",
            "no public API model ID has been announced",
        ),
        "01-llm-basics.zh-Hans.md": (
            "Argon：限 Fairwind 可信网络安全防御者", "Argon：公告 1M 输出上限",
            "公开 API context 规格未公布", "一般 API／Google AI Ultra 开放仍待后续发布",
            "公开 API model ID 未公布",
        ),
    }[page.name]
    assert any(label in cells[1] for label in ("發布參考", "发布参考", "release reference"))
    assert restricted in cells[2]
    assert output_limit in cells[3] and no_context in cells[3]
    assert forthcoming in cells[6] and no_id in cells[6]
    assert "$2/$10" in cells[4] and "$4/$20" in cells[4]
    assert "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/" in cells[7]
    assert not re.search(r"`gemini-4[^`]*`", row)
    visible_selector = text.split("<details", maxsplit=1)[0]
    assert "Gemini 3.8 Flash" in visible_selector
    assert "Gemini 4 Argon" not in visible_selector


@pytest.mark.parametrize("page", [item[0] for item in PAGES if item[0].suffix == ".md" and ".en." not in item[0].name])
def test_refreshed_model_row_sentences_fit_written_chinese_style(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    for family in ("GPT", "Gemini"):
        row = next(line for line in text.splitlines() if line.startswith(f"| {family} |"))
        # Exclude model-name lists and official-link lists. For descriptive,
        # specification, and pricing cells count rendered text, not link URLs.
        for cell in row.strip("|").split("|")[2:7]:
            visible = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", cell)
            visible = visible.replace("**", "").replace("`", "")
            for sentence in re.split(r"(?<=[。！？])", visible):
                if sentence.strip():
                    assert len(sentence.strip()) <= 60, sentence


@pytest.mark.parametrize("page", [item[0] for item in PAGES if ".en." not in item[0].name])
def test_refreshed_model_review_date_sentences_fit_written_style(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    summary = next(line for line in text.splitlines() if line.startswith("<small>") and "2026-10-02 UTC" in line)
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

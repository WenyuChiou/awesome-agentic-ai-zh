"""Beginner path, anchor, terminology, and freshness contracts for the glossary."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "zh-TW": ROOT / "resources/glossary.md",
    "en": ROOT / "resources/glossary.en.md",
    "zh-Hans": ROOT / "resources/glossary.zh-Hans.md",
}

PUBLISHED_TERMS = (
    "LLM",
    "Model Provider / Provider API",
    "LLM Router / API Router",
    "Token",
    "Context Window",
    "Prompt",
    "Zero-shot / One-shot / Few-shot",
    "Chain-of-Thought",
    "Agent",
    "Tool Use / Function Calling",
    "Tool Schema",
    "Tool Call",
    "Tool Result",
    "ReAct",
    "Structured Output",
    "Agent Loop",
    "Self-Refine",
    "Memory",
    "RAG",
    "Reflexion",
    "Embedding",
    "Vector DB",
    "Semantic Search",
    "Chunking",
    "Hybrid Search",
    "Reranking",
    "Contextual Retrieval",
    "Fine-tuning",
    "Multi-Agent",
    "Handoff",
    "A2A",
    "MCP",
    "Project Instructions",
    "Skills / SKILL.md",
    "One-off Prompt",
    "Plugin / Marketplace",
    "Slash Command",
    "CLAUDE.md",
    "Hooks",
    "Deep Agent",
    "Subagent",
    "CI",
    "Eval",
    "Observability",
    "Prompt Caching",
    "Streaming",
    "Batch API",
    "Token Cost / Inference Cost",
    "Guardrails",
    "Prompt Injection",
    "Lethal Trifecta",
    "CLI Agent",
    "BYO API Key",
    "Local LLM / On-Device",
    "Quantization",
    "Hallucination",
    "Frontier Model",
    "Context Engineering",
    "Agent Production Engineering",
    "Harness Engineering",
    "Loop Engineering",
    "Graph Engineering",
    "Computer Use",
    "Browser Use",
    "Sandbox",
    "microVM",
    "Firecracker",
    "gVisor",
)
NEW_TERMS = ("Model Runtime", "Workflow Graph", "Agent Harness")
MODEL_LIFECYCLE_TERMS = (
    "Pre-training",
    "Post-training",
    "Inference",
    "SFT",
    "DPO",
    "RLHF / RL",
    "GRPO",
    "PEFT / LoRA",
    "Distillation",
)
CORE_TERMS = (
    "Prompt",
    "Token",
    "Context Window",
    "Agent",
    "Tool Use",
    "Agent Loop",
    "RAG",
    "Memory",
    "MCP",
    "Eval",
    "Agent Harness",
    "Workflow Graph",
)
IDENTITY_URLS = (
    "https://platform.claude.com/docs/en/api/overview",
    "https://openrouter.ai/docs/faq",
    "https://docs.ollama.com/api/introduction",
    "https://opencode.ai/docs",
    "https://github.com/earendil-works/pi",
    "https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/",
)
FRESHNESS = (
    "<!-- freshness: canonical=resources/glossary.md; "
    "verified_on=2026-08-31; "
    "scope=protocols,product-identities,terminology,official-links,model-lifecycle; "
    "max_age_days=90 -->"
)


def _without_details(text: str) -> str:
    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.DOTALL)


def _section(text: str, start: str, end: str) -> str:
    return text[text.index(start) : text.index(end)]


@pytest.mark.parametrize("locale", PAGES)
def test_glossary_has_a_visible_beginner_lookup_path(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    headings = {
        "zh-TW": (
            "## ⚡ 先從 12 個詞開始",
            "## 🧭 先分清五種工具身分",
            "## 📚 依主題查詞",
            "## 找不到的詞？",
        ),
        "en": (
            "## ⚡ Start with these 12 terms",
            "## 🧭 Separate five tool identities first",
            "## 📚 Look up terms by topic",
            "## Cannot find a term?",
        ),
        "zh-Hans": (
            "## ⚡ 先从 12 个词开始",
            "## 🧭 先分清五种工具身份",
            "## 📚 按主题查词",
            "## 找不到的词？",
        ),
    }[locale]
    positions = [visible.index(heading) for heading in headings]
    assert positions == sorted(positions)

    quick_map = _section(visible, headings[0], headings[1])
    assert len(re.findall(r"\]\(#[^)]+\)", quick_map)) == 12
    for term in CORE_TERMS:
        assert f"**{term}" in quick_map

    identity_table = _section(visible, headings[1], headings[2])
    assert len(re.findall(r"<tr>", identity_table)) == 6
    for url in IDENTITY_URLS:
        assert url in identity_table


@pytest.mark.parametrize("page", PAGES.values())
def test_every_published_term_and_new_boundary_term_stays_visible(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    visible = _without_details(text)
    headings = re.findall(r"^### (.+)$", visible, flags=re.MULTILINE)
    assert len(headings) == 80
    for term in (*PUBLISHED_TERMS, *NEW_TERMS, *MODEL_LIFECYCLE_TERMS):
        assert any(heading.startswith(term) for heading in headings), term


@pytest.mark.parametrize("page", PAGES.values())
def test_only_maintenance_and_sources_are_collapsed(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    openings = re.findall(r"^<details\b[^>]*>", text, flags=re.MULTILINE)
    assert openings == ['<details markdown="1">'] * 2
    assert not re.search(r"<details\b[^>]*\bopen\b", text)

    first_details = re.search(r"<details.*?</details>", text, flags=re.DOTALL).group(0)
    assert sum(int(value) for value in re.findall(r'rowspan="(\d+)"', first_details)) == 37
    assert len(re.findall(r'<th scope="rowgroup"', first_details)) == 5


def test_three_locales_share_official_urls_and_freshness_marker() -> None:
    external_orders = []
    for page in PAGES.values():
        text = page.read_text(encoding="utf-8")
        assert text.count(FRESHNESS) == 1
        external_orders.append(tuple(re.findall(r"https://[^)\s<>\"']+", text)))
    assert len(set(external_orders)) == 1


@pytest.mark.parametrize("page", PAGES.values())
def test_volatile_or_misleading_glossary_snapshots_do_not_return(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    forbidden = (
        "1.5-2 token",
        "1.3 token",
        "75 萬中文字",
        "75 万中文字",
        "750,000 Chinese",
        "GPT-5.6",
        "Claude Opus 5",
        "Gemini 3.5",
        "DeepSeek-V4",
        "Fable 5",
        "v1.0",
        "150+",
        "7 種事件",
        "7 种事件",
        "seven event types",
        "Prompt engineering 的下一層",
        "Prompt engineering 的下一层",
        "next layer after prompt engineering",
        "90% off",
        "50% off",
        "5 折",
        '""',
        "“”",
    )
    assert not any(value in text for value in forbidden)
    assert not re.search(r"\b(?:Prompt|Context|Harness|Loop|Graph)\s*[→>]\s*", text)


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_runtime_and_prompt_cache_definitions_keep_current_boundaries(
    locale: str, page: Path
) -> None:
    text = page.read_text(encoding="utf-8")
    runtime = _section(text, "### Model Runtime", "### Token")
    assert "[MLX LM](https://github.com/ml-explore/mlx-lm)" in runtime
    assert "MLX" in runtime and "array framework" in runtime

    caching = _section(text, "### Prompt Caching", "### Streaming")
    assert "https://platform.claude.com/docs/en/build-with-claude/prompt-caching" in caching
    required = {
        "zh-TW": ("內容完全相同", "相似但不同的內容不算命中"),
        "en": ("byte-identical", "similar but different content is a cache miss"),
        "zh-Hans": ("内容完全相同", "相似但不同的内容不会命中"),
    }[locale]
    assert all(marker in caching for marker in required)


def test_subagent_deep_links_keep_their_published_fragments() -> None:
    expected = {
        "zh-TW": "### Subagent（子 agent）",
        "en": "### Subagent",
        "zh-Hans": "### Subagent（子 agent）",
    }
    for locale, heading in expected.items():
        assert heading in PAGES[locale].read_text(encoding="utf-8")


def test_freshness_config_enrols_the_glossary_fact_pack_and_page() -> None:
    config = yaml.safe_load((ROOT / "scripts/freshness-models.yml").read_text(encoding="utf-8"))
    pack = config["glossary_fact_pack"]
    assert pack["canonical"] == "resources/glossary.md"
    assert pack["verified_on"] == "2026-08-31"
    assert pack["scope"] == [
        "protocols",
        "product-identities",
        "terminology",
        "official-links",
        "model-lifecycle",
    ]
    assert pack["official_sources"]["mlx_lm"] == "https://github.com/ml-explore/mlx-lm"
    assert pack["official_sources"]["claude_prompt_caching"] == (
        "https://platform.claude.com/docs/en/build-with-claude/prompt-caching"
    )

    page = next(
        item
        for item in config["verified_pages"]
        if item["canonical"] == "resources/glossary.md"
    )
    assert page["required_scopes"] == pack["scope"]
    assert page["max_age_days"] == 90

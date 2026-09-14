"""Cross-chapter entry/deepening checks for Agent Loop and workflow graphs."""

from __future__ import annotations

from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "zh-TW": (
        ROOT / "stages/03-tool-use-and-hello-agent.md",
        ROOT / "stages/04-agent-frameworks.md",
    ),
    "en": (
        ROOT / "stages/03-tool-use-and-hello-agent.en.md",
        ROOT / "stages/04-agent-frameworks.en.md",
    ),
    "zh-Hans": (
        ROOT / "stages/03-tool-use-and-hello-agent.zh-Hans.md",
        ROOT / "stages/04-agent-frameworks.zh-Hans.md",
    ),
}
GLOSSARIES = {
    "zh-TW": ROOT / "resources/glossary.md",
    "en": ROOT / "resources/glossary.en.md",
    "zh-Hans": ROOT / "resources/glossary.zh-Hans.md",
}
GLOSSARY_MARKERS = {
    "zh-TW": (
        "### Agent Production Engineering",
        "學習順序是 [Stage 3 的 Agent Loop](../stages/03-tool-use-and-hello-agent.md) → [Stage 4 的 Workflow Graph／Agent Framework](../stages/04-agent-frameworks.md) → [Stage 7 的 Agent Production Engineering](../stages/07-multi-agent-production.md)",
        "Prompt、Context、Harness、Loop、Graph 會一起工作；它們不是五層",
        "同一個 Harness 可以包含 Agent Loop",
        "而不是取代它們",
        "不是所有供應商共同採用的標準",
    ),
    "en": (
        "### Agent Production Engineering",
        "The learning order is [Stage 3 Agent Loop](../stages/03-tool-use-and-hello-agent.en.md) → [Stage 4 Workflow Graph / Agent Framework](../stages/04-agent-frameworks.en.md) → [Stage 7 Agent Production Engineering](../stages/07-multi-agent-production.en.md)",
        "Prompt, Context, Harness, Loop, and Graph work together; they are not five layers",
        "the same Harness may contain an Agent Loop",
        "instead of replacing them",
        "not a cross-vendor standard",
    ),
    "zh-Hans": (
        "### Agent Production Engineering",
        "学习顺序是 [Stage 3 的 Agent Loop](../stages/03-tool-use-and-hello-agent.zh-Hans.md) → [Stage 4 的 Workflow Graph／Agent Framework](../stages/04-agent-frameworks.zh-Hans.md) → [Stage 7 的 Agent Production Engineering](../stages/07-multi-agent-production.zh-Hans.md)",
        "Prompt、Context、Harness、Loop、Graph 会一起工作；它们不是五层",
        "同一个 Harness 可以包含 Agent Loop",
        "而不是替代它们",
        "不是所有供应商共同采用的标准",
    ),
}
GLOSSARY_FORBIDDEN = {
    "zh-TW": ("這是正在形成的名稱", "Stage 7 Harness Engineering"),
    "en": ("This name is still emerging", "Stage 7 Harness Engineering"),
    "zh-Hans": ("这是正在形成的名称", "Stage 7 Harness Engineering"),
}
GLOSSARY_SOURCE_URLS = (
    "https://openai.com/index/harness-engineering/",
    "https://www.ibm.com/think/topics/loop-engineering",
    "https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/",
    "https://arxiv.org/abs/2608.21156",
)


@pytest.mark.parametrize("locale,pages", PAGES.items())
def test_existing_entry_chapters_support_the_stage7_route(
    locale: str, pages: tuple[Path, Path]
) -> None:
    stage3, stage4 = (page.read_text(encoding="utf-8") for page in pages)
    assert "**Agent Loop" in stage3
    assert "Workflow" in stage4
    assert "Graph" in stage4


@pytest.mark.parametrize("pages", PAGES.values())
def test_graph_engineering_is_not_misdefined_as_knowledge_graph(
    pages: tuple[Path, Path]
) -> None:
    _stage3, stage4 = (page.read_text(encoding="utf-8") for page in pages)
    assert "GraphRAG" not in stage4


@pytest.mark.parametrize("locale,glossary", GLOSSARIES.items())
def test_glossary_keeps_loop_and_graph_boundaries_current(
    locale: str, glossary: Path
) -> None:
    text = glossary.read_text(encoding="utf-8")
    assert all(marker in text for marker in GLOSSARY_MARKERS[locale])
    assert all(url in text for url in GLOSSARY_SOURCE_URLS)
    assert all(term not in text for term in GLOSSARY_FORBIDDEN[locale])

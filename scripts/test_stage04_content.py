"""Stage 03→04 Agent Loop, framework, and workflow-graph route checks."""

from __future__ import annotations

import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
STAGE3 = {
    "zh-TW": ROOT / "stages/03-tool-use-and-hello-agent.md",
    "en": ROOT / "stages/03-tool-use-and-hello-agent.en.md",
    "zh-Hans": ROOT / "stages/03-tool-use-and-hello-agent.zh-Hans.md",
}
STAGE4 = {
    "zh-TW": ROOT / "stages/04-agent-frameworks.md",
    "en": ROOT / "stages/04-agent-frameworks.en.md",
    "zh-Hans": ROOT / "stages/04-agent-frameworks.zh-Hans.md",
}
STAGE3_TITLES = {
    "zh-TW": "# Stage 3 — 工具使用與第一個 Agent Loop ⭐",
    "en": "# Stage 3 — Tool Use & Your First Agent Loop ⭐",
    "zh-Hans": "# Stage 3 — 工具使用与第一个 Agent Loop ⭐",
}
STAGE4_TITLES = {
    "zh-TW": "# Stage 4 — Workflow Graph 與 Agent 框架",
    "en": "# Stage 4 — Workflow Graphs & Agent Frameworks",
    "zh-Hans": "# Stage 4 — Workflow Graph 与 Agent 框架",
}
STAGE4_LEGACY_FRAMEWORK_ANCHORS = {
    "zh-TW": '-什麼是-multi-agent-framework',
    "en": '-what-is-a-multi-agent-framework',
    "zh-Hans": '-什么是-multi-agent-framework',
}
STAGE3_READING_URLS = (
    "https://docs.ollama.com/capabilities/tool-calling",
    "https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works",
    "https://arxiv.org/abs/2210.03629",
)
STAGE4_READING_URLS = (
    "https://www.anthropic.com/engineering/building-effective-agents",
    "https://docs.langchain.com/oss/python/langgraph/workflows-agents",
    "https://openai.github.io/openai-agents-python/multi_agent/",
    "https://docs.langchain.com/oss/python/langgraph/overview",
    "https://docs.crewai.com/",
)
STAGE4_PROJECT_COUNT_TEXT = {
    "zh-TW": ("19 個專案", "19 筆表格"),
    "en": ("19 projects", "19-row table"),
    "zh-Hans": ("19 个项目", "19 笔表格"),
}
BRIDGE_LABELS = (
    "Agent Loop",
    "Agent Framework",
    "Workflow Graph",
    "Loop Engineering",
    "Graph Engineering",
)
EXAMPLE_LINK_LABELS = {
    "zh-TW": (
        "Stage 3 — 工具使用與第一個 Agent Loop",
        "Stage 4 — Workflow Graph 與 Agent 框架",
    ),
    "en": (
        "Stage 3 — Tool Use & Your First Agent Loop",
        "Stage 4 — Workflow Graphs & Agent Frameworks",
    ),
    "zh-Hans": (
        "Stage 3 — 工具使用与第一个 Agent Loop",
        "Stage 4 — Workflow Graph 与 Agent 框架",
    ),
}


def _without_closed_details(text: str) -> str:
    return re.sub(
        r"<details(?![^>]*\bopen\b)[^>]*>.*?</details>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )


@pytest.mark.parametrize("locale,page", STAGE3.items())
def test_stage3_title_and_agent_loop_definition_are_visible(
    locale: str, page: Path
) -> None:
    text = page.read_text(encoding="utf-8")
    visible = _without_closed_details(text)
    assert text.startswith(STAGE3_TITLES[locale])
    assert "model → tool call → execute → tool result → model" in visible
    assert visible.index("Agent Loop") < visible.index("Exercise 1" if locale == "en" else "練習 1" if locale == "zh-TW" else "练习 1")


@pytest.mark.parametrize("locale,page", STAGE4.items())
def test_stage4_title_and_framework_graph_bridge_are_visible(
    locale: str, page: Path
) -> None:
    text = page.read_text(encoding="utf-8")
    visible = _without_closed_details(text)
    assert text.startswith(STAGE4_TITLES[locale])
    assert "model → tool call → execute → tool result → model" in visible
    assert all(f"**{label}" in visible for label in BRIDGE_LABELS)
    assert "toolbox" in visible.lower() or "工具箱" in visible
    assert "design" in visible.lower() or "設計" in visible or "设计" in visible
    assert "Multi-Agent" in visible
    assert f'id="{STAGE4_LEGACY_FRAMEWORK_ANCHORS[locale]}"' in text


@pytest.mark.parametrize("page", STAGE3.values())
def test_stage3_required_reading_and_all_rated_resources_are_visible(
    page: Path,
) -> None:
    visible = _without_closed_details(page.read_text(encoding="utf-8"))
    assert all(url in visible for url in STAGE3_READING_URLS)
    projects = visible[visible.index("## 🎯") :]
    table = re.search(r"<table>.*?</table>", projects, flags=re.DOTALL)
    assert table
    assert len(re.findall(r"<td>⭐{2,5}</td>", table.group())) == 21
    assert 'scope="rowgroup"' in table.group()


@pytest.mark.parametrize("locale,page", STAGE4.items())
def test_stage4_required_reading_and_all_rated_resources_are_visible(
    locale: str, page: Path,
) -> None:
    source = page.read_text(encoding="utf-8")
    visible = _without_closed_details(source)
    assert all(url in visible for url in STAGE4_READING_URLS)
    assert all(text in source for text in STAGE4_PROJECT_COUNT_TEXT[locale])
    projects = visible[visible.index("## 🎯") :]
    table = re.search(r"<table>.*?</table>", projects, flags=re.DOTALL)
    assert table
    table_html = table.group()
    assert len(
        re.findall(r"<td>⭐{2,5}[^<]*</td>", table_html)
    ) == 19
    assert "https://github.com/maximhq/bifrost" in table_html
    assert "https://github.com/BerriAI/litellm" in table_html
    assert 'scope="rowgroup"' in table_html


@pytest.mark.parametrize("page", STAGE4.values())
def test_agent_framework_is_not_defined_as_multi_agent_only(page: Path) -> None:
    visible = _without_closed_details(page.read_text(encoding="utf-8"))
    assert "multi-agent framework?" not in visible.lower()
    assert "multi-agent framework？" not in visible.lower()
    assert "one Agent" in visible or "一個 Agent" in visible or "一个 Agent" in visible


@pytest.mark.parametrize("locale,suffix", (("zh-TW", ""), ("en", ".en"), ("zh-Hans", ".zh-Hans")))
def test_direct_example_return_labels_match_localized_stage_titles(
    locale: str, suffix: str
) -> None:
    stage3 = ROOT / f"examples/stage-3/01-function-calling/README{suffix}.md"
    stage3_label, stage4_label = EXAMPLE_LINK_LABELS[locale]
    assert f"[{stage3_label}]" in stage3.read_text(encoding="utf-8")

    for example in sorted((ROOT / "examples/stage-4").glob("*/README.md")):
        localized = example.with_name(f"README{suffix}.md")
        assert f"[{stage4_label}]" in localized.read_text(encoding="utf-8")


def test_mdbook_summary_generator_uses_current_canonical_titles() -> None:
    script = (ROOT / "scripts/build-mdbook.sh").read_text(encoding="utf-8")
    assert "[Stage 3 — 工具使用與第一個 Agent Loop](stages/03-tool-use-and-hello-agent.md)" in script
    assert "[Stage 4 — Workflow Graph 與 Agent 框架](stages/04-agent-frameworks.md)" in script
    assert "Stage 3 — Tool Use & Hello Agent" not in script
    assert "[Stage 4 — Agent 框架](stages/04-agent-frameworks.md)" not in script


@pytest.mark.parametrize("page", STAGE4.values())
def test_visible_resource_copy_does_not_claim_visible_lists_are_collapsed(
    page: Path,
) -> None:
    text = page.read_text(encoding="utf-8")
    stale_claims = (
        "完整清單預設收合",
        "The full list is collapsed by default",
        "完整清单默认收起",
        "其他 17 筆依用途收合",
        "The other 17 entries are collapsed by purpose",
        "其他 17 笔依用途收合",
    )
    assert not any(claim in text for claim in stale_claims)

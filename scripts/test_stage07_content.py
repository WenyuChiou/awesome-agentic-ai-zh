"""Stage 07 reader path, current-fact, diagram, and locale regression checks."""

from __future__ import annotations

import hashlib
import re
import struct
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "zh-TW": ROOT / "stages/07-multi-agent-production.md",
    "en": ROOT / "stages/07-multi-agent-production.en.md",
    "zh-Hans": ROOT / "stages/07-multi-agent-production.zh-Hans.md",
}
DIAGRAMS = {
    "zh-TW": (
        ROOT / "resources/diagrams/agent-engineering-control-questions.png",
        ROOT / "resources/diagrams/inside-a-graph.png",
    ),
    "en": (
        ROOT / "resources/diagrams/agent-engineering-control-questions.en.png",
        ROOT / "resources/diagrams/inside-a-graph.en.png",
    ),
    "zh-Hans": (
        ROOT / "resources/diagrams/agent-engineering-control-questions.zh-Hans.png",
        ROOT / "resources/diagrams/inside-a-graph.zh-Hans.png",
    ),
}
CONTROL_DIAGRAM_ALT_MARKERS = {
    "zh-TW": (
        "Harness 內含 Agent Loop",
        "Workflow Graph 排整條路",
        "Loop Engineering 依證據調整",
    ),
    "en": (
        "Harness contains the Agent Loop",
        "Workflow Graph arranges the route",
        "Loop Engineering adjusts from evidence",
    ),
    "zh-Hans": (
        "Harness 内含 Agent Loop",
        "Workflow Graph 排整条路线",
        "Loop Engineering 根据证据调整",
    ),
}
CORE_LABELS = {
    "zh-TW": (
        "Eval（評測）",
        "Outcome（結果）",
        "Trajectory（軌跡）",
        "Observability（可觀測性）",
        "Guardrail（護欄）",
        "Human Approval（人工核准）",
        "Checkpoint（檢查點）",
        "Resume（續跑）",
        "Recovery（復原）",
        "Idempotency（冪等）",
        "Harness",
        "Loop Engineering",
        "Graph Engineering",
        "Orchestration",
        "Multi-Agent（多 Agent）",
        "Handoff",
    ),
    "en": (
        "Eval",
        "Outcome",
        "Trajectory",
        "Observability",
        "Guardrail",
        "Human Approval",
        "Checkpoint",
        "Resume",
        "Recovery",
        "Idempotency",
        "Harness",
        "Loop Engineering",
        "Graph Engineering",
        "Orchestration",
        "Multi-Agent",
        "Handoff",
    ),
    "zh-Hans": (
        "Eval（评测）",
        "Outcome（结果）",
        "Trajectory（轨迹）",
        "Observability（可观测性）",
        "Guardrail（护栏）",
        "Human Approval（人工批准）",
        "Checkpoint（检查点）",
        "Resume（续跑）",
        "Recovery（恢复）",
        "Idempotency（幂等）",
        "Harness",
        "Loop Engineering",
        "Graph Engineering",
        "Orchestration",
        "Multi-Agent（多 Agent）",
        "Handoff",
    ),
}
CORE_SECTION_HEADINGS = {
    "zh-TW": ("## 🧩 十六個核心詞（分三組讀）", "## 🚪 進入條件"),
    "en": ("## 🧩 Sixteen Core Terms (Read Them in Three Groups)", "## 🚪 Entry Conditions"),
    "zh-Hans": ("## 🧩 十六个核心词（分三组读）", "## 🚪 进入条件"),
}
PAGE_TITLES = {
    "zh-TW": "# Stage 7 — Agent Production Engineering：Harness、Loop 與 Graph",
    "en": "# Stage 7 — Agent Production Engineering: Harness, Loops, and Graphs",
    "zh-Hans": "# Stage 7 — Agent Production Engineering：Harness、Loop 与 Graph",
}
OLD_PAGE_TITLES = {
    "zh-TW": "# Stage 7 — Loop／Graph Engineering：多 Agent 與穩定運作",
    "en": "# Stage 7 — Loop & Graph Engineering: Multi-Agent Production",
    "zh-Hans": "# Stage 7 — Loop／Graph Engineering：多 Agent 与稳定运行",
}
EXERCISE_DIRS = (
    "01-multi-agent-debate",
    "02-eval",
    "03-observability",
    "04-sdk-advanced",
    "05-deploy",
    "06-safe-execution",
)
CORE_EXERCISE_DIRS = (
    "02-eval",
    "03-observability",
    "06-safe-execution",
    "05-deploy",
)
CURRENT_FACT_URLS = {
    "https://openai.github.io/openai-agents-python/running_agents/",
    "https://openai.github.io/openai-agents-python/multi_agent/",
    "https://www.ibm.com/think/topics/loop-engineering",
    "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents",
    "https://openai.github.io/openai-agents-python/tracing/",
    "https://openai.github.io/openai-agents-python/human_in_the_loop/",
    "https://docs.langchain.com/oss/python/langgraph/persistence",
    "https://docs.langchain.com/oss/python/langgraph/interrupts",
    "https://docs.langchain.com/oss/python/langgraph/workflows-agents",
    "https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/",
    "https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/builder-and-execution",
    "https://openai.com/index/harness-engineering/",
    "https://www.anthropic.com/engineering/managed-agents",
    "https://www.anthropic.com/engineering/harness-design-long-running-apps",
    "https://platform.claude.com/docs/en/test-and-evaluate/develop-tests",
    "https://github.com/open-telemetry/semantic-conventions-genai",
    "https://github.com/earendil-works/pi",
    "https://github.com/anomalyco/opencode",
    "https://github.com/stablyai/orca",
    "https://github.com/yc-software/qm",
}
REQUIRED_READING_URLS = (
    "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents",
    "https://openai.github.io/openai-agents-python/tracing/",
    "https://openai.github.io/openai-agents-python/human_in_the_loop/",
    "https://docs.langchain.com/oss/python/langgraph/persistence",
    "https://docs.langchain.com/oss/python/langgraph/interrupts",
    "https://www.anthropic.com/engineering/building-effective-agents",
)
FORBIDDEN_TERMINOLOGY = (
    "Loop Engineering（本專案教學用語）",
    "Graph Engineering（本專案教學用語）",
    "Loop Engineering (a teaching term in this project)",
    "Graph Engineering (a teaching term in this project)",
    "Loop Engineering（本项目教学用语）",
    "Graph Engineering（本项目教学用语）",
)
ROUTE_MARKERS = {
    "zh-TW": (
        "Stage 3：Agent Loop 入門",
        "Stage 4：Workflow Graph 入門",
        "Stage 7：Agent Production Engineering 整合",
    ),
    "en": (
        "Stage 3: Agent Loop entry",
        "Stage 4: Workflow Graph entry",
        "Stage 7: Agent Production Engineering integration",
    ),
    "zh-Hans": (
        "Stage 3：Agent Loop 入门",
        "Stage 4：Workflow Graph 入门",
        "Stage 7：Agent Production Engineering 整合",
    ),
}
RESOURCE_URL_RATINGS = (
    ("https://www.anthropic.com/engineering/building-effective-agents", "⭐⭐⭐⭐⭐"),
    ("https://openai.github.io/openai-agents-python/multi_agent/", "⭐⭐⭐⭐⭐"),
    ("https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/", "⭐⭐⭐⭐"),
    ("https://github.com/langchain-ai/langgraph", "⭐⭐⭐⭐⭐"),
    ("https://platform.claude.com/docs/en/test-and-evaluate/develop-tests", "⭐⭐⭐⭐⭐"),
    ("https://github.com/promptfoo/promptfoo", "⭐⭐⭐⭐⭐"),
    ("https://github.com/open-telemetry/semantic-conventions-genai", "⭐⭐⭐⭐"),
    ("https://github.com/langfuse/langfuse", "⭐⭐⭐⭐⭐"),
    ("https://github.com/Arize-ai/phoenix", "⭐⭐⭐⭐"),
    ("https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents", "⭐⭐⭐⭐⭐"),
    ("https://github.com/anthropics/claude-agent-sdk-python", "⭐⭐⭐⭐⭐"),
    ("https://github.com/deepseek-ai/deepseek-harness", "⭐⭐⭐"),
    ("https://openai.github.io/openai-agents-python/human_in_the_loop/", "⭐⭐⭐⭐⭐"),
    ("https://docs.langchain.com/oss/python/langgraph/interrupts", "⭐⭐⭐⭐⭐"),
    ("https://github.com/bentoml/BentoML", "⭐⭐⭐⭐"),
    ("https://github.com/crewAIInc/crewAI", "⭐⭐⭐⭐"),
    ("https://github.com/stablyai/orca", "⭐⭐⭐⭐"),
    ("https://github.com/yc-software/qm", "⭐⭐⭐⭐"),
    ("https://github.com/AMAP-ML/LongHorizon-Harness", "⭐⭐⭐"),
    ("https://github.com/cft0808/edict", "⭐⭐⭐"),
)


def _without_closed_details(text: str) -> str:
    return re.sub(
        r"<details(?![^>]*\bopen\b)[^>]*>.*?</details>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )


def _external_urls(text: str) -> list[str]:
    return re.findall(r"https://[^\s<>)\"']+", text)


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_reader_path_has_seven_closed_disclosures(locale: str, page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    assert text.startswith(PAGE_TITLES[locale])
    assert OLD_PAGE_TITLES[locale] not in text
    assert len(re.findall(r'<details markdown="1">', text)) == 7
    assert not re.search(r"<details[^>]*\bopen\b", text)
    visible = _without_closed_details(text)
    assert "Stage 7" in visible
    assert "python test.py" in visible


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_all_core_terms_are_bold_and_defined_before_exercises(
    locale: str, page: Path
) -> None:
    text = page.read_text(encoding="utf-8")
    core_heading, next_heading = CORE_SECTION_HEADINGS[locale]
    core_start = text.index(core_heading)
    core_end = text.index(next_heading, core_start)
    core = text[core_start:core_end]
    positions = []
    for label in CORE_LABELS[locale]:
        marker = f"<strong>{label}</strong>"
        assert marker in core
        positions.append(core.index(marker))
    assert positions == sorted(positions)
    assert re.findall(r'scope="rowgroup" rowspan="(\d+)"', core) == ["4", "6", "6"]
    assert len(re.findall(r"<tr>", core)) == 17


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_control_questions_are_not_product_generations_or_chapter_numbering(
    locale: str, page: Path
) -> None:
    text = page.read_text(encoding="utf-8")
    visible = _without_closed_details(text)
    assert all(marker in visible for marker in ROUTE_MARKERS[locale])
    assert not any(term in text for term in FORBIDDEN_TERMINOLOGY)
    assert not re.search(
        r"^## (?:五層工程分工|五层工程分工|The Five-Layer Engineering Split)",
        text,
        flags=re.MULTILINE,
    )
    old_backpack_phrases = (
        "一次出門用的安全書包",
        "一次出门用的安全书包",
        "A safe backpack for one trip",
    )
    assert not any(phrase in text for phrase in old_backpack_phrases)


BOUNDARY_HEADINGS = {
    "zh-TW": (
        "## 🧭 Harness、Loop、Graph 各自管什麼？",
        "## 🏗 Harness Engineering",
        "## 🔁 Loop Engineering",
        "## 🗺 Workflow Graph／Production Orchestration",
    ),
    "en": (
        "## 🧭 What Does Harness, Loop, and Graph Each Control?",
        "## 🏗 Harness Engineering",
        "## 🔁 Loop Engineering",
        "## 🗺 Workflow Graph / Production Orchestration",
    ),
    "zh-Hans": (
        "## 🧭 Harness、Loop、Graph 各自管什么？",
        "## 🏗 Harness Engineering",
        "## 🔁 Loop Engineering",
        "## 🗺 Workflow Graph／Production Orchestration",
    ),
}


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_harness_loop_graph_boundaries_are_visible_and_ordered(
    locale: str, page: Path
) -> None:
    visible = _without_closed_details(page.read_text(encoding="utf-8"))
    positions = [visible.index(heading) for heading in BOUNDARY_HEADINGS[locale]]
    assert positions == sorted(positions)
    loop_names = {
        "zh-TW": ("程式迴圈", "Agent Loop", "Loop Engineering"),
        "en": ("Program loop", "Agent Loop", "Loop Engineering"),
        "zh-Hans": ("程序循环", "Agent Loop", "Loop Engineering"),
    }
    assert all(name in visible for name in loop_names[locale])
    assert "IBM" in visible
    assert "Anthropic" in visible


@pytest.mark.parametrize("page", PAGES.values())
def test_required_reading_and_featured_resources_are_visible(page: Path) -> None:
    visible = _without_closed_details(page.read_text(encoding="utf-8"))
    assert all(url in visible for url in REQUIRED_READING_URLS)
    assert all(url in visible and rating in visible for url, rating in RESOURCE_URL_RATINGS)


ENTRY_SENTENCES = {
    "zh-TW": "先做四個核心練習，再為核心練習 4 補 Docker",
    "en": "Do the four core exercises first and learn Docker for Core Exercise 4",
    "zh-Hans": "先做四个核心练习，再为核心练习 4 补 Docker",
}


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_six_real_exercises_exist_and_the_four_step_core_path_is_visible(
    locale: str, page: Path
) -> None:
    text = page.read_text(encoding="utf-8")
    visible = _without_closed_details(text)
    for folder in EXERCISE_DIRS:
        assert (ROOT / "examples/stage-7" / folder / "README.md").is_file()
    positions = []
    for folder in CORE_EXERCISE_DIRS:
        command = f"cd examples/stage-7/{folder}"
        assert command in visible
        positions.append(visible.index(command))
    assert positions == sorted(positions)
    assert "../examples/stage-7/01-multi-agent-debate/README" in visible
    assert "../examples/stage-7/04-sdk-advanced/README" in visible
    assert "cd examples/stage-7/01-multi-agent-debate" not in visible
    assert "cd examples/stage-7/04-sdk-advanced" not in visible
    assert ENTRY_SENTENCES[locale] in visible


PRODUCTION_PATH_HEADINGS = {
    "zh-TW": "## 🛡 上線四步：Eval → Observability → Approval／Recovery → Deploy",
    "en": "## 🛡 Four Release Steps: Eval → Observability → Approval / Recovery → Deploy",
    "zh-Hans": "## 🛡 上线四步：Eval → Observability → Approval／Recovery → Deploy",
}


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_production_path_is_visible_and_multi_agent_stays_optional(
    locale: str, page: Path
) -> None:
    visible = _without_closed_details(page.read_text(encoding="utf-8"))
    assert PRODUCTION_PATH_HEADINGS[locale] in visible
    assert "Outcome" in visible and "Trajectory" in visible
    core_path = visible.index(PRODUCTION_PATH_HEADINGS[locale])
    exercise_path = visible.index(CORE_EXERCISE_DIRS[0])
    optional_path = visible.index("01-multi-agent-debate")
    assert core_path < exercise_path < optional_path


def test_three_locales_have_the_same_external_urls_and_current_fact_sources() -> None:
    url_lists = {
        locale: _external_urls(page.read_text(encoding="utf-8"))
        for locale, page in PAGES.items()
    }
    assert url_lists["zh-TW"] == url_lists["en"] == url_lists["zh-Hans"]
    assert CURRENT_FACT_URLS <= set(url_lists["zh-TW"])
    for page in PAGES.values():
        assert "2026-08-31 UTC" in page.read_text(encoding="utf-8")


@pytest.mark.parametrize("page", PAGES.values())
def test_resource_table_has_accessible_merged_groups_and_20_ratings(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    tables = re.findall(r"<table>.*?</table>", text, flags=re.DOTALL)
    rated_tables = [table for table in tables if re.search(r"⭐{3,5}", table)]
    assert len(rated_tables) == 1
    table = rated_tables[0]
    assert len(re.findall(r'<th scope="col">', table)) == 5
    groups = re.findall(r"<tbody>(.*?)</tbody>", table, flags=re.DOTALL)
    expected = [4, 6, 5, 5]
    assert len(groups) == len(expected)
    for group, rows in zip(groups, expected):
        assert len(re.findall(r"<tr>", group)) == rows
        assert f'scope="rowgroup" rowspan="{rows}"' in group
    pairs = tuple(
        re.findall(
            r'<a href="([^"]+)">.*?</a></td><td>(⭐{3,5})</td>',
            table,
        )
    )
    assert pairs == RESOURCE_URL_RATINGS


@pytest.mark.parametrize("page", PAGES.values())
def test_static_leaderboard_and_stale_project_claims_are_absent(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    forbidden = (
        "benchmarkingagents.com",
        "rapidclaw.dev",
        "anthropics/anthropic-cookbook",
        "laude-institute/terminal-bench",
        "princeton-nlp/SWE-agent",
        "geekan/MetaGPT",
        "hiyouga/LLaMA-Factory",
        "langchain-ai/langserve",
        "qwen2.5:3b",
        "Prompt Caching（Anthropic-only）",
        "Fable 5",
        "Mythos 5",
        "Opus 4.8",
        '""',
        "“”",
    )
    assert not any(term in text for term in forbidden)
    assert not re.search(
        r"SOTA.{0,80}\d+(?:\.\d+)?%|\d+(?:\.\d+)?%.{0,80}SOTA",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )


def test_locale_diagrams_are_distinct_large_assets_and_referenced() -> None:
    hashes: set[str] = set()
    for locale, diagrams in DIAGRAMS.items():
        page_text = PAGES[locale].read_text(encoding="utf-8")
        assert all(marker in page_text for marker in CONTROL_DIAGRAM_ALT_MARKERS[locale])
        for diagram in diagrams:
            data = diagram.read_bytes()
            assert diagram.suffix == ".png"
            assert data.startswith(b"\x89PNG\r\n\x1a\n")
            width, height = struct.unpack(">II", data[16:24])
            assert width >= 1600 and height >= 900
            if diagram.name.startswith("agent-engineering-control-questions"):
                assert (width, height) == (1672, 941)
            hashes.add(hashlib.sha256(data).hexdigest())
            assert f"../resources/diagrams/{diagram.name}" in page_text
    assert len(hashes) == 6


def test_control_questions_use_png_only() -> None:
    diagram_dir = ROOT / "resources/diagrams"
    assert not list(diagram_dir.glob("agent-engineering-control-questions*.svg"))


def test_english_page_has_no_untranslated_cjk() -> None:
    text = PAGES["en"].read_text(encoding="utf-8")
    text = text.replace("繁體中文", "").replace("简体中文", "")
    assert re.search(r"[\u3400-\u9fff]", text) is None

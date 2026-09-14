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
        ROOT / "resources/diagrams/agent-production-relationship.png",
        ROOT / "resources/diagrams/eval-case-anatomy.png",
    ),
    "en": (
        ROOT / "resources/diagrams/agent-production-relationship.en.png",
        ROOT / "resources/diagrams/eval-case-anatomy.en.png",
    ),
    "zh-Hans": (
        ROOT / "resources/diagrams/agent-production-relationship.zh-Hans.png",
        ROOT / "resources/diagrams/eval-case-anatomy.zh-Hans.png",
    ),
}
EVAL_DIAGRAM_ALT_MARKERS = {
    "zh-TW": ("完整 Eval Case", "Input 只是其中一格"),
    "en": ("complete Eval Case", "Input is only one part"),
    "zh-Hans": ("完整 Eval Case", "Input 只是其中一格"),
}
CONTROL_DIAGRAM_ALT_MARKERS = {
    "zh-TW": (
        "Agent Harness 是工作環境",
        "Workflow Graph 是帶分支的路線",
        "Eval 是跨越三者的檢查量尺",
    ),
    "en": (
        "Agent Harness is the work environment",
        "Workflow Graph is the branching route",
        "Eval is the measuring stick across all three",
    ),
    "zh-Hans": (
        "Agent Harness 是工作环境",
        "Workflow Graph 是带分支的路线",
        "Eval 是跨越三者的检查量尺",
    ),
}
CORE_LABELS = {
    "zh-TW": (
        "Agent Harness（Agent 執行架構）",
        "Agent Loop（Agent 迴圈）",
        "Workflow Graph（工作流程圖）",
        "Orchestration（編排）",
        "Multi-Agent（多 Agent）",
        "Handoff（交接）",
        "Evaluation／Eval（評測）",
        "Outcome（結果）",
        "Trajectory（軌跡）",
        "Evaluation Harness（評測執行架構）",
        "Trace（追蹤紀錄）",
        "Observability（可觀測性）",
        "Guardrail（護欄）",
        "Human Approval（人工核准）",
        "Checkpoint（檢查點）",
        "Resume（續跑）",
        "Recovery（復原）",
        "Idempotency（冪等）",
    ),
    "en": (
        "Agent Harness",
        "Agent Loop",
        "Workflow Graph",
        "Orchestration",
        "Multi-Agent",
        "Handoff",
        "Evaluation / Eval",
        "Outcome",
        "Trajectory",
        "Evaluation Harness",
        "Trace",
        "Observability",
        "Guardrail",
        "Human Approval",
        "Checkpoint",
        "Resume",
        "Recovery",
        "Idempotency",
    ),
    "zh-Hans": (
        "Agent Harness（Agent 执行架构）",
        "Agent Loop（Agent 循环）",
        "Workflow Graph（工作流程图）",
        "Orchestration（编排）",
        "Multi-Agent（多 Agent）",
        "Handoff（交接）",
        "Evaluation／Eval（评测）",
        "Outcome（结果）",
        "Trajectory（轨迹）",
        "Evaluation Harness（评测执行架构）",
        "Trace（追踪纪录）",
        "Observability（可观测性）",
        "Guardrail（护栏）",
        "Human Approval（人工批准）",
        "Checkpoint（检查点）",
        "Resume（续跑）",
        "Recovery（恢复）",
        "Idempotency（幂等）",
    ),
}
CORE_SECTION_HEADINGS = {
    "zh-TW": ("## 🧩 先認識核心詞", "## 🚪 進入條件"),
    "en": ("## 🧩 Meet the Core Terms First", "## 🚪 Entry Conditions"),
    "zh-Hans": ("## 🧩 先认识核心词", "## 🚪 进入条件"),
}
EVAL_SECTION_HEADINGS = {
    "zh-TW": (
        "## 🧪 Eval：先說要什麼，再決定怎麼評",
        "## 🔎 Observability：出錯時看得見是哪一步",
    ),
    "en": (
        "## 🧪 Eval: State What Good Means, Then Decide How to Grade",
        "## 🔎 Observability: See Which Step Failed",
    ),
    "zh-Hans": (
        "## 🧪 Eval：先说要什么，再决定怎么评",
        "## 🔎 Observability：出错时看得见是哪一步",
    ),
}
EVAL_TEACHING_TERMS = (
    "Outcome",
    "Eval Case",
    "Eval Suite",
    "Reviewed Eval Set",
    "Golden",
    "Trial",
    "Baseline",
    "Regression",
    "Development Set",
    "Holdout Set",
)
PAGE_TITLES = {
    "zh-TW": "# Stage 7 — Agent 上線工程：可測、可看、可停、可恢復",
    "en": "# Stage 7 — Agent Production Engineering: Testable, Observable, Stoppable, and Recoverable",
    "zh-Hans": "# Stage 7 — Agent 上线工程：可测、可看、可停、可恢复",
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
    "https://platform.openai.com/docs/api-reference/graders?api-mode=chat",
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
        "Stage 3 的 Agent Loop",
        "Stage 4 的 Workflow Graph",
        "本章的安全上線整合",
    ),
    "en": (
        "Stage 3 Agent Loop",
        "Stage 4 Workflow Graph / Agent Framework",
        "safe production integration in this chapter",
    ),
    "zh-Hans": (
        "Stage 3 的 Agent Loop",
        "Stage 4 的 Workflow Graph",
        "本章的安全上线集成",
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
    ("https://github.com/sandbaseai/sandbase-harness", "⭐⭐⭐⭐"),
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
    prose = core[: core.index("<table>")]
    positions = []
    for label in CORE_LABELS[locale]:
        assert f"**{label}**" in prose
        marker = f"<strong>{label}</strong>"
        assert marker in core
        positions.append(core.index(marker))
    assert "Grader" in prose and prose.index("Grader") < prose.index("Evaluation Harness")
    assert positions == sorted(positions)
    assert re.findall(r'scope="rowgroup" rowspan="(\d+)"', core) == ["6", "6", "6"]
    assert len(re.findall(r"<tr>", core)) == 19


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_eval_case_is_complete_and_terms_follow_the_teaching_order(
    locale: str, page: Path
) -> None:
    text = page.read_text(encoding="utf-8")
    start_heading, next_heading = EVAL_SECTION_HEADINGS[locale]
    start = text.index(start_heading)
    end = text.index(next_heading, start)
    section = text[start:end]
    visible = _without_closed_details(section)
    assert start_heading in visible
    positions = [visible.index(term) for term in EVAL_TEACHING_TERMS]
    assert positions == sorted(positions)
    for field in (
        "Input",
        "Initial State",
        "Success Criteria",
        "Forbidden Actions",
        "Optional Reference Answer",
        "Grader",
        "Case Metadata",
    ):
        assert field in visible
    assert re.search(r"Golden[^\n]*(?:not input alone|不只是 input)", visible, re.I)
    assert re.search(r"Golden[^\n]*(?:training data|訓練資料|训练数据)", visible, re.I)
    assert "few-shot" in visible.lower()
    assert "20–50" in text and (
        "not a universal minimum" in text
        or "不是所有專案的硬性最低數" in text
        or "不是所有项目的硬性最低数" in text
        or "不是通用最低要求" in text
    )


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
        "## 🧭 Harness、Loop、Graph 與 Eval 怎麼合作？",
        "## 🏗 Agent Harness：先把安全工作間準備好",
        "## 🔁 Agent Loop：做一步、看結果，再決定",
        "## 🗺 Workflow Graph：遇到岔路時知道往哪走",
        "## 🧪 Eval：先說要什麼，再決定怎麼評",
        "## 🔎 Observability：出錯時看得見是哪一步",
        "## 🛑 Approval、Checkpoint、Resume 與 Recovery：先停，再安全繼續",
    ),
    "en": (
        "## 🧭 Harness, Loop, Graph, and Eval: How They Work Together",
        "## 🏗 Agent Harness: Prepare the Safe Workspace",
        "## 🔁 Agent Loop: Act, Observe, Then Decide",
        "## 🗺 Workflow Graph: Know Where to Go at a Branch",
        "## 🧪 Eval: State What Good Means, Then Decide How to Grade",
        "## 🔎 Observability: See Which Step Failed",
        "## 🛑 Approval, Checkpoint, Resume, and Recovery: Stop, Then Continue Safely",
    ),
    "zh-Hans": (
        "## 🧭 Harness、Loop、Graph 与 Eval 怎么合作？",
        "## 🏗 Agent Harness：先把安全工作间准备好",
        "## 🔁 Agent Loop：做一步、看结果，再决定",
        "## 🗺 Workflow Graph：遇到岔路时知道往哪走",
        "## 🧪 Eval：先说要什么，再决定怎么评",
        "## 🔎 Observability：出错时看得见是哪一步",
        "## 🛑 Approval、Checkpoint、Resume 与 Recovery：先停，再安全继续",
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
    "zh-TW": "## 🛡 完整上線路線：Eval → Observability → Approval／Recovery → Deploy",
    "en": "## 🛡 Complete Production Route: Eval → Observability → Approval / Recovery → Deploy",
    "zh-Hans": "## 🛡 完整上线路线：Eval → Observability → Approval／Recovery → Deploy",
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
        assert "2026-09-13 UTC" in page.read_text(encoding="utf-8")


@pytest.mark.parametrize("page", PAGES.values())
def test_resource_table_has_accessible_merged_groups_and_21_ratings(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    tables = re.findall(r"<table>.*?</table>", text, flags=re.DOTALL)
    rated_tables = [table for table in tables if re.search(r"⭐{3,5}", table)]
    assert len(rated_tables) == 1
    table = rated_tables[0]
    assert len(re.findall(r'<th scope="col">', table)) == 5
    groups = re.findall(r"<tbody>(.*?)</tbody>", table, flags=re.DOTALL)
    expected = [4, 6, 6, 5]
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
    assert "v0.x" in table


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
        "Rerun the same hold-out cases whenever you change",
        "每次更换模型、Prompt、Tool 或 Harness，都重新运行同一组 hold-out cases",
        "Start with five fixed questions",
        "先用 5 个固定题目做 baseline",
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
        assert all(marker in page_text for marker in EVAL_DIAGRAM_ALT_MARKERS[locale])
        for diagram in diagrams:
            data = diagram.read_bytes()
            assert diagram.suffix == ".png"
            assert data.startswith(b"\x89PNG\r\n\x1a\n")
            width, height = struct.unpack(">II", data[16:24])
            assert width >= 1600 and height >= 900
            assert (width, height) == (1672, 941)
            hashes.add(hashlib.sha256(data).hexdigest())
            assert f"../resources/diagrams/{diagram.name}" in page_text
    assert len(hashes) == 6


def test_new_stage7_diagrams_use_png_only() -> None:
    diagram_dir = ROOT / "resources/diagrams"
    assert not list(diagram_dir.glob("agent-production-relationship*.svg"))
    assert not list(diagram_dir.glob("eval-case-anatomy*.svg"))


def test_stage7_diagram_provenance_records_both_new_layouts() -> None:
    provenance = (ROOT / "resources/diagrams/locale-variant-prompts.md").read_text(
        encoding="utf-8"
    )
    section = provenance[provenance.index("## 2026-09-13 · Stage 7 上線工程關係與 Eval Case") :]
    assert "agent-production-relationship" in section
    assert "eval-case-anatomy" in section
    assert "Input 只是完整 Eval Case 的其中一格" in section
    assert "內建圖片生成工具沒有暴露可選 model ID" in section


def test_english_page_has_no_untranslated_cjk() -> None:
    text = PAGES["en"].read_text(encoding="utf-8")
    text = text.replace("繁體中文", "").replace("简体中文", "")
    assert re.search(r"[\u3400-\u9fff]", text) is None

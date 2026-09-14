"""Reader-facing contract for structures, engineering work, and chapter order."""

from __future__ import annotations

import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
DIAGRAM_PROMPT = ROOT / "resources/diagrams/locale-variant-prompts.md"
LOCALES = {
    "zh-TW": {
        "stage4": ROOT / "stages/04-agent-frameworks.md",
        "stage7": ROOT / "stages/07-multi-agent-production.md",
        "readme": ROOT / "README.md",
        "stage4_title": "# Stage 4 — Workflow Graph 與 Agent 框架",
        "stage7_title": "# Stage 7 — Agent 上線工程：可測、可看、可停、可恢復",
        "umbrella": "**Agent Production Engineering（Agent 上線工程）**",
        "relationship_heading": "Harness、Loop、Graph 與 Eval 怎麼合作？",
        "cross_system_eval": "Eval 可以讓 Loop 重試、讓 Graph 換路，或要求 Harness 停止",
        "readme_route": "Stage 4 先看懂 **Workflow Graph**，再用 framework 把它做出來",
        "term_status": "**Loop Engineering** 是 IBM 使用的新興說法",
    },
    "en": {
        "stage4": ROOT / "stages/04-agent-frameworks.en.md",
        "stage7": ROOT / "stages/07-multi-agent-production.en.md",
        "readme": ROOT / "README.en.md",
        "stage4_title": "# Stage 4 — Workflow Graphs & Agent Frameworks",
        "stage7_title": "# Stage 7 — Agent Production Engineering: Testable, Observable, Stoppable, and Recoverable",
        "umbrella": "**Agent Production Engineering**",
        "relationship_heading": "Harness, Loop, Graph, and Eval: How They Work Together",
        "cross_system_eval": "Eval can make the Loop retry, make the Graph choose another route, or make the Harness stop",
        "readme_route": "Stage 4 first explains the **Workflow Graph**, then uses a framework to build it",
        "term_status": "**Loop Engineering** is an emerging label used by IBM",
    },
    "zh-Hans": {
        "stage4": ROOT / "stages/04-agent-frameworks.zh-Hans.md",
        "stage7": ROOT / "stages/07-multi-agent-production.zh-Hans.md",
        "readme": ROOT / "README.zh-Hans.md",
        "stage4_title": "# Stage 4 — Workflow Graph 与 Agent 框架",
        "stage7_title": "# Stage 7 — Agent 上线工程：可测、可看、可停、可恢复",
        "umbrella": "**Agent Production Engineering（Agent 上线工程）**",
        "relationship_heading": "Harness、Loop、Graph 与 Eval 怎么合作？",
        "cross_system_eval": "Eval 可以让 Loop 重试、让 Graph 换路，或要求 Harness 停止",
        "readme_route": "Stage 4 先看懂 **Workflow Graph**，再用 framework 把它做出来",
        "term_status": "**Loop Engineering** 是 IBM 使用的新兴说法",
    },
}

def without_closed_details(text: str) -> str:
    return re.sub(
        r"<details(?![^>]*\bopen\b)[^>]*>.*?</details>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_chapter_titles_put_the_concept_before_the_tool_and_production_details(
    locale: str, config: dict[str, object]
) -> None:
    stage4 = Path(config["stage4"]).read_text(encoding="utf-8")
    stage7 = Path(config["stage7"]).read_text(encoding="utf-8")
    assert stage4.startswith(str(config["stage4_title"]))
    assert stage7.startswith(str(config["stage7_title"]))
    assert str(config["umbrella"]) in without_closed_details(stage7)
    assert str(config["term_status"]) in without_closed_details(stage7)
    assert "taking shape in 2026" not in stage7
    assert "2026 年正在形成" not in stage7


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_four_responsibilities_are_distinct_and_eval_crosses_the_system(
    locale: str, config: dict[str, object]
) -> None:
    stage7 = without_closed_details(
        Path(config["stage7"]).read_text(encoding="utf-8")
    )
    assert str(config["relationship_heading"]) in stage7
    relationship = stage7[stage7.index(str(config["relationship_heading"])) :]
    for responsibility in ("Agent Harness", "Agent Loop", "Workflow Graph", "Eval"):
        assert f"**{responsibility}**" in relationship
    assert str(config["cross_system_eval"]) in relationship
    assert "Harness + Eval = Loop" not in stage7
    assert "Harness 和 Eval 放在一起，仍不會自動產生" in stage7 or locale != "zh-TW"
    assert "Harness 和 Eval 放在一起，仍不会自动产生" in stage7 or locale != "zh-Hans"
    assert "Putting a Harness and Eval together still does not create" in stage7 or locale != "en"


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_stage4_teaches_workflow_graph_before_presenting_framework_as_the_toolbox(
    locale: str, config: dict[str, object]
) -> None:
    stage4 = without_closed_details(
        Path(config["stage4"]).read_text(encoding="utf-8")
    )
    graph_pos = stage4.index("**Workflow")
    framework_pos = stage4.index("**Framework")
    assert graph_pos < framework_pos, locale


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_readme_names_the_graph_before_the_framework_toolbox(
    locale: str, config: dict[str, object]
) -> None:
    readme = Path(config["readme"]).read_text(encoding="utf-8")
    assert str(config["readme_route"]) in readme, locale


def test_diagram_regeneration_contract_keeps_responsibilities_distinct() -> None:
    prompt = DIAGRAM_PROMPT.read_text(encoding="utf-8")
    for marker in (
        "Stage 7 上線工程關係與 Eval Case",
        "Workflow Graph 是帶條件的分支路線",
        "Harness 可以是路線中的工作環境",
        "Harness 裡可以執行 Loop",
        "Outcome、Trajectory、Grader 三個實際評測元素",
        "不宣稱 `Harness + Eval = Loop`",
    ):
        assert marker in prompt

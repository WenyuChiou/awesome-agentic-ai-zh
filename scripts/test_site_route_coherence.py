from __future__ import annotations

import hashlib
import re
import struct
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]

LOCALES = {
    "zh-TW": {
        "suffix": "",
        "track_a": "### Track A",
        "track_b": "### Track B",
        "optional": ("建議", "不擋"),
        "stage5_core": "5.1–5.4",
        "stage5_optional": "5.5–5.8",
        "readme_example_label": "可直接執行的小練習",
        "readme_forbidden": ("illustrative", "1-5", "想 USE", "想 BUILD", "5.5-5.7", "5.5–5.7"),
        "readme_sdk_condition": "需要連模型時",
        "walkthrough_next": (
            "../stages/07.5-advanced-agentic-concepts.md",
            "../stages/08-agent-interfaces.md",
            "../README.md",
        ),
        "walkthrough_stale": ("300 行", "for-researcher branch", "個人助理 branch"),
        "legacy_a2_anchor": "-進-a3-前的自我檢查",
        "legacy_stage5_anchor": "-進入-stage-6-前的自我檢查",
        "legacy_roadmap_anchors": (
            "近期想補的缺口",
            "進行中--隨時可貢獻",
            "-動手練習覆蓋補齊",
            "-audience-branch-深化",
            "-stage-2--stage-3-2026-freshness-小修",
            "基礎建設maintainer-進行中",
            "想法箱待討論還沒承諾",
        ),
        "foundation_route": "`Stage 0 → Stage 1 → Stage 2`",
        "track_a_route": "`A1 → A2 → Stage 5 → A3 → Stage 8`",
        "track_b_route": "`Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7 → Stage 7.5 → Stage 8`",
        "roadmap_stale": (
            "2026-05 snapshot",
            "Stage 2 / Stage 3 2026 freshness 小修",
            "GitHub Pages,評估中",
            "首頁學習地圖之後再重畫",
        ),
        "stage3_title": "Stage 3 — 工具使用與第一個 Agent Loop",
        "stage3_topic": "工具使用與第一個 Agent Loop",
        "stage4_title": "Stage 4 — Workflow Graph 與 Agent 框架",
        "stage4_topic": "Workflow Graph 與 Agent 框架",
        "stage7_title": "Stage 7 — Agent Production Engineering：Harness、Loop 與 Graph",
        "stage7_topic": "Agent Production Engineering：Harness、Loop 與 Graph",
        "stage7_compact": "Stage 7 — Agent Production Engineering",
    },
    "en": {
        "suffix": ".en",
        "track_a": "### Track A",
        "track_b": "### Track B",
        "optional": ("recommended", "does not block"),
        "stage5_core": "5.1–5.4",
        "stage5_optional": "5.5–5.8",
        "readme_example_label": "small runnable examples",
        "readme_forbidden": ("illustrative", "1-5", "5.5-5.7", "5.5–5.7"),
        "readme_sdk_condition": "When a model connection is needed",
        "walkthrough_next": (
            "../stages/07.5-advanced-agentic-concepts.en.md",
            "../stages/08-agent-interfaces.en.md",
            "../README.en.md",
        ),
        "walkthrough_stale": ("300 lines", "for-researcher branch", "personal-assistant branch"),
        "legacy_a2_anchor": "-self-check-before-a3",
        "legacy_stage5_anchor": "-self-check-before-stage-6",
        "legacy_roadmap_anchors": (
            "near-term-gaps-we-want-to-fill",
            "in-progress--always-open-to-contributions",
            "-fill-out-hands-on-exercise-coverage",
            "-deepen-the-audience-branch-files",
            "-stage-2--stage-3-2026-freshness-touch-up",
            "infrastructure-maintainer-in-progress",
            "idea-box-pending-discussion-not-committed-yet",
        ),
        "foundation_route": "`Stage 0 → Stage 1 → Stage 2`",
        "track_a_route": "`A1 → A2 → Stage 5 → A3 → Stage 8`",
        "track_b_route": "`Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7 → Stage 7.5 → Stage 8`",
        "roadmap_stale": (
            "2026-05 snapshot",
            "Stage 2 / Stage 3 2026 freshness",
            "GitHub Pages, under evaluation",
            "homepage learning map is redrawn",
        ),
        "stage3_title": "Stage 3 — Tool Use & Your First Agent Loop",
        "stage3_topic": "Tool Use & Your First Agent Loop",
        "stage4_title": "Stage 4 — Workflow Graphs & Agent Frameworks",
        "stage4_topic": "Workflow Graphs & Agent Frameworks",
        "stage7_title": "Stage 7 — Agent Production Engineering: Harness, Loops, and Graphs",
        "stage7_topic": "Agent Production Engineering: Harness, Loops, and Graphs",
        "stage7_compact": "Stage 7 — Agent Production Engineering",
    },
    "zh-Hans": {
        "suffix": ".zh-Hans",
        "track_a": "### Track A",
        "track_b": "### Track B",
        "optional": ("建议", "不影响"),
        "stage5_core": "5.1–5.4",
        "stage5_optional": "5.5–5.8",
        "readme_example_label": "可直接运行的小练习",
        "readme_forbidden": ("illustrative", "1-5", "想 USE", "想 BUILD", "5.5-5.7", "5.5–5.7"),
        "readme_sdk_condition": "需要连接模型时",
        "walkthrough_next": (
            "../stages/07.5-advanced-agentic-concepts.zh-Hans.md",
            "../stages/08-agent-interfaces.zh-Hans.md",
            "../README.zh-Hans.md",
        ),
        "walkthrough_stale": ("300 行", "for-researcher branch", "个人助理 branch"),
        "legacy_a2_anchor": "-进入-a3-前的自我检查",
        "legacy_stage5_anchor": "-进入-stage-6-前的自我检查",
        "legacy_roadmap_anchors": (
            "近期想补的缺口",
            "进行中--随时可贡献",
            "-动手练习覆盖补齐",
            "-audience-branch-深化",
            "-stage-2--stage-3-2026-freshness-小修",
            "基础建设maintainer-进行中",
            "想法箱待讨论还没承诺",
        ),
        "foundation_route": "`Stage 0 → Stage 1 → Stage 2`",
        "track_a_route": "`A1 → A2 → Stage 5 → A3 → Stage 8`",
        "track_b_route": "`Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7 → Stage 7.5 → Stage 8`",
        "roadmap_stale": (
            "2026-05 snapshot",
            "Stage 2 / Stage 3 2026 freshness 小修",
            "GitHub Pages,评估中",
            "首页学习地图之后再重画",
        ),
        "stage3_title": "Stage 3 — 工具使用与第一个 Agent Loop",
        "stage3_topic": "工具使用与第一个 Agent Loop",
        "stage4_title": "Stage 4 — Workflow Graph 与 Agent 框架",
        "stage4_topic": "Workflow Graph 与 Agent 框架",
        "stage7_title": "Stage 7 — Agent Production Engineering：Harness、Loop 与 Graph",
        "stage7_topic": "Agent Production Engineering：Harness、Loop 与 Graph",
        "stage7_compact": "Stage 7 — Agent Production Engineering",
    },
}


def locale_path(stem: str, suffix: str) -> Path:
    return ROOT / f"{stem}{suffix}.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def between(text: str, start: str, end: str) -> str:
    start_at = text.index(start)
    end_at = text.index(end, start_at + len(start))
    return text[start_at:end_at]


def assert_in_order(text: str, needles: tuple[str, ...]) -> None:
    positions = [text.index(needle) for needle in needles]
    assert positions == sorted(positions), dict(zip(needles, positions, strict=True))


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_readme_uses_one_track_a_order(locale: str, config: dict[str, object]) -> None:
    text = read(locale_path("README", str(config["suffix"])))
    track_a = between(text, str(config["track_a"]), str(config["track_b"]))
    assert_in_order(
        track_a,
        (
            "tracks/cli/A1-cli-intro",
            "tracks/cli/A2-cli-workflow",
            "stages/05-claude-code-ecosystem",
            "tracks/cli/A3-cli-production",
            "stages/08-agent-interfaces",
        ),
    )


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_readme_keeps_shared_foundation_and_track_b_order(
    locale: str, config: dict[str, object]
) -> None:
    text = read(locale_path("README", str(config["suffix"])))
    assert_in_order(
        text,
        (
            "stages/00-foundations",
            "stages/01-llm-basics",
            "stages/02-prompt-engineering",
        ),
    )
    track_b = text[text.index(str(config["track_b"])) :]
    assert_in_order(
        track_b,
        (
            "stages/03-tool-use-and-hello-agent",
            "stages/04-agent-frameworks",
            "stages/05-claude-code-ecosystem",
            "stages/06-memory-rag",
            "stages/07-multi-agent-production",
            "stages/07.5-advanced-agentic-concepts",
            "stages/08-agent-interfaces",
        ),
    )


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_progress_matches_route_and_marks_stage8_recommended(
    locale: str, config: dict[str, object]
) -> None:
    text = read(locale_path("PROGRESS", str(config["suffix"])))
    track_a = between(text, "## Track A", "## Track B")
    assert_in_order(
        track_a,
        (
            "tracks/cli/A1-cli-intro",
            "tracks/cli/A2-cli-workflow",
            "stages/05-claude-code-ecosystem",
            "tracks/cli/A3-cli-production",
            "stages/08-agent-interfaces",
        ),
    )
    stage8_line = next(line for line in track_a.splitlines() if "08-agent-interfaces" in line)
    for marker in config["optional"]:
        assert marker in stage8_line, (locale, marker, stage8_line)


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_a2_sends_reader_to_stage5_not_directly_to_a3(
    locale: str, config: dict[str, object]
) -> None:
    text = read(locale_path("tracks/cli/A2-cli-workflow", str(config["suffix"])))
    header = "\n".join(text.splitlines()[:8])
    self_check = text[text.index("## ✅") :]
    target = "../../stages/05-claude-code-ecosystem"
    assert target in header
    assert target in self_check
    assert "A3-cli-production" not in header


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_stage5_routes_track_a_to_a3_and_track_b_to_stage6(
    locale: str, config: dict[str, object]
) -> None:
    text = read(locale_path("stages/05-claude-code-ecosystem", str(config["suffix"])))
    entry = text[text.index("## 🚪") : text.index("<details", text.index("## 🚪"))]
    self_check = text[text.index("## ✅") :]
    assert "../tracks/cli/A2-cli-workflow" in entry
    assert "../tracks/cli/A3-cli-production" in entry
    assert "../tracks/cli/A3-cli-production" in self_check
    assert "06-memory-rag" in self_check


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_a3_requires_stage5_and_recommends_stage8_next(
    locale: str, config: dict[str, object]
) -> None:
    text = read(locale_path("tracks/cli/A3-cli-production", str(config["suffix"])))
    before_exercises = text[: text.index("## 🛠")]
    self_check = text[text.index("## ✅") :]
    assert "../../stages/05-claude-code-ecosystem" in before_exercises
    assert "../../stages/08-agent-interfaces" in self_check


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_track_a_capstone_keeps_stage8_optional(
    locale: str, config: dict[str, object]
) -> None:
    text = read(locale_path("CAPSTONE", str(config["suffix"])))
    track_a = between(text, "## Track A", "## Track B")
    assert "Stage 0" in track_a
    assert "A1" in track_a and "A2" in track_a and "A3" in track_a
    assert "Stage 5" in track_a and "Stage 8" in track_a
    assert str(config["stage5_core"]) in track_a
    for marker in config["optional"]:
        assert marker in track_a, (locale, marker)


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_readme_keeps_stage5_core_and_every_optional_section(
    locale: str, config: dict[str, object]
) -> None:
    suffix = str(config["suffix"])
    readme = read(locale_path("README", suffix))
    stage5 = read(locale_path("stages/05-claude-code-ecosystem", suffix))

    assert str(config["stage5_core"]) in readme
    assert str(config["stage5_optional"]) in readme
    assert "## 5.8" in stage5


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_readme_uses_plain_runnable_example_copy(
    locale: str, config: dict[str, object]
) -> None:
    text = read(locale_path("README", str(config["suffix"])))

    assert str(config["readme_example_label"]).casefold() in text.casefold()
    assert str(config["readme_sdk_condition"]) in text
    for stale in config["readme_forbidden"]:
        assert str(stale).casefold() not in text.casefold(), (locale, stale)


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_roadmap_states_the_exact_canonical_routes(
    locale: str, config: dict[str, object]
) -> None:
    text = read(locale_path("ROADMAP", str(config["suffix"])))
    assert str(config["foundation_route"]) in text
    assert str(config["track_a_route"]) in text
    assert str(config["track_b_route"]) in text


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_developer_branch_uses_the_canonical_track_a_route(
    locale: str, config: dict[str, object]
) -> None:
    text = read(locale_path("branches/for-developer", str(config["suffix"])))
    route_line = next(
        line
        for line in text.splitlines()
        if "A1-cli-intro" in line and "05-claude-code-ecosystem" in line
    )
    assert "A1 → A2 →" in route_line
    assert "stages/05-claude-code-ecosystem" in route_line
    assert "→ A3" in route_line
    for marker in config["optional"]:
        assert marker in route_line, (locale, marker, route_line)


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_roadmap_drops_completed_or_stale_gap_claims(
    locale: str, config: dict[str, object]
) -> None:
    text = read(locale_path("ROADMAP", str(config["suffix"])))
    for stale in config["roadmap_stale"]:
        assert stale not in text, (locale, stale)


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_walkthrough_returns_to_stage75_stage8_and_role_paths(
    locale: str, config: dict[str, object]
) -> None:
    text = read(
        locale_path("walkthroughs/build-first-agent-in-7-steps", str(config["suffix"]))
    )

    for target in config["walkthrough_next"]:
        assert str(target) in text, (locale, target)
    for target in (
        "../branches/for-researcher",
        "../branches/for-knowledge-worker",
        "../branches/for-everyday-users",
    ):
        assert target in text, (locale, target)
    for stale in config["walkthrough_stale"]:
        assert str(stale) not in text, (locale, stale)
    assert not re.search(r"~\d+\s*(?:行|lines)", text), locale


def test_stage_design_matches_current_stage0_and_stage5_shapes() -> None:
    text = read(ROOT / "stages/DESIGN.md")

    assert "1 個整合練習：公開 GitHub API → JSON → terminal → Git" in text
    assert "九個核心詞、五題累加練習、5.1–5.8 延伸入口" in text
    assert "4 個 動手練習 self-test" not in text
    assert "4 個 sub-stage" not in text


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_renamed_route_headings_keep_legacy_deep_links(
    locale: str, config: dict[str, object]
) -> None:
    suffix = str(config["suffix"])
    a2 = read(locale_path("tracks/cli/A2-cli-workflow", suffix))
    stage5 = read(locale_path("stages/05-claude-code-ecosystem", suffix))
    roadmap = read(locale_path("ROADMAP", suffix))

    assert f'<a id="{config["legacy_a2_anchor"]}"></a>' in a2
    assert f'<a id="{config["legacy_stage5_anchor"]}"></a>' in stage5
    for anchor in config["legacy_roadmap_anchors"]:
        assert f'<a id="{anchor}"></a>' in roadmap


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_stage3_stage4_titles_match_across_reader_entry_points(
    locale: str, config: dict[str, object]
) -> None:
    suffix = str(config["suffix"])
    stage3_title = str(config["stage3_title"])
    stage3_topic = str(config["stage3_topic"])
    stage4_title = str(config["stage4_title"])
    stage4_topic = str(config["stage4_topic"])

    readme = read(locale_path("README", suffix))
    index = read(locale_path("index", suffix))
    progress = read(locale_path("PROGRESS", suffix))
    stage2 = read(locale_path("stages/02-prompt-engineering", suffix))
    examples_index = read(locale_path("examples/README", suffix))

    assert f"[{stage3_topic}]" in readme
    assert f"[{stage4_topic}]" in readme
    assert f"__{stage3_title}__" in index
    assert f"__{stage4_title}__" in index
    assert f"**{stage3_title}**" in progress
    assert f"**{stage4_title}**" in progress
    assert f"[{stage3_title}]" in stage2
    assert stage3_topic in examples_index
    assert stage4_topic in examples_index


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_all_stage3_companion_pages_use_the_current_localized_title(
    locale: str, config: dict[str, object]
) -> None:
    suffix = str(config["suffix"])
    stage3_title = str(config["stage3_title"])
    label = f"[{stage3_title}]"

    examples = sorted((ROOT / "examples/stage-3").glob(f"*/README{suffix}.md"))
    assert len(examples) == 6, (locale, examples)
    for page in examples:
        assert label in read(page), (locale, page)

    tutor = ROOT / f"examples/stage-5/tool-calling-tutor/README{suffix}.md"
    cheatsheet = locale_path("resources/schema-design-cheatsheet", suffix)
    assert label in read(tutor)
    assert read(cheatsheet).count(label) == 2


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_stage7_umbrella_title_matches_all_direct_reader_routes(
    locale: str, config: dict[str, object]
) -> None:
    suffix = str(config["suffix"])
    stage7_title = str(config["stage7_title"])
    stage7_topic = str(config["stage7_topic"])
    stage7_compact = str(config["stage7_compact"])

    stage7 = read(locale_path("stages/07-multi-agent-production", suffix))
    readme = read(locale_path("README", suffix))
    index = read(locale_path("index", suffix))
    progress = read(locale_path("PROGRESS", suffix))
    stage6 = read(locale_path("stages/06-memory-rag", suffix))
    examples_index = read(locale_path("examples/README", suffix))

    assert stage7.startswith(f"# {stage7_title}\n")
    assert f"[{stage7_topic}]" in readme
    assert f"__{stage7_compact}__" in index
    assert f"**{stage7_title}**" in progress
    assert f"[{stage7_title}]" in stage6
    assert stage7_compact.removeprefix("Stage 7 — ") in examples_index

    examples = sorted((ROOT / "examples/stage-7").glob(f"*/README{suffix}.md"))
    assert len(examples) == 5, (locale, examples)
    for page in examples:
        assert f"[{stage7_title}]" in read(page), (locale, page)

    if locale == "zh-TW":
        assert f"- {stage7_title}: stages/07-multi-agent-production.md" in (
            ROOT / "mkdocs.yml"
        ).read_text(encoding="utf-8")
        assert f"[{stage7_title}](stages/07-multi-agent-production.md)" in (
            ROOT / "scripts/build-mdbook.sh"
        ).read_text(encoding="utf-8")


def test_secondary_stage4_route_surfaces_put_the_graph_before_the_framework() -> None:
    expected_en = "Stage 4 (Workflow Graphs & Agent Frameworks)"
    for path in (
        ROOT / ".github/outreach/_send-day-packages.md",
        ROOT / ".github/outreach/langchain-ai.md",
    ):
        assert expected_en in read(path), path

    assert "Stage 4（Workflow Graph／Agent Framework）" in read(
        ROOT / "docs/HOW_TO_USE.md"
    )
    assert "Stage 4 — Workflow Graphs & Agent Frameworks" in read(
        ROOT / ".github/ISSUE_TEMPLATE/project-suggestion.md"
    )


@pytest.mark.parametrize("locale,config", LOCALES.items())
def test_readme_explains_learning_order_separately_from_control_scope(
    locale: str, config: dict[str, object]
) -> None:
    text = read(locale_path("README", str(config["suffix"])))
    route = next(line for line in text.splitlines() if line.startswith("> 🔭"))
    stages = tuple(f"Stage {number}" for number in range(2, 8))
    positions = [route.index(stage) for stage in stages]

    assert positions == sorted(positions)
    assert "**Agent Loop**" in route
    assert "**Workflow Graph**" in route
    assert "**Context Engineering**" in route
    assert "`prompt → context → harness → loop → graph`" in route


def test_legacy_stage_titles_are_absent_repo_wide() -> None:
    stale = (
        "Tool Use & Hello Agent",
        "Tool Use & Agent Intro",
        "Tool Use & Agent intro",
        "Tool Use and Agent Basics",
        "Tool Use & Agent 入門",
        "Tool Use & Agent 入门",
        "Tool Use 與 Agent 入門",
        "Tool Use 与 Agent 入门",
        "Stage 3 — 工具呼叫__",
        "Stage 3 — 工具调用__",
        "Stage 4 (Agent Frameworks)",
        "**4** Agent 框架 |",
        "Stage 7 — Loop／Graph Engineering：多 Agent 與穩定運作",
        "Stage 7 — Loop & Graph Engineering: Multi-Agent Production",
        "Stage 7 — Loop／Graph Engineering：多 Agent 与稳定运行",
        "Stage 7 — Multi-Agent · 進階應用",
        "Stage 7 — Multi-Agent · Advanced Applications",
        "Stage 7 — Multi-Agent · 进阶应用",
        "Stage 7 — Multi-Agent 與 Production",
        "Stage 7 — Multi-Agent & Production",
        "Stage 7 — Multi-Agent 与 Production",
    )
    excluded = {ROOT / "CHANGELOG.md"}
    excluded_root = ROOT / "docs/plans"
    generated_or_private = {ROOT / ".ai", ROOT / ".git", ROOT / "_build"}
    offenders: list[tuple[Path, str]] = []

    for page in ROOT.rglob("*.md"):
        if (
            page in excluded
            or excluded_root in page.parents
            or any(root in page.parents for root in generated_or_private)
        ):
            continue
        text = read(page)
        for phrase in stale:
            if phrase in text:
                offenders.append((page.relative_to(ROOT), phrase))

    assert not offenders, offenders


ENTRY_ROUTE = {
    "zh-TW": {
        "suffix": "",
        "route_shape": "8 個主題 Stage + Stage 0 準備關 + Stage 7.5 進階閱讀站",
        "count": "10 個學習站",
        "summary": "⏱️ 查看時間估算（安排參考，不是截止日期）",
        "stat": '<span class="aaz-num">10</span><span class="aaz-lbl">學習站</span>',
        "heading": "## 從 Stage 0 到 Stage 8，另有 Stage 7.5 閱讀站",
        "banner": "banner.png",
    },
    "en": {
        "suffix": ".en",
        "route_shape": (
            "8 topic stages + the Stage 0 readiness check + the Stage 7.5 advanced reading stop"
        ),
        "count": "10 learning stops",
        "summary": "⏱️ View time estimates (planning aid, not a deadline)",
        "stat": '<span class="aaz-num">10</span><span class="aaz-lbl">learning stops</span>',
        "heading": "## Stage 0 through Stage 8, plus the Stage 7.5 reading stop",
        "banner": "banner.en.png",
    },
    "zh-Hans": {
        "suffix": ".zh-Hans",
        "route_shape": "8 个主题 Stage + Stage 0 准备关 + Stage 7.5 进阶阅读站",
        "count": "10 个学习站",
        "summary": "⏱️ 查看时间估算（安排参考，不是截止日期）",
        "stat": '<span class="aaz-num">10</span><span class="aaz-lbl">学习站</span>',
        "heading": "## 从 Stage 0 到 Stage 8，另有 Stage 7.5 阅读站",
        "banner": "banner.zh-Hans.png",
    },
}


@pytest.mark.parametrize("locale,config", ENTRY_ROUTE.items())
def test_readme_names_all_learning_stops_and_hides_only_time_detail(
    locale: str, config: dict[str, str]
) -> None:
    text = read(locale_path("README", config["suffix"]))
    summary = f'<summary>{config["summary"]}</summary>'
    start = text.index('<details markdown="1">', text.index(summary) - 40)
    end = text.index("</details>", start) + len("</details>")
    time_block = text[start:end]
    visible = text[:start] + text[end:]

    assert config["route_shape"] in text
    assert config["count"] in text
    assert summary in time_block
    assert "<details" not in time_block.replace('<details markdown="1">', "", 1)
    assert not re.search(r"<details[^>]*\sopen(?:\s|>)", time_block)
    assert "8–10" in time_block and "16–22" in time_block and "5–7" in time_block
    assert "8-10" not in visible and "16-22" not in visible and "5-7" not in visible
    assert "2024-2026" not in text and "2024–2026" not in text
    assert "~300" not in text
    assert "mv starter.py" not in text and "starter_" + "reference.py" not in text
    assert "### 🤖" not in text
    for term in (
        "zero-shot",
        "one-shot",
        "few-shot",
        "CoT",
        "model comparison",
        "Smolagents",
        "long-term memory",
        "contextual retrieval",
        "advanced SDK",
        "12 ",
        "reading list",
        "PAR loop",
        "agent-as-judge",
    ):
        assert term in text, (locale, term)


def test_active_public_and_export_surfaces_drop_the_old_stage_count_shorthand() -> None:
    paths = [
        ROOT / "README.md",
        ROOT / "README.en.md",
        ROOT / "README.zh-Hans.md",
        ROOT / "mkdocs.yml",
        ROOT / "scripts/build-pdf.sh",
        *sorted((ROOT / ".github/outreach").glob("*.md")),
    ]
    stale = re.compile(
        r"\b8[- ]stages?\b|"
        r"8\s*(?:(?:個|个)\s*(?:階段|阶段)|(?:階段|阶段))"
    )
    offenders = [path.relative_to(ROOT) for path in paths if stale.search(read(path))]
    assert not offenders, offenders


EXERCISE_CALLOUT_DIRS = (
    "stage-1/04-cross-provider",
    "stage-1/05-error-handling",
    "stage-2/01-prompt-eval-loop",
    "stage-3/02-multi-tool-selection",
    "stage-3/03-react-from-scratch",
    "stage-3/04-multi-step-reasoning",
    "stage-3/05-error-handling",
    "stage-3/06-schema-design",
    "stage-4/01-same-agent-two-frameworks",
    "stage-4/02-multi-agent-roles",
    "stage-4/03-graph-workflow",
    "stage-4/04-codeact-vs-json-tool",
    "stage-4/05-typed-agent",
)


@pytest.mark.parametrize(
    "suffix,required",
    (
        ("", ("先執行", "只改一個", "重新執行", "不需要改名", "不需要整份")),
        (
            ".en",
            (
                "First run",
                "change exactly one",
                "run the existing test",
                "do not need to rename",
                "rewrite the whole solution",
            ),
        ),
        (".zh-Hans", ("先运行", "只改一个", "重新运行", "不需要重命名", "不需要重写整份")),
    ),
)
def test_exercise_callouts_teach_run_change_one_thing_and_retest(
    suffix: str, required: tuple[str, ...]
) -> None:
    pages = [ROOT / "examples" / folder / f"README{suffix}.md" for folder in EXERCISE_CALLOUT_DIRS]
    assert len(pages) == 13
    forbidden = (
        "mv starter.py",
        "starter_" + "reference.py",
        "starter_template.py",
        "write your own `starter.py` from scratch",
        "自己重寫一份",
        "自己重写一份",
    )
    for page in pages:
        text = read(page)
        callout = next(line for line in text.splitlines() if line.startswith("> 🎓"))
        assert "docs/HOW_TO_USE.md" in callout, page
        for marker in required:
            assert marker in callout, (page, marker)
        for marker in forbidden:
            assert marker not in callout, (page, marker)

    testing_plan = read(ROOT / "docs/TESTING_PLAN.md")
    active_v2 = between(testing_plan, "## v2 path (deferred)", "## Historical:")
    for marker in forbidden:
        assert marker not in active_v2, marker
        assert marker not in testing_plan, marker


@pytest.mark.parametrize("locale,config", ENTRY_ROUTE.items())
def test_landing_page_shows_all_ten_stops(
    locale: str, config: dict[str, str]
) -> None:
    text = read(locale_path("index", config["suffix"]))
    assert config["stat"] in text
    assert config["heading"] in text
    route_cards = text[text.index(config["heading"]) :]
    assert len(re.findall(r"__Stage (?:0|1|2|3|4|5|6|7|7\.5|8)\b", route_cards)) == 10
    assert_in_order(
        route_cards,
        tuple(
            f"stages/{path}"
            for path in (
                "00-foundations",
                "01-llm-basics",
                "02-prompt-engineering",
                "03-tool-use-and-hello-agent",
                "04-agent-frameworks",
                "05-claude-code-ecosystem",
                "06-memory-rag",
                "07-multi-agent-production",
                "07.5-advanced-agentic-concepts",
                "08-agent-interfaces",
            )
        ),
    )


def test_banner_trio_uses_one_wide_canvas_and_distinct_locale_assets() -> None:
    hashes: set[str] = set()
    for config in ENTRY_ROUTE.values():
        path = ROOT / "resources" / "diagrams" / config["banner"]
        data = path.read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n"), path
        width, height = struct.unpack(">II", data[16:24])
        assert (width, height) == (1672, 941), (path, width, height)
        assert len(data) < 2_000_000, (path, len(data))
        hashes.add(hashlib.sha256(data).hexdigest())

    assert len(hashes) == 3


def test_banner_regeneration_contract_avoids_mutable_metrics() -> None:
    prompt = read(ROOT / "resources" / "diagrams" / "locale-variant-prompts.md")
    section = prompt[prompt.index("## 2026-08-30：首頁學習路徑 Banner") :]
    for marker in (
        "Stage 0–1–2",
        "A1 → A2 → Stage 5 → A3 → Stage 8",
        "3 → 4 → Stage 5 → 6 → 7 → 7.5 → Stage 8",
    ):
        assert marker in section
    for forbidden in ("週數", "月份", "每週時數", "價格", "版本", "年份", "stars"):
        assert forbidden in section


def test_how_to_use_teaches_run_change_one_thing_and_retest() -> None:
    text = read(ROOT / "docs" / "HOW_TO_USE.md")
    assert_in_order(
        text,
        (
            "## 先認識 `starter.py`",
            "## 六步學習循環",
            "## 可以改什麼？",
            "## 每題做完問自己三句話",
            "## 章節怎麼接",
            "## 如果卡住",
        ),
    )
    for required in ("直接執行", "只改一個", "再跑測試", "git diff", "不要貼 API key"):
        assert required in text
    for stale in (
        "mv starter.py",
        "starter_" + "reference.py",
        "學到 100%",
        "學到 60%",
        "自己重寫",
        "默寫一遍",
        "v2 規劃",
    ):
        assert stale not in text
    time = text[text.index('<summary>⏱️ 查看練習時間安排</summary>') :]
    assert "固定小時" in time
    assert not re.search(r"<details[^>]*\sopen(?:\s|>)", text)

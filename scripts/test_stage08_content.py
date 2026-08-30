"""Stage 08 reader path, current-fact, resource, diagram, and mirror contracts."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import struct
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "zh-TW": ROOT / "stages/08-agent-interfaces.md",
    "en": ROOT / "stages/08-agent-interfaces.en.md",
    "zh-Hans": ROOT / "stages/08-agent-interfaces.zh-Hans.md",
}
GLOSSARIES = {
    "zh-TW": ROOT / "resources/glossary.md",
    "en": ROOT / "resources/glossary.en.md",
    "zh-Hans": ROOT / "resources/glossary.zh-Hans.md",
}
DIAGRAMS = {
    "zh-TW": (
        ROOT / "resources/diagrams/interface-choice-map.png",
        ROOT / "resources/diagrams/agent-guardrail-patterns.png",
    ),
    "en": (
        ROOT / "resources/diagrams/interface-choice-map.en.png",
        ROOT / "resources/diagrams/agent-guardrail-patterns.en.png",
    ),
    "zh-Hans": (
        ROOT / "resources/diagrams/interface-choice-map.zh-Hans.png",
        ROOT / "resources/diagrams/agent-guardrail-patterns.zh-Hans.png",
    ),
}

CORE_LABELS = {
    "zh-TW": (
        "Agent Interface（Agent 操作介面）",
        "Browser Use（瀏覽器操作）",
        "Computer Use（電腦操作）",
        "Sandbox（沙箱）",
        "Accessibility Tree（無障礙樹）",
        "Harness（執行框架）",
        "Approval Gate（批准閘門）",
        "Prompt Injection（提示注入）",
    ),
    "en": (
        "Agent Interface",
        "Browser Use",
        "Computer Use",
        "Sandbox",
        "Accessibility Tree",
        "Harness",
        "Approval Gate",
        "Prompt Injection",
    ),
    "zh-Hans": (
        "Agent Interface（Agent 操作界面）",
        "Browser Use（浏览器操作）",
        "Computer Use（电脑操作）",
        "Sandbox（沙箱）",
        "Accessibility Tree（无障碍树）",
        "Harness（执行框架）",
        "Approval Gate（批准闸门）",
        "Prompt Injection（提示注入）",
    ),
}

FRESHNESS = (
    "<!-- freshness: canonical=stages/08-agent-interfaces.md; "
    "verified_on=2026-08-28; "
    "scope=computer-use,browser-use,sandboxes,availability,benchmarks,security; "
    "max_age_days=90 -->"
)

RESOURCE_PAIRS = (
    ("https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool", "⭐⭐⭐⭐⭐"),
    ("https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool", "⭐⭐⭐⭐⭐"),
    ("https://developers.openai.com/api/docs/guides/tools-computer-use", "⭐⭐⭐⭐⭐"),
    ("https://openai.github.io/openai-agents-python/sandbox/guide/", "⭐⭐⭐⭐"),
    ("https://support.google.com/chrome/answer/16283624?hl=en", "⭐⭐⭐"),
    ("https://github.com/anthropics/claude-quickstarts", "⭐⭐⭐⭐⭐"),
    ("https://github.com/browser-use/browser-use", "⭐⭐⭐⭐⭐"),
    ("https://github.com/microsoft/playwright-mcp", "⭐⭐⭐⭐⭐"),
    ("https://github.com/trycua/cua", "⭐⭐⭐⭐"),
    ("https://github.com/bytedance/UI-TARS-desktop", "⭐⭐⭐⭐"),
    ("https://github.com/e2b-dev/E2B", "⭐⭐⭐⭐⭐"),
    ("https://github.com/cloudflare/sandbox-sdk", "⭐⭐⭐⭐"),
    ("https://modal.com/docs/guide/sandboxes", "⭐⭐⭐⭐"),
    ("https://vercel.com/docs/sandbox", "⭐⭐⭐⭐"),
    ("https://github.com/microsoft/OmniParser", "⭐⭐⭐⭐"),
    ("https://osworld-v2.xlang.ai/", "⭐⭐⭐⭐⭐"),
    ("https://github.com/xlang-ai/OSWorld", "⭐⭐⭐⭐⭐"),
    ("https://github.com/web-arena-x/webarena", "⭐⭐⭐⭐"),
    ("https://github.com/OSU-NLP-Group/Mind2Web", "⭐⭐⭐⭐"),
    ("https://brave.com/blog/indirect-prompt-injection/", "⭐⭐⭐⭐"),
    ("https://research.perplexity.ai/articles/browsesafe", "⭐⭐⭐"),
)
RESOURCE_HEADINGS = {
    "zh-TW": "## 📚 21 筆完整學習資源與限制",
    "en": "## 📚 21 complete learning resources and limits",
    "zh-Hans": "## 📚 21 项完整学习资源与限制",
}
DETAIL_TAG = re.compile(r"<details\b[^>]*>|</details>")

# These were all public headings before the progressive rewrite. A renamed
# heading must keep the old slug as an explicit alias near its new landing spot.
LEGACY_ANCHORS = {
    "zh-TW": """
-agent-interfaces-是什麼先定位
跟前面-stage-的差別避免概念混淆
為什麼-2024-2026-是-agent-interface-的-breakthrough-年
為什麼兩-track-共用
-學習目標
-進入條件
-必修閱讀
-computer-use--螢幕級-agent
mental-model--工作流跟-why
2026-frontier-4-強對比
為什麼-osworld-數字差這麼大理解-benchmark-紀律
平台支援現況2026-05
-browser-use--web-級-agent
mental-model--dom-aware-vs-screen-pixel--why
mini-glossary就地解釋
閉源-ai-browser-5-強對比2026-05
開源-browser-use-框架
跟-web-scraping--rpa-的差別
-code-execution-sandbox--隔離環境含術語小辭典
為什麼-agent-一定要-sandbox
-隔離技術術語小辭典
7-個-sandbox-對比2026-05
openai-agents-sdk-april-2026-更新--why-是-milestone
-track-a-怎麼用cli-power-user-視角
1-在-claude-code-內接-computer-use--browser-mcp
2-用-codex-desktop-在-background-跑
3-用-comet--gemini-in-chrome--chatgpt-agent-mode-跑-web-任務
跨-app-workflow-範例
-track-b-怎麼-buildagent-builder-視角
1-用-browser-use-寫-web-agent
2-用-e2b-跑-agent-generated-code
3-用-openai-agents-sdk-內建-sandbox2026-04-新
4-gui-agent-訓練資料
-2026-safety--security-重點
案例-1--comet-被-brave-發現可被網頁注入
案例-2--federal-injunction2026-03-comet-禁存取-amazon
4-個防護-pattern必加
-動手練習兩-track-各有
練習-1track-a跨-app-workflow-用-computer-use
練習-2track-bbrowser-use-寫-web-agent
練習-3兩-tracke2b-跑-agent-code
練習-4進階openai-agents-sdk--sandbox--computer-use
-常用工具推薦按用途分類
-精選-projects範本--sdk--工具-collection
-stage-8-之後的自我檢查
-下一個-frontier--voice-agents--vla-機器人
voice-agents語音介面
vlavision-language-action機器人
接下來
""".split(),
    "en": """
-what-are-agent-interfaces-positioning
how-this-stage-differs-from-previous-ones-avoiding-conceptual-confusion
why-2024-2026-is-the-breakthrough-era-for-agent-interfaces
why-is-this-a-shared-hub
-learning-objectives
-entry-conditions
-required-reading
-computer-use--the-screen-level-agent
mental-model-the-workflow-and-why
2026-frontier-a-4-way-comparison
why-the-osworld-numbers-vary-so-much-understanding-benchmark-discipline
platform-support-as-of-may-2026
-browser-use--the-web-level-agent
mental-model-dom-aware-vs-screen-pixel--why
mini-glossary-in-place-explanations
top-5-closed-source-ai-browsers-as-of-may-2026
open-source-browser-use-frameworks
how-it-differs-from-web-scraping--rpa
-code-execution-sandbox--the-isolated-environment-with-mini-glossary
why-agents-absolutely-need-a-sandbox
-mini-glossary-of-isolation-technologies
a-comparison-of-7-sandboxes-as-of-may-2026
why-the-april-2026-openai-agents-sdk-update-is-a-milestone
-how-track-a-uses-it-cli-power-user-perspective
1-connect-to-computer-use--browser-mcps-in-claude-code
2-run-tasks-in-the-background-with-codex-desktop
3-use-comet--gemini-in-chrome--chatgpt-agent-mode-for-web-tasks
example-cross-app-workflow
-how-track-b-builds-it-agent-builder-perspective
1-write-a-web-agent-with-browser-use
2-run-agent-generated-code-with-e2b
3-use-the-built-in-sandbox-in-the-openai-agents-sdk-new-in-april-2026
4-training-data-for-gui-agents
-2026-safety--security-highlights
case-1-comet-found-to-be-vulnerable-to-web-page-injection-by-brave
case-2-federal-injunction-march-2026-comet-banned-from-accessing-amazon
4-must-have-defensive-patterns
-hands-on-exercises-one-for-each-track
exercise-1-track-a-cross-app-workflow-with-computer-use
exercise-2-track-b-write-a-web-agent-with-browser-use
exercise-3-both-tracks-run-agent-code-with-e2b
exercise-4-advanced-openai-agents-sdk--sandbox--computer-use
-recommended-tools-by-use-case
-featured-projects-templates--sdks--tool-collections
-self-check-after-stage-8
-the-next-frontier--voice-agents--vla-robots
voice-agents
vla-vision-language-action-robots
whats-next
""".split(),
    "zh-Hans": """
-agent-interfaces-是什么定位
与之前阶段的区别避免概念混淆
为什么-2024-2026-是-agent-interface-的突破年
为什么两-track-共享
-学习目标
-进入条件
-必修阅读
-computer-use--屏幕级智能体
心智模型--工作流与原因
2026-前沿-4-强对比
为什么-osworld-数据差异巨大理解-benchmark-规范
平台支持现状2026-05
-browser-use--web-级智能体
心智模型--dom-感知-vs-屏幕像素--原因
迷你术语词典就地解释
闭源-ai-浏览器-5-强对比2026-05
开源-browser-use-框架
与-web-scraping--rpa-的区别
-code-execution-sandbox--隔离环境含术语小词典
为什么智能体必须使用沙箱
-隔离技术术语小词典
7-个沙箱对比2026-05
openai-agents-sdk-2026-年-4-月更新--为何是里程碑
-track-a-如何使用cli-高级用户视角
1-在-claude-code-内接入-computer-use--browser-mcp
2-使用-codex-desktop-在后台运行
3-使用-comet--gemini-in-chrome--chatgpt-agent-mode-运行-web-任务
跨应用工作流示例
-track-b-如何构建agent-构建者视角
1-使用-browser-use-编写-web-智能体
2-使用-e2b-运行智能体生成的代码
3-使用-openai-agents-sdk-内置沙箱2026-04-新功能
4-gui-智能体训练数据
-2026-安全性--风险重点
案例-1--comet-被-brave-发现可被网页注入
案例-2--联邦禁令2026-03-comet-禁止访问-amazon
4-个防护模式必须添加
-动手练习两-track-各有
练习-1track-a使用-computer-use-的跨应用工作流
练习-2track-b使用-browser-use-编写-web-智能体
练习-3两-track使用-e2b-运行智能体代码
练习-4进阶openai-agents-sdk--沙箱--computer-use
-常用工具推荐按用途分类
-精选项目模板--sdk--工具合集
-stage-8-之后的自我检查
-下一个前沿--voice-agents--vla-机器人
voice-agents语音界面
vlavision-language-action机器人
接下来
""".split(),
}


def _without_details(text: str) -> str:
    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.DOTALL)


def _html_tables(text: str) -> list[str]:
    return re.findall(r"<table>.*?</table>", text, flags=re.DOTALL)


def _detail_depth_at(text: str, offset: int) -> int:
    """Return open `<details>` depth immediately before `offset`."""
    depth = 0
    for match in DETAIL_TAG.finditer(text, 0, offset):
        depth += -1 if match.group().startswith("</details") else 1
        assert depth >= 0, "closing </details> appears before an opening tag"
    return depth


def test_detail_depth_detects_a_resource_hidden_after_its_heading() -> None:
    hidden = "## 📚 Learning resources\n<details>\n<table></table>\n</details>\n"
    assert _detail_depth_at(hidden, hidden.index("## 📚")) == 0
    assert _detail_depth_at(hidden, hidden.index("<table>")) == 1


def _policy_snippet(text: str) -> str:
    snippets = re.findall(r"~~~python\n(.*?)\n~~~", text, flags=re.DOTALL)
    matches = [snippet for snippet in snippets if "def check_action" in snippet]
    assert len(matches) == 1
    return matches[0]


def _anchor_checker():
    path = ROOT / "scripts/check-anchors.py"
    spec = importlib.util.spec_from_file_location("stage08_anchor_checker", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("locale", PAGES)
def test_visible_path_keeps_landmarks_core_terms_and_safe_first_actions(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    exercise_start = visible.index("## 🛠")

    for icon in ("## 📌", "## 🚪", "## 📚", "## 🔑", "## 🧭", "## 🛡", "## 🛠", "## 🎯", "## ✅"):
        assert icon in visible
    for label in CORE_LABELS[locale]:
        token = f"**{label}**"
        assert token in visible
        assert visible.index(token) < exercise_start

    assert "example.com" in visible
    assert "ALLOWED_DOMAINS" in visible
    assert "HIGH_IMPACT_ACTIONS" in visible
    assert "$0" in visible
    assert "Excel" not in visible


@pytest.mark.parametrize(
    ("locale", "previous_stage", "exercise_headings"),
    (
        (
            "zh-TW",
            "./07.5-advanced-agentic-concepts.md",
            ("### 練習 1", "### 練習 2", "### 練習 3", "### 練習 4"),
        ),
        (
            "en",
            "./07.5-advanced-agentic-concepts.en.md",
            ("### Exercise 1", "### Exercise 2", "### Exercise 3", "### Exercise 4"),
        ),
        (
            "zh-Hans",
            "./07.5-advanced-agentic-concepts.zh-Hans.md",
            ("### 练习 1", "### 练习 2", "### 练习 3", "### 练习 4"),
        ),
    ),
)
def test_previous_stage_and_all_exercise_landings_stay_visible(
    locale: str, previous_stage: str, exercise_headings: tuple[str, ...]
) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    visible = _without_details(text)

    assert previous_stage in visible
    positions = [visible.index(heading) for heading in exercise_headings]
    assert positions == sorted(positions)
    assert all(text.count(heading) == 1 for heading in exercise_headings)


@pytest.mark.parametrize("page", PAGES.values())
def test_all_nine_disclosures_are_closed_and_render_markdown(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    openings = re.findall(r"^<details\b[^>]*>", text, flags=re.MULTILINE)
    assert openings == ['<details markdown="1">'] * 9
    assert "<details open" not in text


def test_resources_keep_ordered_urls_ratings_and_real_rowgroups() -> None:
    for locale, page in PAGES.items():
        text = page.read_text(encoding="utf-8")
        tables = [table for table in _html_tables(text) if RESOURCE_PAIRS[0][0] in table]
        assert len(tables) == 1
        table = tables[0]
        heading_index = text.index(RESOURCE_HEADINGS[locale])
        table_index = text.index(table)
        checked_index = text.index("<small>", heading_index)
        assert heading_index < checked_index < table_index
        assert _detail_depth_at(text, heading_index) == 0
        assert _detail_depth_at(text, checked_index) == 0
        assert _detail_depth_at(text, table_index) == 0
        assert _detail_depth_at(text, len(text)) == 0
        groups = re.findall(r"<tbody>(.*?)</tbody>", table, flags=re.DOTALL)
        assert len(groups) == 5
        for group, rows in zip(groups, (5, 5, 4, 5, 2)):
            assert len(re.findall(r"<tr>", group)) == rows
            assert f'scope="rowgroup" rowspan="{rows}"' in group
        pairs = re.findall(
            r'<a href="(https?://[^"]+)">.*?</a>.*?(⭐{3,5})',
            table,
            flags=re.DOTALL,
        )
        assert tuple(pairs) == RESOURCE_PAIRS
        assert all(
            _detail_depth_at(text, text.index(url, table_index)) == 0
            for url, _rating in RESOURCE_PAIRS
        ), f"{locale}: at least one learning resource is hidden"


def test_three_locales_share_sources_and_freshness_marker() -> None:
    expected_urls: list[str] | None = None
    for page in PAGES.values():
        text = page.read_text(encoding="utf-8")
        assert text.count(FRESHNESS) == 1
        urls = re.findall(r"https?://[^)\s<>\"]+", text)
        if expected_urls is None:
            expected_urls = urls
        else:
            assert urls == expected_urls


def test_copyable_policy_is_identical_and_fails_closed() -> None:
    snippets = [_policy_snippet(page.read_text(encoding="utf-8")) for page in PAGES.values()]
    assert len(set(snippets)) == 1

    namespace: dict[str, object] = {}
    exec(compile(snippets[0], "<stage08-policy>", "exec"), namespace)
    check_action = namespace["check_action"]

    assert check_action("https://example.com/page", "read") == "ALLOW"
    assert check_action("https://example.com/page", "SCREENSHOT") == "ALLOW"
    assert check_action("https://example.com/page", " Login ") == "ASK"
    assert check_action("https://example.com/page", "upload_credentials") == "BLOCK"
    assert check_action("file:///etc/passwd", "read") == "BLOCK"
    assert check_action("http://example.com/page", "read") == "BLOCK"
    assert check_action("https://user@example.com/page", "read") == "BLOCK"
    assert check_action("https://example.com.evil.test/page", "read") == "BLOCK"


@pytest.mark.parametrize("locale", PAGES)
def test_current_interface_sandbox_license_and_benchmark_facts(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    for literal in (
        "computer_toolset_20260801",
        "browser_toolset_20260801",
        '"computer"',
        "computer-use-preview",
        "computer_use_preview",
        "deprecated",
        "SandboxAgent",
        "Manifest",
        "SandboxRunConfig",
        "Beta",
        "gradual rollout",
        "CC-BY-4.0",
        "108",
        "20.6%",
        "2026-08-28",
    ):
        assert literal in text

    assert re.search(r"OmniParser.{0,180}Apache[- ]2\.0", text, flags=re.DOTALL) is None
    assert re.search(r"Apache[- ]2\.0.{0,180}OmniParser", text, flags=re.DOTALL) is None
    row = re.search(r"<tr>.*?OmniParser.*?</tr>", text, flags=re.DOTALL)
    assert row is not None
    assert "CC-BY-4.0" in row.group(0)
    assert "MIT" not in row.group(0) and "AGPL" not in row.group(0)
    assert re.search(r"icon_detect_v3.{0,140}MIT", text, flags=re.DOTALL)
    assert re.search(r"Ultralytics detectors.{0,140}AGPL", text, flags=re.DOTALL)
    assert re.search(r"caption models.{0,140}MIT", text, flags=re.DOTALL)

    cloudflare_row = re.search(
        r"<tr>.*?cloudflare/sandbox-sdk.*?</tr>", text, flags=re.DOTALL
    )
    assert cloudflare_row is not None
    assert "Beta" in cloudflare_row.group(0)
    assert "v1.0" in cloudflare_row.group(0)
    assert any(term in cloudflare_row.group(0) for term in ("may change", "可能改變", "可能变化"))
    assert "daytonaio/daytona" not in text
    assert "Daytona" not in text


@pytest.mark.parametrize("locale", GLOSSARIES)
def test_glossary_keeps_stable_stage08_concepts_without_volatile_snapshots(locale: str) -> None:
    text = GLOSSARIES[locale].read_text(encoding="utf-8")
    section = text.split("## 8. Agent Interfaces", 1)[1].split("\n---", 1)[0]
    for literal in (
        "Harness",
        "executor",
        "Accessibility Tree",
        "Browser Use",
        "Sandbox",
        "secret",
    ):
        assert literal in section

    forbidden = (
        "76.26%",
        "SOTA",
        "105k",
        "< 100ms",
        "4 強",
        "4强",
        "4-vendor",
        "5 強",
        "5强",
        "5-vendor",
        "7 強",
        "7强",
        "7-vendor",
        "Agent sandbox 多半",
        "Most agent sandboxes",
        "內建支援這些 provider",
        "内建支持这些 provider",
        "natively supports these",
        "Sandbox Agents",
        "Beta",
        "108",
    )
    assert not any(term in section for term in forbidden)


def test_glossary_routes_each_locale_back_to_stage08() -> None:
    for locale, glossary in GLOSSARIES.items():
        text = glossary.read_text(encoding="utf-8")
        section = text.split("## 8. Agent Interfaces", 1)[1].split("\n---", 1)[0]
        target = f"../stages/{PAGES[locale].name}"
        assert section.count(target) == 1


@pytest.mark.parametrize("locale", PAGES)
def test_every_old_heading_anchor_still_lands(locale: str) -> None:
    checker = _anchor_checker()
    text = PAGES[locale].read_text(encoding="utf-8")
    anchors = checker.collect_anchors(text)
    assert set(LEGACY_ANCHORS[locale]).issubset(anchors)


def test_six_locale_diagrams_are_distinct_readable_pngs_and_referenced() -> None:
    hashes: set[str] = set()
    for locale, diagrams in DIAGRAMS.items():
        page_text = PAGES[locale].read_text(encoding="utf-8")
        for diagram in diagrams:
            data = diagram.read_bytes()
            assert data.startswith(b"\x89PNG\r\n\x1a\n")
            width, height = struct.unpack(">II", data[16:24])
            assert width >= 1200 and height >= 675
            hashes.add(hashlib.sha256(data).hexdigest())
            assert f"../resources/diagrams/{diagram.name}" in page_text
    assert len(hashes) == 6


@pytest.mark.parametrize("page", PAGES.values())
def test_stale_overclaim_and_display_artifacts_are_absent(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    # Compatibility IDs intentionally preserve old public slugs such as
    # ``...2026-05`` and ``...4-強...``. They are invisible targets, not claims.
    text = re.sub(r'<a\s+(?:id|name)="[^"]+"></a>', "", text)
    forbidden = (
        "108k",
        "5 行 Python",
        "5 lines of Python",
        "10 行內",
        "10 lines",
        "< 90ms",
        "唯一 GPU sandbox",
        "only GPU sandbox",
        "Top 5",
        "5 強",
        "5强",
        "4 強",
        "4强",
        "7 強",
        "7强",
        "2026-05",
        "anthropics/anthropic-quickstarts",
        "Stage 9",
        '""',
        "“”",
    )
    assert not any(term in text for term in forbidden)


def test_english_body_has_no_untranslated_cjk() -> None:
    text = PAGES["en"].read_text(encoding="utf-8")
    text = text.replace("繁體中文", "").replace("简体中文", "")
    assert re.search(r"[\u3400-\u9fff]", text) is None

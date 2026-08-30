"""Stage 07.5 reader-path, fact, diagram, and locale-mirror contracts."""

from __future__ import annotations

import hashlib
import re
import struct
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "stages/DESIGN.md"
PROMPT_LOG = ROOT / "resources/diagrams/locale-variant-prompts.md"
PAGES = {
    "zh-TW": ROOT / "stages/07.5-advanced-agentic-concepts.md",
    "en": ROOT / "stages/07.5-advanced-agentic-concepts.en.md",
    "zh-Hans": ROOT / "stages/07.5-advanced-agentic-concepts.zh-Hans.md",
}
DIAGRAMS = {
    "zh-TW": (
        ROOT / "resources/diagrams/concept-cluster.png",
        ROOT / "resources/diagrams/reading-decision-tree.png",
        ROOT / "resources/diagrams/model-harness-fit.png",
    ),
    "en": (
        ROOT / "resources/diagrams/concept-cluster.en.png",
        ROOT / "resources/diagrams/reading-decision-tree.en.png",
        ROOT / "resources/diagrams/model-harness-fit.en.png",
    ),
    "zh-Hans": (
        ROOT / "resources/diagrams/concept-cluster.zh-Hans.png",
        ROOT / "resources/diagrams/reading-decision-tree.zh-Hans.png",
        ROOT / "resources/diagrams/model-harness-fit.zh-Hans.png",
    ),
}

CONCEPTS = (
    "Work Boundary／Scope Discipline",
    "Contract-driven Hand-off",
    "Spec-driven Development",
    "Speculative／Parallel Exploration",
    "Hierarchical Task Decomposition",
    "Self-organizing Teams",
    "Agent-as-Judge／Principle-based Review",
    "Plan-Act-Reflect Loop",
    "Failure Injection／Chaos Eval",
    "Autonomy Gradients／Trust Layers",
    "Cost-aware Budget Gates",
    "Graceful Degradation",
)
CORE_LABELS = {
    "zh-TW": (
        "Work Boundary（工作邊界）",
        "Contract（契約）",
        "Reflection（反思／回看）",
        "Autonomy（自主權）",
        "Budget Gate（預算閘門）",
        "Graceful Degradation（平穩降級）",
    ),
    "en": (
        "Work Boundary (scope)",
        "Contract",
        "Reflection (look-back)",
        "Autonomy",
        "Budget Gate",
        "Graceful Degradation",
    ),
    "zh-Hans": (
        "Work Boundary（工作边界）",
        "Contract（契约）",
        "Reflection（反思／回看）",
        "Autonomy（自主权）",
        "Budget Gate（预算闸门）",
        "Graceful Degradation（平稳降级）",
    ),
}
LEGACY_ANCHORS = {
    "zh-TW": "-dynamic-workflowsopus-48-當-agent-自己寫出-workflow",
    "en": "-dynamic-workflowsopus-48--agent--workflow",
    "zh-Hans": "-dynamic-workflowsopus-48-当-agent-自己写出-workflow",
}
FRESHNESS = (
    "<!-- freshness: canonical=stages/07.5-advanced-agentic-concepts.md; "
    "verified_on=2026-08-29; "
    "scope=agent-patterns,harnesses,evals,dynamic-workflows,framework-status,research; "
    "max_age_days=90 -->"
)
RESOURCE_PAIRS = (
    ("https://www.anthropic.com/engineering/building-effective-agents", "⭐⭐⭐⭐⭐"),
    ("https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents", "⭐⭐⭐⭐⭐"),
    ("https://openai.com/index/harness-engineering/", "⭐⭐⭐⭐⭐"),
    ("https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents", "⭐⭐⭐⭐"),
    ("https://www.anthropic.com/engineering/harness-design-long-running-apps", "⭐⭐⭐⭐"),
    ("https://www.anthropic.com/engineering/multi-agent-research-system", "⭐⭐⭐⭐⭐"),
    ("https://github.com/langchain-ai/langgraph", "⭐⭐⭐⭐"),
    ("https://github.com/microsoft/agent-framework", "⭐⭐⭐⭐⭐"),
    ("https://openai.github.io/openai-agents-python/sandbox/guide/", "⭐⭐⭐⭐"),
    ("https://code.claude.com/docs/en/workflows", "⭐⭐⭐⭐"),
    ("https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents", "⭐⭐⭐⭐⭐"),
    ("https://www.anthropic.com/engineering/infrastructure-noise", "⭐⭐⭐⭐"),
    ("https://arxiv.org/abs/2507.02825", "⭐⭐⭐⭐"),
    ("https://github.com/sierra-research/tau2-bench", "⭐⭐⭐⭐"),
    ("https://github.com/SWE-bench/SWE-bench", "⭐⭐⭐⭐⭐"),
    ("https://arxiv.org/abs/2210.03629", "⭐⭐⭐⭐⭐"),
    ("https://arxiv.org/abs/2303.11366", "⭐⭐⭐⭐"),
    ("https://arxiv.org/abs/2212.08073", "⭐⭐⭐⭐"),
    ("https://arxiv.org/abs/2303.17760", "⭐⭐⭐"),
    ("https://github.com/stanfordnlp/dspy", "⭐⭐⭐⭐"),
    ("https://github.com/datawhalechina/hello-agents", "⭐⭐⭐⭐⭐"),
    ("https://github.com/microsoft/ai-agents-for-beginners", "⭐⭐⭐⭐"),
    ("https://github.com/langchain-ai/deepagents", "⭐⭐⭐⭐"),
    ("https://speech.ee.ntu.edu.tw/~hylee/", "⭐⭐⭐⭐⭐"),
)
RESOURCE_HEADINGS = {
    "zh-TW": "## 📚 完整學習資源與限制",
    "en": "## 📚 Complete learning resources and limits",
    "zh-Hans": "## 📚 完整学习资源与限制",
}
DETAIL_TAG = re.compile(r"<details\b[^>]*>|</details>")


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


@pytest.mark.parametrize("locale", PAGES)
def test_visible_map_keeps_landmarks_core_terms_and_boundary_card(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    concept_start = visible.index("<table>")

    for label in CORE_LABELS[locale]:
        token = f"**{label}**"
        assert token in visible
        assert visible.index(token) < concept_start

    for line in ("Can do:", "Cannot do:", "Completion evidence:", "Stopping condition:"):
        if locale == "en":
            assert line in visible
    if locale != "en":
        for line in ("可以做：", "不能做：", "完成證據：", "停止條件："):
            localized = line if locale == "zh-TW" else line.replace("證據", "证据").replace("條件", "条件")
            assert localized in visible

    assert "## 🗺️" in visible
    assert "## 🧭" in visible
    assert "## 🛠" in visible
    assert "## ✅" in visible


@pytest.mark.parametrize("locale", PAGES)
def test_model_harness_fit_is_visible_and_evidence_based(locale: str) -> None:
    visible = _without_details(PAGES[locale].read_text(encoding="utf-8"))
    headings = {
        "zh-TW": "## ⚖️ Model–Harness Fit：用 Eval 決定保留、簡化或移除",
        "en": "## ⚖️ Model–Harness Fit: Use Evals to Keep, Simplify, or Remove",
        "zh-Hans": "## ⚖️ Model–Harness Fit：用 Eval 决定保留、简化或移除",
    }
    assert headings[locale] in visible
    semantic_markers = {
        "zh-TW": (
            "權限、sandbox、log、Eval、人工核准與 recovery 代表長期責任",
            "**不會因模型升級就自動消失**",
            "一次只拿一個 Harness 元件做刪除測試，再跑同一組品質與安全 Eval。",
            "| **保留 Keep** | 拿掉後，同一個可重現失敗又回來 |",
            "| **簡化 Simplify** | 保護還有用，但較少步驟也能通過同一組 Eval |",
            "| **移除 Remove** | 刪除測試通過，品質與安全沒有退步 |",
        ),
        "en": (
            "Permissions, sandboxes, logs, Evals, human approvals, and recovery represent lasting responsibilities",
            "do **not disappear automatically after a model upgrade**",
            "Test one Harness component at a time, then run the same quality and safety Evals.",
            "| **Keep** | Removing it brings back the same repeatable failure |",
            "| **Simplify** | The protection still helps, but fewer steps pass the same Eval |",
            "| **Remove** | The deletion test passes without reducing quality or safety |",
        ),
        "zh-Hans": (
            "权限、sandbox、log、Eval、人工批准和 recovery 代表长期责任",
            "**不会因为模型升级就自动消失**",
            "一次只拿一个 Harness 元件做删除测试，再运行同一组质量和安全 Eval。",
            "| **保留 Keep** | 拿掉后，同一个可重复的失败又回来 |",
            "| **简化 Simplify** | 保护仍有用，但更少步骤也能通过同一组 Eval |",
            "| **移除 Remove** | 删除测试通过，质量和安全没有退步 |",
        ),
    }
    for marker in semantic_markers[locale]:
        assert marker in visible


def test_model_harness_fit_diagram_contract_records_parallel_results_and_hans_audit() -> None:
    design = DESIGN.read_text(encoding="utf-8")
    prompt_log = PROMPT_LOG.read_text(encoding="utf-8")
    assert "三個判斷是平行結果，不是成熟度階梯" in design
    assert "no maturity ladder" in prompt_log
    assert "簡中橘卡人工逐字確認為「保护仍然需要，但步骤可以更少」" in prompt_log


@pytest.mark.parametrize("page", PAGES.values())
def test_all_eight_disclosures_are_closed_and_render_markdown(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    openings = re.findall(r"^<details\b[^>]*>", text, flags=re.MULTILINE)
    assert openings == ['<details markdown="1">'] * 8
    assert "<details open" not in text


@pytest.mark.parametrize("page", PAGES.values())
def test_concept_table_has_twelve_preserved_concepts_and_true_rowgroups(page: Path) -> None:
    concept_table = _html_tables(page.read_text(encoding="utf-8"))[0]
    assert tuple(re.findall(r"<strong>(.*?)</strong>", concept_table)) == CONCEPTS
    groups = re.findall(r"<tbody>(.*?)</tbody>", concept_table, flags=re.DOTALL)
    assert len(groups) == 4
    for group in groups:
        assert len(re.findall(r"<tr>", group)) == 3
        assert 'scope="rowgroup" rowspan="3"' in group


def test_resource_table_preserves_24_urls_ratings_and_five_real_rowgroups() -> None:
    for locale, page in PAGES.items():
        text = page.read_text(encoding="utf-8")
        heading = RESOURCE_HEADINGS[locale]
        table = _html_tables(text)[-1]
        heading_index = text.index(heading)
        table_index = text.index(table)
        assert heading_index < table_index
        assert _detail_depth_at(text, heading_index) == 0
        assert _detail_depth_at(text, table_index) == 0
        assert _detail_depth_at(text, len(text)) == 0
        groups = re.findall(r"<tbody>(.*?)</tbody>", table, flags=re.DOTALL)
        assert len(groups) == 5
        for group, rows in zip(groups, (5, 5, 5, 5, 4)):
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


def test_three_locales_share_external_sources_and_freshness_marker() -> None:
    expected_urls: list[str] | None = None
    for page in PAGES.values():
        text = page.read_text(encoding="utf-8")
        assert text.count(FRESHNESS) == 1
        urls = re.findall(r"https?://[^)\s<>\"]+", text)
        if expected_urls is None:
            expected_urls = urls
        else:
            assert urls == expected_urls


@pytest.mark.parametrize("locale", PAGES)
def test_current_status_and_dynamic_workflow_facts_are_mirrored(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    for literal in (
        "Microsoft Agent Framework",
        "AutoGen",
        "maintenance mode",
        "Sandbox Agents",
        "Beta",
        "v2.1.154+",
        "v2.1.203+",
        "16",
        "1,000",
        "2026-05-28",
        "2026-08-28",
    ):
        assert literal in text
    assert "Constitutional AI" in text
    assert "runtime LLM judge" in text


@pytest.mark.parametrize("locale", PAGES)
def test_legacy_dynamic_workflow_anchor_and_heading_remain_visible(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    assert f'<a id="{LEGACY_ANCHORS[locale]}"></a>' in visible
    assert "### 🔀 Dynamic Workflows" in visible


def test_nine_locale_diagrams_are_distinct_full_size_pngs_and_referenced() -> None:
    hashes: set[str] = set()
    for locale, diagrams in DIAGRAMS.items():
        page_text = PAGES[locale].read_text(encoding="utf-8")
        for diagram in diagrams:
            data = diagram.read_bytes()
            assert data.startswith(b"\x89PNG\r\n\x1a\n")
            assert struct.unpack(">II", data[16:24]) == (1672, 941)
            hashes.add(hashlib.sha256(data).hexdigest())
            assert f"../resources/diagrams/{diagram.name}" in page_text
    assert len(hashes) == 9


@pytest.mark.parametrize("page", PAGES.values())
def test_stale_or_confusing_stage075_claims_are_absent(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    forbidden = (
        "Replit Agent 2024",
        "Voyager paper (Wang 2024)",
        "Context 200k",
        "< 500 lines",
        "< 500 行",
        "3.5 PR/day",
        "75% reward hacking",
        "2026-05 snapshot",
        "word `workflow` in the prompt",
        '""',
        "“”",
    )
    assert not any(term in text for term in forbidden)


def test_english_body_has_no_untranslated_cjk_or_stripped_fragments() -> None:
    text = PAGES["en"].read_text(encoding="utf-8")
    text = text.replace("繁體中文", "").replace("简体中文", "")
    assert re.search(r"[\u3400-\u9fff]", text) is None
    assert not re.search(r"[：。，；][：。，；]", text)
    assert '<th scope="col"></th>' not in text

"""Stage 7.5 reader-path, fact, diagram, and locale-mirror contracts."""

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
        ROOT / "resources/diagrams/advanced-agentic-decision-map.png",
        ROOT / "resources/diagrams/model-harness-fit.png",
    ),
    "en": (
        ROOT / "resources/diagrams/advanced-agentic-decision-map.en.png",
        ROOT / "resources/diagrams/model-harness-fit.en.png",
    ),
    "zh-Hans": (
        ROOT / "resources/diagrams/advanced-agentic-decision-map.zh-Hans.png",
        ROOT / "resources/diagrams/model-harness-fit.zh-Hans.png",
    ),
}
FEATURED_CONCEPTS = (
    "Evaluator–Optimizer／Agent-as-Judge",
    "Failure Injection／Chaos Eval",
    "Autonomy Gradients／Trust Layers",
    "Model–Harness Fit",
)
SELECTION_PATTERNS = (
    "Parallel Exploration",
    "Hierarchical Delegation",
    "Multi-Agent Handoff",
    "Plan–Act–Reflect",
    "Dynamic Workflows",
)
LEGACY_ANCHORS = {
    "zh-TW": "-dynamic-workflowsopus-48-當-agent-自己寫出-workflow",
    "en": "-dynamic-workflowsopus-48--agent--workflow",
    "zh-Hans": "-dynamic-workflowsopus-48-当-agent-自己写出-workflow",
}
FRESHNESS = (
    "<!-- freshness: canonical=stages/07.5-advanced-agentic-concepts.md; "
    "verified_on=2026-09-13; "
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


def _detail_depth_at(text: str, offset: int) -> int:
    depth = 0
    for match in DETAIL_TAG.finditer(text, 0, offset):
        depth += -1 if match.group().startswith("</details") else 1
        assert depth >= 0
    return depth


@pytest.mark.parametrize("locale", PAGES)
def test_visible_path_starts_with_stage7_and_keeps_the_advanced_choices(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    first_heading = visible.index("## ")
    assert "Stage 7" in visible[:first_heading]
    for concept in FEATURED_CONCEPTS:
        assert f"**{concept}" in visible
    for pattern in SELECTION_PATTERNS:
        assert f"**{pattern}" in visible
    assert visible.index("Evaluator–Optimizer") < visible.index("Failure Injection")
    assert visible.index("Failure Injection") < visible.index("Autonomy Gradients")
    assert visible.index("Autonomy Gradients") < visible.index("Model–Harness Fit")
    assert "## 📚" in visible
    assert "## ✅" in visible


@pytest.mark.parametrize("locale", PAGES)
def test_decision_map_appears_only_after_all_terms_are_explained(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    diagram_ref = f"../resources/diagrams/{DIAGRAMS[locale][0].name}"
    last_term = max(
        visible.index(f"**{term}")
        for term in (*FEATURED_CONCEPTS, *SELECTION_PATTERNS)
    )
    assert last_term < visible.index(diagram_ref)
    assert visible.index(diagram_ref) < visible.index("## 🧪")


@pytest.mark.parametrize("page", PAGES.values())
def test_four_disclosures_are_closed_and_resources_stay_visible(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    openings = re.findall(r"^<details\b[^>]*>", text, flags=re.MULTILINE)
    assert openings == ['<details markdown="1">'] * 4
    assert text.count("</details>") == 4
    assert "<details open" not in text
    resource_table = re.findall(r"<table>.*?</table>", text, flags=re.DOTALL)[-1]
    assert _detail_depth_at(text, text.index(resource_table)) == 0
    assert _detail_depth_at(text, len(text)) == 0


def test_resource_table_preserves_24_urls_ratings_and_true_rowgroups() -> None:
    for locale, page in PAGES.items():
        text = page.read_text(encoding="utf-8")
        table = re.findall(r"<table>.*?</table>", text, flags=re.DOTALL)[-1]
        heading_offset = text.index(RESOURCE_HEADINGS[locale])
        table_offset = text.index(table, heading_offset)
        assert heading_offset < table_offset
        assert _detail_depth_at(text, heading_offset) == 0
        assert _detail_depth_at(text, table_offset) == 0
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
        for url, _rating in RESOURCE_PAIRS:
            url_offset = text.index(url, table_offset, table_offset + len(table))
            assert _detail_depth_at(text, url_offset) == 0


def test_three_locales_share_sources_dates_and_current_status() -> None:
    expected_urls: list[str] | None = None
    for page in PAGES.values():
        text = page.read_text(encoding="utf-8")
        assert text.count(FRESHNESS) == 1
        for literal in (
            "2026-09-13",
            "Microsoft Agent Framework",
            "AutoGen",
            "maintenance mode",
            "Sandbox Agents",
            "Beta",
            "v2.1.203+",
            "16",
            "1,000",
            "2026-05-28",
            "Constitutional AI",
            "runtime LLM judge",
        ):
            assert literal in text
        assert "v2.1.154+" not in text
        urls = re.findall(r"https?://[^)\s<>\"]+", text)
        if expected_urls is None:
            expected_urls = urls
        else:
            assert urls == expected_urls


@pytest.mark.parametrize("locale", PAGES)
def test_legacy_anchor_and_dynamic_workflows_heading_remain_visible(locale: str) -> None:
    visible = _without_details(PAGES[locale].read_text(encoding="utf-8"))
    assert f'<a id="{LEGACY_ANCHORS[locale]}"></a>' in visible
    assert "### 🔀 Dynamic Workflows" in visible


def test_six_locale_diagrams_are_distinct_full_size_pngs_and_referenced() -> None:
    hashes: set[str] = set()
    for locale, diagrams in DIAGRAMS.items():
        page_text = PAGES[locale].read_text(encoding="utf-8")
        for diagram in diagrams:
            data = diagram.read_bytes()
            assert data.startswith(b"\x89PNG\r\n\x1a\n")
            assert struct.unpack(">II", data[16:24]) == (1672, 941)
            hashes.add(hashlib.sha256(data).hexdigest())
            assert f"../resources/diagrams/{diagram.name}" in page_text
    assert len(hashes) == 6


def test_documentation_records_the_advanced_only_boundary_and_image_contract() -> None:
    design = DESIGN.read_text(encoding="utf-8")
    prompt_log = PROMPT_LOG.read_text(encoding="utf-8")
    assert "Stage 7 負責基礎，Stage 7.5 只保留進階選擇" in design
    assert "四張平行概念卡" in prompt_log
    assert "三個判斷是平行結果，不是成熟度階梯" in prompt_log


@pytest.mark.parametrize("page", PAGES.values())
def test_stale_or_repeated_foundation_claims_are_absent(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    forbidden = (
        "Replit Agent 2024",
        "Voyager paper (Wang 2024)",
        "Context 200k",
        "3.5 PR/day",
        "75% reward hacking",
        "2026-05 snapshot",
        "v2.1.154+",
        "Cross-vendor Harness Engineering",
        "Coding Agent Harness",
        '""',
        "“”",
    )
    assert not any(term in text for term in forbidden)


def test_english_body_has_no_untranslated_cjk() -> None:
    text = PAGES["en"].read_text(encoding="utf-8")
    text = text.replace("繁體中文", "").replace("简体中文", "")
    assert re.search(r"[\u3400-\u9fff]", text) is None

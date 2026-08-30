"""Stage 06 standalone Advanced RAG and Agent Memory reading contracts."""

from __future__ import annotations

import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "advanced-rag": {
        "zh-TW": ROOT / "resources/advanced-rag.md",
        "en": ROOT / "resources/advanced-rag.en.md",
        "zh-Hans": ROOT / "resources/advanced-rag.zh-Hans.md",
    },
    "agent-memory": {
        "zh-TW": ROOT / "resources/agent-memory.md",
        "en": ROOT / "resources/agent-memory.en.md",
        "zh-Hans": ROOT / "resources/agent-memory.zh-Hans.md",
    },
}
ROWGROUPS = {
    "advanced-rag": [4, 4, 4],
    "agent-memory": [4, 3, 4],
}
CORE_TERMS = {
    "advanced-rag": (
        "Baseline",
        "Hybrid Search",
        "Reranking",
        "Query Transformation",
        "Contextual Retrieval",
        "Corrective",
        "Agentic RAG",
        "GraphRAG",
    ),
    "agent-memory": ("Chat History", "Context", "RAG", "Memory"),
}


def _without_details(text: str) -> str:
    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.DOTALL)


@pytest.mark.parametrize("topic", PAGES)
@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_deep_dive_has_two_closed_secondary_disclosures(topic: str, locale: str) -> None:
    text = PAGES[topic][locale].read_text(encoding="utf-8")
    openings = re.findall(r"^<details\b[^>]*>", text, flags=re.MULTILINE)
    assert openings == ['<details markdown="1">'] * 2
    assert "<details open" not in text


@pytest.mark.parametrize("topic", PAGES)
@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_required_reading_projects_and_core_terms_are_visible(topic: str, locale: str) -> None:
    text = PAGES[topic][locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    assert "2026-08-30" in visible
    assert len(re.findall(r"⭐{3,5}", visible)) == sum(ROWGROUPS[topic])
    assert visible.count("https://") >= sum(ROWGROUPS[topic]) + 5
    for term in CORE_TERMS[topic]:
        assert re.search(rf"\*\*[^*]*{re.escape(term)}[^*]*\*\*", visible)


@pytest.mark.parametrize("topic", PAGES)
@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_resource_tables_use_real_rowgroups(topic: str, locale: str) -> None:
    text = PAGES[topic][locale].read_text(encoding="utf-8")
    table = re.search(r"<table>.*?⭐{3,5}.*?</table>", text, flags=re.DOTALL)
    assert table
    groups = re.findall(r"<tbody>(.*?)</tbody>", table.group(), flags=re.DOTALL)
    assert len(groups) == len(ROWGROUPS[topic])
    for group, rows in zip(groups, ROWGROUPS[topic]):
        assert len(re.findall(r"<tr>", group)) == rows
        assert f'scope="rowgroup" rowspan="{rows}"' in group
    assert sum(int(value) for value in re.findall(r'rowspan="(\d+)"', table.group())) == sum(
        ROWGROUPS[topic]
    )


@pytest.mark.parametrize("topic", PAGES)
def test_locale_pages_share_external_sources_and_ratings(topic: str) -> None:
    texts = {locale: page.read_text(encoding="utf-8") for locale, page in PAGES[topic].items()}
    urls = {
        locale: re.findall(r"https://[^)\s<>\"]+", text)
        for locale, text in texts.items()
    }
    ratings = {
        locale: re.findall(r"⭐{3,5}", text)
        for locale, text in texts.items()
    }
    assert urls["zh-TW"] == urls["en"] == urls["zh-Hans"]
    assert ratings["zh-TW"] == ratings["en"] == ratings["zh-Hans"]


@pytest.mark.parametrize("locale,suffix", (("zh-TW", ""), ("en", ".en"), ("zh-Hans", ".zh-Hans")))
def test_pages_link_back_to_locale_matching_stage06(locale: str, suffix: str) -> None:
    expected = f"../stages/06-memory-rag{suffix}.md"
    for topic in PAGES:
        text = PAGES[topic][locale].read_text(encoding="utf-8")
        assert text.count(expected) == 2


@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_advanced_rag_keeps_the_full_learning_ladder(locale: str) -> None:
    visible = _without_details(PAGES["advanced-rag"][locale].read_text(encoding="utf-8"))
    for term in (
        "BM25",
        "Multi-Query",
        "HyDE",
        "RAG Fusion",
        "Self-RAG",
        "CRAG",
        "Adaptive RAG",
        "RAPTOR",
        "DSPy",
    ):
        assert term in visible
    assert "maintenance mode" in visible


@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_memory_page_keeps_lifecycle_and_safety_visible(locale: str) -> None:
    visible = _without_details(PAGES["agent-memory"][locale].read_text(encoding="utf-8"))
    for term in ("Semantic Memory", "Episodic Memory", "Procedural Memory", "namespace"):
        assert term in visible
    for operation in ("add", "search", "update", "delete"):
        assert operation in visible
    assert "user_id" in visible
    assert "API key" in visible


@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_memory_page_uses_current_letta_and_mem0_entrypoints(locale: str) -> None:
    text = PAGES["agent-memory"][locale].read_text(encoding="utf-8")
    assert "https://github.com/letta-ai/letta" in text
    assert "landing page" in text
    assert "https://github.com/letta-ai/letta-code" in text
    assert "https://github.com/mem0ai/memory-benchmarks" in text
    assert "https://github.com/mem0ai/mem0/tree/main/evaluation" not in text


@pytest.mark.parametrize("topic", PAGES)
@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_stale_or_broken_copy_is_absent(topic: str, locale: str) -> None:
    text = PAGES[topic][locale].read_text(encoding="utf-8")
    forbidden = (
        "explodinggradients/ragas",
        "text-embedding-ada-002",
        "★ 51k+",
        "★ 62k+",
        '""',
        "“”",
        "邀請限定",
    )
    assert not any(term in text for term in forbidden)

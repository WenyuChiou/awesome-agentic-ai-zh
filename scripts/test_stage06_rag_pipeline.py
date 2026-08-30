"""Contracts for the Stage 06 detailed RAG pipeline and localized diagrams."""

from __future__ import annotations

import hashlib
import re
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "zh-TW": ROOT / "stages/06-memory-rag.md",
    "en": ROOT / "stages/06-memory-rag.en.md",
    "zh-Hans": ROOT / "stages/06-memory-rag.zh-Hans.md",
}
ADVANCED_PAGES = {
    "zh-TW": ROOT / "resources/advanced-rag.md",
    "en": ROOT / "resources/advanced-rag.en.md",
    "zh-Hans": ROOT / "resources/advanced-rag.zh-Hans.md",
}
DIAGRAMS = {
    "zh-TW": ROOT / "resources/diagrams/rag-pipeline-overview.png",
    "en": ROOT / "resources/diagrams/rag-pipeline-overview.en.png",
    "zh-Hans": ROOT / "resources/diagrams/rag-pipeline-overview.zh-Hans.png",
}
PIPELINE_HEADINGS = {
    "zh-TW": "## 🌐 RAG 基礎流水線",
    "en": "## 🌐 Basic RAG pipeline",
    "zh-Hans": "## 🌐 RAG 基础流水线",
}


def _basic_pipeline_detail(text: str) -> str:
    matches = re.findall(r'<details markdown="1">(.*?)</details>', text, flags=re.DOTALL)
    candidates = [block for block in matches if "2-step RAG" in block]
    assert len(candidates) == 1
    return candidates[0]


def test_each_locale_uses_its_own_readable_distinct_pipeline_diagram() -> None:
    hashes: set[str] = set()
    for locale, diagram in DIAGRAMS.items():
        data = diagram.read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", data[16:24])
        assert width >= 1600 and height >= 900
        hashes.add(hashlib.sha256(data).hexdigest())

        text = PAGES[locale].read_text(encoding="utf-8")
        detail = _basic_pipeline_detail(text)
        assert f"../resources/diagrams/{diagram.name}" in detail
    assert len(hashes) == 3


def test_pipeline_keeps_two_lanes_and_optional_steps_clear() -> None:
    expected = {
        "zh-TW": ("先整理資料", "問題來", "可選", "證據", "來源"),
        "en": ("prepares the data", "question arrives", "optional", "evidence", "citations"),
        "zh-Hans": ("先整理数据", "问题来", "可选", "证据", "来源"),
    }
    for locale, page in PAGES.items():
        detail = _basic_pipeline_detail(page.read_text(encoding="utf-8"))
        for term in expected[locale]:
            assert term.casefold() in detail.casefold()
        assert "2-step RAG" in detail
        assert "Agentic RAG" in detail
        assert "Hybrid RAG" in detail
        assert "Hybrid Search" in detail


def test_retrieval_is_not_reduced_to_vector_database() -> None:
    web_terms = {"zh-TW": "網站", "en": "web", "zh-Hans": "网站"}
    for locale, page in PAGES.items():
        text = page.read_text(encoding="utf-8")
        detail = _basic_pipeline_detail(text)
        for term in ("BM25", "SQL", web_terms[locale], "vector database"):
            assert term.casefold() in detail.casefold()


def test_current_hybrid_search_sources_and_graphrag_status_are_locked() -> None:
    langchain = "https://docs.langchain.com/oss/python/deepagents/retrieval"
    old_langchain = "https://docs.langchain.com/oss/python/langchain/retrieval"
    qdrant = "https://qdrant.tech/documentation/search/hybrid-queries/"
    weaviate = "https://docs.weaviate.io/weaviate/concepts/search/hybrid-search"
    old_urls = (
        "https://qdrant.tech/documentation/concepts/hybrid-queries/",
        "https://docs.weaviate.io/weaviate/search/hybrid",
    )
    maintenance_terms = {
        "zh-TW": "維護模式",
        "en": "maintenance mode",
        "zh-Hans": "维护模式",
    }
    for locale, page in PAGES.items():
        gateway = page.read_text(encoding="utf-8")
        advanced = ADVANCED_PAGES[locale].read_text(encoding="utf-8")
        combined = gateway + advanced
        assert langchain in combined
        assert old_langchain not in combined
        assert "2026-08-30" in gateway
        assert "2026-08-30" in advanced
        assert qdrant in advanced
        assert weaviate in advanced
        assert not any(url in combined for url in old_urls)
        assert "https://github.com/microsoft/graphrag" in advanced
        assert re.search(
            rf"GraphRAG.{{0,500}}{maintenance_terms[locale]}", advanced, flags=re.DOTALL
        )


def test_pipeline_diagram_stays_inside_a_closed_disclosure() -> None:
    for page in PAGES.values():
        text = page.read_text(encoding="utf-8")
        detail = _basic_pipeline_detail(text)
        assert "rag-pipeline-overview" in detail
        opening = text[: text.index(detail)].rsplit("<details", 1)[-1].split(">", 1)[0]
        assert " open" not in opening


def test_pipeline_heading_stays_visible_and_adjacent_to_its_disclosure() -> None:
    for locale, page in PAGES.items():
        text = page.read_text(encoding="utf-8")
        heading = PIPELINE_HEADINGS[locale]
        expected = (
            f'{heading}\n\n<details markdown="1">\n'
            "<summary>"
        )
        assert text.count(heading) == 1
        assert expected in text
        assert "\n## " not in _basic_pipeline_detail(text)

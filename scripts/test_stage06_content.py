"""Stage 06 reader-path, fact, and locale-mirror regression checks."""

from __future__ import annotations

import hashlib
import re
import struct
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "zh-TW": ROOT / "stages/06-memory-rag.md",
    "en": ROOT / "stages/06-memory-rag.en.md",
    "zh-Hans": ROOT / "stages/06-memory-rag.zh-Hans.md",
}
DIAGRAMS = {
    "zh-TW": ROOT / "resources/diagrams/rag-memory-map.png",
    "en": ROOT / "resources/diagrams/rag-memory-map.en.png",
    "zh-Hans": ROOT / "resources/diagrams/rag-memory-map.zh-Hans.png",
}
DIAGRAM_ALT_TEXT = {
    "zh-TW": "RAG 取回外部證據；Memory 寫入並讀回重要狀態",
    "en": "RAG retrieves external evidence; Memory writes and reads back important state",
    "zh-Hans": "RAG 检索外部证据；Memory 写入并读回重要状态",
}

# Old heading slugs are public deep links. The beginner rewrite gives those
# ideas clearer headings, so every former slug remains as an explicit alias.
LEGACY_ANCHORS = {
    "zh-TW": """
agent-需要的兩種-context-能力
-context-engineering-是什麼先定位
五層-stack-中的位置
本-stage-處理-4-個-sub-problem-中的-2-個lance-martin-2025-framework
4-個常被搞混的概念--一張表分清楚
rag-vs-long-context-vs-fine-tuning--何時用什麼
-進入條件
-單元指引漸進式-flow
-adaptive--agentic-rag--self-rag--crag--adaptive-rag讓-retrieval-變成可判斷的流程
-動手練習基礎-illustrative-練習
練習-1embeddings
練習-2vector-db
練習-3chunking-對照
練習-4完整-rag-流水線
練習-5long-term-memory
-rag-進階技巧縱覽--2025-2026-三條主軸
-contextual-retrieval--anthropic-的-prompt-caching-解法
-hybrid-search--reranking--production-rag-的兩個常見強化元件
-常用-memory--rag-工具推薦按用途分類
query-transformations--hyde--multi-query--rag-fusion
-raptor--階層式遞迴-retrievaliclr-2024
-dspy--不寫-prompt用-program-自動-optimizepath-3-paradigm
stage-6--上下文管理context-engineeringrag-與-memory
先把名詞切開retrieval--rag--vector-store--memory-不是同一件事
-5-個可上線使用的-memory-layer按-use-case-挑
2024-2026-最新-memory-作品--三條主軸
-進階-reasoning--reflection--2024-2026-思潮--兩個-track-都看
path-1prompt-based-reflection--reasoning傳統做法
path-2trained-in-reasoning--reflection2024-2026-大轉折
兩條路怎麼選
-精選-projects範本--spec--範例-collection
""".split(),
    "en": """
the-two-context-capabilities-an-agent-needs
-what-is-context-engineering-positioning
where-it-sits-in-the-five-layer-stack
this-stage-covers-2-of-the-4-sub-problems-lance-martin-2025-framing
four-concepts-commonly-mixed-up
rag-vs-long-context-vs-fine-tuning--when-to-use-what
-learning-objectives
-prerequisites
-unit-guide-progressive-flow
-adaptive--agentic-rag--self-rag--crag--adaptive-rag-2024-focus
3-design-patterns-when-to-use-what--essential-for-track-b
-want-to-implement--dive-deeper
-hands-on-exercises-illustrative-basics
exercise-1-embeddings
exercise-2-vector-db
exercise-3-chunking-comparison
exercise-4-full-rag-pipeline
exercise-5-long-term-memory
-advanced-rag-techniques-read-after-basic-rag
-overview-of-advanced-rag-techniques--2025-2026-main-themes-
-graphrag--knowledge-graph--rag
-contextual-retrieval--anthropics-prompt-caching-solution
-hybrid-search--reranking--two-common-reinforcement-components-for-production-rag
-recommended-tools-for-common-memory--rag-use-cases-categorized-by-purpose
query-transformations--hyde--multi-query--rag-fusion
-raptor--hierarchical-recursive-retrieval-iclr-2024
-dspy--programmatic-optimization-without-prompting-path-3-paradigm
stage-6--context-engineering-rag-and-memory
separate-the-terms-first-retrieval--rag--vector-store--memory-are-not-the-same-thing
-from-rag-to-memory--why-rag-isnt-enough
-5-mainstream-memory-layers-that-can-ship-choose-by-use-case
2024-2026-latest-memory-works--3-main-themes
advanced-generative-agents--triple-score-weighting-classic-case-study
-advanced-reasoning--reflection--2024-2026-trends--covers-both-tracks
path-1-prompt-based-reflection--reasoning-traditional-approach
path-2-trained-in-reasoning--reflection-major-shift-in-2024-2026
how-to-choose-between-the-two-paths
-rag--memory-eval--running-is-not-running-accurately
-featured-projects-templates--specs--example-collections
-what-is-memory--how-to-design-it
advanced-coala-framework--a-4-layer-taxonomy-for-agent-memory
-advanced-full-reflexion-with-persistent-memory--track-b-elective
-self-check-before-entering-stage-7
""".split(),
    "zh-Hans": """
agent-需要的两种-context-能力
-context-engineering-是什么先定位
在五层-stack-里的位置
本-stage-处理-4-个-sub-problem-中的-2-个lance-martin-2025-框架
四个常被混淆的概念
rag-vs-long-context-vs-fine-tuning--何时用什么
-进入条件
-必读材料
-单元指引渐进式流程
-进阶-rag-技巧跑完基础-rag-之后再看
-adaptive--agentic-rag--self-rag--crag--adaptive-rag2024-主轴
-动手练习基础示例性练习
练习-1embeddings
练习-2vector-db
练习-3chunking-对照
练习-4完整-rag-流水线
练习-5long-term-memory
-rag-进阶技巧概览--2025-2026-年的三大主线-
-contextual-retrieval--anthropic-的-prompt-caching-解决方案
-hybrid-search--reranking--production-rag-的两个常见强化组件
-常用-memory--rag-工具推荐按用途分类
query-transformations--hyde--multi-query--rag-fusion
-raptor--阶层式递归检索iclr-2024
-dspy--不写-prompt用程序自动优化path-3-范式
stage-6--上下文管理context-engineeringrag-与-memory
先把名词切开retrieval--rag--vector-store--memory-不是同一件事
-5-个可上生产的-memory-layer按-use-case-选
2024-2026-最新-memory-作品--三大主线
进阶generative-agents--三重评分加权经典案例
-进阶-reasoning--reflection--2024-2026-年思潮--覆盖两种路径
path-1-prompt-based-reflection--reasoning传统做法
path-2-trained-in-reasoning--reflection2024-2026-年重大转变
两条路径如何选择
-精选-projects模板--规范--示例合集
进阶coala-framework--agent-memory-的-4-层分类法
""".split(),
}

SECTION_HEADINGS = {
    "zh-TW": [
        "## 📌 學習目標",
        "## 🧩 先認識七個核心詞",
        "## 🚪 進入條件與閱讀路線",
        "## 📚 必修閱讀",
        "## 🛠 動手練習",
        "## 🎯 精選 Projects 與學習資源",
        "## ✅ 進入 Stage 7 前的自我檢查",
    ],
    "en": [
        "## 📌 Learning goals",
        "## 🧩 Meet seven core terms first",
        "## 🚪 Entry requirements and reading paths",
        "## 📚 Required reading",
        "## 🛠 Hands-on exercises",
        "## 🎯 Curated projects and learning resources",
        "## ✅ Self-check before Stage 7",
    ],
    "zh-Hans": [
        "## 📌 学习目标",
        "## 🧩 先认识七个核心术语",
        "## 🚪 进入条件与阅读路径",
        "## 📚 必修阅读",
        "## 🛠 动手练习",
        "## 🎯 精选项目与学习资源",
        "## ✅ 进入 Stage 7 前的自我检查",
    ],
}

EXERCISE_HEADINGS = {
    "zh-TW": [
        "### 練習 1：把兩句話變成 Embedding",
        "### 練習 2：把 Embedding 放進 Vector Database",
        "### 練習 3：比較三種 Chunking 方法",
        "### 練習 4：串起完整 RAG",
        "### 練習 5：記住一項偏好",
    ],
    "en": [
        "### Exercise 1: Turn two sentences into embeddings",
        "### Exercise 2: Put embeddings in a vector database",
        "### Exercise 3: Compare three chunking methods",
        "### Exercise 4: Connect a complete RAG pipeline",
        "### Exercise 5: Remember a preference",
    ],
    "zh-Hans": [
        "### 练习 1：把两句话变成 Embedding",
        "### 练习 2：把 Embedding 放进 Vector Database",
        "### 练习 3：比较三种 Chunking 方法",
        "### 练习 4：串起完整 RAG",
        "### 练习 5：记住一项偏好",
    ],
}

CORE_LABELS = {
    "zh-TW": [
        "Retrieval（檢索）",
        "RAG（Retrieval-Augmented Generation）",
        "Embedding（嵌入向量）",
        "Vector Store／Vector Database",
        "Chunk（文字片段）",
        "Reranking（重新排序）",
        "Memory（記憶）",
    ],
    "en": [
        "Retrieval",
        "RAG (Retrieval-Augmented Generation)",
        "Embedding",
        "Vector Store / Vector Database",
        "Chunk",
        "Reranking",
        "Memory",
    ],
    "zh-Hans": [
        "Retrieval（检索）",
        "RAG（Retrieval-Augmented Generation）",
        "Embedding（嵌入向量）",
        "Vector Store／Vector Database",
        "Chunk（文字片段）",
        "Reranking（重新排序）",
        "Memory（记忆）",
    ],
}

EXERCISE_5_TRUTHFUL_OUTCOMES = {
    "zh-TW": "本練習只會在程式仍執行時新增、搜尋並讀回一項偏好；暫存資料不代表長期持久記憶。",
    "en": "This exercise only adds, searches, and reads one preference while the program is running; temporary storage is not long-term persistence.",
    "zh-Hans": "本练习只会在程序仍运行时新增、搜索并读回一项偏好；临时存储不代表长期持久记忆。",
}


def _without_details(text: str) -> str:
    """Remove closed details bodies so assertions model the first page view."""

    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.DOTALL)


def test_visible_source_excludes_attributed_closed_details_body() -> None:
    hidden = "THIS_OUTCOME_IS_HIDDEN"
    text = (
        '<details markdown="1">\n<summary>More</summary>\n'
        f"{hidden}\n</details>\nVisible outcome.\n"
    )
    visible = _without_details(text)
    assert hidden not in visible
    assert "Visible outcome." in visible


@pytest.mark.parametrize("locale", PAGES)
def test_visible_beginner_path_is_ordered_and_complete(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    positions = [visible.index(heading) for heading in SECTION_HEADINGS[locale]]
    assert positions == sorted(positions)
    assert "<details open" not in text
    for heading in EXERCISE_HEADINGS[locale]:
        assert heading in visible


@pytest.mark.parametrize("locale", PAGES)
def test_closed_disclosures_render_their_markdown(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    openings = re.findall(r"^<details\b[^>]*>", text, flags=re.MULTILINE)
    assert len(openings) == 2
    assert openings == ['<details markdown="1">'] * 2


@pytest.mark.parametrize("locale", PAGES)
def test_required_reading_and_rated_resources_stay_visible(locale: str) -> None:
    visible = _without_details(PAGES[locale].read_text(encoding="utf-8"))
    for url in (
        "https://docs.langchain.com/oss/python/deepagents/retrieval",
        "https://developers.llamaindex.ai/python/framework/getting_started/concepts/",
        "https://docs.trychroma.com/docs/overview/getting-started",
        "https://docs.langchain.com/oss/python/langgraph/agentic-rag",
    ):
        assert url in visible
    assert "../resources/advanced-rag" in visible
    assert "../resources/agent-memory" in visible
    assert visible.count("<tr>") >= 10
    assert visible.count("⭐") >= 9


@pytest.mark.parametrize("locale", PAGES)
def test_legacy_deep_links_have_explicit_aliases(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    explicit = set(re.findall(r'<a\s+(?:id|name)="([^"]+)"', text))
    missing = set(LEGACY_ANCHORS[locale]) - explicit
    assert not missing, f"missing legacy anchor aliases: {sorted(missing)}"
    assert "#<a" not in text


@pytest.mark.parametrize("locale", PAGES)
def test_core_terms_are_bold_and_appear_before_exercises(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    core_start = text.index(SECTION_HEADINGS[locale][1])
    exercise_start = text.index(SECTION_HEADINGS[locale][4])
    core = text[core_start:exercise_start]
    for label in CORE_LABELS[locale]:
        assert f"**{label}**" in core


@pytest.mark.parametrize("locale", PAGES)
def test_exercise_5_does_not_overclaim_ephemeral_memory(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    assert EXERCISE_5_TRUTHFUL_OUTCOMES[locale] in visible


def test_three_locales_share_current_fact_urls_and_date() -> None:
    required = {
        "https://github.com/vibrantlabsai/ragas",
        "https://github.com/run-llama/llama_index",
        "https://github.com/chroma-core/chroma",
    }
    for page in PAGES.values():
        text = page.read_text(encoding="utf-8")
        assert all(url in text for url in required)
        assert "2026-08-30" in text


def test_locale_diagrams_are_distinct_full_size_pngs_and_referenced() -> None:
    hashes: set[str] = set()
    for locale, diagram in DIAGRAMS.items():
        data = diagram.read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n")
        assert struct.unpack(">II", data[16:24]) == (1672, 941)
        hashes.add(hashlib.sha256(data).hexdigest())
        page_text = PAGES[locale].read_text(encoding="utf-8")
        expected_image = f"![{DIAGRAM_ALT_TEXT[locale]}](../resources/diagrams/{diagram.name})"
        assert expected_image in page_text
    assert len(hashes) == 3, "locale diagrams must not reuse identical image bytes"


def test_english_hidden_sections_have_no_untranslated_cjk() -> None:
    text = PAGES["en"].read_text(encoding="utf-8")
    text = text.replace("繁體中文", "").replace("简体中文", "")
    match = re.search(r"[\u3400-\u9fff]", text)
    assert match is None, f"untranslated CJK character at offset {match.start()}"


@pytest.mark.parametrize("page", PAGES.values())
def test_stale_stage06_claims_are_absent(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    forbidden = (
        "text-embedding-ada-002",
        "explodinggradients/ragas",
        "GraphRAG**](https://github.com/microsoft/graphrag) — 原始參考實作，Apache-2.0",
        "GraphRAG**](https://github.com/microsoft/graphrag) — Original reference implementation, Apache-2.0",
        "GraphRAG**](https://github.com/microsoft/graphrag) — 原始参考实现，Apache-2.0",
        "★ 51k+",
        "★ 62k+",
        '""',
        "“”",
    )
    assert not any(term in text for term in forbidden)


@pytest.mark.parametrize("page", PAGES.values())
def test_resource_table_uses_real_rowgroups_and_preserves_9_ratings(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    table = re.search(r"<table>.*?⭐{3,5}.*?</table>", text, flags=re.DOTALL)
    assert table, "missing grouped resource table"
    assert len(re.findall(r'<th scope="col">', table.group())) == 6
    groups = re.findall(r"<tbody>(.*?)</tbody>", table.group(), flags=re.DOTALL)
    assert len(groups) == 3
    expected = [3, 4, 2]
    for group, rows in zip(groups, expected):
        assert len(re.findall(r"<tr>", group)) == rows
        assert f'scope="rowgroup" rowspan="{rows}"' in group
    assert sum(int(value) for value in re.findall(r'rowspan="(\d+)"', text)) == 9
    assert len(re.findall(r"⭐{3,5}", text)) == 9

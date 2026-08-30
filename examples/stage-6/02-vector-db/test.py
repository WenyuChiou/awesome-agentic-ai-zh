"""Stage 6 練習 2 自我驗證 — Chroma collection + query 邏輯。

跑法：
    python test.py

測試使用 fake collection，不下載 embedding model，也不連 API。
"""

from __future__ import annotations

import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import DOCS, build_collection, index_docs, keyword_query, semantic_query


class FakeCollection:
    """只模擬本課會用到的 Chroma 行為，測試時不下載模型。"""

    def __init__(self):
        self.rows: dict[str, dict] = {}

    def count(self):
        return len(self.rows)

    def get(self):
        return {
            "ids": list(self.rows),
            "documents": [row["text"] for row in self.rows.values()],
        }

    def add(self, ids, documents, metadatas):
        for doc_id, text, metadata in zip(ids, documents, metadatas):
            self.rows[doc_id] = {"text": text, "metadata": metadata}

    def query(self, query_texts, n_results):
        query_words = set(re.findall(r"[a-z]+", query_texts[0].lower()))
        aliases = {"typed": "typing", "drink": "coffee", "language": "python"}
        query_words |= {aliases[word] for word in query_words if word in aliases}
        ranked = sorted(
            self.rows.items(),
            key=lambda item: len(query_words & set(re.findall(r"[a-z]+", item[1]["text"].lower()))),
            reverse=True,
        )[:n_results]
        return {
            "ids": [[doc_id for doc_id, _ in ranked]],
            "documents": [[row["text"] for _, row in ranked]],
            "distances": [[float(i) for i in range(len(ranked))]],
        }


class FakeClient:
    def __init__(self):
        self.collections: dict[str, FakeCollection] = {}

    def get_or_create_collection(self, name, embedding_function=None):
        return self.collections.setdefault(name, FakeCollection())


def fresh_collection():
    return build_collection(client=FakeClient(), embedding_function=lambda rows: rows)


def test_default_memory_collections_are_isolated():
    client = FakeClient()
    first = build_collection(client=client, embedding_function=lambda rows: rows)
    second = build_collection(client=client, embedding_function=lambda rows: rows)
    assert first is not second
    print("✅ test_default_memory_collections_are_isolated")


def test_docs_corpus_shape():
    assert len(DOCS) == 8
    assert all({"id", "text", "category"} <= d.keys() for d in DOCS)
    print("✅ test_docs_corpus_shape")


def test_index_and_count():
    collection = fresh_collection()
    index_docs(collection, DOCS)
    assert collection.count() == 8, f"預期 8 doc、得到 {collection.count()}"
    print("✅ test_index_and_count")


def test_semantic_query_ranks_relevant_first():
    """coffee 相關 query 應該 retrieve doc 3（coffee shops）排前。"""
    collection = fresh_collection()
    index_docs(collection, DOCS)
    results = semantic_query(collection, "where to drink good coffee", top_k=3)
    top_ids = [r["id"] for r in results]
    assert "3" in top_ids, f"預期 doc 3（coffee shops）出現在 top-3、得到 {top_ids}"
    print("✅ test_semantic_query_ranks_relevant_first")


def test_keyword_vs_semantic_difference():
    """指出兩個 search 方法差異：
    keyword 對「python programming」會抓 doc 2；
    semantic 對「dynamic language」（無 python 字眼）也能抓到 doc 2。"""
    collection = fresh_collection()
    index_docs(collection, DOCS)

    # Semantic 抓「dynamic language」
    sem_results = semantic_query(collection, "dynamic typed language", top_k=2)
    sem_ids = [r["id"] for r in sem_results]
    assert "2" in sem_ids, f"semantic 應抓到 doc 2、得到 {sem_ids}"

    # Keyword 對同 query「dynamic typed language」未必抓到（因為 doc 2 是「Python is a high-level...dynamic typing」）
    # 至少驗 keyword 不會跨語意：「coffee in Asia」keyword 抓 coffee 句
    kw_results = keyword_query(DOCS, "coffee", top_k=3)
    assert any("coffee" in r["text"].lower() for r in kw_results)
    print("✅ test_keyword_vs_semantic_difference")


def test_top_k_respected():
    collection = fresh_collection()
    index_docs(collection, DOCS)
    assert len(semantic_query(collection, "test", top_k=2)) == 2
    assert len(semantic_query(collection, "test", top_k=5)) == 5
    print("✅ test_top_k_respected")


if __name__ == "__main__":
    test_docs_corpus_shape()
    test_default_memory_collections_are_isolated()
    test_index_and_count()
    test_semantic_query_ranks_relevant_first()
    test_keyword_vs_semantic_difference()
    test_top_k_respected()
    print("\n🎉 全部通過 — Chroma vector DB 邏輯正確")

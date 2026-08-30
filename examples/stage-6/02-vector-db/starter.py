"""Stage 6 練習 2：Vector DB（ChromaDB）— Path A（本機、$0）。

把 embedding 存進 Chroma、做 semantic query、對照 keyword search。

跑法：
    pip install -r requirements.txt
    python starter.py

驗證：
    python test.py

預算：$0。Chroma 跑在本機 SQLite 後端、規模到萬筆都 OK。
"""

from __future__ import annotations

import sys
import uuid
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DOCS = [
    {"id": "1", "text": "Taipei is the capital of Taiwan, known for night markets and tech.", "category": "city"},
    {"id": "2", "text": "Python is a high-level programming language with dynamic typing.", "category": "tech"},
    {"id": "3", "text": "Coffee shops in Taipei often serve pour-over with single-origin beans.", "category": "food"},
    {"id": "4", "text": "Machine learning models learn patterns from training data.", "category": "tech"},
    {"id": "5", "text": "Night markets in Taiwan offer street food like stinky tofu.", "category": "food"},
    {"id": "6", "text": "JavaScript is mainly used for web frontend development.", "category": "tech"},
    {"id": "7", "text": "Tokyo is the capital of Japan with a population of about 14 million.", "category": "city"},
    {"id": "8", "text": "Neural networks use layers of weighted connections.", "category": "tech"},
]


def build_collection(
    path: str = ":memory:",
    collection_name: str | None = None,
    *,
    client: Any = None,
    embedding_function: Any = None,
) -> Any:
    """建立 / 取回 chroma collection。path=':memory:' 表 in-memory。"""
    if client is None:
        import chromadb
        client = (
            chromadb.EphemeralClient()
            if path == ":memory:"
            else chromadb.PersistentClient(path=path)
        )
    if embedding_function is None:
        from chromadb.utils import embedding_functions
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
        )
    if collection_name is None:
        collection_name = (
            f"stage06_demo_{uuid.uuid4().hex[:8]}"
            if path == ":memory:"
            else "stage06_demo"
        )
    collection = client.get_or_create_collection(
        name=collection_name, embedding_function=embedding_function,
    )
    return collection


def index_docs(collection: Any, docs: list[dict]) -> None:
    """Bulk add docs to collection."""
    if collection.count() > 0:
        # Avoid duplicate add—Chroma raises on duplicate id
        existing = set(collection.get()["ids"])
        new = [d for d in docs if d["id"] not in existing]
    else:
        new = docs
    if not new:
        return
    collection.add(
        ids=[d["id"] for d in new],
        documents=[d["text"] for d in new],
        metadatas=[{"category": d["category"]} for d in new],
    )


def semantic_query(collection: Any, query: str, top_k: int = 3) -> list[dict]:
    """Semantic search."""
    result = collection.query(query_texts=[query], n_results=top_k)
    return [
        {"id": result["ids"][0][i], "text": result["documents"][0][i],
         "distance": result["distances"][0][i]}
        for i in range(len(result["ids"][0]))
    ]


def keyword_query(docs: list[dict], query: str, top_k: int = 3) -> list[dict]:
    """簡化 keyword search（substring match、無 BM25）。"""
    q = query.lower()
    matches = [d for d in docs if any(w in d["text"].lower() for w in q.split() if len(w) > 2)]
    return matches[:top_k]


if __name__ == "__main__":
    print("Building Chroma collection (in-memory)...")
    collection = build_collection()
    index_docs(collection, DOCS)
    print(f"   Indexed {collection.count()} docs.\n")

    query = "where to drink good coffee in Asian cities"
    print(f"❓ Query: {query}")
    print("-" * 60)

    print("\n🔍 Semantic search (vector):")
    for r in semantic_query(collection, query, top_k=3):
        print(f"   d={r['distance']:.3f} [{r['id']}] {r['text']}")

    print("\n📝 Keyword search (substring):")
    for r in keyword_query(DOCS, query, top_k=3):
        print(f"   [{r['id']}] {r['text']}")

    # === 自我驗證 ===
    sem_top = semantic_query(collection, query, top_k=1)
    assert sem_top[0]["id"] in {"3", "1"}, f"預期 coffee 或 Taipei 句、得到 {sem_top[0]}"
    assert collection.count() == len(DOCS), "每份文件應只存一次"
    print("\n✅ 練習 2 通過 — Chroma vector DB 跑通、$0/run")
    print("   觀察：query 沒「coffee」字眼、keyword 漏；semantic 抓得到")

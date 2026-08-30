"""Stage 6 練習 4：完整 RAG 流水線 — Path A（Ollama 默認、$0）。

document → chunk → embed → top-k retrieve → LLM 生答案

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter.py

驗證：
    python test.py

預算：$0/run。Path B 用 Claude 生答案、見 starter_anthropic.py。
"""

from __future__ import annotations

import os
import sys
import uuid
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:3b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# Sample knowledge base
KB_DOC = """# Company Onboarding

## Vacation Policy

Full-time employees get 15 days of paid vacation per year, accruing monthly. Unused days roll over up to 5 days into the next year. Vacation must be requested at least 1 week in advance via the HR portal.

## Remote Work

Hybrid model: 3 days in office, 2 days remote per week. Fully remote requires manager approval and HR review.

## Expenses

Submit receipts via Concur within 30 days. Meals over $50 need pre-approval. Travel is booked through corporate travel portal only.

## Tech Stack

We use Python 3.11+ for backend, React 18 for frontend. Code reviews are mandatory; minimum 1 approver before merging to main.
"""


def chunk_doc(text: str) -> list[str]:
    """Simple heading-aware chunking."""
    import re
    sections = re.split(r"\n(?=#{1,3} )", text)
    return [s.strip() for s in sections if s.strip()]


def build_kb(
    doc: str,
    *,
    client: Any = None,
    embedding_function: Any = None,
    collection_name: str | None = None,
) -> Any:
    if client is None:
        import chromadb
        client = chromadb.EphemeralClient()
    if embedding_function is None:
        from chromadb.utils import embedding_functions
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBED_MODEL,
        )
    collection_name = collection_name or f"knowledge_base_{uuid.uuid4().hex[:8]}"
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function,
    )
    chunks = chunk_doc(doc)
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
    )
    return collection


def retrieve(collection: Any, query: str, top_k: int = 2) -> list[str]:
    result = collection.query(query_texts=[query], n_results=top_k)
    return result["documents"][0]


def generate(query: str, contexts: list[str], llm: Any = None) -> str:
    """Use LLM to answer query given retrieved contexts."""
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    context_text = "\n\n---\n\n".join(contexts)
    prompt = f"""Answer the user's question based ONLY on the context below. If the context doesn't contain the answer, say "I don't have that information".

Context:
{context_text}

Question: {query}

Answer:"""
    resp = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content or ""


def rag(
    query: str,
    doc: str = KB_DOC,
    llm: Any = None,
    top_k: int = 2,
    collection: Any = None,
) -> dict:
    """Full RAG pipeline."""
    collection = collection or build_kb(doc)
    contexts = retrieve(collection, query, top_k=top_k)
    answer = generate(query, contexts, llm=llm)
    return {"query": query, "contexts": contexts, "answer": answer}


if __name__ == "__main__":
    queries = [
        "How many vacation days do I get?",
        "Can I work fully remote?",
        "What's the Python version?",
    ]
    for q in queries:
        print(f"\n❓ {q}")
        result = rag(q)
        print(f"   contexts retrieved: {len(result['contexts'])}")
        print(f"   answer: {result['answer']}")

    # === 自我驗證 ===
    result = rag("How many vacation days do I get?")
    assert any("15 days" in c for c in result["contexts"]), \
        f"預期 retrieve 到含 15 days 的 chunk、得到 {result['contexts']}"
    assert result["answer"], "模型應回傳文字答案"
    print("\n✅ 練習 4 通過 — 完整 RAG pipeline 跑通、$0/run（using Ollama {MODEL})")

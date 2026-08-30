"""Stage 6 練習 4：完整 RAG — Path B（Anthropic Claude）。

跟 starter.py 同一個 pipeline、只把 generate() 的 LLM 換成 Claude。
Chunking + retrieval（vector DB）跨 backend 一致。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py

預算：每次 ≈ $0.001（claude-haiku-4-5、短 context + 短答案）。
Production RAG 通常用 cloud LLM 生成、答案質量明顯比 qwen2.5:3b 高。
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

from starter import KB_DOC, build_kb, retrieve

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")


def generate_anthropic(query: str, contexts: list[str], client: Any = None) -> str:
    client = client or anthropic.Anthropic()
    context_text = "\n\n---\n\n".join(contexts)
    prompt = f"""Answer the user's question based ONLY on the context below. If the context doesn't contain the answer, say "I don't have that information".

Context:
{context_text}

Question: {query}

Answer:"""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return " ".join(b.text for b in resp.content if b.type == "text")


def rag_anthropic(query: str, doc: str = KB_DOC, top_k: int = 2) -> dict:
    collection = build_kb(doc)
    contexts = retrieve(collection, query, top_k=top_k)
    answer = generate_anthropic(query, contexts)
    return {"query": query, "contexts": contexts, "answer": answer}


if __name__ == "__main__":
    queries = [
        "How many vacation days do I get?",
        "What's the Python version?",
    ]
    for q in queries:
        print(f"\n❓ {q}")
        result = rag_anthropic(q)
        print(f"   answer: {result['answer']}")
    # === 自我驗證 ===
    assert result["contexts"], "RAG 應找回至少一段 context"
    assert result["answer"], "Claude 應回傳文字答案"
    print(f"\n✅ 練習 4 (Anthropic) 通過 — Claude {MODEL}")

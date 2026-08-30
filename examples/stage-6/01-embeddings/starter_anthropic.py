"""Stage 6 練習 1：Embeddings — Path B（cloud embedding 對照）。

Anthropic 沒提供官方 embedding API、官方推薦 Voyage AI。OpenAI 也是常見選擇。
這份示範用 OpenAI 的 text-embedding-3-small 對照本機 sentence-transformers。

跑法：
    pip install -r requirements.txt
    export OPENAI_API_KEY=sk-...    # OR set VOYAGE_API_KEY
    python starter_anthropic.py

預算：每次 ≈ $0.00002 per 100 sentences（text-embedding-3-small）。極便宜。
但**對 RAG demo / 個人實驗，本機 sentence-transformers 完全夠用**——cloud embedding 主要差別在 multilingual 跟 long-context 場景。
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np

MODEL = os.environ.get("EMBED_MODEL", "text-embedding-3-small")


def embed_openai(texts: list[str], client: Any = None) -> np.ndarray:
    """Encode via OpenAI embeddings API."""
    from openai import OpenAI
    client = client or OpenAI()
    resp = client.embeddings.create(model=MODEL, input=texts)
    vecs = np.array([d.embedding for d in resp.data])
    # Normalize for cosine similarity
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs / norms


def find_nearest_openai(query: str, sentences: list[str], top_k: int = 3) -> list[dict]:
    from openai import OpenAI
    client = OpenAI()
    sent_vecs = embed_openai(sentences, client=client)
    q_vec = embed_openai([query], client=client)[0]
    sims = sent_vecs @ q_vec
    top_idx = np.argsort(-sims)[:top_k]
    return [
        {"sentence": sentences[i], "similarity": float(sims[i]), "rank": int(rank)}
        for rank, i in enumerate(top_idx, 1)
    ]


if __name__ == "__main__":
    from starter import SENTENCES
    query = "I love programming in Python"
    print(f"❓ Query: {query}（using OpenAI {MODEL}）")
    print("-" * 60)
    results = find_nearest_openai(query, SENTENCES, top_k=5)
    for r in results:
        print(f"   #{r['rank']} sim={r['similarity']:.3f}: {r['sentence']}")
    # === 自我驗證 ===
    assert len(results) == 5, f"預期 5 筆結果、得到 {len(results)}"
    assert results[0]["similarity"] >= results[-1]["similarity"], "結果應由相似到不相似排序"
    print("\n✅ 練習 1 (Path B cloud) 通過 — OpenAI embeddings 回傳正常")
    print("   對照本機版本（starter.py）、看 ranking 差異")

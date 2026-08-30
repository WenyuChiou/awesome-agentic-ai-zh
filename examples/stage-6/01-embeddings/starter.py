"""Stage 6 練習 1：Embeddings — Path A（本機 sentence-transformers、$0）。

把 100 個句子轉成 vector、查 nearest neighbors。理解 cosine similarity / distance。

跑法：
    pip install -r requirements.txt
    python starter.py   # 第一次會自動下載 model (~80MB)

驗證：
    python test.py

預算：$0（model 跑在 CPU）。Path B 用 cloud embedding（OpenAI / Voyage）見 starter_anthropic.py。
"""

from __future__ import annotations

import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


SENTENCES = [
    "The cat sat on the mat.",
    "A dog is chasing the ball in the park.",
    "Taipei is the capital of Taiwan.",
    "Python is a programming language.",
    "Machine learning models learn patterns from data.",
    "Neural networks are inspired by the human brain.",
    "Coffee shops in Taipei often serve great pour-over.",
    "JavaScript runs in web browsers.",
    "The weather forecast says it will rain tomorrow.",
    "Cats and dogs are common household pets.",
] + [f"Random filler sentence number {i}." for i in range(90)]


def embed(texts: list[str], model: Any = None) -> np.ndarray:
    """Encode a list of strings to vectors (L2-normalized)."""
    if model is None:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(MODEL_NAME)
    return model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)


def find_nearest(query: str, sentences: list[str], top_k: int = 3, model: Any = None) -> list[dict]:
    """Returns top-k nearest sentences with cosine similarity scores."""
    if top_k < 1:
        raise ValueError("top_k 必須至少是 1")
    if model is None:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(MODEL_NAME)
    sent_vecs = embed(sentences, model=model)
    q_vec = embed([query], model=model)[0]
    # cosine similarity = dot product (because normalized)
    sims = sent_vecs @ q_vec
    top_idx = np.argsort(-sims)[:top_k]
    return [
        {"sentence": sentences[i], "similarity": float(sims[i]), "rank": int(rank)}
        for rank, i in enumerate(top_idx, 1)
    ]


if __name__ == "__main__":
    query = "I love programming in Python"
    print(f"❓ Query: {query}")
    print(f"   Embedding {len(SENTENCES)} sentences with {MODEL_NAME}...")
    print("-" * 60)

    results = find_nearest(query, SENTENCES, top_k=5)
    for r in results:
        print(f"   #{r['rank']} sim={r['similarity']:.3f}: {r['sentence']}")

    # === 自我驗證 ===
    assert "Python" in results[0]["sentence"] or "programming" in results[0]["sentence"].lower(), \
        f"預期 top-1 跟 programming 相關、得到 {results[0]['sentence']}"
    assert len(results) == 5, f"預期 5 筆結果、得到 {len(results)}"
    print("\n✅ 練習 1 通過 — sentence-transformers 在本機跑通、$0/run")
    print("   觀察：cosine similarity 越高、語意越近")

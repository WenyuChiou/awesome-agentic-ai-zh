"""Stage 6 練習 3：Chunking 對照 — 3 種切法 A/B（純 Python、$0）。

同一份文件 → 3 種切法：
  1. fixed-length（每 N 字一段、可加 overlap）
  2. paragraph-based（按段落切、保語意完整）
  3. heading-aware（看 # / ## 切、保章節 hierarchy）

對 5 個真實 query 比較 top-k 結果、看哪種切法撈到正確 context。

跑法：
    pip install -r requirements.txt
    python starter.py

驗證：
    python test.py
"""

from __future__ import annotations

import re
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# 範例 markdown 文件（含 heading + paragraph）
SAMPLE_DOC = """# Taipei Travel Guide

## Food

Taipei is famous for night markets. Shilin Night Market is the most famous, with stinky tofu and bubble tea stalls. Local breakfast often features dan bing (egg crepe) and youtiao with hot soy milk.

For coffee, Taipei has many third-wave specialty shops. Fika Fika and GABEE are well-known. Prices are roughly NT$150-250 per cup.

## Transit

The MRT (metro) covers most tourist areas. EasyCard is the universal payment. A single ride costs NT$20-65. Buses are cheaper but slower.

Bicycles are also popular — YouBike is the city's bike-share. Cost is NT$10 per 30 min.

## Weather

Taipei summer is hot and humid, often 32-35°C with afternoon thunderstorms. Winter is mild (15-20°C) but can be rainy for weeks. The best time to visit is October-November or March-April.
"""


# === 3 個 chunking strategy ===

def chunk_fixed(text: str, chunk_size: int = 200, overlap: int = 40) -> list[str]:
    """固定長度切（with overlap）。簡單但會切壞句子 / 段落。"""
    if chunk_size < 1:
        raise ValueError("chunk_size 必須至少是 1")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap 必須介於 0 和 chunk_size - 1 之間")
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i + chunk_size])
        i += chunk_size - overlap
    return [c.strip() for c in chunks if c.strip()]


def chunk_paragraphs(text: str) -> list[str]:
    """按段落切（雙 newline 為界）。保語意完整、但段落長短不一。"""
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def chunk_headings(text: str) -> list[str]:
    """Heading-aware：按 # / ## 切、每個 section 含 heading + body、有 hierarchy 標記。"""
    sections = re.split(r"\n(?=#{1,3} )", text)
    return [s.strip() for s in sections if s.strip()]


# === Retrieval comparison ===

def embed_chunks(chunks: list[str], model: Any) -> np.ndarray:
    return model.encode(chunks, normalize_embeddings=True, convert_to_numpy=True)


def top_k_for_query(query: str, chunks: list[str], chunk_vecs: np.ndarray,
                    model: Any, k: int = 2) -> list[dict]:
    q_vec = model.encode([query], normalize_embeddings=True, convert_to_numpy=True)[0]
    sims = chunk_vecs @ q_vec
    top_idx = np.argsort(-sims)[:k]
    return [{"chunk": chunks[i], "similarity": float(sims[i])} for i in top_idx]


def compare_strategies(doc: str, queries: list[str], k: int = 2, model: Any = None) -> dict:
    """3 種 chunking、跑同樣 query、回傳對比結果。"""
    if model is None:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(EMBED_MODEL)

    strategies = {
        "fixed_200_overlap_40": chunk_fixed(doc, chunk_size=200, overlap=40),
        "paragraphs": chunk_paragraphs(doc),
        "headings": chunk_headings(doc),
    }

    results = {}
    for name, chunks in strategies.items():
        vecs = embed_chunks(chunks, model)
        per_query = []
        for q in queries:
            per_query.append({"query": q, "top": top_k_for_query(q, chunks, vecs, model, k=k)})
        results[name] = {"chunk_count": len(chunks), "queries": per_query}
    return results


if __name__ == "__main__":
    queries = [
        "What food can I try at night markets?",
        "How much does the MRT cost?",
        "Best time of year to visit?",
        "How to rent bicycles?",
        "Any coffee shops?",
    ]
    print("Document: Taipei Travel Guide (3 headings)")
    print(f"Queries: {len(queries)}\n")

    out = compare_strategies(SAMPLE_DOC, queries, k=2)
    for name, data in out.items():
        print(f"=== {name} ({data['chunk_count']} chunks) ===")
        for entry in data["queries"]:
            best = entry["top"][0]
            print(f"   Q: {entry['query']}")
            print(f"   → sim={best['similarity']:.3f}: {best['chunk'][:80]}...")
        print()

    # === 自我驗證 ===
    assert out["headings"]["chunk_count"] <= 5, "heading chunks 應該少而 self-contained"
    assert set(out) == {"fixed_200_overlap_40", "paragraphs", "headings"}
    print("✅ 練習 3 通過 — 3 種 chunking 對照、$0/run")
    print("   觀察：heading-aware 對 sectional query 最準；fixed-length 容易切壞句子")

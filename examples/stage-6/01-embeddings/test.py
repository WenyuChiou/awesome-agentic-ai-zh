"""Stage 6 練習 1 自我驗證 — 不下載 model、用 mock。

跑法：
    python test.py

驗證內容：
    - find_nearest 排序正確（相關句子 sim 最高）
    - L2-normalized vector 的 dot product = cosine similarity
    - top_k 邊界
"""

from __future__ import annotations

import sys
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np

from starter import SENTENCES, find_nearest


def make_fake_model(vec_map: dict) -> MagicMock:
    """Mock SentenceTransformer：給定 text → vec 對應表。"""
    m = MagicMock()
    def encode(texts, **kw):
        out = np.array([vec_map.get(t, np.zeros(4)) for t in texts])
        # Normalize（模擬 normalize_embeddings=True）
        norms = np.linalg.norm(out, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return out / norms
    m.encode.side_effect = encode
    return m


def test_top_1_is_most_similar():
    """構造 4 個 sentence、其中第 2 個跟 query 完全同向、應排第 1。"""
    sentences = ["a", "b", "c", "d"]
    # 故意做：b 跟 query 同向（→ similarity 1.0）
    vecs = {
        "a": np.array([1, 0, 0, 0], dtype=float),
        "b": np.array([0, 1, 0, 0], dtype=float),
        "c": np.array([0, 0, 1, 0], dtype=float),
        "d": np.array([0, 0, 0, 1], dtype=float),
        "query for b": np.array([0, 1, 0, 0], dtype=float),
    }
    model = make_fake_model(vecs)
    results = find_nearest("query for b", sentences, top_k=2, model=model)
    assert results[0]["sentence"] == "b"
    assert results[0]["similarity"] == 1.0
    print("✅ test_top_1_is_most_similar")


def test_top_k_respected():
    sentences = ["a", "b", "c", "d", "e"]
    vecs = {s: np.random.rand(4) for s in sentences + ["q"]}
    model = make_fake_model(vecs)
    results = find_nearest("q", sentences, top_k=3, model=model)
    assert len(results) == 3
    assert {r["rank"] for r in results} == {1, 2, 3}
    print("✅ test_top_k_respected")


def test_top_k_must_be_positive():
    model = make_fake_model({"a": np.array([1, 0]), "q": np.array([1, 0])})
    try:
        find_nearest("q", ["a"], top_k=0, model=model)
    except ValueError as exc:
        assert "top_k" in str(exc)
    else:
        raise AssertionError("top_k=0 應該被拒絕")
    print("✅ test_top_k_must_be_positive")


def test_similarity_in_minus_one_to_one():
    """L2-normalized → cosine sim ∈ [-1, 1]。"""
    sentences = ["a", "b"]
    vecs = {
        "a": np.array([1, 0, 0, 0], dtype=float),
        "b": np.array([-1, 0, 0, 0], dtype=float),
        "q": np.array([1, 0, 0, 0], dtype=float),
    }
    model = make_fake_model(vecs)
    results = find_nearest("q", sentences, top_k=2, model=model)
    sims = [r["similarity"] for r in results]
    assert all(-1.0 - 1e-6 <= s <= 1.0 + 1e-6 for s in sims), f"sim 越界: {sims}"
    print("✅ test_similarity_in_minus_one_to_one")


def test_corpus_size():
    """SENTENCES corpus 應該有 100 個。"""
    assert len(SENTENCES) == 100, f"預期 100 個句子、得到 {len(SENTENCES)}"
    print("✅ test_corpus_size")


if __name__ == "__main__":
    test_top_1_is_most_similar()
    test_top_k_respected()
    test_top_k_must_be_positive()
    test_similarity_in_minus_one_to_one()
    test_corpus_size()
    print("\n🎉 全部通過 — embedding 邏輯正確（無需下載 model）")

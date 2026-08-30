"""Stage 6 練習 3：Chunking — Path B concept demo（同 starter）。

Chunking 是純資料前處理、不依賴 LLM。Path A == Path B。
要把 retrieval 結果丟給 Claude 生答案、見 練習 4 完整 RAG。
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import SAMPLE_DOC, compare_strategies

if __name__ == "__main__":
    print("ℹ️ Chunking 跨 LLM provider 一致、Path A == Path B。")
    out = compare_strategies(SAMPLE_DOC, ["food at night markets"], k=1)
    for name, data in out.items():
        print(f"   {name}: {data['chunk_count']} chunks")
    # === 自我驗證 ===
    assert set(out) == {"fixed_200_overlap_40", "paragraphs", "headings"}
    assert all(data["queries"] for data in out.values()), "每種切法都要跑查詢"
    print("✅ 練習 3 (concept demo) 通過")

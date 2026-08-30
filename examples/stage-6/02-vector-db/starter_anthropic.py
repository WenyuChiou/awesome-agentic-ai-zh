"""Stage 6 練習 2：Vector DB — Path B 概念展示。

Chroma 本身是本機 vector DB、不依賴 LLM provider。Path B 跟 Path A 跑出來一樣。
RAG 流水線裡的 LLM 步驟（generation）會在練習 4 才出現——這題只測 retrieval。

要切 cloud-grade embedding（OpenAI / Voyage）見 starter.py 註解：
    把 embed_fn 換成 OpenAIEmbeddingFunction(api_key=..., model_name=...)
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import DOCS, build_collection, index_docs, semantic_query

if __name__ == "__main__":
    print("ℹ️ Vector DB（Chroma）跨 LLM provider 一致。Path A == Path B。")
    print("   Cloud embedding 替換在 build_collection() 註解、不必跑 LLM。\n")
    collection = build_collection()
    index_docs(collection, DOCS)
    results = semantic_query(collection, "coffee in Asian cities", top_k=2)
    for r in results:
        print(f"   {r}")
    # === 自我驗證 ===
    assert collection.count() == len(DOCS), "全部文件都應寫入 collection"
    assert len(results) == 2, "top_k=2 應回傳兩筆"
    print("✅ 練習 2 (concept demo) 通過")

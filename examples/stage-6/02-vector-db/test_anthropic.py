"""Stage 6 練習 2 — Path B 載入檢查。

Vector DB 跨 LLM provider 一致、Path B 跟 Path A 跑出來相同。
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def test_path_b_reuses_vector_db_code():
    import starter_anthropic
    assert hasattr(starter_anthropic, "build_collection")
    assert hasattr(starter_anthropic, "semantic_query")
    print("✅ test_path_b_reuses_vector_db_code")


if __name__ == "__main__":
    test_path_b_reuses_vector_db_code()
    print("\n🎉 通過 — Path B concept demo 可載入")

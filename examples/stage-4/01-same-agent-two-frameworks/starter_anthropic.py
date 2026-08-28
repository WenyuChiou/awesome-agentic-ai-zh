"""Stage 4 練習 1：同一個 agent、兩個 framework — LangGraph + Anthropic（Path B）。

跟 starter.py 同樣的 LangGraph 圖、只把 LLM backend 換成 Claude。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py

預算：每次 ≈ $0.001（claude-haiku-4-5）。
Ollama 版本見 starter.py。
"""

from __future__ import annotations

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from langchain_anthropic import ChatAnthropic

from starter import run

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")


if __name__ == "__main__":
    query = "summarize what you know about Taipei"
    print(f"❓ Query: {query}（using Anthropic {MODEL}）")
    print("-" * 60)
    llm = ChatAnthropic(model=MODEL, temperature=0)
    result = run(query, llm=llm)
    print(f"✅ Final: {result['final']}")
    print(f"   Steps: {result['steps']}")
    assert result["final"], "expected non-empty summary"
    assert result["steps"] >= 2, "expected a visible graph trace"
    print("✅ 練習 1 (Anthropic path) 通過 — LangGraph + 固定 Anthropic model ID；費用依 tokens 計算")

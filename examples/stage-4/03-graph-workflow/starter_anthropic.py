"""Stage 4 練習 3 Path B：把同一張 LangGraph 圖接到 ChatAnthropic。

流程、暫停點與人工核准規則都不變；只有負責寫草稿的模型不同。
"""

from __future__ import annotations

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from langchain_anthropic import ChatAnthropic
from starter import run

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")


def make_anthropic_llm() -> ChatAnthropic:
    """建立使用固定 model ID 的 Anthropic chat model。"""
    return ChatAnthropic(model=MODEL, temperature=0)


if __name__ == "__main__":
    result = run("What is the Taipei population?", approve=True, llm=make_anthropic_llm())
    print(result["final"])
    assert result["final"].startswith("PUBLISHED:")
    assert "Taipei" in result["final"]

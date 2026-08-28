r"""Stage 4 練習 2 Path B：用 Anthropic 跑同一個三角色 CrewAI 流程。

CrewAI 用 provider-prefixed model string 選擇後端；
``crewai[anthropic]`` 會安裝 Anthropic provider，這份範例再固定 model ID。

跑法：
    $env:ANTHROPIC_API_KEY="sk-ant-..."
    .\.venv\Scripts\python.exe starter_anthropic.py

實際費用依 tokens、呼叫次數與重試而變；README 提供公式與 $0.10 支出上限。
"""

from __future__ import annotations

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import run

MODEL = os.environ.get("MODEL", "anthropic/claude-haiku-4-5-20251001")  # provider-prefixed format


if __name__ == "__main__":
    topic = "react"
    print(f"❓ Topic: {topic}（using CrewAI + Anthropic {MODEL}）")
    print(f"   3 agents: Researcher → Writer → Critic（sequential）")
    print("-" * 60)
    result = run(topic, llm_model=MODEL)
    print(f"✅ Final (critic's verdict):\n{result['final']}")
    assert result["final"], "expected critic to produce a verdict"
    assert "max_iter=4" in result["stop_condition"]
    print("\n✅ 練習 2 (Anthropic path) 通過 — 3-agent crew 已走到有界停止條件")

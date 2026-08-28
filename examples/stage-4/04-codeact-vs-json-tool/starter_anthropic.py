"""Stage 4 練習 4 Path B：用 LiteLLM 的固定 Anthropic model ID 跑 CodeAct。

它和 Path A 共用同一組工具、Docker 邊界與最多四步的限制。
"""

from __future__ import annotations

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from smolagents import LiteLLMModel
from starter import run

MODEL = os.environ.get("MODEL", "anthropic/claude-haiku-4-5-20251001")


def make_anthropic_model() -> LiteLLMModel:
    """建立 Smolagents 可識別的 Anthropic LiteLLM model。"""
    return LiteLLMModel(model_id=MODEL)


if __name__ == "__main__":
    result = run("Find Taipei population divided by New York population.", model=make_anthropic_model())
    print(result["final"])
    assert result["final"]
    assert MODEL.startswith("anthropic/")

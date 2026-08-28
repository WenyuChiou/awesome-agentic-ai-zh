"""Stage 4 練習 5 Path B：用固定 Anthropic model ID 跑同一個輸出契約。"""

from __future__ import annotations

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pydantic_ai.models.anthropic import AnthropicModel
from starter import run

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")


def make_anthropic_model() -> AnthropicModel:
    """建立 Pydantic AI 目前支援的 Anthropic model 物件。"""
    return AnthropicModel(MODEL)


if __name__ == "__main__":
    answer = run("What is the population of Taipei?", model=make_anthropic_model())
    print(answer.model_dump())
    assert answer.answer and answer.sources
    assert 0.0 <= answer.confidence <= 1.0

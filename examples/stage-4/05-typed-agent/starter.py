"""Stage 4 練習 5：用 Pydantic AI ``output_type`` 檢查輸出形狀。

型別檢查像表格的格子：它能確保欄位存在、種類正確、數字在範圍內，
但不能證明內容是真的。真實性仍要靠可信來源與額外的語意檢查。
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pydantic import BaseModel, Field, field_validator
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

MODEL = os.environ.get("MODEL", "qwen2.5:3b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")


class AnswerWithConfidence(BaseModel):
    """已驗證的資料形狀；它不是答案為真的證據。"""
    answer: str = Field(min_length=1, description="A non-empty, cautious answer.")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence from 0.0 through 1.0.")
    sources: list[str] = Field(min_length=1, description="At least one non-empty source label.")

    @field_validator("answer")
    @classmethod
    def answer_is_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("answer must not be blank")
        return value.strip()

    @field_validator("sources")
    @classmethod
    def sources_are_nonempty_labels(cls, value: list[str]) -> list[str]:
        if not all(isinstance(item, str) and item.strip() for item in value):
            raise ValueError("sources must contain non-empty strings")
        return [item.strip() for item in value]


def make_ollama_model() -> OpenAIChatModel:
    """用目前 Pydantic AI 的 OpenAIChatModel 連到本機 Ollama。"""
    return OpenAIChatModel(MODEL, provider=OpenAIProvider(base_url=OLLAMA_BASE, api_key="ollama"))


def build_agent(model: Any | None = None) -> Agent:
    """建立會重試兩次、並要求 AnswerWithConfidence 的 agent。"""
    return Agent(
        model or make_ollama_model(),
        output_type=AnswerWithConfidence,
        retries=2,
        instructions=(
            "Return a cautious AnswerWithConfidence. Use a non-empty answer, a confidence between 0 and 1, "
            "and at least one source label. A valid schema does not establish semantic truth."
        ),
    )


def run(question: str, model: Any | None = None) -> AnswerWithConfidence:
    """執行 agent，並在回傳前再檢查本練習的結果契約。"""
    output = build_agent(model).run_sync(question).output
    if not output.answer or not output.sources or not 0.0 <= output.confidence <= 1.0:
        raise RuntimeError("Validated output did not meet the exercise's result contract.")
    return output


if __name__ == "__main__":
    answer = run("What is the population of Taipei?")
    print(answer.model_dump())
    assert 0.0 <= answer.confidence <= 1.0
    assert answer.answer and answer.sources

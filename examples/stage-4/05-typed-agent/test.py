"""Path A 離線行為測試：使用 Pydantic AI 官方 TestModel，不連網。"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pydantic import ValidationError
from pydantic_ai.models.test import TestModel
from starter import AnswerWithConfidence, run


def test_official_test_model_produces_valid_typed_output() -> None:
    model = TestModel(custom_output_args={"answer": "Offline answer", "confidence": 0.6, "sources": ["offline fixture"]})
    answer = run("Test question", model=model)
    assert answer.answer == "Offline answer"
    assert answer.sources == ["offline fixture"]


def test_invalid_contract_values_are_rejected() -> None:
    invalid = [
        {"answer": "ok", "confidence": 1.1, "sources": ["source"]},
        {"answer": "ok", "confidence": 0.5, "sources": "source"},
        {"answer": " ", "confidence": 0.5, "sources": ["source"]},
        {"answer": "ok", "confidence": 0.5, "sources": []},
    ]
    for payload in invalid:
        try:
            AnswerWithConfidence.model_validate(payload)
        except ValidationError:
            pass
        else:
            raise AssertionError(f"Expected validation failure for {payload!r}")


if __name__ == "__main__":
    test_official_test_model_produces_valid_typed_output()
    test_invalid_contract_values_are_rejected()
    print("all pass")

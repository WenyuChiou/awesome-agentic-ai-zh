"""Path B 離線行為測試：檢查 Anthropic 設定，再用官方 TestModel 執行。"""

from __future__ import annotations

import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pydantic_ai.models.test import TestModel
from starter import run
from starter_anthropic import MODEL, make_anthropic_model


def test_anthropic_provider_construction() -> None:
    os.environ.setdefault("ANTHROPIC_API_KEY", "offline-test-key")
    model = make_anthropic_model()
    assert MODEL == "claude-haiku-4-5-20251001"
    assert model.model_name == MODEL


def test_path_b_behavior_with_official_offline_model() -> None:
    offline = TestModel(custom_output_args={"answer": "Offline Anthropic-path answer", "confidence": 0.4, "sources": ["fixture"]})
    answer = run("Test question", model=offline)
    assert answer.answer.startswith("Offline Anthropic")
    assert answer.confidence == 0.4


if __name__ == "__main__":
    test_anthropic_provider_construction()
    test_path_b_behavior_with_official_offline_model()
    print("all pass")

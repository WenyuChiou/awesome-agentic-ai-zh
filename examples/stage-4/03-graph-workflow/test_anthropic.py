"""Path B 離線行為測試：檢查 Anthropic 設定，並用假模型跑共用圖。"""

from __future__ import annotations

import sys
import os
from types import SimpleNamespace

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import run
from starter_anthropic import MODEL, make_anthropic_llm


class FakeAnthropicLLM:
    """不發出 API 請求，只提供可預測的 Anthropic-path 草稿。"""
    def invoke(self, prompt: str) -> SimpleNamespace:
        return SimpleNamespace(content="Anthropic-path offline draft")


def test_anthropic_provider_construction() -> None:
    os.environ.setdefault("ANTHROPIC_API_KEY", "offline-test-key")
    llm = make_anthropic_llm()
    assert llm.model == MODEL
    assert MODEL == "claude-haiku-4-5-20251001"


def test_anthropic_path_graph_behavior() -> None:
    result = run("Explain Python", approve=True, llm=FakeAnthropicLLM(), thread_id="anthropic-offline")
    assert result["final"] == "PUBLISHED: Anthropic-path offline draft"
    assert result["approved"] is True


if __name__ == "__main__":
    test_anthropic_provider_construction()
    test_anthropic_path_graph_behavior()
    print("all pass")

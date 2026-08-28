"""Offline behavioral test for Path B; no Anthropic request is made."""

from __future__ import annotations

import sys
import os
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from langchain_core.messages import AIMessage
from starter import run
from starter_anthropic import MODEL


def test_pinned_provider_and_shared_graph_behavior() -> None:
    from langchain_anthropic import ChatAnthropic
    assert MODEL == "claude-haiku-4-5-20251001"
    os.environ.setdefault("ANTHROPIC_API_KEY", "offline-test-key")
    assert ChatAnthropic(model=MODEL, temperature=0).model == MODEL
    llm = MagicMock()
    llm.bind_tools.return_value = llm
    llm.invoke.side_effect = [
        AIMessage(content="", tool_calls=[{"name": "search", "args": {"query": "Taipei"}, "id": "call_1", "type": "tool_call"}]),
        AIMessage(content="Taipei is the capital of Taiwan.", tool_calls=[]),
    ]
    result = run("Summarize Taipei", llm=llm)
    assert result["final"].startswith("Taipei")
    assert result["steps"] >= 4


if __name__ == "__main__":
    test_pinned_provider_and_shared_graph_behavior()
    print("all pass")

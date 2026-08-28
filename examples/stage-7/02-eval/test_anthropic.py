"""Stage 7 練習 2 — Path B Anthropic mock test。"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_anthropic import agent_answer_anthropic


def test_agent_answer_anthropic_mock():
    client = MagicMock()
    client.messages.create.return_value = SimpleNamespace(
        content=[SimpleNamespace(type="text", text="Tokyo")]
    )
    out = agent_answer_anthropic("Capital of Japan?", client=client)
    assert "Tokyo" in out
    print("✅ test_agent_answer_anthropic_mock")


def test_agent_answer_anthropic_rejects_empty_text():
    client = MagicMock()
    client.messages.create.return_value = SimpleNamespace(
        content=[SimpleNamespace(type="text", text="")]
    )
    try:
        agent_answer_anthropic("Capital of Japan?", client=client)
    except ValueError as error:
        assert "empty text" in str(error)
    else:
        raise AssertionError("empty model output must fail")
    print("✅ test_agent_answer_anthropic_rejects_empty_text")


if __name__ == "__main__":
    test_agent_answer_anthropic_mock()
    test_agent_answer_anthropic_rejects_empty_text()
    print("\n🎉 通過")

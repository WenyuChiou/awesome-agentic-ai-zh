"""Offline tests for the Anthropic adapter."""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_anthropic import agent_answer_anthropic, judge_answer_anthropic


def test_agent_answer_anthropic_mock() -> None:
    client = MagicMock()
    client.messages.create.return_value = SimpleNamespace(
        content=[SimpleNamespace(type="text", text="Tokyo")]
    )
    output = agent_answer_anthropic("Capital of Japan?", client=client)
    assert output == "Tokyo"


def test_agent_answer_anthropic_rejects_empty_text() -> None:
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


def test_judge_answer_anthropic_mock() -> None:
    client = MagicMock()
    client.messages.create.return_value = SimpleNamespace(
        content=[SimpleNamespace(type="text", text="PASS")]
    )
    case = {
        "input": "Is this correct?",
        "success_criteria": ["The answer is correct."],
        "grader": {"type": "llm_judge", "value": "Use the criterion."},
    }
    assert judge_answer_anthropic("yes", case, client=client) == "PASS"


if __name__ == "__main__":
    test_agent_answer_anthropic_mock()
    print("PASS test_agent_answer_anthropic_mock")
    test_agent_answer_anthropic_rejects_empty_text()
    print("PASS test_agent_answer_anthropic_rejects_empty_text")
    test_judge_answer_anthropic_mock()
    print("PASS test_judge_answer_anthropic_mock")
    print("\n🎉 3/3 passed — no network or API key used")

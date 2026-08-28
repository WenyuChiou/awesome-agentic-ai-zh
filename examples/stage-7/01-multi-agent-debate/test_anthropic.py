"""Stage 7 練習 1 — Anthropic mock test。"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_anthropic import debate_anthropic, llm_call_anthropic, parse_winner


def test_debate_anthropic_3_calls():
    client = MagicMock()
    responses = ["pro", "con", "WINNER=CON. Better reasoning."]
    client.messages.create.side_effect = [
        SimpleNamespace(content=[SimpleNamespace(type="text", text=r)]) for r in responses
    ]
    result = debate_anthropic("Q?", client=client)
    assert client.messages.create.call_count == 3
    assert "WINNER=CON" in result["judge"]
    assert result["winner"] == "CON"
    print("✅ test_debate_anthropic_3_calls")


def test_anthropic_rejects_empty_text_and_loose_judge_output():
    client = MagicMock()
    client.messages.create.return_value = SimpleNamespace(
        content=[SimpleNamespace(type="text", text="   ")]
    )
    try:
        llm_call_anthropic("system", "user", client=client)
    except ValueError as error:
        assert "empty text" in str(error)
    else:
        raise AssertionError("empty model output must fail")

    try:
        parse_winner("The WINNER=PRO is obvious")
    except ValueError:
        pass
    else:
        raise AssertionError("Judge parser accepted extra text")
    print("✅ test_anthropic_rejects_empty_text_and_loose_judge_output")


if __name__ == "__main__":
    test_debate_anthropic_3_calls()
    test_anthropic_rejects_empty_text_and_loose_judge_output()
    print("\n🎉 通過")

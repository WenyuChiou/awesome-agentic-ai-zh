"""Stage 3 練習 2 自我驗證 — Path B（Anthropic starter_anthropic.py）。

跑法：
    python test_anthropic.py

用 mock 取代 Anthropic client、不打真 API、$0/run。
Ollama 版本見 test.py（OpenAI-compat shape）。
"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_anthropic import TOOLS_SPEC, calculator, execute_tool, run_tool_selection


def block_text(text: str):
    return SimpleNamespace(type="text", text=text)


def block_tool_use(tool_id: str, name: str, inp: dict):
    return SimpleNamespace(type="tool_use", id=tool_id, name=name, input=inp)


def make_resp(stop_reason: str, *blocks):
    return SimpleNamespace(stop_reason=stop_reason, content=list(blocks))


def mock_client_for(name: str, inp: dict) -> MagicMock:
    client = MagicMock()
    client.messages.create.return_value = make_resp(
        "tool_use",
        block_text(f"I should use {name}."),
        block_tool_use("toolu_1", name, inp),
    )
    return client


def test_tool_spec_contains_three_tools():
    assert [tool["name"] for tool in TOOLS_SPEC] == ["web_search", "calculator", "calendar_lookup"]
    assert calculator("2 * (3 + 4)") == "14"


def test_calculator_rejects_unsafe_expressions():
    expressions = [
        "2 ** 3", "7 // 2", "10 ** 1000", "1000000000001",
        "-" * 20 + "1", "1+" * 100 + "1",
        "__import__('os').system('ls')", "1 / 0",
    ]
    for expression in expressions:
        assert calculator(expression).startswith("error:"), expression


def test_llm_selects_calculator():
    client = mock_client_for("calculator", {"expression": "20 / 5"})
    result = run_tool_selection("What is 20 divided by 5?", client=client)
    assert result["tool"] == "calculator"
    assert result["observation"] == "4.0"


def test_llm_selects_calendar():
    client = mock_client_for("calendar_lookup", {"date": "tomorrow"})
    result = run_tool_selection("Do I have anything tomorrow?", client=client)
    assert result["tool"] == "calendar_lookup"
    assert "Stage 3 review" in result["observation"]


def test_llm_uses_search_instead_of_calendar_for_news():
    client = mock_client_for("web_search", {"query": "latest Claude tool use examples"})
    result = run_tool_selection("Find recent examples of Claude tool use.", client=client)
    assert result["tool"] == "web_search"
    assert "latest Claude tool use examples" in result["observation"]


def test_untrusted_arguments_are_rejected():
    _, missing = execute_tool("calculator", {})
    _, wrong_shape = execute_tool("calculator", ["2 + 2"])
    _, unknown = execute_tool("delete_everything", {})
    _, extra = execute_tool("calculator", {"expression": "2 + 2", "unexpected": "x"})
    _, wrong_type = execute_tool("calculator", {"expression": 4})
    _, empty = execute_tool("calculator", {"expression": "  "})
    assert missing.startswith("error:")
    assert wrong_shape.startswith("error:")
    assert "not allowed" in unknown
    assert extra.startswith("error:")
    assert wrong_type.startswith("error:")
    assert empty.startswith("error:")


def test_multiple_calls_are_not_silently_partially_executed():
    client = MagicMock()
    client.messages.create.return_value = make_resp(
        "tool_use",
        block_tool_use("toolu_1", "calculator", {"expression": "2 + 2"}),
        block_tool_use("toolu_2", "calendar_lookup", {"date": "tomorrow"}),
    )
    result = run_tool_selection("Do both", client=client)
    assert result["tool"] is None
    assert "exactly one" in result["observation"]


if __name__ == "__main__":
    test_tool_spec_contains_three_tools()
    test_calculator_rejects_unsafe_expressions()
    test_llm_selects_calculator()
    test_llm_selects_calendar()
    test_llm_uses_search_instead_of_calendar_for_news()
    test_untrusted_arguments_are_rejected()
    test_multiple_calls_are_not_silently_partially_executed()
    print("all pass")

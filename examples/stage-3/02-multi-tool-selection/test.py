"""練習 2 自我驗證 — Path A（Ollama starter.py）。

跑法：
    python test.py

驗證內容：
    - tool 清單完整、calculator 邏輯正確
    - LLM 三種題目分別選到 calculator / calendar / web_search
    - mock 用 OpenAI-compat shape（不需要 Anthropic SDK）

Anthropic 版本 test 見 test_anthropic.py。
"""

from __future__ import annotations

import json
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import TOOLS_SPEC, calculator, execute_tool, run_tool_selection


# === Helpers for building mock OpenAI-compat responses ===

def make_tool_call(call_id: str, name: str, args: dict):
    return SimpleNamespace(
        id=call_id,
        type="function",
        function=SimpleNamespace(name=name, arguments=json.dumps(args)),
    )


def make_resp(content: str, tool_calls=None, finish_reason: str = "tool_calls"):
    msg = SimpleNamespace(content=content, tool_calls=tool_calls)
    return SimpleNamespace(choices=[SimpleNamespace(finish_reason=finish_reason, message=msg)])


def mock_client_for(name: str, args: dict) -> MagicMock:
    client = MagicMock()
    client.chat.completions.create.return_value = make_resp(
        f"I should use {name}.",
        [make_tool_call("call_1", name, args)],
    )
    return client


# === Tests ===

def test_tool_spec_contains_three_tools():
    names = [t["function"]["name"] for t in TOOLS_SPEC]
    assert names == ["web_search", "calculator", "calendar_lookup"]
    assert calculator("2 * (3 + 4)") == "14"
    print("✅ test_tool_spec_contains_three_tools")


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
    print("✅ test_llm_selects_calculator")


def test_llm_selects_calendar():
    client = mock_client_for("calendar_lookup", {"date": "tomorrow"})
    result = run_tool_selection("Do I have anything tomorrow?", client=client)
    assert result["tool"] == "calendar_lookup"
    assert "Stage 3 review" in result["observation"]
    print("✅ test_llm_selects_calendar")


def test_llm_uses_search_instead_of_calendar_for_news():
    client = mock_client_for("web_search", {"query": "latest Claude tool use examples"})
    result = run_tool_selection("Find recent examples of Claude tool use.", client=client)
    assert result["tool"] == "web_search"
    assert "latest Claude tool use examples" in result["observation"]
    print("✅ test_llm_uses_search_instead_of_calendar_for_news")


def test_no_tool_call_returns_none():
    client = MagicMock()
    client.chat.completions.create.return_value = make_resp(
        "I don't think any of these tools applies.", tool_calls=None, finish_reason="stop",
    )
    result = run_tool_selection("Tell me a joke.", client=client)
    assert result["tool"] is None
    assert result["observation"] is None
    print("✅ test_no_tool_call_returns_none")


def test_untrusted_arguments_are_rejected():
    _, malformed = execute_tool("calculator", "{not-json")
    _, missing = execute_tool("calculator", "{}")
    _, unknown = execute_tool("delete_everything", "{}")
    _, extra = execute_tool("calculator", json.dumps({"expression": "2 + 2", "unexpected": "x"}))
    _, wrong_type = execute_tool("calculator", json.dumps({"expression": 4}))
    _, empty = execute_tool("calculator", json.dumps({"expression": "  "}))
    assert malformed.startswith("error:")
    assert missing.startswith("error:")
    assert "not allowed" in unknown
    assert extra.startswith("error:")
    assert wrong_type.startswith("error:")
    assert empty.startswith("error:")


def test_multiple_calls_are_not_silently_partially_executed():
    client = MagicMock()
    client.chat.completions.create.return_value = make_resp(
        "two calls",
        [
            make_tool_call("call_1", "calculator", {"expression": "2 + 2"}),
            make_tool_call("call_2", "calendar_lookup", {"date": "tomorrow"}),
        ],
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
    test_no_tool_call_returns_none()
    test_untrusted_arguments_are_rejected()
    test_multiple_calls_are_not_silently_partially_executed()
    print("\n🎉 全部通過 — Ollama path tool selection 邏輯正確")

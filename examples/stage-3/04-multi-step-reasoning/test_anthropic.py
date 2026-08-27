"""Stage 3 練習 4 自我驗證 — Path B（Anthropic starter_anthropic.py）。

跑法：
    python test_anthropic.py

用 mock 取代 Anthropic client、不打真 API、$0/run。
Ollama 版本見 test.py（OpenAI-compat shape）。
"""

from __future__ import annotations

import json
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_anthropic import divide, execute_tool, react_loop, to_percentage


def block_text(text: str):
    return SimpleNamespace(type="text", text=text)


def block_tool_use(tool_id: str, name: str, inp: dict):
    return SimpleNamespace(type="tool_use", id=tool_id, name=name, input=inp)


def make_resp(stop_reason: str, *blocks):
    return SimpleNamespace(stop_reason=stop_reason, content=list(blocks))


def test_tools_handle_math_edges():
    assert divide(10, 2) == "5.0"
    assert to_percentage(0.3122) == "31.22"
    _, zero_error, is_error = execute_tool("divide", {"a": 10, "b": 0})
    assert is_error is True
    assert json.loads(zero_error)["error"]["code"] == "division_by_zero"


def test_population_ratio_uses_four_tool_steps():
    client = MagicMock()
    client.messages.create.side_effect = [
        make_resp("tool_use", block_text("Need Taipei population."), block_tool_use("t1", "lookup_population", {"city": "Taipei"})),
        make_resp("tool_use", block_text("Need New York population."), block_tool_use("t2", "lookup_population", {"city": "New York"})),
        make_resp("tool_use", block_text("Divide the two populations."), block_tool_use("t3", "divide", {"a": 2602000, "b": 8336000})),
        make_resp("tool_use", block_text("Convert ratio to percent."), block_tool_use("t4", "to_percentage", {"ratio": 0.3122})),
        make_resp("end_turn", block_text("Taipei is about 31% of New York by population.")),
    ]
    result = react_loop("Compare Taipei and New York population.", client=client)
    tools = [entry["tool"] for entry in result["trace"] if entry["tool"]]
    assert tools == ["lookup_population", "lookup_population", "divide", "to_percentage"]
    assert "31%" in result["final"]
    assert result["steps"] == 5


def test_zero_population_path_returns_an_error():
    client = MagicMock()
    client.messages.create.side_effect = [
        make_resp("tool_use", block_text("Need numerator."), block_tool_use("t1", "lookup_population", {"city": "Taipei"})),
        make_resp("tool_use", block_text("Need denominator."), block_tool_use("t2", "lookup_population", {"city": "Empty City"})),
        make_resp("tool_use", block_text("Try divide."), block_tool_use("t3", "divide", {"a": 2602000, "b": 0})),
        make_resp("end_turn", block_text("The ratio is undefined because the denominator is zero.")),
    ]
    result = react_loop("Compare Taipei with an empty city.", client=client)
    sent = client.messages.create.call_args_list[3].kwargs["messages"][-2]["content"][0]
    assert sent["is_error"] is True
    assert json.loads(sent["content"])["error"]["code"] == "division_by_zero"
    assert "undefined" in result["final"]


def test_non_finite_and_oversized_numbers_are_rejected():
    for value, expected_code in (
        (float("inf"), "non_finite_number"),
        (float("nan"), "non_finite_number"),
        (10_000_000_000_000, "number_too_large"),
        (10 ** 399, "number_too_large"),
    ):
        _, obs, is_error = execute_tool("round_int", {"x": value})
        assert is_error is True
        assert json.loads(obs)["error"]["code"] == expected_code


def test_invalid_call_is_marked_as_error():
    client = MagicMock()
    client.messages.create.side_effect = [
        make_resp("tool_use", block_tool_use("bad", "divide", {"a": 1})),
        make_resp("end_turn", block_text("The tool failed.")),
    ]
    result = react_loop("divide", client=client)
    sent = client.messages.create.call_args_list[1].kwargs["messages"][-2]["content"][0]
    assert sent["is_error"] is True
    assert result["trace"][0]["obs"].startswith("error:")
    _, unknown, unknown_error = execute_tool("delete_everything", {})
    assert unknown_error is True and "not allowed" in unknown
    _, extra, extra_error = execute_tool("divide", {"a": 1, "b": 2, "unexpected": 3})
    _, wrong_type, wrong_type_error = execute_tool("divide", {"a": True, "b": 2})
    _, empty_city, empty_city_error = execute_tool("lookup_population", {"city": "  "})
    assert extra_error is True and extra.startswith("error:")
    assert wrong_type_error is True and wrong_type.startswith("error:")
    assert empty_city_error is True and empty_city.startswith("error:")


def test_max_tokens_is_not_a_final_answer():
    client = MagicMock()
    client.messages.create.return_value = make_resp("max_tokens", block_text("unfinished"))
    result = react_loop("too long", client=client)
    assert result["final"] is None
    assert result["terminal_reason"] == "max_tokens"


if __name__ == "__main__":
    test_tools_handle_math_edges()
    test_population_ratio_uses_four_tool_steps()
    test_zero_population_path_returns_an_error()
    test_non_finite_and_oversized_numbers_are_rejected()
    test_invalid_call_is_marked_as_error()
    test_max_tokens_is_not_a_final_answer()
    print("all pass")

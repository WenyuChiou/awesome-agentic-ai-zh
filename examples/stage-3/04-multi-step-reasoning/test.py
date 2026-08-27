"""練習 4 自我驗證 — Path A（Ollama starter.py）。

跑法：
    python test.py

驗證內容：
    - divide / to_percentage 邊界正確（除 0、四捨五入）
    - react_loop 跑完 4 步工具 + end_turn 給最終答案
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

from starter import divide, execute_tool, react_loop, to_percentage


def make_tool_call(call_id: str, name: str, args: dict):
    return SimpleNamespace(
        id=call_id,
        type="function",
        function=SimpleNamespace(name=name, arguments=json.dumps(args)),
    )


def make_resp(finish_reason: str, content: str = "", tool_calls=None):
    msg = SimpleNamespace(content=content, tool_calls=tool_calls)
    return SimpleNamespace(choices=[SimpleNamespace(finish_reason=finish_reason, message=msg)])


def test_tools_handle_math_edges():
    assert divide(10, 2) == "5.0"
    assert to_percentage(0.3122) == "31.22"
    _, zero_error, is_error = execute_tool("divide", json.dumps({"a": 10, "b": 0}))
    assert is_error is True
    assert json.loads(zero_error)["error"]["code"] == "division_by_zero"
    print("✅ test_tools_handle_math_edges")


def test_population_ratio_uses_four_tool_steps():
    client = MagicMock()
    client.chat.completions.create.side_effect = [
        make_resp("tool_calls", "Need Taipei.", [make_tool_call("t1", "lookup_population", {"city": "Taipei"})]),
        make_resp("tool_calls", "Need NY.", [make_tool_call("t2", "lookup_population", {"city": "New York"})]),
        make_resp("tool_calls", "Divide.", [make_tool_call("t3", "divide", {"a": 2602000, "b": 8336000})]),
        make_resp("tool_calls", "Percentage.", [make_tool_call("t4", "to_percentage", {"ratio": 0.3122})]),
        make_resp("stop", "Taipei is about 31% of New York by population."),
    ]
    result = react_loop("Compare Taipei and New York population.", client=client)
    tools = [entry["tool"] for entry in result["trace"] if entry["tool"]]
    assert tools == ["lookup_population", "lookup_population", "divide", "to_percentage"]
    assert "31%" in result["final"]
    assert result["steps"] == 5
    print("✅ test_population_ratio_uses_four_tool_steps")


def test_zero_population_path_returns_an_error():
    client = MagicMock()
    client.chat.completions.create.side_effect = [
        make_resp("tool_calls", "Numerator.", [make_tool_call("t1", "lookup_population", {"city": "Taipei"})]),
        make_resp("tool_calls", "Denominator.", [make_tool_call("t2", "lookup_population", {"city": "Empty City"})]),
        make_resp("tool_calls", "Try divide.", [make_tool_call("t3", "divide", {"a": 2602000, "b": 0})]),
        make_resp("stop", "The ratio is undefined because the denominator is zero."),
    ]
    result = react_loop("Compare Taipei with an empty city.", client=client)
    error = json.loads(result["trace"][2]["obs"])["error"]
    assert error["code"] == "division_by_zero"
    assert "undefined" in result["final"]
    assert result["steps"] == 4
    print("✅ test_zero_population_path_returns_an_error")


def test_non_finite_and_oversized_numbers_are_rejected():
    for raw, expected_code in (
        ('{"x": 1e309}', "non_finite_number"),
        ('{"x": NaN}', "non_finite_number"),
        ('{"x": 10000000000000}', "number_too_large"),
        (json.dumps({"x": 10 ** 399}), "number_too_large"),
        ('{"x": ' + "9" * 5000 + "}", "number_too_large"),
    ):
        _, obs, is_error = execute_tool("round_int", raw)
        assert is_error is True
        assert json.loads(obs)["error"]["code"] == expected_code


def test_react_loop_respects_max_iter():
    """LLM 一直 tool_calls、永不收尾、應該在 max_iter 停。"""
    client = MagicMock()
    def never_ending(**kwargs):
        return make_resp("tool_calls", "again", [make_tool_call("c", "lookup_population", {"city": "Taipei"})])
    client.chat.completions.create.side_effect = never_ending

    result = react_loop("never stop", max_iter=3, client=client)
    assert result.get("truncated") is True
    assert result["steps"] == 3
    assert result["final"] is None
    print("✅ test_react_loop_respects_max_iter")


def test_invalid_tool_calls_are_returned_as_data():
    _, malformed, malformed_error = execute_tool("divide", "{not-json")
    _, missing, missing_error = execute_tool("divide", "{}")
    _, unknown, unknown_error = execute_tool("delete_everything", "{}")
    _, extra, extra_error = execute_tool("divide", json.dumps({"a": 1, "b": 2, "unexpected": 3}))
    _, wrong_type, wrong_type_error = execute_tool("divide", json.dumps({"a": True, "b": 2}))
    _, empty_city, empty_city_error = execute_tool("lookup_population", json.dumps({"city": "  "}))
    assert malformed_error is True and malformed.startswith("error:")
    assert missing_error is True and missing.startswith("error:")
    assert unknown_error is True and "not allowed" in unknown
    assert extra_error is True and extra.startswith("error:")
    assert wrong_type_error is True and wrong_type.startswith("error:")
    assert empty_city_error is True and empty_city.startswith("error:")


def test_length_is_not_a_final_answer():
    client = MagicMock()
    client.chat.completions.create.return_value = make_resp("length", "unfinished")
    result = react_loop("too long", client=client)
    assert result["final"] is None
    assert result["terminal_reason"] == "length"


if __name__ == "__main__":
    test_tools_handle_math_edges()
    test_population_ratio_uses_four_tool_steps()
    test_zero_population_path_returns_an_error()
    test_non_finite_and_oversized_numbers_are_rejected()
    test_react_loop_respects_max_iter()
    test_invalid_tool_calls_are_returned_as_data()
    test_length_is_not_a_final_answer()
    print("\n🎉 全部通過 — Ollama path 多步 ReAct loop 邏輯正確")

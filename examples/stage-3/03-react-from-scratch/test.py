"""
練習 3 自我驗證 — Path A（Ollama starter.py）。

跑法：
    python test.py

驗證內容：
    - react_loop 收到 tool_calls → 執行 tool → observation 接回 → 拿到 finish_reason='stop'
    - react_loop 在 max_iter 內停（避免無限迴圈）
    - tool_calculator / tool_lookup_fact 邏輯正確
    - 跨 backend：mock 用 OpenAI-compat shape（不需要 Anthropic SDK）

Anthropic 版本 test 見 test_anthropic.py。
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import json
from types import SimpleNamespace
from unittest.mock import MagicMock

from starter import execute_tool, react_loop, tool_calculator, tool_lookup_fact


# === Helpers for building mock OpenAI-compat responses ===

def make_tool_call(call_id: str, name: str, args: dict):
    return SimpleNamespace(
        id=call_id,
        type="function",
        function=SimpleNamespace(name=name, arguments=json.dumps(args)),
    )


def make_resp(finish_reason: str, content: str = "", tool_calls=None):
    """Build a fake OpenAI chat.completions response."""
    msg = SimpleNamespace(content=content, tool_calls=tool_calls)
    return SimpleNamespace(choices=[SimpleNamespace(finish_reason=finish_reason, message=msg)])


# === Tests ===

def test_calculator_basic():
    assert tool_calculator("2 + 3") == "5"
    assert tool_calculator("(10 + 2) / 4") == "3.0"
    print("✅ test_calculator_basic")


def test_calculator_rejects_unsafe_expressions():
    expressions = [
        "2 ** 3", "7 // 2", "10 ** 1000", "1000000000001",
        "-" * 20 + "1", "1+" * 100 + "1",
        "__import__('os').system('ls')", "1 / 0",
    ]
    for expression in expressions:
        assert tool_calculator(expression).startswith("error:"), expression
    print("✅ test_calculator_rejects_unsafe_expressions")


def test_lookup_fact():
    assert tool_lookup_fact("台北人口") == "2602000"
    assert tool_lookup_fact("不存在的東西").startswith("unknown:")
    print("✅ test_lookup_fact")


def test_react_loop_single_tool_call():
    """模擬：LLM 第 1 輪 tool_calls lookup_fact、第 2 輪 stop 給答案。"""
    client = MagicMock()
    client.chat.completions.create.side_effect = [
        make_resp("tool_calls", "我先查台北人口。",
                  [make_tool_call("call_1", "lookup_fact", {"query": "台北人口"})]),
        make_resp("stop", "台北人口是 2602000 人。"),
    ]

    result = react_loop("台北人口是多少？", max_iter=4, client=client)

    assert result["final"] == "台北人口是 2602000 人。"
    assert result["steps"] == 2
    assert result["trace"][0]["tool"] == "lookup_fact"
    assert result["trace"][0]["obs"] == "2602000"
    print("✅ test_react_loop_single_tool_call")


def test_react_loop_multi_step():
    """模擬：lookup_fact x2 + calculator x1 + stop = 4 輪。"""
    client = MagicMock()
    client.chat.completions.create.side_effect = [
        make_resp("tool_calls", "查台北。",
                  [make_tool_call("c1", "lookup_fact", {"query": "台北人口"})]),
        make_resp("tool_calls", "查紐約。",
                  [make_tool_call("c2", "lookup_fact", {"query": "紐約人口"})]),
        make_resp("tool_calls", "算比例。",
                  [make_tool_call("c3", "calculator", {"expression": "2602000 / 8336000"})]),
        make_resp("stop", "台北 / 紐約 約 0.3122。"),
    ]

    result = react_loop("台北 / 紐約 人口比？", max_iter=6, client=client)

    assert result["final"] is not None
    assert "0.3122" in result["final"]
    assert result["steps"] == 4
    tool_seq = [t["tool"] for t in result["trace"] if t["tool"]]
    assert tool_seq == ["lookup_fact", "lookup_fact", "calculator"]
    print("✅ test_react_loop_multi_step")


def test_react_loop_respects_max_iter():
    """模擬：LLM 一直 tool_calls、永不收尾、應該在 max_iter 停。"""
    client = MagicMock()

    def never_ending(**kwargs):
        return make_resp("tool_calls", "再查一次。",
                         [make_tool_call("c", "lookup_fact", {"query": "光速"})])

    client.chat.completions.create.side_effect = never_ending

    result = react_loop("永遠跑下去", max_iter=3, client=client)

    assert result.get("truncated") is True
    assert result["steps"] == 3
    assert result["final"] is None
    print("✅ test_react_loop_respects_max_iter")


def test_invalid_tool_call_is_returned_as_data():
    _, malformed, malformed_error = execute_tool("calculator", "{not-json")
    _, unknown, unknown_error = execute_tool("delete_everything", "{}")
    _, extra, extra_error = execute_tool("calculator", json.dumps({"expression": "2 + 2", "unexpected": "x"}))
    _, wrong_type, wrong_type_error = execute_tool("calculator", json.dumps({"expression": 4}))
    _, empty, empty_error = execute_tool("lookup_fact", json.dumps({"query": "  "}))
    assert malformed_error is True and malformed.startswith("error:")
    assert unknown_error is True and "not allowed" in unknown
    assert extra_error is True and extra.startswith("error:")
    assert wrong_type_error is True and wrong_type.startswith("error:")
    assert empty_error is True and empty.startswith("error:")


def test_non_stop_terminal_reason_is_not_a_final_answer():
    client = MagicMock()
    client.chat.completions.create.return_value = make_resp("length", "unfinished", None)
    result = react_loop("too long", client=client)
    assert result["final"] is None
    assert result["terminal_reason"] == "length"
    assert result["truncated"] is True


if __name__ == "__main__":
    test_calculator_basic()
    test_calculator_rejects_unsafe_expressions()
    test_lookup_fact()
    test_react_loop_single_tool_call()
    test_react_loop_multi_step()
    test_react_loop_respects_max_iter()
    test_invalid_tool_call_is_returned_as_data()
    test_non_stop_terminal_reason_is_not_a_final_answer()
    print("\n🎉 全部通過 — Ollama path ReAct loop 邏輯正確")

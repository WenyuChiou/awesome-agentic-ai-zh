"""
練習 3 自我驗證：用 mock 取代 anthropic client、不花 API 錢。

跑法：
    python test.py

驗證內容：
    1. react_loop 收到 tool_use → 執行 tool → 把 observation 接回去 → 拿到 end_turn
    2. react_loop 在 max_iter 內停（避免無限迴圈）
    3. tool_calculator / tool_lookup_fact 邏輯正確
"""

from __future__ import annotations

import sys

# Windows cp950 console 無法印 emoji / 中文、強制 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from unittest.mock import MagicMock
from types import SimpleNamespace

from starter_anthropic import execute_tool, react_loop, tool_calculator, tool_lookup_fact


# === Helpers for building mock Anthropic responses ===

def block_text(s: str):
    return SimpleNamespace(type="text", text=s)


def block_tool_use(tool_id: str, name: str, inp: dict):
    return SimpleNamespace(type="tool_use", id=tool_id, name=name, input=inp)


def make_resp(stop_reason: str, *blocks):
    return SimpleNamespace(stop_reason=stop_reason, content=list(blocks))


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
    assert tool_lookup_fact("不存在的東西") .startswith("unknown:")
    print("✅ test_lookup_fact")


def test_react_loop_single_tool_call():
    """模擬：LLM 第 1 輪 tool_use lookup_fact、第 2 輪直接 end_turn 給答案。"""
    client = MagicMock()
    client.messages.create.side_effect = [
        make_resp(
            "tool_use",
            block_text("我先查台北人口。"),
            block_tool_use("toolu_1", "lookup_fact", {"query": "台北人口"}),
        ),
        make_resp(
            "end_turn",
            block_text("台北人口是 2602000 人。"),
        ),
    ]

    result = react_loop("台北人口是多少？", max_iter=4, client=client)

    assert result["final"] == "台北人口是 2602000 人。"
    assert result["steps"] == 2
    assert result["trace"][0]["tool"] == "lookup_fact"
    assert result["trace"][0]["obs"] == "2602000"
    print("✅ test_react_loop_single_tool_call")


def test_react_loop_multi_step():
    """模擬：lookup_fact x2 + calculator x1 + end_turn = 4 輪。"""
    client = MagicMock()
    client.messages.create.side_effect = [
        make_resp("tool_use", block_text("查台北。"),
                  block_tool_use("t1", "lookup_fact", {"query": "台北人口"})),
        make_resp("tool_use", block_text("查紐約。"),
                  block_tool_use("t2", "lookup_fact", {"query": "紐約人口"})),
        make_resp("tool_use", block_text("算比例。"),
                  block_tool_use("t3", "calculator", {"expression": "2602000 / 8336000"})),
        make_resp("end_turn", block_text("台北 / 紐約 約 0.3122。")),
    ]

    result = react_loop("台北 / 紐約 人口比？", max_iter=6, client=client)

    assert result["final"] is not None
    assert "0.3122" in result["final"]
    assert result["steps"] == 4
    tool_seq = [t["tool"] for t in result["trace"] if t["tool"]]
    assert tool_seq == ["lookup_fact", "lookup_fact", "calculator"]
    print("✅ test_react_loop_multi_step")


def test_react_loop_respects_max_iter():
    """模擬：LLM 一直 tool_use、永不收尾、應該在 max_iter 停。"""
    client = MagicMock()
    def never_ending(**kwargs):
        return make_resp(
            "tool_use",
            block_text("再查一次。"),
            block_tool_use("t", "lookup_fact", {"query": "光速"}),
        )
    client.messages.create.side_effect = never_ending

    result = react_loop("永遠跑下去", max_iter=3, client=client)

    assert result.get("truncated") is True
    assert result["steps"] == 3
    assert result["final"] is None
    print("✅ test_react_loop_respects_max_iter")


def test_invalid_tool_call_is_marked_as_error():
    client = MagicMock()
    client.messages.create.side_effect = [
        make_resp("tool_use", block_tool_use("bad", "calculator", {})),
        make_resp("end_turn", block_text("The tool failed.")),
    ]
    result = react_loop("calculate", client=client)
    sent_block = client.messages.create.call_args_list[1].kwargs["messages"][-2]["content"][0]
    assert sent_block["is_error"] is True
    assert result["trace"][0]["obs"].startswith("error:")
    _, unknown, unknown_error = execute_tool("delete_everything", {})
    _, extra, extra_error = execute_tool("calculator", {"expression": "2 + 2", "unexpected": "x"})
    _, wrong_type, wrong_type_error = execute_tool("calculator", {"expression": 4})
    _, empty, empty_error = execute_tool("lookup_fact", {"query": "  "})
    assert unknown_error is True and "not allowed" in unknown
    assert extra_error is True and extra.startswith("error:")
    assert wrong_type_error is True and wrong_type.startswith("error:")
    assert empty_error is True and empty.startswith("error:")


def test_non_end_turn_is_not_a_final_answer():
    client = MagicMock()
    client.messages.create.return_value = make_resp("max_tokens", block_text("unfinished"))
    result = react_loop("too long", client=client)
    assert result["final"] is None
    assert result["terminal_reason"] == "max_tokens"
    assert result["truncated"] is True


if __name__ == "__main__":
    test_calculator_basic()
    test_calculator_rejects_unsafe_expressions()
    test_lookup_fact()
    test_react_loop_single_tool_call()
    test_react_loop_multi_step()
    test_react_loop_respects_max_iter()
    test_invalid_tool_call_is_marked_as_error()
    test_non_end_turn_is_not_a_final_answer()
    print("\n🎉 全部通過 — 你的 ReAct loop 邏輯正確")

"""練習 5 自我驗證 — Path A（Ollama starter.py）。

跑法：
    python test.py

驗證內容：
    - fetch_weather failure plan 邏輯正確
    - react_loop 第一輪錯誤 + 第二輪 retry + 第三輪 end_turn
    - 連續失敗也能 graceful end（不 crash）
    - mock 用 OpenAI-compat shape

Anthropic 版本 test 見 test_anthropic.py。
"""

from __future__ import annotations

import json
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import execute_tool, fetch_weather, react_loop, set_weather_failures


def make_tool_call(call_id: str, name: str, args: dict):
    return SimpleNamespace(
        id=call_id,
        type="function",
        function=SimpleNamespace(name=name, arguments=json.dumps(args)),
    )


def make_resp(finish_reason: str, content: str = "", tool_calls=None):
    msg = SimpleNamespace(content=content, tool_calls=tool_calls)
    return SimpleNamespace(choices=[SimpleNamespace(finish_reason=finish_reason, message=msg)])


def test_fetch_weather_failure_plan():
    set_weather_failures([True, False])
    first = fetch_weather("Taipei")
    second = fetch_weather("Taipei")
    assert first["error"] == "network timeout"
    assert second["forecast"] == "rain"
    print("✅ test_fetch_weather_failure_plan")


def test_retry_then_success():
    set_weather_failures([True, False])
    client = MagicMock()
    client.chat.completions.create.side_effect = [
        make_resp("tool_calls", "Check weather.", [make_tool_call("t1", "fetch_weather", {"city": "Taipei"})]),
        make_resp("tool_calls", "Got retry_hint, retry once.", [make_tool_call("t2", "fetch_weather", {"city": "Taipei"})]),
        make_resp("stop", "Taipei is rainy now."),
    ]
    result = react_loop("Will it rain in Taipei?", client=client)
    tools = [entry["tool"] for entry in result["trace"] if entry["tool"]]
    assert tools == ["fetch_weather", "fetch_weather"]
    assert result["trace"][0]["obs"]["retry_hint"] == "try again in 1s"
    assert result["trace"][1]["obs"]["forecast"] == "rain"
    assert result["final"] == "Taipei is rainy now."
    print("✅ test_retry_then_success")


def test_repeated_errors_can_end_gracefully():
    set_weather_failures([True, True])
    client = MagicMock()
    client.chat.completions.create.side_effect = [
        make_resp("tool_calls", "Try weather API.", [make_tool_call("t1", "fetch_weather", {"city": "Taipei"})]),
        make_resp("tool_calls", "Retry once.", [make_tool_call("t2", "fetch_weather", {"city": "Taipei"})]),
        make_resp("stop", "Weather is unavailable after retry; please try again later."),
    ]
    result = react_loop("Will it rain in Taipei?", client=client)
    assert result["trace"][0]["obs"]["error"] == "network timeout"
    assert result["trace"][1]["obs"]["error"] == "network timeout"
    assert "unavailable" in result["final"]
    print("✅ test_repeated_errors_can_end_gracefully")


def test_unknown_tool_returns_structured_error():
    """模擬 LLM 呼叫不存在的 tool、確認 loop 不 crash、而是把 error 給 LLM 看。"""
    set_weather_failures([])
    client = MagicMock()
    client.chat.completions.create.side_effect = [
        make_resp("tool_calls", "I'll try a weird tool.", [make_tool_call("t1", "magic_tool", {"city": "Taipei"})]),
        make_resp("stop", "OK, no magic tool here."),
    ]
    result = react_loop("Try magic.", client=client)
    assert result["trace"][0]["obs"]["error"] == "tool not allowed"
    print("✅ test_unknown_tool_returns_structured_error")


def test_malformed_arguments_return_structured_error():
    _, malformed, malformed_error = execute_tool("fetch_weather", "{not-json")
    _, empty, empty_error = execute_tool("fetch_weather", json.dumps({"city": ""}))
    assert malformed_error is True and malformed["error"] == "invalid arguments"
    assert empty_error is True and empty["error"] == "invalid arguments"


def test_length_is_not_a_final_answer():
    client = MagicMock()
    client.chat.completions.create.return_value = make_resp("length", "unfinished")
    result = react_loop("too long", client=client)
    assert result["final"] is None
    assert result["terminal_reason"] == "length"


if __name__ == "__main__":
    test_fetch_weather_failure_plan()
    test_retry_then_success()
    test_repeated_errors_can_end_gracefully()
    test_unknown_tool_returns_structured_error()
    test_malformed_arguments_return_structured_error()
    test_length_is_not_a_final_answer()
    print("\n🎉 全部通過 — Ollama path tool error handling 邏輯正確")

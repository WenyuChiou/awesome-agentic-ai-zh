"""Stage 3 練習 5 自我驗證 — Path B（Anthropic starter_anthropic.py）。

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

from starter_anthropic import execute_tool, fetch_weather, react_loop, set_weather_failures


def block_text(text: str):
    return SimpleNamespace(type="text", text=text)


def block_tool_use(tool_id: str, name: str, inp: dict):
    return SimpleNamespace(type="tool_use", id=tool_id, name=name, input=inp)


def make_resp(stop_reason: str, *blocks):
    return SimpleNamespace(stop_reason=stop_reason, content=list(blocks))


def test_fetch_weather_failure_plan():
    set_weather_failures([True, False])
    first = fetch_weather("Taipei")
    second = fetch_weather("Taipei")
    assert first["error"] == "network timeout"
    assert second["forecast"] == "rain"


def test_retry_then_success():
    set_weather_failures([True, False])
    client = MagicMock()
    client.messages.create.side_effect = [
        make_resp("tool_use", block_text("Check weather."), block_tool_use("t1", "fetch_weather", {"city": "Taipei"})),
        make_resp("tool_use", block_text("Tool returned retry_hint, retry once."), block_tool_use("t2", "fetch_weather", {"city": "Taipei"})),
        make_resp("end_turn", block_text("Taipei is rainy now.")),
    ]
    result = react_loop("Will it rain in Taipei?", client=client)
    tools = [entry["tool"] for entry in result["trace"] if entry["tool"]]
    assert tools == ["fetch_weather", "fetch_weather"]
    assert result["trace"][0]["obs"]["retry_hint"] == "try again in 1s"
    assert result["trace"][1]["obs"]["forecast"] == "rain"
    assert result["final"] == "Taipei is rainy now."


def test_repeated_errors_can_end_gracefully():
    set_weather_failures([True, True])
    client = MagicMock()
    client.messages.create.side_effect = [
        make_resp("tool_use", block_text("Try weather API."), block_tool_use("t1", "fetch_weather", {"city": "Taipei"})),
        make_resp("tool_use", block_text("Retry once."), block_tool_use("t2", "fetch_weather", {"city": "Taipei"})),
        make_resp("end_turn", block_text("Weather is unavailable after retry; please try again later.")),
    ]
    result = react_loop("Will it rain in Taipei?", client=client)
    assert result["trace"][0]["obs"]["error"] == "network timeout"
    assert result["trace"][1]["obs"]["error"] == "network timeout"
    assert "unavailable" in result["final"]


def test_failed_result_is_marked_and_correlated():
    set_weather_failures([True])
    client = MagicMock()
    client.messages.create.side_effect = [
        make_resp("tool_use", block_tool_use("weather_1", "fetch_weather", {"city": "Taipei"})),
        make_resp("end_turn", block_text("Weather is unavailable.")),
    ]
    react_loop("Weather?", client=client)
    sent = client.messages.create.call_args_list[1].kwargs["messages"][-2]["content"][0]
    assert sent["tool_use_id"] == "weather_1"
    assert sent["is_error"] is True


def test_invalid_input_and_terminal_reason_are_safe():
    _, invalid, invalid_error = execute_tool("fetch_weather", {"city": "", "extra": True})
    _, unknown, unknown_error = execute_tool("delete_everything", {})
    assert invalid_error is True and invalid["error"] == "invalid arguments"
    assert unknown_error is True and unknown["error"] == "tool not allowed"

    client = MagicMock()
    client.messages.create.return_value = make_resp("max_tokens", block_text("unfinished"))
    result = react_loop("too long", client=client)
    assert result["final"] is None
    assert result["terminal_reason"] == "max_tokens"


if __name__ == "__main__":
    test_fetch_weather_failure_plan()
    test_retry_then_success()
    test_repeated_errors_can_end_gracefully()
    test_failed_result_is_marked_and_correlated()
    test_invalid_input_and_terminal_reason_are_safe()
    print("all pass")

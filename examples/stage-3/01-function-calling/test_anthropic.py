"""Offline checks for the Anthropic Exercise 1 starter."""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_anthropic import execute_tool, run_once


def text_block(text: str):
    return SimpleNamespace(type="text", text=text)


def tool_block(name: str, arguments: dict):
    return SimpleNamespace(type="tool_use", id="toolu_1", name=name, input=arguments)


def response(stop_reason: str, *content):
    return SimpleNamespace(stop_reason=stop_reason, content=list(content))


def test_valid_call_completes_round_trip():
    client = MagicMock()
    client.messages.create.side_effect = [
        response("tool_use", tool_block("get_weather", {"city": "Taipei"})),
        response("end_turn", text_block("26 C")),
    ]
    result = run_once("Weather?", client=client)
    assert result["tool_result"]["data"]["temperature"] == 26
    assert result["result_block"]["tool_use_id"] == "toolu_1"
    assert "is_error" not in result["result_block"]


def test_invalid_input_becomes_an_error_result():
    client = MagicMock()
    client.messages.create.side_effect = [
        response("tool_use", tool_block("get_weather", {"city": "", "extra": True})),
        response("end_turn", text_block("I could not run the tool.")),
    ]
    result = run_once("Weather?", client=client)
    assert result["tool_result"]["error"] == "invalid_arguments"
    assert result["result_block"]["is_error"] is True


def test_unknown_tool_is_rejected():
    result = execute_tool("delete_everything", {})
    assert result["error"] == "tool_not_allowed"


if __name__ == "__main__":
    test_valid_call_completes_round_trip()
    test_invalid_input_becomes_an_error_result()
    test_unknown_tool_is_rejected()
    print("all pass")

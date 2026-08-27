"""Offline checks for the Ollama-compatible Exercise 1 starter."""

from __future__ import annotations

import json
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import execute_tool, run_once


def message(content: str = "", tool_calls=None):
    data = {"role": "assistant", "content": content}
    obj = SimpleNamespace(content=content, tool_calls=tool_calls)
    obj.model_dump = lambda exclude_none=True: data | ({"tool_calls": tool_calls} if tool_calls else {})
    return obj


def tool_call(name: str, arguments: str):
    return SimpleNamespace(
        id="call_1", function=SimpleNamespace(name=name, arguments=arguments),
    )


def response(msg):
    return SimpleNamespace(choices=[SimpleNamespace(message=msg)])


def test_valid_call_completes_round_trip():
    client = MagicMock()
    call = tool_call("get_weather", json.dumps({"city": "Taipei", "unit": "celsius"}))
    client.chat.completions.create.side_effect = [response(message(tool_calls=[call])), response(message("26 C"))]
    result = run_once("Weather?", client=client)
    assert result["tool_result"]["data"]["temperature"] == 26
    assert result["final"] == "26 C"
    assert result["messages"][-1]["tool_call_id"] == "call_1"


def test_invalid_json_never_runs_tool():
    result = execute_tool("get_weather", "{not-json")
    assert result == {"ok": False, "error": "invalid_arguments", "message": "Arguments must be JSON."}


def test_extra_or_wrong_fields_are_rejected():
    extra = execute_tool("get_weather", json.dumps({"city": "Taipei", "unit": "celsius", "admin": True}))
    wrong = execute_tool("get_weather", json.dumps({"city": "Taipei", "unit": "fahrenheit"}))
    assert extra["ok"] is False
    assert wrong["ok"] is False


def test_unknown_tool_is_rejected():
    result = execute_tool("delete_everything", "{}")
    assert result["error"] == "tool_not_allowed"


if __name__ == "__main__":
    test_valid_call_completes_round_trip()
    test_invalid_json_never_runs_tool()
    test_extra_or_wrong_fields_are_rejected()
    test_unknown_tool_is_rejected()
    print("all pass")

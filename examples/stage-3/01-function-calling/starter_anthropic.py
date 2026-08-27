"""Stage 3 Exercise 1: one Anthropic tool call and one tool result.

PowerShell:
    python -m pip install -r requirements.txt
    $env:ANTHROPIC_API_KEY = "your-key"
    python starter_anthropic.py

Reserve $0.05 before a live run; tests use mocks and cost $0.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")
TOOLS = [{
    "name": "get_weather",
    "description": "Return demonstration weather data for one city.",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string", "description": "A non-empty city name"}},
        "required": ["city"],
        "additionalProperties": False,
    },
}]


def get_weather(city: str) -> dict:
    """Return fixed data so the lesson does not depend on a weather service."""
    return {"city": city, "temperature": 26, "unit": "celsius"}


def execute_tool(name: str, arguments: Any) -> dict:
    """Treat a model-produced tool call as untrusted input."""
    if name != "get_weather":
        return {"ok": False, "error": "tool_not_allowed", "message": f"Tool not allowed: {name}"}
    if (
        not isinstance(arguments, dict)
        or set(arguments) != {"city"}
        or not isinstance(arguments.get("city"), str)
        or not arguments["city"].strip()
    ):
        return {
            "ok": False,
            "error": "invalid_arguments",
            "message": "city must be a non-empty string.",
        }
    return {"ok": True, "data": get_weather(arguments["city"].strip())}


def run_once(question: str, client: Any = None) -> dict:
    client = client or anthropic.Anthropic()
    messages: list[dict] = [{"role": "user", "content": question}]
    first = client.messages.create(
        model=MODEL, max_tokens=512, tools=TOOLS, messages=messages,
    )
    calls = [block for block in first.content if getattr(block, "type", None) == "tool_use"]
    if len(calls) != 1:
        raise RuntimeError(
            f"Expected exactly one tool call; received {len(calls)}; stop_reason={first.stop_reason}."
        )

    messages.append({"role": "assistant", "content": first.content})
    call = calls[0]
    tool_result = execute_tool(call.name, call.input)
    result_block = {
        "type": "tool_result",
        "tool_use_id": call.id,
        "content": json.dumps(tool_result, ensure_ascii=False),
    }
    if not tool_result["ok"]:
        result_block["is_error"] = True
    messages.append({"role": "user", "content": [result_block]})

    final = client.messages.create(
        model=MODEL, max_tokens=512, tools=TOOLS, messages=messages,
    )
    final_text = "".join(
        getattr(block, "text", "")
        for block in final.content
        if getattr(block, "type", None) == "text"
    )
    return {
        "tool": call.name,
        "tool_result": tool_result,
        "result_block": result_block,
        "final": final_text,
        "messages": messages,
    }


if __name__ == "__main__":
    result = run_once("What is the temperature in Taipei? Use the weather tool.")
    print(result["final"])
    assert result["tool"] == "get_weather"
    assert result["tool_result"]["ok"] is True
    assert result["result_block"]["tool_use_id"]
    print("Stage 3 Exercise 1 Anthropic check passed")

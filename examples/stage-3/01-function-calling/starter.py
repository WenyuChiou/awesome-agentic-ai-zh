"""Stage 3 Exercise 1: one Ollama tool call and one tool result.

PowerShell:
    python -m pip install -r requirements.txt
    ollama pull qwen2.5:3b
    python starter.py

The OpenAI SDK talks only to the local Ollama endpoint. API cost: $0.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:3b")
TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Return demonstration weather data for one city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "A non-empty city name"},
                "unit": {"type": "string", "enum": ["celsius"]},
            },
            "required": ["city", "unit"],
            "additionalProperties": False,
        },
    },
}]


def get_weather(city: str, unit: str) -> dict:
    """Return fixed data so the lesson does not depend on a weather service."""
    return {"city": city, "temperature": 26, "unit": unit}


def execute_tool(name: str, raw_arguments: str) -> dict:
    """Treat a model-produced tool call as untrusted input."""
    if name != "get_weather":
        return {"ok": False, "error": "tool_not_allowed", "message": f"Tool not allowed: {name}"}
    try:
        args = json.loads(raw_arguments)
    except (TypeError, json.JSONDecodeError):
        return {"ok": False, "error": "invalid_arguments", "message": "Arguments must be JSON."}
    if (
        not isinstance(args, dict)
        or set(args) != {"city", "unit"}
        or not isinstance(args.get("city"), str)
        or not args["city"].strip()
        or args.get("unit") != "celsius"
    ):
        return {
            "ok": False,
            "error": "invalid_arguments",
            "message": "city must be a non-empty string; unit must be celsius.",
        }
    return {"ok": True, "data": get_weather(args["city"].strip(), args["unit"])}


def run_once(question: str, client: Any = None) -> dict:
    client = client or OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    messages: list[Any] = [{"role": "user", "content": question}]
    first = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
    assistant = first.choices[0].message
    calls = assistant.tool_calls or []
    if len(calls) != 1:
        raise RuntimeError(f"Expected exactly one tool call; received {len(calls)}.")

    messages.append(assistant.model_dump(exclude_none=True))
    call = calls[0]
    tool_result = execute_tool(call.function.name, call.function.arguments)
    messages.append({
        "role": "tool",
        "tool_call_id": call.id,
        "content": json.dumps(tool_result, ensure_ascii=False),
    })
    final = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
    return {
        "tool": call.function.name,
        "tool_result": tool_result,
        "final": final.choices[0].message.content or "",
        "messages": messages,
    }


if __name__ == "__main__":
    result = run_once("What is the temperature in Taipei? Use the weather tool.")
    print(result["final"])
    assert result["tool"] == "get_weather"
    assert result["tool_result"]["ok"] is True
    assert any(message.get("role") == "tool" for message in result["messages"])
    print("Stage 3 Exercise 1 Ollama check passed")

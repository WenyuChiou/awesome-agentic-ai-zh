"""練習 6：Schema 設計 — Bad schema（Path B、Anthropic Claude）。

故意保留 anti-pattern：description 太模糊、參數都用 string、沒有 required、沒有 enum。
模型很容易把溫度轉換誤判給 `process_data`。對照 `starter_good_anthropic.py`。

跑法：
    pip install -r requirements.txt
    $env:ANTHROPIC_API_KEY = "your-key"
    python starter_bad_anthropic.py

預算：每次先保留 $0.05；實際費用依 token 數計算。
Ollama 版本見 starter_bad.py。
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")


def process_data(data: str = "") -> str:
    return f"processed generic data: {data}"


def convert_temperature(value: str = "") -> str:
    return f"converted something from: {value}"


TOOLS_SPEC = [
    {
        "name": "process_data",
        "description": "Process data.",
        "input_schema": {"type": "object", "properties": {"data": {"type": "string"}}},
    },
    {
        "name": "convert_temperature",
        "description": "Convert a value.",
        "input_schema": {"type": "object", "properties": {"value": {"type": "string"}, "unit": {"type": "string"}}},
    },
]

TOOL_IMPL = {
    "process_data": lambda i: process_data(i.get("data", "")),
    "convert_temperature": lambda i: convert_temperature(i.get("value", "")),
}

def _validate_args(name: str, args: dict) -> str | None:
    expected = {
        "process_data": {"data"},
        "convert_temperature": {"value", "unit"},
    }[name]
    if set(args) != expected:
        return "arguments contain unexpected or missing fields"
    for field, value in args.items():
        if not isinstance(value, str) or not value.strip():
            return f"{field} must be a non-empty string"
    if name == "convert_temperature" and args["unit"].strip().lower() not in {
        "celsius",
        "fahrenheit",
    }:
        return "unit must be celsius or fahrenheit"
    return None


def execute_tool(name: str, arguments: Any) -> tuple[dict, object]:
    """Even a deliberately bad schema still needs a safe application boundary."""
    if name not in TOOL_IMPL:
        return {}, {"error": "tool not allowed"}
    if not isinstance(arguments, dict):
        return {}, {"error": "arguments must be an object"}
    args = dict(arguments)
    validation_error = _validate_args(name, args)
    if validation_error:
        return args, {"error": validation_error}
    try:
        return args, TOOL_IMPL[name](args)
    except (KeyError, TypeError, ValueError) as exc:
        return args, {"error": f"invalid arguments: {exc}"}


def select_and_run(question: str, client: Any = None) -> dict:
    client = client or anthropic.Anthropic()
    resp = client.messages.create(model=MODEL, max_tokens=512, tools=TOOLS_SPEC, messages=[{"role": "user", "content": question}])
    calls = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]
    if not calls:
        return {"tool": None, "tool_input": {}, "observation": None}
    if len(calls) != 1:
        return {"tool": None, "tool_input": {}, "observation": {"error": f"expected one tool call; received {len(calls)}"}}
    call = calls[0]
    args, observation = execute_tool(call.name, call.input)
    return {"tool": call.name, "tool_input": args, "observation": observation}


if __name__ == "__main__":
    result = select_and_run("Convert 32 Celsius to Fahrenheit.")
    print(result)

    # === 自我檢查 ===
    assert result["tool"] is not None, "even bad schema should produce an observable selection"
    assert result["observation"] is not None, "selected tool should produce an observable result"
    print("Stage 3 exercise 6 bad-schema starter check passed")

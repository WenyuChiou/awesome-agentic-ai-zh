"""練習 6：Schema 設計 — Good schema（Path B、Anthropic Claude）。

清楚的工具用途、正確型別、必填欄位與 enum 讓選擇條件更明確。
對照 `starter_bad_anthropic.py`，再用固定題目重跑多次比較。

跑法：
    pip install -r requirements.txt
    $env:ANTHROPIC_API_KEY = "your-key"
    python starter_good_anthropic.py

預算：每次先保留 $0.05；實際費用依 token 數計算。
Ollama 版本見 starter_good.py。
"""

from __future__ import annotations

import os, sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")


def process_data(data: list[dict], operation: str) -> dict:
    if operation == "count_rows":
        return {"rows": len(data)}
    if operation == "list_columns":
        return {"columns": sorted({key for row in data for key in row})}
    return {"error": "unknown operation", "retry_hint": "use count_rows or list_columns"}


def convert_temperature(value: float, unit: str) -> dict:
    if unit == "celsius":
        return {"value": round(value * 9 / 5 + 32, 2), "unit": "fahrenheit"}
    if unit == "fahrenheit":
        return {"value": round((value - 32) * 5 / 9, 2), "unit": "celsius"}
    return {"error": "unsupported unit", "retry_hint": "unit must be celsius or fahrenheit"}


TOOLS_SPEC = [
    {
        "name": "process_data",
        "description": "Use only to summarize structured JSON table rows. Do not use for temperature conversion.",
        "input_schema": {
            "type": "object",
            "properties": {
                "data": {"type": "array", "items": {"type": "object"}, "description": "Rows to inspect"},
                "operation": {"type": "string", "enum": ["count_rows", "list_columns"]},
            },
            "required": ["data", "operation"],
            "additionalProperties": False,
        },
    },
    {
        "name": "convert_temperature",
        "description": "Use this when the user asks to convert temperatures between Fahrenheit and Celsius.",
        "input_schema": {
            "type": "object",
            "properties": {
                "value": {"type": "number", "description": "Temperature value to convert"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"], "description": "Unit of the input value"},
            },
            "required": ["value", "unit"],
            "additionalProperties": False,
        },
    },
]

TOOL_IMPL = {"process_data": lambda i: process_data(i["data"], i["operation"]), "convert_temperature": lambda i: convert_temperature(i["value"], i["unit"])}

def _validate_args(name: str, args: dict) -> str | None:
    expected = {
        "process_data": {"data", "operation"},
        "convert_temperature": {"value", "unit"},
    }[name]
    if set(args) != expected:
        return "arguments contain unexpected or missing fields"
    if name == "process_data":
        if not isinstance(args["data"], list) or any(not isinstance(row, dict) for row in args["data"]):
            return "data must be a list of objects"
        if args["operation"] not in {"count_rows", "list_columns"}:
            return "operation must be count_rows or list_columns"
    else:
        if not isinstance(args["value"], (int, float)) or isinstance(args["value"], bool):
            return "value must be a number"
        if args["unit"] not in {"celsius", "fahrenheit"}:
            return "unit must be celsius or fahrenheit"
    return None


def execute_tool(name: str, arguments: Any) -> tuple[dict, object]:
    """Validate model output even when the schema is clear."""
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
    assert result["tool"] == "convert_temperature", f"expected convert_temperature, got {result['tool']}"
    assert result["observation"] == {"value": 89.6, "unit": "fahrenheit"}
    print("Stage 3 exercise 6 good-schema starter check passed")

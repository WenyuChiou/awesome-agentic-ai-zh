"""練習 6：Schema 設計 — Good schema（Path A、Ollama 默認）。

清楚的工具用途、正確型別、必填欄位與 enum 讓選擇條件更明確。對照 `starter_bad.py`，
再用固定題目重跑多次比較。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter_good.py
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


# Good schema: 用途明確、正確型別、required、enum
TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "process_data",
            "description": "Use only to summarize structured JSON table rows. Do not use for temperature conversion.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "array", "items": {"type": "object"}, "description": "Rows to inspect"},
                    "operation": {"type": "string", "enum": ["count_rows", "list_columns"]},
                },
                "required": ["data", "operation"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_temperature",
            "description": "Use this when the user asks to convert temperatures between Fahrenheit and Celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {"type": "number", "description": "Temperature value to convert"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"], "description": "Unit of the input value"},
                },
                "required": ["value", "unit"],
                "additionalProperties": False,
            },
        },
    },
]

TOOL_IMPL = {
    "process_data": lambda i: process_data(i["data"], i["operation"]),
    "convert_temperature": lambda i: convert_temperature(i["value"], i["unit"]),
}

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


def execute_tool(name: str, raw_arguments: str) -> tuple[dict, object]:
    """Validate model output even when the schema is clear."""
    if name not in TOOL_IMPL:
        return {}, {"error": "tool not allowed"}
    try:
        args = json.loads(raw_arguments)
    except (TypeError, json.JSONDecodeError):
        return {}, {"error": "arguments must be valid JSON"}
    if not isinstance(args, dict):
        return {}, {"error": "arguments must be a JSON object"}
    validation_error = _validate_args(name, args)
    if validation_error:
        return args, {"error": validation_error}
    try:
        return args, TOOL_IMPL[name](args)
    except (KeyError, TypeError, ValueError) as exc:
        return args, {"error": f"invalid arguments: {exc}"}


def select_and_run(question: str, client: Any = None) -> dict:
    client = client or OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    resp = client.chat.completions.create(
        model=MODEL,
        tools=TOOLS_SPEC,
        messages=[{"role": "user", "content": question}],
    )
    msg = resp.choices[0].message
    tool_calls = msg.tool_calls or []
    if not tool_calls:
        return {"tool": None, "tool_input": {}, "observation": None}
    if len(tool_calls) != 1:
        return {"tool": None, "tool_input": {}, "observation": {"error": f"expected one tool call; received {len(tool_calls)}"}}
    call = tool_calls[0]
    args, observation = execute_tool(call.function.name, call.function.arguments)
    return {"tool": call.function.name, "tool_input": args, "observation": observation}


if __name__ == "__main__":
    question = "Convert 32 Celsius to Fahrenheit."
    print(f"❓ 問題：{question}（using Ollama {MODEL}、GOOD schema）")
    result = select_and_run(question)
    print(f"   tool: {result['tool']}")
    print(f"   tool_input: {result.get('tool_input')}")
    print(f"   observation: {result['observation']}")

    assert result["tool"] == "convert_temperature", f"預期 convert_temperature、得到 {result['tool']}"
    assert result["observation"] == {"value": 89.6, "unit": "fahrenheit"}
    print("✅ Good schema starter 通過 — 這次模型在清楚的 schema 上挑對 tool、API 費 $0")

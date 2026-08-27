"""練習 6：Schema 設計 — Bad schema（Path A、Ollama 默認）。

故意保留 anti-pattern：description 太模糊、參數都用 string、沒有 required、沒有 enum。
這個 schema 讓模型更容易誤解。實際差異會隨模型、版本與 prompt 改變；請用固定 eval 比較。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter_bad.py
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


def process_data(data: str = "") -> str:
    return f"processed generic data: {data}"


def convert_temperature(value: str = "") -> str:
    return f"converted something from: {value}"


# Anti-pattern: description 太短、params 都 string、無 required、無 enum
TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "process_data",
            "description": "Process data.",
            "parameters": {"type": "object", "properties": {"data": {"type": "string"}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_temperature",
            "description": "Convert a value.",
            "parameters": {
                "type": "object",
                "properties": {"value": {"type": "string"}, "unit": {"type": "string"}},
            },
        },
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


def execute_tool(name: str, raw_arguments: str) -> tuple[dict, object]:
    """Even a deliberately bad schema still needs a safe application boundary."""
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
    print(f"❓ 問題：{question}（using Ollama {MODEL}、BAD schema）")
    result = select_and_run(question)
    print(f"   tool: {result['tool']}")
    print(f"   observation: {result['observation']}")

    # 寬鬆驗證：bad schema 不保證選對 tool、但至少要產出一個 tool call
    assert result["tool"] is not None, "even bad schema should produce an observable selection"
    assert result["observation"] is not None, "selected tool should produce an observable result"
    if result["tool"] != "convert_temperature":
        print("⚠ 這次壞 schema 挑錯了。對照 starter_good.py，並用固定題目重跑多次。")
    print("✅ Bad schema starter 跑通 — 對照 starter_good.py")

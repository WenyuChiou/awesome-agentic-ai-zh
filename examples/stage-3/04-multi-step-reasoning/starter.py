"""練習 4：多步驟推理任務 — Path A（Ollama 默認、本機免費）。

把練習 3 的 ReAct loop 延伸成 3-5 步任務：查台北人口 → 查紐約人口 → 相除 → 轉百分比。
重點：工具寫窄而穩、LLM 負責規劃下一步、max_iter 是 safety net。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter.py

驗證：
    python test.py   （用 mock、不打 API）

想看 Anthropic Claude 版本：
    python starter_anthropic.py   （需 ANTHROPIC_API_KEY；每次先保留 $0.05）

⚠️ 不同模型、版本與 prompt 的結果會變。用固定題目跑多次，記錄每一步再比較。
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:3b")
MAX_ABS_NUMBER = 1_000_000_000_000.0


class ToolExecutionError(ValueError):
    """A tool error that the loop should return to the model as data."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def bounded_number(value: float, field: str) -> float:
    """Accept only ordinary finite numbers that stay inside the lesson's limit."""
    if isinstance(value, int) and abs(value) > MAX_ABS_NUMBER:
        raise ToolExecutionError("number_too_large", f"{field} is outside the allowed range")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ToolExecutionError(
            "number_too_large", f"{field} is outside the allowed range"
        ) from exc
    if not math.isfinite(number):
        raise ToolExecutionError("non_finite_number", f"{field} must be finite")
    if abs(number) > MAX_ABS_NUMBER:
        raise ToolExecutionError("number_too_large", f"{field} is outside the allowed range")
    return number


def error_payload(code: str, message: str) -> str:
    return json.dumps({"error": {"code": code, "message": message}}, ensure_ascii=False)


# === 1. Tools 定義（含實作）===

def lookup_population(city: str) -> str:
    data = {"taipei": 2_602_000, "new york": 8_336_000, "empty city": 0}
    return str(data.get(city.strip().lower(), 0))


def divide(a: float, b: float) -> str:
    numerator = bounded_number(a, "a")
    denominator = bounded_number(b, "b")
    if denominator == 0:
        raise ToolExecutionError("division_by_zero", "b must not be zero")
    return str(bounded_number(numerator / denominator, "result"))


def to_percentage(ratio: float) -> str:
    result = bounded_number(bounded_number(ratio, "ratio") * 100, "result")
    return f"{result:.2f}"


def round_int(x: float) -> str:
    return str(round(bounded_number(x, "x")))


# OpenAI-compat 包一層 {"type": "function", "function": {...}}
TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "lookup_population",
            "description": "Return the population for a known city.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "divide",
            "description": "Divide a by b. Returns a structured error when b is zero.",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                "required": ["a", "b"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "to_percentage",
            "description": "Convert a ratio such as 0.31 into a percentage number.",
            "parameters": {
                "type": "object",
                "properties": {"ratio": {"type": "number"}},
                "required": ["ratio"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "round_int",
            "description": "Round a number to the nearest integer.",
            "parameters": {
                "type": "object",
                "properties": {"x": {"type": "number"}},
                "required": ["x"],
                "additionalProperties": False,
            },
        },
    },
]

TOOL_IMPL = {
    "lookup_population": lambda i: lookup_population(i["city"]),
    "divide": lambda i: divide(i["a"], i["b"]),
    "to_percentage": lambda i: to_percentage(i["ratio"]),
    "round_int": lambda i: round_int(i["x"]),
}

TOOL_ARGUMENTS = {
    "lookup_population": {"city": "string"},
    "divide": {"a": "number", "b": "number"},
    "to_percentage": {"ratio": "number"},
    "round_int": {"x": "number"},
}


def execute_tool(name: str, raw_arguments: str) -> tuple[dict, str, bool]:
    """Validate an untrusted tool call before dispatch."""
    if name not in TOOL_IMPL:
        return {}, f"error: tool not allowed: {name}", True
    try:
        args = json.loads(raw_arguments)
    except (TypeError, json.JSONDecodeError):
        return {}, "error: arguments must be valid JSON", True
    except ValueError:
        return {}, error_payload("number_too_large", "numeric argument is too large"), True
    if not isinstance(args, dict):
        return {}, "error: arguments must be a JSON object", True
    expected = TOOL_ARGUMENTS[name]
    if set(args) != set(expected):
        return {}, "error: arguments contain unexpected or missing fields", True
    for field, kind in expected.items():
        value = args[field]
        if kind == "string":
            if not isinstance(value, str) or not value.strip():
                return {}, f"error: {field} must be a non-empty string", True
        elif not isinstance(value, (int, float)) or isinstance(value, bool):
            return {}, f"error: {field} must be a number", True
        else:
            try:
                bounded_number(value, field)
            except ToolExecutionError as exc:
                return args, error_payload(exc.code, str(exc)), True
    try:
        return args, TOOL_IMPL[name](args), False
    except ToolExecutionError as exc:
        return args, error_payload(exc.code, str(exc)), True
    except (KeyError, OverflowError, TypeError, ValueError) as exc:
        return args, f"error: invalid arguments: {exc}", True


# === 2. ReAct loop（OpenAI-compat）===

def react_loop(question: str, max_iter: int = 8, client: Any = None) -> dict:
    """OpenAI-compat 多步驟 ReAct loop。"""
    client = client or OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    messages = [{"role": "user", "content": question}]
    trace: list[dict] = []

    for step in range(max_iter):
        resp = client.chat.completions.create(
            model=MODEL,
            tools=TOOLS_SPEC,
            messages=messages,
        )
        msg = resp.choices[0].message
        text = msg.content or ""
        tool_calls = msg.tool_calls or []

        assistant_entry: dict = {"role": "assistant", "content": text}
        if tool_calls:
            assistant_entry["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in tool_calls
            ]
        messages.append(assistant_entry)

        finish_reason = resp.choices[0].finish_reason
        if not tool_calls:
            trace.append({"step": step, "assistant_text": text, "tool": None, "obs": None})
            if finish_reason == "stop":
                return {"final": text, "trace": trace, "steps": step + 1}
            return {
                "final": None,
                "trace": trace,
                "steps": step + 1,
                "terminal_reason": finish_reason or "missing_tool_call",
                "truncated": finish_reason == "length",
            }

        for tc in tool_calls:
            args, obs, _ = execute_tool(tc.function.name, tc.function.arguments)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": obs,
            })
            trace.append({"step": step, "assistant_text": text, "tool": tc.function.name, "tool_input": args, "obs": obs})

    return {"final": None, "trace": trace, "steps": max_iter, "truncated": True}


# === 3. 自我驗證 ===

if __name__ == "__main__":
    question = "Find Taipei population divided by New York population, then express it as a percentage."
    print(f"❓ 問題：{question}（using Ollama {MODEL}）")
    print("-" * 60)

    result = react_loop(question)
    for entry in result["trace"]:
        if entry["tool"]:
            print(f"[step {entry['step']}] tool: {entry['tool']}({entry.get('tool_input')}) → {entry['obs']}")
    print("-" * 60)
    print(f"✅ 最終答案：{result['final']}")
    print(f"   共 {result['steps']} 輪")

    # 寬鬆驗證：小 model 不一定走完 4 步、但 loop 至少要收尾或顯式 truncate
    assert result.get("final") is not None or result.get("truncated"), "loop 應收尾或 truncate"
    assert result["steps"] <= 8, "loop 不可超過 max_iter"
    print("✅ 練習 4 通過 — 你已用本機 qwen2.5:3b 跑通多步 ReAct loop、$0/run")

"""練習 4：多步驟推理任務 — Path B（Anthropic Claude）。

把練習 3 的 ReAct loop 延伸成 3-5 步任務：查台北人口 → 查紐約人口 → 相除 → 轉百分比。
工具負責執行小動作、LLM 負責規劃下一步。

跑法：
    pip install -r requirements.txt
    $env:ANTHROPIC_API_KEY = "your-key"
    python starter_anthropic.py

預算：每次先保留 $0.05；實際費用依 token 數與累積 messages 計算。
Ollama 版本見 starter.py（API 費 $0）。
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")
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


TOOLS_SPEC = [
    {"name": "lookup_population", "description": "Return the population for a known city.", "input_schema": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"], "additionalProperties": False}},
    {"name": "divide", "description": "Divide a by b. Returns a structured error when b is zero.", "input_schema": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}, "required": ["a", "b"], "additionalProperties": False}},
    {"name": "to_percentage", "description": "Convert a ratio such as 0.31 into a percentage number.", "input_schema": {"type": "object", "properties": {"ratio": {"type": "number"}}, "required": ["ratio"], "additionalProperties": False}},
    {"name": "round_int", "description": "Round a number to the nearest integer.", "input_schema": {"type": "object", "properties": {"x": {"type": "number"}}, "required": ["x"], "additionalProperties": False}},
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


def execute_tool(name: str, arguments: Any) -> tuple[dict, str, bool]:
    """Validate an untrusted tool call before dispatch."""
    if name not in TOOL_IMPL:
        return {}, f"error: tool not allowed: {name}", True
    if not isinstance(arguments, dict):
        return {}, "error: arguments must be an object", True
    args = dict(arguments)
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


def react_loop(question: str, max_iter: int = 8, client: Any = None) -> dict:
    client = client or anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]
    trace: list[dict] = []
    for step in range(max_iter):
        resp = client.messages.create(model=MODEL, max_tokens=1024, tools=TOOLS_SPEC, messages=messages)
        text = " ".join(getattr(b, "text", "") for b in resp.content if getattr(b, "type", None) == "text")
        calls = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]
        messages.append({"role": "assistant", "content": resp.content})
        if not calls:
            trace.append({"step": step, "assistant_text": text, "tool": None, "obs": None})
            if resp.stop_reason == "end_turn":
                return {"final": text, "trace": trace, "steps": step + 1}
            return {
                "final": None,
                "trace": trace,
                "steps": step + 1,
                "terminal_reason": resp.stop_reason or "missing_tool_call",
                "truncated": resp.stop_reason == "max_tokens",
            }
        results = []
        for call in calls:
            args, obs, is_error = execute_tool(call.name, call.input)
            result_block = {"type": "tool_result", "tool_use_id": call.id, "content": obs}
            if is_error:
                result_block["is_error"] = True
            results.append(result_block)
            trace.append({"step": step, "assistant_text": text, "tool": call.name, "tool_input": args, "obs": obs})
        messages.append({"role": "user", "content": results})
    return {"final": None, "trace": trace, "steps": max_iter, "truncated": True}


if __name__ == "__main__":
    result = react_loop("Find Taipei population divided by New York population, then express it as a percentage.")
    print(result)

    # === 自我檢查 ===
    assert result["final"] is not None, "expected the loop to reach end_turn"
    assert any(str(n) in result["final"] for n in range(28, 35)), "expected a final answer near 31%"
    print("Stage 3 exercise 4 starter check passed")

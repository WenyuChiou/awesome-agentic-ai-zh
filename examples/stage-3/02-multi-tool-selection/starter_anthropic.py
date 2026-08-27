"""練習 2：多工具選擇 — Path B（Anthropic Claude）。

讓 Claude 在 3 個 tool（web_search / calculator / calendar_lookup）裡選一個執行。
重點：tool schema 的 description 越精準、模型選對的機率越高。

跑法：
    pip install -r requirements.txt
    $env:ANTHROPIC_API_KEY = "your-key"
    python starter_anthropic.py

預算：每次先保留 $0.05；實際費用依 token 數計算。
Ollama 版本見 starter.py（本機 $0）。
"""

from __future__ import annotations

import ast
import math
import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")


def web_search(query: str) -> str:
    return f"search result: {query} -> Anthropic tool use docs and examples"


MAX_EXPRESSION_LENGTH = 200
MAX_AST_NODES = 50
MAX_AST_DEPTH = 12
MAX_ABS_NUMBER = 1_000_000_000_000


def _within_bounds(value: int | float) -> bool:
    if isinstance(value, int):
        return abs(value) <= MAX_ABS_NUMBER
    return math.isfinite(value) and abs(value) <= MAX_ABS_NUMBER


def _evaluate_arithmetic(expression: str) -> int | float:
    """Evaluate only small numeric expressions; model text never becomes code."""
    if len(expression) > MAX_EXPRESSION_LENGTH:
        raise ValueError("expression is too long")
    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, ValueError, TypeError):
        raise ValueError("calculator only accepts basic arithmetic") from None
    if sum(1 for _ in ast.walk(tree)) > MAX_AST_NODES:
        raise ValueError("expression has too many parts")

    def visit(node: ast.AST, depth: int = 0) -> int | float:
        if depth > MAX_AST_DEPTH:
            raise ValueError("expression is too deeply nested")
        if isinstance(node, ast.Expression):
            return visit(node.body, depth + 1)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            value = node.value
            if not _within_bounds(value):
                raise ValueError("number is out of bounds")
            return value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand, depth + 1)
            result = value if isinstance(node.op, ast.UAdd) else -value
        elif isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            left = visit(node.left, depth + 1)
            right = visit(node.right, depth + 1)
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ValueError("division by zero")
                result = left / right
            elif isinstance(node.op, ast.Add):
                result = left + right
            elif isinstance(node.op, ast.Sub):
                result = left - right
            else:
                result = left * right
        else:
            raise ValueError("calculator only accepts numbers and + - * /")
        if not _within_bounds(result):
            raise ValueError("result is out of bounds")
        return result

    return visit(tree)


def calculator(expression: str) -> str:
    try:
        return str(_evaluate_arithmetic(expression))
    except (TypeError, ValueError) as exc:
        return f"error: {exc}"


def calendar_lookup(date: str) -> str:
    events = {"2026-05-13": "10:00 Stage 3 review, 15:00 agent study group", "tomorrow": "10:00 Stage 3 review, 15:00 agent study group"}
    return events.get(date.strip(), f"no events found for {date}")


def tool_schema(name: str, description: str, field: str, field_description: str) -> dict:
    return {"name": name, "description": description, "input_schema": {"type": "object", "properties": {field: {"type": "string", "description": field_description}}, "required": [field], "additionalProperties": False}}


TOOLS_SPEC = [
    tool_schema("web_search", "Search current or external information not in the prompt.", "query", "Search query"),
    tool_schema("calculator", "Evaluate basic arithmetic with +, -, *, /, and parentheses.", "expression", "Math expression"),
    tool_schema("calendar_lookup", "Look up events for a specific date or relative day.", "date", "Date to inspect"),
]

TOOL_IMPL = {
    "web_search": lambda args: web_search(args["query"]),
    "calculator": lambda args: calculator(args["expression"]),
    "calendar_lookup": lambda args: calendar_lookup(args["date"]),
}

TOOL_FIELDS = {
    "web_search": "query",
    "calculator": "expression",
    "calendar_lookup": "date",
}


def execute_tool(name: str, arguments: Any) -> tuple[dict, str]:
    """Validate model output before dispatching an allowlisted tool."""
    if name not in TOOL_IMPL:
        return {}, f"error: tool not allowed: {name}"
    if not isinstance(arguments, dict):
        return {}, "error: arguments must be an object"
    args = dict(arguments)
    field = TOOL_FIELDS[name]
    if set(args) != {field}:
        return {}, f"error: arguments must contain exactly {field}"
    if not isinstance(args[field], str) or not args[field].strip():
        return {}, f"error: {field} must be a non-empty string"
    try:
        return args, TOOL_IMPL[name](args)
    except (KeyError, TypeError, ValueError) as exc:
        return args, f"error: invalid arguments: {exc}"


def run_tool_selection(question: str, client: Any = None) -> dict:
    client = client or anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=512,
        tools=TOOLS_SPEC,
        messages=[{"role": "user", "content": question}],
    )
    text = " ".join(getattr(b, "text", "") for b in resp.content if getattr(b, "type", None) == "text")
    tool_calls = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]
    if not tool_calls:
        return {"tool": None, "assistant_text": text, "observation": None}
    if len(tool_calls) != 1:
        return {
            "tool": None,
            "assistant_text": text,
            "observation": f"error: expected exactly one tool call; received {len(tool_calls)}",
        }
    call = tool_calls[0]
    args, observation = execute_tool(call.name, call.input)
    return {"tool": call.name, "tool_input": args, "assistant_text": text, "observation": observation}


if __name__ == "__main__":
    result = run_tool_selection("What is (19 * 42) - 8? Use the best available tool.")
    print(result)

    # === 自我檢查 ===
    assert result["tool"] == "calculator", f"expected calculator, got {result['tool']}"
    assert result["observation"] and not result["observation"].startswith("error:")
    print("Stage 3 exercise 2 starter check passed")

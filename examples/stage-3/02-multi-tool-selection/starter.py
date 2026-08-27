"""練習 2：多工具選擇 — Path A（Ollama 默認、本機免費）。

讓本機 qwen2.5:3b 在 3 個 tool（web_search / calculator / calendar_lookup）裡選一個。
重點不是工具強不強，是觀察 schema 的 description / 參數 / required 如何引導模型選對。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b   # Stage 3+ tool-use 默認 model
    ollama serve             # 預設 port 11434
    python starter.py

驗證：
    python test.py   （用 mock、不打 API）

想看 Anthropic Claude 版本：
    python starter_anthropic.py   （需 ANTHROPIC_API_KEY；每次先保留 $0.05）
"""

from __future__ import annotations

import ast
import json
import math
import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:3b")


# === 1. Tools 定義（含實作）===

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
    events = {
        "2026-05-13": "10:00 Stage 3 review, 15:00 agent study group",
        "tomorrow": "10:00 Stage 3 review, 15:00 agent study group",
    }
    return events.get(date.strip(), f"no events found for {date}")


# OpenAI-compat 的 tools schema 要包一層 {"type": "function", "function": {...}}
def _wrap(name: str, description: str, field: str, field_description: str) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {field: {"type": "string", "description": field_description}},
                "required": [field],
                "additionalProperties": False,
            },
        },
    }


TOOLS_SPEC = [
    _wrap("web_search", "Search current or external information not in the prompt.", "query", "Search query"),
    _wrap("calculator", "Evaluate basic arithmetic with +, -, *, /, and parentheses.", "expression", "Math expression"),
    _wrap("calendar_lookup", "Look up events for a specific date or relative day.", "date", "Date to inspect"),
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


def execute_tool(name: str, raw_arguments: str) -> tuple[dict, str]:
    """Parse and validate model output before dispatching an allowlisted tool."""
    if name not in TOOL_IMPL:
        return {}, f"error: tool not allowed: {name}"
    try:
        args = json.loads(raw_arguments)
    except (TypeError, json.JSONDecodeError):
        return {}, "error: arguments must be valid JSON"
    if not isinstance(args, dict):
        return {}, "error: arguments must be a JSON object"
    field = TOOL_FIELDS[name]
    if set(args) != {field}:
        return {}, f"error: arguments must contain exactly {field}"
    if not isinstance(args[field], str) or not args[field].strip():
        return {}, f"error: {field} must be a non-empty string"
    try:
        return args, TOOL_IMPL[name](args)
    except (KeyError, TypeError, ValueError) as exc:
        return args, f"error: invalid arguments: {exc}"


# === 2. 單輪 tool selection ===

def run_tool_selection(question: str, client: Any = None) -> dict:
    """單輪 call：LLM 看完 question + tools 後選一個 tool 呼叫，本地執行 observation 接回去。"""
    client = client or OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    resp = client.chat.completions.create(
        model=MODEL,
        tools=TOOLS_SPEC,
        messages=[{"role": "user", "content": question}],
    )
    msg = resp.choices[0].message
    text = msg.content or ""
    tool_calls = msg.tool_calls or []
    if not tool_calls:
        return {"tool": None, "assistant_text": text, "observation": None}
    if len(tool_calls) != 1:
        return {
            "tool": None,
            "assistant_text": text,
            "observation": f"error: expected exactly one tool call; received {len(tool_calls)}",
        }
    call = tool_calls[0]
    args, observation = execute_tool(call.function.name, call.function.arguments)
    return {
        "tool": call.function.name,
        "tool_input": args,
        "assistant_text": text,
        "observation": observation,
    }


# === 3. 自我驗證 ===

if __name__ == "__main__":
    question = "What is (19 * 42) - 8? Use the best available tool."
    print(f"❓ 問題：{question}（using Ollama {MODEL}）")
    result = run_tool_selection(question)
    print(f"   tool: {result['tool']}")
    print(f"   tool_input: {result.get('tool_input')}")
    print(f"   observation: {result['observation']}")

    assert result["tool"] == "calculator", f"預期 calculator、得到 {result['tool']}"
    assert result["observation"] and not result["observation"].startswith("error:")
    print("✅ 練習 2 通過 — 你已用本機 qwen2.5:3b 跑通 multi-tool selection、$0/run")

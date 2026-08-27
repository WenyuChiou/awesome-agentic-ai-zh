"""
練習 3：從零實作 ReAct（不用 framework）— starter.py

目的：用一小段 Python 把「assistant 文字 → Tool Call → Tool Result」迴圈寫出來。
不要 LangChain、不要 LangGraph，就是純 while loop。

跑法：
    pip install -r requirements.txt
    $env:ANTHROPIC_API_KEY = "your-key"
    python starter_anthropic.py

驗證：
    python test_anthropic.py  （用 mock、不花 API 錢）
"""

from __future__ import annotations

import ast
import json
import math
import os
import sys
from typing import Any

# Windows cp950 console 無法印 emoji / 中文、強制 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")

# === 1. Tools 定義（含實作） ===

MAX_EXPRESSION_LENGTH = 200
MAX_AST_NODES = 50
MAX_AST_DEPTH = 12
MAX_ABS_NUMBER = 1_000_000_000_000


def _within_bounds(value: int | float) -> bool:
    if isinstance(value, int):
        return abs(value) <= MAX_ABS_NUMBER
    return math.isfinite(value) and abs(value) <= MAX_ABS_NUMBER


def _evaluate_arithmetic(expression: str) -> int | float:
    """只計算小型數學式；模型文字永遠不會變成程式碼。"""
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


def tool_calculator(expression: str) -> str:
    """安全的計算器：只允許 + - * / 跟數字。"""
    try:
        return str(_evaluate_arithmetic(expression))
    except (TypeError, ValueError) as exc:
        return f"error: {exc}"


def tool_lookup_fact(query: str) -> str:
    """假的事實查詢（避免依賴外部 API、教學專用）。"""
    facts = {
        "台北人口": "2602000",
        "紐約人口": "8336000",
        "光速": "299792458",  # m/s
    }
    return facts.get(query.strip(), f"unknown: {query}")


TOOLS_SPEC = [
    {
        "name": "calculator",
        "description": "做基本算術運算（加減乘除）。輸入是表達式字串，例如 '3 * (5+2)'。",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "算術表達式"},
            },
            "required": ["expression"],
            "additionalProperties": False,
        },
    },
    {
        "name": "lookup_fact",
        "description": "查詢一個事實（人口 / 物理常數等）。輸入是查詢關鍵字、回傳一個字串答案或 'unknown: ...'。",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "查詢關鍵字（如「台北人口」、「光速」）"},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
]

TOOL_IMPL = {
    "calculator": lambda inp: tool_calculator(inp["expression"]),
    "lookup_fact": lambda inp: tool_lookup_fact(inp["query"]),
}

TOOL_FIELDS = {
    "calculator": "expression",
    "lookup_fact": "query",
}


def execute_tool(name: str, arguments: Any) -> tuple[dict, str, bool]:
    """Validate an untrusted tool call before dispatch."""
    if name not in TOOL_IMPL:
        return {}, f"error: tool not allowed: {name}", True
    if not isinstance(arguments, dict):
        return {}, "error: arguments must be an object", True
    args = dict(arguments)
    field = TOOL_FIELDS[name]
    if set(args) != {field}:
        return {}, f"error: arguments must contain exactly {field}", True
    if not isinstance(args[field], str) or not args[field].strip():
        return {}, f"error: {field} must be a non-empty string", True
    try:
        observation = TOOL_IMPL[name](args)
    except (KeyError, TypeError, ValueError) as exc:
        return args, f"error: invalid arguments: {exc}", True
    return args, observation, observation.startswith("error:")


# === 2. ReAct loop ===

def react_loop(question: str, max_iter: int = 6, client: Any = None) -> dict:
    """
    純 while 迴圈、每輪：
      1. 問 LLM（含 tools）
      2. 看 stop_reason：tool_use → 執行工具、把結果加進 messages、繼續
                       end_turn → 完成、回傳最終答案
    回傳 {final, trace}。trace 只記錄可觀察的 assistant 文字、tool 與 result。
    """
    client = client or anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]
    trace: list[dict] = []

    for step in range(max_iter):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOLS_SPEC,
            messages=messages,
        )

        assistant_text = " ".join(b.text for b in resp.content if b.type == "text")
        tool_calls = [b for b in resp.content if b.type == "tool_use"]

        # 把 assistant 整個 response 加進 messages（給下一輪 context）
        messages.append({"role": "assistant", "content": resp.content})

        if not tool_calls:
            trace.append({"step": step, "assistant_text": assistant_text, "tool": None, "obs": None})
            if resp.stop_reason == "end_turn":
                return {"final": assistant_text, "trace": trace, "steps": step + 1}
            return {
                "final": None,
                "trace": trace,
                "steps": step + 1,
                "terminal_reason": resp.stop_reason or "missing_tool_call",
                "truncated": resp.stop_reason == "max_tokens",
            }

        # 執行所有 tool call、把 observation 接回去
        tool_results = []
        for call in tool_calls:
            args, obs, is_error = execute_tool(call.name, call.input)
            result_block = {"type": "tool_result", "tool_use_id": call.id, "content": obs}
            if is_error:
                result_block["is_error"] = True
            tool_results.append(result_block)
            trace.append({
                "step": step,
                "assistant_text": assistant_text,
                "tool": call.name,
                "tool_input": args,
                "obs": obs,
            })
        messages.append({"role": "user", "content": tool_results})

    # 跑滿 max_iter 還沒收尾
    return {"final": None, "trace": trace, "steps": max_iter, "truncated": True}


# === 3. 自我驗證（跑真 API） ===

if __name__ == "__main__":
    question = "台北人口除以紐約人口、答案保留 4 位小數。"
    print(f"❓ 問題：{question}")
    print("-" * 60)

    result = react_loop(question, max_iter=5)

    for entry in result["trace"]:
        print(f"[step {entry['step']}] assistant: {entry['assistant_text'][:80]}...")
        if entry["tool"]:
            print(f"           tool: {entry['tool']}({entry.get('tool_input')}) → {entry['obs']}")
    print("-" * 60)
    print(f"✅ 最終答案：{result['final']}")
    print(f"   共 {result['steps']} 輪")

    # === 自我驗證 ===
    assert result.get("final") is not None, "預期 react_loop 在 max_iter 內收尾"
    assert "0.3" in (result["final"] or ""), f"預期答案含 0.3xxx（2602000/8336000≈0.3122）"
    print("✅ 練習 3 通過 — ReAct loop 自己連用了 lookup_fact 跟 calculator")

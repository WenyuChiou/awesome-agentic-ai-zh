"""Stage 4 練習 4：比較有界 CodeAct 與安全的 JSON tool 算術路徑。

JSON tool 只允許固定工具與固定參數；算式先轉成 AST，再逐節點檢查。
CodeAct 會執行模型產生的 Python，所以只在受限制的 Docker 容器裡示範。
Jupyter 控制埠只綁到主機的 127.0.0.1；容器仍可能連網，因此這不是 production
sandbox。兩條路都設有步數與輸入邊界。
"""

from __future__ import annotations

import ast
import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from smolagents import CodeAgent, OpenAIServerModel, ToolCallingAgent, tool

MODEL = os.environ.get("MODEL", "qwen2.5:3b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")
MAX_AST_NODES = 40
MAX_NUMBER = 1_000_000


def evaluate_arithmetic(expression: str) -> float:
    """只計算小型算術 AST；模型文字不會交給 ``eval`` 或 ``exec``。"""
    if not isinstance(expression, str) or len(expression) > 120:
        raise ValueError("Expression must be a string of at most 120 characters.")
    tree = ast.parse(expression, mode="eval")
    if sum(1 for _ in ast.walk(tree)) > MAX_AST_NODES:
        raise ValueError("Expression is too complex.")

    def visit(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            value = float(node.value)
            if abs(value) > MAX_NUMBER:
                raise ValueError("Number magnitude is too large.")
            return value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            return visit(node.operand) if isinstance(node.op, ast.UAdd) else -visit(node.operand)
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add): return left + right
            if isinstance(node.op, ast.Sub): return left - right
            if isinstance(node.op, ast.Mult): return left * right
            if right == 0: raise ValueError("Division by zero is not allowed.")
            return left / right
        raise ValueError(f"Unsupported arithmetic syntax: {type(node).__name__}")

    value = visit(tree)
    if abs(value) > MAX_NUMBER:
        raise ValueError("Result magnitude is too large.")
    return value


@tool
def calculator(expression: str) -> str:
    """Return a guarded arithmetic result for a small expression.

    Args:
        expression: Digits, parentheses, and the +, -, *, / operators only.
    """
    try:
        return str(evaluate_arithmetic(expression))
    except (SyntaxError, ValueError) as error:
        return f"error: {error}"


@tool
def lookup_fact(query: str) -> str:
    """Return one fixed offline fact from a tiny allowlist.

    Args:
        query: Either ``Taipei population`` or ``New York population``.
    """
    facts = {"taipei population": "2602000", "new york population": "8336000"}
    return facts.get(query.strip().lower(), f"unknown: {query}")


def run_json_tool_call(call: dict[str, Any]) -> str:
    """JSON tool 邊界：工具名、參數形狀與算式都要先通過檢查。"""
    if not isinstance(call, dict) or set(call) != {"name", "arguments"}:
        raise ValueError("A JSON tool call needs exactly name and arguments.")
    if call["name"] != "calculator" or not isinstance(call["arguments"], dict) or set(call["arguments"]) != {"expression"}:
        raise ValueError("Only calculator(expression=...) is allowed.")
    return calculator.forward(expression=call["arguments"]["expression"])


def codeact_executor_config() -> dict[str, Any]:
    """縮小示範容器權限，並把 Jupyter 控制埠只綁到本機。"""
    return {
        "allow_pickle": False,
        "host": "127.0.0.1",
        "container_run_kwargs": {
            "network_mode": "bridge",
            "mem_limit": "256m",
            "pids_limit": 64,
            "cap_drop": ["ALL"],
            "security_opt": ["no-new-privileges"],
        },
    }


def build_codeact_agent(model: Any | None = None, executor_type: str = "docker") -> CodeAgent:
    """建立最多走四步、且預設只在 Docker 裡執行程式碼的 agent。"""
    model = model or OpenAIServerModel(model_id=MODEL, api_base=OLLAMA_BASE, api_key="ollama")
    executor_kwargs = codeact_executor_config() if executor_type == "docker" else {}
    return CodeAgent(tools=[calculator, lookup_fact], model=model, max_steps=4, additional_authorized_imports=[], executor_type=executor_type, executor_kwargs=executor_kwargs)


def build_json_agent(model: Any) -> ToolCallingAgent:
    """建立同工具集合的 JSON tool 對照組。"""
    return ToolCallingAgent(tools=[calculator, lookup_fact], model=model, max_steps=4)


def run(question: str, model: Any | None = None) -> dict[str, str]:
    agent = build_codeact_agent(model=model)
    try:
        return {"final": str(agent.run(question))}
    finally:
        agent.cleanup()


if __name__ == "__main__":
    result = run("Find Taipei population, divide it by New York population, and report the ratio.")
    print(result["final"])
    assert result["final"]
    assert run_json_tool_call({"name": "calculator", "arguments": {"expression": "2 + 3 * 4"}}) == "14.0"

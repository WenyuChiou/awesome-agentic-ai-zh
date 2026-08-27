"""練習 5：Tool 錯誤處理 — Path B（Anthropic Claude）。

故意讓 fetch_weather 第一次回 error、第二次才成功。觀察 ReAct loop 怎麼把錯誤
observation 交回 LLM、讓模型決定要 retry / 改 query / 放棄。錯誤回傳是
結構化 dict（`{"error", "retry_hint"}`）、不是 Python exception。

跑法：
    pip install -r requirements.txt
    $env:ANTHROPIC_API_KEY = "your-key"
    python starter_anthropic.py

預算：每次先保留 $0.05；實際費用依 token 數與累積 messages 計算。
Ollama 版本見 starter.py（API 費 $0）。
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")
_failure_plan: list[bool] = [True, False]


def set_weather_failures(plan: list[bool]) -> None:
    global _failure_plan
    _failure_plan = list(plan)


def fetch_weather(city: str) -> dict:
    should_fail = _failure_plan.pop(0) if _failure_plan else False
    if should_fail:
        return {"error": "network timeout", "retry_hint": "try again in 1s"}
    return {"city": city, "forecast": "rain", "temperature_c": 24}


TOOLS_SPEC = [
    {
        "name": "fetch_weather",
        "description": "Fetch current weather. If an error is returned, inspect retry_hint before retrying.",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "City name"}},
            "required": ["city"],
            "additionalProperties": False,
        },
    }
]


def execute_tool(name: str, arguments: Any) -> tuple[dict, dict, bool]:
    """Validate an untrusted call and always return a structured result."""
    if name != "fetch_weather":
        return {}, {"error": "tool not allowed", "retry_hint": "choose fetch_weather"}, True
    if (
        not isinstance(arguments, dict)
        or set(arguments) != {"city"}
        or not isinstance(arguments.get("city"), str)
        or not arguments["city"].strip()
    ):
        args = dict(arguments) if isinstance(arguments, dict) else {}
        return args, {"error": "invalid arguments", "retry_hint": "city must be a non-empty string"}, True
    args = dict(arguments)
    observation = fetch_weather(args["city"].strip())
    return args, observation, "error" in observation


def react_loop(question: str, max_iter: int = 5, client: Any = None) -> dict:
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
            result_block = {"type": "tool_result", "tool_use_id": call.id, "content": json.dumps(obs, ensure_ascii=False)}
            if is_error:
                result_block["is_error"] = True
            results.append(result_block)
            trace.append({"step": step, "assistant_text": text, "tool": call.name, "tool_input": args, "obs": obs})
        messages.append({"role": "user", "content": results})
    return {"final": None, "trace": trace, "steps": max_iter, "truncated": True}


if __name__ == "__main__":
    set_weather_failures([True, False])
    result = react_loop("Will it rain in Taipei today?")
    print(result)

    # === 自我檢查 ===
    assert result["trace"][0]["obs"]["error"] == "network timeout"
    assert result["trace"][1]["obs"]["forecast"] == "rain"
    assert result["final"] is not None
    print("Stage 3 exercise 5 starter check passed")

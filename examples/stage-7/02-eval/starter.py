"""Stage 7 練習 2：Eval — Path A（Ollama）。

Eval pipeline = 「pytest for LLMs」。為 production agent 寫 5-10 個 eval case、跑 baseline、
追蹤 regression。Production 沒 eval = 沒 confidence ship。

兩種 evaluator：
1. **String match**：output 含特定 keyword（簡單、無 LLM cost）
2. **LLM-as-judge**：用 LLM 評分（複雜但 flexible）

跑法：
    pip install -r requirements.txt
    ollama pull qwen3.5:4b
    ollama serve
    python starter.py
"""

from __future__ import annotations

import os
import re
import sys
from typing import Any, Callable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen3.5:4b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")


def require_text(value: str | None, label: str) -> str:
    """Reject a provider response that contains no usable text."""
    text = (value or "").strip()
    if not text:
        raise ValueError(f"{label} returned empty text")
    return text


def parse_verdict(verdict: str) -> bool:
    """Map an exact PASS or FAIL Judge response to a boolean."""
    match = re.fullmatch(r"(PASS|FAIL)", verdict.strip(), re.IGNORECASE)
    if not match:
        raise ValueError("Judge must reply with exactly PASS or FAIL")
    return match.group(1).upper() == "PASS"


# === Eval cases ===

EVAL_CASES = [
    {"id": "math_1", "input": "What is 2 + 2?", "expected_substring": "4"},
    {"id": "math_2", "input": "What is 10 * 5?", "expected_substring": "50"},
    {"id": "geo_1", "input": "What is the capital of Japan?", "expected_substring": "Tokyo"},
    {"id": "geo_2", "input": "What is the capital of France?", "expected_substring": "Paris"},
    {"id": "ground_1", "input": "What is 'flrgglemerk'?",
     "expected_substring": "don't know", "instruction": "If you don't know, say so."},
]


# === Agent under test ===

def agent_answer(question: str, llm: Any = None, instruction: str = "") -> str:
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    system = "Answer concisely (1-2 sentences). " + instruction
    resp = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": question}],
    )
    return require_text(resp.choices[0].message.content, "Agent")


# === Evaluators ===

def eval_substring(output: str, case: dict) -> bool:
    return case["expected_substring"].lower() in output.lower()


def eval_llm_as_judge(output: str, case: dict, judge_llm: Any = None) -> bool:
    """Use an LLM to judge whether output answers the question correctly."""
    judge_llm = judge_llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    prompt = f"""Given a user question and an AI's answer, decide if the answer is correct. Reply with ONLY 'PASS' or 'FAIL'.

Question: {case['input']}
Expected to contain: {case['expected_substring']}
AI Answer: {output}

Verdict:"""
    resp = judge_llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    verdict = require_text(resp.choices[0].message.content, "Judge")
    return parse_verdict(verdict)


# === Eval runner ===

def run_eval(cases: list[dict], agent_fn: Callable, eval_fn: Callable, **agent_kwargs) -> dict:
    results = []
    for case in cases:
        instruction = case.get("instruction", "")
        output = agent_fn(case["input"], instruction=instruction, **agent_kwargs)
        passed = eval_fn(output, case)
        results.append({"id": case["id"], "passed": passed, "output": output[:80]})
    passes = sum(1 for r in results if r["passed"])
    return {"results": results, "pass_count": passes, "total": len(results),
            "pass_rate": passes / len(results)}


if __name__ == "__main__":
    print(f"Running eval on {len(EVAL_CASES)} cases (using {MODEL})...\n")

    print("=== Evaluator: string match ===")
    out = run_eval(EVAL_CASES, agent_answer, eval_substring)
    for r in out["results"]:
        mark = "✅" if r["passed"] else "❌"
        print(f"   {mark} [{r['id']}] {r['output']}")
    print(f"   Pass: {out['pass_count']}/{out['total']} ({out['pass_rate']:.0%})")

    assert out["total"] == 5
    print("\n✅ 練習 2 通過 — 五個案例都完成並產生可比較結果")
    print(f"   觀察：production 應該 pin baseline pass rate、每次 ship 前確認沒 regression")

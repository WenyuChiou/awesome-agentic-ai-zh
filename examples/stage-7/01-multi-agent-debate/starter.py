"""Stage 7 練習 1：Multi-Agent 辯論 — Path A（Ollama）。

2 個 agent 對同一個問題持相反立場辯論、第 3 個 judge agent 評分。
這個小例子只示範角色分工。多看一個觀點不代表答案更正確、bias 更低；
請用固定 eval 驗證，醫療、法律或其他高風險工作仍要由合格的人員審查。

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
from typing import Any

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


def parse_winner(verdict: str) -> tuple[str, str]:
    """Accept only ``WINNER=PRO|CON. reason`` as the Judge contract."""
    match = re.fullmatch(r"WINNER=(PRO|CON)\s*[.:-]\s*(.+)", verdict.strip(), re.IGNORECASE)
    if not match:
        raise ValueError("Judge must reply with WINNER=PRO or WINNER=CON, followed by a reason")
    return match.group(1).upper(), match.group(2).strip()


def llm_call(system: str, user: str, llm: Any = None) -> str:
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    resp = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
    )
    return require_text(resp.choices[0].message.content, "LLM")


def debate(question: str, llm: Any = None) -> dict:
    """3-agent debate：pro / con / judge。"""
    pro_argument = llm_call(
        system="You argue the PRO position on the user's question. Be concise (2-3 sentences).",
        user=question, llm=llm,
    )
    con_argument = llm_call(
        system="You argue the CON position on the user's question. Be concise (2-3 sentences).",
        user=question, llm=llm,
    )
    judge_verdict = llm_call(
        system="You are a neutral judge. Read both arguments below and pick the stronger one. "
               "Reply with: WINNER=PRO or WINNER=CON, then 1-sentence reasoning.",
        user=f"Question: {question}\n\nPRO: {pro_argument}\n\nCON: {con_argument}",
        llm=llm,
    )
    winner, reason = parse_winner(judge_verdict)
    return {
        "question": question,
        "pro": pro_argument,
        "con": con_argument,
        "judge": judge_verdict,
        "winner": winner,
        "reason": reason,
    }


if __name__ == "__main__":
    q = "Should small teams use a framework (LangGraph/CrewAI) or build agents from scratch?"
    print(f"❓ Question: {q}\n")
    result = debate(q)
    print(f"PRO:    {result['pro']}\n")
    print(f"CON:    {result['con']}\n")
    print(f"Judge:  {result['judge']}")
    assert result["winner"] in {"PRO", "CON"}
    assert result["reason"]
    print("\n✅ 練習 1 通過 — 三個角色都回覆，Judge 格式也正確")

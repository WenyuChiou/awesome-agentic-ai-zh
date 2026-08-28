"""Stage 7 練習 1：Multi-Agent 辯論 — Path B（Anthropic Claude）。

這條路只更換模型供應商，不證明 Claude 一定比 Qwen 穩定或正確。
請用同一組固定案例比較兩條路，再由人檢查重要結論。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py
"""

from __future__ import annotations

import os
import re
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")


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


def llm_call_anthropic(system: str, user: str, client: Any = None) -> str:
    client = client or anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL, max_tokens=300, system=system,
        messages=[{"role": "user", "content": user}],
    )
    joined = " ".join(b.text for b in resp.content if b.type == "text")
    return require_text(joined, "Anthropic")


def debate_anthropic(question: str, client: Any = None) -> dict:
    pro = llm_call_anthropic(
        "You argue the PRO position on the user's question. Be concise (2-3 sentences).",
        question, client=client,
    )
    con = llm_call_anthropic(
        "You argue the CON position on the user's question. Be concise (2-3 sentences).",
        question, client=client,
    )
    judge = llm_call_anthropic(
        "You are a neutral judge. Reply with: WINNER=PRO or WINNER=CON, then 1-sentence reasoning.",
        f"Question: {question}\n\nPRO: {pro}\n\nCON: {con}",
        client=client,
    )
    winner, reason = parse_winner(judge)
    return {
        "question": question,
        "pro": pro,
        "con": con,
        "judge": judge,
        "winner": winner,
        "reason": reason,
    }


if __name__ == "__main__":
    q = "Should small teams use a framework or build from scratch?"
    print(f"❓ {q}\n")
    r = debate_anthropic(q)
    for k in ("pro", "con", "judge"):
        print(f"{k.upper()}: {r[k]}\n")
    assert r["winner"] in {"PRO", "CON"}
    assert r["reason"]
    print(f"✅ 練習 1 (Anthropic) 通過 — Claude {MODEL}，三次呼叫都完成")

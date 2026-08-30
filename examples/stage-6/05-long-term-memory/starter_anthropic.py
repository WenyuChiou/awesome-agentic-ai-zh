"""Stage 6 練習 5：Long-term memory — Path B（Anthropic）。

把 generate 改成 Claude；memory store（vector DB）跨 backend 一致。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

from starter import MemoryStore, maybe_remember_fact

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")


def chat_anthropic(user_msg: str, memory: MemoryStore, client: Any = None) -> dict:
    client = client or anthropic.Anthropic()
    memories = memory.recall(user_msg, top_k=3)
    memory_text = "\n".join(f"- {m}" for m in memories) if memories else "(no relevant memories)"

    system = f"""You are a helpful assistant with long-term memory. Use the relevant memories below to personalize answers.

Relevant memories:
{memory_text}
"""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    )
    answer = " ".join(b.text for b in resp.content if b.type == "text")
    return {"answer": answer, "recalled": memories, "user_msg": user_msg}


if __name__ == "__main__":
    memory = MemoryStore()
    maybe_remember_fact("I live in Taipei and I prefer Python over JavaScript.", memory)
    maybe_remember_fact("I work as a data scientist.", memory)

    r = chat_anthropic("Recommend a programming language for me to learn.", memory)
    print(f"recalled: {r['recalled']}")
    print(f"answer: {r['answer']}")
    # === 自我驗證 ===
    assert any("Python" in fact for fact in r["recalled"]), "應找回 Python 偏好"
    assert r["answer"], "Claude 應回傳文字答案"
    print(f"\n✅ 練習 5 (Anthropic path) 通過 — Claude {MODEL}")

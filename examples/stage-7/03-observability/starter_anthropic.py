"""Stage 7 練習 3：Observability — Path B（Anthropic usage 欄位）。

這條路記錄供應商回傳的 input_tokens 與 output_tokens，不自行猜 token 數。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py
"""

from __future__ import annotations

import os
import sys
import time
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

from starter import TraceContext, require_text, trace_span

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")


def observable_agent_anthropic(question: str, ctx: TraceContext, client: Any = None) -> str:
    client = client or anthropic.Anthropic()
    with trace_span(ctx, "llm_call", model=MODEL):
        resp = client.messages.create(
            model=MODEL, max_tokens=300,
            messages=[{"role": "user", "content": question}],
        )
        joined = " ".join(b.text for b in resp.content if b.type == "text")
        answer = require_text(joined, "Anthropic")
        ctx.add_tokens(input_t=resp.usage.input_tokens, output_t=resp.usage.output_tokens)
    return answer


if __name__ == "__main__":
    ctx = TraceContext(request_id=f"req_{int(time.time()*1000)}")
    answer = observable_agent_anthropic("What's 2+2?", ctx)
    print(f"answer: {answer}")
    print(f"trace: {ctx.summary()}")
    print(f"\n✅ 練習 3 (Anthropic) 通過 — {MODEL} 回傳的 usage 已寫入 trace")

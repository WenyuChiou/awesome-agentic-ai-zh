"""Stage 7 練習 4：SDK 進階 — Path B（Anthropic streaming + prompt caching）。

這份小程式示範兩個 SDK 功能：
1. **Streaming**：答案還在生成時，先顯示已到達的文字。
2. **Prompt caching**：標記可重用的長前綴，再讀 usage 判斷是否建立或命中 cache。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py
"""

from __future__ import annotations

import os
import sys
import time
from typing import Any, Iterator

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")
CACHE_MINIMUM_TOKENS = 4096
CACHE_DEMO_REPEAT = 1200


def require_text(value: str | None, label: str) -> str:
    """Reject a provider response that contains no usable text."""
    text = (value or "").strip()
    if not text:
        raise ValueError(f"{label} returned empty text")
    return text


def build_cache_demo_prompt() -> str:
    """Build a long, repeated prefix deliberately above Haiku 4.5's cache minimum."""
    rule = "Reference rule: verify every claim against the supplied source. "
    return "You answer only from these reference rules.\n" + (rule * CACHE_DEMO_REPEAT)


def stream_anthropic(prompt: str, client: Any = None) -> Iterator[str]:
    client = client or anthropic.Anthropic()
    saw_non_whitespace = False
    with client.messages.stream(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            if text:
                if text.strip():
                    saw_non_whitespace = True
                yield text
    if not saw_non_whitespace:
        raise ValueError("Anthropic stream returned empty text")


def cached_query(question: str, large_system_prompt: str, client: Any = None) -> dict:
    """Send a cacheable prefix and return the provider's observed usage fields."""
    client = client or anthropic.Anthropic()

    resp = client.messages.create(
        model=MODEL,
        max_tokens=200,
        system=[
            {
                "type": "text",
                "text": large_system_prompt,
                "cache_control": {"type": "ephemeral"},   # ← key
            }
        ],
        messages=[{"role": "user", "content": question}],
    )

    usage = resp.usage
    answer = require_text(" ".join(b.text for b in resp.content if b.type == "text"), "Anthropic")
    return {
        "answer": answer,
        "input_tokens": usage.input_tokens,
        "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", 0),
        "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0),
        "output_tokens": usage.output_tokens,
    }


if __name__ == "__main__":
    # Demo 1: streaming
    print("=== Streaming demo ===")
    print("(token by token...)\n")
    t0 = time.perf_counter()
    for delta in stream_anthropic("Explain Python list comprehension in 3 sentences."):
        print(delta, end="", flush=True)
    print(f"\n[took {time.perf_counter()-t0:.2f}s]\n")

    # Demo 2: use the same long prefix twice, then inspect actual usage.
    print("=== Prompt caching demo ===")
    big_system = build_cache_demo_prompt()
    print(f"The demo prefix uses {len(big_system.split())} words; documented minimum is {CACHE_MINIMUM_TOKENS} tokens.")
    r1 = cached_query("What's 2+2?", big_system)
    print(f"Call 1: input={r1['input_tokens']}, cache_create={r1['cache_creation_input_tokens']}, cache_read={r1['cache_read_input_tokens']}")
    r2 = cached_query("What's 3+3?", big_system)
    print(f"Call 2: input={r2['input_tokens']}, cache_create={r2['cache_creation_input_tokens']}, cache_read={r2['cache_read_input_tokens']}")

    if r2["cache_read_input_tokens"] > 0:
        print("\n✅ Provider usage shows a cache read on the second call.")
    elif r1["cache_creation_input_tokens"] > 0:
        print("\nℹ️ Provider usage shows cache creation, but not a second-call cache read.")
    else:
        print("\nℹ️ Provider usage did not report cache creation or a cache read.")
    print(f"\n✅ 練習 4 (Anthropic) 通過 — streaming + usage inspection、Claude {MODEL}")

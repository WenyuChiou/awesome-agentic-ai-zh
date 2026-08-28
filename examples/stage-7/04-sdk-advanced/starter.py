"""Stage 7 練習 4：SDK 進階 — Path A（Ollama streaming）。

Production agent 兩個必備 SDK 進階 feature：
1. **Streaming**：答案還在生成時，就把已到達的文字先顯示給使用者。
2. **Prompt caching**：重用相同長前綴；實際是否命中要看供應商回傳的 usage。

跑法：
    pip install -r requirements.txt
    ollama pull qwen3.5:4b
    ollama serve
    python starter.py
"""

from __future__ import annotations

import os
import sys
import time
from typing import Any, Iterator

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


def stream_response(prompt: str, llm: Any = None) -> Iterator[str]:
    """Yield each token chunk as it arrives."""
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    stream = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    saw_non_whitespace = False
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            if delta.strip():
                saw_non_whitespace = True
            yield delta
    if not saw_non_whitespace:
        raise ValueError("Ollama stream returned empty text")


def stream_to_string(prompt: str, llm: Any = None) -> dict:
    """Helper：consume streaming generator + 統計 latency。"""
    t0 = time.perf_counter()
    first_token_at = None
    chunks = []
    for delta in stream_response(prompt, llm=llm):
        if first_token_at is None and delta.strip():
            first_token_at = time.perf_counter() - t0
        chunks.append(delta)
    total_latency = time.perf_counter() - t0
    text = require_text("".join(chunks), "Ollama stream")
    return {
        "text": text,
        "first_token_ms": (first_token_at or 0) * 1000,
        "total_latency_ms": total_latency * 1000,
        "chunk_count": len(chunks),
    }


if __name__ == "__main__":
    prompt = "Explain what a Python list comprehension is in 3 sentences."
    print(f"❓ {prompt}\n")
    print("(streaming token by token...)\n")

    t0 = time.perf_counter()
    for delta in stream_response(prompt):
        print(delta, end="", flush=True)
    total = time.perf_counter() - t0

    print(f"\n\n📊 Total: {total:.2f}s")
    print("✅ 練習 4 通過 — streaming SDK 能逐段顯示答案")
    print("   請在自己的電腦量 first-token 與 total latency；速度會隨模型和硬體改變")

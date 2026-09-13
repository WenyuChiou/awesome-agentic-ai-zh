"""Stage 7 Eval example — Path A (Ollama)."""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

from eval_core import require_text, run_cli


MODEL = os.environ.get("MODEL", "qwen3.5:4b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")


def agent_answer(question: str, llm: Any = None) -> str:
    """Ask the local model one case and reject an empty response."""
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    response = llm.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Answer concisely. Follow the user's format exactly.",
            },
            {"role": "user", "content": question},
        ],
    )
    return require_text(response.choices[0].message.content, "Agent")


def judge_answer(output: str, case: dict[str, Any], llm: Any = None) -> str:
    """Ask the same provider for a strict PASS or FAIL when requested."""
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    prompt = (
        "Evaluate the answer using only the supplied criterion. "
        "Reply with exactly PASS or FAIL.\n\n"
        f"Question: {case['input']}\n"
        f"Success criteria: {'; '.join(case['success_criteria'])}\n"
        f"Judge rubric: {case['grader']['value']}\n"
        f"Answer: {output}"
    )
    response = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return require_text(response.choices[0].message.content, "Judge")


# === 自我驗證 ===
assert MODEL.strip(), "MODEL must not be empty"
assert OLLAMA_BASE.startswith(("http://", "https://")), (
    "OLLAMA_API_BASE must be HTTP(S)"
)


if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            agent_answer,
            model=MODEL,
            provider="ollama",
            judge_fn=judge_answer,
        )
    )

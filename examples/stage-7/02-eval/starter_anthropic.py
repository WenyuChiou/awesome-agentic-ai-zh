"""Stage 7 Eval example — Path B (Anthropic)."""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from eval_core import require_text, run_cli


MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")


def new_anthropic_client() -> Any:
    """Load the optional Anthropic client only when the example runs."""
    try:
        import anthropic
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing optional package 'anthropic'. Run: pip install anthropic"
        ) from exc
    return anthropic.Anthropic()


def agent_answer_anthropic(question: str, client: Any = None) -> str:
    """Ask Claude one case and reject an empty response."""
    client = client or new_anthropic_client()
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        system="Answer concisely. Follow the user's format exactly.",
        messages=[{"role": "user", "content": question}],
    )
    joined = " ".join(block.text for block in response.content if block.type == "text")
    return require_text(joined, "Anthropic agent")


def judge_answer_anthropic(
    output: str, case: dict[str, Any], client: Any = None
) -> str:
    """Ask Claude for a strict PASS or FAIL when a case requests it."""
    client = client or new_anthropic_client()
    prompt = (
        "Evaluate the answer using only the supplied criterion. "
        "Reply with exactly PASS or FAIL.\n\n"
        f"Question: {case['input']}\n"
        f"Success criteria: {'; '.join(case['success_criteria'])}\n"
        f"Judge rubric: {case['grader']['value']}\n"
        f"Answer: {output}"
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}],
    )
    joined = " ".join(block.text for block in response.content if block.type == "text")
    return require_text(joined, "Anthropic Judge")


# === 自我驗證 ===
assert MODEL.strip(), "MODEL must not be empty"
assert callable(agent_answer_anthropic), "Anthropic adapter must be callable"


if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            agent_answer_anthropic,
            model=MODEL,
            provider="anthropic",
            judge_fn=judge_answer_anthropic,
        )
    )

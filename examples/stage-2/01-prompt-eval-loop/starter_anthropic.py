"""Stage 2 Path B: run the same prompt-eval loop with Anthropic."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import (
    CASES,
    EvalReport,
    build_prompt,
    evaluate,
    print_report,
    run_fixture,
)

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5")


def classify_anthropic(message: str, improved: bool, client: Any = None) -> str:
    if client is None:
        from anthropic import Anthropic

        client = Anthropic()
    reply = client.messages.create(
        model=MODEL,
        max_tokens=10,
        temperature=0,
        messages=[{"role": "user", "content": build_prompt(message, improved)}],
    )
    return "".join(block.text for block in reply.content if block.type == "text")


def run_live() -> tuple[EvalReport, EvalReport]:
    from anthropic import Anthropic

    client = Anthropic()
    before = evaluate(lambda message: classify_anthropic(message, False, client))
    after = evaluate(lambda message: classify_anthropic(message, True, client))
    return before, after


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Anthropic prompt-eval path.")
    parser.add_argument(
        "--live",
        action="store_true",
        help="call Anthropic; otherwise use the free deterministic fixture",
    )
    args = parser.parse_args()
    before_report, after_report = run_live() if args.live else run_fixture()
    print_report("Before: four-part prompt", before_report)
    print_report("After: same prompt plus three examples", after_report)
    print("\nDone: same six cases, one prompt change, two visible scores.")

    # === 自我驗證 ===
    assert len(before_report.rows) == len(after_report.rows) == len(CASES)
    assert [row.message for row in before_report.rows] == [row.message for row in after_report.rows]
    assert args.live or (before_report.score, after_report.score) == (3, 6)

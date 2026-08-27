"""Stage 2: compare two prompts on the same six support messages."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MODEL = os.environ.get("OLLAMA_MODEL", "gemma4:e4b")
LABELS = frozenset({"billing", "bug", "other"})


@dataclass(frozen=True)
class Case:
    message: str
    expected: str


@dataclass(frozen=True)
class EvalRow:
    message: str
    expected: str
    actual: str
    passed: bool


@dataclass(frozen=True)
class EvalReport:
    score: int
    rows: tuple[EvalRow, ...]


CASES = (
    Case("我被扣款兩次", "billing"),
    Case("發票上的金額不對", "billing"),
    Case("按下登入後畫面全白", "bug"),
    Case("更新後一直閃退", "bug"),
    Case("你們週末有上班嗎", "other"),
    Case("謝謝你幫我處理", "other"),
)

BASELINE_FIXTURE = {
    CASES[0].message: "billing",
    CASES[1].message: "other",
    CASES[2].message: "bug",
    CASES[3].message: "other",
    CASES[4].message: "other",
    CASES[5].message: "billing",
}
IMPROVED_FIXTURE = {case.message: case.expected for case in CASES}

EXAMPLES = """例子：
輸入：信用卡又扣了一次
輸出：billing
輸入：送出表單後沒有反應
輸出：bug
輸入：可以更改聯絡信箱嗎
輸出：other
"""


def build_prompt(message: str, improved: bool) -> str:
    """Build one prompt. The improved version changes only by adding examples."""
    example_block = f"{EXAMPLES}\n" if improved else ""
    return (
        "目標：把客服留言分到 billing、bug 或 other。\n"
        f"{example_block}"
        f"資料：<input_data>{message}</input_data>\n"
        "規則：只根據資料分類；不知道時選 other。\n"
        "輸出：只回一個小寫標籤。"
    )


def normalize_label(text: str) -> str | None:
    """Accept one legal label; extra explanation counts as an invalid answer."""
    value = text.strip().lower().strip("`.,:;。")
    return value if value in LABELS else None


def evaluate(labeler: Callable[[str], str]) -> EvalReport:
    rows = []
    for case in CASES:
        actual = normalize_label(labeler(case.message))
        shown = actual or "<invalid>"
        rows.append(EvalRow(case.message, case.expected, shown, actual == case.expected))
    return EvalReport(sum(row.passed for row in rows), tuple(rows))


def fixture_labeler(answers: Mapping[str, str]) -> Callable[[str], str]:
    return lambda message: answers[message]


def classify_ollama(message: str, improved: bool, client: Any = None) -> str:
    if client is None:
        from openai import OpenAI

        client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    reply = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": build_prompt(message, improved)}],
        temperature=0,
        max_tokens=10,
    )
    return reply.choices[0].message.content or ""


def print_report(title: str, report: EvalReport) -> None:
    print(f"\n{title}")
    for row in report.rows:
        mark = "PASS" if row.passed else "MISS"
        print(f"  {mark:4}  {row.message} -> {row.actual} (answer: {row.expected})")
    print(f"  score: {report.score}/{len(report.rows)}")


def run_fixture() -> tuple[EvalReport, EvalReport]:
    before = evaluate(fixture_labeler(BASELINE_FIXTURE))
    after = evaluate(fixture_labeler(IMPROVED_FIXTURE))
    return before, after


def run_live() -> tuple[EvalReport, EvalReport]:
    from openai import OpenAI

    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    before = evaluate(lambda message: classify_ollama(message, False, client))
    after = evaluate(lambda message: classify_ollama(message, True, client))
    return before, after


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run one tiny prompt-eval loop.")
    parser.add_argument("--live", action="store_true",
                        help="call local Ollama; otherwise use the free deterministic fixture")
    args = parser.parse_args()
    before_report, after_report = run_live() if args.live else run_fixture()
    print_report("Before: four-part prompt", before_report)
    print_report("After: same prompt plus three examples", after_report)
    print("\nDone: same six cases, one prompt change, two visible scores.")

    # === 自我驗證 ===
    assert len(before_report.rows) == len(after_report.rows) == len(CASES)
    assert [row.message for row in before_report.rows] == [row.message for row in after_report.rows]
    assert args.live or (before_report.score, after_report.score) == (3, 6)

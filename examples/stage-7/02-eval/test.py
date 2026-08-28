"""Stage 7 練習 2 自我驗證 — eval pipeline + 兩種 evaluator。"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import EVAL_CASES, eval_llm_as_judge, eval_substring, parse_verdict, run_eval


def test_eval_substring_pass():
    case = {"id": "x", "input": "?", "expected_substring": "Tokyo"}
    assert eval_substring("The capital is Tokyo.", case) is True
    print("✅ test_eval_substring_pass")


def test_eval_substring_fail():
    case = {"id": "x", "input": "?", "expected_substring": "Tokyo"}
    assert eval_substring("The capital is Beijing.", case) is False
    print("✅ test_eval_substring_fail")


def test_eval_substring_case_insensitive():
    case = {"id": "x", "input": "?", "expected_substring": "tokyo"}
    assert eval_substring("The capital is TOKYO.", case) is True
    print("✅ test_eval_substring_case_insensitive")


def test_eval_llm_as_judge_pass():
    """Mock judge replies PASS。"""
    judge = MagicMock()
    judge.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="PASS"))]
    )
    case = {"id": "x", "input": "What's the capital?", "expected_substring": "Tokyo"}
    assert eval_llm_as_judge("Tokyo!", case, judge_llm=judge) is True
    print("✅ test_eval_llm_as_judge_pass")


def test_eval_llm_as_judge_fail():
    judge = MagicMock()
    judge.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="FAIL"))]
    )
    case = {"id": "x", "input": "?", "expected_substring": "Tokyo"}
    assert eval_llm_as_judge("Beijing", case, judge_llm=judge) is False
    print("✅ test_eval_llm_as_judge_fail")


def test_judge_parser_rejects_extra_or_empty_text():
    assert parse_verdict(" pass ") is True
    assert parse_verdict("FAIL") is False
    for invalid in ("PASS because it looks right", "NOT PASS", "", "PASS\nFAIL"):
        try:
            parse_verdict(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid verdict accepted: {invalid!r}")
    print("✅ test_judge_parser_rejects_extra_or_empty_text")


def test_run_eval_aggregates_correctly():
    """Mock agent 答對 4/5、ground_1（fake word）故意 hallucinate fail、驗 aggregation。"""
    def fake_agent(question, instruction="", **kw):
        if "2 + 2" in question:
            return "The answer is 4."
        if "10 * 5" in question:
            return "50"
        if "Japan" in question:
            return "Tokyo"
        if "France" in question:
            return "Paris"
        # ground_1: fake agent hallucinates instead of saying "don't know" — fail
        return "I made something up"

    out = run_eval(EVAL_CASES, fake_agent, eval_substring)
    assert out["total"] == 5
    assert out["pass_count"] == 4, f"預期 4 pass（4 個有 substring）+ 1 fail（ground_1）、得到 {out['pass_count']}"
    failed = [r for r in out["results"] if not r["passed"]]
    assert len(failed) == 1 and failed[0]["id"] == "ground_1"
    print("✅ test_run_eval_aggregates_correctly")


def test_eval_cases_corpus_shape():
    assert len(EVAL_CASES) == 5
    for c in EVAL_CASES:
        assert {"id", "input", "expected_substring"} <= c.keys()
    print("✅ test_eval_cases_corpus_shape")


if __name__ == "__main__":
    test_eval_substring_pass()
    test_eval_substring_fail()
    test_eval_substring_case_insensitive()
    test_eval_llm_as_judge_pass()
    test_eval_llm_as_judge_fail()
    test_judge_parser_rejects_extra_or_empty_text()
    test_run_eval_aggregates_correctly()
    test_eval_cases_corpus_shape()
    print("\n🎉 全部通過 — eval pipeline 邏輯正確")

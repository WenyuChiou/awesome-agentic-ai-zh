"""Path A tests: no Ollama server and no network calls are required."""

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import (
    BASELINE_FIXTURE,
    CASES,
    IMPROVED_FIXTURE,
    build_prompt,
    classify_ollama,
    evaluate,
    fixture_labeler,
    normalize_label,
)


def test_prompt_changes_one_layer() -> None:
    baseline = build_prompt("我被扣款兩次", improved=False)
    improved = build_prompt("我被扣款兩次", improved=True)
    assert "例子" not in baseline
    assert "例子" in improved
    assert "我被扣款兩次" in baseline and "我被扣款兩次" in improved
    print("PASS  prompt keeps the same data and adds examples")


def test_normalize_rejects_extra_words() -> None:
    assert normalize_label(" Billing ") == "billing"
    assert normalize_label("billing because it mentions money") is None
    assert normalize_label("unknown") is None
    print("PASS  only one legal label counts as correct")


def test_fixture_runs_all_six_cases() -> None:
    before = evaluate(fixture_labeler(BASELINE_FIXTURE))
    after = evaluate(fixture_labeler(IMPROVED_FIXTURE))
    assert len(CASES) == len(before.rows) == len(after.rows) == 6
    assert before.score == 3
    assert after.score == 6
    print("PASS  fixture compares the same six cases: 3/6 -> 6/6")


def test_ollama_response_shape() -> None:
    client = MagicMock()
    client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="bug"))]
    )
    actual = classify_ollama("更新後一直閃退", improved=True, client=client)
    assert actual == "bug"
    sent = client.chat.completions.create.call_args.kwargs
    assert sent["model"]
    assert "例子" in sent["messages"][0]["content"]
    print("PASS  Ollama/OpenAI-compatible response is read correctly")


if __name__ == "__main__":
    test_prompt_changes_one_layer()
    test_normalize_rejects_extra_words()
    test_fixture_runs_all_six_cases()
    test_ollama_response_shape()
    print("\n4/4 passed — Path A prompt-eval loop is ready")

"""Offline tests for approval, checkpoint, resume, and idempotency."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

from starter import (
    CANCELLED,
    COMPLETED,
    WAITING,
    StateError,
    resume_workflow,
    start_workflow,
)


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _paths(directory: str) -> tuple[Path, Path]:
    root = Path(directory)
    return root / "state.json", root / "ledger.json"


def test_start_pauses_without_a_side_effect() -> None:
    with tempfile.TemporaryDirectory() as directory:
        state_path, ledger_path = _paths(directory)
        state = start_workflow(state_path, action="publish draft", idempotency_key="task-001")
        assert state["status"] == WAITING
        assert state["approval"] is None
        assert not ledger_path.exists()


def test_rejection_cancels_without_a_side_effect() -> None:
    with tempfile.TemporaryDirectory() as directory:
        state_path, ledger_path = _paths(directory)
        start_workflow(state_path, action="publish draft", idempotency_key="task-002")
        state = resume_workflow(state_path, ledger_path, decision="reject")
        assert state["status"] == CANCELLED
        assert state["approval"] == "rejected"
        assert not ledger_path.exists()


def test_approval_executes_exactly_once() -> None:
    with tempfile.TemporaryDirectory() as directory:
        state_path, ledger_path = _paths(directory)
        start_workflow(state_path, action="publish draft", idempotency_key="task-003")
        first = resume_workflow(state_path, ledger_path, decision="approve")
        second = resume_workflow(state_path, ledger_path, decision="approve")
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        assert first["status"] == COMPLETED
        assert second == first
        assert ledger["executed"] == [
            {"idempotency_key": "task-003", "action": "publish draft"}
        ]


def test_resume_after_ledger_write_does_not_repeat_the_side_effect() -> None:
    with tempfile.TemporaryDirectory() as directory:
        state_path, ledger_path = _paths(directory)
        start_workflow(state_path, action="publish draft", idempotency_key="task-004")
        ledger_path.write_text(
            json.dumps(
                {
                    "executed": [
                        {"idempotency_key": "task-004", "action": "publish draft"}
                    ]
                }
            ),
            encoding="utf-8",
        )
        state = resume_workflow(state_path, ledger_path, decision="approve")
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        assert state["status"] == COMPLETED
        assert len(ledger["executed"]) == 1


def test_recorded_side_effect_wins_over_a_late_reject() -> None:
    with tempfile.TemporaryDirectory() as directory:
        state_path, ledger_path = _paths(directory)
        start_workflow(state_path, action="publish draft", idempotency_key="task-008")
        ledger_path.write_text(
            json.dumps(
                {
                    "executed": [
                        {"idempotency_key": "task-008", "action": "publish draft"}
                    ]
                }
            ),
            encoding="utf-8",
        )
        state = resume_workflow(state_path, ledger_path, decision="reject")
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        assert state["status"] == COMPLETED
        assert state["approval"] == "approved"
        assert len(ledger["executed"]) == 1


def test_completed_checkpoint_requires_a_matching_ledger_record() -> None:
    with tempfile.TemporaryDirectory() as directory:
        state_path, ledger_path = _paths(directory)
        start_workflow(state_path, action="publish draft", idempotency_key="task-009")
        resume_workflow(state_path, ledger_path, decision="approve")
        ledger_path.unlink()
        try:
            resume_workflow(state_path, ledger_path, decision="approve")
        except StateError as error:
            assert "missing its ledger record" in str(error)
        else:
            raise AssertionError("completed state without a ledger record must fail closed")

    with tempfile.TemporaryDirectory() as directory:
        state_path, ledger_path = _paths(directory)
        start_workflow(state_path, action="publish draft", idempotency_key="task-010")
        resume_workflow(state_path, ledger_path, decision="approve")
        ledger_path.write_text(
            json.dumps(
                {
                    "executed": [
                        {"idempotency_key": "task-010", "action": "delete draft"}
                    ]
                }
            ),
            encoding="utf-8",
        )
        try:
            resume_workflow(state_path, ledger_path, decision="approve")
        except StateError as error:
            assert "different action" in str(error)
        else:
            raise AssertionError("completed state with a mismatched ledger must fail closed")


def test_cancelled_checkpoint_rejects_an_existing_ledger_record() -> None:
    with tempfile.TemporaryDirectory() as directory:
        state_path, ledger_path = _paths(directory)
        start_workflow(state_path, action="publish draft", idempotency_key="task-011")
        resume_workflow(state_path, ledger_path, decision="reject")
        ledger_path.write_text(
            json.dumps(
                {
                    "executed": [
                        {"idempotency_key": "task-011", "action": "publish draft"}
                    ]
                }
            ),
            encoding="utf-8",
        )
        try:
            resume_workflow(state_path, ledger_path, decision="reject")
        except StateError as error:
            assert "cancelled checkpoint conflicts" in str(error)
        else:
            raise AssertionError("cancelled state with a ledger record must fail closed")


def test_corrupt_or_mismatched_state_fails_closed() -> None:
    with tempfile.TemporaryDirectory() as directory:
        state_path, ledger_path = _paths(directory)
        state_path.write_text("not-json", encoding="utf-8")
        try:
            resume_workflow(state_path, ledger_path, decision="approve")
        except StateError as error:
            assert "trusted JSON" in str(error)
        else:
            raise AssertionError("corrupt state must fail closed")

    with tempfile.TemporaryDirectory() as directory:
        state_path, _ = _paths(directory)
        start_workflow(state_path, action="publish draft", idempotency_key="task-005")
        try:
            start_workflow(state_path, action="delete draft", idempotency_key="task-005")
        except StateError as error:
            assert "different task" in str(error)
        else:
            raise AssertionError("one key must not be reused for another action")

    with tempfile.TemporaryDirectory() as directory:
        state_path, ledger_path = _paths(directory)
        state = start_workflow(
            state_path,
            action="publish draft",
            idempotency_key="task-006",
        )
        state["approval"] = "approved"
        state_path.write_text(json.dumps(state), encoding="utf-8")
        try:
            resume_workflow(state_path, ledger_path, decision="approve")
        except StateError as error:
            assert "do not agree" in str(error)
        else:
            raise AssertionError("contradictory status and approval must fail closed")

    with tempfile.TemporaryDirectory() as directory:
        state_path, ledger_path = _paths(directory)
        start_workflow(state_path, action="publish draft", idempotency_key="task-007")
        ledger_path.write_text(
            json.dumps(
                {
                    "executed": [
                        {"idempotency_key": "task-007", "action": "publish draft"},
                        {"idempotency_key": "task-007", "action": "publish draft"},
                    ]
                }
            ),
            encoding="utf-8",
        )
        try:
            resume_workflow(state_path, ledger_path, decision="approve")
        except StateError as error:
            assert "duplicate idempotency key" in str(error)
        else:
            raise AssertionError("duplicate ledger keys must fail closed")


if __name__ == "__main__":
    tests = (
        test_start_pauses_without_a_side_effect,
        test_rejection_cancels_without_a_side_effect,
        test_approval_executes_exactly_once,
        test_resume_after_ledger_write_does_not_repeat_the_side_effect,
        test_recorded_side_effect_wins_over_a_late_reject,
        test_completed_checkpoint_requires_a_matching_ledger_record,
        test_cancelled_checkpoint_rejects_an_existing_ledger_record,
        test_corrupt_or_mismatched_state_fails_closed,
    )
    for test in tests:
        test()
        print(f"✅ {test.__name__}")
    print("\n🎉 8/8 passed — paused, approved/rejected, reconciled, and executed at most once")

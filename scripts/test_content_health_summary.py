from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).with_name("content-health-summary.py")
SPEC = importlib.util.spec_from_file_location("content_health_summary", SCRIPT)
ch = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ch)


def test_hard_failure_wins_over_unverified() -> None:
    result = ch.summarize(
        {"failed": 1, "unverified": 2, "new_unverified": 1},
        {"records": {}, "findings": []},
        freshness_exit=0,
        freshness_ran=False,
        mode="weekly",
    )
    assert result["state"] == "hard-failure"
    assert result["hard_failures"] == 1


def test_unverified_is_review_not_broken() -> None:
    result = ch.summarize(
        {"failed": 0, "unverified": 3, "new_unverified": 1},
        {"records": {"x": {"state": "unverified"}}, "findings": []},
        freshness_exit=0,
        freshness_ran=True,
        mode="monthly",
    )
    assert result["state"] == "review"
    assert result["unverified"] == 4


def test_report_names_one_human_decision_boundary() -> None:
    payload = {
        "mode": "weekly",
        "state": "healthy",
        "hard_failures": 0,
        "unverified": 0,
        "new_unverified": 0,
        "repository_warnings": 0,
        "freshness_ran": False,
        "freshness_failed": False,
    }
    text = ch.render(payload)
    assert "不會自動改寫教材" in text
    assert "Maintainer" in text

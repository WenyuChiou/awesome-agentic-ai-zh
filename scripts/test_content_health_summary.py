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


def test_provenance_and_warning_breakdown_preserve_review_state() -> None:
    result = ch.summarize(
        {"failed": 0, "unverified": 8, "new_unverified": 3},
        {"records": {}, "findings": [
            {"severity": "warning", "code": "no-latest-release"},
            {"severity": "warning", "code": "no-latest-release"},
            {"severity": "warning", "code": "no-license-metadata"},
        ]},
        freshness_exit=0, freshness_ran=True, mode="release",
        run_url="https://github.com/example/roadmap/actions/runs/123",
        source_sha="a" * 40,
    )
    assert result["state"] == "review"
    assert result["hard_failures"] == 0
    assert result["unverified"] == 8
    assert result["repository_warnings"] == 3
    assert result["repository_warning_codes"] == {"no-latest-release": 2, "no-license-metadata": 1}
    text = ch.render(result)
    assert result["run_url"] in text
    assert result["source_sha"] in text
    assert "`no-latest-release` 2" in text
    assert "freshness：**通過**" in text


def test_failed_freshness_is_never_rendered_as_passed() -> None:
    for mode, state in (("monthly", "review"), ("release", "hard-failure")):
        result = ch.summarize({}, {}, freshness_exit=1, freshness_ran=True, mode=mode)
        assert result["state"] == state
        assert "freshness：**失敗，需檢查**" in ch.render(result)
        assert "freshness：**通過**" not in ch.render(result)


def test_both_health_workflows_link_exact_checked_out_source() -> None:
    root = SCRIPT.parent.parent
    for name in ("content-health.yml", "release.yml"):
        workflow = (root / ".github/workflows" / name).read_text()
        assert '--run-url "$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"' in workflow
        assert '--source-sha "$(git rev-parse HEAD)"' in workflow

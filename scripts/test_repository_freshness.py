#!/usr/bin/env python3
"""Network-free tests for the repository freshness gate."""

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import repository_freshness as rf

_CHECKER_SPEC = importlib.util.spec_from_file_location(
    "check_repository_freshness",
    Path(__file__).resolve().parent / "check-repository-freshness.py",
)
checker = importlib.util.module_from_spec(_CHECKER_SPEC)
_CHECKER_SPEC.loader.exec_module(checker)

NOW = datetime(2026, 8, 27, tzinfo=timezone.utc)


def verified(**overrides):
    row = {
        "requested": "owner/repo", "state": "verified", "canonical": "owner/repo",
        "redirected": False, "archived": False, "disabled": False,
        "license": "MIT", "pushed_at": "2026-08-01T00:00:00Z",
        "latest_release": {"tag": "v1.0.0", "published_at": "2026-07-01T00:00:00Z"},
    }
    row.update(overrides)
    return row


def occurrence(text="https://github.com/acme/tool"):
    return rf.DiffOccurrence("acme/tool", "stages/02.md", 12, text)


def test_normalize_repo_and_exclusions():
    assert rf.normalize_repo("Foo", "Bar.git") == "Foo/Bar"
    assert rf.normalize_repo("settings", "tokens") is None
    assert rf.normalize_repo("owner", "repo") is None


def test_inventory_can_include_self_repo():
    assert rf.normalize_repo("WenyuChiou", "awesome-agentic-ai-zh") is None
    assert rf.normalize_repo("WenyuChiou", "awesome-agentic-ai-zh", include_self=True)


def test_changed_occurrences_keep_moved_or_reformatted_link():
    diff = (
        "--- a/stages/02.md\n+++ b/stages/02.md\n@@ -1 +1 @@\n"
        "-old https://github.com/acme/tool\n"
        "+recommended https://github.com/acme/tool\n"
    )
    rows = rf.changed_occurrences(diff)
    assert len(rows) == 1 and rows[0].line == 1 and "recommended" in rows[0].text


def test_diff_ignores_non_markdown_files():
    diff = "--- a/x.py\n+++ b/x.py\n@@ -1,0 +1 @@\n+https://github.com/acme/tool\n"
    assert rf.changed_occurrences(diff) == []


def test_missing_is_hard_failure():
    findings = rf.findings_for({"requested": "owner/repo", "state": "missing"}, [occurrence()], NOW)
    assert findings == [{"severity": "error", "code": "missing", "repo": "owner/repo",
                         "message": "repository is missing or not public"}]


def test_rate_limit_is_not_healthy():
    row = {"requested": "owner/repo", "state": "unverified", "error": "HTTP 429"}
    assert rf.findings_for(row, [occurrence()], NOW)[0]["code"] == "unverified"


def test_redirect_is_hard_failure():
    rows = rf.findings_for(verified(redirected=True, canonical="new/repo"), [occurrence()], NOW)
    assert any(item["code"] == "redirected" and item["severity"] == "error" for item in rows)


def test_archived_described_current_is_hard_failure():
    rows = rf.findings_for(verified(archived=True), [occurrence("Current recommended https://github.com/owner/repo")], NOW)
    assert any(item["code"] == "inactive-described-active" for item in rows)


def test_archived_with_history_caveat_is_not_hard_failure():
    rows = rf.findings_for(verified(archived=True), [occurrence("Historical archived example https://github.com/owner/repo")], NOW)
    assert not any(item["severity"] == "error" for item in rows)


def test_license_mismatch_is_hard_failure():
    rows = rf.findings_for(verified(license="Apache-2.0"), [occurrence("MIT · https://github.com/acme/tool")], NOW)
    assert any(item["code"] == "license-mismatch" for item in rows)


def test_no_license_metadata_is_warning():
    rows = rf.findings_for(verified(license="NOASSERTION"), [occurrence()], NOW)
    assert any(item["code"] == "no-license-metadata" and item["severity"] == "warning" for item in rows)


def test_no_release_is_warning_only():
    rows = rf.findings_for(verified(latest_release=None), [occurrence()], NOW)
    assert any(item["code"] == "no-latest-release" for item in rows)
    assert not any(item["severity"] == "error" for item in rows)


def test_old_stable_repo_is_warning_only():
    rows = rf.findings_for(verified(pushed_at="2020-01-01T00:00:00Z"), [occurrence()], NOW)
    assert any(item["code"] == "old-last-push" for item in rows)
    assert not any(item["severity"] == "error" for item in rows)


def test_github_client_404_is_missing():
    client = rf.GitHubClient(token="x")
    with mock.patch.object(client, "_get", return_value=(404, None, "HTTP 404", None)):
        assert client.inspect("owner/repo", "2026-08-27T00:00:00Z")["state"] == "missing"


def test_github_client_release_rate_limit_is_unverified():
    client = rf.GitHubClient(token="x")
    repo = {"full_name": "owner/repo", "license": {"spdx_id": "MIT"}}
    with mock.patch.object(client, "_get", side_effect=[
        (200, repo, None, "Thu, 27 Aug 2026 00:00:00 GMT"),
        (429, None, "HTTP 429", "Thu, 27 Aug 2026 00:00:00 GMT"),
    ]):
        row = client.inspect("owner/repo", "2026-08-27T00:00:00Z")
    assert row["state"] == "unverified" and "release" in row["error"]


def test_github_client_invalid_release_json_is_unverified():
    client = rf.GitHubClient(token="x")
    repo = {"full_name": "owner/repo", "license": {"spdx_id": "MIT"}}
    with mock.patch.object(client, "_get", side_effect=[
        (200, repo, None, "Thu, 27 Aug 2026 00:00:00 GMT"),
        (200, [], None, "Thu, 27 Aug 2026 00:00:00 GMT"),
    ]):
        row = client.inspect("owner/repo", "2026-08-27T00:00:00Z")
    assert row["state"] == "unverified"


def test_official_checked_at_uses_github_date_header():
    client = rf.GitHubClient(token="x")
    with mock.patch.object(client, "_get", return_value=(
        200, {}, None, "Thu, 27 Aug 2026 06:08:18 GMT"
    )):
        assert client.official_checked_at() == "2026-08-27T06:08:18Z"


def test_snapshot_coverage_detects_missing_and_extra():
    inventory = {"a/b": {}}
    snapshot = {"repository_count": 1, "repositories": {"c/d": {}}}
    problems = rf.snapshot_coverage(snapshot, inventory)
    assert any("missing" in item for item in problems)
    assert any("unreferenced" in item for item in problems)


def test_snapshot_coverage_rejects_bad_schema_future_date_and_empty_row():
    inventory = {"a/b": {}}
    snapshot = {
        "schema_version": 999,
        "verified_at": "2999-01-01T00:00:00Z",
        "repository_count": 1,
        "repositories": {"a/b": {}},
    }
    problems = rf.snapshot_coverage(snapshot, inventory)
    assert any("schema_version" in item for item in problems)
    assert any("future" in item for item in problems)
    assert any("identity" in item for item in problems)


def test_snapshot_coverage_compares_reference_metadata_exactly():
    inventory = {"a/b": {"reference_count": 2, "sources": ["one.md", "two.md"]}}
    row = {
        "requested": "a/b", "state": "missing", "checked_at": "2026-08-27T00:00:00Z",
        "api_status": 404, "reference_count": 999, "sources": ["wrong.md"],
    }
    snapshot = {
        "schema_version": 1, "verified_at": "2026-08-27T00:00:00Z",
        "repository_count": 1, "repositories": {"a/b": row},
    }
    problems = rf.snapshot_coverage(snapshot, inventory)
    assert any("reference_count does not match" in item for item in problems)
    assert any("sources do not match" in item for item in problems)


def test_inventory_is_file_stable_not_line_numbered():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "a.md").write_text("x https://github.com/acme/tool\n", encoding="utf-8")
        fake = mock.Mock(returncode=0, stdout=b"a.md\0", stderr=b"")
        with mock.patch.object(rf.subprocess, "run", return_value=fake):
            rows = rf.inventory_markdown(root)
    assert rows["acme/tool"]["sources"] == ["a.md"]
    assert rows["acme/tool"]["reference_count"] == 1
    assert "line" not in rows["acme/tool"]


def test_add_file_context_finds_license_on_nearby_line():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "stage.md").write_text(
            "https://github.com/acme/tool\n\nLicense: Apache-2.0\n", encoding="utf-8"
        )
        rows = rf.add_file_context(root, [rf.DiffOccurrence("acme/tool", "stage.md", 1, "link")])
    assert "Apache-2.0" in rows[0].context


def test_all_occurrences_keeps_caveat_near_its_own_repo():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "stage.md").write_text(
            "https://github.com/acme/tool\nHistorical archived example\n", encoding="utf-8"
        )
        fake = mock.Mock(returncode=0, stdout=b"stage.md\0", stderr=b"")
        with mock.patch.object(rf.subprocess, "run", return_value=fake):
            rows = rf.all_occurrences(root)
    assert rf.ARCHIVE_CAVEAT_RE.search(rows["acme/tool"][0].context)


def test_context_stops_before_next_repository_row():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "stage.md").write_text(
            "| [A](https://github.com/acme/tool) | MIT |\n"
            "| [B](https://github.com/other/project) | Apache-2.0 |\n",
            encoding="utf-8",
        )
        fake = mock.Mock(returncode=0, stdout=b"stage.md\0", stderr=b"")
        with mock.patch.object(rf.subprocess, "run", return_value=fake):
            rows = rf.all_occurrences(root)
    assert "Apache-2.0" not in rows["acme/tool"][0].context
    assert "MIT" not in rows["other/project"][0].context


def test_heading_context_does_not_read_previous_entry_license():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "stage.md").write_text(
            "### [First](https://github.com/first/project)\n| License | MIT |\n\n"
            "### [Tool](https://github.com/acme/tool)\n| License | Apache-2.0 |\n",
            encoding="utf-8",
        )
        fake = mock.Mock(returncode=0, stdout=b"stage.md\0", stderr=b"")
        with mock.patch.object(rf.subprocess, "run", return_value=fake):
            rows = rf.all_occurrences(root)
    context = rows["acme/tool"][0].context
    assert "Apache-2.0" in context and "MIT" not in context


def test_license_only_edit_selects_owning_repo_entry():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "stage.md").write_text(
            "### [Tool](https://github.com/acme/tool)\n| License | Apache-2.0 |\n",
            encoding="utf-8",
        )
        diff = (
            "--- a/stage.md\n+++ b/stage.md\n@@ -2 +2 @@\n"
            "-| License | MIT |\n+| License | Apache-2.0 |\n"
        )
        rows = rf.changed_entry_occurrences(root, diff)
    assert len(rows) == 1 and rows[0].repo == "acme/tool"
    findings = rf.findings_for(verified(license="MIT"), rows, NOW)
    assert any(item["code"] == "license-mismatch" for item in findings)


def test_license_edit_nine_lines_below_url_is_still_inspected():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        filler = "\n".join(f"note {number}" for number in range(1, 9))
        (root / "stage.md").write_text(
            f"### [Tool](https://github.com/acme/tool)\n{filler}\n| License | Apache-2.0 |\n",
            encoding="utf-8",
        )
        diff = (
            "--- a/stage.md\n+++ b/stage.md\n@@ -10 +10 @@\n"
            "-| License | MIT |\n+| License | Apache-2.0 |\n"
        )
        rows = rf.changed_entry_occurrences(root, diff)
    assert "Apache-2.0" in rows[0].context
    findings = rf.findings_for(verified(license="MIT"), rows, NOW)
    assert any(item["code"] == "license-mismatch" for item in findings)


def test_replacing_a_repo_link_does_not_audit_the_removed_repo():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "stage.md").write_text(
            "[New](https://github.com/newco/project)\n", encoding="utf-8"
        )
        diff = (
            "--- a/stage.md\n+++ b/stage.md\n@@ -1 +1 @@\n"
            "-[Old](https://github.com/oldco/project)\n"
            "+[New](https://github.com/newco/project)\n"
        )
        rows = rf.changed_entry_occurrences(root, diff)
    assert [item.repo for item in rows] == ["newco/project"]


def test_caveat_only_deletion_selects_owning_repo_entry():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "stage.md").write_text(
            "### [Tool](https://github.com/acme/tool)\nRecommended for current projects.\n",
            encoding="utf-8",
        )
        diff = (
            "--- a/stage.md\n+++ b/stage.md\n@@ -2,2 +2 @@\n"
            "-Archived historical example.\n Recommended for current projects.\n"
        )
        rows = rf.changed_entry_occurrences(root, diff)
    findings = rf.findings_for(verified(archived=True), rows, NOW)
    assert any(item["code"] == "inactive-described-active" for item in findings)


def test_workflow_runs_read_only_changed_gate_for_forks():
    workflow = (Path(__file__).resolve().parent.parent / ".github" / "workflows" /
                "repository-freshness.yml").read_text(encoding="utf-8")
    changed_job = workflow.split("  changed-links:", 1)[1].split("  full-inventory:", 1)[0]
    assert "permissions:\n      contents: read" in changed_job
    assert "head.repo.full_name" not in changed_job
    assert "pull_request_target" not in workflow
    full_job = workflow.split("  full-inventory:", 1)[1]
    assert full_job.count("if: always()") >= 2
    assert "scan did not produce an inventory" in full_job


def test_unverified_scan_artifact_does_not_replace_verified_baseline():
    with TemporaryDirectory() as tmp:
        folder = Path(tmp)
        scan = folder / "scan.json"
        baseline = folder / "baseline.json"
        report = folder / "report.md"
        baseline.write_text('{"keep":true}\n', encoding="utf-8")
        client = mock.Mock()
        client.official_checked_at.return_value = "2026-08-27T06:08:18Z"
        inventory = {"acme/tool": {
            "requested": "acme/tool", "reference_count": 1, "sources": ["stage.md"],
        }}
        records = {"acme/tool": {
            "requested": "acme/tool", "state": "unverified",
            "checked_at": "2026-08-27T06:08:18Z", "api_status": 429,
            "error": "HTTP 429; rate limited",
        }}
        with mock.patch.object(checker, "inventory_markdown", return_value=inventory), \
             mock.patch.object(checker, "GitHubClient", return_value=client), \
             mock.patch.object(checker, "inspect_many", return_value=records), \
             mock.patch.object(checker, "all_occurrences", return_value={}):
            code = checker.main([
                "full", "--output-snapshot", str(scan),
                "--update-baseline", str(baseline), "--report", str(report),
            ])
        data = json.loads(scan.read_text(encoding="utf-8"))
        baseline_text = baseline.read_text(encoding="utf-8")
    assert code == 1 and data["repositories"]["acme/tool"]["state"] == "unverified"
    assert baseline_text == '{"keep":true}\n'


def test_prose_only_changed_mode_skips_github_api():
    with TemporaryDirectory() as tmp:
        folder = Path(tmp)
        diff = folder / "change.diff"
        diff.write_text(
            "--- a/README.md\n+++ b/README.md\n@@ -1 +1 @@\n-old prose\n+new prose\n",
            encoding="utf-8",
        )
        with mock.patch.object(checker, "inventory_markdown", return_value={}), \
             mock.patch.object(checker, "changed_entry_occurrences", return_value=[]), \
             mock.patch.object(checker, "GitHubClient", side_effect=AssertionError("API must not run")):
            code = checker.main(["changed", "--base", "base", "--diff-file", str(diff)])
    assert code == 0


def test_two_repos_on_one_prose_line_do_not_share_license():
    row = rf.DiffOccurrence(
        "acme/tool", "CHANGELOG.md", 1,
        "[A](https://github.com/acme/tool) and [B](https://github.com/other/project) Apache-2.0",
    )
    assert not any(item["code"] == "license-mismatch" for item in
                   rf.findings_for(verified(license="MIT"), [row], NOW))


def test_heading_entry_can_read_its_license_field():
    row = rf.DiffOccurrence(
        "acme/tool", "resource.md", 1, "### [Tool](https://github.com/acme/tool)",
        "### [Tool](https://github.com/acme/tool)\n| License | Apache-2.0 |",
    )
    findings = rf.findings_for(verified(license="MIT"), [row], NOW)
    assert any(item["code"] == "license-mismatch" for item in findings)


def _run_all():
    tests = [value for name, value in sorted(globals().items())
             if name.startswith("test_") and callable(value)]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS {test.__name__}")
        except Exception as exc:
            failed += 1
            print(f"  FAIL {test.__name__}: {exc!r}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return failed


if __name__ == "__main__":
    raise SystemExit(1 if _run_all() else 0)

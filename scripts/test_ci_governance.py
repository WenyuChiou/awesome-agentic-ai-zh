from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"


def test_required_gate_is_stable_and_has_no_path_filter() -> None:
    text = (WORKFLOWS / "pr-gate.yml").read_text(encoding="utf-8")
    assert text.startswith("name: Required\n")
    assert "    name: pr-gate" in text
    trigger = text.split("jobs:", 1)[0]
    assert "pull_request:" in trigger
    assert "paths:" not in trigger
    assert "pull_request_target" not in text


def test_required_gate_covers_the_reader_contract() -> None:
    text = (WORKFLOWS / "pr-gate.yml").read_text(encoding="utf-8")
    required = (
        "git diff --check",
        "check-anchors.py --strict",
        "check-mirror-parity.py",
        "check-locale-links.py",
        "check-hans-chars.py --require-opencc",
        "check-reader-ux.py",
        "check-2026-freshness.py",
        "check-duplicate-repos.py",
        "check-changed-links.py",
        "check-repository-freshness.py changed",
        "python -m pytest scripts -q",
        "python -m mkdocs build",
        "check-image-delivery.py --site _build/site",
    )
    missing = [item for item in required if item not in text]
    assert not missing, f"required gate lost: {missing}"


def test_content_health_never_changes_or_merges_curriculum() -> None:
    text = (WORKFLOWS / "content-health.yml").read_text(encoding="utf-8")
    forbidden = ("refresh-stars.py", "create-pull-request", "gh pr merge", "auto-merge")
    assert not [item for item in forbidden if item in text]
    assert "[automation] Content health needs review" in text
    assert "link-health.json" in text
    assert "repository-health.json" in text
    assert "freshness-health.md" in text
    assert "leaving any existing monthly issue unchanged" in text
    assert "without replacing the issue body or monthly freshness evidence" in text
    weekly_branch = text.split("elif [ -n \"$number\" ]; then", 1)[1].split("else\n            gh issue create", 1)[0]
    assert "gh issue comment" in weekly_branch
    assert weekly_branch.index("gh issue comment") < weekly_branch.index("gh issue edit")


def test_legacy_auto_merge_workflow_is_gone() -> None:
    assert not (WORKFLOWS / "weekly-catalog-refresh.yml").exists()

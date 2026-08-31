from __future__ import annotations

import importlib.util
import json
from pathlib import Path


SCRIPT = Path(__file__).with_name("pr-readiness.py")
SPEC = importlib.util.spec_from_file_location("pr_readiness", SCRIPT)
pr = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(pr)


def test_parse_changed_paths_handles_add_modify_and_delete() -> None:
    diff = """diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -1 +1 @@
-old
+new
diff --git a/stages/01.en.md b/stages/01.en.md
deleted file mode 100644
--- a/stages/01.en.md
+++ /dev/null
"""
    assert pr.changed_paths(diff) == {"README.md", "stages/01.en.md"}


def test_locale_coverage_requires_all_existing_mirrors(tmp_path: Path) -> None:
    for name in ("lesson.md", "lesson.en.md", "lesson.zh-Hans.md"):
        (tmp_path / name).write_text("x", encoding="utf-8")
    changed = {"lesson.md", "lesson.en.md"}
    coverage = pr.locale_coverage(tmp_path, changed)
    assert coverage["state"] == "incomplete"
    assert coverage["missing"] == ["lesson.zh-Hans.md"]


def test_locale_coverage_ignores_non_mirrored_policy_file(tmp_path: Path) -> None:
    (tmp_path / "SECURITY.md").write_text("x", encoding="utf-8")
    assert pr.locale_coverage(tmp_path, {"SECURITY.md"}) == {
        "state": "complete",
        "missing": [],
        "families": [],
    }


def test_locale_coverage_rejects_new_public_page_without_mirrors(tmp_path: Path) -> None:
    page = tmp_path / "stages" / "new.md"
    page.parent.mkdir()
    page.write_text("x", encoding="utf-8")
    coverage = pr.locale_coverage(tmp_path, {"stages/new.md"})
    assert coverage["state"] == "incomplete"
    assert coverage["missing"] == [
        "stages/new.en.md",
        "stages/new.zh-Hans.md",
    ]


def test_locale_coverage_allows_documented_single_locale_design_page(tmp_path: Path) -> None:
    page = tmp_path / "stages" / "DESIGN.md"
    page.parent.mkdir()
    page.write_text("x", encoding="utf-8")
    assert pr.locale_coverage(tmp_path, {"stages/DESIGN.md"}) == {
        "state": "complete",
        "missing": [],
        "families": [],
    }


def test_risk_flags_are_evidence_based() -> None:
    paths = {
        ".github/workflows/release.yml",
        "examples/demo/app.py",
        "stages/01-llm-basics.md",
        "docs/stylesheets/extra.css",
    }
    risks = pr.risk_flags(paths, "+ price and model availability\n")
    assert risks == [
        "general-content",
        "volatile-information",
        "executable-example",
        "security-or-actions",
        "actions-or-release",
        "visual-or-layout",
    ]


def test_report_keeps_maintainer_as_final_decider(tmp_path: Path) -> None:
    payload = {
        "machine_gate": "passed",
        "dependency_review": "unverified",
        "locale_coverage": {"state": "complete", "missing": [], "families": []},
        "risks": ["general-content"],
        "changed_files": ["README.md"],
    }
    report = pr.render_markdown(payload)
    assert "最終評定：等待 Maintainer" in report
    assert "通過" in report
    assert "未驗證" in report

    out = tmp_path / "report.json"
    pr.write_json(out, payload)
    assert json.loads(out.read_text(encoding="utf-8")) == payload

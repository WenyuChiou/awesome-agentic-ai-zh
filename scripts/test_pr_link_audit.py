#!/usr/bin/env python3
"""Regression tests for scripts/pr-link-audit.py.

Pins the diff-parsing (which repos count as "new"), the advisory-flag logic
(archived / no-license / stale), and the Markdown rendering. Pure-stdlib and
network-free — ``audit_repo`` (the only ``gh`` caller) is never invoked; tests
feed fact dicts straight into ``flags_for`` / ``format_report`` and inject a
fixed ``now`` so nothing is time-dependent.

Run:  python scripts/test_pr_link_audit.py     (plain, exit 1 on failure)
      pytest scripts/test_pr_link_audit.py
"""

import importlib.util
import pathlib
from datetime import datetime, timezone
from unittest import mock

_SPEC = importlib.util.spec_from_file_location(
    "pr_link_audit", pathlib.Path(__file__).resolve().parent / "pr-link-audit.py"
)
pla = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(pla)

NOW = datetime(2026, 7, 17, tzinfo=timezone.utc)


# --- extract_new_repos --------------------------------------------------------

def test_added_repo_is_new():
    diff = "+- [cool/tool](https://github.com/cool/tool) — nice\n"
    assert pla.extract_new_repos(diff) == ["cool/tool"]


def test_moved_repo_not_new():
    # Present on both a + and a - line → moved/reformatted, not newly added.
    diff = (
        "-old line https://github.com/moved/repo end\n"
        "+new line https://github.com/moved/repo end\n"
    )
    assert pla.extract_new_repos(diff) == []


def test_case_insensitive_move_detection():
    diff = (
        "-https://github.com/Moved/Repo\n"
        "+https://github.com/moved/repo\n"
    )
    assert pla.extract_new_repos(diff) == []


def test_file_headers_ignored():
    # +++ / --- headers carry no repo even if a path looks URL-ish.
    diff = (
        "+++ b/resources/foo.md\n"
        "--- a/resources/foo.md\n"
        "+add https://github.com/real/repo here\n"
    )
    assert pla.extract_new_repos(diff) == ["real/repo"]


def test_non_repo_owner_excluded():
    diff = "+see https://github.com/settings/tokens and https://github.com/marketplace\n"
    assert pla.extract_new_repos(diff) == []


def test_self_and_placeholder_excluded():
    diff = (
        "+https://github.com/WenyuChiou/awesome-agentic-ai-zh\n"
        "+https://github.com/owner/repo\n"
    )
    assert pla.extract_new_repos(diff) == []


def test_multiple_repos_one_line_deduped_sorted():
    diff = (
        "+a https://github.com/zzz/last and https://github.com/aaa/first\n"
        "+dup https://github.com/aaa/first again\n"
    )
    assert pla.extract_new_repos(diff) == ["aaa/first", "zzz/last"]


def test_dotgit_suffix_normalized():
    diff = "+clone https://github.com/foo/bar.git\n"
    assert pla.extract_new_repos(diff) == ["foo/bar"]


def test_plusplus_content_line_not_mistaken_for_header():
    # A genuine added line whose CONTENT starts with "++" (raw diff line
    # "+++...") must NOT be swallowed as a "+++ b/path" file header.
    diff = "+++x see https://github.com/foo/bar for the ++x idiom\n"
    assert pla.extract_new_repos(diff) == ["foo/bar"]


def test_dashdash_content_line_not_mistaken_for_header():
    # Symmetric to the "+++" case: a REMOVED line whose content starts with
    # "-- " (raw diff line "--- foo ...") must be seen as removed content, not a
    # "--- a/path" header. Here the same repo is removed then re-added = a MOVE,
    # so it must NOT be reported as new.
    diff = (
        "--- foo old line https://github.com/moved/repo end\n"
        "+new line https://github.com/moved/repo end\n"
    )
    assert pla.extract_new_repos(diff) == []


def test_real_git_headers_still_skipped():
    # The a/ , b/ , /dev/null header prefixes must still be skipped so a path
    # that looks URL-ish never counts as a repo.
    diff = (
        "--- a/resources/foo.md\n"
        "+++ b/resources/foo.md\n"
        "+add https://github.com/real/repo here\n"
    )
    assert pla.extract_new_repos(diff) == ["real/repo"]


def test_get_git_diff_decodes_markdown_as_utf8_on_every_platform():
    completed = mock.Mock(
        returncode=0,
        stdout="+++ b/stages/07.md\n@@ -0,0 +1 @@\n+繁體中文\n",
        stderr="",
    )
    with mock.patch.object(pla.subprocess, "run", return_value=completed) as run:
        output = pla.get_git_diff("base", "head")

    assert "繁體中文" in output
    assert run.call_args.kwargs["encoding"] == "utf-8"
    assert run.call_args.kwargs["errors"] == "strict"


# --- audit_repo (gh api boundary, fully mocked — no network) ------------------

def test_audit_repo_success():
    fake = mock.Mock(returncode=0, stdout=(
        '{"stars":123,"archived":false,"license":"MIT",'
        '"pushed":"2026-07-01T00:00:00Z"}'))
    with mock.patch.object(pla.subprocess, "run", return_value=fake):
        r = pla.audit_repo("foo/bar")
    assert r["ok"] and r["stars"] == 123 and r["license"] == "MIT"
    assert r["archived"] is False


def test_audit_repo_not_found():
    fake = mock.Mock(returncode=1, stdout="")
    with mock.patch.object(pla.subprocess, "run", return_value=fake):
        r = pla.audit_repo("foo/bar")
    assert r["ok"] is False and "not found" in r["error"]


def test_audit_repo_bad_json():
    fake = mock.Mock(returncode=0, stdout="not-json{{")
    with mock.patch.object(pla.subprocess, "run", return_value=fake):
        r = pla.audit_repo("foo/bar")
    assert r["ok"] is False


def test_audit_repo_missing_gh_binary():
    # FileNotFoundError (an OSError) is the "gh not installed" case — must be
    # caught, not propagated (would otherwise fail the CI step).
    with mock.patch.object(pla.subprocess, "run",
                           side_effect=FileNotFoundError("gh not found")):
        r = pla.audit_repo("foo/bar")
    assert r["ok"] is False


# --- flags_for ----------------------------------------------------------------

def test_flag_archived():
    r = {"repo": "x/y", "ok": True, "stars": 100, "license": "MIT",
         "archived": True, "pushed": "2026-07-01T00:00:00Z"}
    flags = pla.flags_for(r, NOW)
    assert any("archived" in f for f in flags)


def test_flag_no_license():
    r = {"repo": "x/y", "ok": True, "stars": 100, "license": "none",
         "archived": False, "pushed": "2026-07-01T00:00:00Z"}
    flags = pla.flags_for(r, NOW)
    assert any("no clear license" in f for f in flags)


def test_flag_stale_push():
    r = {"repo": "x/y", "ok": True, "stars": 100, "license": "MIT",
         "archived": False, "pushed": "2024-01-01T00:00:00Z"}  # ~30 months
    flags = pla.flags_for(r, NOW)
    assert any("stale" in f for f in flags)


def test_healthy_repo_no_flags():
    r = {"repo": "x/y", "ok": True, "stars": 5000, "license": "Apache-2.0",
         "archived": False, "pushed": "2026-07-01T00:00:00Z"}
    assert pla.flags_for(r, NOW) == []


def test_recent_push_not_stale():
    # exactly ~5 months old — under the 6-month bar, must NOT flag stale.
    r = {"repo": "x/y", "ok": True, "stars": 5000, "license": "MIT",
         "archived": False, "pushed": "2026-02-17T00:00:00Z"}
    assert not any("stale" in f for f in pla.flags_for(r, NOW))


def test_lookup_failure_flagged():
    r = {"repo": "x/y", "ok": False, "error": "not found / private / renamed"}
    flags = pla.flags_for(r, NOW)
    assert len(flags) == 1 and "verify" in flags[0]


# --- format_report ------------------------------------------------------------

def test_report_has_marker_and_table():
    r = {"repo": "cool/tool", "ok": True, "stars": 12300, "license": "MIT",
         "archived": False, "pushed": "2026-07-01T00:00:00Z"}
    md = pla.format_report([r], NOW)
    assert pla.MARKER in md
    assert "| Repo | ★ Stars | License | Last push | Notes |" in md
    assert "[cool/tool](https://github.com/cool/tool)" in md
    assert "12.3k" in md
    assert "👍" in md  # healthy summary line


def test_report_flagged_summary():
    r = {"repo": "dead/repo", "ok": True, "stars": 40, "license": "none",
         "archived": True, "pushed": "2023-01-01T00:00:00Z"}
    md = pla.format_report([r], NOW)
    assert "已封存" in md          # the flagged-rows guidance block
    assert "archived" in md
    assert "no clear license" in md


def _run_all():
    fns = [v for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"  PASS {fn.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"  FAIL {fn.__name__}: {exc}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"  ERROR {fn.__name__}: {exc!r}")
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    return failed


if __name__ == "__main__":
    import sys
    sys.exit(1 if _run_all() else 0)

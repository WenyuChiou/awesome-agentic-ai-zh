#!/usr/bin/env python3
"""Regression tests for scripts/check-duplicate-repos.py.

The gate exists because on 2026-08-23 `microsoft/agent-framework` was added to
the Stage 4 table as a new project when it had been in that same table since
2026-06-13. Stars, license and push date were all verified; the slug was never
grepped. All six content gates stayed green, because the only gate that counts
catalog entries is scoped to resources/mcp-skills-catalog.* and cannot see a
prose table in a stage.

The gate's first two versions were WRONG in the noisy direction, and that
matters more than it sounds: a check that reports 229 problems gets muted, and
a muted check is worse than no check because it looks like coverage.

  v1: compared per FILE  -> 229 findings. A repo explained in prose and then
      listed in a table below is normal; that is most of the corpus.
  v2: compared per BLOCK but used every link on a line -> 6 findings, all of
      them an entry that cross-references another entry ("see also X").
  v3: per block, FIRST link per line only -> 3 findings, all one book listed
      one row per chapter, which no URL comparison can separate from the real
      defect. Those three are baselined, not engineered around.

These tests pin both directions: the real defect must fail, and each of the
three false-positive shapes must pass.

Run:  python scripts/test_duplicate_repos.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location(
    "check_duplicate_repos", Path(__file__).with_name("check-duplicate-repos.py")
)
dup = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(dup)

G = "https://github.com"


def test_the_defect_this_gate_exists_for_is_caught() -> None:
    """Two table rows listing the same repo root. The 2026-08-23 shape."""
    md = (
        "| 分類 | Project | 備註 |\n"
        "|---|---|---|\n"
        f"| A | [x]({G}/microsoft/agent-framework) | 舊的那列 |\n"
        f"| B | [x]({G}/microsoft/agent-framework) | 以為是新的 |\n"
    )
    found = dup.dupes_in(md)
    assert "microsoft/agent-framework" in found, (
        f"the duplicate row was not detected: {found!r}"
    )


def test_the_same_defect_in_a_list_is_caught() -> None:
    md = (
        f"1. [a]({G}/owner/repo) — first\n"
        f"2. [b]({G}/owner/repo) — same repo again\n"
    )
    assert "owner/repo" in dup.dupes_in(md)


def test_prose_mention_plus_a_listing_is_not_a_duplicate() -> None:
    """v1's failure mode. A stage explains a tool, then lists it; that is the
    point of the document, not a defect."""
    md = (
        f"Some prose about [thing]({G}/owner/repo) and why it matters.\n"
        "\n"
        "| Project | 備註 |\n"
        "|---|---|\n"
        f"| [thing]({G}/owner/repo) | the entry |\n"
    )
    assert dup.dupes_in(md) == {}, "a prose mention was counted as a listing"


def test_a_cross_reference_inside_one_entry_is_not_a_duplicate() -> None:
    """v2's failure mode. Row 1 IS repo-a and merely points at repo-b, whose
    own row follows. Both rows are correct and distinct."""
    md = (
        f"1. [a]({G}/owner/repo-a) — see also [b]({G}/owner/repo-b)\n"
        f"2. [b]({G}/owner/repo-b) — its own entry\n"
    )
    assert dup.dupes_in(md) == {}, (
        "an entry that cross-references another entry was called a duplicate"
    )


def test_monorepo_subdirectories_are_distinct_entries() -> None:
    """Eleven plugins under one repo are eleven entries, not one repeated."""
    md = (
        "| Plugin | 備註 |\n"
        "|---|---|\n"
        f"| [a]({G}/anthropics/claude-plugins-official/tree/main/plugins/a) | x |\n"
        f"| [b]({G}/anthropics/claude-plugins-official/tree/main/plugins/b) | y |\n"
    )
    assert dup.dupes_in(md) == {}, "monorepo subdirectory entries were collapsed"


def test_two_separate_tables_do_not_collide() -> None:
    """Listing a repo in a frameworks table and again in a harness table is
    deliberate; only repetition inside ONE block is a defect."""
    md = (
        "| Project |\n|---|\n" f"| [x]({G}/owner/repo) |\n"
        "\n本段散文把兩張表隔開。\n\n"
        "| Project |\n|---|\n" f"| [x]({G}/owner/repo) |\n"
    )
    assert dup.dupes_in(md) == {}, "two different tables were treated as one block"


def test_code_blocks_are_ignored() -> None:
    md = (
        "```bash\n"
        f"git clone {G}/owner/repo\n"
        f"git clone {G}/owner/repo\n"
        "```\n"
    )
    assert dup.dupes_in(md) == {}, "a shell sample was read as two listings"


def test_baseline_is_exact_and_scoped() -> None:
    """Exact equality, not a membership check. Widening the baseline is how a
    ratchet quietly stops ratcheting, and every key must name a real file."""
    assert dup.BASELINE == {
        "stages/03-tool-use-and-hello-agent.md::datawhalechina/hello-agents",
        "stages/03-tool-use-and-hello-agent.en.md::datawhalechina/hello-agents",
        "stages/03-tool-use-and-hello-agent.zh-Hans.md::datawhalechina/hello-agents",
    }, f"baseline changed: {dup.BASELINE!r}"
    for key in dup.BASELINE:
        rel = key.split("::")[0]
        assert (REPO / rel).exists(), f"baseline names a missing file: {rel}"


def test_repo_is_currently_clean() -> None:
    import subprocess
    r = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "check-duplicate-repos.py"), "--quiet"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    assert r.returncode == 0, f"gate reports duplicates:\n{r.stdout[-1200:]}"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
        except AssertionError as e:
            failed += 1
            print(f"FAIL {name}\n  {e}")
        except BaseException as e:
            failed += 1
            print(f"ERROR {name}: {type(e).__name__}: {e}")
    if failed:
        print(f"\n{failed}/{len(tests)} failed.")
        return 1
    print(f"{len(tests)}/{len(tests)} passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""pr-link-audit.py — advisory audit of NEW GitHub repo links added by a PR.

For every ``github.com/owner/repo`` URL the PR *adds* (present on a ``+`` diff
line, absent from the ``-`` lines — a repo merely moved around is not new), this
queries ``gh api`` and reports stars / license / archived / last-push against
the repo's own inclusion bar (CONTRIBUTING ``§策展標準``):

  * maintained  — a commit within the last 6 months (else flag: needs an
    explicit "stable / no longer maintained" note),
  * clear license — MIT / Apache-2 / BSD / ... (else flag: repo policy avoids
    unlicensed projects),
  * not archived — an archived repo needs a deprecation caveat in the entry.

**Advisory only.** The GitHub Action posts the table as a sticky PR comment and
NEVER fails the build: star counts have no hard numeric bar here (that was a
CLI-guide-specific rule, not repo-wide), and "self-promo without teaching value"
is a human judgment the bot cannot make. The bot surfaces facts; the maintainer
decides. This mirrors the existing ``star-drift`` job's "warn only" philosophy.

**Coverage (v1):** only same-repo (maintainer) branches are audited. Fork PRs —
how most external "add a project" contributions actually arrive — are skipped by
the workflow, because a fork-triggered ``pull_request`` gets a read-only
``GITHUB_TOKEN`` that cannot post a comment (a GitHub platform restriction, not a
config choice). Closing that gap needs the two-workflow ``pull_request`` ->
``workflow_run`` pattern; deferred until fork coverage is actually wanted.

Usage:
    python scripts/pr-link-audit.py --base origin/main --out audit.md
    python scripts/pr-link-audit.py --diff-file some.diff --out audit.md  # offline / tests
    python scripts/pr-link-audit.py --base origin/main                    # md to stdout

With ``--out``, stdout carries a single machine-readable line ``NEW_REPOS=<n>``
so the workflow can skip posting when the PR adds no repos.

Environment: ``gh`` (GitHub CLI) on PATH, authenticated (CI: ``GH_TOKEN`` is set
automatically on ubuntu-latest runners). stdlib-only — no pip deps.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from repository_freshness import (
    GITHUB_RE, NON_REPO_OWNERS, PLACEHOLDER_REPOS, SELF_REPO,
    normalize_repo as _normalize_repo,
)

STALE_DAYS = 183  # ~6 months, matching CONTRIBUTING §策展標準 "最近 6 個月內有 commit"
MARKER = "<!-- pr-link-audit -->"  # sticky-comment anchor used by the workflow
NO_LICENSE = {"", "none", "noassertion", "no-license", None}

# Genuine unified-diff FILE-header line prefixes. `git diff` with default
# prefixes emits "--- a/<path>" / "+++ b/<path>" (and ".../dev/null" for
# adds/deletes). Matching these exact prefixes lets a content line that merely
# starts with "--"/"++" through unharmed on both sides of the diff.
_DIFF_HEADER_PREFIXES = (
    "--- a/", "--- b/", "--- /dev/null",
    "+++ a/", "+++ b/", "+++ /dev/null",
)


def normalize_repo(owner: str, name: str) -> str | None:
    """Normalize an owner/name pair; return None to skip (non-repo / placeholder / self)."""
    return _normalize_repo(owner, name)


def _repos_in_line(line: str) -> set[str]:
    """All normalized repo ids referenced on a single line (may be several)."""
    out: set[str] = set()
    for m in GITHUB_RE.finditer(line):
        repo = normalize_repo(m.group(1), m.group(2))
        if repo is not None:
            out.add(repo)
    return out


def extract_new_repos(diff_text: str) -> list[str]:
    """Repos added by the diff: on a ``+`` line and not on any ``-`` line.

    Operates on a unified diff. ``+++``/``---`` file headers are ignored. A repo
    that appears in both added and removed lines was moved/reformatted, not newly
    introduced, so it is excluded to keep the audit focused on genuinely new
    entries. Comparison is case-insensitive on the repo id.
    """
    added: dict[str, str] = {}   # lowercased id -> canonical id (first seen)
    removed: set[str] = set()
    for line in diff_text.splitlines():
        # Skip only genuine unified-diff FILE headers. `git diff` (our
        # invocation, default prefixes) always emits them as "--- a/<path>",
        # "+++ b/<path>", or ".../dev/null". Matching those exact prefixes —
        # rather than a bare "+++ "/"--- " — means a real CONTENT line whose
        # text starts with "++"/"--" (a "--flag" example, a "-- SQL comment",
        # "++i") is NOT mistaken for a header on EITHER the added or removed
        # side and silently dropped.
        if line.startswith(_DIFF_HEADER_PREFIXES):
            continue
        if line.startswith("+"):
            for repo in _repos_in_line(line[1:]):
                added.setdefault(repo.lower(), repo)
        elif line.startswith("-"):
            for repo in _repos_in_line(line[1:]):
                removed.add(repo.lower())
    new = [canon for low, canon in added.items() if low not in removed]
    return sorted(new, key=str.lower)


def get_git_diff(base: str, head: str) -> str:
    """`git diff --unified=0 base...head -- '*.md'` (three-dot = changes on head)."""
    result = subprocess.run(
        ["git", "diff", "--unified=0", f"{base}...{head}", "--", "*.md"],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git diff failed: {result.stderr.strip()}")
    return result.stdout


def audit_repo(repo: str) -> dict:
    """Query `gh api repos/<repo>`; return a fact dict (``ok=False`` on 404/private)."""
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{repo}", "--jq",
             '{stars:.stargazers_count, archived:.archived, '
             'license:(.license.spdx_id // "none"), pushed:.pushed_at}'],
            capture_output=True, text=True, timeout=20,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        # OSError catches a missing `gh` binary (FileNotFoundError); either way
        # the repo is reported as un-auditable rather than crashing the run.
        return {"repo": repo, "ok": False, "error": str(exc)}
    if result.returncode != 0:
        return {"repo": repo, "ok": False, "error": "not found / private / renamed"}
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"repo": repo, "ok": False, "error": "unparseable gh output"}
    return {
        "repo": repo,
        "ok": True,
        "stars": data.get("stars"),
        "archived": bool(data.get("archived")),
        "license": data.get("license") or "none",
        "pushed": data.get("pushed"),
    }


def _months_since(iso_ts: str, now: datetime) -> float | None:
    if not iso_ts:
        return None
    try:
        dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (now - dt).days / 30.44


def _fmt_stars(n) -> str:
    if not isinstance(n, int):
        return "?"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}m"
    if n >= 1_000:
        return f"{n / 1000:.1f}k".replace(".0k", "k")
    return str(n)


def flags_for(result: dict, now: datetime) -> list[str]:
    """Advisory flags for one audited repo (empty list = clean ✅)."""
    if not result.get("ok"):
        return [f"❓ {result.get('error', 'lookup failed')} — verify the link"]
    flags: list[str] = []
    if result.get("archived"):
        flags.append("❌ archived — needs a deprecation caveat")
    lic = (result.get("license") or "none").strip()
    if lic.lower() in NO_LICENSE:
        # Intentional double-flag: an archived repo often reports NOASSERTION,
        # so it can carry both "archived" and "no clear license". Per
        # CONTRIBUTING §策展標準 NOASSERTION genuinely isn't a clear license, so
        # surfacing both is correct, not a bug.
        flags.append("⚠️ no clear license")
    pushed = result.get("pushed")
    months = _months_since(pushed, now) if pushed else None
    if months is not None and months > (STALE_DAYS / 30.44):
        flags.append(f"⚠️ stale — last push {months:.0f}mo ago")
    return flags


def _push_cell(result: dict, now: datetime) -> str:
    if not result.get("ok"):
        return "—"
    if result.get("archived"):
        return "archived"
    pushed = result.get("pushed")
    if not pushed:
        return "?"
    date = pushed[:10]
    months = _months_since(pushed, now)
    return f"{date} ({months:.0f}mo)" if months is not None else date


def format_report(results: list[dict], now: datetime) -> str:
    """Render the audited repos as a sticky-comment Markdown table."""
    lines = [
        MARKER,
        "### 🔗 New repo links in this PR — automated audit",
        "",
        "_Advisory only (never blocks the PR). Checks CONTRIBUTING "
        "`§策展標準`: maintained within 6 months · clear license · not archived. "
        "Star counts are informational (no hard bar); self-promo / teaching "
        "value is a human call the bot can't make._",
        "",
        "| Repo | ★ Stars | License | Last push | Notes |",
        "|---|---|---|---|---|",
    ]
    any_flag = False
    for r in sorted(results, key=lambda x: x["repo"].lower()):
        repo = r["repo"]
        url = f"https://github.com/{repo}"
        stars = _fmt_stars(r.get("stars")) if r.get("ok") else "—"
        lic = r.get("license", "—") if r.get("ok") else "—"
        flags = flags_for(r, now)
        if flags:
            any_flag = True
        note = " · ".join(flags) if flags else "✅"
        lines.append(
            f"| [{repo}]({url}) | {stars} | {lic} | {_push_cell(r, now)} | {note} |"
        )
    lines.append("")
    if any_flag:
        lines.append(
            "> **For flagged rows:** archived or stale repos need an explicit "
            "「已封存 / no longer maintained」note in the entry; unlicensed repos "
            "are generally declined (CONTRIBUTING `§策展標準`). Please confirm each "
            "flagged repo still earns its slot before merging."
        )
    else:
        lines.append("> All added repos look healthy against the inclusion bar. 👍")
    lines.append("")
    lines.append("<sub>🤖 pr-link-audit — facts only; the maintainer decides.</sub>")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="origin/main",
                        help="base ref for the diff (default origin/main)")
    parser.add_argument("--head", default="HEAD", help="head ref (default HEAD)")
    parser.add_argument("--diff-file", help="read a unified diff from this file "
                        "instead of running git (offline / tests)")
    parser.add_argument("--out", help="write the Markdown report here "
                        "(stdout then carries only NEW_REPOS=<n>)")
    args = parser.parse_args()

    # The report contains non-latin-1 glyphs; make stdout UTF-8 so a local
    # Windows console (cp950/cp1252) can print it. CI writes via --out (already
    # explicit UTF-8), so this only matters for interactive local runs.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    # Advisory-only invariant: ANY failure (git diff error, missing `gh` binary,
    # network/API hiccup, unexpected gh output) must degrade to "post nothing",
    # never a non-zero exit that would fail the PR check.
    try:
        if args.diff_file:
            diff_text = Path(args.diff_file).read_text(encoding="utf-8")
        else:
            diff_text = get_git_diff(args.base, args.head)

        repos = extract_new_repos(diff_text)

        if not repos:
            if args.out:
                print("NEW_REPOS=0")
            else:
                print("No new GitHub repo links added by this PR.")
            return 0

        print(f"Auditing {len(repos)} new repo(s): {', '.join(repos)}", file=sys.stderr)
        now = datetime.now(timezone.utc)
        results = [audit_repo(r) for r in repos]
        report = format_report(results, now)

        if args.out:
            Path(args.out).write_text(report, encoding="utf-8")
            print(f"NEW_REPOS={len(repos)}")
        else:
            print(report)
        return 0
    except Exception as exc:  # noqa: BLE001 — advisory tool must never fail CI
        print(f"pr-link-audit: skipped (non-fatal): {exc!r}", file=sys.stderr)
        if args.out:
            print("NEW_REPOS=0")
        return 0


if __name__ == "__main__":
    sys.exit(main())

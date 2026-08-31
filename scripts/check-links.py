#!/usr/bin/env python3
"""
check-links.py — 掃描所有 markdown 檔案的 URL，回報 4xx / 5xx / timeout。

用法：
    python scripts/check-links.py            # 檢查所有 .md 檔
    python scripts/check-links.py --fast     # 只查 GitHub repos（最容易 404）
    python scripts/check-links.py --quiet    # 只印失敗

環境需求：
    pip install requests
"""

import argparse
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_fences import strip_code_blocks  # noqa: E402
from typing import Iterable, NamedTuple

try:
    import requests
except ImportError:
    print("ERROR: 需要 requests。請先執行：pip install requests", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
MD_GLOB = "**/*.md"
EXCLUDE_DIRS = {".git", ".ai", "node_modules", "_build", ".venv"}

# 抓 markdown link [text](url) 的正則。處理 url 內可能含巢狀 ()。
# 用「至少 1 個非空白非右括號字元，後接任意可選 (...) 對」的策略。
LINK_RE = re.compile(
    r"\[([^\]]+)\]"
    r"\((https?://[^\s()]+(?:\([^\s()]*\))?[^\s)]*)\)"
)
HTML_HREF_RE = re.compile(
    r"<a\b[^>]*?\bhref\s*=\s*([\"'])(https?://[^\"']+)\1",
    re.IGNORECASE,
)
AUTOLINK_RE = re.compile(r"<(https?://[^<>\s]+)>")

TIMEOUT = 15
MAX_WORKERS = 10


def find_md_files(root: Path) -> list[Path]:
    files = []
    for fp in root.glob(MD_GLOB):
        # Relative to `root`, not fp.parts — matching the ABSOLUTE path makes a
        # checkout under an excluded-looking directory (e.g. `.ai/`, `book/`,
        # `.claude/worktrees/`) skip everything and report a silent all-clear.
        # Same bug as the 2026-08-02 check-locale-links.py fix.
        if any(part in EXCLUDE_DIRS for part in fp.relative_to(root).parts):
            continue
        files.append(fp)
    return files


def extract_urls_from_text(text: str, *, source: str = "<memory>") -> list[tuple[int, str]]:
    """Return Markdown, HTML href, and autolink URLs outside fenced code."""
    urls = []
    # Fenced code blanked by the shared parser (md_fences), not a local toggle —
    # see #95/#97. Without this the checker fetches every URL in every code
    # sample, which is both slow and a source of phantom "dead link" reports.
    text = strip_code_blocks(text, source=source)
    for line_no, line in enumerate(text.splitlines(), start=1):
        found: set[str] = set()
        for match in LINK_RE.finditer(line):
            found.add(match.group(2).rstrip(".,;:!?"))
        for match in HTML_HREF_RE.finditer(line):
            found.add(match.group(2).rstrip(".,;:!?"))
        for match in AUTOLINK_RE.finditer(line):
            found.add(match.group(1).rstrip(".,;:!?"))
        urls.extend((line_no, url) for url in sorted(found))
    return urls


def extract_urls(md_path: Path) -> list[tuple[int, str]]:
    """Return [(line_no, url), ...], skipping fenced code blocks."""
    return extract_urls_from_text(
        md_path.read_text(encoding="utf-8"), source=str(md_path)
    )


# A real browser's headers. The old identifying UA
# ("awesome-agentic-ai-zh-link-check/1.0") was refused by several hosts, and the
# report then called those links BROKEN. A checker that is wrong that often stops
# being read, which is worse than not having one — see issue #94, where 3 of 14
# reported failures were nothing but this.
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Statuses a checker CANNOT resolve: the server is answering, it just will not
# answer us. Login walls, bot/geo walls, rate limits. Reported separately and
# NOT counted as failures, because acting on them is impossible and their
# flakiness is what trains people to ignore the whole report — the same three
# URLs returned 200 to a browser one day and 403 the next while triaging #94.
# 451 is a legal/geo block — a refusal like the rest. 429 differs from the
# others in kind: it is TRANSIENT and says nothing about the link at all, only
# about how fast we asked. Both belong here; neither is actionable.
UNVERIFIABLE_STATUSES = {401, 403, 429, 451}

# 404/410 are the ONLY codes that speak about THIS resource. Every other 4xx can
# plausibly be about the host, which is what the root probe below is for — but a
# host-wide 404 must never excuse a page-level 404, or the checker loses the one
# thing it exists to detect.
#
# This is not hypothetical: `langchain-ai.github.io` is a GitHub Pages org site
# with no root page, so its root answers 404. Without this exclusion the probe
# classified both dead LangGraph URLs from issue #94 as "host-level block — do
# not fix", i.e. the gate would have argued against the commit that fixes them,
# and 33 links on that host plus 4 on deepseek-harness.github.io would have gone
# permanently undetectable.
NOT_FOUND_STATUSES = {404, 410}

# URLs that are correctly unreachable and always will be: they need a signed-in
# session. Listing them keeps them out of the report entirely rather than having
# a human re-triage them every run.
LOGIN_GATED = {
    "https://www.zotero.org/settings/keys",  # requires a Zotero account session
}

# Long-standing refusals, recorded so they stay quiet. Without this, "unverifiable
# never fails the run" also means a link that JUST started refusing looks exactly
# like the fourteen that have refused for months — and nobody would ever be
# nudged about it. Same shape as scripts/mirror-parity-baseline.json.
#
# A baseline is a record of what a human already looked at, so it is only ever
# written by an explicit `--update-baseline` run, never silently on a green run.
UNVERIFIABLE_BASELINE = REPO_ROOT / "scripts" / "link-unverifiable-baseline.json"


def load_unverifiable_baseline(path: Path | None = None) -> set[str]:
    """Missing or unreadable file -> empty set: everything is NEW, which is noisy
    but never hides anything. The opposite default would silence the whole check
    the moment the file was deleted.

    The SHAPE is validated, not just the syntax. `json.loads` happily returns a
    list or a null for a hand-edited file, and `data.get` on those raises
    AttributeError — which is neither of the two behaviours above, it just kills
    the whole run. This file is meant to be human-editable, so a bad edit has to
    degrade to noisy, never to a crash and never to silence.
    """
    path = path or UNVERIFIABLE_BASELINE
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        # ValueError, not json.JSONDecodeError. Invalid UTF-8 bytes in the file
        # raise UnicodeDecodeError, which is a sibling ValueError subclass and
        # was NOT caught by the narrower clause — so a file corrupted by encoding
        # rather than by syntax still killed the whole run. Same defect as the
        # shape check below, reached by a different corruption mode.
        return set()
    if not isinstance(data, dict):
        return set()
    urls = data.get("unverifiable")
    if not isinstance(urls, list):
        return set()
    return {u for u in urls if isinstance(u, str)}


def save_unverifiable_baseline(urls: Iterable[str], path: Path | None = None) -> None:
    path = path or UNVERIFIABLE_BASELINE
    payload = {
        "_comment": (
            "URLs whose host answers but refuses this checker (401/403/429/451, "
            "or a host-level block). Not dead links. Regenerate with: "
            "python scripts/check-links.py --update-baseline"
        ),
        "unverifiable": sorted(urls),
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")


# --- Classification -------------------------------------------------------
# The failed/unverifiable split and the exit code used to live inside main(),
# untested, and four mutations survived because of it — including
# `sys.exit(1 if failures else 0)` -> `sys.exit(0)`, which would have made the
# gate permanently green without a single test noticing (issue #102).
#
# So the decision is a pure function over a structured result. main() only
# counts and prints; it makes no judgements of its own.

OK = "ok"
FAILED = "failed"
UNVERIFIABLE = "unverifiable"
SKIPPED = "skipped"


class Probe(NamedTuple):
    """One URL's result. `host_blocked` and `skipped` are FLAGS, not messages to
    re-parse.

    main() used to route on `msg.startswith("host-level block")`. Renaming that
    human-readable string would silently have re-filed every host block as a
    dead link, and the only test that noticed asserted the string rather than
    the behaviour.

    `skipped` exists for the same reason. Both a skip and a connection error have
    `status is None`, and the split used to be `detail.startswith("skipped")` —
    so rewording "skipped (--fast)" would have turned every fast-mode skip into a
    reported dead link. Leaving one string-sniff in place while removing the
    other is not a design, it is a leftover.
    """

    url: str
    status: int | None
    detail: str = ""
    host_blocked: bool = False
    skipped: bool = False
    final_url: str = ""


def classify(probe: Probe) -> str:
    """OK / FAILED / UNVERIFIABLE / SKIPPED — the whole decision, in one place."""
    if probe.skipped:
        return SKIPPED
    if probe.status is None:
        # No HTTP response is evidence about the scanner's reachability, not
        # proof that the page is gone. Keep it visible, but never call it 404.
        return UNVERIFIABLE
    if probe.status in UNVERIFIABLE_STATUSES or probe.host_blocked:
        return UNVERIFIABLE
    if probe.status >= 400:
        return FAILED
    if bad_redirect(probe.url, probe.final_url):
        return FAILED
    return OK


def bad_redirect(original: str, final: str) -> bool:
    """A deep page collapsing to a site root is not a successful page move."""
    if not final or final.rstrip("/") == original.rstrip("/"):
        return False
    source = urlsplit(original)
    target = urlsplit(final)
    source_path = source.path.rstrip("/")
    target_path = target.path.rstrip("/")
    return bool(source_path and source_path != "/" and target_path in ("", "/"))


def probe_label(probe: Probe) -> str:
    """Describe the result with enough redirect evidence to act on it."""
    if bad_redirect(probe.url, probe.final_url):
        return f"HTTP {probe.status} — collapsed to site root: {probe.final_url}"
    if probe.status is None:
        return probe.detail
    return f"HTTP {probe.status}" + (f" — {probe.detail}" if probe.detail else "")


def exit_code(kinds: Iterable[str]) -> int:
    """1 iff something is ACTIONABLE. Refusals and skips never fail the run."""
    return 1 if any(k == FAILED for k in kinds) else 0


# Root probes are memoized per host: N dead links on one blocked host would
# otherwise mean N identical root requests. Short timeout — the probe is
# advisory, and a hanging one must not stall the whole run.
_ROOT_TIMEOUT = 5
_root_cache: dict[str, int | None] = {}
_root_lock = threading.Lock()


def _root_status(root: str) -> int | None:
    with _root_lock:
        if root in _root_cache:
            return _root_cache[root]
    try:
        rr = requests.get(root, timeout=_ROOT_TIMEOUT, allow_redirects=True,
                          stream=True, headers=BROWSER_HEADERS)
        rr.close()
        status = rr.status_code
    except requests.exceptions.RequestException:
        status = None
    with _root_lock:
        _root_cache[root] = status
    return status


ATTEMPTS = 2
RETRY_DELAY = 2


def check_url(url: str, fast_mode: bool = False) -> Probe:
    """回傳 Probe。allow_redirects=True 表示 final_status 不會是 3xx
    （會被 follow 到 2xx 或 4xx/5xx）。"""
    if fast_mode and "github.com" not in url:
        return Probe(url, None, "skipped (--fast)", skipped=True)
    if url in LOGIN_GATED:
        return Probe(url, None, "skipped (login-gated)", skipped=True)

    # A bounded LOOP, deliberately not recursion. The first version of this retry
    # called check_url again; flipping its guard to always-true turned it into an
    # unbounded recursion sleeping RETRY_DELAY per level — a multi-thousand-second
    # hang rather than a red test. A loop cannot express that bug.
    for attempt in range(1, ATTEMPTS + 1):
        try:
            r = requests.head(url, timeout=TIMEOUT, allow_redirects=True,
                              headers=BROWSER_HEADERS)
            # Retry with GET on ANY 4xx. HEAD is widely mis-implemented — measured on
            # this repo's own links, openai.com/chatgpt/desktop answers HEAD 404 and
            # GET 200, and learnshell.org answers HEAD 415 and GET 200. Retrying only
            # on 405/403 (the old behaviour) reported both as dead.
            if 400 <= r.status_code < 500:
                r = requests.get(url, timeout=TIMEOUT, allow_redirects=True, stream=True,
                                 headers=BROWSER_HEADERS)
                r.close()
            status = r.status_code

            # A 4xx that is NOT one of the obvious refusal codes might still be a
            # host-level block rather than a missing page. Ask the host's own root:
            # if that returns the same status, the host is refusing us and says
            # nothing about this URL. Measured case — every Meta domain
            # (ai.meta.com, developer.meta.com, llama.com) answers 400 to a
            # non-browser client, including its own root.
            if (400 <= status < 500
                    and status not in UNVERIFIABLE_STATUSES
                    and status not in NOT_FOUND_STATUSES):
                # Derive the root from the FINAL url, not the requested one. llama.com
                # is itself a root and redirects to developer.meta.com/ai/, so probing
                # its own root proves nothing; probing the root it LANDS on does.
                parts = urlsplit(r.url or url)
                root = f"{parts.scheme}://{parts.netloc}/"
                if root.rstrip("/") != url.rstrip("/"):
                    root_status = _root_status(root)
                    if root_status == status:
                        return Probe(
                            url, status,
                            f"host-level block ({parts.netloc} root returns the same)",
                            host_blocked=True,
                        )

            return Probe(url, status, final_url=r.url or url)
        except requests.exceptions.RequestException as e:
            # One retry before calling a link dead. A single connection blip on
            # one of 700 URLs would otherwise fail the whole run, which is the
            # same "report is wrong, so nobody reads it" problem this file is
            # fixing — observed live while building this: one run exited 1, the
            # next exited 0 with no change to the tree.
            if attempt < ATTEMPTS:
                time.sleep(RETRY_DELAY)
                continue
            return Probe(url, None, str(e)[:80])


def main() -> int:
    # This script prints ✓ / ❌ / ⚠ and CJK paths. A default Windows console is
    # cp950, where the first ✓ raises UnicodeEncodeError and kills the run
    # PART WAY THROUGH — so the summary and the failure list never appear and
    # the output looks like a crash rather than a report. Every other gate in
    # scripts/ already does this; check-links did not.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, ValueError):
                pass

    parser = argparse.ArgumentParser(description="Check markdown links for rot.")
    parser.add_argument("--fast", action="store_true", help="只查 GitHub URL")
    parser.add_argument("--quiet", action="store_true", help="只印失敗")
    parser.add_argument("--update-baseline", action="store_true",
                        help="把目前所有 unverifiable URL 寫進 baseline（人工看過之後才跑）")
    parser.add_argument("--json-report", type=Path,
                        help="write machine-readable results to this path")
    args = parser.parse_args()

    files = find_md_files(REPO_ROOT)
    print(f"Scanning {len(files)} markdown files...", file=sys.stderr)

    # 收集所有 URL（去重，但記下出現位置）
    occurrences: dict[str, list[tuple[Path, int]]] = {}
    for fp in files:
        for line_no, url in extract_urls(fp):
            occurrences.setdefault(url, []).append((fp, line_no))

    print(f"Found {len(occurrences)} unique URLs.", file=sys.stderr)

    buckets: dict[str, list[tuple[str, str]]] = {FAILED: [], UNVERIFIABLE: [], OK: [], SKIPPED: []}

    records: list[dict] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(check_url, url, args.fast): url for url in occurrences}
        for i, fut in enumerate(as_completed(futures), start=1):
            probe = fut.result()
            # main() makes NO judgement of its own — see classify().
            kind = classify(probe)
            label = probe_label(probe)
            buckets[kind].append((probe.url, label))
            records.append({
                "url": probe.url,
                "state": kind,
                "status": probe.status,
                "detail": probe.detail,
                "final_url": probe.final_url,
            })
            if not args.quiet:
                mark = {OK: "✓", FAILED: "❌", UNVERIFIABLE: "⚠", SKIPPED: "-"}[kind]
                suffix = "" if kind == OK else f" — {label}"
                print(f"[{i}/{len(occurrences)}] {mark} {probe.url}{suffix}")

    failures = buckets[FAILED]
    unverifiable = buckets[UNVERIFIABLE]
    skipped = len(buckets[SKIPPED])

    baseline = load_unverifiable_baseline()
    seen_unverifiable = {u for u, _ in unverifiable}
    new_unverifiable = sorted(seen_unverifiable - baseline)
    recovered = sorted(baseline - seen_unverifiable)

    if args.update_baseline:
        save_unverifiable_baseline(seen_unverifiable)
        print(f"Baseline updated: {len(seen_unverifiable)} unverifiable URL(s) recorded.")
        # Deliberately NOT an early return. The first version returned 0 here,
        # which meant `--update-baseline` skipped the failure report entirely and
        # forced the run green even with a dead link in the same scan — the exact
        # "gate goes green and nobody notices" defect this whole file exists to
        # close, reintroduced in the one branch that had no test. Recording a
        # refusal must not change what happens to an unrelated dead link.
        #
        # Nothing is "new" once it has just been recorded, so that section goes
        # quiet; everything below still runs, and there is ONE exit path.
        #
        # `recovered` is deliberately KEPT. save_unverifiable_baseline overwrites
        # rather than merges, so those URLs are being dropped from the baseline by
        # this very run — and the run that drops them is the only one in a
        # position to say so.
        new_unverifiable = []

    # 報告
    print()
    print("=" * 60)
    print(f"Total checked:   {len(occurrences) - skipped}")
    print(f"OK (2xx):        {len(buckets[OK])}")
    print(f"Failed:          {len(failures)}")
    print(f"Unverifiable:    {len(unverifiable)}  (host refuses non-browser clients, or blocks at host level)")
    if new_unverifiable:
        print(f"  └ NEW:          {len(new_unverifiable)}  (not in the baseline — worth a look)")
    if skipped:
        # Printed unconditionally. Under --fast this is the GitHub-only filter;
        # in a full run it is the LOGIN_GATED list, and without this line those
        # URLs just vanish between "Found N" and "Total checked N-1".
        print(f"Skipped:         {skipped}  (--fast filter and/or login-gated)")
    print()

    if failures:
        print("=== Failures by file (ACTIONABLE — the link is dead) ===")
        for url, reason in failures:
            print(f"\n❌ {url}  [{reason}]")
            for fp, line_no in occurrences[url]:
                print(f"   {fp.relative_to(REPO_ROOT)}:{line_no}")

    # NEW unverifiable entries get their own section. Excluding refusals from the
    # exit code is right, but it also means a permanently-403 link is something
    # nobody would ever be nudged about again — the baseline keeps long-standing
    # ones quiet while a newly-appearing one still surfaces.
    if new_unverifiable:
        print()
        print("=== NEW unverifiable (not in the baseline) ===")
        print("Not a failure, but it was verifiable before. Open one in a browser;")
        print("if it is fine, re-run with --update-baseline to record it.")
        for url in new_unverifiable:
            reason = next(r for u, r in unverifiable if u == url)
            print(f"\n⚠ {url}  [{reason}]")
            for fp, line_no in occurrences[url]:
                print(f"   {fp.relative_to(REPO_ROOT)}:{line_no}")

    if recovered:
        print()
        if args.update_baseline:
            # These just got dropped from the file by this run's overwrite.
            print("=== Dropped from the baseline (they verify again) ===")
        else:
            print("=== Baselined URLs that now verify (consider --update-baseline) ===")
        for url in recovered:
            print(f"   {url}")

    # Printed even under --quiet. Every automated invocation passes --quiet, and
    # these are exactly what a human still has to eyeball.
    if unverifiable:
        print()
        print("=== Unverifiable (NOT failures — do not 'fix' these) ===")
        print("The host answered and refused a non-browser client. The page may be")
        print("perfectly fine in a browser; these same URLs have flipped between 200")
        print("and 403 between runs. Open one yourself before touching the link.")
        for url, reason in unverifiable:
            print(f"\n⚠ {url}  [{reason}]")
            for fp, line_no in occurrences[url]:
                print(f"   {fp.relative_to(REPO_ROOT)}:{line_no}")

    if args.json_report:
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "checked": len(occurrences) - skipped,
            "ok": len(buckets[OK]),
            "failed": len(failures),
            "unverified": len(unverifiable),
            "new_unverified": len(new_unverifiable),
            "skipped": skipped,
            "results": sorted(records, key=lambda row: row["url"]),
        }
        args.json_report.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    # Every classification made this run, not a re-derived summary — so a bucket
    # accidentally left out of the report still counts toward the verdict.
    return exit_code(kind for kind, entries in buckets.items() for _ in entries)


if __name__ == "__main__":
    # main() RETURNS the code rather than calling sys.exit itself, so a test can
    # assert on it directly. `sys.exit(1 if failures else 0)` -> `sys.exit(0)`
    # survived mutation testing precisely because nothing could call main()
    # without killing the interpreter (issue #102).
    sys.exit(main())

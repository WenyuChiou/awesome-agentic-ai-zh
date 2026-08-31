#!/usr/bin/env python3
"""Block clearly broken links added by a PR; keep refusals as unverified evidence."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
_LINKS_SPEC = importlib.util.spec_from_file_location(
    "check_links_shared", Path(__file__).with_name("check-links.py")
)
_links = importlib.util.module_from_spec(_LINKS_SPEC)
assert _LINKS_SPEC.loader is not None
_LINKS_SPEC.loader.exec_module(_links)
Probe = _links.Probe


def _run_git(arguments: list[str]) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=90,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(arguments)} failed")
    return result.stdout


def changed_markdown_pairs(
    base: str, head: str,
) -> tuple[str, list[tuple[str | None, str | None]]]:
    """Return the merge base and Markdown paths changed by the PR branch."""
    comparison_base = _run_git(["merge-base", base, head]).strip()
    if not comparison_base:
        raise RuntimeError(f"git merge-base returned no commit for {base} and {head}")
    raw = _run_git([
        "diff", "--name-status", "-z", "--find-renames", f"{comparison_base}..{head}",
        "--", "*.md",
    ])
    tokens = raw.split("\0")
    if tokens and not tokens[-1]:
        tokens.pop()
    pairs: list[tuple[str | None, str | None]] = []
    index = 0
    while index < len(tokens):
        status = tokens[index]
        index += 1
        if status.startswith(("R", "C")):
            if index + 1 >= len(tokens):
                raise RuntimeError("git diff returned an incomplete rename/copy record")
            old_path, new_path = tokens[index], tokens[index + 1]
            index += 2
            pairs.append((old_path, new_path))
        else:
            if index >= len(tokens):
                raise RuntimeError("git diff returned an incomplete path record")
            path = tokens[index]
            index += 1
            pairs.append((path if status != "A" else None, path if status != "D" else None))
    return comparison_base, pairs


def urls_in_text(text: str, *, source: str) -> set[str]:
    return {url for _, url in _links.extract_urls_from_text(text, source=source)}


def extract_new_urls_from_texts(base_text: str, head_text: str) -> set[str]:
    """Compare complete documents so fenced-code context is never lost."""
    return urls_in_text(head_text, source="head") - urls_in_text(base_text, source="base")


def git_file(ref: str, path: str | None) -> str:
    if path is None:
        return ""
    return _run_git(["show", f"{ref}:{path}"])


def new_urls_from_git(base: str, head: str) -> list[str]:
    base_urls: set[str] = set()
    head_urls: set[str] = set()
    comparison_base, pairs = changed_markdown_pairs(base, head)
    for base_path, head_path in pairs:
        if base_path:
            base_urls.update(urls_in_text(
                git_file(comparison_base, base_path),
                source=f"{comparison_base}:{base_path}",
            ))
        if head_path:
            head_urls.update(urls_in_text(git_file(head, head_path), source=f"{head}:{head_path}"))
    return sorted(head_urls - base_urls)


def verdict(probe: Probe) -> str:
    if probe.status is None:
        return "unverified"
    if probe.status in _links.UNVERIFIABLE_STATUSES or probe.host_blocked:
        return "unverified"
    if probe.status >= 400:
        return "failed"
    final = getattr(probe, "final_url", "")
    return "failed" if _links.bad_redirect(probe.url, final) else "passed"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    urls = new_urls_from_git(args.base, args.head)
    rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=min(10, max(1, len(urls)))) as pool:
        futures = {pool.submit(_links.check_url, url): url for url in urls}
        for future in as_completed(futures):
            probe = future.result()
            rows.append({
                "url": probe.url,
                "status": probe.status,
                "state": verdict(probe),
                "detail": probe.detail,
                "final_url": getattr(probe, "final_url", ""),
            })
    rows.sort(key=lambda row: row["url"])
    payload = {
        "checked": len(rows),
        "failed": sum(row["state"] == "failed" for row in rows),
        "unverified": sum(row["state"] == "unverified" for row in rows),
        "links": rows,
    }
    lines = [
        "# Changed-link report", "",
        f"Checked **{payload['checked']}** new link(s); hard failures: **{payload['failed']}**; unverified: **{payload['unverified']}**.", "",
    ]
    for row in rows:
        icon = {"passed": "✅", "failed": "❌", "unverified": "⚠️"}[row["state"]]
        suffix = f" → {row['final_url']}" if row["final_url"] and row["final_url"] != row["url"] else ""
        lines.append(f"- {icon} `{row['url']}`{suffix} ({row['status'] or row['detail'] or 'no response'})")
    report = "\n".join(lines).rstrip() + "\n"
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 1 if payload["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

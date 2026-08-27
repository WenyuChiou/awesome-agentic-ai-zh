#!/usr/bin/env python3
"""Check changed or all GitHub repository links against official GitHub data."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from repository_freshness import (
    GitHubClient, all_occurrences, changed_entry_occurrences, findings_for,
    git_diff, inspect_many, inventory_markdown, make_snapshot, snapshot_coverage,
    stamp_scan_completed_at,
)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SNAPSHOT = ROOT / "scripts" / "repository-freshness-snapshot.json"


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _report(records: dict[str, dict], findings: list[dict], checked_at: str) -> str:
    errors = [f for f in findings if f["severity"] == "error"]
    warnings = [f for f in findings if f["severity"] == "warning"]
    lines = [
        "# Repository freshness report", "", f"Checked: `{checked_at}`", "",
        f"Repositories: **{len(records)}** · errors: **{len(errors)}** · warnings: **{len(warnings)}**",
        "", "Old activity alone is a warning, not a reason to remove a useful stable project.", "",
    ]
    for title, items in (("Errors", errors), ("Review items", warnings)):
        lines.extend([f"## {title}", ""])
        if not items:
            lines.append("None.\n")
            continue
        for item in items:
            where = f" ({item['where']})" if item.get("where") else ""
            lines.append(f"- `{item['repo']}`{where}: {item['message']} (`{item['code']}`)")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    changed = sub.add_parser("changed", help="check repository entries touched by Markdown edits")
    changed.add_argument("--base", required=True)
    changed.add_argument("--head", default="HEAD")
    changed.add_argument("--diff-file")
    changed.add_argument("--report", type=Path)
    changed.add_argument("--json-report", type=Path)
    full = sub.add_parser("full", help="query every tracked Markdown repo link")
    full.add_argument("--output-snapshot", type=Path)
    full.add_argument("--update-baseline", type=Path,
                      help="replace a durable baseline only when every API result is verified")
    full.add_argument("--report", type=Path)
    full.add_argument("--json-report", type=Path)
    full.add_argument("--workers", type=int, default=4)
    verify = sub.add_parser("verify-snapshot", help="offline coverage check")
    verify.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    args = parser.parse_args(argv)

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    inventory = inventory_markdown(ROOT)
    if args.mode == "verify-snapshot":
        try:
            snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"ERROR: cannot read snapshot: {exc}", file=sys.stderr)
            return 1
        problems = snapshot_coverage(snapshot, inventory)
        if problems:
            print("\n".join(f"ERROR: {item}" for item in problems), file=sys.stderr)
            return 1
        print(f"Repository snapshot covers all {len(inventory)} tracked repo links.")
        return 0

    if args.mode == "changed":
        diff_text = Path(args.diff_file).read_text(encoding="utf-8") if args.diff_file else git_diff(ROOT, args.base, args.head)
        occurrences = changed_entry_occurrences(ROOT, diff_text)
        grouped = {}
        for occurrence in occurrences:
            grouped.setdefault(occurrence.repo.lower(), []).append(occurrence)
        if not grouped:
            checked_at = "not-run: no repository entry changed"
            payload = {"checked_at": None, "records": {}, "findings": []}
            report = _report({}, [], checked_at)
            if args.report:
                args.report.parent.mkdir(parents=True, exist_ok=True)
                args.report.write_text(report, encoding="utf-8")
            else:
                print(report, end="")
            if args.json_report:
                _write_json(args.json_report, payload)
            return 0
        client = GitHubClient()
        scan_started_at = client.official_checked_at()
        records = inspect_many((items[0].repo for items in grouped.values()), client=client,
                               checked_at=scan_started_at, workers=4)
        checked_at = client.official_checked_at()
        stamp_scan_completed_at(records, scan_started_at, checked_at)
        findings = []
        for key, record in records.items():
            findings.extend(findings_for(record, grouped[key], datetime.now(timezone.utc)))
    else:
        client = GitHubClient()
        scan_started_at = client.official_checked_at()
        records = inspect_many((item["requested"] for item in inventory.values()),
                               client=client, checked_at=scan_started_at, workers=args.workers)
        checked_at = client.official_checked_at()
        stamp_scan_completed_at(records, scan_started_at, checked_at)
        grouped = all_occurrences(ROOT)
        findings = []
        for key, record in records.items():
            findings.extend(findings_for(record, grouped.get(key, []), datetime.now(timezone.utc)))
        snapshot = make_snapshot(inventory, records, checked_at)
        if args.output_snapshot:
            _write_json(args.output_snapshot, snapshot)
        if args.update_baseline:
            if any(row.get("state") == "unverified" for row in records.values()):
                print("Baseline not replaced: at least one API result is unverified.", file=sys.stderr)
            else:
                _write_json(args.update_baseline, snapshot)

    payload = {"checked_at": checked_at, "records": records, "findings": findings}
    report = _report(records, findings, checked_at)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    if args.json_report:
        _write_json(args.json_report, payload)
    return 1 if any(item["severity"] == "error" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())

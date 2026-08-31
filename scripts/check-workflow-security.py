#!/usr/bin/env python3
"""Fail closed on mutable Actions, broad default tokens, and unsafe PR events."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"
USES_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)(?:\s+#\s*(\S.*))?$", re.MULTILINE)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
WRITE_ALLOWLIST = {
    (".github/workflows/docs.yml", "deploy"): {"pages", "id-token"},
    (".github/workflows/content-health.yml", "scan"): {"issues"},
    (".github/workflows/pr-gate.yml", "comment"): {"pull-requests"},
    (".github/workflows/release.yml", "publish"): {"contents"},
}


def _events(value: object) -> set[str]:
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {str(item) for item in value}
    if isinstance(value, dict):
        return {str(item) for item in value}
    return set()


def _write_keys(value: object) -> set[str]:
    if value == "write-all":
        return {"*"}
    if not isinstance(value, dict):
        return set()
    return {str(key) for key, permission in value.items() if permission == "write"}


def problems_for_text(path: Path, text: str) -> list[str]:
    problems: list[str] = []
    loaded: dict = {}
    try:
        # BaseLoader follows YAML syntax without YAML 1.1's surprising
        # `on` -> True coercion, so event names remain inspectable strings.
        loaded = yaml.load(text, Loader=yaml.BaseLoader)
        if not isinstance(loaded, dict):
            problems.append("workflow does not parse to a mapping")
            loaded = {}
    except yaml.YAMLError as exc:
        problems.append(f"invalid YAML: {exc}")

    events = _events(loaded.get("on"))
    if "pull_request_target" in events:
        problems.append("pull_request_target is forbidden; use pull_request with a read-only token")
    if "permissions" not in loaded:
        problems.append("missing explicit top-level permissions")
    top_writes = _write_keys(loaded.get("permissions"))
    if top_writes:
        problems.append(f"top-level write permissions are forbidden: {sorted(top_writes)}")
    if re.search(r"\$\{\{\s*github\.event\.pull_request\.(?:title|body|head\.ref)", text):
        problems.append("untrusted pull-request text must not be interpolated into workflow code")

    workflow_path = path.as_posix()
    jobs = loaded.get("jobs", {})
    if isinstance(jobs, dict):
        for job_name, job in jobs.items():
            if not isinstance(job, dict):
                continue
            writes = _write_keys(job.get("permissions"))
            allowed = WRITE_ALLOWLIST.get((workflow_path, str(job_name)), set())
            unexpected = writes - allowed
            if unexpected:
                problems.append(
                    f"job {job_name} has unapproved write permissions: {sorted(unexpected)}"
                )
            if writes and "pull_request" in events:
                steps = job.get("steps", [])
                if not isinstance(steps, list):
                    continue
                for step in steps:
                    if not isinstance(step, dict):
                        continue
                    uses = str(step.get("uses", ""))
                    run = str(step.get("run", ""))
                    if uses.startswith("actions/checkout@"):
                        problems.append(
                            f"PR writer job {job_name} must not checkout PR-controlled code"
                        )
                    if "scripts/" in run or "scripts\\" in run:
                        problems.append(
                            f"PR writer job {job_name} must not execute repository scripts"
                        )

    for match in USES_RE.finditer(text):
        target, comment = match.groups()
        if target.startswith(("./", "docker://")):
            continue
        if "@" not in target:
            problems.append(f"action has no immutable ref: {target}")
            continue
        action, ref = target.rsplit("@", 1)
        if not SHA_RE.fullmatch(ref):
            problems.append(f"{action} must use a full 40-character commit SHA, not {ref}")
        if not comment or not re.match(r"v?\d", comment):
            problems.append(f"{action}@{ref} needs a human-readable version comment")
    return [f"{path}: {item}" for item in problems]


def main() -> int:
    problems: list[str] = []
    for path in sorted(WORKFLOWS.glob("*.y*ml")):
        problems.extend(problems_for_text(path.relative_to(ROOT), path.read_text(encoding="utf-8")))
    if problems:
        print("\n".join(f"ERROR: {item}" for item in problems), file=sys.stderr)
        return 1
    print(f"Workflow security check passed for {len(list(WORKFLOWS.glob('*.y*ml')))} workflow(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

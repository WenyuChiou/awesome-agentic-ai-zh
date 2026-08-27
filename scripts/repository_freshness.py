#!/usr/bin/env python3
"""Shared GitHub-repository inventory and claim checks.

This module deliberately checks only facts GitHub can answer. It cannot prove
that a project is good teaching material or that nearby product/model facts are
current.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

GITHUB_RE = re.compile(r"https://github\.com/([\w.-]+)/([\w.-]+?)(?:[#?/),;:\s]|$)")
NON_REPO_OWNERS = {
    "settings", "marketplace", "login", "logout", "join", "topics",
    "trending", "collections", "events", "explore", "issues", "pulls",
    "notifications", "search", "new", "organizations", "users", "blog",
    "about", "pricing", "features", "security", "enterprise",
    "customer-stories", "sponsors", "apps", "orgs",
}
PLACEHOLDER_REPOS = {
    "owner/repo", "example/repo", "your-org/your-repo", "user/repo",
}
SELF_REPO = "wenyuchiou/awesome-agentic-ai-zh"
EXCLUDE_DIRS = {".git", ".ai", ".claude", "node_modules", "_build", ".venv"}
STALE_DAYS = 183

ARCHIVE_CAVEAT_RE = re.compile(
    r"archiv(?:ed|e)|historical|legacy|deprecated|no longer maintained|"
    r"unmaintained|已封存|封存|已歸檔|歸檔|歷史|已归档|归档|历史|停止維護|停止维护",
    re.IGNORECASE,
)
ACTIVE_CLAIM_RE = re.compile(
    r"actively maintained|\bactive\b|\bcurrent\b|\brecommended\b|"
    r"持續維護|持续维护|目前|現行|当前|推薦|推荐",
    re.IGNORECASE,
)
LICENSE_ALIASES = {
    "MIT": "MIT",
    "APACHE 2.0": "Apache-2.0",
    "APACHE-2.0": "Apache-2.0",
    "BSD-2-CLAUSE": "BSD-2-Clause",
    "BSD-3-CLAUSE": "BSD-3-Clause",
    "GPL-3.0": "GPL-3.0",
    "GPL-3.0-ONLY": "GPL-3.0",
    "AGPL-3.0": "AGPL-3.0",
    "AGPL-3.0-ONLY": "AGPL-3.0",
    "MPL-2.0": "MPL-2.0",
}
LICENSE_RE = re.compile(
    r"(?<![\w.-])(?:MIT|Apache(?:-|\s)2\.0|BSD-[23]-Clause|"
    r"A?GPL-3\.0(?:-only)?|MPL-2\.0)(?![\w.-])",
    re.IGNORECASE,
)


def normalize_repo(owner: str, name: str, *, include_self: bool = False) -> str | None:
    """Return a normalized owner/repo, or None for GitHub non-repo paths."""
    owner = owner.strip()
    name = name.strip().removesuffix(".git").rstrip(".")
    if not owner or not name or owner.lower() in NON_REPO_OWNERS:
        return None
    repo = f"{owner}/{name}"
    if repo.lower() in PLACEHOLDER_REPOS:
        return None
    if not include_self and repo.lower() == SELF_REPO:
        return None
    return repo


def repos_in_text(text: str, *, include_self: bool = False) -> list[str]:
    found: dict[str, str] = {}
    for match in GITHUB_RE.finditer(text):
        repo = normalize_repo(match.group(1), match.group(2), include_self=include_self)
        if repo:
            found.setdefault(repo.lower(), repo)
    return sorted(found.values(), key=str.lower)


def tracked_markdown_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "*.md"], cwd=root, capture_output=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip())
    files = []
    for raw in result.stdout.decode("utf-8").split("\0"):
        if not raw:
            continue
        rel = Path(raw)
        if any(part in EXCLUDE_DIRS for part in rel.parts):  # abs-parts-ok: git ls-files returns paths relative to root
            continue
        files.append(rel)
    return files


def inventory_markdown(root: Path) -> dict[str, dict]:
    """Collect each unique repo once, with stable file-level source metadata."""
    inventory: dict[str, dict] = {}
    for rel in tracked_markdown_files(root):
        text = (root / rel).read_text(encoding="utf-8")
        per_file: dict[str, int] = {}
        canonical: dict[str, str] = {}
        for match in GITHUB_RE.finditer(text):
            repo = normalize_repo(match.group(1), match.group(2), include_self=True)
            if not repo:
                continue
            key = repo.lower()
            per_file[key] = per_file.get(key, 0) + 1
            canonical.setdefault(key, repo)
        for key, count in per_file.items():
            item = inventory.setdefault(key, {
                "requested": canonical[key], "reference_count": 0, "sources": [],
            })
            item["reference_count"] += count
            item["sources"].append(rel.as_posix())
    for item in inventory.values():
        item["sources"].sort()
    return dict(sorted(inventory.items()))


@dataclass(frozen=True)
class DiffOccurrence:
    repo: str
    path: str
    line: int
    text: str
    context: str = ""


def _bounded_context(lines: list[str], line_number: int, radius: int) -> str:
    """Nearby prose, stopping before another repository's entry begins."""
    index = line_number - 1
    # An entry's metadata follows its URL heading/row. Starting above the URL
    # can assign the previous entry's License field to this one.
    start = index
    end = min(len(lines), index + radius + 1)
    for position in range(index - 1, start - 1, -1):
        if repos_in_text(lines[position], include_self=True):
            start = position + 1
            break
    for position in range(index + 1, end):
        if repos_in_text(lines[position], include_self=True):
            end = position
            break
    return "\n".join(lines[start:end])


def add_file_context(root: Path, occurrences: list[DiffOccurrence], radius: int = 6) -> list[DiffOccurrence]:
    """Attach nearby prose without persisting churn-prone line numbers."""
    cache: dict[str, list[str]] = {}
    enriched = []
    for item in occurrences:
        try:
            lines = cache.setdefault(
                item.path, (root / item.path).read_text(encoding="utf-8").splitlines()
            )
        except OSError:
            enriched.append(item)
            continue
        enriched.append(DiffOccurrence(
            item.repo, item.path, item.line, item.text,
            _bounded_context(lines, item.line, radius),
        ))
    return enriched


def all_occurrences(root: Path, radius: int = 6) -> dict[str, list[DiffOccurrence]]:
    """Find every repo reference with nearby text for scheduled claim checks."""
    grouped: dict[str, list[DiffOccurrence]] = {}
    for rel in tracked_markdown_files(root):
        lines = (root / rel).read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines, start=1):
            repos = repos_in_text(line, include_self=True)
            if not repos:
                continue
            context = _bounded_context(lines, index, radius)
            for repo in repos:
                grouped.setdefault(repo.lower(), []).append(
                    DiffOccurrence(repo, rel.as_posix(), index, line, context)
                )
    return grouped


_HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def changed_occurrences(diff_text: str) -> list[DiffOccurrence]:
    """Return repository links from added Markdown lines in a unified diff."""
    path = ""
    new_line = 0
    out: list[DiffOccurrence] = []
    for raw in diff_text.splitlines():
        if raw.startswith("+++ b/"):
            path = raw[6:]
            continue
        if raw.startswith("+++ /dev/null"):
            path = ""
            continue
        match = _HUNK_RE.match(raw)
        if match:
            new_line = int(match.group(1))
            continue
        if not path or not path.endswith(".md"):
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            text = raw[1:]
            for repo in repos_in_text(text, include_self=True):
                out.append(DiffOccurrence(repo, path, new_line, text))
            new_line += 1
        elif raw.startswith("-") and not raw.startswith("---"):
            continue
        elif not raw.startswith("\\"):
            new_line += 1
    return out


@dataclass(frozen=True)
class ChangedLine:
    path: str
    line: int
    text: str


def changed_lines(diff_text: str) -> list[ChangedLine]:
    """Map added and removed Markdown lines to their location in the new file."""
    path = ""
    new_line = 0
    out = []
    for raw in diff_text.splitlines():
        if raw.startswith("+++ b/"):
            path = raw[6:]
            continue
        if raw.startswith("+++ /dev/null"):
            path = ""
            continue
        match = _HUNK_RE.match(raw)
        if match:
            new_line = int(match.group(1))
            continue
        if not path or not path.endswith(".md"):
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            out.append(ChangedLine(path, new_line, raw[1:]))
            new_line += 1
        elif raw.startswith("-") and not raw.startswith("---"):
            out.append(ChangedLine(path, new_line, raw[1:]))
        elif not raw.startswith("\\"):
            new_line += 1
    return out


def changed_entry_occurrences(root: Path, diff_text: str, max_distance: int = 12) -> list[DiffOccurrence]:
    """Find repo entries touched by URL, License, or status-only edits."""
    by_path: dict[str, list[ChangedLine]] = {}
    for item in changed_lines(diff_text):
        by_path.setdefault(item.path, []).append(item)
    selected: dict[tuple[str, str, int], DiffOccurrence] = {}
    for path, changes in by_path.items():
        try:
            lines = (root / path).read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        repo_lines: list[tuple[int, list[str]]] = []
        for number, line in enumerate(lines, start=1):
            repos = repos_in_text(line, include_self=True)
            if repos:
                repo_lines.append((number, repos))
        for change in changes:
            direct = repos_in_text(change.text, include_self=True)
            if direct:
                line_number = min(max(change.line, 1), max(len(lines), 1))
                current_text = lines[line_number - 1] if lines else change.text
                current = {repo.lower() for repo in repos_in_text(current_text, include_self=True)}
                for repo in direct:
                    # A removed URL maps to the next new-file line. Do not audit
                    # a repo the PR is deleting or replacing.
                    if repo.lower() not in current:
                        continue
                    selected[(repo.lower(), path, line_number)] = DiffOccurrence(
                        repo, path, line_number, current_text
                    )
                continue
            candidates = [(number, repos) for number, repos in repo_lines
                          if number <= change.line and change.line - number <= max_distance]
            if not candidates:
                continue
            line_number, repos = candidates[-1]
            # A new heading starts a different entry even when it contains no URL.
            between = lines[line_number: max(line_number, change.line - 1)]
            if any(re.match(r"^\s*#{1,6}\s", line) for line in between):
                continue
            for repo in repos:
                selected[(repo.lower(), path, line_number)] = DiffOccurrence(
                    repo, path, line_number, lines[line_number - 1]
                )
    return add_file_context(root, list(selected.values()), radius=max_distance)


def git_diff(root: Path, base: str, head: str) -> str:
    result = subprocess.run(
        ["git", "diff", "--unified=0", f"{base}...{head}", "--", "*.md"],
        cwd=root, capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git diff failed: {result.stderr.strip()}")
    return result.stdout


def _token() -> str | None:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        result = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, timeout=10,
        )
    except OSError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


class GitHubClient:
    def __init__(self, token: str | None = None, timeout: int = 20):
        self.token = token if token is not None else _token()
        self.timeout = timeout

    def _get(self, path: str) -> tuple[int, dict | None, str | None, str | None]:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "awesome-agentic-ai-zh-repository-freshness/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = Request(f"https://api.github.com{path}", headers=headers)
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return response.status, json.load(response), None, response.headers.get("Date")
        except HTTPError as exc:
            detail = f"HTTP {exc.code}"
            if exc.code == 429 or exc.headers.get("X-RateLimit-Remaining") == "0":
                detail += "; rate limited"
            return exc.code, None, detail, exc.headers.get("Date")
        except (URLError, TimeoutError, OSError, ValueError) as exc:
            return 0, None, f"{type(exc).__name__}: {exc}", None

    def official_checked_at(self) -> str:
        """Use GitHub's HTTP Date header as the one scan timestamp."""
        status, _, error, date_header = self._get("/rate_limit")
        if status != 200 or not date_header:
            raise RuntimeError(error or "GitHub API response did not include a Date header")
        try:
            value = parsedate_to_datetime(date_header).astimezone(timezone.utc)
        except (TypeError, ValueError) as exc:
            raise RuntimeError(f"invalid GitHub API Date header: {date_header!r}") from exc
        return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def inspect(self, repo: str, checked_at: str) -> dict:
        encoded = "/".join(quote(part, safe="") for part in repo.split("/", 1))
        status, data, error, _ = self._get(f"/repos/{encoded}")
        if status == 404:
            return {"requested": repo, "state": "missing", "checked_at": checked_at,
                    "api_status": 404}
        if status != 200 or not isinstance(data, dict):
            return {"requested": repo, "state": "unverified", "checked_at": checked_at,
                    "api_status": status or None, "error": error or "invalid response"}

        release_status, release, release_error, _ = self._get(f"/repos/{encoded}/releases/latest")
        if release_status not in {200, 404}:
            return {"requested": repo, "state": "unverified", "checked_at": checked_at,
                    "api_status": release_status or None,
                    "error": f"latest release: {release_error or 'invalid response'}"}
        latest_release = None
        if release_status == 200 and not isinstance(release, dict):
            return {"requested": repo, "state": "unverified", "checked_at": checked_at,
                    "api_status": 200, "error": "latest release: invalid response"}
        if release_status == 200:
            latest_release = {
                "tag": release.get("tag_name"),
                "published_at": release.get("published_at"),
            }
        canonical = data.get("full_name") or repo
        license_data = data.get("license") if isinstance(data.get("license"), dict) else {}
        return {
            "requested": repo,
            "state": "verified",
            "checked_at": checked_at,
            "api_status": 200,
            "canonical": canonical,
            "html_url": data.get("html_url"),
            "redirected": canonical.lower() != repo.lower(),
            "archived": bool(data.get("archived")),
            "disabled": bool(data.get("disabled")),
            "visibility": data.get("visibility"),
            "default_branch": data.get("default_branch"),
            "license": license_data.get("spdx_id") or "NOASSERTION",
            "pushed_at": data.get("pushed_at"),
            "latest_release": latest_release,
        }


def inspect_many(repos: Iterable[str], *, client: GitHubClient, checked_at: str,
                 workers: int = 4) -> dict[str, dict]:
    unique = {repo.lower(): repo for repo in repos}
    results: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=max(1, min(workers, 8))) as pool:
        futures = {pool.submit(client.inspect, repo, checked_at): key
                   for key, repo in unique.items()}
        for future in as_completed(futures):
            key = futures[future]
            try:
                results[key] = future.result()
            except Exception as exc:  # fail visibly; never call an exception healthy
                results[key] = {
                    "requested": unique[key], "state": "unverified",
                    "checked_at": checked_at, "api_status": None,
                    "error": f"{type(exc).__name__}: {exc}",
                }
    return dict(sorted(results.items()))


def _iso_days_ago(timestamp: str | None, now: datetime) -> int | None:
    if not timestamp:
        return None
    try:
        value = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return (now - value).days


def _license_claim(text: str) -> str | None:
    match = LICENSE_RE.search(text)
    if not match:
        return None
    raw = re.sub(r"\s+", " ", match.group(0)).upper()
    return LICENSE_ALIASES.get(raw)


def _license_claim_for_occurrence(occurrence: DiffOccurrence) -> str | None:
    """Read a license only when it can be tied to this one repository."""
    if len(repos_in_text(occurrence.text, include_self=True)) != 1:
        return None
    claim = _license_claim(occurrence.text)
    if claim:
        return claim
    # Entry headings commonly put the URL on the heading and License in a small
    # field table below. General nearby prose is intentionally not accepted:
    # it caused one table row's license to be assigned to its neighbour.
    if re.match(r"^\s*#{1,6}\s", occurrence.text):
        for line in occurrence.context.splitlines():
            if re.search(r"(?:^|\|)\s*(?:\*\*)?License(?:\*\*)?\s*(?:\||:)", line,
                         re.IGNORECASE):
                return _license_claim(line)
    return None


def findings_for(record: dict, occurrences: list[DiffOccurrence], now: datetime) -> list[dict]:
    """Classify hard contradictions separately from review-only warnings."""
    findings: list[dict] = []
    repo = record.get("requested", "?")
    if record.get("state") == "missing":
        return [{"severity": "error", "code": "missing", "repo": repo,
                 "message": "repository is missing or not public"}]
    if record.get("state") != "verified":
        return [{"severity": "error", "code": "unverified", "repo": repo,
                 "message": record.get("error", "GitHub API could not verify it")}]
    if record.get("redirected"):
        findings.append({"severity": "error", "code": "redirected", "repo": repo,
                         "message": f"use canonical slug {record.get('canonical')}"})

    for occurrence in occurrences:
        prose = occurrence.context or occurrence.text
        caveat = bool(ARCHIVE_CAVEAT_RE.search(prose))
        active = bool(ACTIVE_CLAIM_RE.search(prose))
        where = f"{occurrence.path}:{occurrence.line}"
        if (record.get("archived") or record.get("disabled")) and active and not caveat:
            findings.append({"severity": "error", "code": "inactive-described-active",
                             "repo": repo, "where": where,
                             "message": "archived/disabled repository is described as current"})
        claim = _license_claim_for_occurrence(occurrence)
        actual = record.get("license")
        if claim and actual and actual != "NOASSERTION" and claim.lower() != actual.lower():
            findings.append({"severity": "error", "code": "license-mismatch",
                             "repo": repo, "where": where,
                             "message": f"text says {claim}; GitHub reports {actual}"})

    combined = "\n".join((item.context or item.text) for item in occurrences)
    caveat_anywhere = bool(ARCHIVE_CAVEAT_RE.search(combined))
    if (record.get("archived") or record.get("disabled")) and not caveat_anywhere:
        findings.append({"severity": "warning", "code": "inactive-needs-caveat",
                         "repo": repo, "message": "add a clear archived/history note"})
    if record.get("license") == "NOASSERTION":
        findings.append({"severity": "warning", "code": "no-license-metadata",
                         "repo": repo, "message": "GitHub reports no SPDX license"})
    if record.get("latest_release") is None:
        findings.append({"severity": "warning", "code": "no-latest-release",
                         "repo": repo, "message": "GitHub reports no published release"})
    age = _iso_days_ago(record.get("pushed_at"), now)
    if age is not None and age > STALE_DAYS:
        findings.append({"severity": "warning", "code": "old-last-push", "repo": repo,
                         "message": f"last push was {age} days ago; age alone is not a failure"})
    return findings


def make_snapshot(inventory: dict[str, dict], records: dict[str, dict], checked_at: str) -> dict:
    rows = {}
    for key, source in inventory.items():
        row = dict(records[key])
        row["reference_count"] = source["reference_count"]
        row["sources"] = source["sources"]
        rows[key] = row
    return {
        "schema_version": 1,
        "verified_at": checked_at,
        "repository_count": len(rows),
        "repositories": rows,
    }


def snapshot_coverage(snapshot: dict, inventory: dict[str, dict]) -> list[str]:
    rows = snapshot.get("repositories") if isinstance(snapshot, dict) else None
    if not isinstance(rows, dict):
        return ["snapshot.repositories must be an object"]
    problems = []
    if snapshot.get("schema_version") != 1:
        problems.append("schema_version must be 1")
    verified_at = snapshot.get("verified_at")
    try:
        verified_dt = datetime.fromisoformat(str(verified_at).replace("Z", "+00:00"))
        if verified_dt.tzinfo is None or verified_dt > datetime.now(timezone.utc):
            problems.append("verified_at must be timezone-aware and not in the future")
    except ValueError:
        problems.append("verified_at must be a valid ISO timestamp")
    missing = sorted(set(inventory) - set(rows))
    extra = sorted(set(rows) - set(inventory))
    if missing:
        problems.append(f"snapshot missing {len(missing)} repo(s): {', '.join(missing[:5])}")
    if extra:
        problems.append(f"snapshot has {len(extra)} unreferenced repo(s): {', '.join(extra[:5])}")
    if snapshot.get("repository_count") != len(rows):
        problems.append("repository_count does not match repositories")
    for key, row in rows.items():
        if not isinstance(row, dict):
            problems.append(f"{key}: row must be an object")
            continue
        if str(row.get("requested", "")).lower() != key:
            problems.append(f"{key}: requested identity does not match key")
        if row.get("state") not in {"verified", "missing", "unverified"}:
            problems.append(f"{key}: invalid state")
        if row.get("checked_at") != verified_at:
            problems.append(f"{key}: checked_at must match verified_at")
        if not isinstance(row.get("reference_count"), int) or row.get("reference_count", 0) < 1:
            problems.append(f"{key}: reference_count must be a positive integer")
        sources = row.get("sources")
        if not isinstance(sources, list) or not sources or not all(isinstance(x, str) for x in sources):
            problems.append(f"{key}: sources must be a non-empty string list")
        expected = inventory.get(key, {})
        if row.get("reference_count") != expected.get("reference_count"):
            problems.append(f"{key}: reference_count does not match current Markdown")
        if row.get("sources") != expected.get("sources"):
            problems.append(f"{key}: sources do not match current Markdown")
        if row.get("state") == "verified":
            required = {"canonical", "html_url", "archived", "disabled", "visibility",
                        "default_branch", "license", "pushed_at", "latest_release"}
            absent = sorted(required - set(row))
            if absent:
                problems.append(f"{key}: verified row missing {', '.join(absent)}")
            if not isinstance(row.get("archived"), bool) or not isinstance(row.get("disabled"), bool):
                problems.append(f"{key}: archived and disabled must be booleans")
            if not isinstance(row.get("canonical"), str) or not isinstance(row.get("html_url"), str):
                problems.append(f"{key}: canonical and html_url must be strings")
        elif row.get("state") == "missing" and row.get("api_status") != 404:
            problems.append(f"{key}: missing row must have api_status 404")
        elif row.get("state") == "unverified" and not isinstance(row.get("error"), str):
            problems.append(f"{key}: unverified row must explain the error")
    return problems

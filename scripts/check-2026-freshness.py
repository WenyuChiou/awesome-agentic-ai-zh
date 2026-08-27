#!/usr/bin/env python3
"""
2026 model freshness check.

掃所有 .md 找 stale model references (Claude 3.5 / GPT-4o / Gemini 2.0 / etc.)
that lack a 'lineage' / '前身' / '歷史' qualifier within ±N lines context.

Config: scripts/freshness-models.yml (whitelist + stale pattern list)

Usage:
    python scripts/check-2026-freshness.py              # exit 1 on stale
    python scripts/check-2026-freshness.py --warn-only  # exit 0, prefix ::warning::

Exit codes:
    0 — no stale refs OR --warn-only mode
    1 — stale refs found in strict mode
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime, timezone
from fnmatch import fnmatch
from pathlib import Path

try:
    import yaml
except ImportError:
    print(
        '❌ PyYAML required. Install: pip install pyyaml',
        file=sys.stderr,
    )
    sys.exit(2)


# '.claude' holds git worktrees (.claude/worktrees/<name>/), each a full second copy
# of the tree. This walker uses Path.rglob, which — unlike glob.glob — descends into
# dot-directories, so without this every finding is reported twice and the count is
# meaningless. 2026-08-02: a stray worktree turned 6 stale refs into 13.
EXCLUDE_DIRS = {'.ai', 'book', 'node_modules', '.git', '.claude', 'archives', '.coord', '_build', '_site'}
MIRROR_SUFFIXES = ('.en.md', '.zh-Hans.md')  # trilingual mirror locales (zh-TW is canonical)
FRESHNESS_MARKER_RE = re.compile(
    r'<!--\s*freshness:\s*'
    r'canonical=(?P<canonical>[A-Za-z0-9_./-]+);\s*'
    r'verified_on=(?P<verified>\d{4}-\d{2}-\d{2});\s*'
    r'scope=(?P<scope>[a-z0-9_, -]+);\s*'
    r'max_age_days=(?P<max_age_days>\d+)\s*-->'
)


def load_config(repo_root: Path) -> dict:
    cfg_path = repo_root / 'scripts' / 'freshness-models.yml'
    with open(cfg_path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def canonical_rel(rel: str) -> str:
    """Map a mirror-locale rel path to its zh-TW canonical form for config matching.

    'stages/06-memory-rag.en.md' -> 'stages/06-memory-rag.md'. Mirror locales are
    now scanned (not skipped), so per-file overrides and exclude_files written for
    the canonical file must also apply to its .en.md / .zh-Hans.md siblings.
    """
    for suffix in MIRROR_SUFFIXES:
        if rel.endswith(suffix):
            return rel[: -len(suffix)] + '.md'
    return rel


def matches_exclude(path: Path, repo_root: Path, exclude_patterns: list[str]) -> bool:
    """Check if a file path (or its canonical mirror form) matches any exclude glob."""
    rel = path.relative_to(repo_root).as_posix()
    for candidate in {rel, canonical_rel(rel)}:
        for pat in exclude_patterns:
            if fnmatch(candidate, pat) or fnmatch(candidate + '/', pat):
                return True
    return False


def has_qualifier(
    lines: list[str], idx: int, terms: list[str], window: int
) -> bool:
    """Check if any qualifier term appears in ±window lines around idx."""
    start = max(0, idx - window)
    end = min(len(lines), idx + window + 1)
    context = ' '.join(lines[start:end])
    return any(q in context for q in terms)


def scan_file(
    path: Path,
    cfg: dict,
    repo_root: Path,
) -> list[tuple[Path, int, str, str, str]]:
    """
    Scan one file for stale model refs.

    Returns list of (file, line_no, matched_text, pattern, note).
    """
    findings: list[tuple[Path, int, str, str, str]] = []
    content = path.read_text(encoding='utf-8')
    lines = content.split('\n')

    window = cfg.get('qualifier_context_lines', 2)

    # Check per-file context override (mirror locales inherit the canonical file's override)
    rel = path.relative_to(repo_root).as_posix()
    canon = canonical_rel(rel)
    for override in cfg.get('exclude_files_pattern_specific', []):
        pat = override.get('file', '')
        if fnmatch(rel, pat) or fnmatch(canon, pat):
            # Accept both new (qualifier_window) and legacy (skip_patterns_with_context)
            # field names for backward compat
            window = override.get(
                'qualifier_window',
                override.get('skip_patterns_with_context', window),
            )
            break

    # Check stale_patterns
    for entry in cfg.get('stale_patterns', []):
        include_files = entry.get('include_files', [])
        if include_files and not any(
            fnmatch(rel, file_pattern) or fnmatch(canon, file_pattern)
            for file_pattern in include_files
        ):
            continue
        pat_str = entry['pattern']
        try:
            pat = re.compile(pat_str)
        except re.error as e:
            print(f'⚠ Invalid regex in freshness-models.yml: {pat_str!r}: {e}', file=sys.stderr)
            continue
        terms = entry.get('qualifier_terms', [])
        note = entry.get('note', '')
        for idx, line in enumerate(lines):
            m = pat.search(line)
            if m and not has_qualifier(lines, idx, terms, window):
                findings.append((path, idx + 1, m.group(0), pat_str, note))

    # Check stale_date_phrases
    for entry in cfg.get('stale_date_phrases', []):
        pat_str = entry['pattern']
        try:
            pat = re.compile(pat_str)
        except re.error as e:
            print(f'⚠ Invalid regex: {pat_str!r}: {e}', file=sys.stderr)
            continue
        terms = entry.get('qualifier_terms', [])
        note = entry.get('note', '')
        for idx, line in enumerate(lines):
            m = pat.search(line)
            if m:
                # Date phrases either need qualifier OR no qualifier needed (different rule)
                if terms and has_qualifier(lines, idx, terms, window):
                    continue
                findings.append((path, idx + 1, m.group(0), pat_str, note))

    return findings


def should_skip(path: Path, repo_root: Path, cfg: dict) -> bool:
    # Match on the path RELATIVE to the repo root — matching path.parts tests
    # the ABSOLUTE path, so a checkout under e.g. `.claude/worktrees/<name>/`
    # skips every file and this gate reports a silent all-clear. Same bug as the
    # 2026-08-02 check-locale-links.py / check-catalog-counts.py fix.
    if any(part in EXCLUDE_DIRS for part in path.relative_to(repo_root).parts):
        return True
    # Mirror locales (.en.md / .zh-Hans.md) are NO LONGER skipped: stale facts drift
    # into them when canonical is fixed but the mirror is left behind (2026-07 gap).
    exclude_files = cfg.get('exclude_files', [])
    return matches_exclude(path, repo_root, exclude_files)


def _freshness_mirror_paths(canonical: Path) -> list[Path]:
    """Return canonical + English + Simplified-Chinese paths for one page."""
    if canonical.suffix != '.md':
        raise ValueError(f'freshness canonical must be a .md file: {canonical}')
    return [
        canonical,
        canonical.with_name(canonical.stem + '.en.md'),
        canonical.with_name(canonical.stem + '.zh-Hans.md'),
    ]


def _parse_freshness_marker(path: Path) -> tuple[str, date, tuple[str, ...], int]:
    """Parse the single machine-readable freshness marker in ``path``."""
    text = path.read_text(encoding='utf-8')
    matches = list(FRESHNESS_MARKER_RE.finditer(text))
    if not matches:
        if 'freshness:' in text:
            raise ValueError('malformed freshness marker')
        raise ValueError('missing freshness marker')
    if len(matches) != 1:
        raise ValueError(f'expected one freshness marker, found {len(matches)}')

    match = matches[0]
    try:
        verified = date.fromisoformat(match.group('verified'))
    except ValueError as exc:
        raise ValueError(f'invalid verified date: {match.group("verified")}') from exc

    scopes = tuple(part.strip() for part in match.group('scope').split(','))
    if not scopes or any(not part for part in scopes) or len(scopes) != len(set(scopes)):
        raise ValueError('scope must be a non-empty comma-separated list without duplicates')
    return match.group('canonical'), verified, scopes, int(match.group('max_age_days'))


def scan_verified_pages(
    repo_root: Path,
    cfg: dict,
    today: date | None = None,
) -> tuple[list[str], list[str]]:
    """Validate freshness markers and return (blocking errors, age warnings)."""
    today = today or datetime.now(timezone.utc).date()
    errors: list[str] = []
    warnings: list[str] = []
    fact_packs: dict[str, tuple[str, dict]] = {}

    # Fact packs hold the evidence URLs; their date and scope must not drift
    # from the page marker that the gate validates. The suffix convention keeps
    # this generic as later stages add their own independently named packs.
    for pack_name, pack in cfg.items():
        if not pack_name.endswith('_fact_pack'):
            continue
        if not isinstance(pack, dict) or not pack.get('canonical'):
            errors.append(f'{pack_name}: fact pack is missing canonical metadata')
            continue
        pack_canonical = pack['canonical']
        if pack_canonical in fact_packs:
            errors.append(f'{pack_name}: duplicate fact pack for {pack_canonical}')
            continue
        fact_packs[pack_canonical] = (pack_name, pack)

    for entry in cfg.get('verified_pages', []):
        canonical_rel_path = entry.get('canonical', '')
        expected_scopes = tuple(entry.get('required_scopes', []))
        expected_max_age = entry.get('max_age_days')
        if not canonical_rel_path or not expected_scopes or not isinstance(expected_max_age, int):
            errors.append(f'freshness config is incomplete: {entry!r}')
            continue

        canonical = repo_root / canonical_rel_path
        parsed: list[tuple[str, tuple[str, date, tuple[str, ...], int]]] = []
        for page in _freshness_mirror_paths(canonical):
            rel = page.relative_to(repo_root).as_posix()
            if not page.is_file():
                errors.append(f'{rel}: freshness page is missing')
                continue
            try:
                marker = _parse_freshness_marker(page)
            except (OSError, ValueError) as exc:
                errors.append(f'{rel}: {exc}')
                continue
            parsed.append((rel, marker))

            marker_canonical, verified, scopes, max_age = marker
            if marker_canonical != canonical_rel_path:
                errors.append(
                    f'{rel}: canonical={marker_canonical} does not match '
                    f'{canonical_rel_path}'
                )
            if verified > today:
                errors.append(f'{rel}: verified date {verified} is in the future (UTC today {today})')
            if scopes != expected_scopes:
                errors.append(
                    f'{rel}: scope {",".join(scopes)} does not match '
                    f'{",".join(expected_scopes)}'
                )
            if max_age != expected_max_age:
                errors.append(
                    f'{rel}: max_age_days={max_age} does not match {expected_max_age}'
                )
            if verified <= today and (today - verified).days > expected_max_age:
                warnings.append(
                    f'{rel}: freshness review is {(today - verified).days} days old '
                    f'(recommended maximum {expected_max_age})'
                )

        if len(parsed) == 3:
            canonical_marker = parsed[0][1]
            for rel, marker in parsed[1:]:
                if marker != canonical_marker:
                    errors.append(
                        f'{rel}: freshness marker differs from {canonical_rel_path}'
                    )

            pack_entry = fact_packs.get(canonical_rel_path)
            if pack_entry is None:
                errors.append(f'{canonical_rel_path}: matching fact pack is missing')
            else:
                pack_name, pack = pack_entry
                try:
                    pack_verified = date.fromisoformat(str(pack.get('verified_on', '')))
                except ValueError:
                    errors.append(f'{pack_name}: invalid verified_on={pack.get("verified_on")!r}')
                else:
                    if pack_verified != canonical_marker[1]:
                        errors.append(
                            f'{pack_name}: fact pack verified_on={pack_verified} differs from '
                            f'page marker {canonical_marker[1]}'
                        )
                pack_scopes = tuple(pack.get('scope', []))
                if pack_scopes != canonical_marker[2]:
                    errors.append(
                        f'{pack_name}: fact pack scope {",".join(pack_scopes)} differs from '
                        f'page marker {",".join(canonical_marker[2])}'
                    )

    return errors, warnings


def main() -> int:
    # Force UTF-8 stdout
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--warn-only',
        action='store_true',
        help='Exit 0 even if stale refs found, print ::warning:: prefix',
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    cfg = load_config(repo_root)

    marker_errors, marker_warnings = scan_verified_pages(repo_root, cfg)
    for warning in marker_warnings:
        print(f'::warning::{warning}')

    all_findings: list[tuple[Path, int, str, str, str]] = []
    for md in sorted(repo_root.rglob('*.md')):
        if should_skip(md, repo_root, cfg):
            continue
        try:
            all_findings.extend(scan_file(md, cfg, repo_root))
        except Exception as e:
            print(f'⚠ scan error {md.relative_to(repo_root)}: {e}', file=sys.stderr)

    if not all_findings and not marker_errors:
        print('✓ No stale model references or invalid freshness markers detected.')
        return 0

    prefix = '::warning::' if args.warn_only else '❌ '
    for error in marker_errors:
        print(f'{prefix}{error}')
    for path, lineno, matched, pat, note in all_findings:
        rel = path.relative_to(repo_root).as_posix()
        print(f'{prefix}{rel}:{lineno}: stale "{matched}" — {note} [pattern: {pat}]')

    if all_findings:
        print(f'\nFound {len(all_findings)} stale model reference(s).')
        print(
            'Tip: add a qualifier ("前身" / "歷史" / "lineage" / "baseline" / "原始")'
            ' nearby to mark as historical reference.'
        )
    if marker_errors:
        print(f'Found {len(marker_errors)} freshness marker error(s).')
    return 0 if args.warn_only else 1


if __name__ == '__main__':
    sys.exit(main())

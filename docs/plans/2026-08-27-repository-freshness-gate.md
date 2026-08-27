# Repository Freshness Gate Implementation Plan

**Goal:** Check every GitHub repository link without pretending repository activity alone proves that the surrounding lesson is correct.

**Delivery:** One independent PR, `codex/repository-freshness-gate`, after the reader-UX foundation merges and before Stage 02 begins. It must be independently revertible and must not rewrite chapter content.

## Current coverage and gaps

The repository already has three useful pieces:

- `check-links.py` performs scheduled URL probes.
- `refresh-stars.py` and `weekly-catalog-refresh.yml` maintain volatile star labels.
- `pr-link-audit.py` reports metadata for newly added repo links.

They leave four gaps:

1. The PR audit is advisory, skips fork PRs, and checks only newly added repos.
2. The scheduled fast scan proves reachability, not archived status, moves, license, release, or written-claim consistency.
3. There is no durable inventory showing when each unique repository was last verified.
4. A successful API call can still leave stale prose, such as calling an archived project active.

## Evidence model

Create one generated snapshot keyed by lowercase `owner/repo`. Each record stores:

- canonical `html_url` and whether the original slug redirects;
- `archived`, `disabled`, visibility, default branch, SPDX license;
- `pushed_at`, latest release tag and publish date when one exists;
- every Markdown file plus the total reference count. Line numbers are computed
  in each report instead of stored, so inserting one paragraph does not rewrite
  hundreds of otherwise unchanged snapshot rows;
- `checked_at`, HTTP/API result, and an explicit `verified`, `unverified`, or `missing` state.

Do not store authentication data or raw API headers. Deduplicate before querying so the same repo is fetched once per run.

## Two execution modes

### Pull request mode

- Scan repository links on added or changed Markdown lines.
- Reuse the base snapshot for unchanged repos.
- Block only hard, actionable contradictions: missing/private repository, changed canonical slug not reflected in the link, archived repo described as active/current, or an explicit SPDX license claim that disagrees with API metadata.
- Report staleness, no release, and `NOASSERTION` as review items rather than automatic deletion.
- Support fork PRs with a read-only analysis job; posting a sticky comment is optional and must be separated from untrusted checkout execution.

### Scheduled full mode

- Query every unique GitHub repository link with bounded concurrency and authenticated API requests.
- Respect rate-limit headers and use conditional requests or the prior snapshot where practical.
- Upload JSON inventory and Markdown summary as workflow artifacts.
- Open or update one tracking issue for hard failures; do not create duplicate issues every week.
- Preserve the last verified snapshot when GitHub is unavailable. A network failure is `unverified`, never `healthy`.

## Claim validation boundaries

Machine-checkable repository facts include archive state, canonical slug, license metadata, push date, releases, and reachability. They do **not** prove teaching quality, API behavior, model price, context length, product availability, or whether an old stable project remains useful.

For those claims, each migrated chapter keeps an official-source fact pack with an ISO verification date. A chapter review compares the fact pack with all three languages immediately before staging. Scheduled expiry produces a warning; a direct contradiction blocks the relevant PR.

## Planned files

- Create `scripts/check-repository-freshness.py`.
- Create `scripts/test_repository_freshness.py`.
- Create `scripts/repository-freshness-snapshot.json`.
- Modify `scripts/pr-link-audit.py` to share URL normalization and classification rules.
- Modify `.github/workflows/pr-link-audit.yml` for changed-link and fork-safe coverage.
- Create `.github/workflows/repository-freshness.yml` for the scheduled full inventory.
- Update `scripts/README.md`, `CONTRIBUTING.md`, and `CHANGELOG.md`.

## Acceptance criteria

- Every unique GitHub repository URL in tracked Markdown appears in the generated inventory or in an explicit non-repository exclusion.
- Redirects, archived/disabled state, SPDX license, last push, and latest release are recorded with `checked_at`.
- Changed-link PR mode has unit tests for moved, archived, missing, unlicensed, stale-but-stable, rate-limited, and fork-PR cases.
- Hard contradictions fail; age-only findings warn.
- A rate-limited or failed scan cannot return a clean result.
- The snapshot contains no token, credential, or response header.
- Existing link, star, duplicate-repository, anchor, mirror, and docs gates still pass.

# Visible learning contract

## Goal

A learner should not need to guess which closed menu contains the important part. Required reading,
curated projects, and the complete rated learning-resource table stay visible. Setup, cost,
alternatives, deeper theory, and troubleshooting may stay closed.

## Audit result

The earlier chapter-by-chapter changes left important material closed in Stage 0, Stage 1, Stage 2,
Stage 5, and Track A1–A3. Stage 7.5, Stage 8, and the Researcher and Developer paths already kept
their rated tables visible, but their minimum counts were not all protected by the common checker.

## Change shape

- Open the existing reading and resource sections without changing their rows, links, order, or ratings.
- Keep the same three-locale structure and existing deep-link headings.
- Block closed summaries named Required Reading, Curated Projects, or Learning Resources.
- Lock each modernized visible section to its expected minimum link and rating count.
- Keep the dedicated MCP／Skills catalog as the deliberate exception: categories and safety boundaries
  are visible, while hundreds of entries open by category only when needed.

## Verification

Run the reader-UX checker, its unit tests, locale／anchor／mirror gates, documentation builds, and the
full relevant test suite. Review the final staged fingerprint once. This branch stacks on PR #200 and
must remain a Draft PR until the maintainer approves the stack.

# Curriculum Modernization Implementation Plan

> **For Codex:** Use `bounded-agent-harness`, `verification-before-completion`, and an independent `code-reviewer` for every shipping PR. Plan each chapter before editing it.

**Goal:** Modernize the whole learning map one reversible chapter at a time, while keeping the main path simple enough that a new learner always knows what to do next.

**Architecture:** Use a migration train: a small foundation PR establishes shared rules and gates, then chapter PRs move through the repository in the agreed order. A normal chapter is one self-contained trilingual PR. A high-risk chapter uses a short stack of two or three PRs, each independently reviewable and revertible.

**Tech Stack:** Markdown, MkDocs, mdBook, Python validation scripts, GitHub Actions, native Git stacked branches, GitHub PRs.

---

## 1. Audit baseline

- Baseline: `origin/main` at `b5282ed682d2ecce19d208eafd380888cddce733`.
- Audit worktree, promoted into the first delivery branch: `codex/curriculum-reader-contract`.
- The user's main workspace was left untouched; its pre-existing `stages/01-llm-basics.md` modification belongs to the concurrent Claude session.
- Repository size inspected: 234 Markdown files and 684 unique URLs.
- Fast link audit: 361 GitHub URLs verified, 0 failed, 323 non-GitHub or login-gated URLs skipped by fast mode.
- Existing template, mirror-parity, and image-locale gates pass. This proves structure has not regressed; it does not prove that pages are easy to read or semantically current.

## 2. Reading-load findings

The number below is the final reader-UX checker's conservative zh-TW source-level proxy: non-whitespace Markdown visible on first load. Default-open bodies and fenced code count; HTML comments and closed bodies do not. It is a ratchet metric, not a browser DOM text-length claim.

| Page | Visible characters | `<details>` | Open by default | Initial conclusion |
|---|---:|---:|---:|---|
| Stage 00 | 2,125 | 5 | 0 | Migrated; use as the prerequisite-gateway pattern |
| Stage 01 | 6,609 | 14 | 3 | Migrated main path, but three open code paths remain as an explicit baseline |
| Stage 02 | 13,702 | 8 | 4 | Next migration; too much code and setup visible |
| Stage 03 | 17,377 | 7 | 1 | Needs a beginner core plus collapsed technical depth |
| Stage 04 | 14,960 | 0 | 0 | Needs progressive disclosure and framework freshness |
| Stage 05 | 53,437 | 1 | 0 | Highest reading-load risk; must use a short stack |
| Stage 06 | 38,465 | 2 | 0 | Research survey and beginner tutorial are mixed together |
| Stage 07 | 24,856 | 0 | 0 | Production concepts and resource catalog need separation |
| Stage 07.5 | 34,532 | 0 | 0 | Reference-map content is presented like required reading |
| Stage 08 | 24,246 | 0 | 0 | Security-sensitive and highly time-sensitive; short stack |

Additional high-load pages:

- Root `README.md`: 334 lines, 13,855 visible proxy characters, no progressive disclosure.
- Walkthrough: 623 lines, 14,140 visible proxy characters, no progressive disclosure.
- Cookbook: 606 lines, 14,760 visible proxy characters, no progressive disclosure.
- Glossary: 472 lines, 17,798 visible proxy characters, no progressive disclosure.
- MCP / Skills catalog: 1,136 lines, 30,774 visible proxy characters, no progressive disclosure.
- Five audience branches: all have zero `<details>`; researcher and developer paths need both freshness and a clearer first action.

## 3. Cross-project defects confirmed by the audit

### 3.1 Gates do not measure reader experience

The current gates can pass a 53,000-character visible page. Add a ratcheted reader-UX gate for migrated pages only. It must measure visible text, default-open details, visible deep-link headings, resource group structure, and trilingual parity without causing untouched pages to fail merely because time passes.

### 3.2 The contributor contract conflicts with the new reading rule

`CLAUDE.md` requires every Ollama Path A block to use `<details ... open>`. `stages/DESIGN.md` and the style guide also preserve this exception. Stage 02 demonstrates why an unconditional exception is too broad: four large code blocks become visible before the reader can understand the chapter.

Replace the unconditional rule with this decision:

- The exercise title, result, and first action stay visible.
- Long code and troubleshooting stay collapsed.
- Path A may open only when it is the single immediate action and its rendered body is short.
- Path B remains collapsed.

### 3.3 The learning route is not expressed consistently

- `README.md` lists Track A as A1, A2, A3, then shared Stage 5.
- `PROGRESS.md` and the shortest-route sentence use A1, A2, Stage 5, A3.
- `learning-map.png` visually uses A1 → A2 → A3 → Stage 5 and omits Stage 7.5.

The user's requested order is treated as the **editing order**, not automatically as the learner route. During the final coherence pass, choose one canonical learner route, update text first, then redraw the image.

### 3.4 Tool identities are scattered

OpenRouter and OpenCode appear in Stage 1 examples, Track A, setup, cookbook, glossary, and CLI comparison pages. Pi has no stable learning-map entry. Beginners need one shared identity card:

| Thing | Plain role | Canonical detailed home |
|---|---|---|
| LLM | The brain that generates an answer | Stage 01 |
| Direct provider API | A direct door to one model company | Stage 01 / setup guide |
| OpenRouter | One API and billing/routing layer across providers | Stage 01 short card; Stage A1 detailed comparison |
| OpenCode | Open-source coding agent / harness using selectable models | Track A1; cross-link from Stage 05 |
| Pi | Minimal terminal coding harness extended with packages, skills, prompts, and providers | Track A1; advanced SDK note in Stage 05 |

Official identity sources:

- [OpenRouter FAQ](https://openrouter.ai/docs/faq)
- [OpenCode documentation](https://opencode.ai/docs)
- [Pi documentation](https://pi.dev/docs/latest)

### 3.5 Resource tables mix learning levels

Many pages place tutorials, production frameworks, historical repos, and inspiration lists in one ranking table. Star counts draw attention but do not explain where to begin. For stage pages:

- Keep a visible “start with these 3” list.
- Collapse the full resource table.
- Group rows with separate `<tbody>` blocks and `scope="rowgroup"` headers.
- Use `best for`, `start here`, `status`, `license`, and `verified on` instead of star counts.
- Keep historical projects only in a clearly labeled historical group.
- Let the catalog, not every chapter, own volatile popularity metadata.

## 4. Migration train and PR method

### 4.1 Rules

1. Never rewrite the entire site in one branch.
2. Each merged PR must be useful on its own and reversible with one revert.
3. Normal chapter: one trilingual PR including direct glossary/index/changelog updates.
4. Large or high-risk chapter: two or three stacked PRs, never a long stack across many chapters.
5. Open stacked PRs against the previous topic branch. Merge bottom-up. After a lower PR merges, rebase the next branch onto `origin/main`, push with `--force-with-lease`, retarget, and rerun every gate.
6. A reviewer acknowledgment belongs to one staged fingerprint. Any file change invalidates it.
7. Squash each PR so every migration layer has one clean rollback commit.
8. Do not start the next chapter until main CI passes for the merged SHA.

### 4.2 Planned train

| Order | Delivery | Shape | Reason |
|---:|---|---|---|
| F0 | Reader-UX contract and ratcheted gate | One PR | Resolve Path A rule conflict before Stage 02 |
| F1 | Repository-link health and claim freshness | One PR | Upgrade the existing advisory checks before adding more Stage 02 resources |
| 02 | Prompt engineering | Two-PR short stack | Reader path first; runnable prompt-eval example second |
| A1 | CLI identities and first choice | One PR | Add OpenRouter/OpenCode/Pi distinction and current setup |
| A2 | Reusable CLI workflow | One PR | Simplify commands, rules, and portable prompt concepts |
| A3 | CLI integration and production | One or two PRs | Many fast-moving tools and security/cost claims |
| 03 | Tool use and first agent | One PR | Core path can be separated from advanced variants |
| 04 | Agent frameworks | One PR | Freshness-heavy but only 235 canonical lines |
| 05 | Claude Code ecosystem | Three-PR short stack | 947 lines, 91 GitHub links, 107 version tokens, diagram rewrite |
| 06 | Context, RAG, and memory | Three-PR short stack | Beginner path, research appendix, then examples/resources |
| 07 | Multi-agent and production | Two-PR short stack | Core production loop, then benchmark/resources |
| 07.5 | Advanced concepts reading map | Two-PR short stack | Simplify entry map; move deep research into collapsed reference |
| 08 | Interfaces and security | Two-PR short stack | Computer/browser/sandbox facts plus security review |
| X1 | Audience branches | Five small PRs or two short stacks | Researcher, developer, teacher, knowledge worker, everyday user |
| X2 | Cookbook, glossary, catalogs | Resource-specific PRs | Preserve searchability; do not collapse definitions blindly |
| X3 | Full walkthrough | One or two PRs | Keep end-to-end value while exposing checkpoints progressively |
| X4 | Final coherence + README + diagrams | Two-PR short stack | Canonical route/text first; images and homepage second |

## 5. Per-phase audit notes

### A1–A3

- All three pages have zero progressive disclosure.
- A1 still links the old `sst/opencode` path while stating the repository moved; use `anomalyco/opencode` directly.
- Add Pi only after confirming `pi.dev` and its current package/repository identity.
- Separate model providers, routers, subscriptions, coding agents, IDEs, and local runtimes before comparing products.
- Security defaults, authentication, local-model support, and subscription reuse require official-source checks.

### Stage 03–04

- Stage 03 still defines CoT as exposing the reasoning process and points to Stage 02's old exercise; update after Stage 02.
- Stage 03 contains 42 external links and 21 GitHub repositories; keep a short canonical route and collapse alternatives.
- Stage 04 has no `<details>` and contains fast-changing framework/API/version claims. Verify each framework from official docs and repository releases before editing examples.

### Stage 05

- Highest visible load in the project.
- The “7-layer” diagram includes a `Layer 2.5`, and its Prompt/Context/Harness brackets are hard for a beginner to reconcile.
- Split the work into foundation/customization, subagents/workflows, and SDK/diagram layers.
- Treat Claude-specific commands, feature maturity, model names, authentication, permissions, and plugin structure as freshness-sensitive.

### Stage 06–08

- Stage 06 duplicates current-model comparisons that belong in Stage 01; link to Stage 01 rather than maintain two current-model tables.
- Stage 06 has 151 external links and 109 year references. Keep a simple RAG/memory path visible and move research surveys into a researcher-facing appendix.
- Stage 07 has 34 star claims and no progressive disclosure; separate the production checklist from the benchmark landscape.
- Stage 07.5 is a reading map, not a required chapter-length tutorial. Make the “which problem do you have?” decision visible and collapse the 12-concept reference.
- Stage 08 is security-sensitive. Claims about browser/computer use, sandboxes, permissions, and data handling must use current official sources.

### Audience branches and resource pages

- Add a visible “start here today” action to each role branch.
- Researcher content needs current research workflow tools, evidence boundaries, citation verification, and privacy guidance.
- Developer content needs current CLI/IDE agent identities, plan/review/rollback workflow, and security defaults.
- Teacher content needs stronger evidence and age/privacy/academic-integrity guidance.
- Cookbook recipes should show outcome first; setup, variants, and troubleshooting collapse beneath it.
- Glossary should remain directly searchable. Use short definitions first and collapse examples/history, rather than hiding the term itself.
- The 1,137-line catalog needs category navigation, status/freshness metadata, and perhaps generated filters; do not turn every entry into a separate `<details>` block.

## 6. Diagram decision log

| Diagram | Decision now | Trigger for final action |
|---|---|---|
| Main learning map | Redraw later | After canonical Track A order and shared-hub route are decided |
| Branch decision tree | Keep for now | Redraw only if role names or branch boundaries change |
| Stage 05 architecture | Redraw with Stage 05 | Current layer count and discipline boundaries are confusing |
| Stage 07.5 concept cluster | Move to advanced/collapsed area; create a simpler entry map if needed | After the 12 concepts are revalidated |
| Stage 06 small pipeline diagrams | Reassess during Stage 06 | Keep if each directly helps one visible task |

Text or semantic HTML is preferred when it can express the relationship accessibly. Generate a localized image only when the spatial relationship materially improves understanding.

### Repository freshness is a separate gate

The existing automation already checks broken links, star drift, and new repo metadata, but it does not prove that every written status, license, version, or recommendation is still true. Deliver F1 after F0 as a separate PR:

- PR checks query only added or changed repository links and fail on hard contradictions such as missing/private repos, an active recommendation that is archived, or a declared license that disagrees with GitHub metadata.
- A scheduled job inventories every unique `github.com/owner/repo` link, follows repository moves, records `archived`, `disabled`, `pushed_at`, latest release, default branch, and SPDX license, and uploads both JSON evidence and a readable report.
- Age alone is a warning. A stable specification can be old without being obsolete; `pushed_at` must never be used as the sole deletion rule.
- Product capabilities, model prices, API availability, and other non-repository claims use page-specific official-source fact packs and ISO verification dates. GitHub metadata cannot validate those claims.
- Transient API failures, secondary rate limits, and GitHub outages produce an explicit “unverified” result and retain the previous snapshot. They never masquerade as a clean scan.

Detailed design: [`2026-08-27-repository-freshness-gate.md`](./2026-08-27-repository-freshness-gate.md).

## 7. New acceptance gates

### Task 1: Add a reader-UX ratchet

**Files:**

- Create: `scripts/check-reader-ux.py`
- Create: `scripts/test_reader_ux.py`
- Create: `scripts/reader-ux-pages.yml`
- Create: `scripts/requirements-reader-ux.txt`
- Modify: `.github/workflows/stage-template-check.yml`
- Modify: `CLAUDE.md`
- Modify: `stages/DESIGN.md`
- Modify: `resources/style-guide.md`
- Modify: `resources/style-guide.en.md`
- Modify: `resources/style-guide.zh-Hans.md`

**Checks:**

- Migrated page has a configured maximum visible-character count.
- Required deep-link headings remain outside `<details>`.
- Page-specific default-open allowance is not exceeded.
- `<details>` never uses `open` for time, prerequisites, cost, long tables, troubleshooting, or optional reading.
- Resource row groups use `<tbody>`, `scope="col"`, and `scope="rowgroup"`.
- All three locales use the same reader-UX configuration and section identities.
- Expired review dates warn on schedule; they do not break an unrelated PR only because time passed.

### Task 2: Run the standard gate for every chapter PR

Run, in this order:

```powershell
git diff --check
python scripts/check-reader-ux.py
python scripts/check-stage-template.py
python scripts/check-anchors.py --strict
python scripts/test_anchor_slug_parity.py
python scripts/check-mirror-parity.py
python scripts/check-locale-links.py
python scripts/zh-hans-localize.py --check
python scripts/check-hans-chars.py
python scripts/check-image-locale.py --strict
python scripts/check-duplicate-repos.py
python scripts/check-2026-freshness.py
python scripts/build-docs-tree.py
python -m mkdocs build --quiet
```

Then run chapter-specific example tests, perform an element-landing audit, compare trilingual meaning, and invoke one independent `code-reviewer` on the final staged fingerprint.

## 8. Stop conditions

Stop the current chapter and ask for direction when:

- two official sources disagree and the newer source does not clearly supersede the older one;
- a term or project name is ambiguous, such as “Pi,” without a confirmed official URL;
- a change would alter the canonical learner route rather than merely clarify it;
- a stacked PR cannot pass independently without weakening a gate;
- concurrent Claude edits touch the same bytes and cannot be integrated without choosing between two meanings.

# Contributing

> [繁體中文](./CONTRIBUTING.md) | [简体中文](./CONTRIBUTING.zh-Hans.md) | **English**


Thanks for considering a contribution. **This is a curated learning roadmap, not an exhaustive catalog. Quality > quantity.**

This repo is **designed for community-driven improvement** — one person can't keep pace with the AI agent ecosystem alone. The maintainer's quarterly review isn't enough; more eyes are needed.

The catalog is split into **two tracks**: **Track A** (CLI Power User, `tracks/cli/A1-A3`) and **Track B** (Agent Builder, `stages/03-08`, including Stage 7.5). When contributing, please indicate which track you're modifying — the two have different audiences.

## 🚪 First-time contribution: 5 easy starting points

Not sure where to start? Pick one you can finish in 30 minutes:

1. **🐛 Report a stale entry**: run `python scripts/check-repository-freshness.py full`, then put evidence of archival, disabling, relocation, or license mismatch in an issue
2. **🔗 Fix one broken link**: hit a 404 reading stage X? Just PR the fix
3. **✍️ Fill in an entry's "Run it" section**: many entries lack install commands; if you've run it, add them
4. **🌏 Fix a locale mirror**: compare Traditional Chinese, Simplified Chinese, and English, then fix mismatched meaning, links, or awkward wording
5. **💬 Add a personal note to an entry**: stuck on `Exercise 3`? Add a "Note: xxx" line

None of these require reading the full style guide first. Their small, checkable scope makes them good first contributions.

> 🧪 **Running the walkthrough / build script / CI workflow for the first time?** See [`.github/TESTING-STATUS.md`](.github/TESTING-STATUS.md) — an **honest disclosure** of what the maintainer has actually executed vs only syntax-checked vs not tested at all. Being the first to hit a bug and open an issue + PR is the highest-value contribution.

## What We Accept

### High-value PRs
- **Adding a project** to a stage with reasoning for why it teaches that stage
- **Completing or correcting trilingual content**: finalize Traditional Chinese first, then make English and Simplified Chinese say the same thing
- **Flagging stale / unmaintained projects** (open an issue first)
- **Improving curation notes** on existing projects (clearer "what it teaches" explanations)
- **Reorganizing** within a stage if the current ordering doesn't match learning progression

### Lower priority (still welcome)
- Typo fixes
- Link fixes (verify with `curl -I` first)
- Stage description polish

### Not accepted
- Bulk additions of repos without curation reasoning
- Self-promotion without educational value
- Projects with no documentation
- Projects without clear license

## How to Add a Project

Each project in a stage page should follow this format:

```markdown
### [Project Name](url)

| Field | Value |
|---|---|
| Language | Python / TS / etc. |
| License | MIT / Apache 2 / ... |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: 1-sentence summary of the core learning.

**Best for**: who should study this and why.

**Notes**: 1-3 sentence personal evaluation. What's strong, what's weak, what to skip.

**Run it**:
\`\`\`bash
# minimal install / first-run command
\`\`\`
```

## Curation Criteria

A project worth listing must have:

1. **Active maintenance**: commits within last 6 months OR explicit "stable, no longer maintained" notice
2. **Documented hello-world**: a reader should be able to run something within 30 minutes
3. **Clear license**: MIT, Apache 2, BSD, or comparable. Avoid no-license repos.
4. **Trustworthy maintainer**: well-known org, company, or individual with track record

The automated check merges duplicate links to the same repo, then checks whether it moved, was archived or disabled, and which SPDX license GitHub reports. No push in six months is only a prompt to look again: a stable project with teaching value may stay when its status is clear. If the GitHub API cannot answer, the result says “unverified”; it never pretends everything is healthy.

## Trilingual Style

- **Traditional Chinese (zh-TW) is canonical**; English (`*.en.md`) and Simplified Chinese (`*.zh-Hans.md`) are formal mirrors.
- A change to public learning material that already has three locales must update all three in the same PR. If you write only one language, open an issue with the evidence and proposed wording so a maintainer can arrange the complete sync.
- Concepts, URLs, numbers, ratings, safety limits, and completion criteria must match across all three locales.
- **Natural translation**, not word-for-word. Technical terms can stay in English where natural ("使用 LangGraph 建 multi-agent 系統").
- **Full style rules: see [`resources/style-guide.md`](resources/style-guide.md)** (zh) or [`resources/style-guide.en.md`](resources/style-guide.en.md) (en) — banned words, entry schema, license conventions, writing style, recommendation star definitions all live there. Read before PR.

## Process

1. Open an issue first for new projects or bigger restructuring
2. PR with focused scope (one stage at a time)
3. Wait for review (typically 7 days)
4. Reviewer may ask for clarification on "why this teaches that stage"

## Anti-patterns to Avoid

- ❌ "leverage", "delve", "comprehensive", "robust" (LLM-tells)
- ❌ Hype framing ("revolutionary", "game-changing")
- ❌ Listing a project just because it's popular
- ❌ Long quotes from the project's own marketing copy

## Becoming a Stage / Branch Maintainer

Beyond one-shot PRs, we welcome **long-term maintainers** for specific stages
or branches — responsible for periodic review, triaging issues in that area,
and gating PRs.

Self-nomination process:

1. Open an issue titled `[maintainer] Stage N — your-handle` or `[maintainer] for-X branch — your-handle`
2. State your time commitment (suggested: at least one quarter = 3 months)
3. Briefly describe your background in this area

See [`CONTRIBUTORS.md`](CONTRIBUTORS.md) for the current maintainer roster.

## License

By contributing, you agree your work is licensed under MIT.

# Outreach draft — English awesome-lists (get listed)

> **Status**: draft, not submitted. Passive reach (be listed in lists
> English builders already browse). Each is a PR to their list's
> learning/tutorials section. The `-zh` repo name reads as "Chinese-only"
> on these lists — the PR description must say "trilingual, English fully
> maintained" up front or it gets filed under a zh-only section.

## Targets

| Target | Section to PR into | Notes |
|---|---|---|
| [kyrolabs/awesome-agents](https://github.com/kyrolabs/awesome-agents) | learning / guides | Agent-specific; recheck the live learning section and contribution rules before submitting |
| [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | tutorials / learning | It is an *apps* list — confirm it has a learning/tutorials section before PR, else it gets rejected as out-of-scope |
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | Tutorials | ALREADY in progress (PR #6135, see channel-partners.md #6) — don't double-submit |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | 📖 Tutorials & Guides | ALREADY tracked (channel-partners.md #9) — don't double-submit |

## PR title

```
Add awesome-agentic-ai-zh — trilingual staged roadmap (LLM basics → multi-agent)
```

## PR description (entry + rationale)

```
Adding **awesome-agentic-ai-zh** to the [learning/tutorials] section.

What it is: a staged learning roadmap for agentic AI (not a flat list) —
10 learning stops: 8 topic stages + Stage 0 readiness + Stage 7.5 reading, 2 tracks
(use CLI agents vs build your own), 5 audience branches, curated
projects, runnable exercises. MIT.

Why it fits this list: it's the "where do I start / in what order"
companion to the reference lists already here.

Note on the name: the repo is `-zh` (Chinese-origin) but it is
**trilingual and the English edition is fully maintained** (~0.4% of
English lines carry any CJK; English-native required reading per stage;
CI-checked). Please file it under the general
learning/tutorials section, not a zh-only sub-section.

Repo: https://github.com/WenyuChiou/awesome-agentic-ai-zh
Rendered site: https://wenyuchiou.github.io/awesome-agentic-ai-zh/
```

## Suggested one-line list entry (match each list's existing format)

```
- [awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh) — Trilingual staged roadmap: 10 learning stops (8 topic stages + Stage 0 readiness + Stage 7.5 reading) + 2 tracks + curated projects. MIT.
```

## Don'ts
- ❌ Don't PR to a list whose CONTRIBUTING forbids "roadmap/aggregate" entries — read it first.
- ❌ Don't double-submit to punkpeye / travisvn (already tracked).
- ❌ Don't PR to `e2b-dev/awesome-ai-agents` — verified 2026-05-21, last
  push 2025-02-26 (~15 months stale / effectively abandoned); a PR there
  will not be merged. Removed from the target table for this reason.

- ❌ Don't omit the "trilingual / English-maintained" note — the `-zh`
  name otherwise gets it mis-filed or rejected as out-of-scope.

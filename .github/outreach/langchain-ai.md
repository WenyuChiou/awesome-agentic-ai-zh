# Outreach: LangChain ecosystem (langchain-ai / kyrolabs/awesome-langchain)

> ⚠️ **Send content is now canonical in [`_send-day-packages.md`](_send-day-packages.md)** (package C — 10 learning stops / curated resources). This file is kept for positioning rationale; do not paste its older entry/stats blocks directly.

> **Status**: not contacted · **Channel**: GitHub PR
> **Primary lang**: en (with zh as bonus)
> **Last updated**: 2026-08-30 (refreshed — 10-stop structure, correct section target)
> **Repos**:
> - https://github.com/langchain-ai/langchain (main repo)
> - https://github.com/kyrolabs/awesome-langchain (community awesome list)

**Why this target**: Our Stage 4 teaches LangChain and LangGraph, and the Chinese-ecosystem catalog includes Langchain-Chatchat plus a Chinese LangChain getting-started guide. The target list already has a learning section, so the cross-link is relevant.

**Pitch angle**:

- For `langchain-ai/langchain` itself: too big a target; aim instead at the **community awesome list** (`kyrolabs/awesome-langchain`).
- For `kyrolabs/awesome-langchain`: we're a multilingual learning-order complement to their flat catalog.
- **Target section confirmed (2026-05-26)**: `## Learn → ### Notebooks`. Precedent: `liaokongVFX/LangChain-Chinese-Getting-Started-Guide` already sits there. There is **no** "Tutorials & Learning Resources" section in the current README; do not propose one.

**Their counter-value**: Their learning section reaches developers who are already looking for LangChain guidance.

---

## Variant 1 — Social post (X / LinkedIn, ~280 chars)

```
LangChain learners often ask: "I have the docs, but where do I actually start?"

Built a 10-stop trilingual learning roadmap (8 topic stages + Stage 0 readiness + Stage 7.5 reading; zh-TW · zh-Hans · en). Stage 4
walks through LangChain / LangGraph / AutoGen / CrewAI / Smolagents with
prerequisites and time estimates. Curated projects · MIT.

🔗 github.com/WenyuChiou/awesome-agentic-ai-zh
```

## Variant 2 — GitHub PR to kyrolabs/awesome-langchain (200-300 words)

**PR title**: Add awesome-agentic-ai-zh (trilingual learning roadmap) to Learn → Notebooks

**Diff** (against `## Learn → ### Notebooks`, after the `liaokongVFX/LangChain-Chinese-Getting-Started-Guide` line — keeps the two zh-ecosystem learning resources adjacent):

```diff
  - [LangChain Chinese Getting Started Guide](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide): Chinese LangChain Tutorial for Beginners ![GitHub Repo stars](https://img.shields.io/github/stars/liaokongVFX/LangChain-Chinese-Getting-Started-Guide?style=social)
+ - [WenyuChiou/awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh): Trilingual (zh-TW / zh-Hans / en) 10-stop learning roadmap for agentic AI — Stage 4 covers Workflow Graphs, LangGraph, AutoGen, CrewAI, and Smolagents with hands-on exercises ![GitHub Repo stars](https://img.shields.io/github/stars/WenyuChiou/awesome-agentic-ai-zh?style=social)
```

**PR description**:

```markdown
Hi kyrolabs maintainers,

Proposing addition of [WenyuChiou/awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh) to **Learn → Notebooks**, next to the existing `liaokongVFX/LangChain-Chinese-Getting-Started-Guide` entry (same zh-learning surface).

**Why this is a good fit**:
- Trilingual (zh-TW canonical · zh-Hans · en — all three fully maintained, not MT) — fills a gap for non-English learners
- **Stage 4 (Workflow Graphs & Agent Frameworks)** walks new developers through **LangChain / LangGraph / AutoGen / CrewAI / Smolagents** with prerequisites, time estimates, and hands-on exercises
- The Chinese-ecosystem catalog includes `chatchat-space/Langchain-Chatchat` and the LangChain Chinese Getting Started Guide that's already in your list
- Stage 5 covers the Claude Code / MCP / Skills layer; Stage 8 covers Agent Interfaces (Computer Use / Browser / Sandbox). Together with the catalog this is the complement-to-LangChain-docs that doesn't currently exist in zh

**Stable facts**: MIT licensed. Rendered docs at https://wenyuchiou.github.io/awesome-agentic-ai-zh/. CI runs banned-word + link-rot + anchor-integrity lints on every PR. Cached stars, forks, and traffic totals are intentionally omitted.

If a different section or shape works better, happy to redirect. Thanks for maintaining awesome-langchain.

— Wenyu Chiou (individual maintainer)
```

## Variant 3 — Email to LangChain DevRel (150 words)

```
Hi LangChain team,

I built awesome-agentic-ai-zh — a trilingual (zh-TW / zh-Hans / en) Stage 0 → Stage 8
learning roadmap for agentic AI, with a Chinese-ecosystem resource section.

Stage 4 walks new developers through LangChain → LangGraph → AutoGen →
CrewAI → Smolagents with prerequisites and time estimates per step.
Designed to bridge "I know Python" to "I can build a working agent."

Two questions:
1. Is there a LangChain-side surface where this would fit (Learn, blog,
   docs sidebar)?
2. Any specific LangChain features I should cover better in Stage 4? Open
   to feedback.

No expectation, just opening dialogue.

— Wenyu
```

---

## Notes

- **First target**: kyrolabs/awesome-langchain (community awesome list, lower
  barrier to merge). **Section: `Learn → Notebooks`**, not "Tutorials" (no such
  section exists in the current README — verified 2026-05-26).

- **Second target**: LangChain blog/docs (higher signal but harder to land)
- Avoid pitching `langchain-ai/langchain` itself directly — too big, signal is
  drowned out

- LangSmith / LangGraph teams are separate — different DevRel; don't pitch all
  three at once

- **Do not paste popularity snapshots** — stars, forks, and traffic totals drift and do not prove teaching quality. Recheck only the target section, contribution rules, links, and licenses before submitting.

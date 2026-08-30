# Roadmap

> [繁體中文](./ROADMAP.md) | [简体中文](./ROADMAP.zh-Hans.md) | **English**

This page answers two questions: **What is usable now, and what still needs work?** It is not a release date or delivery promise.

**Status:** 🟢 active / open to contributions · 🟡 known gap · 🔵 idea · ✅ recently completed

---

<a id="near-term-gaps-we-want-to-fill"></a>
<a id="in-progress--always-open-to-contributions"></a>
<a id="-fill-out-hands-on-exercise-coverage"></a>
<a id="-deepen-the-audience-branch-files"></a>
<a id="-stage-2--stage-3-2026-freshness-touch-up"></a>

## 🟢 Active work

### 1. Connect the site into one route

- Shared foundation: `Stage 0 → Stage 1 → Stage 2`
- Track A: `A1 → A2 → Stage 5 → A3 → Stage 8`
- Track B: `Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7 → Stage 7.5 → Stage 8`

Track A may start its Capstone after A3. Stage 8 is recommended, but it does not block entry. The homepage map, text, and tests now use the same route; any future order change must update all three together.

### 2. Improve the five role paths

Researcher, developer, teacher, knowledge-worker, and everyday-user paths will each show one “start today” action. Full project tables, alternatives, and troubleshooting stay closed by default. Core terms and editorial star ratings stay intact.

### 3. Improve setup, courses, cookbook, glossary, and catalog

- Setup first helps readers choose Web, Desktop, IDE, CLI, or API.
- Cookbook recipes show the outcome, first copyable action, and success check first.
- Glossary terms and short definitions remain directly searchable.
- The MCP/Skills catalog stays searchable and gains category navigation and maintenance status.

### 4. Keep repositories and volatile facts current

The weekly workflow checks canonical GitHub repositories, redirects, archives, license metadata, releases, and activity. An older last push is a warning, not an automatic deletion rule. Models, prices, APIs, and capabilities still require chapter-by-chapter official-source checks.

---

<a id="infrastructure-maintainer-in-progress"></a>

## ✅ Recently completed

- Stage 0–8 and A1–A3 completed their first progressive-disclosure, core-term, resource-table, and trilingual pass.
- Stage 2 retained zero-shot, one-shot, few-shot, and Chain of Thought, and gained a localized Prompt Engineering map.
- Stage 3 now teaches the first Agent Loop with a localized diagram; Stage 4 uses frameworks to teach Workflow Graphs; Stage 7 integrates both through Agent Production Engineering across Harness, Loops, and Graphs. Stage 6 gained a two-lane RAG pipeline; Stage 8 gained interface-choice and safety maps.
- Stage 0 has an integrated exercise. Stage 7.5 is intentionally a reading map. Stage 8 has copyable safety exercises; a separate end-to-end example remains open to contributions.
- MkDocs build, mirror/anchor/locale checks, reader-UX, freshness, and repository snapshot gates are in the maintenance flow.

---

## 🟢 Good contribution tasks

- Report an outdated fact or broken link with a current official source.
- Add a clearer “how to run” and success check to one exercise.
- Improve one English or Simplified Chinese sentence without changing meaning, numbers, URLs, or safety rules.
- Add one real role-path scenario with input, output, human review, and privacy boundaries.
- Add status, license, or limits for a stable project; do not judge it only by stars or last-push date.

Start with [`CONTRIBUTING.en.md`](CONTRIBUTING.en.md). For long-term chapter maintenance, see [`CONTRIBUTORS.en.md`](CONTRIBUTORS.en.md).

---

<a id="idea-box-pending-discussion-not-committed-yet"></a>

## 🔵 Still under discussion

- Whether a third formal no-code/web-only track is needed; everyday users can already enter through their role path.
- Whether to add a minimal video walkthrough, including subtitle, trilingual, and maintenance cost.
- Whether Voice Agents and VLA belong under Stage 8/research/developer extensions or need a separate topic page.

Use [Discussions](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions) for ideas; keep issues for defects, stale information, or concrete new resources.

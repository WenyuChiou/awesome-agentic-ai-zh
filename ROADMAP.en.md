# Roadmap

> [繁體中文](./ROADMAP.md) | [简体中文](./ROADMAP.zh-Hans.md) | **English**

This repo is a **community-maintained learning roadmap**: no release date, no promised schedule. This document makes public “where we know things are not good enough and where we want to go next”, so people who want to contribute can pick one piece to start with, without reading the whole repo first just to know what is missing.

> Want to work on one item? Open a [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions) first, or send a PR directly. For long-term stage / branch maintainers, see [`CONTRIBUTORS.md`](CONTRIBUTORS.md). For beginner entry points, see the “5 easy entry points” section in [`CONTRIBUTING.en.md`](CONTRIBUTING.en.md).

**Status legend**: 🟢 In progress / always open to contributions · 🟡 Known gap, wanted · 🔵 Idea, pending discussion · ✅ Recently completed

---

## Near-Term Gaps We Want to Fill

### 🟡 Fill Out Hands-On Exercise Coverage
`examples/` currently covers Stage 1, 2, 3, 4, 5, 6, and 7. **Missing**: Stage 0 (Foundation Concepts), Stage 7.5 (Advanced Agentic Concepts), and Stage 8 (Agent Interfaces). In other words, only Stage 0, 7.5, and 8 remain without corresponding hands-on examples. Each example should run in under 30 minutes and include `how to run` commands.

### 🟡 Deepen the audience branch Files
5 audience branch files by length (zh-TW canonical, 2026-05 snapshot): for-knowledge-worker (143 lines, shortest) < for-developer (166) < for-everyday-users (179) < for-researcher (208) < for-teacher (224). **The shortest files, `for-knowledge-worker.md` / `for-developer.md`, need scenario coverage the most**. `for-teacher.md` is actually the longest, but `CONTRIBUTORS.md` still marks it as “especially open to self-nominations”: what is truly thin is the **academic citation depth for teacher scenarios** (currently only Chen 2020 / Mittal 2024), and more 3-tier teacher AI application scenarios + matching citations are welcome.

### 🟡 Stage 2 / Stage 3 2026 freshness Touch-Up
A few small 2026 wording / model-reference updates have not been synced to mirrors yet (about 5 lines of diff × 2 locales).

---

## In Progress / Always Open to Contributions

- 🟢 **Outdated entry reports** — Run `python scripts/refresh-stars.py` to find repos with large star-count gaps, then open an issue or PR to annotate / remove them.
- 🟢 **Broken link fixes** — Monthly CI scans for link-rot, but direct PRs for anything found in real time are fastest.
- 🟢 **Complete `how to run` sections** — Many entries are missing installation / execution commands. If you have run one, add them.
- 🟢 **Mirror translation smoothing** — Compare `.en.md` / `.zh-Hans.md` against zh-TW, and fix one sentence that reads awkwardly.
- 🟢 **Long-term stage / branch maintainers** — Claim one stage or branch and review it when you have time. The slot table is in `CONTRIBUTORS.md`.

---

## Infrastructure (maintainer in progress)

- ✅ **Community health files** — `CODE_OF_CONDUCT.md` / `SECURITY.md` / `CITATION.cff` / issue-template routing (same batch as this roadmap).
- 🟢 **Learner progress layer** — `PROGRESS.md` self-check template + “Self check / Exit check” at the end of each stage (planned).
- 🔵 **Browsable docs site** — Render stages/tracks/branches into a website with navigation + search + language switching (GitHub Pages, under evaluation).
- 🟢 **Trilingual mirror parity** — `mirror-sync-reminder` + `check-mirror-sync.py` already guard PRs, and legacy drift is being cleaned continuously.
- 🟢 **Quality gates** — link-rot / star-drift / banned-word / anchor / zh-Hans localization CI is online and maintained.

---

## Idea Box (pending discussion, not committed yet)

- 🔵 **More audience branch files**: There are currently 5 (researcher / developer / teacher / knowledge-worker / everyday-users). Whether to split further (for example PM / designer / legal) depends on community needs.
- 🔵 **A third track?**: Today, Track A = CLI Power User (A1–A3 under `tracks/cli/`), and Track B = stages learning path (`stages/` directory Stage 0–8, **not** a standalone directory under `tracks/`). Whether to add a third track (for example “no-code agent only”) is pending discussion.
- 🔵 **Video / interactive supplements**: Whether a text-only learning roadmap should include minimal video walkthroughs depends on cost and maintenance load.

To suggest an idea, open a [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions), not an issue (issues are for bugs / outdated entries / new projects).

---

> This roadmap is not a contract. It reflects the direction “now”, and will change as the community contributes. The most reliable source for “what should happen next” is always open issues + Discussions.

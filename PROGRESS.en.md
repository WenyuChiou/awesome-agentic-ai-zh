# Progress Tracker

> [繁體中文](./PROGRESS.md) | [简体中文](./PROGRESS.zh-Hans.md) | **English**

This is a checklist **for your own use**. You do not need to submit it, open a PR, or have anyone inspect it. Copy it (or fork the repo), tick your own progress, and see where you are and what comes next.

**How to use it**:

1. Each stage's "Learning goals", "Entry requirements", and "Self-check" live in that stage file. This checklist is only an **overview + entry point** and does not repeat the content.
2. A stage's ✅ condition = you can pass the "**Self-check**" section at the end of that stage. Tick it only after passing, then move to the next stop.
3. You do not need to finish everything. Pick one track (Track A or B) + one audience branch to get started.

> Not sure which track to choose? See the dual-track explanation in [`README.en.md`](README.en.md), or [`branches/DESIGN.md`](branches/DESIGN.md). If you get stuck, open a [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions).

---

## Shared Foundations (required for both tracks)

- [ ] **Stage 0 — Foundations** · [`stages/00-foundations.en.md`](stages/00-foundations.en.md)
  ✅ Pass this stage's completion criteria (Stage 0 is a prerequisite gateway; see the stage file for the criteria)

- [ ] **Stage 1 — LLM Basics** · [`stages/01-llm-basics.en.md`](stages/01-llm-basics.en.md)
  ✅ Pass this stage's "Self-check"

- [ ] **Stage 2 — Prompt Design** · [`stages/02-prompt-engineering.en.md`](stages/02-prompt-engineering.en.md)
  ✅ Pass this stage's "Self-check"

---

## Track A — CLI Power User

> You want to **use** agent tools to get work done, and you do not necessarily want to build them yourself.

- [ ] **A1 — CLI Agent Introduction + Selection** · [`tracks/cli/A1-cli-intro.en.md`](tracks/cli/A1-cli-intro.en.md)
- [ ] **A2 — CLI Workflow Patterns** · [`tracks/cli/A2-cli-workflow.en.md`](tracks/cli/A2-cli-workflow.en.md)
- [ ] **Stage 5 — Claude Code Ecosystem (shared by both tracks)** · [`stages/05-claude-code-ecosystem.en.md`](stages/05-claude-code-ecosystem.en.md)
- [ ] **A3 — Integration & Production** · [`tracks/cli/A3-cli-production.en.md`](tracks/cli/A3-cli-production.en.md)
- [ ] **Stage 8 — Agent Interfaces (recommended; does not block Track A Capstone entry)** · [`stages/08-agent-interfaces.en.md`](stages/08-agent-interfaces.en.md)

---

## Track B — Agent Builder

> You want to **build** agents, frameworks, or multi-agent systems yourself.

- [ ] **Stage 3 — Tool Use & Your First Agent Loop** ⭐ · [`stages/03-tool-use-and-hello-agent.en.md`](stages/03-tool-use-and-hello-agent.en.md)
- [ ] **Stage 4 — Workflow Graphs & Agent Frameworks** · [`stages/04-agent-frameworks.en.md`](stages/04-agent-frameworks.en.md)
- [ ] **Stage 5 — Claude Code Ecosystem** ⭐⭐(shared by both tracks)· [`stages/05-claude-code-ecosystem.en.md`](stages/05-claude-code-ecosystem.en.md)
- [ ] **Stage 6 — Context Management: RAG and Memory** · [`stages/06-memory-rag.en.md`](stages/06-memory-rag.en.md)
- [ ] **Stage 7 — Agent Production Engineering: Testable, Observable, Stoppable, and Recoverable** · [`stages/07-multi-agent-production.en.md`](stages/07-multi-agent-production.en.md)
- [ ] **Stage 7.5 — Advanced Agentic Concepts** · [`stages/07.5-advanced-agentic-concepts.en.md`](stages/07.5-advanced-agentic-concepts.en.md)
- [ ] **Stage 8 — Agent Interfaces (shared by both tracks)** · [`stages/08-agent-interfaces.en.md`](stages/08-agent-interfaces.en.md)

---

## Choose one audience branch (matching your role)

> A branch is not "another course layer". It maps what you learned in the stages above to your real scenario. Pick just one.

- [ ] 🔬 **for-researcher** · [`branches/for-researcher.en.md`](branches/for-researcher.en.md)
- [ ] 💻 **for-developer** · [`branches/for-developer.en.md`](branches/for-developer.en.md)
- [ ] 🎓 **for-teacher** · [`branches/for-teacher.en.md`](branches/for-teacher.en.md)
- [ ] 📊 **for-knowledge-worker** · [`branches/for-knowledge-worker.en.md`](branches/for-knowledge-worker.en.md)
- [ ] 👥 **for-everyday-users** · [`branches/for-everyday-users.en.md`](branches/for-everyday-users.en.md)

---

## Capstone

After finishing a track, build something you can show + self-assess. The brief, requirements, and 4-level rubric all live in [`CAPSTONE.en.md`](CAPSTONE.en.md) — this list is just the checkbox entry point; the standard is not duplicated.

- [ ] **Track A Capstone** — assemble a reusable CLI-agent workflow · [`CAPSTONE.en.md`](CAPSTONE.en.md)
- [ ] **Track B Capstone** — build + **evaluate** a multi-agent / RAG system · [`CAPSTONE.en.md`](CAPSTONE.en.md)

---

## Shortest viable path (if you only want one recommendation)

Do not want to plan it yourself? Follow this path to reach "able to do hands-on work" with roughly the fewest detours:

`Stage 0 → Stage 1 → Stage 2 →` choose a track `→` (Track A: `A1 → A2 → Stage 5 → A3 → Stage 8`; Track B: `Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7 → 7.5 → 8`) `→` your branch `→` your track's **Capstone** (see [`CAPSTONE.en.md`](CAPSTONE.en.md)). Track A can start the Capstone after A3; Stage 8 is recommended but does not block entry.

---

> This checklist only tracks "where you are". For each stop, "what to learn / what you need before entering / how to know you learned it" is always defined by that stage file's "Learning goals / Entry requirements / Self-check" sections, to avoid splitting the same standard across two places.

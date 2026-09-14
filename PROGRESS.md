# 學習進度追蹤 / Progress Tracker

> **繁體中文** | [简体中文](./PROGRESS.zh-Hans.md) | [English](./PROGRESS.en.md)

這是一份**給你自己用**的打勾清單——不用提交、不用 PR、沒有人會檢查。複製一份(或 fork repo)勾你自己的進度,知道走到哪、下一站是哪。

**怎麼用**:

1. 每個 stage 的「學習目標」「進入條件」「自我檢查」都在該 stage 檔案裡——這份清單只是**總覽 + 入口**,不重複內容。
2. 一個 stage 的 ✅ 條件 = 你能通過該 stage 結尾的「**自我檢查**」那一節。通過了才勾,勾完往下一站。
3. 不用全部做完。先選一條軌道(Track A 或 B)+ 一條你的 audience branch 就夠開始。

> 不確定選哪條?看 [`README.md`](README.md) 的雙軌說明,或 [`branches/DESIGN.md`](branches/DESIGN.md)。卡住開 [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions)。

---

## 共用基礎(兩條軌道都要)

- [ ] **Stage 0 — 基礎準備** · [`stages/00-foundations.md`](stages/00-foundations.md)
  ✅ 過該 stage 的通過條件(Stage 0 是 prerequisite gateway,通過條件見 stage 內說明)

- [ ] **Stage 1 — LLM 基礎** · [`stages/01-llm-basics.md`](stages/01-llm-basics.md)
  ✅ 過該 stage 的「自我檢查」

- [ ] **Stage 2 — Prompt 設計** · [`stages/02-prompt-engineering.md`](stages/02-prompt-engineering.md)
  ✅ 過該 stage 的「自我檢查」

---

## Track A — CLI Power User

> 你想「**用** agent 工具把工作做完」,不一定要自己 build。

- [ ] **A1 — CLI Agent 入門 + 選擇** · [`tracks/cli/A1-cli-intro.md`](tracks/cli/A1-cli-intro.md)
- [ ] **A2 — CLI Workflow Patterns** · [`tracks/cli/A2-cli-workflow.md`](tracks/cli/A2-cli-workflow.md)
- [ ] **Stage 5 — Claude Code 生態(兩軌共用)** · [`stages/05-claude-code-ecosystem.md`](stages/05-claude-code-ecosystem.md)
- [ ] **A3 — Integration & Production** · [`tracks/cli/A3-cli-production.md`](tracks/cli/A3-cli-production.md)
- [ ] **Stage 8 — Agent 操作介面（建議；不擋 Track A Capstone 入場）** · [`stages/08-agent-interfaces.md`](stages/08-agent-interfaces.md)

---

## Track B — Agent Builder

> 你想「**自己 build** agent / 框架 / 多 agent 系統」。

- [ ] **Stage 3 — 工具使用與第一個 Agent Loop** ⭐ · [`stages/03-tool-use-and-hello-agent.md`](stages/03-tool-use-and-hello-agent.md)
- [ ] **Stage 4 — Workflow Graph 與 Agent 框架** · [`stages/04-agent-frameworks.md`](stages/04-agent-frameworks.md)
- [ ] **Stage 5 — Claude Code 生態** ⭐⭐(兩軌共用)· [`stages/05-claude-code-ecosystem.md`](stages/05-claude-code-ecosystem.md)
- [ ] **Stage 6 — 上下文管理:RAG 與 Memory** · [`stages/06-memory-rag.md`](stages/06-memory-rag.md)
- [ ] **Stage 7 — Agent 上線工程：可測、可看、可停、可恢復** · [`stages/07-multi-agent-production.md`](stages/07-multi-agent-production.md)
- [ ] **Stage 7.5 — 進階 Agentic 概念** · [`stages/07.5-advanced-agentic-concepts.md`](stages/07.5-advanced-agentic-concepts.md)
- [ ] **Stage 8 — Agent 操作介面(兩軌共用)** · [`stages/08-agent-interfaces.md`](stages/08-agent-interfaces.md)

---

## 選一條 audience branch(對應你的身分)

> Branch 不是「再上一層課」,是把上面 stage 學到的東西**對應到你的實際場景**。挑 1 條就好。

- [ ] 🔬 **for-researcher** · [`branches/for-researcher.md`](branches/for-researcher.md)
- [ ] 💻 **for-developer** · [`branches/for-developer.md`](branches/for-developer.md)
- [ ] 🎓 **for-teacher** · [`branches/for-teacher.md`](branches/for-teacher.md)
- [ ] 📊 **for-knowledge-worker** · [`branches/for-knowledge-worker.md`](branches/for-knowledge-worker.md)
- [ ] 👥 **for-everyday-users** · [`branches/for-everyday-users.md`](branches/for-everyday-users.md)

---

## 結業專題 / Capstone

走完一條軌道後,做一個能展示的作品 + 自評。題目、必要條件、四級評分 rubric 全在 [`CAPSTONE.md`](CAPSTONE.md)——這份清單只放打勾入口,標準不重複。

- [ ] **Track A Capstone** — 組一條會重複用的 CLI-agent 工作流 · [`CAPSTONE.md`](CAPSTONE.md)
- [ ] **Track B Capstone** — build + **評測** 一個 multi-agent / RAG 系統 · [`CAPSTONE.md`](CAPSTONE.md)

---

## 一條最短可行路線(如果你只想要一個建議)

不想自己排?照這個走,大約能在最少繞路下到「能動手做事」:

`Stage 0 → Stage 1 → Stage 2 →` 選軌道 `→`（Track A：`A1 → A2 → Stage 5 → A3 → Stage 8`；Track B：`Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7 → 7.5 → 8`）`→` 你的 branch `→` 你那軌的 **Capstone**（見 [`CAPSTONE.md`](CAPSTONE.md)）。Track A 做完 A3 就能開始 Capstone；Stage 8 建議完成，但不擋入場。

---

> 這份清單只追蹤「你走到哪」。每一站「學什麼 / 進入前要會什麼 / 怎麼算學會」一律以該 stage 檔案內的「學習目標 / 進入條件 / 自我檢查」為準——避免同一份標準散兩處。

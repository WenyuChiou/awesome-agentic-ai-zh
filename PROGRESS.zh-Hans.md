# 学习进度追踪 / Progress Tracker

> [繁體中文](./PROGRESS.md) | **简体中文** | [English](./PROGRESS.en.md)

这是一份**给你自己用**的打勾清单——不用提交、不用 PR、没人会检查。复制一份（或 fork repo）勾你自己的进度，知道走到哪、下一站是哪。

**怎么用**：

1. 每个 stage 的“学习目标”“进入条件”“自我检查”都在该 stage 文件里——这份清单只是**总览 + 入口**，不重复内容。
2. 一个 stage 的 ✅ 条件 = 你能通过该 stage 结尾的“**自我检查**”那一节。通过了才勾，勾完往下一站。
3. 不用全部做完。先选一条轨道（Track A 或 B）+ 一条你的 audience branch 就够开始。

> 不确定选哪条？看 [`README.zh-Hans.md`](README.zh-Hans.md) 的双轨说明，或 [`branches/DESIGN.md`](branches/DESIGN.md)。卡住开 [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions)。

---

## 共用基础（两条轨道都要）

- [ ] **Stage 0 — 基础准备** · [`stages/00-foundations.zh-Hans.md`](stages/00-foundations.zh-Hans.md)
  ✅ 通过该 stage 的通过条件（Stage 0 是 prerequisite gateway，通过条件见 stage 内说明）

- [ ] **Stage 1 — LLM 基础** · [`stages/01-llm-basics.zh-Hans.md`](stages/01-llm-basics.zh-Hans.md)
  ✅ 通过该 stage 的“自我检查”

- [ ] **Stage 2 — Prompt 设计** · [`stages/02-prompt-engineering.zh-Hans.md`](stages/02-prompt-engineering.zh-Hans.md)
  ✅ 通过该 stage 的“自我检查”

---

## Track A — CLI Power User

> 你想“**用** agent 工具把工作做完”，不一定要自己 build。

- [ ] **A1 — CLI Agent 入门 + 选择** · [`tracks/cli/A1-cli-intro.zh-Hans.md`](tracks/cli/A1-cli-intro.zh-Hans.md)
- [ ] **A2 — CLI Workflow Patterns** · [`tracks/cli/A2-cli-workflow.zh-Hans.md`](tracks/cli/A2-cli-workflow.zh-Hans.md)
- [ ] **Stage 5 — Claude Code 生态(两轨共用)** · [`stages/05-claude-code-ecosystem.zh-Hans.md`](stages/05-claude-code-ecosystem.zh-Hans.md)
- [ ] **A3 — Integration & Production** · [`tracks/cli/A3-cli-production.zh-Hans.md`](tracks/cli/A3-cli-production.zh-Hans.md)
- [ ] **Stage 8 — Agent 操作界面（建议；不影响 Track A Capstone 入场）** · [`stages/08-agent-interfaces.zh-Hans.md`](stages/08-agent-interfaces.zh-Hans.md)

---

## Track B — Agent Builder

> 你想“**自己 build** agent / 框架 / 多 agent 系统”。

- [ ] **Stage 3 — 工具使用与第一个 Agent Loop** ⭐ · [`stages/03-tool-use-and-hello-agent.zh-Hans.md`](stages/03-tool-use-and-hello-agent.zh-Hans.md)
- [ ] **Stage 4 — Workflow Graph 与 Agent 框架** · [`stages/04-agent-frameworks.zh-Hans.md`](stages/04-agent-frameworks.zh-Hans.md)
- [ ] **Stage 5 — Claude Code 生态** ⭐⭐(两轨共用)· [`stages/05-claude-code-ecosystem.zh-Hans.md`](stages/05-claude-code-ecosystem.zh-Hans.md)
- [ ] **Stage 6 — 上下文管理：RAG 与 Memory** · [`stages/06-memory-rag.zh-Hans.md`](stages/06-memory-rag.zh-Hans.md)
- [ ] **Stage 7 — Agent 上线工程：可测、可看、可停、可恢复** · [`stages/07-multi-agent-production.zh-Hans.md`](stages/07-multi-agent-production.zh-Hans.md)
- [ ] **Stage 7.5 — 进阶 Agentic 概念** · [`stages/07.5-advanced-agentic-concepts.zh-Hans.md`](stages/07.5-advanced-agentic-concepts.zh-Hans.md)
- [ ] **Stage 8 — Agent 操作界面(两轨共用)** · [`stages/08-agent-interfaces.zh-Hans.md`](stages/08-agent-interfaces.zh-Hans.md)

---

## 选一条 audience branch（对应你的身份）

> Branch 不是“再上一层课”，是把上面 stage 学到的东西**对应到你的实际场景**。挑 1 条就好。

- [ ] 🔬 **for-researcher** · [`branches/for-researcher.zh-Hans.md`](branches/for-researcher.zh-Hans.md)
- [ ] 💻 **for-developer** · [`branches/for-developer.zh-Hans.md`](branches/for-developer.zh-Hans.md)
- [ ] 🎓 **for-teacher** · [`branches/for-teacher.zh-Hans.md`](branches/for-teacher.zh-Hans.md)
- [ ] 📊 **for-knowledge-worker** · [`branches/for-knowledge-worker.zh-Hans.md`](branches/for-knowledge-worker.zh-Hans.md)
- [ ] 👥 **for-everyday-users** · [`branches/for-everyday-users.zh-Hans.md`](branches/for-everyday-users.zh-Hans.md)

---

## 结业专题 / Capstone

走完一条轨道后,做一个能展示的作品 + 自评。题目、必要条件、四级评分 rubric 全在 [`CAPSTONE.zh-Hans.md`](CAPSTONE.zh-Hans.md)——这份清单只放打勾入口,标准不重复。

- [ ] **Track A Capstone** — 组一条会重复用的 CLI-agent 工作流 · [`CAPSTONE.zh-Hans.md`](CAPSTONE.zh-Hans.md)
- [ ] **Track B Capstone** — build + **评测** 一个 multi-agent / RAG 系统 · [`CAPSTONE.zh-Hans.md`](CAPSTONE.zh-Hans.md)

---

## 一条最短可行路线（如果你只想要一个建议）

不想自己排？照这个走，大约能在最少绕路下到“能动手做事”：

`Stage 0 → Stage 1 → Stage 2 →` 选轨道 `→`（Track A：`A1 → A2 → Stage 5 → A3 → Stage 8`；Track B：`Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7 → 7.5 → 8`）`→` 你的 branch `→` 你那轨的 **Capstone**（见 [`CAPSTONE.zh-Hans.md`](CAPSTONE.zh-Hans.md)）。Track A 做完 A3 就能开始 Capstone；Stage 8 建议完成，但不影响入场。

---

> 这份清单只追踪“你走到哪”。每一站“学什么 / 进入前要会什么 / 怎么算学会”一律以该 stage 文件内的“学习目标 / 进入条件 / 自我检查”为准——避免同一份标准散两处。

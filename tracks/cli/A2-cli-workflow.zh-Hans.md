# A2 — 建立可重复使用的 CLI 工作流程（CLI Workflow Patterns）

> [繁體中文](./A2-cli-workflow.md) | **简体中文** | [English](./A2-cli-workflow.en.md)

> [← A1 — CLI 入门](A1-cli-intro.zh-Hans.md) · **Track A: CLI Power User** 第 2 站

⏱ **时间估算**：1-2 周（约 8-15 小时）

> 📋 **本章组成**：学习目标 → 进入条件 → 必修阅读 → 动手练习 → 精选 Projects → 自我检查
> 🔑 **关键名词**：见 [`resources/glossary.zh-Hans.md` 5](../../resources/glossary.zh-Hans.md#5-claude-code-生态)（CLAUDE.md / slash command / SKILL.md / plugin / portable prompt）

装好 CLI、跑过第一个任务之后，下一个问题：**怎么让 CLI 一致地、可重复地、可分享地做事**？这节讲 workflow pattern——把“我每次都要重打一遍 prompt”变成“设好一次后 CLI 自己会用对方法”。

## 📌 学习目标

- 写一份实用的 `CLAUDE.md` / `AGENTS.md`——实用的最低构成：**(1) 角色** + **(2) 项目背景** + **(3) 禁止事项** + **(4) 测试指令** + **(5) 交付格式**。实务上 30-50 行可同时涵盖这 5 件事；超过 50 行通常该拆文件
- 设计可重复的 slash command / custom prompt
- 把多步骤任务拆成 CLI 能跑完的小步骤
- 设计 prompt 让任务在不同 CLI 上 portable

## 🚪 进入条件

你应该已经：

- 完成 [A1](A1-cli-intro.zh-Hans.md)：选定主用 CLI、装好、认证好、跑过至少 5 个非 hello-world 任务
- 写过 1 份 `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`（即使只是试水温）
- 对 Stage 2 prompt engineering 基础上手

没到的话 → 先回 [A1](A1-cli-intro.zh-Hans.md) 把 CLI-1/2 练熟。

## 📚 必修阅读

1. [**Anthropic — CLAUDE.md best practices**](https://code.claude.com/docs/en/memory) ⭐
2. [**Stage 2 — Prompt 设计**](../../stages/02-prompt-engineering.zh-Hans.md) — workflow design 跟 prompt design 是同一件事的两面
3. [**Stage 5.1 — Claude Code 基础**](../../stages/05-claude-code-ecosystem.zh-Hans.md#51--claude-code-基础) — slash commands 细节
4. [**`resources/cli-agents-guide.zh-Hans.md`** “跨 CLI 都通用的 prompt 写法”](../../resources/cli-agents-guide.zh-Hans.md) — portable prompt 原则

## 🛠 动手练习

### 动手练习 CLI-5：写 production CLAUDE.md
你 CLAUDE.md 应该至少包含：

- **角色**：“你是一个 senior Python engineer / 学术写作为助手 / 等”
- **这个 repo 的 context**：是什么项目、用什么套件、有什么 convention
- **不能做的事**：别乱改 main、别动 secrets、别 commit
- **怎么做事**：先 plan、跑 test 再 commit、要写 type hint
- **常用指令**：怎么跑 test、怎么 lint、怎么 deploy

把这份提交到 git。下次新成员 clone repo，他的 Claude Code 自动加载你的 convention。

### 动手练习 CLI-6：第一个 slash command
写 `.claude/commands/review.md`（或对应 CLI 的位置）：
```markdown
---
name: review
description: Review staged changes for security + style
---

请执行以下流程：
1. `git diff --cached` 抓 staged 的 changes
2. 找：hard-coded secrets、SQL injection、type errors
3. 对应 CLAUDE.md 内的 style 规则检查
4. 输出：PASS / 或 list of 具体要改的点
```
之后每次 `/review`，CLI 都跑同一套流程。

### 动手练习 CLI-7：多步骤任务拆解
给 CLI 一个复杂任务（譬如“把这 50 个 markdown 翻译成英文 + 加 frontmatter + 移到 en/ 子目录”）。

- 第一次：直接丢整个任务 → 观察 CLI 怎么做、什么地方会错
- 第二次：你先拆成 5 个 sub-task，逐一给 CLI → 观察结果差别
- 学到：CLI 跟你一样，太大的任务要拆；给太小的任务又会 over-orchestrate

> ⭐ **进阶补充：Claude Code 原生 multi-agent 机制**（这 1 句先看就好，不展开）：CLI-7 教的“手动拆 sub-task”其实 Claude Code 有 **Subagent / Agent team / Background agent** 三种原生工具可以自动化。完整 3 种机制 + 动手练习 + 何时不该用（团队权限、上下文隔离、结果审查流程都要先想好）见 **[Stage 5.5](../../stages/05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能)**——在 A2 阶段先知道有这层，不需要学细节。

### 动手练习 CLI-8：Portable prompt
写一个 prompt 给 Claude Code 跑成功了。**换到 Codex / OpenCode / Gemini CLI 跑同一个 prompt**——什么地方需要改？通常会发现：

- file path convention 不同（cwd vs absolute）
- 对“执行 shell”的权限默认不同
- “先 plan 再做”的 prompt 在某些 CLI 要明确说，在某些是默认行为

把这些差异整理成你自己的 cheat sheet。

## 🎯 精选 Projects

按用途分 4 类、7 个项目一张表搞定。**挑入口看“适合谁”、想深入细节点链接看 repo**。

| 分类 | Project | ⭐ | 适合谁 | 为什么推荐 / 备注 |
|---|---|---|---|---|
| **CLAUDE.md 范例库** | [Anthropic 官方 CLAUDE.md 指南](https://code.claude.com/docs/en/memory) | ⭐⭐⭐⭐⭐ | 第一份 CLAUDE.md 从这抄结构 | 官方 — Claude Code memory / CLAUDE.md 编写的官方说明，含 best practices；就是 Claude Code repo 自己的 CLAUDE.md、官方写法 |
| | [obra/superpowers](https://github.com/obra/superpowers) | ⭐⭐⭐⭐ | 看实际在用的 `.claude/` 完整目录结构 | 不只是 skill collection，也是 production CLAUDE.md 范本（★ 265k+） |
| | [mattpocock/skills](https://github.com/mattpocock/skills) | ⭐⭐⭐⭐ | 想看工程师日常用的 skill 库 | `.claude/` structure 是好参考。**更多 skill 范例见 [Stage 5.3 — Skills](../../stages/05-claude-code-ecosystem.zh-Hans.md#53--skillsclaude-code-的行为层-claude-code-生态最关键的一层)** |
| **Slash Commands / Custom Prompts** | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | ⭐⭐⭐⭐⭐ | 找官方 plugin 范本 | 官方 plugin marketplace；每个 plugin 内的 commands / skills 是 slash command 范例（★ 32k+） |
| | [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | ⭐⭐⭐ | 想逛社群 slash command 范例 | 社群整理的 Claude Code 资源清单 |
| **Prompt 设计参考** | [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) | ⭐⭐⭐⭐ | 卡关时找 CLI 通用的 prompt 模式 | 虽然是 ChatGPT 起家，prompt 写法 90% 在 CLI 上也通（★ 166k+、CC0）。完整 prompt engineering 进阶见 [Stage 2 精选 Projects](../../stages/02-prompt-engineering.zh-Hans.md#-精选-projects)（DSPy、Prompt-Engineering-Guide 等） |
| **多 CLI 并用 pattern** | [`resources/cli-agents-guide.zh-Hans.md`](../../resources/cli-agents-guide.zh-Hans.md) “3 个常见搭配” | ⭐⭐⭐⭐ | 想试多 CLI 配对策略 | 本 repo 内部资源；看 Setup A / B / C，挑一个合的试 |

> 💡 **建议入手路径**：先抄 Anthropic 官方 CLAUDE.md 结构 → 加自己的 repo context → 看 obra/superpowers 看“完整 `.claude/` 长什么样” → 然后写 1-2 个 slash command（从 hesreallyhim awesome 列表捞灵感）。

### 推荐工具

- [**yamadashy/repomix**](https://github.com/yamadashy/repomix) ⭐⭐⭐⭐⭐ ★ 27k+ — 把整个 codebase packed 成单个 AI-friendly 文件（XML / Markdown / JSON），方便 Claude Code / Codex 做 code review / refactoring。带 MCP server mode + tree-sitter 压缩（压缩率依语言与文件结构而异）+ secretlint 过滤敏感信息。**Track A 的必备 daily-driver 工具。**
- [**langchain-ai/openwiki**](https://github.com/langchain-ai/openwiki) ⭐⭐⭐⭐ ★ 15k+ — CLI，自动帮你的 codebase 生成并持续维护一份 wiki，并在 `CLAUDE.md` / `AGENTS.md` 里加一条指向 wiki 的引用，让 coding agent 需要时自己去读、随代码变动自动更新。`npm i -g openwiki` → `openwiki --init`。底层是 DeepAgents、可接 LangSmith 追踪。MIT。

> 💡 **概念：*agent-facing documentation*（给 agent 读的文档）。** repomix 跟 OpenWiki 在解同一个痛点（agent 不了解你的 repo），只是切角不同：一个是一次性打包快照，一个是会持续长大、自动维护的 wiki。共同的做法是给 agent *一份它需要时自己去读的结构化 codebase context*，跟 `CLAUDE.md` 的指令分开放，而不是全部塞进 prompt。

## ✅ 进 A3 前的自我检查

你能不能：

- [ ] 写过至少 1 份你 production / 工作 repo 的 CLAUDE.md（不是 demo repo）
- [ ] 写过至少 2 个 slash command 并实际在用
- [ ] 把同一个 prompt 在 2 个不同 CLI 上跑过、知道差异
- [ ] 讲得出“什么任务该拆、什么任务不该拆”的判准

如果可以 → 进 [A3 — Integration & Production](A3-cli-production.zh-Hans.md)。

如果不行 → CLAUDE.md 一直 demo 等于白写；先去你真实 repo 写一份再回来。

## 💡 常见坑

- **CLAUDE.md 写太长**：超过 100 行 CLI 会自己 truncate / 忽略后段。Sweet spot 30-60 行。
- **Slash command 写成“请做 X、Y、Z、A、B”一句**：CLI 容易跳步骤。改写成编号 list + 每步成功标准。
- **Portable 过头**：每个 CLI 还是有自己的特长；不要为了能跨 CLI 把 prompt 变得太抽象、失去具体性。
- **觉得自己“都会”就不写了**：CLAUDE.md 是给未来的你（跟新成员）看的，不是给现在的你看的。

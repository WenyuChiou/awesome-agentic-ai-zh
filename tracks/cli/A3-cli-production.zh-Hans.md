# A3 — 把 CLI Agent 接进真实工作流程（Integration & Production）

> [繁體中文](./A3-cli-production.md) | **简体中文** | [English](./A3-cli-production.en.md)

> [← A2 — CLI Workflow Patterns](A2-cli-workflow.zh-Hans.md) · **Track A: CLI Power User** 第 3 站（最后）

⏱ **时间估算**：1-2 周（约 8-15 小时）

> 📋 **本章组成**：学习目标 → 进入条件 → 必修阅读 → 动手练习 → 精选 Projects → 自我检查
> 🔑 **关键名词**（本章用到）：
> - **本章一定会用**：MCP（让 CLI 接外部数据 / 工具）、CI（每次 push 自动跑检查）
> - **延伸阅读名词**：observability（追踪 CLI 行为）、eval（量化 CLI 质量）、prompt caching（重复 context 省钱）、cost tracking（token 花费记录）
>
> 完整定义见 [`resources/glossary.zh-Hans.md` 5 + 6](../../resources/glossary.zh-Hans.md#5-claude-code-生态)。

CLI 跑得顺了之后，下一步：**把 CLI 接到你的真实团队流程**。这节达成 3 件事：

1. **工具连接** — MCP server 把 CLI 接到 Slack / Gmail / 你的 internal API
2. **自动检查** — CI（GitHub Actions）每个 PR 自动跑 CLI review
3. **成本与记录** — observability 工具追踪每个任务的 cost / latency

这节之后，CLI 不只是你个人的工具，而是 team 工作流的一部分。

## 📌 学习目标

- 把 1-3 个 MCP server 接到你的 CLI（Slack / Gmail / 你的 internal API / DB）
- 设置 GitHub Actions 自动跑 Claude Code（PR review、release notes 等）
- 加 observability（trace、cost、latency）到 CLI workflow
- 规划 cost budget，知道大 task 会花多少 token

## 🚪 进入条件

你应该已经：

- 完成 [A1](A1-cli-intro.zh-Hans.md)：CLI 已选好、装好、认证好
- 完成 [A2](A2-cli-workflow.zh-Hans.md)：完成项目规则卡和 review Skill
- 对 GitHub Actions / CI 基础熟悉（会看 `.yml` workflow）
- 对 MCP 概念有印象（没有的话先翻 [Stage 5.2](../../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础)）

没到的话 → 补完 [A1](A1-cli-intro.zh-Hans.md) + [A2](A2-cli-workflow.zh-Hans.md)。A3 是“组合所有前面学的 → 接到 production”，跳级会看不懂。

## 📚 必修阅读

1. [**Stage 5.2 — MCP（Model Context Protocol）**](../../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础) — MCP 概念跟基础
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — 在符合缓存条件时（context 不变、≤ 5 分钟 reuse window 等）可大幅降低重复上下文的成本；实际比例依工作流而异，请以官方文章的条件为准
3. [**Stage 7 — Observability section**](../../stages/07-multi-agent-production.zh-Hans.md#练习-3observability) — langfuse / Helicone / weave
4. [**`resources/cli-agents-guide.zh-Hans.md`** “常见坑”](../../resources/cli-agents-guide.zh-Hans.md) — production 用 CLI 最常踩的问题

## 🛠 动手练习

### 动手练习 CLI-9：MCP server 接 CLI
照 [Stage 5.2 练习：MCP client](../../stages/05-claude-code-ecosystem.zh-Hans.md#动手练习) 的步骤，把至少一个有用的 MCP server 接到你的 CLI：

- `filesystem` server → 让 CLI 在指定目录外也能读文件
- `github` server → 让 CLI 直接读 PR / issue
- 自架 server → 接你的 internal API / DB

成功标准：在 CLI 对话里直接问“我这个 PR 有 conflict 吗”，CLI 通过 MCP 回答你（不用你开浏览器）。

### 动手练习 CLI-10：GitHub Actions + CLI
写一个 `.github/workflows/cli-review.yml`：

- 触发：PR opened / synchronize
- 跑：在 GH Actions runner 内执行 Claude Code（或 Codex），给它 `git diff`，并请它使用 A2 做好的 [`review-changes` Skill](A2-cli-workflow.zh-Hans.md#动手练习-cli-6把重复-review-做成-skill)
- 输出：PR comment

成功标准：开新 PR，1-2 分钟内 PR 出现 review comment。

> 起点：Anthropic 官方有 [`claude-code-action`](https://github.com/anthropics/claude-code-action)（GitHub Actions 集成）；Codex 有 GitHub App 跟 CLI 两种模式。

### 动手练习 CLI-11：Cost tracking
跑你日常的一个 task，**先预估** token 用量，再实际跑、查 token usage。差距通常很大（多半你低估）。

- 算式：input tokens + output tokens 各乘以 model 单价
- 接 langfuse 或 Helicone（[Stage 7 Observability section](../../stages/07-multi-agent-production.zh-Hans.md#练习-3observability)）做 trace
- 观察：哪个 sub-task 花最多 token？是不是有不必要的 long context？

### 动手练习 CLI-12：Skill / plugin 跨 team 分享
把 A2 的 `review-changes` Skill 放进 plugin 根目录的 `skills/review-changes/SKILL.md`，再发布到内部 marketplace 或 GitHub。Team 其他人安装 plugin 后，就能取得同一个 Skill。

`CLAUDE.md` 是项目自己的说明文件，应该留在 repo；它不是这个 plugin 要打包的内容。

- Skill / plugin 细节见 [Stage 5.3 + 5.4](../../stages/05-claude-code-ecosystem.zh-Hans.md)
- 范本：[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

## 🧭 进阶概念在 CLI 日常工作中的应用（7 个 playbooks）🆕

Track A 的人**已经在用** [Stage 7.5 的进阶概念](../../stages/07.5-advanced-agentic-concepts.zh-Hans.md)，只是没给它命名。下面挑 **最常用 2-3 个 playbook** 细看，其余折叠为延伸阅读——每个 ≤ 6 行。**想深挖原理 → 进 Stage 7.5。**

> 📌 **规则**：每个 playbook 看完先问自己“下一个 PR 我会做不一样的事吗？”**会** → applied；**不会** → 跳下一个。

### 📋 Playbook 1：任务 scope 不明，agent 越界

- **When**：派 Codex/Gemini 跑 sweep，不确定它会不会擅自改别的档（F11/F12 那种）
- **Do**：brief 开头明写“动 X / 不能跨 Y”，acceptance preset 加 path filter
- **Concepts**：Work Boundary + Hierarchical Task Decomposition · 📊 图见 [concept-cluster](../../resources/diagrams/concept-cluster.zh-Hans.png) Service × 编排 cluster
- **Read more**：

  | Source | Link |
  |---|---|
  | HumanLayer | [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) |
  | Anthropic | [How Anthropic teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) |
  | 内部 | [Stage 7.5 🧭 work boundary stack](../../stages/07.5-advanced-agentic-concepts.zh-Hans.md#-概念地图主轴四层工作边界work-boundary) |

### 📋 Playbook 2：多 agent 并行，结果乱

- **When**：Claude planner + 2-3 Codex 并行跑，结果 merge 冲突 / drift
- **Do**：每个 agent 自己一个 commit，用 reviewer pattern 抓 drift（不是大合一）；brief 统一 task format + result.json schema
- **Concepts**：Contract Hand-offs + Speculative Parallel · 📊 图见 [concept-cluster](../../resources/diagrams/concept-cluster.zh-Hans.png) Service × 编排 + Types × 编排
- **Read more**：

  | Source | Link |
  |---|---|
  | Addy Osmani | [Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/) |
  | Daniel Vaughan | [Running Multiple Codex Agents Parallel](https://codex.danielvaughan.com/2026/04/18/running-multiple-codex-agents-parallel-orchestration/) |
  | 内部 | [agent-collab-skills](https://github.com/WenyuChiou/agent-collab-skills)（`agent-task-splitter` + `agent-output-reconciler`） |

### 📋 Playbook 3：Review agent 输出

- **When**：agent 写完 PR，不放心直接 merge，人工 review 跟不上吞吐
- **Do**：加 LLM-as-judge subagent 自动评（binary pass/fail），人类只 spot-check edge case；commit 前跑 acceptance-gate preset
- **Concepts**：Agent-as-Judge + Plan-Act-Reflect · 📊 图见 [reading-decision-tree](../../resources/diagrams/reading-decision-tree.zh-Hans.png) 蓝色 eval 分支
- **Read more**：

  | Source | Link |
  |---|---|
  | Hamel Husain | [LLM-as-a-Judge: Complete Guide](https://hamel.dev/blog/posts/llm-judge/) |
  | Hamel Husain | [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) |
  | Simon Willison | [Sub-agents in Claude Code](https://simonwillison.net/2025/Oct/11/sub-agents/) |

### 📋 Playbook 4：派遣 subagent 跑独立任务

> 💡 **第一次听到 subagent？** 一句话：**subagent = 主 Claude session spawn 出来的“子 Claude”**，有自己独立的 context，跑完回报结果。**派遣（dispatch）**就是叫 subagent 去做事——像派任务给同事。完整概念 → [Stage 5.5](../../stages/05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能)。

- **When**：写了大改动要 commit 前 / 进新 repo 不熟结构 / 想跑 LLM-as-judge 自动评估 / 4 个目标要做同样审查
- **Do**：调用 Claude Code **内置** subagent（不用自己写任何文件）：
  - `code-reviewer` — review staged diff、找 bug + security
  - `Explore` — 只读搜索 codebase、找 entry point / symbol
  - `Plan` — 设计 step-by-step 实作计划
  - `general-purpose` — 不确定该用哪个 / 多步骤研究的 fallback
- **Concepts**：Hierarchical Task Decomposition + Context Isolation · 📊 图见 [concept-cluster](../../resources/diagrams/concept-cluster.zh-Hans.png) Service × 编排 cluster
- **Read more**：
  - [Stage 5.5 Subagents](../../stages/05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能)（完整理论 + decision table）
  - [`resources/subagent-cookbook.zh-Hans.md`](../../resources/subagent-cookbook.zh-Hans.md)（**15 个 recipe**、复制粘贴即可用的 prompt 模板）

---

### 📋 Playbook 5：在 CI 里跑 CLI agent

- **When**：把 `codex exec` / `claude --print` 接进 GitHub Actions，不能每次都需要人按 yes，带宽限制也不能用 Opus
- **Do**：分层 autonomy（preset 自动跑 / commit 需审 / push 需人签），设 fallback 便宜 model（Opus 挂了就 fallback Haiku）
- **Concepts**：Autonomy Gradients + Graceful Degradation · 📊 图见 [concept-cluster](../../resources/diagrams/concept-cluster.zh-Hans.png) Config × 治理 cluster
- **Read more**：

  | Source | Link |
  |---|---|
  | Anthropic | [How Anthropic teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) |
  | Anthropic Engineering | [Equipping Agents with Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) |
  | 内部 | [Stage 5.5 Subagents](../../stages/05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能) + 动手练习 CLI-10 |

### 📋 Playbook 6：控制成本

- **When**：用 Codex 跑大批 work，每月 API 账单失控，想压在 budget 内
- **Do**：`plan.yml` 设 `max_cost_usd`，便宜 model（Haiku）跑探索 / 贵 model（Opus）只跑 polish；开 prompt caching（符合缓存条件时可大幅降低重复 context 成本）；自动化 QA（不靠人时间）
- **Concepts**：Cost-aware Budget Gates + Throughput-Merge Philosophy · 📊 图见 [concept-cluster](../../resources/diagrams/concept-cluster.zh-Hans.png) Config × 韧性 cluster
- **Read more**：

  | Source | Link |
  |---|---|
  | Simon Willison | [Sub-agents](https://simonwillison.net/2025/Oct/11/sub-agents/) |
  | Anthropic | [Prompt Caching](https://www.anthropic.com/news/prompt-caching) |
  | 内部 | 本 stage 动手练习 CLI-11（token tracking + langfuse 集成） |

### 📋 Playbook 7：强化 workflow，防 drift

- **When**：CLAUDE.md / SKILL.md rule 写了但没人 enforce，preset YAML 加了也不知道有没有效
- **Do**：故意 break 一条 rule 跑 acceptance gate 看抓不抓得到（chaos test）；`docs/` 当 single source，CLAUDE.md 只当 entry map
- **Concepts**：Failure Injection + System of Record · 📊 图见 [failure-lifecycle](../../resources/diagrams/failure-lifecycle.zh-Hans.png)（F11-F14 进化循环）
- **Read more**：

  | Source | Link |
  |---|---|
  | HumanLayer | [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) |
  | agent-collab-skills | [observed-failure-modes.md](https://github.com/WenyuChiou/agent-collab-skills/blob/main/docs/observed-failure-modes.md) |
  | 内部 | [Stage 7.5 🔁 failure-mode lifecycle](../../stages/07.5-advanced-agentic-concepts.zh-Hans.md#-failure-mode-lifecycle产业级-agent-失败模式怎么演化成最佳实践) |

---

→ **7 个 playbook = 7 个 trigger × 12 个 concept ×“对应 reading source”的桥梁**。深挖原理 / 看完整 12 个 concept 跟 8 个 cross-vendor 原则 → [Stage 7.5](../../stages/07.5-advanced-agentic-concepts.zh-Hans.md)。

## 🎯 精选 Projects

按用途分 4 类、9 个项目一张表搞定。**挑入口看“适合谁”，想深入细节点链接看 repo**。

> 💡 **要找接日常工具的 MCP**（Notion / Obsidian / Excel / Postgres / Playwright / Slack / Linear / Figma 等）：[`resources/mcp-skills-catalog.zh-Hans.md`](../../resources/mcp-skills-catalog.zh-Hans.md)——81+ 个分类整理，每个都有 stars / license / 适合谁。下表只列“写自己 MCP server / 找 reference”用的核心 catalog。

| 分类 | Project | ⭐ | 适合谁 | 为什么推荐 / 备注 |
|---|---|---|---|---|
| **MCP server collection**<br>（接 CLI 用） | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | ⭐⭐⭐⭐⭐ | 第一个 MCP 从 reference 学起 | 官方 reference servers（现有 7 个：everything、fetch、filesystem、git、memory、sequentialthinking、time；github、sqlite 已移到 `servers-archived`），★ 89k+。详见 [Stage 5.2](../../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础) |
| | [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) | ⭐⭐⭐⭐ | 想找特定领域的社群 MCP | 社群 MCP server catalog、150+ 个依分类整理 |
| **CI 集成 patterns** | [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) | ⭐⭐⭐⭐⭐ | 第一个 CI workflow 从官方范本起步 | 官方 GitHub Action 范本、PR review / issue triage / 自动 fix |
| | [continuedev/continue](https://github.com/continuedev/continue) | ⭐⭐⭐⭐ | 想把 AI checks 接到 PR pipeline 强制执行 | ★ 35k+。完整介绍见 [`branches/for-developer.zh-Hans.md`](../../branches/for-developer.zh-Hans.md) |
| **Observability + Cost** | [langfuse/langfuse](https://github.com/langfuse/langfuse) | ⭐⭐⭐⭐⭐ | 想把 trace、cost、session 都接起来 | open source LLM observability，★ 32k+。详见 [Stage 7 Observability](../../stages/07-multi-agent-production.zh-Hans.md#练习-3observability) |
| | [Helicone](https://github.com/Helicone/helicone) | ⭐⭐⭐⭐ | 想要最快的 logging（改 base_url 就好） | proxy-based 监控、改 base_url 就有 logging + caching，★ 6k+ |
| | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | ⭐⭐⭐⭐⭐ | CLI workflow 升级到 production 前跑回归测试 | eval framework，★ 24k+。详见 [Stage 7 Eval](../../stages/07-multi-agent-production.zh-Hans.md#练习-2eval) |
| **Production CLI workflow 范本** | [obra/superpowers](https://github.com/obra/superpowers) | ⭐⭐⭐⭐ | 看完整实际在用的 workflow 长什么样 | 整套 production-ready skill collection、★ 265k+。看别人怎么把 CLI workflow 做完整 |
| | [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) | ⭐⭐⭐ | 要把 team 的 CLI workflow 打包共用 | 最简 marketplace template、★ 1.2k+ |

> 💡 **建议入手路径**：先从 `modelcontextprotocol/servers` 挑一个 reference MCP 接到 CLI → 用 `claude-code-action` 跑第一个 CI workflow → 加 langfuse 看 trace + cost → production 规模化时把 workflow 打包成 marketplace plugin。

## ✅ Track A 完整通关自我检查

你能不能：

- [ ] 已有至少 1 个 MCP server 接到你日常 CLI
- [ ] 已有至少 1 个 CI workflow 在自动跑 CLI agent
- [ ] 你能讲出某个 task 跑下去的 token 用量、cost、latency 大致范围
- [ ] 把至少一个 Skill 放进 plugin 的 `skills/<name>/SKILL.md`，并验证安装后能找到它（即使只有自己用）
- [ ] 知道什么任务值得加 observability、什么不值得

如果都可以 → **Track A 完整通关**。建议接着走 [**Stage 8 — Agent Interfaces**](../../stages/08-agent-interfaces.zh-Hans.md)（**两 track 共用 hub**：Computer Use / Browser Use / Code Sandbox，Track A 视角约 1-2 周），或挑一个 [specialized branch](../../README.zh-Hans.md#-学习地图两条学习路径) 继续走（researcher / developer / teacher / knowledge-worker / everyday-users）。

如果想再深入“**怎么写自己的 CLI agent**”（不是用现有的）→ 跳到 [Track B Stage 3](../../stages/03-tool-use-and-hello-agent.zh-Hans.md) 开始。Track A 跟 Track B 互补。

## 💡 接下来

走完 Track A 你已经是 CLI power user。下一阶段选择：

1. **加深 CLI workflow**（持续优化你的 setup）
   - 订阅 Anthropic / OpenAI changelog
   - 每季 review 一次 [`resources/cli-agents-guide.zh-Hans.md`](../../resources/cli-agents-guide.zh-Hans.md) 看新工具
   - 跟你 team 分享 CLAUDE.zh-Hans.md / skills

2. **跨到 Track B**（学怎么写自己的 agent）
   - Stage 3-4 学 tool use + framework
   - Stage 5 深挖 Claude Code 内部运作
   - Stage 7 写自己的 multi-agent system

3. **走 specialized branch**（把 CLI 应用在特定领域）
   - 研究人员 / 开发人员 / 知识工作者 / 教师 / 日常用户
   - 各 branch 都会用到 Track A 学的东西

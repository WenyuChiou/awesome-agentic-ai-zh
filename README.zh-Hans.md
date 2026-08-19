<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

<div align="center" markdown="1">

![AI Agent 学习路径](resources/diagrams/banner.zh-Hans.png)

# awesome-agentic-ai-zh

### 🤖 AI Agent 学习地图 — 从基础 LLM 概念到自己构建多 agent 系统

<p><em><b>学习路线图 + 240+ 资源 curation + 简单 illustrative 案例</b><br/>结构化 8 阶段、从“LLM 是什么、token 怎么算”走到 multi-agent 编排、Computer Use / Browser Use / Sandbox</em></p>

[![License](https://img.shields.io/badge/license-MIT-blue?style=flat)](LICENSE)
[![繁中](https://img.shields.io/badge/语言-繁體中文-red?style=flat)](README.md)
[![简中](https://img.shields.io/badge/语言-简体中文-orange?style=flat)](README.zh-Hans.md)
[![EN](https://img.shields.io/badge/lang-English-blue?style=flat)](README.en.md)
![GitHub stars](https://img.shields.io/github/stars/WenyuChiou/awesome-agentic-ai-zh?style=flat&logo=github)
![GitHub forks](https://img.shields.io/github/forks/WenyuChiou/awesome-agentic-ai-zh?style=flat&logo=github)
[![在线文档站](https://img.shields.io/badge/在线文档站-Pages-2ea44f?style=flat)](https://wenyuchiou.github.io/awesome-agentic-ai-zh/)

</div>

> 📱 **用手机看的话，建议走[在线文档站](https://wenyuchiou.github.io/awesome-agentic-ai-zh/)而不是这一页。** 内容一样，但站上的表格会随屏幕折行、不用左右拖，另外有跨页搜索与侧边目录。桌面端两边都好读，手机上差得多。

---

## 🎯 项目介绍

**本 repo 角色定位**：**学习路线图 + 240+ 资源 curation + 简单 illustrative 案例**——三件事为核心、帮想学 AI / AI agent 的人从“不知道从哪开始”走到“能设计多 agent 系统”。

具体做法：

| 核心 | 做什么 | 规模 |
|---|---|---|
| **学习路线图** | 把网上散落的高质量项目、教材、必修阅读，按**从零开始、循序渐进**整理成 **8 个阶段**（含 Stage 5 + Stage 8 两个共用 hub）+ 2 条学习路线 + 5 条延伸路径 | 8 stages、2 tracks |
| **资源 curation** | 每阶段精选 **240+** 个 project（含星等、适合谁、教什么、怎么跑），加上中文 AI 生态(DeepSeek / Zhipu / Kimi 等)MCP / Skill 完整 catalog | 240+ projects、79 MCP/Skill |
| **简单 illustrative 案例** | 每阶段附 1-5 个**基础练习**（70-150 行 starter + dual-path Ollama/Anthropic SDK 对照 + mock-based test） | 23 个练习 folder |

走完这条路线，你会从“**LLM 用户**”进阶到“**agent 系统构建者**”——能看懂 framework 在做什么、能设计多 agent 协作、能写自己的 MCP server。

> 📖 **关于中英文混用**：本项目保留 AI Agent 领域常见英文术语（Prompt Engineering / Context Engineering / Harness / MCP / Skills / RAG 等），因为官方文档、paper、GitHub repo 与 API 文档多以英文为主。每个重要概念会提供 **中文理解名 + 英文正式术语 + 一句白话定位**，让读者能先理解概念，再对接英文生态。完整对照见 [`resources/glossary.zh-Hans.md`](resources/glossary.zh-Hans.md)。

---

## 📋 目录

- [🎯 项目介绍](#-项目介绍)
- [📚 快速开始](#-快速开始)
  - [在线阅读](#在线阅读)
  - [本地下载](#本地下载)
  - [✨ 你会收获什么？](#-你会收获什么)
- [🗺️ 学习地图（两条学习路径）](#-学习地图两条学习路径)
- [💡 如何学习](#-如何学习)
- [📚 相关资源](#-相关资源)
- [🤝 如何贡献](#-如何贡献)
- [🙏 致谢](#-致谢)
- [🎓 引用](#-引用)
- [☕ 支持这个项目](#-支持这个项目)
- [License](#license)

---

## 📚 快速开始

### 🚀 第一次接触 AI agent / 没写过 code？

先看 **[`resources/setup-guide.zh-Hans.md`](resources/setup-guide.zh-Hans.md)** — 30-45 分钟从零带你申请 API key、装好 Python、跑出第一个 LLM hello-world。

### 在线阅读
- **[学习地图（两条学习路径）](#-学习地图两条学习路径)** — 看完这节决定走 Track A 还 Track B
- **[Stage 0 基础准备](stages/00-foundations.zh-Hans.md)** — 已经会 Python / git / API 的人可以直接跳 Stage 1

### 本地下载
```bash
git clone https://github.com/WenyuChiou/awesome-agentic-ai-zh.git
cd awesome-agentic-ai-zh
# 从 stages/00-foundations.zh-Hans.md 开始
```

### ✨ 你会收获什么？

- 📖 **完全免费** — MIT 授权，所有内容开放共学
- 🗺️ **两条学习路径** — Track A（CLI Power User）给“想 USE 现成 CLI agent”的人；Track B（Agent Builder）给“想 BUILD 自己 agent”的人。共用 Stage 0-2 基础
- 🛠️ **基础动手练习** — 每阶段附 1-5 个 illustrative 练习（题目 + dual-path SDK 对照 + success criteria）。定位是**基础入门 + 路线确认**——chapter-length 深度练习见对应 stage 的 hello-agents / Anthropic Cookbook callout
- 🎯 **精选 240+ 个 projects** — 每个都附星等推荐、适合谁、教什么、怎么跑（含本地 LLM 执行：Ollama、llama.cpp、LocalAI、MLX）
- 🌏 **三语完整维护** — 繁中(canonical)/ 简中 / English,三版皆完整维护、英文非薄翻译
- 🎓 **不只“框架”、还有“Claude Code 生态”** — MCP / Skills / Plugins 完整堆叠
- 🔬 **5 条依用户分流的延伸路线** — 研究员 / 开发者 / 老师 / 知识工作者 / 日常用户
- ⏱️ **预估时程写清楚** — Track A 8-10 周 / Track B 主干最少 16-22 周、现实 5-7 个月（每周 5-8 hr）

---

## 🗺 学习地图（两条学习路径）

![AI Agent 学习地图](resources/diagrams/learning-map.zh-Hans.png)

走完 **Stage 0-2（共用基础）** 之后，依你的目的选一条学习路径：

- **Track A — CLI Power User**：你想**用**现成的 CLI agent（Claude Code、Codex、OpenCode、Gemini CLI 等）把工作做顺、效率拉高，不打算自己从零写 agent。3 个 sub-stage（A1-A3）。
- **Track B — Agent Builder**: 你想**从零构建**自己的 agent——学 framework、写 ReAct、设计 multi-agent。Stage 3-8 是主路线。

两条学习路径**不互斥**——多数人是先走 A 把 CLI 用起来，再回到 B 学内部运作；或反过来也行。Stage 5（Claude Code 生态）两条路径都会用到。

### 共用基础（Stage 0-2）

| Stage | 主题 | 关键内容 | 预估时程 |
|---|---|---|---|
| **0** | [基础准备（Foundations）](stages/00-foundations.zh-Hans.md) | Python · CLI · git · API · JSON | 1-2 周 |
| **1** | [LLM 基础（LLM Basics）](stages/01-llm-basics.zh-Hans.md) | token · API · 各家 LLM 比较 · 本地 LLM | 1 周 |
| **2** | [Prompt 设计（Prompt Engineering）](stages/02-prompt-engineering.zh-Hans.md) | 系统 prompt · few-shot · CoT | 1-2 周 |

### Track A — CLI Power User（想用 CLI 把事情做完）

| Stage | 主题 | 关键内容 | 预估时程 |
|---|---|---|---|
| **A1** | [选一个 CLI Agent，开始用它做事（CLI Agent Intro & Selection）](tracks/cli/A1-cli-intro.zh-Hans.md) | 8 个主流 CLI 比较 · 安装 · 第一次跑 | 1 周 |
| **A2** | [建立可重复使用的 CLI 工作流程（CLI Workflow Patterns）](tracks/cli/A2-cli-workflow.zh-Hans.md) | CLAUDE.md · slash command · 多步骤拆解 | 1-2 周 |
| **A3** | [把 CLI Agent 接进真实工作流程（Integration & Production）](tracks/cli/A3-cli-production.zh-Hans.md) | MCP 接 CLI · CI 自动化 · cost / observability | 1-2 周 |
| **+5** | [Stage 5 — Claude Code 生态系（Claude Code Ecosystem）](stages/05-claude-code-ecosystem.zh-Hans.md)（**共用 hub**）| MCP · Skills · Plugins · Subagents、Track A 必看 5.1-5.4 / 选读 5.5-5.7 | 1-2 周（Track A 视角）|
| **+8** | [Stage 8 — Agent 操作介面（Agent Interfaces）](stages/08-agent-interfaces.zh-Hans.md)（**共用 hub**）| Computer Use · Browser Use · Code Sandbox、Track A 视角看 Track A 怎么用 | 1-2 周（Track A 视角）|

> **Track A 预估总时程**：含 Stage 0-2（共用基础）+ A1-A3 + **Stage 5 + Stage 8（两个共用 hub）= 约 8-10 周**。核心参考：[`resources/cli-agents-guide.zh-Hans.md`](resources/cli-agents-guide.zh-Hans.md)。

### Track B — Agent Builder（想从零构建 agent）

| Stage | 主题 | 关键内容 | 预估时程 |
|---|---|---|---|
| **3** ⭐ | [工具使用与第一个 Agent（Tool Use & Hello Agent）](stages/03-tool-use-and-hello-agent.zh-Hans.md) | function calling · ReAct · 5 个动手练习 | 2-3 周 |
| **4** | [Agent 框架（Agent Frameworks）](stages/04-agent-frameworks.zh-Hans.md) | LangGraph · AutoGen · CrewAI · Smolagents | 2-3 周 |
| **5** ⭐⭐ | [Claude Code 生态系（Claude Code Ecosystem）](stages/05-claude-code-ecosystem.zh-Hans.md)（**共用 hub**、Track A 也学）| MCP · Skills · Plugins · Subagents | 3-4 周（Track B 视角）|
| **6** | [上下文管理（Context Engineering）：RAG 与 Memory](stages/06-memory-rag.zh-Hans.md) | vector DB · long-term memory · contextual retrieval | 2 周 |
| **7** | [多 Agent 系统与稳定运作（Multi-Agent & Production）](stages/07-multi-agent-production.zh-Hans.md) | multi-agent orchestration · eval · observability · SDK 进阶 | 2-4 周 |
| **7.5** | [进阶 Agentic Workflow 概念（Advanced Agentic Concepts）](stages/07.5-advanced-agentic-concepts.zh-Hans.md)（reading map）| 工作边界 · PAR loop · agent-as-judge · 12 个进阶概念 + reading list | 1 周（不写 code）|
| **8** ⭐⭐ | [Agent 操作介面（Agent Interfaces）](stages/08-agent-interfaces.zh-Hans.md)（**共用 hub**、Track A 也学）| Computer Use · Browser Use · Code Sandbox、2024-2026 frontier | 2-3 周（Track B 视角）|

> **Track B 预估总时程**：主干最少 **16-22 周**、现实 **5-7 个月**（每周 5-8 hr 兼职）

> **两个共用 hub（Track A + Track B 都会用到）**：
> - **Stage 5** = Claude Code 生态（MCP / Skills / Plugins / Subagents）—— Track A 学 MCP 接 CLI、Track B 学 agent runtime 结构
> - **Stage 8** = Agent Interfaces（Computer Use / Browser / Sandbox、2024-2026 frontier）—— Track A 学“**怎么用**”委派任务、Track B 学“**怎么 build**”embed 进 agent
>
> 两个 hub 出现在两条 track 内、视角不同、学的深度也不同（内文有 Track A / Track B 分视角段）。

> 💡 **想看跨 stage 的完整示例？** [7 步构建你的第一个 AI Agent](walkthroughs/build-first-agent-in-7-steps.zh-Hans.md) — 同一个 Paper Summary Bot 从 Stage 1 一路写到 Stage 7，~300 行真实代码（**Track B 适用**）

走完主干后，依你的身份挑一条延伸路线继续走。**不确定挑哪条？**

![Branch 决策树](resources/diagrams/branch-decision-tree.zh-Hans.png)

> 💡 **“日常用户”这条路线不必走完主干就能直接读**——是给“想用 AI、但不一定要写 code”的人。

| 路线 | 适合谁 | 主题 |
|---|---|---|
| 🔬 [研究员](branches/for-researcher.zh-Hans.md) | 研究生、博后、PI | 文献整理 · paper 写作 · multi-agent review |
| 💻 [开发者](branches/for-developer.zh-Hans.md) | 软件工程师 | Cursor · Aider · CLI delegation · code review |
| 🎓 [老师](branches/for-teacher.zh-Hans.md) | 老师、讲师 | 备课 · 幻灯片 · 学生 feedback · 隐私 / 伦理 · prompt 范本 |
| 📊 [知识工作者](branches/for-knowledge-worker.zh-Hans.md) | 顾问、PM、分析师 | Email · 会议记录 · report 自动化 |
| 👥 [日常用户](branches/for-everyday-users.zh-Hans.md) | ChatGPT / Claude.ai 用户 | 写信 · 学习 · 隐私场景 · CLI agent 入门 |

---

## 💡 如何学习

这份路线图兼顾概念与实作，目标是带你“从 LLM 用户一路走到 agent 系统构建者”。适合“有基本 Python 能力”的开发者、研究生、自学者。动手之前，先确认你有：

- 基本 Python — 写过 function、用过 API、看得懂 JSON
- 基本 git — clone、commit、push
- 想学的动机 — agent 是 2025 年之后变化最快的领域，需要持续投入

上面有缺的就从 Stage 0 补齐；都会了就直接跳 Stage 1。

主干分 5 部分：

- **Part 1（Stage 0-2）：基础与 LLM 入门** — Python / git / API、什么是 LLM、怎么设计 prompt
- **Part 2（Stage 3-4）：构建你的 Agent** — 从 tool use 进化到 agent，学主流 framework
- **Part 3（Stage 5） 共用 hub** — Claude Code 生态系（MCP / Skills / Plugins / Subagents、Track A + B 都会用到）
- **Part 4（Stage 6-7）：进阶集成** — memory / RAG / multi-agent 协作 / harness engineering
- **Part 5（Stage 8） 共用 hub** — Agent Interfaces（Computer Use / Browser Use / Code Sandbox、2024-2026 frontier、两条 track 都会用到）

> 🔭 **概念分层的演进**：**prompt engineering**（Stage 2、单一 prompt 怎么写）→ **context engineering**（Stage 3 之后、怎么动态组 system prompt + memory + retrieved chunks + tool schema）→ **harness engineering**（Stage 7、agent loop / eval / observability / deploy 整套包成 production system）。2026 之后社群又往外接了 **loop**（让它自己跑完）与 **graph**（把流程摊开来看得到）两层——**完整五层与各层目的见 [Stage 7 五层工程分工](stages/07-multi-agent-production.zh-Hans.md#五层工程分工prompt--context--harness--loop--graph)**。详见 [`stages/02-prompt-engineering.zh-Hans.md`](stages/02-prompt-engineering.zh-Hans.md) 进阶：context engineering 跟 [`stages/07-multi-agent-production.zh-Hans.md`](stages/07-multi-agent-production.zh-Hans.md) 必修阅读 5+6。

走完主干（Track B 16-22 周 / Track A 8-10 周）后，依你的身份挑一条延伸路线继续走。

最重要的说一句话：**不要跳过动手练习**。每个 stage 的动手练习都是“不动手就学不会”的东西，光读过去后面会卡住。

> 🎓 **动手练习怎么用才对**：每个练习 folder 里的 `starter.py` 是**完整解答**、不是 TODO skeleton。如果你 clone 下来直接 `cat starter.py` + `python test.py` pass、会误以为“我学会了”、其实没写一行 code。**正确学习法**：`mv starter.py starter_reference.py`、看 signature 不看 body、自己重写、卡住才回去对照。完整方法论 + 每个 stage 的时间预算 + 卡住处理流程看 [`docs/HOW_TO_USE.md`](docs/HOW_TO_USE.md)。

准备好了吗？[从 Stage 0 开始](stages/00-foundations.zh-Hans.md)。

---

## 📚 相关资源

完整的相关资源（用语说明 + 常用 MCP / Skill highlight + awesome lists + 中文社群）抽到 **[RESOURCES.zh-Hans.md](RESOURCES.zh-Hans.md)** 避免主页过长。

直接看常用入口、依**情境**分组：

### 🚀 入门 / 环境设定

| 你的状况 | 去哪 | 内容 |
|---|---|---|
| 完全没写过 code、第一次接触 AI agent | [`resources/setup-guide.zh-Hans.md`](resources/setup-guide.zh-Hans.md) | 30-45 分钟从零装好（API key、Python、第一个 hello-world） |
| 不知道挑哪个 LLM provider | [`resources/setup-guide.zh-Hans.md` A](resources/setup-guide.zh-Hans.md#a--申请第一个-api-key约-10-分钟) | Anthropic / OpenAI / DeepSeek / Kimi / NVIDIA NIM 对照 |
| 同主题 awesome list / 中文社群 | [`RESOURCES.zh-Hans.md` 同主题清单](RESOURCES.zh-Hans.md#同主题的清单型-awesome-lists) | 5-10 分钟逛一轮 |

### 📖 概念 / 用语

| 你的状况 | 去哪 | 内容 |
|---|---|---|
| 不懂某个词（LLM / agent / RAG / token / MCP / Skill / 向量数据库…） | [`resources/glossary.zh-Hans.md`](resources/glossary.zh-Hans.md) | 30+ 词、每个 30-80 字 + 哪 stage 讲细的 |
| 想搞懂 agent 为什么有的在 terminal、有的在 Telegram、有的在 Jetson | [`resources/agent-paradigms.zh-Hans.md`](resources/agent-paradigms.zh-Hans.md) | 5 种 agent 型态 mental model + Hermes / OpenClaw 例子 |
| MCP / Skills / Plugins 用语对照 | [`RESOURCES.zh-Hans.md` 三个核心用语](RESOURCES.zh-Hans.md#三个核心用语mcp--skills--plugins) | 1 页速查表 |
| 想找带证书的线上 AI agent 课（英文 + 中文） | [`resources/courses.zh-Hans.md`](resources/courses.zh-Hans.md) | 10 门 credible、会发证书的课，分 tier；并诚实标注完成证书不是学历 |

### 🛠 动手实作

| 你的状况 | 去哪 | 内容 |
|---|---|---|
| 想动手写 Skill / MCP server / 接 Word / Zotero / 本机 LLM | [`resources/cookbook.zh-Hans.md`](resources/cookbook.zh-Hans.md) | 6 个 step-by-step recipe、每个 30-50 分钟 |
| 想用 subagent 但不知道该派谁、怎么派、派什么工作 | [`resources/subagent-cookbook.zh-Hans.md`](resources/subagent-cookbook.zh-Hans.md) | 15 个复制粘贴即用的 dispatch recipe |
| 自己写 subagent / 组合多个 / debug 跑坏的（进阶）| [`resources/subagent-advanced.zh-Hans.md`](resources/subagent-advanced.zh-Hans.md) | description 写法 4 个 bug + composition 3 pattern + debug 5 切点 |
| 卡在 tool calling（LLM 不调用 / schema 写不好 / ReAct loop 跑不停） | [`examples/stage-5/tool-calling-tutor/`](examples/stage-5/tool-calling-tutor/) | 可装进 Claude Code 的 skill、4-symptom diagnostic |
| 动手练习怎么正确使用（主动 vs 被动模式） | [`docs/HOW_TO_USE.md`](docs/HOW_TO_USE.md) | 5-10 分钟读完、配合每个 stage 用 |

### 🔌 接日常工具 / 找 MCP server

| 你的状况 | 去哪 | 规模 |
|---|---|---|
| 接 Notion / Obsidian / Excel / GitHub 等工具 | [`RESOURCES.zh-Hans.md` 接日常工具](RESOURCES.zh-Hans.md#接日常工具常用-mcp-server--skill) | 7-8 个 highlight |
| 完整 MCP server / Skill 目录（含星等、分类） | [`resources/mcp-skills-catalog.zh-Hans.md`](resources/mcp-skills-catalog.zh-Hans.md) | 79+ 条、16 大分类 |

### 🔬 研究 / production 级

| 你的状况 | 去哪 | 内容 |
|---|---|---|
| 研究 workflow + multi-LLM delegation skill | [`RESOURCES.zh-Hans.md` 研究工作流](RESOURCES.zh-Hans.md#研究工作流本-repo-维护者出品) | 本 repo 维护者出品的 Claude Code 研究 skill 对 |
| CLI agent 8 家对照 + production 搭配 | [`resources/cli-agents-guide.zh-Hans.md`](resources/cli-agents-guide.zh-Hans.md) | Track A 的核心参考、148 行 |
| Schema 设计规则（tool calling 必看） | [`resources/schema-design-cheatsheet.zh-Hans.md`](resources/schema-design-cheatsheet.zh-Hans.md) | 5 条黄金规则 + 5 个 anti-pattern |

---

## 🤝 如何贡献

这个 repo 是一个 AI 学习文档，如果你也有收集很好的资源，也欢迎贡献：

- 🐛 **汇报 Bug** — 内容错误、链接失效、过时信息 → 开 Issue
- 💡 **提建议** — 缺什么 stage、该加哪个 project → 开 Issue 讨论
- 📝 **完善内容** — 改进现有 stage 内容、修 typo → 直接 PR
- ✍️ **新增 project** — 在某个 stage 加 1-3 个 project，并附上“为什么这个 project 适合放这个 stage”的说明
- 🌏 **翻译** — 补英文 companion 没翻到的段落，或翻成其他语言
- 🌱 **担任 Stage / Branch maintainer** — 长期 review 特定领域，详见 [CONTRIBUTORS.md](CONTRIBUTORS.md)。

PR 流程跟 style 规范请看 [CONTRIBUTING.zh-Hans.md](CONTRIBUTING.zh-Hans.md) 和 [resources/style-guide.zh-Hans.md](resources/style-guide.zh-Hans.md)。

> 🤖 **新增 project 的链接会自动过审核** — PR 一加新的 `github.com/owner/repo` 链接，一个 GitHub Action 会留言贴出它的 star 数、license、是否封存、最后更新，并对照策展标准标出已封存 / 停更（>6 个月）/ 无 license 的项目。纯信息、不挡 PR，收不收仍由 maintainer 决定（目前只在 maintainer 开的 branch 上跑，fork PR 因 token 限制暂略）。

> 📅 **想看最近 ship 了什么** → [`CHANGELOG.md`](CHANGELOG.md)（最近 14 天）。
> Maintainer 内部进度与 launch checklist 放在 [.github/launch-checklist.md](.github/launch-checklist.md)（内部文件）。

---

## 💬 顾问 / 联系

公开学习版（MIT），欢迎自由取用。

目前以顾问为主：团队或公司若需 **prompt review / audit** 或 **AI agent workflow 咨询**，欢迎来信（博士生、时间有限）：📧 [wenyuchiou12@gmail.com](mailto:wenyuchiou12@gmail.com)

---

## 🙏 致谢

### Inspiration

- [**Datawhale Hello-Agents**](https://github.com/datawhalechina/hello-agents) — 中文圈最完整的 chapter-length agent 教材，本 repo 的“章节 + 进度”结构受这份启发；每个 stage / 练习 folder 都有 📚 callout 点过去深度章节。特别感谢。
- [**Datawhale 社群**](https://github.com/datawhalechina) — 中文 ML 共学社群的标杆，本 repo 多个 anchor project 来自这里
- [**liyupi/ai-guide**](https://github.com/liyupi/ai-guide) — 中文圈最大"AI 资源大全" + Vibe Coding 教学（涵盖 Agent Skills / RAG / MCP / A2A / Harness Engineering）。本 repo 是"结构化路线"、ai-guide 是"广度资源库"，互为补充

### 其他相关项目

同主题、不同切入角度的清单，搜资源时可以一起用：

- [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) — MCP server 清单，按分类整理
- [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) — 另一份 MCP server 清单
- [`hesreallyhim/awesome-claude-code`](https://github.com/hesreallyhim/awesome-claude-code) — Claude Code 相关工具与 plugin 清单（整理中）
- [`travisvn/awesome-claude-skills`](https://github.com/travisvn/awesome-claude-skills) — Claude Skills 清单
- [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official) — Anthropic 官方 plugin 模板，要打包自己的 plugin 从这份开始

这些是纯清单形式（看到再挑），本 repo 的不同点是有“从 Stage 0 一路走到 production 的学习顺序”。

### 贡献者

[![Contributors](https://contrib.rocks/image?repo=WenyuChiou/awesome-agentic-ai-zh)](https://github.com/WenyuChiou/awesome-agentic-ai-zh/graphs/contributors)

新贡献者会自动出现在上方。完整列表 → [GitHub Contributors](https://github.com/WenyuChiou/awesome-agentic-ai-zh/graphs/contributors)。

### 个人

- [@WenyuChiou](https://github.com/WenyuChiou) — Maintainer

---

## 🎓 引用

如果这个学习地图对你的学习或工作有帮助，欢迎引用：

```bibtex
@misc{awesome_agentic_ai_zh_2026,
  title = {awesome-agentic-ai-zh: A Structured Learning Roadmap for Agentic AI},
  author = {Chiou, Wenyu},
  year = {2026},
  url = {https://github.com/WenyuChiou/awesome-agentic-ai-zh},
  note = {8-stage learning path from prerequisites to Agent Interfaces (Computer Use / Browser Use / Code Sandbox), with curated projects + hello-X demos. Trilingual (zh-TW / 简中 / English).}
}
```

---

## ☕ 支持这个项目

这份学习地图是免费、开源（MIT）。如果它对你有帮助，除了给个 ⭐ Star，也欢迎请作者喝杯咖啡、支持它持续更新：

<a href="https://www.buymeacoffee.com/wenyuchiou" target="_blank" rel="noopener noreferrer"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="44"></a>

或直接点 repo 右上角的 **❤ Sponsor** 按钮。（GitHub Sponsors 审核中，通过后会一并加上。）

---

## License

MIT。Maintained by [@WenyuChiou](https://github.com/WenyuChiou)。

<div align="center">
  <p>⭐ 如果这个 repo 对你有帮助，欢迎给个 Star — 这对作者继续更新是很大的鼓励</p>
</div>

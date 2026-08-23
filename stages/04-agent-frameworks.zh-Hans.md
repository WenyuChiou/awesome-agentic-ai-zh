# Stage 4 — Agent 框架（Agent Frameworks）

> [繁體中文](./04-agent-frameworks.md) | **简体中文** | [English](./04-agent-frameworks.en.md)

⏱ **时间估算**：2-3 周（约 10-15 小时）

> 💡 用语不熟（framework / supervisor / worker / handoff⋯）→ 翻 [`resources/glossary.zh-Hans.md`](../resources/glossary.zh-Hans.md)。

> 📋 **本章组成**：学习目标 → 进入条件 → 必读 →〔可选 · 概念地图：multi-agent intro + 进阶 tool patterns〕→ 动手练习 → 精选 Projects → 自我检查
> 🔑 **关键名词**：见 [`resources/glossary.zh-Hans.md`](../resources/glossary.zh-Hans.md)（framework / agent loop / handoff / supervisor 等收在 2、4）

你已经从零打造过一个 ReAct agent（Stage 3）。现在来看 framework 到底帮你做了什么。**挑一个深入学**，其他的浏览过去就好，知道什么时候该换。

## 📌 学习目标

完成这个 stage 后你会：

- 比较 5 个主流 agent framework（LangGraph、AutoGen、CrewAI、Smolagents、OpenAI Agents SDK）
- 替任务挑出对的 framework
- 用两个 framework 各做一次同样的 agent，亲身感受差异
- 看出什么时候该丢掉 framework、自己写

## 🚪 进入条件

你应该已经：

- 跑完 Stage 3 的全部 5 个 hello-X projects
- 从零写过 ReAct（练习 3）
- 对 async Python 上手（framework 大量依赖 async）

## 📚 必读

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — 什么时候用 framework、什么时候直接用 raw API
2. [**LangChain — Conceptual Guide: Agents**](https://python.langchain.com/docs/concepts/agents/) — agent 的抽象概念
3. [**Best Multi-Agent Frameworks 2026 comparison**](https://gurusup.com/blog/best-multi-agent-frameworks-2026) — 当前市场定位
4. **挑一个 framework 的 Quickstart** — 选 LangGraph 或 CrewAI，把官方教学从头跑到尾

## 🤔 什么是 multi-agent framework？

### 两个维度先分清楚（workflow vs agent / single vs multi）

要看懂 multi-agent framework 之前、有一个有用的厘清方式——把 **workflow vs agent** 跟 **single vs multi LLM** 当成两个正交维度。Anthropic“Building Effective Agents”原文的核心区别是 workflow（固定 code path）vs agent（LLM 自主决定 next step）；我们把它跟 single/multi 叠起来看 4 个象限：

| | **Workflow**<br>（你写好的 code path） | **Agent**<br>（LLM 动态决定下一步） |
| -------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Single LLM** | 线性 pipeline、无分支判断 | 一个 LLM + ReAct loop、自己 plan + adapt<br>（**Stage 3 写的就是这个**） |
| **Multi LLM** | 预设 routing（譬如“销售问题 → agent A、技术问题 → agent B”） | 2+ agent 互相 handoff、orchestrator 动态分配<br>（**本 stage 主题**） |

**为什么这个区别有用**：production 场景大多落在“Single LLM”那一行——不管是 Workflow 象限（线性 pipeline）还是 Agent 象限（ReAct loop）——多数任务根本不需要 multi-agent。**真正需要 multi-agent framework 的是右下角象限**——LLM 自主性高 + 多角色协作。但实作上四个象限的边界有时模糊（LangGraph 的 conditional edge 可以同时看成 workflow routing 跟 agent 动态决策）、不要把这个 matrix 当互斥分类。

→ 本 stage 后续讨论都假设你已经知道：**Multi-agent framework 主要帮你处理多个 agent 之间的协调、交接、状态管理与重复性样板代码，让你不用从零写整套协作流程**（右下角象限的 orchestration boilerplate）。

### Single-agent vs multi-agent — 一张对照表先看清楚差异

| 维度 | **Single-agent**（你 Stage 3 写过了） | **Multi-agent system** |
| ------------ | --------------------------------------------- | --------------------------------------------------------------------------- |
| **架构** | 一个 LLM + ReAct loop + 若干 tools | 2+ LLM、各有角色（researcher / writer / critic ...）、orchestrator 协调 |
| **怎么决策** | 同一个 LLM 从头想到尾 | 角色拆分 + handoff、不同 LLM instance 看不同视角 |
| **State 管理** | 线性 message history | shared state / message passing / checkpoint |
| **适合场景** | 逻辑线性、tool < 20-30 个、单一目标 | 任务可分解、需要 perspective diversity、长 workflow、并行化 |
| **Debug 成本** | 低（单一 loop 可以一路 trace） | 高（cross-agent 互动、error propagation 难定位） |
| **Token 成本** | 1x | 通常 **3-10x**（每个 sub-agent 都有自己的 prompt + thinking + tool call） |
| **Latency** | 低 | 高（除非 sub-agent 并行跑） |

### 什么时候**真的**需要 multi-agent（不要硬上）

**Multi-agent 不是 default、是 last resort**。**Anthropic 跟 Cognition 两家 frontier lab 在 2024-2025 都明白写过：90% 用例其实不该用 multi-agent。** 硬上会付三个代价：**3-10× token、debug 痛苦、context fragmentation**——context 被切散在多个 agent、彼此看不到全貌。

| 立场 | 来源 | 核心论点 |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Anthropic** | [Building Effective Agents (2024)](https://www.anthropic.com/engineering/building-effective-agents)、[How we built our multi-agent research system (2025)](https://www.anthropic.com/engineering/built-multi-agent-research-system) | 多数场景 simple workflow + single agent 就够；multi-agent 只在“**研究型 / 并行探索**”任务真的有帮助 |
| **Cognition** | [Don't Build Multi-Agents (2025)](https://cognition.ai/blog/dont-build-multi-agents) | multi-agent 的 context fragmentation 严重、shared state 维护痛苦；先穷尽 single-agent + long-context 才考虑 |

需要 multi-agent 通常是这 4 个信号之一：

| 信号 | 描述 | 对应 pattern |
| ------------------- | ---------------------------------------------------------- | ---------------------------------- |
| **1. 任务天然分解** | 大任务有清楚的子步骤、step-by-step 完成 | Sequential / Planner-Executor |
| **2. Token explosion**| single agent prompt 塞不下所有 tool description / context | Supervisor-Worker（分流给 sub-agent）|
| **3. 角色冲突** | 同一个 LLM 既当 writer 又当 critic 会 self-justify | Debate / Peer review |
| **4. 并行加速** | 3 个 research 子任务同时跑、wall-clock 1/3 | Parallel / Map-Reduce 变种 |

**4 个信号都不在？** → single agent + 好 prompt + tool use 就够，不必为此付出前面说的那三个代价，而且 multi-agent 也不保证会比较准。

> 💡 **后续阅读**：到 [Stage 7 但你真的需要 multi-agent 吗？](07-multi-agent-production.zh-Hans.md#-但你真的需要-multi-agent-吗) 会再带 production 视角的决策——本节是设计阶段的决策、那边是 deploy 前的最后一次回头检查。

### Multi-agent 经典 pattern（按复杂度排序）

> 📝 **跟 Stage 3 经典范式怎么分**：[Stage 3 的 4 个 paradigm](03-tool-use-and-hello-agent.zh-Hans.md#agent-的经典范式thinking-patterns)（CoT / ReAct / Reflection / Planning）是**单一 agent 内部怎么想**；本节这 5 个 pattern 是**多个 agent 之间怎么协作**——正交的两个层。

| Pattern | 复杂度 | 什么样 | 经典场景 | 代表 framework / paper |
| -------------------------------- | -------- | ------------------------------------------------------ | -------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **1. Routing / Handoff** | ⭐ | agent 之间 1:1 handoff、无中央 orchestrator | customer support routing、context switch | [OpenAI Swarm](https://github.com/openai/swarm)、[OpenAI Agents SDK](https://github.com/openai/openai-agents-python) |
| **2. Sequential**<br>（Planner → Executor） | ⭐⭐ | planner 规划多步骤 + executor 执行 | 多步骤自动化、code generation | LangGraph、[ChatDev paper](https://arxiv.org/abs/2307.07924) |
| **3. Parallel**<br>（并行加速） | ⭐⭐⭐ | N 个 agent 同时跑、结果 aggregate | research / map-reduce 任务、wall-clock 1/N | LangGraph parallel branches、CrewAI parallel tasks。**坑点**：async coordination + partial failure + state merge 一致性 |
| **4. Supervisor-Worker**<br>（hub-spoke） | ⭐⭐⭐ | 1 主 + N worker、主分配 + 整合 | 任务拆解、报告整合 | LangGraph、AutoGen GroupChat |
| **5. Debate / Society**<br>（多视角收敛） | ⭐⭐⭐⭐ | 2+ agent 互相 critique 或角色扮演 | research、judgment task、social simulation | AutoGen GroupChat、[CAMEL paper](https://arxiv.org/abs/2303.17760)、[Generative Agents paper](https://arxiv.org/abs/2304.03442) |

### Claude Code subagent — 另一条 orchestration 路线

> **这节跟上面的 5 个 pattern 不同层**：上面 5 个 pattern 是 framework / 自己 code 都能实作的设计选择；本节介绍的 **Claude Code subagent 是另一个 execution model**（runtime 内建的 orchestration、不写 framework code）。读完 5 个 pattern 后、本节让你知道“multi-agent 还有第二条路”。

Anthropic 自家的 Claude Code 提供另一个 abstraction 层：[subagent](05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能) — 写一个 `.claude/agents/<name>.md` 档就是一个 subagent，**不需要 framework**。

跟 framework 路线的根本差异（一句话）：**framework 路线**跨 LLM provider、写 Python orchestration code、checkpointing / audit trail 完整；**Claude Code subagent** 只在 Claude Code runtime 内、写 markdown 不写 code、天生 context 隔离。

> 📌 **完整逐维度对照表（启动方式 / runtime / context 隔离 / provider lock-in / 学习曲线）的 canonical 在 [Stage 5.5 开头](05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能)**——逐项实作差异到 5.5 再看。

**何时选 subagent 而非 framework**：

- 你已经在使用 Claude Code 跑日常工作
- 任务 context 大、会吃光主 session window（读整个 codebase 之类）
- 多 subagent 并行（research / write / critic）省 wall-clock 时间
- 不需要跨 provider migration

详细写法 + 动手练习见 [Stage 5.5](05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能)（**建议先完成 Stage 5.1 Claude Code 基础再回来看 5.5**——subagent 是 Claude Code 生态的进阶功能、需要先熟悉基础用法）。

### Framework 的工作

Framework 把上面这 5 个 pattern 的 orchestration boilerplate（roles、handoff、state、retry、checkpoint、HITL pause）抽出来、让你只写角色定义跟任务描述。一句话：**framework 是 multi-agent 的脚手架，不是必需品**——简单情境你自己写个 dict 跟 for loop 也行（Stage 7 练习 1 就是这样）。

### 📚 想系统化深入？

**🇺🇸 学术 paper（影响后续所有 framework 设计）**：

1. [**Anthropic — "Building Effective Agents"**](https://www.anthropic.com/engineering/building-effective-agents) ⭐⭐⭐ — 何时用 workflow 何时用 agent、5 个经典 orchestration pattern。**英文圈 multi-agent 设计入门必读**
2. [**AutoGen paper (Wu et al. 2023)**](https://arxiv.org/abs/2308.08155) — Microsoft 多 agent 对话框架原 paper
3. [**CAMEL paper (Li et al. 2023)**](https://arxiv.org/abs/2303.17760) — multi-agent role-play 开山之作
4. [**ChatDev paper (Qian et al. 2023)**](https://arxiv.org/abs/2307.07924) — multi-agent software dev、planner-executor canonical
5. [**Generative Agents paper (Park et al. 2023)**](https://arxiv.org/abs/2304.03442) — 25 个 agent 在 The Sims 互动、社会 simulation

**🀄 中文系统教材**：

1. [**hello-agents Ch6“框架开发实践”+ Ch7“构建你的 Agent 框架”**](https://github.com/datawhalechina/hello-agents) ⭐ — 中文圈完整讲 framework 开发 + 从零构建。**注意：Ch4“智能体经典范式构建”是 single-agent paradigm（ReAct / Plan-and-Solve / Reflection），不是 multi-agent**
2. [**李宏毅 — 生成式 AI 导论**](https://speech.ee.ntu.edu.tw/~hylee/genai/2024-spring.php) — 中后段有 AI agent / multi-agent 相关集数

**Framework 官方 multi-agent docs**：

- [**LangGraph — Multi-Agent Systems**](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) — supervisor / swarm / hierarchical 三种架构官方教学
- [**Anthropic Cookbook — `customer_service_agent.ipynb`**](https://github.com/anthropics/claude-cookbooks/tree/main/tool_use) — multi-agent orchestration canonical 范例（routing + handoff）
- [**Microsoft AutoGen — Examples**](https://microsoft.github.io/autogen/) — group-chat / debate / peer review pattern 完整范例

> 💡 **建议框架学习流程**（5 步）：
> 1. **建立 mental model**（30 min）— 读 Anthropic Building Effective Agents、把 workflow vs agent 跟 single vs multi 两维度搞清楚
> 2. **跑 1 个 framework quickstart**（2-3 hr）— LangGraph 或 CrewAI 二选一、跑官方多 agent 教学
> 3. **对照 Anthropic Cookbook `customer_service_agent`**（1 hr）— production-style routing + handoff 范例
> 4. *(可选)* **深入学术侧**：挑 paper 1-2 篇看（AutoGen / CAMEL / ChatDev / Generative Agents）
> 5. *(Claude 用户可选)* **写一个 subagent 对照**：见 [Stage 5.5](05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能)、跟 framework 路线比较
>
> **不必把 5 个 paper 全读完**、挑跟你场景最近的 1-2 个。

## 🛠 进阶 tool patterns（framework 替你处理掉的东西）⭐ Track B 必看

Stage 3 教你写 single tool / multi-tool selection（手写 `if/elif/else` 路由）。Framework 把这层抽掉，并加了三种更进阶的 tool pattern——**这三个 pattern 都需要 framework 抽象层才写得干净，Stage 3 自己手写会炸开**：

| Pattern | 解决什么问题 | 代表实作 |
| ---------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Dynamic tool selection** | 工具 > 30 个时、`tools=[...]` 塞不下 prompt（context 太大、selection 也变差） | [LlamaIndex tool router](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/) — embedding-based 路由：先 semantic search 找 top-K tool、只把这 K 个塞进 prompt |
| **Tool composition / chaining**| tool A output → tool B input、不要 LLM 中间 narrative（省 token + 省 latency） | LangGraph `state graph` 直接连接 node、CrewAI `sequential tasks`、Pydantic AI 的 type-safe pipeline |
| **Tool-augmented retrieval** | tool 本身是 RAG search → 回结果再 reason | Stage 6 练习 4 RAG pipeline + Stage 3 练习 2 multi-tool 结合（LangGraph 直接把 retriever 包成 tool node） |

**📚 深度资源**：

- [**Anthropic — Tool Use best practices**](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) — 官方 tool design guide
- [**LlamaIndex — Tool Router pattern**](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/) — Dynamic selection canonical reference
- [**LangGraph — Tool Node**](https://langchain-ai.github.io/langgraph/) — composition graph 写法

> 💡 **Track B 学完本节**：你应该讲得出“同一个任务”在 (a) Stage 3 手写 (b) 本 stage framework 写 (c) Stage 5.5 Claude subagent 写 三种路线的差别。这是 Track B 路线“会设计 agent”核心问题。

## 🛠 动手练习

### 练习 1：同一个 agent、两个 framework
用以下两个 framework 各做一次同样的简单 agent（搜索 + 摘要）：

- LangGraph
- CrewAI
比较代码行数、debug 体验、以及它们各自把哪些复杂度藏在哪里。

### 练习 2：多 agent 角色分配
用 CrewAI 做一个 2-3 个 agent、各自有不同角色一起完成同一个任务的 demo。（这种情境 CrewAI 最拿手。）

### 练习 3：图式 workflow
用 LangGraph 做一个有分支逻辑跟 human-in-the-loop checkpoint 的 workflow。（这种情境 LangGraph 最拿手。）

### 练习 4：CodeAct vs JSON tool
用 Smolagents 做一个会写 Python 代码当作 action 的 agent（CodeAct pattern），跟 练习 1 用的 JSON tool call 路线比较。问同一个问题，看两种路线怎么解。

### 练习 5：类型安全 agent
用 Pydantic AI 做一个会返回结构化输出的 agent（例如：问问题回 `{ "answer": str, "confidence": float, "sources": [str] }`）。看 Pydantic 的 schema validation 怎么防止 agent 偷懒或 hallucinate 结构。

## 🎯 精选 Projects

按用途分 5 类、17 个项目一张表搞定。**挑入口看“适合谁”、想深入点链接看 repo / quickstart**。

| 分类 | Project | ⭐ | 适合谁 | 为什么推荐 / 备注 |
| ------------------------------------------ | ---------------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Production 级**<br>（复杂 multi-agent / 需要 audit） | [LangGraph](https://github.com/langchain-ai/langgraph) ⭐ **本 stage 推荐 #1** | ⭐⭐⭐⭐⭐ | Production multi-agent + 稽核轨迹 / rollback / replay | 图式 orchestration + checkpointing + time-travel debug、企业广泛采用，★ 39k+、MIT、Python+TS。搭 LangSmith 做 observability |
| | [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) | ⭐⭐⭐⭐ | 在 .NET / Java 环境做 agent、Microsoft 技术栈 | C# / Python / Java 三语官方 SDK、kernel + plugin + planner pattern，★ 28k+、MIT。抽象厚、不适合初学者 |
| | [agno-agi/agno](https://github.com/agno-agi/agno) | ⭐⭐⭐⭐ | 要“build + serve + monitor”一条龙但不想全套 LangGraph + LangSmith | multi-modal agent runtime + control plane，★ 41k+、Apache-2.0。Stage 4 学 API、Stage 7 用 runtime |
| | [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | ⭐⭐⭐⭐ | 想用微软整合 AutoGen + Semantic Kernel 的后继框架（Python 或 .NET）的团队 | 微软开源框架、让多个 agent 一起协作——合并 AutoGen 与 Semantic Kernel 的后继者，★ 12k+、MIT、Python + .NET |
| **快速雏形 / 多 agent**<br>（role-based / handoff） | [CrewAI](https://github.com/crewAIInc/crewAI) ⭐ **本 stage 推荐 #2** | ⭐⭐⭐⭐ | 快速雏形“researcher → writer → critic”pipeline | ~20 行写完 crew、学习曲线最低，★ 55k+、MIT。⚠️ 长 workflow 没 checkpointing；雏形用 CrewAI、production 用 LangGraph |
| | [Microsoft AutoGen / AG2](https://github.com/microsoft/autogen) | ⭐⭐⭐⭐ | 多 agent 辩论 / 脑力激荡 / peer review pattern | 对话式多 agent、group-chat 强，★ 60k+、CC-BY-4.0（文件 license）。⚠️ AG2 v0.4 重写成 async-first、旧教学多半还在 v0.2、新教学用 v0.4、留意版本分支 |
| | [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | ⭐⭐⭐⭐⭐ | 已 commit OpenAI 生态 | OpenAI 官方、agent hand-off + 结构化输出、API 干净、MIT。**2026-04 起内建** sandbox（7 个 provider）+ harness 抽象层、production coding agent 首次 architecturally sound（[详见 Stage 8](08-agent-interfaces.zh-Hans.md#openai-agents-sdk-2026-年-4-月更新--为何是里程碑)） |
| | [deepagents (LangChain)](https://github.com/langchain-ai/deepagents) | ⭐⭐⭐⭐ | 想要“开箱即用”的 deep agent 骨架、不想自己拼 | LangGraph 之上的 opinionated harness（有主见的骨架、替你做好设计选择）：内建规划（todo）、文件系统记忆、子 agent、可加载 skills、context offload（把庞大的中间结果挪出 LLM 视窗）。`pip install deepagents`、MIT、v0.6.12（2026-06）|
| | [OpenAI Swarm](https://github.com/openai/swarm) | ⭐⭐⭐⭐ 教育用<br>⭐⭐⭐ production | 想理解 multi-agent **核心 mental model** 但不想学整套 framework | ~200 LOC、只有 Agent + handoff 两个观念、MIT。⚠️ OpenAI 自己标 experimental / educational、不是 production tool。**读 source 当 chapter-length 教材** |
| | [Strands Agents (AWS)](https://github.com/strands-agents/sdk-python) | ⭐⭐⭐⭐ | 已 commit AWS 云、Bedrock-native | model-driven 设计（LLM 自己 plan、无 explicit graph）、Apache 2.0。2025 后段推出、AWS Lambda / Step Functions / Bedrock Agents 整合 |
| **特殊路线**<br>（CodeAct / typed / memory-first / filesystem-first） | [Hugging Face Smolagents](https://github.com/huggingface/smolagents) | ⭐⭐⭐⭐ | 本地 LLM 生态、HF 整合场景 | CodeAct pattern 代表（agent 写 Python 代码当作 action、非 JSON tool call），★ 28k+、Apache 2.0、≤1000 LOC |
| | [Pydantic AI](https://github.com/pydantic/pydantic-ai) | ⭐⭐⭐ | production 预设要 runtime 类型安全 + structured output | type-safe agent、Pydantic 团队出品、MIT。较新 |
| | [Letta (formerly MemGPT)](https://github.com/letta-ai/letta) | ⭐⭐⭐⭐ | **长 session / 跨 day / persona-stable** agent（long-term assistant、therapist、tutor） | memory-first multi-agent、OS-paging 概念（working memory + archival store），★ 24k+、Apache 2.0。Stage 6 练习 5 也会提 |
| | [vercel/eve](https://github.com/vercel/eve) | ⭐⭐⭐ | 想在 TS/JS 生态建长驻、可维运的 agent；喜欢“文件即接口”的项目结构 | Vercel 出品的 filesystem-first framework：agent 的组成都是惯例位置的文件——`instructions.md`（系统提示）、`tools/`、`skills/`、`channels/`（HTTP / Slack / Discord）、`schedules/`（定时任务），好检视、好扩充。`npx eve@latest init` 起手、Apache-2.0、TypeScript，★ 4.5k+。⚠️ 2026-06 才发布、很新 |
| **特化** | [LlamaIndex Agents](https://github.com/run-llama/llama_index) | ⭐⭐⭐ | 文件密集型 agent（研究助理、知识工作者类） | 跟 RAG 紧整合，★ 51k+、MIT。retrieval 强、orchestration 弱——纯 orchestration 别选 |
| | [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | ⭐⭐⭐ | 想要可视化 debug 多 agent 流程的研究者 | 多 agent 平台、可视化 debug 工具强，★ 28k+、Apache 2.0。西方社群采用低、技术扎实 |
| | [LangChain](https://github.com/langchain-ai/langchain) | ⭐⭐⭐ | 需要黏合很多零件（retrieval + chain）的快速雏形 | 万用工具袋 framework，★ 143k+、MIT。**agent orchestration 改用 LangGraph**、LangChain 适合 retrieval + chaining 黏合 |
| **基础设施**<br>（不是 framework、跨 stage 用） | [BerriAI/litellm](https://github.com/BerriAI/litellm) | ⭐⭐⭐⭐ | 要切换 Claude / GPT / Gemini / 开源模型但不想改 code | provider-agnostic SDK + AI gateway、用 OpenAI 形状 call 100+ LLM、附 cost tracking / fallback / guardrail，★ 54k+、MIT（`enterprise/` 子目录另授权） |

> 💡 **建议阅读路径**：挑 **1 个 production 等级**（LangGraph）+ **1 个快速雏形**（CrewAI）深入学 → 跑练习 1-3 → 其他 framework README 浏览过去、知道存在即可。**特殊路线那 4 个**（CodeAct / typed / memory-first / filesystem-first）在特定场景才有对手、平常不必碰。

## ✅ 进 Stage 5 前的自我检查

你能不能：

- [ ] 用 LangGraph 跟 CrewAI 各做一次同一个 agent
- [ ] 替任务挑出对的 framework（production vs 雏形）
- [ ] 解释 LangGraph 的 checkpoint 跟 CrewAI 的 task delegation 差在哪
- [ ] 看出什么时候 CodeAct（Smolagents）比 JSON-tool 更好
- [ ] 判断什么时候该丢掉 framework、直接用 raw API

如果可以 → 进 [Stage 5 — Claude Code Ecosystem](05-claude-code-ecosystem.zh-Hans.md)。

## 💡 策略提示 + 过程中可能踩到的坑

阅读路径见上面【精选 Projects】那则提示（LangGraph + CrewAI 深入、其他浏览过去即可），这里不重复。

**Memory 预备**（学的时候可能碰到、不用先读）：有些 framework 功能会用到 memory 概念 — LangGraph 的 checkpointing（状态持久化）、CrewAI agent 之间传递任务结果（轻量 memory）。这些在 [Stage 6 — Memory & RAG](06-memory-rag.zh-Hans.md) 完整讲；本 stage 看不懂某个 framework 功能时、再去那边查就好，**不用先读完才能继续本 stage**。

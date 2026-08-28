# 术语小词典（Glossary）

> [繁體中文](./glossary.md) | **简体中文** | [English](./glossary.en.md)

> 本路线图会大量出现“LLM”、“RAG”、“MCP”、“agent”这类词。读到不懂的词先在这里查 30 秒，再回去读 stage 内容。
>
> 每个词**只给最小可用的解释**（30-80 字 + 在哪一个 stage 讲细的）——不是维基百科。

## 🌐 统一词汇对照表（中英对照、跨 stage 一致）

本表是项目内**强制统一的命名约定**——所有 stage 用同一个中文理解名。如果你在 stage 内看到不一致，请报 issue。

| 英文术语 | 中文理解名 | 主要 stage |
|---|---|---|
| Prompt Engineering | Prompt 设计 | Stage 2 |
| Context Engineering | 上下文管理 | Stage 6 |
| Harness Engineering | Agent 执行系统设计 | Stage 7 |
| Tool Use | 工具使用 | Stage 3 |
| Function Calling | 函数 / 工具调用 | Stage 3 |
| Tool Schema | 工具纲要 / 工具说明卡 | Stage 3 |
| Tool Call | 工具请求 | Stage 3 |
| Tool Result | 工具结果 | Stage 3 |
| Structured Output | 结构化输出 | Stage 3 |
| Agent Loop | Agent 执行循环 | Stage 3 |
| Framework | 框架 | Stage 4 |
| Orchestration | 协调与编排 | Stage 4 / 7 |
| Handoff | 任务交接 | Stage 7 |
| Supervisor / Worker | 协调者 / 执行者 | Stage 7 |
| Runtime | 执行层 | Stage 7 |
| Scaffolding | 支撑架构 | Stage 7 |
| Observability | 观测与记录 | Stage 7 |
| Telemetry | 运行记录 | Stage 7 |
| Eval | 效果评估 | Stage 7 |
| Evaluation Harness | 评估框架 | Stage 7 |
| Production | 可稳定使用 / 上线化 | Stage 7 |
| Production-grade | 可长期稳定使用的 | Stage 7 |
| Deployment | 部署 | Stage 7 |
| Cost Tracking | 成本追踪 | Stage 7 |
| Latency | 延迟 / 等待时间 | Stage 7 |
| Vector DB | 向量数据库 | Stage 6 |
| Retrieval | 检索 | Stage 6 |
| Reranking | 重排序 | Stage 6 |
| Long Context | 长上下文 | Stage 6 |
| Fine-tuning | 模型微调 | Stage 6 |
| Agent Interfaces | Agent 操作界面 | Stage 8 |
| Code Sandbox | 隔离程序执行环境 | Stage 8 |
| Cold Start | 启动延迟 | Stage 8 |
| Reward Hacking | 钻评分漏洞 | Stage 7 / 8 |

→ 详细定义请看下面各区块。

---

## 1. 基本概念

### LLM（Large Language Model，大语言模型）

GPT、Claude、Gemini 这类模型会根据输入预测下一个 token。不同模型可以接收文字、图片或声音，也可能产生不同媒体。模型不会自行执行你的 client tool；网络、文件、工具与跨 session 记忆要由外部系统接上。

📍 详细：[Stage 1](../stages/01-llm-basics.zh-Hans.md)

### Model Provider / Provider API（模型供应商／模型 API）

**直接通往模型公司的入口。** 例如 Anthropic API、OpenAI API、Gemini API。你选择模型、发送 prompt，供应商返回结果并向你计费。它提供模型服务，但不是会读写你电脑文件的 CLI agent。

### LLM Router / API Router（模型路由器）

**一个入口，替你转接多个模型或后端。** [OpenRouter](https://openrouter.ai/docs/faq) 就是例子：通过同一个 API 和账单入口，你可以选择不同模型，并按设置使用 provider routing 或 fallback。Router 不是模型，也不是 OpenCode、Pi 这类 coding agent。

📍 五种身份对照：[Track A A1](../tracks/cli/A1-cli-intro.zh-Hans.md)

### Token

LLM 看到的不是“字”，是 **token**（次字单位）。中文 1 个字 ≈ 1.5-2 token，英文 1 个 word ≈ 1.3 token。LLM 计费跟 context window 都以 token 计。“100 万 token context”≈ 75 万中文字。

📍 详细：[Stage 1](../stages/01-llm-basics.zh-Hans.md)

### Context Window（上下文视窗）

LLM 一次能“看”多少 token。**2026 frontier**：Claude Sonnet 5 / Opus 5 1M、GPT-5.6 1.05M、Gemini 3.5 Flash 1M（Pro 系列上看 2M）、xAI Grok 4.5 500K、Mistral Medium 3.5 256k。**不是越大越好**——超过某个长度后 LLM 会“在中间遗漏”（Lost in the Middle）。

### Prompt（提示词）

你交给 LLM 的完整任务包。它不一定只有一个问题，可以包含指令、输入数据、背景、范例和输出限制，也可能分放在多个 message 里。**Prompt engineering** 是设计并测试这份任务包，让结果更符合成功条件。`system`、`developer`、`user` 是 API 的 message role（消息角色），不是 prompt 固定的三个部分，也不能直接当成“指令”的同义词。

📍 详细：[Stage 2](../stages/02-prompt-engineering.zh-Hans.md)

### Zero-shot / One-shot / Few-shot

在 prompt 里放“几个示范例子”让 LLM 照着做——这三个词的差别只在**你给几个范例**：

- **Zero-shot**（0 个范例）：直接问、不给任何范例。
- **One-shot**（1 个范例）：先给 **1 个** input → output 范例再问。
- **Few-shot**（少量范例）：先给少量 input → output 范例再问。没有通用的固定数字；它能展示格式和边界案例，但是否变好仍要用固定 eval 检查。

### Chain-of-Thought（CoT，思维链）

早期 prompting 技巧会要求 LLM 写出中间推理，再给答案。常见研究形式有两种：

- **Few-shot CoT**（原始 paper、[Wei et al. 2022](https://arxiv.org/abs/2201.11903)）：在 prompt 里放几个带推理步骤的例子，让 LLM 模仿推理
- **Zero-shot CoT**（[Kojima et al. 2022](https://arxiv.org/abs/2205.11916)）：在 prompt 结尾加上“Let's think step by step”。

现在不要把输出完整思维链当成通用要求。推理模型通常会在内部完成推理；需要核对时，要求**最后答案后附一段简短、可验证的理由**。哪种写法较好，必须用同一组 eval 比较。

---

## 2. Agent / 工具使用

### Agent（代理人）

以模型为核心、能在**有界循环**中**读取状态 → 选择动作 → 执行 → 观察结果**，直到完成、失败或碰到上限的系统。本学习地图使用三个部件来教入门：

- **LLM**（推理 / 规划 / decide）
- **Actions**（做事的手段——不限于 function call。可以是写代码执行（CodeAct）、操作浏览器（computer use）、查 KB（RAG retrieval）、call MCP server、纯规划拆任务等）
- **Loop**（有最大步数、timeout、费用与停止条件的执行循环）

这是本路线图的 **working definition**，不是唯一学术定义。**ReAct 是其中一种 agent pattern，不是 agent 的定义**；CodeAct、computer-use、planning agent 也可能使用不同的 action 与 loop。

📍 详细：[Stage 3](../stages/03-tool-use-and-hello-agent.zh-Hans.md)

### Tool Use / Function Calling

模型需要查资料或采取动作时，会返回一个带工具名称、call ID 与参数的结构化请求。对于 client tool，**模型只提出请求**；你的程序验证参数、执行函数，再把对应结果送回模型。

**Tool Use** 是更广的能力名称；**Function Calling** 是常见的结构化调用机制。供应商的 schema 与消息格式不同：

- **Anthropic 的 "Tool Use"**：schema 用 `input_schema`（直接放 JSON Schema）
- **OpenAI / Ollama 的 "Function Calling"**：外面再包一层 `{"type": "function", "function": {...}}`
- 编写跨供应商 SDK 时，要分别处理 Tool Call、Tool Result、错误标志与停止原因

📍 详细：[Stage 3](../stages/03-tool-use-and-hello-agent.zh-Hans.md)
📍 schema 怎么写好：[Function Schema 设计 cheatsheet](schema-design-cheatsheet.zh-Hans.md)

### Tool Schema（工具纲要）

工具的说明卡：名称、用途、输入栏位、类型与限制。Schema 能限制请求外形，但不能代替权限、数值范围与业务规则验证。不同供应商的 strict mode 支持也不完全相同。

### Tool Call（工具请求）

模型根据 Tool Schema 填好的工作单，通常包含工具名称、call ID 与参数。它只是**请求**，不是函数已经执行的证明。程序应先比对 allowlist，再解析和验证参数。

### Tool Result（工具结果）

程序执行工具后返回的数据，并用 call ID 对回正确的 Tool Call。成功与错误都要明确表示；外部工具结果可能含错误、恶意内容或 prompt injection，必须视为不可信数据。

### ReAct（Reasoning + Acting）

一种交替 **Reasoning → Action → Observation** 的 agent pattern。本路线图只要求可观察的 Tool Call、Tool Result、停止原因和简短可验证摘要；不要求模型公开私有 Chain-of-Thought。循环必须有步数、时间与费用上限。

📍 详细：[Stage 3](../stages/03-tool-use-and-hello-agent.zh-Hans.md)

### Structured Output（结构化输出）

要模型输出 **JSON 或其他固定 schema**，而不是自由文字。它和 Function Calling 都可能使用 schema，但目的不同：Structured Output 要固定形状的数据；Function Calling 要应用程序采取动作。供应商支持不一，schema 合法也不保证内容正确，程序仍要处理 refusal、截断、解析与语义错误。

### Agent Loop

“模型 → Tool Call → 程序执行 → Tool Result → 模型”这个重复循环。每个结果要对回原 call ID。Loop 必须在完成、拒答、错误、最大步数、timeout 或费用上限时停止；不能把 retry 全交给模型。

⚠️ **这是“一次执行里面”的循环**，是 harness 的一个零件，跟五层阶梯第 4 层的 [Loop Engineering（循环工程）](#loop-engineering循环工程)（管的是跨 session 的长时间执行）同名但不同层次。两者的分界见 [Stage 7](../stages/07-multi-agent-production.zh-Hans.md)。

### Self-Refine（基础版反思 / 无记忆）

模型自我评估上一轮输出、修改下一轮的做法——“Actor 出答案 → Critic 找问题 → Actor 看 feedback 再答”的 single-session loop。**不一定需要持久记忆层**，是 ReAct 的 sibling pattern，不是 Tool Use 的同义词。

代表 paper：[Self-Refine (Madaan 2023)](https://arxiv.org/abs/2303.17651)。**完整版 Reflexion**（含 episodic memory）见 3 Memory / Retrieval / RAG（这是不同层的东西）。

📍 详细 + 路由：[Stage 3 反思](../stages/03-tool-use-and-hello-agent.zh-Hans.md#-反思reflexion--self-refine-概念--路由)

---

## 3. Memory / Retrieval / RAG

### Memory（记忆）— 两种正交分类轴

“memory”常被混在一起讲，其实有 **2 种正交分类轴**：

- **时效轴**：short-term（当前对话）vs long-term（跨 session 持久）
- **内容轴**（CoALA framework）：**Working**（暂存）/ **Episodic**（过去经历）/ **Semantic**（事实知识）/ **Procedural**（怎么做）

→ 两条轴并不冲突：long-term memory 里可以**同时**有 episodic（user 上次说了什么）+ semantic（公司知识库事实）+ procedural（用过的 tool sequence）。

📍 详细：[Stage 6 Memory 是什么 + 如何设计](../stages/06-memory-rag.zh-Hans.md#-memory-是什么--怎么设计) + [Stage 6 CoALA Framework](../stages/06-memory-rag.zh-Hans.md#进阶coala-framework--agent-memory-的-4-层分类法)

### RAG（Retrieval-Augmented Generation）

两阶段架构模式：

1. **Ingest**（一次性 / 定期）：document → chunk → embed → 存进 vector store（建一个可检索的 KB）
2. **Query**（每次 user 提问）：question embed → semantic search（或 hybrid + BM25）→ top-K chunks → 塞进 prompt → LLM 回答

**解决的是 LLM 不知道你的私有 / 变动 / 过期资料**。Retrieval **不只限于 dense embedding**——production 默认配置通常是 hybrid（dense + BM25）+ reranker。

📍 详细：[Stage 6](../stages/06-memory-rag.zh-Hans.md)
📍 paper：[Lewis et al. 2020](https://arxiv.org/abs/2005.11401)

### Reflexion（完整版反思 / 带 episodic memory）

跟 Self-Refine（2 Agent）不同：Reflexion **需要持久 episodic memory store**——agent 跑完一次 trial 后，会**写一段 reflection summary 进 memory**，下一次 trial 开始时再检索进 prompt。**跨 trial 累积教训**才是 Reflexion 的本质（不是 single-session loop）。

放在 3 而不是 2 Agent，是因为它**本质上是 memory pattern**——episodic memory store 是核心，不是 optional。

代表 paper：[Reflexion (Shinn 2023)](https://arxiv.org/abs/2303.11366)。

📍 详细：[Stage 6 进阶：带持久记忆的 Reflexion 完整版](../stages/06-memory-rag.zh-Hans.md#-进阶带持久记忆的-reflexion-完整版--track-b-选读)

### Embedding（嵌入）

把文字 / 图片转成 N 维**向量**，让“意思接近”的东西距离更近。本路线图默认指 **dense embedding**（稠密向量，由 sentence-transformers / OpenAI ada-002 等产生）；另外也有 **sparse embedding**（BM25 / SPLADE 等，按字面 token 匹配）——production RAG 往往两者一起用来做 hybrid search。

📍 详细：[Stage 6](../stages/06-memory-rag.zh-Hans.md)

### Vector DB（向量数据库）

存储 + 高效查询 embedding 的存储层。**主要查询类型 = approximate nearest-neighbor (ANN)**——Vector DB 存在的意义就是 ANN 比直接做 cosine 全扫快几百倍。代表：Pinecone / Chroma / Qdrant / Weaviate / pgvector。

📍 详细：[Stage 6](../stages/06-memory-rag.zh-Hans.md)

### Semantic Search（语义搜索）

用 embedding 比较“意思相似”而不是“字符串完全相同”。“电动车怎么充电”可以捞到“EV charging tutorial”。传统关键字搜索（BM25 等）做不到这个。

### Chunking（切块）

把长文件切成适合 embedding 的小段（通常 200-1000 token）。**切法直接影响 RAG 质量**——切太碎丢脉络、切太长相关度模糊。常见策略：固定大小、按段落、按结构（heading）。

### Hybrid Search（混合搜索）

语义搜索 + 关键字搜索一起用，再 merge 排序。多半比单一方法准。上线部署 RAG 的标配。

### Reranking（重新排序）

第一轮 retrieval 捞 top-50，再用更贵但更准的模型（cross-encoder）重排成 top-5 给 LLM。Cohere Rerank、bge-reranker 等。

### Contextual Retrieval

Anthropic 2024 提的方法——chunk 加上“整份文件的脉络摘要”一起 embed，避免“这 chunk 拿出来看不知道是哪份文件讲的”问题。

📍 详细：[Stage 6](../stages/06-memory-rag.zh-Hans.md)

### Fine-tuning（模型微调）

拿你自己的资料**再训练**模型、把知识或行为“烧进”权重里（跟 RAG 不同——RAG 是 inference 时才把资料塞进 context、不改权重）。适合让模型稳定学会某种**格式 / 风格 / 领域用语**；**不适合**拿来塞“最新事实”（那是 RAG 的活，fine-tune 进去的事实会过期又难更新）。多数 agent 场景**先试 prompt + RAG**，真的不够才考虑 fine-tune。

📍 详细：[Stage 6](../stages/06-memory-rag.zh-Hans.md)

---

## 4. Multi-Agent

### Multi-Agent（多 agent）

多个 agent 互相协作完成一个任务。常见 pattern：

- **Supervisor + Worker**：一个 agent 规划 / 分派、其他执行
- **Swarm（群集）**：平等的 agent 群，没有固定 supervisor
- **Debate（辩论）**：多个 agent 各持立场、最后 consensus

📍 详细：[Stage 7](../stages/07-multi-agent-production.zh-Hans.md)

### Handoff

一个 agent 把任务交给另一个 agent。比直接 function call 多了“context 怎么传”、“失败谁处理”的问题。

### A2A（Agent-to-Agent）Protocol

Google 发起、现由 Linux Foundation 治理的 agent 之间沟通协议，类似 MCP 但用于 agent ↔ agent（不是 agent ↔ tool）。2026 已达 **v1.0**（已有 150+ 组织采用，并加入身分验证、让一个 agent 能确认对方是不是真的它），是 MCP（agent↔tool）的姊妹标准。

---

## 5. Claude Code 生态

### MCP（Model Context Protocol）

Anthropic 在 2024 推出的开放协议，让任何 LLM host（Claude Code、Cursor、自写 agent）都能用同一套接口连接外部 tool server，2025-12 已捐给 Linux Foundation 旗下的 Agentic AI Foundation。把它想成“**LLM 的 USB 接口**”。

**技术上标准化了 3 种 primitives**：

- **Tools**：LLM 可调用的 function（read DB / search web / send email…）
- **Resources**：LLM 可读取的数据（文件内容、API response、DB rows…）
- **Prompts**：可复用的 prompt 模板（给用户在 host 内用 `/` 触发）

**架构**：server / client 模式——tool server 跑在本地或远端，LLM host 当 client 连接。Server 通过两种 transport 之一暴露这些 primitives：**stdio**（本地 subprocess）与 **Streamable HTTP**（远端）；旧的 HTTP+SSE transport 已在 2025-03-26 spec revision 标为 deprecated。

📍 详细：[Stage 5.2](../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础)

### Project Instructions（项目规则）

CLI agent 每次进入项目时都要读取的共同守则，像贴在工作室墙上的规则。这里放项目用途、禁止事项、验证指令和交付格式。不同工具使用不同文件名和加载顺序，例如 Codex／OpenCode V2 的 `AGENTS.md`、Claude Code 的 `CLAUDE.md`、Gemini CLI 的 `GEMINI.md`。

📍 入门：[Track A A2](../tracks/cli/A2-cli-workflow.zh-Hans.md)

### Skills / SKILL.md

需要时才拿出的可复用“操作卡”。一个 Skill 通常是一个含 `SKILL.md` 的文件夹，还可以附带 references、scripts 或其他文件。Codex、Claude Code、Gemini CLI 和 OpenCode V2 都有 Skill 机制，但搜索路径、frontmatter、加载方式和权限并不完全相同。

`description` 要清楚说明“什么情况使用”以及“能做什么”，让 agent 能选到正确 Skill。第三方 Skill 可能执行程序或调用外部工具；安装前要读完内容和权限，不要把 Skill 当成安全边界。

📍 入门：[Track A A2](../tracks/cli/A2-cli-workflow.zh-Hans.md)；Claude Code 深入：[Stage 5.3](../stages/05-claude-code-ecosystem.zh-Hans.md#53--skillsclaude-code-的行为层-claude-code-生态最关键的一层)

### One-off Prompt（单次提示）

只为眼前任务使用的一次性交代，像今天才要用的便条。它放本次任务、范围、输入、禁止事项和成功条件；每次都相同的项目规则应移到 project instructions，重复流程应移到 Skill。

📍 练习：[Track A A2 CLI-8](../tracks/cli/A2-cli-workflow.zh-Hans.md#cli-8)

### Plugin / Marketplace

把多个 Skills + slash commands + hooks + MCP 设置打包成一个发布单位。**Marketplace** 就是 plugin 的目录，社群可以 `claude plugin install` 安装别人写好的。

📍 详细：[Stage 5.4](../stages/05-claude-code-ecosystem.zh-Hans.md#54--plugins-与-marketplaces)

### Slash Command

Claude Code 内以 `/` 开头的指令，例如 `/help`、`/compact`、`/plan`。旧项目可能把自定义 prompt 放在 `.claude/commands/<name>.md`；这是兼容旧做法。新的可复用流程建议写成 `.claude/skills/<name>/SKILL.md`。

### CLAUDE.md

放在 project root 的 markdown 档，Claude Code 每次启动都会读。写 project 级的规则 / 规范 / context（用什么语言、coding style、别动哪些档等）。

### Hooks

在 Claude Code 特定事件前后执行的 script。**官方支持 7 种事件类型**：

| Hook | 触发时机 | 典型用途 |
|---|---|---|
| `PreToolUse` | 工具调用**前** | 拦截危险操作（`rm -rf`、destructive op）、改参数 |
| `PostToolUse` | 工具调用**后** | 记 log、自动格式化刚写好的文件 |
| `UserPromptSubmit` | user 提交消息时 | 加 context（git status / 当前时间） |
| `Notification` | Claude Code 发通知时 | 桌面 toast / Slack ping |
| `Stop` | session 结束时 | 自动 commit / 清理 |
| `PreCompact` | 自动 compact 前 | 把重要决定提升到 memory |
| `PostCompact` | compact 后 | 确认哪些 context 被压缩 |

写法：在 `.claude/settings.json` 里加 `"hooks"` 区块，指向 script 路径。

### Deep Agent（深度 agent）

“自带完整配备”的 agent 设计——不只会调用工具，还内建规划（待办清单）、长期记忆（文件系统）、子 agent 分工、可加载的 skills。对照：简单的 agent 只有 LLM + 几个工具。代表实作：LangChain 的 [deepagents](https://github.com/langchain-ai/deepagents)。

---

### Subagent（子 agent）

主 Claude Code session 之外，spawn 出来跑特定任务的 agent。有自己的 context window。例如“给我一个 code-reviewer subagent 看看 diff”。

写法：在 `.claude/agents/<name>.md` 放 frontmatter + system prompt + tool whitelist。主 session 用 **Agent tool** invoke（自动 parallel / sequential）。**跟 framework-based multi-agent 对照**：subagent 不需要装 LangGraph / CrewAI 等 framework，直接写 markdown 即可；但绑定 Claude Code runtime。完整教学见 [Stage 5.5](../stages/05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能)；**15 个复制粘贴即用的 dispatch recipe** → [`subagent-cookbook.zh-Hans.md`](./subagent-cookbook.zh-Hans.md)。

---

## 6. Production / Eval / Cost

### CI（Continuous Integration，持续集成）

push 或 PR 出现时自动执行固定工作的检查站。CI 可以跑测试、lint 或只读 agent review，但它使用的 token、secret、repo 权限和触发条件都要另外限制。CI 成功不代表可以自动 merge 或跳过人工 review。

📍 练习：[Track A A3 CLI-10](../tracks/cli/A3-cli-production.zh-Hans.md#cli-10)

### Eval（评估）

拿一组固定 test case 检查 prompt 或 agent。最小的 eval 就像一张小答案卡：同一组题目、清楚的正确条件、每次修改后重跑。规模变大后，还能一起记录准确度、latency 与 cost。常见工具有 promptfoo、LangSmith 与 Langfuse evals。

📍 入门：[Stage 2](../stages/02-prompt-engineering.zh-Hans.md)；完整 eval harness：[Stage 7](../stages/07-multi-agent-production.zh-Hans.md)

### Observability

把 agent 执行过的步骤、模型、tool、usage、时间和结果留下来，像收据加行车记录。出 bug 时可以找出哪一步失败；拿不到的字段要写“未确认”，不能靠猜。常见工具有 Langfuse、Phoenix、Helicone。

📍 入门：[Track A A3 CLI-11](../tracks/cli/A3-cli-production.zh-Hans.md#cli-11)；深入：[Stage 7](../stages/07-multi-agent-production.zh-Hans.md)

### Prompt Caching

LLM 把 prompt 前缀 cache 起来，下次同前缀只算 cache hit 的便宜价（Anthropic 90% off、OpenAI 50% off）。Long context + 重复 query 的场景可以省很多钱。

### Streaming（流式输出）

LLM 边生边回（一个 token 一个 token），不是等全部生成完才丢整段回来。读者体验较好（像在打字）；技术上用 SSE 或 chunked transfer。**production 交互式应用几乎都开**。代价：客户端要能 handle partial response、ReAct 内 tool call 解析要等到 stream 结束。

### Batch API（批量 API）

把大量 LLM 请求打包送（不要求实时），24 小时内回。**Anthropic / OpenAI 通常打 5 折**。适合非交互场景：批量摘要、批量分类、eval 跑大量 test case、ETL pipeline。**交互式 chat 不能用**——延迟对用户体验来说太久。

### Token Cost / Inference Cost

每次 LLM 调用的成本 = input tokens × input price + output tokens × output price。Agent 跑 ReAct loop 的成本可以累积很快——大 codebase grep 一次可能花 10 万 token。

### Guardrails

防 LLM 做坏事的规则层——挡掉 prompt injection、PII 外流、有害输出等。NeMo Guardrails、Guardrails AI 等。

### Prompt Injection（提示注入）

把恶意指令藏在 LLM 会读到的内容里（网页、文档、工具返回），诱导它无视原任务、改做攻击者要的事。根因：LLM 分不清“指令”与“数据里夹带的指令”。防法：最小权限、隔离不可信内容、高风险动作人审。相关：lethal trifecta、Guardrails。

### Lethal Trifecta（致命三角）

Simon Willison 提出：agent 同时有（1）访问私密数据、（2）接触不可信内容、（3）对外通讯三种能力时，就可能被 prompt injection 操控去偷数据外传。防法是打断至少一环（常见：切断对外通讯或隔离不可信输入）。

---

## 7. 用词 / Buzzword

### CLI Agent

跑在终端、能在你允许的范围内读文件、改文件和执行命令的 agent / harness（Claude Code、Codex、OpenCode、Pi、Aider、Gemini CLI 等）。**它是工作台，不是里面的 LLM。** 同一个 CLI 可能绑定一个模型生态，也可能让你切换 provider。

📍 详细：[Track A A1](../tracks/cli/A1-cli-intro.zh-Hans.md)、[`resources/cli-agents-guide.zh-Hans.md`](cli-agents-guide.zh-Hans.md)

### BYO API Key（Bring Your Own）

工具让你提供自己的 provider API key，而不是只使用工具内建的订阅登录。Aider、OpenCode、goose、Pi 等可以接一个或多个 provider；Claude Code、Codex 也各有官方文档列出的订阅或 API 认证路径。实际支持方式会变化，使用前请看该工具的官方认证文档。

### Local LLM / On-Device

模型在自己的机器上运行。Ollama、llama.cpp、MLX、LocalAI 是 **local runtime**：它们负责把模型运行起来，不等于 coding agent。只有模型、工具和数据路径都留在本机，而且没有另外调用云端服务时，数据才不会因为这次流程送到云端；能力和速度要用自己的任务和硬件测试。

📍 详细：[Stage 1](../stages/01-llm-basics.zh-Hans.md)

### Quantization（量化）

把模型权重从 fp16 压到 int8 / int4，省内存跟速度，代价是准确度小幅降低。Local LLM 用户常碰到（Q4_K_M、Q8_0 等）。

### Hallucination（幻觉）

LLM “自信地说错”——把不存在的 API 编出来、把错的数字当成事实写。所有 production agent 都要防这个（用 RAG / structured output / eval / guardrails）。

### Frontier Model

当下最顶的模型（**2026-07**：Claude **Opus 5**（2026-07-24、`claude-opus-5`、1M、$5/$25，官方 docs 建议的默认起点）、OpenAI **GPT-5.6**（Sol / Terra / Luna 三级、1.05M context、ChatGPT / Codex / API 都能用）；**2026-06 后半**：Claude Sonnet 5（速度×智慧的最佳平衡、接近 Opus 级但更便宜）、Google Gemini 3.5 Flash、xAI Grok 4.5（500K context）、Mistral Medium 3.5；**2026-06 前半**：Claude Fable 5（Mythos-class，定位在 Opus 之上）发布，2026-06-12 曾被美国出口管制暂停，但 **出口管制 2026-06-30 解除、[Fable 5 于 2026-07-01 全球恢复](https://www.anthropic.com/news/redeploying-fable-5)**（Mythos 5 仅对核准美国组织恢复）；**2026-05**：GPT-5.5、Claude Opus 4.8（当时的 Opus-class 旗舰，2026-07 由 Opus 5 接替、仍可用）、Gemini 3.1 Pro、DeepSeek-V4-Pro 等）。一般智慧任务用 frontier；简单分类 / 翻译用便宜的小模型省钱。

### Context Engineering

工程 **每次 LLM call 时，context window 里装什么信息** 的学科——动态把 RAG retrieve 结果、memory、tool definitions、对话 history 组装成模型看得到的 context。Karpathy 2025：把 **刚好对下一步有用的信息** 填进窗口的精细艺术。重点是 *what goes in the window*，不是“跨了几次 call”。**Prompt engineering 的下一层**——前者工程 **字符串**，后者工程 **信息**。

📍 详细：[Stage 2 结尾](../stages/02-prompt-engineering.zh-Hans.md) / [Stage 6](../stages/06-memory-rag.zh-Hans.md) / [Stage 7](../stages/07-multi-agent-production.zh-Hans.md)
📍 延伸：[`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering)

### Harness Engineering

工程 **模型外面的执行与控制层**——所有不是 model weights、也不是 prompt string 本身的工程元件：agent loop / tool registry / context manager / permissions / safety layer / memory layer / eval / observability / retry / circuit breaker 等。Simon Willison 2025：**coding agent = LLM + harness**。Addy Osmani：harness = 所有不是 model 本身的代码。[OpenAI 也在 2026-02 使用了 "Harness Engineering" 这个说法](https://openai.com/index/harness-engineering)。Claude Code、Cursor、OpenCode 等 CLI agent 都是 harness。**framework 把 LLM 包成 agent，harness 把 agent 包成可上线使用的产品**。

对比：

- **Framework**（Stage 4）规范 **API**：你调用的接口长什么样
- **Harness**（本词）规范 **runtime**：怎么跑、怎么 recovery、怎么观测

📍 学科级概念（**8 个核心元件** / prompt→context→harness 五层工程分工 / framework vs harness）：[Stage 7 Harness Engineering](../stages/07-multi-agent-production.zh-Hans.md)
📍 Reference implementation case study（读 Claude Code source）：[Stage 5 5.7](../stages/05-claude-code-ecosystem.zh-Hans.md)
📍 延伸：[`anthropics/claude-agent-sdk-python`](https://github.com/anthropics/claude-agent-sdk-python)、[`ai-boost/awesome-harness-engineering`](https://github.com/ai-boost/awesome-harness-engineering)、[`ZhangHanDong/harness-engineering-from-cc-to-ai-coding`](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding)

### Loop Engineering（循环工程）

五层工程分工的第 4 层（完整阶梯与各层目的见 [Stage 7](../stages/07-multi-agent-production.zh-Hans.md)，那里是 canonical）：设计 / 调校 agent 的“迭代循环”本身——目标、工具、context 管理、终止条件、错误处理，让长时间（数百步、跨 session）运行仍可靠、可控、不跑偏。相关：harness、Dynamic Workflows、ReAct。

⚠️ **不要跟 harness 里那个 [Agent Loop](#agent-loop) 搞混**。这一层管的是**跨越好几次执行**的长时间问题；`Agent Loop` 是 harness 的一个零件，管的是**一次执行里面**的机械循环。

### Graph Engineering（图工程）

把 agent 的执行流程设计成**显式的图**：node = 一个步骤（2026 起一个 node 里可以放一整个 agent run，不再只是一个 function），edge = 转移条件，node 之间传递一个有 schema、可 checkpoint、可 replay 的 state。**读到这个词要知道两件事**：

- **这里的“图”是执行流程图（control / execution graph），不是 GraphRAG 那种知识图谱检索**——后者见 [Stage 6](../stages/06-memory-rag.zh-Hans.md)。两者常被混为一谈。
- **这是 2026-07 才流行的新名字，不是新技术**。LangGraph 从 2023 就是这样运作，LangChain 官方也直言这不是新想法；Anthropic 称同类机制为 *dynamic workflows*、Google ADK 与 Microsoft Agent Framework 用 *graph-based workflow(s)*，三家官方文档都没有采用“graph engineering”这个说法。

**跟循环的关系**：不是二选一。**格子里面是 agent 自己绕圈，格子跟格子之间才是你安排的顺序**——所以图是把好几个循环装进格子再排顺序；全部塞回同一个格子，就退回单纯的循环了。格子里也不一定是 agent，可以是一个工具、一段检查、或“这里要人按核准才能往下”。五层阶梯的完整说明见 [Stage 7](../stages/07-multi-agent-production.zh-Hans.md)（canonical）。

真正要学的东西在 [Stage 4 的 multi-agent pattern](../stages/04-agent-frameworks.zh-Hans.md) 和可以直接跑的 [`examples/stage-4/03-graph-workflow/`](../examples/stage-4/03-graph-workflow/README.zh-Hans.md)（`StateGraph` / conditional edge / checkpointer）。相关：harness、Loop Engineering、orchestration。

---

## 8. Agent Interfaces

### Computer Use（屏幕级 agent）

Agent 通过 **screenshot → vision → 算坐标 → 模拟键鼠** 操作真实桌面 app——不靠 API、直接像人类用屏幕。代表：Anthropic Claude Computer Use（Opus 5 / Sonnet 5）/ OpenAI Codex desktop / Google Gemini in Chrome。**2024-10 Anthropic 公开 beta 开启；OSWorld v1 2026-05 达 76.26% 后接近饱和，OSWorld 2.0（2026-06、long-horizon）把 SOTA 重设到 ~20%（Opus 4.8）**。

📍 完整解说 + 4 强对比：[Stage 8 Computer Use](../stages/08-agent-interfaces.zh-Hans.md)

### Browser Use（web 级 agent）

Agent 操作网页、主要用 **DOM-aware navigation**（直接 query CSS selector）+ 必要时 vision fallback。代表闭源：Comet / Dia / Gemini in Chrome（Atlas 2026-08 停运）。代表 OSS：[browser-use](https://github.com/browser-use/browser-use)（★ 105k+）。

📍 完整解说 + 5 强对比 + OSS 框架：[Stage 8 Browser Use](../stages/08-agent-interfaces.zh-Hans.md)

### Sandbox（程序代码隔离环境）

让 agent 写的 code 在隔离环境跑、不在 host 机器——避免 agent `rm -rf /` / 连 internet 泄资料 / 偷 credentials 等灾难。代表：E2B（Firecracker microVM）/ Daytona（Container）/ Modal（GPU sandbox）/ Vercel / Cloudflare。**OpenAI Agents SDK 2026-04 内建支持这些 provider**。

📍 完整 9-row 术语小词典（含 microVM / Container 差异）+ 7 强对比：[Stage 8 Code Sandbox](../stages/08-agent-interfaces.zh-Hans.md)

### microVM（micro Virtual Machine）

VM 的精简版、极小 footprint、启动 < 100ms 但仍**独立 kernel**——介于 Docker container（快 + 弱隔离）跟 full VM（慢 + 强隔离）之间。**Agent sandbox 多半选 microVM**。代表实现：[Firecracker](#firecracker)（AWS、E2B 用）。

📍 完整对比：[Stage 8 术语小词典](../stages/08-agent-interfaces.zh-Hans.md)

### Firecracker

AWS 开源的 microVM、Rust 写、**AWS Lambda 底层** + E2B sandbox 用它做 isolation。强隔离 + 快启动兼顾。

📍 [Stage 8 术语小词典](../stages/08-agent-interfaces.zh-Hans.md)

### gVisor

Google 写的“用户空间 kernel”、拦截 syscall 自己模拟、**不用 hypervisor**——介于 container 跟 VM。

📍 [Stage 8 术语小词典](../stages/08-agent-interfaces.zh-Hans.md)

---

## 找不到的词？

- 看 [Stage 5.2 — MCP](../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础) / [5.3 — Skills](../stages/05-claude-code-ecosystem.zh-Hans.md#53--skillsclaude-code-的行为层-claude-code-生态最关键的一层) / [5.4 — Plugins](../stages/05-claude-code-ecosystem.zh-Hans.md#54--plugins-与-marketplaces) 的内文
- 看 [Stage 1](../stages/01-llm-basics.zh-Hans.md) / [Stage 6](../stages/06-memory-rag.zh-Hans.md) / [Stage 7](../stages/07-multi-agent-production.zh-Hans.md) / [Stage 8](../stages/08-agent-interfaces.zh-Hans.md) 的延伸阅读清单
- 想要更白话的解释？[baihuaai.com（白话AI）](https://baihuaai.com) 是一个免费、无广告的简中入门词典，用大白话搭配现实类比讲 AI 术语（有“术语索引”与“零基础专区”）。
- 找不到的词 → 开 issue 或直接 PR 加进这份小词典

# Glossary

> [繁體中文](./glossary.md) | [简体中文](./glossary.zh-Hans.md) | **English**

> The roadmap leans heavily on terms like LLM, RAG, MCP, agent. Look up unfamiliar ones here in 30 seconds, then go back to reading the stage.
>
> Each entry gives **the smallest usable definition** (30-80 words + which stage covers it in depth) — not Wikipedia.

## 🌐 Unified terminology table (English ↔ Chinese, consistent across stages)

This table is the project's **enforced naming convention** — every stage uses the same Chinese readability label for each English term. If you see drift inside a stage, please file an issue.

| English term | Chinese readability label | Primary stage |
|---|---|---|
| Prompt Engineering | Prompt 設計 / Prompt 设计 | Stage 2 |
| Context Engineering | 上下文管理 | Stage 6 |
| Harness Engineering | Agent 執行系統設計 / Agent 执行系统设计 | Stage 7 |
| Tool Use | 工具使用 | Stage 3 |
| Function Calling | 函式 / 函数 / 工具呼叫 | Stage 3 |
| Structured Output | 結構化輸出 / 结构化输出 | Stage 3 |
| Agent Loop | Agent 執行迴圈 / Agent 执行循环 | Stage 3 |
| Framework | 框架 | Stage 4 |
| Orchestration | 協調與編排 / 协调与编排 | Stage 4 / 7 |
| Handoff | 任務交接 / 任务交接 | Stage 7 |
| Supervisor / Worker | 協調者 / 執行者 (协调者 / 执行者) | Stage 7 |
| Runtime | 執行層 / 执行层 | Stage 7 |
| Scaffolding | 支撐架構 / 支撑架构 | Stage 7 |
| Observability | 觀測與紀錄 / 观测与记录 | Stage 7 |
| Telemetry | 運行紀錄 / 运行记录 | Stage 7 |
| Eval | 效果評估 / 效果评估 | Stage 7 |
| Evaluation Harness | 評估框架 / 评估框架 | Stage 7 |
| Production | 可穩定使用 / 上線化 (可稳定使用 / 上线化) | Stage 7 |
| Production-grade | 可長期穩定使用的 / 可长期稳定使用的 | Stage 7 |
| Deployment | 部署 | Stage 7 |
| Cost Tracking | 成本追蹤 / 成本追踪 | Stage 7 |
| Latency | 延遲 / 等待時間 (延迟 / 等待时间) | Stage 7 |
| Vector DB | 向量資料庫 / 向量数据库 | Stage 6 |
| Retrieval | 檢索 / 检索 | Stage 6 |
| Reranking | 重排序 | Stage 6 |
| Long Context | 長上下文 / 长上下文 | Stage 6 |
| Fine-tuning | 模型微調 / 模型微调 | Stage 6 |
| Agent Interfaces | Agent 操作介面 / Agent 操作界面 | Stage 8 |
| Code Sandbox | 隔離程式執行環境 / 隔离程序执行环境 | Stage 8 |
| Cold Start | 啟動延遲 / 启动延迟 | Stage 8 |
| Reward Hacking | 鑽評分漏洞 / 钻评分漏洞 | Stage 7 / 8 |

→ For full definitions, see the sections below.

---

## 1. Basic concepts

### LLM (Large Language Model)

GPT, Claude, Gemini — models that take text in and produce text out. Fundamentally a pure function: input prompt → output text. **They don't browse the web, they don't remember past conversations** — those need to be wired up externally.

📍 Detail: [Stage 1](../stages/01-llm-basics.en.md)

### Model Provider / Provider API

**The direct door to a model company.** Examples include Anthropic API, OpenAI API, and Gemini API. You choose a model and send a prompt; the provider returns the result and charges you. It provides a model service, but it is not a CLI agent that reads and writes files on your computer.

### LLM Router / API Router

**One entry point that forwards requests to multiple models or backends.** [OpenRouter](https://openrouter.ai/docs/faq) is an example: through one API and billing entry point, you can choose different models and, depending on your settings, use provider routing or fallback. A Router is not a model, and it is not a coding agent such as OpenCode or Pi.

📍 Five identities compared: [Track A A1](../tracks/cli/A1-cli-intro.en.md)

### Token

LLMs see **tokens** (sub-word units), not characters. Roughly 1 English word ≈ 1.3 tokens, 1 Chinese character ≈ 1.5–2 tokens. LLM pricing and context windows are measured in tokens. "1M-token context" ≈ 750k English words.

📍 Detail: [Stage 1](../stages/01-llm-basics.en.md)

### Context Window

The maximum tokens an LLM can "see" in one call. **2026 frontier**: Claude Sonnet 5 / Opus 5 1M, GPT-5.6 1.05M, Gemini 3.5 Flash 1M (Pro series up to 2M), xAI Grok 4.5 500K, Mistral Medium 3.5 256k. **Bigger isn't always better** — beyond a length the LLM gets "Lost in the Middle".

### Prompt

The complete task package you give an LLM. It is not always one question; it can include instructions, input data, background, examples, and output limits, and these may be split across multiple messages. **Prompt engineering** is designing and testing this task package so results better meet success criteria. `system`, `developer`, and `user` are API message roles, not three fixed sections of a prompt and not synonyms for instruction.

📍 Detail: [Stage 2](../stages/02-prompt-engineering.en.md)

### Zero-shot / One-shot / Few-shot

Put "a few worked examples" in the prompt for the LLM to copy — the only difference between the three terms is **how many examples you give**:

- **Zero-shot** (0 examples): just ask, no examples at all.
- **One-shot** (1 example): give **1** input → output example first, then ask.
- **Few-shot** (a small number): give a small number of input → output examples first. There is no universal fixed count; it can show the format and boundary cases, but whether it helps must be checked with a fixed eval.

### Chain-of-Thought (CoT)

Early prompting techniques asked the LLM to write intermediate reasoning before the answer. Two common research forms are:

- **Few-shot CoT** (original paper, [Wei et al. 2022](https://arxiv.org/abs/2201.11903)): put a few examples with reasoning steps into the prompt, and the LLM imitates the reasoning
- **Zero-shot CoT** ([Kojima et al. 2022](https://arxiv.org/abs/2205.11916)): add "Let's think step by step" at the end of the prompt.

Do not treat outputting a full chain of thought as a general requirement now. Reasoning models usually reason internally. When you need to check the result, ask for **a short, verifiable reason after the final answer**. Which wording works better must be compared with the same eval.

---

## 2. Agents / Tool Use

### Agent

A system centered on an LLM that can **perceive state → make decisions → take actions → observe results** in a **loop**, repeating until the goal is completed. **Three core elements**:

- **LLM** (reasoning / planning / deciding)
- **Actions** (ways to do things — not limited to function calls. This can include writing and running code (CodeAct), operating a browser (computer use), retrieving from a KB (RAG retrieval), calling an MCP server, or pure planning / task decomposition)
- **Loop** (the heartbeat — the fundamental difference between an agent and plain LLM Q&A)

The difference is this: plain LLM = Q&A; agent = the three elements + a continuing loop until the goal is reached or the budget runs out. **ReAct is one agent pattern, not the definition of an agent** — CodeAct, computer-use, and planning agents are all agents.

📍 Detail: [Stage 3](../stages/03-tool-use-and-hello-agent.en.md)

### Tool Use / Function Calling

Lets the LLM call functions you defined (DB lookup, math, browser, …). Instead of plain text, the LLM returns `{"function": "search", "args": {…}}`. Your code executes it and feeds the result back to the LLM.

**The concept is the same; the API schema differs**:

- **Anthropic "Tool Use"**: uses `input_schema` (JSON Schema directly)
- **OpenAI / Ollama "Function Calling"**: wraps it in an outer `{"type": "function", "function": {...}}`
- The token representation the LLM sees differs internally, so when writing a cross-vendor SDK you need to map them correctly

📍 Detail: [Stage 3](../stages/03-tool-use-and-hello-agent.en.md)
📍 How to write good schemas: [Function Schema Design cheatsheet](schema-design-cheatsheet.en.md)

### ReAct (Reasoning + Acting)

The classic agent pattern: **Thought → Action (call tool) → Observation (see result) → Thought ...** loop until done. Most agent frameworks implement this internally.

📍 Detail: [Stage 3](../stages/03-tool-use-and-hello-agent.en.md)

### Structured Output

Make the LLM output **JSON or another fixed schema** instead of free text. All major LLM APIs have `response_format` or similar. Agent frameworks rely on it for LLM ↔ code communication.

### Agent Loop

The "LLM → tool → result → LLM" repeated cycle. Termination: LLM says "done" / step budget exhausted / cost cap hit.

⚠️ **This is the loop *inside a single run*** — one component of a harness. It shares a name with [Loop Engineering](#loop-engineering), Layer 4 of the five-layer ladder, which governs long-horizon execution *across* sessions. Different levels, same word. The boundary is drawn in [Stage 7](../stages/07-multi-agent-production.en.md).

### Self-Refine (Basic reflection / no memory)

The agent evaluates the previous round's output and changes the next round's behavior — an "Actor answers → Critic finds issues → Actor reads feedback and answers again" single-session loop. **It does not need a persistent memory layer**; it is purely a reasoning-loop mechanism, a sibling pattern to ReAct. Production agents (Cursor / Cline / Claude Code) run variants of this every day.

Representative paper: [Self-Refine (Madaan 2023)](https://arxiv.org/abs/2303.17651). **For the full Reflexion version** (with episodic memory), see 3 Memory / Retrieval / RAG.

📍 Detail + routing: [Stage 3 Reflection](../stages/03-tool-use-and-hello-agent.en.md#-reflection-reflexion--self-refine--concept--routing)

---

## 3. Memory / Retrieval / RAG

### Memory — Two Orthogonal Axes

"Memory" often gets lumped together, but there are actually **2 orthogonal classification axes**:

- **Time axis**: short-term (current conversation) vs long-term (persistent across sessions)
- **Content axis** (CoALA framework): **Working** (scratch space) / **Episodic** (past experiences) / **Semantic** (factual knowledge) / **Procedural** (how to do things)

→ The two axes do not conflict: long-term memory can contain **at the same time** episodic memory (what the user said last time), semantic memory (facts from the company's knowledge base), and procedural memory (tool sequences that worked before).

📍 Detail: [Stage 6 What is Memory + How to Design It](../stages/06-memory-rag.en.md#-what-is-memory--how-to-design-it) + [Stage 6 CoALA Framework](../stages/06-memory-rag.en.md#advanced-coala-framework--a-4-layer-taxonomy-for-agent-memory)

### RAG (Retrieval-Augmented Generation)

Two-stage architectural pattern:

1. **Ingest** (one-time / periodic): document → chunk → embed → store in a vector store (build a retrievable KB)
2. **Query** (every user question): embed the question → semantic search (or hybrid + BM25) → top-K chunks → put them into the prompt → LLM answers

**Solves the problem that the LLM does not know your private / changing / stale data**. Retrieval is **not limited to dense embeddings** — the production default is hybrid (dense + BM25) + reranker.

📍 Detail: [Stage 6](../stages/06-memory-rag.en.md)
📍 Paper: [Lewis et al. 2020](https://arxiv.org/abs/2005.11401)

### Reflexion (Full reflection / with episodic memory)

Unlike Self-Refine (2 Agents), Reflexion **requires a persistent episodic memory store** — after each trial, the agent **writes a reflection summary into memory**, then retrieves it into the prompt at the start of the next trial. **Accumulating lessons across trials** is the essence of Reflexion (not a single-session loop).

It is placed in 3 instead of 2 because it is **fundamentally a memory pattern** — the episodic memory store is core, not optional.

Representative paper: [Reflexion (Shinn 2023)](https://arxiv.org/abs/2303.11366).

📍 Detail: [Stage 6 Advanced: Full Reflexion with Persistent Memory](../stages/06-memory-rag.en.md#-advanced-full-reflexion-with-persistent-memory--track-b-elective)

### Embedding

Turn text / images into N-dimensional **vectors** so that things with similar meanings are close together. This roadmap defaults to **dense embeddings** (dense vectors produced by sentence-transformers / OpenAI ada-002, etc.); there are also **sparse embeddings** (BM25 / SPLADE, etc., based on lexical token matching) — production RAG often uses both together for hybrid search.

📍 Detail: [Stage 6](../stages/06-memory-rag.en.md)

### Vector DB

The storage layer for storing + efficiently querying embeddings. **The main query type = approximate nearest-neighbor (ANN)** — the whole point of a vector DB is that ANN is hundreds of times faster than brute-force cosine scanning. Examples: Pinecone / Chroma / Qdrant / Weaviate / pgvector.

📍 Detail: [Stage 6](../stages/06-memory-rag.en.md)

### Semantic Search

Use embeddings to compare "meaning similarity" rather than "exact string match". "How do I charge an EV" can retrieve "electric car battery tutorial". Traditional keyword search (BM25, etc.) can't do this.

### Chunking

Splitting long documents into embedding-friendly small pieces (typically 200–1000 tokens). **Chunk strategy directly affects RAG quality** — too small loses context, too long blurs relevance. Common: fixed-size, by paragraph, by structure (heading-based).

### Hybrid Search

Run semantic search and keyword search together, merge and rerank. Usually beats either alone. Production-grade RAG default.

### Reranking

After first-pass retrieval pulls top-50, use a more expensive but more accurate model (cross-encoder) to rerank to top-5 for the LLM. Cohere Rerank, bge-reranker, etc.

### Contextual Retrieval

Anthropic 2024 method — embed each chunk together with a summary of the document it came from, so "this chunk taken alone makes no sense" doesn't break retrieval.

📍 Detail: [Stage 6](../stages/06-memory-rag.en.md)

### Fine-tuning

Re-train the model on your own data, baking knowledge or behavior into the weights (unlike RAG — RAG injects data into the context at inference time and never changes the weights). Good for making the model reliably learn a **format / style / domain vocabulary**; **not** for stuffing in "the latest facts" (that is RAG's job — facts fine-tuned in go stale and are hard to update). In most agent scenarios, **try prompt + RAG first**, and only consider fine-tuning if that genuinely is not enough.

📍 Detail: [Stage 6](../stages/06-memory-rag.en.md)

---

## 4. Multi-Agent

### Multi-Agent

Multiple agents collaborating on one task. Common patterns:

- **Supervisor + Worker**: one agent plans/dispatches, others execute.
- **Swarm**: peer agents, no fixed supervisor.
- **Debate**: agents argue different positions, then form consensus.

📍 Detail: [Stage 7](../stages/07-multi-agent-production.en.md)

### Handoff

One agent transfers a task to another. Adds "how to pass context" and "who handles failure" beyond a plain function call.

### A2A (Agent-to-Agent) Protocol

An agent ↔ agent communication protocol started by Google and now governed by the Linux Foundation. Sibling to MCP, but for agent-to-agent rather than agent-to-tool. Reached **v1.0** in 2026 (150+ organizations, plus identity verification so one agent can confirm another really is who it claims to be).

---

## 5. Claude Code Ecosystem

### MCP (Model Context Protocol)

Anthropic's open protocol, introduced in 2024, that lets any LLM host (Claude Code, Cursor, your own agent) connect to external tool servers through one interface; donated to the Linux Foundation's Agentic AI Foundation in 2025-12. Think "**USB for LLMs**".

**Technically it standardizes 3 primitives**:

- **Tools**: functions an LLM can call (read DB / search web / send email…)
- **Resources**: data an LLM can read (file contents, API responses, DB rows…)
- **Prompts**: reusable prompt templates (triggered inside the host with `/`)

**Architecture**: server / client pattern — the tool server runs locally or remotely, and the LLM host connects as the client. The server exposes those primitives over one of two transports: **stdio** (local subprocess) or **Streamable HTTP** (remote); the older HTTP+SSE transport was deprecated in the 2025-03-26 spec revision.

📍 Detail: [Stage 5.2](../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol--foundation)

### Project Instructions

Shared rules that a CLI agent reads whenever it enters a project, like rules posted on a workshop wall. Put the project purpose, forbidden actions, verification commands, and delivery format here. Tools use different filenames and loading order, such as `AGENTS.md` for Codex/OpenCode V2, `CLAUDE.md` for Claude Code, and `GEMINI.md` for Gemini CLI.

📍 Getting started: [Track A A2](../tracks/cli/A2-cli-workflow.en.md)

### Skills / SKILL.md

Reusable "instruction cards" taken out when needed. A Skill is usually a folder containing `SKILL.md`, with optional references, scripts, or other files. Codex, Claude Code, Gemini CLI, and OpenCode V2 all have Skill mechanisms, but their search paths, frontmatter, loading methods, and permissions differ.

`description` should clearly say when to use the Skill and what it can do, so the agent can select the right one. A third-party Skill may run programs or call external tools; read its content and permissions before installing it, and do not treat a Skill as a security boundary.

📍 Getting started: [Track A A2](../tracks/cli/A2-cli-workflow.en.md); Claude Code deep dive: [Stage 5.3](../stages/05-claude-code-ecosystem.en.md#53--skills-claude-codes-behavior-layer--the-most-critical-layer-of-the-claude-code-ecosystem)

### One-off Prompt

A one-time instruction for the task in front of you, like a note needed only today. It contains this task’s scope, inputs, forbidden actions, and success conditions; move project rules used every time to project instructions, and repeated workflows to a Skill.

📍 Practice: [Track A A2 CLI-8](../tracks/cli/A2-cli-workflow.en.md#cli-8)

### Plugin / Marketplace

Package multiple Skills + slash commands + hooks + MCP configs into one shippable unit. A **Marketplace** is a catalog of plugins; users `claude plugin install` to grab community-built ones.

📍 Detail: [Stage 5.4](../stages/05-claude-code-ecosystem.en.md#54--plugins--marketplaces)

### Slash Command

Commands inside Claude Code that start with `/`, such as `/help`, `/compact`, and `/plan`. Older projects may keep a custom prompt in `.claude/commands/<name>.md`; that is a compatibility path. For a new reusable workflow, use `.claude/skills/<name>/SKILL.md`.

### CLAUDE.md

A markdown file at project root that Claude Code reads on every launch. Project-level rules / conventions / context (language, code style, files to avoid, etc.).

### Hooks

Scripts that run before or after specific Claude Code events. **The official system supports 7 event types**:

| Hook | Trigger time | Typical use |
|---|---|---|
| `PreToolUse` | **Before** a tool call | Block dangerous operations (`rm -rf`, destructive ops), rewrite parameters |
| `PostToolUse` | **After** a tool call | Logging, auto-format files that were just written |
| `UserPromptSubmit` | When the user submits a message | Add context (git status / current time) |
| `Notification` | When Claude Code emits a notification | Desktop toast / Slack ping |
| `Stop` | When the session ends | Auto-commit / cleanup |
| `PreCompact` | Before auto-compact | Promote important decisions into memory |
| `PostCompact` | After compact | Check what context got compressed |

Configuration: add a `"hooks"` block in `.claude/settings.json` and point it at your script path.

### Deep Agent

An agent design that comes "fully equipped" — beyond just calling tools, it has built-in planning (a todo list), long-term memory (a filesystem), division of labor via subagents, and loadable skills. Contrast: a plain agent is just an LLM plus a few tools. Reference implementation: LangChain's [deepagents](https://github.com/langchain-ai/deepagents).

---

### Subagent

A spawned agent from the main Claude Code session, with its own context window, dedicated to a specific task. E.g. "spin up a code-reviewer subagent for this diff."

How to set up: put frontmatter + system prompt + tool whitelist in `.claude/agents/<name>.md`. The main session invokes it with the Task tool (automatic parallel / sequential). **Compared with framework-based multi-agent**: a subagent does not require LangGraph / CrewAI or similar frameworks; markdown is enough, but it is tied to the Claude Code runtime. Full guide: [Stage 5.5](../stages/05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature); **15 copy-paste dispatch recipes** → [`subagent-cookbook.en.md`](./subagent-cookbook.en.md).

---

## 6. Production / Eval / Cost

### CI (Continuous Integration)

A checkpoint that automatically runs fixed work when a push or PR appears. CI can run tests, lint, or a read-only agent review, but its tokens, secrets, repo permissions, and triggers must be limited separately. A successful CI run does not mean auto-merge is safe or human review can be skipped.

📍 Practice: [Track A A3 CLI-10](../tracks/cli/A3-cli-production.en.md#cli-10)

### Eval (Evaluation)

Use a fixed test case set to check a prompt or agent. The smallest eval is like a small answer card: the same questions, clear success conditions, and a rerun after every change. As it grows, it can also record accuracy, latency, and cost. Common tools include promptfoo, LangSmith, and Langfuse evals.

📍 Getting started: [Stage 2](../stages/02-prompt-engineering.en.md); full eval harness: [Stage 7](../stages/07-multi-agent-production.en.md)

### Observability

Keep the agent’s steps, model, tools, usage, time, and result, like a receipt plus a dashcam recording. When a bug appears, you can find the failed step; mark unavailable fields as “unconfirmed” instead of guessing. Common tools include Langfuse, Phoenix, and Helicone.

📍 Getting started: [Track A A3 CLI-11](../tracks/cli/A3-cli-production.en.md#cli-11); deep dive: [Stage 7](../stages/07-multi-agent-production.en.md)

### Prompt Caching

LLM caches the prefix of a prompt; on repeat, only the new suffix is billed at full price (Anthropic 90% off cached, OpenAI 50% off). Long-context repeated queries save a lot.

### Streaming

LLM returns tokens as they're generated (one at a time) instead of waiting for the full response. Better UX (looks like typing); technically uses SSE or chunked transfer. **Default for production interactive apps**. Trade-offs: client must handle partial responses; ReAct tool-call parsing waits for stream end.

### Batch API

Bundle a large number of LLM requests for delayed (≤24h) processing. **Typically 50% off (Anthropic, OpenAI)**. Good for non-interactive: batch summarization, batch classification, eval suites, ETL pipelines. **Don't use for interactive chat** — latency unacceptable.

### Token Cost / Inference Cost

Per LLM call: input tokens × input price + output tokens × output price. Costs of an agent's ReAct loop add up fast — a single grep over a large codebase can run 100k tokens.

### Guardrails

Rule layer that prevents the LLM from doing bad things — block prompt injection, PII leakage, harmful output, etc. NeMo Guardrails, Guardrails AI, etc.

### Prompt Injection

Hiding malicious instructions inside content the LLM will read (web pages, documents, tool results) so it ignores its real task and does what the attacker wants. Root cause: the LLM can't tell "instructions" apart from "instructions smuggled inside data". Defenses: least privilege, isolating untrusted content, human review of high-risk actions. Related: lethal trifecta, Guardrails.

### Lethal Trifecta

Simon Willison's framing: an agent becomes exploitable when it has all three of (1) access to private data, (2) exposure to untrusted content, (3) the ability to communicate externally — at which point prompt injection can make it steal and exfiltrate data. The defense is to break at least one leg (commonly: cut external comms, or isolate untrusted input).

---

## 7. Buzzwords / Loose Terms

### CLI Agent

An agent / harness that runs in a terminal and, within the scope you allow, reads files, edits files, and runs commands (Claude Code, Codex, OpenCode, Pi, Aider, Gemini CLI, etc.). **It is the workbench, not the LLM inside it.** The same CLI may be tied to one model ecosystem or let you switch providers.

📍 Detail: [Track A A1](../tracks/cli/A1-cli-intro.en.md), [`resources/cli-agents-guide.en.md`](cli-agents-guide.en.md)

### BYO API Key (Bring Your Own)

Tools that let you provide your own provider API key instead of using only the tool’s built-in subscription sign-in. Aider, OpenCode, goose, and Pi can connect to one or more providers; Claude Code and Codex also have subscription or API authentication paths listed in their official docs. Supported methods change, so read the tool’s official authentication docs before use.

### Local LLM / On-Device

Models running on your own machine. Ollama, llama.cpp, MLX, and LocalAI are **local runtimes**: they run the model and are not coding agents. Data stays off the cloud for this workflow only when the model, tools, and data paths all remain local and no cloud service is called; test capability and speed with your own task and hardware.

📍 Detail: [Stage 1](../stages/01-llm-basics.en.md)

### Quantization

Compress model weights from fp16 down to int8 / int4 to save memory and increase speed at small accuracy cost. Local LLM users see this constantly (Q4_K_M, Q8_0, etc.).

### Hallucination

The LLM "confidently asserts something false" — invents APIs, fabricates numbers and presents them as fact. Every production agent needs defenses (RAG / structured output / eval / guardrails).

### Frontier Model

The current top tier (**2026-07**: Claude **Opus 5** (2026-07-24, `claude-opus-5`, 1M, $5/$25 — the default starting point the official docs recommend), OpenAI **GPT-5.6** (Sol / Terra / Luna — three tiers, 1.05M context, available in ChatGPT, Codex, and the API); **2026-06 (late)**: Claude Sonnet 5 (best speed-intelligence balance, close to Opus-class but cheaper), Google Gemini 3.5 Flash, xAI Grok 4.5 (500K context), Mistral Medium 3.5; **2026-06 (early)**: Claude Fable 5 (Mythos-class, above Opus) shipped, was suspended 2026-06-12 by a US export-control directive, but **the controls were lifted 2026-06-30 and [Fable 5 was redeployed globally 2026-07-01](https://www.anthropic.com/news/redeploying-fable-5)** (Mythos 5 restored only for approved US orgs); **2026-05**: GPT-5.5, Claude Opus 4.8 (the Opus-class flagship at the time; superseded by Opus 5 in 2026-07 but still available), Gemini 3.1 Pro, DeepSeek-V4-Pro, etc.). Use frontier for hard reasoning; use cheap small models for simple classification / translation to save cost.

### Context Engineering

The discipline of engineering **what information goes into the context window on each LLM call** — dynamically assembling RAG retrieval results, memory, tool definitions, and conversation history into the context the model can see. Karpathy 2025: the delicate art of putting **just the right information for the next step** into the window. The key question is *what goes in the window*, not "how many calls are involved." **The next layer above prompt engineering** — prompt engineering shapes **strings**; context engineering shapes **information**.

📍 Detail: [Stage 2 closing](../stages/02-prompt-engineering.en.md) / [Stage 6](../stages/06-memory-rag.en.md) / [Stage 7](../stages/07-multi-agent-production.en.md)
📍 Further: [`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering)

### Harness Engineering

The discipline of engineering the **execution and control layer around the model** — everything that is not model weights and not just the prompt string itself: agent loop / tool registry / context manager / permissions / safety layer / memory layer / eval / observability / retry / circuit breaker, etc. Simon Willison 2025: **coding agent = LLM + harness**. Addy Osmani: harness = all the code that is not the model itself. [OpenAI also used the term "Harness Engineering" in February 2026](https://openai.com/index/harness-engineering). Claude Code, Cursor, OpenCode, etc. are harnesses. **A framework wraps an LLM into an agent; a harness wraps an agent into a product that can actually go live.**

Contrast:

- **Framework** (Stage 4) defines the **API**: what the interface you call looks like
- **Harness** (this term) defines the **runtime**: how it runs, how it recovers, how it is observed

📍 Discipline-level concept (**8 core components** / prompt→context→harness five-layer engineering split / framework vs harness): [Stage 7 Harness Engineering](../stages/07-multi-agent-production.en.md)
📍 Reference implementation case study (reading Claude Code source): [Stage 5 5.7](../stages/05-claude-code-ecosystem.en.md)
📍 Further: [`anthropics/claude-agent-sdk-python`](https://github.com/anthropics/claude-agent-sdk-python), [`ai-boost/awesome-harness-engineering`](https://github.com/ai-boost/awesome-harness-engineering), [`ZhangHanDong/harness-engineering-from-cc-to-ai-coding`](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding)

### Loop Engineering

Layer 4 in the five-layer engineering split (see [Stage 7](../stages/07-multi-agent-production.en.md), the canonical source for the full ladder and each layer's purpose): designing and tuning an agent's iteration loop itself (goal, tools, context management, termination logic, error handling) so long-running, multi-step, cross-session execution stays reliable and on-target. Related: harness, Dynamic Workflows, ReAct.

⚠️ **Do not confuse this with the [Agent Loop](#agent-loop) inside a harness**. This layer governs the long-horizon problem *across many runs*; `Agent Loop` is a harness component governing the mechanical cycle *within one run*.

### Graph Engineering

Designing an agent's execution flow as an **explicit graph**: nodes are steps (as of 2026 a node can hold an entire agent run, not just a single function), edges are transition conditions, and nodes pass around a schema'd state that can be checkpointed and replayed. **Two things to know when you meet this term**:

- **The "graph" here is a control / execution graph, not the knowledge-graph retrieval of GraphRAG** — for that, see [Stage 6](../stages/06-memory-rag.en.md). The two are frequently conflated.
- **It is a name that became popular in July 2026, not a new technique.** LangGraph has worked this way since 2023, and LangChain itself says the idea is not new; Anthropic calls the equivalent mechanism *dynamic workflows*, while Google ADK and Microsoft Agent Framework say *graph-based workflow(s)* — none of the three vendors' docs use the phrase "graph engineering".

**Relationship to loops**: this is not either-or. **Inside a box, the agent loops; between boxes, you define the order**. A graph puts several loops into boxes, then orders those boxes. If you put everything back into one box, you are back to a plain loop. A box does not have to contain an agent either; it can be a tool, a check, or a "human approval required before continuing" gate. For the full five-layer ladder, see [Stage 7](../stages/07-multi-agent-production.en.md) (canonical).

What is actually worth learning lives in [Stage 4's multi-agent patterns](../stages/04-agent-frameworks.en.md) and the runnable [`examples/stage-4/03-graph-workflow/`](../examples/stage-4/03-graph-workflow/README.en.md) (`StateGraph` / conditional edges / checkpointer). Related: harness, Loop Engineering, orchestration.

---

## 8. Agent Interfaces

### Computer Use (screen-level agent)

An agent operates real desktop apps via **screenshot → vision → coordinates → simulated mouse/keyboard** — no API needed, the agent uses the screen like a human. Representative: Anthropic Claude Computer Use (Opus 5 / Sonnet 5), OpenAI Codex desktop, Google Gemini in Chrome. **Anthropic public beta opened Oct 2024; OSWorld v1 hit 76.26% by May 2026 but then approached saturation — OSWorld 2.0 (2026-06, long-horizon) reset SOTA to ~20% (Opus 4.8)**.

📍 Full coverage + 4-vendor comparison: [Stage 8 Computer Use](../stages/08-agent-interfaces.en.md)

### Browser Use (web-level agent)

An agent operates web pages, primarily via **DOM-aware navigation** (direct CSS selector queries) with vision fallback. Closed-source: Comet / Dia / Gemini in Chrome (Atlas discontinued Aug 2026). OSS leader: [browser-use](https://github.com/browser-use/browser-use) (★ 105k+).

📍 Full coverage + 5-vendor comparison + OSS frameworks: [Stage 8 Browser Use](../stages/08-agent-interfaces.en.md)

### Sandbox (code execution isolation)

Runs agent-written code in an isolated environment instead of the host — avoids `rm -rf /`, internet data exfiltration, credential theft. Representatives: E2B (Firecracker microVM), Daytona (container), Modal (GPU sandbox), Vercel, Cloudflare. **OpenAI Agents SDK natively supports these as of April 2026**.

📍 Full 9-row terminology glossary + 7-vendor comparison: [Stage 8 Code Sandbox](../stages/08-agent-interfaces.en.md)

### microVM (micro Virtual Machine)

A slimmed-down VM with minimal footprint, < 100ms startup, yet still has an **independent kernel** — sits between Docker containers (fast + weak isolation) and full VMs (slow + strong isolation). **Most agent sandboxes choose microVM**. Implementation example: Firecracker (AWS, used by E2B).

📍 Full comparison: [Stage 8 terminology glossary](../stages/08-agent-interfaces.en.md)

### Firecracker

AWS's open-source microVM, written in Rust, **the underlying technology of AWS Lambda** and E2B sandbox isolation. Provides strong isolation + fast startup.

### gVisor

Google's "user-space kernel" — intercepts syscalls and emulates them itself, no hypervisor required. Sits between containers and VMs.

---

## Term not here?

- Read the actual stage content: [Stage 5.2 MCP](../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol--foundation) / [5.3 Skills](../stages/05-claude-code-ecosystem.en.md#53--skills-claude-codes-behavior-layer--the-most-critical-layer-of-the-claude-code-ecosystem) / [5.4 Plugins](../stages/05-claude-code-ecosystem.en.md#54--plugins--marketplaces)
- Required reading lists in [Stage 1](../stages/01-llm-basics.en.md) / [Stage 6](../stages/06-memory-rag.en.md) / [Stage 7](../stages/07-multi-agent-production.en.md) / [Stage 8](../stages/08-agent-interfaces.en.md)
- Want plainer language? [baihuaai.com (白话AI)](https://baihuaai.com) is a free, ad-free Simplified-Chinese beginner glossary that explains AI terms in everyday words with real-world analogies (has a term index + a zero-basics zone).
- Missing? Open an issue or PR a new entry.

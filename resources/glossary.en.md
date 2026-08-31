# Glossary

> [繁體中文](./glossary.md) | [简体中文](./glossary.zh-Hans.md) | **English**

When an unfamiliar term appears, you do not need to stop reading the whole chapter. Find one plain-language explanation here, then return to the Stage you were working on.

## ⚡ Start with these 12 terms

- [**Prompt**](#prompt) — the complete task package you give a model, including the job, data, examples, and limits.
- [**Token**](#token) — a small unit a model uses to split input; usage limits and billing often count it.
- [**Context Window**](#context-window) — the information space a model can consider together in one call.
- [**Agent**](#agent) — an AI-powered system that acts on a person's behalf within rules, checks results, and adjusts its next step.
- [**Tool Use**](#tool-use--function-calling) — the model requests a tool, but the program checks and executes it.
- [**Agent Loop**](#agent-loop) — the running cycle of deciding, acting, and observing until completion or a stop condition.
- [**RAG**](#rag-retrieval-augmented-generation) — retrieve evidence first, then give that evidence to the model for an answer.
- [**Memory**](#memory--two-orthogonal-classification-axes) — save information that will matter later, then read it back when needed.
- [**MCP**](#mcp-model-context-protocol) — an open protocol for connecting AI applications to tools and data in a shared way.
- [**Eval**](#eval) — fixed cases and success rules that show whether a change really improved the system.
- [**Agent Harness**](#agent-harness) — the system around a model that manages tools, permissions, state, records, and stopping.
- [**Workflow Graph**](#workflow-graph) — nodes and edges that make steps, branches, and shared state explicit.

## 🧭 Separate five tool identities first

One screen may contain a model, a Router, and an Agent at the same time. Ask what job each product performs before comparing their names.

<table>
<thead>
<tr><th>Identity</th><th>Plain-language job</th><th>Example and boundary</th></tr>
</thead>
<tbody>
<tr><td><strong>Model Provider / API</strong></td><td>The model company's service entrance.</td><td><a href="https://platform.claude.com/docs/en/api/overview">Anthropic API</a>; it returns model output but is not an Agent that edits files.</td></tr>
<tr><td><strong>LLM Router</strong></td><td>One entrance that forwards requests to models or providers.</td><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a>; it is neither a model nor a coding agent.</td></tr>
<tr><td><strong>Model Runtime</strong></td><td>Loads and runs a model locally or as a service.</td><td><a href="https://docs.ollama.com/api/introduction">Ollama</a>; it exposes a model API but does not edit a project by itself.</td></tr>
<tr><td><strong>Coding Agent / Harness</strong></td><td>Reads files, edits files, runs commands, and reports results.</td><td><a href="https://opencode.ai/docs">OpenCode</a> and <a href="https://github.com/earendil-works/pi">Pi</a>; the model inside can be changed.</td></tr>
<tr><td><strong>Agent Framework</strong></td><td>Helps developers combine Agents, tools, state, and workflows.</td><td><a href="https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/">Microsoft Agent Framework</a>; it is a toolkit, not a model.</td></tr>
</tbody>
</table>

<details markdown="1">
<summary>Maintainers: fixed project terminology (37 terms)</summary>

This table keeps names consistent across Stages. General readers do not need to memorize it first.

<table>
<thead>
<tr><th>Group</th><th>English term</th><th>Project meaning</th><th>Main Stage</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Input and information</th><td>Prompt Engineering</td><td>Prompt design</td><td>Stage 2</td></tr>
<tr><td>Context Engineering</td><td>Context management</td><td>Stage 6 / 7</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="17">Agent execution</th><td>Agent Production Engineering</td><td>Making Agents dependable</td><td>Stage 7</td></tr>
<tr><td>Harness Engineering</td><td>Agent execution-system design</td><td>Stage 7</td></tr>
<tr><td>Loop Engineering</td><td>Agent loop design</td><td>Stage 7</td></tr>
<tr><td>Graph Engineering</td><td>Workflow Graph engineering</td><td>Stage 4 / 7</td></tr>
<tr><td>Tool Use</td><td>Using tools</td><td>Stage 3</td></tr>
<tr><td>Function Calling</td><td>Function / tool calling</td><td>Stage 3</td></tr>
<tr><td>Tool Schema</td><td>Tool description card</td><td>Stage 3</td></tr>
<tr><td>Tool Call</td><td>Tool request</td><td>Stage 3</td></tr>
<tr><td>Tool Result</td><td>Tool result</td><td>Stage 3</td></tr>
<tr><td>Structured Output</td><td>Machine-readable output</td><td>Stage 3</td></tr>
<tr><td>Agent Loop</td><td>Agent execution loop</td><td>Stage 3</td></tr>
<tr><td>Framework</td><td>Toolkit</td><td>Stage 4</td></tr>
<tr><td>Orchestration</td><td>Coordination and scheduling</td><td>Stage 4 / 7</td></tr>
<tr><td>Handoff</td><td>Task handoff</td><td>Stage 7</td></tr>
<tr><td>Supervisor / Worker</td><td>Coordinator / executor</td><td>Stage 7</td></tr>
<tr><td>Runtime</td><td>Execution layer</td><td>Stage 7</td></tr>
<tr><td>Scaffolding</td><td>Supporting structure</td><td>Stage 7</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="9">Quality and production</th><td>Observability</td><td>Inspectable operation records</td><td>Stage 7</td></tr>
<tr><td>Telemetry</td><td>Runtime records</td><td>Stage 7</td></tr>
<tr><td>Eval</td><td>Outcome evaluation</td><td>Stage 7</td></tr>
<tr><td>Evaluation Harness</td><td>Evaluation system</td><td>Stage 7</td></tr>
<tr><td>Production</td><td>Dependable use / going live</td><td>Stage 7</td></tr>
<tr><td>Production-grade</td><td>Dependable over time</td><td>Stage 7</td></tr>
<tr><td>Deployment</td><td>Deployment</td><td>Stage 7</td></tr>
<tr><td>Cost Tracking</td><td>Cost tracking</td><td>Stage 7</td></tr>
<tr><td>Latency</td><td>Waiting time</td><td>Stage 7</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">Retrieval and models</th><td>Vector DB</td><td>Vector database</td><td>Stage 6</td></tr>
<tr><td>Retrieval</td><td>Retrieval</td><td>Stage 6</td></tr>
<tr><td>Reranking</td><td>Reordering candidates</td><td>Stage 6</td></tr>
<tr><td>Long Context</td><td>Long context</td><td>Stage 6</td></tr>
<tr><td>Fine-tuning</td><td>Adjusting model weights</td><td>Stage 6</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Interfaces</th><td>Agent Interfaces</td><td>Ways an Agent acts</td><td>Stage 8</td></tr>
<tr><td>Code Sandbox</td><td>Isolated code environment</td><td>Stage 8</td></tr>
<tr><td>Cold Start</td><td>Startup delay</td><td>Stage 8</td></tr>
<tr><td>Reward Hacking</td><td>Gaming the score</td><td>Stage 7 / 8</td></tr>
</tbody>
</table>

</details>

## 📚 Look up terms by topic

The sections below are not a new reading order. Jump directly to the term you just encountered.

## 1. Basic concepts

### LLM (Large Language Model)

An **LLM** is a model that generates content from input and learned patterns. It can request a tool, but an outside program is what actually reads a file, uses the network, or sends a message.

📍 Details: [Stage 1](../stages/01-llm-basics.en.md)

### Model Provider / Provider API

A **Model Provider / Provider API** is the service entrance to a model company. Your program sends messages, the provider returns results and bills according to its plan; it is not a coding agent.

### LLM Router / API Router

An **LLM Router / API Router** works like a switchboard: one API can forward requests to different models or backends. It chooses a route; it does not become the model or the Agent.

### Model Runtime

A **Model Runtime** loads a model and exposes an inference API. Ollama, llama.cpp, and [MLX LM](https://github.com/ml-explore/mlx-lm) fit this identity; a separate Agent or application is still needed to read files or run commands. MLX itself is an array framework; MLX LM is the package meant here for running LLMs with MLX.

### Token

A **Token** is a small unit used when a model splits text or other input. Tokenizers differ, so there is no universal characters-per-token formula; use the counter for the model you selected.

📍 Details: [Stage 1](../stages/01-llm-basics.en.md)

### Context Window

A **Context Window** is the token space a model can consider in one call. A larger space does not make every part equally important; include what the task needs, then check [Stage 1](../stages/01-llm-basics.en.md) for current official limits.

### Prompt

A **Prompt** is the complete task package sent to a model, not only one question. It may include instructions, input data, background, examples, success criteria, and an output format; **Prompt Engineering** designs and tests that package with Evals.

📍 Details: [Stage 2](../stages/02-prompt-engineering.en.md)

### Zero-shot / One-shot / Few-shot

These names only count how many demonstrations appear in the Prompt:

- **Zero-shot**: give no demonstration; state the task directly.
- **One-shot**: give one example input and answer first.
- **Few-shot**: give a small set of examples to show format or boundaries.

More examples are not automatically better. Compare them with the same Eval.

### Chain-of-Thought (CoT)

**Chain-of-Thought (CoT)** is a prompting research method in which a model goes through intermediate reasoning before answering. Early work includes [Few-shot CoT](https://arxiv.org/abs/2201.11903) and [Zero-shot CoT](https://arxiv.org/abs/2205.11916). In practice, ask for short, verifiable reasons and evidence rather than a model's private reasoning transcript.

## Model training and adaptation

### Pre-training

**Pre-training** uses large amounts of data to teach a model general patterns. It changes model weights and produces a Base Model that can be adapted later.

### Post-training

**Post-training** is the training stage after a Base Model is complete. It uses demonstrations, preferences, or feedback to help the model follow instructions and complete tasks safely.

### Inference

**Inference** is when a trained model receives this input and produces this result. It uses the model; it does not retrain it.

### Fine-tuning

**Fine-tuning** continues changing model weights with smaller, specialized data. It suits repeated behavior or formats; facts that change daily usually belong in RAG or tools.

### SFT (Supervised Fine-Tuning)

**SFT** gives the model good inputs and answers to imitate. It is a common Post-training method and changes model weights.

### DPO (Direct Preference Optimization)

**DPO** teaches preferences from pairs of better and worse answers. It needs trustworthy preference data and changes weights.

### RLHF / RL

**RLHF/RL** trains a model with human or rule-based feedback. Poorly designed feedback can teach the model to exploit the score, so an independent Eval is still needed.

### GRPO

**GRPO** compares several answers to the same question, then updates the model from their relative results. It is one Post-training method, not a requirement for every project.

### PEFT / LoRA

**PEFT** is a group of methods that trains fewer parameters; **LoRA** freezes the original weights and trains added low-rank matrices. They reduce the parameters that must be updated, but still need data and Eval.

### Distillation

**Distillation** teaches a smaller Student Model from a larger Teacher Model. It often aims to shrink a model or lower inference cost; test the result on your own task.

📍 Optional guide: [Model training and adaptation guide](model-training-guide.en.md)

## 2. Agent / tool use

### Agent

An **Agent** is an AI-powered system that acts on a person's behalf within clear rules and permissions. Once a person gives it a goal, it reads the current state, decides the next step, uses tools when needed, then, based on the result, continues, corrects course, stops, or hands control back to the person.

A one-shot chatbot or a fixed script with every step hard-coded in advance is not necessarily an Agent. The key is whether the AI decides how to achieve the goal based on the current state while it runs. This boundary follows [OpenAI's practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) and [Anthropic's explanation of effective agents](https://www.anthropic.com/engineering/building-effective-agents).

### Tool Use / Function Calling

**Tool Use / Function Calling** lets a model produce a structured tool request. The model only says what it wants to call; your program must still validate the tool name, arguments, and permissions before execution.

📍 Details: [Stage 3](../stages/03-tool-use-and-hello-agent.en.md)

### Tool Schema

A **Tool Schema** is a tool description card with its name, purpose, input fields, types, and required values. A schema constrains format, but it cannot prove that model-supplied content is safe or true.

### Tool Call

A **Tool Call** contains the tool name and arguments requested by a model. Treat it as untrusted input: validate it before executing, rejecting, or asking a person for approval.

### Tool Result

A **Tool Result** is what the program returns to the model after running a tool. Success, failure, and the original call ID must line up so the model knows what happened.

### ReAct (Reasoning + Acting)

**ReAct** alternates observable Actions and Observations so a model can choose the next step from new evidence. It comes from the [ReAct paper](https://arxiv.org/abs/2210.03629); implementations still need step limits, tool permissions, and stop conditions.

### Structured Output

**Structured Output** requires output to follow a JSON Schema or type. It makes parsing dependable, but valid structure does not make the contents true; values, sources, and business rules still need checks.

### Agent Loop

An **Agent Loop** is the cycle that actually runs: the model chooses an action, the program executes it, the model reads the result, and then chooses again. It must stop on completion, error, timeout, budget limits, or maximum steps.

### Workflow Graph

A **Workflow Graph** uses nodes, edges, branches, and state to make a route explicit. A node may contain an Agent Loop, ordinary code, a tool, or human approval; not every Agent needs this shape.

📍 Details: [Stage 4](../stages/04-agent-frameworks.en.md)

### Self-Refine (basic reflection / no memory)

**Self-Refine** asks a model to produce an answer, use feedback, and revise one or more times. The original method is in the [Self-Refine paper](https://arxiv.org/abs/2303.17651); without an outside check and stop rule, repeated rewriting can remain wrong.

## 3. Memory / retrieval / RAG

### Memory — two orthogonal classification axes

**Memory** saves information in a storage layer for later use. It can be grouped by duration as short-term or long-term, and separately by content as episodic, semantic, or procedural; these are two different axes.

### RAG (Retrieval-Augmented Generation)

**RAG** means retrieving evidence before asking a model to answer from it. The original method appears in the [RAG paper](https://arxiv.org/abs/2005.11401). It does not guarantee correctness; data quality, retrieval, citations, and answer faithfulness still need tests.

📍 Details: [Stage 6](../stages/06-memory-rag.en.md)

### Reflexion (full reflection / episodic memory)

**Reflexion** stores earlier attempts, feedback, and reflections as episodic memory for later attempts. It adds memory across attempts to the basic Self-Refine idea; see the [Reflexion paper](https://arxiv.org/abs/2303.11366).

### Embedding

An **Embedding** turns text, images, or other data into vectors so a system can compare similarity. Dense and sparse representations capture different signals; evaluate them on your own queries instead of choosing by vector size alone.

### Vector DB

A **Vector DB** stores vectors, metadata, and indexes and retrieves nearby items. It is one retrieval layer, not the whole RAG pipeline; chunking, querying, Reranking, and answering are separate steps.

### Semantic Search

**Semantic Search** finds content by similar meaning rather than only identical words. It helps with paraphrases, while names, IDs, and exact strings often still need keyword search.

### Chunking

**Chunking** divides a long document into smaller retrievable pieces. Test the split against document structure and real questions; no fixed size works for every dataset.

### Hybrid Search

**Hybrid Search** combines semantic-vector and keyword signals before merging results. It often balances similar meaning with exact-name matches.

### Reranking

**Reranking** uses another model or rule to inspect initial candidates and move the most relevant ones upward. It may improve quality, but it also adds latency and cost.

### Contextual Retrieval

**Contextual Retrieval** adds a short piece of document context to each chunk before indexing it. Anthropic's [method description](https://www.anthropic.com/engineering/contextual-retrieval) evaluates contextual embeddings together with contextual BM25; measure the effect on your own data.

## 4. Multi-Agent

### Multi-Agent

**Multi-Agent** means two or more Agents divide or hand off work. Use it when roles, tools, permissions, or context truly need separation; adding more Agents does not automatically improve an answer.

### Handoff

A **Handoff** moves a task and the required context from one Agent to another. A good handoff states the goal, completed work, evidence, remaining work, and stopping conditions.

### A2A (Agent-to-Agent) Protocol

**A2A** is an open protocol that helps independent, potentially opaque Agents discover capabilities, exchange messages, and manage collaborative tasks. It handles Agent-to-Agent interoperability; use the [official latest specification](https://a2a-protocol.org/latest/specification/) instead of freezing a version number in a tutorial.

## 5. Claude Code ecosystem

### MCP (Model Context Protocol)

**MCP** is an open protocol that connects AI applications to external data and capabilities. A Server may expose **Prompts**, **Resources**, and **Tools**, while the Host / Client decides presentation, consent, and transport. Use the [current specification](https://modelcontextprotocol.io/specification) for fields, transports, and security rules.

📍 Details: [Stage 5.2](../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol--foundation)

### Project Instructions

**Project Instructions** are shared rules a tool reads for a project, such as purpose, prohibited actions, verification commands, and delivery format. File names and loading order vary by tool, so one configuration is not automatically portable to every CLI.

📍 Start: [Track A A2](../tracks/cli/A2-cli-workflow.en.md)

### Skills / SKILL.md

A **Skill** is an operation card loaded when needed. Under the [Agent Skills specification](https://agentskills.io/specification), a Skill is at least a directory with `SKILL.md` and may also contain scripts, references, and assets; inspect third-party Skills and permissions before installing them.

### One-off Prompt

A **One-off Prompt** is an instruction used only for the current task. Put rules that apply every time in Project Instructions, and turn a repeated workflow into a Skill.

### Plugin / Marketplace

A **Plugin** packages components such as Skills, commands, hooks, or MCP configuration for distribution; a **Marketplace** is a catalog for finding and installing those packages. This is a product feature, not a universal component every Agent needs.

### Slash Command

A **Slash Command** begins with `/` and is supplied by an application. It may open a feature, setting, or reusable workflow; names and behavior come from the tool's current documentation.

### CLAUDE.md

**CLAUDE.md** is one project-instruction file Claude Code can read to learn how a project works. It is context for the model to follow, not an enforcement boundary that can block unsafe operations by itself.

### Hooks

**Hooks** run a fixed check or action when a selected event occurs. They work well for linting, logging, notifications, or blocking high-risk actions; events and configuration evolve, so use the [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks) instead of memorizing a count.

### Deep Agent

**Deep Agent** is not one formal cross-vendor standard. LangChain's [deepagents](https://github.com/langchain-ai/deepagents) uses the label for an agent harness with planning, files, subagents, and context management; check which definition an author means.

### Subagent

A **Subagent** is an isolated worker that receives delegated work from a main Agent and usually has its own context. Current Claude Code configuration, inheritance, and permission boundaries are in the [official documentation](https://code.claude.com/docs/en/sub-agents); a Subagent still needs a clear task and verification.

📍 Learn: [Stage 5.5](../stages/05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature) · [copyable recipes](./subagent-cookbook.en.md) · [advanced composition](./subagent-advanced.en.md)

## 6. Production / eval / cost

### CI (Continuous Integration)

**CI** automatically runs fixed checks on a push or PR, such as tests, lint, and security scans. A green CI result only says the configured checks passed; it does not replace review or authorize deployment.

### Eval

An **Eval** compares a Prompt, model, or Agent with fixed inputs, success criteria, and records. Start with a small representative set and rerun the same cases before and after a change to compare quality, cost, and latency.

📍 Start: [Stage 2](../stages/02-prompt-engineering.en.md); Agent systems: [Stage 7](../stages/07-multi-agent-production.en.md)

### Observability

**Observability** leaves inspectable records of Agent steps, tools, state, timing, usage, and results. It works like a flight recorder; redact secrets, private data, and unnecessary Prompt content.

### Prompt Caching

**Prompt Caching** reuses a previously cached, byte-identical Prompt prefix to reduce repeated processing; similar but different content is a cache miss. Minimum length, retention, and price vary by provider, so check the [current caching documentation](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) and record actual usage.

### Streaming

**Streaming** sends small pieces as the model produces them instead of waiting for a complete answer. The interface reacts sooner, but the client must handle partial content, cancellation, errors, and incomplete tool calls.

### Batch API

A **Batch API** groups requests that do not need an immediate response. It suits offline classification, summaries, or Evals; completion time, limits, and discounts come from the provider's current documentation.

### Token Cost / Inference Cost

**Token Cost / Inference Cost** is the price of model inference. The smallest formula is input usage times input price plus output usage times output price; an Agent also adds every loop turn, tool service, and compute cost.

### Guardrails

**Guardrails** are rules that constrain inputs, outputs, and actions, such as schema validation, allowlists, permissions, and human approval. They reduce risk but do not replace least privilege, isolation, and testing.

### Prompt Injection

**Prompt Injection** hides malicious instructions in a page, document, or tool result to steer an Agent away from its task. Treat external content as untrusted data and use least privilege plus human review for high-risk actions.

### Lethal Trifecta

The **Lethal Trifecta** describes an Agent that can read private data, encounter untrusted content, and communicate outward at the same time; Prompt Injection may then exfiltrate data. [Simon Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) framed the concept. Break at least one dangerous path.

## 7. Terms / buzzwords

### CLI Agent

A **CLI Agent** is an Agent / Harness that reads files, edits files, and runs commands from a terminal. Claude Code, Codex, OpenCode, Pi, Aider, and Gemini CLI fit this identity; the workbench is not the LLM inside it.

### BYO API Key (Bring Your Own)

**BYO API Key** means a tool lets you supply your own model-provider key. This can make provider switching easier, but billing, permissions, storage, and revocation remain your responsibility.

### Local LLM / On-Device

**Local LLM / On-Device** means the model runs on your device or self-managed machine. The full workflow stays local only when its model, tools, data, and records do not call a cloud service elsewhere.

### Quantization

**Quantization** represents model weights at lower precision and often reduces memory and compute needs. Changes in speed, size, and quality depend on the model, format, and hardware, so measure them.

### Hallucination

A **Hallucination** is content that sounds plausible but lacks reliable support. Citations, RAG, tools, and Structured Output can help, but important facts still need sources or Evals.

### Frontier Model

A **Frontier Model** is a model near the capability frontier at a particular time, not a permanent roster. Model names, prices, Context, and availability change quickly; use the [official-source table in Stage 1](../stages/01-llm-basics.en.md) for current facts.

### Context Engineering

**Context Engineering** decides what information enters each model call, in what order, and when it should be removed or compressed. It works with Prompt Engineering rather than replacing it; see [Anthropic's practical guide](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

### Agent Production Engineering

**Agent Production Engineering** is this roadmap's umbrella name for making an Agent dependable, safe, and observable over time. It brings Harnesses, Loops, Workflow Graphs, Evals, Guardrails, cost, recovery, and human approval into one chapter.

The learning order is [Stage 3 Agent Loop](../stages/03-tool-use-and-hello-agent.en.md) → [Stage 4 Workflow Graph / Agent Framework](../stages/04-agent-frameworks.en.md) → [Stage 7 Agent Production Engineering](../stages/07-multi-agent-production.en.md). Prompt, Context, Harness, Loop, and Graph are five overlapping control questions, not five product generations that replace one another.

📍 Full chapter: [Stage 7](../stages/07-multi-agent-production.en.md)

### Agent Harness

An **Agent Harness** is the execution system around a model. It connects tools and context and manages permissions, state, records, errors, and stop rules; the same Harness may contain an Agent Loop or sit inside a Workflow Graph node.

### Harness Engineering

**Harness Engineering** designs and improves an Agent Harness. OpenAI's [case study](https://openai.com/index/harness-engineering/) emphasizes environments, knowledge, tests, and feedback loops; Harness Engineering is not merely a wrapper around one framework and is not replaced by Loop Engineering.

### Loop Engineering

**Loop Engineering** designs how an Agent starts, acts repeatedly, checks work, saves progress, stops, or escalates to a person. IBM describes it as an emerging practice around goals, actions, observations, and adjustments; see the [current explanation](https://www.ibm.com/think/topics/loop-engineering).

An **Agent Loop** is the cycle that runs. **Loop Engineering** is the work of designing that cycle and its surrounding rules. It can use Harnesses, Hooks, Skills, Subagents, and Workflow Graphs instead of replacing them.

### Graph Engineering

**Graph Engineering** is an emerging label some authors use for Workflow Graph design, not a cross-vendor standard. The stable learning objects are nodes, edges, branches, state, and checkpoints; see the current [survey preprint](https://arxiv.org/abs/2608.21156) for one research use of the label.

Here, graph means an execution flow rather than the GraphRAG knowledge graph in Stage 6. Learn a basic Workflow Graph in [Stage 4](../stages/04-agent-frameworks.en.md), then add production boundaries in [Stage 7](../stages/07-multi-agent-production.en.md).

## 8. Agent Interfaces

### Computer Use

**Computer Use** lets a model read a screen and propose mouse or keyboard actions. A Harness checks rules before an executor acts; prefer a smaller, verifiable API or typed tool when one can do the job.

### Browser Use

**Browser Use** lets an Agent read data, find elements, fill forms, or move between pages. It may use the DOM, Accessibility Tree, and screenshots; [browser-use](https://github.com/browser-use/browser-use) is one open-source implementation.

### Sandbox

A **Sandbox** limits what running code can see and do. Its real boundary depends on file, network, process, secret, CPU / memory, and lifecycle controls; using a container alone does not prove safety.

To compare Search / Fetch, Browser Use, Computer Use, and Sandboxes, return to [Stage 8](../stages/08-agent-interfaces.en.md).

### microVM (micro Virtual Machine)

A **microVM** is a streamlined execution environment that still uses a virtual-machine isolation boundary. It is often used for untrusted code, but security still depends on images, networking, permissions, and host configuration.

### Firecracker

**Firecracker** is an open-source Virtual Machine Monitor that creates microVMs with KVM. It supplies isolation technology but does not automatically manage image updates, network policy, or tenant safety; see the [official repository](https://github.com/firecracker-microvm/firecracker).

### gVisor

**gVisor** places a userspace application kernel between an application and the host kernel, reducing direct exposure to host system calls. It is not a full virtual machine; use the [official documentation](https://gvisor.dev/docs/) for compatibility and performance tradeoffs.

## Cannot find a term?

- Return to the Stage you were reading; an important term should also have a plain-language definition at first use.
- See [Stage 5.2 on MCP](../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol--foundation), [Stage 5.3 on Skills](../stages/05-claude-code-ecosystem.en.md#53--skills-claude-codes-behavior-layer--the-most-critical-layer-of-the-claude-code-ecosystem), or [Stage 7 production boundaries](../stages/07-multi-agent-production.en.md).
- If it is still missing, open an issue and include where the term appeared and which sentence was unclear.

<details markdown="1">
<summary>Sources and verification</summary>

Changeable product and protocol statements above use official documentation; research terms link to original papers. Current model, price, and Context tables live in Stage 1 instead of being copied here.

<small>Official links, product identities, and model lifecycle checked: 2026-08-31 UTC.</small>

<!-- freshness: canonical=resources/glossary.md; verified_on=2026-08-31; scope=protocols,product-identities,terminology,official-links,model-lifecycle; max_age_days=90 -->

</details>

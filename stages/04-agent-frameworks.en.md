# Stage 4 — Agent Frameworks

> [繁體中文](./04-agent-frameworks.md) | [简体中文](./04-agent-frameworks.zh-Hans.md) | **English**

⏱ **Estimated time**: 2-3 weeks (approx. 10-15 hours)

> 💡 Unfamiliar with terms like `framework`, `supervisor`, `worker`, `handoff`? → Check [`resources/glossary.en.md`](../resources/glossary.en.md).

> 📋 **Chapter structure**: Learning Objectives → Entry Conditions → Required Reading → [Optional · Concept Map: multi-agent intro + advanced tool patterns] → Hands-on Exercises → Curated Projects → Self-Check
> 🔑 **Key Terms**: See [`resources/glossary.en.md`](../resources/glossary.en.md) (2 & 4 cover terms like `framework`, `agent loop`, `handoff`, `supervisor`).

You've built a ReAct agent from scratch (Stage 3). Now, let's see what a framework actually does for you. **Pick one to learn deeply**, and just skim the others to know when to switch.

## 📌 Learning Objectives

After completing this stage, you will be able to:

- Compare 5 major agent frameworks (LangGraph, AutoGen, CrewAI, Smolagents, OpenAI Agents SDK)
- Select the right framework for a given task
- Build the same agent using two different frameworks to experience the differences firsthand
- Recognize when to ditch the framework and write your own code

## 🚪 Entry Conditions

You should have already:

- Completed all 5 hello-X projects from Stage 3
- Written a ReAct agent from scratch (Exercise 3)
- Become comfortable with async Python (frameworks rely heavily on it)

## 📚 Required Reading

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — When to use a framework vs. when to use the raw API directly.
2. [**LangChain — Conceptual Guide: Agents**](https://python.langchain.com/docs/concepts/agents/) — The abstract concepts of agents.
3. [**Best Multi-Agent Frameworks 2026 comparison**](https://gurusup.com/blog/best-multi-agent-frameworks-2026) — Current market positioning.
4. **A Quickstart from one framework** — Choose either LangGraph or CrewAI and go through the official tutorial from start to finish.

## 🤔 What is a multi-agent framework?

### Two Dimensions to Clarify First (Workflow vs. Agent / Single vs. Multi)

To understand multi-agent frameworks, a useful clarification is to treat **workflow vs. agent** and **single vs. multi LLM** as two orthogonal dimensions. The core distinction in Anthropic's "Building Effective Agents" is between a workflow (fixed code path) and an agent (LLM autonomously decides the next step). Let's stack this with single/multi to see the four quadrants:

| | **Workflow**<br>(Your pre-written code path) | **Agent**<br>(LLM dynamically decides the next step) |
| -------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Single LLM** | Linear pipeline, no branching logic | One LLM + ReAct loop, plans and adapts on its own<br>(**This is what you built in Stage 3**) |
| **Multi LLM** | Pre-defined routing (e.g., "sales questions → agent A, tech questions → agent B") | 2+ agents handing off to each other, with an orchestrator dynamically assigning tasks<br>(**The topic of this stage**) |

**Why this distinction is useful**: Most production scenarios sit in the **Single LLM** row, whether in the Workflow column (a linear pipeline) or the Agent column (a ReAct loop). Most tasks simply don't require multi-agent setups. **The quadrant that truly needs a multi-agent framework is the bottom right**—high LLM autonomy + multi-role collaboration. In practice, the boundaries between these quadrants can be blurry (LangGraph's conditional edges can be seen as both workflow routing and dynamic agent decision-making). Don't treat this matrix as a mutually exclusive classification.

→ All later discussion in this stage assumes you already know: **a multi-agent framework mainly handles the coordination, handoff, state management, and repetitive scaffolding code between multiple agents, so you don't have to write the whole collaboration flow from scratch** (the orchestration boilerplate in the lower-right quadrant).

### Single-agent vs. multi-agent — A comparison table to clarify the differences

| Dimension | **Single-agent** (You built this in Stage 3) | **Multi-agent system** |
| ------------------ | --------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Architecture** | One LLM + ReAct loop + several tools | 2+ LLMs, each with a role (researcher / writer / critic...), coordinated by an orchestrator |
| **Decision Making**| The same LLM thinks from start to finish | Role-based decomposition + handoff, different LLM instances see different perspectives |
| **State Management**| Linear message history | Shared state / message passing / checkpoints |
| **Suitable For** | Linear logic, < 20-30 tools, single objective | Decomposable tasks, need for perspective diversity, long workflows, parallelization |
| **Debug Cost** | Low (a single loop is easy to trace) | High (cross-agent interaction, error propagation is hard to pinpoint) |
| **Token Cost** | 1x | Typically **3-10x** (each sub-agent has its own prompt + thinking + tool calls) |
| **Latency** | Low | High (unless sub-agents run in parallel) |

### When do you **really** need multi-agent? (Don't force it)

**Multi-agent is not the default; it's a last resort.** **Both Anthropic and Cognition, two frontier labs, explicitly stated in 2024-2025 that 90% of use cases should not use multi-agent setups.** Forcing it results in **3-10× token costs, painful debugging, and severe context fragmentation.**

| Stance | Source | Core Argument |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Anthropic** | [Building Effective Agents (2024)](https://www.anthropic.com/engineering/building-effective-agents), [How we built our multi-agent research system (2025)](https://www.anthropic.com/engineering/built-multi-agent-research-system) | Most scenarios are fine with a simple workflow + single agent; multi-agent is only truly helpful for "**research-style / parallel exploration**" tasks. |
| **Cognition** | [Don't Build Multi-Agents (2025)](https://cognition.ai/blog/dont-build-multi-agents) | Multi-agent setups suffer from severe context fragmentation and painful shared state maintenance; exhaust single-agent + long-context options first. |

You typically need multi-agent when one of these four signals appears:

| Signal | Description | Corresponding Pattern |
| ----------------------- | ----------------------------------------------------------------------- | --------------------------------------- |
| **1. Natural Task Decomposition** | A large task has clear sub-steps that can be completed step-by-step. | Sequential / Planner-Executor |
| **2. Token Explosion** | A single agent's prompt can't fit all tool descriptions/context. | Supervisor-Worker (offloads to sub-agents) |
| **3. Role Conflict** | Having the same LLM act as both writer and critic leads to self-justification. | Debate / Peer review |
| **4. Parallel Acceleration**| Running 3 research sub-tasks concurrently reduces wall-clock time to 1/3. | Parallel / Map-Reduce variant |

**None of these four signals present?** → A single agent + a good prompt + tool use is enough, without paying the three costs listed above, and multi-agent is not guaranteed to be more accurate either.

> 💡 **Further Reading**: [Stage 7 But do you really need multi-agent?](07-multi-agent-production.en.md#-but-do-you-really-need-multi-agent) will revisit this decision from a production perspective. This section covers the design-phase decision; that one is the final check before deployment.

### Classic Multi-agent Patterns (ordered by complexity)

> 📝 **How this differs from Stage 3 Classic Paradigms**: [The 4 paradigms in Stage 3](03-tool-use-and-hello-agent.en.md#classic-agent-paradigms-thinking-patterns) (CoT / ReAct / Reflection / Planning) describe **how a single agent thinks internally**. The 5 patterns in this section describe **how multiple agents collaborate**—two orthogonal layers.

| Pattern | Complexity | What it looks like | Classic Scenarios | Representative Framework / Paper |
| ---------------------------- | ---------- | ---------------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **1. Routing / Handoff** | ⭐ | 1:1 handoff between agents, no central orchestrator | Customer support routing, context switching | [OpenAI Swarm](https://github.com/openai/swarm), [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) |
| **2. Sequential**<br>(Planner → Executor) | ⭐⭐ | Planner creates multi-step plan + executor carries it out | Multi-step automation, code generation | LangGraph, [ChatDev paper](https://arxiv.org/abs/2307.07924) |
| **3. Parallel**<br>(Parallel Acceleration) | ⭐⭐⭐ | N agents run concurrently, results are aggregated | Research / map-reduce tasks, 1/N wall-clock time | LangGraph parallel branches, CrewAI parallel tasks. **Pitfalls**: async coordination, partial failure, state merge consistency. |
| **4. Supervisor-Worker**<br>(hub-spoke) | ⭐⭐⭐ | 1 supervisor + N workers, supervisor assigns + integrates | Task decomposition, report integration | LangGraph, AutoGen GroupChat |
| **5. Debate / Society**<br>(Multi-perspective convergence) | ⭐⭐⭐⭐ | 2+ agents critique each other or role-play | Research, judgment tasks, social simulation | AutoGen GroupChat, [CAMEL paper](https://arxiv.org/abs/2303.17760), [Generative Agents paper](https://arxiv.org/abs/2304.03442) |

### Claude Code subagent — An alternative orchestration path

> **This section is on a different level than the 5 patterns above**: The 5 patterns are design choices that can be implemented with or without a framework. The **Claude Code subagent** introduced here is another execution model (built-in runtime orchestration, no framework code). After reading about the 5 patterns, this section shows you "there's a second path for multi-agent."

Anthropic's own Claude Code offers another layer of abstraction: the [subagent](05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature). You create a subagent by writing a `.claude/agents/<name>.md` file—**no framework required**.

The fundamental difference from the framework path (in one line): the **framework path** is cross-LLM-provider, written as Python orchestration code, with full checkpointing / audit trail; **Claude Code subagent** runs only inside the Claude Code runtime, written as markdown not code, with built-in context isolation.

> 📌 **The full dimension-by-dimension comparison table (startup / runtime / context isolation / provider lock-in / learning curve) lives canonically at [Stage 5.5](05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature)** — see 5.5 for the per-item implementation differences.

**When to choose subagents over a framework**:

- You're already using Claude Code for your daily work.
- The task context is large and would consume the entire main session window (e.g., reading a whole codebase).
- You want to run multiple subagents in parallel (research / write / critic) to save wall-clock time.
- You don't need cross-provider migration.

For detailed implementation and hands-on exercises, see [Stage 5.5](05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature) (**it's recommended to complete Stage 5.1 on Claude Code basics before tackling 5.5**—subagents are an advanced feature of the ecosystem and require familiarity with the basics).

### What Frameworks Do

Frameworks abstract away the orchestration boilerplate for the 5 patterns above (roles, handoffs, state, retries, checkpoints, HITL pauses), letting you focus on writing role definitions and task descriptions. In short: **a framework is scaffolding for multi-agent systems, not a necessity**. For simple scenarios, you could write your own solution with a dictionary and a for loop (which is exactly what you'll do in Stage 7, Exercise 1).

### 📚 Want a more systematic, in-depth look?

**🇺🇸 Academic Papers (Influenced all subsequent framework designs)**:

1. [**Anthropic — "Building Effective Agents"**](https://www.anthropic.com/engineering/building-effective-agents) ⭐⭐⭐ — When to use a workflow vs. an agent, 5 classic orchestration patterns. **Essential reading for multi-agent design in the English-speaking world.**
2. [**AutoGen paper (Wu et al. 2023)**](https://arxiv.org/abs/2308.08155) — The original paper for Microsoft's multi-agent conversation framework.
3. [**CAMEL paper (Li et al. 2023)**](https://arxiv.org/abs/2303.17760) — The seminal work on multi-agent role-playing.
4. [**ChatDev paper (Qian et al. 2023)**](https://arxiv.org/abs/2307.07924) — Canonical example of planner-executor for multi-agent software development.
5. [**Generative Agents paper (Park et al. 2023)**](https://arxiv.org/abs/2304.03442) — 25 agents interacting in a Sims-like environment, a classic in social simulation.

**🀄 Chinese Systematic Resources**:

1. [**hello-agents Ch6 "Framework Development Practice" + Ch7 "Build Your Agent Framework"**](https://github.com/datawhalechina/hello-agents) ⭐ — A comprehensive Chinese resource on framework development and building one from scratch. **Note: Ch4 "Classic Agent Paradigm Construction" covers single-agent paradigms (ReAct / Plan-and-Solve / Reflection), not multi-agent.**
2. [**Hung-yi Lee — Introduction to Generative AI**](https://speech.ee.ntu.edu.tw/~hylee/genai/2024-spring.php) — Later episodes cover AI agents / multi-agent systems.

**Framework Official Multi-Agent Docs**:

- [**LangGraph — Multi-Agent Systems**](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) — Official tutorials for supervisor, swarm, and hierarchical architectures.
- [**Anthropic Cookbook — `customer_service_agent.ipynb`**](https://github.com/anthropics/claude-cookbooks/tree/main/tool_use) — A canonical example of multi-agent orchestration (routing + handoff).
- [**Microsoft AutoGen — Examples**](https://microsoft.github.io/autogen/) — Complete examples for group-chat, debate, and peer review patterns.

> 💡 **Recommended Learning Path for Frameworks** (5 steps):
> 1. **Build a mental model** (30 min) — Read Anthropic's Building Effective Agents and get the workflow vs. agent and single vs. multi dimensions straight.
> 2. **Run a framework quickstart** (2-3 hr) — Pick either LangGraph or CrewAI and run their official multi-agent tutorial.
> 3. **Cross-reference with Anthropic's Cookbook `customer_service_agent`** (1 hr) — A production-style routing + handoff example.
> 4. *(Optional)* **Dive into the academic side**: Pick 1-2 papers to read (AutoGen / CAMEL / ChatDev / Generative Agents).
> 5. *(Optional for Claude users)* **Write a subagent for comparison**: See [Stage 5.5](05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature) and compare it to the framework approach.
>
> **You don't need to read all 5 papers.** Pick the 1-2 that are most relevant to your use case.

## 🛠 Advanced Tool Patterns (What frameworks handle for you) ⭐ Must-read for Track B

Stage 3 taught you to write single-tool / multi-tool selection (by hand-writing `if/elif/else` routing). Frameworks abstract this layer away and add three more advanced tool patterns. **These three patterns need a framework's abstraction layer to be written cleanly; trying to hand-write them like in Stage 3 would be a mess:**

| Pattern | What problem it solves | Representative Implementation |
| ----------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Dynamic tool selection**| When you have >30 tools, `tools=[...]` is too large for the prompt (context window issues, poor selection). | [LlamaIndex tool router](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/) — Embedding-based routing: first, a semantic search finds the top-K tools, and only those K are put into the prompt. |
| **Tool composition / chaining** | Chaining tool A's output to tool B's input without LLM narrative in between (saves tokens + latency). | LangGraph `state graph` directly connecting nodes, CrewAI `sequential tasks`, Pydantic AI's type-safe pipeline. |
| **Tool-augmented retrieval**| The tool itself is a RAG search → returns results → the agent reasons on the results. | A combination of the Stage 6 Exercise 4 RAG pipeline and Stage 3 Exercise 2 multi-tool selection (LangGraph wraps the retriever as a tool node). |

**📚 In-depth Resources**:

- [**Anthropic — Tool Use best practices**](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) — The official tool design guide.
- [**LlamaIndex — Tool Router pattern**](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/) — The canonical reference for dynamic selection.
- [**LangGraph — Tool Node**](https://langchain-ai.github.io/langgraph/) — How to write a composition graph.

> 💡 **For Track B after this section**: You should be able to explain the differences between implementing the "same task" via (a) hand-writing it in Stage 3, (b) using a framework in this stage, and (c) using a Claude subagent in Stage 5.5. This is a core question for Track B's "knows how to design agents" path.

## 🛠 Hands-on Exercises

### Exercise 1: Same agent, two frameworks
Build the same simple agent (search + summarize) using these two frameworks:

- LangGraph
- CrewAI
Compare the lines of code, the debugging experience, and where each framework hides its complexity.

### Exercise 2: Multi-agent role assignment
Use CrewAI to build a demo with 2-3 agents, each with a different role, collaborating on a single task. (This is CrewAI's strong suit.)

### Exercise 3: Graph-based workflow
Use LangGraph to build a workflow with branching logic and a human-in-the-loop checkpoint. (This is LangGraph's strong suit.)

### Exercise 4: CodeAct vs. JSON tool
Use Smolagents to build an agent that writes Python code as its action (the CodeAct pattern). Compare this with the JSON tool-calling approach from Exercise 1. Ask the same question and see how each approach solves it.

### Exercise 5: Type-safe agent
Use Pydantic AI to build an agent that returns structured output (e.g., for a given question, it returns `{ "answer": str, "confidence": float, "sources": [str] }`). See how Pydantic's schema validation prevents the agent from being lazy or hallucinating the structure.

## 🎯 Curated Projects

17 projects across 5 categories, all in one table. **Start by looking at "Who it's for", then if you want to dive deeper, check out the repo / quickstart link.**

| Category | Project | ⭐ | Who it's for | Why it's recommended / Notes |
| ------------------------------------------ | ---------------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Production-tier**<br>(Complex multi-agent / needs audit) | [LangGraph](https://github.com/langchain-ai/langgraph) ⭐ **This stage's #1 recommendation** | ⭐⭐⭐⭐⭐ | Production multi-agent systems that require audit trails / rollback / replay. | Graph-based orchestration + checkpointing + time-travel debugging. Widely adopted across enterprises. ★ 39k+, MIT, Python+TS. Pairs with LangSmith for observability. |
| | [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) | ⭐⭐⭐⭐ | Building agents in .NET / Java environments, within the Microsoft tech stack. | Official SDKs in C#, Python, and Java. Follows a kernel + plugin + planner pattern. ★ 28k+, MIT. Thick abstraction, not for beginners. |
| | [agno-agi/agno](https://github.com/agno-agi/agno) | ⭐⭐⭐⭐ | Those who want a "build + serve + monitor" solution without the full LangGraph + LangSmith suite. | Multi-modal agent runtime + control plane. ★ 41k+, Apache-2.0. Learn the API in Stage 4, use the runtime in Stage 7. |
| | [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | ⭐⭐⭐⭐ | Teams wanting Microsoft's unified successor to AutoGen + Semantic Kernel, in Python or .NET. | Microsoft's open framework for getting multiple agents to work together — the successor that merges AutoGen and Semantic Kernel. ★ 12k+, MIT, Python + .NET. |
| **Rapid Prototyping / Multi-agent**<br>(Role-based / handoff) | [CrewAI](https://github.com/crewAIInc/crewAI) ⭐ **This stage's #2 recommendation** | ⭐⭐⭐⭐ | Rapidly prototyping "researcher → writer → critic" pipelines. | Build a crew in ~20 lines of code. Lowest learning curve. ★ 55k+, MIT. ⚠️ No checkpointing for long workflows; use CrewAI for prototypes, LangGraph for production. |
| | [Microsoft AutoGen / AG2](https://github.com/microsoft/autogen) | ⭐⭐⭐⭐ | Multi-agent debate / brainstorming / peer review patterns. | Conversational multi-agent, strong group-chat capabilities. ★ 60k+, CC-BY-4.0 (for docs). ⚠️ AG2 v0.4 was a major async-first rewrite; older tutorials still target v0.2 while newer ones use v0.4, mind the version. |
| | [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | ⭐⭐⭐⭐⭐ | Teams already committed to the OpenAI ecosystem. | OpenAI's official library. Clean API for agent hand-off + structured output. MIT. **Built-in since April 2026**: a sandbox (7 providers) + harness abstraction layer. The first architecturally sound approach for production coding agents ([details in Stage 8](08-agent-interfaces.en.md#why-the-april-2026-openai-agents-sdk-update-is-a-milestone)). |
| | [deepagents (LangChain)](https://github.com/langchain-ai/deepagents) | ⭐⭐⭐⭐ | Want a "batteries-included" deep-agent harness without wiring it yourself. | An opinionated harness (it makes the design choices for you) on top of LangGraph: built-in planning (todo list), filesystem memory, subagents, loadable skills, context offload (keeps big intermediate results out of the LLM's window). `pip install deepagents`, MIT, v0.6.12 (2026-06). |
| | [OpenAI Swarm](https://github.com/openai/swarm) | ⭐⭐⭐⭐ Edu<br>⭐⭐⭐ Prod | To understand the **core mental model** of multi-agent systems without learning a full framework. | ~200 LOC, just two concepts: Agent + handoff. MIT. ⚠️ OpenAI labels it experimental/educational, not a production tool. **Read the source code as a chapter-length tutorial.** |
| | [Strands Agents (AWS)](https://github.com/strands-agents/sdk-python) | ⭐⭐⭐⭐ | Teams already committed to the AWS cloud and Bedrock-native solutions. | Model-driven design (LLM plans on its own, no explicit graph). Apache 2.0. Released late 2025, integrates with AWS Lambda / Step Functions / Bedrock Agents. |
| **Specialized Paths**<br>(CodeAct / typed / memory-first / filesystem-first) | [Hugging Face Smolagents](https://github.com/huggingface/smolagents) | ⭐⭐⭐⭐ | Local LLM ecosystems, HF integration scenarios. | A prime example of the CodeAct pattern (agent writes Python code as its action, not JSON tool calls). ★ 28k+, Apache 2.0, ≤1000 LOC. |
| | [Pydantic AI](https://github.com/pydantic/pydantic-ai) | ⭐⭐⭐ | Production systems that require runtime type safety + structured output by default. | Type-safe agents from the Pydantic team. MIT. Relatively new. |
| | [Letta (formerly MemGPT)](https://github.com/letta-ai/letta) | ⭐⭐⭐⭐ | **Long-session / cross-day / persona-stable** agents (long-term assistants, therapists, tutors). | A memory-first multi-agent system based on OS-paging concepts (working memory + archival store). ★ 24k+, Apache 2.0. Also mentioned in Stage 6, Exercise 5. |
| | [vercel/eve](https://github.com/vercel/eve) | ⭐⭐⭐ | Building long-running, operable agents in the TS/JS ecosystem; you like a "files as the interface" project layout. | Vercel's filesystem-first framework: an agent's parts are conventional files — `instructions.md` (system prompt), `tools/`, `skills/`, `channels/` (HTTP / Slack / Discord), `schedules/` (cron) — easy to inspect and extend. Start with `npx eve@latest init`. Apache-2.0, TypeScript, ★ 4.5k+. ⚠️ Released 2026-06, very new. |
| **Specialized** | [LlamaIndex Agents](https://github.com/run-llama/llama_index) | ⭐⭐⭐ | Document-heavy agents (research assistants, knowledge workers, etc.). | Tightly integrated with RAG. ★ 51k+, MIT. Strong on retrieval, weak on orchestration—don't choose it for pure orchestration. |
| | [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | ⭐⭐⭐ | Researchers who want to visually debug multi-agent workflows. | A multi-agent platform with strong visual debugging tools. ★ 28k+, Apache 2.0. Low adoption in Western communities, but solid tech. |
| | [LangChain](https://github.com/langchain-ai/langchain) | ⭐⭐⭐ | Rapid prototypes that need to glue together many components (retrieval + chains). | The swiss-army-knife framework. ★ 143k+, MIT. **For agent orchestration, use LangGraph now.** LangChain is better for gluing retrieval + chaining. |
| **Infrastructure**<br>(Not a framework, used across stages) | [BerriAI/litellm](https://github.com/BerriAI/litellm) | ⭐⭐⭐⭐ | When you need to switch between Claude / GPT / Gemini / open-source models without changing code. | A provider-agnostic SDK + AI gateway. Call 100+ LLMs using OpenAI's format. Includes cost tracking / fallbacks / guardrails. ★ 54k+, MIT (`enterprise/` subdirectory licensed separately). |

> 💡 **Recommended reading path**: Pick **1 for production deployment** (LangGraph) + **1 for rapid prototyping** (CrewAI) framework to learn deeply → Do exercises 1-3 → Skim the READMEs of the others to know they exist. The **4 specialized paths** (CodeAct / typed / memory-first / filesystem-first) are only rivals in specific scenarios; you don't need to touch them otherwise.

## ✅ Self-Check Before Moving to Stage 5

Can you:

- [ ] Build the same agent using both LangGraph and CrewAI?
- [ ] Choose the right framework for a task (production vs. prototype)?
- [ ] Explain the difference between LangGraph's checkpointing and CrewAI's task delegation?
- [ ] See when CodeAct (Smolagents) is better than JSON-tool?
- [ ] Judge when to ditch a framework and use the raw API directly?

If yes → Proceed to [Stage 5 — The Claude Code Ecosystem](05-claude-code-ecosystem.en.md).

## 💡 Strategic Tips + Potential Pitfalls

The reading path is in the **Selected Projects** callout above (go deep on LangGraph + CrewAI, skim the rest); it is not repeated here.

**A heads-up on Memory** (you might encounter this while learning, no need to read ahead): Some framework features use memory concepts—LangGraph's checkpointing (state persistence), CrewAI agents passing task results to each other (lightweight memory). These are covered in full in [Stage 6 — Memory & RAG](06-memory-rag.en.md). If you get stuck on a framework feature in this stage, check that section, but **you don't need to read it all before continuing this stage**.

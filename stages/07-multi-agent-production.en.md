# Stage 7 — Multi-Agent · Productionization

> [繁體中文](./07-multi-agent-production.md) | [简体中文](./07-multi-agent-production.zh-Hans.md) | **English**

⏱ **Estimated Time**: 2-4 weeks (approx. 15-30 hours)

> 💡 High density of terminology (multi-agent / handoff / eval / observability / guardrails...) → Refer to [`resources/glossary.en.md` 4 + 6](../resources/glossary.en.md#4-multi-agent).

> 📋 **Chapter Composition**: [What is Multi-Agent · Productionization (Positioning) + Five-layer engineering split + When to use multi-agent] → Learning Objectives → Entry Conditions → Required Reading → Harness Engineering (**8 core components including Cost/Latency**) → Hands-on Exercises (including Exercise 6 Cost Optimization) → **Agent Benchmark Landscape: how to read it, not just the leaderboard** → Recommended Tools → Featured Projects → Self-Check
> 🔑 **Key Terms**: See [`resources/glossary.en.md` 4 + 6](../resources/glossary.en.md#4-multi-agent) (multi-agent / orchestration / handoff / eval / observability / harness (the execution and control layer around the model))

This is the final stage. You are moving from "I can build an agent" to "I can make an agent **truly stable for people to use**"—with multiple agents collaborating, with eval, with observability, and deployable to a usable environment. How the scope is drawn is in the three lines below.

## 🎯 What Is Multi-Agent · Productionization (Positioning)

**This stage = how multiple agents collaborate + how to push an agent from prototype to the point where others can use it stably.** Three sentences clarify the scope:

- **It is not just about learning frameworks** — Stage 4 already taught how to choose frameworks
- **It does not have to be enterprise scale** — as long as an agent can be used by others, it counts as productionization
- **The core is harness engineering** — 8 core components + eval + observability + cost / latency control

**Division of labor with adjacent stages**:

- **Stage 4** = how to choose a single-agent framework, patterns like ReAct / Plan-Execute
- **This stage** = **multi-agent collaboration** + **harness engineering** (execution-system engineering) + **deployment to a usable environment / observability / eval**

### The five-layer engineering split: Prompt → Context → Harness → Loop → Graph

> 📍 **This section is the canonical source for this repo's "layering" model**. Other chapters that mention layers should point back here instead of restating the model each time. Previously, six places explained it separately and drifted into three different versions.

These five layers are **not a difficulty ladder**. They describe **how much scope you are managing**. They are also not a flat list: **each next layer appears because the previous layer hits a wall** (unrelated to "one call vs. many calls"):

| Layer | Concept | Purpose (what it solves) | Wall it hits → why the next layer exists | Where it is taught | Name source |
|---|---|---|---|---|---|
| 1 | **Prompt Engineering** | Ask the right thing this time | It does not know the data you have | [Stage 2](02-prompt-engineering.en.md) | Officially used |
| 2 | **Context Engineering** | Let it read the right information | It knows, but still cannot act | [Stage 6](06-memory-rag.en.md) | Officially used |
| **3** | **Harness Engineering**<br>(**This stage**) | Let it actually act without blowing up on errors | One run cannot finish a large job | **This stage** | Officially used |
| 4 | **Loop Engineering**<br>(long-horizon) | Let it finish by itself without you watching | It runs by itself, so you cannot see what it is doing | [Stage 5.6](05-claude-code-ecosystem.en.md) | ⚠️ Unofficial name |
| 5 | **Graph Engineering** | Make the process visible, controllable, and resumable | — (currently the outermost layer) | [Stage 4](04-agent-frameworks.en.md) | ⚠️ Unofficial name |

![Agent engineering five-layer stack](../resources/diagrams/agent-engineering-5layer.en.png)

> ⚠️ **"Where it is taught" is not a reading order**. Layers 4 and 5 happen to be covered in earlier chapters (5.6 and 4), so that column appears to run backwards as you read down. **Just read Stage 0 → 8 in order**; this column only tells you where to go when you want the detail.
>
> ⚠️ **Layer 4's "Loop" means long-horizon**: hundreds of steps, picking up again in a new session, deciding when to stop. It shares a name with the `Agent loop` in the harness component table further down (the mechanical cycle inside a single run) but sits at a different level; that table says so again when you reach it.
>
> ⚠️ **Pay attention to the "Name source" column**. The first three terms are used by vendor documentation (Anthropic has context engineering material, and OpenAI used harness engineering in 2026-02). **The last two are not**: Loop / Graph Engineering are community names. The concepts are real, but Anthropic calls similar mechanisms *dynamic workflows*, while Google ADK and Microsoft Agent Framework use *graph-based workflow(s)*. If you cannot find "graph engineering" in official docs, you are not missing it.

**Plain-language difference**:

- **Prompt** = design a good way of asking so the model answers correctly this time
- **Context** = dynamically decide which background, memory, documents, and tool results to include so the model understands the current situation
- **Harness** = connect prompt, context, tools, state, flow control, and error handling into a system that can actually run
- **Loop** = give it a goal, let it repeat until the result is good enough, decide when it should stop, and let a fresh session pick up where the last one left off (**not** the single-run mechanical loop inside the harness)
- **Graph** = split the work into boxes first, draw which box connects to which, and make the process visible and resumable

### Loop vs. graph: what is the difference?

**Loop** = you give it a goal, and it keeps working until it decides the result is good enough. You do not see much in the middle; you mostly see the result. Like washing dishes: pick one up, wash it, check whether it is clean, wash again if needed. **There is one path; the agent decides how many times to go around.**

**Graph** = you first split the work into **boxes** and draw lines for who follows whom. Like a restaurant kitchen: chop, cook, plate. The order is written down, and two burners can run at the same time.

The easiest sentence to remember:

> **Inside a box, the agent loops; between boxes, you define the order.**

![What is actually inside a "graph"](../resources/diagrams/inside-a-graph.en.png)

So this is not either-or. **A graph puts several loops into boxes, then orders those boxes.** And a box does not have to contain an agent: **it can also be a tool, a check, or a "human must approve before continuing" gate**.

**Why add this layer**: once the boxes are drawn, you can see which box is stuck, resume from the middle, and run two boxes in parallel. Conversely, **if you put everything back into one box, you are back to a plain loop**.

**The cost matters**: a graph forces you to decide up front which boxes exist. If the job is simply "keep trying until it works" and nobody needs to inspect the path afterward, drawing a graph is extra work. In that case, a loop is the right tool. **The more you trust the agent, the fewer boxes you draw.**

**Lineage**: ReAct (2022) → AutoGPT (2023) → Claude Code's `/goal` (2026, give a verifiable completion condition and let the agent loop until it is met). [Stage 5.6 Dynamic Workflows](05-claude-code-ecosystem.en.md) is the agent writing its own loop script; the runnable graph example is in [`examples/stage-4/03-graph-workflow/`](../examples/stage-4/03-graph-workflow/README.en.md).

**This stage's 3 core questions**:

1. **Multi-agent collaboration** — debate / planner-executor / peer review / handoff / supervisor-worker patterns
2. **Harness Engineering** — agent loop / tool registry (the list of tools an agent can call + interface definitions) / context manager / safety / retry / telemetry / eval / cost (8 core components, detailed below)
3. **Productionization** — eval harness / observability / cost & latency optimization / deployment to a usable environment

**Division of labor with Stage 5** (to avoid confusion):

| Comparison | What's Covered There | What's Covered in This Stage |
|---|---|---|
| **Stage 5.5 Subagents** | Claude Code's native subagent mechanism (markdown-based, no coding) | General multi-agent frameworks (autogen / crewAI / langgraph, vendor-agnostic) |
| **Stage 5.7 Claude Code source** | Claude Code source dissection (reference implementation case study) | General harness engineering principles (not tied to a specific vendor) |

### ⚠ But do you really need multi-agent?

**Multi-agent is not the default; it is a design you use only when the task truly needs it.** In most scenarios, you should first try a simple workflow or a single agent; **only when the task is naturally decomposable, needs parallel exploration, a single context is not enough, or explicit role separation is needed, is multi-agent worth introducing**. Forcing it increases **token, latency, debugging, and context-fragmentation costs**; measure the multiplier on your own task. Anthropic's Research system used about `15×` the tokens of ordinary chat, but that is a result from one specific system, not a universal rule.

> 📌 **The decision framework's canonical home is Stage 4**: the full Anthropic / Cognition stance comparison + the 4 "should you go multi-agent" signals + each signal's corresponding pattern live in [Stage 4 §When do you really need multi-agent](04-agent-frameworks.en.md#when-do-you-really-need-multi-agent-dont-force-it) (design-phase decision). This section is only the last sanity check before production — **none of the 4 signals present?** → a single agent + good prompts + tool use is enough; don't force multi-agent. **The harness engineering part of this stage (8 components / eval / observability) still applies even if you end up using a single agent**—so this stage is still required reading even if you decide against multi-agent.

## 📌 Learning Objectives

- Design multi-agent orchestration patterns (debate, planner-executor, peer review)
- Build an evaluation harness for your agent
- Add observability (tracing, logging, cost tracking)
- Use the Anthropic SDK / OpenAI SDK for production deployment (advanced features: streaming, prompt caching, batching)
- Deploy an agent to production (Docker, serverless, monitoring)

## 🚪 Entry Conditions

You should already have:

- Completed Stage 4 (used at least one agent framework to run a multi-agent demo)
- Completed Stage 5 (understand the roles of MCP / Skills / Plugins / Subagents, and have dissected a harness internally in 5.7)
- Completed Stage 6 (know basic RAG, can explain the differences between memory patterns)
- Basic familiarity with Docker / git / CI (will be used in production deployment)

If not, go back and complete the previous stages. This stage is about "combining everything you've learned → running in production," and any missing piece will be a blocker.

## 📚 Required Reading

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — Reread it from a production perspective
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — A technique for 90% cost reduction
3. [**Anthropic — Message Batches API**](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) — Asynchronous batch jobs
4. [**anthropics/courses — Prompt Evaluations**](https://github.com/anthropics/courses) ⭐⭐⭐⭐⭐ ★ 22k+ — Anthropic's official 5-course umbrella; **module 4 "Prompt Evaluations" maps to this stage's eval / observability section**. Jupyter notebooks covering systematic evaluation of prompt and agent behavior.
5. **Documentation for any eval framework** — promptfoo, LangSmith, or weave
6. [**ai-boost/awesome-harness-engineering**](https://github.com/ai-boost/awesome-harness-engineering) (★ 3.4k+) — A collection of tools / patterns / eval / memory / MCP / observability for agent harnesses
7. [**ZhangHanDong/harness-engineering-from-cc-to-ai-coding**](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding) (★ 1.5k+) — Learning harness design from Claude Code's source code (in Chinese)
8. [**stablyai/orca**](https://github.com/stablyai/orca) (★ 48k+, MIT) — the largest "**many agents at once**" desktop environment right now: fan a single prompt across several agents, each in its own git worktree, then compare the results side by side and merge the winner. It treats Codex / Claude Code / OpenCode / Pi as swappable backends, so the thing worth studying is not which ones it supports but **what problems the interface has to solve once five agents are editing the same repo**: isolation, comparison, review, and how you get told an agent has finished. Ships an iOS app for watching progress from a phone.
9. [**yc-software/qm**](https://github.com/yc-software/qm) (★ 13k+, MIT) — **quartermaster**, open-sourced by Y Combinator, running in Slack and on the web. The split against orca is instructive: orca handles "one person running many agents", qm handles "**a whole company sharing an agent**". Each employee gets an isolated workspace (its own memory, files, keychain view, permissions, crons, sandbox) while still collaborating in channels and projects; the harness and model are pluggable (Pi / OpenCode / Codex / Claude Code drive the same core), so a deployment is not tied to one vendor. If you want to see what **org-level agent permissions and governance** actually look like, this is one of the few implementations you can just read.
10. [**cft0808/edict**](https://github.com/cft0808/edict) (★ 16k+, MIT) — a Chinese-language project that designs multi-agent division of labour after the Three Departments and Six Ministries, a 1,300-year-old imperial civil service structure: triage, then planning, then review, then dispatch, then parallel execution across ministries, then a report back. It is here not for the historical conceit but because it writes down **who may decide, who reviews, and who only executes** as explicit roles and handoffs, which maps directly onto this stage's planner-executor and peer-review patterns. Ships a live board showing what each agent is doing. Part of the OpenClaw ecosystem; a one-line docker demo is provided.
11. **(Optional — this one is still a developer preview)** [**deepseek-ai/deepseek-harness**](https://github.com/deepseek-ai/deepseek-harness) (★ 188k+, MIT) — DeepSeek's agent harness, open-sourced 2026-08-13. Its thesis is "**everything is a plugin**": models, tools, skills, sessions, sandboxes, storage, the loop, scheduling and the UI are all supplied by plugins. **Read it, don't depend on it** — the README itself says it is "currently in *developer preview* and is iterating rapidly. **THERE WILL BE COMPATIBILITY-BREAKING CHANGES.**", the version is `0.1.0-rc.5`, and there are no GitHub releases yet. It earns a place here because it is one of the few complete implementations you can open up and see **what parts a harness is actually made of** — which maps directly onto the eight core components below. If you do read it, start from [`docs/architecture.md`](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md) rather than diving into the monorepo. It is not locked to DeepSeek models: the [model configuration guide](https://deepseek-harness.github.io/deepseek-harness/guide/providers) covers Anthropic, OpenAI, Bedrock, Vertex, Azure and custom OpenAI-compatible endpoints. It is absent from [`resources/cli-agents-guide.md`](../resources/cli-agents-guide.en.md) because **the interactive interface is a Web UI** (`npx @deepseek-ai/dsh web`); the shipped non-web mode, `dsh --profile headless "job"`, runs once and exits rather than being an interactive terminal agent (the plugin repo that `--profile tui` points at currently 404s).

## 🏗 Harness Engineering — Engineering Design for a Production Agent Runtime ⭐ Core Concept of This Stage

### Positioning: The execution and control layer around the model

To turn an LLM into a usable agent, the first thing you meet is **the first three of the five layers** (the full ladder is in "The five-layer engineering split" above). These three layers correspond to different engineering positions, not simply "one call" versus "many calls."

> 💡 **Simon Willison 2025**: "coding agent = LLM + harness"; harness = all the code **that is not the model itself**.
>
> 💡 **OpenAI also uses the term "Harness Engineering" in 2026** (see the [OpenAI Harness Engineering article](https://openai.com/index/harness-engineering), published 2026-02).

| Layer | What you are engineering | Where to learn it |
|---|---|---|
| **1. Prompt Engineering** | The **string** sent into the LLM (system prompt / few-shot / format) | [Stage 2](02-prompt-engineering.en.md) |
| **2. Context Engineering** | The **information** placed inside the window (RAG / memory / tool defs / history assembly) | [Stage 6](06-memory-rag.en.md) |
| **3. Harness Engineering**<br>(**This section**) | The **execution and control layer around the model** (loop / retry / sandbox / observability / deployment) | This stage |

**How do you tell which layer you are working on? Ask**:

1. Am I changing the **string itself**? → Prompt engineering
2. Am I changing the **information put into the window**? → Context engineering
3. Am I changing the **surrounding program that calls the model**? → Harness engineering

→ The three layers are **orthogonal**: a one-call RAG app is still doing context engineering (the key is how the window is assembled); a 50-call chatbot with no retrieval is still only doing prompt engineering.

### The 8 Core Components of a Harness

**Harness Engineering (agent runtime design) = connecting the LLM, tools, memory, state, workflow control, error handling, eval, observability, and deployment into an executable, observable, maintainable agent system.**

→ Everything that is **not part of the model weights**, and is not just the prompt string itself, falls under harness. A deployable agent runtime includes these 8 core components (the first 6 are built into the runtime, the 7th, eval, is a plug-in tool, and the 8th, cost / latency, is a cross-cutting concern):

| Component | What it Does | Corresponding Exercise in this Stage |
|---|---|---|
| **Agent loop**<br>(within one run) | The "LLM → tool → result → LLM" loop, stably handling multiple turns. **This is the loop inside a single run**, a different level from Layer 4 Loop Engineering, which is about long-horizon execution across sessions | Exercise 1 Multi-agent debate |
| **Tool registry** | Dynamic tool dispatch, permission gates, sandboxing | (Present in every framework / SDK) |
| **Context manager** | Message history management, context window control, auto-compaction | Stage 6 + This stage's Exercise 4 SDK |
| **Safety layer** | Permission prompts, sandboxed execution, interception of destructive ops | (Built into Claude Code, customizable in SDKs) |
| **Retry / recovery** | How to handle tool failure (exception vs. the LLM reflecting on the error itself) | Exercise 4 SDK Advanced |
| **Telemetry / Observability** | Metrics, logging, token counting, trace export | **Exercise 3 Observability** |
| **Eval harness** | Regression testing, quality gates, A/B testing | **Exercise 2 Eval** |
| **Cost / Latency optimization** ⭐ Required for 2024-2026 | Prompt caching, model routing, thinking budget, batching, semantic cache | **Exercise 6 Cost optimization** (New) |

**Framework vs. Harness: key difference**:

- **Framework** ([Stage 4](04-agent-frameworks.en.md)) defines the **API** — what the interface you call looks like
- **Harness** (this section) defines the **runtime** — how it runs, how it recovers, and how it is observed

### Feedback loops: agents improve from feedback, not a more perfect prompt

The 8 components above are the harness "skeleton." But what actually makes the skeleton work is something more basic than any single component: **an agent gets better by feeding feedback back into the loop, not by wording the opening prompt more perfectly.**

An analogy: a student doesn't get better because the assignment was phrased more elegantly; they improve by getting feedback at the right moments — handing in a draft, a teacher's mid-task nudge, having the finished work graded, redoing it next time. Agents are the same, and feedback can enter at four moments:

| Moment | In plain words | What it looks like in engineering |
|---|---|---|
| **1. Tool return values** | The text a tool returns is itself feedback written for the agent | Write the error message, hints, and next-step suggestions *clearly* — don't just dump a stack trace |
| **2. Mid-run steering** | Slip a message in between the agent's two thinking steps to redirect it | Inject a message mid-run (steering); no need to wait a whole turn to course-correct |
| **3. End-of-turn acceptance** | When a turn finishes, have *someone else* check it against the goal | Use a separate evaluator to compare against the goal, instead of letting the agent grade itself |
| **4. Outer loop** | Re-invoke the agent against the same goal until it's done | Goal-driven re-runs (like OpenAI Codex's `/goal`, or a cron re-run) |

**Why #3 (an independent check) matters most**: Anthropic's own experiments found that when you ask an agent to check its own work, it almost always praises it — even when the quality is obviously mediocre. So they split the "maker" agent from the "checker" agent: one builds, the other uses tools (like Playwright) to actually click and test, then reports bugs back. Tuning an external checker to be more skeptical is far easier than making one agent harder on itself.

> 📚 Real example: Anthropic's [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) (2026-03) uses planner → generator → evaluator, letting an agent run for hours to build a full music-production app, correcting on every round from the evaluator's feedback.

### Reference Implementations

Want to see what a harness running in production looks like? Two references:

- **The entire Claude Code runtime** — is a reference harness implementation. **For a source-reading exercise, see [Stage 5.7](05-claude-code-ecosystem.en.md#57--dissecting-claude-code-source-reference-harness-implementation--a-must-read-for-track-b)** (clone `claude-agent-sdk-python` and dissect the main loop + where the first 6 runtime components from the table above live; the 7th, Eval harness, is a plugin, and the 8th, Cost / Latency, is cross-cutting, see the deep-dive below)
- **`anthropics/claude-agent-sdk-python`** source — the specific repo used in the exercise above


**Full harnesses you can just open and read** (all open-sourced in 2026 and large enough to be worth it; read them against the eight core components above):

| Project | ⭐ | Language / License | What it demonstrates |
|---|---|---|---|
| [xai-org/grok-build](https://github.com/xai-org/grok-build) | ★ 25k+ | Rust / Apache-2.0 | SpaceXAI's terminal coding agent. One core serves an interactive TUI, a headless mode for CI, and editor embedding, which makes it a complete example of **how many execution modes one harness has to serve** |
| [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw) | ★ 22k+ | TypeScript / Apache-2.0 | A reference stack for running other people's agents (Hermes, LangChain Deep Agents, OpenClaw) inside a managed runtime. The interesting part is **where responsibility splits between harness and sandbox**: it builds no agent of its own, only inference management and lifecycle. **⚠️ The maintainers call it alpha** and handle issues and PRs on a best-effort basis |

→ The remaining 6 exercises in this stage (multi-agent / eval / observability / SDK / deploy / cost) each cover one facet of the harness. Completing the full stage = assembling a complete mental model of harness engineering.

### Deep dive into the 8th core component — Cost / Latency Optimization (Required for 2024-2026 Productionization)

When a production agent runs long enough, **cost and latency will eat up most of your budget and user experience**. From 2024-2026, frontier models have treated this as a first-class API feature—**knowing how to use it = saving 50-90% on cost / latency**.

| Technique | How it Saves | 2026 Status |
|---|---|---|
| **Prompt caching** | Recurring prefixes (system prompt, long context) are billed once, subsequent cache hits get a ~90% discount | Fully supported by Anthropic / OpenAI / Gemini, automatic or manual tagging |
| **Model routing / cascade** | Simple queries → smaller model, difficult queries → frontier model | Built into [RouteLLM](https://github.com/lm-sys/RouteLLM) / [OpenRouter](https://openrouter.ai/) for production |
| **Thinking budget** | Controllable thinking token limit for reasoning models, trading off latency / quality | Claude / Gemini API parameter, high by default in o-series |
| **Speculative decoding** | A smaller model predicts N tokens, a larger model validates them at once, ×2-3 speedup for a single model | Built into vLLM / TGI, automatic at the inference layer |
| **Batching** | Processing multiple queries in parallel for higher GPU utilization | vLLM, production inference layer |
| **Semantic caching** | Sharing answers for similar queries (not just exact matches) | Built into [GPTCache](https://github.com/zilliztech/GPTCache) / Helicone |

**How Track A can use this** (for those using CLI agents):

- Set up prompt caching in Claude Code / Cursor to save 50-90% on daily session costs
- Use [RouteLLM](https://github.com/lm-sys/RouteLLM) / [OpenRouter](https://openrouter.ai/) to dynamically switch models (simple questions use Haiku / Flash, difficult ones use Opus / Pro)
- Use the `thinking_budget` parameter in the Claude API to control the token limit for reasoning models

**How Track B can build this** (for those writing their own agents):

- Build a custom cascade router that maps query embeddings → classifier → model
- Monitor token cost within the agent loop and automatically downgrade if the budget is exceeded
- Integrate a semantic cache layer in the deployed environment
- Observability platforms like [Helicone](https://github.com/Helicone/helicone) / [langfuse](https://github.com/langfuse/langfuse) already have these features built in, so you do not have to write them yourself

## 🛠 Hands-on Exercises (Basic Illustrative Exercises)

### Exercise 1: Multi-Agent Debate
Have two agents debate a topic (e.g., "Should we use Python or Rust for the backend?"), with a third agent acting as a referee. Observe the patterns of convergence or divergence in the debate.

### Exercise 2: Eval
Write an eval for your previous agent, run it N times, and measure the success rate. Replace the habit of "I'll just take a look" with a quantitative approach.

### Exercise 3: Observability
Connect LangSmith, Helicone, or weave to an agent and view the full trace. Understand that "debugging an agent without observability = a black box".

### Exercise 4: Advanced SDK
Use streaming + prompt caching + tool use in a single call. See how the costs come down.

### Exercise 5: Deploy
Package an agent into Docker and deploy it to the cloud (any provider will do). Learn to turn a prototype into something that can be run by others.

### Exercise 6: Cost Optimization (New) ⭐
Measure the token cost of any of your previous exercise agents, then add prompt caching and measure again. Observe the relationship between cache hit rate and cost reduction. **Bonus**: Connect to [RouteLLM](https://github.com/lm-sys/RouteLLM) or [OpenRouter](https://openrouter.ai/) and implement cascade routing (simple queries → Haiku / difficult queries → Opus), and measure the average cost.

## 📊 Agent Benchmark Landscape: How to read it, not just the leaderboard + ⚠ Reward-Hacking Warning

Before choosing a model or building an agent, you'll want to look at benchmark numbers—but in **April 2026, UC Berkeley discovered that all 8 major agent benchmarks can be reward-hacked to ~100%**. Below is the 2026 leaderboard status + how to read it without getting misled.

### Mainstream Agent Benchmark SOTA as of 2026-05

| Benchmark | Domain | 2026-05 SOTA | Leading Model |
|---|---|---|---|
| [**SWE-bench Verified**](https://www.swebench.com/) | Software Engineering / code agent | **88.6%** | Claude Opus 4.8 |
| [**Terminal-Bench**](https://github.com/laude-institute/terminal-bench) | terminal tasks | Leading | Claude Opus 4.8 |
| **GAIA** | general assistant | **74.6%** | Claude Sonnet 4.5 (Princeton HAL) |
| [**WebArena**](https://github.com/web-arena-x/webarena) | web navigation | **68.7%** | (leading model not disclosed) |
| [**ClawBench**](https://github.com/TIGER-AI-Lab/ClawBench) | browser-agent tasks on real websites | **44.6%** (lenient)/**24.6%** (strict) | Claude Opus 4.7 (V2 Hermes leaderboard history, 2026-08 snapshot: 58/130 passed); 283 tasks, 144 real websites, Apache-2.0, [paper](https://arxiv.org/abs/2604.08523); V2's two-stage rubric is stricter than V1 |
| [**OSWorld**](https://github.com/xlang-ai/OSWorld) | OS-level desktop control | v1 **76.26%** (near-saturated) | OpenAI CUA 38%; [OSWorld 2.0](https://osworld-v2.xlang.ai/) (2026-06, long-horizon) superseded v1 — realistic long-task SOTA only ~20% (Opus 4.8 20.6%), see Stage 8 |
| [**τ-bench**](https://github.com/sierra-research/tau-bench) | multi-turn dialogue with tool use | (Harder to hack) | Anthropic / OpenAI leading |
| **RE-bench** | research engineering | (Harder to hack, close to human baseline) | Frontier models |

> **⚠ The table above holds Opus 4.8-era numbers**: these are measured results attributed to the model that produced them, so they stay as-is. Claude Opus 5 (`claude-opus-5`) shipped 2026-07-24 and Anthropic published claims of improvement, but those claims have no third-party replication yet, so the table is deliberately not updated with them.

> **Mythos-class tier (Claude Fable 5 — shipped 2026-06-09)**: [**Claude Fable 5**](https://www.anthropic.com/news/claude-fable-5-mythos-5) (`claude-fable-5`, Mythos-class, positioned above the Opus class) shipped as the publicly available highest-capability Claude tier alongside its sibling Claude Mythos 5 (`claude-mythos-5`, some safeguards lifted, limited to approved customers). It was suspended 2026-06-12 by a US export-control directive and [redeployed globally 2026-07-01](https://www.anthropic.com/news/redeploying-fable-5) (Mythos 5 restored only for approved US organizations). The numbers above stay attributed to their original models; Fable 5's official benchmark numbers were never published, so it is not listed. **Fable 5 is the highest Claude tier; the Opus-class flagship is now Claude Opus 5 (Opus 4.8 remains available, listed under legacy models).**

→ For detailed rankings + live updates: [Agent Benchmark Leaderboard 2026](https://benchmarkingagents.com/agent-benchmarks/), [Rapid Claw AI Agent Framework Scorecard 2026](https://rapidclaw.dev/blog/ai-agent-benchmarks-2026)

### ⚠ Berkeley 2026-04 Reward-Hacking Warning

[**UC Berkeley RDI Report 2026-04-12**](https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/): An automated scanning agent systematically audited **8 major benchmarks** (SWE-bench / WebArena / OSWorld / GAIA / Terminal-Bench / FieldWorkArena / CAR-bench, etc.) and found that **every single one could be reward-hacked to nearly 100% without the agent actually solving a single task**.

This means that for numbers on the leaderboard like "Claude 87.6% / GPT 85.0%", some X% of that might be hacked, not from genuinely solving the task.

### How to Read Benchmarks Without Being Misled

| Approach | Recommendation |
|---|---|
| Only look at the leaderboard top | ❌ All 8 above have been proven hackable |
| Look at task-level success rate breakdown | ✅ Most hacks are concentrated in a few tasks |
| Run your own hold-out test set | ✅✅ The most reliable method, a must for production agents |
| Check the trajectory / log to see if the task was really solved | ✅ Distinguishes reward hacking from a genuine solve |
| Look at multiple benchmarks + your own use case | ✅ Don't rely on a single metric |

**Which benchmarks are harder to hack (as of 2026-05)**:

- **τ-bench** — Multi-turn dialogue + tool use, denser reward function
- **RE-bench** — Real-world research engineering tasks
- **Your own production eval set** ⭐ Always the most reliable

> 💡 **The discipline of production agent eval**:
> - Don't take external benchmark numbers as ground truth; they tell you the "upper limit," not "real-world performance."
> - Your own eval set (internal hold-out test) is the basis for go-live decisions.
> - Every time a model is upgraded → run it against your internal eval set for validation, don't just look at the vendor's published benchmark improvements.
> - Connect to [langfuse](https://github.com/langfuse/langfuse) / [promptfoo](https://github.com/promptfoo/promptfoo) to automate eval and run it with every deployment.

> 📊 **For observability, learn one portable standard + two eval ideas**: (1) **OpenTelemetry GenAI conventions** (`gen_ai.*`): langfuse / Arize Phoenix / Helicone all emit OTel-compatible spans, so learning this layer keeps you from being locked to one tool; the OTel-native [Arize Phoenix](https://github.com/Arize-ai/phoenix) (★ 11k+) is worth a look. (2) **pass^k**: the probability of solving the same task k times in a row (reliability, not a single pass), measured by [τ²-bench](https://github.com/sierra-research/tau2-bench). (3) Multi-agent failures have a ready vocabulary: **MAST** ([arXiv 2503.13657](https://arxiv.org/abs/2503.13657), 14 failure modes in 3 categories).

## 🎯 Recommended Tools for Multi-Agent / Production (by Use Case)

Don't know where to start choosing tools? Below are the common pairings in the industry for 2025-2026—**use "Scenario" as your entry point, and click the repo link for a deeper dive**:

| Scenario | Recommended Tool | Why |
|---|---|---|
| **Writing your first multi-agent** (fastest to get started) | [crewAI](https://github.com/crewAIInc/crewAI) | Role-based, get it running in a few lines of code, straightforward production patterns |
| **Want a group debate / brainstorm pattern** | [AutoGen](https://github.com/microsoft/autogen) | GroupChat for free-form debate, from Microsoft |
| **Need an audit trail / checkpoint / human-in-the-loop for production** | [LangGraph](https://github.com/langchain-ai/langgraph) | State machine approach, most complete control |
| **Standardizing eval** (a must for CI / regression) | [promptfoo](https://github.com/promptfoo/promptfoo) ⭐ | YAML config, cross-model comparison, ★ 24k+ |
| **Eval + observability on the same platform** | [langfuse](https://github.com/langfuse/langfuse) ⭐ | OSS, tracing + eval + prompt mgmt, ★ 32k+ |
| **Quick instrumentation without code changes** | [Helicone](https://github.com/Helicone/helicone) | Proxy-based, not tied to a framework |
| **Entire stack is on LangChain** | [LangSmith](https://www.langchain.com/langsmith) (Commercial) | Official observability from LangChain |
| **Building a Claude agent** (programmatically) | [claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) ⭐ | Official agent SDK from Anthropic, same runtime as Claude Code |
| **Deploying an agent as an API service** | [BentoML](https://github.com/bentoml/BentoML) | The most complete, Docker + serving |
| **Self-hosting an open-source LLM** (to replace paid APIs) | [vLLM](https://github.com/vllm-project/vllm) | High-throughput serving, ★ 87k+ |
| **Fine-tuning an open-source LLM** | [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | Unified SFT/DPO/PPO/GRPO for 100+ models, no-code Web UI, widest Chinese community, ★ 73k+ |

**Suggested adoption sequence**:

1. First multi-agent: **crewAI** (role-based, simplest)
2. Add eval: **promptfoo** (YAML, CI integration)
3. Add observability: **langfuse** (OSS, complete)
4. Production upgrade: Switch to **LangGraph** (stronger control) + **BentoML** (deploy)
5. Advanced: Self-host LLMs with **vLLM**, fine-tune with **LLaMA-Factory**

## 🎯 Featured Projects (Templates / SDKs / Tool Collections)

Categorized by use case, a single table to get you started with 29 projects. **Use "Who is it for" as your entry point, and click the repo link for a deeper dive.**

| Category | Project | ⭐ | Who is it for | Why it's recommended / Notes |
|---|---|---|---|---|
| **Multi-Agent Orchestration** | [microsoft/autogen](https://github.com/microsoft/autogen) | ⭐⭐⭐⭐⭐ | Those who want a GroupChat free-debate pattern | Introduced in Stage 4, revisit for multi-agent debate / brainstorming patterns in production scenarios |
| | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | ⭐⭐⭐⭐⭐ | Those who want a role-based assembly line | Role-based multi-agent (research → writer → reviewer), the simplest production pattern |
| | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | ⭐⭐⭐⭐⭐ | Those needing an audit trail / checkpoint / human-in-the-loop | State machine approach, strongest for production control |
| | [open-multi-agent/open-multi-agent](https://github.com/open-multi-agent/open-multi-agent) | ⭐⭐⭐⭐ | TypeScript users who want to compare dynamic planning against a fixed pipeline in one repo | A coordinator plans the task DAG at runtime and hands it to a scheduler; `runTeam()` plans from a goal while `runTasks()` runs an explicitly defined pipeline, so the two styles sit side by side. The three above are Python-ecosystem; this adds the TypeScript route. ★ 6.8k+, MIT |
| | [AMAP-ML/LongHorizon-Harness](https://github.com/AMAP-ML/LongHorizon-Harness) | ⭐⭐⭐ | Those who want to see what the "check" box looks like in a real project | Splits long tasks into Manager / Executor / **Auditor** roles. The Executor starts each round with fresh context, and the Auditor independently checks the result before it is written into persistent state. This is the concrete implementation of the "check whether it is right" box in the graph above. It wraps Claude Code / Codex externally, so you do not need to rewrite the agent loop yourself. **Very new**: created 2026-08-04, 2 contributors, no long-term maintenance record yet. ★ 1.1k+, MIT |
| **Eval Frameworks** | [promptfoo](https://github.com/promptfoo/promptfoo) ⭐ | ⭐⭐⭐⭐⭐ | To standardize the eval process, CI integration | YAML config, cross-model comparison. ★ 24k+, MIT |
| | [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | ⭐⭐⭐⭐ | For academic benchmarks (MMLU / HellaSwag / GSM8K) | Academic grade. ★ 13k+, MIT |
| | [openai/evals](https://github.com/openai/evals) | ⭐⭐⭐⭐ | For OpenAI-specific evals / want to contribute upstream | ★ 19k+ |
| **Observability** | [langfuse](https://github.com/langfuse/langfuse) ⭐ | ⭐⭐⭐⭐⭐ | For self-hosting production observability | OSS LangSmith alternative, traces + sessions + evals + prompt mgmt. ★ 32k+, MIT |
| | [LangSmith](https://www.langchain.com/langsmith) (Commercial) | ⭐⭐⭐⭐ | For those with their entire stack on LangChain / LangGraph | Official from LangChain, hosted version only |
| | [Helicone](https://github.com/Helicone/helicone) | ⭐⭐⭐⭐ | For quick instrumentation without code changes | Proxy-based, get logging + caching for free. ★ 6k+, Apache 2.0 |
| | [weave (W&B)](https://github.com/wandb/weave) | ⭐⭐⭐⭐ | For teams already using W&B for ML experiment tracking | W&B tracing + eval, integrates with wandb |
| | [comet-ml/opik](https://github.com/comet-ml/opik) | ⭐⭐⭐⭐ | For eval + observability on one open-source platform | Trace what your LLM / agent did, track experiments, and run quality checks (evals). ★ 21k+, Apache 2.0 |
| | [pydantic/logfire](https://github.com/pydantic/logfire) | ⭐⭐⭐⭐ | For tracing agent / LLM calls on the OpenTelemetry standard | Watch and debug what your agent / LLM calls did; from the Pydantic team, built on the OpenTelemetry standard. ★ 4.4k+, MIT |
| **Safety / Guardrails** | [NVIDIA-NeMo/Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) | ⭐⭐⭐⭐ | For safety rules around an agent's inputs and outputs | Safety rules you wrap around an LLM app — keep it on-topic, block jailbreaks, filter bad output. ★ 6.6k+, Apache 2.0 |
| **Advanced Anthropic SDK** | [anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python) | ⭐⭐⭐⭐⭐ | For building applications directly on the Claude API | Official Python SDK: streaming / async / tool use / prompt caching / batches / files |
| | [anthropic-sdk-typescript](https://github.com/anthropics/anthropic-sdk-typescript) | ⭐⭐⭐⭐ | For TypeScript / Node / web apps | The TS version of the Python SDK |
| | [claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) ⭐ | ⭐⭐⭐⭐⭐ | For building Claude-based agents, not just API calls | Built-in tool use loop / file access / sandbox / subagent orchestration; same runtime as Claude Code, read the source to see how it works internally. ★ 7.6k+, MIT |
| | [claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript) | ⭐⭐⭐⭐ | For Claude agents in a Node / web app environment | The TS version of the Claude Agent SDK. ★ 1.7k+ |
| | [Anthropic Cookbook (Advanced)](https://github.com/anthropics/anthropic-cookbook) | ⭐⭐⭐⭐ | For seeing official advanced SDK patterns | Especially the `prompt_caching.ipynb` / `tool_use/` / `multimodal/` notebooks |
| **Structured Output** | [BoundaryML/baml](https://github.com/BoundaryML/baml) | ⭐⭐⭐⭐ | For getting reliable, validated JSON out of any model | A small dedicated language for getting reliable, checked JSON out of LLMs; works with Claude / OpenAI / local models across 7 programming languages. ★ 8.8k+, Apache 2.0 |
| **Deployment** | [BentoML](https://github.com/bentoml/BentoML) | ⭐⭐⭐⭐ | For packaging an agent into a production API service | Docker + serving framework. ★ 8.8k+, Apache 2.0 |
| | [LangServe](https://github.com/langchain-ai/langserve) | ⭐⭐⭐ (⚠️ archived) | For quickly deploying a LangChain agent | Based on FastAPI; ⚠️ **repo archived 2026-05** — use LangGraph Platform for new deploys |
| | [vLLM](https://github.com/vllm-project/vllm) | ⭐⭐⭐⭐ | For self-hosting an open-source LLM to replace paid APIs | High-throughput LLM serving for Llama / Qwen, etc. ★ 87k+, Apache 2.0 |
| **Chinese Deploy / Fine-tune** | [datawhalechina/self-llm](https://github.com/datawhalechina/self-llm) | ⭐⭐⭐⭐ | For Chinese teams wanting to self-host open-source LLMs | A complete Chinese guide from training-to-deployment, for Qwen / Llama / GLM / multimodal. ★ 31k+, Apache 2.0 |
| | [hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | ⭐⭐⭐⭐⭐ | For fine-tuning open-source LLMs (beyond just prompt eng) | Unified SFT/DPO/PPO/GRPO for 100+ models, no-code Web UI, widest Chinese community. ★ 73k+, Apache 2.0 |
| **Multi-Agent Case Studies** | [geekan/MetaGPT](https://github.com/geekan/MetaGPT) | ⭐⭐⭐⭐⭐ | For seeing role division + artifact handoff patterns | An SOP-based multi-agent team of PM / Architect / Engineer, generating PRD → design → code. ★ 67k+, MIT |
| | [OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev) | ⭐⭐⭐⭐ | For seeing agent debate / peer-review patterns | Conversational software development where agents debate each other on design / code / test. ★ 33k+, Apache 2.0, has a zh README |
| | [princeton-nlp/SWE-agent](https://github.com/princeton-nlp/SWE-agent) | ⭐⭐⭐⭐ | To understand why tool design > prompt tuning | The Agent-Computer Interface (ACI) design philosophy, backed by a Princeton paper, a leading method on SWE-Bench. ★ 20k+, MIT |

> 🌳 For **Claude's native subagent mechanism** (multi-agent without a framework), see [Stage 5.5](05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature). This stage focuses on frameworks / production; Stage 5.5 focuses on markdown-based subagent orchestration.

## ✅ Self-Check After Stage 7

Can you:

- [ ] Design a multi-agent system and clearly explain its collaboration protocol?
- [ ] Run an automated eval pipeline in CI?
- [ ] Connect observability (tracing) to a production agent?
- [ ] Measure the cost difference before and after implementing prompt caching on a real workload?
- [ ] Deploy an agent to the cloud (any provider)?

If you can do all of these → first go to [**Stage 7.5 — Advanced Agentic Concepts Map**](07.5-advanced-agentic-concepts.en.md) (1 week, no coding — build a frontier concept map and locate which advanced concepts the industry is still debating), then proceed to [**Stage 8 — Agent Interfaces**](08-agent-interfaces.en.md) (**a shared hub for both tracks**) to learn how agents interact with the non-API world (Computer Use / Browser Use / Sandbox). Or, pick a [specialized branch](../README.en.md#-learning-map-two-tracks), or come back and contribute to this repo.

## 💡 What's Next

You now have the foundational skills. For the next 6-12 months, you should focus on:

1. **Picking one production system** and taking it from prototype to production.
2. **Contributing upstream** (LangGraph, AutoGen, MCP servers, Anthropic cookbook).
3. **Reading papers**—agent research is moving fast.
4. **Making something tangible**—open-source a real tool, stop just writing tutorials.

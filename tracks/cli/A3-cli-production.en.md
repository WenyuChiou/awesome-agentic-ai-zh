# A3 — Integration & Production

> [繁體中文](./A3-cli-production.md) | [简体中文](./A3-cli-production.zh-Hans.md) | **English**

> [← A2 — CLI Workflow Patterns](A2-cli-workflow.en.md) · **Track A: CLI Power User** — Stop 3 (final)

⏱ **Time estimate**: 1-2 weeks (~8-15 hours)

> 📋 **Chapter structure**: Learning goals → Entry conditions → Required reading → Hands-on exercises → Curated Projects → Self-check
> 🔑 **Key terms** (used in this chapter):
> - **Required here**: MCP (connect CLI to external data / tools), CI (run checks automatically on every push)
> - **Further-reading terms**: observability (trace CLI behavior), eval (measure CLI quality), prompt caching (reduce repeated-context cost), cost tracking (record token spend)
>
> Full definitions: [`resources/glossary.en.md` 5 + 6](../../resources/glossary.en.md#5-claude-code-ecosystem)

After your CLI runs smoothly, the next step is to **wire the CLI into your real team workflow**. This stop does 3 things:

1. **Tool connection** — MCP servers connect the CLI to Slack / Gmail / your internal API
2. **Automated checks** — CI (GitHub Actions) runs CLI review on every PR
3. **Cost and logs** — observability tools track cost / latency for each task

After this stop, the CLI is no longer just your personal tool — it's part of your team's workflow.

## 📌 Learning Goals

- Connect 1-3 MCP servers to your CLI (Slack / Gmail / internal API / DB)
- Set up GitHub Actions to auto-run Claude Code (PR review, release notes, etc.)
- Add observability (trace, cost, latency) to CLI workflows
- Plan a cost budget — know roughly what a big task costs in tokens

## 🚪 Entry Conditions

You should already:

- Have completed [A1](A1-cli-intro.en.md): CLI picked, installed, authenticated
- Have completed [A2](A2-cli-workflow.en.md): finished the project-rules card and review Skill
- Be comfortable with GitHub Actions / CI basics (can read a `.yml` workflow)
- Have at least a rough idea of what MCP is (if not, skim [Stage 5.2](../../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol--foundation) first)

Not there yet? → finish [A1](A1-cli-intro.en.md) + [A2](A2-cli-workflow.en.md) first. A3 is "combine everything so far → wire it into production"; skipping ahead won't make sense.

## 📚 Required Reading

1. [**Stage 5.2 — MCP (Model Context Protocol)**](../../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol--foundation) — MCP concept and basics
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — can significantly reduce repeated context cost under cache-eligible conditions (unchanged context, ≤5-minute reuse window, etc.); actual savings depend on the workflow, so use the official article's conditions as the reference
3. [**Stage 7 — Observability section**](../../stages/07-multi-agent-production.en.md#exercise-3-observability) — langfuse / Helicone / weave
4. [**`resources/cli-agents-guide.en.md`** "Common pitfalls"](../../resources/cli-agents-guide.en.md) — most common production issues with CLIs

## 🛠 Hands-on Exercises

### Exercise CLI-9: MCP server connected to CLI
Following [Stage 5.2 Exercise: MCP client](../../stages/05-claude-code-ecosystem.en.md#hands-on-exercises), connect at least one useful MCP server to your CLI:

- `filesystem` server → let the CLI read files outside its default scope
- `github` server → let it read PRs / issues directly
- Custom server → connect your internal API / DB

Success: in a CLI conversation, ask "does my PR have conflicts?" and have the CLI answer via MCP (without you opening a browser).

### Exercise CLI-10: GitHub Actions + CLI
Write `.github/workflows/cli-review.yml`:

- Trigger: PR opened / synchronize
- Run: in the GH Actions runner, execute Claude Code (or Codex), give it `git diff`, and ask it to use the [`review-changes` Skill](A2-cli-workflow.en.md#hands-on-exercise-cli-6-turn-a-repeated-review-into-a-skill) you built in A2
- Output: PR comment

Success: open a new PR, see a review comment within 1-2 minutes.

> Starting points: Anthropic's official [`claude-code-action`](https://github.com/anthropics/claude-code-action); Codex has GitHub App and CLI modes.

### Exercise CLI-11: Cost tracking
Run a daily task. **Predict** the token usage first, then actually run it and check the usage. The gap is usually big (you typically underestimate).

- Math: input tokens + output tokens × model price each
- Connect langfuse or Helicone ([Stage 7 Observability](../../stages/07-multi-agent-production.en.md#exercise-3-observability)) for tracing
- Observe: which sub-task consumes the most tokens? Are you sending unnecessary long context?

### Exercise CLI-12: Skill / plugin team sharing
Put A2’s `review-changes` Skill at `skills/review-changes/SKILL.md` inside the plugin root, then publish the plugin to an internal marketplace or GitHub. Teammates get the same Skill after installing the plugin.

`CLAUDE.md` is the project’s own instruction file and stays in the repo; it is not content to package in this plugin.

- Skill / plugin details in [Stage 5.3 + 5.4](../../stages/05-claude-code-ecosystem.en.md)
- Template: [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

## 🧭 Advanced Concepts in Daily CLI Work (7 Playbooks) 🆕

Track A users are **already using** [Stage 7.5 advanced concepts](../../stages/07.5-advanced-agentic-concepts.en.md) — they just have not named them yet. Pick the **2-3 playbooks you use most often** and treat the rest as further reading — each in ≤ 6 lines. **Want the deeper theory → go to Stage 7.5.**

> 📌 **Rule**: after each playbook, ask yourself "will I do something differently in the next PR?" **Yes** → applied; **No** → skip to the next one.

### 📋 Playbook 1: Scope unclear, agent overreaches

- **When**: You send Codex/Gemini on a sweep and are not sure whether it will silently touch unrelated files (the F11/F12 kind of failure)
- **Do**: At the top of the brief, state "change X / do not cross Y" explicitly; add a path filter to the acceptance preset
- **Concepts**: Work Boundary + Hierarchical Task Decomposition · 📊 See [concept-cluster](../../resources/diagrams/concept-cluster.en.png), Service × orchestration cluster
- **Read more**:

  | Source | Link |
  |---|---|
  | HumanLayer | [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) |
  | Anthropic | [How Anthropic teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) |
  | Internal | [Stage 7.5 🧭 work boundary stack](../../stages/07.5-advanced-agentic-concepts.en.md#-concept-map-spine-the-four-layer-work-boundary) |

### 📋 Playbook 2: Multi-agent parallel runs, results conflict

- **When**: Claude planner + 2-3 Codex agents run in parallel and the merge ends up with conflicts / drift
- **Do**: Give each agent its own commit; use a reviewer pattern to catch drift (not one giant merge); standardize the brief format + `result.json` schema
- **Concepts**: Contract Hand-offs + Speculative Parallel · 📊 See [concept-cluster](../../resources/diagrams/concept-cluster.en.png), Service × orchestration + Types × orchestration
- **Read more**:

  | Source | Link |
  |---|---|
  | Addy Osmani | [Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/) |
  | Daniel Vaughan | [Running Multiple Codex Agents Parallel](https://codex.danielvaughan.com/2026/04/18/running-multiple-codex-agents-parallel-orchestration/) |
  | Internal | [agent-collab-skills](https://github.com/WenyuChiou/agent-collab-skills) (`agent-task-splitter` + `agent-output-reconciler`) |

### 📋 Playbook 3: Reviewing agent output

- **When**: An agent finished the PR, you do not want to merge it blindly, and human review cannot keep up with the throughput
- **Do**: Add an LLM-as-judge subagent for automatic evaluation (binary pass/fail); humans only spot-check edge cases; run the acceptance-gate preset before commit
- **Concepts**: Agent-as-Judge + Plan-Act-Reflect · 📊 See [reading-decision-tree](../../resources/diagrams/reading-decision-tree.en.png), blue eval branch
- **Read more**:

  | Source | Link |
  |---|---|
  | Hamel Husain | [LLM-as-a-Judge: Complete Guide](https://hamel.dev/blog/posts/llm-judge/) |
  | Hamel Husain | [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) |
  | Simon Willison | [Sub-agents in Claude Code](https://simonwillison.net/2025/Oct/11/sub-agents/) |

### 📋 Playbook 4: Dispatching subagents for independent tasks

> 💡 **First time hearing about subagents?** In one sentence: **a subagent is a “child Claude” spawned from the main Claude session**. It has its own isolated context and reports back when done. **Dispatch** means asking the subagent to do work, like assigning a task to a teammate. Full concept → [Stage 5.5](../../stages/05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature).

- **When**: before committing a large change / entering an unfamiliar repo / running an LLM-as-judge auto-eval / applying the same review to 4 targets
- **Do**: invoke Claude Code **built-in** subagents (no custom file required):
  - `code-reviewer` — review staged diff, find bugs + security issues
  - `Explore` — read-only codebase search, find entry points / symbols
  - `Plan` — design a step-by-step implementation plan
  - `general-purpose` — fallback when you are unsure which one to use, or for multi-step research
- **Concepts**: Hierarchical Task Decomposition + Context Isolation · 📊 See [concept-cluster](../../resources/diagrams/concept-cluster.en.png), Service × orchestration cluster
- **Read more**:
  - [Stage 5.5 Subagents](../../stages/05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature) (full theory + decision table)
  - [`resources/subagent-cookbook.en.md`](../../resources/subagent-cookbook.en.md) (**15 recipes** with copy-paste prompt templates)

---

### 📋 Playbook 5: Running CLI agent in CI

- **When**: You wire `codex exec` / `claude --print` into GitHub Actions, cannot require a human to hit yes every time, and bandwidth constraints mean you cannot always use Opus
- **Do**: Use layered autonomy (preset auto-runs / commit requires review / push requires human sign-off); set a fallback cheaper model (if Opus is down, fall back to Haiku)
- **Concepts**: Autonomy Gradients + Graceful Degradation · 📊 See [concept-cluster](../../resources/diagrams/concept-cluster.en.png), Config × governance cluster
- **Read more**:

  | Source | Link |
  |---|---|
  | Anthropic | [How Anthropic teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) |
  | Anthropic Engineering | [Equipping Agents with Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) |
  | Internal | [Stage 5.5 Subagents](../../stages/05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature) + Exercise CLI-10 |

### 📋 Playbook 6: Controlling cost

- **When**: You use Codex for a large batch of work, the monthly API bill is getting out of control, and you want to stay inside budget
- **Do**: Set `max_cost_usd` in `plan.yml`; use a cheap model (Haiku) for exploration and an expensive model (Opus) only for polish; turn on prompt caching (can significantly reduce repeated context cost under cache-eligible conditions); automate QA instead of spending human time
- **Concepts**: Cost-aware Budget Gates + Throughput-Merge Philosophy · 📊 See [concept-cluster](../../resources/diagrams/concept-cluster.en.png), Config × resilience cluster
- **Read more**:

  | Source | Link |
  |---|---|
  | Simon Willison | [Sub-agents](https://simonwillison.net/2025/Oct/11/sub-agents/) |
  | Anthropic | [Prompt Caching](https://www.anthropic.com/news/prompt-caching) |
  | Internal | This stage's Exercise CLI-11 (token tracking + langfuse integration) |

### 📋 Playbook 7: Hardening workflow, preventing drift

- **When**: You wrote rules in `CLAUDE.md` / `SKILL.md` but nobody enforces them, or you added a preset YAML and do not know whether it actually works
- **Do**: Intentionally break one rule and run the acceptance gate to see whether it catches it (chaos test); treat `docs/` as the single source of truth and keep `CLAUDE.md` as an entry map only
- **Concepts**: Failure Injection + System of Record · 📊 See [failure-lifecycle](../../resources/diagrams/failure-lifecycle.en.png) (the F11-F14 evolution loop)
- **Read more**:

  | Source | Link |
  |---|---|
  | HumanLayer | [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) |
  | agent-collab-skills | [observed-failure-modes.md](https://github.com/WenyuChiou/agent-collab-skills/blob/main/docs/observed-failure-modes.md) |
  | Internal | [Stage 7.5 🔁 failure-mode lifecycle](../../stages/07.5-advanced-agentic-concepts.en.md#-failure-mode-lifecycle-how-industry-agent-failures-evolved-into-best-practice) |

---

→ **7 playbooks = a bridge from 7 triggers to 12 concepts and the corresponding reading sources**. Want the underlying theory / the full set of 12 concepts / all 8 cross-vendor principles → [Stage 7.5](../../stages/07.5-advanced-agentic-concepts.en.md).

## 🎯 Curated Projects

Four categories, nine projects, one table. **Pick an entry point from the "Who it's for" column; click through to the repo when you want the details.**

> 💡 **Looking for MCPs that connect to daily tools** (Notion / Obsidian / Excel / Postgres / Playwright / Slack / Linear / Figma…): see [`resources/mcp-skills-catalog.en.md`](../../resources/mcp-skills-catalog.en.md) — 81+ entries grouped by category, each with stars / license / audience. The table below is for "writing your own MCP server / finding reference implementations".

| Category | Project | ⭐ | Who it's for | Why recommended / notes |
|---|---|---|---|---|
| **MCP server collection**<br>(CLI-friendly) | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | ⭐⭐⭐⭐⭐ | Starting your first MCP from a reference implementation | Official reference servers (7 today: everything, fetch, filesystem, git, memory, sequentialthinking, time; github and sqlite have moved to `servers-archived`), ★ 89k+. See [Stage 5.2](../../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol--foundation) |
| | [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) | ⭐⭐⭐⭐ | Hunting for a community MCP in a specific domain | Community MCP server catalog, 150+ servers categorized |
| **CI Integration Patterns** | [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) | ⭐⭐⭐⭐⭐ | Starting your first CI workflow from the official template | Official GitHub Action template, PR review / issue triage / auto-fix |
| | [continuedev/continue](https://github.com/continuedev/continue) | ⭐⭐⭐⭐ | Wiring AI checks into the PR pipeline and enforcing them | ★ 35k+. Full intro in [`branches/for-developer.en.md`](../../branches/for-developer.en.md) |
| **Observability + Cost** | [langfuse/langfuse](https://github.com/langfuse/langfuse) | ⭐⭐⭐⭐⭐ | Wanting trace / cost / sessions all in one place | Open-source LLM observability, ★ 32k+. See [Stage 7 Observability](../../stages/07-multi-agent-production.en.md#exercise-3-observability) |
| | [Helicone](https://github.com/Helicone/helicone) | ⭐⭐⭐⭐ | Wanting the fastest logging there is (just change `base_url`) | Proxy-based monitoring, change `base_url` and you get logging + caching, ★ 6k+ |
| | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | ⭐⭐⭐⭐⭐ | Running regression tests before promoting a CLI workflow to production | Eval framework, ★ 24k+. See [Stage 7 Eval](../../stages/07-multi-agent-production.en.md#exercise-2-eval) |
| **Production CLI Workflow Templates** | [obra/superpowers](https://github.com/obra/superpowers) | ⭐⭐⭐⭐ | Seeing what a complete, actually-in-use workflow looks like | Production-ready skill collection, ★ 265k+. See how someone else does a complete CLI workflow |
| | [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) | ⭐⭐⭐ | Packaging your team's CLI workflow for sharing | Minimal marketplace template, ★ 1.2k+ |

> 💡 **Suggested order to pick these up**: start by wiring one reference MCP from `modelcontextprotocol/servers` into your CLI → run your first CI workflow with `claude-code-action` → add langfuse to see traces + cost → when you scale to production, package the workflow as a marketplace plugin.

## ✅ Track A Full Self-Check

Can you:

- [ ] Have at least 1 MCP server connected to your daily CLI
- [ ] Have at least 1 CI workflow auto-running a CLI agent
- [ ] State the rough token / cost / latency for some specific task you run
- [ ] Put at least one Skill in a plugin’s `skills/<name>/SKILL.md` and verify it is found after installation (even just for yourself)
- [ ] Know which tasks deserve observability and which don't

If yes → **Track A complete**. We recommend continuing to [**Stage 8 — Agent Interfaces**](../../stages/08-agent-interfaces.en.md) (**a shared hub for both tracks**: Computer Use / Browser Use / Code Sandbox, ~1-2 weeks from the Track A angle), or pick a [specialized branch](../../README.en.md#-learning-map-two-tracks) and continue (researcher / developer / teacher / knowledge-worker / everyday-users).

If you want to go deeper into "**how to write your own CLI agent**" (not use existing) → jump to [Track B Stage 3](../../stages/03-tool-use-and-hello-agent.en.md). Track A and Track B are complementary.

## 💡 What's Next

After Track A you're a CLI power user. Next phase choices:

1. **Deepen CLI workflow** (keep refining your setup)
   - Subscribe to Anthropic / OpenAI changelogs
   - Quarterly review of [`resources/cli-agents-guide.en.md`](../../resources/cli-agents-guide.en.md) for new tools
   - Share CLAUDE.md / skills with your team

2. **Cross to Track B** (learn to write your own agent)
   - Stage 3-4: tool use + frameworks
   - Stage 5: deep dive into Claude Code internals
   - Stage 7: write your own multi-agent system

3. **Walk a specialized branch** (apply CLI to a specific domain)
   - Researcher / developer / knowledge-worker / teacher / everyday-users
   - Each branch uses what you learned in Track A

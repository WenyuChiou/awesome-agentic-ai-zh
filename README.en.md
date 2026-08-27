<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

<div align="center" markdown="1">

![AI Agent Learning Roadmap](resources/diagrams/banner.en.png)

# awesome-agentic-ai-zh

### 🤖 AI Agent Learning Roadmap — from basic LLM concepts to building your own multi-agent systems

<p><em><b>Learning roadmap + 240+ curated resources + simple illustrative cases</b><br/>A structured 8-stage path, from "what is an LLM, how are tokens counted" to multi-agent orchestration, Computer Use / Browser Use / Sandbox</em></p>

[![License](https://img.shields.io/badge/license-MIT-blue?style=flat)](LICENSE)
[![繁中](https://img.shields.io/badge/lang-繁體中文-red?style=flat)](README.md)
[![简中](https://img.shields.io/badge/lang-简体中文-orange?style=flat)](README.zh-Hans.md)
[![EN](https://img.shields.io/badge/lang-English-blue?style=flat)](README.en.md)
![GitHub stars](https://img.shields.io/github/stars/WenyuChiou/awesome-agentic-ai-zh?style=flat&logo=github)
![GitHub forks](https://img.shields.io/github/forks/WenyuChiou/awesome-agentic-ai-zh?style=flat&logo=github)
[![Docs site](https://img.shields.io/badge/docs-Pages-2ea44f?style=flat)](https://wenyuchiou.github.io/awesome-agentic-ai-zh/)

</div>

> 📱 **On a phone, read the [docs site](https://wenyuchiou.github.io/awesome-agentic-ai-zh/) rather than this page.**

> **Trilingual — the English edition is fully maintained, not a thin machine translation** (only ~0.4% of English lines carry any CJK, almost all intentional bilingual term-mapping). zh-TW is the curation source of truth (new content lands there first); the English and 简中 editions track the same structure, with CI checking localization correctness and anchor integrity across all three.

---

## 🎯 Why this exists

**What this repo is**: **a learning roadmap + 240+ curated resources + simple illustrative cases** — three pillars helping AI / AI-agent learners go from "I don't know where to start" to "I can design multi-agent systems."

Concretely:

| Pillar | What it does | Scale |
|---|---|---|
| **Learning roadmap** | Organizes scattered high-quality projects, tutorials, and required reading into **8 stages** (including Stage 5 + Stage 8 as two shared hubs) + 2 tracks + 5 specialized branches, from zero to advanced | 8 stages, 2 tracks |
| **Resource curation** | Each stage curates **240+** projects (star rating, audience, what they teach, how to run) plus an MCP/Skill catalog covering the Chinese AI ecosystem (DeepSeek, Zhipu, Kimi, …) | 240+ projects, 81 MCP/Skill |
| **Simple illustrative cases** | Each stage ships 1-5 **foundational exercises** (70-150 line starter + dual-path Ollama/Anthropic SDK comparison + mock-based tests) | 23 exercise folders |

After the main path, you go from "**LLM user**" to "**agent system builder**" — capable of designing multi-agent collaboration, writing your own MCP server, and shipping real agent systems.

---

## 📋 Table of Contents

- [🎯 Why this exists](#-why-this-exists)
- [📚 Quick Start](#-quick-start)
  - [Read online](#read-online)
  - [Local clone](#local-clone)
  - [✨ What you get](#-what-you-get)
- [🗺️ Learning Map (Two Tracks)](#-learning-map-two-tracks)
- [💡 How to Learn](#-how-to-learn)
- [📚 Related Resources](#-related-resources)
- [🤝 Contributing](#-contributing)
- [🙏 Acknowledgments](#-acknowledgments)
- [🎓 Citation](#-citation)
- [☕ Support this project](#-support-this-project)
- [License](#license)

---

## 📚 Quick Start

### 🚀 First time with AI agents / never written code before?

Start here: **[`resources/setup-guide.en.md`](resources/setup-guide.en.md)** — 30-45 minutes from zero, walks you through getting an API key, installing Python, and running your first LLM hello-world.

### Read online
- **[Learning Map (Two Tracks)](#-learning-map-two-tracks)** — read this section to decide Track A or Track B
- **[Stage 0 Foundations](stages/00-foundations.en.md)** — already know Python / git / API? Skip straight to Stage 1

### Local clone
```bash
git clone https://github.com/WenyuChiou/awesome-agentic-ai-zh.git
cd awesome-agentic-ai-zh
# Start with stages/00-foundations.en.md
```

### ✨ What you get

- 📖 **Fully free** — MIT-licensed, all content open
- 🗺️ **Two learning tracks** — Track A (CLI Power User) for "use existing CLIs"; Track B (Agent Builder) for "build your own". Shared Stages 0-2 foundation.
- 🛠️ **Foundational hands-on exercises** — 1-5 illustrative exercises per stage (specs + dual-path SDK comparison + success criteria). Positioned as **foundational + roadmap verification** — for chapter-length depth exercises see the hello-agents / Anthropic Cookbook callout in each stage
- 🎯 **240+ curated projects** — each with star rating, audience, what it teaches, how to run (incl. local LLM runners: Ollama, llama.cpp, LocalAI, MLX)
- 🌏 **Trilingual, fully maintained** — zh-TW (canonical) / 简中 / English; the English edition is complete, not a thin mirror
- 🎓 **Beyond frameworks: Claude Code ecosystem** — MCP / Skills / Plugins / SDK full stack
- 🔬 **5 specialized branches** — researcher / developer / teacher / knowledge worker / **everyday user**
- ⏱️ **Time commitment, stated upfront** — Track A 8-10 weeks / Track B 16-22 weeks minimum, 5-7 months realistic (5-8 hr/week part-time)

---

## 🗺 Learning Map (Two Tracks)

![AI Agent Learning Map](resources/diagrams/learning-map.en.png)

After **Stages 0-2 (shared foundations)**, pick a track based on your goal:

- **Track A — CLI Power User**: you want to **USE** existing CLI agents (Claude Code, Codex, OpenCode, Gemini CLI, etc.) to get work done — not build agents from scratch. 3 sub-stages (A1-A3).
- **Track B — Agent Builder**: you want to **BUILD** your own agents — learn frameworks, write ReAct, design multi-agent systems. Stages 3-8 main path.

The two tracks are **not mutually exclusive** — most people start with A to get hands-on, then come back to B for internals (or vice versa). Stage 5 (Claude Code Ecosystem) is used by both tracks.

### Shared Foundations (Stages 0-2)

| Stage | Topic | Key Content | Time |
|---|---|---|---|
| **0** | [Foundations](stages/00-foundations.en.md) | Python · CLI · git · API · JSON | 1-2 wks |
| **1** | [LLM Fundamentals](stages/01-llm-basics.en.md) | tokens · API · model comparison · local LLM | 1 wk |
| **2** | [Prompt Engineering](stages/02-prompt-engineering.en.md) | system prompts · few-shot · CoT | 1-2 wks |

### Track A — CLI Power User (use CLIs to get work done)

| Stage | Topic | Key Content | Time |
|---|---|---|---|
| **A1** | [CLI Agent Intro & Selection](tracks/cli/A1-cli-intro.en.md) | CLI agent selection · install · first run | 1 wk |
| **A2** | [CLI Workflow Patterns](tracks/cli/A2-cli-workflow.en.md) | Project instructions · Skill · task decomposition | 1-2 wks |
| **A3** | [Integration & Production](tracks/cli/A3-cli-production.en.md) | MCP-into-CLI · CI automation · cost / observability | 1-2 wks |
| **+5** | [Stage 5 — Claude Code Ecosystem](stages/05-claude-code-ecosystem.en.md) (**Shared Hub**) | MCP · Skills · Plugins · Subagents; Track A reads 5.1-5.4 (5.5-5.7 optional) | 1-2 wks (Track A view) |
| **+8** | [Stage 8 — Agent Interfaces](stages/08-agent-interfaces.en.md) (**Shared Hub**) | Computer Use · Browser Use · Code Sandbox; Track A reads Track A usage | 1-2 wks (Track A view) |

> **Track A total time**: includes Stages 0-2 (shared foundations) + A1-A3 + **Stage 5 + Stage 8 (two shared hubs) ≈ 8-10 weeks**. Core reference: [`resources/cli-agents-guide.en.md`](resources/cli-agents-guide.en.md).

### Track B — Agent Builder (build agents from scratch)

| Stage | Topic | Key Content | Time |
|---|---|---|---|
| **3** ⭐ | [Tool Use & Hello Agent](stages/03-tool-use-and-hello-agent.en.md) | function calling · ReAct · 6 hands-on exercises | 2-3 wks |
| **4** | [Agent Frameworks](stages/04-agent-frameworks.en.md) | LangGraph · AutoGen · CrewAI · Smolagents | 2-3 wks |
| **5** ⭐⭐ | [Claude Code Ecosystem](stages/05-claude-code-ecosystem.en.md) (**Shared Hub**, Track A also studies) | MCP · Skills · Plugins · Subagents | 3-4 wks (Track B view) |
| **6** | [Context Engineering: RAG and Memory](stages/06-memory-rag.en.md) | vector DB · long-term memory · contextual retrieval | 2 wks |
| **7** | [Multi-Agent · Productionization](stages/07-multi-agent-production.en.md) | multi-agent orchestration · eval · observability · advanced SDK | 2-4 wks |
| **7.5** | [Advanced Agentic Workflow Concepts](stages/07.5-advanced-agentic-concepts.en.md) (reading map) | work boundary · PAR loop · agent-as-judge · 12 advanced concepts + reading list | 1 wk (no code) |
| **8** ⭐⭐ | [Agent Interfaces](stages/08-agent-interfaces.en.md) (**Shared Hub**, Track A also studies) | Computer Use · Browser Use · Code Sandbox; 2024-2026 frontier | 2-3 wks (Track B view) |

> **Track B total time**: minimum **16-22 weeks**, realistic **5-7 months** (5-8 hr/week part-time)

> **Two shared hubs (used by both Track A + Track B)**:
> - **Stage 5** = Claude Code Ecosystem (MCP / Skills / Plugins / Subagents) — Track A learns MCP-into-CLI, Track B learns agent runtime structure
> - **Stage 8** = Agent Interfaces (Computer Use / Browser / Sandbox, 2024-2026 frontier) — Track A learns "how to use" for task delegation, Track B learns "how to build" with embedded interfaces

> 💡 **Want a concrete cross-stage example?** [Build Your First AI Agent in 7 Steps](walkthroughs/build-first-agent-in-7-steps.en.md) — same Paper Summary Bot traced from Stage 1 through Stage 7, ~300 lines of executable code (**Track B**)

After the main path, pick one of 5 specialized branches. **Not sure which?**

![Branch decision tree](resources/diagrams/branch-decision-tree.en.png)

> 💡 **The Everyday User branch can be read directly without walking the main path** — it's for people who want to use AI without writing code.

| Branch | Best for | Topics |
|---|---|---|
| 🔬 [Researcher](branches/for-researcher.en.md) | Grad students, postdocs, PIs | Lit triage · paper writing · multi-agent review |
| 💻 [Developer](branches/for-developer.en.md) | Software engineers | Cursor · Aider · CLI delegation · code review |
| 🎓 [Teacher](branches/for-teacher.en.md) | Teachers, instructors | Lesson planning · slides · student feedback · privacy / ethics · prompt templates |
| 📊 [Knowledge Worker](branches/for-knowledge-worker.en.md) | Consultants, PMs, analysts | Email · meeting notes · report automation |
| 👥 [Everyday User](branches/for-everyday-users.en.md) | ChatGPT / Claude.ai users | Daily writing · learning · privacy · CLI agent intro |

---

## 💡 How to Learn

Welcome — future agent system builder. Some guidance before you start.

This roadmap balances concepts with hands-on work, helping you **transform from an LLM user into an agent system builder**. It assumes **basic Python**. Before starting:

- **Basic Python** — written functions, used APIs, can read JSON
- **Basic git** — clone, commit, push
- **Motivation to learn** — agents are the fastest-changing area in AI 2025+, and require sustained effort

If anything's missing, do Stage 0; if not, **start at Stage 1**.

The main path has 5 parts:

- **Part 1 (Stages 0-2): Foundations & LLM Basics** — Python / git / API, what's an LLM, prompt design
- **Part 2 (Stages 3-4): Build Your Agent** — from tool use to agents, learn the major frameworks
- **Part 3 (Stage 5) Shared Hub** — Claude Code Ecosystem (MCP / Skills / Plugins / Subagents; used by both Track A + B)
- **Part 4 (Stages 6-7): Advanced Integration** — memory / RAG / multi-agent collaboration / harness engineering
- **Part 5 (Stage 8) Shared Hub** — Agent Interfaces (Computer Use / Browser Use / Code Sandbox, 2024-2026 frontier; used by both tracks)

> 🔭 **How the concept layers evolved**: **prompt engineering** (Stage 2 — how to write a single prompt) → **context engineering** (Stage 3 onward — how to dynamically assemble system prompt + memory + retrieved chunks + tool schema) → **harness engineering** (Stage 7 — agent loop / eval / observability / deploy as a complete production system). After 2026, the community extended this outward with two more layers: **loop** (letting the agent run itself to completion) and **graph** (making the execution flow explicit). For the full five-layer model and each layer's purpose, see [Stage 7 five-layer engineering split](stages/07-multi-agent-production.en.md#the-five-layer-engineering-split-prompt--context--harness--loop--graph). See [`stages/02-prompt-engineering.en.md`](stages/02-prompt-engineering.en.md) "Beyond prompts: context engineering" and [`stages/07-multi-agent-production.en.md`](stages/07-multi-agent-production.en.md) Required Reading 5+6.

After the main path (16-22 weeks for Track B, 8-10 weeks for Track A), pick a branch.

The most important advice: **don't skip the hands-on exercises**. Each stage's exercises are "you can't learn this without doing it" — skim past them and you'll get stuck later.

> 🎓 **How to actually use the exercises**: the `starter.py` in each exercise folder is a **complete solution**, not a TODO skeleton. If you clone, `cat starter.py`, and run `python test.py` to all-green, you'll think "I learned it" — but you haven't written a single line. **Correct learning loop**: `mv starter.py starter_reference.py`, look at signatures (not bodies), write your own, peek at the reference only after 20 min stuck. Full method + per-stage time budgets + escalation order in [`docs/HOW_TO_USE.md`](docs/HOW_TO_USE.md).

Ready? [Start at Stage 0](stages/00-foundations.en.md).

---

## 📚 Related Resources

The full related-resources block (term definitions + daily-tool MCP/Skill highlights + awesome lists + Chinese-community resources) lives in **[RESOURCES.en.md](RESOURCES.en.md)** so this README stays focused.

Common quick links, grouped by **scenario**:

### 🚀 Onboarding / Environment

| Your situation | Where | What's there |
|---|---|---|
| Never written code, first time with AI agents | [`resources/setup-guide.en.md`](resources/setup-guide.en.md) | 30-45 min from zero (API key, Python, first hello-world) |
| Not sure which LLM provider to pick | [`resources/setup-guide.en.md` A](resources/setup-guide.en.md#a--get-your-first-api-key-about-10-minutes) | Anthropic / OpenAI / DeepSeek / Kimi / NVIDIA NIM comparison |
| Topic-based awesome lists / Chinese community | [`RESOURCES.en.md` topic-based](RESOURCES.en.md#topic-based-awesome-lists) | 5-10 min skim |

### 📖 Concepts / Terminology

| Your situation | Where | What's there |
|---|---|---|
| Don't know a term (LLM / agent / RAG / token / MCP / Skill / vector DB…) | [`resources/glossary.en.md`](resources/glossary.en.md) | 30+ terms, 30-80 words each + which stage covers it |
| Why some agents live in terminal vs Telegram vs Jetson | [`resources/agent-paradigms.en.md`](resources/agent-paradigms.en.md) | 5 paradigms mental model + Hermes Agent / OpenClaw examples |
| MCP / Skills / Plugins glossary mapping | [`RESOURCES.en.md` three core terms](RESOURCES.en.md#three-core-terms-mcp--skills--plugins) | 1-page lookup |
| Certificate-granting online AI agent courses (EN + ZH) | [`resources/courses.en.md`](resources/courses.en.md) | 10 credible cert-granting courses, tiered; with an honest "completion cert ≠ a degree" caveat |

### 🛠 Hands-on

| Your situation | Where | What's there |
|---|---|---|
| Want to build Skill / MCP server / Word / Zotero / local LLM integration | [`resources/cookbook.en.md`](resources/cookbook.en.md) | 6 step-by-step recipes, 30-50 min each |
| Want to use subagents but do not know who to dispatch, how to dispatch, or what work to dispatch | [`resources/subagent-cookbook.en.md`](resources/subagent-cookbook.en.md) | 15 copy-paste dispatch recipes |
| Write your own subagent / compose several / debug a broken one (advanced) | [`resources/subagent-advanced.en.md`](resources/subagent-advanced.en.md) | 4 description-writing bugs + 3 composition patterns + 5 debug entry points |
| Stuck on tool calling (LLM won't call / schema broken / ReAct won't stop) | [`examples/stage-5/tool-calling-tutor/`](examples/stage-5/tool-calling-tutor/) | Claude Code installable skill, 4-symptom diagnostic |
| How to use the hands-on exercises correctly (active vs passive mode) | [`docs/HOW_TO_USE.md`](docs/HOW_TO_USE.md) | 5-10 min read, applies to every stage |

### 🔌 Daily tool integrations / Finding MCP servers

| Your situation | Where | Scope |
|---|---|---|
| Connect to Notion / Obsidian / Excel / GitHub / etc. | [`RESOURCES.en.md` daily-tool integrations](RESOURCES.en.md#daily-tool-integrations-mcp-servers--skills) | 7-8 highlights |
| Full MCP server / Skill catalog (stars, categories) | [`resources/mcp-skills-catalog.en.md`](resources/mcp-skills-catalog.en.md) | 81+ entries, 16 categories |

### 🔬 Research / Production

| Your situation | Where | What's there |
|---|---|---|
| Research workflow + multi-LLM delegation skill pair | [`RESOURCES.en.md` research workflow](RESOURCES.en.md#research-workflow-by-the-repo-maintainer) | Maintainer's own Claude Code research skill set |
| CLI agent identity & selection guide | [`resources/cli-agents-guide.en.md`](resources/cli-agents-guide.en.md) | Track A's core reference |
| Schema design rules (must-read for tool calling) | [`resources/schema-design-cheatsheet.en.md`](resources/schema-design-cheatsheet.en.md) | 5 golden rules + 5 anti-patterns |

---

## 🤝 Contributing

This repo is an AI learning document — if you've also curated great resources, contributions are very welcome:

- 🐛 **Bug reports** — wrong content, broken links, stale info → open Issue
- 💡 **Suggestions** — missing stage / new project to add → open Issue to discuss
- 📝 **Improvements** — refine existing stage content, fix typos → direct PR
- ✍️ **Add a project** — 1-3 new projects per stage with "why this teaches that stage" rationale
- 🌏 **Translations** — improve the English edition or translate to other languages
- 🌱 **Become a Stage / Branch maintainer** — long-term review of a specific area, see [CONTRIBUTORS.md](CONTRIBUTORS.md)

PR process and style rules: [CONTRIBUTING.en.md](CONTRIBUTING.en.md) + [resources/style-guide.en.md](resources/style-guide.en.md).

> 🤖 **Project links have two automated checks** — on maintainer branches, the comment bot reports stars, license, archive state, and last push for newly added repos; that layer is informational only. A separate read-only freshness gate runs on every PR, including forks, and checks each repo entry touched by the change. It blocks only hard contradictions such as 404/private, an outdated moved slug, calling an archived repo current, or an explicit license mismatch. Six months without a push is only a reminder; maintainers still decide what belongs.

> 📅 **Want to see what shipped recently?** → [`CHANGELOG.md`](CHANGELOG.md) (last 14 days).
> Internal phase rollout progress and launch checklist: [`.github/launch-checklist.md`](.github/launch-checklist.md) (maintainer-facing internal doc).

---

## 💬 Advisory / Contact

A free, open (MIT) learning edition — use it freely.

Currently focused on advisory work: teams or companies needing **prompt review / audit** or **AI agent workflow consulting** are welcome to reach out (PhD student, limited availability): 📧 [wenyuchiou12@gmail.com](mailto:wenyuchiou12@gmail.com)

---

## 🙏 Acknowledgments

### Inspiration

- [**Datawhale Hello-Agents**](https://github.com/datawhalechina/hello-agents) — the most thorough chapter-length agent tutorial in the Chinese-language ecosystem; inspired our chapter + progress structure. Every stage / exercise folder has a 📚 callout pointing to the relevant depth chapter. Special thanks.
- [**Datawhale community**](https://github.com/datawhalechina) — landmark Chinese ML learning community; multiple anchor projects come from them
- [**liyupi/ai-guide**](https://github.com/liyupi/ai-guide) — largest Chinese-language "AI mega-guide" + Vibe Coding tutorial (covers Agent Skills / RAG / MCP / A2A / Harness Engineering). This repo is a "structured roadmap"; ai-guide is a "breadth resource hub" — complementary

### Related projects

Other lists in the same space — useful to browse alongside this repo when hunting for specific tools:

- [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) — categorized MCP server catalog
- [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) — another MCP server catalog
- [`hesreallyhim/awesome-claude-code`](https://github.com/hesreallyhim/awesome-claude-code) — Claude Code tools & plugins list

These are pure catalogs (browse and pick). This repo is different in that it has a **learning order from Stage 0 all the way to production**.

### Contributors

[![Contributors](https://contrib.rocks/image?repo=WenyuChiou/awesome-agentic-ai-zh)](https://github.com/WenyuChiou/awesome-agentic-ai-zh/graphs/contributors)

New contributors appear above automatically. Full list → [GitHub Contributors](https://github.com/WenyuChiou/awesome-agentic-ai-zh/graphs/contributors).

### Personal

- [@WenyuChiou](https://github.com/WenyuChiou) — Maintainer

---

## 🎓 Citation

If this learning roadmap helps your study or work, please cite:

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

## ☕ Support this project

This learning map is free and open-source (MIT). If it helps you, a ⭐ Star means a lot — and if you'd like to support ongoing updates, you can buy the author a coffee:

<a href="https://www.buymeacoffee.com/wenyuchiou" target="_blank" rel="noopener noreferrer"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="44"></a>

Or use the **❤ Sponsor** button at the top of the repo. (GitHub Sponsors is under review and will be added once approved.)

---

## License

MIT. Maintained by [@WenyuChiou](https://github.com/WenyuChiou).

<div align="center">
  <p>⭐ If this repo helps you, please give it a Star — it matters for ongoing iteration</p>
</div>

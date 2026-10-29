<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

<div align="center" markdown="1">

![Stages 0–2 split into CLI and Agent paths, sharing Stages 5 and 8; choose role paths as needed](resources/diagrams/banner.en.svg)

# awesome-agentic-ai-zh

**🤖 One map from “what is an AI agent?” to “I can build a reliable system.”**

**Pick a route, then walk it one step at a time. Concepts, exercises, and resources are already in order.**

[![License](https://img.shields.io/badge/license-MIT-blue?style=flat)](LICENSE)
[![zh-TW](https://img.shields.io/badge/語言-繁體中文-red?style=flat)](README.md)
[![zh-Hans](https://img.shields.io/badge/語言-简体中文-orange?style=flat)](README.zh-Hans.md)
[![EN](https://img.shields.io/badge/lang-English-blue?style=flat)](README.en.md)
![GitHub stars](https://img.shields.io/github/stars/WenyuChiou/awesome-agentic-ai-zh?style=flat&logo=github)
[![Docs site](https://img.shields.io/badge/線上閱讀-立即開始-2ea44f?style=flat)](https://wenyuchiou.github.io/awesome-agentic-ai-zh/)

[![Star History global rank](https://api.star-history.com/badge?repo=WenyuChiou/awesome-agentic-ai-zh&type=rank)](https://www.star-history.com/wenyuchiou/awesome-agentic-ai-zh)

</div>

> 📱 On a phone, read the [docs site](https://wenyuchiou.github.io/awesome-agentic-ai-zh/).

## 🎯 What does this map help you do?

An **AI Agent** is an AI system that can decide what to do next and take action toward a person's goal. It reads the situation, chooses the next step, and uses tools when needed; based on the result, it continues, corrects course, stops, or hands control back. It can do work automatically, but only within a person's rules and permissions. A one-shot chatbot or fixed script is not necessarily an Agent. The map covers three things in order:

1. **Get the basics**: what an LLM (Large Language Model, reads and writes language), a prompt, an API (Application Programming Interface, programs request a service), and a token are.
2. **Then build something**: let a model call tools, run an agent loop, read documents, remember things.
3. **Then make it reliable**: add permissions, Eval, human approval, observability, and failure recovery.

This repo is **a learning roadmap + curated resources + small runnable examples**. For chapter-length depth we point to the official docs, [Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents), or a cookbook rather than rewriting an encyclopedia. When a model connection is needed, each exercise explains the cloud or local path.

Chapters explain important terms in plain language at first use. Forgot one? See the [glossary](resources/glossary.en.md).

## 🚀 Start now

1. **Never written code**: start at [Stage 0: Foundations](stages/00-foundations.en.md). If APIs or CLI Agents are new, use the [zero-to-setup guide](resources/setup-guide.en.md) beside it.
2. **Already know Python, Git, and APIs**: start at [Stage 1: LLM fundamentals](stages/01-llm-basics.en.md).
3. **Not sure which route fits**: read the Track A / Track B table below.

Before Track A or Track B, check Stage 0–2. If you only want everyday AI use, go straight to the role guide.

<div class="reader-route-table" role="region" tabindex="0" aria-label="Choose a route by need">
<table align="center">
<thead><tr><th scope="col">What do you want to do?</th><th scope="col">Route</th><th scope="col">Route entrance</th></tr></thead>
<tbody>
<tr><td>Get work done with a CLI agent — Claude Code, Codex, OpenCode</td><td><strong>Track A — CLI Power User</strong></td><td><a href="tracks/cli/A1-cli-intro.en.md">A1: Pick a CLI agent</a></td></tr>
<tr><td>Write your own agent, tool loop, workflow, and service</td><td><strong>Track B — Agent Builder</strong></td><td><a href="stages/03-tool-use-and-hello-agent.en.md">Stage 3: First agent loop</a></td></tr>
<tr><td>Use AI safely in daily life, no coding for now</td><td><strong>Everyday user route</strong></td><td><a href="branches/for-everyday-users.en.md">Everyday user guide</a></td></tr>
</tbody>
</table>
</div>

<details markdown="1">
<summary>💻 Expand: clone it to your machine</summary>

```powershell
git clone https://github.com/WenyuChiou/awesome-agentic-ai-zh.git
cd awesome-agentic-ai-zh
```

Then open `stages/00-foundations.en.md`, or jump to your first stop above.

</details>

## Stage 0 through Stage 8, plus the Stage 7.5 reading stop

![AI Agent learning map](resources/diagrams/learning-map.en.png)

The map has **8 topic stages + the Stage 0 readiness check + the Stage 7.5 advanced reading stop**: **10 learning stops** in total. Track A / B readers first check the **shared Stage 0–2 foundations**; skip Stage 0 if you already know Python, Git, and APIs. Everyday users can go straight to the role guide.

### Shared foundations: Stages 0–2

<div class="reader-route-table" role="region" tabindex="0" aria-label="Shared foundations route comparison">
<table align="center">
<thead><tr><th scope="col" width="260">Stage</th><th scope="col">What it settles</th><th scope="col">What you can do after</th></tr></thead>
<tbody>
<tr><td><strong>0</strong> · <a href="stages/00-foundations.en.md">Foundations</a></td><td>Machine and tools ready?</td><td>Call a public API in Python, read JSON (JavaScript Object Notation, a text data-exchange format), save with Git</td></tr>
<tr><td><strong>1</strong> · <a href="stages/01-llm-basics.en.md">LLM fundamentals</a></td><td>What are LLM, token, context; how do models differ?</td><td>Call an LLM and pick a cloud or local model</td></tr>
<tr><td><strong>2</strong> · <a href="stages/02-prompt-engineering.en.md">Prompt design</a></td><td>How to state goal, data, rules, output clearly?</td><td>Compare Zero-Shot, One-Shot, Few-Shot, and the boundary of CoT (Chain-of-Thought, reason through intermediate steps)</td></tr>
</tbody>
</table>
</div>

### Track A: get work done with a CLI agent

The intended order is `A1 → A2 → Stage 5 → A3 → Stage 8`.

<div class="reader-route-table" role="region" tabindex="0" aria-label="Track A route comparison">
<table align="center">
<thead><tr><th scope="col" width="260">Order</th><th scope="col">What it settles</th><th scope="col">What you can do after</th></tr></thead>
<tbody>
<tr><td><strong>A1</strong> · <a href="tracks/cli/A1-cli-intro.en.md">Pick a CLI agent</a></td><td>What are OpenRouter, OpenCode, Pi, Ollama?</td><td>Pick a tool and finish one small task</td></tr>
<tr><td><strong>A2</strong> · <a href="tracks/cli/A2-cli-workflow.en.md">Build a repeatable process</a></td><td>How to keep rules and steps for next time?</td><td>Write project instructions, a Skill, a reusable workflow</td></tr>
<tr><td><strong>5</strong> · <a href="stages/05-claude-code-ecosystem.en.md">Claude Code ecosystem</a></td><td>How do MCP, Skills, Plugins, Hooks, Subagents differ?</td><td>Read core 5.1–5.4; choose 5.5–5.8 only when your work needs them</td></tr>
<tr><td><strong>A3</strong> · <a href="tracks/cli/A3-cli-production.en.md">Plug into real work</a></td><td>How to safely connect tools, CI, and team process?</td><td>Integrate with least privilege, human checks, a record</td></tr>
<tr><td><strong>8</strong> · <a href="stages/08-agent-interfaces.en.md">Agent interfaces</a></td><td>How does an agent drive a browser, screen, sandbox?</td><td>Decide if a task needs CLI, browser, Computer Use, or API</td></tr>
</tbody>
</table>
</div>

### Track B: build an agent from scratch

<div class="reader-route-table" role="region" tabindex="0" aria-label="Track B route comparison">
<table align="center">
<thead><tr><th scope="col">Order</th><th scope="col">What it settles</th><th scope="col">What you can do after</th></tr></thead>
<tbody>
<tr><td><strong>3</strong> · <a href="stages/03-tool-use-and-hello-agent.en.md">Tool Use &amp; Your First Agent Loop</a></td><td>How does a model call tools safely and continue?</td><td>Build an agent loop with a turn limit and validated arguments</td></tr>
<tr><td><strong>4</strong> · <a href="stages/04-agent-frameworks.en.md">Workflow Graphs &amp; Agent Frameworks</a></td><td>How to draw several steps as one map?</td><td>Choose between workflow, agent, graph, framework</td></tr>
<tr><td><strong>5</strong> · <a href="stages/05-claude-code-ecosystem.en.md">Claude Code ecosystem</a></td><td>How do MCP, Skills, Plugins, Hooks, Subagents work together?</td><td>Combine tools, rules, reusable capabilities</td></tr>
<tr><td><strong>6</strong> · <a href="stages/06-memory-rag.en.md">Memory · RAG (Retrieval-Augmented Generation, retrieve information before answering)</a></td><td>How does an agent search, save, and get back what matters?</td><td>Build a minimal RAG, long-term memory, and contextual retrieval flow</td></tr>
<tr><td><strong>7</strong> · <a href="stages/07-multi-agent-production.en.md">Agent Production Engineering: Testable, Observable, Stoppable, and Recoverable</a></td><td>How does an agent stay stable in production?</td><td>Add Eval, observability, budget, Human-in-the-loop approval, recovery</td></tr>
<tr><td><strong>7.5</strong> · <a href="stages/07.5-advanced-agentic-concepts.en.md">Advanced agentic concept map</a></td><td>Which advanced patterns are worth knowing?</td><td>Pick what you need from 12 concepts such as PAR loop and agent-as-judge</td></tr>
<tr><td><strong>8</strong> · <a href="stages/08-agent-interfaces.en.md">Agent interfaces</a></td><td>How does an agent work beyond the API?</td><td>Choose Computer Use, Browser Use, or a code sandbox</td></tr>
</tbody>
</table>
</div>

Stage 4 first explains the **Workflow Graph**, then uses a framework to build it. Stage 7 adds Eval, observability, approval, and recovery so the same work map can run reliably.

> 🔭 **Learning order**: Stage 2 Prompt → Stage 3 **Agent Loop** → Stage 4 **Workflow Graph** / framework → Stage 5 tools and rules → Stage 6 **Context Engineering** → Stage 7 production. Prompt, Context, Harness, Loop, and Graph work together; they are not five layers or product generations that replace one another.

After A3 or Stage 7, start the [Capstone project](CAPSTONE.en.md); track your progress in [PROGRESS.en.md](PROGRESS.en.md).

<details markdown="1">
<summary>⏱️ View time estimates (planning aid, not a deadline)</summary>

- **Track A**: about 8–10 weeks, using an existing CLI agent to get work done.
- **Track B**: main path about 16–22 weeks; at 5–8 hours a week, usually 5–7 months.
- **Stage 5** is the tools-and-rules hub: Track A uses them, Track B combines them.
- **Stage 8** is the interface hub: Track A delegates, Track B builds them in.

The timeline is a planning aid. Finish the step in front of you; no need to read the whole map at once.

</details>

### Keep going by who you are

![Research, development, teaching, knowledge work, and everyday use are five options; choose what you need, not every path](resources/diagrams/branch-decision-tree.en.svg)

<div class="reader-route-table" role="region" tabindex="0" aria-label="Choose a route by role">
<table align="center">
<thead><tr><th scope="col">Route</th><th scope="col">Who it fits</th><th scope="col">What you will handle</th></tr></thead>
<tbody>
<tr><td>🔬 <a href="branches/for-researcher.en.md">Researcher</a></td><td>Grad students, postdocs, PIs</td><td>Literature evidence, reproducible pipelines, multi-agent review</td></tr>
<tr><td>💻 <a href="branches/for-developer.en.md">Developer</a></td><td>Software engineers</td><td>CLI delegation, code review, tests and rollback</td></tr>
<tr><td>🎓 <a href="branches/for-teacher.en.md">Teacher</a></td><td>Teachers, instructors</td><td>Lesson prep, feedback, privacy, teaching prompts</td></tr>
<tr><td>📊 <a href="branches/for-knowledge-worker.en.md">Knowledge worker</a></td><td>Consultants, PMs, analysts</td><td>Email, meeting, reporting workflows</td></tr>
<tr><td>👥 <a href="branches/for-everyday-users.en.md">Everyday user</a></td><td>AI users who may not code</td><td>Writing, learning, privacy, safe use</td></tr>
</tbody>
</table>
</div>

## 💡 How do you learn without getting stuck?

1. **One Stage at a time**: answer that chapter's core question first.
2. **Read the core terms and required reading first**: the exercises use them directly.
3. **Copy the first command as-is**: run the offline test first, don't retype a blank file.
4. **Change one thing at a time**: rerun the test right after, so you know what caused the result.
5. **Meet the completion check before moving on**: understanding is not the same as doing.

## 📚 Learning entrances to bookmark

<details markdown="1">
<summary>Extra resources</summary>

Only the most-used entrances are here; the full list is in [RESOURCES.en.md](RESOURCES.en.md). Stars mean **learning priority**, not a ranking.

<div class="reader-reference-table" role="region" tabindex="0" aria-label="Learning resource comparison">
<table align="center">
  <thead><tr><th>Purpose</th><th>Entrance</th><th>When to use it</th><th>Priority</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3" align="center" valign="middle">Start</th><td><a href="resources/setup-guide.en.md">Zero-to-setup guide</a></td><td>First install and first run</td><td align="center" valign="middle">⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="docs/HOW_TO_USE.md">How to use this material</a></td><td>Before your first hands-on exercise</td><td align="center" valign="middle">⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="PROGRESS.en.md">Progress tracker</a></td><td>Want the next step, or to log what you finished</td><td align="center" valign="middle">⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3" align="center" valign="middle">Learn</th><td><a href="resources/glossary.en.md">Core glossary</a></td><td>You hit an unfamiliar word: token, RAG, MCP</td><td align="center" valign="middle">⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="examples/README.en.md">Runnable examples</a></td><td>Want to run offline tests and small cases</td><td align="center" valign="middle">⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="resources/cookbook.en.md">Hands-on cookbook</a></td><td>Building a Skill, MCP, Office, Zotero, or local LLM</td><td align="center" valign="middle">⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4" align="center" valign="middle">Look it up</th><td><a href="resources/README.en.md">Resource toolbox</a></td><td>Not sure if you need a guide, catalog, or cookbook</td><td align="center" valign="middle">⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="RESOURCES.en.md">Full resource list</a></td><td>Official docs, courses, communities, further reading</td><td align="center" valign="middle">⭐⭐⭐⭐</td></tr>
    <tr><td><a href="resources/cli-agents-guide.en.md">CLI agent selection guide</a></td><td>Starting Track A, or comparing CLI tools</td><td align="center" valign="middle">⭐⭐⭐⭐</td></tr>
    <tr><td><a href="resources/courses.en.md">Course and certification map</a></td><td>Separates completion certificates, skill badges, and certification exams</td><td align="center" valign="middle">⭐⭐⭐⭐</td></tr>
  </tbody>
</table>
</div>

</details>

## 🤝 Help improve this map

- Wrong content, broken links, or stale information: open an [Issue](https://github.com/WenyuChiou/awesome-agentic-ai-zh/issues).
- Adding a project or learning resource: say which Stage it teaches, and what.
- Sending a PR: read [CONTRIBUTING.en.md](CONTRIBUTING.en.md) and the [style guide](resources/style-guide.en.md) first.
- Recent changes: see [CHANGELOG.md](CHANGELOG.md).

<details markdown="1">
<summary>🧰 Expand: all the ways to contribute, and the automated checks</summary>

You can fix wording, fill in a missing trilingual mirror, report a missing topic, or maintain a Stage or role route long term. For a new GitHub project link, the automated check shows archive status, license, and last update; inclusion stays a maintainer call based on learning value.

Full roles and rules are in [CONTRIBUTORS.md](CONTRIBUTORS.md).

</details>

## 🙏 Key inspirations and related projects

- [**Datawhale Hello-Agents**](https://github.com/datawhalechina/hello-agents) — for readers who want full chapters and deep hands-on work.
- [**Datawhale community**](https://github.com/datawhalechina) — a Chinese-language machine learning study community with many reliable entrances.
- [**liyupi/ai-guide**](https://github.com/liyupi/ai-guide) — a breadth-first resource hub; this repo handles the learning order instead.

<details markdown="1">
<summary>📖 Expand: contributors and citation format</summary>

[![Contributors](https://contrib.rocks/image?repo=WenyuChiou/awesome-agentic-ai-zh)](https://github.com/WenyuChiou/awesome-agentic-ai-zh/graphs/contributors)

```bibtex
@misc{awesome_agentic_ai_zh_2026,
  title = {awesome-agentic-ai-zh: A Structured Learning Roadmap for Agentic AI},
  author = {Chiou, Wenyu},
  year = {2026},
  url = {https://github.com/WenyuChiou/awesome-agentic-ai-zh}
}
```

</details>

## ☕ Support and contact

This learning map is MIT-licensed and stays free and public. Use an Issue for questions; for private contact, email [wenyuchiou12@gmail.com](mailto:wenyuchiou12@gmail.com).

If this map helped you, a ⭐ Star is welcome, or [buy the author a coffee](https://www.buymeacoffee.com/wenyuchiou).

[![Greptile: The War on Bugs](https://www.greptile.com/badge.svg)](https://www.greptile.com/?utm_source=oss_badge&utm_medium=readme&utm_campaign=greptile_for_open_source)

## ⭐ Star History

[![GitHub star history for this project](https://api.star-history.com/svg?repos=WenyuChiou/awesome-agentic-ai-zh&type=Date)](https://www.star-history.com/#WenyuChiou/awesome-agentic-ai-zh&Date)

## License

MIT. Maintained by [@WenyuChiou](https://github.com/WenyuChiou).

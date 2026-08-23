# A1 — CLI Agent Intro & Selection

> [繁體中文](./A1-cli-intro.md) | [简体中文](./A1-cli-intro.zh-Hans.md) | **English**

> [← Back to main path README](../../README.en.md) · **Track A: CLI Power User** — Stop 1

⏱ **Time estimate**: 1 week (~5-10 hours)

> 📋 **Chapter structure**: Learning goals → Entry conditions → Required reading → Hands-on exercises → Curated Projects → Self-check
> 🔑 **Key term**: this page only uses **CLI agent** (an AI tool that runs in the terminal). MCP / Skill / plugin and other ecosystem terms are introduced where they first appear in A2 / A3. Full glossary: [`resources/glossary.en.md`](../../resources/glossary.en.md).

After Stages 0-2, you want to use existing CLI agents to get real work done — **not write agent code yourself, just use existing tools to complete tasks first**. This track is for you. First stop: **pick a CLI agent and get it running**.

## 📌 Learning Goals

- Know the differences between 8 mainstream CLI agents (Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent / Grok Build)
- Pick a first CLI tool based on your scenario
- Complete install + auth + your first real task (not a hello world)
- Know when to switch / add a second CLI

## 🚪 Entry Conditions

You should already:

- Have completed Stage 0's Exercise: CLI (basic command-line literacy)
- Have a Claude / OpenAI / Google account (paid not required)
- Be comfortable with prompt design (Stage 2)

## 📚 Required Reading

1. [**`resources/agent-paradigms.en.md`**](../../resources/agent-paradigms.en.md) ⭐ — the 5-paradigm map of the agent landscape; read this first to see where CLI agents sit (Type 2 + Type 3) in the wider ecosystem
2. [**`resources/cli-agents-guide.en.md`**](../../resources/cli-agents-guide.en.md) ⭐ — the core reference for this track. 8 mainstream CLI agents side by side, use-case picks, real-world setups
3. [**Anthropic — Claude Code Quickstart**](https://code.claude.com/docs/en/quickstart) — official install
4. [**OpenAI — Codex Quickstart**](https://github.com/openai/codex/blob/main/README.md) — Codex install + auth

## 🛠 Hands-on Exercises (foundational, illustrative)

### Exercise CLI-1: Install + first run

**Finish it in 3 steps**:

1. **Install**: follow your chosen CLI's quickstart (each CLI's official docs should have a ≤5-minute install guide)
2. **Pick a low-risk real task**: don't write "hello world" — choose something you were already going to do today, e.g. "organize my Downloads folder and move all PDFs to ~/Documents/PDFs"
3. **Observe 3 things**: how it decomposes the task, when it asks for confirmation, and what output format it uses

→ Real tasks are what make the difference between an agent and a chatbot visible.

### Exercise CLI-2: CLI's built-in system prompt file
- Claude Code → write a `CLAUDE.md` at the repo root
- Codex → write `AGENTS.md`
- Gemini CLI → write `GEMINI.md`
- goose / OpenCode → see each tool's docs

Put 3 things in it: "your persona / preferred code style / things you can't do". Then run a task and observe behavioral differences.

### Exercise CLI-3: Run a second CLI alongside
Install a second CLI (suggest Codex or OpenCode as backup). Run the same prompt and compare output style, speed, cost. **Not to pick a winner — to learn that "different CLIs solve the same problem from different angles".**

### Exercise CLI-4: Auth corner cases
Deliberately break your API key (one wrong character) and see how the CLI errors out. Then "correct key but wrong model name". Production usage will hit auth issues — step on these now.

## 🎯 Curated Projects

Two categories, 10 projects, one table covers it. **Pick your entry point from the "Who it's for" column; for the deeper detail (strengths and weaknesses, recommended use cases, real-world pairings) → [`resources/cli-agents-guide.en.md`](../../resources/cli-agents-guide.en.md)**.

| Category | Project | ⭐ | Who it's for | Why recommended / notes |
|---|---|---|---|---|
| **8 mainstream CLI agents** | [anthropics/claude-code](https://github.com/anthropics/claude-code) | ⭐⭐⭐⭐⭐ | **Recommended as your first CLI agent** | Built-in SKILL / plugin ecosystem, CLAUDE.md prompt system, rich community resources (★ 140k+) |
| | [openai/codex](https://github.com/openai/codex) | ⭐⭐⭐⭐⭐ | People already subscribed to ChatGPT Plus / Pro | The same account works in the terminal (★ 105k+) |
| | [sst/opencode](https://github.com/sst/opencode) | ⭐⭐⭐⭐⭐ | Self-hosting / avoiding vendor lock-in | Open-source, not tied to any LLM provider, fastest community iteration (★ 190k+) |
| | [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | ⭐⭐⭐⭐ | Working on big codebases / large PDFs | 1M-token long context (★ 103k+) |
| | [block/goose](https://github.com/block/goose) | ⭐⭐⭐⭐ | Using existing Claude / ChatGPT / Gemini subscriptions + local Ollama | 15+ provider support (incl. Ollama), ★ 51k+. **Now at `aaif-goose/goose` (AAIF / Linux Foundation)** |
| | [Aider-AI/aider](https://github.com/Aider-AI/aider) | ⭐⭐⭐⭐⭐ | Writing code and wanting a clean git workflow | git-native, auto commit / branch (★ 47k+) |
| | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | ⭐⭐⭐⭐⭐ | Wanting a cloud-deployed agent (Telegram / Discord / Slack front-end) + Chinese-ecosystem LLMs | Nous Research's auto-evolving agent, 200+ provider routing incl. GLM / Kimi / Xiaomi MiMo / MiniMax, built-in cron scheduler + skill self-evolution loop (★ data as of 2026-05; check the official GitHub for current numbers). ⚠️ Auto-evolving skills are experimental and lack third-party independent audits — verify safety and maintenance status yourself before production use, and start in low-risk contexts |
| | [xai-org/grok-build](https://github.com/xai-org/grok-build) | ⭐⭐⭐ | Already in the Grok / X ecosystem, happy to try something new | SpaceXAI's (xAI) official TUI coding agent, Rust, headless mode / ACP editor embedding (★ 25k+). ⚠️ Open-sourced 2026-07-14, very new — watch it first; not recommended as your first CLI agent |
| **Advanced: complementary tools**<br>(not CLIs, but common pairings) | [LM Studio](https://lmstudio.ai/) | ⭐⭐⭐ | On Windows / Mac, don't want to learn the command line, want to run a local LLM | Closed-source desktop app, drag-and-drop UI for running local LLMs |
| | [Ollama](https://github.com/ollama/ollama) | ⭐⭐⭐⭐⭐ | Wanting a local LLM for your CLI agent to use | Local LLM runner, pairs with OpenCode / goose, or any tool taking an OpenAI-compatible base_url (★ 170k+). See [Stage 1 — Local LLM section](../../stages/01-llm-basics.en.md) |

> 💡 **Suggested way in**: pick Claude Code as your first CLI (most complete ecosystem) → install a second one (Codex / OpenCode) to feel the difference in style → add Ollama when you want to run locally → use Hermes Agent when you want a cloud-deployed, cross-platform setup.

## ✅ Self-Check Before A2

Can you:

- [ ] Articulate the core differences between the 8 mainstream CLIs (3-4 without checking the table)
- [ ] Have a working primary CLI (installed, authed, ran 5+ real tasks)
- [ ] Written your own `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`
- [ ] Run a second CLI at least once, know the style differences

If yes → proceed to [A2 — CLI Workflow Patterns](A2-cli-workflow.en.md).

If no → don't skip. Sloppy CLI usage isn't productive CLI usage; do Exercises CLI-1/2 at least 3 more times.

## 💡 Reminder for Track A learners

A CLI agent is not "the same thing with a different UI" as Claude.ai / ChatGPT web — it can read/write files on your machine, run shell commands, modify git. This capability difference deserves caution **before use**:

- Week 1: review the plan before letting it execute (or use `--dry-run`)
- Don't let CLI commit directly to production codebases yet
- Put sensitive data (keys, contracts, medical records) in `.cursorignore` / `.claudeignore` to exclude

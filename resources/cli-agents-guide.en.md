> [繁體中文](./cli-agents-guide.md) | [简体中文](./cli-agents-guide.zh-Hans.md) | **English**

# CLI Agents Comparison Guide

> [← Back to main path README](../README.en.md)

> 📌 **This is a reference doc** (depth comparison, selection logic, pitfalls, recommended setups).
> First time touching CLI agents, want step-by-step onboarding → see [`tracks/cli/A1-cli-intro.en.md`](../tracks/cli/A1-cli-intro.en.md) (Track A first stop).
> First want to understand "why does one agent live in a terminal, another in Telegram, another on a Jetson board?" mental model → see [`resources/agent-paradigms.en.md`](agent-paradigms.en.md) (5 agent paradigms).
> Already using one, want to decide / compare / upgrade → stay here.

A cross-branch reference shared by Track A (A1-A3) + all 5 specialized branches: **how to choose between Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent / Grok Build?** Every branch references CLI agents but no single branch "owns" this comparison, so it lives in `resources/`.

---

## 📋 8 Major Terminal CLI Agents

Only terminal-based CLI agents are included. IDE-based agents (Cursor / Cline / Continue) live in [for-developer](../branches/for-developer.en.md). The first 6 numbers verified via `gh api` on 2026-05-06; Hermes Agent verified on 2026-05-10; Grok Build verified on 2026-07-16 (⚠️ open-sourced 2026-07-14, very new; numbers and features are still moving fast).

| Tool | Provider | License | Primary LLM | Auth / Pricing | Stars |
|---|---|---|---|---|---|
| [Claude Code](https://github.com/anthropics/claude-code) | Anthropic (official) | NOASSERTION | Claude | Claude subscription **OR** Anthropic Console API key | ★ 140k+ |
| [Codex](https://github.com/openai/codex) | OpenAI (official) | Apache-2.0 | GPT family | ChatGPT account sign-in **OR** OpenAI API key | ★ 115k+ |
| [OpenCode](https://github.com/sst/opencode) | community (repo now at `anomalyco/opencode`) | MIT | Any (multi-provider) | BYO API key, or built-in OpenCode Zen hosted | ★ 190k+ |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Google (official) | Apache-2.0 | Gemini | Generous free tier, paid above quota | ★ 103k+ |
| [goose](https://github.com/block/goose) | Agentic AI Foundation (repo now at `aaif-goose/goose`) | Apache-2.0 | 15+ providers (incl. Ollama) | BYO API key, or existing Claude / ChatGPT / Gemini subscription via ACP | ★ 51k+ |
| [Aider](https://github.com/Aider-AI/aider) | Aider-AI (community) | Apache-2.0 | Any | BYO API key | ★ 47k+ |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Nous Research | MIT | 200+ via OpenRouter / NVIDIA NIM / Zhipu GLM / Kimi / Xiaomi MiMo / MiniMax / HF / OpenAI | BYO API key (multi-provider) | ★ 224k+ |
| [Grok Build](https://github.com/xai-org/grok-build) | SpaceXAI (xAI, official) | Apache-2.0 | Grok | Browser sign-in on first launch | ★ 25k+ |

---

## 🎯 Which to Pick? Decide by Use Case

### Writing papers / literature / research
**Top pick**: Claude Code (long context, strong reasoning, good hallucination resistance). Gemini CLI is the alternative — its million-token context fits whole-PDF / whole-dataset workflows.

### Writing code / refactoring a codebase
**Top pick**: Aider (git-native — auto-commits each change, easy to revert) or Claude Code. OpenCode fits when you need to switch between LLMs.

### Privacy / offline / no cloud
**Top pick**: goose or OpenCode + local Ollama. Both support BYO LLM and connect to `http://localhost:11434/v1` (Ollama default).

### Already subscribed to ChatGPT Plus / Pro
**Top pick**: Codex — same account, no separate billing.

### Want 1M-token long context + Google ecosystem
**Top pick**: Gemini CLI. Generous free tier and long context are the differentiators. Note: Google service integration (Gmail / Drive / Docs) goes through MCP extensions, not built-in connectors — same setup pattern as other CLIs.

### Want to avoid vendor lock-in
**Top pick**: OpenCode > goose > Aider. None tie you to a specific provider; models are swappable.

### First time installing a CLI agent — wanting easiest start
**Top pick**: Claude Code. Broad ecosystem, CLAUDE.md mechanism for version-controlled prompts, plenty of community resources when you hit issues.

### Want it running on a cloud VM, talking to it via Telegram / Slack / Discord, with mainland China LLMs as primary
**Top pick**: Hermes Agent. Three differentiators:

- **Decoupled from your laptop** — agent runs on a $5 VPS / Modal serverless / Vercel Sandbox; you message it from Telegram / Discord / Slack / WhatsApp / Signal
- **Model-neutral** — supports GLM / Kimi / Xiaomi MiMo / MiniMax, matching the 11 Chinese-ecosystem catalog entries
- **Built-in self-improving skill loop + cron scheduler** — agent autonomously generates skills from interaction, refines them across sessions, runs scheduled jobs unattended
- ⚠️ Self-evolving skills is a frontier feature with no independent audit yet; for production tasks, start with low-stakes experiments

---

## 📝 Portable Prompts Across CLIs

If you want prompts that work across CLI tools (or want to switch without rewriting), follow these principles:

1. **Specify file paths explicitly** — "modify `src/auth.py`" beats "modify that auth file"
2. **Ask for multi-step breakdowns** — "first list a plan, then act after I confirm" works in every CLI
3. **Avoid CLI-specific magic** — `/init` `/compact` are Claude-Code-specific; OpenCode doesn't have them
4. **Use `.cursorrules` / `CLAUDE.md` / `AGENTS.md` for persistent preferences** — Claude Code reads `CLAUDE.md`, Codex reads `AGENTS.md`, OpenCode reads `OPENCODE.md`, **content can be the same**
5. **State review scope clearly** — "review only my diff" vs "review the whole repo"

Cross-CLI prompts are usually 5-10% more verbose than CLI-specific ones, but the upside is you can switch tools without rewriting.

---

## ⚠️ Common Pitfalls

### File path handling
- Windows uses backslashes (`C:\Users\...`); most CLIs translate internally but sometimes get confused
- Recommendation: in git-bash / WSL use forward slashes, avoid weird quoting

### Git integration differences
- **Aider** auto-commits every change (by design, not a bug)
- **Claude Code / Codex / OpenCode / goose** don't auto-commit by default — manual or via prompt

### Default sandbox (each CLI varies; verify against official docs before use)
- **Claude Code**: bash writes default to cwd; reads broader (except deny-rule paths)
- **Codex**: in version-controlled folders, `Auto` (workspace-write + on-request escalation) is recommended; in non-git folders, `read-only`
- **goose / OpenCode**: relatively permissive — add explicit sandbox / approval rules; don't rely on defaults

### Token cost accumulation
- Running a `grep` on a large codebase can consume 100k+ tokens
- Summarizing a long PDF can hit 500k tokens (Gemini handles this; other tools need to be cost-aware)
- Recommendation: estimate cost before each operation; set a monthly cap

### Multi-CLI session interference
- Two CLIs in the same repo (e.g. Claude Code + Aider) can race-condition file edits
- Recommendation: one repo, one CLI (unless you genuinely need parallelism)

---

## 🔧 Real-World Setups

Three common combinations; pick one that fits:

### Setup A: Claude Code primary + OpenCode backup
- Claude Code handles 90% of daily work (code, docs, debug)
- OpenCode + Ollama for privacy-sensitive data (medical, financial)
- One prompt, runs in either

### Setup B: Codex (GPT) + Aider (Claude) mix
- Codex handles small tasks within ChatGPT Plus quota
- Aider with Claude API key handles big refactors (git-native commit convenient)
- Separate billing, no interference

### Setup C: Gemini CLI primary (long-context scenarios)
- Whole PDF / whole codebase fed at once
- Add Aider for scenarios needing precise git diff
- Fits scholars, knowledge workers

### Setup D: Hermes Agent + Local Ollama (multi-platform + mainland China LLMs + offline)
- **Hermes Agent** runs on a low-cost VPS or your own machine as a multi-platform agent gateway
- **LLM endpoint** can be Ollama (`http://localhost:11434/v1`), or swapped to providers such as z.ai GLM / Kimi
- **Chat entrypoint** can be Telegram / Slack / Discord; Hermes routes platform messages into the agent workflow
- **When you want zero Anthropic / OpenAI dependency**, this setup fits offline, privacy-sensitive, and low-cost repeat experiments
- Step-by-step walkthrough: [`resources/cookbook.en.md` Recipe 6](cookbook.en.md#6-local-llm--cli-agent-quick-walkthrough)

---

## Linking Back to Branches

Different audiences have different CLI needs:

- **[for-developer](../branches/for-developer.en.md)**: also see IDE-based agents (Cursor, Cline, Continue)
- **[for-everyday-users](../branches/for-everyday-users.en.md)** Tier 2: CLI is the advanced option; try Tier 0 / 1 (Web / Desktop App) first
- **[for-researcher](../branches/for-researcher.en.md)**: also see paper-specific tools (paper-qa, gpt-researcher, ChatPaper)
- **[for-knowledge-worker](../branches/for-knowledge-worker.en.md)**: also see workflow automation (n8n, Make)
- **[for-teacher](../branches/for-teacher.en.md)**: CLI is advanced for teachers; start with prompt libraries

---

## Maintenance Notes

- 8 CLI tools' stars / license / pushed_at auto-refreshed weekly by the `weekly-catalog-refresh` CI (manual run: `python scripts/refresh-stars.py`)
- The CLI market moves fast — new tools require evaluation before inclusion (bar: 30k+ stars, actively maintained, true CLI not IDE; an official-vendor or very-new CLI can be an exception, e.g. Grok Build)
- The comparison table deliberately leaves out "strengths / weaknesses" columns — avoiding subjective bias and letting the use-case section + readers' own judgment do that work

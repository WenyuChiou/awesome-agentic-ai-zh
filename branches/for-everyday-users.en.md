# Extension Path: For Everyday Users

> [繁體中文](./for-everyday-users.md) | [简体中文](./for-everyday-users.zh-Hans.md) | **English**

> 🚀 **Everyday users can start directly at Tier 0** (web / mobile apps), **without any setup**. Only read [`resources/setup-guide.en.md` A-C](../resources/setup-guide.en.md) (about 30 minutes from zero) when you want to run a local LLM (Tier 3) or use CLI automation (Tier 2).

> [← Back to main path README](../README.en.md) · You **don't have to walk the full main path** to start here — this branch is for people who **just want to USE AI, not build agents**.

## Use Cases (Life Scenarios × How AI Helps)

The table below splits everyday AI use into 7 common scenarios. Most of them are fully covered by web apps at Tier 0:

| Scenario | Pain point | How AI helps | Recommended tools |
|---|---|---|---|
| **Writing email / cover letters** | Getting stuck on how to start | Drafting + tone edits + version comparison | Claude.ai / ChatGPT |
| **Learning new skills** | Materials feel formal; nobody is there to ask | Personalized tutoring, interruptible at any time | Claude.ai / ChatGPT |
| **Language practice** | No conversation partner; unclear grammar mistakes | Voice conversation and instant correction | ChatGPT Voice / Gemini |
| **Research / comparison** | Hard to know which source to trust | Multi-source search with citations | Perplexity |
| **Organizing life workflows** | Recipes / trips / todo lists are scattered | Consolidation + structure | Claude.ai / ChatGPT |
| **Batch file cleanup** | 100 PDFs / images with no clear grouping | Rename + classify + summarize | Claude Desktop / Claude Code |
| **Privacy-sensitive chat** | Medical / legal / financial notes should not go to the cloud | Run a local LLM | Ollama + qwen2.5 |

> 💡 **Do not rush upgrades**: the first 5 scenarios can stay at Tier 0 (web). You only need Tier 1-3 when you repeat the same flow often or data absolutely cannot leave your machine.

## Where to Start: 4 Tiers by "How Hands-On Are You?"

```
Tier 0: Web / Mobile App (recommended starting point)
   ↓
Tier 1: Desktop App (upgrade when you need to handle local files)
   ↓
Tier 2: CLI Agent (willing to learn a bit of command line; automate daily flows)
   ↓
Tier 3: Local LLM (privacy-sensitive, cost-sensitive, want offline)
```

**Most people stay at Tier 0 / Tier 1** — Tiers 2-3 are for special needs or learners.

---

## 🎯 Curated Projects

### Tier 0 — Web / Mobile App ⭐ Entry-level

#### [Claude.ai](https://claude.ai) ⭐⭐⭐⭐⭐
Anthropic's official interface. Best for long-form writing, in-depth discussion, complex questions — answer style is more restrained, less hallucination-prone.

#### [ChatGPT](https://chatgpt.com) ⭐⭐⭐⭐⭐
OpenAI's official interface. Largest ecosystem (GPTs, Custom Instructions, Voice mode). The standard general-purpose pick.

#### [Gemini](https://gemini.google.com) ⭐⭐⭐⭐
Google's offering. Long context — enough to read very long documents, roughly a thick book — is particularly useful for dropping in a whole PDF and asking questions; still check whether citations and summaries are correct. Integrated with Google services (Gmail, Docs).

#### [Perplexity](https://perplexity.ai) ⭐⭐⭐⭐
Search engine × LLM — every answer cites sources. Better than ChatGPT for "needs current info" scenarios.

---

### Tier 1 — Desktop App

#### [Claude Desktop](https://claude.ai/download) ⭐⭐⭐⭐⭐
Beyond the web version: drag files in, read local files, retain long conversation context. **Also the gateway to AI-tool integration (MCP)** — you can connect Slack / Gmail / Calendar and operate them directly inside Claude.

#### [ChatGPT Desktop](https://chatgpt.com/download/) ⭐⭐⭐⭐
Desktop version of ChatGPT. Ask questions about screenshots, voice conversation, integrate with other apps.

---

### Tier 2 — CLI Agents (advanced users willing to learn the command line)

> These tools are positioned for developers but **everyday users can use them too** — e.g. batch-rename files, organize the Downloads folder, auto-write weekly reviews, summarize PDFs into Markdown.
>
> Want to know which kind of CLI agent fits you? See [`resources/cli-agents-guide.en.md`](../resources/cli-agents-guide.en.md) — choose by how you work, common pitfalls, and real-world setups.
>
> Want step-by-step onboarding? See [`tracks/cli/A1-cli-intro.en.md`](../tracks/cli/A1-cli-intro.en.md) — Track A first stop, from install to your first task.
>
> Want to wire your CLI agent to Notion / Obsidian / Excel / Google docs / etc.? See [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md) — 81+ MCP servers / Skills grouped by use case.

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 138k+ — Anthropic's official CLI agent. Reads/writes files, runs commands, handles multi-step tasks. **The most beginner-friendly CLI tool for everyday users.**

#### [openai/codex](https://github.com/openai/codex) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 115k+ |
| License | Apache-2.0 |

**What it teaches**: OpenAI's terminal agent — it can help organize files, batch-process text, and run multi-step tasks from the command line; coding is only one use case. Same category as Claude Code, but uses OpenAI models.

**Best for**: People who already subscribe to ChatGPT Plus / Pro and want to use the same account in the terminal.

#### [anomalyco/opencode](https://github.com/anomalyco/opencode) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 196k+ |
| License | MIT |

**What it teaches**: Open-source coding agent **not tied to any specific LLM provider** — use Claude, GPT, Gemini, or local Ollama, your choice. Community-maintained, fast iteration.

**Best for**: Self-hosters; people who don't want vendor lock-in; anyone switching between multiple LLMs.

#### [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 103k+ |
| License | Apache-2.0 |

**What it teaches**: Google's official Gemini CLI agent. Brings Gemini's long context and Google ecosystem integration to the terminal.

**Best for**: Heavy users of the Google ecosystem (Gmail, Drive, Docs).

---

### Tier 3 — Local LLM (privacy / offline / cost)

#### [Ollama](https://github.com/ollama/ollama) ⭐⭐⭐⭐⭐
★ 170k+ — One command to run a local LLM. Use this when privacy-sensitive data (medical records, contracts, family conversations) shouldn't leave your machine. See [Stage 1 — Local LLM](../stages/01-llm-basics.en.md).

#### [LM Studio](https://lmstudio.ai/)
Closed-source but the most beginner-friendly option — drag-and-drop UI, no command line. Mac / Windows / Linux.

---

### Prompt Library

#### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) ⭐⭐⭐⭐
★ 161k+ — Community-maintained prompt megacatalog. "Act as a translator / résumé consultant / chef..." in hundreds of roles. **When stuck on how to start, browse here.**

---

## Required Reading

1. [**Anthropic — How to write effective prompts**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — readable without code
2. [**OpenAI — Prompting Guide**](https://platform.openai.com/docs/guides/prompt-engineering) — the parallel official doc

If you want to go deeper, see [Stage 2 — Prompt Engineering](../stages/02-prompt-engineering.en.md), which has a more systematic treatment.

## Workflows You Can Build (by frequency)

Use these 5 templates as starting points and adapt them to your own context:

| Frequency | Workflow | Steps (≤3) | Recommended tools |
|---|---|---|---|
| **Daily** | Email triage | (1) Paste pending emails into Claude in the morning<br>(2) Ask it to classify "reply now / today / this week / skip"<br>(3) Draft replies for your review | Claude.ai / ChatGPT |
| **Daily** | Speaking practice | (1) Open ChatGPT Voice<br>(2) Practice English / Japanese conversation<br>(3) Ask it to flag grammar mistakes | ChatGPT Voice / Gemini |
| **Weekly** | Weekly journal | (1) Tell Claude what you did this week<br>(2) Ask for a journal + next week's priorities<br>(3) Save it to Obsidian / Notion | Claude.ai |
| **Occasional** | Batch file cleanup | (1) Run Claude Code in your Downloads folder<br>(2) Rename by date + topic<br>(3) Sort into subfolders | Claude Code |
| **Privacy scenario** | Local medical / legal / financial notes | (1) Run qwen2.5:7b in Ollama<br>(2) Organize personal notes without sending data to the cloud<br>(3) ⚠️ It protects **privacy**, not **correctness**: specific diagnoses / legal judgments / investment decisions still require professionals | Ollama + qwen2.5 |

> 💡 **Starter habit**: run "daily email triage" and "speaking practice" for a month first, then add other workflows.

## Tier Recommendations for Everyday Users

Recommended progression:

| Tier | Tools | Best for | Learning cost |
|---|---|---|---|
| **Tier 0** | Claude.ai / ChatGPT / Gemini / Perplexity (web) | 90% of scenarios: no install, no payment required | 0 (if you can use a browser) |
| **Tier 1** | Claude Desktop / ChatGPT Desktop + MCP | Local files, retained conversation history, Gmail / Notion integrations | 30 minutes |
| **Tier 2** | Claude Code / opencode (CLI) | Repeated automation needs, such as doing the same task 100 times daily | 1-2 days |
| **Tier 3** | Ollama local LLM | Privacy-sensitive data that cannot go to the cloud, API-cost sensitivity, offline use | Half a day |

> **Do not let anyone push you to upgrade prematurely**. Tier 0 is enough for most people. Tiers 2-3 are tools, not status symbols.

## Community Notes

Contributions especially welcome:

- Domain-specific prompt templates (cooking, fitness, language learning)
- Chinese-friendly chat tools (Chinese LLMs, localized wrappers)
- Privacy / safety best practices (what data is OK to send / what isn't)

See [CONTRIBUTING.en.md](../CONTRIBUTING.en.md).

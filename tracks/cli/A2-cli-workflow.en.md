# A2 — CLI Workflow Patterns

> [繁體中文](./A2-cli-workflow.md) | [简体中文](./A2-cli-workflow.zh-Hans.md) | **English**

> [← A1 — CLI Intro](A1-cli-intro.en.md) · **Track A: CLI Power User** — Stop 2

⏱ **Time estimate**: 1-2 weeks (~8-15 hours)

> 📋 **Chapter structure**: Learning goals → Entry conditions → Required reading → Hands-on exercises → Curated Projects → Self-check
> 🔑 **Key terms**: see [`resources/glossary.en.md` 5](../../resources/glossary.en.md#5-claude-code-ecosystem) (CLAUDE.md / slash command / SKILL.md / plugin / portable prompt)

After installing a CLI and running first tasks, the next question: **how do I make the CLI consistent, repeatable, shareable?** This stop covers workflow patterns — turning "I retype the same prompt every time" into "set it up once, the CLI does the right thing automatically".

## 📌 Learning Goals

- Write a practical `CLAUDE.md` / `AGENTS.md` — the minimum practical shape is **(1) role** + **(2) project context** + **(3) forbidden actions** + **(4) test commands** + **(5) delivery format**. In practice, 30-50 lines can usually cover those 5 things; beyond 50 lines, split the file
- Design repeatable slash commands / custom prompts
- Decompose multi-step tasks into ones the CLI can execute end-to-end
- Design prompts portable across CLIs

## 🚪 Entry Conditions

You should already:

- Have completed [A1](A1-cli-intro.en.md): picked a primary CLI, installed it, authenticated, and run at least 5 non-hello-world tasks
- Have written one `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` (even just a rough first pass)
- Be comfortable with the Stage 2 prompt engineering basics

Not there yet? → go back to [A1](A1-cli-intro.en.md) and get comfortable with CLI-1/2 first.

## 📚 Required Reading

1. [**Anthropic — CLAUDE.md best practices**](https://code.claude.com/docs/en/memory) ⭐
2. [**Stage 2 — Prompt Engineering**](../../stages/02-prompt-engineering.en.md) — workflow design and prompt design are two sides of the same coin
3. [**Stage 5.1 — Claude Code Basics**](../../stages/05-claude-code-ecosystem.en.md#51--claude-code-basics) — slash command details
4. [**`resources/cli-agents-guide.en.md`** "Cross-CLI portable prompt patterns"](../../resources/cli-agents-guide.en.md) — portable prompt principles

## 🛠 Hands-on Exercises

### Exercise CLI-5: Write production CLAUDE.md
Your CLAUDE.md should at minimum contain:

- **Persona**: "You're a senior Python engineer / academic writing assistant / etc."
- **Repo context**: what project, what stack, what conventions
- **Don't do**: don't touch main, don't move secrets, don't auto-commit
- **How to do things**: plan first, run tests before commit, use type hints
- **Common commands**: how to run tests, lint, deploy

Commit it to git. Next time a teammate clones the repo, their Claude Code auto-loads your conventions.

### Exercise CLI-6: First slash command
Write `.claude/commands/review.md` (or your CLI's equivalent):
```markdown
---
name: review
description: Review staged changes for security + style
---

Run this flow:
1. `git diff --cached` to get staged changes
2. Look for: hard-coded secrets, SQL injection, type errors
3. Check against the style rules in CLAUDE.md
4. Output: PASS / or list of specific changes needed
```
After this, every `/review` runs the same flow.

### Exercise CLI-7: Multi-step task decomposition
Give the CLI a complex task ("translate these 50 markdown files to English + add frontmatter + move to en/ subdirectory").

- First time: throw the whole task at it → observe how it does it, where it errs
- Second time: pre-decompose into 5 sub-tasks, give them one by one → observe the difference
- Lesson: the CLI is like you — too-big tasks need decomposition; too-small tasks lead to over-orchestration

> ⭐ **Advanced note: Claude Code native multi-agent mechanisms** (read this one sentence for now; no need to expand it in A2): the manual sub-task splitting in CLI-7 can be automated with Claude Code's **Subagent / Agent team / Background agent** mechanisms. The full explanation, exercises, and when-not-to-use guidance (team permissions, context isolation, and result-review flow all matter) are in **[Stage 5.5](../../stages/05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature)**.

### Exercise CLI-8: Portable prompt
Write a prompt that works in Claude Code. **Run the same prompt in Codex / OpenCode / Gemini CLI** — what needs to change? Common discoveries:

- file path conventions differ (cwd vs absolute)
- shell execution permission defaults differ
- "plan-first" prompting needs explicit instructions in some, default in others

Compile these into your own cheat sheet.

## 🎯 Curated Projects

Four categories, seven projects, one table covers it. **Pick your entry point from the "Who it's for" column; follow the link when you want the detail in the repo.**

| Category | Project | ⭐ | Who it's for | Why recommended / notes |
|---|---|---|---|---|
| **CLAUDE.md Examples** | [Anthropic official CLAUDE.md guide](https://code.claude.com/docs/en/memory) | ⭐⭐⭐⭐⭐ | Copying the structure for your first CLAUDE.md | Official — Claude Code memory / CLAUDE.md authoring docs, including best practices; it is the Claude Code repo's own CLAUDE.md, written the official way |
| | [obra/superpowers](https://github.com/obra/superpowers) | ⭐⭐⭐⭐ | Reading a complete `.claude/` directory that is actually in use | Not just a skill collection but also a production CLAUDE.md template (★ 265k+) |
| | [mattpocock/skills](https://github.com/mattpocock/skills) | ⭐⭐⭐⭐ | Anyone who wants a practitioner's daily skill library | The `.claude/` structure is a great reference. **More skill examples in [Stage 5.3 — Skills](../../stages/05-claude-code-ecosystem.en.md#53--skills-claude-codes-behavior-layer--the-most-critical-layer-of-the-claude-code-ecosystem)** |
| **Slash Commands / Custom Prompts** | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | ⭐⭐⭐⭐⭐ | Finding the official plugin template | Official plugin marketplace; each plugin's commands / skills serve as slash command examples (★ 32k+) |
| | [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | ⭐⭐⭐ | Browsing community slash command examples | Community-curated list of Claude Code resources |
| **Prompt Design References** | [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) | ⭐⭐⭐⭐ | Finding CLI-agnostic prompt patterns when you are stuck | Started for ChatGPT but ~90% of the patterns work in CLIs too (★ 166k+, CC0). Full prompt engineering deep dive: [Stage 2 — Curated Projects](../../stages/02-prompt-engineering.en.md#-curated-projects) (DSPy, Prompt-Engineering-Guide, etc.) |
| **Multi-CLI Patterns** | [`resources/cli-agents-guide.en.md`](../../resources/cli-agents-guide.en.md) "Three common combinations" | ⭐⭐⭐⭐ | Trying a multi-CLI pairing strategy | In-repo resource — look at Setup A / B / C and try one that fits |

> 💡 **Suggested order to pick these up**: copy Anthropic's official CLAUDE.md structure first → add your own repo context → look at obra/superpowers to see what a complete `.claude/` actually looks like → then write 1-2 slash commands (mine the hesreallyhim awesome list for ideas).

### Recommended Tools

- [**yamadashy/repomix**](https://github.com/yamadashy/repomix) ⭐⭐⭐⭐⭐ ★ 27k+ — Packs your entire codebase into a single AI-friendly file (XML / Markdown / JSON) for Claude Code / Codex code review / refactoring. Includes MCP server mode + tree-sitter compression (compression varies by language and file structure) + secretlint for secret filtering. **A must-have, daily-driver-grade tool for Track A.**
- [**langchain-ai/openwiki**](https://github.com/langchain-ai/openwiki) ⭐⭐⭐⭐ ★ 15k+ — CLI that generates and auto-maintains a wiki of your codebase, then wires a reference into `CLAUDE.md` / `AGENTS.md` so your coding agent reads it on demand and it stays updated as code changes. `npm i -g openwiki` → `openwiki --init`. Built on DeepAgents, traces to LangSmith. MIT.

> 💡 **Concept: *agent-facing documentation*.** repomix and OpenWiki attack the same gap (your agent doesn't know the repo) from two angles: a one-shot packed snapshot vs a living, auto-maintained wiki. The shared move is to give the agent *structured codebase context it reads on demand*, kept separate from your `CLAUDE.md` instructions rather than crammed into the prompt.

## ✅ Self-Check Before A3

Can you:

- [ ] Written at least 1 CLAUDE.md for a production / work repo (not a demo repo)
- [ ] Written at least 2 slash commands you actually use
- [ ] Run the same prompt across 2 different CLIs and know the differences
- [ ] Articulate "what tasks should be decomposed vs not"

If yes → proceed to [A3 — Integration & Production](A3-cli-production.en.md).

If no → CLAUDE.md only on demo repos is wasted; go write one for your real repo first.

## 💡 Common Pitfalls

- **CLAUDE.md too long**: over 100 lines and the CLI auto-truncates / ignores the back half. Sweet spot: 30-60 lines.
- **Slash command written as "do X, Y, Z, A, B" in one sentence**: CLIs skip steps. Rewrite as numbered list with a success criterion per step.
- **Over-portable**: each CLI has its own strengths; don't strip a prompt of specifics just to make it cross-CLI.
- **"I already know all this, I don't need to write it"**: CLAUDE.md is for future you (and new team members), not for current you.

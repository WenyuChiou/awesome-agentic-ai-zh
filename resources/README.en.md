# `resources/` Index

<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

> This is the repo's **reference area**: supplementary material that sits outside the main path and is meant to be opened when needed. Each file has a distinct role.

---

## 7 References + When to Read Each

| File | Role | When to Read | Lines |
|---|---|---|---|
| [`glossary.en.md`](glossary.en.md) | **30-second term lookup** | You hit terms like LLM / RAG / token / agent / vector DB / streaming / batch API while reading a stage | ~210 |
| [`cli-agents-guide.en.md`](cli-agents-guide.en.md) | **8 CLI agents compared** | First time choosing among Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent / Grok Build | ~134 |
| [`mcp-skills-catalog.en.md`](mcp-skills-catalog.en.md) | **81+ integration catalog** | You want Claude Code connected to Notion / Obsidian / Excel / Postgres / Slack / other real tools | ~775 |
| [`schema-design-cheatsheet.en.md`](schema-design-cheatsheet.en.md) | **5 function-schema rules + 5 anti-patterns** | You are writing a tool schema / MCP server schema / function calling and the LLM picks the wrong tool or arguments | ~159 |
| [`cookbook.en.md`](cookbook.en.md) | **6 step-by-step recipes** | You want to build a first Skill / MCP server / Office integration / NotebookLM flow / Zotero flow / local LLM in 30-50 minutes | ~620 |
| [`setup-guide.en.md`](setup-guide.en.md) | **From-zero setup guide** | No dev background; first time creating an API key, installing Python, or using Claude Code | ~400 |
| [`style-guide.en.md`](style-guide.en.md) | **Format and wording rules before PRs** | You want to contribute to the repo, add entries, or improve translations | ~338 |

Together these are about ~2500 lines of reference. That sounds large, but **each file is read at a different moment**. You do not read all of them at once; you open the relevant one for 30 seconds to 45 minutes.

---

## Entry Points: "What Am I Trying to Do?"

### 🆕 I Have Never Written Code / This Is My First AI Agent Setup

→ [`setup-guide.en.md`](setup-guide.en.md) (30-45 minutes from zero)

### 🆕 I Am Just Starting to Learn AI Agents

You do not need any reference first. **Start with the main [README](../README.en.md) → [Stage 0](../stages/00-foundations.en.md)**. When a term is unclear, come back to [`glossary.en.md`](glossary.en.md).

### 🛠 I Need to Choose a CLI Agent

→ [`cli-agents-guide.en.md`](cli-agents-guide.en.md) (CLI comparison + recommendations by use case)

### 🔌 I Want to Connect Claude Code to Tool X (Notion / Excel / Postgres / etc.)

→ [`mcp-skills-catalog.en.md`](mcp-skills-catalog.en.md) (81+ integrations in 16 categories)

### 🍳 I Want to Build My First Skill / MCP Server / Word Integration

→ [`cookbook.en.md`](cookbook.en.md) (6 step-by-step recipes)

### 📐 I Wrote a Tool Schema and the LLM Is Not Following It

→ [`schema-design-cheatsheet.en.md`](schema-design-cheatsheet.en.md) (5 rules + 5 anti-patterns)

### 📚 I Hit an Unclear Term While Reading a Stage

→ [`glossary.en.md`](glossary.en.md) (30-80 words per term + which stage goes deeper)

### 🤝 I Want to Send a PR / Translate / Add a New Entry

→ [`style-guide.en.md`](style-guide.en.md) + [`../CONTRIBUTING.en.md`](../CONTRIBUTING.en.md)

---

## Duplication?

Duplication is deliberately avoided. Here is how each reference relates to the main path and to the other references:

- **glossary** is a 30-second lookup, stage text is a 3-5 minute read, and cookbook is a 30-50 minute build — three depths, no overlap.
- **schema-design-cheatsheet** overlaps with cookbook 2 (building an MCP server), but the cheatsheet explains **the rules for writing a schema** while the cookbook explains **how to get a server running**. Which one you want depends on where you are stuck.
- **cli-agents-guide** is a reference table; the catalog is plug-in tools — two different levels.
- **Relationship to [Hello-Agents](https://github.com/datawhalechina/hello-agents)**: Hello-Agents is the most complete Chinese-language agent course available, and it goes deep. This repo works from a different angle, **roadmap + curated catalog + hands-on recipes**, and does not replace it. Stage 5.3 and cookbook 1 both cross-reference Hello-Agents Extra08, "How to Write a Good Skill", as deeper follow-up reading.

---

## Language Coverage

| File | zh-TW (canonical) | zh-Hans | English |
|---|---|---|---|
| glossary | ✅ | ✅ | ✅ |
| cli-agents-guide | ✅ | ✅ | ✅ |
| mcp-skills-catalog | ✅ | ✅ | ✅ |
| schema-design-cheatsheet | ✅ | ✅ | ✅ |
| cookbook | ✅ | ✅ | ✅ |
| setup-guide | ✅ | ✅ | ✅ |
| style-guide | ✅ | ✅ | ✅ |

---

## Standards for Adding a New Reference

A new reference file should not be added casually. It must:

1. **Avoid duplicating any existing role** in the table above.
2. **Solve a problem the main path cannot cover well**. If 50 lines in Stage X would cover it, put it in that stage.
3. **Be expected to receive 3+ cross-references** from stages or branches. If it only serves one stage, keep it in that stage.

Possible future references:

- `cost-calculator-guide.md`: cross-provider pricing. [Stage 1](../stages/01-llm-basics.en.md) covers enough for now.
- `troubleshooting-guide.md`: common error runbook. Existing material is enough until more community reports arrive.
- `prompt-patterns-guide.md`: CoT / few-shot template library. [Stage 2](../stages/02-prompt-engineering.en.md) already covers the basics; a deeper version can wait for community PRs.

If the community wants one of these added, open an issue to discuss it.

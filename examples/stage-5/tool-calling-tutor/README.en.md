<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# tool-calling-tutor — Claude Code skill

> What this skill does: when you're stuck on tool calling (LLM won't call, args wrong, ReAct loop runs forever, or the schema is unclear), open it directly with `/tool-calling-tutor`. It may also load automatically in a relevant context and guide you through a four-symptom diagnostic and five-step fix.

Pairs with [Stage 3 — Tool Use & Agent Intro](../../../stages/03-tool-use-and-hello-agent.en.md). Also serves as the **bundled skill example** for [Stage 5 — Claude Code Ecosystem](../../../stages/05-claude-code-ecosystem.en.md) 5.3.

## Why this skill exists

Tool calling is the steepest learning curve in the curriculum — schema design + SDK response shape + ReAct loop are three mental models stacked at once. The Stage 3 doc covers the concepts, but **when you hit "this just doesn't work", you need interactive debugging**.

This skill fills that gap:

| Existing resource | Limit | What this skill adds |
|---|---|---|
| `stages/03-tool-use-and-hello-agent.en.md` | Covers 6 exercises, not interactive | Interactive triage: which symptom are you stuck on? |
| `resources/schema-design-cheatsheet.en.md` | 5 rules + 5 anti-patterns, prescriptive | Procedural: bad → good schema in 4 step-by-step iterations |
| `resources/glossary.en.md` 2 | 1-line definitions | Doesn't redefine, references |
| `examples/stage-3/02-06/` | Full runnable starters | Skill points at them as fork templates |

## Dual purpose

1. **For learners**: install it as a personal debug assistant. Open it with `/tool-calling-tutor`; it may also load automatically when your request matches its description.
2. **As a Stage 5 5.3 meta-example**: when learning to write SKILL.md, study this one directly. Includes full frontmatter (with trigger phrases + Do NOT use for), `references/` design, and `evals/evals.json` example.

## Install

Run every command below from the root of this repository.

### Option A: user-level (shared across all projects)

```powershell
$repoRoot = Get-Location
$skillSource = Join-Path $repoRoot "examples\stage-5\tool-calling-tutor"
$skillTarget = Join-Path $env:USERPROFILE ".claude\skills\tool-calling-tutor"
New-Item -ItemType Directory -Force -Path $skillTarget | Out-Null
Copy-Item -Force -LiteralPath (Join-Path $skillSource "translations\SKILL.en.md") -Destination (Join-Path $skillTarget "SKILL.md")
Copy-Item -Recurse -Force -LiteralPath (Join-Path $skillSource "references") -Destination $skillTarget
Copy-Item -Recurse -Force -LiteralPath (Join-Path $skillSource "evals") -Destination $skillTarget
```

For Traditional Chinese, copy `SKILL.md` instead. For Simplified Chinese, copy `translations/SKILL.zh-Hans.md` instead.

### Option B: project-level (only triggers in this repo)

```powershell
$repoRoot = Get-Location
$skillSource = Join-Path $repoRoot "examples\stage-5\tool-calling-tutor"
$skillTarget = Join-Path $repoRoot ".claude\skills\tool-calling-tutor"
New-Item -ItemType Directory -Force -Path $skillTarget | Out-Null
Copy-Item -Force -LiteralPath (Join-Path $skillSource "translations\SKILL.en.md") -Destination (Join-Path $skillTarget "SKILL.md")
Copy-Item -Recurse -Force -LiteralPath (Join-Path $skillSource "references") -Destination $skillTarget
Copy-Item -Recurse -Force -LiteralPath (Join-Path $skillSource "evals") -Destination $skillTarget
```

<details markdown="1">
<summary>macOS/Linux commands</summary>

```bash
skill_source="examples/stage-5/tool-calling-tutor"
mkdir -p ~/.claude/skills/tool-calling-tutor
cp "$skill_source/translations/SKILL.en.md" ~/.claude/skills/tool-calling-tutor/SKILL.md
cp -R "$skill_source/references" "$skill_source/evals" ~/.claude/skills/tool-calling-tutor/

mkdir -p .claude/skills/tool-calling-tutor
cp "$skill_source/translations/SKILL.en.md" .claude/skills/tool-calling-tutor/SKILL.md
cp -R "$skill_source/references" "$skill_source/evals" .claude/skills/tool-calling-tutor/
```
</details>

### Verify the install

Enter this command in Claude Code:

```
/tool-calling-tutor
```

Expected: the skill opens and asks for, or confirms, the matching symptom route. This is the deterministic installation check. Automatic loading is context-dependent, so do not use it as proof that installation worked.

Claude Code detects changes in an existing personal or project skills directory during the session. Restart only when the top-level skills directory did not exist when the session started.

## What's inside

```
tool-calling-tutor/
├── SKILL.md # main skill file (zh-TW canonical)
├── README.md / .en.md / .zh-Hans.md # this file
├── references/
│ ├── debug-flowchart.md # 4-symptom diagnostic
│ ├── schema-evolution.md # bad → good schema worked example
│ └── sdk-diff.md # Anthropic vs OpenAI-compat side-by-side
│ (each has .en.md / .zh-Hans.md translations)
├── translations/
│ ├── SKILL.en.md # English version of SKILL.md
│ └── SKILL.zh-Hans.md # Simplified Chinese version
└── evals/
    ├── evals.json # 5 offline contract cases
    └── check_evals.py # checker that does not call a model
```

## Run evals (optional)

```powershell
python evals/check_evals.py
```

This is an **offline contract check** for five cases: it does not ask a model; it checks that every written promise is complete and linked. `evals.json` is not a promptfoo configuration file. If you later want a model-graded evaluation, [promptfoo](https://github.com/promptfoo/promptfoo) is one well-known optional path. This example ships no provider configuration and no quality score.

## Relationship to other resources

```
        ┌─────────────────────────────────┐
        │ Stage 3 doc + inline 練習 1-6 │
        │ (learn tool-calling concepts) │
        └────────────────┬─────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────┐
        │ examples/stage-3/02-06/ │
        │ (full runnable starters) │
        └────────────────┬─────────────────┘
                         │ fork template
                         ▼
        ┌─────────────────────────────────┐
        │ your tool-calling agent │
        │ ❓ stuck │
        └────────────────┬─────────────────┘
                         │ skill loads
                         ▼
        ┌─────────────────────────────────┐
        │ tool-calling-tutor skill (this) │
        │ → 4-symptom triage │
        │ → references/ deep dive │
        │ → route to cookbook / Stage 4/7 │
        └─────────────────────────────────┘
```

## What this skill does NOT handle

| Situation | Route to |
|---|---|
| LangChain / LangGraph / CrewAI / Pydantic AI | Stage 4 |
| Building MCP server / client | `resources/cookbook.en.md` 2 |
| Production observability / cost tracking | Stage 7 |
| General prompt engineering | Stage 2 |

## Extensions

- **Customize trigger phrases**: add your own catch phrases to SKILL.md frontmatter `description`
- **Add your cases to references/**: open new sections in debug-flowchart for weird cases you've hit
- **Fork it**: this skill is designed as a Stage 5 5.3 meta-example — forking welcome

<details markdown="1">
<summary>Current sources</summary>

Small, current references (checked 2026-08-28 UTC): [Claude Code skills](https://code.claude.com/docs/en/skills), [Agent Skills](https://agentskills.io), [Anthropic skills](https://github.com/anthropics/skills), and [promptfoo](https://github.com/promptfoo/promptfoo).
</details>

## License

Same as repo (MIT). Free to rewrite, fork, use commercially.

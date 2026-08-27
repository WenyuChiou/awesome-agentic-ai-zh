# Extension Path: For Developers

> [繁體中文](./for-developer.md) | [简体中文](./for-developer.zh-Hans.md) | **English**

> 🚀 **First time installing Claude Code or writing `CLAUDE.md` / `SKILL.md`?** The quick setup guide is [`resources/setup-guide.en.md` D-E](../resources/setup-guide.en.md). Skip it if you already know this.

> [← Back to main path README](../README.en.md) · Continue here after **Track A's A3** or **Track B's Stage 7**. Apply agentic AI to coding workflows.

## Use Cases (Developer Scenarios × How AI Helps)

The table below splits a developer's day into 7 common scenarios. Each has a different pain point, and each calls for a different level of AI tooling:

| Scenario | Pain point | How AI helps | Recommended tools (light → heavy) |
|---|---|---|---|
| **AI pair programming** | You forget syntax mid-flow or cannot recall a method name | Autocomplete + rewrite + explanation | Cursor / Copilot → Claude Code |
| **Multi-file refactoring** | Changing one class risks missed references; cross-file rename is error-prone | Batch refactors while keeping style consistent across many files | Cursor → Claude Code → codex-delegate |
| **Code review (your own PR)** | Reviewing your own diff makes it easy to miss problems | Find bugs / smells and check edge cases | Claude Code / Cline → Continue (CI) |
| **Writing tests** | TDD cases are easy to miss; coverage falls short | Generate pytest cases from signatures / specs | Claude Code + Aider |
| **Debugging** | Logs are thin; stack traces are hard to interpret | Explain traces, generate hypotheses, run minimal repros | Claude Code |
| **Docs** | Docstrings / READMEs lag behind refactors | Generate docs from code and update docs alongside PRs | Claude Code |
| **CI / team automation** | Manual review is repetitive; style varies across people | Run automated review / lint in GitHub Actions | Claude Code Action + Continue |

> 💡 **Individual vs team**: the first 6 rows are personal daily workflows. The final row (CI) is team governance. For teams under 5 people, AI automation in CI often has low ROI; you can defer it.

## Curated Projects

> **CLI agent identity & selection guide**: choose a tool by how you work in [`resources/cli-agents-guide.en.md`](../resources/cli-agents-guide.en.md). New to CLI agents and want step-by-step onboarding → [`tracks/cli/A1-cli-intro.en.md`](../tracks/cli/A1-cli-intro.en.md) (Track A first stop).
>
> **MCP catalog**: Looking for integrations to wire CLI into daily tools (GitHub, Linear, Atlassian, Postgres, Playwright, Figma…) → [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md) (81+ entries by category).
>
> This page only lists tool entry points directly relevant to developer workflows.

### Coding Agents

#### [Cursor](https://www.cursor.com/) ⭐⭐⭐⭐⭐
Editor-integrated AI pair-programming tool. Widely adopted in AI editor tools and a useful baseline for comparing other IDE agents.

#### [Aider-AI/aider](https://github.com/Aider-AI/aider) ⭐⭐⭐⭐⭐
★ 47k+ · Apache-2.0 — git-aware CLI pair-programmer. Edits files in your repo directly and writes commits for you. **The open-source reference for "git-native AI editing."** Model-agnostic.

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 138k+ — Anthropic's official agentic coding assistant. Skills + plugins ecosystem.

#### [cline/cline](https://github.com/cline/cline) ⭐⭐⭐⭐⭐
★ 65k+ · Apache-2.0 — VS Code extension, autonomous in-IDE agent: tool use, browser, step-by-step approval. **The first pick for VS Code users wanting IDE-native agentic dev.**

#### [continuedev/continue](https://github.com/continuedev/continue) ⭐⭐⭐⭐
★ 35k+ · Apache-2.0 — source-controlled AI checks, enforceable in CI. Represents the **team / governance** angle on coding agents.

#### [OpenHands (formerly OpenDevin)](https://github.com/All-Hands-AI/OpenHands) ⭐⭐⭐⭐
★ 81k+ · MIT — open-source autonomous software development agent. More aggressive design than Aider / Claude Code — agent runs in its own sandbox and commits autonomously. Best for "throw a whole issue at it" scenarios.

#### [aaif-goose/goose](https://github.com/aaif-goose/goose) ⭐⭐⭐⭐
★ 51k+ · Apache-2.0 — Open-source, extensible AI agent that goes beyond code suggestions — install / execute / edit / test, with any LLM. Supports multiple LLM providers and MCP, ships as desktop app, CLI, and API. (Repo now resolves to `aaif-goose/goose`.)

#### [RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code) ⭐⭐⭐ (⚠️ archived)
★ 24k+ · Apache-2.0 — VS Code coding agent with a "**team of specialized modes**" model. Different from Cline's single-agent flow. **⚠️ Repo archived 2026-05 (read-only, no longer maintained)** — still usable, but don't expect new features.

### Code Review

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
20+ battle-tested skills including TDD patterns, debugging, collaboration patterns. Good source for code-review skill design.

### Recommended Tools

- [**yamadashy/repomix**](https://github.com/yamadashy/repomix) ⭐⭐⭐⭐⭐ ★ 27k+ — **Typical developer use case: package the whole codebase for a reviewer / refactor agent**. Outputs a single AI-friendly file (XML / Markdown / JSON) for Claude Code / Codex code review / refactoring. See the official README for technical details such as MCP server mode, tree-sitter compression, and secretlint filtering. **A must-have, daily-driver-grade tool for Track A.**

## Workflows to Master (by frequency)

| Frequency | Workflow | Steps (≤3) | Recommended tools | Best for |
|---|---|---|---|---|
| **Daily** | AI pair programming | (1) Open a branch<br>(2) Give the task to Claude Code and **ask for a plan first** (no code yet)<br>(3) Review plan → approve → code → review your own diff | Claude Code / Cursor / Cline | All developers |
| **Daily** | Git-native AI editing | (1) `aider`<br>(2) Ask in natural language<br>(3) review + commit / `/undo` | Aider | People who want a clean git flow |
| **Per PR** | Automated code review | (1) `.github/workflows/claude-review.yml`<br>(2) Capture git diff → run prompt → post back to PR<br>(3) human + AI review | Claude Code Action + Continue | Teams |
| **Per feature** | Test generation | (1) Provide function signature + docstring<br>(2) Ask AI for pytest cases, including edge cases<br>(3) Run coverage + intentionally break a bug to verify tests catch it | Claude Code / Aider | Test-writing phase |
| **Occasional** | Multi-file batch edits | (1) Claude writes a plan<br>(2) codex-delegate handles mechanical refactors<br>(3) Claude reviews the diff | Claude + codex-delegate | Refactors across 30+ files |

> 💡 **Starter habit**: run "daily AI pairing" and "test generation" for a month first, then add automated PR review.

### 3 Concrete Workflow Recipes

**1. AI Pair Programming (daily cadence)**

1. Start a feature → `git checkout -b feature/xxx`
2. Hand the task to Claude Code / Cursor — **make it write a plan first** (don't dive into code)
3. Review the plan, course-correct → only then approve coding
4. After it's done: run tests + lint → review the diff yourself (**don't blind-accept**)
5. Write the commit message yourself, or have AI draft and edit before committing

**2. Aider Git-Native Flow (closest "pair with AI" experience)**
```bash
# Inside the repo
aider --model anthropic/claude-sonnet-5

# Natural-language ask
> Add a timezone parameter to parse_date in utils.py, default UTC

# Aider edits + commits automatically. To roll back:
> /undo # undoes the last AI commit
```

**3. PR-time Claude code review (GitHub Action)**

`.github/workflows/claude-review.yml`:
```yaml
on:
  pull_request:
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Run Claude review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # Use anthropics/claude-code-action or your own script
          # Get git diff, run prompt, post results back to PR
```
Reference: official [`anthropics/claude-code-action`](https://github.com/anthropics/claude-code-action) GitHub Action.

## Common Pitfalls (Anti-patterns)

| ❌ Don't | ✅ Do instead |
|---|---|
| Let AI push directly to main | Always go through PR → review → merge |
| Blind-accept large refactor diffs | Break into < 50 LOC chunks, review each |
| Hand `.env` / API keys to the AI | Use your tool's exclusion mechanism — Cursor `.cursorignore` / Aider `.aiderignore` / Claude Code `permissions.deny` in `.claude/settings.json` |
| Let AI run shell freely against production code | Sandbox + permission whitelist |
| Take AI-generated tests at face value | Run coverage + intentionally break a unit to see if tests catch it |
| Discover wrong direction after many commits | **Plan-first** mode: review the plan before any coding |

## Tier Progression

Recommended progression:

| Tier | Tools | Best for | Learning cost |
|---|---|---|---|
| **Tier 0** | Cursor / Copilot / Claude.ai | IDE chat, autocomplete, no custom agents | 0 (if you can use an editor) |
| **Tier 1** | Claude Code / Cline / OpenCode + `CLAUDE.md` | CLI with file-system access, human-in-the-loop | 1-2 days |
| **Tier 2** | Custom Skills + MCP server | Packaging dev workflows as shared team skills | 1 week of setup |
| **Tier 3** | Auto-running agents in CI + production observability | [Stage 7](../stages/07-multi-agent-production.en.md) territory | Several weeks, governance required |

> **Most individual developers can stay at Tier 0-1**. **Validate ROI before going Tier 2+**: it is only worth the investment if the team is large, the workflows repeat often, and failures are hard to reverse.

## Other Branches Also Apply

Branches that overlap heavily with developers:

- **Doing ML research / writing papers** → [Researcher branch](./for-researcher.en.md)
- **Wire Notion / Linear / Atlassian / Postgres / Figma into your CLI** → [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md)
- **Author your own Skill / MCP server** → [Stage 5](../stages/05-claude-code-ecosystem.en.md) + [`resources/cookbook.en.md`](../resources/cookbook.en.md)
- **Schema design details** → [`resources/schema-design-cheatsheet.en.md`](../resources/schema-design-cheatsheet.en.md)
- **CLI from zero** → [Track A](../tracks/cli/A1-cli-intro.en.md) (A1 → A2 → A3)

## Community Note

Contributions especially welcome:

- IDE-specific config templates (Cursor `.cursorrules`, Claude Code `CLAUDE.md` for Python / Go / Rust, etc.)
- Language-specific Skills (Python / TypeScript / Rust / Go best-practice patterns)
- CI / pre-commit hook integration case studies
- **Multi-developer team governance** — sharing Skills across devs, permission design, cost tracking

See [CONTRIBUTING.en.md](../CONTRIBUTING.en.md).

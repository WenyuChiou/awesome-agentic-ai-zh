# Subagent Cookbook — 15 Copy-Paste Dispatch Recipes

> [繁體中文](./subagent-cookbook.md) | [简体中文](./subagent-cookbook.zh-Hans.md) | **English**

> 📋 **What this is**: [Stage 5.5](../stages/05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature) teaches the concept of subagents. This cookbook teaches you how to **use them today**: 15 scenarios, each with “which subagent to use + a complete prompt template you can copy-paste + when not to use it.”
>
> ⚠️ **First time here? Read Stage 5.5’s “Which subagents can you dispatch?” and “decision table” sections first**. Once you understand what a subagent is and which ones Claude Code includes, come back and pick a recipe.

---

## How to Read This Cookbook

Each recipe uses the same 4-part structure:

| Section | Content | Why it exists |
|---|---|---|
| **Scenario** | A concrete situation you might run into today | Find a recipe from “I have X problem,” not from “I want to use a subagent” |
| **Subagent** | Which one to use (Claude Code’s built-in name) | Copy the name directly; no guessing |
| **Prompt Template** | Copy-paste-ready instruction text | No need to invent the prompt yourself |
| **When Not to Use It** | A better alternative than using a subagent | Avoid overkill |

> 💡 **How to actually dispatch a subagent**: in your Claude Code terminal conversation, **type or paste the prompt template directly**. That is all. Claude sees the instruction, automatically uses the **Agent tool** (Claude Code’s internal dispatch mechanism) to find the right subagent, runs it, and returns a short summary to the main session. **No slash command or special syntax is required**.
>
> 📌 **Subagent vs slash command**: `/agents` is a list command, **not how you invoke a subagent**. To dispatch a subagent, type ordinary prompt text directly. For complete comparison tables (subagent vs skill / vs slash command / description router), see [Stage 5.5 §Common Confusing Concepts Clarified](../stages/05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature).

---

## First, Check Which Subagents You Have Available

Run `/agents` inside your Claude Code session. It lists every subagent currently available to you: built-in, plugin-provided, and custom.

**The 7 built-in Claude Code subagents**: `general-purpose` / `code-reviewer` / `Explore` / `Plan` / `frontend-developer` / `claude-code-guide` / `statusline-setup` (as of 2025-11; this may change).

> 📌 **Each built-in subagent's purpose + the "task X → use subagent Y" decision table live canonically at [Stage 5.5 §Which subagents can you dispatch?](../stages/05-claude-code-ecosystem.en.md#which-subagents-can-you-dispatch)** — this cookbook focuses on the 15 dispatch recipes; treat Stage 5.5 as the source of truth for the built-in list and selection logic.

> 💡 **If your `/agents` list does not match this cookbook**: you may have installed plugins, or your Claude Code version may differ. **When a recipe name does not match, use the closest available subagent**. For example, if you do not have `Explore`, `general-purpose` can still run a search task.

After confirming what is available, use the 15 recipes below: **find the recipe that matches your scenario, then copy the Prompt Template into the Claude Code conversation**.

---

## The 15 Recipes

### Recipe 1: Review a batch of new code before committing

**Scenario**: You just wrote ≥ 50 lines of new code and want to commit, but you are worried you missed a bug or security issue.

**Subagent**: `code-reviewer`

**Prompt Template**:
```
Review the staged changes in this repo (git diff --cached).
Focus on: (1) security issues (hardcoded secrets, SQL injection, XSS),
(2) error handling gaps, (3) missing tests, (4) violations of CLAUDE.md
conventions. Per-category PASS/FAIL + concrete fix for each issue with
file:line reference + overall verdict (APPROVE / REQUEST CHANGES).
```

**When Not to Use It**: A < 20-line typo or formatting fix. Just scan `git diff` yourself; do not spend subagent tokens.

---

### Recipe 2: Enter a new repo and find where to start reading

**Scenario**: You cloned someone else’s repo, `README.md` does not clearly explain the entry point, and you do not want to dig randomly.

**Subagent**: `Explore`

**Prompt Template**:
```
Map the entry points and core structure of this codebase. Report:
(1) main entry script(s) — what file gets run first,
(2) core module organization — top 3-5 directories and what each does,
(3) test directory layout,
(4) any "where to start reading" guidance in docs/.
Under 300 words with file paths.
```

**When Not to Use It**: You already know the exact file path to read. Use the Read tool directly.

---

### Recipe 3: Design a refactor / migration plan before touching code

**Scenario**: You need to refactor a large module or do a framework migration, but the steps are unclear and you want a plan first.

**Subagent**: `Plan`

**Prompt Template**:
```
Design a step-by-step plan to refactor <module-name> (currently a single
file with tight coupling) into clear, testable components with explicit
interfaces. Include: (1) phased breakdown (≤ 5 phases), (2) which files
touched per phase, (3) what tests gate each phase, (4) rollback strategy
if a phase fails. Don't write code — just the plan.
```

**When Not to Use It**: The refactor only touches 1-2 files. Start directly; the planning overhead is not worth it.

---

### Recipe 4: Review multi-file / cross-locale parity

**Scenario**: You changed zh-TW + zh-Hans + en mirror files and want to confirm the three versions still match.

**Subagent**: `code-reviewer`

**Prompt Template**:
```
Review the staged diff for cross-locale parity across the 3 locale
variants of <file-stem> (.md / .zh-Hans.md / .en.md). Check: (1) same
section structure (## headers match), (2) same table row counts, (3)
same required terms present in each locale, (4) locale conventions
correct (zh-Hans uses "" not 「」; en uses English). Report per-file
PASS/FAIL.
```

**When Not to Use It**: You only changed one locale. There is no parity issue to check.

---

### Recipe 5: Multi-source fact-check / research

**Scenario**: You need to write a cited statement, but you are not sure whether multiple sources are talking about the same thing and need cross-checking.

**Subagent**: `general-purpose`

**Prompt Template**:
```
Fact-check this claim: "<claim>". Search for: (1) primary source / official
docs / paper, (2) 2-3 independent secondary sources, (3) any contradictions
or version differences. Report: confirmed / contradicted / nuanced, with
direct quotes and URLs. Under 400 words.
```

**When Not to Use It**: You already have one authoritative source. Read that source directly.

---

### Recipe 6: Find where a symbol / function is defined

**Scenario**: A codebase imports `parse_config` everywhere, and you want to know which file implements it.

**Subagent**: `Explore`

**Prompt Template**:
```
Find where `<symbol-name>` is defined in this codebase. Report: (1) the
file:line where it's defined, (2) what it does (1-line summary), (3) which
files import / use it (top 5). Use Grep, not full file reads.
```

**When Not to Use It**: Your IDE’s “Go to definition” already jumps there. The IDE is faster than a subagent.

---

### Recipe 7: Compare whether several papers / sources agree on a claim

**Scenario**: You are writing a literature review. Three papers disagree about the same thing, and you do not know which one to trust.

**Subagent**: `general-purpose`

**Prompt Template**:
```
Find and compare 3 independent sources on the topic <topic>. For each
source, capture: title + author + year + URL. Then report: (1) what
they agree on, (2) where they disagree (with direct quotes), (3) which
is most recent / authoritative, (4) suggested phrasing if you had to
summarize the consensus. Flag if a key source is behind a paywall and
unreadable.
```

**When Not to Use It**: All 3 papers are by the same author or lab. There is no real multi-perspective comparison.

---

### Recipe 8: Release commit security audit

**Scenario**: You are about to ship v1.0 or a major version and want one final security pass.

**Subagent**: `code-reviewer`

**Prompt Template**:
```
Pre-release security audit for <release-tag> (use git log to find the
relevant commit range since last release). Check: (1) hardcoded
credentials / API keys, (2) eval() / exec() / shell injection risks,
(3) deprecated dependencies with known CVEs, (4) any auth / session
handling changes since last release, (5) public API surface changes
(breaking? documented?). Per-category PASS/FAIL + remediation per
finding.
```

**When Not to Use It**: A patch release or hotfix that changes one line. Manual review takes < 1 minute.

---

### Recipe 9: Assess the blast radius of an architecture change

**Scenario**: You want to change a base class or shared utility, but you do not know how many files it will affect.

**Subagent**: `Plan`

**Prompt Template**:
```
Assess the blast radius of changing <component>. Report: (1) direct
dependents (which files import this), (2) indirect dependents (transitive
imports), (3) tests that gate the change, (4) suggested rollout order
(safest → riskiest), (5) feature flag / kill switch strategy if available.
Don't make the change yet — just the impact analysis.
```

**When Not to Use It**: The change only affects internals of one file. There is no blast-radius problem.

---

### Recipe 10: Spawn parallel subagents for the same task across multiple targets

**Scenario**: Four branch files all need the same “academic-style audit,” and you want to run all four in parallel.

**Subagent**: `general-purpose` × N (spawn several at the same time)

> 💡 **How to spawn several at the same time**: in the Claude Code conversation, **enter the prompt below 4 times in a row** (changing `<file-path>` each time). Claude Code will run them in parallel automatically. You do not need to wait for the first subagent to finish before entering the second prompt. That is the practical workflow for “parallel spawn.”

**Prompt Template** (change `<file-path>` each time):
```
Audit `<file-path>` for academic-style issues: (1) over-engineering
jargon without first-use explanation, (2) clarity (long sentences,
vague pronouns), (3) unsupported % claims, (4) persona-fit (wrong
technical level for the file's stated target audience — see the
file's banner / intro callout for who it's for). Report 4-category
PASS/FAIL + fix-list with line numbers. Under 500 words.
```

**When Not to Use It**: There is only one target. Invoke one subagent directly; do not over-orchestrate.

---

### Recipe 11: Find similar implementations across repos

**Scenario**: You saw a pattern in one repo and want to know whether another repo has a similar implementation.

**Subagent**: `Explore`

**Prompt Template**:
```
In <repo-path>, search for code patterns similar to: <description of
pattern, e.g., "retry decorator with exponential backoff">. Report:
(1) up to 5 candidates with file:line, (2) brief description of each,
(3) which is most idiomatic for this codebase's style.
```

**When Not to Use It**: You have a specific function name to find. Use Recipe 6 / `Explore` with a precise grep; it will be faster.

---

### Recipe 12: LLM-as-judge eval (structured PASS / FAIL)

**Scenario**: You ran 100 test cases and need to judge whether each output meets the spec, without reading them all manually.

**Subagent**: `general-purpose`

**Prompt Template**:
```
Evaluate the agent outputs in <eval-file.jsonl> against the spec stated
in the file's first 5 lines (or in <spec-file.md>). For each row: PASS /
FAIL with 1-sentence reason. Aggregate: pass rate + top-3 failure modes.
Output as structured JSON: {"case_id": "...", "verdict": "PASS|FAIL",
"reason": "..."}.
```

**When Not to Use It**: There are < 5 cases; read them yourself. Or the evaluation requires subjective judgment; an LLM judge is not reliable enough.

---

### Recipe 13: UI component design / accessibility audit

**Scenario**: You wrote a React component and want to confirm ARIA, keyboard navigation, and responsive behavior are all correct.

**Subagent**: `frontend-developer`

**Prompt Template**:
```
Audit <component-file> for: (1) ARIA roles + labels (screen reader
compatibility), (2) keyboard navigation (tab order, Enter / Esc / arrows
behavior), (3) responsive breakpoints (mobile 360px / tablet 768px /
desktop 1280px), (4) color contrast (WCAG AA), (5) touch target size
(≥ 44px). Report per-category findings + fixes.
```

**When Not to Use It**: Pure backend or CLI tooling. There is no UI to audit.

---

### Recipe 14: Ask how to use a Claude Code feature

**Scenario**: You forgot how to configure hooks, forgot the frontmatter fields for slash commands, or want to look up documentation.

**Subagent**: `claude-code-guide`

**Prompt Template**:
```
How do I <specific Claude Code feature question, e.g., "configure a
PreToolUse hook to block dangerous bash commands">? Show: (1) minimum
config in settings.json, (2) example hook script (Python or shell),
(3) 1 common gotcha, (4) where in the official docs to read more.
```

**When Not to Use It**: You have already written this a few times. Looking at your own `~/.claude/settings.json` example is faster.

---

### Recipe 15: Implement React form validation logic

**Scenario**: You need to build a sign-up form with email format validation, password strength, and real-time validation.

**Subagent**: `frontend-developer`

**Prompt Template**:
```
Implement a React sign-up form with: (1) email format validation
(real-time, debounce 300ms), (2) password strength meter (≥ 8 chars,
mixed case, digit, symbol), (3) inline error messages with ARIA
live region, (4) submit button disabled until valid. Use <library, e.g.,
React Hook Form + Zod>. Include: component code, validation schema,
1 happy-path test, 1 error-path test.
```

**When Not to Use It**: You are not using a React stack. Use the matching Vue / Svelte subagent, or `general-purpose`.

---

## Recipe Index (by Subagent Type)

Not sure which subagent to use? Look it up by **task type**:

| Subagent | Recipes |
|---|---|
| `code-reviewer` | **1** (pre-commit review) / **4** (cross-locale parity) / **8** (release security audit)|
| `Explore` | **2** (new codebase) / **6** (find symbol) / **11** (cross-repo similar code)|
| `Plan` | **3** (refactor plan) / **9** (blast radius)|
| `general-purpose` | **5** (fact-check) / **7** (multi-paper compare) / **10** (parallel multi-target) / **12** (LLM-as-judge eval)|
| `frontend-developer` | **13** (a11y audit) / **15** (React form)|
| `claude-code-guide` | **14** (Claude Code feature lookup)|

---

## When NOT to Use a Subagent

Subagents are not free. Every dispatch **spends tokens and adds latency**. In the 4 situations below, **do not use a subagent**; doing it yourself is more efficient:

1. **The task takes < 5 minutes to do yourself** — This is overkill; the subagent overhead is not worth it.
2. **The result needs step-by-step user feedback** — A subagent is “dispatch it, let it run, get one final report.” It cannot ask you midway. Tasks that need iterative confirmation should stay in the main session.
3. **The task needs the main session’s context memory** — A subagent has an **independent context window** and cannot see earlier discussion in the main session. Tasks that depend on references like “the X we discussed earlier” are a bad fit.
4. **The task involves conversation-level judgment** — For example, “how should we weigh this architecture decision?” needs collaborative discussion and should not be thrown to a subagent.

> 💡 **A quick way to decide**: if you can describe the task as “**write a complete brief for a stranger to pick up**,” it is a good fit for a subagent. If it needs “**let’s talk this through**,” keep it in the main session.

---

## Next Steps

- **Understand the full theory** (how subagents differ from skills / MCP, and the 3 multi-agent mechanisms) → [Stage 5.5](../stages/05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature)
- **CLI daily-use playbook** → [`tracks/cli/A3-cli-production.en.md` Playbook 4](../tracks/cli/A3-cli-production.en.md#-playbook-4-dispatching-subagents-for-independent-tasks)
- **See where subagents fit in the agent paradigm map** → [`resources/agent-paradigms.en.md`](./agent-paradigms.en.md#subagent--spawning-an-agent-inside-an-agent-runtime)
- **Glossary lookup** → [`resources/glossary.en.md` § 5. Claude Code Ecosystem — Subagent](./glossary.en.md#subagent)

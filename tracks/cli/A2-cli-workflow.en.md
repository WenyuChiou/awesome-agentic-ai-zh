# A2 — Make CLI agents follow the same method every time

> [繁體中文](./A2-cli-workflow.md) | [简体中文](./A2-cli-workflow.zh-Hans.md) | **English**

> [← A1 — Safely complete your first CLI task](A1-cli-intro.en.md) · **Track A: CLI Power User** Stop 2 · [Next: A3](A3-cli-production.en.md)

This stop answers one question: **How do you make a CLI agent remember the same way of working when it enters the same repo next time?**

You will put rules that must always be known into the project-instructions file, turn frequently repeated steps into a Skill, and leave temporary tasks in a one-off prompt. It is like changing “explain everything again every day” into “the rules are on the wall, and the toolbox has an instruction card.”

## First, tell the three things apart

<table>
<thead>
<tr><th scope="col">Correct term</th><th scope="col">Plain-language meaning</th><th scope="col">When to use it</th></tr>
</thead>
<tbody>
<tr><th scope="row">Project instructions<br>project rules</th><td>Rules you read every time you enter the workshop</td><td>Put the project purpose, forbidden actions, test commands, and delivery format here</td></tr>
<tr><th scope="row">Skill</th><td>An instruction card you take out when needed</td><td>Put repeated processes such as review, release, and document cleanup here</td></tr>
<tr><th scope="row">One-off prompt<br>single-use prompt</th><td>Instructions needed only today</td><td>Put this task’s scope, inputs, and success conditions here</td></tr>
</tbody>
</table>

## Learning goals

- Use four fields to write short, clear project instructions.
- Turn a repeated review process into a read-only Skill.
- Tell apart what can be shared from filenames, permissions, and commands that must be adjusted for each tool.

<details markdown="1">
<summary>Expand time, prerequisites, environment, and cost</summary>

- **Time**: Complete CLI-5 and CLI-6 first; CLI-7 and CLI-8 can wait, so you do not need to finish everything at once.
- **Prerequisites**: Complete [A1](A1-cli-intro.en.md), know how to use `git status` and `git diff`, and have a secret-free, recoverable demo repo.
- **Environment**: Choose one primary CLI agent. Claude Code, Codex, Gemini CLI, and OpenCode do not use exactly the same filenames; the comparison below shows the differences.
- **Cost**: Writing project-instructions files and Skills does not incur model charges; asking a CLI to test them may use quota or API tokens. Check the official usage/pricing page for the current date.

If you have not completed A1, go back and run “read-only inspection → view the plan → make a small change → `git diff` → restore” once.
</details>

<details markdown="1">
<summary>Expand required reading and suggested order</summary>

1. First read the official project-instructions documentation for your primary tool: Codex uses [`AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md), Claude Code uses [`CLAUDE.md`](https://code.claude.com/docs/en/memory), Gemini CLI uses [`GEMINI.md`](https://geminicli.com/docs/cli/gemini-md/), and OpenCode V2 uses [`AGENTS.md`](https://opencode.ai/v2/docs/instructions).
2. Then read your tool’s Skill documentation: [Codex/ChatGPT](https://learn.chatgpt.com/docs/build-skills), [Claude Code](https://code.claude.com/docs/en/slash-commands), [Gemini CLI](https://geminicli.com/docs/cli/using-agent-skills/), and [OpenCode V2](https://opencode.ai/v2/docs/skills).
3. Finally, revisit [Stage 2 — Prompt Engineering](../../stages/02-prompt-engineering.en.md) and add the “task, scope, and success conditions” to your one-off prompt.
</details>

<details markdown="1">
<summary>Expand the project-instructions and Skill locations for four CLIs</summary>

Official information checked on: **2026-08-27 UTC**.

<table>
<thead>
<tr><th scope="col">Tool</th><th scope="col">Project instructions</th><th scope="col">Project Skill</th><th scope="col">What to note</th></tr>
</thead>
<tbody>
<tr><th scope="row">Codex</th><td><code>AGENTS.md</code></td><td><code>.agents/skills/&lt;name&gt;/SKILL.md</code></td><td>Rules are layered by directory; the closer rule loads later</td></tr>
<tr><th scope="row">Claude Code</th><td><code>CLAUDE.md</code></td><td><code>.claude/skills/&lt;name&gt;/SKILL.md</code></td><td>Old <code>.claude/commands/</code> remains compatible, but new workflows should prefer Skills</td></tr>
<tr><th scope="row">Gemini CLI</th><td><code>GEMINI.md</code></td><td><code>.agents/skills/&lt;name&gt;/SKILL.md</code> or <code>.gemini/skills/…</code></td><td>Skill activation asks for consent; do not put secrets in a Skill</td></tr>
<tr><th scope="row">OpenCode V2</th><td><code>AGENTS.md</code></td><td><code>.agents/skills/&lt;name&gt;/SKILL.md</code> or <code>.opencode/skills/…</code></td><td>V2 does not use the old-document <code>CLAUDE.md</code> fallback</td></tr>
</tbody>
</table>

The common part is what you need to explain; filenames, search locations, permissions, and extra settings differ. Do not treat one tool’s special feature as something every CLI has.
</details>

<a id="cli-5"></a>
### Hands-on exercise CLI-5: Make a minimal project-rules card

**Outcome:** Every time the CLI agent enters the repo, it knows what the project does, what it must not touch, how to verify changes, and what to report when finished.

First choose the project-instructions file for your tool from the comparison above, then add these four things:

```markdown
# Project rules

- Purpose: This is a practice documentation repo.
- Do not: Do not delete files, read secrets, or auto-commit or push.
- Verification: Run `git diff --check` after changes.
- Report: Explain what changed, the verification results, and what remains unhandled.
```

This card should contain only what must be known every time. Do not pack long tutorials, API references, or processes you use only occasionally into it.

<details markdown="1">
<summary>Expand CLI-5 creation and verification steps</summary>

1. Create your primary tool’s project-instructions file in a clean demo repo. Run `git status --short` first so you do not overwrite someone else’s unfinished changes.
2. Replace the four fields above with real content for this demo repo. Commands must be copyable; do not write vague instructions such as “fix the formatting” when success cannot be checked.
3. Open a new CLI session and ask it to read only the rules and restate them in its own words. If it cannot find the file, check the official filename and loading scope first.
4. Give it a test that touches a forbidden action, such as “commit this change directly.” The correct result is for the agent to stop or ask first, not commit by itself.
5. Run `git status --short -- <rules-file-path>` first to see whether the rules file is old or new.
   - Existing file: inspect it with `git diff -- <rules-file-path>`. Use `git restore -- <rules-file-path>` only if that exact file was clean before the exercise.
   - New file: Git shows `??`; `git restore` cannot remove it. You may keep it as the exercise result. To discard it, verify the full path, delete only that file with your file manager, and run `git status --short -- <rules-file-path>` again.

No line count can guarantee that rules are good. Keep only content that changes behavior; move a section used only for a specific task into a Skill or another on-demand document.
</details>

<a id="cli-6"></a>
### Hands-on exercise CLI-6: Turn a repeated review into a Skill

**Outcome:** You can ask the agent to run the same read-only review and output `PASS` or concrete problems without committing, pushing, or deploying by itself.

Claude Code uses `.claude/skills/review-changes/SKILL.md`; Codex, Gemini CLI, and OpenCode can use `.agents/skills/review-changes/SKILL.md`. After creating the file, put in:

```markdown
---
name: review-changes
description: Review the current git diff and report concrete risks. Use when the user asks to review local changes.
---

1. Read `git diff --no-ext-diff HEAD` without changing files.
2. Check for secrets, unsafe commands, broken links, and missing verification.
3. Report `PASS` when no problem is found; otherwise list each problem with its file and reason.
4. Do not edit, commit, push, deploy, or send messages.
```

`name` is the instruction-card name; `description` tells the agent when to take the card. The body is the set of steps to follow.

<details markdown="1">
<summary>Expand CLI-6 testing, permissions, and compatibility notes</summary>

1. Read `SKILL.md` all the way through first, confirming that it does not download unfamiliar programs, read secrets, or change external systems.
2. Make a small documentation change in the demo repo, but do not commit it. Ask the agent to “review my local changes” and observe whether it finds the Skill; you can also enable it manually according to the tool’s documentation.
3. Compare the report with `git diff`. Run `git status --short` after testing to confirm that the Skill did not quietly change files.
4. To share one Skill across multiple CLIs, share the core content above first, then adjust the folders, permissions, and tool-specific frontmatter for each tool. Unknown fields may be ignored; do not assume every setting is valid everywhere.

Claude Code’s `.claude/commands/<name>.md` can still create a same-named `/name`, but Skills already include custom commands and support attached files and on-demand loading. This tutorial uses Skills; understand legacy commands only when maintaining an older project.
</details>

<a id="cli-7"></a>
### Hands-on exercise CLI-7: Break a large task into visible small steps

**Outcome:** You can split a recoverable documentation task into “inventory → plan → modify → verify,” with a visible result at each step.

<details markdown="1">
<summary>Expand CLI-7 comparison exercise and multi-agent extension</summary>

Choose a small task, such as “add the same run command to two README files.” The first time, ask the agent for a plan without changing files; the second time, ask it to inventory the two files, list the differences, make the change, run `git diff --check`, and report what remains unhandled.

When comparing the two results, ask only: Were any files missed? Can the changes be recovered? Did verification actually run? Do not assign every small step to a different agent just to make the process look impressive. If tasks must wait for one another, touch the same batch of files, or have unclear success conditions, start with a single agent.

The complete subagent, agent team, background-work, and review processes are in [Stage 5.5](../../stages/05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature). A2 only practices making the work clear.
</details>

<a id="cli-8"></a>
### Hands-on exercise CLI-8: Make a portable prompt comparison card

**Outcome:** You can keep the same task core while clearly marking which filenames, permissions, commands, and activation methods must change when you switch tools.

<details markdown="1">
<summary>Expand CLI-8 cross-tool testing steps</summary>

1. Put only four fields in the shared core: task, scope, forbidden actions, and success conditions.
2. Run it once in a clean demo repo with the first CLI, recording the CLI version, model/provider, permission settings, and `git diff`.
3. Restore the changes, then switch to the second CLI. Do not let two file-writing sessions operate on the same directory at the same time.
4. Also record the differences: project-instructions filename, Skill location, shell/sandbox permissions, tool names, login, and cost.

“Portable” means the core meaning is easy to carry over; it does not mean the whole text and settings can be copied without changes. If the second tool has no same-named feature, return to the success conditions and choose a method it actually supports.
</details>

## Self-check before A3

- [ ] I can distinguish project instructions, Skill, and one-off prompt in my own words.
- [ ] My project-rules card states the purpose, forbidden actions, verification command, and delivery format, and the agent can read it.
- [ ] My review Skill reads changes only; after testing, `git status --short` shows no unexpected modifications.
- [ ] I know that a “shared core” does not mean every CLI has the same filenames and permissions.

Once all four are done, move on to [A3 — Connect a CLI agent to a safe production workflow](A3-cli-production.en.md). If not, return to the demo repo and repeat CLI-5 or CLI-6; you do not need to read every supplement first.

<details markdown="1">
<summary>Expand the complete learning resource table (16 entries)</summary>

The resources below are divided into five groups by purpose. Each group shows its category only once so repeated text does not stretch the table.

<table>
<thead>
<tr><th scope="col">Type</th><th scope="col">Resource</th><th scope="col">What to look at first</th><th scope="col">When it is useful</th><th scope="col">Source</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Official project instructions</th><td>Codex <code>AGENTS.md</code></td><td>Layered loading and precedence</td><td>Writing repo rules for Codex</td><td><a href="https://learn.chatgpt.com/docs/agent-configuration/agents-md">Official docs</a></td></tr>
<tr><td>Claude Code <code>CLAUDE.md</code></td><td>When to put something in rules and when to move it to a Skill</td><td>Writing persistent rules for Claude Code</td><td><a href="https://code.claude.com/docs/en/memory">Official docs</a></td></tr>
<tr><td>Gemini CLI <code>GEMINI.md</code></td><td>Directory scope and loading method</td><td>Adding project context for Gemini CLI</td><td><a href="https://geminicli.com/docs/cli/gemini-md/">Official docs</a></td></tr>
<tr><td>OpenCode V2 <code>AGENTS.md</code></td><td>V2 merging and nested discovery</td><td>Writing rules for OpenCode V2</td><td><a href="https://opencode.ai/v2/docs/instructions">Official docs</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Official Skill docs</th><td>Codex/ChatGPT Build skills</td><td><code>SKILL.md</code> structure and loading location</td><td>Making a reusable Codex process</td><td><a href="https://learn.chatgpt.com/docs/build-skills">Official docs</a></td></tr>
<tr><td>Claude Code Skills</td><td>On-demand loading, legacy commands, and permissions</td><td>Making a Claude Code Skill</td><td><a href="https://code.claude.com/docs/en/slash-commands">Official docs</a></td></tr>
<tr><td>Gemini CLI Agent Skills</td><td>Discovery, installation consent, and activation consent</td><td>Managing Gemini CLI Skills</td><td><a href="https://geminicli.com/docs/cli/using-agent-skills/">Official docs</a></td></tr>
<tr><td>OpenCode V2 Agent Skills</td><td>Supported locations, frontmatter, and permission</td><td>Making an OpenCode Skill</td><td><a href="https://opencode.ai/v2/docs/skills">Official docs</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Standards and readable examples</th><td>Agent Skills specification</td><td>Minimum requirements for a shared format</td><td>Making the core content easier to carry across tools</td><td><a href="https://agentskills.io/specification">Standard</a></td></tr>
<tr><td><code>anthropics/claude-plugins-official</code></td><td>Skills and commands inside official plugins</td><td>Seeing how a Skill is packaged for sharing</td><td><a href="https://github.com/anthropics/claude-plugins-official">GitHub repo</a></td></tr>
<tr><td><code>mattpocock/skills</code></td><td>Short Skill examples used in engineering work</td><td>Comparing different writing styles</td><td><a href="https://github.com/mattpocock/skills">GitHub repo</a></td></tr>
<tr><td><code>obra/superpowers</code></td><td>How real workflows are split into Skills</td><td>After completing your first Skill</td><td><a href="https://github.com/obra/superpowers">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Indexes and prompt practice</th><td><code>hesreallyhim/awesome-claude-code</code></td><td>Finding Claude Code resources by type</td><td>When you know the need and want more examples</td><td><a href="https://github.com/hesreallyhim/awesome-claude-code">GitHub repo</a></td></tr>
<tr><td><code>anthropics/prompt-eng-interactive-tutorial</code></td><td>Comparing prompt approaches step by step</td><td>When the shared core in CLI-8 is unclear</td><td><a href="https://github.com/anthropics/prompt-eng-interactive-tutorial">Official GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Repo context tools</th><td><code>yamadashy/repomix</code></td><td>Creating a one-off codebase snapshot</td><td>When you need to organize repo contents for an agent</td><td><a href="https://github.com/yamadashy/repomix">GitHub repo</a></td></tr>
<tr><td><code>langchain-ai/openwiki</code></td><td>Creating a continuously updated repo wiki</td><td>When a large repo needs on-demand document lookup</td><td><a href="https://github.com/langchain-ai/openwiki">GitHub repo</a></td></tr>
</tbody>
</table>
</details>

<details markdown="1">
<summary>Expand common questions and fixes</summary>

- **The rules are long, but the agent still misses them**: Delete background stories and repeated sentences first, keeping only observable behavior. Safety checks that must run every time should use the tool’s hook/policy instead of relying only on text reminders.
- **The Skill does not appear**: Check the folder, the capitalization of `SKILL.md`, YAML frontmatter, and the locations supported by the tool, then reload or reopen the session according to the official method.
- **The Skill performs a dangerous action by itself**: Change deploy, send, commit, and push to actions that users must explicitly enable, and test with a read-only version first. Read all third-party Skill content and scripts before using it.
- **The same Skill breaks in another CLI**: Keep the shared goal and steps, then compare the frontmatter, permissions, and tool names recognized by that tool; do not guess.
- **There is too much project information**: Treat project instructions as a map only; put details in `docs/`, the Skill’s `references/`, or another on-demand document. Longer rules are not automatically more reliable.
</details>

> Safety baseline: Rules and Skills are text instructions, not absolute protection. Do not put API keys, tokens, or personal data in them. Any workflow that writes files, commits, pushes, deploys, or calls an external service needs a visible permission boundary and verification steps.

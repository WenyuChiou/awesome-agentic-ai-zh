# Extension Path: For Developers

> [繁體中文](./for-developer.md) | [简体中文](./for-developer.zh-Hans.md) | **English**

[← Back to the main route](../README.en.md)

<!-- freshness: canonical=branches/for-developer.md; verified_on=2026-08-29; scope=coding-agents,tool-identity,permissions,sandboxing,project-status; max_age_days=90 -->

<a id="use-cases-developer-scenarios--how-ai-helps"></a>
## 📌 What this path helps you do

An AI coding assistant reads files, edits code, and runs commands. It is fast and can be wrong. This path teaches you to narrow the task, understand each change, and let a person decide whether to keep it.

Recommended route: `A1 → A2 → Stage 5 core 5.1–5.4 → A3`. Progress through [A1](../tracks/cli/A1-cli-intro.en.md), [A2](../tracks/cli/A2-cli-workflow.en.md), [Stage 5](../stages/05-claude-code-ecosystem.en.md), and [A3](../tracks/cli/A3-cli-production.en.md); [Stage 8](../stages/08-agent-interfaces.en.md) is recommended but does not block starting this path. Track B readers can start with [Stage 7](../stages/07-multi-agent-production.en.md).

## 🎯 Learning goals

After this page, you can:
1. Separate what a tool is from the surface where you use it.
2. Limit files, commands, and network access before the tool acts.
3. Manage a small change with a diff, test, human review, and rollback.
4. Check code quality, agent behavior, and production telemetry separately.

<a id="coding-agents"></a>
## 🧩 Eight core terms

- **IDE／Surface (Integrated Development Environment / interface)**: an IDE is a code workbench; a Surface is where you operate a tool, such as CLI, IDE, desktop, or cloud. One tool can have many Surfaces; looking like an IDE does not mean it only works in an IDE.
- **Coding Agent／Harness**: a Coding Agent reads code, uses tools, edits files, and continues from results. A Harness connects model, tools, rules, and execution loops. They may be in one product but are not the same thing.
- **Provider／Router**: a Provider supplies model services; a Router sends requests to one or more Providers. A Router is not a model and does not manage repo permissions.
- **Model／Runtime**: a Model generates the next content; a Runtime runs it locally or in a service. A local Runtime is not a coding agent.
- **Sandbox**: a limited area for running code. It reduces the blast radius but is not a perfect guarantee.
- **Approval**: a person explicitly permits a high-risk action. A passing Test does not grant push, merge, or deploy permission.
- **Diff／Rollback**: a Diff shows what changed; Rollback reverses the unwanted change. Read the Diff first so you know which files Rollback should touch.
- **Eval／Observability**: Eval tests quality with fixed cases; Observability records traces, logs, cost, and errors during execution.

### Do not mix up OpenCode, Pi, OpenRouter, and Ollama

<div align="center" markdown="1">

| Name | Core identity | Plain-language description |
|:---|:---|:---|
| OpenCode | Coding Agent／Harness | Reads, edits, and tests in a code project |
| Pi | Coding Agent／Harness | Adds extensions, skills, or RPC to a small core |
| OpenRouter | API Router | Sends model requests to Providers; does not edit your repo |
| Ollama | Local Model Runtime | Runs models and an API locally; is not itself a Coding Agent |

</div>

**OpenCode／Pi do the work, OpenRouter routes requests, and Ollama runs local models.**

<a id="code-review"></a>
## 🛠 First exercise: make one small, reversible change

Use a disposable demo repo or a new branch. Paste this to a Coding Agent:
```text
First make a read-only plan; do not modify any files.
Task: find one sentence in README.md that could be clearer without changing its technical meaning.
Report which sentence, why it is small scope, which test or documentation check to run, and how to rollback.
Before my explicit human Approval, do not write files. After approval, modify only README.md.
Show git diff -- README.md and report the Test result. Do not push, merge, or deploy.
```
Read the plan and approve it as a human. After the change, run:

```powershell
git diff -- README.md
# Then run this repository's documentation test or smallest relevant test
```

If wrong, confirm README.md has no other work and Rollback only this exercise’s change; never clear the whole worktree.

<a id="recommended-tools"></a><a id="tier-progression"></a>
## 📚 Choose an entry point

<div align="center" markdown="1">

| What you want | Start with | Why |
|:---|:---|:---|
| Learn permission and sandbox workflows | [Claude Code](https://code.claude.com/docs/en/overview) | Its docs separate permissions, isolation, and Surfaces |
| Work through app, CLI, IDE, or cloud | [OpenAI Codex](https://github.com/openai/codex) | One Coding Agent works across multiple entry points |
| Give a GitHub issue to a cloud agent | [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent) | Understand cloud-agent versus IDE-agent mode |
| Use an open, Provider-flexible tool | [OpenCode](https://github.com/anomalyco/opencode) | Keep Agent, Provider, and Router distinct |
| Start in an IDE with step-by-step Approval | [Cline](https://github.com/cline/cline) | Practice approving tools, files, and browser actions |

</div>

Do not ask only “which is strongest?” Ask what files and commands it can access, whether it can connect to the network, who approves high-risk actions, and how failure is reversed.

## 📖 Required reading

Read in order, answering one question for each:
1. [Claude Code permissions](https://code.claude.com/docs/en/permissions): what do `allow`, `ask`, and `deny` mean?
2. [OpenAI Codex agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security): how do Sandbox, Approval, and network controls work together?
3. [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent): where do cloud and IDE agent modes run?
4. [Pi — Permissions & Containerization](https://github.com/earendil-works/pi#permissions--containerization): who is responsible without a built-in permission Sandbox?
5. [OpenRouter provider selection](https://openrouter.ai/docs/guides/routing/provider-selection): how does a Router select a Provider?
6. [Ollama docs](https://docs.ollama.com/): what does a Local Model Runtime provide, and what does it not provide?

<a id="curated-projects"></a><a id="community-note"></a>
## ⭐ Curated tools and projects
<small>Tool identity, Surface, license, and repository status were checked against official documentation and the GitHub API on 2026-08-29 UTC. Ratings are editorial ratings for this map, not GitHub stars or performance rankings.</small>

<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="Resources by category, use and limits">
<table align="center">
<thead><tr><th scope="col">Group</th><th scope="col">Project / document</th><th scope="col">Rating</th><th scope="col">Use</th><th scope="col">Limits</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">Official / commercial Coding Agents</th><td><div data-field="entry"><strong><a href="https://code.claude.com/docs/en/overview">Claude Code</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> coding agent</div><div data-field="surface"><strong>Main Surface:</strong>  CLI／IDE／desktop／cloud</div><div data-field="use">Permissions, sandbox, project rules, and workflow</div></td><td><div data-field="status">Commercial; keep permission prompts and start with a small repo</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/openai/codex">codex</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> coding agent</div><div data-field="surface"><strong>Main Surface:</strong>  app／CLI／IDE／cloud</div><div data-field="use">Compare local and remote operation</div></td><td><div data-field="status">Active; repository code is Apache-2.0, while app/cloud follow their service terms; do not disable required Approval or expand workspace permissions</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent">GitHub Copilot</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> coding agent／code assistant</div><div data-field="surface"><strong>Main Surface:</strong>  GitHub／IDE／CLI／app</div><div data-field="use">Move from IDE collaboration to issues, branches, and PRs</div></td><td><div data-field="status">Commercial; Cloud Agent and IDE mode have different permissions; output needs human review</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://cursor.com/docs">Cursor</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> coding agent + AI editor</div><div data-field="surface"><strong>Main Surface:</strong>  IDE／CLI／cloud／SDK</div><div data-field="use">Compare editor, background agent, and other Surfaces</div></td><td><div data-field="status">Commercial; check permissions and data boundaries per Surface</div></td></tr>
</tbody><tbody>
<tr><th scope="rowgroup" rowspan="6" align="center" valign="middle" width="80">Open-source Coding Agents／Harnesses</th><td><div data-field="entry"><strong><a href="https://github.com/anomalyco/opencode">opencode</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> coding agent／harness</div><div data-field="surface"><strong>Main Surface:</strong>  terminal／desktop</div><div data-field="use">Switch Provider or compatible endpoint</div></td><td><div data-field="status">Active; MIT; <code>AGENTS.md</code> has priority, with <code>CLAUDE.md</code> used only when absent</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/earendil-works/pi">pi</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> coding agent／harness</div><div data-field="surface"><strong>Main Surface:</strong>  terminal／SDK／RPC</div><div data-field="use">Add extensions, skills, and custom workflows to a small core</div></td><td><div data-field="status">Active; MIT; no built-in Sandbox, so isolate it yourself</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/Aider-AI/aider">aider</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> coding agent／pair programmer</div><div data-field="surface"><strong>Main Surface:</strong>  CLI</div><div data-field="use">Manage small changes with Git diff, commit, and undo</div></td><td><div data-field="status">Active; Apache-2.0; auto-commit does not skip hooks</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/aaif-goose/goose">goose</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> coding／general agent</div><div data-field="surface"><strong>Main Surface:</strong>  CLI／desktop／API</div><div data-field="use">Connect Providers, MCP, and extensions</div></td><td><div data-field="status">Active; Apache-2.0; start with low-privilege extensions</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/cline/cline">cline</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> coding agent</div><div data-field="surface"><strong>Main Surface:</strong>  IDE／CLI／SDK</div><div data-field="use">Approve tools, files, and browser actions step by step</div></td><td><div data-field="status">Active; Apache-2.0; an IDE Surface is not a safety guarantee</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/OpenHands/OpenHands">OpenHands</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> software-development agent platform</div><div data-field="surface"><strong>Main Surface:</strong>  web／CLI／SDK／cloud</div><div data-field="use">Handle a fuller issue in an isolated environment</div></td><td><div data-field="status">Active; MIT; larger tasks need checkpoints and human review</div></td></tr>
</tbody><tbody>
<tr><th scope="rowgroup" rowspan="2" align="center" valign="middle" width="80">Workflow support</th><td><div data-field="entry"><strong><a href="https://github.com/obra/superpowers">superpowers</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> workflow collection</div><div data-field="surface"><strong>Main Surface:</strong>  agent plugin／skills</div><div data-field="use">Planning, TDD, debugging, and review workflows</div></td><td><div data-field="status">Active; MIT; adapt templates to your repo gate</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/yamadashy/repomix">repomix</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> repo context packer</div><div data-field="surface"><strong>Main Surface:</strong>  CLI／MCP</div><div data-field="use">Prepare one-time codebase context</div></td><td><div data-field="status">Active; MIT; exclude secrets and unnecessary files before output</div></td></tr>
</tbody><tbody>
<tr><th scope="rowgroup" rowspan="2" align="center" valign="middle" width="80">Maintenance / history</th><td><div data-field="entry"><strong><a href="https://github.com/continuedev/continue">continue</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> coding agent</div><div data-field="surface"><strong>Main Surface:</strong>  CLI／VS Code／JetBrains</div><div data-field="use">Study the history of open-source editor-agent integration</div></td><td><div data-field="status">Read-only; Apache-2.0; official 2.0.0 is the last version and it is no longer actively maintained</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/RooCodeInc/Roo-Code">Roo Code</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐</span></td><td><div data-field="identity"><strong>Core identity:</strong> coding agent</div><div data-field="surface"><strong>Main Surface:</strong>  VS Code extension</div><div data-field="use">Study multi-mode agent design history</div></td><td><div data-field="status">Archived; Apache-2.0; use a maintained tool for new projects</div></td></tr>
</tbody></table>
</div>

<a id="other-branches-also-apply"></a>
## ✅ Completion check and next stop
- [ ] I can explain Coding Agent／Harness, Router, and Local Model Runtime.
- [ ] The tool gives a read-only plan and changes one file only after human Approval.
- [ ] I read the complete Diff and ran the relevant Test.
- [ ] I know how to Rollback only this change, and the tool did not push, merge, or deploy.

Next stop: design Skills／MCP with [Stage 5](../stages/05-claude-code-ecosystem.en.md); build Eval, Observability, and production gates with [Stage 7](../stages/07-multi-agent-production.en.md); compare CLI agents in the [CLI agent guide](../resources/cli-agents-guide.en.md).

<details markdown="1"><summary>⏱ Expand: time, environment, cost, and secret boundaries</summary>
The first exercise takes about 20–40 minutes. Use a disposable repo or new branch, check `git status`, and do not let an agent overwrite work from a colleague or another tool. Keep API keys in environment variables or a secret store, not prompts, README files, or commits. Disable unnecessary network, external-directory, and shell access. Cost varies with Model, Provider, input, and retries. Sandbox limits the blast radius; protect external services, credentials, and human Approval separately.
</details>
<a id="workflows-to-master-by-frequency"></a><a id="3-concrete-workflow-recipes"></a>
<details markdown="1"><summary>🧪 Expand: from daily changes to team workflows</summary>
### Daily development
`plan → human Approval → small change → diff → test → review → commit`. Every step should be stoppable.
### PR review
Treat agent advice as candidate findings; require files, behavior, reproduction, and a suggested Test. Unsupported guesses must not block.
### CI
Use read-only tokens, minimum repository permissions, and fixed inputs. Do not turn Issue, PR, or web text directly into executable commands. Keep releases, merges, and secrets behind extra Approval.
### Batch refactoring
Build baseline tests, then work by module. Each batch gets a checkpoint, Diff, and Rollback; do not hand over the whole repo at once.
</details>
<a id="common-pitfalls-anti-patterns"></a>
<details markdown="1"><summary>🧯 Expand: common mistakes, alternatives, and rollback</summary>
| Problem | Use this instead |
|---|---|
| An IDE screen makes you think the tool only works in an IDE | Separate core identity from every Surface |
| Treating OpenRouter, Ollama, and OpenCode as one category | Choose Router, Runtime, and Coding Agent separately |
| Accepting a green Test immediately | Read the Diff, confirm coverage, then approve |
| Judging safety by line count | Check scope, testability, reversibility, and readable Diff |
| Skipping hooks because Aider auto-commits | Enable required verification/hooks and follow the review gate |
| Multiple tools edit one file simultaneously | Clarify ownership, use separate worktrees, and integrate manually |
Rollback only confirmed targets after checking `git status` and Diff; never use a broad reset to erase others’ work.
</details>

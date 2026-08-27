# A3 — Connect a CLI agent to a safe team workflow

> [繁體中文](./A3-cli-production.md) | [简体中文](./A3-cli-production.zh-Hans.md) | **English**

> [← A2 — Make the CLI agent follow the same method every time](A2-cli-workflow.en.md) · **Track A: CLI Power User** Stop 3 (final)

This stop has one goal: **have a CLI agent perform a read-only check on a test PR. It may give feedback, but it must not merge, deploy, or obtain extra permissions by itself.**

## 📌 Learning Goals

After finishing, you can:

- Give an **MCP** server only one safe scope.
- Have **CI** automatically produce a reviewable suggestion on a PR.
- Use **Observability** to understand the usage, time, and result left by one run.
- Hand the A2 Skill to a teammate and let them rerun it safely.

## 🧩 Three Core Terms First

| Core term | What it is, in plain language | How A3 uses it | What it is not |
|---|---|---|---|
| **MCP (Model Context Protocol)** | A standard adapter that connects an agent to external tools or data | Give a server only one demo folder or read-only tool | Not automatically safe; permissions still decide what it can touch |
| **CI (Continuous Integration)** | A checkpoint that runs automatically when a push or PR appears | Run one read-only review automatically on a test PR | Not an auto-merge button that skips human review |
| **Observability** | A receipt plus dashcam recording that keeps what happened | Record provider, model, usage, time, result, and failure reason | Not just one total-token number or a guess about unavailable cost |

The three terms appear together but are not the same thing: MCP connects tools, CI decides when to run automatically, and observability records the evidence after a run.

## Follow the safety ladder first

1. **Read-only**: let the agent see data first, without letting it change data.
2. **Least privilege**: open only the folder, repo, tool, or token scope needed for this task.
3. **Demo repo**: test first in a disposable practice environment.
4. **Human review**: a person decides whether to use the agent’s suggestion.
5. **Only then consider writes**: auto-merge, push, and deploy are outside this stop.

<details markdown="1">
<summary>Expand for time, prerequisites, environment, and cost</summary>

- **Time**: finish the four smallest outcomes first. You can usually split them into several short practices; do not connect many services at once just to save time.
- **Prerequisites**: complete [A1](A1-cli-intro.en.md) and [A2](A2-cli-workflow.en.md), and be able to recognize the basic screens for `git status`, PRs, and GitHub Actions.
- **Environment**: a demo repo with no real secrets; use a GitHub-hosted Linux runner for the first round because a sandbox is easier to apply there.
- **Cost**: GitHub Actions, a CLI subscription, and model APIs may be billed separately. Check your own plan before running; do not treat someone else’s prices as yours.

If A2’s `review-changes` Skill cannot yet reliably output `PASS` or concrete issues, fix that first before starting A3.
</details>

## 📚 Required Reading

<details markdown="1">
<summary>Expand for required reading and reading order (checked 2026-08-27 UTC)</summary>

1. First read [MCP Connect to local servers](https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers) to learn that a server can receive only the paths you give it.
2. Then read [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) to understand least privilege and untrusted PRs first.
3. Choose one CI path:
   - Claude Code: [official GitHub Actions documentation](https://code.claude.com/docs/en/github-actions)
   - Codex: [official GitHub Action documentation](https://learn.chatgpt.com/docs/github-action)
4. When you need trace, eval, or complete production theory, continue to [Stage 7](../../stages/07-multi-agent-production.en.md) and [Stage 7.5](../../stages/07.5-advanced-agentic-concepts.en.md).

The check date means the material was checked that day; it does not mean it will never change.
</details>

## 🛠 Hands-on Exercises

<a id="cli-9"></a>
### Hands-on exercise CLI-9: Connect only one MCP server

**Outcome:** the agent can read a newly created demo folder, but it has not received access to your entire home directory, disk, real project, or secrets.

First copy the command for your computer to create `a3-mcp-demo/hello.txt`.

PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path a3-mcp-demo | Out-Null
Set-Content -LiteralPath a3-mcp-demo/hello.txt -Value 'hello from A3'
```

macOS/Linux:

```bash
mkdir -p a3-mcp-demo
printf 'hello from A3\n' > a3-mcp-demo/hello.txt
```

When connecting the official filesystem reference server to your CLI, **pass only the absolute path to this folder**.

When it works, the agent can read `hello.txt`; when asked to read a file outside the allowed scope, it should fail or ask you to grant authorization again.

<details markdown="1">
<summary>Expand for CLI-9 installation, permission tests, and the GitHub MCP extension</summary>

1. Open the configuration using the official MCP documentation for your main CLI; configuration files and commands differ between CLIs.
2. Use the official package `@modelcontextprotocol/server-filesystem`; its arguments should contain only the absolute path to `a3-mcp-demo`. Do not enter `~`, your home directory, the disk root, or the whole workspace.
3. Restart the CLI, ask it to list the demo folder, and then read `hello.txt`.
4. Ask it to read an ordinary filename outside the demo scope. The correct result is a refusal or a request to add authorization; it must not read the file secretly.
5. Remove the server configuration after practice and confirm that the CLI can no longer use it.

To read PRs or issues, use GitHub’s official [`github/github-mcp-server`](https://github.com/github/github-mcp-server) instead. Start with `--read-only`, then use toolsets or a tools allow-list to open only the capabilities you need. If you use a PAT, put it in a secure secret or environment variable, grant the smallest scope, and revoke it after practice; when OAuth is available, configure it through the host’s official process.

[`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) is useful for reading reference implementations, but its official description says they are not production-ready. The old `github` reference server has moved to the historical collection; do not use it as the current GitHub entry point.

**Cost reminder:** a local filesystem server usually has no separate charge, but the CLI or model may still cost money. A remote MCP may have its own plan too.
</details>

<a id="cli-10"></a>
### Hands-on exercise CLI-10: Give a PR one more read-only checker

**Outcome:** the test PR gets a review result; a person still decides whether to edit, merge, or deploy.

Choose Anthropic’s [`claude-code-action`](https://github.com/anthropics/claude-code-action) or OpenAI’s [`codex-action`](https://github.com/openai/codex-action). For the first round, run it only in a demo repo and branch you control, reusing A2’s [`review-changes` Skill](A2-cli-workflow.en.md#cli-6).

The success standard is not “finish within a few minutes.” It is that the workflow finishes successfully and leaves a readable result in a PR comment, job summary, or artifact.

<details markdown="1">
<summary>Expand for CLI-10 security settings and validation steps</summary>

1. Build the workflow from the provider’s official example; do not copy YAML from an unknown source.
2. Put the API key in a GitHub Actions secret. Do not write it into the workflow, prompt, repo, or log.
3. Start `GITHUB_TOKEN` at `contents: read`. Add only the necessary pull-request permission to that job when it needs to post a PR comment.
4. For Codex read-only work, use the currently supported `permission-profile: ":read-only"` setting in the official action; do not also set mutually exclusive legacy sandbox fields. For Claude Code, restrict capabilities through the official action’s permissions and allowed tools.
5. Make the prompt ask only to read the diff, list issues, and output `PASS` or concrete suggestions. State explicitly: do not edit, commit, push, merge, deploy, or send extra messages.
6. Start with a same-repo test branch that you created yourself. Do not use `pull_request_target` to check out untrusted PR code; this can expose secrets or write permissions to untrusted content.
7. Check the Actions log, review result, and repo diff. If there is any sign of secret leakage, immediately delete the log, revoke the secret, and rotate it.

GitHub recommends pinning third-party Actions in production workflows to a full commit SHA because a tag can move. The `@v1` or `@v5` forms in official documentation are useful for identifying product versions; before production use, verify and pin the trusted full SHA for that time.

**Cost reminder:** set a job timeout and concurrency to avoid hangs or duplicate triggers. Keep model APIs, provider plans, and GitHub Actions minutes separate.
</details>

<a id="cli-11"></a>
### Hands-on exercise CLI-11: Read the receipt for one run

**Outcome:** you record the provider/model, input usage, output usage, time, and result; fields you cannot obtain are clearly marked “unconfirmed” instead of guessed.

First distinguish whether you use a subscription plan or pay by API usage. When the official source provides token counts and prices, calculate cost only with this formula:

`input tokens × input price + output tokens × output price`

<details markdown="1">
<summary>Expand for the CLI-11 record card, stop rules, and observability</summary>

Start with one small task and fill in this card:

| Field | What to record |
|---|---|
| Task | What you asked the agent to do |
| Provider/model | The provider and model actually used; write unconfirmed if unavailable |
| Usage | Input/output usage; do not write only a vague “total tokens” |
| Time | The actual duration shown by the workflow or CLI |
| Result | `PASS`, an issue list, or the reason for failure |
| Cost | Calculate only when it matches official prices; otherwise write the billing method or unconfirmed |

Then set a stop rule the tool really supports, such as a job timeout, maximum retries, provider spend limit, or human confirmation before each paid step. Do not create a setting a tool will not read just to create a false sense of safety.

For comparing multiple runs, you can choose [Langfuse](https://github.com/langfuse/langfuse), [Phoenix](https://github.com/Arize-ai/phoenix), [Helicone](https://github.com/Helicone/helicone), or [promptfoo](https://github.com/promptfoo/promptfoo). First confirm where data will be sent and whether it contains the original prompt, code, or PII before deciding to connect it.

Prompt caching TTL, eligibility, and pricing vary by provider and model. Anthropic’s current documentation describes both a default 5-minute TTL and an optional 1-hour TTL; treat this as a product setting to check, not a fixed rule for every CLI.
</details>

<a id="cli-12"></a>
### Hands-on exercise CLI-12: Safely hand a Skill to a teammate

**Outcome:** a second clean demo repo can find the `review-changes` Skill, and running it makes no unexpected changes.

Put A2’s `review-changes` Skill in a version-controlled team repo and include four things: installation location, required permissions, test method, and removal method. Claude Code users can package it according to the official plugin format; other CLIs should follow their own Skill documentation.

<details markdown="1">
<summary>Expand for CLI-12 sharing, installation, and revocation steps</summary>

1. Before sharing, read `SKILL.md` and its attached scripts. Confirm that they do not download unfamiliar programs, read secrets, or change external systems.
2. Keep `skills/review-changes/SKILL.md` at the plugin root; do not package the project’s own `CLAUDE.md`, `AGENTS.md`, or secrets with it.
3. Install it in a second clean demo repo according to the tool’s documentation. Claude Code users can refer to the [Plugins documentation](https://code.claude.com/docs/en/plugins) and [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official).
4. Make a small document diff, run the Skill, and use `git status --short` to confirm that it only reviews and does not edit files.
5. Record the version or commit SHA. Read the diff before updating; when you stop using it, remove the plugin/Skill according to the documentation and confirm that the agent can no longer find it.

The core idea of a Skill can be shared, but folders, permissions, frontmatter, and installation methods may differ. Do not describe one tool’s plugin format as universal to all CLIs.

**Cost reminder:** sharing the files usually does not incur model charges, but each teammate’s Skill run may use their own subscription or API allowance.
</details>

## Remember only this production safety loop

`Define the scope → run read-only → leave a record → human judgment → recoverable`

If you have no scope, evidence, or recovery method, do not increase permissions yet. This matters more than memorizing many tool names.

### 📋 Playbook 4: Dispatching subagents for independent tasks

**Outcome:** first list the agents the current tool really provides, then delegate an independent, verifiable task; do not assume every computer has an agent with the same name.

<details markdown="1">
<summary>Expand for Playbook 4 and the other six advanced playbooks</summary>

**Playbook 4 — subagent:** a subagent is an independent helper dispatched by the main session. Claude Code currently has built-in subagents such as `Explore`, `Plan`, and `general-purpose`; the available list still depends on the version, session, and settings. `code-reviewer` is a **custom example** in the official documentation, not a built-in agent that every installation has. First run the tool’s agent list, then choose a read-only agent or create a restricted reviewer.

For other situations, remember one action and keep the theory in [Stage 7.5](../../stages/07.5-advanced-agentic-concepts.en.md):

- **Unclear scope:** write down paths that may and may not change; request a plan before changing files.
- **Multiple people/agents in parallel:** separate ownership and commits, then integrate at the end; do not change the same batch of files at the same time.
- **Review-agent output:** the reviewer provides evidence; it does not replace tests, branch protection, or human judgment.
- **Running an agent in CI:** start with read-only access and a trusted trigger; model fallback must be explicitly configured and revalidated, never switched silently.
- **Cost control:** use actual usage, timeouts, retries, and provider limits; say when data is unavailable.
- **Preventing rule drift:** deliberately make a small safe failure to confirm that the gate really blocks it; rule text by itself is not evidence.

Further reading: [`resources/subagent-cookbook.en.md`](../../resources/subagent-cookbook.en.md) and [Stage 5.5](../../stages/05-claude-code-ecosystem.en.md#55--subagents-claude-codes-native-multi-agent-mechanism--2025-new-feature). These pages will be rechecked in their own layer later; before using agent names, follow the official documentation and the actual list available to you.
</details>

## 🎯 Curated Projects

Editorial ratings are learning-map guidance, not GitHub stars. `⭐⭐⭐⭐⭐` marks a must-read or must-run entry for this path; it does not mean the tool is always safe or that production can skip its own threat model.

<details markdown="1">
<summary>Expand the complete learning resource table (18 items, checked 2026-08-27 UTC)</summary>

<table>
<thead>
<tr><th scope="col">Type</th><th scope="col">Resource</th><th scope="col">Read first</th><th scope="col">When to use</th><th scope="col">Rating</th><th scope="col">Source</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Safe MCP connections</th><td>MCP Connect to local servers</td><td>Allowed directories and explicit authorization</td><td>Connecting a local server for the first time</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers">Official docs</a></td></tr>
<tr><td>MCP Security Best Practices</td><td>Least privilege, scopes, and token handling</td><td>Before connecting an account or remote service</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices">Official docs</a></td></tr>
<tr><td><code>github/github-mcp-server</code></td><td><code>--read-only</code>, toolsets, and tools allow-list</td><td>Reading GitHub PRs/issues</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/github/github-mcp-server">GitHub repo</a></td></tr>
<tr><td><code>modelcontextprotocol/servers</code></td><td>Reference implementations and the not-production-ready warning</td><td>Learning the protocol or reading example code</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/modelcontextprotocol/servers">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">CI and PR review</th><td>GitHub Actions Secure Use</td><td>Least privilege, untrusted input, and pinning SHAs</td><td>Before writing any workflow with secrets</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://docs.github.com/en/actions/reference/security/secure-use">Official docs</a></td></tr>
<tr><td>Claude Code GitHub Actions</td><td>Official setup, permissions, and troubleshooting</td><td>Running Claude Code in CI</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://code.claude.com/docs/en/github-actions">Official docs</a></td></tr>
<tr><td><code>anthropics/claude-code-action</code></td><td>Official examples and action inputs</td><td>Starting from an executable template</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/anthropics/claude-code-action">GitHub repo</a></td></tr>
<tr><td>Codex GitHub Action</td><td>Permission profile, trigger, and output</td><td>Running Codex in CI</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://learn.chatgpt.com/docs/github-action">OpenAI official docs</a></td></tr>
<tr><td><code>openai/codex-action</code></td><td><code>:read-only</code> and safety strategy</td><td>Checking the latest inputs and examples</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/openai/codex-action">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Observability and evaluation</th><td><code>langfuse/langfuse</code></td><td>Traces, usage, and eval</td><td>Viewing multiple runs together</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/langfuse/langfuse">GitHub repo</a></td></tr>
<tr><td><code>Arize-ai/phoenix</code></td><td>Tracing and evaluation</td><td>Observing an AI system with open source</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/Arize-ai/phoenix">GitHub repo</a></td></tr>
<tr><td><code>Helicone/helicone</code></td><td>Proxy/gateway data flow and privacy boundary</td><td>Collecting request records from a gateway</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/Helicone/helicone">GitHub repo</a></td></tr>
<tr><td><code>promptfoo/promptfoo</code></td><td>Eval cases and CI regression</td><td>Comparing whether a change made things worse</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/promptfoo/promptfoo">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="3">Sharing Skills/plugins</th><td>Claude Code Plugins</td><td>Plugin structure, installation, and marketplace</td><td>Packaging for Claude Code</td><td>⭐⭐⭐⭐</td><td><a href="https://code.claude.com/docs/en/plugins">Official docs</a></td></tr>
<tr><td><code>anthropics/claude-plugins-official</code></td><td>Officially managed plugin directory</td><td>Finding readable official examples</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/anthropics/claude-plugins-official">GitHub repo</a></td></tr>
<tr><td><code>obra/superpowers-marketplace</code></td><td>Minimal marketplace shell</td><td>Understanding curator-only structure</td><td>⭐⭐⭐</td><td><a href="https://github.com/obra/superpowers-marketplace">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Directories and complete examples</th><td><code>wong2/awesome-mcp-servers</code></td><td>Classify first, then check sources and permissions one by one</td><td>When official resources lack the server you need</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/wong2/awesome-mcp-servers">GitHub repo</a></td></tr>
<tr><td><code>obra/superpowers</code></td><td>How Skills, rules, and workflows fit together</td><td>Looking at a complete example after the minimal workflow works</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/obra/superpowers">GitHub repo</a></td></tr>
</tbody>
</table>

The directory only helps you “find candidates”; it does not guarantee a candidate is safe. Before installing any MCP, Action, Skill, or plugin, check its source, permissions, recent maintenance, and removal method again.
</details>

## ✅ Track A Completion Check

- [ ] MCP received only the demo folder or a minimal read-only toolset.
- [ ] The PR workflow only gives feedback; it does not auto-merge, push, or deploy.
- [ ] Secrets are not in the repo, prompt, or log; the workflow uses least privilege.
- [ ] I can point to the result and usage for one run; unavailable data was not guessed.
- [ ] A teammate can run the Skill in a clean demo repo, and `git status` shows no unexpected changes afterward.

Once all five are true, Track A is complete. Then choose by purpose: return to [Stage 3](../../stages/03-tool-use-and-hello-agent.en.md) to build an application; go to [Stage 7](../../stages/07-multi-agent-production.en.md) to study production systems; or read [Stage 7.5](../../stages/07.5-advanced-agentic-concepts.en.md) to understand agent concepts more deeply.

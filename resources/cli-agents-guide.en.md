> [繁體中文](./cli-agents-guide.md) | [简体中文](./cli-agents-guide.zh-Hans.md) | **English**

# CLI Agents Reference Guide

> [← Back to the main path README](../README.en.md) · [A1: Safely run your first small task](../tracks/cli/A1-cli-intro.en.md)

This reference doc organizes 9 terminal CLIs around “what do you want to do now?” and checkable official sources. It does not score tools or choose an entry point by popularity or subjective ranking; first identify the role, then choose based on your provider, sign-in method, and safety boundaries.

## First separate the roles: an agent is not a model or API

<table align="center">
<thead>
<tr><th scope="col">Type</th><th scope="col">What it does</th><th scope="col">Examples</th><th scope="col">Do not confuse it with</th></tr>
</thead>
<tbody>
<tr><th scope="row">LLM</th><td>Generates text, code, or tool calls</td><td>Claude, GPT, Gemini</td><td>The model does not automatically have access to files on your computer</td></tr>
<tr><th scope="row">Provider API</th><td>Provides requests, authentication, and billing for one model provider</td><td>Anthropic API, OpenAI API, Gemini API</td><td>An API is not a terminal workbench</td></tr>
<tr><th scope="row">Router</th><td>Forwards requests to multiple providers</td><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a></td><td>A Router does not manage files or command permissions on an agent’s behalf</td></tr>
<tr><th scope="row">Coding agent / harness</th><td>Reads files, edits, runs commands, and reports results in the terminal</td><td>Claude Code, Codex, OpenCode, Pi</td><td>Its approval, sandbox, and project trust settings need separate checking</td></tr>
<tr><th scope="row">Local runtime</th><td>Loads and runs a model locally</td><td><a href="https://ollama.com/">Ollama</a></td><td>It can be called by an agent, but it is not a coding agent</td></tr>
</tbody>
</table>

## Find an entry point from your situation

<table align="center">
<thead>
<tr><th scope="col">Your situation</th><th scope="col">What to check first</th><th scope="col">Differences to record</th></tr>
</thead>
<tbody>
<tr><th scope="row">You already have an account with a model service</th><td>A CLI from that ecosystem, such as Claude Code, Codex, or Gemini CLI</td><td>Sign-in flow, approval, sandbox, and usage page</td></tr>
<tr><th scope="row">You need to switch providers</th><td>OpenCode, goose, Aider, Hermes Agent, or Pi</td><td>Supported endpoints, model IDs, and where API keys are stored</td></tr>
<tr><th scope="row">You want to route multiple providers through one place</th><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a> paired with an agent</td><td>The actual provider route, data policy, usage, and billing</td></tr>
<tr><th scope="row">You want to practice locally</th><td><a href="https://ollama.com/">Ollama</a> paired with an agent that supports a compatible API</td><td>Whether the model is local, and whether the agent can still run shell commands / write files</td></tr>
</tbody>
</table>

## 9 CLI tools

The tool facts below are visible. Record the “checked on” date alongside your installed version. Official data checked on: **2026-08-30 UTC**.

> **Stable channels and a scoped check (2026-10-11 UTC):** Use an official stable release as the beginner baseline. Use alpha, preview,
> or nightly only to test a specific capability in an isolated demo repo; read release notes, pin the exact version, and keep a rollback path.
> The official release pages mark [Codex CLI `0.163.0-alpha.5`](https://github.com/openai/codex/releases/tag/rust-v0.163.0-alpha.5) and
> [Gemini CLI `0.65.0-nightly.20261010.g9b6e0265d`](https://github.com/google-gemini/gemini-cli/releases/tag/v0.65.0-nightly.20261010.g9b6e0265d) as pre-releases,
> so neither is a stable beginner baseline. This checks only release-channel labels; the full table’s last complete check remains 2026-08-30 UTC.

<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="CLI tools and learning resources">
<table align="center">
<thead><tr><th scope="col">Group</th><th scope="col">Project / document</th><th scope="col">Rating</th><th scope="col">Use</th><th scope="col">Limits</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">Official model ecosystems</th><td><div data-field="entry"><strong>Claude Code</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>Who it currently suits:</strong> People who want to use the Anthropic ecosystem in the terminal</div><div data-field="models"><strong>Model / provider choices:</strong> Claude; Anthropic API</div></td><td><div data-field="auth"><strong>Sign-in method:</strong> Claude account or Anthropic API key</div><div data-field="safety"><strong>Safe starting point:</strong> Use a demo repo; keep the permission prompt</div><div data-field="status"><strong>Status:</strong> One of Anthropic’s official terminal, desktop, IDE, and cloud interfaces</div><div data-field="sources"><strong>Official sources:</strong> <a href="https://code.claude.com/docs/en/overview">docs</a> · <a href="https://github.com/anthropics/claude-code">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>Codex CLI</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>Who it currently suits:</strong> People who want to use OpenAI / ChatGPT sign-in in the terminal</div><div data-field="models"><strong>Model / provider choices:</strong> GPT family; OpenAI API</div></td><td><div data-field="auth"><strong>Sign-in method:</strong> ChatGPT sign-in or OpenAI API key</div><div data-field="safety"><strong>Safe starting point:</strong> Use the default approval and workspace sandbox; inspect the diff first</div><div data-field="status"><strong>Status:</strong> OpenAI’s open-source terminal coding agent</div><div data-field="sources"><strong>Official sources:</strong> <a href="https://learn.chatgpt.com/docs/codex/cli">docs</a> · <a href="https://github.com/openai/codex">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>Gemini CLI</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>Who it currently suits:</strong> People with Google authentication who want Gemini in the terminal</div><div data-field="models"><strong>Model / provider choices:</strong> Gemini; Google AI API or Vertex AI</div></td><td><div data-field="auth"><strong>Sign-in method:</strong> Google sign-in, Gemini API key, or Vertex AI</div><div data-field="safety"><strong>Safe starting point:</strong> Use approval mode; explicitly enable <code>--sandbox</code> when needed</div><div data-field="status"><strong>Status:</strong> Google’s open-source terminal agent</div><div data-field="sources"><strong>Official sources:</strong> <a href="https://google-gemini.github.io/gemini-cli/">docs</a> · <a href="https://github.com/google-gemini/gemini-cli">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>Grok Build</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>Who it currently suits:</strong> People who want to try xAI’s Grok terminal TUI</div><div data-field="models"><strong>Model / provider choices:</strong> Grok; xAI sign-in or API key</div></td><td><div data-field="auth"><strong>Sign-in method:</strong> Interactive browser sign-in on first launch; CI can use <code>XAI_API_KEY</code></div><div data-field="safety"><strong>Safe starting point:</strong> Start in a demo repo; do not copy <code>~/.grok/auth.json</code></div><div data-field="status"><strong>Status:</strong> xAI’s official open-source TUI coding agent</div><div data-field="sources"><strong>Official sources:</strong> <a href="https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/02-authentication.md">authentication</a> · <a href="https://github.com/xai-org/grok-build">repo</a></div></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5" align="center" valign="middle" width="80">Provider-flexible</th><td><div data-field="entry"><strong>OpenCode</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>Who it currently suits:</strong> People who need to switch among multiple providers</div><div data-field="models"><strong>Model / provider choices:</strong> Multiple providers; can connect to OpenRouter or a compatible endpoint</div></td><td><div data-field="auth"><strong>Sign-in method:</strong> Configure an API key, OAuth, or environment variable for the provider</div><div data-field="safety"><strong>Safe starting point:</strong> Check permission settings first; test outside directories only in a demo repo</div><div data-field="status"><strong>Status:</strong> Open-source terminal coding agent; <code>AGENTS.md</code> has priority, with <code>CLAUDE.md</code> as a compatibility fallback when absent</div><div data-field="sources"><strong>Official sources:</strong> <a href="https://opencode.ai/docs/providers/">provider</a> · <a href="https://github.com/anomalyco/opencode">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>goose</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>Who it currently suits:</strong> People who need a CLI, desktop app, or API and want to connect tools and data sources</div><div data-field="models"><strong>Model / provider choices:</strong> 15+ providers, including Anthropic, OpenAI, Google, Ollama, and OpenRouter</div></td><td><div data-field="auth"><strong>Sign-in method:</strong> Provider API key, or ACP sign-in through some existing subscriptions</div><div data-field="safety"><strong>Safe starting point:</strong> Start with low-privilege extensions and a sandbox; do not connect production data</div><div data-field="status"><strong>Status:</strong> AAIF’s open-source local agent, with CLI, desktop, and API</div><div data-field="sources"><strong>Official sources:</strong> <a href="https://block.github.io/goose/">docs</a> · <a href="https://github.com/aaif-goose/goose">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>Aider</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>Who it currently suits:</strong> People who want to manage code changes with git diff / commit</div><div data-field="models"><strong>Model / provider choices:</strong> Multiple cloud APIs, OpenRouter, OpenAI-compatible endpoints, and local models</div></td><td><div data-field="auth"><strong>Sign-in method:</strong> Provider API key, config file, or environment variable</div><div data-field="safety"><strong>Safe starting point:</strong> Start in a clean demo repo; note Aider’s git auto-commit behavior</div><div data-field="status"><strong>Status:</strong> Open-source terminal pair-programming tool; official docs specify its git integration</div><div data-field="sources"><strong>Official sources:</strong> <a href="https://aider.chat/docs/">docs</a> · <a href="https://github.com/Aider-AI/aider">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>Pi</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>Who it currently suits:</strong> People who want to start from a small core and extend it with extensions, skills, or RPC</div><div data-field="models"><strong>Model / provider choices:</strong> Subscription providers, API-key providers, custom providers; can connect to a local endpoint</div></td><td><div data-field="auth"><strong>Sign-in method:</strong> <code>/login</code> or a provider API key</div><div data-field="safety"><strong>Safe starting point:</strong> Pi has no built-in sandbox; use a disposable repo or container and review commands manually</div><div data-field="status"><strong>Status:</strong> An extensible minimal terminal coding harness</div><div data-field="sources"><strong>Official sources:</strong> <a href="https://pi.dev/docs/latest/providers">provider</a> · <a href="https://github.com/earendil-works/pi">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>Hermes Agent</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>Who it currently suits:</strong> People who want to use the same agent in a terminal, desktop app, or chat platform</div><div data-field="models"><strong>Model / provider choices:</strong> Nous Portal, OpenRouter, Anthropic, Google, and other providers</div></td><td><div data-field="auth"><strong>Sign-in method:</strong> Set an API key or OAuth with <code>hermes model</code>; Nous Portal supports OAuth</div><div data-field="safety"><strong>Safe starting point:</strong> Start in a low-risk repo; enable skills, MCP, and provider permissions one at a time</div><div data-field="status"><strong>Status:</strong> Nous Research’s open-source agent; docs provide CLI and multi-interface integrations</div><div data-field="sources"><strong>Official sources:</strong> <a href="https://hermes-agent.nousresearch.com/docs/integrations/providers/">provider</a> · <a href="https://github.com/NousResearch/hermes-agent">repo</a></div></td></tr>
</tbody>
</table>
</div>

<details markdown="1">
<summary>More about OpenRouter and Ollama</summary>

### Where do OpenRouter and Ollama fit?

OpenRouter is a Router, so it is not one of the 9 coding CLIs above; it provides a unified API, provider routing, and centralized usage. Ollama is a local runtime, not an agent; it can provide a compatible API at `http://localhost:11434/v1` for OpenCode, goose, Aider, or another client. Neither replaces an agent’s file permissions and sandbox design.
</details>

## Keep four things when moving a prompt between CLIs

1. Write down the file paths, allowed scope, and the order “list a plan first, then change after confirmation.”
2. Record the model, provider, API key, and approval / sandbox settings separately; do not assume they stay the same when you change CLIs.
3. Describe the goal in ordinary language; use slash commands such as `/login` and `/permissions` only in the relevant tool’s section.
4. Ask for `git diff`, test results, and unfinished items, and restore the worktree before using another CLI.

<details markdown="1">
<summary>Expand rules files, sandbox, and common questions</summary>

- Claude Code’s project rules are in `CLAUDE.md`; Codex uses `AGENTS.md`. OpenCode gives `AGENTS.md` priority and uses `CLAUDE.md` as a compatibility fallback when it is absent; do not treat a nonexistent `OPENCODE.md` as a common format.
- Gemini CLI’s project context and `.gemini/` settings follow its official docs; `--sandbox`, approval mode, and `--yolo` have different risks, so do not skip confirmation on your first try.
- Pi’s project trust is not a sandbox. Its official safety docs explicitly warn that it runs with the permissions of the user who starts it; use a container or another OS-level boundary when isolation is needed.
- Aider’s official docs explain git integration and auto-commit after editing; start in a clean demo repo, inspect the commit, then bring it into a working repo.
- For goose, Hermes Agent, and other agents that can connect MCP / extensions, start with a low-privilege, read-only integration; do not use Gmail, Slack, or a production DB as your first external connection.
- Put API keys only in an officially supported credential store or environment variable; never put them in a repo, prompt, screenshot, or issue. Calculate cost from the day’s official price and actual usage, not from the model name.

#### Official verification entry points (2026-08-30 UTC)

- [Claude Code overview](https://code.claude.com/docs/en/overview) · [permissions](https://code.claude.com/docs/en/permissions)
- [OpenAI Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [OpenCode](https://opencode.ai/docs/) · [canonical repository](https://github.com/anomalyco/opencode)
- [Gemini CLI](https://google-gemini.github.io/gemini-cli/)
- [goose](https://block.github.io/goose/) · [canonical repository](https://github.com/aaif-goose/goose)
- [Aider](https://aider.chat/docs/)
- [Hermes Agent](https://hermes-agent.nousresearch.com/docs/)
- [Grok Build](https://github.com/xai-org/grok-build)
- [Pi](https://pi.dev/docs/latest) · [canonical repository](https://github.com/earendil-works/pi)
- [OpenRouter FAQ](https://openrouter.ai/docs/faq) · [Ollama](https://ollama.com/)
</details>

## Return to Track A

- For your first safe operation, return to [A1](../tracks/cli/A1-cli-intro.en.md).
- To fix rules files and repeatable workflows in place, go to [A2](../tracks/cli/A2-cli-workflow.en.md).
- To work on MCP, CI, and usage traces, go to [A3](../tracks/cli/A3-cli-production.en.md).

> Maintenance principle: tools, sign-in, pricing, sandbox, and providers change. Recheck official docs and update the checked-on date before editing the table. Keep this table factual; do not maintain popularity or subjective ratings.

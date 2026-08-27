> [繁體中文](./cli-agents-guide.md) | [简体中文](./cli-agents-guide.zh-Hans.md) | **English**

# CLI Agents Reference Guide

> [← Back to the main path README](../README.en.md) · [A1: Safely run your first small task](../tracks/cli/A1-cli-intro.en.md)

This reference doc organizes 9 terminal CLIs around “what do you want to do now?” and checkable official sources. It does not score tools or choose an entry point by popularity or subjective ranking; first identify the role, then choose based on your provider, sign-in method, and safety boundaries.

## First separate the roles: an agent is not a model or API

<table>
<thead>
<tr><th scope="col">Type</th><th scope="col">What it does</th><th scope="col">Examples</th><th scope="col">Do not confuse it with</th></tr>
</thead>
<tbody>
<tr><th scope="row">LLM</th><td>Generates text, code, or tool calls</td><td>Claude, GPT, Gemini</td><td>The model does not automatically have access to files on your computer</td></tr>
<tr><th scope="row">Provider API</th><td>Provides requests, authentication, and billing for one model provider</td><td>Anthropic API, OpenAI API, Gemini API</td><td>An API is not a terminal workbench</td></tr>
<tr><th scope="row">Router</th><td>Forwards requests to multiple providers</td><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a></td><td>A Router does not manage files or command permissions on an agent’s behalf</td></tr>
<tr><th scope="row">Coding agent / harness</th><td>Reads files, edits, runs commands, and reports results in the terminal</td><td>Claude Code, Codex, OpenCode V2, Pi</td><td>Its approval, sandbox, and project trust settings need separate checking</td></tr>
<tr><th scope="row">Local runtime</th><td>Loads and runs a model locally</td><td><a href="https://ollama.com/">Ollama</a></td><td>It can be called by an agent, but it is not a coding agent</td></tr>
</tbody>
</table>

## Find an entry point from your situation

<table>
<thead>
<tr><th scope="col">Your situation</th><th scope="col">What to check first</th><th scope="col">Differences to record</th></tr>
</thead>
<tbody>
<tr><th scope="row">You already have an account with a model service</th><td>A CLI from that ecosystem, such as Claude Code, Codex, or Gemini CLI</td><td>Sign-in flow, approval, sandbox, and usage page</td></tr>
<tr><th scope="row">You need to switch providers</th><td>OpenCode V2, goose, Aider, Hermes Agent, or Pi</td><td>Supported endpoints, model IDs, and where API keys are stored</td></tr>
<tr><th scope="row">You want to route multiple providers through one place</th><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a> paired with an agent</td><td>The actual provider route, data policy, usage, and billing</td></tr>
<tr><th scope="row">You want to practice locally</th><td><a href="https://ollama.com/">Ollama</a> paired with an agent that supports a compatible API</td><td>Whether the model is local, and whether the agent can still run shell commands / write files</td></tr>
</tbody>
</table>

## 9 CLI tools

The full table is collapsed by default; after expanding it, record the “checked on” date alongside your installed version. Official data checked on: **2026-08-27 UTC**.

<details markdown="1">
<summary>Expand installation, authentication, provider, and safety facts for the 9 CLIs</summary>

<table>
<thead>
<tr><th scope="col">Type</th><th scope="col">Tool</th><th scope="col">Who it currently suits</th><th scope="col">Model / provider choices</th><th scope="col">Sign-in method</th><th scope="col">Safe starting point</th><th scope="col">Status</th><th scope="col">Official sources</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Official model ecosystems</th><td>Claude Code</td><td>People who want to use the Anthropic ecosystem in the terminal</td><td>Claude; Anthropic API</td><td>Claude account or Anthropic API key</td><td>Use a demo repo; keep the permission prompt</td><td>One of Anthropic’s official terminal, desktop, IDE, and cloud interfaces</td><td><a href="https://code.claude.com/docs/en/overview">docs</a> · <a href="https://github.com/anthropics/claude-code">repo</a></td></tr>
<tr><td>Codex CLI</td><td>People who want to use OpenAI / ChatGPT sign-in in the terminal</td><td>GPT family; OpenAI API</td><td>ChatGPT sign-in or OpenAI API key</td><td>Use the default approval and workspace sandbox; inspect the diff first</td><td>OpenAI’s open-source terminal coding agent</td><td><a href="https://learn.chatgpt.com/docs/codex/cli">docs</a> · <a href="https://github.com/openai/codex">repo</a></td></tr>
<tr><td>Gemini CLI</td><td>People with Google authentication who want Gemini in the terminal</td><td>Gemini; Google AI API or Vertex AI</td><td>Google sign-in, Gemini API key, or Vertex AI</td><td>Use approval mode; explicitly enable `--sandbox` when needed</td><td>Google’s open-source terminal agent</td><td><a href="https://google-gemini.github.io/gemini-cli/">docs</a> · <a href="https://github.com/google-gemini/gemini-cli">repo</a></td></tr>
<tr><td>Grok Build</td><td>People who want to try xAI’s Grok terminal TUI</td><td>Grok; xAI sign-in or API key</td><td>Interactive browser sign-in on first launch; CI can use `XAI_API_KEY`</td><td>Start in a demo repo; do not copy `~/.grok/auth.json`</td><td>xAI’s official open-source TUI coding agent</td><td><a href="https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/02-authentication.md">authentication</a> · <a href="https://github.com/xai-org/grok-build">repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">Provider-flexible</th><td>OpenCode V2</td><td>People who need to switch among multiple providers</td><td>Multiple providers; can connect to OpenRouter or a compatible endpoint</td><td>Configure an API key, OAuth, or environment variable for the provider</td><td>Check permission settings first; test outside directories only in a demo repo</td><td>Open-source terminal coding agent; V2 project rules use `AGENTS.md` and do not use the old `CLAUDE.md` fallback</td><td><a href="https://opencode.ai/v2/docs/providers">provider</a> · <a href="https://github.com/anomalyco/opencode">repo</a></td></tr>
<tr><td>goose</td><td>People who need a CLI, desktop app, or API and want to connect tools and data sources</td><td>15+ providers, including Anthropic, OpenAI, Google, Ollama, and OpenRouter</td><td>Provider API key, or ACP sign-in through some existing subscriptions</td><td>Start with low-privilege extensions and a sandbox; do not connect production data</td><td>AAIF’s open-source local agent, with CLI, desktop, and API</td><td><a href="https://block.github.io/goose/">docs</a> · <a href="https://github.com/aaif-goose/goose">repo</a></td></tr>
<tr><td>Aider</td><td>People who want to manage code changes with git diff / commit</td><td>Multiple cloud APIs, OpenRouter, OpenAI-compatible endpoints, and local models</td><td>Provider API key, config file, or environment variable</td><td>Start in a clean demo repo; note Aider’s git auto-commit behavior</td><td>Open-source terminal pair-programming tool; official docs specify its git integration</td><td><a href="https://aider.chat/docs/">docs</a> · <a href="https://github.com/Aider-AI/aider">repo</a></td></tr>
<tr><td>Pi</td><td>People who want to start from a small core and extend it with extensions, skills, or RPC</td><td>Subscription providers, API-key providers, custom providers; can connect to a local endpoint</td><td>`/login` or a provider API key</td><td>Pi has no built-in sandbox; use a disposable repo or container and review commands manually</td><td>An extensible minimal terminal coding harness</td><td><a href="https://pi.dev/docs/latest/providers">provider</a> · <a href="https://github.com/earendil-works/pi">repo</a></td></tr>
<tr><td>Hermes Agent</td><td>People who want to use the same agent in a terminal, desktop app, or chat platform</td><td>Nous Portal, OpenRouter, Anthropic, Google, and other providers</td><td>Set an API key or OAuth with `hermes model`; Nous Portal supports OAuth</td><td>Start in a low-risk repo; enable skills, MCP, and provider permissions one at a time</td><td>Nous Research’s open-source agent; docs provide CLI and multi-interface integrations</td><td><a href="https://hermes-agent.nousresearch.com/docs/integrations/providers/">provider</a> · <a href="https://github.com/NousResearch/hermes-agent">repo</a></td></tr>
</tbody>
</table>

### Where do OpenRouter and Ollama fit?

OpenRouter is a Router, so it is not one of the 9 coding CLIs above; it provides a unified API, provider routing, and centralized usage. Ollama is a local runtime, not an agent; it can provide a compatible API at `http://localhost:11434/v1` for OpenCode V2, goose, Aider, or another client. Neither replaces an agent’s file permissions and sandbox design.
</details>

## Keep four things when moving a prompt between CLIs

1. Write down the file paths, allowed scope, and the order “list a plan first, then change after confirmation.”
2. Record the model, provider, API key, and approval / sandbox settings separately; do not assume they stay the same when you change CLIs.
3. Describe the goal in ordinary language; use slash commands such as `/login` and `/permissions` only in the relevant tool’s section.
4. Ask for `git diff`, test results, and unfinished items, and restore the worktree before using another CLI.

<details markdown="1">
<summary>Expand rules files, sandbox, and common questions</summary>

- Claude Code’s project rules are in `CLAUDE.md`; Codex uses `AGENTS.md`. OpenCode V2 also uses `AGENTS.md` and does not use the old `CLAUDE.md` fallback; do not treat a nonexistent `OPENCODE.md` as a common format.
- Gemini CLI’s project context and `.gemini/` settings follow its official docs; `--sandbox`, approval mode, and `--yolo` have different risks, so do not skip confirmation on your first try.
- Pi’s project trust is not a sandbox. Its official safety docs explicitly warn that it runs with the permissions of the user who starts it; use a container or another OS-level boundary when isolation is needed.
- Aider’s official docs explain git integration and auto-commit after editing; start in a clean demo repo, inspect the commit, then bring it into a working repo.
- For goose, Hermes Agent, and other agents that can connect MCP / extensions, start with a low-privilege, read-only integration; do not use Gmail, Slack, or a production DB as your first external connection.
- Put API keys only in an officially supported credential store or environment variable; never put them in a repo, prompt, screenshot, or issue. Calculate cost from the day’s official price and actual usage, not from the model name.

#### Official verification entry points (2026-08-27 UTC)

- [Claude Code overview](https://code.claude.com/docs/en/overview) · [permissions](https://code.claude.com/docs/en/permissions)
- [OpenAI Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [OpenCode V2](https://opencode.ai/v2/docs) · [canonical repository](https://github.com/anomalyco/opencode)
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

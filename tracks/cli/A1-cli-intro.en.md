# A1 — Choose a CLI agent and safely complete your first small task

> [繁體中文](./A1-cli-intro.md) | [简体中文](./A1-cli-intro.zh-Hans.md) | **English**

> [← Back to the main path README](../../README.en.md) · **Track A: CLI Power User** — Stop 1 · [Next: A2](A2-cli-workflow.en.md)

This stop explains what “AI in the terminal” means, then has you run it once in a disposable demo repo (a Git-managed practice project folder). You will first have the tool read files, find the test command, and propose a plan; only after you confirm the plan will it make a small change that you can inspect with `git diff` and undo.

If you want to use existing tools to get work done and do not want to write agent programs yet, this is your entry point.

## Do only this for now

Prepare a disposable demo repo with no secrets. If you have not installed a tool yet, choose one in the short table below, follow its official entry point to install and sign in, then send this request:

> Read the current demo repo only, explain its purpose, find the test command, and propose a small documentation-change plan. Do not modify or delete files yet, and do not run commands that change data.

When it is done, you should see a repo summary, a test command, a plan waiting for confirmation, and a permission prompt when the tool requests access. That is the first verifiable result of this track.

## Learning goals

- Distinguish an LLM, Provider API, Router, coding agent / harness, and local runtime.
- Choose an entry point based on the account, provider, or local environment you already have; do not make an overall ranking.
- Complete one “read first → inspect the plan → confirm → small change → `git diff` → undo” cycle in a demo repo.

<details markdown="1">
<summary>Expand time, prerequisites, account, and cost</summary>

- **Time:** The first read-only pass and plan review can usually be completed in one short session; you can spread CLI-1 through CLI-4 over several days rather than doing them all at once.
- **Prerequisites:** You can enter a folder and inspect `git status` and `git diff`; you have a disposable demo repo on hand.
- **Account:** Prepare a sign-in method supported by the tool you choose, or connect the agent to a local model runtime. If you have no account, start with the selection table and the official Quickstart below.
- **Cost:** Do not guess. Check the day’s official pricing / usage page before you start; this exercise has no model API charge only when the entire flow stays local.
</details>

## Keep these five identities separate

<table>
<thead>
<tr><th scope="col">Type</th><th scope="col">Plain-language meaning</th><th scope="col">Examples</th><th scope="col">How this track uses it</th></tr>
</thead>
<tbody>
<tr><th scope="row">LLM</th><td>The model that generates answers</td><td>Claude, GPT, Gemini</td><td>Provides responses; does not manage the repo</td></tr>
<tr><th scope="row">Provider API</th><td>The door to one model service</td><td>Anthropic API, OpenAI API, Gemini API</td><td>Handles requests, authentication, and billing</td></tr>
<tr><th scope="row">Router</th><td>An entry point that sends requests to multiple providers</td><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a></td><td>Not an LLM or a coding agent</td></tr>
<tr><th scope="row">Coding agent / harness</th><td>A workbench that reads files, edits files, and runs commands in the terminal</td><td>Claude Code, Codex, OpenCode, Pi</td><td>Operates in the working directory; start with a demo repo</td></tr>
<tr><th scope="row">Local runtime</th><td>An engine that runs a model on your own computer</td><td><a href="https://github.com/ollama/ollama">Ollama</a></td><td>Can be called by an agent; is not an agent</td></tr>
</tbody>
</table>

## Choose an entry point from what you already have

<table>
<thead>
<tr><th scope="col">What you already have</th><th scope="col">Entry points to check first</th><th scope="col">Confirm first</th></tr>
</thead>
<tbody>
<tr><th scope="row">An Anthropic account or API</th><td><a href="https://code.claude.com/docs/en/quickstart">Claude Code</a></td><td>Sign-in and permission prompts</td></tr>
<tr><th scope="row">ChatGPT or an OpenAI API</th><td><a href="https://developers.openai.com/codex/cli">Codex CLI</a></td><td>Approval, sandbox, and working directory</td></tr>
<tr><th scope="row">A Google account, API, or Vertex AI</th><td><a href="https://google-gemini.github.io/gemini-cli/">Gemini CLI</a></td><td>Authentication and sandbox</td></tr>
<tr><th scope="row">You want to switch providers or use a local model</th><td><a href="https://opencode.ai/docs">OpenCode</a>, <a href="https://block.github.io/goose/">goose</a>, <a href="https://aider.chat/docs/">Aider</a>, or <a href="https://pi.dev/docs/latest">Pi</a></td><td>Provider and permission boundaries</td></tr>
<tr><th scope="row">You want a Router or local runtime</th><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a> or <a href="https://ollama.com/">Ollama</a></td><td>They must be paired with a coding agent</td></tr>
</tbody>
</table>

<a id="cli-1"></a>
### Hands-on CLI-1: Read the demo repo first, then make one reversible small change

**Outcome:** You can see the repo description, test command, and a plan waiting for confirmation; after confirming, you leave one small change that can be checked with `git diff`.

<details markdown="1">
<summary>Expand CLI-1 preparation, operation, and undo steps</summary>

1. Create or copy a disposable demo repo. Include only a README, a small amount of source code, and tests; do not include API keys, personal data, contracts, or production settings. Before you start, run `git status --short` and confirm that no one else has unfinished changes.
2. Use the “read only” request above first. Compare the files, test command, and plan the tool lists; ask about anything unclear instead of approving it immediately.
3. After you confirm the plan, allow only one small documentation change, such as adding “How to run the tests” to `README.md`. Ask the tool to show the diff first, then approve it.
4. Run `git diff -- README.md` in the terminal and confirm that it contains only the expected content. Run `git restore -- README.md` only if Step 1 confirmed that the file was clean originally; then run `git status --short` again to confirm that the small change is undone.

If the tool does not have git, keep an original-file backup and compare line by line; do not give the same demo repo to two agents that can write files at the same time.
</details>

<a id="cli-2"></a>
### Hands-on CLI-2: Make sure the project rules are read correctly

**Outcome:** You can use a short rules file to state the project purpose, prohibitions, test command, and delivery format, then verify that the tool followed it.

<details markdown="1">
<summary>Expand project-rule locations and verification for each CLI</summary>

- Claude Code reads the project’s `CLAUDE.md`; Codex uses `AGENTS.md`.
- OpenCode uses `AGENTS.md`, with `CLAUDE.md` as a compatibility fallback; do not create `OPENCODE.md` as a general rules file.
- Gemini CLI commonly uses `GEMINI.md`; goose, Aider, Hermes Agent, Pi, and Grok Build use filenames and loading scopes set by their respective official docs.
- Keep rules limited to content that changes behavior: project purpose, things it must not do, the test command, and the delivery format. Do not put a long API reference into a rules file that loads every time.

Add one observable rule in the demo repo, such as “propose a plan first; do not modify `data/`,” then send a request that triggers it. Finally, inspect the agent’s response and `git diff`.
</details>

<a id="cli-3"></a>
### Hands-on CLI-3: Run the same request again with a second harness

**Outcome:** You can record differences between two tools in model / provider, permission prompts, sandbox, and output format instead of choosing a winner by subjective score.

<details markdown="1">
<summary>Expand the fair-comparison steps for a second CLI</summary>

Run each tool once in the same clean demo repo with the same prompt and same set of files. Record the date, CLI version, LLM, provider, sign-in method, approval / sandbox settings, whether it actually changed files, and the `git diff` result. Do not start two sessions that can write at the same time; undo the changes after each run before starting the next one.
</details>

<a id="cli-4"></a>
### Hands-on CLI-4: Observe authentication failure with fake credentials

**Outcome:** You can distinguish “sign-in failed,” “provider API key failed,” “model name does not exist,” and “permission / sandbox blocked,” without putting a real secret into a prompt or log.

<details markdown="1">
<summary>Expand the safe authentication-error experiment</summary>

In a one-time terminal session, use a value clearly marked as fake, such as `not-a-real-key`; do not change a production shell configuration or shared `.env`. First observe the not-signed-in error; then, in a signed-in CLI, enter an officially nonexistent model name and record the error type and recovery guidance. Clear the fake value immediately after testing, and confirm that the shell history, working directory, and logs contain no real key.

Requests using valid credentials may incur charges; for the first exercise, you can use local Ollama or a provider’s explicitly free quota, based on that day’s official pricing and actual usage.
</details>

## For a full comparison, use the reference table

A1 teaches you how to start safely; it does not maintain the same fast-changing data in two pages. Sign-in, provider, sandbox, and official sources for the 9 tools are centralized in the [`CLI Agents reference guide`](../../resources/cli-agents-guide.en.md). Official data checked on: **2026-08-27 UTC**.

<details markdown="1">
<summary>Expand the shortest way to distinguish “tool, Router, and local runtime”</summary>

- Claude Code, Codex, Gemini CLI, OpenCode, goose, Aider, Hermes Agent, Grok Build, and Pi: CLI agents / harnesses that receive tasks and operate in the working directory.
- OpenRouter: a Router that sends an agent’s request to a provider; it does not manage your file permissions.
- Ollama: a runtime for running models locally; it does not read a repo by itself and must be called by an agent that supports it.
- When unsure, ask only three questions: Who runs the model? Who forwards the request? Who can read and write my files?
</details>

## Required reading and cost boundaries

<details markdown="1">
<summary>Expand official reading, account, and budget notes</summary>

- [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart) and [permissions](https://code.claude.com/docs/en/permissions)
- [Codex CLI](https://developers.openai.com/codex/cli)
- [Gemini CLI authentication](https://google-gemini.github.io/gemini-cli/docs/get-started/authentication.html) and [sandbox configuration](https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html)
- [OpenCode docs](https://opencode.ai/docs) and [goose docs](https://block.github.io/goose/)
- [Aider docs](https://aider.chat/docs/), [Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/), [Grok Build repo](https://github.com/xai-org/grok-build), and [Pi docs](https://pi.dev/docs/latest)
- [OpenRouter FAQ](https://openrouter.ai/docs/faq) and [Ollama](https://ollama.com/)

The per-request cost and total cost for this track’s cloud requests vary with your account, provider, model, input and output tokens, and subscription quota; check the day’s official pricing or usage page before practicing. Only when both the agent and provider are configured to connect solely to local Ollama, with no other cloud service called, will this exercise have no model API charge; file and command permissions still need the usual checks.
</details>

## ✅ Self-check before A2

- [ ] I can explain the five identities in my own words and know that OpenRouter is not an LLM and Ollama is not a coding agent.
- [ ] In a demo repo, I completed a read-only explanation and plan without giving the tool any secrets.
- [ ] I checked the diff for one small change and can undo it.
- [ ] I know the selected CLI’s sign-in method, provider, and approval / sandbox settings.

After that, continue to [A2 — Build a reusable CLI workflow](A2-cli-workflow.en.md). To compare the tools’ official status again, return to [`resources/cli-agents-guide.en.md`](../../resources/cli-agents-guide.en.md).

> Safety baseline: do not run your first experiment in a directory containing secrets or production permissions; do not use a mode that skips all confirmations; do not paste API keys, browser tokens, or auth files into prompts, issues, logs, or git.

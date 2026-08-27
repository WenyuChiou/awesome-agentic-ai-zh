# A1 — Choose a CLI agent and safely complete your first small task

> [繁體中文](./A1-cli-intro.md) | [简体中文](./A1-cli-intro.zh-Hans.md) | **English**

> [← Back to the main path README](../../README.en.md) · **Track A: CLI Power User** — Stop 1 · [Next: A2](A2-cli-workflow.en.md)

This stop explains what “AI in the terminal” means, then has you run it once in a disposable demo repo (a Git-managed practice project folder). You will first have the tool read files, find the test command, and propose a plan; only after you confirm the plan will it make a small change that you can inspect with `git diff` and undo.

If you want to use existing tools to get work done and do not want to write agent programs yet, this is your entry point.

## Do only this for now

Prepare a disposable demo repo with no secrets. If you have not installed a tool yet, choose one in the short table below, follow its official entry point to install and sign in, then copy this request directly:

```text
Read the current demo repo only, explain its purpose, find the test command, and propose a small documentation-change plan. Do not modify or delete files yet, and do not run commands that change data.
```

When it is done, you should see a repo summary, a test command, a plan waiting for confirmation, and a permission prompt when the tool requests access. That is the first verifiable result of this track.

## 📌 Learning Goals

- Distinguish an **LLM**, **Provider API**, **Router**, **Coding agent**, and **Local runtime**.
- Choose an entry point based on the account, provider, or local environment you already have; do not make an overall ranking.
- Complete one “read first → inspect the plan → confirm → small change → `git diff` → undo” cycle in a demo repo.

<details markdown="1">
<summary>Expand time, prerequisites, account, and cost</summary>

- **Time:** The first read-only pass and plan review can usually be completed in one short session; you can spread CLI-1 through CLI-4 over several days rather than doing them all at once.
- **Prerequisites:** You can enter a folder and inspect `git status` and `git diff`; you have a disposable demo repo on hand.
- **Account:** Prepare a sign-in method supported by the tool you choose, or connect the agent to a local model runtime. If you have no account, start with the selection table and the official Quickstart below.
- **Cost:** Do not guess. Check the day’s official pricing / usage page before you start; this exercise has no model API charge only when the entire flow stays local.
</details>

## 🧩 Five Core Terms First

| Core term | What it is, in plain language | How A1 uses it | What it is not |
|---|---|---|---|
| **LLM (Large Language Model)** | The model that generates text or code, like the brain that thinks of answers in a workbench | Claude, GPT, and Gemini are model families | It does not manage the repo, file permissions, or billing |
| **Provider API (model-service entry point)** | The door that lets a tool send a request to one model service | Anthropic, OpenAI, and Gemini APIs handle authentication and billing | It is not a coding agent that edits files |
| **Router** | A transfer station that sends the same request to different providers | [OpenRouter](https://openrouter.ai/docs/faq) can centralize API, routing, and usage | It is not an LLM and does not manage file permissions |
| **Coding agent (coding workbench)** | A workbench that can read files, edit files, and run commands in the terminal | Claude Code, Codex, OpenCode V2, and Pi are in this group | Its model, provider, and sandbox still need separate checks |
| **Local runtime (local model engine)** | An engine that runs a model on your own computer, like a motor starting the model | [Ollama](https://github.com/ollama/ollama) lets compatible agents call a local model | It is not a coding agent and does not read a repo by itself |

## Choose an entry point from what you already have

<table>
<thead>
<tr><th scope="col">What you already have</th><th scope="col">Entry points to check first</th><th scope="col">Confirm first</th></tr>
</thead>
<tbody>
<tr><th scope="row">An Anthropic account or API</th><td><a href="https://code.claude.com/docs/en/quickstart">Claude Code</a></td><td>Sign-in and permission prompts</td></tr>
<tr><th scope="row">ChatGPT or an OpenAI API</th><td><a href="https://learn.chatgpt.com/docs/codex/cli">Codex CLI</a></td><td>Approval, sandbox, and working directory</td></tr>
<tr><th scope="row">A Google account, API, or Vertex AI</th><td><a href="https://google-gemini.github.io/gemini-cli/">Gemini CLI</a></td><td>Authentication and sandbox</td></tr>
<tr><th scope="row">You want to switch providers or use a local model</th><td><a href="https://opencode.ai/v2/docs">OpenCode V2</a>, <a href="https://block.github.io/goose/">goose</a>, <a href="https://aider.chat/docs/">Aider</a>, or <a href="https://pi.dev/docs/latest">Pi</a></td><td>Provider and permission boundaries</td></tr>
<tr><th scope="row">You want a Router or local runtime</th><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a> or <a href="https://ollama.com/">Ollama</a></td><td>They must be paired with a coding agent</td></tr>
</tbody>
</table>

## 📚 Required Reading

<details markdown="1">
<summary>Expand official reading, account, and budget notes</summary>

- [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart) and [permissions](https://code.claude.com/docs/en/permissions)
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [Gemini CLI authentication](https://google-gemini.github.io/gemini-cli/docs/get-started/authentication.html) and [sandbox configuration](https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html)
- [OpenCode V2 docs](https://opencode.ai/v2/docs) and [goose docs](https://block.github.io/goose/)
- [Aider docs](https://aider.chat/docs/), [Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/), [Grok Build repo](https://github.com/xai-org/grok-build), and [Pi docs](https://pi.dev/docs/latest)
- [OpenRouter FAQ](https://openrouter.ai/docs/faq) and [Ollama](https://ollama.com/)

The per-request cost and total cost for this track’s cloud requests vary with your account, provider, model, input and output tokens, and subscription quota; check the day’s official pricing or usage page before practicing. Only when both the agent and provider are configured to connect solely to local Ollama, with no other cloud service called, will this exercise have no model API charge; file and command permissions still need the usual checks.
</details>

## 🛠 Hands-on Exercises

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
- OpenCode V2 uses `AGENTS.md`; current V2 does not use the old `CLAUDE.md` fallback. Do not create `OPENCODE.md` as a general rules file.
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

## 🎯 Curated Projects

A1 teaches you how to start safely; it does not maintain the same fast-changing data in two pages. Sign-in, provider, sandbox, and official sources for the 9 tools are centralized in the [`CLI Agents reference guide`](../../resources/cli-agents-guide.en.md). Official data checked on: **2026-08-27 UTC**.

<details markdown="1">
<summary>Expand the complete tool ratings table (11 entries)</summary>

Editorial ratings are learning-map guidance, not GitHub stars or an overall ranking. `⭐⭐⭐⭐⭐` means read this first when you choose that tool path; it does not mean install every five-star tool.

<table>
<thead>
<tr><th scope="col">Category</th><th scope="col">Project</th><th scope="col">Rating</th><th scope="col">Best for</th><th scope="col">Watch first</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Official model ecosystems</th><td><a href="https://github.com/anthropics/claude-code">anthropics/claude-code</a></td><td>⭐⭐⭐⭐⭐</td><td>People using the Anthropic ecosystem</td><td>Keep the permission prompt; start in a demo repo</td></tr>
<tr><td><a href="https://github.com/openai/codex">openai/codex</a></td><td>⭐⭐⭐⭐⭐</td><td>People with ChatGPT or an OpenAI API</td><td>Confirm approval, sandbox, and working directory</td></tr>
<tr><td><a href="https://github.com/google-gemini/gemini-cli">google-gemini/gemini-cli</a></td><td>⭐⭐⭐⭐</td><td>People with Google auth or Vertex AI</td><td>Confirm authentication and sandbox first</td></tr>
<tr><td><a href="https://github.com/xai-org/grok-build">xai-org/grok-build</a></td><td>⭐⭐⭐</td><td>People trying the xAI ecosystem or a new tool</td><td>Observe in a demo repo; do not make it your first production tool</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">Provider-flexible</th><td><a href="https://github.com/anomalyco/opencode">anomalyco/opencode</a></td><td>⭐⭐⭐⭐⭐</td><td>People switching providers or using a compatible endpoint</td><td>V2 uses <code>AGENTS.md</code>; check permission settings</td></tr>
<tr><td><a href="https://github.com/aaif-goose/goose">aaif-goose/goose</a></td><td>⭐⭐⭐⭐</td><td>People using CLI, desktop, and extensions</td><td>Start with low-privilege extensions</td></tr>
<tr><td><a href="https://github.com/Aider-AI/aider">Aider-AI/aider</a></td><td>⭐⭐⭐⭐⭐</td><td>People who value git diff and commit workflows</td><td>Understand its git auto-commit behavior</td></tr>
<tr><td><a href="https://github.com/earendil-works/pi">earendil-works/pi</a></td><td>⭐⭐⭐⭐</td><td>People extending a small core with extensions, skills, or RPC</td><td>No built-in sandbox; use a container or VM when isolation is needed</td></tr>
<tr><td><a href="https://github.com/NousResearch/hermes-agent">NousResearch/hermes-agent</a></td><td>⭐⭐⭐⭐⭐</td><td>People using one agent in terminal, desktop, or chat</td><td>Enable provider, Skill, and MCP permissions one at a time</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Router / local engine</th><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a></td><td>⭐⭐⭐⭐</td><td>People switching providers through one API</td><td>It is a Router and still needs an agent</td></tr>
<tr><td><a href="https://github.com/ollama/ollama">ollama/ollama</a></td><td>⭐⭐⭐⭐⭐</td><td>People running models on their own computer</td><td>It is a local runtime and still needs an agent</td></tr>
</tbody>
</table>
</details>

<details markdown="1">
<summary>Expand the shortest way to distinguish “tool, Router, and local runtime”</summary>

- Claude Code, Codex, Gemini CLI, OpenCode, goose, Aider, Hermes Agent, Grok Build, and Pi: CLI agents / harnesses that receive tasks and operate in the working directory.
- OpenRouter: a Router that sends an agent’s request to a provider; it does not manage your file permissions.
- Ollama: a runtime for running models locally; it does not read a repo by itself and must be called by an agent that supports it.
- When unsure, ask only three questions: Who runs the model? Who forwards the request? Who can read and write my files?
</details>

## ✅ Self-check before A2

- [ ] I can explain the five identities in my own words and know that OpenRouter is not an LLM and Ollama is not a coding agent.
- [ ] In a demo repo, I completed a read-only explanation and plan without giving the tool any secrets.
- [ ] I checked the diff for one small change and can undo it.
- [ ] I know the selected CLI’s sign-in method, provider, and approval / sandbox settings.

After that, continue to [A2 — Build a reusable CLI workflow](A2-cli-workflow.en.md). To compare the tools’ official status again, return to [`resources/cli-agents-guide.en.md`](../../resources/cli-agents-guide.en.md).

> Safety baseline: do not run your first experiment in a directory containing secrets or production permissions; do not use a mode that skips all confirmations; do not paste API keys, browser tokens, or auth files into prompts, issues, logs, or git.

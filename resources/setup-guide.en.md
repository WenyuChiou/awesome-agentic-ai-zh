> [繁體中文](./setup-guide.md) | [简体中文](./setup-guide.zh-Hans.md) | **English**

# 🚀 From Zero — Setup Guide for People Without a Development Background

> [← Back to the main roadmap README](../README.en.md)

<!-- freshness: canonical=resources/setup-guide.md; verified_on=2026-08-30; scope=install-paths,api-keys,authentication,provider-entrypoints,project-status; max_age_days=90 -->

This page does not ask you to install every tool. Just choose one door first and complete one small result.

Already comfortable with Python, Git, and the terminal, and know how to protect an **API Key**? Go straight to [Stage 1](../stages/01-llm-basics.en.md).

## 📌 What This Guide Will Help You Complete

- Distinguish Web Chat, Desktop, IDE, **CLI Agent**, and **API** so you no longer treat them as the same kind of tool.
- Understand why an **API Key** is like a password and where it must not be placed.
- Use `uv` to prepare Python 3.12 without first learning a pile of package-management details.
- Copy a Python program and actually receive a model response.
- Know when to go to Stage 1 and when to go to Stage 5.

<details markdown="1">
<summary>View time, device, and prerequisites</summary>

- Web Chat only: you can start in a few minutes.
- Complete the API quick start: usually about 20–40 minutes; account review, payment setup, and network conditions may make it longer.
- You need: a Windows, macOS, or Linux computer where you can install software, plus an account that can open the provider Console.
- You do not need: prior programming experience, knowledge of Git branches, or a full IDE installed.

Company or school computers may prohibit installing programs or creating API keys. If that happens, ask an administrator; do not bypass the restriction.

</details>

## 🚪 Choose One Door First

The five doors are parallel choices, not five levels that must be completed in order.

| What you want to do | What this door is | First action |
|---|---|---|
| Chat with a model first | **Web Chat**: conversation in a browser | Open [Claude](https://claude.ai), [ChatGPT](https://chatgpt.com), [Gemini](https://gemini.google.com), or [Le Chat](https://chat.mistral.ai) |
| Chat or handle files in a computer app | **Desktop App**: a chat interface installed on your computer | Install it from the product's official download page |
| Have AI assist while you write code | **IDE Assistant**: lives inside the editor | Start with the [developer branch](../branches/for-developer.en.md) |
| Let an Agent read and edit files and run commands in a specified folder | **CLI Agent**: works in the terminal | Start with the [CLI Agents guide](cli-agents-guide.en.md) |
| Write your own program to call a model | **API**: the entry point where a program talks to a model service | Continue with A → B → C below |

<details markdown="1">
<summary>View the complete official entry points for Web, Desktop, IDE, and CLI</summary>

The table below is an entry-point list, not a ranking. The recommendation rating means “how suitable is it as a starting point for this learning roadmap.”

<table>
<thead><tr><th scope="col">Type</th><th scope="col">Official entry point / project</th><th scope="col">Know this first</th><th scope="col">Recommendation</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Web Chat</th><td><a href="https://claude.ai">Claude</a></td><td>Cloud chat interface; plans and features vary by account and region</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://chatgpt.com">ChatGPT</a></td><td>Cloud chat interface; a ChatGPT subscription is not OpenAI API credit</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://gemini.google.com">Gemini</a></td><td>Cloud chat interface; check data permissions before connecting services</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://chat.mistral.ai">Le Chat</a></td><td>Mistral's cloud chat interface</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Desktop</th><td><a href="https://claude.com/download">Claude Desktop</a></td><td>Use the official page for the current Windows, macOS, and Linux entry points</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://chatgpt.com/download">ChatGPT Desktop</a></td><td>Use the official download page for platform requirements</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://gemini.google.com/mac">Gemini for macOS</a></td><td>Currently a macOS app; use the Web version on other systems</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://lmstudio.ai/download">LM Studio</a></td><td>Local-model runtime and graphical interface; you still manage models, hardware, and file permissions</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">IDE／Editor</th><td><a href="https://cursor.com">Cursor</a></td><td>AI editor; confirm every modification and terminal action</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://windsurf.com/editor">Windsurf</a></td><td>AI editor; use the official documentation for plans and permissions</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://cline.bot">Cline</a></td><td>VS Code coding agent; start with low permissions</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://zed.dev/ai">Zed AI</a></td><td>AI features in the Zed editor</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/features/copilot">GitHub Copilot</a></td><td>Available in GitHub, IDEs, and other interfaces; permissions differ by interface</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="7">CLI Agent</th><td><a href="https://code.claude.com/docs/en/quickstart">Claude Code</a></td><td>Keep the permission prompt enabled first; begin with a small folder</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/openai/codex">OpenAI Codex</a></td><td>Coding agent; confirm its sandbox, approval, and diff</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/google-gemini/gemini-cli">Gemini CLI</a></td><td>Gemini's open-source terminal agent</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/anomalyco/opencode">OpenCode</a></td><td>Multi-provider coding agent / harness, not a model router</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/aaif-goose/goose">goose</a></td><td>Connects to providers and extensions; narrow tool permissions first</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://aider.chat/docs/">Aider</a></td><td>Git-first pair programmer; auto-commit does not mean you can skip review</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/NousResearch/hermes-agent">Hermes Agent</a></td><td>General-purpose agent; try small tasks in an isolated environment first</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
</table>

</details>

## 🧩 Seven Core Terms to Distinguish

- **Chat Surface**: the screen where you type, paste files, and read replies, such as Claude.ai. It is not a model API.
- **API**: the entry point where a program sends a request and receives a result. People usually do not chat directly on an API screen.
- **API Key**: a secret string that tells a service which account this program may use. Whoever obtains it may spend your credit.
- **Environment Variable**: a small drawer for handing settings to a program. The program can read it without the secret being written in source code.
- **Runtime**: what actually runs a program; Python is a runtime, and Ollama is a local-model runtime.
- **Package Manager**: helps install and run packages written by others. This guide uses `uv`.
- **CLI Agent**: an Agent that reads files, edits files, and runs tools in the terminal. It is not an API Provider or a single model.

## 📚 Required Reading and Official Starting Points

These five entry points stay visible; when versions differ, use the official page as the authority.

<table>
<thead><tr><th scope="col">Category</th><th scope="col">Official resource</th><th scope="col">What it helps you do</th><th scope="col">Recommendation</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Claude API</th><td><a href="https://platform.claude.com/docs/en/get-started">Claude API Quickstart</a></td><td>Create a key and send the first request</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://platform.claude.com/docs/en/api/sdks/python">Anthropic Python SDK</a></td><td>Confirm Python requirements, environment variables, and the current code shape</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">Python tools</th><td><a href="https://docs.astral.sh/uv/getting-started/installation/">uv Installation</a></td><td>Install or update uv for your operating system</td><td>⭐⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">CLI basics</th><td><a href="https://code.claude.com/docs/en/terminal-guide">Claude Code Terminal Guide</a></td><td>Open a terminal for the first time, change folders, and run commands</td><td>⭐⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">Secret security</th><td><a href="https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning">GitHub Secret Scanning</a></td><td>Understand why secrets must not enter Git history</td><td>⭐⭐⭐⭐</td></tr></tbody>
</table>

<a id="a--get-your-first-api-key-about-10-minutes"></a>

## 🛠 A — Get Your First API Key

This quick start uses Anthropic Claude because Stage 1's canonical API path uses it too. A Claude.ai subscription and a Claude API bill are separate things.

1. Open the [Claude Console](https://platform.claude.com/).
2. Go to **API Keys** and create a key for this exercise only.
3. If the screen lets you choose an owner, workspace, or expiration, use the narrowest scope and shortest reasonable duration.
4. Copy the key and put it in a password manager first; do not paste it into a chat window.
5. Check billing / usage in the Console first; if your account offers a spend limit or alert, set it to a small amount you can accept before calling the API.

**Three API Key rules:**

- **Do not paste** it into chat, group chats, email, issues, or screenshots.
- **Do not write** it into Python source code or Git history.
- **Do not share** one key across many projects; revoke it when you no longer need it.

<details markdown="1">
<summary>View other Cloud APIs and the local Runtime</summary>

The table below lists only current official entry points. Click the official pages for prices, free quotas, and available models; this getting-started guide does not freeze them.

<table>
<thead><tr><th scope="col">Type</th><th scope="col">Official entry point</th><th scope="col">Compatibility / limits</th><th scope="col">Recommendation</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="7">Cloud API</th><td><a href="https://platform.openai.com/docs/quickstart">OpenAI API</a></td><td>Official SDK and API; a ChatGPT subscription is not API billing</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://ai.google.dev/gemini-api/docs/openai">Gemini API</a></td><td>Google officially documents compatibility with OpenAI libraries</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://docs.api.nvidia.com/nim/re/reference/llm-apis">NVIDIA NIM</a></td><td>Check the endpoint for its supported API shape and models</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://api-docs.deepseek.com/">DeepSeek API</a></td><td>Official documentation provides an OpenAI-compatible way to use it</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://platform.kimi.com/docs/api/overview">Kimi API</a></td><td>Use the official Console for the region, endpoint, and models</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://help.aliyun.com/en/model-studio/base-url">Alibaba Model Studio／Qwen</a></td><td>Use the corresponding base URL for your region; the official service provides an OpenAI-compatible endpoint</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://docs.z.ai/api-reference/introduction">Z.ai／GLM API</a></td><td>Use the current endpoint in the official reference</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">Local Runtime</th><td><a href="https://docs.ollama.com/api/openai-compatibility">Ollama</a></td><td>Compatible with only part of the OpenAI API; you must download local models separately</td><td>⭐⭐⭐⭐⭐</td></tr></tbody>
</table>

Local inference has no provider model API bill, but you remain responsible for hardware, electricity, download time, device security, files, and logs. For the complete path, see the [Cookbook local LLM walkthrough](cookbook.en.md#6-local-llm--cli-agent-quick-walkthrough).

This repo currently uses these practice tags: `gemma4:e4b` for Stages 1–2, `qwen2.5:3b` for Tool Use／ReAct in Stages 3–6, and `qwen3.5:4b` for Eval／Observability／Streaming／Deploy in Stage 7. These are curriculum defaults, not a universal model ranking.

</details>

<a id="b--install-your-local-environment-about-10-minutes"></a>

## 🛠 B — Set Up the Python Runtime

Here `uv` manages both Python and packages. Install `uv` first:

macOS, Linux, or WSL:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen the terminal, then copy these in order:

```bash
uv --version
uv python install 3.12
uv run --python 3.12 python --version
```

When the last line shows `Python 3.12`, B is complete. `uv` also supports other Python versions; this tutorial fixes 3.12 to reduce package-compatibility problems for beginners.

<details markdown="1">
<summary>View operating-system alternatives if installation fails</summary>

- On Windows, you can use `winget install --id=astral-sh.uv -e`.
- On macOS, you can use `brew install uv`.
- You can also download a release binary from the [official uv installation page](https://docs.astral.sh/uv/getting-started/installation/).
- If your company blocks installation scripts, stop and ask an administrator for an approved method; do not force your way past security software.

Already having Python 3.10–3.14 is fine; `uv` will find an available Python. The commands above simply prepare a consistent 3.12 for this tutorial.

</details>

<a id="c--run-your-first-hello-claudepy-about-5-minutes"></a>

## 🛠 C — Run Your First `hello-claude.py`

### 1. Create an Exercise Folder

PowerShell, macOS, and Linux terminals can all use:

```bash
mkdir my-first-llm
cd my-first-llm
```

### 2. Create `.gitignore` First

Create a file named `.gitignore` and paste in:

```gitignore
.env
__pycache__/
*.pyc
```

Exclude `.env` first, before creating the secret file, to reduce the chance of accidentally adding it to Git.

### 3. Create `.env` Next

Create a file named `.env`. Replace the placeholder with your own key; do not paste a real key into this document or commit it:

```dotenv
ANTHROPIC_API_KEY=PASTE_YOUR_KEY_HERE
```

### 4. Copy the Python Program

Create `hello-claude.py`:

```python
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()  # Read the key from ANTHROPIC_API_KEY

message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=120,
    messages=[{"role": "user", "content": "Introduce yourself in one sentence."}],
)

for block in message.content:
    if block.type == "text":
        print(block.text)
```

### 5. Run It Directly

```bash
uv run --python 3.12 --with anthropic --with python-dotenv python hello-claude.py
```

When the model prints an introduction, Python, the packages, the API key, and the network are all connected.

<details markdown="1">
<summary>View common errors and safe recovery</summary>

| What you see | What it usually means | Do this first |
|---|---|---|
| `401`／`authentication_error` | The key was not read, has expired, or was pasted incorrectly | Revoke any questionable key; confirm the filename is `.env`, then create a new key |
| `429`／`rate_limit_error` | A usage, rate, or account-credit limit | Stop retrying, return to the Console to check usage / billing, then wait as the error message says |
| `ModuleNotFoundError` | You did not use the environment from this `uv run --with ...` command | Copy the full run command; do not run only `python hello-claude.py` |
| `uv` not found | The post-install terminal has not read the new PATH | Close and reopen the terminal; then check the official uv installation page |
| Connection error | A network, proxy, firewall, or service-status problem | Check the provider status page first; ask your company / school administrator about managed networks |

If a key has appeared in Git, chat, a screenshot, or a public log, deleting the text is not enough; revoke it in the Console immediately and create a new key.

</details>

<a id="d--install-claude-code-for-the-first-time-about-10-minutes-needed-for-stage-5--for-developer"></a>

## 🛠 D — Open Claude Code for the First Time

This is the entry point for Stage 5, not a requirement for completing the API quick start. Claude Code now prefers the native installer; you do not need to install Node.js first.

macOS, Linux, or WSL:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://claude.ai/install.ps1 | iex
```

After installation, run `claude --version` first, then run `claude` in a small exercise folder. See [Claude Code Installation](https://code.claude.com/docs/en/installation) for complete requirements and other installation methods.

<details markdown="1">
<summary>View login, system requirements, and your first CLAUDE.md</summary>

Claude Code currently requires one of the Claude plans, a Console account, or a supported cloud provider listed by the official documentation; the free Claude.ai plan does not include Claude Code. After running `claude`, follow the browser login prompt; see [Authentication](https://code.claude.com/docs/en/authentication) for identity details.

The current basic requirements include a supported Windows, macOS, or Linux system, at least 4 GB RAM, an internet connection, and an available shell. Windows can use PowerShell natively; consider WSL 2 when you need a Linux toolchain or sandbox.

You can create `CLAUDE.md` in the project root:

```markdown
# What this project does
This is a small learning project.

# Working rules
- Say which files you plan to change before editing them.
- Do not read or modify `.env`.
- Do not commit automatically; let me review the diff first.
- Ask before deleting files, installing packages, or using the network.

# Done when
- Run the smallest relevant test.
- Explain what changed, what you tested, and what risks remain.
```

`CLAUDE.md` is project instructions, not a security sandbox. Tool permissions, approval, version control, and human review still need to remain in place.

</details>

<a id="e--your-first-skill-example-about-5-minutes-needed-for-stage-53"></a>

## 🛠 E — Create Your First Skill

This is an extension for Stage 5.3. A **Skill** is a reusable folder with a name, description, and operating instructions; it does not automatically become a security permission.

First action: create `.claude/skills/hello-skill/SKILL.md`.

<details markdown="1">
<summary>View a directly copyable SKILL.md</summary>

```markdown
---
name: hello-skill
description: When the user explicitly asks for a greeting, reply in two languages.
---

When the user asks for a greeting:

1. Say hello once in Traditional Chinese.
2. Say hello once in English.
3. Do not read files, use the network, or run other tools.
```

Open `claude` in that project and enter “Please say hello.” Seeing both languages, with no extra actions, means you are done.

For fuller responsibility boundaries, see [Stage 5.3 — Skills](../stages/05-claude-code-ecosystem.en.md#53--skills-on-demand-procedure-cards); for more examples, see the [Cookbook](cookbook.en.md).

</details>

## ✅ Completion Check

Once any one of the following is true, you can leave this guide; you do not need to install every entry point:

- I can complete one conversation in Web Chat and know that it is not an API.
- I completed A → B → C and saw `hello-claude.py` print a model response.
- I chose the CLI path and can state the CLI Agent's working folder and permission scope.

Also confirm:

- A real API key has not appeared in source code, Git, chat, screenshots, or logs.
- I know how to revoke a key and know that API billing and chat subscriptions are separate.
- I did not skip diffs, tests, or human confirmation just because a tool can execute automatically.

## Where to Go Next

| What you want to do now | Next stop |
|---|---|
| Understand models, Tokens, Context Windows, and APIs | [Stage 1 — LLM Basics](../stages/01-llm-basics.en.md) |
| Learn Prompt directly | [Stage 2 — Prompt Engineering](../stages/02-prompt-engineering.en.md) |
| Work with a CLI Agent | [Track A1 — CLI Basics](../tracks/cli/A1-cli-intro.en.md) |
| Understand Claude Code, MCP, Skills, Plugins, and Subagents | [Stage 5 — Claude Code Ecosystem](../stages/05-claude-code-ecosystem.en.md) |
| Use local models | [Cookbook: local LLM walkthrough](cookbook.en.md#6-local-llm--cli-agent-quick-walkthrough) |
| Still cannot distinguish OpenRouter, Ollama, OpenCode, or Pi | [Glossary: distinguish five tool identities](glossary.en.md#-separate-five-tool-identities-first) |

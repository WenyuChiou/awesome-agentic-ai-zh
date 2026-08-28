> [繁體中文](./setup-guide.md) | [简体中文](./setup-guide.zh-Hans.md) | **English**

# 🚀 From Zero — Setup Guide for People Without a Dev Background

> [← Back to main README](../README.en.md)

> Expected time: 30-45 minutes. You will get your first API key, install Python / uv, and run your first LLM hello world.
> This guide is for people who want to learn AI agents but have not written code before. If you already know Python, git, and the CLI, you can skip to [Stage 1](../stages/01-llm-basics.en.md).

## Pick Your On-Ramp First

Ordered shallow → deep by setup effort. **Never touched an LLM? Just start with 1️⃣**.

### 1️⃣ Web (easiest, free tier, zero setup)

Open a browser, type the URL — done. **Best place to start if it's your first time**. Free tier usually covers a week of experimentation.

| Service | URL | Notes |
|---|---|---|
| **Claude** | https://claude.ai | Anthropic. Free tier has daily limits; Pro is $20/mo |
| **ChatGPT** | https://chatgpt.com | OpenAI. Free GPT-5.5 Instant (rate-limited); Plus $20/mo unlocks Thinking/Pro |
| **Gemini** | https://gemini.google.com | Google. Generous free tier, integrates Google apps |
| **Le Chat** | https://chat.mistral.ai | Mistral (EU open-source LLM lab). Free, privacy-focused |

### 2️⃣ Desktop app (free, better cross-app integration)

Native apps for macOS / Windows — adds system shortcut, clipboard / screenshot integration, drag-and-drop files.

| App | Download | Platform |
|---|---|---|
| **Claude Desktop** | https://claude.ai/download | macOS / Windows |
| **ChatGPT Desktop** | https://openai.com/chatgpt/download | macOS / Windows |
| **Gemini** | No native desktop app yet | (use web) |
| **LM Studio** | https://lmstudio.ai | macOS / Windows / Linux — runs local LLMs as a desktop app; $0 but needs GPU/RAM |

### 3️⃣ IDE with built-in AI (write code with an AI sidekick)

Lives inside a code editor — you write code normally, AI suggests / edits / answers questions alongside. **Best fit if you already write code and want an AI-native IDE**.

| Tool | Download | Shape |
|---|---|---|
| **Cursor** | https://cursor.com | Standalone IDE (VS Code fork) |
| **Windsurf** | https://codeium.com/windsurf | Standalone IDE (by Codeium) |
| **Cline** | https://cline.bot | VS Code extension (agentic style) |
| **Continue** | https://continue.dev | VS Code / JetBrains extension (open-source) |
| **Roo Code** | https://github.com/RooCodeInc/Roo-Code | VS Code extension (Cline fork); ⚠️ **repo archived 2026-05 (read-only)** |
| **Zed** | https://zed.dev | Standalone editor with built-in AI assistant |
| **GitHub Copilot** | https://github.com/features/copilot | Multi-IDE extension (VS Code / JetBrains / etc.) |

→ Detailed comparison → [`branches/for-developer.en.md`](../branches/for-developer.en.md)

### 4️⃣ CLI agent (terminal, can read/write files, run shell, manage git)

Agents that live in your terminal — you give one prompt (e.g. "refactor this module"), the agent reads files, edits them, runs commands, commits. **More autonomous than the IDE mode and handles multi-step tasks**, but setup is heavier (requires Node.js or Python; see B / D below).

| CLI Agent | Install / Docs | Primary LLM |
|---|---|---|
| **Claude Code** | https://code.claude.com/docs/en/quickstart | Claude |
| **Codex CLI** | https://github.com/openai/codex | GPT family |
| **Gemini CLI** | https://github.com/google-gemini/gemini-cli | Gemini |
| **OpenCode** | https://github.com/anomalyco/opencode | Any (multi-provider) |
| **goose** | https://block.github.io/goose | Any |
| **Aider** | https://aider.chat | Any (git-native) |
| **Hermes Agent** | https://github.com/NousResearch/hermes-agent | 200+ (model-neutral) |

→ CLI agent identity & selection guide → [`cli-agents-guide.en.md`](cli-agents-guide.en.md)
→ Detailed Claude Code first install → [D](#d--install-claude-code-for-the-first-time-about-10-minutes-needed-for-stage-5--for-developer) below

> 💡 **IDE vs CLI — how to pick?** Want AI alongside you while you code → IDE. Want to give one prompt and let the agent run a multi-step task → CLI. Many people use both.

### 5️⃣ API + write your own code (most advanced)

Want to script with Python, run batch jobs, integrate LLMs into your own app/automation? A-C below are for you.

> 💡 **What's an API key?** A password that lets a program call a model. Treat it like payment information.

---

## A — Get Your First API Key (About 10 Minutes)

### Anthropic Claude (Recommended First)

1. Open https://console.anthropic.com/
2. Sign up with Google, GitHub, or email.
3. After login, find **API Keys**, then choose **Create Key**.
4. **Copy the key immediately**. Most platforms show it only once.
5. Put it in a local password manager, or briefly in a local text file; the next section moves it into `.env`.

> ⚠️ **Three API-key rules**
> - **Do not paste it** into chat windows, group chats, email, or screenshots.
> - **Do not upload it** to git; GitHub may detect and revoke it.
> - **Do not store it** as a plain text cloud-drive file; syncing creates more exposure.

### Other LLM Options

#### Western cloud (US-friendly, English-first)

- **OpenAI**: https://platform.openai.com/api-keys
  ChatGPT Plus and API access are separate; Plus subscribers still need an API key.

- **Google AI Studio**: https://aistudio.google.com/
  Useful for trying the Gemini API. Free quota depends on region and account state.

- **NVIDIA NIM**: https://build.nvidia.com/
  **Hosts many open-source models (Llama / Mistral / DeepSeek / Qwen / Gemma etc.), OpenAI-compatible API, new accounts get 1000 free credits**. Great when you want to try several open models without local GPU. `base_url=https://integrate.api.nvidia.com/v1`.

#### Chinese / Chinese-language cloud (region-friendly, very cheap)

> If you're in mainland China and Anthropic / OpenAI are inaccessible, or you want to test Chinese-native models, start here. **All these APIs are OpenAI-compatible** — just change `base_url` and model name to run the same exercises.

- **DeepSeek**: https://platform.deepseek.com/
  Free web at https://chat.deepseek.com (with a deep-thinking mode). API is extremely cheap (**$0.14 input / $0.28 output per 1M tokens — about 7× cheaper than haiku**). Strong code and reasoning.
  `base_url=https://api.deepseek.com/v1`, `model=deepseek-v4-flash` or `deepseek-v4-pro`.

- **Moonshot Kimi**: https://platform.moonshot.cn/ (China) / https://platform.moonshot.ai/ (international)
  Free web at https://kimi.com. Selling point: **1M-token context window** (great for large files / long conversations). API ~$5-15 per 1M input, tiered by context size.
  `base_url=https://api.moonshot.cn/v1` (CN) / `https://api.moonshot.ai/v1` (intl), e.g. `model=kimi-k3`.

- **Qwen (Alibaba)**: https://dashscope.console.aliyun.com/
  Free web at https://chat.qwen.ai. API via Alibaba Cloud DashScope with an **OpenAI-compatible endpoint** ([docs](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/)). **The same Qwen models also run locally via Ollama** (`ollama pull qwen2.5:3b`) — cloud and local paths both work.

- **GLM (ZhipuAI)**: https://open.bigmodel.cn/ (China) / https://z.ai/ (intl)
  Free web at https://chatglm.cn. Has GLM-4.5 and GLM-4-Plus. Free tier available; students can apply for extra credit.

#### Local (no provider model API bill; offline after download)

- **Ollama local models**: no API key needed. For the local path, see [Cookbook Recipe 6](cookbook.en.md#6-local-llm--cli-agent-quick-walkthrough).
  This repo's "Path A" defaults to Ollama: Stage 1–2 use `gemma4:e4b`, Stage 3–6 tool-use/ReAct exercises use `qwen2.5:3b`, and Stage 7 debate/eval/observability/streaming/deploy mechanics use `qwen3.5:4b`. Local inference has no provider model API bill, but hardware, electricity, downloads, and waiting time still cost resources.

> 💡 **How to pick your first**:
> - Learning agents / production, **US-region account OK** → **Anthropic Claude** (the curriculum's canonical path)
> - Learning agents / production, **China region** or want a Chinese-native model → **DeepSeek** (cheapest cloud option, OpenAI-compat, strong Chinese support)
> - Want to try many models without a local GPU → **NVIDIA NIM** (1000 credits, 10+ hosted open models)
> - Want local data handling / mainland China without cloud access → **Ollama** (still protect your device, files, logs, and access permissions; local data is not automatically safe)

---

## B — Install Your Local Environment (About 10 Minutes)

### Install Python 3.10+

- **macOS**: open Terminal and run `brew install python@3.12`. If Homebrew is not installed, start at https://brew.sh.
- **Windows**: download the installer from https://www.python.org/downloads/ and make sure **Add Python to PATH** is checked.
- **Linux**: on Ubuntu, run `sudo apt install python3 python3-venv`; on Fedora, run `sudo dnf install python3`.
- **Verify**: macOS / Linux: `python3 --version`; Windows: `py --version`. You want `Python 3.10` or newer.

### Install uv

uv is a Python package tool. For this guide, think of it as "install the packages I need, then run this script."

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
irm https://astral.sh/uv/install.ps1 | iex
```

Verify:

```bash
uv --version
```

### Create Your First `.env` File

In the folder where you want to run the script, create a file named `.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-...paste the key you copied
```

`.env` is where local secrets live. Your program can read it, but you should not upload it to GitHub.

### Add `.gitignore`

In the same folder, create `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
```

This keeps git from recording your `.env` file.

---

## C — Run Your First `hello-claude.py` (About 5 Minutes)

Create `hello-claude.py`:

```python
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic() # Automatically reads ANTHROPIC_API_KEY

msg = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello, who are you?"}],
)

print(msg.content[0].text)
```

Run it:

```bash
uv run --with anthropic --with python-dotenv python hello-claude.py
```

If Claude introduces itself, your API key, Python, and packages are working.

### Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| `401 Unauthorized` | API key is missing or mistyped | Copy it again from A and check the `.env` filename and value |
| `429 Rate limit` | Too many requests too quickly | Wait a few seconds or minutes, then retry |
| `connection refused` | Network or firewall issue | Check your network, company firewall, or school firewall |
| `ModuleNotFoundError` | A package was not installed | Make sure you ran the exact `uv run --with ...` command above |

---

## D — Install Claude Code for the First Time (About 10 Minutes; Needed for Stage 5 / for-developer)

### Install Node.js First

> 💡 **What is Node.js?** A runtime for running JavaScript, similar to a Python interpreter but for JS. **`npm`** is its bundled package manager, which plays the same role as Python's `pip`: installing tools other people wrote, including Claude Code below. `npm install -g X` means install X globally so you can use it from any folder.

- **macOS / Linux**: run `brew install node`, or download from https://nodejs.org.
- **Windows**: download the installer from https://nodejs.org.
- **Verify**: run `node --version`; v18 or newer is enough.

### Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### First Authentication

```bash
claude
```

On first launch, you will usually choose between:

- **Claude subscription**: sign in with your Claude.ai account. This is the simplest path for beginners.
- **API key**: paste the key you created in A.

### Create Your First `CLAUDE.md`

Create `CLAUDE.md` at the root of your project. Claude Code reads it on startup so it understands how you want help.

```markdown
# Who you are
I am [your name], a [your field, such as teacher / researcher / writer].

# Code style
- Write comments in Traditional Chinese, and code in English
- Prefer type hints when writing functions
- Do not commit automatically; let me run git add myself

# Do not do these
- Do not browse the web unless I explicitly allow it
- Do not modify `.env` or `.gitignore`
- Do not delete folders, including subfolders
```

---

## E — Your First Skill Example (About 5 Minutes; Needed for Stage 5.3)

A Skill is a reusable prompt package for Claude Code. When your message matches the description, Claude Code loads that instruction automatically.

Create `.claude/skills/hello-skill/SKILL.md`:

```markdown
---
name: hello-skill
description: First hello skill. Trigger when the user says "請打招呼" or "say hi".
---

When the user asks you to greet them, return three things:

1. Say hello once in Traditional Chinese and once in English
2. Mention today's date using system time
3. Give one small daily reminder, randomly chosen from health / learning / mood
```

Run `claude`, then type `say hi`. If Claude returns the three items, the Skill loaded.

> For deeper Skill design, see [Stage 5.3 — Skills](../stages/05-claude-code-ecosystem.en.md#53--skills-claude-codes-behavior-layer--the-most-critical-layer-of-the-claude-code-ecosystem).
> For copy-and-run examples, see the [Cookbook](cookbook.en.md).

---

## Where to Go Next

| Your Current State | Next Step |
|---|---|
| You want to understand LLMs, APIs, and tokens | [Stage 1 — LLM Basics](../stages/01-llm-basics.en.md) |
| You want to pick a role-based branch | [Everyday users](../branches/for-everyday-users.en.md) / [Teachers](../branches/for-teacher.en.md) / [Knowledge workers](../branches/for-knowledge-worker.en.md) / [Researchers](../branches/for-researcher.en.md) / [Developers](../branches/for-developer.en.md) |
| You want the full Claude Code ecosystem | [Stage 5 — Claude Code Ecosystem](../stages/05-claude-code-ecosystem.en.md) |
| You want local LLMs without a cloud key | [Cookbook Recipe 6](cookbook.en.md#6-local-llm--cli-agent-quick-walkthrough) |
| You want to compare CLI agents | [CLI Agents Comparison Guide](cli-agents-guide.en.md) |
| A term is unclear | [Glossary](glossary.en.md) |

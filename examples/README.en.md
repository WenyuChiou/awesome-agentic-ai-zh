<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# `examples/` — small runnable exercises

> [← Back to the main README](../README.en.md)

<!-- freshness: canonical=examples/README.md; verified_on=2026-08-30; scope=example-inventory,local-model-tags,download-sizes,sdk-entry-points; max_age_days=90 -->

A Stage page first explains what an idea means. This folder lets you run it once. You do not need to install every model or read every line of code before starting.

## 📌 First, separate five terms

| Core term | Plain explanation | Exact meaning |
|---|---|---|
| **Example** | A small model already assembled | A demonstration program you can run and observe |
| **Starter** | A model with a few pieces left for you | The smallest exercise entry point, usually `starter.py` |
| **Path** | Different roads to the same destination | This project uses Path A, B, and C for different ways to run an exercise |
| **Mock** | Practicing with a toy phone | A fixed fake answer used to check program logic without a real model |
| **Live call** | Making the real phone call | A request to a local or cloud model; output, time, and cost can vary |

## 🎯 What you will learn

- Use a **Mock** to find program errors before a **Live call** checks model behavior.
- Know what Ollama, the Anthropic API, and tests each do.
- Find the right folder from the Stage index instead of guessing filenames.
- Read tests, diffs, and limits instead of treating “it printed something” as proof.

## 📚 Required reading

1. [Setup guide](../resources/setup-guide.en.md): make Python, Git, and your chosen model path work first.
2. [Stage 1: LLM Basics](../stages/01-llm-basics.en.md): choose a model and understand cost and Context.
3. [CLI Agents guide](../resources/cli-agents-guide.en.md): separate a Coding Agent, Router, and Local Runtime.

## 🛠 First run: start with a test that uses no model API

This example has a complete `test.py`. Copy these three lines first:

```powershell
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
python test.py
```

A passing message means the fixed program logic works. It does not prove that every model will answer correctly. Next, choose one real-model path.

| Path | Who produces the answer | First action | Best time to use it |
|---|---|---|---|
| **Path C: Mock** | A fixed fake answer | `python test.py` | First; find program errors |
| **Path A: Ollama** | A model on your computer | Install Ollama and pull the model named by the exercise | Practice real model behavior without a provider model API bill |
| **Path B: Anthropic** | An Anthropic cloud model | Set `ANTHROPIC_API_KEY` | Compare the same exercise with a cloud model |

<details markdown="1">
<summary>Expand the full Path A/B commands, environment, and cost notes</summary>

### Path A: Ollama

```powershell
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

Local execution does not create a provider model API bill, but it still uses storage, memory, electricity, and time. Protect files, logs, and tool permissions.

### Path B: Anthropic API

```powershell
$env:ANTHROPIC_API_KEY = "your-key"
python starter_anthropic.py
```

A cloud call may use quota or create charges. Before running it, check the current official pricing/usage page and set a limit you accept. Never put a key in source code or a commit.

</details>

## 🧭 Find examples by Stage

This table lists folders that actually exist. Short exercises still live directly inside their Stage pages.

| Stage | What this Stage teaches | Runnable folders |
|---|---|---|
| [Stage 1](../stages/01-llm-basics.en.md) | LLM basics and error handling | `stage-1/`: 2 |
| [Stage 2](../stages/02-prompt-engineering.en.md) | Prompt design and a small evaluation loop | `stage-2/`: 1 |
| [Stage 3](../stages/03-tool-use-and-hello-agent.en.md) | **Tool Use & Your First Agent Loop** | `stage-3/`: 6 |
| [Stage 4](../stages/04-agent-frameworks.en.md) | **Workflow Graphs & Agent Frameworks** | `stage-4/`: 5; use a separate Python 3.11 environment for each |
| [Stage 5](../stages/05-claude-code-ecosystem.en.md) | Claude Code ecosystem and Skills | `stage-5/`: 1; the others stay in the Stage page |
| [Stage 6](../stages/06-memory-rag.en.md) | Embeddings, RAG, and Memory | `stage-6/`: 5 |
| [Stage 7](../stages/07-multi-agent-production.en.md) | **Agent Production Engineering** | `stage-7/`: 5 |
| [Track A1–A3](../tracks/cli/A1-cli-intro.en.md) | CLI workflows | Inline exercises; there is no `examples/track-a/` |

## 🧠 Choose a local model

A newer model is not automatically the right model. Start with the tag named by the exercise, then run its fixed tests. Download sizes are the values shown by the official Ollama tag pages on **2026-08-30 UTC**.

| Range | Default tag | Official download size | Why |
|---|---|---:|---|
| Stages 1–2 | [`gemma4:e4b`](https://ollama.com/library/gemma4:e4b) | 9.6 GB | Chat and Prompt exercises |
| Stages 3–6 | [`qwen2.5:3b`](https://ollama.com/library/qwen2.5:3b) | 1.9 GB | Current default for tool-use examples |
| Stage 7 | [`qwen3.5:4b`](https://ollama.com/library/qwen3.5:4b) | 3.4 GB | Observe evaluation, monitoring, and deployment flows |

Current models, prices, Context, and alternatives are maintained only in [Stage 1](../stages/01-llm-basics.en.md), so two pages do not tell two different stories.

## ✅ Folders do not all have the same shape

Open that exercise's `README` first. File names change with the lesson, so a folder is not broken just because it has no plain `starter.py`.

| Shape | Actual folder | What you will see |
|---|---|---|
| Standard two-path | Most Python exercises | `starter.py`, `starter_anthropic.py`, two offline tests, three locale READMEs, and `requirements.txt` |
| Provider switch | `stage-1/04-cross-provider/` | It compares endpoints with one OpenAI-compatible client, so it has only `starter.py` and `test.py` |
| Good/bad schema comparison | `stage-3/06-schema-design/` | `starter_bad*` and `starter_good*` instead of the usual starter names |
| Framework/deployment extra | `stage-4/01-same-agent-two-frameworks/`<br>`stage-4/04-codeact-vs-json-tool/`<br>`stage-7/05-deploy/` | A standard two-path folder plus CrewAI, a Docker smoke test, or a `Dockerfile` |
| Skill package | `stage-5/tool-calling-tutor/` | `SKILL.md`, references, translations, and three locale READMEs; it is not a Python starter project |

Design baseline: every Python exercise must check its fixed logic with an offline test; repository structure tests check the Skill package. Keep starters small; use fake keys in examples; check real model behavior with fixed evals; never disable required hooks or approvals.

<details markdown="1">
<summary>Expand Windows encoding, contribution rules, and troubleshooting</summary>

- On Windows, `starter.py` and `test.py` need UTF-8 stdout configuration so cp950 does not fail on Chinese text or emoji.
- A starter should normally stay under 80 LOC. Route chapter-length depth to official docs or a canonical tutorial.
- When something fails, record the folder, Python version, full error, command, and Path before opening an issue.
- Never upload a real API key, `.env`, private data, or model-response logs.

</details>

## 🎯 Curated Projects and learning resources

Stars are this learning map's reading priority. They are not GitHub stars or an overall tool ranking.

<table>
<thead><tr><th>Group</th><th>Resource</th><th>Learn this first</th><th>Rating</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Model execution</th><td><a href="https://github.com/ollama/ollama">ollama/ollama</a></td><td>Run one model locally, then call it from a starter</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/vllm-project/vllm">vllm-project/vllm</a></td><td>Learn it later when you need server-grade throughput</td><td>⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Python SDKs</th><td><a href="https://github.com/openai/openai-python">openai/openai-python</a></td><td>Understand an OpenAI-compatible client and response shape</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/anthropics/anthropic-sdk-python">anthropics/anthropic-sdk-python</a></td><td>Compare Anthropic messages and tool schemas</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Validation and data</th><td><a href="https://github.com/pytest-dev/pytest">pytest-dev/pytest</a></td><td>Move from small asserts to repeatable tests</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/pydantic/pydantic">pydantic/pydantic</a></td><td>Validate tool input, structured output, and errors</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
</table>

## ✅ Completion check

- [ ] I can use the Stage index to find a folder that really exists.
- [ ] I run a Mock before deciding whether to make a Live call.
- [ ] I know OpenRouter is a Router, Ollama is a Local Runtime, and OpenCode/Pi are Coding Agents.
- [ ] I did not put a key or private data in the repo.
- [ ] I judge results with tests and diffs, not only by whether the program printed something.

<small>Example inventory, model tags, and official entry points checked: 2026-08-30 UTC.</small>

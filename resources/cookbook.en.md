# Cookbook — Turn concepts into real results

> [繁體中文](./cookbook.md) | [简体中文](./cookbook.zh-Hans.md) | **English**

<!-- freshness: canonical=resources/cookbook.md; verified_on=2026-08-30; scope=skills,mcp,documents,gemini-notebook,zotero,local-runtime,cli-tools; max_age_days=90 -->

You do not need to read this Cookbook in one sitting. Pick one result you want, copy its first action, and open the details only when you need the remaining steps.

If these terms are new to you, first return to [Stage 5: Claude Code Ecosystem](../stages/05-claude-code-ecosystem.en.md). To compare OpenRouter, Pi, OpenCode, and Ollama, open the [Complete CLI Agent Guide](cli-agents-guide.en.md).

## 📌 What this Cookbook helps you do

A **Recipe** is a short route from "What do I want to do?" to "How do I know it is done?" Complete any recipe and you will have something you can check—not just another page you have read:

- A reusable action card.
- A small tool an Agent can call.
- A document, research note, or literature workflow.
- A CLI Agent that runs on your own computer.

You will also see **Skill**, **MCP Server**, and **Coding Agent**. They mean a reusable instruction card, a tool connector for an Agent, and an assistant that reads files, edits them, and checks the result.

## 🎯 Choose one recipe first

| What you want to accomplish | Where to start | Key risks |
|---|---|---|
| Let Claude remember a repeatable method | [1. First Skill](#1-write-your-first-skill) | Rules that are too vague |
| Let an Agent call your Python tool | [2. First MCP server](#2-write-your-first-mcp-server) | Giving the tool too much access |
| Generate Word, Excel, PowerPoint, or PDF files | [3. Office Docs Workflow](#3-office-docs-workflow) | Failing to open and inspect the result |
| Get cited answers from your own sources | [4. Gemini Notebook Workflow](#4-gemini-notebook-workflow) | A **Community Integration**—a bridge maintained by users—may stop working |
| Search or organize Zotero items | [5. Zotero Workflow](#5-zotero-workflow) | Writing changes without a preview |
| Use a local model to help edit code | [6. Local LLM + CLI Agent](#6-local-llm--cli-agent-quick-walkthrough) | A model or computer that is too small for the task |

## 🧩 Six core terms

- **Recipe**: A short route from "What do I want to do" to "How do I know it's done?"
- **Skill**: Repeatable instructions placed in `SKILL.md`. The agent reads it only when needed.
- **MCP Server**: A program that presents code, data, or services as tools, resources, or prompts an Agent can use.
- **Community Integration**: A bridge made by the community rather than the product team. It may work well, but an upstream change can break it.
- **Model Runtime**: The program that actually loads and executes the model, such as Ollama; it is not a Coding Agent.
- **Coding Agent**: An assistant that reads files, edits them, runs commands, and checks the result, such as Claude Code, OpenCode, Pi, or Aider.

<details markdown="1">
<summary>⏱️ Expand: time, environment and safety bottom line</summary>

- Each recipe takes about 20–50 minutes; complete the shortest path first, then do the advanced options.
- Git, Python 3.11+, and Node.js 20+ are useful here. Install only what your chosen recipe needs.
- Practice using test materials only. Don't paste passwords, API keys, unpublished papers, or private files into tools you don't trust.
- Before an action deletes, sends, publishes, or changes many files, inspect its diff or preview.

</details>

---

## 1. Write your first Skill

**Result:** Create one reusable instruction card for your project and run it once.

First create a folder:

```bash
mkdir -p .claude/skills/summarize-changes
```

<details markdown="1">
<summary>Expand complete steps, tests and FAQ</summary>

Create `.claude/skills/summarize-changes/SKILL.md`:

```markdown
---
description: Summarize uncommitted changes and flag risks. Use when the user asks what changed or requests a diff review.
---

## Instructions

1. Read the current git diff.
2. Explain the change in three short bullets.
3. List risks, missing tests, and files that should not be committed.
4. If there is no diff, say so. Do not invent changes.
```

After starting Claude Code, enter:

```text
/summarize-changes
```

You can also ask, "What did I just change?" Claude should choose the Skill automatically. It normally notices changes to `SKILL.md` inside an existing skills directory without a restart. Restart only if `.claude/skills/` did not exist when the session began.

Success criteria: The answer is really based on the current diff, and it says "what could go wrong".

FAQ:

| Symptom | What to check first |
|---|---|
| `/summarize-changes` does not exist | Check that the path is exactly `.claude/skills/summarize-changes/SKILL.md` |
| It triggers for unrelated requests | Make the "when to use" sentence in `description` more specific |
| The Skill is becoming too long | Move background material into a reference file in the same folder and read it only when needed |

Start with a project Skill because it travels only with this repository. Move it to the personal path `~/.claude/skills/<name>/SKILL.md` only after you know several projects need the same procedure.

| Often-confused item | What it solves | When to use it |
|---|---|---|
| One-off Prompt | Describes only the task in front of you | The procedure will not be reused |
| **Skill** | Saves how to handle a recurring kind of work | The same procedure recurs in a project |
| **MCP Server** | Provides a new typed tool, data source, or service | The Agent must call an external program or API |

A Skill can direct an Agent to use existing tools, but a Skill is not a new API. Do not use the oversimplification that “Skills cannot read files while MCP can” to distinguish them.

If you want to do a formal eval, you can test the description with a fixed "should trigger/should not trigger" sentence, and then check whether the answer follows the four steps.

</details>

---

## 2. Write your first MCP server

**Result:** Create an MCP tool that adds two numbers and make it visible to Claude Code.

First install the currently stable MCP SDK in a clean Python environment:

```bash
python -m pip install "mcp>=2,<3"
```

<details markdown="1">
<summary>Expand the server program, connection methods and error troubleshooting</summary>

Create `server.py`:

```python
from mcp.server import MCPServer

mcp = MCPServer("hello-mcp")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


if __name__ == "__main__":
    mcp.run()
```

This program is short because MCP v2 creates an input schema from **type hints**, uses the **docstring** as the tool description, and wraps return values as MCP content. Incorrect parameter names, types, or docstrings can make an Agent choose the wrong tool or pass the wrong data.

Add this local stdio server to Claude Code:

```bash
claude mcp add --transport stdio hello-mcp -- python server.py
claude mcp get hello-mcp
```

Enter Claude Code and ask: "Use `add` to calculate 27 + 15." If successful, you should get `42`, and you can see the parameters in the tool call record.

The high-level class in MCP v2 is `MCPServer`, imported with `from mcp.server import MCPServer`. Do not mix this example with old `FastMCP` tutorials or v1 import paths.

Safety bottom line:

- Give a tool only the parameters it needs.
- Limit file tools to the directories they need to read or write.
- Require human approval before writing, paying, sending, or deleting.
- A third-party MCP server may see your data. Check its source and permissions before installing it.

| Transport | Best for | Verification note |
|---|---|---|
| **stdio** | Claude Code or a desktop host on the same computer | Use this for a first server; OAuth is usually not implemented inside the transport |
| **Streamable HTTP** | Remote, multi-user, or service deployments | Design authentication against the current MCP authorization specification; do not copy old HTTP+SSE tutorials |

When you need an API key, read it from an environment variable. Do not put a secret in `server.py`, a configuration example, or Git.

If `claude mcp get` shows failure, first run `python server.py` directly to see the import error, and then confirm that the startup command after `--` is consistent with the Python environment.

</details>

---

## 3. Office Docs Workflow

**Result:** Generate a file from test data, then inspect it in a real Office app or PDF reader.

First download Anthropic's official reference repository:

```bash
git clone --depth 1 https://github.com/anthropics/skills.git anthropic-skills-reference
```

<details markdown="1">
<summary>Expand skill installation, sample prompt and quality check</summary>

The `docx`, `xlsx`, `pptx`, and `pdf` folders in `anthropics/skills` are complex Skill references used in Anthropic products. They are **source-available**, not Apache-2.0 open-source examples. Read each folder's license and `SKILL.md` first.

To try out a skill within a project, place the skill itself at the correct level, rather than wrapping the entire repo in an extra layer:

```bash
mkdir -p .claude/skills
cp -R anthropic-skills-reference/skills/docx .claude/skills/docx
```

PowerShell can be used instead:

```powershell
New-Item -ItemType Directory -Force .claude/skills
Copy-Item -Recurse anthropic-skills-reference/skills/docx .claude/skills/docx
```

The four folders are not interchangeable. Install only the one you want to practice first:

| Skill | First small task | Check when finished |
|---|---|---|
| `docx` | Make a one-page summary from test data | Title, paragraphs, tables, and page breaks |
| `xlsx` | Total a small table while preserving formulas | Formulas, cell types, and values |
| `pptx` | Make three slides from a three-point outline | No overflowing text; images and sources are correct |
| `pdf` | Extract three claims from a public PDF | Page numbers, citations, and source text match |

Copyable DOCX task:

```text
Create a one-page DOCX summary from the test data I provided.
Keep a title, three key points, and a source field. Write "missing" when the data is absent; do not guess.
Reopen the finished file and check for clipped text, blank pages, and broken tables.
```

Check in this order: content → formulas and numbers → layout → whether the file reopens. A message saying "file created" is not proof that the file is correct.

If the skill does not appear, make sure the path is `.claude/skills/docx/SKILL.md`. The file capabilities built into Claude's product may differ from the reference version you clone, so don't claim that the two will necessarily produce exactly the same results.

</details>

---

## 4. Gemini Notebook Workflow

**Result:** Add your own sources and get cited answers you can check against the originals.

Google renamed NotebookLM to **Gemini Notebook**; some packages and URLs still use the old name. Start with the official website:

```bash
python -m webbrowser https://notebooklm.google.com
```

Upload two public documents and ask: "Where do these sources agree and disagree? Cite a source for each point." Open every citation and compare it with the original before you automate anything.

<details markdown="1">
<summary>Expand the community CLI automation path: notebooklm-py</summary>

Google does not currently provide a public official API for this automation. `notebooklm-py` is a community project that uses an unpublished interface. It is useful for personal research and prototypes, but a production workflow needs a fallback in case it breaks.

```bash
uv tool install "notebooklm-py[browser]"
notebooklm login
notebooklm auth check --test --json
notebooklm create "My Research"
notebooklm use NOTEBOOK_ID
notebooklm source add ./paper.pdf
notebooklm ask "List three main claims and cite a source for each one."
```

To make Claude Code or other tools that support Agent Skills use it:

```bash
notebooklm skill install
```

Signing in will open the browser and save the verification status. Don't commit cookies, tokens, or personal browser data to Git.

</details>

<details markdown="1">
<summary>Expand another browser skill and troubleshooting reminder</summary>

[`PleasePrompto/notebooklm-skill`](https://github.com/PleasePrompto/notebooklm-skill) queries notebooks through a browser. It is also an unofficial Google integration and requires a browser login.

How to choose:

| What you need | Best starting point |
|---|---|
| Just want reliable reading and manual verification | Gemini Notebook official website |
| Want to add sources, Q&A or export in batches | `notebooklm-py` CLI |
| You already use Claude Code and want a browser-based Skill | `notebooklm-skill` |

If your login fails, first go back to the official website to confirm that your account can be used normally, and then log in again according to the community project's own auth instructions. Don't use lots of retries to bypass Google's restrictions.

</details>

---

## 5. Zotero Workflow

**Result:** Find an item through Zotero's local API. Before writing anything, preview and approve the change.

In Zotero, enable "Settings → Advanced → Allow other applications on this computer to communicate with Zotero," then test the local API:

```bash
curl http://localhost:23119/api/
```

<details markdown="1">
<summary>Expand search, Zotero 10+ write authorization and security practices</summary>

The local API lives at `http://localhost:23119/api/`. It works offline and is not subject to the Web API rate limit. Zotero 10+ supports `POST`, `PUT`, `PATCH`, and `DELETE`, so old read-only guidance is no longer correct.

Write access is not enabled silently. An app must request a **local API key** from `/api/local/authorize`, and Zotero shows an approval window. This key is different from a zotero.org Web API key and can change any library you are allowed to edit, so:

1. Only read and search for the first time.
2. List the items expected to be added, moved or deleted before writing.
3. Let the user approve in the Zotero window.
4. After practicing, go to Settings → Advanced and press **Clear Write Authorizations** to cancel the remembered key.

When using [`WenyuChiou/zotero-skills`](https://github.com/WenyuChiou/zotero-skills), you can copy this sentence first:

```text
Search only; do not change anything. Find Zotero items published after 2024 about multi-agent evaluation.
List each title, year, DOI, and Zotero item key. Write "not provided" for a missing field.
```

Only try writing for the second time, and ask for preview first:

```text
Prepare to add those results to the "agent-evals" collection.
List the item keys that would move, but do not make the change. Wait for my approval before writing.
```

`403` usually means that the native API is not enabled; `401` means that the write key does not exist or is invalid; `428` means that the write lacks the correct `Zotero-Server-ID`.

</details>

---

## 6. Local LLM + CLI Agent quick walkthrough

**Result:** Let a Coding Agent use a model on your computer to make one small change that Git can undo.

First install [Ollama](https://ollama.com/) and download the current lightweight model:

```bash
ollama pull gemma4:e4b
```

Let’s first distinguish what they are:

| Name | What it does | What it is not |
|---|---|---|
| **Ollama** | Loads and runs a model on your computer | It does not read a repo, edit files, or run tests by itself |
| **OpenRouter** | Routes one API account to many cloud models and providers | It is not a local model or a terminal Coding Agent |
| **OpenCode／Pi／Aider** | Coding Agents that read files, edit them, and run commands | They are not models; each still needs a local or cloud model |
| **Claude Code** | A Coding Agent built for Claude | Its official setup cannot replace Claude with an Ollama model |

<details markdown="1">
<summary>Expand the main path: OpenCode＋Ollama</summary>

OpenCode is the Coding Agent that reads files, edits them, and runs commands; Ollama is the runtime that runs a model locally. Install OpenCode, then start it with `opencode`:

```bash
curl -fsSL https://opencode.ai/install | bash
opencode
```

OpenCode automatically looks for Ollama at `http://127.0.0.1:11434`. In the TUI, select `ollama/gemma4:e4b`, open a practice repo already managed by Git, and paste:

```text
Change only README.md by adding one line: "Local agent test".
First tell me where you will edit. After editing, show the diff and do not commit.
```

Success criteria: only README has been modified, diff meets the requirements, and there are no unfamiliar files in `git status`. When the model is small, the task should also be small; only change one thing at a time.

</details>

<details markdown="1">
<summary>Expand the Aider alternative, Pi／OpenRouter options, and troubleshooting</summary>

Aider officially recommends using `aider-install`, and Ollama model prefix uses `ollama_chat/`:

```bash
python -m pip install aider-install
aider-install
aider --model ollama_chat/gemma4:e4b
```

Other options:

- [Pi](https://github.com/earendil-works/pi) is an extensible Agent harness and Coding Agent. It inherits the user's permissions by default, so use a separate sandbox or container for sensitive projects.
- [OpenRouter](https://openrouter.ai/docs/quickstart) provides one API for many cloud models and providers. It may cost money, and data handling depends on the provider you select.
- The [Complete CLI Agent Guide](cli-agents-guide.en.md) explains when to choose Claude Code, OpenCode, Pi, Aider, OpenRouter, or a local runtime.

FAQ:

| Symptoms | What to do first |
|---|---|
| Ollama model not found | Run `ollama list` and make sure the tag is exactly `gemma4:e4b` |
| Slow answer or out of memory | Use `gemma4:e2b` instead and narrow the task and context |
| Agent changed too many files | Stop immediately and inspect `git diff`; shrink the task to one change in one file |
| Tool calling is unstable | Use a Stage 3 model that officially supports tool calling |

</details>

---

## 📚 Required reading

These are the fact sources for the instructions above. You do not need to read them all: start with the row for your chosen recipe.

<small>Data verification: 2026-08-30 UTC</small>

| Source | What to see first | Editor's Rating |
|---|---|---|
| [Claude Code — Skills](https://code.claude.com/docs/en/slash-commands) | Path, triggering method and live change detection | ⭐⭐⭐⭐⭐ |
| [MCP Python SDK v2 — What’s new](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/whats-new.md) | Differences between `MCPServer` import and v1→v2 | ⭐⭐⭐⭐⭐ |
| [Anthropic Skills](https://github.com/anthropics/skills) | Skill structure and file skill authorization | ⭐⭐⭐⭐⭐ |
| [Google — NotebookLM is now Gemini Notebook](https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/) | The new product name and what remains available | ⭐⭐⭐⭐⭐ |
| [Zotero Local API](https://www.zotero.org/support/dev/web_api/v3/local_api) | Local API, write authorization, and revocation | ⭐⭐⭐⭐⭐ |
| [OpenCode](https://opencode.ai/docs/) | Installation, the `opencode` command, and local model connection | ⭐⭐⭐⭐⭐ |
| [Aider＋Ollama](https://aider.chat/docs/llms/ollama.html) | Correct installation with `ollama_chat/` prefix | ⭐⭐⭐⭐⭐ |
| [Ollama — Gemma 4](https://ollama.com/library/gemma4) | `e2b`/`e4b` tag and hardware selection | ⭐⭐⭐⭐⭐ |

## ⭐ Curated projects and learning resources

The rating measures teaching usefulness in this project. It is not a GitHub star count or a permanent score.

<table>
  <thead><tr><th scope="col">Category</th><th scope="col">Project／resource</th><th scope="col">Use it to</th><th scope="col">Limitation</th><th scope="col">Rating</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">Skills</th><td><a href="https://agentskills.io">Agent Skills standard</a></td><td>Understand the skill format shared across tools</td><td>Each product still has its own expansion field</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/anthropics/skills">anthropics/skills</a></td><td>Read mature skill examples</td><td>File skills are source-available</td><td>⭐⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">MCP</th><td><a href="https://modelcontextprotocol.io/specification">MCP specification</a></td><td>Check the formal definition of protocol</td><td>You don’t have to read it from the beginning to get started</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/modelcontextprotocol/python-sdk">MCP Python SDK</a></td><td>Use Python to write server/client</td><td>Note that v1 and v2 teaching cannot be mixed</td><td>⭐⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">Documents</th><td><a href="https://github.com/anthropics/skills/tree/main/skills/docx">Anthropic DOCX skill</a></td><td>Study a complex document Skill</td><td>Check its license and runtime requirements first</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/anthropics/skills/tree/main/skills/xlsx">Anthropic XLSX skill</a></td><td>Learn spreadsheet analysis and output process</td><td>Finished products still need to be checked with spreadsheet software</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">Gemini Notebook</th><td><a href="https://github.com/teng-lin/notebooklm-py">notebooklm-py</a></td><td>Add sources, ask questions, and export artifacts in batches</td><td>Unofficial; its unpublished API may change</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/PleasePrompto/notebooklm-skill">notebooklm-skill</a></td><td>Query a notebook from Claude Code through a browser</td><td>Unofficial and dependent on browser login</td><td>⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">Zotero</th><td><a href="https://github.com/WenyuChiou/zotero-skills">zotero-skills</a></td><td>Search and organize Zotero from an Agent</td><td>Always preview before writing</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/WenyuChiou/research-hub">research-hub</a></td><td>Connect Zotero, Obsidian, and a research workflow</td><td>More advanced than a single recipe</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/MuiseDestiny/zotero-gpt">zotero-gpt</a></td><td>Chat while reading inside Zotero</td><td>A Zotero plugin follows a different path from an external Agent</td><td>⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">Local/CLI</th><td><a href="https://github.com/anomalyco/opencode">OpenCode</a></td><td>Change programs with local or cloud models</td><td>Check provider and permission settings first</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/earendil-works/pi">Pi</a></td><td>Extensible coding harness/CLI</td><td>No built-in permission isolation by default</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/Aider-AI/aider">Aider</a></td><td>Pair-program with a Git-centered workflow</td><td>Small local models may not code well enough</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
</table>

## ✅ Completion check and next stop

- [ ] I have completed at least one recipe and can point out the generated file, tool or answer.
- [ ] I've seen the success path and I've seen a failure message or error output.
- [ ] I did not submit tokens, cookies, personal files or unpublished information.
- [ ] I know whether I'm using the official feature or Community Integration.
- [ ] Any write or bulk changes have preview, diff or manual approval.

Then return to [Stage 5](../stages/05-claude-code-ecosystem.en.md) to choose the next skill. To find more tools, open the [MCP／Skills Catalog](mcp-skills-catalog.en.md).

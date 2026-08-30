# Extension Path: For Everyday Users

> [繁體中文](./for-everyday-users.md) | [简体中文](./for-everyday-users.zh-Hans.md) | **English**

> [← Back to the main route](../README.en.md) · You do not need to code or finish the whole main route first.

<!-- freshness: canonical=branches/for-everyday-users.md; verified_on=2026-08-29; scope=chat-apps,connectors,cli-agents,local-runtimes,privacy,project-status; max_age_days=90 -->

<a id="use-cases-life-scenarios--how-ai-helps"></a>
## 📌 What this path helps you do

This path teaches you to use AI as an assistant that makes the first draft. You give it the material and request; it makes a draft; you compare that draft with the original, fix it, and decide whether to use it.

You can start with the first exercise. Do not begin with real names, passwords, medical records, contracts, or company secrets.

## 🎯 Learning goals

After this page, you can:

1. State the job, usable material, and output format clearly.
2. Tell a chat interface, **App／Connector**, **CLI Agent**, and local model runtime apart.
3. Check permissions before connecting an account, opening files, or running commands.
4. Compare an AI draft with the **Source** instead of treating fluent writing as a correct answer.

## 🧩 Nine core terms

- **Prompt**: the request you give AI. It is like a short job note that says what to do, what material it may use, and what the result should look like.
- **Source**: the original text, image, or data that AI should follow. Return to it at the end; do not rely only on the model's memory.
- **Private Data**: information you should not casually give away, such as passwords, ID numbers, unpublished company files, or another person's personal data.
- **Hallucination**: AI can write something that sounds real even when it does not know the answer. Smooth writing is not proof.
- **Human Review**: a person compares the draft with the Source item by item, fixes it, and then decides whether to use it.
- **App／Connector**: a door from a chat service to Gmail, Drive, or another service. What it can do depends on the product and the permissions you grant.
- **CLI Agent**: an assistant that works in a terminal. It may read or write files and run commands, so inspect its plan and diff before it acts.
- **Local LLM／Runtime**: software that runs a model on your computer. A runtime runs the model; it is not the same thing as a chat app or CLI Agent.
- **Approval Gate**: a stop where a person confirms before the system sends, edits files, or performs another high-impact action.

## 🛠 First exercise: turn a fictional message into a checkable reminder

This exercise uses **fictional** data only. Copy the whole block into the chat tool you already use:

```text
Source message:
"An said she will give the poster draft to May by Friday. The event date is September 12. The message does not give a delivery time."

Write a short reminder. Use only facts in the source message. Do not guess.
Output:
1. Draft
2. Facts copied
3. Needs confirmation

Do not send this message for me.
```

Then check three things yourself:

1. Can you find every item under `Facts copied` in the Source?
2. Is the missing delivery time under `Needs confirmation`?
3. Did the tool only make a Draft, without sending it?

<a id="where-to-start-4-tiers-by-how-hands-on-are-you"></a>
<a id="tier-recommendations-for-everyday-users"></a>
## 🚪 Choose one of four doors for the job

**These four doors are not levels. Open only the door the job needs.** Most one-off tasks need only the first door; more tools do not automatically make a better result.

<table>
  <thead><tr><th>Door</th><th>Plain explanation</th><th>Good for</th><th>Before it acts</th></tr></thead>
  <tbody>
    <tr><td><strong>Chat surface</strong></td><td>Open a conversation box and ask for a draft</td><td>Writing, explaining an article, or organizing public material</td><td>Remove Private Data and prepare a checkable Source</td></tr>
    <tr><td><strong>App／Connector</strong></td><td>Open a door from chat to another service</td><td>Searching authorized mail, files, or calendars</td><td>Check read and write permissions; keep human confirmation for every write action</td></tr>
  </tbody>
</table>

<a id="tier-2--cli-agents-advanced-users-willing-to-learn-the-command-line"></a>
<table>
  <thead><tr><th>Door</th><th>Plain explanation</th><th>Good for</th><th>Before it acts</th></tr></thead>
  <tbody>
    <tr><td><strong>CLI Agent</strong></td><td>An assistant that works in a terminal</td><td>Repeated file organization or multi-step tasks</td><td>Limit the folder; inspect the preview／dry-run, command, and diff before approval</td></tr>
    <tr><td><strong>Local LLM／Runtime</strong></td><td>The model runs on your own computer</td><td>Offline experiments or data you chose not to send to a cloud model</td><td>Choose a local model; cloud models, web search, and cloud features still use the network</td></tr>
  </tbody>
</table>

If you only want to chat, you do not need a CLI Agent or local runtime. Go to [Track A1](../tracks/cli/A1-cli-intro.en.md) when you want the command line, or [Stage 1](../stages/01-llm-basics.en.md) when you want to understand models.

<a id="required-reading"></a>
## 📖 Required reading

Read these six short starting points. Together they explain how to ask, what a tool can connect to, and where data may go:

1. [OpenAI — Prompt engineering best practices for ChatGPT](https://help.openai.com/en/articles/10032626-how-do-i-prompt-chatgpt-effectively): make the request and context clear.
2. [Anthropic — Get started with Claude](https://support.claude.com/en/articles/8114491-get-started-with-claude): start with normal conversation and add constraints step by step.
3. [OpenAI — Apps in ChatGPT](https://help.openai.com/en/articles/11487775-connectors-in): app capabilities vary by plan, region, and workspace, plus administrator settings.
4. [Anthropic — When to use desktop and web connectors](https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors): distinguish remote connectors from local desktop extensions.
5. [Google — Gemini Apps Privacy Hub](https://support.google.com/gemini/answer/13594961?hl=en): check activity, human review, and third-party policies before connecting data.
6. [Ollama — FAQ](https://docs.ollama.com/faq): distinguish local execution, cloud models, web search, and the `local-only` setting.

For a systematic introduction to prompts, zero-shot, one-shot, few-shot, and verification, continue to [Stage 2 — Prompt Engineering](../stages/02-prompt-engineering.en.md).

<a id="-curated-projects"></a>
## ⭐ Curated projects and learning resources

The stars are this project's editorial rating for beginner value, documentation, and clear safety boundaries—not GitHub stars. Status and limitations were checked on `2026-08-29 UTC`.

<table>
  <thead><tr><th scope="col">Category</th><th scope="col">Entry／project</th><th scope="col">What it is</th><th scope="col">Good for</th><th scope="col">Status／terms</th><th scope="col">Know this first</th><th scope="col">Rating</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Chat surfaces</th><td><a href="https://claude.ai">Claude</a></td><td>Cloud Chat surface</td><td>Reading, writing, and iterative discussion</td><td>Available; commercial cloud service</td><td>Features vary by plan and region; compare important content with the Source</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://chatgpt.com">ChatGPT</a></td><td>Cloud Chat surface</td><td>General questions, voice, and several work entry points</td><td>Available; commercial cloud service</td><td>It can still be wrong; use Human Review for high-impact output</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://gemini.google.com">Gemini</a></td><td>Google cloud Chat surface</td><td>Questions and eligible Google service connections</td><td>Available; commercial cloud service</td><td>Check activity and human review settings; do not add confidential data</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://perplexity.ai">Perplexity</a></td><td>Cloud search assistant with source links</td><td>Finding candidate sources and starting verification</td><td>Available; commercial cloud service</td><td>A citation is not proof; open each source</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Official starter and safety guides</th><td><a href="https://help.openai.com/en/articles/10032626-how-do-i-prompt-chatgpt-effectively">OpenAI Prompt Guide</a></td><td>Official ChatGPT guidance</td><td>Clear, specific, iterative prompting</td><td>Current; official guidance</td><td>A good prompt cannot guarantee correctness; still verify</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://support.claude.com/en/articles/8114491-get-started-with-claude">Claude Get Started</a></td><td>Official Claude introduction</td><td>First conversation and basic controls</td><td>Current; official guidance</td><td>Plans have usage limits; do not assume every feature is available</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://help.openai.com/en/articles/11487775-connectors-in">Apps in ChatGPT</a></td><td>Official App／Connector guide</td><td>Understanding search, sync, and external actions</td><td>Commercial; commercial cloud service</td><td>Capabilities and permissions differ; high-impact actions need human confirmation</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://support.google.com/gemini/answer/13594961?hl=en">Gemini Privacy Hub</a></td><td>Official Gemini privacy guidance</td><td>Checking settings before connecting Google or third-party data</td><td>Current; official privacy guidance</td><td>Sensitive content may be processed; do not connect confidential data you would not want a reviewer to see</td><td>⭐⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">CLI Agents</th><td><a href="https://github.com/anthropics/claude-code">Claude Code</a></td><td>Anthropic CLI Agent</td><td>Reading, editing, and running tasks inside a chosen workspace</td><td>Active; commercial service; repository has no standard open-source license</td><td>Set permissions; inspect commands and diffs before approval</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/openai/codex">Codex</a></td><td>OpenAI coding agent</td><td>App／CLI／IDE／cloud work</td><td>Active; repository code is Apache-2.0, while app/cloud follow their service terms</td><td>Use approval to limit file writes, commands, and external actions</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/anomalyco/opencode">OpenCode</a></td><td>Coding agent／harness that can connect to several providers</td><td>Multi-step model work in a terminal or desktop app</td><td>Active; MIT</td><td>Providers still need accounts or API keys; use permissions and AGENTS.md to limit scope</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/google-gemini/gemini-cli">Gemini CLI</a></td><td>Google CLI Agent</td><td>Using Gemini and tools in a terminal</td><td>Active; Apache-2.0</td><td>Inspect the diff and command; a sandbox only reduces risk</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">Local LLM runtimes</th><td><a href="https://github.com/ollama/ollama">Ollama</a></td><td>Local model runtime</td><td>Downloading and running models on your computer</td><td>Active; MIT</td><td>Choose a local model; cloud models and web search are not local inference</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://lmstudio.ai/">LM Studio</a></td><td>Graphical local model runtime</td><td>Loading downloaded models through a desktop interface</td><td>Commercial; commercial desktop application</td><td>Local features can work offline; cloud models, search, and other cloud features still use the network</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="1">Prompt material</th><td><a href="https://github.com/f/prompts.chat">prompts.chat</a></td><td>Community prompt examples</td><td>Finding sentence patterns to adapt to your job</td><td>Active; MIT / CC0</td><td>Quality varies; do not paste Private Data directly</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
</table>

<details markdown="1">
<summary>🔐 Accounts, data, permissions, and cost</summary>

- Whether an App／Connector appears depends on the **plan, region, and workspace**, device, and administrator settings. A missing feature does not mean you did something wrong.
- Before connecting, ask: what can it read, what does it send to which service, can it write back, and how do I revoke access?
- Search and drafting are usually lower-impact. Sending mail, changing a calendar, deleting files, or purchasing is a write action and must keep an Approval Gate plus human confirmation.
- Free quotas, subscriptions, and API prices change. Check the current plan shown by the product instead of relying on a fixed price in this guide.
- If you are unsure whether you may upload something, do not upload it. Publicly readable does not mean you have permission to give someone else's content to a third-party service for processing.

</details>

<details markdown="1">
<summary>🧪 Advanced CLI Agent and local-model steps</summary>

A safe CLI Agent start:

1. Put a few recoverable fictional files in a test folder.
2. Ask for a read-only plan or preview／dry-run first.
3. Limit read and write access to that folder.
4. Inspect the command and diff before approving a small step.
5. Review the result yourself. Do not start by letting it send mail, delete files, pay, push, or deploy.

Official boundaries:

- [Gemini CLI tools](https://geminicli.com/docs/reference/tools/) show an action before a mutating tool runs; the [sandbox guide](https://geminicli.com/docs/cli/sandbox/) also says a sandbox is not a zero-risk guarantee.
- [OpenCode permissions](https://opencode.ai/docs/agents/) can set ask／allow／deny for edit, bash, and external folders; its [provider guide](https://opencode.ai/docs/providers/) shows that model access still needs the matching account, OAuth, API key, or environment setup.
- Ollama can enable [cloud models](https://docs.ollama.com/cloud). For local-only use, follow the FAQ and set `disable_ollama_cloud` or `OLLAMA_NO_CLOUD=1`.
- LM Studio's [offline guide](https://lmstudio.ai/docs/app/offline) says downloaded models, chats, documents, and the local server can work offline; its [privacy guide](https://lmstudio.ai/app-privacy) separates local processing from cloud models and web search.

</details>

<a id="workflows-you-can-build-by-frequency"></a>
<details markdown="1">
<summary>🧰 More workflows, alternatives, and troubleshooting</summary>

Low-risk workflows you can add slowly:

- **Language practice**: ask AI to be a conversation partner, correct only two errors at a time, and check the final explanation against your learning material.
- **Weekly-note draft**: use only notes you are willing to place in the tool; list facts before writing the summary.
- **Public article summary**: attach the original, ask each point to name its Source paragraph, and open the original yourself.
- **Fictional file cleanup**: preview new filenames in a test folder and rename only after human approval.

Common problems:

- The answer invents missing facts: make the job smaller and say, “If it is unknown, put it under Needs confirmation.”
- A connector cannot find data: check permissions in the original service, the plan, the workspace administrator, and the supported surface.
- A local model is slow: try a smaller model; “it runs” does not mean “it answers correctly.”
- You do not know which door to choose: do the first exercise in a Chat surface. Open another door only when you truly need external-service access, file changes, or offline work.

</details>

<a id="community-notes"></a>
## ✅ Completion check and next stop

- [ ] I can explain the difference between a Chat surface, App／Connector, CLI Agent, and Local LLM／Runtime.
- [ ] I know AI can Hallucinate, so I return to the Source for Human Review.
- [ ] I do not paste Private Data into a service whose data policy I do not understand.
- [ ] I keep an Approval Gate before sending, editing files, running commands, or another high-impact action.

Choose your next stop by need:

- Write clearer prompts: continue to [Stage 2](../stages/02-prompt-engineering.en.md).
- Use a CLI Agent safely: continue to [Track A1](../tracks/cli/A1-cli-intro.en.md).
- Distinguish Apps, Connectors, MCP, and automation: use the [knowledge-worker path](./for-knowledge-worker.en.md).
- Help improve this path: read [CONTRIBUTING.en.md](../CONTRIBUTING.en.md).

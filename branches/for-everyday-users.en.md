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

<!-- connector-safety:start -->
**Before connecting an account, ask four questions:**

1. **What will it read?** Grant only the data this task needs.
2. **Where will it send data?** Check which services will receive it.
3. **What can it change?** Keep an **Approval Gate** before sending mail, editing files, or paying.
4. **How do I take it back?** Find how to stop the task, revoke the connection, and delete stored data.
<!-- connector-safety:end -->

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

<div class="reader-route-table" role="region" tabindex="0" aria-label="Chat and connector entry comparison">
<table align="center">
  <thead><tr><th>Door</th><th>Plain explanation</th><th>Good for</th><th>Before it acts</th></tr></thead>
  <tbody>
    <tr><td><strong>Chat surface</strong></td><td>Open a conversation box and ask for a draft</td><td>Writing, explaining an article, or organizing public material</td><td>Remove Private Data and prepare a checkable Source</td></tr>
    <tr><td><strong>App／Connector</strong></td><td>Open a door from chat to another service</td><td>Searching authorized mail, files, or calendars</td><td>Check read and write permissions; keep human confirmation for every write action</td></tr>
  </tbody>
</table>
</div>

<a id="tier-2--cli-agents-advanced-users-willing-to-learn-the-command-line"></a>
<div class="reader-route-table" role="region" tabindex="0" aria-label="CLI and local model entry comparison">
<table align="center">
  <thead><tr><th>Door</th><th>Plain explanation</th><th>Good for</th><th>Before it acts</th></tr></thead>
  <tbody>
    <tr><td><strong>CLI Agent</strong></td><td>An assistant that works in a terminal</td><td>Repeated file organization or multi-step tasks</td><td>Limit the folder; inspect the preview／dry-run, command, and diff before approval</td></tr>
    <tr><td><strong>Local LLM／Runtime</strong></td><td>The model runs on your own computer</td><td>Offline experiments or data you chose not to send to a cloud model</td><td>Choose a local model; cloud models, web search, and cloud features still use the network</td></tr>
  </tbody>
</table>
</div>

If you only want to chat, you do not need a CLI Agent or local runtime. Go to [Track A1](../tracks/cli/A1-cli-intro.en.md) when you want the command line, or [Stage 1](../stages/01-llm-basics.en.md) when you want to understand models.

## 🧑 Personal Agents: define the goal and boundaries first

<small>Personal Agent products checked: 2026-10-02 UTC; additions and re-verification: 2026-10-16 UTC. Only Claude Duet was added on `2026-10-23 UTC`.</small>

A **Personal Agent** can do multi-step work across tools after you give it a goal, like researching, drafting, and returning for approval. These products combine a model, tools, and permissions; a product name is not an underlying model name or a new upgrade level.

Messaging-based personal agents belong here too: look for ongoing personal context, everyday-tool access, and delegated tasks with follow-through. The table adds startup-origin Instinct, Tab, Tomo, and Poke; Poke has joined Cognition and is not listed as independent. Companionship chatbots, standalone reminders, and business workflow platforms do not necessarily fit this scope. See “Accounts, data, permissions, and cost” below for access and privacy details.

Start with the fictional message above, without connecting accounts. When you need multiple tools, specify what the agent may read or change and when it must stop for your approval. Keep an **Approval Gate** before sending, publishing, deleting files, or paying; ongoing work still needs human review.

**Claude Duet** follows tasks, not a new model. It is a US Pro／Max research preview by waitlist invitation; Team／Enterprise is not open. The official guide says it asks approval before sending mail, paying, signing, or deleting. Revoke an App connection; **memory is not automatically deleted**. Read [access and data limits](https://support.claude.com/en/articles/17631495-get-started-with-claude-duet) before connecting.

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

The stars are this project's editorial rating for beginner value, documentation, and clear safety boundaries, not GitHub stars. Other resources retain their `2026-08-29 UTC` status check. Personal Agent entries were added or re-verified on `2026-10-16 UTC`. They receive three stars as optional concrete product examples to compare, rather than required tools. Only Claude Duet was added on `2026-10-23 UTC`. These are untested reference/comparison examples. Ratings reflect documented teaching value, not hands-on product quality.

<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="Resources by category, use and limits">
<table align="center">
  <thead><tr><th scope="col">Group</th><th scope="col">Project / document</th><th scope="col">Rating</th><th scope="col">Use</th><th scope="col">Limits</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">Chat surfaces</th><td><div data-field="entry"><strong><a href="https://claude.ai">Claude</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity">Cloud Chat surface</div><div data-field="use">Reading, writing, and iterative discussion</div></td><td><div data-field="status">Available; commercial cloud service</div><div data-field="limits">Features vary by plan and region; compare important content with the Source</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://chatgpt.com">ChatGPT</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity">Cloud Chat surface</div><div data-field="use">General questions, voice, and several work entry points</div></td><td><div data-field="status">Available; commercial cloud service</div><div data-field="limits">It can still be wrong; use Human Review for high-impact output</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://gemini.google.com">Gemini</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="identity">Google cloud Chat surface</div><div data-field="use">Questions and eligible Google service connections</div></td><td><div data-field="status">Available; commercial cloud service</div><div data-field="limits">Check activity and human review settings; do not add confidential data</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://perplexity.ai">Perplexity</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="identity">Cloud search assistant with source links</div><div data-field="use">Finding candidate sources and starting verification</div></td><td><div data-field="status">Available; commercial cloud service</div><div data-field="limits">A citation is not proof; open each source</div></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="8" align="center" valign="middle" width="80">Personal Agents</th><td><div data-field="entry"><strong><a href="https://learn.chatgpt.com/docs/dots">OpenAI dots</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐</span></td><td><div data-field="identity">Personal Agent product／official docs</div><div data-field="use">For everyday users learning ongoing tasks and approval boundaries. Teaches goals, tools, and approval boundaries with fictional data.</div></td><td><div data-field="status">Gradual rollout; commercial cloud service</div><div data-field="limits">Plan, age, region, and admin limits; your account may not have access yet</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://support.claude.com/en/articles/17631495-get-started-with-claude-duet">Claude Duet</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐</span></td><td><div data-field="identity">Personal Agent product／official docs</div><div data-field="use">For everyday users comparing ongoing tasks. Teaches limiting data before approving external actions.</div></td><td><div data-field="status">Research preview; US Pro／Max, waitlist invitation required; commercial cloud service</div><div data-field="limits">Team／Enterprise not open; revoking a connection does not delete memory automatically</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/">Meta Muse</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐</span></td><td><div data-field="identity">Personal Agent product／official introduction</div><div data-field="use">For everyday users and small-business owners practicing cross-app drafts. Teaches cross-app drafting and human approval before actions.</div></td><td><div data-field="status">Region-limited; commercial cloud service</div><div data-field="limits">US and Canada; Meta says publishing, sending, and spending require approval</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://docs.x.ai/grok-bot/overview">Grok Bot</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐</span></td><td><div data-field="identity">Personal Agent product／official docs</div><div data-field="use">For everyday users comparing ongoing tasks and shared data. Teaches ongoing tasks and shared-computer data boundaries.</div></td><td><div data-field="status">Eligible-plan access; commercial cloud service</div><div data-field="limits">Eligible paid plan required; same-account Bots share files and logins</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://instinct.com/">Instinct</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐</span></td><td><div data-field="identity">Text/call personal agent</div><div data-field="use">For users comparing everyday delegation. Teaches model-training and permission boundaries.</div></td><td><div data-field="status">Commercial service; check account eligibility</div><div data-field="limits">18+; training opt-out has exceptions</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://tab.bot/">Tab</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐</span></td><td><div data-field="identity">Messaging personal agent</div><div data-field="use">For users comparing cross-tool delegation. Teaches waitlists, payment approval, and credential separation.</div></td><td><div data-field="status">Private beta; commercial service</div><div data-field="limits">Waitlist does not guarantee access; limited-beta payments</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://www.tomo.ai/about">Tomo</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐</span></td><td><div data-field="identity">Mapo Labs personal AI</div><div data-field="use">For goal tracking and daily planning. Teaches ongoing context and group-chat data boundaries.</div></td><td><div data-field="status">Paid plans; commercial service</div><div data-field="limits">Authorized staff may review chats; groups include others’ data</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://poke.com/">Poke</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐</span></td><td><div data-field="identity">Startup-origin messaging personal agent</div><div data-field="use">For users comparing email/calendar automation. Teaches proactive reminders, plans, and ownership changes.</div></td><td><div data-field="status">Free/paid plans; joined Cognition</div><div data-field="limits">Check usage, extra charges, and Maximum Privacy</div></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">Official starter and safety guides</th><td><div data-field="entry"><strong><a href="https://help.openai.com/en/articles/10032626-how-do-i-prompt-chatgpt-effectively">OpenAI Prompt Guide</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity">Official ChatGPT guidance</div><div data-field="use">Clear, specific, iterative prompting</div></td><td><div data-field="status">Current; official guidance</div><div data-field="limits">A good prompt cannot guarantee correctness; still verify</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://support.claude.com/en/articles/8114491-get-started-with-claude">Claude Get Started</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity">Official Claude introduction</div><div data-field="use">First conversation and basic controls</div></td><td><div data-field="status">Current; official guidance</div><div data-field="limits">Plans have usage limits; do not assume every feature is available</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://help.openai.com/en/articles/11487775-connectors-in">Apps in ChatGPT</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity">Official App／Connector guide</div><div data-field="use">Understanding search, sync, and external actions</div></td><td><div data-field="status">Commercial; commercial cloud service</div><div data-field="limits">Capabilities and permissions differ; high-impact actions need human confirmation</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://support.google.com/gemini/answer/13594961?hl=en">Gemini Privacy Hub</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity">Official Gemini privacy guidance</div><div data-field="use">Checking settings before connecting Google or third-party data</div></td><td><div data-field="status">Current; official privacy guidance</div><div data-field="limits">Sensitive content may be processed; do not connect confidential data you would not want a reviewer to see</div></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">CLI Agents</th><td><div data-field="entry"><strong><a href="https://github.com/anthropics/claude-code">Claude Code</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity">Anthropic CLI Agent</div><div data-field="use">Reading, editing, and running tasks inside a chosen workspace</div></td><td><div data-field="status">Active; commercial service; repository has no standard open-source license</div><div data-field="limits">Set permissions; inspect commands and diffs before approval</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/openai/codex">Codex</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity">OpenAI coding agent</div><div data-field="use">App／CLI／IDE／cloud work</div></td><td><div data-field="status">Active; repository code is Apache-2.0, while app/cloud follow their service terms</div><div data-field="limits">Use approval to limit file writes, commands, and external actions</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/anomalyco/opencode">OpenCode</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity">Coding agent／harness that can connect to several providers</div><div data-field="use">Multi-step model work in a terminal or desktop app</div></td><td><div data-field="status">Active; MIT</div><div data-field="limits">Providers still need accounts or API keys; use permissions and AGENTS.md to limit scope</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/google-gemini/gemini-cli">Gemini CLI</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="identity">Google CLI Agent</div><div data-field="use">Using Gemini and tools in a terminal</div></td><td><div data-field="status">Active; Apache-2.0</div><div data-field="limits">Inspect the diff and command; a sandbox only reduces risk</div></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2" align="center" valign="middle" width="80">Local LLM runtimes</th><td><div data-field="entry"><strong><a href="https://github.com/ollama/ollama">Ollama</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="identity">Local model runtime</div><div data-field="use">Downloading and running models on your computer</div></td><td><div data-field="status">Active; MIT</div><div data-field="limits">Choose a local model; cloud models and web search are not local inference</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://lmstudio.ai/">LM Studio</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="identity">Graphical local model runtime</div><div data-field="use">Loading downloaded models through a desktop interface</div></td><td><div data-field="status">Commercial; commercial desktop application</div><div data-field="limits">Local features can work offline; cloud models, search, and other cloud features still use the network</div></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="1" align="center" valign="middle" width="80">Prompt material</th><td><div data-field="entry"><strong><a href="https://github.com/f/prompts.chat">prompts.chat</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="identity">Community prompt examples</div><div data-field="use">Finding sentence patterns to adapt to your job</div></td><td><div data-field="status">Active; MIT / CC0</div><div data-field="limits">Quality varies; do not paste Private Data directly</div></td></tr>
  </tbody>
</table>
</div>

<details markdown="1">
<summary>🔐 Accounts, data, permissions, and cost</summary>

- Whether an App／Connector appears depends on the **plan, region, and workspace**, device, and administrator settings. A missing feature does not mean you did something wrong.
- Before connecting, ask: what can it read, what does it send to which service, can it write back, and how do I revoke access?
- Search and drafting are usually lower-impact. Sending mail, changing a calendar, deleting files, or purchasing is a write action and must keep an Approval Gate plus human confirmation.
- Free quotas, subscriptions, and API prices change. Check the current plan shown by the product instead of relying on a fixed price in this guide.
- If you are unsure whether you may upload something, do not upload it. Publicly readable does not mean you have permission to give someone else's content to a third-party service for processing.

Personal Agent product details (2026-10-16 UTC; document checks, not hands-on tests):

- [Claude Duet](https://support.claude.com/en/articles/17631495-get-started-with-claude-duet) (only this item: `2026-10-23 UTC`): works on its own cloud computer, uses Claude Opus 5.5, and does not let you choose the model. Background work counts against Pro／Max plan usage; it is not an unlimited free API. Existing Claude memory, Skills, and connectors continue to apply. Check shared data and memory settings first; sending mail, paying, signing, and deleting still require human approval. See the [10/21 official announcement](https://claude.com/resources/articles/claude-duet).

- [OpenAI dots](https://learn.chatgpt.com/docs/dots): an always-on cloud assistant with its own cloud computer and browser (underlying model: GPT-6 Astra); work can continue while your computer is off. It remembers your preferences and ongoing work, runs background agents in parallel, and must get your permission before sharing private-conversation information with others. The [2026-09-29 update](https://learn.chatgpt.com/docs/whats-new/devday-2026) describes a gradual rollout. Pro 100, Pro 200, and Pro 500 require users over 18 outside the European Economic Area, United Kingdom, and Switzerland. Business Premium and Enterprise are rolling out worldwide; Enterprise needs administrator enablement. An eligible plan does not mean your account has access yet.
- [Meta Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/): works across apps on its own cloud computer. The [2026-09-29 Muse for Small Business update](https://about.fb.com/news/2026/09/introducing-muse-small-business/) confirms US and Canada access and adds business skills and connectors; Meta says publishing, sending, and spending require your approval. A separate Sentinel agent reviews outbound network actions; Muse provides an activity audit trail. Passwords and payment details are stored separately in secure storage that Muse itself cannot see. Muse is the product; Muse Spark is a model, and Muse Code is a terminal coding agent.
- [Grok Bot](https://docs.x.ai/grok-bot/overview): uses a browser, files, and terminal on a persistent cloud computer; access needs a paid Cursor plan or an eligible linked SuperGrok plan; usage resets weekly. Bots on the same account share the computer, files, browser sessions, and app logins, so do not treat them as isolated from one another. The [2026-09-28 Team Bots update](https://x.ai/news/team-bots) adds a public beta for Teams and Enterprise, with shared skills and tools and Slack collaboration. Grok Bot is a product, not a Grok model name or the coding agent [Grok Build](https://docs.x.ai/build/overview).
- [Instinct](https://instinct.com/) (Spear Street Technology): accepts everyday requests by text or call, with shopping and ticket-booking examples. Its [terms](https://instinct.com/terms) require users to be 18+. Complete pricing and regional eligibility are not listed publicly; check the current account offer. Its [privacy policy](https://instinct.com/privacy-policy) permits some model training with an opt-out and exceptions. Do not assume every external action automatically waits for approval.
- [Tab](https://tab.bot/) (Terrasoft): delegates work through messages, retains previous context, and uses its own computer, browser, connected accounts, and outbound calls. It is in [private beta](https://tab.bot/terms); waitlisting guarantees neither access timing, pricing, nor features. Payments are limited-beta features. Its [security documentation](https://tab.bot/security) describes transaction-specific approval and separate credential/payment flows; do not paste passwords or card details into messages.
- [Tomo](https://www.tomo.ai/about) (Mapo Labs): a small-team personal AI with remembered context, proactive reminders, email, and calendar connections. Useful for comparing goal follow-through and everyday scheduling. Paid plans have user-dependent pricing and messaging limits. Its [privacy policy](https://www.tomo.ai/privacy) permits authorized staff to review conversations and covers data from other group-chat participants; check sharing boundaries first.
- [Poke](https://poke.com/) (The Interaction Company, now [part of Cognition](https://cognition.com/blog/interaction)): combines personal context, connected services, and proactive messages for email, calendars, and automations. [Plans](https://poke.com/pricing) include free and paid tiers; check usage limits and additional charges. Its [privacy policy](https://poke.com/privacy) excludes Maximum Privacy users’ data from model training; review settings before connecting personal accounts.

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
- [ ] I can distinguish a Personal Agent product from a model and check access and shared-data boundaries.

Choose your next stop by need:

- Write clearer prompts: continue to [Stage 2](../stages/02-prompt-engineering.en.md).
- Use a CLI Agent safely: continue to [Track A1](../tracks/cli/A1-cli-intro.en.md).
- Distinguish Apps, Connectors, MCP, and automation: use the [knowledge-worker path](./for-knowledge-worker.en.md).
- Help improve this path: read [CONTRIBUTING.en.md](../CONTRIBUTING.en.md).

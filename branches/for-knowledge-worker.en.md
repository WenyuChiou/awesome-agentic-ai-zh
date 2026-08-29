# Extension Path: For Knowledge Workers

> [繁體中文](./for-knowledge-worker.md) | [简体中文](./for-knowledge-worker.zh-Hans.md) | **English**

> 🚀 **No development background at all?** Most knowledge workers can start directly with Claude.ai / Claude Desktop, **without any setup**. Only read [`resources/setup-guide.en.md` A-D](../resources/setup-guide.en.md) (30-45 minutes from zero) when you need to connect an MCP server (such as Gmail / Notion) or use CLI automation.

> [← Back to main path README](../README.en.md) · Continue here after **Track A's A3** or **Track B's Stage 7**. Apply agentic AI to office / knowledge work.

## Use Cases (Office Scenarios × How AI Helps)

The table below splits a knowledge worker's day into 7 common scenarios. Most of them are covered by Claude Desktop + MCP at Tier 1:

| Scenario | Pain point | How AI helps | Recommended tools |
|---|---|---|---|
| **Email triage** | 100 messages a day; priority is hard to judge | Categorize + draft replies for your review | Claude Desktop + Gmail MCP |
| **Meetings → action items** | You forget half of a 30-minute meeting; action items are not captured | Transcript → key decisions + action items | Otter / Zoom transcript + Claude |
| **Cross-tool report aggregation** | Slack / Gmail / Notion each hold part of the picture | Pull metrics + synthesize + email summary | n8n / Make / Langflow |
| **Research / market intelligence** | Hard to know what to ask or who to trust | Multi-source search + cross-validation + memo | Perplexity + Claude |
| **Slack / messaging** | Tone is hard to calibrate in sensitive situations | Rewrite + adjust tone + produce alternatives | Claude.ai |
| **Notion / knowledge-base cleanup** | Notes are messy, unstructured, and hard to find | Retag + classify + auto-summarize | Claude Desktop + Notion MCP |
| **Documents / proposal drafts** | Specs and proposals get stuck | Outline → sections → polish | Claude.ai |

> 💡 **MCP is central for knowledge workers**: new to MCP? Read [Stage 5.2 — MCP Foundation](../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol--foundation). Looking for available MCP servers? See [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md).

## Curated Projects

> 💡 **Want to wire your AI agent to Notion / Gmail / Outlook / Slack / Excel / Lark?** Example: automatically turn Gmail messages into Notion todos. 81+ commonly-used office integration tools are listed in [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md) (grouped by use case). The section below stays focused on workflow / integration-platform-level tools.

### Workflow Tools

#### [n8n](https://github.com/n8n-io/n8n) ⭐⭐⭐⭐
Self-hostable workflow automation platform with built-in AI integration; visual node-based editor.

**Best for**: When you need glue between many SaaS tools (Slack + Gmail + Notion + AI).

---

#### [Make.com](https://www.make.com/) (formerly Integromat)
Hosted workflow automation. Strong AI integration nodes.

---

### Knowledge Worker Skills

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐

Brainstorming, planning, and decision-making skills.

---

### Knowledge Management / Personal AI

#### [khoj-ai/khoj](https://github.com/khoj-ai/khoj) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 36k+ |
| License | AGPL-3.0 |

**What it teaches**: Self-hosted "second brain" — chat with web + local docs, schedule automations, build custom agents.

**Best for**: People wanting a self-hosted personal knowledge base + AI assistant.

**Notes**: AGPL-3.0 license (copyleft).

---

#### [lobehub/lobehub](https://github.com/lobehub/lobehub) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 81k+ |
| License | LobeHub Community License (Apache-2.0 base + commercial conditions) |

**What it teaches**: Deployable multi-agent chat platform — plugin marketplace, knowledge bases, team collaboration. One representative option for self-hosted AI workspaces.

**Best for**: Self-hosting a collaborative chat workspace.

**Notes**: Commercial use needs to verify the LobeHub Community License's added conditions.

---

#### [langflow-ai/langflow](https://github.com/langflow-ai/langflow) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 147k+ |
| License | MIT |

**What it teaches**: Visual AI-agent design platform — useful for mapping customer support, report assembly, and data-query workflows into nodes. More agent-focused than n8n (n8n is generic workflow). API / MCP server deployment is an advanced note, not something you need to learn first.

**Best for**: Knowledge workers who'd rather wire nodes than write Python; or anyone designing agent flows for team handoff.

---

#### [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 64k+ |
| License | MIT |

**What it teaches**: All-in-one private RAG workspace — upload documents, build agents, MCP-compatible, on-device by default. **A self-hosted alternative to NotebookLM**.

**Best for**: Knowledge workers wanting a NotebookLM-style tool, self-hosted, without sending data to the cloud.

---

### MCP Servers Useful for Knowledge Workers

#### Communication MCP servers ⭐⭐⭐⭐
Slack / Gmail / Discord etc. The original Anthropic-hosted reference servers were reorganized in 2025; community-maintained servers now live in [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers#communication) and [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers). Browse those lists for current Slack / Gmail / Drive / Calendar MCP servers.

---

## Workflows You Can Build (by frequency)

| Frequency | Workflow | Steps (≤3) | Recommended tools | Best for |
|---|---|---|---|---|
| **Daily** | Email triage | (1) Scan inbox<br>(2) Categorize into "now / today / this week / no reply"<br>(3) Draft replies for your review | Claude Desktop + Gmail MCP | All knowledge workers |
| **Per meeting** | Meetings → action items | (1) Capture transcript (Otter / Zoom)<br>(2) Have Claude extract "key decisions + action items"<br>(3) Assign + announce in Slack / email | Claude.ai + transcript tool | Managers / PMs |
| **Weekly** | Cross-tool report | (1) Pull metrics from N tools<br>(2) Synthesize with Claude / n8n<br>(3) Send email summary | n8n / Make / Langflow | People who send regular updates |
| **Occasional** | Research / market intelligence | (1) Clarify the question<br>(2) Search multiple sources + cross-validate<br>(3) Write a 1-2 page memo | Perplexity + Claude | Analysts / strategy roles |
| **Occasional** | Notion / knowledge-base cleanup | (1) Paste scattered notes into Claude<br>(2) Ask it to retag + classify<br>(3) Output structured Notion format | Claude Desktop + Notion MCP | Notion / Obsidian users |

> 💡 **Starter habit**: run "daily email triage" for a month first so "open inbox, open Claude" becomes natural. Adding too many automations at once is hard to sustain.

## Tier Recommendations

Recommended progression:

| Tier | Tools | Best for | Learning cost |
|---|---|---|---|
| **Tier 0** | Claude.ai / ChatGPT / Gemini / Perplexity (web) | Most knowledge workers start here | 0 (if you can use a browser) |
| **Tier 1** | Claude Desktop + MCP (Gmail / Notion / calendar) | Repeat workflows over local / cloud files | Half a day |
| **Tier 2** | n8n / Make / Langflow (automation platforms) | Connecting several SaaS tools without writing code | 1 week of setup |
| **Tier 3** | Claude Code / Codex / your own Python | Dev background or dev support, workflows ready for production deployment | Several weeks, overlaps with Track A |

**Tier 3+ (CLI / SDK) is too heavy for most knowledge worker tasks**. Most people can stop at Tier 1-2.

## Reading

- [How I Turned Claude Code Into My Personal AI Agent OS](https://aimaker.substack.com/p/how-i-turned-claude-code-into-personal-ai-agent-operating-system-for-writing-research-complete-guide) — knowledge worker case study
- [**Anthropic — The Founder's Playbook**](https://claude.com/blog/the-founders-playbook) — Anthropic's 35-page startup playbook (2026-05-14); maps Idea / MVP / Launch / Scale onto 2026 AI capability

# MCP / Skills Integration Catalog

> [繁體中文](./mcp-skills-catalog.md) | [简体中文](./mcp-skills-catalog.zh-Hans.md) | **English**

> This is a task-based catalog for finding tools when needed, not an install list. Start with an official entry point; expand a category only when the work calls for it.

## 📌 How to use this catalog

1. First state whether you need to read data or write to a real service.
2. Prefer official hosted / reference entry points, then check maintenance, licensing, and permissions.
3. Start with test data, read-only access, and least privilege. Keep human approval before write, send, or delete actions.

Installation and testing belong in [Stage 5](../stages/05-claude-code-ecosystem.en.md); this page only helps you find candidates.

## 🧩 Five terms to separate first

- **MCP Server**: a program or hosted service that exposes data or actions as MCP tools.
- **Skill**: reusable instructions, scripts, templates, and references; loading differs by host.
- **Plugin**: a host-specific package that may bundle Skills, commands, hooks, or MCP configuration; it is not the MCP specification.
- **Remote MCP**: an MCP Server operated by a provider, usually using OAuth, so you do not run it locally.
- **Permission Boundary**: the range an Agent can actually read, write, send, or delete. A tool being capable does not mean every action should run.

## 📚 Five safe starting points

| Starting point | Learn first | Editorial rating |
|---|---|---|
| [Official MCP Registry](https://registry.modelcontextprotocol.io/) | Find published MCP Servers; still check the maintainer, permissions, and source | ⭐⭐⭐⭐⭐ |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | See educational reference implementations; they are not a production recommendation | ⭐⭐⭐⭐⭐ |
| [Notion MCP](https://developers.notion.com/guides/mcp/overview) | See how a hosted OAuth MCP follows the user’s workspace permissions | ⭐⭐⭐⭐⭐ |
| [GitHub MCP Server](https://github.com/github/github-mcp-server) | Learn OAuth, tool groups, and repository permissions from an official implementation | ⭐⭐⭐⭐⭐ |
| [anthropics/skills](https://github.com/anthropics/skills) | See how Agent Skill folders, instructions, and resources fit together | ⭐⭐⭐⭐⭐ |

> ⚠️ An MCP Server may touch real data. Even with an official source, confirm the signed-in account, scopes, writable tools, and approval screen.

### Index

1. [Notes / Knowledge Bases](#1-notes--knowledge-bases)
2. [Office Documents (Word / Excel / PowerPoint / PDF)](#2-office-documents-word--excel--powerpoint--pdf)
3. [Google Workspace](#3-google-workspace)
4. [Microsoft 365](#4-microsoft-365)
5. [Dev Collaboration (GitHub / Atlassian / Slack…)](#5-dev-collaboration-github--atlassian--slack)
6. [Databases](#6-databases)
7. [Browser Automation / Web Scraping](#7-browser-automation--web-scraping)
8. [Design (Figma / Excalidraw)](#8-design-figma--excalidraw)
9. [Monitoring / Observability](#9-monitoring--observability)
10. [Media / Streaming (YouTube / Spotify)](#10-media--streaming-youtube--spotify)
11. [Chinese-language Ecosystem](#11-chinese-language-ecosystem)
12. [Other Common (Cloudflare / Stripe…)](#12-other-common-cloudflare--stripe)
13. [Research Workflow Skills (Academic / Paper / Literature)](#13-research-workflow-skills-academic--paper--literature)
14. [Multi-LLM Delegation Skills](#14-multi-llm-delegation-skills)
15. [Finance / Trading Agents](#15-finance--trading-agents)
16. [Web Search / Retrieval](#16-web-search--retrieval)
17. [Security / MCP Governance](#17-security--mcp-governance)

---

<a id="1-notes--knowledge-base"></a>
## 1. Notes / Knowledge Bases

<details markdown="1">
<summary>Expand selected entries for category 1</summary>

### [Notion MCP](https://developers.notion.com/guides/mcp/overview) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Delivery | Notion hosted remote MCP; OAuth |
| Rating | ⭐⭐⭐⭐⭐ (**official**) |

**What it does**: Notion’s official hosted MCP can search, read, create, and update content the user can already access.
**Audience**: People who use Notion for notes, projects, or a wiki and want an MCP-capable client.
**Notes**: OAuth follows user permissions; review the approval screen before writing. The older open-source `makenotion/notion-mcp-server` is no longer actively maintained and is not a default for new installs.

### [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ (community maintained) |

**What it does**: read/write your Obsidian vault via the Obsidian REST API community plugin.
**Audience**: heavy Obsidian users wanting Claude Code to organize daily notes, auto-link, search across files.
**Notes**: requires the [Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) plugin in Obsidian.

### [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**What it does**: a Claude Code Skill that uses browser automation to query Gemini Notebook (formerly NotebookLM), with citation-backed answers.
**Audience**: people who manage papers / research notes in Gemini Notebook (formerly NotebookLM) but want to query from Claude Code in one prompt.
**Notes**: requires Google account auth.

### [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**What it does**: unofficial Gemini Notebook (formerly NotebookLM) Python API, CLI, and agentic Skill.
**Audience**: people doing programmatic or batch operations in Gemini Notebook (formerly NotebookLM).
**Notes**: unofficial; may break with Google policy changes — check the issue tracker before relying on it.

### [ergut/mcp-logseq](https://github.com/ergut/mcp-logseq) ⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: read/write Logseq graph via Logseq's Local HTTP API.
**Audience**: Logseq users automating daily journals, cross-page links, backlink queries.
**Notes**: enable Logseq's HTTP API (Settings → Features → HTTP API).

### [skridlevsky/graphthulhu](https://github.com/skridlevsky/graphthulhu) ⭐⭐⭐ (archived / historical example)

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐ (historical learning value; archived, so new projects should not start with it) |

**What it does**: a broad tool set across navigation, search, analysis, writing, journals, flashcards, whiteboards.
**Audience**: people studying early Logseq + Obsidian MCP design; new projects should choose a maintained alternative.
**Notes**: this GitHub project is archived and is useful as historical reference; do not use it as the starting point for a new project.

### [ankimcp/anki-mcp-server](https://github.com/ankimcp/anki-mcp-server) ⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: create / query / batch-edit Anki decks via AnkiConnect.
**Audience**: people using Anki for languages / medicine / law — let the LLM auto-generate cards from study material.
**Notes**: requires Anki Desktop + the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) addon.

---

</details>
## 2. Office Documents (Word / Excel / PowerPoint / PDF)

<details markdown="1">
<summary>Expand selected entries for category 2</summary>

### [anthropics/skills](https://github.com/anthropics/skills) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | No license file (none provided upstream; confirm terms before use) |
| Rating | ⭐⭐⭐⭐⭐ (**official examples**) |

**What it does**: Anthropic's official Agent Skills examples include document workflows for docx, xlsx, pptx, and pdf files.
**Audience**: people who want to study how a standard Skill folder, `SKILL.md`, scripts, and resources work together.
**Notes**: this is a Skills collection, not MCP. Preloading, installation, and support differ across Claude / Agent surfaces; check the repository and current host documentation before use.

### [haris-musa/excel-mcp-server](https://github.com/haris-musa/excel-mcp-server) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (community-maintained Excel MCP) |

**What it does**: Excel file manipulation MCP — read / write / modify cells, formulas, sheets.
**Audience**: people working with Excel reports daily who want LLM-driven data filling and cleanup.
**Notes**: Python-based, depends on openpyxl.

### [GongRzhe/Office-PowerPoint-MCP-Server](https://github.com/GongRzhe/Office-PowerPoint-MCP-Server) ⭐⭐⭐ (⚠️ archived 2025-12; use anthropics/skills pptx)

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐ (⚠️ archived) |

**What it does**: PPT manipulation via python-pptx — create decks, edit slides, insert images, change layouts.
**Audience**: people who want LLMs to auto-generate decks from outlines / Markdown (consultants, lecturers, students).
**Notes**: overlaps with `anthropics/skills`'s pptx skill; use this when the official one isn't enough.

### [1weiho/open-slide](https://github.com/1weiho/open-slide) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ (agent-native slide framework) |

**What it does**: a React slide framework built for coding agents — describe a deck in natural language and let Claude Code / Codex / Cursor write the React; ships two Claude Code Skills (`/create-slide`, `/slide-authoring`).
**Audience**: people who want agents to produce decks as code (git-versionable) — a different route from PowerPoint-MCP's .pptx output.
**Notes**: TypeScript / React / Vite; scaffold with `npx @open-slide/cli init`. It's an agent-native tool (agents author with it), not a Stage 4 agent-building / orchestration framework.

### [SylphxAI/pdf-reader-mcp](https://github.com/SylphxAI/pdf-reader-mcp) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ (high-throughput PDF) |

**What it does**: high-speed PDF parsing MCP, ~5-10× faster than `anthropics/skills`'s pdf skill (per their claim).
**Audience**: people doing batch reads of papers / contracts / reports.
**Notes**: parallel processing; noticeable on large PDFs.

### [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) ⭐⭐⭐

| Field | Value |
|---|---|
| License | NOASSERTION |
| Rating | ⭐⭐⭐ (Office skill add-on) |

**What it does**: extends `anthropics/skills` with Office workflows it doesn't cover (automation, advanced formatting).
**Audience**: people who find the official docx/xlsx/pptx skills too coarse-grained.
**Notes**: complements `anthropics/skills`, not a replacement.

### [xberg-io/xberg](https://github.com/xberg-io/xberg) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐ |

**What it does**: Rust framework for parsing PDF, Office, image, and other common document formats. Provides an MCP server, REST API, and CLI.
**Audience**: cross-format batch parsing engineers who care about throughput.
**Notes**: covers obscure formats like HWP, ODT, etc., not just PDF / Office.

---

</details>
## 3. Google Workspace

<details markdown="1">
<summary>Expand selected entries for category 3</summary>

### [Google Workspace MCP](https://developers.google.com/workspace/guides/configure-mcp-servers) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Delivery | Google hosted remote MCP; OAuth 2.0 |
| Rating | ⭐⭐⭐⭐ (**official**, **Developer Preview**) |

**What it does**: Google provides dedicated remote MCP servers for Gmail, Drive, Docs, Sheets, Slides, Calendar, Chat, and People.
**Audience**: people who want an official entry point for reading Workspace data or creating drafts, updating documents, and scheduling meetings.
**Notes**: this is a **Developer Preview**. OAuth 2.0 and user / organization governance apply; enable only the APIs and scopes the task needs.

### [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (community-maintained broad Workspace MCP) |

**What it does**: Gmail, Calendar, Docs, Sheets, Slides, Drive, Chat, Forms, Tasks, Search — all in one MCP server.
**Audience**: people who need community features beyond the official Preview and are willing to maintain the OAuth setup.
**Notes**: community-maintained; broad coverage also means a broader permission surface. Start with read-only access and the smallest useful scope.

### [xing5/mcp-google-sheets](https://github.com/xing5/mcp-google-sheets) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ (Sheets-only) |

**What it does**: focused Google Sheets / Drive integration — create sheets, edit cells, query formulas.
**Audience**: people using only Google Sheets who don't want the full Workspace MCP.
**Notes**: narrower scope than `google_workspace_mcp`, but simpler setup.

---

</details>
## 4. Microsoft 365

<details markdown="1">
<summary>Expand selected entries for category 4</summary>

### [Softeria/ms-365-mcp-server](https://github.com/Softeria/ms-365-mcp-server) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ (full M365) |

**What it does**: M365 + Office services via Microsoft Graph API — Outlook, Teams, OneDrive, SharePoint.
**Audience**: enterprise M365 users wanting LLM-driven email replies, calendar lookups, OneDrive operations.
**Notes**: requires Azure AD app registration; corporate IT policies may block this.

### [ryaker/outlook-mcp](https://github.com/ryaker/outlook-mcp) ⭐⭐⭐

| Field | Value |
|---|---|
| License | NOASSERTION |
| Rating | ⭐⭐⭐ (Outlook only) |

**What it does**: Outlook mail / calendar via Graph API.
**Audience**: people who only need Outlook, not the rest of M365.
**Notes**: narrower scope than `ms-365-mcp-server`.

### [merill/lokka](https://github.com/merill/lokka) ⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: M365 + Microsoft Graph admin operations — Entra (AD), Intune, etc.
**Audience**: M365 system admins managing tenants / users / policies.
**Notes**: more useful for IT admins than end users.

---

</details>
## 5. Dev Collaboration (GitHub / Atlassian / Slack…)

<details markdown="1">
<summary>Expand selected entries for category 5</summary>

### [github/github-mcp-server](https://github.com/github/github-mcp-server) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (**official**) |

**What it does**: GitHub's official MCP — issues / PRs / repos / Actions / Codespaces.
**Audience**: GitHub users who need to look up repositories, organize issues, or assist with PR review.
**Notes**: prefer OAuth or a least-privilege token. Keep human approval before creating an issue, changing a PR, or triggering a workflow. Track A exercise CLI-9 in A3 uses this entry point.

### [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (community-maintained Atlassian MCP) |

**What it does**: Connects Confluence and Jira through a community MCP server you can self-host.
**Audience**: teams that need self-hosting, custom authentication, or a deployment shape the official remote MCP does not support.
**Notes**: community maintained. Choose this or the official Atlassian remote MCP below after checking company IT policy and permission requirements.

### [Atlassian Rovo MCP](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Delivery | Atlassian hosted remote MCP; OAuth 2.1 |
| Rating | ⭐⭐⭐⭐⭐ (**Atlassian official**) |

**What it does**: Lets an MCP-capable client read and write Jira, Confluence, and Bitbucket Cloud according to user permissions.
**Audience**: teams using Atlassian Cloud.
**Notes**: OAuth 2.1 applies; review approval details before changing issues, pages, or repositories.

### [Slack MCP Server](https://docs.slack.dev/ai/mcp-overview/) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Delivery | Slack official MCP Server |
| Rating | ⭐⭐⭐⭐⭐ (**Slack official**) |

**What it does**: Lets an AI app search Slack channels, send messages, manage canvases, and perform other Slack actions.
**Audience**: teams using Slack with an MCP-capable client.
**Notes**: this is not read-only; confirm organization policy and keep human approval before sending or changing content.

### [Linear MCP](https://linear.app/docs/mcp) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Delivery | Linear hosted remote MCP; Streamable HTTP |
| Rating | ⭐⭐⭐⭐⭐ (**Linear official**) |

**What it does**: Queries or updates Linear issues, projects, and comments.
**Audience**: Linear users who manage sprints or backlogs.
**Notes**: use the official read-only option when needed; writes follow signed-in user permissions.

### [SaseQ/discord-mcp](https://github.com/SaseQ/discord-mcp) ⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: Discord MCP — read/write channel messages, manage servers.
**Audience**: maintainers running OSS / community Discord servers.
**Notes**: requires Discord bot token; watch rate limits.

### [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ |

**What it does**: AI coding skill that turns codebases / SQL schemas / R scripts / shell scripts / docs / papers / images / videos into a queryable knowledge graph. Works across Claude Code, Codex, OpenCode, Cursor, Gemini CLI.
**Audience**: engineers / researchers analyzing large codebases, tracking cross-file references, or asking questions across "app code + DB schema + infra" together.
**Notes**: cross-cutting tool — fits both dev collaboration (understanding existing codebases) and research workflow (turning any artifact into a graph). When stuck on a big codebase, use graphify to extract structure, then feed it back to Claude for reasoning.

### [upstash/context7](https://github.com/upstash/context7) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (coding context) |

**What it does**: Finds documentation snippets by library and version, then puts them into the Agent's current context to reduce the chance of using an old API.
**Audience**: developers who write code across library versions and want to find relevant documentation before editing.
**Notes**: still check the version and original official documentation. It helps find material; it does not guarantee that every result is current or complete.

### [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (code intelligence) |

**What it does**: Indexes a codebase into a queryable knowledge graph, so a coding agent can inspect structure, symbols, and call paths before returning to the actual code to verify them.
**Audience**: people running coding agents on large or unfamiliar repos who want fast orientation and lower token use.
**Notes**: re-index after big edits, since the graph can go stale; treat its answers as a fast first pass and verify load-bearing claims (who-calls-X / is-this-dead) against the actual code.

---

</details>
## 6. Databases

<details markdown="1">
<summary>Expand selected entries for category 6</summary>

### [googleapis/mcp-toolbox](https://github.com/googleapis/mcp-toolbox) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Google official**, multi-DB) |

**What it does**: cross-DB MCP server — MySQL / PostgreSQL / Cloud SQL / Spanner / BigQuery.
**Audience**: engineers running databases on Google Cloud, or anyone needing multi-engine support.
**Notes**: open-source + Google-maintained; solid choice for production use.

### [bytebase/dbhub](https://github.com/bytebase/dbhub) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (community multi-DB) |

**What it does**: zero-dependency, token-efficient multi-DB MCP — Postgres, MySQL, SQL Server, MariaDB, SQLite.
**Audience**: engineers who don't want the Google Cloud SDK and need cross-OSS-DB support.
**Notes**: overlaps with `googleapis/mcp-toolbox` but lighter weight.

### [supabase/mcp](https://github.com/supabase/mcp) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Supabase official-community**) |

**What it does**: connect Supabase (Postgres, Auth, Storage, Edge Functions) to LLMs.
**Audience**: full-stack devs using Supabase as backend.
**Notes**: official community-maintained.

### [timescale/pg-aiguide](https://github.com/timescale/pg-aiguide) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (Postgres coding aid) |

**What it does**: MCP server + Claude plugin to help LLMs write better PostgreSQL code.
**Audience**: Postgres-heavy SQL writers / DBAs.
**Notes**: focused on "LLM writes better SQL", not just query execution.

### [benborla/mcp-server-mysql](https://github.com/benborla/mcp-server-mysql) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ (read-only MySQL) |

**What it does**: read-only MySQL MCP — let the LLM see schemas, run queries.
**Audience**: scenarios where the LLM should analyze production DBs but never modify them.
**Notes**: read-only is a safety feature, not a limitation.

### [mongodb-js/mongodb-mcp-server](https://github.com/mongodb-js/mongodb-mcp-server) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (**MongoDB official**) |

**What it does**: MongoDB and MongoDB Atlas Cluster MCP server.
**Audience**: engineers using MongoDB / Atlas.
**Notes**: `mongodb-js` is MongoDB's official GitHub org.

### [redis/mcp-redis](https://github.com/redis/mcp-redis) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ (**Redis official**) |

**What it does**: official Redis MCP — natural-language operations on Redis and Redis Stack (Vector / Search / JSON).
**Audience**: people using Redis as cache / vector DB / queue.
**Notes**: officially maintained; includes vector search.

### [awslabs/mcp](https://github.com/awslabs/mcp) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (**AWS official**) |

**What it does**: AWS's first-party MCP servers (Lambda / S3 / DynamoDB / CloudWatch / Cost Explorer and more).
**Audience**: teams on AWS who want agents to query / operate their cloud.
**Notes**: officially maintained by AWS; uses your existing AWS login (CLI profiles / IAM roles), no separate token to manage.

---

</details>
## 7. Browser Automation / Web Scraping

<details markdown="1">
<summary>Expand selected entries for category 7</summary>

### [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Microsoft official**) |

**What it does**: Playwright MCP server — let the LLM open browsers, click buttons, fill forms, scrape pages.
**Audience**: anyone doing E2E automation, cross-site integration, scraping behind logins.
**Notes**: Playwright is an official project; evaluate it alongside the browser permissions and login flows your task needs.

### [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Chrome official**) |

**What it does**: expose Chrome DevTools to coding agents — performance, network, console traces all available to the LLM.
**Audience**: developers debugging frontend bugs, doing web performance analysis.
**Notes**: pairs perfectly with Playwright MCP — one drives, one observes.

### [firecrawl/firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (**Firecrawl official**) |

**What it does**: Firecrawl's official MCP — large-scale web scraping + search + structured extraction.
**Audience**: people scraping large amounts of web data for training / RAG / research.
**Notes**: requires Firecrawl API key (has a free tier).

### [browserbase/mcp-server-browserbase](https://github.com/browserbase/mcp-server-browserbase) ⭐⭐⭐⭐ (⚠️ archived)

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (**Browserbase official**, ⚠️ archived) |

**What it does**: Browserbase's official MCP, paired with Stagehand for cloud-based browser automation.
**Audience**: people whose local browser automation is too heavy / who need parallel cloud sessions.
**Notes**: commercial service (free tier exists); complementary to Playwright MCP (local vs cloud).

---

</details>
## 8. Design (Figma / Excalidraw)

<details markdown="1">
<summary>Expand selected entries for category 8</summary>

### [Canva MCP](https://www.canva.dev/docs/mcp/) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Delivery | Canva hosted remote MCP; `https://mcp.canva.com/mcp` |
| Rating | ⭐⭐⭐⭐⭐ (**Canva official**) |

**What it does**: Lets an AI assistant create, edit, search, and export Canva designs, and work with assets, brands, and comments.
**Audience**: people who want to operate Canva while following existing design permissions.
**Notes**: each user authenticates; operations follow asset and design permissions, and some features vary by plan. Review high-impact edits before approving them.

### [GLips/Figma-Context-MCP](https://github.com/GLips/Figma-Context-MCP) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (community-maintained design-to-code MCP) |

**What it does**: feed Figma layout info to coding agents — read design files, expose component structure, let Cursor / Claude Code generate matching React components.
**Audience**: front-end devs going from Figma designs to component code.
**Notes**: requires a Figma access token. Start with a test file and least privilege while checking whether it fits your design-to-code workflow.

### [excalidraw/excalidraw-mcp](https://github.com/excalidraw/excalidraw-mcp) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐⭐ (**Excalidraw official**) |

**What it does**: streamable Excalidraw MCP — let LLMs draw architecture diagrams and flowcharts directly.
**Audience**: anyone writing design docs / system architecture / flowcharts who wants Claude to draw from text.
**Notes**: official Excalidraw; output imports straight into Excalidraw for editing.

### [yctimlin/mcp_excalidraw](https://github.com/yctimlin/mcp_excalidraw) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ (alternative Excalidraw) |

**What it does**: MCP server + Claude Code Skill, real-time canvas sync, create / edit / export.
**Audience**: people who need real-time canvas sync and programmatic operation.
**Notes**: complementary to the official; community-maintained.

### [pbakaus/impeccable](https://github.com/pbakaus/impeccable) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ |

**What it does**: "**The design language that makes your AI harness better at design.**" A vocabulary / pattern set that helps AI agents produce UI / visual output that escapes the generic "AI-generated" feel.
**Audience**: developers using AI to generate UI / mockups / visual designs but getting generic results; front-end + AI workflows.
**Notes**: not an MCP server or Skill bundle — it's a **design language** reference. Feed AI the higher-quality design vocabulary and it produces better output.

---

</details>
## 9. Monitoring / Observability

<details markdown="1">
<summary>Expand selected entries for category 9</summary>

### [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Grafana official**) |

**What it does**: Grafana's official MCP — query dashboards / metrics / alerts from the LLM.
**Audience**: SREs / DevOps using Grafana for metrics.
**Notes**: "why did this dashboard line drop?" — ask, and the LLM pulls metrics for the answer.

### [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐ (**Sentry official**) |

**What it does**: query Sentry error events / issues / traces from LLMs.
**Audience**: engineers using Sentry for production errors.
**Notes**: "show me last week's stack trace for this error" works directly in Claude Code.

### [winor30/mcp-server-datadog](https://github.com/winor30/mcp-server-datadog) ⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐ (community Datadog) |

**What it does**: Datadog API MCP — monitors / logs / metrics.
**Audience**: Datadog users while there's no official Datadog MCP yet.
**Notes**: likely to be replaced once Datadog ships an official MCP.

---

</details>
## 10. Media / Streaming (YouTube / Spotify)

<details markdown="1">
<summary>Expand selected entries for category 10</summary>

### [varunneal/spotify-mcp](https://github.com/varunneal/spotify-mcp) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**What it does**: connect LLMs to Spotify — play tracks, manage playlists, query history.
**Audience**: anyone integrating playback control or text → music workflows with Claude Code.
**Notes**: requires Spotify Premium (API restriction).

### [kimtaeyoon83/mcp-server-youtube-transcript](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ (YouTube transcripts) |

**What it does**: pull YouTube video transcripts into the LLM for summary / translation / RAG.
**Audience**: people using video as study material, batch-summarizing YouTube content.
**Notes**: depends on YouTube auto-captions; non-English transcripts are hit-or-miss.

### [ZubeidHendricks/youtube-mcp-server](https://github.com/ZubeidHendricks/youtube-mcp-server) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ (full YouTube API) |

**What it does**: full YouTube API MCP — beyond transcripts, also video management, Shorts, analytics.
**Audience**: YouTube creators automating channel management.
**Notes**: requires YouTube Data API key + OAuth.

---

</details>
## 11. Chinese-language Ecosystem

<details markdown="1">
<summary>Expand selected entries for category 11</summary>

### [leemysw/feishu-docx](https://github.com/leemysw/feishu-docx) ⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: bidirectional Feishu (Lark) docs / sheet / bitable ↔ Markdown, with OAuth 2.0, CLI, TUI, Claude Skills.
**Audience**: Chinese-language users on Feishu / Lark wanting to bridge Lark content with Claude Code.
**Notes**: community maintained. Lark APIs, OAuth scopes, and supported features can change; check the current documentation and start in a test space.

### [netease-youdao/LobsterAI](https://github.com/netease-youdao/LobsterAI) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**What it does**: NetEase Youdao's product-style Agent demonstrates workflow automation, cross-app coordination, and file processing.
**Audience**: people evaluating a Chinese interface and integrations with mainland Chinese services.
**Notes**: this is a complete Agent product, not a Skill or MCP server. Check the current project documentation for supported integrations, permissions, and deployment options.

### [QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ |

**What it does**: Alibaba's official Qwen agent framework — RAG, tool use, code interpreter, multi-agent, MCP-compatible. Defaults to Qwen models but swappable to other LLMs.
**Audience**: developers using Qwen / Tongyi as primary LLM; teams that want a Chinese-native agent framework (examples + docs are bilingual but Chinese-first).
**Notes**: MCP compatibility and replaceable models are the main teaching points; check current releases, examples, and supported hosts before adopting it.

### [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ |

**What it does**: open-source release of ByteDance Coze — no-code agent builder (workflow / plugin / knowledge / memory), self-hosted or cloud.
**Audience**: teams building agents without writing code; engineers wanting a reference implementation of an enterprise agent platform (RAG, workflow, memory, plugin system).
**Notes**: built on Coze's in-house Eino framework; connects to OpenAI / Claude / Qwen / domestic Chinese LLMs. Powers both the international (coze.com) and mainland (coze.cn) products.

### [coze-dev/coze-loop](https://github.com/coze-dev/coze-loop) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ |

**What it does**: Coze's agent observability + evaluation platform — trace, debug, eval, prompt management. The back half of the agent dev lifecycle.
**Audience**: teams whose agents are running in production and need monitoring; developers wanting to see how "agent eval / observability" can be designed.
**Notes**: peer to LangSmith / Arize Phoenix; OSS release is self-hostable.

### [liaokongVFX/LangChain-Chinese-Getting-Started-Guide](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | unspecified |
| Rating | ⭐⭐⭐⭐ |

**What it does**: Chinese-language LangChain getting-started guide — covers basics, prompts, memory, agents, chains, and applied examples. It is a structured Chinese learning resource.
**Audience**: Chinese-language users who want LangChain but find the English docs heavy; readers who want to understand LangChain's design before committing to the framework.
**Notes**: no formal license (content is openly readable); LangChain itself moves fast — some APIs in the guide may diverge from the latest version.

### [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ |

**What it does**: LangChain-based open-source knowledge-base QA system — local deployment, supports multiple vector stores, end-to-end RAG example.
**Audience**: Chinese teams who want RAG without building it from scratch; scenarios requiring local-only deployment (no cloud LLM).
**Notes**: useful for reading the end-to-end structure of a locally deployed RAG system. Maintenance has slowed; before using it for a new project, check the current branch, dependencies, and issues, and treat it primarily as a reference implementation.

### [usewhale/whale](https://github.com/usewhale/whale) ⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: Terminal AI coding assistant optimized for DeepSeek models — supports MCP server integration, Claude-style Skills, conversation caching, written in Go.
**Audience**: Chinese developers who use DeepSeek as their primary LLM; those who want a terminal tool without the full Claude Code stack.
**Notes**: One of the few open-source tools with DeepSeek-specific optimization; MCP + Skills dual support allows incremental capability expansion.

### [simonlin1212/a-stock-data](https://github.com/simonlin1212/a-stock-data) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ |

**What it does**: China A-share data Skill that wraps mootdx, EastMoney, akshare, iwencai, and other sources as a data entry point an AI coding assistant can call.
**Audience**: Chinese developers using Claude Code / Codex / OpenClaw for investment research or quantitative analysis; those who don't want to build data-fetching logic from scratch.
**Notes**: community implementation. Data-source terms, stability, and fields can change; verify the original data and licenses before investment research. Check the project's current documentation for compatible hosts.

> Looking for WeChat / DingTalk integrations? Today the mainstream is chatbot frameworks (e.g., zhayujie/CowAgent), not pure MCP servers. Will add when proper MCPs emerge.

### [MoonshotAI/Kimi-K2](https://github.com/MoonshotAI/Kimi-K2) ⭐⭐⭐

| Field | Value |
|---|---|
| License | Modified MIT |
| Rating | ⭐⭐⭐ |

**What it does**: Moonshot's Kimi K2 open-weight LLM series — open weights + OpenAI/Anthropic-compatible API, oriented toward agentic / coding / long-horizon tasks; usable as a backend model for an agent stack.
**Audience**: Chinese developers who want to run agent / coding workflows on a domestic open model, or to self-host open weights.
**Notes**: License is Modified MIT (standard MIT + added large-scale-commercial clauses) — read the original LICENSE before commercial use; weights are also available on Hugging Face.

### [zai-org/GLM-4.5](https://github.com/zai-org/GLM-4.5) ⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐ |

**What it does**: Zhipu (Z.ai)'s GLM-4.5 open model — positioned as Agentic, Reasoning, and Coding (ARC) foundation models; open weights + API, usable as a backend for agent / tool use / coding.
**Audience**: Chinese developers evaluating domestic open agentic models, or who need weights under a permissive license (Apache-2.0).
**Notes**: zai-org is Zhipu's open-source org; the same series also has GLM-4 () for context; weights are on Hugging Face.

---

</details>
## 12. Other Common (Cloudflare / Stripe…)

<details markdown="1">
<summary>Expand selected entries for category 12</summary>

### [cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Cloudflare official**) |

**What it does**: Cloudflare's official MCP — Workers, Pages, R2, KV, D1, DNS, Zero Trust.
**Audience**: anyone running edge / serverless on Cloudflare.
**Notes**: officially maintained; compare its permissions and supported operations with the edge workflows you need.

### [stripe/ai](https://github.com/stripe/ai) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ (**Stripe official**) |

**What it does**: Stripe's official AI agent toolkit, includes an MCP server — handle payments, subscriptions, refunds, customers.
**Audience**: developers wiring payment / billing into agent flows.
**Notes**: ⚠️ this is real money. Test thoroughly in sandbox before going to production.

### YIELD INTELLIGENCE MCP (Hosted Remote Server)

| Field | Value |
|---|---|
| Type | hosted MCP server |
| Rating | ⭐⭐⭐ (finance analysis tool; practical example of hosted vs self-hosted MCP architecture) |

**What it does**: Uses a hosted remote MCP to read US Treasury yields and income-asset analysis, while showing the connection shape of hosted versus self-hosted MCP.
**Audience**: learners who want to observe MCP requests and results with test finance questions; it is not an automatic trading entry point.
**Notes**: the [live endpoint](https://api.intuitek.ai/yield/mcp) is provided by the MIT [thebrierfox/intuitek-ace](https://github.com/thebrierfox/intuitek-ace) repository. Data timing, methods, authentication, and pricing can change; check current service documentation and original market data before use. Not investment advice.

### [ComposioHQ/composio](https://github.com/ComposioHQ/composio) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (many tool-integration hub) |

**What it does**: a platform (SDKs + MCP servers) that connects agents to many apps (Slack / GitHub / Gmail / Salesforce / Notion…) and handles the logins for you, so you don't build a separate connector for each one.
**Audience**: teams whose agents need broad API coverage without maintaining dozens of separate MCP servers.
**Notes**: provides MCP servers + Python / TypeScript SDKs; connect to Claude Code via MCP. A "tool aggregator" (compare with n8n / Zapier for automation).

---

### [morluto/jacobian](https://github.com/morluto/jacobian) ⭐⭐⭐ (⚠️ submitted by its author)

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it teaches**: a directly installable math MCP server for practicing agent calls to composable, exact computations across polynomial maps, linear algebra, and graph algorithms.
**Who it's for**: researchers and developers who want to add mathematical computation to MCP workflows or have agents work with structured mathematical problems.
**Notes**: a Python project, but the launcher ships on npm, which is why it starts with `npx`. Provides an MCP server, CLI, and Python library. Start with a local MCP configuration and use the native Python API when needed.
**How to run**:
```bash
npx -y jacobian mcp
```

---

</details>
<a id="13-research-workflow-skills-academic--paper--literature"></a>
## 13. Research Workflow Skills (academic / paper / lit)

Research Skills can organize literature and writing workflows; the researcher remains responsible for citations, source data, and academic integrity.

<details markdown="1">
<summary>Expand selected entries for category 13</summary>

> ⚠️ **Maintainer's own projects**: these are research tools the repo maintainer [@WenyuChiou](https://github.com/WenyuChiou) uses and has published. Inclusion is based on the workflow problem solved, not popularity; evaluate them against your research requirements, data, and host.

### [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (full research workflow) |

**What it does**: Uses a set of research Skills to cover literature triage, research design, project context, manuscript writing, and multi-AI delegation, distributed through a marketplace.
**Audience**: grad students / postdocs wanting a complete "research workflow" skill set in one drop.
**Notes**: marketplace format, aligns with the plugin/marketplace concept taught in Stage 5.4.

### [WenyuChiou/academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills) ⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐ (narrow but deep) |

**What it does**: rigorous academic paper writing / revision / submission skill for Claude Code. Field-agnostic, customizable per-paper via journal_format.md and style_overrides.md.
**Audience**: researchers actively writing / revising papers who want to automate banned-word audit, figure-text coupling, submission checklists.
**Notes**: use it through the complete marketplace, or install it separately by following the current official instructions.

### [WenyuChiou/zotero-skills](https://github.com/WenyuChiou/zotero-skills) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**What it does**: Zotero CLI skill — programmatically search, add, classify, annotate references.
**Audience**: Zotero users wanting Claude Code to organize their library directly.
**Notes**: complementary to [`MuiseDestiny/zotero-gpt`](https://github.com/MuiseDestiny/zotero-gpt) — that one is a Zotero plugin (chat inside Zotero), this one is a CLI / Skill (operate Zotero from Claude Code).

### [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**What it does**: AI-operable research workspace integrating Zotero, Obsidian, and Gemini Notebook (formerly NotebookLM), with several interfaces.
**Audience**: researchers using Zotero, Obsidian, and Gemini Notebook (formerly NotebookLM) together.
**Notes**: complementary to single-tool MCPs (mcp-obsidian, notion-mcp, etc.) — this is a hub that integrates multiple tools.

---

</details>
## 14. Multi-LLM Delegation Skills

Delegation tools need clear files, budgets, acceptance checks, and stop conditions. A second model does not automatically make an answer correct.

<details markdown="1">
<summary>Expand selected entries for category 14</summary>

> ⚠️ **Maintainer's own projects**: these delegation skills come from the maintainer's daily workflow. Inclusion depends on whether each entry can bound responsibility, inputs, outputs, and acceptance—not popularity. Multi-LLM tools change quickly; evaluate them with the production framework in Stage 7.

<!-- not-an-entry -->
### How delegation skills compose

The skills below can work together, but each one needs a clear task boundary and acceptance check:

![Claude + 3 delegate skills — division of labor](../resources/diagrams/multi-llm-delegation-composition.en.png)

Do not turn model names into permanent job titles. First check the current models, tools, and costs; then assign **design / review, implementation, and long-form synthesis** to the suitable executors. Use the same acceptance criteria for the final result.

### [WenyuChiou/codex-delegate](https://github.com/WenyuChiou/codex-delegate) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ |

**What it does**: Claude Code skill that uses Codex CLI as the execution specialist — multi-file refactors, batch edits, boilerplate generation, wrapper-based implementation tasks. Claude writes the plan + reviews; Codex executes.
**Audience**: developers wanting to save tokens / accelerate large-scale mechanical edits; learners who want to verify "multi-agent isn't just a buzzword".
**Use it for**: applying one transform across many files, generating test scaffolds, porting an existing pattern, or writing migration scripts.
**Don't use for**: tasks without a clear responsibility boundary or acceptance criteria, or tasks that still need an independent security review.
**Notes**: treat it as a bounded executor, not a permanent job assigned to one model. Validate the result with the same acceptance criteria.

### [WenyuChiou/gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill) ⭐⭐⭐ (⚠️ archived 2026-07)

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐ (⚠️ archived) |

**What it does**: Historical Claude Code delegation skill that sent long-form, cross-document, or CJK tasks to another CLI executor.
**Audience**: maintainers of older setups and readers studying early multi-LLM delegation patterns.
**Use it for**: history and migration reference only.
**Don't use for**: new work; the repository is archived and is not a current installation starting point.
**Notes**: do not preserve its old fixed model roles. Use a maintained delegation entry that fits the current host and can be checked against explicit acceptance criteria.

### [WenyuChiou/agent-collab-skills](https://github.com/WenyuChiou/agent-collab-skills) ⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐ (experimental — treat as reference) |

**What it does**: Claude Code marketplace for multi-agent collaboration — task splitter, output reconciler, adversarial debate, shared memory, acceptance gate.
**Audience**: people coordinating multiple delegates who want to see one way of packaging multi-agent coordination into a marketplace.
**Notes**: **experimental** — don't treat this as a framework ready for production use. It's the maintainer's own setup made public as a reference. For multi-agent frameworks built for production, see LangGraph / Microsoft Agent Framework / CrewAI in Stage 7.

---

</details>
## 15. Finance / Trading Agents

> ⚠️ **Application-domain section**: agents applied to quantitative trading, hedge-fund simulation, and automated order placement. The two entries here are Apache-2.0 and MIT, but licensing across this category varies widely — verify each repo before reuse. **Caveat**: real-money trading agents carry significant risk; listed here for agent-design study, not as investment advice.

<details markdown="1">
<summary>Expand selected entries for category 15</summary>

### [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) ⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐ |

**What it does**: a multi-agent LLM framework for financial trading decisions, with bull / bear / fundamentals / technicals / risk agents collaborating.
**Audience**: learners studying how multi-agent systems split analytical work; quant researchers experimenting with LLM augmentation of existing pipelines.
**Notes**: Apache-2.0 — modification and commercial use permitted (retain license notice). **Not investment advice — do not run on real funds directly.**

### [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) ⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: a multi-role AI hedge-fund simulation where bull / bear / fundamentals / technicals / risk agents collaborate to produce trade recommendations.
**Audience**: Stage 7 multi-agent learners wanting a complete application example; people interested in the agent × finance crossover.
**Notes**: MIT-licensed; same caveat as above. **Simulation only — not investment advice.**

---

</details>
## 16. Web Search / Retrieval

<details markdown="1">
<summary>Expand selected entries for category 16</summary>

### [exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ (**Exa official**) |

**What it does**: Exa's official MCP — LLM / agent-oriented web search (neural + keyword) that returns clean results to feed straight into prompts.
**Audience**: people doing research / fact-check / online RAG retrieval — semantic search shines for "concept-related" queries, less so for pure keyword lookups.
**Notes**: requires an Exa API key.

### [tavily-ai/tavily-mcp](https://github.com/tavily-ai/tavily-mcp) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | MIT |
| Rating | ⭐⭐⭐⭐ (LLM search MCP) |

**What it does**: wraps the Tavily search API as MCP, giving an Agent search results and sources.
**Audience**: beginners who want an Agent to search the web and then verify the source content separately.
**Notes**: requires a Tavily API key. Plans and quotas can change; check the current official documentation.

---

</details>
## 17. Security / MCP Governance

<details markdown="1">
<summary>Expand selected entries for category 17</summary>

### [trailofbits/skills](https://github.com/trailofbits/skills) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | CC-BY-SA-4.0 |
| Rating | ⭐⭐⭐⭐⭐ (**official Trail of Bits**) |

**What it does**: the official Claude Code plugin marketplace from security firm Trail of Bits, carrying the skills they use themselves for security analysis, testing, and vulnerability research.
**Audience**: people who want an agent to help with code audits, vulnerability analysis, and security testing; also anyone curious how a professional security team encodes its own methodology as skills.
**Notes**: install with `/plugin marketplace add trailofbits/skills`; Codex supports the same marketplace directly. The license is **CC-BY-SA-4.0** (share-alike), so derivative work ships under the same terms; check that before commercial integration. Note this is a **different repo** from [`trailofbits/skills-curated`](https://github.com/trailofbits/skills-curated) in the Stage 5 table: that one is a curation marketplace of community-contributed plugins reviewed by Trail of Bits staff, this one is Trail of Bits' own security skills.

### [stacklok/toolhive](https://github.com/stacklok/toolhive) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ |

**What it does**: runs every MCP server in an isolated container, replaces local credentials with a minimal permission file, and adds audit logs plus configurable identity and access policy. Ships a Kubernetes operator as well.
**Audience**: teams where everyone has installed their own pile of MCP servers and somebody now has to answer "who installed what, and which credentials can it reach".
**Notes**: Go project, available as a desktop app and a CLI. Open-source ToolHive and Stacklok's enterprise product are separate, so check which features sit on which side.

### [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (**NVIDIA official**) |

**What it does**: a sandboxed execution environment for autonomous agents, with declarative policy over files, network and processes. Claude Code and Codex run inside it unmodified; OpenClaw goes through NemoClaw, the next entry below.
**Audience**: people who want an agent to actually execute commands without handing it the whole machine.
**Notes**: Rust project. Needs Docker / Podman or host virtualization for MicroVM-backed sandboxes; Windows goes through WSL 2 and is marked experimental. **⚠️ The project still calls itself alpha**, so read it and try it, but assess before depending on it. The split against `toolhive`: toolhive governs MCP servers, this governs the Agent's own execution boundary.

### [nolabs-ai/nono](https://github.com/nolabs-ai/nono) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ |

**What it does**: confines agents using the operating system's own isolation (Linux Landlock, macOS Seatbelt), with no daemon and no container.
**Audience**: people who want a sandbox without installing a whole container runtime for it.
**Notes**: Rust project, maintained by the team behind Sigstore. Going container-free is the main trade against OpenShell: faster to start, but the isolation is only as strong as what the OS provides.

## What's not here?

If your integration isn't above, check these catalogs first:

- [Official MCP Registry](https://registry.modelcontextprotocol.io/) — find published MCP servers, then check the maintainer, permissions, license, and current status
- [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) — community MCP server catalog with many entries by category
- [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) — another MCP server catalog, complementary
- [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) — official reference implementations for learning how MCP works; not production recommendation material.
- [`travisvn/awesome-claude-skills`](https://github.com/travisvn/awesome-claude-skills) — Claude Skills catalog

### Want to add something?

1. Open an issue with the repo link, why it should be added, and which category it fits.
2. Or open a PR with its source, license or service status, editorial rating, purpose, audience, permissions, and limits.
3. Explain which learning gap it fills; popularity numbers alone do not prove quality or safety.

Read [`resources/style-guide.en.md`](style-guide.en.md) and [`CONTRIBUTING.en.md`](../CONTRIBUTING.en.md) before submitting.

---

## Notes for anyone helping out later

Not an SLA — just "do what you can" guidance:

- Treat vendor documentation or the canonical repo as the source for official status, licensing, permissions, and hosted endpoints.
- CI periodically scans repository redirects, archive status, HTTP errors, and freshness signals. A warning still needs human judgment; do not remove a stable tool only because it has not released recently.
- Define the reader's task and safety boundary before opening a new category, then add verifiable official or high-quality community entries.
- Apply the same learning-value, maintenance, licensing, and permission standards to Chinese-community tools; do not use a star threshold.
- Make wording and formatting clear enough for a five-year-old to follow while preserving exact terms, limits, and sources.
</details>

# MCP / Skills Integration Catalog

> [繁體中文](./mcp-skills-catalog.md) | [简体中文](./mcp-skills-catalog.zh-Hans.md) | **English**

> Connect Claude Code (or any other CLI agent) to the apps you already use, without window-hopping. This page is a curated index of 81+ MCP servers / Claude Skills / integrations grouped by use case (incl. research-workflow + multi-LLM-delegation dedicated sections).

---

## How to use this catalog

- **Looking for a specific tool's MCP**: jump to the relevant section below
- **Want to know what MCP / Skills / Plugins are**: see [RESOURCES.en.md "Three core terms"](../RESOURCES.en.md#three-core-terms-mcp--skills--plugins) first, then [Stage 5 — Claude Code Ecosystem](../stages/05-claude-code-ecosystem.en.md)
- **Want hands-on exercises (install + test)**: see [Stage 5.2 (MCP)](../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol--foundation) and [Stage 5.3 (Skills)](../stages/05-claude-code-ecosystem.en.md#53--skills-claude-codes-behavior-layer--the-most-critical-layer-of-the-claude-code-ecosystem)

### Inclusion direction (not strict rules)

- **Official first**: Anthropic / vendor-published MCP / Skill usually ranks higher
- **Stars are a hint, not a gate**: community repos around 100+ tend to be maintained, but "niche but useful" repos are welcome via PR with a sentence explaining why
- **Metadata when possible**: pull stars / license via `gh api`; refresh whenever
- **Avoid (not forbidden)**: archived, long-stale, unclear-license repos — niche tools can be exceptions

### Index

1. [Notes / Knowledge Base](#1-notes--knowledge-base) (7)
2. [Office Documents (Word / Excel / PowerPoint / PDF)](#2-office-documents-word--excel--powerpoint--pdf) (7)
3. [Google Workspace](#3-google-workspace) (2)
4. [Microsoft 365](#4-microsoft-365) (3)
5. [Dev Collaboration (GitHub / Atlassian / Slack…)](#5-dev-collaboration-github--atlassian--slack) (9)
6. [Databases](#6-databases) (8)
7. [Browser Automation / Web Scraping](#7-browser-automation--web-scraping) (4)
8. [Design (Figma / Excalidraw)](#8-design-figma--excalidraw) (4)
9. [Monitoring / Observability](#9-monitoring--observability) (3)
10. [Media / Streaming (YouTube / Spotify)](#10-media--streaming-youtube--spotify) (3)
11. [Chinese-language Ecosystem](#11-chinese-language-ecosystem) (11)
12. [Other Common (Cloudflare / Stripe…)](#12-other-common-cloudflare--stripe) (5)
13. [Research Workflow Skills](#13-research-workflow-skills-academic--paper--lit) (4)
14. [Multi-LLM Delegation Skills](#14-multi-llm-delegation-skills) (3)
15. [Finance / Trading Agents](#15-finance--trading-agents) (2)
16. [Web Search / Retrieval](#16-web-search--retrieval) (2)
17. [Security / MCP Governance](#17-security--mcp-governance) (4)

---

## 1. Notes / Knowledge Base

### [makenotion/notion-mcp-server](https://github.com/makenotion/notion-mcp-server) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 4.5k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (**official**) |

**What it does**: Notion's official MCP server — query pages, create pages, manipulate databases.
**Audience**: heavy Notion users for note-taking / project management / wikis — let the LLM pull data and write pages directly.
**Notes**: requires Notion integration token; supports both read-only and read-write modes.

### [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 4.1k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (community, most popular) |

**What it does**: read/write your Obsidian vault via the Obsidian REST API community plugin.
**Audience**: heavy Obsidian users wanting Claude Code to organize daily notes, auto-link, search across files.
**Notes**: requires the [Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) plugin in Obsidian.

### [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 7.4k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**What it does**: a Claude Code Skill that uses browser automation to query NotebookLM, with citation-backed answers.
**Audience**: people who manage papers / research notes in NotebookLM but want to query from Claude Code in one prompt.
**Notes**: requires Google account auth.

### [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 18k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**What it does**: unofficial NotebookLM Python API + CLI + agentic skill; broader feature set than the skill above, including capabilities the web UI doesn't expose.
**Audience**: people doing programmatic / batch operations on NotebookLM (auto-create notebooks, bulk-import documents).
**Notes**: unofficial; may break with Google policy changes — check the issue tracker before relying on it.

### [ergut/mcp-logseq](https://github.com/ergut/mcp-logseq) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 312 |
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: read/write Logseq graph via Logseq's Local HTTP API.
**Audience**: Logseq users automating daily journals, cross-page links, backlink queries.
**Notes**: enable Logseq's HTTP API (Settings → Features → HTTP API).

### [skridlevsky/graphthulhu](https://github.com/skridlevsky/graphthulhu) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 171 |
| License | MIT |
| Rating | ⭐⭐⭐ (covers both Logseq + Obsidian) |

**What it does**: 39 tools across navigation, search, analysis, writing, journals, flashcards, whiteboards.
**Audience**: people using both Logseq and Obsidian who don't want two MCP servers.
**Notes**: community project; broad tool surface but each tool is relatively basic.

### [ankimcp/anki-mcp-server](https://github.com/ankimcp/anki-mcp-server) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 430 |
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: create / query / batch-edit Anki decks via AnkiConnect.
**Audience**: people using Anki for languages / medicine / law — let the LLM auto-generate cards from study material.
**Notes**: requires Anki Desktop + the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) addon.

---

## 2. Office Documents (Word / Excel / PowerPoint / PDF)

### [anthropics/skills](https://github.com/anthropics/skills) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 162k+ |
| License | No license file (none provided upstream; confirm terms before use) |
| Rating | ⭐⭐⭐⭐⭐ (**official**, must-install) |

**What it does**: Anthropic's official Agent Skills repo — includes docx / xlsx / pptx / pdf processing skills.
**Audience**: every Claude Code user — `claude skill install` and Claude can read/write Office files directly.
**Notes**: this is a Skills collection, not an MCP; lives in the Stage 5.3 Skills system.

### [haris-musa/excel-mcp-server](https://github.com/haris-musa/excel-mcp-server) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 4.1k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (most popular community Excel MCP) |

**What it does**: Excel file manipulation MCP — read / write / modify cells, formulas, sheets.
**Audience**: people working with Excel reports daily who want LLM-driven data filling and cleanup.
**Notes**: Python-based, depends on openpyxl.

### [GongRzhe/Office-PowerPoint-MCP-Server](https://github.com/GongRzhe/Office-PowerPoint-MCP-Server) ⭐⭐⭐ (⚠️ archived 2025-12; use anthropics/skills pptx)

| Field | Value |
|---|---|
| Stars | ★ 1.8k+ |
| License | MIT |
| Rating | ⭐⭐⭐ (⚠️ archived) |

**What it does**: PPT manipulation via python-pptx — create decks, edit slides, insert images, change layouts.
**Audience**: people who want LLMs to auto-generate decks from outlines / Markdown (consultants, lecturers, students).
**Notes**: overlaps with `anthropics/skills`'s pptx skill; use this when the official one isn't enough.

### [1weiho/open-slide](https://github.com/1weiho/open-slide) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 6.5k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (agent-native slide framework) |

**What it does**: a React slide framework built for coding agents — describe a deck in natural language and let Claude Code / Codex / Cursor write the React; ships two Claude Code Skills (`/create-slide`, `/slide-authoring`).
**Audience**: people who want agents to produce decks as code (git-versionable) — a different route from PowerPoint-MCP's .pptx output.
**Notes**: TypeScript / React / Vite; scaffold with `npx @open-slide/cli init`. It's an agent-native tool (agents author with it), not a Stage 4 agent-building / orchestration framework.

### [SylphxAI/pdf-reader-mcp](https://github.com/SylphxAI/pdf-reader-mcp) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 880 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (high-throughput PDF) |

**What it does**: high-speed PDF parsing MCP, ~5-10× faster than `anthropics/skills`'s pdf skill (per their claim).
**Audience**: people doing batch reads of papers / contracts / reports.
**Notes**: parallel processing; noticeable on large PDFs.

### [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 790 |
| License | NOASSERTION |
| Rating | ⭐⭐⭐ (Office skill add-on) |

**What it does**: extends `anthropics/skills` with Office workflows it doesn't cover (automation, advanced formatting).
**Audience**: people who find the official docx/xlsx/pptx skills too coarse-grained.
**Notes**: complements `anthropics/skills`, not a replacement.

### [kreuzberg-dev/kreuzberg](https://github.com/kreuzberg-dev/kreuzberg) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 8.8k+ |
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐ |

**What it does**: 97+ document format parser framework, Rust core. Provides MCP server + REST API + CLI.
**Audience**: cross-format batch parsing engineers who care about throughput.
**Notes**: covers obscure formats like HWP, ODT, etc., not just PDF / Office.

---

## 3. Google Workspace

### [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 2.9k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (one server, all of Google) |

**What it does**: Gmail, Calendar, Docs, Sheets, Slides, Drive, Chat, Forms, Tasks, Search — all in one MCP server.
**Audience**: heavy Google Workspace users — replying to email, scheduling, writing docs, manipulating sheets, all from one server.
**Notes**: OAuth setup is a bit involved but only needs to be done once; most complete coverage of Google's tools.

### [xing5/mcp-google-sheets](https://github.com/xing5/mcp-google-sheets) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 952 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (Sheets-only) |

**What it does**: focused Google Sheets / Drive integration — create sheets, edit cells, query formulas.
**Audience**: people using only Google Sheets who don't want the full Workspace MCP.
**Notes**: narrower scope than `google_workspace_mcp`, but simpler setup.

---

## 4. Microsoft 365

### [Softeria/ms-365-mcp-server](https://github.com/Softeria/ms-365-mcp-server) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 908 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (full M365) |

**What it does**: M365 + Office services via Microsoft Graph API — Outlook, Teams, OneDrive, SharePoint.
**Audience**: enterprise M365 users wanting LLM-driven email replies, calendar lookups, OneDrive operations.
**Notes**: requires Azure AD app registration; corporate IT policies may block this.

### [ryaker/outlook-mcp](https://github.com/ryaker/outlook-mcp) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 407 |
| License | NOASSERTION |
| Rating | ⭐⭐⭐ (Outlook only) |

**What it does**: Outlook mail / calendar via Graph API.
**Audience**: people who only need Outlook, not the rest of M365.
**Notes**: narrower scope than `ms-365-mcp-server`.

### [merill/lokka](https://github.com/merill/lokka) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 278 |
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: M365 + Microsoft Graph admin operations — Entra (AD), Intune, etc.
**Audience**: M365 system admins managing tenants / users / policies.
**Notes**: more useful for IT admins than end users.

---

## 5. Dev Collaboration (GitHub / Atlassian / Slack…)

### [github/github-mcp-server](https://github.com/github/github-mcp-server) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 31k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (**official**) |

**What it does**: GitHub's official MCP — issues / PRs / repos / Actions / Codespaces.
**Audience**: every GitHub user; once Claude Code is wired up, PR review, issue triage, release notes all work.
**Notes**: **must-install for Track A's A3 Exercise CLI-9**.

### [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 5.6k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (most popular community Atlassian) |

**What it does**: Confluence + Jira in one MCP, more flexible than the official remote.
**Audience**: people using Atlassian who find the official remote server too restrictive.
**Notes**: pick this OR `atlassian/atlassian-mcp-server` (official) depending on your IT policy.

### [atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 927 |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (**official**) |

**What it does**: Atlassian's official Remote MCP, secure connection to Jira / Confluence.
**Audience**: companies with enterprise Atlassian + IT policies requiring official tooling.
**Notes**: remote model with official SLA.

### [korotovsky/slack-mcp-server](https://github.com/korotovsky/slack-mcp-server) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 1.8k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (no admin permissions needed) |

**What it does**: Slack MCP — DMs, group DMs, channel messages, with built-in history fetch logic.
**Audience**: individual users (not Slack admins) who still want LLM-Slack integration.
**Notes**: doesn't need admin tokens; uses user-level OAuth.

### [jerhadf/linear-mcp-server](https://github.com/jerhadf/linear-mcp-server) ⭐⭐⭐ (⚠️ last commit 2025-05, over a year stale)

| Field | Value |
|---|---|
| Stars | ★ 344 |
| License | MIT |
| Rating | ⭐⭐⭐ (⚠️ no update in over a year) |

**What it does**: Linear (issue tracker) MCP — query issues, create issues, change status.
**Audience**: developers managing sprints / backlogs in Linear.
**Notes**: requires Linear API key.

### [SaseQ/discord-mcp](https://github.com/SaseQ/discord-mcp) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 443 |
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: Discord MCP — read/write channel messages, manage servers.
**Audience**: maintainers running OSS / community Discord servers.
**Notes**: requires Discord bot token; watch rate limits.

### [safishamsi/graphify](https://github.com/safishamsi/graphify) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 101k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ |

**What it does**: AI coding skill that turns codebases / SQL schemas / R scripts / shell scripts / docs / papers / images / videos into a queryable knowledge graph. Works across Claude Code, Codex, OpenCode, Cursor, Gemini CLI.
**Audience**: engineers / researchers analyzing large codebases, tracking cross-file references, or asking questions across "app code + DB schema + infra" together.
**Notes**: cross-cutting tool — fits both dev collaboration (understanding existing codebases) and research workflow (turning any artifact into a graph). When stuck on a big codebase, use graphify to extract structure, then feed it back to Claude for reasoning.

### [upstash/context7](https://github.com/upstash/context7) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 60k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (must-have for coding) |

**What it does**: pulls up-to-date library / framework docs into the agent's context so it stops hallucinating outdated APIs — one of the most-installed coding MCPs.
**Audience**: developers who hit "the LLM wrote code against a stale version of this library" — Context7 feeds the agent current docs on demand.
**Notes**: among the highest-starred coding MCPs; reach for it whenever the agent's library knowledge lags the version you're actually on.

### [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 38k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (code intelligence) |

**What it does**: indexes a codebase into a queryable knowledge graph, so a coding agent can ask about structure / symbols / call paths instead of repeatedly grepping and reading files. Single static binary, 158 languages.
**Audience**: people running coding agents on large or unfamiliar repos who want fast orientation and lower token use.
**Notes**: re-index after big edits, since the graph can go stale; treat its answers as a fast first pass and verify load-bearing claims (who-calls-X / is-this-dead) against the actual code.

---

## 6. Databases

### [googleapis/mcp-toolbox](https://github.com/googleapis/mcp-toolbox) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 16k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Google official**, multi-DB) |

**What it does**: cross-DB MCP server — MySQL / PostgreSQL / Cloud SQL / Spanner / BigQuery.
**Audience**: engineers running databases on Google Cloud, or anyone needing multi-engine support.
**Notes**: open-source + Google-maintained; solid choice for production use.

### [bytebase/dbhub](https://github.com/bytebase/dbhub) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 3.2k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (community multi-DB) |

**What it does**: zero-dependency, token-efficient multi-DB MCP — Postgres, MySQL, SQL Server, MariaDB, SQLite.
**Audience**: engineers who don't want the Google Cloud SDK and need cross-OSS-DB support.
**Notes**: overlaps with `googleapis/mcp-toolbox` but lighter weight.

### [supabase-community/supabase-mcp](https://github.com/supabase-community/supabase-mcp) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 2.9k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Supabase official-community**) |

**What it does**: connect Supabase (Postgres, Auth, Storage, Edge Functions) to LLMs.
**Audience**: full-stack devs using Supabase as backend.
**Notes**: official community-maintained.

### [timescale/pg-aiguide](https://github.com/timescale/pg-aiguide) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 1.8k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (Postgres coding aid) |

**What it does**: MCP server + Claude plugin to help LLMs write better PostgreSQL code.
**Audience**: Postgres-heavy SQL writers / DBAs.
**Notes**: focused on "LLM writes better SQL", not just query execution.

### [benborla/mcp-server-mysql](https://github.com/benborla/mcp-server-mysql) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 2k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (read-only MySQL) |

**What it does**: read-only MySQL MCP — let the LLM see schemas, run queries.
**Audience**: scenarios where the LLM should analyze production DBs but never modify them.
**Notes**: read-only is a safety feature, not a limitation.

### [mongodb-js/mongodb-mcp-server](https://github.com/mongodb-js/mongodb-mcp-server) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 1.1k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (**MongoDB official**) |

**What it does**: MongoDB and MongoDB Atlas Cluster MCP server.
**Audience**: engineers using MongoDB / Atlas.
**Notes**: `mongodb-js` is MongoDB's official GitHub org.

### [redis/mcp-redis](https://github.com/redis/mcp-redis) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 555 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (**Redis official**) |

**What it does**: official Redis MCP — natural-language operations on Redis and Redis Stack (Vector / Search / JSON).
**Audience**: people using Redis as cache / vector DB / queue.
**Notes**: officially maintained; includes vector search.

### [awslabs/mcp](https://github.com/awslabs/mcp) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 9.3k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (**AWS official**) |

**What it does**: AWS's first-party MCP servers (Lambda / S3 / DynamoDB / CloudWatch / Cost Explorer and more).
**Audience**: teams on AWS who want agents to query / operate their cloud.
**Notes**: officially maintained by AWS; uses your existing AWS login (CLI profiles / IAM roles), no separate token to manage.

---

## 7. Browser Automation / Web Scraping

### [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 35k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Microsoft official**) |

**What it does**: Playwright MCP server — let the LLM open browsers, click buttons, fill forms, scrape pages.
**Audience**: anyone doing E2E automation, cross-site integration, scraping behind logins.
**Notes**: official Playwright; most robust. **First choice for Claude Code + web automation**.

### [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 47k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Chrome official**) |

**What it does**: expose Chrome DevTools to coding agents — performance, network, console traces all available to the LLM.
**Audience**: developers debugging frontend bugs, doing web performance analysis.
**Notes**: pairs perfectly with Playwright MCP — one drives, one observes.

### [firecrawl/firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 7k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (**Firecrawl official**) |

**What it does**: Firecrawl's official MCP — large-scale web scraping + search + structured extraction.
**Audience**: people scraping large amounts of web data for training / RAG / research.
**Notes**: requires Firecrawl API key (has a free tier).

### [browserbase/mcp-server-browserbase](https://github.com/browserbase/mcp-server-browserbase) ⭐⭐⭐⭐ (⚠️ archived)

| Field | Value |
|---|---|
| Stars | ★ 3.3k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (**Browserbase official**, ⚠️ archived) |

**What it does**: Browserbase's official MCP, paired with Stagehand for cloud-based browser automation.
**Audience**: people whose local browser automation is too heavy / who need parallel cloud sessions.
**Notes**: commercial service (free tier exists); complementary to Playwright MCP (local vs cloud).

---

## 8. Design (Figma / Excalidraw)

### [GLips/Figma-Context-MCP](https://github.com/GLips/Figma-Context-MCP) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 15k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (most popular Figma MCP) |

**What it does**: feed Figma layout info to coding agents — read design files, expose component structure, let Cursor / Claude Code generate matching React components.
**Audience**: front-end devs going from Figma designs to component code.
**Notes**: requires Figma access token; must-install for design-to-code workflows.

### [excalidraw/excalidraw-mcp](https://github.com/excalidraw/excalidraw-mcp) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 5k+ |
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐⭐ (**Excalidraw official**) |

**What it does**: streamable Excalidraw MCP — let LLMs draw architecture diagrams and flowcharts directly.
**Audience**: anyone writing design docs / system architecture / flowcharts who wants Claude to draw from text.
**Notes**: official Excalidraw; output imports straight into Excalidraw for editing.

### [yctimlin/mcp_excalidraw](https://github.com/yctimlin/mcp_excalidraw) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 2.2k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (alternative Excalidraw) |

**What it does**: MCP server + Claude Code Skill, real-time canvas sync, create / edit / export.
**Audience**: people who need real-time canvas sync and programmatic operation.
**Notes**: complementary to the official; community-maintained.

### [pbakaus/impeccable](https://github.com/pbakaus/impeccable) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 57k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ |

**What it does**: "**The design language that makes your AI harness better at design.**" A vocabulary / pattern set that helps AI agents produce UI / visual output that escapes the generic "AI-generated" feel.
**Audience**: developers using AI to generate UI / mockups / visual designs but getting generic results; front-end + AI workflows.
**Notes**: not an MCP server or Skill bundle — it's a **design language** reference. Feed AI the higher-quality design vocabulary and it produces better output.

---

## 9. Monitoring / Observability

### [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 3.3k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Grafana official**) |

**What it does**: Grafana's official MCP — query dashboards / metrics / alerts from the LLM.
**Audience**: SREs / DevOps using Grafana for metrics.
**Notes**: "why did this dashboard line drop?" — ask, and the LLM pulls metrics for the answer.

### [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 782 |
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐ (**Sentry official**) |

**What it does**: query Sentry error events / issues / traces from LLMs.
**Audience**: engineers using Sentry for production errors.
**Notes**: "show me last week's stack trace for this error" works directly in Claude Code.

### [winor30/mcp-server-datadog](https://github.com/winor30/mcp-server-datadog) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 142 |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐ (community Datadog) |

**What it does**: Datadog API MCP — monitors / logs / metrics.
**Audience**: Datadog users while there's no official Datadog MCP yet.
**Notes**: likely to be replaced once Datadog ships an official MCP.

---

## 10. Media / Streaming (YouTube / Spotify)

### [varunneal/spotify-mcp](https://github.com/varunneal/spotify-mcp) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 599 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**What it does**: connect LLMs to Spotify — play tracks, manage playlists, query history.
**Audience**: anyone integrating playback control or text → music workflows with Claude Code.
**Notes**: requires Spotify Premium (API restriction).

### [kimtaeyoon83/mcp-server-youtube-transcript](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 581 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (YouTube transcripts) |

**What it does**: pull YouTube video transcripts into the LLM for summary / translation / RAG.
**Audience**: people using video as study material, batch-summarizing YouTube content.
**Notes**: depends on YouTube auto-captions; non-English transcripts are hit-or-miss.

### [ZubeidHendricks/youtube-mcp-server](https://github.com/ZubeidHendricks/youtube-mcp-server) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 557 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (full YouTube API) |

**What it does**: full YouTube API MCP — beyond transcripts, also video management, Shorts, analytics.
**Audience**: YouTube creators automating channel management.
**Notes**: requires YouTube Data API key + OAuth.

---

## 11. Chinese-language Ecosystem

### [leemysw/feishu-docx](https://github.com/leemysw/feishu-docx) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 243 |
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: bidirectional Feishu (Lark) docs / sheet / bitable ↔ Markdown, with OAuth 2.0, CLI, TUI, Claude Skills.
**Audience**: Chinese-language users on Feishu / Lark wanting to bridge Lark content with Claude Code.
**Notes**: currently one of the few MCP / Skill options in the Chinese ecosystem; WeChat / DingTalk don't have standalone MCPs yet (they live inside chatbot frameworks).

### [netease-youdao/LobsterAI](https://github.com/netease-youdao/LobsterAI) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 5.6k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**What it does**: NetEase Youdao's "24/7 all-scenario AI agent" — workflow automation, cross-app coordination, file processing. Chinese-native.
**Audience**: Chinese-language users wanting an alternative to Claude Code / OpenAI Operator-class all-in-one agents; scenarios needing tight integration with mainland Chinese services (NetEase, DingTalk, etc.).
**Notes**: product-style agent (not a Skill / MCP); substitutes for Claude Code / Codex rather than complementing them.

### [QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 16k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ |

**What it does**: Alibaba's official Qwen agent framework — RAG, tool use, code interpreter, multi-agent, MCP-compatible. Defaults to Qwen models but swappable to other LLMs.
**Audience**: developers using Qwen / Tongyi as primary LLM; teams that want a Chinese-native agent framework (examples + docs are bilingual but Chinese-first).
**Notes**: MCP compatibility is the highlight — plugs into Claude Code-style hosts directly; active maintenance (last commit 2026-03).

### [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 21k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ |

**What it does**: open-source release of ByteDance Coze — no-code agent builder (workflow / plugin / knowledge / memory), self-hosted or cloud.
**Audience**: teams building agents without writing code; engineers wanting a reference implementation of an enterprise agent platform (RAG, workflow, memory, plugin system).
**Notes**: built on Coze's in-house Eino framework; connects to OpenAI / Claude / Qwen / domestic Chinese LLMs. Powers both the international (coze.com) and mainland (coze.cn) products.

### [coze-dev/coze-loop](https://github.com/coze-dev/coze-loop) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 5.6k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ |

**What it does**: Coze's agent observability + evaluation platform — trace, debug, eval, prompt management. The back half of the agent dev lifecycle.
**Audience**: teams whose agents are running in production and need monitoring; developers wanting to see how "agent eval / observability" can be designed.
**Notes**: peer to LangSmith / Arize Phoenix; OSS release is self-hostable.

### [liaokongVFX/LangChain-Chinese-Getting-Started-Guide](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 8.9k+ |
| License | unspecified |
| Rating | ⭐⭐⭐⭐ |

**What it does**: Chinese-language LangChain getting-started guide — covers basics, prompts, memory, agents, chains, and applied examples. The earliest and most complete LangChain Chinese learning resource.
**Audience**: Chinese-language users who want LangChain but find the English docs heavy; readers who want to understand LangChain's design before committing to the framework.
**Notes**: no formal license (content is openly readable); LangChain itself moves fast — some APIs in the guide may diverge from the latest version.

### [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 37k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ |

**What it does**: LangChain-based open-source knowledge-base QA system — local deployment, supports multiple vector stores, end-to-end RAG example.
**Audience**: Chinese teams who want RAG without building it from scratch; scenarios requiring local-only deployment (no cloud LLM).
**Notes**: ★ 37k makes it the most popular RAG implementation in the Chinese ecosystem; maintenance has slowed (last commit 2025-11). For new projects, fork and evaluate as a reference, not a turnkey base.

### [usewhale/whale](https://github.com/usewhale/whale) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 967 |
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: Terminal AI coding assistant optimized for DeepSeek models — supports MCP server integration, Claude-style Skills, conversation caching, written in Go.
**Audience**: Chinese developers who use DeepSeek as their primary LLM; those who want a terminal tool without the full Claude Code stack.
**Notes**: One of the few open-source tools with DeepSeek-specific optimization; MCP + Skills dual support allows incremental capability expansion.

### [simonlin1212/a-stock-data](https://github.com/simonlin1212/a-stock-data) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 9.2k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ |

**What it does**: China A-share market data toolkit — a single SKILL.md file wrapping 8 data sources (mootdx, EastMoney, akshare, iwencai, etc.) with 21 endpoints, directly usable by AI coding assistants.
**Audience**: Chinese developers using Claude Code / Codex / OpenClaw for investment research or quantitative analysis; those who don't want to build data-fetching logic from scratch.
**Notes**: Installable with a single `curl` + `pip install`; highest-starred community Skill for Chinese A-share data. Compatible with Claude Code, Codex, and OpenClaw.

> Looking for WeChat / DingTalk integrations? Today the mainstream is chatbot frameworks (e.g., zhayujie/CowAgent), not pure MCP servers. Will add when proper MCPs emerge.

### [MoonshotAI/Kimi-K2](https://github.com/MoonshotAI/Kimi-K2) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 10.7k+ |
| License | Modified MIT |
| Rating | ⭐⭐⭐ |

**What it does**: Moonshot's Kimi K2 open-weight LLM series — open weights + OpenAI/Anthropic-compatible API, oriented toward agentic / coding / long-horizon tasks; usable as a backend model for an agent stack.
**Audience**: Chinese developers who want to run agent / coding workflows on a domestic open model, or to self-host open weights.
**Notes**: License is Modified MIT (standard MIT + added large-scale-commercial clauses) — read the original LICENSE before commercial use; weights are also available on Hugging Face.

### [zai-org/GLM-4.5](https://github.com/zai-org/GLM-4.5) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 4.3k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐ |

**What it does**: Zhipu (Z.ai)'s GLM-4.5 open model — positioned as Agentic, Reasoning, and Coding (ARC) foundation models; open weights + API, usable as a backend for agent / tool use / coding.
**Audience**: Chinese developers evaluating domestic open agentic models, or who need weights under a permissive license (Apache-2.0).
**Notes**: zai-org is Zhipu's open-source org; the same series also has GLM-4 (★ 7k+) for context; weights are on Hugging Face.

---

## 12. Other Common (Cloudflare / Stripe…)

### [cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 4k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Cloudflare official**) |

**What it does**: Cloudflare's official MCP — Workers, Pages, R2, KV, D1, DNS, Zero Trust.
**Audience**: anyone running edge / serverless on Cloudflare.
**Notes**: officially maintained; the best edge platform MCP.

### [stripe/ai](https://github.com/stripe/ai) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 1.7k+ |
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

**What it does**: YIELD INTELLIGENCE hosted remote MCP server — live US Treasury yield rates, dividend ETF / REIT / preferred stock analysis, and passive income portfolio optimization. Two tools: `analyze_yield_opportunities` (scans passive income options) + `optimize_income_portfolio` (builds a portfolio toward a target monthly income). Listed in the official MCP Registry (`io.github.thebrierfox/intuitek-ace`, since 2026-05-10).
**Audience**: people doing personal finance analysis in Claude Code / Claude Desktop who want AI to surface passive income opportunities. Good hands-on example of a hosted remote MCP server — plug the URL in, zero install, useful for Stage 5 learners exploring the hosted vs self-hosted difference.
**Notes**: Live endpoint `https://api.intuitek.ai/yield/mcp` (no auth, no API key required). x402 micropayment $1 USDC/call on Base (agent-to-agent scenarios); free for regular users. Analysis-only, no trading. GitHub: [thebrierfox/intuitek-ace](https://github.com/thebrierfox/intuitek-ace) (MIT License).

### [ComposioHQ/composio](https://github.com/ComposioHQ/composio) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 28.8k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (1000+ tool-integration hub) |

**What it does**: a platform (SDKs + MCP servers) that connects agents to 1000+ apps (Slack / GitHub / Gmail / Salesforce / Notion…) and handles the logins for you, so you don't build a separate connector for each one.
**Audience**: teams whose agents need broad API coverage without maintaining dozens of separate MCP servers.
**Notes**: provides MCP servers + Python / TypeScript SDKs; connect to Claude Code via MCP. A "tool aggregator" (compare with n8n / Zapier for automation).

---

### [morluto/jacobian](https://github.com/morluto/jacobian) ⭐⭐⭐ (⚠️ submitted by its author)

| Field | Value |
|---|---|
| Stars | ★ 58 |
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

## 13. Research Workflow Skills (academic / paper / lit)

> ⚠️ **Maintainer's own projects**: the following are skills the repo maintainer [@WenyuChiou](https://github.com/WenyuChiou) (Lehigh CEE PhD candidate) uses daily for research and open-sourced for other researchers. **Star counts are lower than general-purpose tools** because these are niche / research-specific. The ★ 100+ inclusion floor is relaxed in this section — the only criterion here is "actually useful in the maintainer's research workflow". Evaluate fit yourself.

### [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 222 |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (full research workflow) |

**What it does**: 14 Claude Code skills covering common research tasks — literature triage, research design, project context, manuscript writing, multi-AI delegation. Packaged as a 5-plugin marketplace, install with one command.
**Audience**: grad students / postdocs wanting a complete "research workflow" skill set in one drop.
**Notes**: marketplace format, aligns with the plugin/marketplace concept taught in Stage 5.4.

### [WenyuChiou/academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 17 |
| License | MIT |
| Rating | ⭐⭐⭐ (narrow but deep) |

**What it does**: rigorous academic paper writing / revision / submission skill for Claude Code. Field-agnostic, customizable per-paper via journal_format.md and style_overrides.md.
**Audience**: researchers actively writing / revising papers who want to automate banned-word audit, figure-text coupling, submission checklists.
**Notes**: one of the 5 plugins inside ai-research-skills; can also be installed standalone.

### [WenyuChiou/zotero-skills](https://github.com/WenyuChiou/zotero-skills) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 50 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**What it does**: Zotero CLI skill — programmatically search, add, classify, annotate references.
**Audience**: Zotero users wanting Claude Code to organize their library directly.
**Notes**: complementary to [`MuiseDestiny/zotero-gpt`](https://github.com/MuiseDestiny/zotero-gpt) — that one is a Zotero plugin (chat inside Zotero), this one is a CLI / Skill (operate Zotero from Claude Code).

### [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 52 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**What it does**: AI-operable research workspace bridging Zotero + Obsidian + NotebookLM, with CLI / MCP / REST / dashboard interfaces.
**Audience**: researchers using Zotero / Obsidian / NotebookLM together, wanting to bind them into one workspace for LLMs to operate.
**Notes**: complementary to single-tool MCPs (mcp-obsidian, notion-mcp, etc.) — this is a hub that integrates multiple tools.

---

## 14. Multi-LLM Delegation Skills

> ⚠️ **Maintainer's own projects** (same as 13): delegation skills the maintainer extracted from daily workflow. Star floor is relaxed; criterion is "the Claude-planner + Codex/Gemini-executor combo runs reliably". Multi-LLM space evolves quickly — evaluate alongside the multi-agent frameworks listed in Stage 7 before adopting.

<!-- not-an-entry -->
### How the three skills compose

The 3 skills below are **designed to be used together**, not as standalone tools:

![Claude + 3 delegate skills — division of labor](../resources/diagrams/multi-llm-delegation-composition.en.png)

Claude is bad at token-heavy mechanical work (cost, context blowout); Codex is bad at conversational coordination; Gemini's 1M context is great but mid-tier reasoning. **Division of labor: Claude handles design / review, Codex handles implementation, Gemini handles long-form drafting / synthesis.**

### [WenyuChiou/codex-delegate](https://github.com/WenyuChiou/codex-delegate) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 62 |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ |

**What it does**: Claude Code skill that uses Codex CLI as the execution specialist — multi-file refactors, batch edits, boilerplate generation, wrapper-based implementation tasks. Claude writes the plan + reviews; Codex executes.
**Audience**: developers wanting to save tokens / accelerate large-scale mechanical edits; learners who want to verify "multi-agent isn't just a buzzword".
**Use it for**: refactoring 30+ files, generating test scaffolds, porting the same pattern across N files, writing migration scripts.
**Don't use for**: architecture decisions, bug diagnosis, security review, tasks needing conversation memory — Claude does these better directly.
**Notes**: pairs with `gemini-delegate-skill`. Practical implementation of the Stage 7 multi-agent concept.

### [WenyuChiou/gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill) ⭐⭐⭐ (⚠️ archived 2026-07)

| Field | Value |
|---|---|
| Stars | ★ 37 |
| License | MIT |
| Rating | ⭐⭐⭐ (⚠️ archived) |

**What it does**: Claude Code skill that uses Gemini CLI as the long-form / large-context / CJK executor — 1M-token context window, Chinese long-form drafting, second-opinion review. Claude provides the outline and critique; Gemini writes the long form.
**Audience**: researchers writing papers, knowledge workers writing Chinese reports / Threads posts, people who want a second LLM's perspective for cross-checking.
**Use it for**: long-form drafts (>3000 words), cross-document synthesis (stuffing many long docs into the 1M-token context), Chinese / CJK content, LLM-vs-LLM comparison views.
**Don't use for**: short queries, code generation (use codex), production-critical decisions (final human review).
**Notes**: pairs with `codex-delegate` for the "Codex writes code, Gemini writes prose" split.

### [WenyuChiou/agent-collab-skills](https://github.com/WenyuChiou/agent-collab-skills) ⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 22 |
| License | MIT |
| Rating | ⭐⭐ (experimental — treat as reference) |

**What it does**: Claude Code marketplace for multi-agent collaboration — task splitter, output reconciler, adversarial debate, shared memory, acceptance gate. Composes with codex-delegate / gemini-delegate.
**Audience**: people running 2+ delegate agents per round who want to see one way of packaging multi-agent coordination into a marketplace.
**Notes**: **experimental** — don't treat this as a framework ready for production use. It's the maintainer's own setup made public as a reference. For multi-agent frameworks built for production, see LangGraph / AutoGen / CrewAI in Stage 7.

---

## 15. Finance / Trading Agents

> ⚠️ **Application-domain section**: agents applied to quantitative trading, hedge-fund simulation, and automated order placement. The two entries here are Apache-2.0 and MIT, but licensing across this category varies widely — verify each repo before reuse. **Caveat**: real-money trading agents carry significant risk; listed here for agent-design study, not as investment advice.

### [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 97k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐ |

**What it does**: a multi-agent LLM framework for financial trading decisions, with bull / bear / fundamentals / technicals / risk agents collaborating.
**Audience**: learners studying how multi-agent systems split analytical work; quant researchers experimenting with LLM augmentation of existing pipelines.
**Notes**: Apache-2.0 — modification and commercial use permitted (retain license notice). **Not investment advice — do not run on real funds directly.**

### [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) ⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 62k+ |
| License | MIT |
| Rating | ⭐⭐⭐ |

**What it does**: a multi-role AI hedge-fund simulation where bull / bear / fundamentals / technicals / risk agents collaborate to produce trade recommendations.
**Audience**: Stage 7 multi-agent learners wanting a complete application example; people interested in the agent × finance crossover.
**Notes**: MIT-licensed; same caveat as above. **Simulation only — not investment advice.**

---

## 16. Web Search / Retrieval

### [exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 4.8k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (**Exa official**) |

**What it does**: Exa's official MCP — LLM / agent-oriented web search (neural + keyword) that returns clean results to feed straight into prompts.
**Audience**: people doing research / fact-check / online RAG retrieval — semantic search shines for "concept-related" queries, less so for pure keyword lookups.
**Notes**: requires an Exa API key.

### [tavily-ai/tavily-mcp](https://github.com/tavily-ai/tavily-mcp) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 2.3k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (beginner-friendly web search) |

**What it does**: Tavily's search API as an MCP — web search built for LLMs / RAG, returning an answer plus its sources.
**Audience**: a beginner who just wants the agent to search the web — good first pick thanks to an easy free tier.
**Notes**: free tier available; returns both a synthesized answer and the underlying sources.

---

## 17. Security / MCP Governance

### [trailofbits/skills](https://github.com/trailofbits/skills) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 6.6k+ |
| License | CC-BY-SA-4.0 |
| Rating | ⭐⭐⭐⭐⭐ (**official Trail of Bits**) |

**What it does**: the official Claude Code plugin marketplace from security firm Trail of Bits, carrying the skills they use themselves for security analysis, testing, and vulnerability research.
**Audience**: people who want an agent to help with code audits, vulnerability analysis, and security testing; also anyone curious how a professional security team encodes its own methodology as skills.
**Notes**: install with `/plugin marketplace add trailofbits/skills`; Codex supports the same marketplace directly. The license is **CC-BY-SA-4.0** (share-alike), so derivative work ships under the same terms; check that before commercial integration. Note this is a **different repo** from [`trailofbits/skills-curated`](https://github.com/trailofbits/skills-curated) in the Stage 5 table: that one is a curation marketplace of community-contributed plugins reviewed by Trail of Bits staff, this one is Trail of Bits' own security skills.

### [stacklok/toolhive](https://github.com/stacklok/toolhive) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 2k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ |

**What it does**: runs every MCP server in an isolated container, replaces local credentials with a minimal permission file, and adds audit logs plus configurable identity and access policy. Ships a Kubernetes operator as well.
**Audience**: teams where everyone has installed their own pile of MCP servers and somebody now has to answer "who installed what, and which credentials can it reach".
**Notes**: Go project, available as a desktop app and a CLI. Open-source ToolHive and Stacklok's enterprise product are separate, so check which features sit on which side.

### [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 8.3k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (**NVIDIA official**) |

**What it does**: a sandboxed execution environment for autonomous agents, with declarative policy over files, network and processes. Claude Code and Codex run inside it unmodified; OpenClaw goes through NemoClaw, the next entry below.
**Audience**: people who want an agent to actually execute commands without handing it the whole machine.
**Notes**: Rust project. Needs Docker / Podman or host virtualization for MicroVM-backed sandboxes; Windows goes through WSL 2 and is marked experimental. **⚠️ The project still calls itself alpha** (latest release is still `v0.0.x`), so read it and try it, but assess before depending on it. The split against `toolhive`: toolhive governs MCP servers, this governs the agent's own execution boundary.

### [nolabs-ai/nono](https://github.com/nolabs-ai/nono) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 3.7k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ |

**What it does**: confines agents using the operating system's own isolation (Linux Landlock, macOS Seatbelt), with no daemon and no container.
**Audience**: people who want a sandbox without installing a whole container runtime for it.
**Notes**: Rust project, maintained by the team behind Sigstore. Going container-free is the main trade against OpenShell: faster to start, but the isolation is only as strong as what the OS provides.

## What's not here?

If your integration isn't above, check these catalogs first:

- [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) — most complete community MCP server catalog, 150+ entries by category
- [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) — another MCP server catalog, complementary
- [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) — official reference servers (7 today: everything, fetch, filesystem, git, memory, sequentialthinking, time; github and sqlite have moved to `servers-archived`)
- [`travisvn/awesome-claude-skills`](https://github.com/travisvn/awesome-claude-skills) — Claude Skills catalog

### Want to add something?

1. Open an issue with the repo link, why it should be added, and which category it fits.
2. Or PR directly: add an entry under the relevant category in this format (Stars / License / Rating + What it does / Audience / Notes).
3. **Stars < 100 + non-official** typically gets rejected unless you can argue a strong niche use case.

Read [`resources/style-guide.en.md`](style-guide.en.md) and [`CONTRIBUTING.en.md`](../CONTRIBUTING.en.md) before submitting.

---

## Notes for anyone helping out later

Not an SLA — just "do what you can" guidance:

- Pull stars / license via `gh api repos/<owner>/<repo>`. **Refresh whenever you have time** — no fixed cadence.
- Spot a broken link / archived repo? Just remove it.
- New category (AR/VR, IoT, etc.) — open it once you have 1-2 entries worth listing.
- "Chinese-language ecosystem" stays loose; Chinese-community repos accumulate stars more slowly.
- Inconsistent wording or formatting between entries — don't sweat it. Readability of the PR comes first.

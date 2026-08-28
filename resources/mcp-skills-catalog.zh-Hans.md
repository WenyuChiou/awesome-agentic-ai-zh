# MCP / Skills 集成目录

> [繁體中文](./mcp-skills-catalog.md) | **简体中文** | [English](./mcp-skills-catalog.en.md)

> 把 Claude Code（或其他 CLI agent）接到你已经正在用的工具，不用反复切换视窗。本页是 81+ 个分类整理过的 MCP server / Claude Skill / 集成范例（含研究工作流 + multi-LLM delegation 两个专属区）。

---

## 怎么用这份目录

- **想找特定工具的 MCP**：直接看下面分类目录
- **想看 MCP / Skills / Plugins 是什么**：先看 [RESOURCES.zh-Hans.md 三个核心用语](../RESOURCES.zh-Hans.md#三个核心用语mcp--skills--plugins)，再看 [Stage 5 — Claude Code 生态系](../stages/05-claude-code-ecosystem.zh-Hans.md)
- **想看 动手练习 怎么装、怎么测**：看 [Stage 5.2 (MCP)](../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础) 跟 [Stage 5.3 (Skills)](../stages/05-claude-code-ecosystem.zh-Hans.md#53--skillsclaude-code-的行为层-claude-code-生态最关键的一层)

### 收录方向（不是死规则）

- **官方优先**：Anthropic、厂商自己出的 MCP / Skill 通常排前面
- **stars 看一下就好**：社群 repo 大致 100+ 比较有人在维护，但“小众但好用”也欢迎送 PR 解释为什么要收
- **尽量有 metadata**：stars / license 用 `gh api` 抓、有空就更新一轮
- **避免（不是禁止）**：archived、长期没 commit、license 不明的 repo——niche 工具可以例外

### 目录

1. [笔记 / 知识库](#1-笔记--知识库)（7）
2. [办公文件（Word / Excel / PowerPoint / PDF）](#2-办公文件word--excel--powerpoint--pdf)（7）
3. [Google Workspace](#3-google-workspace)（2）
4. [Microsoft 365](#4-microsoft-365)（3）
5. [开发协作（GitHub / Atlassian / Slack…）](#5-开发协作github--atlassian--slack)（9）
6. [数据库](#6-数据库)（8）
7. [浏览器自动化 / 网页抓取](#7-浏览器自动化--网页抓取)（4）
8. [设计（Figma / Excalidraw）](#8-设计figma--excalidraw)（4）
9. [监控 / Observability](#9-监控--observability)（3）
10. [媒体 / 串流（YouTube / Spotify）](#10-媒体--串流youtube--spotify)（3）
11. [中文圈专属](#11-中文圈专属)（11）
12. [其他常用（Cloudflare / Stripe…）](#12-其他常用cloudflare--stripe)（5）
13. [研究工作流 Skills（学术 / paper / 文献）](#13-研究工作流-skills学术--paper--文献)（4）
14. [Multi-LLM Delegation Skills](#14-multi-llm-delegation-skills)（3）
15. [金融 / 交易 Agents](#15-金融--交易-agents)（2）
16. [网页搜索 / 检索（Web Search / Retrieval）](#16-网页搜索--检索web-search--retrieval)（2）
17. [安全 / MCP 安全治理](#17-安全--mcp-安全治理)（4）

---

## 1. 笔记 / 知识库

### [makenotion/notion-mcp-server](https://github.com/makenotion/notion-mcp-server) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 4.5k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐（**官方**） |

**教什么**：Notion 官方 MCP server，可查询 page、创建 page、操作 database。
**适合谁**：日常用 Notion 写笔记 / 管项目 / 跑 wiki 的人——叫 LLM 直接捞数据、写 page。
**备注**：需要 Notion integration token；有 read-only 跟 read-write 两种模式可选。

### [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 4.1k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（社群、最热门） |

**教什么**：透过 Obsidian REST API community plugin 让 LLM 读写你的 Obsidian vault。
**适合谁**：Obsidian 重度用户，想用 Claude Code 整理 daily note、自动 link、跨文件搜索。
**备注**：要先在 Obsidian 装 [Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) plugin。

### [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 7.4k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：Claude Code Skill，用浏览器自动化操作 NotebookLM、查询上传文件，回复带 citation。
**适合谁**：用 NotebookLM 管 paper 跟研究笔记，但想在 Claude Code 一条 prompt 直接查的人。
**备注**：需要 Google 账号登录授权。

### [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 18k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：非官方 NotebookLM Python API + CLI + agentic skill；功能比上面 skill 多，包含一些 web UI 没开放的能力。
**适合谁**：要程序化批量操作 NotebookLM 的人（例如自动建 notebook、批量导入文件）。
**备注**：非官方、Google 政策变动可能会坏；用前看一下 issue tracker。

### [ergut/mcp-logseq](https://github.com/ergut/mcp-logseq) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 312 |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：透过 Logseq Local HTTP API 让 LLM 读写 Logseq graph。
**适合谁**：Logseq 用户要自动化 daily journal、跨页 link、查询 backlinks。
**备注**：需要 Logseq 开启 HTTP API（Settings → Features → HTTP API）。

### [skridlevsky/graphthulhu](https://github.com/skridlevsky/graphthulhu) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 171 |
| License | MIT |
| 推荐度 | ⭐⭐⭐（同时支持 Logseq + Obsidian） |

**教什么**：39 个 tool，覆盖 navigation、search、analysis、writing、journals、flashcards、whiteboards。
**适合谁**：同时用 Logseq 跟 Obsidian、不想装两套 MCP server 的人。
**备注**：community project，工具数多但每个工具相对基本。

### [ankimcp/anki-mcp-server](https://github.com/ankimcp/anki-mcp-server) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 430 |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：透过 AnkiConnect 让 LLM 建卡、查卡、批改 deck。
**适合谁**：用 Anki 学语言 / 医学 / 法律的人——叫 LLM 从教材自动产卡。
**备注**：需要 Anki 桌面版装 [AnkiConnect](https://ankiweb.net/shared/info/2055492159) addon。

---

## 2. 办公文件（Word / Excel / PowerPoint / PDF）

### [anthropics/skills](https://github.com/anthropics/skills) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 162k+ |
| License | 无 license 文件（上游未提供；使用前请先确认授权） |
| 推荐度 | ⭐⭐⭐⭐⭐（**官方**，必装） |

**教什么**：Anthropic 官方 Agent Skills repo，含 docx / xlsx / pptx / pdf 处理 skill。
**适合谁**：所有 Claude Code 用户——直接 `claude skill install` 就能让 Claude 读写 Office 档。
**备注**：是 Skills 集合不是 MCP；走 Stage 5.3 Skill 体系。

### [haris-musa/excel-mcp-server](https://github.com/haris-musa/excel-mcp-server) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 4.1k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐（社群最热门 Excel MCP） |

**教什么**：Excel 档操作 MCP server——读 / 写 / 改 cell、formula、sheet。
**适合谁**：日常处理 Excel 报表、要 LLM 自动填表 / 整理数据的人。
**备注**：Python 写的，依赖 openpyxl。

### [GongRzhe/Office-PowerPoint-MCP-Server](https://github.com/GongRzhe/Office-PowerPoint-MCP-Server) ⭐⭐⭐（⚠️ 已封存 2025-12、可改用 anthropics/skills pptx）

| 栏位 | 内容 |
|---|---|
| Stars | ★ 1.8k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐（⚠️ 已封存） |

**教什么**：用 python-pptx 操作 PPT——建简报、改 slide、插图、改 layout。
**适合谁**：要 LLM 从大纲 / Markdown 自动生 PPT 的人（顾问、讲师、学生）。
**备注**：跟 anthropics/skills 的 pptx skill 重叠；那边不够用再来这边。

### [1weiho/open-slide](https://github.com/1weiho/open-slide) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 6.5k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（agent-native 简报框架） |

**教什么**：为 coding agent 打造的 React 简报框架——用自然语言描述简报、让 Claude Code / Codex / Cursor 写出 React slides；内附 `/create-slide`、`/slide-authoring` 两个 Claude Code Skill。
**适合谁**：想让 agent 直接产出“代码即简报、可进 git 版控”的人，跟 PowerPoint-MCP 走 .pptx 不同路。
**备注**：TypeScript / React / Vite，`npx @open-slide/cli init` 起手。它是 agent-native 工具（agent 来写），不是 Stage 4 那种构建 agent 的编排框架。

### [SylphxAI/pdf-reader-mcp](https://github.com/SylphxAI/pdf-reader-mcp) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 880 |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（PDF 高效解析） |

**教什么**：高速 PDF 解析 MCP，比 anthropics/skills 的 pdf skill 快 5-10×（号称）。
**适合谁**：要批量读 paper / contract / report 的人。
**备注**：parallel processing；大 PDF 处理速度有感差别。

### [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 790 |
| License | NOASSERTION |
| 推荐度 | ⭐⭐⭐（补强版 Office skill） |

**教什么**：补强 anthropics/skills 没覆盖到的 Office workflow（automation、进阶格式）。
**适合谁**：觉得官方 docx/xlsx/pptx skill 不够细的人。
**备注**：跟 anthropics/skills 是补充关系，不是替代。

### [kreuzberg-dev/kreuzberg](https://github.com/kreuzberg-dev/kreuzberg) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 8.8k+ |
| License | NOASSERTION |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：97+ 种文件格式（PDF、Office、图片）解析框架，Rust 核心。提供 MCP server + REST API + CLI。
**适合谁**：跨格式批量处理文件、要 throughput 的工程师。
**备注**：不只是 PDF / Office——还支持冷门格式如 HWP、ODT 等。

---

## 3. Google Workspace

### [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 2.9k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐（一个 server 包整套 Google） |

**教什么**：Gmail、Calendar、Docs、Sheets、Slides、Drive、Chat、Forms、Tasks、Search 全部一个 MCP server 搞定。
**适合谁**：Google Workspace 重度用户——回信、开会、写文件、操作 sheet 都一个 server 处理。
**备注**：OAuth 设置稍微麻烦但一次设置好；功能覆盖 Google 各家最完整。

### [xing5/mcp-google-sheets](https://github.com/xing5/mcp-google-sheets) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 952 |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（单纯 Sheets 用） |

**教什么**：专门 Google Sheets / Drive 集成，建 sheet、改 cell、查 formula。
**适合谁**：只用 Google Sheets、不想装整套 Workspace MCP 的人。
**备注**：scope 比 google_workspace_mcp 窄，但设置简单。

---

## 4. Microsoft 365

### [Softeria/ms-365-mcp-server](https://github.com/Softeria/ms-365-mcp-server) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 908 |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（M365 全套） |

**教什么**：透过 Microsoft Graph API 操作 M365——Outlook、Teams、OneDrive、SharePoint。
**适合谁**：用 M365 的企业用户——要 LLM 回信、查行事历、捞 OneDrive 档。
**备注**：需要 Azure AD app registration；公司 IT 政策可能挡。

### [ryaker/outlook-mcp](https://github.com/ryaker/outlook-mcp) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 407 |
| License | NOASSERTION |
| 推荐度 | ⭐⭐⭐（只 Outlook） |

**教什么**：透过 Graph API 读写 Outlook mail / calendar。
**适合谁**：只要操作 Outlook 不需要其他 M365 服务的人。
**备注**：scope 比上面的 ms-365 server 窄。

### [merill/lokka](https://github.com/merill/lokka) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 278 |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：M365 + Microsoft Graph 全套，含 Entra（AD）、Intune 等管理用 API。
**适合谁**：M365 系统管理员、要操作 Tenant / 用户 / 策略的人。
**备注**：对 IT admin 比 end user 更有用。

---

## 5. 开发协作（GitHub / Atlassian / Slack…）

### [github/github-mcp-server](https://github.com/github/github-mcp-server) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 31k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐（**官方**） |

**教什么**：GitHub 官方 MCP——issue / PR / repo / Actions / Codespaces 操作。
**适合谁**：所有 GitHub 用户；Claude Code 接上去后 PR review、issue triage、release notes 都能跑。
**备注**：**走 Track A 的 A3 动手练习 CLI-9 必装**。

### [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 5.6k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐（社群最热门 Atlassian） |

**教什么**：Confluence + Jira 一个 MCP server，社群版本功能多、设置弹性。
**适合谁**：用 Atlassian 但 Atlassian 官方 remote server 限制多的人。
**备注**：跟下面 atlassian/atlassian-mcp-server（官方）择一，看公司 IT 政策。

### [atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 927 |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐（**官方**） |

**教什么**：Atlassian 官方 Remote MCP，安全连 Jira / Confluence。
**适合谁**：公司有 enterprise Atlassian、IT 规定只能用官方的人。
**备注**：Remote 模式，有官方 SLA。

### [korotovsky/slack-mcp-server](https://github.com/korotovsky/slack-mcp-server) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 1.8k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（无 admin 权限也能用） |

**教什么**：Slack MCP，DM / group DM / 频道消息抓取，自带 history fetch logic。
**适合谁**：个人用户（不是 Slack admin）也想接 Slack 的人。
**备注**：不需要 admin 级别 token；走用户层 OAuth。

### [jerhadf/linear-mcp-server](https://github.com/jerhadf/linear-mcp-server) ⭐⭐⭐（⚠️ 最后 commit 2025-05、已逾一年未更新）

| 栏位 | 内容 |
|---|---|
| Stars | ★ 344 |
| License | MIT |
| 推荐度 | ⭐⭐⭐（⚠️ 已逾一年未更新） |

**教什么**：Linear（issue tracker）MCP——查 issue、建 issue、改 status。
**适合谁**：用 Linear 管 sprint / backlog 的开发者。
**备注**：要 Linear API key。

### [SaseQ/discord-mcp](https://github.com/SaseQ/discord-mcp) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 443 |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：Discord MCP——读写频道消息、管理服务器。
**适合谁**：用 Discord 跑社群 / 开源项目的 maintainer。
**备注**：要 Discord bot token；要小心 rate limit。

### [safishamsi/graphify](https://github.com/safishamsi/graphify) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 101k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：把 codebase / SQL schemas / R scripts / shell scripts / docs / papers / images / videos 变成 queryable knowledge graph 的 AI coding skill。Claude Code、Codex、OpenCode、Cursor、Gemini CLI 都能接。
**适合谁**：要对大型 codebase 做架构分析、跨档追 reference、把"app code + DB schema + infra"放一起问的工程师 / 研究者。
**备注**：跨界——既是 dev collab tool（理解既有 codebase）也算 research workflow（把任意素材转成 graph）。撞墙时用 graphify 抽结构、再丢回 Claude 推论。

### [upstash/context7](https://github.com/upstash/context7) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 60k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐（写代码必装） |

**教什么**：把最新版的 library / framework 文档拉进 agent 的 context，让它别再用过时或幻觉出来的 API；是安装量最高的 coding MCP 之一。
**适合谁**：用 Claude Code / Cursor 写代码、常被旧版 API 或编造出来的方法坑到的开发者。
**备注**：直接缓解“模型知识截止后 API 已经变了”的问题——写代码时把它挂上，省掉手动贴文档。

### [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 38k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐（code intelligence） |

**教什么**：把 codebase 索引成可查询的 knowledge graph，让 coding agent 用“查结构 / 符号 / 调用路径”取代反复 grep + 读文件。单一 static binary、158 种语言。
**适合谁**：在大型或不熟的 repo 上跑 coding agent、想快速定位又想省 token 的人。
**备注**：大改后要重新索引（graph 会 stale）；把它的回答当“快速第一手”、load-bearing 的结论（谁调用 X / 这段是不是死码）再用实际代码验证。

---

## 6. 数据库

### [googleapis/mcp-toolbox](https://github.com/googleapis/mcp-toolbox) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 16k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐⭐（**Google 官方**，多 DB） |

**教什么**：跨 DB 的 MCP server——MySQL / PostgreSQL / Cloud SQL / Spanner / BigQuery 一次包。
**适合谁**：在 Google Cloud 上跑 DB 的工程师、要支持多 DB 引擎的开发者。
**备注**：开源 + Google 官方维护，是可上线使用的选择。

### [bytebase/dbhub](https://github.com/bytebase/dbhub) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 3.2k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐（社群多 DB MCP） |

**教什么**：zero-dependency、token-efficient 的多 DB MCP——Postgres、MySQL、SQL Server、MariaDB、SQLite。
**适合谁**：不想装 Google Cloud SDK、要跨多种 OSS DB 的工程师。
**备注**：跟 googleapis/mcp-toolbox 重叠，但更轻量。

### [supabase-community/supabase-mcp](https://github.com/supabase-community/supabase-mcp) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 2.9k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐⭐（**Supabase 官方社群**） |

**教什么**：把 Supabase（含 Postgres、Auth、Storage、Edge Functions）接到 LLM。
**适合谁**：用 Supabase 跑后端的全栈开发者。
**备注**：官方 community 维护。

### [timescale/pg-aiguide](https://github.com/timescale/pg-aiguide) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 1.8k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐（Postgres 写代码辅助） |

**教什么**：MCP server + Claude plugin，帮 LLM 生成更好的 PostgreSQL 代码。
**适合谁**：写 Postgres heavy SQL / DBA 工程师。
**备注**：偏“LLM 写 SQL 辅助”，不只是 query 执行。

### [benborla/mcp-server-mysql](https://github.com/benborla/mcp-server-mysql) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 2k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（read-only MySQL） |

**教什么**：read-only MySQL MCP，让 LLM 看 schema、跑 query。
**适合谁**：要让 LLM 分析 production DB 但不能改的场景。
**备注**：故意 read-only 是 safety feature，不是限制。

### [mongodb-js/mongodb-mcp-server](https://github.com/mongodb-js/mongodb-mcp-server) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 1.1k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐（**MongoDB 官方**） |

**教什么**：MongoDB 跟 MongoDB Atlas Cluster MCP server。
**适合谁**：用 MongoDB / Atlas 的工程师。
**备注**：mongodb-js 是 MongoDB 官方 GitHub org。

### [redis/mcp-redis](https://github.com/redis/mcp-redis) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 555 |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（**Redis 官方**） |

**教什么**：Redis 官方 MCP，自然语言操作 Redis 跟 Redis Stack（Vector / Search / JSON）。
**适合谁**：用 Redis 当 cache / vector DB / queue 的人。
**备注**：官方维护；包含 vector search 集成。

### [awslabs/mcp](https://github.com/awslabs/mcp) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 9.3k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐（**AWS 官方**） |

**教什么**：AWS 官方 MCP server（Lambda / S3 / DynamoDB / CloudWatch / Cost Explorer 等）。
**适合谁**：在 AWS 上、想让 agent 查询 / 操作云端资源的团队。
**备注**：AWS 官方维护；沿用你现有的 AWS 登录（CLI profile / IAM role），不用另外管 token。

---

## 7. 浏览器自动化 / 网页抓取

### [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 35k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐⭐（**Microsoft 官方**） |

**教什么**：Playwright MCP server——让 LLM 开浏览器、点按钮、填表单、抓网页。
**适合谁**：要做 E2E 自动化、跨网站集成、抓需要登录的网页的人。
**备注**：Playwright 官方出，最 robust。**Claude Code 接 web 自动化是个不错的选项**。

### [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 47k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐⭐（**Chrome 官方**） |

**教什么**：把 Chrome DevTools 接给 coding agent——performance、network、console 直接给 LLM 看。
**适合谁**：调试前端 bug、做 web performance 分析的开发者。
**备注**：搭配 Playwright MCP 用最强——一个跑、一个观察。

### [firecrawl/firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 7k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐（**Firecrawl 官方**） |

**教什么**：Firecrawl 官方 MCP——大规模网页抓取 + search + 结构化提取。
**适合谁**：要抓大量网页当训练数据 / 做 RAG / 做研究的人。
**备注**：需要 Firecrawl API key（有 free tier）。

### [browserbase/mcp-server-browserbase](https://github.com/browserbase/mcp-server-browserbase) ⭐⭐⭐⭐（⚠️ 已封存）

| 栏位 | 内容 |
|---|---|
| Stars | ★ 3.3k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐（**Browserbase 官方**、⚠️ 已封存） |

**教什么**：Browserbase 官方 MCP，配 Stagehand 跑 cloud-based 浏览器。
**适合谁**：本地跑浏览器太重 / 要在 cloud 并行跑多个 session 的人。
**备注**：商业服务（有免费额度），跟 Playwright MCP 互补（local vs cloud）。

---

## 8. 设计（Figma / Excalidraw）

### [GLips/Figma-Context-MCP](https://github.com/GLips/Figma-Context-MCP) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 15k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐（最热门 Figma MCP） |

**教什么**：把 Figma layout 信息送给 coding agent——读设计稿、提组件结构，给 Cursor / Claude Code 写对应的 React component。
**适合谁**：前端开发者，要 LLM 从 Figma 设计稿生成 component code。
**备注**：要 Figma access token；对 design-to-code workflow 必装。

### [excalidraw/excalidraw-mcp](https://github.com/excalidraw/excalidraw-mcp) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 5k+ |
| License | NOASSERTION |
| 推荐度 | ⭐⭐⭐⭐⭐（**Excalidraw 官方**） |

**教什么**：streamable Excalidraw MCP，让 LLM 直接画架构图、流程图。
**适合谁**：写设计文档 / 系统架构 / 流程图的人——叫 Claude 从文字描述画图。
**备注**：Excalidraw 官方出，输出可直接导入 Excalidraw 编辑。

### [yctimlin/mcp_excalidraw](https://github.com/yctimlin/mcp_excalidraw) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 2.2k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（替代版 Excalidraw） |

**教什么**：MCP server + Claude Code Skill，real-time canvas sync，可创建 / 编辑 / 导出。
**适合谁**：需要 real-time canvas sync 跟编程化操作的人。
**备注**：跟官方版互补，社群维护。

### [pbakaus/impeccable](https://github.com/pbakaus/impeccable) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 57k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**："**让你 AI harness 在 design 上更强的 design language**"——一套设计 vocabulary / pattern，帮 AI 在生成 UI / 视觉成品时跳出常见的"AI 感"生硬风格。
**适合谁**：用 AI 生 UI / mockup / visual design 但结果都很 generic 的开发者；前端 + AI workflow。
**备注**：不是 MCP server 也不是 Skill 包——是一份"**design language**"reference。让 AI 看到比较高质量的设计词汇才生得出比较好的东西。

---

## 9. 监控 / Observability

### [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 3.3k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐⭐（**Grafana 官方**） |

**教什么**：Grafana 官方 MCP，从 LLM 直接查 dashboard、metric、alert。
**适合谁**：用 Grafana 看 metric 的 SRE / DevOps。
**备注**：“dashboard 那条线为什么掉？”直接问，LLM 捞 metric 给答案。

### [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 782 |
| License | NOASSERTION |
| 推荐度 | ⭐⭐⭐⭐（**Sentry 官方**） |

**教什么**：从 LLM 查 Sentry error event、issue、trace。
**适合谁**：用 Sentry 接 production error 的工程师。
**备注**：“上周这个 error 的 stack trace 给我看”直接问 Claude Code。

### [winor30/mcp-server-datadog](https://github.com/winor30/mcp-server-datadog) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 142 |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐（社群版 Datadog） |

**教什么**：Datadog API MCP——查 monitor、log、metric。
**适合谁**：用 Datadog 但 Datadog 还没出官方 MCP 的人。
**备注**：等 Datadog 官方 MCP 出来可能换掉这个。

---

## 10. 媒体 / 串流（YouTube / Spotify）

### [varunneal/spotify-mcp](https://github.com/varunneal/spotify-mcp) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 599 |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：把 LLM 接到 Spotify——播歌、加歌单、查历史。
**适合谁**：想用 Claude Code 控播放列表、做语音 / 文字 → 音乐的集成者。
**备注**：要 Spotify Premium 账号（API 限制）。

### [kimtaeyoon83/mcp-server-youtube-transcript](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 581 |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（YouTube 字幕） |

**教什么**：直接抓 YouTube 视频字幕给 LLM 摘要、翻译、做 RAG。
**适合谁**：用视频当学习材料、要批量摘要 YouTube 内容的人。
**备注**：依赖 YouTube auto-caption；非英文视频字幕质量参差。

### [ZubeidHendricks/youtube-mcp-server](https://github.com/ZubeidHendricks/youtube-mcp-server) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 557 |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（YouTube 完整 API） |

**教什么**：完整 YouTube API MCP——除了 transcript，还能管 video、Shorts、analytics。
**适合谁**：YouTube 创作者要自动化频道管理。
**备注**：需要 YouTube Data API key + OAuth。

---

## 11. 中文圈专属

### [leemysw/feishu-docx](https://github.com/leemysw/feishu-docx) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 243 |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：飞书（Lark）docs / sheet / bitable ↔ Markdown 双向转换，含 OAuth 2.0、CLI、TUI、Claude Skills。
**适合谁**：用飞书 / Lark 写文档的中文用户，要把 Lark 内容跟 Claude Code 串起来。
**备注**：目前中文圈 MCP / Skill 主要选择之一；微信 / 钉钉暂时没有独立 MCP（多半混在 chat bot framework 里）。

### [netease-youdao/LobsterAI](https://github.com/netease-youdao/LobsterAI) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 5.6k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：网易有道出品的"24/7 全场景 AI agent"——支持工作流自动化、跨应用协作、文件处理。中文 native。
**适合谁**：中文圈用户要找一个替代 Claude Code / OpenAI Operator 等级的 all-in-one agent；对中国大陆服务（网易、钉钉等）集成需求高的场景。
**备注**：产品式 agent（不是 Skill / MCP）；跟 Claude Code / Codex 互为替代，不是搭配。

### [QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 16k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：阿里巴巴官方 Qwen agent framework——RAG、tool use、code interpreter、multi-agent、MCP 兼容，默认搭配 Qwen 系列模型但可换其他 LLM。
**适合谁**：用 Qwen / 通义千问 为主 LLM 的开发者；想要中文 native 的 agent framework（范例、文档都中文齐全）。
**备注**：MCP 兼容是亮点——可以直接接到 Claude Code 等 host；维护节奏正常（last commit 2026-03）。

### [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 21k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：字节跳动 Coze 的开源版——no-code agent builder（workflow / plugin / knowledge / memory），可自部署或上云。
**适合谁**：不想写 code 但要做 agent 的团队；想看 enterprise agent platform 内部设计（RAG、工作流、Memory、Plugin 系统的 reference 实现）。
**备注**：底层 framework 是 Coze 自家的 Eino；可接 OpenAI / Claude / Qwen / 国产 LLM。国际版（coze.com）跟中国版（coze.cn）共用此 codebase。

### [coze-dev/coze-loop](https://github.com/coze-dev/coze-loop) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 5.6k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：Coze 出的 agent observability + evaluation 平台——trace、debug、eval、prompt management，agent dev lifecycle 的下半场。
**适合谁**：agent 已经跑起来、要 production 监控的团队；想看"agent eval / observability"可以怎么做的人。
**备注**：跟 LangSmith / Arize Phoenix 同类；开源版可自部署。

### [liaokongVFX/LangChain-Chinese-Getting-Started-Guide](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 8.9k+ |
| License | 未标注 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：LangChain 中文入门指南——从 LangChain 基础、Prompt、Memory、Agent、Chains 到实作应用，最早期且最完整的中文 LangChain 学习资源。
**适合谁**：想用 LangChain 但英文文档吃不下去的中文用户；想理解 LangChain 设计脉络再决定要不要走这条路的人。
**备注**：没有正式 license（内容开放阅读）；LangChain 框架本身演进很快，书中部分 API 可能跟最新版有出入。

### [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 37k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：基于 LangChain 的开源知识库问答系统——本地化部署、支持多种向量数据库、RAG 端到端范例。
**适合谁**：想做 RAG 又不想全部自己刻的中文团队；要本地部署（不能用云端 LLM）的场景。
**备注**：★ 37k 是中文圈最热门的 RAG 实现之一；维护节奏放缓（last commit 2025-11）。新项目建议先 fork 后评估，当参考实现用。

### [usewhale/whale](https://github.com/usewhale/whale) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 967 |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：专为 DeepSeek 模型优化的终端 AI 编码助手——支持 MCP server 接入、Claude-style Skills、对话缓存优化，Go 实现。
**适合谁**：以 DeepSeek 为主力 LLM 的中文开发者；想用终端工具但不需要 Claude Code 全家桶的人。
**备注**：开源同类中少见的 DeepSeek 专属优化；MCP + Skills 双支持让它可以逐步扩充能力。

### [simonlin1212/a-stock-data](https://github.com/simonlin1212/a-stock-data) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 9.2k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：A 股全栈数据工具包——单一 SKILL.md 文件封装 8 个数据源（mootdx、东财、akshare、iwencai 等）21 个端点，AI 编码助手直接可用。
**适合谁**：用 Claude Code / Codex / OpenClaw 做投研或量化分析的中文开发者；不想自己刻数据抓取逻辑的人。
**备注**：一条 `curl` + `pip install` 即可启用；中国 A 股数据类 Skill 中星星数最高的社群实现。兼容 Claude Code、Codex、OpenClaw。

> 想找微信 / 钉钉集成？目前主流是用 chat bot framework（如 zhayujie/CowAgent）而不是纯 MCP server。等正规 MCP 出现再加进来。

### [MoonshotAI/Kimi-K2](https://github.com/MoonshotAI/Kimi-K2) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 10.7k+ |
| License | Modified MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：月之暗面 Moonshot 的 Kimi K2 开源大模型系列——开源权重 + OpenAI / Anthropic 兼容 API，主打 agentic / coding / 长程任务，可当 agent stack 的后端模型。
**适合谁**：想用国产开源模型跑 agent / coding 工作流、或要在自部署环境跑开源权重的中文开发者。
**备注**：License 是 Modified MIT（标准 MIT + 大规模商用附加条款）——商用前先读原始 LICENSE；weights 另在 Hugging Face。

### [zai-org/GLM-4.5](https://github.com/zai-org/GLM-4.5) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 4.3k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐ |

**教什么**：智谱 Zhipu（Z.ai）的 GLM-4.5 开源模型——定位 Agentic / Reasoning / Coding（ARC）基础模型，开源权重 + API，可当 agent / tool use / coding 的后端。
**适合谁**：想评估国产开源 agentic 模型、或需要 Apache-2.0 宽松许可权重的中文开发者。
**备注**：zai-org 是智谱开源 org；同系列另有 GLM-4（★ 7k+）可一起参考；weights 在 Hugging Face。

---

## 12. 其他常用（Cloudflare / Stripe…）

### [cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 4k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐⭐（**Cloudflare 官方**） |

**教什么**：Cloudflare 官方 MCP——Workers、Pages、R2、KV、D1、DNS、Zero Trust 全包。
**适合谁**：用 Cloudflare 跑 edge / serverless 的人。
**备注**：官方维护；最佳的 edge platform MCP。

### [stripe/ai](https://github.com/stripe/ai) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 1.7k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（**Stripe 官方**） |

**教什么**：Stripe 官方 AI agent toolkit，含 MCP server，操作付款、订阅、退款、客户。
**适合谁**：要在 agent 内处理付款 / billing 的开发者。
**备注**：⚠️ 涉及金流，务必用 sandbox 测试够了再接 production。

### YIELD INTELLIGENCE MCP（Hosted Remote Server）

| 栏位 | 内容 |
|---|---|
| 形式 | hosted MCP server |
| 推荐度 | ⭐⭐⭐（金融分析工具；了解 hosted vs self-hosted MCP 实现差异的实例） |

**教什么**：YIELD INTELLIGENCE hosted remote MCP server——即时美国国债收益率 + 股息 ETF / REIT / 优先股分析 + 被动收入投资组合优化。2 个工具：`analyze_yield_opportunities`（扫描被动收入机会）+ `optimize_income_portfolio`（面向目标月收入建立投资组合）。已收录于官方 MCP Registry（`io.github.thebrierfox/intuitek-ace`，since 2026-05-10）。
**适合谁**：用 Claude Code / Claude Desktop 做个人理财分析、想让 AI 找出被动收入机会的人。hosted remote MCP server 范例——直接 plug URL、0 安装、适合 Stage 5 学完 MCP 概念后用来体验 hosted vs self-hosted 差异。
**备注**：Live endpoint `https://api.intuitek.ai/yield/mcp`（no auth、no API key）。x402 micropayment $1 USDC/call on Base（agent-to-agent 场景）；一般用户免费。纯分析工具，不涉及交易。GitHub：[thebrierfox/intuitek-ace](https://github.com/thebrierfox/intuitek-ace)（MIT License）。

### [ComposioHQ/composio](https://github.com/ComposioHQ/composio) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 28.8k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐（1000+ 工具整合枢纽） |

**教什么**：一个平台（SDK + MCP server），把 agent 连到 1000+ 应用（Slack / GitHub / Gmail / Salesforce / Notion…），登录它帮你处理，不用一个服务各写一个连接器。
**适合谁**：agent 要跨大量工具、但不想维护几十个独立 MCP server 的团队。
**备注**：提供 MCP server + Python / TypeScript SDK；可通过 MCP 接到 Claude Code。属"工具聚合器"（跟 n8n / Zapier 自动化平台同类）。

---

### [morluto/jacobian](https://github.com/morluto/jacobian) ⭐⭐⭐（⚠️ 作者本人投稿）

| 栏位 | 内容 |
|---|---|
| Stars | ★ 58 |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：用一个可直接安装的数学 MCP server，练习让 agent 调用可组合的精确计算工具；涵盖 polynomial maps、linear algebra 和 graph algorithms。
**适合谁**：想在 MCP 工作流中加入数学计算，或需要让 agent 处理结构化数学问题的研究者与开发者。
**备注**：Python 项目，但通过 npm 发布启动器，所以用 `npx` 起 server。同时提供 MCP server、CLI 和 Python library；可以从一个简单的本地 MCP 配置开始，再按需使用原生 Python API。
**怎么运行**：
```bash
npx -y jacobian mcp
```

---

## 13. 研究工作流 Skills（学术 / paper / 文献）

> ⚠️ **maintainer 自家项目区**：以下几个是本 repo 维护者 [@WenyuChiou](https://github.com/WenyuChiou)（Lehigh CEE PhD candidate）日常在用的研究 skills，公开出来给其他研究者参考。**因为是自己的东西、又是相对 niche 的研究场景，star 数量会比通用工具低**。star 门槛在这节是放宽的——选收的标准是“在我自己的研究流程里实际有用”。请自己评估是否合用。

### [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 222 |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐（研究流程一整套） |

**教什么**：14 个 Claude Code skills 涵盖常见研究任务——文献分流、研究设计、project context、论文写作、multi-AI delegation。打包成 5-plugin marketplace，一个指令安装。
**适合谁**：研究生 / 博后想一次获取“研究全流程”skill set。
**备注**：marketplace 形式，跟 Stage 5.4 教的 plugin/marketplace 概念对齐。

### [WenyuChiou/academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 17 |
| License | MIT |
| 推荐度 | ⭐⭐⭐（窄但深） |

**教什么**：严谨学术论文写作 / 修改 / 投稿的 Claude Code skill。Field-agnostic，可用 per-paper journal_format.md 跟 style_overrides.md 客制规则。
**适合谁**：在写 / 改 paper 的研究者，想把 banned-word audit、figure-text coupling、submission checklist 自动化。
**备注**：是 ai-research-skills 5 plugin 中的一个，也可独立安装。

### [WenyuChiou/zotero-skills](https://github.com/WenyuChiou/zotero-skills) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 50 |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：Zotero CLI skill——程序化搜索 / 添加 / 分类 / 标记文献。
**适合谁**：用 Zotero 管理文献、想让 Claude Code 直接整理 library 的研究者。
**备注**：跟 [`MuiseDestiny/zotero-gpt`](https://github.com/MuiseDestiny/zotero-gpt) 的区别——后者是 Zotero plugin（在 Zotero 里 chat），这份是 CLI / Skill（从 Claude Code 操作 Zotero）。

### [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 52 |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：AI-operable research workspace，集成 Zotero + Obsidian + NotebookLM 三个工具，提供 CLI / MCP / REST / dashboard 四种接口。
**适合谁**：同时用 Zotero / Obsidian / NotebookLM 的研究者，想把它们绑成一个 workspace 给 LLM 操作。
**备注**：跟单一工具的 MCP（mcp-obsidian、notion-mcp 等）互补——这份是 hub，可集成多个工具。

---

## 14. Multi-LLM Delegation Skills

> ⚠️ **maintainer 自家项目区**：跟 13 一样，以下是维护者把自己 daily workflow 抽出来公开的 delegation skills。star 门槛放宽，选收标准是“真的能让 Claude planner + Codex/Gemini 执行者组合稳定跑下去”。Multi-LLM 领域变化快，建议跟其他 multi-agent framework（Stage 7 列的）一起评估后选择。

<!-- not-an-entry -->
### 三个 skill 的组合（composition）

下面 3 个 skill 是**设计成一起用**的，不是独立工具：

![Claude + 3 个 delegate skill 分工](../resources/diagrams/multi-llm-delegation-composition.zh-Hans.png)

Claude 不擅长 token-heavy 机械式工作（成本高、context 容易爆）；Codex 不擅长对话协作；Gemini 有 1M context 但中型推理稍弱。**分工 = Claude 负责 design / review、Codex 负责 implement、Gemini 负责 long-form draft / synthesis**。

### [WenyuChiou/codex-delegate](https://github.com/WenyuChiou/codex-delegate) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 62 |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：Claude Code skill 把 Codex CLI 当作 execution specialist——大量文件 refactor、batch edits、boilerplate 生成、wrapper-based 实现密集任务。Claude 写 plan + review，Codex 执行。
**适合谁**：要省 token / 提速大规模机械式编辑的开发者；想验证“multi-agent 不只是 buzzword”的学习者。
**何时用**：refactor 30+ files、生成 test scaffold、把同一个 pattern port 到 N 个文件、写 migration script。
**何时不用**：架构决策、bug 诊断、security review、需要 conversation memory 的任务——这些 Claude 直接做更好。
**备注**：跟 `gemini-delegate-skill` 互补。Stage 7 multi-agent 的实战版。

### [WenyuChiou/gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill) ⭐⭐⭐（⚠️ 已封存 2026-07）

| 栏位 | 内容 |
|---|---|
| Stars | ★ 37 |
| License | MIT |
| 推荐度 | ⭐⭐⭐（⚠️ 已封存） |

**教什么**：Claude Code skill 把 Gemini CLI 当作 long-form / large-context / CJK 执行者——百万 token context window、中文长文 draft、second-opinion review。Claude 出大纲跟 critique，Gemini 写长文。
**适合谁**：研究者写 paper、知识工作者写中文报告 / Threads post、需要第二个 LLM 意见对照的人。
**何时用**：长文 draft（>3000 字）、跨多份长文档 synthesis（要塞进 1M token 的 context）、中文 / CJK 内容、要 LLM-vs-LLM 对比视角。
**何时不用**：短查询、code generation（用 codex）、production-critical 决策（最终人类 review）。
**备注**：跟 `codex-delegate` 是“Codex 写 code、Gemini 写 prose”的分工。

### [WenyuChiou/agent-collab-skills](https://github.com/WenyuChiou/agent-collab-skills) ⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 22 |
| License | MIT |
| 推荐度 | ⭐⭐（experimental，当作 reference 看就好） |

**教什么**：Claude Code marketplace for multi-agent collaboration——task splitter、output reconciler、adversarial debate、shared memory、acceptance gate。跟 codex-delegate / gemini-delegate 组合用。
**适合谁**：要跑 2+ delegate agent 在同一轮、想看 multi-agent coordination 怎么打包成 marketplace 的人。
**备注**：experimental——别把它当作生产级 framework，当作维护者把自己 setup 公开的 reference 看就好。要可上线部署的请看 Stage 7 的 LangGraph / Microsoft Agent Framework / CrewAI。

---

## 15. 金融 / 交易 Agents

> ⚠️ **应用领域区**：agent 在量化交易 / hedge fund 模拟 / 自动下单的应用。本节两个 entry 分别是 Apache-2.0 与 MIT，但这类 repo 授权状态普遍混杂，使用前仍请自行查清楚。**警示**：trading agent 跑真实资金有显著风险，本目录列入是为了学习 agent 设计模式、不是投资建议。

### [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 97k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐ |

**教什么**：多 agent LLM 框架做金融交易决策，bull / bear / fundamentals / technicals / risk 各 agent 分工。
**适合谁**：想看 multi-agent 在分析性任务怎么分工的学习者；量化研究者想实验 LLM 增强既有 pipeline。
**备注**：Apache-2.0、允许修改与商用（保留授权声明）；**非投资建议，别直接拿来下实单**。

### [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) ⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 62k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：多角色 AI hedge fund 模拟，bull / bear / 基本面 / 技术面 / 风控 agent 协作产生 trade recommendation。
**适合谁**：看过 Stage 7 multi-agent 想要一个完整应用案例的学习者；对 agent + 金融交叉领域有兴趣的人。
**备注**：MIT 授权；**模拟性质、非投资建议**。

---

## 16. 网页搜索 / 检索（Web Search / Retrieval）

### [exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 4.8k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（**Exa 官方**） |

**教什么**：Exa 官方 MCP——为 LLM / agent 设计的网页搜索（neural + keyword 两种），回传干净结果直接喂进 prompt。
**适合谁**：要做研究 / fact-check / 在线 RAG 检索的人——语义搜索在“概念相关”场景特别强，纯 keyword 反而没那么吃香。
**备注**：需要 Exa API key。

### [tavily-ai/tavily-mcp](https://github.com/tavily-ai/tavily-mcp) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 2.3k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐（新手第一选择） |

**教什么**：把 Tavily search API 包成 MCP——为 LLM / RAG 打造的网页搜索，回传答案 + 出处来源。
**适合谁**：新手只想让 agent 会上网搜东西的第一选择——免费额度好上手。
**备注**：有易用的 free tier；要 Tavily API key。

---

## 17. 安全 / MCP 安全治理

### [trailofbits/skills](https://github.com/trailofbits/skills) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 6.6k+ |
| License | CC-BY-SA-4.0 |
| 推荐度 | ⭐⭐⭐⭐⭐（**Trail of Bits 官方**） |

**教什么**：安全公司 Trail of Bits 官方的 Claude Code plugin marketplace，收的是他们自己在用的安全分析、测试与漏洞研究 skills。
**适合谁**：想让 agent 帮忙做 code audit、漏洞分析、安全测试的人；也适合想看“专业安全团队怎么把方法论写成 skill”的人。
**备注**：用 `/plugin marketplace add trailofbits/skills` 安装，Codex 也直接支持同一套 marketplace。授权是 **CC-BY-SA-4.0**（share-alike），改作后要用相同授权发布，商用集成前先确认。注意它跟 Stage 5 那张表里的 [`trailofbits/skills-curated`](https://github.com/trailofbits/skills-curated) 是**两个不同的 repo**：后者是由 Trail of Bits 审核、内容来自社区贡献的策展 marketplace，这一个是 Trail of Bits 自家的安全 skills。

### [stacklok/toolhive](https://github.com/stacklok/toolhive) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 2k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：把每一个 MCP server 跑在隔离容器里，用最小权限文件取代本机凭证，并提供 audit log 与可配置的身份／访问策略；另附 Kubernetes operator。
**适合谁**：团队里已经有人各自装了一堆 MCP server，开始需要回答“谁装了什么、它能拿到哪些凭证”的人。
**备注**：Go 项目，桌面版与 CLI 都有。开源的 ToolHive 与 Stacklok 的企业版是分开的，评估功能时注意分界在哪。

### [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 8.3k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐（**NVIDIA 官方**） |

**教什么**：给自动化 agent 用的沙箱化执行环境，用声明式策略管住文件、网络与进程；Claude Code 与 Codex 不改任何代码就能跑在里面（OpenClaw 要另外通过下面那则 NemoClaw）。
**适合谁**：要让 agent 真的能执行命令、但不想把整台机器交出去的人。
**备注**：Rust 项目。需要 Docker / Podman 或主机虚拟化（MicroVM sandbox 用）；Windows 走 WSL 2 且标为 experimental。**⚠️ 项目自述仍是 alpha**（最新 release 还在 `v0.0.x`），拿来读与试可以，正式依赖前先自行评估。与 `toolhive` 的分工是：toolhive 管的是 MCP server，这个管的是 agent 本身的执行边界。

### [nolabs-ai/nono](https://github.com/nolabs-ai/nono) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 3.7k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：用操作系统自己的隔离机制（Linux Landlock、macOS Seatbelt）挡住 agent，不需要 daemon 也不需要容器。
**适合谁**：想要沙箱但不想为此装一整套 container runtime 的人。
**备注**：Rust 项目，由做 Sigstore 的团队维护。零容器是它跟 OpenShell 最大的取舍差异：启动快、但隔离强度受限于操作系统提供的机制。

## 还有什么没收录？

如果你需要的集成不在上面，先看这些 catalog：

- [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) — 社群最完整 MCP server 清单，150+ 个按分类整理
- [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) — 另一份 MCP server 清单，跟上面互补
- [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) — 官方 reference servers（现有 7 个：everything、fetch、filesystem、git、memory、sequentialthinking、time；github、sqlite 已移到 `servers-archived`）
- [`travisvn/awesome-claude-skills`](https://github.com/travisvn/awesome-claude-skills) — Claude Skills 清单

### 要加新的？

1. 开 issue，附 repo 链接 + 为什么要加 + 属于哪个分类
2. 或直接送 PR：在对应分类下加一个 entry，按上面的格式写（Stars/License/推荐度 + 教什么/适合谁/备注）
3. **stars < 100 且非官方**通常会被退；除非你能说明 niche use case 强到可以例外

PR 送出前看一下 [`resources/style-guide.zh-Hans.md`](style-guide.zh-Hans.md) 跟 [`CONTRIBUTING.zh-Hans.md`](../CONTRIBUTING.zh-Hans.md)。

---

## 维护备注（给未来想帮忙的人）

不是 SLA，是“能做就做”的方向：

- Stars / license 用 `gh api repos/<owner>/<repo>` 抓，**有空 review 一轮就好**——不用排定期程
- 链接坏了、repo archived → 看到再修
- 新分类（AR/VR、IoT 等）有 1-2 个值得收的就可以先开
- “中文圈专属”分类维持宽松，中文社群 repo star 数累积较慢
- 用词、格式不一致 → 不要苛求，PR 进来能读懂优先

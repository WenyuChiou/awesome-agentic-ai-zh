# MCP / Skills 整合目錄

> **繁體中文** | [简体中文](./mcp-skills-catalog.zh-Hans.md) | [English](./mcp-skills-catalog.en.md)

> 把 Claude Code（或其他 CLI agent）接到你已經在用的工具，不用反覆切換視窗。本頁是 81+ 個分類整理過的 MCP server / Claude Skill / 整合範例（含研究工作流 + multi-LLM delegation 兩個專屬區）。

---

## 怎麼用這份目錄

- **想找特定工具的 MCP**：直接看下面分類目錄
- **想看 MCP / Skills / Plugins 是什麼**：先看 [README 三個核心用語](../README.md#-快速開始)，再看 [Stage 5 — Claude Code 生態系](../stages/05-claude-code-ecosystem.md)
- **想看 動手練習 怎麼裝、怎麼測**：看 [Stage 5.2 (MCP)](../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎) 跟 [Stage 5.3 (Skills)](../stages/05-claude-code-ecosystem.md#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層)

### 收錄方向（不是死規則）

- **官方優先**：Anthropic、廠商自己出的 MCP / Skill 通常排前面
- **stars 看一下就好**：社群 repo 大致 100+ 比較有人在維護，但「小眾但好用」也歡迎送 PR 解釋為什麼要收
- **盡量有 metadata**：stars / license 用 `gh api` 抓、有空就更新一輪
- **避免（不是禁止）**：archived、長期沒 commit、license 不明的 repo——niche 工具可以例外

### 目錄

1. [筆記 / 知識庫](#1-筆記--知識庫)（7）
2. [辦公文件（Word / Excel / PowerPoint / PDF）](#2-辦公文件word--excel--powerpoint--pdf)（7）
3. [Google Workspace](#3-google-workspace)（2）
4. [Microsoft 365](#4-microsoft-365)（3）
5. [開發協作（GitHub / Atlassian / Slack…）](#5-開發協作github--atlassian--slack)（9）
6. [資料庫](#6-資料庫)（8）
7. [瀏覽器自動化 / 網頁抓取](#7-瀏覽器自動化--網頁抓取)（4）
8. [設計（Figma / Excalidraw）](#8-設計figma--excalidraw)（4）
9. [監控 / Observability](#9-監控--observability)（3）
10. [媒體 / 串流（YouTube / Spotify）](#10-媒體--串流youtube--spotify)（3）
11. [中文圈專用](#11-中文圈專用)（11）
12. [其他常用（Cloudflare / Stripe…）](#12-其他常用cloudflare--stripe)（5）
13. [研究工作流 Skills（學術 / paper / 文獻）](#13-研究工作流-skills學術--paper--文獻)（4）
14. [Multi-LLM Delegation Skills](#14-multi-llm-delegation-skills)（3）
15. [金融 / 交易 Agents](#15-金融--交易-agents)（2）
16. [網頁搜尋 / 檢索（Web Search / Retrieval）](#16-網頁搜尋--檢索web-search--retrieval)（2）
17. [資安 / MCP 安全治理](#17-資安--mcp-安全治理)（4）

---

## 1. 筆記 / 知識庫

### [makenotion/notion-mcp-server](https://github.com/makenotion/notion-mcp-server) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 4.5k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐（**官方**） |

**教什麼**：Notion 官方 MCP server，可查詢 page、建立 page、操作 database。
**適合誰**：日常用 Notion 寫筆記 / 管專案 / 跑 wiki 的人——叫 LLM 直接撈資料、寫 page。
**備註**：需要 Notion integration token；有 read-only 跟 read-write 兩種模式可選。

### [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 4.1k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（社群、最熱門） |

**教什麼**：透過 Obsidian REST API community plugin 讓 LLM 讀寫你的 Obsidian vault。
**適合誰**：Obsidian 重度使用者，想用 Claude Code 整理 daily note、自動 link、跨檔搜尋。
**備註**：要先在 Obsidian 裝 [Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) plugin。

### [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 7.4k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：Claude Code Skill，用瀏覽器自動化操作 NotebookLM、查詢上傳文件，回覆帶 citation。
**適合誰**：用 NotebookLM 管 paper 跟研究筆記，但想在 Claude Code 一條 prompt 直接查的人。
**備註**：需要 Google 帳號登入授權。

### [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 18k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：非官方 NotebookLM Python API + CLI + agentic skill；功能比上面 skill 多，包含一些 web UI 沒開放的能力。
**適合誰**：要程式化批次操作 NotebookLM 的人（例如自動建 notebook、批次匯入文件）。
**備註**：非官方、Google 政策變動可能會壞；用前看一下 issue tracker。

### [ergut/mcp-logseq](https://github.com/ergut/mcp-logseq) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 312 |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：透過 Logseq Local HTTP API 讓 LLM 讀寫 Logseq graph。
**適合誰**：Logseq 使用者要自動化 daily journal、跨頁 link、查詢 backlinks。
**備註**：需要 Logseq 開啟 HTTP API（Settings → Features → HTTP API）。

### [skridlevsky/graphthulhu](https://github.com/skridlevsky/graphthulhu) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 171 |
| License | MIT |
| 推薦度 | ⭐⭐⭐（同時支援 Logseq + Obsidian） |

**教什麼**：39 個 tool，覆蓋 navigation、search、analysis、writing、journals、flashcards、whiteboards。
**適合誰**：同時用 Logseq 跟 Obsidian、不想裝兩套 MCP server 的人。
**備註**：community project，工具數多但每個工具相對基本。

### [ankimcp/anki-mcp-server](https://github.com/ankimcp/anki-mcp-server) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 430 |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：透過 AnkiConnect 讓 LLM 建卡、查卡、批改 deck。
**適合誰**：用 Anki 學語言 / 醫學 / 法律的人——叫 LLM 從教材自動產卡。
**備註**：需要 Anki 桌面版裝 [AnkiConnect](https://ankiweb.net/shared/info/2055492159) addon。

---

## 2. 辦公文件（Word / Excel / PowerPoint / PDF）

### [anthropics/skills](https://github.com/anthropics/skills) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 162k+ |
| License | 無 license 檔（上游未提供；使用前請先確認授權） |
| 推薦度 | ⭐⭐⭐⭐⭐（**官方**，必裝） |

**教什麼**：Anthropic 官方 Agent Skills repo，含 docx / xlsx / pptx / pdf 處理 skill。
**適合誰**：所有 Claude Code 使用者——直接 `claude skill install` 就能讓 Claude 讀寫 Office 檔。
**備註**：是 Skills 集合不是 MCP；走 Stage 5.3 Skill 體系。

### [haris-musa/excel-mcp-server](https://github.com/haris-musa/excel-mcp-server) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 4.1k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐（社群最熱門 Excel MCP） |

**教什麼**：Excel 檔操作 MCP server——讀 / 寫 / 改 cell、formula、sheet。
**適合誰**：日常處理 Excel 報表、要 LLM 自動填表 / 整理資料的人。
**備註**：Python 寫的，依賴 openpyxl。

### [GongRzhe/Office-PowerPoint-MCP-Server](https://github.com/GongRzhe/Office-PowerPoint-MCP-Server) ⭐⭐⭐（⚠️ 已封存 2025-12、可改用 anthropics/skills pptx）

| 欄位 | 內容 |
|---|---|
| Stars | ★ 1.8k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐（⚠️ 已封存） |

**教什麼**：用 python-pptx 操作 PPT——建簡報、改 slide、插圖、改 layout。
**適合誰**：要 LLM 從大綱 / Markdown 自動生 PPT 的人（顧問、講師、學生）。
**備註**：跟 anthropics/skills 的 pptx skill 重疊；那邊不夠用再來這邊。

### [1weiho/open-slide](https://github.com/1weiho/open-slide) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 6.5k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（agent-native 簡報框架） |

**教什麼**：為 coding agent 打造的 React 簡報框架——用自然語言描述簡報、讓 Claude Code / Codex / Cursor 寫出 React slides；內附 `/create-slide`、`/slide-authoring` 兩個 Claude Code Skill。
**適合誰**：想讓 agent 直接產出「程式碼即簡報、可進 git 版控」的人，跟 PowerPoint-MCP 走 .pptx 不同路。
**備註**：TypeScript / React / Vite，`npx @open-slide/cli init` 起手。它是 agent-native 工具（agent 來寫），不是 Stage 4 那種建構 agent 的編排框架。

### [SylphxAI/pdf-reader-mcp](https://github.com/SylphxAI/pdf-reader-mcp) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 880 |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（PDF 高效解析） |

**教什麼**：高速 PDF 解析 MCP，比 anthropics/skills 的 pdf skill 快 5-10×（號稱）。
**適合誰**：要批次讀 paper / contract / report 的人。
**備註**：parallel processing；大 PDF 處理速度有感差別。

### [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 790 |
| License | NOASSERTION |
| 推薦度 | ⭐⭐⭐（補強版 Office skill） |

**教什麼**：補強 anthropics/skills 沒覆蓋到的 Office workflow（automation、進階格式）。
**適合誰**：覺得官方 docx/xlsx/pptx skill 不夠細的人。
**備註**：跟 anthropics/skills 是補充關係，不是替代。

### [xberg-io/xberg](https://github.com/xberg-io/xberg) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 8.8k+ |
| License | NOASSERTION |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：97+ 種文件格式（PDF、Office、圖片）解析框架，Rust 核心。提供 MCP server + REST API + CLI。
**適合誰**：跨格式批次處理檔案、要 throughput 的工程師。
**備註**：不只是 PDF / Office——還支援冷門格式如 HWP、ODT 等。

---

## 3. Google Workspace

### [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 2.9k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐（一個 server 包整套 Google） |

**教什麼**：Gmail、Calendar、Docs、Sheets、Slides、Drive、Chat、Forms、Tasks、Search 全部一個 MCP server 搞定。
**適合誰**：Google Workspace 重度使用者——回信、開會、寫文件、操作 sheet 都一個 server 處理。
**備註**：OAuth 設定稍微麻煩但一次設定就好；功能覆蓋 Google 各家最完整。

### [xing5/mcp-google-sheets](https://github.com/xing5/mcp-google-sheets) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 952 |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（單純 Sheets 用） |

**教什麼**：專門 Google Sheets / Drive 整合，建 sheet、改 cell、查 formula。
**適合誰**：只用 Google Sheets、不想裝整套 Workspace MCP 的人。
**備註**：scope 比 google_workspace_mcp 窄，但設定簡單。

---

## 4. Microsoft 365

### [Softeria/ms-365-mcp-server](https://github.com/Softeria/ms-365-mcp-server) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 908 |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（M365 全套） |

**教什麼**：透過 Microsoft Graph API 操作 M365——Outlook、Teams、OneDrive、SharePoint。
**適合誰**：用 M365 的企業使用者——要 LLM 回信、查行事曆、撈 OneDrive 檔。
**備註**：需要 Azure AD app registration；公司 IT 政策可能擋。

### [ryaker/outlook-mcp](https://github.com/ryaker/outlook-mcp) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 407 |
| License | NOASSERTION |
| 推薦度 | ⭐⭐⭐（只 Outlook） |

**教什麼**：透過 Graph API 讀寫 Outlook mail / calendar。
**適合誰**：只要操作 Outlook 不需要其他 M365 服務的人。
**備註**：scope 比上面的 ms-365 server 窄。

### [merill/lokka](https://github.com/merill/lokka) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 278 |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：M365 + Microsoft Graph 全套，含 Entra（AD）、Intune 等管理用 API。
**適合誰**：M365 系統管理員、要操作 Tenant / 使用者 / 政策的人。
**備註**：對 IT admin 比 end user 更有用。

---

## 5. 開發協作（GitHub / Atlassian / Slack…）

### [github/github-mcp-server](https://github.com/github/github-mcp-server) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 31k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐（**官方**） |

**教什麼**：GitHub 官方 MCP——issue / PR / repo / Actions / Codespaces 操作。
**適合誰**：所有 GitHub 使用者；Claude Code 接上去後 PR review、issue triage、release notes 都能跑。
**備註**：**走 Track A 的 A3 動手練習 CLI-9 必裝**。

### [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 5.6k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐（社群最熱門 Atlassian） |

**教什麼**：Confluence + Jira 一個 MCP server，社群版本功能多、設定彈性。
**適合誰**：用 Atlassian 但 Atlassian 官方 remote server 限制多的人。
**備註**：跟下面 atlassian/atlassian-mcp-server（官方）擇一，看公司 IT 政策。

### [atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 927 |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐（**官方**） |

**教什麼**：Atlassian 官方 Remote MCP，安全連 Jira / Confluence。
**適合誰**：公司有 enterprise Atlassian、IT 規定只能用官方的人。
**備註**：Remote 模式，有官方 SLA。

### [korotovsky/slack-mcp-server](https://github.com/korotovsky/slack-mcp-server) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 1.8k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（無 admin 權限也能用） |

**教什麼**：Slack MCP，DM / group DM / 頻道訊息撈取，自帶 history fetch logic。
**適合誰**：個人使用者（不是 Slack admin）也想接 Slack 的人。
**備註**：不需要 admin 級別 token；走使用者層 OAuth。

### [jerhadf/linear-mcp-server](https://github.com/jerhadf/linear-mcp-server) ⭐⭐⭐（⚠️ 最後 commit 2025-05、已逾一年未更新）

| 欄位 | 內容 |
|---|---|
| Stars | ★ 344 |
| License | MIT |
| 推薦度 | ⭐⭐⭐（⚠️ 已逾一年未更新） |

**教什麼**：Linear（issue tracker）MCP——查 issue、建 issue、改 status。
**適合誰**：用 Linear 管 sprint / backlog 的開發者。
**備註**：要 Linear API key。

### [SaseQ/discord-mcp](https://github.com/SaseQ/discord-mcp) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 443 |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：Discord MCP——讀寫頻道訊息、管理伺服器。
**適合誰**：用 Discord 跑社群 / 開源專案的 maintainer。
**備註**：要 Discord bot token；要小心 rate limit。

### [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 101k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：把 codebase / SQL schemas / R scripts / shell scripts / docs / papers / images / videos 變成 queryable knowledge graph 的 AI coding skill。Claude Code、Codex、OpenCode、Cursor、Gemini CLI 都能接。
**適合誰**：要對大型 codebase 做架構分析、跨檔追 reference、把「app code + DB schema + infra」放一起問的工程師 / 研究者。
**備註**：跨界——既是 dev collab tool（理解既有 codebase）也算 research workflow（把任意素材轉成 graph）。撞牆時用 graphify 抽結構、再丟回 Claude 推論。

### [upstash/context7](https://github.com/upstash/context7) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 60k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐（寫 code 必裝） |

**教什麼**：把函式庫 / 框架的**最新版官方文件**即時拉進 agent 的 context，讓 LLM 不再依賴過時、會幻覺的 API；是安裝量最高的 coding MCP 之一。
**適合誰**：所有用 Claude Code / Cursor 寫 code 的人——尤其常踩「LLM 用舊版 API、查半天才發現過時」的開發者。
**備註**：解決的是「LLM 知識有 cutoff、套件卻一直更新」的痛點；一條 prompt 就能讓 agent 抓到當前版本的正確用法。

### [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 38k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐（code intelligence） |

**教什麼**：把 codebase 索引成可查詢的 knowledge graph，讓 coding agent 用「查結構 / 符號 / 呼叫路徑」取代反覆 grep + 讀檔。單一 static binary、158 種語言。
**適合誰**：在大型或不熟的 repo 上跑 coding agent、想快速定位又想省 token 的人。
**備註**：大改後要重新索引（graph 會 stale）；把它的回答當「快速第一手」、load-bearing 的結論（誰呼叫 X / 這段是不是死碼）再用實際程式碼驗證。

---

## 6. 資料庫

### [googleapis/mcp-toolbox](https://github.com/googleapis/mcp-toolbox) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 16k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐（**Google 官方**，多 DB） |

**教什麼**：跨 DB 的 MCP server——MySQL / PostgreSQL / Cloud SQL / Spanner / BigQuery 一次包。
**適合誰**：在 Google Cloud 上跑 DB 的工程師、要支援多 DB 引擎的開發者。
**備註**：開源 + Google 官方維護，是可上線使用的選擇。

### [bytebase/dbhub](https://github.com/bytebase/dbhub) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 3.2k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐（社群多 DB MCP） |

**教什麼**：zero-dependency、token-efficient 的多 DB MCP——Postgres、MySQL、SQL Server、MariaDB、SQLite。
**適合誰**：不想裝 Google Cloud SDK、要跨多種 OSS DB 的工程師。
**備註**：跟 googleapis/mcp-toolbox 重疊，但更輕量。

### [supabase/mcp](https://github.com/supabase/mcp) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 2.9k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐（**Supabase 官方社群**） |

**教什麼**：把 Supabase（含 Postgres、Auth、Storage、Edge Functions）接到 LLM。
**適合誰**：用 Supabase 跑後端的全端開發者。
**備註**：官方 community 維護。

### [timescale/pg-aiguide](https://github.com/timescale/pg-aiguide) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 1.8k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐（Postgres 寫程式輔助） |

**教什麼**：MCP server + Claude plugin，幫 LLM 生成更好的 PostgreSQL 程式碼。
**適合誰**：寫 Postgres heavy SQL / DBA 工程師。
**備註**：偏「LLM 寫 SQL 輔助」，不只是 query 執行。

### [benborla/mcp-server-mysql](https://github.com/benborla/mcp-server-mysql) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 2k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（read-only MySQL） |

**教什麼**：read-only MySQL MCP，讓 LLM 看 schema、跑 query。
**適合誰**：要讓 LLM 分析 production DB 但不能改的場景。
**備註**：故意 read-only 是 safety feature，不是限制。

### [mongodb-js/mongodb-mcp-server](https://github.com/mongodb-js/mongodb-mcp-server) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 1.1k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐（**MongoDB 官方**） |

**教什麼**：MongoDB 跟 MongoDB Atlas Cluster MCP server。
**適合誰**：用 MongoDB / Atlas 的工程師。
**備註**：mongodb-js 是 MongoDB 官方 GitHub org。

### [redis/mcp-redis](https://github.com/redis/mcp-redis) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 555 |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（**Redis 官方**） |

**教什麼**：Redis 官方 MCP，自然語言操作 Redis 跟 Redis Stack（Vector / Search / JSON）。
**適合誰**：用 Redis 當 cache / vector DB / queue 的人。
**備註**：官方維護；包含 vector search 整合。

### [awslabs/mcp](https://github.com/awslabs/mcp) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 9.3k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐（**AWS 官方**） |

**教什麼**：AWS 官方 MCP server（Lambda / S3 / DynamoDB / CloudWatch / Cost Explorer 等）。
**適合誰**：在 AWS 上、想讓 agent 查詢 / 操作雲端資源的團隊。
**備註**：AWS 官方維護；沿用你現有的 AWS 登入（CLI profile / IAM role），不用另外管 token。

---

## 7. 瀏覽器自動化 / 網頁抓取

### [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 35k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐（**Microsoft 官方**） |

**教什麼**：Playwright MCP server——讓 LLM 開瀏覽器、點按鈕、填表單、抓網頁。
**適合誰**：要做 E2E 自動化、跨網站整合、抓需要登入的網頁的人。
**備註**：Playwright 官方出，最 robust。**Claude Code 接 web 自動化的不錯選項**。

### [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 47k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐（**Chrome 官方**） |

**教什麼**：把 Chrome DevTools 接給 coding agent——performance、network、console 直接給 LLM 看。
**適合誰**：除錯前端 bug、做 web performance 分析的開發者。
**備註**：搭配 Playwright MCP 用最強——一個跑、一個觀察。

### [firecrawl/firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 7k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐（**Firecrawl 官方**） |

**教什麼**：Firecrawl 官方 MCP——大規模網頁抓取 + search + 結構化萃取。
**適合誰**：要抓大量網頁當訓練資料 / 做 RAG / 做研究的人。
**備註**：需要 Firecrawl API key（有 free tier）。

### [browserbase/mcp-server-browserbase](https://github.com/browserbase/mcp-server-browserbase) ⭐⭐⭐⭐（⚠️ 已封存）

| 欄位 | 內容 |
|---|---|
| Stars | ★ 3.3k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐（**Browserbase 官方**、⚠️ 已封存） |

**教什麼**：Browserbase 官方 MCP，配 Stagehand 跑 cloud-based 瀏覽器。
**適合誰**：本地跑瀏覽器太重 / 要在 cloud 平行跑多個 session 的人。
**備註**：商業服務（有免費額度），跟 Playwright MCP 互補（local vs cloud）。

---

## 8. 設計（Figma / Excalidraw）

### [GLips/Figma-Context-MCP](https://github.com/GLips/Figma-Context-MCP) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 15k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐（最熱門 Figma MCP） |

**教什麼**：把 Figma layout 資訊送給 coding agent——讀設計稿、提元件結構，給 Cursor / Claude Code 寫對應的 React component。
**適合誰**：前端開發者，要 LLM 從 Figma 設計稿生成 component code。
**備註**：要 Figma access token；對 design-to-code workflow 必裝。

### [excalidraw/excalidraw-mcp](https://github.com/excalidraw/excalidraw-mcp) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 5k+ |
| License | NOASSERTION |
| 推薦度 | ⭐⭐⭐⭐⭐（**Excalidraw 官方**） |

**教什麼**：streamable Excalidraw MCP，讓 LLM 直接畫架構圖、流程圖。
**適合誰**：寫設計文件 / 系統架構 / 流程圖的人——叫 Claude 從文字描述畫圖。
**備註**：Excalidraw 官方出，輸出可直接匯入 Excalidraw 編輯。

### [yctimlin/mcp_excalidraw](https://github.com/yctimlin/mcp_excalidraw) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 2.2k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（替代版 Excalidraw） |

**教什麼**：MCP server + Claude Code Skill，real-time canvas sync，可建立 / 編輯 / 匯出。
**適合誰**：需要 real-time canvas sync 跟程式化操作的人。
**備註**：跟官方版互補，社群維護。

### [pbakaus/impeccable](https://github.com/pbakaus/impeccable) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 57k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：「**讓你 AI harness 在 design 上更強的 design language**」——一套設計 vocabulary / pattern，幫 AI 在生成 UI / 視覺成品時跳出常見的「AI 感」生硬風格。
**適合誰**：用 AI 生 UI / mockup / visual design 但結果都很 generic 的開發者；前端 + AI workflow。
**備註**：不是 MCP server 也不是 Skill 包——是一份「**design language**」reference。讓 AI 看到比較高品質的設計詞彙才生得出比較好的東西。

---

## 9. 監控 / Observability

### [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 3.3k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐（**Grafana 官方**） |

**教什麼**：Grafana 官方 MCP，從 LLM 直接查 dashboard、metric、alert。
**適合誰**：用 Grafana 看 metric 的 SRE / DevOps。
**備註**：「dashboard 那條線為什麼掉？」直接問，LLM 撈 metric 給答案。

### [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 782 |
| License | NOASSERTION |
| 推薦度 | ⭐⭐⭐⭐（**Sentry 官方**） |

**教什麼**：從 LLM 查 Sentry error event、issue、trace。
**適合誰**：用 Sentry 接 production error 的工程師。
**備註**：「上週這個 error 的 stack trace 給我看」直接問 Claude Code。

### [winor30/mcp-server-datadog](https://github.com/winor30/mcp-server-datadog) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 142 |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐（社群版 Datadog） |

**教什麼**：Datadog API MCP——查 monitor、log、metric。
**適合誰**：用 Datadog 但 Datadog 還沒出官方 MCP 的人。
**備註**：等 Datadog 官方 MCP 出來可能換掉這個。

---

## 10. 媒體 / 串流（YouTube / Spotify）

### [varunneal/spotify-mcp](https://github.com/varunneal/spotify-mcp) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 599 |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：把 LLM 接到 Spotify——播歌、加歌單、查歷史。
**適合誰**：想用 Claude Code 控播放清單、做語音 / 文字 → 音樂的整合者。
**備註**：要 Spotify Premium 帳號（API 限制）。

### [kimtaeyoon83/mcp-server-youtube-transcript](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 581 |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（YouTube 字幕） |

**教什麼**：直接抓 YouTube 影片字幕給 LLM 摘要、翻譯、做 RAG。
**適合誰**：用影片當學習材料、要批次摘要 YouTube 內容的人。
**備註**：依賴 YouTube auto-caption；非英文影片字幕品質參差。

### [ZubeidHendricks/youtube-mcp-server](https://github.com/ZubeidHendricks/youtube-mcp-server) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 557 |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（YouTube 完整 API） |

**教什麼**：完整 YouTube API MCP——除了 transcript，還能管 video、Shorts、analytics。
**適合誰**：YouTube 創作者要自動化頻道管理。
**備註**：需要 YouTube Data API key + OAuth。

---

## 11. 中文圈專用

### [leemysw/feishu-docx](https://github.com/leemysw/feishu-docx) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 243 |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：飛書（Lark）docs / sheet / bitable ↔ Markdown 雙向轉換，含 OAuth 2.0、CLI、TUI、Claude Skills。
**適合誰**：用飛書 / Lark 寫文件的中文使用者，要把 Lark 內容跟 Claude Code 串起來。
**備註**：目前中文圈 MCP / Skill 主要選擇之一；微信 / 釘釘暫時沒有獨立 MCP（多半混在 chat bot framework 裡）。

### [netease-youdao/LobsterAI](https://github.com/netease-youdao/LobsterAI) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 5.6k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：網易有道出品的「24/7 全場景 AI agent」——支援工作流自動化、跨應用協作、檔案處理。中文 native。
**適合誰**：中文圈使用者要找一個替代 Claude Code / OpenAI Operator 等級的 all-in-one agent；對中國大陸服務（網易、釘釘等）整合需求高的場景。
**備註**：產品式 agent（不是 Skill / MCP）；跟 Claude Code / Codex 互為替代，不是搭配。

### [QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 16k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：阿里巴巴官方 Qwen agent framework——RAG、tool use、code interpreter、multi-agent、MCP 相容，預設搭配 Qwen 系列模型但可換其他 LLM。
**適合誰**：用 Qwen / 通義千問 為主 LLM 的開發者；想要中文 native 的 agent framework（範例、文件都中文齊全）。
**備註**：MCP 相容是亮點——可以直接接到 Claude Code 等 host；維護節奏正常（last commit 2026-03）。

### [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 21k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：字節跳動 Coze 的開源版——no-code agent builder（workflow / plugin / knowledge / memory），可自部署或上雲。
**適合誰**：不想寫 code 但要做 agent 的團隊；想看 enterprise agent platform 內部設計（RAG、工作流、Memory、Plugin 系統的 reference 實作）。
**備註**：底層 framework 是 Coze 自家的 Eino；可接 OpenAI / Claude / Qwen / 國產 LLM。國際版（coze.com）跟中國版（coze.cn）共用此 codebase。

### [coze-dev/coze-loop](https://github.com/coze-dev/coze-loop) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 5.6k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：Coze 出的 agent observability + evaluation 平台——trace、debug、eval、prompt management，agent dev lifecycle 的下半場。
**適合誰**：agent 已經跑起來、要 production 監控的團隊；想看「agent eval / observability」可以怎麼做的人。
**備註**：跟 LangSmith / Arize Phoenix 同類；開源版可自部署。

### [liaokongVFX/LangChain-Chinese-Getting-Started-Guide](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 8.9k+ |
| License | 未標註 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：LangChain 中文入門指南——從 LangChain 基礎、Prompt、Memory、Agent、Chains 到實作應用，最早期且最完整的中文 LangChain 學習資源。
**適合誰**：想用 LangChain 但英文文件吃不下去的中文使用者；想理解 LangChain 設計脈絡再決定要不要走這條路的人。
**備註**：沒有正式 license（內容開放閱讀）；LangChain 框架本身演進很快，書中部分 API 可能跟最新版有出入。

### [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 37k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：基於 LangChain 的開源知識庫問答系統——本地化部署、支援多種向量資料庫、RAG 端到端範例。
**適合誰**：想做 RAG 又不想全部自己刻的中文團隊；要本地部署（不能用雲端 LLM）的場景。
**備註**：★ 37k 是中文圈最熱門的 RAG 實作之一；維護節奏放緩（last commit 2025-11）。新專案建議先 fork 後評估，當參考實作用。

### [usewhale/whale](https://github.com/usewhale/whale) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 967 |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：專為 DeepSeek 模型優化的終端 AI 編碼助手——支援 MCP server 接入、Claude-style Skills、對話快取優化，Go 實作。
**適合誰**：以 DeepSeek 為主力 LLM 的中文開發者；想用終端工具但不需要 Claude Code 全家桶的人。
**備註**：開源同類中少見的 DeepSeek 專屬優化；MCP + Skills 雙支援讓它可以逐步擴充能力。

### [simonlin1212/a-stock-data](https://github.com/simonlin1212/a-stock-data) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 9.2k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：A 股全棧資料工具包——單一 SKILL.md 檔案封裝 8 個資料源（mootdx、東財、akshare、iwencai 等）21 個端點，AI 編碼助手直接可用。
**適合誰**：用 Claude Code / Codex / OpenClaw 做投研或量化分析的中文開發者；不想自己刻資料抓取邏輯的人。
**備註**：一條 `curl` + `pip install` 即可啟用；中國 A 股資料類 Skill 中星星數最高的社群實作。相容 Claude Code、Codex、OpenClaw。

> 想找微信 / 釘釘整合？目前主流是用 chat bot framework（如 zhayujie/CowAgent）而不是純 MCP server。等正規 MCP 出現再加進來。

### [MoonshotAI/Kimi-K2](https://github.com/MoonshotAI/Kimi-K2) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 10.7k+ |
| License | Modified MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：月之暗面 Moonshot 的 Kimi K2 開源大模型系列——開源權重 + OpenAI / Anthropic 相容 API，主打 agentic / coding / 長程任務，可當 agent stack 的後端模型。
**適合誰**：想用國產開源模型跑 agent / coding 工作流、或要在自架環境跑開源權重的中文開發者。
**備註**：License 是 Modified MIT（標準 MIT + 大規模商用附加條款）——商用前先讀原始 LICENSE；weights 另在 Hugging Face。

### [zai-org/GLM-4.5](https://github.com/zai-org/GLM-4.5) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 4.3k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：智譜 Zhipu（Z.ai）的 GLM-4.5 開源模型——定位 Agentic / Reasoning / Coding（ARC）基礎模型，開源權重 + API，可當 agent / tool use / coding 的後端。
**適合誰**：想評估國產開源 agentic 模型、或需要 Apache-2.0 寬鬆授權權重的中文開發者。
**備註**：zai-org 是智譜開源 org；同系列另有 GLM-4（★ 7k+）可一起參考；weights 在 Hugging Face。

---

## 12. 其他常用（Cloudflare / Stripe…）

### [cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 4k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐（**Cloudflare 官方**） |

**教什麼**：Cloudflare 官方 MCP——Workers、Pages、R2、KV、D1、DNS、Zero Trust 全包。
**適合誰**：用 Cloudflare 跑 edge / serverless 的人。
**備註**：官方維護；最佳的 edge platform MCP。

### [stripe/ai](https://github.com/stripe/ai) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 1.7k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（**Stripe 官方**） |

**教什麼**：Stripe 官方 AI agent toolkit，含 MCP server，操作付款、訂閱、退款、客戶。
**適合誰**：要在 agent 內處理付款 / billing 的開發者。
**備註**：⚠️ 涉及金流，務必用 sandbox 測試夠了再接 production。


### YIELD INTELLIGENCE MCP（Hosted Remote Server）

| 欄位 | 內容 |
|---|---|
| 形式 | hosted MCP server |
| 推薦度 | ⭐⭐⭐（Finance 分析工具；了解 hosted vs self-hosted MCP 實作差異的實例） |

**教什麼**：YIELD INTELLIGENCE hosted remote MCP server——即時美國國債殖利率 + 股息 ETF / REIT / 特別股分析 + 被動收入投資組合優化。2 個工具：`analyze_yield_opportunities`（掃描被動收入機會）+ `optimize_income_portfolio`（目標月收入建立投資組合）。已列入官方 MCP Registry（`io.github.thebrierfox/intuitek-ace`，since 2026-05-10）。
**適合誰**：用 Claude Code / Claude Desktop 做個人理財分析、想讓 AI 找出被動收入機會的人。hosted remote MCP server 範例——直接 plug URL、0 安裝、適合 Stage 5 學完 MCP 概念後拿來實驗 hosted vs self-hosted 差異。
**備註**：Live endpoint `https://api.intuitek.ai/yield/mcp`（no auth、no API key）。x402 micropayment $1 USDC/call on Base（agent-to-agent 場景）；一般使用者免費。非交易型，純分析工具。GitHub：[thebrierfox/intuitek-ace](https://github.com/thebrierfox/intuitek-ace)（MIT License）。

### [ComposioHQ/composio](https://github.com/ComposioHQ/composio) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 28.8k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐（1000+ 工具整合樞紐） |

**教什麼**：一個平台（SDK + MCP server），把 agent 連到 1000+ 應用（Slack / GitHub / Gmail / Salesforce / Notion…），登入它幫你處理，不用一個服務各寫一個連接器。
**適合誰**：agent 要跨大量工具、但不想維護幾十個獨立 MCP server 的團隊。
**備註**：提供 MCP server + Python / TypeScript SDK；可透過 MCP 接到 Claude Code。屬「工具聚合器」（跟 n8n / Zapier 自動化平台同類）。

---

### [morluto/jacobian](https://github.com/morluto/jacobian) ⭐⭐⭐（⚠️ 作者本人投稿）

| 欄位 | 內容 |
|---|---|
| Stars | ★ 58 |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：用一個可直接安裝的數學 MCP server，練習讓 agent 呼叫可組合的精確計算工具；涵蓋 polynomial maps、linear algebra 與 graph algorithms。
**適合誰**：想在 MCP 工作流中加入數學計算、或需要讓 agent 處理結構化數學問題的研究者與開發者。
**備註**：Python 專案，但透過 npm 發佈啟動器，所以用 `npx` 起 server。同時提供 MCP server、CLI 與 Python library；可從一個簡單的本地 MCP 設定開始，再按需使用原生 Python API。
**怎麼跑**：
```bash
npx -y jacobian mcp
```

---

## 13. 研究工作流 Skills（學術 / paper / 文獻）

> ⚠️ **maintainer 自家專案區**：以下幾個是本 repo 維護者 [@WenyuChiou](https://github.com/WenyuChiou)（Lehigh CEE PhD candidate）日常在用的研究 skills，公開出來給其他研究者參考。**因為是自己的東西、又是相對 niche 的研究場景，star 數字會比泛用工具低**。star 門檻在這節是放寬的——選收的標準是「在我自己研究流程裡實際有用」。請自己評估是否合用。

### [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 222 |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐（研究流程一整套） |

**教什麼**：14 個 Claude Code skills 涵蓋常見研究任務——文獻分流、研究設計、project context、論文撰寫、multi-AI delegation。打包成 5-plugin marketplace，一個指令安裝。
**適合誰**：研究生 / 博後想一次取得「研究全流程」skill set。
**備註**：marketplace 形式，跟 Stage 5.4 教的 plugin/marketplace 概念對位。

### [WenyuChiou/academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 17 |
| License | MIT |
| 推薦度 | ⭐⭐⭐（窄但深） |

**教什麼**：嚴謹學術論文寫作 / 修改 / 投稿的 Claude Code skill。Field-agnostic，可用 per-paper journal_format.md 跟 style_overrides.md 客製規則。
**適合誰**：在寫 / 改 paper 的研究者，想把 banned-word audit、figure-text coupling、submission checklist 自動化。
**備註**：是 ai-research-skills 5 plugin 中的一個，也可獨立安裝。

### [WenyuChiou/zotero-skills](https://github.com/WenyuChiou/zotero-skills) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 50 |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：Zotero CLI skill——程式化搜尋 / 加 / 分類 / 標記文獻。
**適合誰**：用 Zotero 管文獻、想讓 Claude Code 直接整理 library 的研究者。
**備註**：跟 [`MuiseDestiny/zotero-gpt`](https://github.com/MuiseDestiny/zotero-gpt) 的差別——後者是 Zotero plugin（在 Zotero 裡 chat），這份是 CLI / Skill（從 Claude Code 操作 Zotero）。

### [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 52 |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：AI-operable research workspace，整合 Zotero + Obsidian + NotebookLM 三個工具，提供 CLI / MCP / REST / dashboard 四種介面。
**適合誰**：同時用 Zotero / Obsidian / NotebookLM 的研究者，想把它們綁成一個 workspace 給 LLM 操作。
**備註**：跟單一工具的 MCP（mcp-obsidian、notion-mcp 等）互補——這份是 hub，可整合多個工具。

---

## 14. Multi-LLM Delegation Skills

> ⚠️ **maintainer 自家專案區**：跟 13 一樣，以下是維護者把自己 daily workflow 抽出來公開的 delegation skills。star 門檻放寬，選收標準是「真的能讓 Claude planner + Codex/Gemini 執行者組合穩定跑下去」。Multi-LLM 領域變化快，建議跟其他 multi-agent framework（Stage 7 列的）一起評估後再選。

<!-- not-an-entry -->
### 三個 skill 的組合（composition）

底下 3 個 skill 是**設計成一起用**的，不是獨立工具：

![Claude + 3 delegate skill 分工](../resources/diagrams/multi-llm-delegation-composition.png)

Claude 不擅長 token-heavy 機械式工作（成本高、context 容易爆）；Codex 不擅長對話協作；Gemini 1M context 但中型推理稍弱。**分工 = Claude 負責 design / review、Codex 負責 implement、Gemini 負責 long-form draft / synthesis**。

### [WenyuChiou/codex-delegate](https://github.com/WenyuChiou/codex-delegate) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 62 |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：Claude Code skill 把 Codex CLI 當 execution specialist——大量檔案 refactor、batch edits、boilerplate 生成、wrapper-based 實作密集任務。Claude 寫 plan + review，Codex 執行。
**適合誰**：要省 token / 提速大規模機械式編輯的開發者；想驗證「multi-agent 不只是 buzzword」的學習者。
**何時用**：refactor 30+ files、生成 test scaffold、port 同樣 pattern 到 N 個檔案、寫 migration script。
**何時不用**：架構決策、bug 診斷、security review、需要 conversation memory 的任務——這些 Claude 直接做更好。
**備註**：跟 `gemini-delegate-skill` 互補。Stage 7 multi-agent 的實戰版。

### [WenyuChiou/gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill) ⭐⭐⭐（⚠️ 已封存 2026-07）

| 欄位 | 內容 |
|---|---|
| Stars | ★ 37 |
| License | MIT |
| 推薦度 | ⭐⭐⭐（⚠️ 已封存） |

**教什麼**：Claude Code skill 把 Gemini CLI 當 long-form / large-context / CJK 執行者——百萬 token context window、中文長文 draft、second-opinion review。Claude 出大綱跟 critique，Gemini 寫長文。
**適合誰**：研究者寫 paper、知識工作者寫中文報告 / Threads post、需要第二 LLM 意見對照的人。
**何時用**：長文 draft（>3000 字）、跨多份長文件 synthesis（要塞進 1M token 的 context）、中文 / CJK 內容、要 LLM-vs-LLM 對比視角。
**何時不用**：短查詢、code generation（用 codex）、production-critical 決策（最終人類 review）。
**備註**：跟 `codex-delegate` 是「Codex 寫 code、Gemini 寫 prose」的分工。

### [WenyuChiou/agent-collab-skills](https://github.com/WenyuChiou/agent-collab-skills) ⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 22 |
| License | MIT |
| 推薦度 | ⭐⭐（experimental，當 reference 看就好） |

**教什麼**：Claude Code marketplace for multi-agent collaboration——task splitter、output reconciler、adversarial debate、shared memory、acceptance gate。跟 codex-delegate / gemini-delegate 組合用。
**適合誰**：要跑 2+ delegate agent 在同一輪、想看 multi-agent coordination 怎麼包成 marketplace 的人。
**備註**：experimental——別把它當生產級 framework，當作維護者把自己 setup 公開的 reference 看就好。要可上線部署的請看 Stage 7 的 LangGraph / Microsoft Agent Framework / CrewAI。

---

## 15. 金融 / 交易 Agents

> ⚠️ **應用領域區**：agent 在量化交易 / hedge fund 模擬 / 自動下單的應用。本節兩個 entry 分別是 Apache-2.0 與 MIT，但這類 repo 授權狀態普遍混雜，使用前仍請自行查清楚。**警示**：trading agent 跑真實資金有顯著風險，本目錄列入是為了學習 agent 設計模式、不是投資建議。

### [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 97k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：多 agent LLM 框架做金融交易決策，bull / bear / fundamentals / technicals / risk 各 agent 分工。
**適合誰**：想看 multi-agent 在分析性任務怎麼分工的學習者；量化研究者想實驗 LLM 增強既有 pipeline。
**備註**：Apache-2.0、允許修改與商用（保留授權聲明）；**非投資建議，別直接拿來下實單**。

### [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) ⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 62k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：多角色 AI hedge fund 模擬，bull / bear / 基本面 / 技術面 / 風控 agent 協作產生 trade recommendation。
**適合誰**：看過 Stage 7 multi-agent 想要一個完整應用案例的學習者；對 agent + 金融交叉領域有興趣的人。
**備註**：MIT 授權；**模擬性質、非投資建議**。

---

## 16. 網頁搜尋 / 檢索（Web Search / Retrieval）

### [exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 4.8k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（**Exa 官方**） |

**教什麼**：Exa 官方 MCP，專為 LLM / agent 設計的網頁搜尋（neural + keyword），回傳乾淨結果直接餵進 prompt。
**適合誰**：要做 research / fact-check / 線上 RAG 檢索的人；semantic search 對「概念相關」特別強，純關鍵字搜尋反而沒那麼吃香。
**備註**：需要 Exa API key。

### [tavily-ai/tavily-mcp](https://github.com/tavily-ai/tavily-mcp) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 2.3k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（新手第一選擇） |

**教什麼**：把 Tavily search API 包成 MCP——專為 LLM / RAG 打造的網頁搜尋，回傳 answer + sources，free tier 容易上手。
**適合誰**：只是想讓 agent 會上網查資料的新手，這是最好的起手選擇。
**備註**：需要 Tavily API key（有好上手的 free tier）。

---

## 17. 資安 / MCP 安全治理

### [trailofbits/skills](https://github.com/trailofbits/skills) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 6.6k+ |
| License | CC-BY-SA-4.0 |
| 推薦度 | ⭐⭐⭐⭐⭐（**Trail of Bits 官方**） |

**教什麼**：資安公司 Trail of Bits 官方的 Claude Code plugin marketplace，收的是他們自己在用的資安分析、測試與漏洞研究 skills。
**適合誰**：想讓 agent 幫忙做 code audit、漏洞分析、安全測試的人；也適合想看「專業資安團隊怎麼把方法論寫成 skill」的人。
**備註**：用 `/plugin marketplace add trailofbits/skills` 安裝，Codex 也直接支援同一套 marketplace。授權是 **CC-BY-SA-4.0**（share-alike），改作後要用相同授權釋出，商用整合前先確認。注意它跟 Stage 5 那張表裡的 [`trailofbits/skills-curated`](https://github.com/trailofbits/skills-curated) 是**兩個不同的 repo**：後者是由 Trail of Bits 審核、內容來自社群貢獻的策展 marketplace，這一個是 Trail of Bits 自家的資安 skills。

### [stacklok/toolhive](https://github.com/stacklok/toolhive) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 2k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：把每一個 MCP server 跑在隔離容器裡，用最小權限檔取代本機憑證，並提供 audit log 與可設定的身分／存取政策；另附 Kubernetes operator。
**適合誰**：團隊裡已經有人各自裝了一堆 MCP server，開始需要回答「誰裝了什麼、它拿得到哪些憑證」的人。
**備註**：Go 專案，桌面版與 CLI 都有。開源的 ToolHive 與 Stacklok 的企業版是分開的，評估功能時注意分界在哪。

### [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 8.3k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐（**NVIDIA 官方**） |

**教什麼**：給自動化 agent 用的沙箱化執行環境，用宣告式政策管住檔案、網路與行程；Claude Code 與 Codex 不改任何程式碼就能跑在裡面（OpenClaw 要另外透過下面那則 NemoClaw）。
**適合誰**：要讓 agent 真的能執行指令、但不想把整台機器交出去的人。
**備註**：Rust 專案。需要 Docker / Podman 或主機虛擬化（MicroVM sandbox 用）；Windows 走 WSL 2 且標為 experimental。**⚠️ 專案自述仍是 alpha**（最新 release 還在 `v0.0.x`），拿來讀與試可以，正式倚賴前先自行評估。與 `toolhive` 的分工是：toolhive 管的是 MCP server，這個管的是 agent 本身的執行邊界。

### [nolabs-ai/nono](https://github.com/nolabs-ai/nono) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 3.7k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：用作業系統自己的隔離機制（Linux Landlock、macOS Seatbelt）擋住 agent，不需要 daemon 也不需要容器。
**適合誰**：想要沙箱但不想為此裝一整套 container runtime 的人。
**備註**：Rust 專案，由做 Sigstore 的團隊維護。零容器是它跟 OpenShell 最大的取捨差異：啟動快、但隔離強度受限於作業系統提供的機制。

## 還有什麼沒收錄？

如果你需要的整合不在上面，先看這些 catalog：

- [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) — 社群最完整 MCP server 清單，150+ 個按分類整理
- [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) — 另一份 MCP server 清單，跟上面互補
- [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) — 官方 reference servers（現有 7 個：everything、fetch、filesystem、git、memory、sequentialthinking、time；github、sqlite 已移到 `servers-archived`）
- [`travisvn/awesome-claude-skills`](https://github.com/travisvn/awesome-claude-skills) — Claude Skills 清單

### 要加新的？

1. 開 issue，附 repo 連結 + 為什麼要加 + 屬於哪個分類
2. 或直接送 PR：在對應分類下加一個 entry，按上面的格式寫（Stars/License/推薦度 + 教什麼/適合誰/備註）
3. **stars < 100 且非官方**通常會被退；除非你能說明 niche use case 強到可以例外

PR 送出前看一下 [`resources/style-guide.md`](style-guide.md) 跟 [`CONTRIBUTING.md`](../CONTRIBUTING.md)。

---

## 維護備註（給未來想幫忙的人）

不是 SLA，是「能做就做」的方向：

- Stars / license 用 `gh api repos/<owner>/<repo>` 抓，**有空 review 一輪就好**——不用排定期程
- 連結壞了、repo archived → 看到再修
- 新分類（AR/VR、IoT 等）有 1-2 個值得收的就可以先開
- 「中文圈專用」分類維持寬鬆，中文社群 repo star 數累積較慢
- 用詞、格式不一致 → 不要苛求，PR 進來能讀懂優先

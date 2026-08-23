# Stage 5 — Claude Code 生態系（Claude Code Ecosystem）⭐⭐

> **繁體中文** | [简体中文](./05-claude-code-ecosystem.zh-Hans.md) | [English](./05-claude-code-ecosystem.en.md)

⏱ **時間估算**：3-4 週（約 15-25 小時）

> 🚪 **進入條件**（共用 hub、依 track 不同）：**Track A（CLI Power User）** 從 A1-A2 過來、會用 Python + 跑過基本 CLI 即可、從 5.1/5.2 起步；**Track B（Agent Builder）** 建議先完成 [Stage 3](03-tool-use-and-hello-agent.md)（tool use）+ [Stage 4](04-agent-frameworks.md)（agent frameworks）再進、把整個 stage 當「Claude Code 內部怎麼運作」深讀。不確定走哪條 → 看下面 📌 的兩軌說明。

> 💡 整個 stage 圍繞 4 個關鍵詞（**MCP / Skills / Plugins / Marketplace**）展開 → 不熟先翻 [`resources/glossary.md` 5](../resources/glossary.md#5-claude-code-生態)。

**👥 共用 hub**：本 stage 是 Track A（CLI Power User）+ Track B（Agent Builder）兩條路徑的共用中心。Stage 5 跟 [Stage 8 — Agent Interfaces](08-agent-interfaces.md) 是 curriculum 的兩個 hub。

> 📌 **這個 stage 兩條軌都用**：
> - **Track A（CLI Power User）**：A2 用 [5.1（Claude Code 基礎）](#51--claude-code-基礎)；A3 用 [5.2（MCP）](#52--mcpmodel-context-protocol-基礎) + 選擇性用到 [5.3（Skills）](#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層) 跟 [5.4（Plugins）](#54--plugins-與-marketplaces)（A3 的 動手練習 CLI-12 會教把 CLAUDE.md 跟 commands 打包成 plugin）。讀的角度是「**怎麼用 Claude Code 把工作做好**」
> - **Track B（Agent Builder）**：把整個 stage 當「**Claude Code 內部怎麼運作**」的深度學習，從 5.1 完整走到 5.4

> 🗺️ **Claude Code 屬於哪種 agent 型態**？→ [`resources/agent-paradigms.md`](../resources/agent-paradigms.md) Type 1（IDE-coupled）+ Type 2（Terminal pair-programmer）；想看完整 5 種 paradigm 對照也從這份開始。

> 🧭 **Claude Code 只是 agent 的其中一種型態**（往下讀前先有個全局感）：Claude Code 是給**工程師**的**終端機** agent——活在命令列、處理程式碼。Anthropic 另外還有 **Claude Cowork**：給**非工程師**（研究、分析、營運）的**桌面 app**——給它一個目標、它會跨你的檔案跟應用程式把事情做完、交回成品。OpenAI 這兩種型態也都有。Stage 5 接下來專講 Claude Code，這張表只是讓你知道它在整張地圖的位置。

| 型態 | 它幫你做什麼 | Anthropic | OpenAI |
|---|---|---|---|
| **終端機 · 給工程師** | 讀 / 改 / 跑你的程式碼 | Claude Code | Codex CLI |
| **App · 給所有人** | 跨你的檔案、應用程式、網頁把一件事做完 | Claude Cowork | ChatGPT agent |

> ⚠️ **想用本機 LLM？這個 stage 不是那條路線。** Claude Code 需要 Anthropic API / OAuth，不能直接改接 Ollama 或本機 endpoint。離線、隱私資料或不想用 API 額度時，請看 [`resources/cookbook.md` Recipe 6](../resources/cookbook.md#6-本機-llm--cli-agent-快速-walkthrough)，用 OpenCode / goose / Aider / Hermes 這類支援 BYO LLM 的 CLI agent。

> 📋 **本章組成**：7 個子章（5.1 基礎 / 5.2 MCP / 5.3 Skills / 5.4 Plugins / 5.5 Subagents / 5.6 Dynamic Workflows / 5.7 Claude Code Source 解剖），每個子章都有「學習目標 → 必修閱讀 → 動手練習 → 精選 Projects」 → 章末 自我檢查。**注意**：Harness Engineering（白話：model 外面的「運行外殼」——怎麼給它工具、記憶、權限，怎麼跑每一輪）的**學科級概念**在 [Stage 7](07-multi-agent-production.md) 系統整理；本章 5.7 則把 Claude Code 當成案例，觀察一個成熟 agent 工具如何處理工具、記憶、設定、權限與執行流程
> 🔑 **關鍵名詞**：見 [`resources/glossary.md` 5](../resources/glossary.md#5-claude-code-生態)

## Stack 一覽

由上往下，每一層都建立在底下那一層上：

![Claude Code Ecosystem Stack](../resources/diagrams/stage5-stack.png)

每一層各自加上一種能力：

- **API + SDK**：用程式存取 LLM
- **Tool Use**：讓 LLM 呼叫你定義的 function
- **MCP**：標準化協定，讓任何 LLM host 都能使用任何 tool server
- **Skills**：Claude Code 的行為包，可以封裝 MCP tool
- **Plugins**：把 Skills、hooks、commands、MCP 設定打包成一個單位發佈

這個階段有 4 個子章節，**請按順序做**——每一節都建立在前一節之上。

```
5.1 Claude Code 基礎 3-5 天 （安裝、slash commands、CLAUDE.md）
5.2 MCP — 協定層 5-7 天 （寫你的第一個 MCP server）
5.3 Skills — 行為層 5-7 天 （寫你的第一個 SKILL.md）
5.4 Plugins 與 Marketplaces 5-7 天 （打包並發佈）
```

跑完這個階段，你會能擴充 Claude Code、寫自己的 MCP server、發佈一個 plugin marketplace。

---

## 🗺 7-Layer Architecture Map（先看這張圖、再讀 5.1-5.7）

> 📋 **這節是什麼**：把 Claude Code 的 7 個 primitive（MCP / Skills / Plugins / Subagents / Hooks / Slash commands / CLI）對應到 **7 個架構層 + 3 個工程學 discipline**——進 5.1-5.7 之前看一次知道接下來在學什麼層、學完回頭看是 synthesis。**分層是教學選擇、不是 absolute 真理**。

![Claude Code 7-Layer Architecture Map](../resources/diagrams/claude-architecture-map.png)

> 📊 **上圖**：Claude Code 7 個架構層 + 3 個工程學 discipline 整合視圖。

### 每層 1 句白話 + Claude 的版本

| Layer | 是什麼 | Claude 的版本 | 誰管 | 學在 |
|---|---|---|---|---|
| **L7 Interface** | 使用者跟 agent 交談入口 | claude-code CLI / Desktop | Harness Eng | [Stage 5.1](#51--claude-code-基礎) |
| **L6 Workflow** | 固定可重用流程模板 | **Skills**（SKILL.md）+ Slash commands + **Plugins**（打包 Skills / hooks / commands、屬 packaging）| Prompt Eng | [Stage 5.3](#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層) / [5.4](#54--plugins-與-marketplaces) |
| **L5 Coordination** | 多 agent 分工合作 | **Subagents** + Agent team + Background | Harness Eng | [Stage 5.5](#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能) |
| **L4 Memory / Context** | 跨對話 / 跨 session 記事情 | History / `/compact` / Memory hooks | Context Eng | [Stage 6](06-memory-rag.md) |
| **L3 Control Plane**（「守門員」層） | tool 執行前 / 後攔截 / validation / 阻擋 | **Hooks**（PreToolUse / PostToolUse 等）| Harness Eng | [Stage 5.1 hooks 段](#51--claude-code-基礎) |
| **L2 Tool Use** | LLM 呼叫外部 function 的 protocol | Anthropic Tool Use（`input_schema`）| Tool design | [Stage 3](03-tool-use-and-hello-agent.md) |
| **L2.5 Tool Provider** | 把外部 API 包成 tool 給 Layer 2 用 | **MCP servers**（Notion / Gmail / Slack）| Context Eng + Tool | [Stage 5.2](#52--mcpmodel-context-protocol-基礎) |
| **L1 Foundation** | LLM 本體（system prompt 直接送達這層）| Anthropic API | Prompt Eng | [Stage 1](01-llm-basics.md) + [Stage 2](02-prompt-engineering.md) |

### 3 工程學 Discipline overlay（核心 insight）

「Prompt / Context / Harness」是**不同層的 discipline**——學會其中一個不會自動會另一個：

| Discipline | 負責哪些 layer | 1 句話 | 學在 |
|---|---|---|---|
| **Prompt Engineering** | L1 + L6 | 「送進 LLM 的字串怎麼設計」 | [Stage 2](02-prompt-engineering.md) |
| **Context Engineering** | L4 + L2.5 | 「context window 裝什麼資訊」 | [Stage 6](06-memory-rag.md) |
| **Harness Engineering** | L3 + L5 + L7 | 「LLM 外面的『運行外殼』——給它工具、記憶、控制流程的那層設置」 | [Stage 7 §Harness Engineering](07-multi-agent-production.md#-harness-engineering--production-agent-runtime-的工程設計--本-stage-核心概念) |

> 💡 **MCP 的特殊位置**：MCP 嚴格說是 **Context Engineering**（feed context source）+ **Tool design**（協議規範）跨層東西、不純歸任一 discipline——所以圖裡用 Layer 2.5 標明。

### 跨 CLI vendor mini-comparison（2026-05 snapshot）

Claude Code 的 **7-layer stack 最完整**；Codex CLI / Gemini CLI 在 2026 已補上 subagents + hooks，其餘各層仍以 Claude Code 最齊：

| Layer | Claude Code | OpenAI Codex | Gemini CLI |
|---|---|---|---|
| L5 Coordination（multi-agent）| ✅ Subagents | ✅ Subagents | ✅ Subagents |
| L3 Control Plane（hooks）| ✅ Hooks | ✅ Hooks | ✅ Hooks |
| L2.5 Tool Provider（MCP）| ✅ | ✅（已支援 MCP）| ✅（需手動裝 MCP server）|
| L6 Workflow（Skills）| ✅ SKILL.md | AGENTS.md（context only）| GEMINI.md（context only）|

→ 細看 [`resources/cli-agents-guide.md`](../resources/cli-agents-guide.md)

---

## 5.1 — Claude Code 基礎

### Claude Code 是什麼（先定位）

**Claude Code = 跑在你 terminal 內的 Claude agent**——有完整 file system / shell / git / subprocess access、可以**自主完成多步驟工作**（讀檔 → 改檔 → 跑 test → commit → 發 PR）。

跟其他 Claude 介面差別：

| 介面 | 跑哪 | 能做什麼 | 用法 |
|---|---|---|---|
| **claude.ai**（web） | 瀏覽器 | 純對話 + 上傳檔案、無 file system 操作 | 偶爾聊一下、ask 一個問題 |
| **Claude API**（programmatic） | 你的 server / script | LLM call、自己包 agent loop | 寫 production system |
| **Claude Agent SDK** | 你的 Python / TS 環境 | 完整 agent runtime + tool use + 多 session | 寫 production agent system |
| **Claude Code**（**本節**） | 你的 terminal | **完整 OS-level agent**（file / shell / git / subprocess）+ skill / plugin / subagent 生態 | **日常工作主力工具** |

進 5.2-5.7 之前你會在這節學到 **4 個 Claude Code 核心結構**：CLAUDE.md（記憶層）/ slash commands（控制層）/ `~/.claude/` 目錄（設定層）/ settings.json（行為層）。

### 學習目標

完成本節後你會：

- 講得出 Claude Code 跟 claude.ai / API / SDK 各自的角色（**「為什麼用 CLI 不用 web」**）
- 安裝 Claude Code、配置認證、跑第一個有 file access 的 session
- 用 8-10 個常用 slash command 控制 Claude Code 行為
- 寫一份 project-level `CLAUDE.md` 設定 baseline 行為
- 認得 `~/.claude/` 目錄結構（skills / agents / plugins / settings.json 各放哪）

### 必修閱讀
1. [**Anthropic — Claude Code Quickstart**](https://code.claude.com/docs/en/quickstart) — 官方安裝指南
2. [**Anthropic — CLAUDE.md best practices**](https://code.claude.com/docs/en/memory) — 怎麼寫專案 memory
3. [**Anthropic — Slash Commands**](https://code.claude.com/docs/en/slash-commands) — 官方完整 slash command 列表
4. [**Anthropic — Settings**](https://code.claude.com/docs/en/settings) — `settings.json` 完整 schema + env var
5. [**KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh**](https://github.com/KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh) — 簡中入門指南

> 🛠️ **要寫好 CLAUDE.md？** 先看 [Stage 7.5 核心 Harness Engineering 原則（多 source）](07.5-advanced-agentic-concepts.md#-跨概念-harness-engineering-原則多-source-整理) 建概念、再用下面 2 個 prompt 動手。

### 📋 CLAUDE.md 設計 prompts（依 5 原則）

寫 / 改 CLAUDE.md 時直接複製貼上：

#### Prompt 1 — Audit 你現有的 CLAUDE.md

```
我有一個 CLAUDE.md（在 [貼路徑]），請依下面 5 個 harness engineering 原則 audit：

1. Legibility — 用 markdown header 分區嗎？conventions 寫具體（"2-space indent"）還是模糊（"format properly"）？
2. Progressive Disclosure — < 200 行嗎？有用 `@-import` 或 `.claude/rules/<topic>.md` 拆分嗎？
3. System of Record — CLAUDE.md 是否當 entry map、實際內容指向 `docs/` + `.coord/`？還是把所有規則塞同一檔？
4. Taste Invariants — 規則可驗證嗎（"run `make lint` before commit"）？還是「follow best practices」這種空話？
5. Transparency — 有要求 agent show planning step 嗎？還是預期它默默做完？

每條給 PASS / FAIL / PARTIAL + 原因 + 改進建議。總分 X/5、最該先修哪條。
```

#### Prompt 2 — 生成新的 CLAUDE.md（依 5 原則）

```
我要為一個 [描述專案，例如：Python data analysis monorepo / 學術論文 repo / Next.js app] 寫 CLAUDE.md。請依下面 5 個 harness engineering 原則生成：

- **< 200 行**
- 當 **entry map**，把實際 conventions 用 `@-import` 引外部 docs 或 `.claude/rules/<topic>.md`
- 每條規則**可驗證**（不要「follow best practices」這種空話）
- 加 **1-2 個 transparency rule**（例如「edit > 50 lines 前先 show plan」）
- 標明哪些內容該放 CLAUDE.md、哪些該分到 `.claude/rules/<topic>.md`

輸出：
1. 完整 CLAUDE.md 內容
2. 建議的 `.claude/rules/` 目錄切法（topic 列表）
3. 1 個示範 `.claude/rules/<topic>.md`（任選一個 topic）
```

→ **建議流程**：寫 CLAUDE.md 前用 Prompt 2 生成、寫完用 Prompt 1 audit。

### 常用 slash commands（10 個必學）

| Command | 用途 | 何時用 |
|---|---|---|
| `/help` | 列出所有可用 command | 不知道有什麼指令時 |
| `/clear` | 清空對話歷史（保留 system context） | session 太長、想重啟邏輯 |
| `/compact` | 自動摘要對話、釋放 context window | context 接近用滿 |
| `/plan` | 進入 plan mode（read-only、先規劃才動手） | 大改動前先讓 Claude 列計畫 |
| `/model` | 切換 model（Sonnet / Haiku / Opus）| 改成更便宜 model 省 token |
| `/agents` | 列 / 管理 subagent（5.5）| 看哪些 subagent 可用、debug |
| `/plugin install <name>@<marketplace>` | 安裝 plugin（5.4）| 加新功能 |
| `/permissions` | 看 / 改當前 session 權限 | 太多 permission prompt 想精簡 |
| `/resume` | 恢復前次 session | 接續昨天工作 |
| `/bg` | 把當前 session 背景化（移到 agent view）| 想同時跑多任務、見 5.5 |

完整列表見上方 [Slash Commands 官方文件](https://code.claude.com/docs/en/slash-commands)。

### `~/.claude/` 目錄結構（先有 mental map）

```
~/.claude/ ← 全域 user-level
├── settings.json ← 全域行為（env / hooks / permissions / model 預設）
├── settings.local.json ← 機器特定（不入 git）
├── CLAUDE.md ← 全域 baseline（每個 session 都載入）
├── skills/<name>/SKILL.md ← user-level skills（5.3）
├── agents/<name>.md ← user-level subagents（5.5）
├── plugins/ ← 已安裝的 plugin（5.4）
├── hooks/ ← user-level hook scripts
└── jobs/<id>/ ← background sessions 狀態（5.5 background agent）

<project-root>/.claude/ ← project-level（隨 repo）
├── settings.local.json ← project 行為（含 permissions）
├── skills/<name>/SKILL.md ← project-level skills（優先級高於 user-level）
├── agents/<name>.md ← project-level subagents
├── commands/<name>.md ← project-level slash command
└── hooks/ ← project-level hook

<project-root>/CLAUDE.md ← project baseline（每個 session 都載入）
```

**優先順序**（衝突時誰贏）：project > user > built-in default。

### 動手練習
- **練習 1：第一個 session** — 安裝、認證、`cd` 到 repo、跑 `claude` → 問「summarize this codebase」→ 觀察怎麼讀檔
- **練習 2：CLAUDE.md** — 寫 repo 根目錄 CLAUDE.md（role / context / 不能做的事 / 怎麼做事 / 常用指令），對照「沒 CLAUDE.md」跟「有 CLAUDE.md」的行為差別
- **練習 3：5 個 slash commands** — 在一個 session 內依序用 `/help` `/plan` `/compact` `/model` `/agents`，觀察各自做什麼
- **練習 4：目錄探索** — `ls ~/.claude/` + `cat ~/.claude/settings.json`、看自己 user-level 設定長什麼樣

### 精選 Projects

| Project | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|
| [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐ 官方 | ⭐⭐⭐⭐⭐ | 追蹤新版本 / 看 release notes / 回報 bug | Claude Code 官方 repo、issues + releases + inline 範例 |
| [Anthropic — Claude Code 官方文件](https://code.claude.com/docs/en/overview) | ⭐⭐⭐⭐⭐ | 任何 reference 查詢 | **真正的 canonical reference**——上面 5 條必修閱讀都從這裡來 |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | ⭐⭐⭐⭐ | 想看社群有什麼（slash commands / skills / hooks 範例）| 較廣泛的資源清單（目前正在重整）|
| [KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh](https://github.com/KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh) | ⭐⭐⭐⭐ | 中文讀者要逐步教學 | 簡中入門導讀 |

### Hooks（L3 控制層）⭐ 把規則寫成程式、自動攔截

MCP / Skills 是「給 agent 更多能力」；**Hooks 則是反過來：在 agent 的生命週期事件上掛你自己的 script，做檢查、攔截、注入**。這是 Claude Code 的控制層（架構圖的 L3）。

**怎麼運作**：在 `settings.json` 的 `hooks` 設定「某事件發生時跑哪個 command」。常用事件（2026 已擴到 ~28 個，先記核心幾個）：

| 事件 | 觸發時機 | 典型用途 |
|---|---|---|
| `PreToolUse` | 工具呼叫前 | 擋危險指令、權限 gate |
| `PostToolUse` | 工具呼叫後 | 自動 format / lint / 跑測試 |
| `UserPromptSubmit` | 你送出 prompt 時 | 注入 context、擋掉某些輸入 |
| `Stop` / `SubagentStop` | （子）agent 想停時 | 強制它繼續、或做收尾檢查 |
| `SessionStart` / `SessionEnd` | session 開始 / 結束 | 載入狀態、寫 log |
| `PreCompact` | context 壓縮前 | 保護重要內容 |

**關鍵語意**：hook **回傳 exit code 2 = 阻擋**：Claude 會把 stderr 當錯誤訊息讀回去（例如 `PreToolUse` 回 2 就擋下那個工具呼叫、`UserPromptSubmit` 回 2 就擋下 prompt）。這就是「用程式強制規則」的機制。

> ⚠️ **安全**：hook 是在你機器上跑的 shell command，別亂裝別人的 hook，也別在 hook 裡跑未經檢查的輸入。
>
> 完整事件清單 + JSON 進階用法見官方文件：[Claude Code Hooks](https://code.claude.com/docs/en/hooks)。

---

## 5.2 — MCP（Model Context Protocol）⭐ 基礎

### MCP 是什麼（先定位）

**MCP = 「**讓 LLM 用任何外部工具 / 資料**」的開放協定**。在 MCP 之前每個 LLM 廠商都得自己定義 tool 規格、每個工具供應商都得為每個 LLM 寫一份接法。MCP 把這層**標準化**——寫一次 MCP server、Claude / Codex / Cursor / 任何支援 MCP 的 host 都能用。

> 📈 **規模參考**（Anthropic 2026-07 [官方數字](https://claude.com/blog/bringing-mcp-2026-07-28-to-claude)）：MCP 的 SDK 月下載量已超過 **4 億**（今年約成長 4 倍），Claude 的 connectors 目錄收錄 **950+ 個 MCP server**。

> 🔄 **2026-07-28 那版把 MCP 改成無狀態（stateless），是目前為止最大的一次改動**：拿掉 `initialize` 握手與 `Mcp-Session-Id`，每個請求自己帶協定版本與能力宣告；server 要跨呼叫記東西，改用自己發的 handle 當普通 tool 參數傳。新增 `server/discover`，client 可以先問「你支援哪些版本」。**Roots / Sampling / Logging 三個功能與舊的 HTTP+SSE transport 都標成 deprecated**，server 主動發請求的做法由 MRTR 取代（server 回一個 `input_required`、client 補齊資訊後重送原請求）。**為什麼你該在意**：2025 年寫的 MCP 教學幾乎都在講那個握手流程，照著做會對不上現在的規格。deprecated 不等於今天就不能用，官方保證至少 12 個月過渡期，但新寫的東西不該再用它們。

> 🧩 **核心之外還有 extension（選讀）**：2026-07-28 那版規格把「核心協定」跟「[extension](https://modelcontextprotocol.io/extensions/overview)」正式分開。官方 extension 目前有 [Tasks](https://modelcontextprotocol.io/extensions/tasks/overview)（長時間任務的非同步執行、可輪詢）、[Apps](https://modelcontextprotocol.io/extensions/apps/overview)（在對話裡直接顯示圖表 / 表單等互動 UI）跟 Skills over MCP。**初學階段不用學這些**——你寫 `@app.tool()` 打不到它們。真正該記住的只有一條**不會過期**的規則：**extension 一律預設關閉、要雙方明確支援才生效**，所以看到教學叫你用某個 extension，先確認你的 client 有支援，否則會靜默退回核心行為。官方 extension 用 `io.modelcontextprotocol/` 前綴、放在 MCP 組織下 `ext-` 開頭的 repo；`experimental-ext-` 開頭的則還在孵化、隨時可能改。

**MCP 三個抽象**：

| 抽象 | 是什麼 | 範例 |
|---|---|---|
| **Tools** | LLM 可以呼叫的 function | `read_file(path)` / `query_db(sql)` / `send_slack(channel, msg)` |
| **Resources** | LLM 可以讀的資料源 | `file:///path/file.md` / `postgres://db/users` |
| **Prompts** | server 預定義的 prompt 樣板 | 一份「review code」的 prompt template |

**多數 MCP server 主要用 Tools 抽象**——Resources 跟 Prompts 用得少。

**MCP vs Tool Use vs Skill vs Plugin**：

- **Tool Use**（Stage 3）：你 in-process 寫的 function 給 LLM 呼叫
- **MCP**（**本節**）：把 tool 標準化成 server / client 協定、跨 host / 跨 LLM 可用
- **Skill**（5.3）：行為層 — 教 Claude「**遇到 X 用哪個 MCP tool**」
- **Plugin**（5.4）：把 MCP + Skill + 其他打包散佈

→ **核心區分**：MCP 是「**能力**」（讓 LLM 能做什麼）、Skill 是「**行為**」（什麼時候用什麼能力）。

### 學習目標
- 解釋 MCP 的三個抽象（Tools、Resources、Prompts）
- 把現成的 MCP server 接上 Claude Desktop 或 Claude Code
- 用 Python 寫一個最小的 MCP server，提供 1-2 個 tool
- 區分 MCP server vs Tool Use vs Skills vs Plugins

### 必修閱讀
1. [**Anthropic — Introducing MCP**](https://www.anthropic.com/news/model-context-protocol) — 最初發表，概念總覽
2. [**MCP Specification**](https://modelcontextprotocol.io/specification) — 實際的協定規格。MCP 規格用日期版號（`YYYY-MM-DD`）發佈修訂版、目前是 **2026-07-28**，所以讀任何 MCP 文件前先確認自己看的是哪一版
3. [**Complete Guide to MCP in 2026**](https://dev.to/x4nent/complete-guide-to-mcp-model-context-protocol-in-2026-architecture-implementation-and-4a11) — 實作導讀
4. [**Microsoft — MCP for Beginners**](https://github.com/microsoft/mcp-for-beginners) — 官方循序漸進 MCP 學習課綱（概念、裝設、動手 lab；免費、GitHub 上）。★ 16k+

### 動手練習
- **練習：MCP client** — 安裝 `modelcontextprotocol/servers/filesystem`，從 Claude Desktop 連上去。看著 Claude 讀你的檔案。
- **練習：MCP server** — 寫一個 Python MCP server，提供一個 tool（例如「換算溫度」）。從 Claude Code 連過去。**step-by-step 怎麼做** → [`resources/cookbook.md` 2](../resources/cookbook.md#2-寫你的第一個-mcp-server)
- **練習：MCP in production** — 在同一個 Claude session 裡同時連 2-3 個 MCP server，看它們互相搭配。

### 精選 Projects（spec / SDK / 範本參考）

> 💡 **找日常工具的 MCP（Notion / Obsidian / Excel / Postgres / Playwright / Figma 等）？**
> 看 [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)——按 16 個分類整理 79+ 個常用 MCP server / Skill，每個都附 stars / license / 適合誰。下表保留的是「**寫自己 MCP server 時的 reference**」性質的官方 server / SDK。

| Project | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) ⭐ 官方 | ⭐⭐⭐⭐⭐ | 練習 1 接 server、之後當參考 | 7 個官方 reference MCP server（everything / fetch / filesystem / git / memory / sequentialthinking / time；github 跟 sqlite 已移到 `servers-archived`），★ 89k+、授權轉換中（新程式碼 Apache-2.0、文件 CC-BY-4.0、未同意轉授權的舊貢獻仍為 MIT）、TS+Python。官方 README 講明這些是 **reference implementation、不是 production-ready**——要實際部署的 server 去官方 Registry 找（目前仍是 preview）。**讀 `everything` 跟 `filesystem` source 理解協定運作**。安裝：`npx -y @modelcontextprotocol/server-filesystem /path` 或 `pip install mcp-server-fetch` |
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | ⭐⭐⭐⭐⭐ | 練習 2 寫自己 MCP server | 官方 Python SDK、`pip install "mcp>=2,<3"`（**一定要鎖版本**：v2.0.0 於 2026-07-28 是破壞性改版）、MIT。跟著官方 quickstart 跑 |
| [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk) | ⭐⭐⭐⭐ | 喜歡 TS 的人 | Python SDK 的 TypeScript 版、MIT |
| [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) ⭐ 目錄 | ⭐⭐⭐⭐⭐ | 自己寫前先找有沒有現成的 | 150+ 社群 MCP server 目錄，按 search / code / cloud / communication / finance 分類。投稿走 mcpservers.org |
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | ⭐⭐⭐⭐ | 跟 wong2 交叉比對 | 另一份 MCP server 目錄、組織方式不同、通常更新更即時 |
| [github/github-mcp-server](https://github.com/github/github-mcp-server) | ⭐⭐⭐⭐ | 想看實際上線的 MCP server source | GitHub 官方維護、真正 production 在跑的範例 |
| [21st-dev/magic-mcp](https://github.com/21st-dev/magic-mcp) | ⭐⭐⭐ | 做完練習 2 找靈感 | 會生成 UI 元件的非平凡 MCP server、★ 5.6k+、NOASSERTION。**看 MCP 不只能做資料抓取** |
| [yamadashy/repomix](https://github.com/yamadashy/repomix) | ⭐⭐⭐⭐⭐ | 把整個 codebase 餵給 LLM | ★ 27k+ MIT、把 repo packed 成 AI-friendly 單一檔案、含 MCP server mode + tree-sitter 壓縮（省 70% token）+ secretlint 過濾密鑰。**daily-driver 工具，搭 Claude Code / Codex 用** |

> 🔭 **MCP 在 2026：從「知道是什麼」到「會用生態」**：(1) **官方 Registry**（registry.modelcontextprotocol.io、**仍在 preview**）——發現 / 發佈 MCP server 的中央目錄；(2) **FastMCP**（[PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp)、★27k、Apache-2.0）——用 `@mcp.tool` 幾行寫出 server，比 low-level SDK 省事（注意：這是**獨立的第三方套件**，跟官方 SDK 內部那個在 v2 改名為 `MCPServer` 的 class 不是同一個東西）；(3) ⚠️ **MCP 安全**：tool 回傳的內容是**不可信輸入**（tool poisoning、confused-deputy），別把沒檢查過的第三方 server 接上有權限的 agent。

---

## 5.3 — Skills（Claude Code 的行為層）⭐ Claude Code 生態最關鍵的一層

### Skill 是什麼（先定位）

Skill = **一個 markdown 檔**（`.claude/skills/<name>/SKILL.md`），告訴 Claude「**遇到某情境 → 走某流程**」。Claude 每次 inference 前掃所有可用 skill 的 `description` frontmatter（檔案開頭那段 YAML metadata）、看是否匹配當前情境、**匹配就把 SKILL.md 自動載入 context**。

> 🛠️ **要寫好 SKILL.md？** 兩條路：
> - **路 A：用 Anthropic 官方 `skill-creator` skill 自動產生**（5.3.x 之後安裝段落會教），它會自動產 frontmatter + 子目錄結構、是 Anthropic 維護的 canonical 工具。
> - **路 B：用下面 SKILL.md 設計 prompts 自己寫**——先看 [Stage 7.5 核心 Harness Engineering 原則](07.5-advanced-agentic-concepts.md#-跨概念-harness-engineering-原則多-source-整理) 建概念、再用 prompt 動手。
>
> 兩條不衝突：`skill-creator` 給結構、5 原則 prompt 給內容品質檢查。

### 📋 SKILL.md 設計 prompts（含 `skill-creator` 替代）

寫 / 改 SKILL.md 時直接複製貼上：

#### Prompt 1 — Audit 你現有的 SKILL.md

```
我有一個 SKILL.md（在 [貼路徑]），請依下面 5 個 harness engineering 原則做 audit。每條給「PASS / FAIL / PARTIAL」+ 1 行原因 + 1 行改進建議：

1. Legibility — description 寫清楚「何時觸發」嗎？tool param 命名一致嗎？
2. Progressive Disclosure — SKILL.md < 200 行嗎？細節是否放 `references/` 而不是塞主檔？
3. System of Record — `references/` 是 single source、主檔不重複嗎？
4. Taste Invariants — success criteria 是否寫死可驗證、不是「盡量好」這種主觀詞？
5. Throughput / Merge — 有附 acceptance check（lint / test / preset YAML）嗎？

最後給：總分 X/5、最該先修哪一條、為什麼。
```

#### Prompt 2 — 生成新的 SKILL.md（依 5 原則）

```
我要寫一個 skill 處理 [描述任務，例如：把 PDF 轉成 markdown / 跑學術論文 banned-word audit]。請依下面 5 個 harness engineering 原則生成 SKILL.md：

- **description** 寫清楚「何時觸發」（讓 Claude 能 match 對情境）
- **主檔 < 200 行**，所有 examples / edge cases / detailed rules 放 `references/<topic>.md`
- 列出建議的 `references/` 結構（1-3 個 topic 檔案）
- 加一個 **success criteria 表**（可驗證、不主觀）
- 加一段 **acceptance check**：要跑哪些 lint / unit test / preset YAML

輸出：
1. 完整 SKILL.md 內容
2. references/ 目錄結構建議
3. 用哪個 acceptance gate preset 驗證它（如 multi-locale-mirror-sync / catalog-entry-add 之一）
```

→ **建議流程**：先 `/skill skill-creator` 拿乾淨骨架 → 用 Prompt 2 填內容 → 寫完用 Prompt 1 audit。

**核心 mental model**：你發現自己「**每次都要打同樣的 prompt 教 Claude 怎麼做某件事**」→ 把它寫成 skill、下次就不用了。Claude Code 生態裡 **skill 是 power user 跟一般使用者的分水嶺**——熟練 skill 寫作的人能把 1 個小時的工作壓到 5 分鐘。

### Skill vs CLAUDE.md vs MCP vs Plugin vs Subagent — 一張表分清楚

各層常被搞混。**一行對照**：

| 元件 | 是什麼 | 何時用 | 觸發方式 | 範例 |
|---|---|---|---|---|
| **CLAUDE.md**（5.1） | repo / project 的 baseline 行為 | repo-wide convention（「用 type hint」、「commit 訊息規範」）| **每個 session 都載入**、不分情境 | 你 repo 根目錄的 CLAUDE.md |
| **MCP server**（5.2） | 提供 tool / data 的 protocol server | 想讓 Claude 能存取**外部資源**（API / DB / 檔案系統） | server 啟動後、任何時候都能呼叫 | `github` MCP / `postgres` MCP |
| **Skill**（**本節**） | **特定情境的行為包** | 想設定「**遇到 X 情境 → 走 Y 流程**」 | **description 匹配自動載入** | `skill-vetter`（裝 skill 前檢查）/ `pdf`（處理 PDF） |
| **Plugin**（5.4） | 把 skills + commands + MCP + hooks 打包散佈 | 想 share / install **一整套** 設定 | `/plugin install <name>@<marketplace>` | `engineering` bundle / `finance` bundle |
| **Subagent**（5.5） | 獨立 context 的 sub-Claude session | 想 delegate **大 context 任務**、結果回主 session | description 匹配自動 delegate | code-reviewer subagent / 研究員 subagent |

**怎麼選**：

- 一句話設定 → 寫進 `CLAUDE.md`
- 多步驟流程、某情境才用 → 寫 **Skill**（本節主題）
- 需要存取外部資源（API / DB） → 寫 **MCP server**
- Skill 跑起來太大、會吃光主 session window → 改成 **Subagent**
- Skill / command / MCP / hook 想打包送人 → 包成 **Plugin**

→ **核心區分**：MCP 是「**能力**」、Skill 是「**行為**」、Plugin 是「**散佈**」、Subagent 是「**獨立 worker**」。

### 學習目標
- `SKILL.md` 的結構（YAML frontmatter + 本文）
- skill 何時會自動載入（description 比對）
- 怎麼寫一份能解決你日常工作的 SKILL.md
- `references/`、`scripts/`、`evals/` 子目錄的用途

### 必修閱讀
1. [**Anthropic — Claude Skills 文件**](https://code.claude.com/docs/en/skills)
2. **幾份範例 SKILL.md**——從 `anthropics/claude-code` 或社群 marketplace 拿
3. [**Hello-Agents — Extra08 如何寫出好的 Skill**](https://github.com/datawhalechina/hello-agents/blob/main/Extra-Chapter/Extra08-如何写出好的Skill.md) — 中文最完整的 Skill 最佳實踐
4. [**Hello-Agents — Extra05 Agent Skills 與 MCP 對比解讀**](https://github.com/datawhalechina/hello-agents/blob/main/Extra-Chapter/Extra05-AgentSkills解读.md) — Skills vs MCP 概念對比

### 動手練習
- **練習：SKILL.md** — 寫一份 200 字的 skill，解決你日常工作中的某一件事。**step-by-step 怎麼做** → [`resources/cookbook.md` 1](../resources/cookbook.md#1-寫你的第一個-skill)
- **練習：SKILL with references** — 加一份 `references/` markdown 讓 skill 可以引用
- **練習：SKILL eval** — 加 `evals/evals.json`，放 3-5 個自我測試

> 📦 **本 repo 自帶 meta-example**：[`examples/stage-5/tool-calling-tutor/`](../examples/stage-5/tool-calling-tutor/) 是這個 stage 的對應 skill 範本——完整 frontmatter（含 trigger phrases + Do NOT use for）、3 份 `references/`、`evals/evals.json` 5 個 test case，**直接 fork 改成你自己的 skill**。雙重用途：(a) 學習者自用、卡在 tool calling 時讓它 auto-load 幫你 debug；(b) Stage 5 5.3 SKILL.md 寫法的對照樣板。

### 常用 Skills 推薦（按用途分類）

> 不知道從哪裡開始？下面是 2025 後段官方 + 社群常用 skill。**安裝方式**：(a) 多數來自 plugin、安裝對應 plugin 即得；(b) 或從 [anthropics/skills](https://github.com/anthropics/skills) clone 後放進 `~/.claude/skills/` 或 `.claude/skills/`。

| 用途 | Skill | 來源 | 為什麼推薦 |
|---|---|---|---|
| **🛡 裝 skill 前安全檢查**（必裝） | `skill-vetter` | anthropics/skills | **裝任何外部 skill 前必跑**——檢查紅旗、permission scope、suspicious pattern。等於 marketplace skill 的 SAST |
| **🔍 找 / 安裝 skill** | `find-skills` | anthropics/skills | 自然語言查詢、自動安裝。「我想要做 X」就回對應 skill |
| | `skill-lookup` | claude-plugins-official | 跟 find-skills 互補，探索 / 搜尋 helper |
| **✍ 寫自己的 skill** | `skill-creator` | anthropics/skills + claude-plugins-official | 自動產生 frontmatter + 子目錄結構、寫 skill 必裝 |
| **📄 Office docs 處理** | `pdf` / `docx` / `xlsx` / `pptx` | anthropics/skills | 讀寫 PDF / Word / Excel / PowerPoint。**必裝 set**——任何 office workflow 必備 |
| **🔧 Code review** | `code-reviewer` / `code-review-excellence` | claude-plugins-official | staged diff 安全 / 風格 / 測試 review |
| **🐛 Debug** | `debugger` / `systematic-debugging` | claude-plugins-official | 系統化 root cause 分析、避免 quick fix |
| **🔐 安全稽核** | `security-audit` | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | Cloudflare 官方開源：六階段管線（偵察 → 漏洞搜獵 → 對抗式驗證 → 報告 → 結構化輸出 → 獨立複驗）派多個平行 agent 找真正可利用的漏洞，是 Cloudflare 自家漏洞挖掘 harness 的起點。`npx skills add` 安裝（MIT） |
| **🎓 學術寫作** | `academic-writing-skills` | community | findings-first / mechanism / banned word audit |
| **🔌 MCP 整合 / 寫 server** | `mcp-builder` / `mcp-integration` | claude-plugins-official | 寫 MCP server 跟整合既有 server 的腳手架 |
| **💻 frontend / fullstack** | `frontend-developer` / `fullstack-developer` | claude-plugins-official | React 元件 / 全棧架構輔助 |
| **📊 資料分析** | `data-analyst` / `visualization-expert` | community | SQL / pandas / chart 選型 |
| **⚙ 權限 / 設定整理** | `update-config` / `fewer-permission-prompts` | claude-plugins-official | hooks / permissions / env var 管理 |
| **🔁 自我改進** | `self-improving-agent` | community | 捕捉 learning / error / correction、agent 持續改進 |
| **🚀 從想法到上線 agent** | `launch-your-agent` | [anthropics/launch-your-agent](https://github.com/anthropics/launch-your-agent) | Anthropic 官方教學 skill：訪談你要做什麼 → 界定 v0 → 在你自己的帳號上線一個 Claude Managed Agent → 用你自己的完成標準評分、迭代 → 會重複跑的就排程。⚠️ 自述 reference implementation、不維護也不收 PR（Apache-2.0） |
| **🌐 通用 / fallback** | `general-purpose` | Claude Code 內建 | 複雜開放任務、未涵蓋情境的 default 入口 |

**建議入手順序**：

1. **第一個必裝**：`skill-vetter`（裝其他 skill 前先用它檢查）
2. **第二批必裝**：`skill-creator` + `find-skills`（寫 / 找 skill 用）
3. **依工作領域**：Office workflow 加 `pdf`/`docx`/`xlsx`、開發加 `code-reviewer`/`debugger`、學術寫作加 `academic-writing-skills`
4. **想看更多**：逛 `obra/superpowers` 或 `wshobson/agents` 看 production 範本

### 精選 Projects（spec / 範本參考）

> 💡 **找日常用 Skill（NotebookLM、Excalidraw、Office docs 等）？**
> 看 [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)——按使用情境分類，含 Anthropic 官方 + 社群 Skill。下表保留的是「**寫自己 Skill 時的 spec / showcase reference**」性質。

| Project | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) ⭐ 官方 spec | ⭐⭐⭐⭐⭐ | 寫自己 SKILL.md 前先讀 | Anthropic 官方 Skills repo：`spec/`（frontmatter 標準）+ `template/` 起手範本 + `skills/` 含 pdf / docx / xlsx / pptx / skill-creator / skill-vetter 等 reference 實作。★ 165k+。**SKILL.md 結構範本參考**。Agent Skills 更廣義標準另見 [agentskills.io](https://agentskills.io) |
| [anthropics/claude-code](https://github.com/anthropics/claude-code) | ⭐⭐⭐⭐ | 追蹤新功能、看 release notes | Claude Code 主 repo、含 issues / releases / inline skill 範例。本 stage 學 Skill 重點看上一個 repo、這個排第二 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | ⭐⭐⭐⭐ | 想看「真實工程師日常 SKILL.md」 | Matt Pocock（TypeScript 社群知名教學者）公開自己工作真實在用的 `.claude/` 目錄。每個 SKILL.md **10-50 行極短**、不過度工程化。**對照 over-engineered 200 行 skill 特別有參考價值**（★ 212k+、MIT）|
| [obra/superpowers](https://github.com/obra/superpowers) | ⭐⭐⭐⭐ | power user setup、學進階寫法 | 20+ 實戰 skill（TDD、debugging、合作模式）+ `/brainstorm` / `/write-plan` / `/execute-plan` 命令 + skills-search tool |
| [wshobson/agents](https://github.com/wshobson/agents) | ⭐⭐⭐⭐ | 中階：學 skill + subagent 組合 | 把 skills + subagents 組合做 multi-agent 編排。**從單一 SKILL.md 進化到 agent-as-skill 組合 pattern** 的範例（★ 38k+、MIT） |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | ⭐⭐⭐⭐ | 自己寫前先找有沒有現成的 | 社群 Claude Skills 精選目錄 |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | ⭐⭐⭐ | 跨工具視角 | 1000+ agent skill、相容 Claude Code / Codex / Gemini CLI / Cursor（★ 29k+、MIT）|
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | ⭐⭐⭐ | 找特定領域 skill 範例 | 232+ Claude Code skill、跨 engineering / marketing / product / compliance |

---

## 5.4 — Plugins 與 Marketplaces

### Plugin 是什麼（先定位）

**Plugin = MCP + Skills + slash commands + hooks 的組合包**——把前面 5.2 / 5.3 學到的零件 **打包成一個單位、可以 `/plugin install` 一次裝進去**。

```
Plugin
├── .mcp.json ← 5.2 學的 MCP server config（提供 tool / data）
├── skills/<name>/SKILL.md ← 5.3 學的 skill（行為包）
├── commands/<name>.md ← slash command（5.1 學的、自訂 prompt 入口）
├── hooks/ ← 觸發點 hook（譬如 PreToolUse、SessionStart）
├── agents/<name>.md ← 5.5 學的 subagent（如果有）
└── .claude-plugin/plugin.json ← 打包元資料
```

**為什麼要 plugin**：你寫了好用的 skill 想 share → 一行 `git clone` 太麻煩、設定也容易裝錯。包成 plugin、push 到 marketplace、team 其他人 `/plugin install foo@your-marketplace` 一次到位。

**Plugin 跟 marketplace 差在哪**：plugin 是**單一打包單位**、marketplace 是**多個 plugin 的目錄**（譬如 anthropics/claude-plugins-official 是 marketplace、裡面 35 個 plugin）。

### 學習目標
- `plugin.json` schema（name、version、skills array、configuration）
- `marketplace.json` schema（plugins array、source、metadata）
- `claude plugin marketplace add` 的流程
- 區分 single-plugin bundle vs multi-plugin marketplace
- 發佈自己的 marketplace

### 必修閱讀
1. [**Anthropic — Plugins 文件**](https://code.claude.com/docs/en/plugins)
2. **讀下面 2-3 個 marketplace 的 `plugin.json` 與 `marketplace.json`**

### 動手練習
- **練習：plugin install** — 安裝下面的某一個 marketplace，看它載入
- **練習：plugin.json** — 把 5.3 寫的 SKILL.md 打包成一個 plugin
- **練習：marketplace publish** — push 到 GitHub，用 `claude plugin marketplace add` 安裝

### 常用 plugin 推薦（按用途分類）

> 不知道從哪裡開始裝 plugin？下面是 2025 後段 Anthropic 官方 + 社群高評價選擇。**安裝指令統一格式**：`/plugin install <plugin-name>@<marketplace-name>`（譬如 `/plugin install code-review@claude-plugins-official`）。

| 用途分類 | Plugin（含直接連結） | Marketplace | 為什麼推薦 |
|---|---|---|---|
| **開發 workflow**<br>（多數開發者必裝） | [`code-review`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-review) | claude-plugins-official | 官方 code review skill 集合、staged diff review + security check |
| | [`pr-review-toolkit`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pr-review-toolkit) | claude-plugins-official | PR review 完整流程（comment、suggest、approve）|
| | [`commit-commands`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands) | claude-plugins-official | git commit message 規範 + branching workflow |
| | [`feature-dev`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/feature-dev) | claude-plugins-official | 完整 feature 開發 cycle（spec → plan → implement → test） |
| | [`frontend-design`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design) | claude-plugins-official | UI 設計 + responsive layout 輔助 |
| **語言工具**<br>（依用的語言挑）| [`typescript-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/typescript-lsp) / [`pyright-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pyright-lsp) / [`rust-analyzer-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/rust-analyzer-lsp) / [`gopls-lsp`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/gopls-lsp) 等 | claude-plugins-official | 各語言 LSP 整合、[35 個語言 plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins) 都在這 |
| **plugin / skill 自建** | [`skill-creator`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) | claude-plugins-official | 寫自己的 skill 時自動產生 frontmatter + 結構 |
| | [`plugin-dev`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/plugin-dev) | claude-plugins-official | 寫自己的 plugin 時自動產生 `.claude-plugin/` 結構 |
| | [`mcp-server-dev`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/mcp-server-dev) | claude-plugins-official | 寫自己的 MCP server 時的腳手架 |
| | [`hookify`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/hookify) | claude-plugins-official | 寫 hooks 規則的工具 |
| **領域特化 — 工程團隊** | [**`engineering` bundle**](https://github.com/anthropics/knowledge-work-plugins/tree/main/engineering) | knowledge-work-plugins | **10 個 skill**：architecture / code-review / debug / deploy-checklist / documentation / incident-response / standup / system-design / tech-debt / testing-strategy |
| **領域特化 — 財務團隊** | [**`finance` bundle**](https://github.com/anthropics/knowledge-work-plugins/tree/main/finance) | knowledge-work-plugins | **8 個 skill**：audit-support / close-management / financial-statements / journal-entry-prep / reconciliation / sox-testing / variance-analysis |
| **領域特化 — 其他**<br>（同 marketplace）| [`sales`](https://github.com/anthropics/knowledge-work-plugins/tree/main/sales) / [`marketing`](https://github.com/anthropics/knowledge-work-plugins/tree/main/marketing) / [`legal`](https://github.com/anthropics/knowledge-work-plugins/tree/main/legal) / [`human-resources`](https://github.com/anthropics/knowledge-work-plugins/tree/main/human-resources) / [`customer-support`](https://github.com/anthropics/knowledge-work-plugins/tree/main/customer-support) / [`data`](https://github.com/anthropics/knowledge-work-plugins/tree/main/data) / [`design`](https://github.com/anthropics/knowledge-work-plugins/tree/main/design) / [`operations`](https://github.com/anthropics/knowledge-work-plugins/tree/main/operations) / [`product-management`](https://github.com/anthropics/knowledge-work-plugins/tree/main/product-management) / [`productivity`](https://github.com/anthropics/knowledge-work-plugins/tree/main/productivity) / [`bio-research`](https://github.com/anthropics/knowledge-work-plugins/tree/main/bio-research) 等 | knowledge-work-plugins | knowledge-work-plugins **[18 個 vertical bundle](https://github.com/anthropics/knowledge-work-plugins)**——挑跟你工作領域對應的那個 |
| **外部整合**<br>（第三方服務） | [`asana`](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/asana) / [`github`](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/github) / [`gitlab`](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/gitlab) / [`linear`](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/linear) / [`firebase`](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/firebase) / [`playwright`](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/playwright) / [`terraform`](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/terraform) / [`discord`](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/discord) / [`imessage`](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/imessage) / [`telegram`](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/telegram) 等 | claude-plugins-official (external) | 整合常用 SaaS / 開發工具 |
| **community 廣度** | （挑感興趣的 skill） | [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) | 社群最大 agents / skills / hooks / templates 目錄 |

**建議入手順序**：

1. 開發者必裝（5 個）：`code-review` + `pr-review-toolkit` + `commit-commands` + `feature-dev` + 一個你語言的 `*-lsp`
2. 按工作領域加 bundle：工程團隊裝 `engineering`、財務裝 `finance`、其他類似
3. 想寫自己的 skill / plugin → 裝 `skill-creator` + `plugin-dev`
4. 想看更多 → 逛 `awesome-claude-code-toolkit` 或 [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)

### 精選 Projects（marketplace 範本參考）

> 💡 上面列的是「**裝哪些 plugin**」；下表列的是「**marketplace 怎麼寫**」——想自建 marketplace 的人才需要看。

| Marketplace | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | ⭐⭐⭐⭐⭐ | 寫自己的 marketplace 前的官方範本 | 35 internal plugins + 15 external、`.claude-plugin/marketplace.json` 標準 schema、`plugins/` 含 plugin 本體 + `external_plugins/` 引用外部 repo。**marketplace.json 該長什麼樣直接看這個**（★ 32k+） |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | ⭐⭐⭐⭐⭐ | 想看「多 vertical bundle」型 marketplace | **18 個領域 plugin bundle**（finance / engineering / sales / legal / marketing / HR / customer-support / data / design / operations / product / productivity / bio-research / enterprise-search / pdf-viewer / small-business / cowork-plugin-management / partner-built）。Anthropic 自家 knowledge worker 場景範本 |
| [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) | ⭐⭐⭐⭐ | 想做「我策展、別人寫」型 marketplace | **最簡 marketplace template**——repo 只有 `marketplace.json` + README、plugin 本體放外部 repo。curator-only pattern 最小範本（★ 1.2k+、MIT）|
| [trailofbits/skills-curated](https://github.com/trailofbits/skills-curated) | ⭐⭐⭐ | 在意供應鏈安全的 reviewer / 團隊 | Trail of Bits 維護的 **security-vetted** marketplace、每個 skill 都經審查、README 寫清楚標準。**示範 marketplace 不只是清單、也是信任機制**（★ 475、CC-BY-SA-4.0）|
| [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) | ⭐⭐⭐ | 想逛社群有什麼 | 社群最大 Claude Code agents / skills / hooks / templates 目錄。涵蓋 use case 廣 |
| [anthropics/life-sciences](https://github.com/anthropics/life-sciences) | ⭐⭐⭐ | 要做特定領域 marketplace（醫療、金融、法律、教育等） | Anthropic 自家**領域特化 marketplace** 範例（生物 / 健康科學）、展示 `marketplace.json` 為單一 vertical 量身設計。**payload 偏生科 MCP server、marketplace.json 結構才是學習重點**（★ 562）|
| [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal) | ⭐⭐⭐⭐ | 想看完整 vertical plugin suite（含 skills + agents + MCP + scheduled agents）| **Anthropic 官方法律 vertical 範例**（★ 8.7k+ Apache-2.0）—— 10 個法律 plugin（commercial / corporate / litigation / privacy / employment / IP / law-student）+ 100+ skills + 20+ MCP connectors + scheduled agents + subagent delegation。**不必懂法律**——是學「**vertical plugin suite 怎麼設計**」的最佳教材：系統 prompt 怎麼寫、accountability surface 怎麼擺、`orchestrate.py` event loop 怎麼跑 |

> 💡 **「如何發佈自己的 marketplace」walkthrough**：目前最可靠的是 [Anthropic 官方 plugin 文件](https://code.claude.com/docs/en/plugins)。社群有好的部落格 / repo？歡迎開 PR 補上。

---

## 5.5 — Subagents（Claude Code 原生 multi-agent 機制）⭐ 2025 新功能

到這裡為止你學了 MCP（工具層）/ Skills（行為層）/ Plugins（散佈層）。**Subagents 是 orchestration 層**（orchestration = 調度一群 agent：分工，再把結果合起來）——讓主 Claude session spawn 出有獨立 context 的子 agent、跑特定任務、回報結果。

![Subagent 的 4 個生命週期：從 .md 檔到執行結果](../resources/diagrams/subagent-4-stage-flow.png)

> 📊 **上圖**：subagent 從**定義 → 發現 → 派遣 → 執行** 4 個階段、看完這張再讀下面細節最快。

跟 Stage 4 的 framework-based multi-agent（LangGraph / CrewAI / AutoGen）對照：

| 維度 | Framework path (Stage 4) | Claude Subagent path（本節） |
|---|---|---|
| 啟動方式 | `pip install crewai` + Python code | 寫一個 `.claude/agents/<name>.md` 即可 |
| Runtime | 你自己的 Python process | Claude Code 內建 Task tool |
| Context isolation | framework 自己管 | **天生** 各 subagent 獨立 window |
| Provider lock-in | 中等（多 framework 支援 multi-LLM） | **強**（綁 Claude Code） |
| 適合 | 跨 LLM provider 的 production system | 已 commit Claude Code 的工程團隊 |
| 學習曲線 | 高（框架抽象 + async） | 低（寫 markdown）|

### 各家 CLI / SDK 的 multi-agent 機制現況（2025 後段）

multi-agent CLI 一度是 Claude Code 獨有——2026 年 Codex CLI 與 Gemini CLI 都已加入**原生 subagents + hooks**（Cursor 仍是單一 agent）。Claude Code 仍是最成熟、最完整的 native multi-agent stack。

| 平台 | Subagent | Agent team | Background agent | 機制 |
|---|:---:|:---:|:---:|---|
| **Claude Code**（CLI） | ✅ | ✅ | ✅ | `.claude/agents/<name>.md` + Task tool（subagent）+ [agent teams](https://code.claude.com/docs/en/agent-teams) + [agent view / background](https://code.claude.com/docs/en/agent-view) |
| **OpenAI Codex CLI** | ✅ | ⚠️ | ✅ | [Subagents](https://developers.openai.com/codex/subagents) GA（≤6 平行）+ [hooks](https://developers.openai.com/codex/hooks)（2026）；cloud / background mode。`AGENTS.md` 仍是 context file |
| **Google Gemini CLI** | ✅ | ⚠️ | ⚠️ | [Subagents](https://geminicli.com/docs/core/subagents/)（2026-04）+ [hooks](https://geminicli.com/docs/hooks/)；`@name` 顯式派遣、可平行。`GEMINI.md` 仍是 context |
| **Cursor**（IDE-coupled） | ❌ | ❌ | ❌ | 單一 Cursor Agent；queued messages 是 sequential、非 parallel |
| **OpenAI Agents SDK**<br>（programmatic、非 CLI） | ⚠️ Handoffs + agents-as-tools | ❌ | ❌ | 純 Python SDK、不是 CLI；handoff pattern 接近 Claude subagent 但要寫 code |
| **Framework path**<br>（Stage 4） | LangGraph / CrewAI / AutoGen | ✅ 自己 wire | 部分 | 跨 LLM provider、Python orchestration、見 [Stage 4](04-agent-frameworks.md) |

**現況解讀**：

- 想用 **CLI** 玩 multi-agent → 目前只有 Claude Code 有 native 支援（**本節主題**）
- 想 **跨 provider / 跨 LLM** → 走 Stage 4 framework path
- 想 **OpenAI 生態 + 多 agent** → 用 OpenAI Agents SDK 寫 handoff pattern（programmatic、非 CLI）
- 想 **完全自己控** → 走 [Stage 5.7 Harness Internals](#57--claude-code-source-解剖reference-harness-implementation-track-b-必看)（讀 SDK source、自己 wire 多 agent）

→ 本節剩下內容都聚焦在 **Claude Code subagent**。Codex / Gemini CLI 已在 2026 加入原生 subagents（見上表）、Cursor 仍是單一 agent；其餘進展追各家 changelog。

### 怎麼派遣 Claude Code 的 3 種 multi-agent 機制（具體 syntax）

| 機制 | 何時用 | 派遣方式 |
|---|---|---|
| **Subagent**<br>（穩定版） | delegate 大 context 任務（讀整個 codebase / 整理 logs）給 isolated context worker、結果回主 session | (1) 寫 `.claude/agents/<name>.md`（frontmatter `name` + `description` + `tools` + 可選 `model`）<br>(2) Claude 看 description **自動 delegate**；或 `/agents` 手動列表 |
| **Agent team**<br>（已有正式 docs、仍需 opt-in flag） | 多 worker 之間要**互相溝通**、challenge 彼此（debate / peer review / 多角度探索） | (1) **啟用**（仍需 opt-in）：`settings.json` 加 `"env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}`、需 Claude Code v2.1.32+<br>(2) 自然語言派遣：`Create an agent team to explore X from different angles: one on UX, one on architecture, one playing devil's advocate`<br>(3) 跟 teammate 對話：`Shift+Down` 切換、直接輸入訊息<br>(4) 收尾：`Clean up the team` |
| **Background agent**<br>（research preview） | 多個**獨立任務**各自背景跑、單一介面監控（同時 3 個 PR review） | (1) shell 派遣：`claude --bg "investigate the flaky test"`（需 v2.1.139+）<br>(2) 從現有 session 背景化：`/bg`<br>(3) 監控：`claude agents`（agent view 介面）<br>(4) 操作：`claude attach <id>` / `claude logs <id>` / `claude stop <id>` |

**3 個機制怎麼選**：

- 任務獨立、worker 不互動、結果回主 session 即可 → **Subagent**（最簡單、token 最省）
- Worker 需要互相溝通 / debate / 共享 task list → **Agent team**（已正式有 docs、但仍需 opt-in env var；token 3-5x、適合 research / debug 競爭假設）
- 多個獨立任務各自跑、想用 1 個介面監控全部 → **Background agent**（research preview、適合長時間任務並行）

---

### 可派遣的 subagent 有哪些？

> 💡 **先解釋一下名詞**：**subagent** = 主 Claude session spawn 出來的「子 Claude」——有自己的 context window（一次能記住的對話量、有上限）、跑完回報結果。**派遣（dispatch）**就是叫 subagent 去做事、像派任務給同事。

很多人以為要用 subagent 都得自己寫一個——其實 **Claude Code 內建一批 subagent、開箱即用**。下表列三種來源：

| 來源 | 範例 subagent | 何時用 | 需要做什麼 |
|---|---|---|---|
| **Claude Code 內建** | `general-purpose` / `code-reviewer` / `Explore` / `Plan` / `frontend-developer` / `claude-code-guide` / `statusline-setup` | 一般任務都先看內建有沒有合的 | **什麼都不用做、直接呼叫** |
| **plugin / marketplace** | `obra/superpowers` 內含的 skill agent、`wshobson/agents` 的多 subagent 組合 | 內建不夠用時 | 裝 plugin / marketplace（[Stage 5.4](#54--plugins-與-marketplaces)）|
| **自己寫的** | 你公司流程 specific 的 reviewer / domain expert | 上面都不符合時 | 寫 `.claude/agents/<name>.md`（範例見下面 details 區塊）|

> 🔍 **想知道你的 Claude Code 現在有哪些 subagent 可用？** 終端機跑 `/agents` 一指令列表（內建 + plugin + 自訂全部）。

### 怎麼選哪一個 subagent？（decision table）

對應上面 7 個 Claude Code 內建 subagent、下表是「**遇到 X 任務、用 Y subagent**」對照（這叫 **decision table**——「要 X 用 Y」的快速對照、不用想自己會選）：

| 你要做的事 | 用哪個內建 subagent | 為什麼 |
|---|---|---|
| 找 code / 探索陌生 codebase 結構 | `Explore` | 專門做 read-only 搜尋、不會亂改 |
| 設計實作 plan（不直接寫 code） | `Plan` | 輸出 step-by-step 計畫、適合大任務拆解前 |
| Review staged diff / 安全審查 / 發 commit 前檢查 | `code-reviewer` | 結構化輸出 PASS/FAIL + 具體 fix |
| 寫 / 改 UI component / 處理 accessibility（無障礙設計）| `frontend-developer` | React / 響應式 / a11y（accessibility 縮寫、視障 / 鍵盤使用者也能用的設計）領域知識 |
| 多步驟研究、不確定任務該歸哪類 | `general-purpose` | 通用、可 web search、適合 fallback |
| 問 Claude Code 自己的 feature 怎麼用 | `claude-code-guide` | hooks（工具執行前 / 後的攔截腳本、見下方 Gotcha #5）/ slash command（`/` 開頭的指令）/ MCP 等問題 |
| 上面都不符合 | 自己寫 `.claude/agents/<name>.md` | 客製或公司 specific 流程 |

**5 個常見情境的 mini cookbook**（完整 15 個 recipe 見下面）：

| 情境 | 用哪個 |
|---|---|
| 寫了 ≥ 50 行新 code、要 commit 前 | `code-reviewer` |
| Clone 完新 repo、不知該從哪個 file 開始 | `Explore` |
| 4 個 stage / branch 都要做同樣審查 | `general-purpose`（spawn 多個並行）|
| 想重構 module、先 review architecture | `Plan` |
| 多 source 比對哪 paper 講的對 | `general-purpose` 跑 deep research |

> 📋 **完整 15 個 recipe**（每個含**情境 + subagent + 直接複製貼上的 prompt 範本 + 何時不用**）→ [`resources/subagent-cookbook.md`](../resources/subagent-cookbook.md)

### 易混淆觀念釐清（學完表格還是有點霧、看這節）

學生最常搞混的 **3 組概念** + **5 條老手才知道的 gotcha**——挑你需要的看：

#### Subagent vs Skill — 5 個關鍵差別

很多人把 Subagent 跟 Skill 當同一件事——其實**完全不同層的東西**：

![Subagent vs Skill — 5 個關鍵差別](../resources/diagrams/subagent-vs-skill.png)

| 維度 | Subagent（子 agent） | Skill（技能） |
|---|---|---|
| **執行環境** | 新的獨立 context window（底層是新 subprocess）| 主 session 內、同 context |
| **工具權限** | 自己的 `tools:` 清單（可限制只能 Read / Grep）| 主 session 的工具（預設全開、skill 可用 `allowed-tools:` 縮減）|
| **回傳結果** | 一個 final message 摘要回主 session | 沒回傳、是行為改變（規則 / persona）|
| **適合做** | 長任務 / 平行跑 / 要 context 隔離 | 知識注入 / 規則 / 改 Claude 行為 |
| **範例** | `code-reviewer` / `Explore` / `Plan` | `codex-delegate` / `pdf`（anthropics/skills）|

**判斷快速辦法**：你**要新 context window** 嗎？要 → subagent；不要 → skill。

#### Subagent vs Slash Command — 一個是任務、一個是指令

| 東西 | 怎麼觸發 | 例子 |
|---|---|---|
| **Subagent** | 直接打對話文字、Claude 看 description 自動派遣 | 你打「Review my staged changes」→ 自動派 `code-reviewer` |
| **Slash command** | 打 `/` 開頭的指令 | `/agents`（列 subagent）/ `/compact`（壓縮 context）/ `/help` |

⚠️ **常見誤會**：`/agents` **不是用來呼叫 subagent**——它是「查當前可用 subagent 清單」的指令。**派遣是直接打對話 prompt 文字**、Claude 自己挑 subagent。

#### Description = 路由 key（**寫法決定能不能被選**）

主 session 怎麼知道該派哪個 subagent？看 `.claude/agents/<name>.md` 的 **`description` 欄位**。**寫法影響觸發行為**：

| Description 寫法 | 觸發模式 | 例 |
|---|---|---|
| `...use **PROACTIVELY** when X...` | **主動觸發**——X 出現 Claude 自己派 | "use PROACTIVELY when reviewing diffs ≥ 50 lines" |
| `...use when user asks Y...` | **被動觸發**——要使用者明白要求 | "use when user asks for code review" |
| 空 description | **隱形**——不會被自主選 | （只能在程式碼裡用 `Agent(subagent_type=...)` 強制呼叫）|

> 💡 **寫 description 像寫廣告詞**——把「我能解決什麼問題」**寫具體**、Claude 越會在對的時機選你。`PROACTIVELY` 是個**強訊號詞**——出現時 Claude 推斷「適合主動派遣」的機率大幅提升；沒寫就更常只在使用者明白要求時才會派。（它影響 Claude 的判斷、**不是程式碼層的 if-then 開關**。）

#### 5 條老手才知道的 Gotcha

| # | Gotcha | 為什麼重要 |
|---|---|---|
| 1 | **Description 寫精準即可** | 無官方字元上限、但過長 description 佔 context budget；建議「觸發條件 + 適用情境」寫具體、避免重複 |
| 2 | **`tools:` 寫空 = 繼承主 session 全部工具** | 想限制 subagent 就要**明寫**工具清單；空字段 ≠ 沒工具 |
| 3 | **不寫 `model:` = 跟主 session 用同 model** | 主 session 是 Opus、subagent 沒指定也 Opus（燒大錢）。省成本就寫 `model: sonnet` 或 `model: haiku`|
| 4 | **Subagent 沒「我之前說過 X」記憶** | 每次派遣都是**全新 context**、看不到主 session 對話。Prompt 要 self-contained、不能 reference「我們剛討論的 Y」 |
| 5 | **Subagent 也吃 hook** | PreToolUse / PostToolUse（工具執行前 / 後的攔截腳本）在 subagent 內**也會 fire**。設 hook 時要想到這層 |

#### Subagent 整體優缺點（讀完前面、回頭看這個 summary）

**5 個優點**（為什麼存在）：

| 優點 | 怎麼幫到你 |
|---|---|
| **Context 隔離** | 主 session window 不被污染——subagent 跑大檔案 / 長 log 不會擠掉主 session 的工作記憶 |
| **Tool allowlist** | 限制 subagent 只能用 Read / Grep（不能寫檔 / 不能跑 Bash）= 安全 sandbox |
| **Model override** | 跑簡單任務用 Haiku、跑難的用 Opus、混搭省成本——主 session 是 Opus 也可以叫 subagent 用 Haiku |
| **Parallel spawn** | 一個 prompt spawn N 個 subagent 平行跑、wall clock 時間 ÷ N（適合 4 個 file 同時 audit）|
| **專業化 prompt** | code-reviewer 永遠只 review、description 寫死「Use PROACTIVELY when commit」、不會被閒聊干擾 |

**5 個缺點**（什麼時候不值得）：

| 缺點 | 影響 |
|---|---|
| **Spawn 有 overhead** | 任務 < 5 分鐘、自己跑更快——subagent startup 也吃時間跟 token |
| **無 cross-call memory** | 每次 spawn 都新 context、看不到「我們剛討論的 X」——prompt 必須 self-contained |
| **只回一個 message** | subagent 是「派出去、跑完回報一次」、不能跟你來回對話、不適合需要逐步 feedback 的任務 |
| **Token cost N ×** | spawn 4 個 = 用 4 倍 token——parallel 的 ROI 要算（時間省、錢花更多）|
| **Debug 多一層** | 出錯不知該怪主 session description / subagent system prompt / 還是 prompt 本身——見 [advanced §3 debug 5 切點](../resources/subagent-advanced.md#3-自製-subagent-的-debug-工具)|

> 📌 **1 句話判斷**：任務 **≥ 5 分鐘** + **可以用一個 brief 寫死**（不需來回對話）+ **結果一次回來夠用**（不需逐步 feedback）→ 用 subagent；否則自己跑。


> 📋 **準備自己寫 subagent / 組合多個 / debug 跑壞的？** → [`resources/subagent-advanced.md`](../resources/subagent-advanced.md)（description 寫法 4 個 bug 對照、composition 3 種 pattern、debug 5 切點）


<details markdown="1">
<summary>👉 具體 subagent 檔案範例（最簡單入門）</summary>

`.claude/agents/code-reviewer.md`：

```markdown
---
name: code-reviewer
description: Review staged git changes for security issues, style violations, and missing tests. Use when user asks "review my changes" or runs /review.
tools:
  - Read
  - Grep
  - Bash
model: claude-haiku-4-5 # 可選、想 route 到便宜 model 省成本
---

You are a senior code reviewer. When invoked:
1. Run `git diff --cached` to get staged changes
2. Check for: hard-coded secrets, SQL injection patterns, missing error handling, missing tests
3. Output: PASS / list of specific issues with file:line references
```

主 session 之後輸入「review my changes」，Claude 看到 description 匹配、自動透過 Task tool（Claude Code 內部派遣機制、你不用直接呼叫）spawn 這個 subagent 跑、回主 session 一段摘要。

</details>

> 📚 **官方完整文件**：
> - [Subagent spec](https://code.claude.com/docs/en/sub-agents)（frontmatter 欄位、project vs user scope、Task tool 介面）
> - [Agent team 完整指南](https://code.claude.com/docs/en/agent-teams)（display modes、task list、subagent-as-teammate 進階）
> - [Agent view / background](https://code.claude.com/docs/en/agent-view)（v2.1.139+、quick start + dispatch 流程）

### 學習目標

- 講得出 subagent 跟 skill / MCP server 的差別（**subagent ≠ skill**：skill 是行為 prompt，subagent 是**另一個 Claude instance with isolated context**）
- 寫一個 `.claude/agents/<name>.md` 自訂 subagent（frontmatter + system prompt + `tools:` 白名單——明寫允許的工具清單）
- 從主 session 用 Task tool invoke subagent，觀察 context 隔離（parent 看不到 subagent 的中間 step、只看到最終 result）
- 知道何時用 subagent（parallel research / large-context isolated task / specialized review），何時不用（小 query 用 skill 即可）

### 必修閱讀

1. [**Anthropic — Claude Code Subagents 官方文件**](https://code.claude.com/docs/en/sub-agents) ⭐ — `.claude/agents/` 結構、Task tool 介面、最佳實踐
2. [**Anthropic — Building Effective Agents orchestrator-workers**](https://www.anthropic.com/engineering/building-effective-agents) — Anthropic 自己對 orchestrator pattern 的看法（理論 + 實例）
3. [**Anthropic Cookbook — `customer_service_agent`**](https://github.com/anthropics/claude-cookbooks/tree/main/tool_use) — canonical multi-agent orchestration 範例（chapter-length 深度教材；notebook 在 `tool_use/customer_service_agent.ipynb`）

### 動手練習

- **練習：第一個 subagent** — 寫 `.claude/agents/code-reviewer.md`（前置 frontmatter 含 `description` 寫清楚何時 trigger、`tools` 限定 Read+Grep）+ system prompt 跑 staged diff review。從主 Claude session 跑 `/agents` list 確認載入、然後用 prompt「review staged changes」觀察 Task tool 怎麼 spawn subagent
- **練習：parallel subagent crew** — 寫 3 個 subagent（`researcher.md` / `writer.md` / `critic.md`）做「研究某主題 → 寫 blog 草稿 → 審稿」pipeline、主 session 用 Task tool 串起來。**對照** [`examples/stage-4/02-multi-agent-roles/`](../examples/stage-4/02-multi-agent-roles/)（CrewAI 框架版同一個任務）、看「framework 路線 vs Claude 原生路線」程式碼差別
- **練習：subagent 跟 skill 的決策練習** — 拿你自己日常工作流的 5 個常用任務、每個判斷該用 skill（行為層）還是 subagent（獨立 context 層）。寫成 1 頁 decision table

> 📚 **想要 chapter-length 深入版**：subagent 進階 pattern（agent-as-skill composition、parallel-spawn、handoff between subagents）→ 看 [`wshobson/agents`](https://github.com/wshobson/agents) repo 整個結構 + [`obra/superpowers`](https://github.com/obra/superpowers) 的 subagent 用法。

### 精選 Projects

4 個項目一張表搞定。**挑入口看「適合誰」、想深入點連結看 repo**。

| Project | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|
| [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) ⭐ 官方 | ⭐⭐⭐⭐⭐ | 5.5 完成後想看「實際在用的 agent 範例怎麼寫」 | Anthropic 官方 chapter-length 範例。**`tool_use/customer_service_agent.ipynb`** = orchestrator-workers canonical（multi-agent routing + handoff）。Python / Jupyter notebook、MIT。**註**：`computer_use_demo` 完整版在另一個 repo [`claude-quickstarts/computer-use-demo`](https://github.com/anthropics/claude-quickstarts/tree/main/computer-use-demo) |
| [wshobson/agents](https://github.com/wshobson/agents) ⭐ subagent canonical | ⭐⭐⭐⭐⭐ | 寫過 1-2 個 subagent 想看真實 team 範本 | 50+ subagent definition 的 production workflow pattern collection。**看 `.claude/agents/` 目錄結構 + 命名 convention + 跨 agent handoff 寫法** |
| [obra/superpowers](https://github.com/obra/superpowers) | ⭐⭐⭐⭐ | 想看 skill + subagent 混搭實作 | 在 Stage 5.3 已介紹。**重點看「什麼任務歸 skill、什麼歸 subagent」決策**——production 範本 |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) 官方 | ⭐⭐⭐⭐ | 看 plugin 怎麼打包 subagent | 在 Stage 5.4 已介紹。每個 plugin 內 `agents/` 子目錄是 subagent definition、看打包方式 |

> 💡 **Subagent 雖然強、不要無腦用**：每個 subagent invoke 都是一個新的 Claude inference call、有 token cost + latency。**簡單 query 用 skill（行為 prompt）即可、不必 spawn subagent**。Subagent 的甜蜜點是：(1) 任務 context 大、會吃光主 session 的 window（譬如 read 整個 codebase），(2) 任務跟主 session 邏輯獨立、隔離 context 有助 main flow，(3) 多 subagent 平行（research / write / critic）能省 wall-clock 時間。

> 🔗 **相關進階機制**（Claude Code 官方、本 stage 不深入講）：
> - **[Agent teams](https://code.claude.com/docs/en/agent-teams)** — 多 sessions 之間互相溝通（reviewer agent ↔ implementer agent 來回交流）
> - **[Background agents / agent view](https://code.claude.com/docs/en/agent-view)** — 多 session 背景跑、單一介面監控（一次 spawn N 個 PR review 同時跑）
>
> Subagent 是這兩個的進入點——本節學完之後想擴展再看官方文件。

---

## 5.6 — Dynamic Workflows（讓 Claude 自己寫出 workflow）⭐ Opus 4.8+ 新機制

> **本節定位**：5.5 教你**手動**派 subagent；本節更上一層——**讓 Claude 自己生成一份 workflow 腳本、再自己執行**。這是 Opus 4.8 起的新機制（research preview 出身），新版 Claude Code 內建。本節只把它放進生態地圖、講清楚跟 5.5 的分工；**機制 / 實例 / quality pattern 的完整版在 [Stage 7.5 — Dynamic Workflows 深入](07.5-advanced-agentic-concepts.md#-dynamic-workflowsopus-48-當-agent-自己寫出-workflow)**。

### 跟 5.5 Subagents 的差別

| | 5.5 Subagents | 5.6 Dynamic Workflows |
|---|---|---|
| 步驟誰決定 | 你手動派、一次一個 | Claude 自己寫出多步驟腳本 |
| 控制流 | model 即興決定下一步 | 腳本裡是**確定性**的 loop / 平行 fan-out / 驗證階段 |
| 適合 | 少數幾個並行子任務 | 大型、要窮舉或多階段驗證（migration、audit、跨檔 review）|
| 關係 | — | DW **建在 subagent 之上**：workflow 腳本去 orchestrate 一群 subagent |

### 什麼時候用、什麼時候別用

- **用**：要窮舉 + 對抗式驗證（找完所有 bug、每個 finding 再派獨立 agent 反駁）、一次性大遷移、跨多檔同樣轉換的 pipeline。
- **別用**：只是想叫一兩個 agent 平行做點事 → 留在 5.5 就好；小任務直接一條 prompt 更省。
- ⚠️ DW 會 spawn 大量 agent、吃 token，不是萬靈丹。「何時值得、怎麼寫不會爆」見下方 7.5 深入。

### 📚 必修閱讀

1. [**Anthropic — Claude Opus 4.8**](https://www.anthropic.com/news/claude-opus-4-8) — Dynamic Workflows 首次發布的官方說明
2. **[Stage 7.5 — Dynamic Workflows 深入](07.5-advanced-agentic-concepts.md#-dynamic-workflowsopus-48-當-agent-自己寫出-workflow)** ⭐ — 機制、quality pattern（adversarial verify / loop-until-dry / judge panel）、何時用的完整版

> 本節無 examples（概念 + 入口節點）；想動手照 7.5 的 pattern 寫。

---

## 5.7 — Claude Code Source 解剖（reference harness implementation）⭐ Track B 必看

> **本節定位**：本節**不是** harness engineering 的學科級概念教學——學科級的定義 / **8 個核心元件** / prompt→context→harness 五層工程分工 是 **[Stage 7 Harness Engineering](07-multi-agent-production.md#-harness-engineering--production-agent-runtime-的工程設計--本-stage-核心概念)** 在講。**本節是 case study**——拿 Claude Code（一個被廣泛使用的參考實作）的 source code 來解剖、把 Stage 7 列的 8 個元件**中前 6 個 runtime-internal 元件**（Eval / Cost-Latency 兩個是跨層議題、不在 source 主 loop）**在實作裡找到對應位置**。

### 學習目標

完成本節後你會：

- 看得懂 `claude-agent-sdk-python` source 的 main loop（不是逐行、是抓得到主幹）
- 在 source 裡標出 [Stage 7 列的 8 個 harness 元件](07-multi-agent-production.md#-harness-engineering--production-agent-runtime-的工程設計--本-stage-核心概念)**中**前 6 個 runtime-internal 元件（agent loop / tool registry（agent 可呼叫工具的清單 + 介面定義） / context manager / safety layer / retry / telemetry）各自的 file:line。Stage 7 列的第 7 個 Eval 是外掛、第 8 個 Cost / Latency 是 cross-cutting、不在 source 主 loop 內、不在本練習範圍
- 講得出 Claude Code 的 agent loop 跟 Stage 3 練習 3 from-scratch ReAct 差在哪——上線部署的 agent 多了哪些東西

> **學科級概念在哪**：harness engineering 是什麼 / framework vs harness 差別 / prompt→context→harness 五層工程分工 → 全部見 **[Stage 7 Harness Engineering](07-multi-agent-production.md#-harness-engineering--production-agent-runtime-的工程設計--本-stage-核心概念)**。本節只負責 Claude Code source 的 case study。

### 📚 必修閱讀

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) ⭐ — orchestrator / worker / handoff / reflection 等 pattern 的 canonical reference
2. [**anthropics/claude-agent-sdk-python**](https://github.com/anthropics/claude-agent-sdk-python) — Claude Code 官方 Python SDK 的 source；**重點 file：`src/claude_agent_sdk/_internal/client.py`**（main loop 在這）+ `query.py`（單回合 API）
3. [**ai-boost/awesome-harness-engineering**](https://github.com/ai-boost/awesome-harness-engineering) ⭐（★ 3.4k+） — community curation：harness pattern / eval / memory / observability 整合
4. [**ZhangHanDong/harness-engineering-from-cc-to-ai-coding**](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding) — 中文圈最完整的 Claude Code 內部解讀

### 🛠 動手練習 — 解剖 agent loop（閱讀題，非寫 code）

這節**不是寫 code 練習，是閱讀練習**——production harness 不是抄 200 行範例能學的，是抄完還看不懂為什麼這樣寫，所以本練習要求你開 source、自己 trace。

**步驟**：

1. **clone**：`git clone https://github.com/anthropics/claude-agent-sdk-python`
2. **定位 agent loop**：找出 `_internal/client.py` 裡實際發出 LLM call、收 tool_use response、dispatch 給 tool runner 的核心 loop。提示：找 `async def` 跟 `tool_use_id` 關鍵字
3. **標出前 6 個 runtime-internal harness 元件**在 source 裡的位置（檔名 + 行號）——對應 [Stage 7 列的 8 元件](07-multi-agent-production.md#-harness-engineering--production-agent-runtime-的工程設計--本-stage-核心概念)的前 6 個（第 7 個 Eval 外掛 / 第 8 個 Cost-Latency cross-cutting 不在 source 主 loop）：
   - (a) **Agent loop**：實際發出 LLM call + 收 response 的迴圈在哪
   - (b) **Tool registry / dispatch**：LLM 回 tool_use → 怎麼 route 到對應 tool 實作
   - (c) **Context manager**：tool result 怎麼寫回 message history、context window 控制 / auto-compact
   - (d) **Safety layer**：tool 執行前有沒有 permission gate / sandboxing
   - (e) **Retry / recovery**：tool fail 時怎麼處理（exception vs LLM 自己看 error 反思）
   - (f) **Telemetry**：metrics / logging / token counting 接在哪
4. **寫一段 80-150 字摘要**：「Claude Code 的 agent loop 跟你 Stage 3 練習 3 from-scratch ReAct 差在哪」。重點不是「Claude Code 比較複雜」這種廢話，是**講得出多了哪些東西、為什麼那些是上線部署必須有的**

**交付物**：一段筆記（寫在自己的 obsidian / notion / `.md` 都行），不必交。但**講不出來你就還沒懂**——這是進 Stage 7 production deploy 之前的必要 mental model。

→ **基礎 starter 範本**：本練習**無 examples folder**——是 source-reading exercise，非 code-writing exercise。illustrative，深度教學見上方 📚。

### 🎯 精選 Projects

4 個項目一張表搞定。**挑入口看「適合誰」、想深入點連結看 repo**。

| Project | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|
| [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | ⭐⭐⭐⭐⭐ | 所有 Track B 學習者、想搞清楚「Claude Code 內部怎麼跑」 | **canonical Python harness、本節練習就是讀這個 repo**。後面 Stage 7 deploy 也會 import |
| [ZhangHanDong/harness-engineering-from-cc-to-ai-coding](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding) | ⭐⭐⭐⭐ | 中文 reader 想看「為什麼 Claude Code 這樣設計」 | 中文圈最完整 CC 內部解讀（harness 概念 → CC 實作 → 跟其他 AI coding tool 對比）。**配合 SDK source 互補看**——一個告訴你「怎麼做」、一個告訴你「為什麼這麼做」 |
| [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) | ⭐⭐⭐⭐ | 5.7 讀完想擴大視野 | community curation：30+ harness / eval / memory / observability / MCP project（★ 3.4k+）。**廣度資源庫、非教學**——挑感興趣的 sub-topic 鑽進去 |
| [wshobson/agents](https://github.com/wshobson/agents) | ⭐⭐⭐⭐ | 寫完 5.5 自己的 subagent 後想看實際在用的範本 | 50+ subagent definition 的 ergonomic 設計（description / tool list / system prompt 分層）。**讀 source 比讀文件學得多**。在 5.5 已介紹、本節 cross-ref |

> 💡 **本節跟 Stage 7 的差別**：本節學「Claude Code 這個 harness 怎麼跑」（具體 reference）；Stage 7 學「production harness 一般要有什麼」（抽象 pattern）。**先具體後抽象**、看完本節再進 Stage 7 會輕鬆很多。

---

## 5.8 — SDK：把 Claude Code 拆開來自己組 ⭐ Track B 可選、production 才需要

> 🎯 **這節是給誰看的**：99% 的人讀完 5.1-5.7 已經夠用，**只在你想做 CLI 做不到的事**才往下走。Stage 5.7 叫你讀 SDK source 是為了理解 harness 內部；這節是為了讓你**會用 SDK** 包成自己的服務。

### 1 個比喻把 SDK / CLI / `CLAUDE.md` 分清楚

- **CLI**（`claude` / `codex` / 等）= 一台**現成的車子**，點一下就能上路
- 改 `CLAUDE.md` / `AGENTS.md` / 加 hooks / 寫 skills = **調車子的性能**，讓它開得更順、更貼你工作習慣 —— 一樣是這台車
- **SDK**（`claude-agent-sdk-python` / `openai-agents-python`）= **把車子從引擎開始重造一台** —— 用 Python / TS 控制 agent loop、tool dispatch、memory 怎麼接

**99% 的學習者天花板停在「調車」就夠了。** 只在「調車怎麼調都到不了你要的場景」時，才需要爬到 SDK。

### 階梯式三層 —— 你現在在哪？

1. **第 1 層 直接用 CLI** —— 90% 的個人 + 團隊使用情境。看 5.1
2. **第 2 層 CLI + 自訂** —— 寫 `CLAUDE.md`、加 hooks、自己寫 skill、套 plugin。看 5.1-5.4。**多數人停在這層、且夠用**
3. **第 3 層 SDK** —— 把 agent 嵌進你的應用。這節在教

### 什麼時候才需要爬到第 3 層

具體場景（不抽象）：

- **嵌進你已有的 web app / 後端** —— 使用者不開 terminal，就不能用 CLI
- **cron / scheduler 自動觸發** —— 沒有人類在 session 裡點 enter，CLI 互動模式不適用
- **公司內部包一層** —— 加 auth、audit log、限額、自訂 prompt template，讓 CLI 的能力以受控方式對外
- **同時跑多 agent、要 programmatic 控制 hand-off** —— 比 Stage 5.5 的 Task tool 更細的控制權

如果你做的不在上面，你大概不需要 SDK。**該回 5.1-5.4。**

### Hello SDK（4 行 Python）

```python
from claude_agent_sdk import query

async for msg in query(prompt="用 git status 看當前狀態"):
    print(msg)  # 所有 message type 都能 print；要拿 agent 回覆要 filter AssistantMessage
```

就這樣 —— 包進 `async def` 就能跑。`query()` 會 yield 多種 message type（`AssistantMessage` / `ResultMessage` / `SystemMessage` 等），上面的 `print(msg)` 全部都能安全印出來；想拿到 agent 真正的回覆要 `isinstance(msg, AssistantMessage)` 再取 `msg.content` —— retry / streaming / prompt caching 等進階用法在 Stage 7 練習 4。

### vs CLI / vs 自訂 對照表（看完上面再看這張）

| | CLI（claude / codex） | CLI + 自訂（改 CLAUDE.md / hooks） | SDK |
|---|---|---|---|
| 嵌進你的 app | ❌ | ❌ | ✅ |
| cron / 排程跑 | ⚠️ 勉強（`-p` flag） | ⚠️ 同左 | ✅ |
| 換語言 / 環境 | 綁 Node / Bash | 同左 | Python / TS 隨你 |
| programmatic 控制 | ❌ | ❌ | ✅ |
| 客製 system prompt | 受限 | 受限 | 完全自由 |
| 學習成本 | 1 天 | 1-2 週 | 1 個月+ |
| 適合誰 | 個人日常用 | 個人 / 小團隊長期用 | 包成產品 / 服務 |

### 兩個主要 SDK

| | [claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | [openai-agents-python](https://github.com/openai/openai-agents-python) |
|---|---|---|
| 出品 | Anthropic 官方 | OpenAI 官方 |
| 模型 | Claude（Opus / Sonnet / Haiku） | OpenAI 系列 + 其他 |
| 強項 | 跟 Claude Code 一致的 tool / skill / hook 抽象 | handoff / agents-as-tools 模式、2026-04 內建 sandbox |
| 適合 | 已在用 Claude Code 想嵌服務的人 | 已 commit OpenAI 生態的人 |

兩個都 MIT 授權、API 設計乾淨，**重點是你的下游選哪家模型**。

### 接下來

- **看程式碼**：回 5.7，讀 `claude-agent-sdk-python` 的 `_internal/client.py` —— 你現在會用 SDK 了，讀那邊的 main loop 會看懂更多
- **動手練 SDK 進階**：Stage 7 練習 4（streaming + prompt caching）；Stage 7 練習 5（FastAPI + Docker production deploy）
- **如果你發現你其實不需要 SDK**：那很好 —— 回 5.1-5.4，把 CLI + 自訂這層用透，通常已經比寫 SDK 划算

> 💡 **本節跟 Stage 7 的差別**：本節學「SDK 是什麼、什麼時候用」（定位 + 入門）；Stage 7 學「用 SDK 寫一個可上線部署的 agent 服務」（streaming / caching / deploy）。

---

## ✅ 進入 Stage 6 前的自我檢查

你能不能：

- [ ] 安裝 Claude Code 並使用 5 個不同的 slash command
- [ ] 在同一個 Claude session 裡接 2 個 MCP server
- [ ] 用 Python 寫自己的 MCP server，提供 1 個能用的 tool
- [ ] 寫一份能在特定觸發詞自動載入的 `SKILL.md`
- [ ] 把 skill 打包成 plugin，再用 `marketplace.json` 發佈
- [ ] **寫過 `.claude/agents/` 自訂 subagent 並從 Task tool invoke 過**
- [ ] **讀過 `claude-agent-sdk-python` 的 main loop、能在 source 裡標出 [Stage 7 列的 8 個 harness 元件](07-multi-agent-production.md#-harness-engineering--production-agent-runtime-的工程設計--本-stage-核心概念) 的前 6 個 runtime-internal 元件**位置（5.7 練習）
- [ ] 從角色分工說出 MCP / Skills / Plugins / Subagents / SDK 各自的位置

如果都可以 → 前往 [Stage 6 — Memory & RAG](06-memory-rag.md)。

> 💡 **Stage 5 是兩 track 第一個 hub**——Track A 跟 Track B 都會用到。第二個 hub 是 [**Stage 8 — Agent Interfaces**](08-agent-interfaces.md)（Computer Use / Browser Use / Sandbox），可以走完主幹後再進、或對 Computer Use / Browser MCP 有興趣可以提前 preview。

## 💡 Bonus：完成這個階段之後

- 對 [`anthropics/claude-cookbooks`](https://github.com/anthropics/claude-cookbooks) 發一個 PR（小修正、文件更新）
- 把自己的 plugin 投稿到社群 marketplace
- 寫一篇文章，比較自己的 hello-MCP server 跟官方 `modelcontextprotocol/servers` 收的某一個

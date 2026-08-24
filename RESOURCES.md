# 相關資源

> **繁體中文** | [简体中文](./RESOURCES.zh-Hans.md) | [English](./RESOURCES.en.md)

> [← 回主路線 README](README.md)

這份檔案集中放：用語說明、常用 MCP / Skill 整合 highlight、同主題 awesome list、中文社群資源。從主 README 抽出來避免主頁過長。

> 💡 **不懂某個詞**（LLM、agent、RAG、token、向量資料庫⋯）→ [`resources/glossary.md`](resources/glossary.md)（用語小辭典，30 多個詞每個 30-80 字解釋）
>
> 🍳 **想動手做但不知怎麼開始**（寫 Skill / 寫 MCP server / 接 Word / 接 NotebookLM / 接 Zotero / 接本機 LLM）→ [`resources/cookbook.md`](resources/cookbook.md)（6 個 step-by-step recipe，每個 30-50 分鐘做完）

---

## 三個核心用語：MCP / Skills / Plugins

主 README 跟各 stage 會頻繁提到這三個 Claude Code 生態的關鍵詞，先快速說明：

- **MCP（Model Context Protocol）** — Anthropic 推的開放協定，讓任何 LLM host（Claude Code、其他 IDE、自寫 agent）都能用同一套介面去呼叫外部 tool server（檔案、DB、API、自家服務）。把它想成「LLM 的 USB 接口」。詳見 [Stage 5.2](stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎)。
- **Skills** — Claude Code 的「行為包」。一個 Skill 就是一份 `SKILL.md`，描述「在什麼情境要做什麼、可以呼叫哪些 MCP tool」。寫好之後 Claude Code 會自動 discover。詳見 [Stage 5.3](stages/05-claude-code-ecosystem.md#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層)。
- **Plugins / Marketplaces** — 把 Skills、slash commands、hooks、MCP 設定打包成一個發佈單位給 team 或社群安裝。Marketplace 就是 plugin 的 catalog。詳見 [Stage 5.4](stages/05-claude-code-ecosystem.md#54--plugins-與-marketplaces)。

對應的 動手練習都在 [Stage 5](stages/05-claude-code-ecosystem.md)，Track A 的 [A3](tracks/cli/A3-cli-production.md) 也會用到。

---

## 接日常工具：常用 MCP server / Skill

把 Claude Code（或其他 CLI agent）接到你已經在用的 app，省掉手動切換的成本。下面幾個是社群 / 官方比較成熟的：

### 筆記 / 知識庫

- [**MarkusPfundstein/mcp-obsidian**](https://github.com/MarkusPfundstein/mcp-obsidian) ★ 4.2k+ — 透過 Obsidian REST API plugin 讓 LLM 讀寫你的 Obsidian vault
- [**makenotion/notion-mcp-server**](https://github.com/makenotion/notion-mcp-server) ★ 4.4k+ — Notion **官方** MCP server，可查詢／建立 page、database
- [**PleasePrompto/notebooklm-skill**](https://github.com/PleasePrompto/notebooklm-skill) ★ 7.3k+ — NotebookLM Skill（瀏覽器自動化），用 Claude Code 直接查你 NotebookLM 裡的文件，回答帶 citation
- [**teng-lin/notebooklm-py**](https://github.com/teng-lin/notebooklm-py) ★ 18k+ — 非官方 NotebookLM Python API + CLI，支援 Claude Code / Codex 等 agent 整合

### 辦公文件（Word / Excel / PowerPoint / PDF）

- [**anthropics/skills**](https://github.com/anthropics/skills) ★ 165k+ — Anthropic **官方** Skills 集合，docx / xlsx / pptx / pdf 處理直接內建
- [**tfriedel/claude-office-skills**](https://github.com/tfriedel/claude-office-skills) ★ 800 — 補強版 Office skills（PPTX/DOCX/XLSX/PDF），含自動化 workflow

### Google Workspace（Gmail / Docs / Drive / Calendar）

- [**taylorwilsdon/google_workspace_mcp**](https://github.com/taylorwilsdon/google_workspace_mcp) ★ 2.9k+ — 一個 server 包整套 Google Workspace（Gmail、Calendar、Docs、Sheets、Slides、Drive）

### 開發協作

- [**github/github-mcp-server**](https://github.com/github/github-mcp-server) ★ 31k+ — GitHub **官方** MCP，issue / PR / repo 操作
- [**atlassian/atlassian-mcp-server**](https://github.com/atlassian/atlassian-mcp-server) ★ 908 — Atlassian **官方** Remote MCP（Jira、Confluence）
- [**jerhadf/linear-mcp-server**](https://github.com/jerhadf/linear-mcp-server) ★ 340+ — Linear MCP server
- [**korotovsky/slack-mcp-server**](https://github.com/korotovsky/slack-mcp-server) ★ 1.7k+ — Slack MCP，無 admin 權限也能用

### 研究工作流（本 repo 維護者出品）

- [**WenyuChiou/ai-research-skills**](https://github.com/WenyuChiou/ai-research-skills) ★ 222 — 14 個研究流程 skill，5-plugin marketplace
- [**WenyuChiou/research-hub**](https://github.com/WenyuChiou/research-hub) ★ 52 — Zotero + Obsidian + NotebookLM 整合 workspace
- [**WenyuChiou/zotero-skills**](https://github.com/WenyuChiou/zotero-skills) ★ 50 — Zotero CLI skill
- [**WenyuChiou/codex-delegate**](https://github.com/WenyuChiou/codex-delegate) ★ 62 [**gemini-delegate-skill**](https://github.com/WenyuChiou/gemini-delegate-skill) ★ 34（⚠️ 已封存）— Multi-LLM delegation 對（Gemini lane 建議改用 Gemini CLI 直接做）

### 中文圈常用

- [**leemysw/feishu-docx**](https://github.com/leemysw/feishu-docx) ★ 235 — 飛書（Lark）docs / sheet / bitable ↔ Markdown，含 Claude Skills 支援

> 上面只是 highlight。**完整 81+ 個整合的分類目錄**（含資料庫、瀏覽器自動化、Figma、Excalidraw、Cloudflare、Stripe、學術寫作 / Multi-LLM delegation 等）在 [`resources/mcp-skills-catalog.md`](resources/mcp-skills-catalog.md)。

> 想找更多 MCP server catalog？看 [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) / [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers)（依分類整理）。**Canva** 現有官方 MCP（[canva.dev/docs/mcp](https://www.canva.dev/docs/mcp/)、endpoint `mcp.canva.com`、~32 工具、任何方案可用、支援 Claude / ChatGPT / Cursor / VS Code）。

---

## 同主題的清單型 awesome lists

本 repo **不取代**清單型 awesome list——你已經知道在找什麼工具時，下面這些查起來更直接：

### MCP 相關

- [**modelcontextprotocol/servers**](https://github.com/modelcontextprotocol/servers) — 官方 MCP reference servers（現有 7 個：everything、fetch、filesystem、git、memory、sequentialthinking、time；github、sqlite 已移到 `servers-archived`）
- [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers) — 社群 MCP server 清單，按分類整理（150+ 個）
- [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers) — 另一份 MCP server 清單

### Claude Code / Skills / Plugins 相關

- [**hesreallyhim/awesome-claude-code**](https://github.com/hesreallyhim/awesome-claude-code) — Claude Code 相關資源清單（整理中）
- [**travisvn/awesome-claude-skills**](https://github.com/travisvn/awesome-claude-skills) — Claude Skills 清單
- [**anthropics/claude-plugins-official**](https://github.com/anthropics/claude-plugins-official) — Anthropic 官方 plugin 範本，要打包自己的 plugin 從這份開始

### 中文社群必看

- [**datawhalechina/hello-agents**](https://github.com/datawhalechina/hello-agents) — Datawhale 系統性 agent 教學（zh-Hans）
- [**WangRongsheng/awesome-LLM-resources**](https://github.com/WangRongsheng/awesome-LLM-resources) — 完整的中文 LLM 資源整理（8.8k+ stars）
- [**AiHubCN/Awesome-Chinese-LLM**](https://github.com/AiHubCN/Awesome-Chinese-LLM) — 中文開源大模型整理
- [**hardness1020/awesome-agent-architecture**](https://github.com/hardness1020/awesome-agent-architecture) — 逐節拆解現代 agent harness（loop engineering、tools、permissions、context、memory、evaluation），以 Claude Code、Hermes Agent 等系統為案例（持續新增），每節附可執行 Python demo（繁中/简中/英文三語）

### 線上課程 / MOOC（帶證書對照）

- [**resources/courses.md**](resources/courses.md) — 10 門 credible、會發證書的線上 AI agent 課（英文 + 中文），分 tier；含「完成證書 ≠ 學歷」的誠實 caveat

---

## 還有什麼？

- 主 README：[README.md](README.md)
- 完整 MCP/Skill 目錄：[resources/mcp-skills-catalog.md](resources/mcp-skills-catalog.md)
- CLI agent 比較指南：[resources/cli-agents-guide.md](resources/cli-agents-guide.md)
- Style guide / 貢獻規範：[resources/style-guide.md](resources/style-guide.md)、[CONTRIBUTING.md](CONTRIBUTING.md)

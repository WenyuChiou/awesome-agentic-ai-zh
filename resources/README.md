# `resources/` 索引

<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

> 本 repo 的「**reference 區**」——非主路線、需要時來查的補充材料。每份檔案有明確角色，不重複。

---

## 7 份 reference + 各自的「什麼時候看」

| 檔案 | 角色 | 什麼時候看 | 行數 |
|---|---|---|---|
| [`glossary.md`](glossary.md) | **30 秒查詞典** | 看 stage 內文時遇到 LLM / RAG / token / agent / vector DB / streaming / batch API 不知道什麼意思 | ~210 |
| [`cli-agents-guide.md`](cli-agents-guide.md) | **CLI agent 身分與選擇指南** | 第一次選 CLI agent、不確定哪個工具適合自己的工作方式 | — |
| [`mcp-skills-catalog.md`](mcp-skills-catalog.md) | **81+ 個整合 catalog** | 想把 Claude Code 接 Notion / Obsidian / Excel / Postgres / Slack / 等等實際工具 | ~775 |
| [`schema-design-cheatsheet.md`](schema-design-cheatsheet.md) | **function schema 設計 5 規則 + 5 anti-pattern** | 寫 tool schema / MCP server schema / function calling，發現 LLM 選錯 tool / 傳錯參數 | ~159 |
| [`cookbook.md`](cookbook.md) | **6 個 step-by-step recipe** | 想 30-50 分鐘做出第一個 Skill / MCP server / 接 Office / 接 NotebookLM / 接 Zotero / 接本機 LLM | ~620 |
| [`setup-guide.md`](setup-guide.md) | **從零開始的 setup 指南** | 完全沒 dev 背景、第一次申請 API key / 裝 Python / 用 Claude Code | ~400 |
| [`style-guide.md`](style-guide.md) | **送 PR 前的格式 / 用詞規範** | 要對 repo 貢獻、寫 entry / 翻譯 | ~338 |

合計 ~2500 行 reference。看起來不少，但**每份檔案讀的時機不同**——你不會一次全讀，只在對應情境查 30 秒到 45 分鐘。

---

## 怎麼進來：以「我現在要做什麼」分類

### 🆕 我完全沒寫過 code / 第一次接觸 AI agent

→ [`setup-guide.md`](setup-guide.md)（30-45 分鐘從零裝好）

### 🆕 我剛開始學 AI agent

不需要先讀任何 reference。**直接從主路線 [README](../README.md) → [Stage 0](../stages/00-foundations.md) 開始**。遇到不懂的詞回來查 [`glossary.md`](glossary.md) 就好。

### 🛠 我要選 CLI agent

→ [`cli-agents-guide.md`](cli-agents-guide.md)（6 個 CLI 比較 + 依 use case 推薦）

### 🔌 我要把 Claude Code 接 X 工具（Notion / Excel / Postgres 等）

→ [`mcp-skills-catalog.md`](mcp-skills-catalog.md)（81+ 個整合分 16 類）

### 🍳 我想動手寫第一個 Skill / MCP server / 接 Word 等

→ [`cookbook.md`](cookbook.md)（6 個 step-by-step recipe）

### 📐 我寫 tool schema 但 LLM 不照我意思做

→ [`schema-design-cheatsheet.md`](schema-design-cheatsheet.md)（5 規則 + 5 anti-pattern）

### 📚 我看 stage 內文遇到不懂的詞

→ [`glossary.md`](glossary.md)（每詞 30-80 字解釋 + 哪 stage 講細）

### 🤝 我想送 PR / 翻譯 / 加新 entry

→ [`style-guide.md`](style-guide.md) + [`../CONTRIBUTING.md`](../CONTRIBUTING.md)

---

## 重複 / 重疊？

刻意避免重複。每份 reference 跟主路線 / 其他 reference 的關係：

- **glossary** 是「30 秒查」、stage 內文是「3-5 分鐘讀」、cookbook 是「30-50 分鐘做」——三層深度，不重疊
- **schema-design-cheatsheet** 跟 cookbook 2（寫 MCP server）有交集——cheatsheet 講「**寫 schema 的規則**」、cookbook 講「**怎麼把 server 跑起來**」。看哪個取決於你卡在哪
- **cli-agents-guide** 是 reference table；catalog 是 plug-in tools——兩個層級不同
- **跟 [Hello-Agents](https://github.com/datawhalechina/hello-agents) 的關係**：Hello-Agents 是中文圈最完整的 agent 教材，深度高。我們是「**roadmap + curated catalog + 動手 recipe**」的角度，不取代它。Stage 5.3 / cookbook 1 都明確 cross-ref Hello-Agents Extra08「如何寫出好的 Skill」當深度補充

---

## 三語覆蓋

| 檔案 | zh-TW（canonical） | zh-Hans | English |
|---|---|---|---|
| glossary | ✅ | ✅ | ✅ |
| cli-agents-guide | ✅ | ✅ | ✅ |
| mcp-skills-catalog | ✅ | ✅ | ✅ |
| schema-design-cheatsheet | ✅ | ✅ | ✅ |
| cookbook | ✅ | ✅ | ✅ |
| setup-guide | ✅ | ✅ | ✅ |
| style-guide | ✅ | ✅ | ✅ |

---

## 加新 reference 檔的標準

不是隨便加。新檔案必須：

1. **不重複既有任何檔的角色**（看上面的「角色」欄）
2. **解決 main path 解決不了的問題**——如果 Stage X 的內文加 50 行就能 cover，就放 stage 裡別開新檔
3. **預期會被 ≥ 3 個 stage 或 branch cross-ref**——只服務一個 stage 的內容，放那個 stage 就好

近期考慮過、但**沒加**的（可選 future work）：

- `cost-calculator-guide.md`（cross-provider 計價）—— 現在 [Stage 1](../stages/01-llm-basics.md) 有提到，等需求明顯再開
- `troubleshooting-guide.md`（常見錯誤 runbook）—— 現有資料夠應付，等社群回報多了再開
- `prompt-patterns-guide.md`（CoT / few-shot 範本庫）—— 現在 [Stage 2](../stages/02-prompt-engineering.md) 有，深度版等社群 PR

社群想加可以開 issue 討論。

# 知識工作者延伸路線（For Knowledge Workers）

> **繁體中文** | [简体中文](./for-knowledge-worker.zh-Hans.md) | [English](./for-knowledge-worker.en.md)

> 🚀 **完全沒開發背景？** 多數知識工作者可以直接從 Claude.ai / Claude Desktop 開始、**不需要任何 setup**。只有當你要接 MCP server（如 Gmail / Notion）或用 CLI 自動化時、才需要看 [`resources/setup-guide.md` A-D](../resources/setup-guide.md)（30-45 分鐘從零）。

> [← 回主路線 README](../README.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 後從這裡接續。把 agentic AI 應用到辦公室 / 知識工作上。

## 使用情境（辦公場景 × AI 怎麼幫）

下表把知識工作者一天會遇到的 7 個情境拆開——多數場景在 Claude Desktop + MCP（Tier 1）就能搞定：

| 場景 | 你常遇到的痛點 | AI 能幫的部分 | 推薦工具 |
|---|---|---|---|
| **Email 分流** | 每天 100 封看不完、優先順序錯 | 分類 + 草擬回信讓你 review | Claude Desktop + Gmail MCP |
| **會議 → 行動項目** | 聽完 30 分鐘忘一半、action item 沒記 | 逐字稿 → 主要決策 + 行動項目 | Otter / Zoom 逐字稿 + Claude |
| **跨工具報告整合** | Slack / Gmail / Notion 各一塊、要手動拉 | 自動拉指標 + 整合 + email summary | n8n / Make / Langflow |
| **研究 / 市場情報** | 不知問什麼問題、不知該信誰 | 多源搜尋 + 交叉驗證 + 備忘錄 | Perplexity + Claude |
| **Slack / 訊息** | 拿捏不準口氣、敏感場景 | 改寫 + 調語氣 + 多版本 | Claude.ai |
| **Notion / 知識庫整理** | 雜亂、沒架構、找不到舊筆記 | 重 tag + 分類 + 自動摘要 | Claude Desktop + Notion MCP |
| **文件 / 提案草稿** | spec / proposal 卡關 | 大綱 → 段落 → 潤色 | Claude.ai |

> 💡 **MCP 是知識工作者的關鍵**：第一次接觸 MCP？看 [Stage 5.2 — MCP 基礎](../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎)；想知道有哪些 MCP server → [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)。

## 精選 Projects

> 💡 **想把 AI agent 接到 Notion / Gmail / Outlook / Slack / Excel / 飛書？**（例：把 Gmail 來信自動整理成 Notion 待辦）81+ 個常用辦公整合工具表見 [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)（按使用情境分類）。下面這節保留 workflow / 整合平台級的工具。

### 工作流工具

#### [n8n](https://github.com/n8n-io/n8n) ⭐⭐⭐⭐
可自架的工作流自動化平台，內建 AI 整合，採用視覺化節點式編輯器。

**適合誰**：要把多個 SaaS 工具串起來時（Slack + Gmail + Notion + AI）。

---

#### [Make.com](https://www.make.com/)（前身為 Integromat）
雲端代管的工作流自動化平台，AI 整合節點功能完整。

---

### 知識工作者 Skills

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐

腦力激盪、規劃、決策類的 skill。

---

### 知識管理 / 個人 AI

#### [khoj-ai/khoj](https://github.com/khoj-ai/khoj) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 36k+ |
| License | AGPL-3.0 |

**教什麼**：自架的「第二大腦」——可以跟 web + 本地文件對話、排程自動化、自訂 agent。

**適合誰**：想自架個人知識庫 + AI assistant 的人。

**備註**：AGPL-3.0 license（傳染性開源）。

---

#### [lobehub/lobehub](https://github.com/lobehub/lobehub) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 81k+ |
| License | LobeHub Community License（基於 Apache-2.0 + 商用附加條款） |

**教什麼**：可部署的多 agent 聊天平台——含 plugin marketplace、知識庫、團隊協作。可自架的 AI workspace 代表選項之一。

**適合誰**：要找可自架的協作 chat workspace。

**備註**：商用使用需確認 LobeHub Community License 的附加條款。

---

#### [langflow-ai/langflow](https://github.com/langflow-ai/langflow) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 147k+ |
| License | MIT |

**教什麼**：視覺化 AI agent 設計平台——適合把客服、報告整理、資料查詢這類流程畫成節點。比 n8n 更專注在 agent 設計（n8n 是泛用工作流）。API / MCP server 部署是進階備註、不必一開始就學。

**適合誰**：寧可拉節點不寫 Python 的知識工作者，或要設計 agent 跟團隊溝通流程的人。

---

#### [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 64k+ |
| License | MIT |

**教什麼**：all-in-one 的私有 RAG 工作平台——上傳文件、建 agent、相容 MCP、預設 on-device。**NotebookLM 的私有 self-hosted 替代方案**。

**適合誰**：知識工作者要私有部署、類 NotebookLM 的工具，避免把資料送到雲端。

---

### 對知識工作者有用的 MCP Server

#### 通訊類 MCP server ⭐⭐⭐⭐
Slack / Gmail / Discord 等。Anthropic 原本維護的 reference server 已於 2025 年重整；目前由社群維護的 server 集中在 [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers#communication) 跟 [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers)，要找最新的 Slack / Gmail / Drive / Calendar MCP server 可以從這兩個清單翻找。

---

## 可以建的流程（按使用頻率）

| 頻率 | 流程 | 怎麼做（≤ 3 步） | 推薦工具 | 適合誰 |
|---|---|---|---|---|
| **每天** | Email 分流 | (1) 掃 inbox<br>(2) 分類成「立即 / 今天 / 這週 / 不用回」<br>(3) 草擬回信讓你 review | Claude Desktop + Gmail MCP | 全知識工作者 |
| **每次會議** | 會議 → 行動項目 | (1) 逐字稿（Otter / Zoom）<br>(2) Claude 抓「主要決策 + 行動項目」<br>(3) 指派 + Slack / email 公告 | Claude.ai + 逐字稿工具 | 主管 / PM |
| **每週** | 跨工具報告 | (1) 從 N 個工具拉指標<br>(2) Claude / n8n 整理<br>(3) email summary 寄出 | n8n / Make / Langflow | 要定期 update 老闆的人 |
| **不定期** | 研究 / 市場情報 | (1) 想清楚問題<br>(2) 多來源搜尋 + 交叉驗證<br>(3) 寫成 1-2 頁備忘錄 | Perplexity + Claude | 分析 / 策略職 |
| **不定期** | Notion / 知識庫重整 | (1) 把散落筆記貼進 Claude<br>(2) 請它重新 tag + 分類<br>(3) 輸出 Notion 結構化格式 | Claude Desktop + Notion MCP | 有 Notion / Obsidian 習慣的人 |

> 💡 **新手起手式**：先把「每天 Email 分流」做一個月、養成「inbox 開 Claude」的習慣、再加其他流程。一次裝太多會養不起來。

## 層級建議

下表是建議的進階路徑：

| Tier | 工具 | 適合誰 | 學習成本 |
|---|---|---|---|
| **Tier 0** | Claude.ai / ChatGPT / Gemini / Perplexity（網頁版） | 大多數知識工作者從這裡開始 | 0（會用瀏覽器就行） |
| **Tier 1** | Claude Desktop + MCP（Gmail / Notion / 行事曆） | 要對本機 / 雲端檔案重複跑流程 | 半天裝好 |
| **Tier 2** | n8n / Make / Langflow（自動化平台） | 要把多個 SaaS 工具串起來、不寫 code | 1 週 setup |
| **Tier 3** | Claude Code / Codex / 自己寫 Python | 有 dev 背景或團隊有 dev 支援、要做能上線部署的成果 | 數週、跟 Track A 重疊 |

**Tier 3+（CLI / SDK）對多數知識工作者任務來說太重**——不要被別人慫恿過去。多數人停在 Tier 1-2 就夠。

## 閱讀

- [How I Turned Claude Code Into My Personal AI Agent OS](https://aimaker.substack.com/p/how-i-turned-claude-code-into-personal-ai-agent-operating-system-for-writing-research-complete-guide) — 知識工作者個案研究
- [**Anthropic — The Founder's Playbook**](https://claude.com/blog/the-founders-playbook) — Anthropic 2026-05-14 發布的 35 頁 startup 指南;Idea / MVP / Launch / Scale 四階段對應到 2026 AI capability

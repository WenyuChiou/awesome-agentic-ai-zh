> **繁體中文** | [简体中文](./cli-agents-guide.zh-Hans.md) | [English](./cli-agents-guide.en.md)

# CLI Agents 比較指南

> [← 回主路線 README](../README.md)

> 📌 **這份是 reference doc**（深度比較、選擇邏輯、坑、推薦搭配）。
> 第一次接觸 CLI agent、想要 step-by-step 上手 → 看 [`tracks/cli/A1-cli-intro.md`](../tracks/cli/A1-cli-intro.md)（Track A 第一站）。
> 想先理解「為什麼有的 agent 在 terminal、有的在 Telegram、有的在 Jetson」這層 mental model → 看 [`resources/agent-paradigms.md`](agent-paradigms.md)（5 種 agent 型態）。
> 已經在用、想決定 / 比較 / 升級 → 留在這份。

跨 5 個 branch + Track A 共用的參考——**Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent / Grok Build 之間怎麼挑？** Track A（A1-A3）的 CLI workflow 設計、5 條 branch 內的 CLI 引用都連到這份；每個 branch 都會用到 CLI agent，但沒有一個 branch 真的「擁有」這份比較，所以放在 `resources/`。

---

## 📋 8 個主流 CLI agent

只列在 terminal 跑的（IDE-based 如 Cursor / Cline / Continue 不在這份；那些放在 [for-developer](../branches/for-developer.md)）。前 6 個數字 `gh api` 驗證於 2026-05-06；Hermes Agent 驗證於 2026-05-10；Grok Build 驗證於 2026-07-16（⚠️ 2026-07-14 才開源、非常新，數字與功能都還在快速變動）。

| 工具 | 提供者 | License | 主推 LLM | 認證 / 計費 | Stars |
|---|---|---|---|---|---|
| [Claude Code](https://github.com/anthropics/claude-code) | Anthropic（官方） | NOASSERTION | Claude | Claude 訂閱 **或** Anthropic Console API key | ★ 140k+ |
| [Codex](https://github.com/openai/codex) | OpenAI（官方） | Apache-2.0 | GPT 系列 | ChatGPT 帳號登入 **或** OpenAI API key | ★ 115k+ |
| [OpenCode](https://github.com/sst/opencode) | 社群（repo 已遷至 `anomalyco/opencode`） | MIT | 任意（多 provider） | BYO API key 或 OpenCode Zen 內建 hosted | ★ 190k+ |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Google（官方） | Apache-2.0 | Gemini | 免費額度寬，超出收費 | ★ 103k+ |
| [goose](https://github.com/block/goose) | Agentic AI Foundation（repo 已遷至 `aaif-goose/goose`） | Apache-2.0 | 15+ provider（含 Ollama） | BYO API key 或既有 Claude / ChatGPT / Gemini 訂閱（ACP） | ★ 51k+ |
| [Aider](https://github.com/Aider-AI/aider) | Aider-AI（社群） | Apache-2.0 | 任意 | BYO API key | ★ 47k+ |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Nous Research | MIT | 200+ via OpenRouter / NVIDIA NIM / 智譜 GLM / Kimi / 小米 MiMo / MiniMax / HF / OpenAI | BYO API key（多 provider） | ★ 224k+ |
| [Grok Build](https://github.com/xai-org/grok-build) | SpaceXAI（xAI，官方） | Apache-2.0 | Grok | 首次啟動開瀏覽器完成登入 | ★ 25k+ |

---

## 🎯 該選哪個？依 use case 決定

### 寫 paper / 文獻 / 研究
**首推**：Claude Code（長 context、reasoning 強、擋幻覺扎實）。Gemini CLI 是備選——它的百萬 token 適合丟整本 PDF / dataset 進去問。

### 寫 code / 改 codebase
**首推**：Aider（git-native——每次改完自動 commit，方便 revert）或 Claude Code。OpenCode 適合需要在多 LLM 間切的場景。

### 隱私 / offline / 不送雲端
**首推**：goose 或 OpenCode + 本地 Ollama。兩個都支援 BYO LLM，可以接 `http://localhost:11434/v1`（Ollama 預設）。

### 已訂 ChatGPT Plus / Pro
**首推**：Codex——同一個帳號就能用，不另外付費。

### 用 Google 生態 + 想要 1M token 長 context
**首推**：Gemini CLI。免費額度寬、長 context 是強項。注意：Google 服務（Gmail / Drive / Docs）的整合靠 MCP 擴充，不是內建——跟其他 CLI 一樣需要安裝 MCP server。

### 不想被 vendor lock-in
**首推**：OpenCode > goose > Aider。三個都不綁特定 provider，模型可換。

### 第一次裝 CLI agent，先試手感
**首推**：Claude Code。生態廣泛、CLAUDE.md 機制讓 prompt 可以版本控制、出問題時社群資源多。

### 想跑在 cloud VM、用 Telegram / Slack 等多平台跟它聊 + 用中國大陸 LLM
**首推**：Hermes Agent。差異化在三件事：

- **不綁 laptop**——agent 跑在 $5 VPS / Modal serverless，你從 Telegram / Discord / Slack / WhatsApp / Signal 任一個介面對話
- **多 LLM 中性**——支援 GLM / Kimi / 小米 MiMo / MiniMax，剛好對應 11 中文圈生態
- **內建 self-improving skill loop + cron 排程**——agent 跟你互動久了會自動生成 skill，跨 session 持續優化
- ⚠️ skill 自動演化是 frontier feature，目前缺獨立審計；對 production 任務建議先在低風險場景試

---

## 📝 跨 CLI 都通用的 prompt 寫法

如果想讓 prompt 在不同 CLI 之間 portable（或想隨時換工具不重寫），照這幾條原則：

1. **明確指定檔案路徑**——「修改 `src/auth.py`」比「修改那個 auth 檔」好
2. **要求多步驟拆解**——`先列 plan、確認後再動手`，所有 CLI 都吃這個結構
3. **避免依賴特定 CLI 的 magic 指令**——`/init` `/compact` 是 Claude Code 專屬，OpenCode 沒有
4. **用 `.cursorrules` / `CLAUDE.md` / `AGENTS.md` 記持續性偏好**——Claude Code 用 `CLAUDE.md`，Codex 用 `AGENTS.md`，OpenCode 用 `OPENCODE.md`，**內容可以一樣**
5. **明確要 review 的 scope**——「只 review 我這次的 diff」vs 「review 整個 repo」

跨 CLI 寫的 prompt 通常會比 CLI-specific prompt 麻煩 5-10%，但好處是切換工具時不用重寫。

---

## ⚠️ 常見坑

### File path 處理
- Windows 路徑用反斜線（`C:\Users\...`），多數 CLI 內部會轉，但有時會搞混
- 建議：在 git-bash / WSL 下用 forward slash，避免奇怪 quoting

### git 整合差異
- **Aider** 自動 commit 每次改動（這是它的設計，不是 bug）
- **Claude Code / Codex / OpenCode / goose** 預設不自動 commit，需要手動或 prompt 要求

### Sandbox 預設值（每個 CLI 文件略有差異，使用前請對照官方文件）
- **Claude Code**：bash 寫入預設限定 cwd，讀取範圍較廣（被 deny rule 排除的除外）
- **Codex**：版本控制目錄建議 `Auto`（workspace-write + on-request 提權）；非 git 目錄建議 `read-only`
- **goose / OpenCode**：相對寬鬆——建議自己加 sandbox / approval 設定，不要靠預設

### Token cost 累積
- 在大 codebase 上跑 `grep` 一次可能消耗 10 萬+ token
- 在大 PDF 上摘要可能 50 萬 token（Gemini 適合，其他要 cost-aware）
- 建議：每次操作前估 cost；訂 monthly cap

### 多 CLI session 互相干擾
- 同一個 repo 開兩個 CLI（譬如 Claude Code + Aider），改檔可能 race condition
- 建議：一個 repo 一個 CLI（除非真的有並行需求）

---

## 🔧 實用搭配（real-world setup）

下面 3 個常見搭配，挑一個合的場景：

### Setup A：Claude Code 主推 + OpenCode 備援
- Claude Code 處理日常 90%（寫 code、寫 doc、debug）
- OpenCode 接 Ollama，處理隱私資料（醫療紀錄、財務分析）
- 一個 prompt 寫一次，兩邊都能跑

### Setup B：Codex（GPT）+ Aider（Claude）混用
- Codex 處理 ChatGPT Plus 額度內的小事
- Aider 接 Claude API key 處理大重構（git-native commit 方便）
- 兩個帳單分開算、互不影響

### Setup C：Gemini CLI 主推（給長 context 場景）
- 整本 PDF / 整個 codebase 一次餵進去
- 加 Aider 處理需要精準 git diff 的場景
- 適合學者、知識工作者

### Setup D：Hermes Agent + 本機 Ollama（多平台 + 中國大陸 LLM + offline）
- **Hermes Agent** 跑在 $5 VPS 或自己的機器上，當作多平台 agent gateway
- **LLM endpoint** 用 Ollama（`http://localhost:11434/v1`），也可以改接 z.ai GLM / Kimi 等 provider
- **聊天入口** 用 Telegram / Slack / Discord；Hermes 負責把平台訊息轉進 agent workflow
- **完全不想接 Anthropic / OpenAI** 時，這條路線適合做離線、隱私資料、低成本重複實驗
- Step-by-step 做法看 [`resources/cookbook.md` Recipe 6](cookbook.md#6-本機-llm--cli-agent-快速-walkthrough)

---

## 從這份指南連回各 branch

不同 audience 對 CLI 的需求不一樣：

- **[for-developer](../branches/for-developer.md)**：除了 CLI，也看 IDE-based agents（Cursor、Cline、Continue）
- **[for-everyday-users](../branches/for-everyday-users.md)** Tier 2：CLI 是進階選項，先試 Tier 0 / 1 的 Web / Desktop App
- **[for-researcher](../branches/for-researcher.md)**：除了 CLI，也看 paper-specific 工具（paper-qa、gpt-researcher、ChatPaper）
- **[for-knowledge-worker](../branches/for-knowledge-worker.md)**：除了 CLI，也看 workflow 自動化（n8n、Make）
- **[for-teacher](../branches/for-teacher.md)**：CLI 對教師偏進階；建議先看 prompt 素材庫

---

## 維護備註

- 8 個 CLI 的 stars / license / pushed_at 由 `weekly-catalog-refresh` CI 每週自動更新（手動可跑 `python scripts/refresh-stars.py`）
- CLI 工具市場變化快——新工具出現要評估是否加入這份比較（門檻：> 30k stars + 維護中 + 真的 CLI 不是 IDE；官方大廠或極新的 CLI 可破例、如 Grok Build）
- 比較表格的「強項 / 弱項」欄位刻意沒填——避免產生主觀 bias，讓 use case section 跟讀者自己的判斷做這件事

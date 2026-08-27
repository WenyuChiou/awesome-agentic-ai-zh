# A1 — 選一個 CLI Agent，開始用它做事（CLI Agent Intro & Selection）

> **繁體中文** | [简体中文](./A1-cli-intro.zh-Hans.md) | [English](./A1-cli-intro.en.md)

> [← 回主路線 README](../../README.md) · **Track A: CLI Power User** 第 1 站

⏱ **時間估算**：1 週（約 5-10 小時）

> 📋 **本章組成**：學習目標 → 進入條件 → 必修閱讀 → 動手練習 → 精選 Projects → 自我檢查
> 🔑 **關鍵名詞**：本頁只用到 **CLI agent**（在終端機跑的 AI 工具）。MCP / Skill / plugin 等其他生態名詞會在 A2 / A3 第一次使用時再解釋。完整詞表見 [`resources/glossary.md`](../../resources/glossary.md)。

讀完 Stage 0-2 之後、你想直接用現成的 CLI agent 把工作做完、**不打算自己寫 agent 程式、只想先用現成工具完成任務**？這條軌就是給你的。第一站：**選一個 CLI agent、跑起來**。

## 📌 學習目標

完成這一節後你會：

- 知道 8 個主流 CLI agent（Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent / Grok Build）的差別
- 依自己的場景挑出第一個 CLI 工具
- 完成安裝 + 認證 + 第一個真正的任務（不是 hello world）
- 知道什麼時候該換 / 加第二個 CLI

## 🚪 進入條件

你應該已經：

- 跑過 Stage 0 的 練習：CLI（會用命令列）
- 有 Claude / OpenAI / Google 任一個帳號（不一定是付費）
- 對 prompt 寫法基本上手（Stage 2）

## 📚 必修閱讀

1. [**`resources/agent-paradigms.md`**](../../resources/agent-paradigms.md) ⭐ — 5 種 agent 型態的全景圖；先讀這份知道 CLI agent 在整個 agent 生態中的位置（Type 2 + Type 3）
2. [**`resources/cli-agents-guide.md`**](../../resources/cli-agents-guide.md) ⭐ — 本軌的核心參考。8 個主流 CLI agent 並列比較、依 use case 推薦、實用搭配
3. [**Anthropic — Claude Code Quickstart**](https://code.claude.com/docs/en/quickstart) — 官方安裝指南
4. [**OpenAI — Codex Quickstart**](https://github.com/openai/codex/blob/main/README.md) — Codex 安裝跟認證流程

## 🛠 動手練習（基礎 illustrative 練習）

### 動手練習 CLI-1：安裝 + 第一次跑

**3 步走完**：

1. **裝**：照你選的 CLI 的 quickstart 安裝（每個 CLI 官網都有 ≤ 5 分鐘的安裝指南）
2. **挑一個低風險真實任務**：不要寫「hello world」——挑一件你今天本來就要做的事（例：「整理我 Downloads 資料夾、把 PDF 全部 move 到 ~/Documents/PDFs」）
3. **觀察 3 件事**：它怎麼分解任務、何時要求確認、輸出格式如何

→ 用真任務跑、才能感受 agent 跟 chatbot 的差別。

### 動手練習 CLI-2：CLI 內建的 system prompt 檔
- Claude Code → 寫一個 `CLAUDE.md` 在 repo 根目錄
- Codex → 寫 `AGENTS.md`
- Gemini CLI → 寫 `GEMINI.md`
- goose / OpenCode → 看各自的設定

寫進去 3 件事：「你的個性 / 偏好的 code style / 不能做的事」。再跑一個任務，觀察行為差異。

### 動手練習 CLI-3：第二個 CLI 並用
裝第二個 CLI（建議 Codex 或 OpenCode 當 backup）。用同一個 prompt 跑，比較輸出風格、速度、cost。**不是要選一個贏家——是要學「不同 CLI 解同一個問題的角度不同」**。

### 動手練習 CLI-4：認證細節
故意把 API key 弄錯一個字元，看 CLI 怎麼報錯。再做一次「正確 key 但 model 名稱錯」的實驗。Production 用一定會遇到 auth 問題，先在這裡踩過。

## 🎯 精選 Projects

按用途分 2 類、10 個項目一張表搞定。**挑入口看「適合誰」、想深入細節（強弱項、推薦場景、實用搭配）→ [`resources/cli-agents-guide.md`](../../resources/cli-agents-guide.md)**。

| 分類 | Project | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|---|
| **8 個主流 CLI agent** | [anthropics/claude-code](https://github.com/anthropics/claude-code) | ⭐⭐⭐⭐⭐ | **推薦作為第一個 CLI agent** | 內建 SKILL / plugin 生態、CLAUDE.md prompt 系統、最完整的中文社群資源（★ 140k+） |
| | [openai/codex](https://github.com/openai/codex) | ⭐⭐⭐⭐⭐ | 已訂 ChatGPT Plus / Pro 的人 | 用同一帳號就能在終端機跑（★ 115k+） |
| | [sst/opencode](https://github.com/sst/opencode) | ⭐⭐⭐⭐⭐ | 要 self-host / 不想 vendor lock-in | 開源、不綁 LLM provider、社群迭代最快（★ 190k+） |
| | [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | ⭐⭐⭐⭐ | 處理大 codebase / 大 PDF | 1M token 長 context（★ 103k+） |
| | [block/goose](https://github.com/block/goose) | ⭐⭐⭐⭐ | 想用既有 Claude/ChatGPT/Gemini 訂閱 + Ollama 本機 | 15+ provider 支援（含 Ollama），★ 51k+。**已遷至 `aaif-goose/goose`（AAIF / Linux Foundation）** |
| | [Aider-AI/aider](https://github.com/Aider-AI/aider) | ⭐⭐⭐⭐⭐ | 要寫 code、想要 git 流程乾淨 | git-native、自動 commit / branch（★ 47k+） |
| | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | ⭐⭐⭐⭐⭐ | 想要 cloud-deployed agent（Telegram / Discord / Slack 介面）+ 中文 LLM 生態 | 自動演化型 agent、200+ provider routing、含 GLM / Kimi / 小米 MiMo / MiniMax、內建 cron + skill 自動演化迴圈（★ 數據截至 2026-05；以官方 GitHub 為準）。⚠️ 自動演化 skill 是實驗性功能、缺第三方獨立審計、production 用前請自行驗證安全性與維護狀態、先在低風險場景試 |
| | [xai-org/grok-build](https://github.com/xai-org/grok-build) | ⭐⭐⭐ | 已在用 Grok / X 生態、想嘗鮮的人 | SpaceXAI（xAI）官方 TUI coding agent、Rust、支援 headless / ACP 編輯器嵌入（★ 25k+）。⚠️ 2026-07-14 才開源、非常新——先觀察、不建議當第一個 CLI agent |
| **進階：互補工具**<br>（不是 CLI、但常搭配） | [LM Studio](https://lmstudio.ai/) | ⭐⭐⭐ | Windows / Mac 不想學 command line、想跑本機 LLM | 非開源 desktop app、拖拉介面跑本地 LLM |
| | [Ollama](https://github.com/ollama/ollama) | ⭐⭐⭐⭐⭐ | 想本機跑 LLM 給 CLI agent 用 | 本地 LLM runner、跟 OpenCode / goose 搭配（也能單獨提供 OpenAI-compatible API），★ 170k+。詳見 [Stage 1 — Local LLM 執行](../../stages/01-llm-basics.md#練習-6local-llm) |

> 💡 **建議入手路徑**：第一個 CLI 選 Claude Code（生態最完整）→ 試裝第二個（Codex / OpenCode）感受風格差異 → 想跑本機就加 Ollama → 想 cloud-deployed 跨平台用 Hermes Agent。

## ✅ 進 A2 前的自我檢查

你能不能：

- [ ] 講得出 8 個主流 CLI 的核心差別（不查表就答得出 3-4 個）
- [ ] 你已經選定一個主用 CLI，並有 working setup（裝好、認證好、跑過至少 5 個非 hello-world 任務）
- [ ] 寫過你自己的 `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`
- [ ] 至少跑過第二個 CLI 一次，知道兩個的風格差異

如果可以 → 進 [A2 — CLI Workflow Patterns](A2-cli-workflow.md)。

如果不行 → 別跳。CLI 工具會用得 sloppy 不會用得 productive；A1 的 動手練習 CLI-1/2 至少各跑 3 次再走。

## 💡 給 Track A 學習者的提醒

CLI agent 跟 web 版（Claude.ai / ChatGPT）的差別不是「一樣的東西換介面」——CLI 能讀寫你電腦上的檔案、執行 shell 指令、改 git。這個能力差異**先了解再用**：

- 第一週：每個任務都加 `--dry-run` 或先 review 計畫再執行
- 不要直接讓 CLI 對 production codebase 做 commit
- 重要資料（key、合約、病歷）放在 `.cursorignore` / `.claudeignore` 排除

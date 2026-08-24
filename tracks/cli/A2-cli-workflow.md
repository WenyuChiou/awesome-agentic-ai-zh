# A2 — 建立可重複使用的 CLI 工作流程（CLI Workflow Patterns）

> **繁體中文** | [简体中文](./A2-cli-workflow.zh-Hans.md) | [English](./A2-cli-workflow.en.md)

> [← A1 — CLI 入門](A1-cli-intro.md) · **Track A: CLI Power User** 第 2 站

⏱ **時間估算**：1-2 週（約 8-15 小時）

> 📋 **本章組成**：學習目標 → 進入條件 → 必修閱讀 → 動手練習 → 精選 Projects → 自我檢查
> 🔑 **關鍵名詞**：見 [`resources/glossary.md` 5](../../resources/glossary.md#5-claude-code-生態)（CLAUDE.md / slash command / SKILL.md / plugin / portable prompt）

裝好 CLI、跑過第一個任務之後，下一個問題：**怎麼讓 CLI 一致地、可重複地、可分享地做事**？這節講 workflow pattern——把「我每次都要重打一遍 prompt」變成「設好一次後 CLI 自己會用對方法」。

## 📌 學習目標

- 寫一份實用的 `CLAUDE.md` / `AGENTS.md`——實用的最低構成：**(1) 角色** + **(2) 專案背景** + **(3) 禁止事項** + **(4) 測試指令** + **(5) 交付格式**。實務上 30-50 行可同時涵蓋這 5 件事；超過 50 行通常該拆檔
- 設計可重複的 slash command / custom prompt
- 把多步驟任務拆成 CLI 能跑完的小步驟
- 設計 prompt 讓任務在不同 CLI 上 portable

## 🚪 進入條件

你應該已經：

- 完成 [A1](A1-cli-intro.md)：選定主用 CLI、裝好、認證好、跑過至少 5 個非 hello-world 任務
- 寫過 1 份 `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`（即使只是試水溫）
- 對 Stage 2 prompt engineering 基礎上手

沒到的話 → 先回 [A1](A1-cli-intro.md) 把 CLI-1/2 練熟。

## 📚 必修閱讀

1. [**Anthropic — CLAUDE.md best practices**](https://code.claude.com/docs/en/memory) ⭐
2. [**Stage 2 — Prompt 設計**](../../stages/02-prompt-engineering.md) — workflow design 跟 prompt design 是同一件事的兩面
3. [**Stage 5.1 — Claude Code 基礎**](../../stages/05-claude-code-ecosystem.md#51--claude-code-基礎) — slash commands 細節
4. [**`resources/cli-agents-guide.md`** 「跨 CLI 都通用的 prompt 寫法」](../../resources/cli-agents-guide.md) — portable prompt 原則

## 🛠 動手練習

### 動手練習 CLI-5：寫 production CLAUDE.md
你 CLAUDE.md 應該至少包含：

- **角色**：「你是一個 senior Python engineer / 學術寫作助手 / 等」
- **這個 repo 的 context**：是什麼專案、用什麼套件、有什麼 convention
- **不能做的事**：別亂改 main、別動 secrets、別 commit
- **怎麼做事**：先 plan、跑 test 再 commit、要寫 type hint
- **常用指令**：怎麼跑 test、怎麼 lint、怎麼 deploy

把這份提交到 git。下次新成員 clone repo，他的 Claude Code 自動載入你的 convention。

### 動手練習 CLI-6：第一個 slash command
寫 `.claude/commands/review.md`（或對應 CLI 的位置）：
```markdown
---
name: review
description: Review staged changes for security + style
---

請執行以下流程：
1. `git diff --cached` 抓 staged 的 changes
2. 找：hard-coded secrets、SQL injection、type errors
3. 對應 CLAUDE.md 內的 style 規則檢查
4. 輸出：PASS / 或 list of 具體要改的點
```
之後每次 `/review`，CLI 都跑同一套流程。

### 動手練習 CLI-7：多步驟任務拆解
給 CLI 一個複雜任務（譬如「把這 50 個 markdown 翻譯成英文 + 加 frontmatter + 移到 en/ 子目錄」）。

- 第一次：直接丟整個任務 → 觀察 CLI 怎麼做、什麼地方會錯
- 第二次：你先拆成 5 個 sub-task，逐一給 CLI → 觀察結果差別
- 學到：CLI 跟你一樣，太大的任務要拆；給太小的任務又會 over-orchestrate

> ⭐ **進階補充：Claude Code 原生 multi-agent 機制**（這 1 句先看就好、不展開）：CLI-7 教的「手動拆 sub-task」其實 Claude Code 有 **Subagent / Agent team / Background agent** 三種原生工具可以自動化。完整 3 種機制 + 動手練習 + 何時不該用（團隊權限、上下文隔離、結果審查流程都要先想好）見 **[Stage 5.5](../../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)**——在 A2 階段先知道有這層、不需要學細節。

### 動手練習 CLI-8：Portable prompt
寫一個 prompt 給 Claude Code 跑成功了。**換到 Codex / OpenCode / Gemini CLI 跑同一個 prompt**——什麼地方需要改？通常會發現：

- file path convention 不同（cwd vs absolute）
- 對「執行 shell」的權限預設不同
- 「先 plan 再做」的 prompt 在某些 CLI 要明確說，在某些是預設行為

把這些差異整理成你自己的 cheat sheet。

## 🎯 精選 Projects

按用途分 4 類、7 個項目一張表搞定。**挑入口看「適合誰」、想深入細節點連結看 repo**。

| 分類 | Project | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|---|
| **CLAUDE.md 範例庫** | [Anthropic 官方 CLAUDE.md 指南](https://code.claude.com/docs/en/memory) | ⭐⭐⭐⭐⭐ | 第一份 CLAUDE.md 從這抄結構 | Claude Code repo 自己的 CLAUDE.md、官方寫法 |
| | [obra/superpowers](https://github.com/obra/superpowers) | ⭐⭐⭐⭐ | 看實際在用的 `.claude/` 完整目錄結構 | 不只是 skill collection、也是 CLAUDE.md 範本（★ 265k+） |
| | [mattpocock/skills](https://github.com/mattpocock/skills) | ⭐⭐⭐⭐ | 想看工程師日常用的 skill 庫 | `.claude/` 結構是好參考。**更多 skill 範例見 [Stage 5.3](../../stages/05-claude-code-ecosystem.md#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層)** |
| **Slash Commands / Custom Prompts** | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | ⭐⭐⭐⭐⭐ | 找官方 plugin 範本 | 官方 plugin marketplace、每個 plugin 內的 commands / skills 是 slash command 範例（★ 32k+） |
| | [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | ⭐⭐⭐ | 想逛社群 slash command 範例 | 社群整理的 Claude Code 資源清單 |
| **Prompt 設計參考** | [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) | ⭐⭐⭐⭐ | 卡關時找 CLI 通用的 prompt 模式 | ChatGPT 起家、prompt 寫法 90% 在 CLI 上也通（★ 166k+、CC0）。完整 prompt engineering 進階見 [Stage 2 精選 Projects](../../stages/02-prompt-engineering.md#-精選-projects)（DSPy、dair-ai 等） |
| **多 CLI 並用 pattern** | [`resources/cli-agents-guide.md`](../../resources/cli-agents-guide.md) 「3 個常見搭配」 | ⭐⭐⭐⭐ | 想試多 CLI 配對策略 | 本 repo 內部資源、看 Setup A / B / C 挑一個合的試 |

> 💡 **建議入手路徑**：先抄 Anthropic 官方 CLAUDE.md 結構 → 加自己的 repo context → 看 obra/superpowers 看「完整 `.claude/` 長什麼樣」→ 然後寫 1-2 個 slash command（從 hesreallyhim awesome 列表撈靈感）。

### 推薦工具

- [**yamadashy/repomix**](https://github.com/yamadashy/repomix) ⭐⭐⭐⭐⭐ ★ 27k+ — 把整個 codebase packed 成單一 AI-friendly 檔案（XML / Markdown / JSON），方便 Claude Code / Codex 做 code review / refactoring。內建 MCP server mode + tree-sitter 壓縮（壓縮率依語言與檔案結構而異）+ secretlint 過濾敏感資訊。**Track A 很值得當 daily driver 的工具。**
- [**langchain-ai/openwiki**](https://github.com/langchain-ai/openwiki) ⭐⭐⭐⭐ ★ 15k+ — CLI，自動幫你的 codebase 生成並持續維護一份 wiki，並在 `CLAUDE.md` / `AGENTS.md` 裡加一條指向 wiki 的參照，讓 coding agent 需要時自己去讀、隨程式碼變動自動更新。`npm i -g openwiki` → `openwiki --init`。底層是 DeepAgents、可接 LangSmith 追蹤。MIT。

> 💡 **概念：*agent-facing documentation*（給 agent 讀的文件）。** repomix 跟 OpenWiki 在解同一個痛點（agent 不了解你的 repo），只是切角不同：一個是一次性打包快照，一個是會持續長大、自動維護的 wiki。共同的做法是給 agent *一份它需要時自己去讀的結構化 codebase context*，跟 `CLAUDE.md` 的指令分開放，而不是全部塞進 prompt。

## ✅ 進 A3 前的自我檢查

你能不能：

- [ ] 寫過至少 1 份你 production / 工作 repo 的 CLAUDE.md（不是 demo repo）
- [ ] 寫過至少 2 個 slash command 並實際在用
- [ ] 把同一個 prompt 在 2 個不同 CLI 上跑過、知道差異
- [ ] 講得出「什麼任務該拆、什麼任務不該拆」的判準

如果可以 → 進 [A3 — Integration & Production](A3-cli-production.md)。

如果不行 → CLAUDE.md 一直 demo 等於白寫；先去你真實 repo 寫一份再回來。

## 💡 常見坑

- **CLAUDE.md 寫太長**：超過 100 行 CLI 會自己 truncate / 忽略後段。Sweet spot 30-60 行。
- **Slash command 寫成「請做 X、Y、Z、A、B」一句**：CLI 容易跳步驟。改寫成編號 list + 每步成功標準。
- **Portable 過頭**：每個 CLI 還是有自己的特長；不要為了能跨 CLI 把 prompt 變得太抽象、失去具體性。
- **覺得自己「都會」就不寫了**：CLAUDE.md 是給未來的你（跟新成員）看的，不是給現在的你看的。

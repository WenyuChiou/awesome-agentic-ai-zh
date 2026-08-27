# 開發者延伸路線（For Developers）

> **繁體中文** | [简体中文](./for-developer.zh-Hans.md) | [English](./for-developer.en.md)

> 🚀 **第一次裝 Claude Code / 寫 `CLAUDE.md` / `SKILL.md`？** 快速 setup 指南在 [`resources/setup-guide.md` D-E](../resources/setup-guide.md)。已經熟可以跳過。

> [← 回主路線 README](../README.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 後從這裡接續。把 agentic AI 應用到開發流程上。

## 使用情境（開發場景 × AI 怎麼幫）

下表把開發者一天會遇到的 7 個情境拆開——每個情境有不同的痛點，AI 工具也不同：

| 場景 | 你常遇到的痛點 | AI 能幫的部分 | 推薦工具（從輕到重） |
|---|---|---|---|
| **AI 結對程式設計** | 寫到一半忘 syntax / 想到 method 名 | 自動補完 + 改寫 + 解釋 | Cursor / Copilot → Claude Code |
| **多檔重構** | 改一個 class 怕漏改、跨檔 rename 易錯 | batch refactor、改 50 個檔保持風格一致 | Cursor → Claude Code → codex-delegate |
| **Code review（自己 PR）** | review 自己的 diff 看不出問題 | 找 bug / smell、檢查 edge case | Claude Code / cline → Continue（CI） |
| **寫 test** | TDD 一直忘加 case、coverage 不足 | 從 signature / spec 生 pytest | Claude Code + Aider |
| **Debug** | log 不夠、stack trace 看不懂 | 解 trace、生 hypothesis、跑 minimal repro | Claude Code |
| **Doc** | docstring / README 沒人寫、refactor 後過期 | 從 code 生 doc、PR 對應改 doc | Claude Code |
| **CI / 團隊自動化** | 重複手動跑 review、跨人風格不一 | GitHub Action 自動跑 review / lint | Claude Code Action + Continue |

> 💡 **個人 vs 團隊**：表中前 6 個是個人 daily workflow；最後 1 個（CI）是團隊規範。團隊規模 < 5 人時 CI 自動化的 ROI 不高、可先不上。

## 精選 Projects

> **CLI agent 身分與選擇指南**：想按工作方式選工具，見 [`resources/cli-agents-guide.md`](../resources/cli-agents-guide.md)。第一次接觸 CLI agent 想要 step-by-step 入門 → [`tracks/cli/A1-cli-intro.md`](../tracks/cli/A1-cli-intro.md)（Track A 第一站）。
>
> **MCP catalog**：要把 CLI 接到日常工具（GitHub、Linear、Atlassian、Postgres、Playwright、Figma 等）→ [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)（81+ 個分類整理）。
>
> 本頁只列**跟開發者 workflow 直接相關**的工具入口。

### Coding Agents

#### [Cursor](https://www.cursor.com/) ⭐⭐⭐⭐⭐
編輯器整合的 AI 結對程式設計工具。在 AI 編輯器類工具中採用度高、可作為比較其他 IDE agent 的基準。

#### [Aider-AI/aider](https://github.com/Aider-AI/aider) ⭐⭐⭐⭐⭐
★ 47k+ · Apache-2.0 — git-aware 的 CLI pair-programmer。直接編輯你 repo 中的檔案，commit 都自動寫好。**「git-native AI 編輯流程」的開源範本**。模型不限。

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 138k+ — Anthropic 官方的 agentic coding 助理。有 Skills + plugin 生態系。

#### [cline/cline](https://github.com/cline/cline) ⭐⭐⭐⭐⭐
★ 65k+ · Apache-2.0 — VS Code extension，autonomous in-IDE agent：tool use、browser、step-by-step approval。**VS Code 使用者要 IDE-native agentic dev 的好選項**。

#### [continuedev/continue](https://github.com/continuedev/continue) ⭐⭐⭐⭐
★ 35k+ · Apache-2.0 — source-controlled AI checks，可以在 CI 強制執行。代表「**團隊 / governance**」這條角度的 coding agent。

#### [OpenHands (前身為 OpenDevin)](https://github.com/All-Hands-AI/OpenHands) ⭐⭐⭐⭐
★ 81k+ · MIT — open source 的自主軟體開發 agent。設計上比 Aider / Claude Code 更激進——agent 自己跑 sandbox、自己 commit，適合「整個 issue 丟給它解」場景。

#### [aaif-goose/goose](https://github.com/aaif-goose/goose) ⭐⭐⭐⭐
★ 51k+ · Apache-2.0 — 開源、可擴充的 AI agent，超出純 code suggestion——能 install / execute / edit / test，搭配任何 LLM。同時支援多家 LLM provider 跟 MCP，提供 desktop app、CLI、API 三種介面。（repo 現指向 `aaif-goose/goose`。）

#### [RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code) ⭐⭐⭐（⚠️ 已封存）
★ 24k+ · Apache-2.0 — VS Code 的 coding agent，採用「**多種專業 mode**」的設計，跟 Cline 的單一 agent flow 不同。**⚠️ repo 已於 2026-05 封存（read-only、不再維護）**——仍可用，但別預期新功能。

### Code Review

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
20+ 個經過實戰驗證的 skill，包括 TDD 模式、debug、協作模式。設計 code-review skill 時的好參考。

### 推薦工具

- [**yamadashy/repomix**](https://github.com/yamadashy/repomix) ⭐⭐⭐⭐⭐ ★ 27k+ — **典型開發者用途：打包整個 codebase 給 reviewer / refactor agent**。輸出單一 AI-friendly 檔案（XML / Markdown / JSON），方便 Claude Code / Codex 做 code review / refactoring。技術細節（MCP server mode、tree-sitter 壓縮、secretlint 過濾）見官方 README。**Track A 很值得當 daily driver 的工具。**

## 必練流程（按使用頻率）

| 頻率 | 流程 | 怎麼做（≤ 3 步） | 推薦工具 | 適合誰 |
|---|---|---|---|---|
| **每天** | AI 結對寫 code | (1) 開 branch<br>(2) 任務丟給 Claude Code、**先 plan**（不寫 code）<br>(3) Review plan → approve → 寫 code → 自己 review diff | Claude Code / Cursor / Cline | 全開發者 |
| **每天** | Git-native AI 編輯 | (1) `aider`<br>(2) 自然語言請求<br>(3) review + commit / `/undo` | Aider | 想要乾淨 git 流程的人 |
| **Per PR** | 自動 code review | (1) `.github/workflows/claude-review.yml`<br>(2) 抓 git diff → 跑 prompt → post 回 PR<br>(3) human + AI 雙審 | Claude Code Action + Continue | 團隊 |
| **Per feature** | 測試生成 | (1) 給 function signature + docstring<br>(2) 請 AI 生 pytest case（含 edge case）<br>(3) 跑覆蓋率 + 故意改 bug 看 test 抓不抓得到 | Claude Code / Aider | 寫 test 階段 |
| **不定期** | 多檔批次修改 | (1) Claude 寫 plan<br>(2) codex-delegate 跑機械式 refactor<br>(3) Claude review diff | Claude + codex-delegate | refactor 30+ 檔的時候 |

> 💡 **新手起手式**：先做「每天 AI 結對」+「測試生成」兩條一個月、習慣後再上 PR 自動 review。

### 3 個具體 workflow recipe

**1. AI 結對程式設計（每日節奏）**

1. 開新 feature → `git checkout -b feature/xxx`
2. 把任務丟給 Claude Code / Cursor，**先讓它寫 plan**（不直接寫 code）
3. Review plan、修正方向 → 才 approve 寫 code
4. 寫完跑 tests + lint → 自己 review diff（**不要 blind accept**）
5. Commit message 自己寫或 prompt 生草稿後改

**2. Aider git-native 流程（最像「跟 AI pair」）**
```bash
# 進入 repo 後
aider --model anthropic/claude-sonnet-5

# 自然語言請求
> 幫我把 utils.py 的 parse_date 加上時區參數，預設 UTC

# Aider 會自動編輯 + commit。若不滿意：
> /undo # 退掉最後一次 AI commit
```

**3. PR 上的 Claude code review（GitHub Action）**

`.github/workflows/claude-review.yml`：
```yaml
on:
  pull_request:
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Run Claude review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # 用 anthropics/claude-code-action 或自寫 script
          # 抓 git diff、跑 prompt、結果 post 回 PR
```
參考 [`anthropics/claude-code-action`](https://github.com/anthropics/claude-code-action) 官方 GitHub Action。

## 常見踩坑（Anti-patterns）

| ❌ 不要 | ✅ 改成 |
|---|---|
| 讓 AI 直接 push 到 main | 永遠 PR → review → merge |
| Blind accept 大規模 refactor diff | 拆成 < 50 LOC 改動，逐個 review |
| 把 .env / API key 丟給 AI 看 | 用工具對應的排除機制：Cursor `.cursorignore` / Aider `.aiderignore` / Claude Code 用 `.claude/settings.json` 的 `permissions.deny` |
| 讓 AI 在 production code 自由跑 shell | sandbox 限制、permission whitelist |
| 用 AI 生 test 後不檢查 assertion | 跑覆蓋率 + 故意改一個 bug 看 test 抓不抓得到 |
| 跨多個 commit 才發現方向錯 | **plan-first** 模式：先 review plan 再寫 code |

## Tier 升級路徑

下表是建議的進階路徑：

| Tier | 工具 | 適合誰 | 學習成本 |
|---|---|---|---|
| **Tier 0** | Cursor / Copilot / Claude.ai | IDE 內 chat、autocomplete、不自己寫 agent | 0（會用編輯器就行） |
| **Tier 1** | Claude Code（`CLAUDE.md`）／Cline／OpenCode V2（`AGENTS.md`） | CLI 接 file system、human-in-the-loop | 1-2 天上手 |
| **Tier 2** | 自寫 Skills + MCP server | 把 dev workflow 包成 skill 給團隊共用 | 1 週 setup |
| **Tier 3** | CI 自動跑 agent + production observability | 進到 [Stage 7](../stages/07-multi-agent-production.md) 領域 | 數週、需 governance |

> **多數個人開發者可先停在 Tier 0-1**。**升級到 Tier 2+ 要先確認 ROI**——團隊夠大、流程夠重複、事故不可逆、才值得 invest。

## 也適用其他分支

開發者重疊度高的分支：

- **要做 ML 研究 / 寫 paper** → [研究員分支](./for-researcher.md)
- **接 Notion / Linear / Atlassian / Postgres / Figma** 等 dev tool → [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)
- **要寫自己的 Skill / MCP server** → [Stage 5](../stages/05-claude-code-ecosystem.md) + [`resources/cookbook.md`](../resources/cookbook.md)
- **想看 schema 設計細節** → [`resources/schema-design-cheatsheet.md`](../resources/schema-design-cheatsheet.md)
- **CLI 從零開始** → [Track A](../tracks/cli/A1-cli-intro.md)（A1 → A2 → A3）

## 社群備註

特別歡迎以下貢獻：

- IDE-specific 設定範本（Cursor `.cursorrules`、Claude Code `CLAUDE.md` for Python / Go / Rust 等）
- 程式語言特化 skill（Python / TypeScript / Rust / Go 各自的 best practice）
- CI / pre-commit hook 整合 case study
- **跨多人團隊用 AI dev 的 governance pattern**——多 dev 共用 Skills、permission 設計、cost tracking

請見 [CONTRIBUTING.md](../CONTRIBUTING.md)。

# Subagent Cookbook — 15 個複製貼上就能用的派遣 recipe

> **繁體中文** | [简体中文](./subagent-cookbook.zh-Hans.md) | [English](./subagent-cookbook.en.md)

> 📋 **這是什麼**：[Stage 5.5](../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能) 教你 subagent 是什麼概念、這份 cookbook 教你**今天就能用**——15 個情境、每個含「該用哪個 subagent + 完整 prompt 範本（複製即可用）+ 何時不用」。
>
> ⚠️ **第一次看？先讀 Stage 5.5 的「可派遣的 subagent 有哪些」+「decision table」兩節**——理解「什麼是 subagent」「Claude Code 內建有哪些」之後再來查 recipe。

---

## 怎麼讀這份 cookbook

每個 recipe 用同樣的 4 段結構：

| 段 | 內容 | 為什麼有這段 |
|---|---|---|
| **情境** | 你今天工作會遇到的具體場景 | 從「我有 X 問題」找到 recipe、不從「我想用 subagent」找 |
| **Subagent** | 用哪一個（Claude Code 內建名稱） | 直接 copy 名字、不用想 |
| **Prompt 範本** | 複製貼上即可用的指令文字 | 不用自己想怎麼寫 |
| **何時不用** | 比用 subagent 更好的替代方案 | 避免「殺雞用牛刀」 |

> 💡 **怎麼實際派遣 subagent**：在你的 Claude Code 終端機對話框裡、**直接輸入（或貼上）prompt 範本**——就這樣。Claude 看到指令、會自動透過 **Agent tool**（內部派遣機制）找到對應 subagent 跑、跑完回主 session 一段摘要。**不需要 slash command、不需要特殊語法**。
>
> 📌 **subagent ≠ slash command**：`/agents` 是查當前可用 subagent 的指令、**不是用來「呼叫」subagent**。派遣 subagent 直接打對話 prompt 文字即可。完整對比表（subagent vs skill / vs slash command / description router）見 [Stage 5.5 §易混淆觀念釐清](../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)。

---

## 先確認你有哪些 subagent 可用

在你的 Claude Code session 內跑 `/agents` 一個指令、會列出全部當前可用的 subagent（內建 + plugin + 自訂）。

**Claude Code 預設內建 7 個** subagent：`general-purpose` / `code-reviewer` / `Explore` / `Plan` / `frontend-developer` / `claude-code-guide` / `statusline-setup`（截至 2025-11、可能會變動）。

> 📌 **每個內建 subagent 的功能說明 + 「遇到 X 任務用 Y」decision table 的 canonical 在 [Stage 5.5 §可派遣的 subagent 有哪些](../stages/05-claude-code-ecosystem.md#可派遣的-subagent-有哪些)**——本 cookbook 聚焦「怎麼派遣」的 15 個 recipe，內建清單與選用邏輯以 Stage 5.5 為準。

> 💡 **如果 `/agents` 列表跟這份 cookbook 不一致**：表示你裝了 plugin 或 Claude Code 版本不同。**recipe 名字對不上時、找最接近的 subagent 用就好**（例如沒有 `Explore`、用 `general-purpose` 也能跑搜尋）。

確認完當前可用清單之後、就可以照下面 15 個 recipe 派遣了——**找到符合你情境的 recipe、複製 Prompt 範本貼進 Claude Code 對話框即可**。

---

## 15 個 Recipe

### Recipe 1: 寫完一批新 code、要 commit 前的 review

**情境**：你剛寫了 ≥ 50 行新 code、想 commit 但怕有 bug / security 問題沒看到

**Subagent**：`code-reviewer`

**Prompt 範本**：
```
Review the staged changes in this repo (git diff --cached).
Focus on: (1) security issues (hardcoded secrets, SQL injection, XSS),
(2) error handling gaps, (3) missing tests, (4) violations of CLAUDE.md
conventions. Per-category PASS/FAIL + concrete fix for each issue with
file:line reference + overall verdict (APPROVE / REQUEST CHANGES).
```

**何時不用**：< 20 行的 typo / formatting fix（直接 `git diff` 自己掃就好、不用花 subagent token）

---

### Recipe 2: 進新 repo、不知該從哪個 file 開始讀

**情境**：複製完一個別人的 repo、`README.md` 講不清楚程式入口在哪、不想隨便挖

**Subagent**：`Explore`

**Prompt 範本**：
```
Map the entry points and core structure of this codebase. Report:
(1) main entry script(s) — what file gets run first,
(2) core module organization — top 3-5 directories and what each does,
(3) test directory layout,
(4) any "where to start reading" guidance in docs/.
Under 300 words with file paths.
```

**何時不用**：你已經知道要看的 file 路徑（直接用 Read tool）

---

### Recipe 3: 設計 refactor / migration plan（先想清楚再動手）

**情境**：要重構一個大 module 或做 framework migration、不確定步驟、想先有 plan 再開始

**Subagent**：`Plan`

**Prompt 範本**：
```
Design a step-by-step plan to refactor <module-name> (currently a single
file with tight coupling) into clear, testable components with explicit
interfaces. Include: (1) phased breakdown (≤ 5 phases), (2) which files
touched per phase, (3) what tests gate each phase, (4) rollback strategy
if a phase fails. Don't write code — just the plan.
```

**何時不用**：refactor 只動 1-2 個 file（直接動手、不需要 plan overhead）

---

### Recipe 4: 多檔 / 跨 locale parity 審查

**情境**：你改了 zh-TW + zh-Hans + en 三個 mirror、想確認三邊內容一致

**Subagent**：`code-reviewer`

**Prompt 範本**：
```
Review the staged diff for cross-locale parity across the 3 locale
variants of <file-stem> (.md / .zh-Hans.md / .en.md). Check: (1) same
section structure (## headers match), (2) same table row counts, (3)
same required terms present in each locale, (4) locale conventions
correct (zh-Hans uses "" not 「」; en uses English). Report per-file
PASS/FAIL.
```

**何時不用**：只改 1 個 locale（沒 parity 問題）

---

### Recipe 5: 多 source fact-check / research

**情境**：要寫一段引用、不確定多個 source 講的是不是同一件事、需要交叉驗證

**Subagent**：`general-purpose`

**Prompt 範本**：
```
Fact-check this claim: "<claim>". Search for: (1) primary source / official
docs / paper, (2) 2-3 independent secondary sources, (3) any contradictions
or version differences. Report: confirmed / contradicted / nuanced, with
direct quotes and URLs. Under 400 words.
```

**何時不用**：你已經有 1 個權威 source（直接讀那一個就好）

---

### Recipe 6: 找某個 symbol / function 在哪定義

**情境**：codebase 內到處在導入 `parse_config`、想知道實作在哪個 file

**Subagent**：`Explore`

**Prompt 範本**：
```
Find where `<symbol-name>` is defined in this codebase. Report: (1) the
file:line where it's defined, (2) what it does (1-line summary), (3) which
files import / use it (top 5). Use Grep, not full file reads.
```

**何時不用**：你已經用 IDE 的 "Go to definition" 可以跳過去（IDE 比 subagent 快）

---

### Recipe 7: 比較多 paper / source 的 claim 是否一致

**情境**：寫文獻回顧、3 篇 paper 對同一件事說法不同、不知該信誰

**Subagent**：`general-purpose`

**Prompt 範本**：
```
Find and compare 3 independent sources on the topic <topic>. For each
source, capture: title + author + year + URL. Then report: (1) what
they agree on, (2) where they disagree (with direct quotes), (3) which
is most recent / authoritative, (4) suggested phrasing if you had to
summarize the consensus. Flag if a key source is behind a paywall and
unreadable.
```

**何時不用**：3 篇都是同一個作者 / 同 lab（沒「多 perspective」可比）

---

### Recipe 8: Release commit security audit

**情境**：要發 v1.0 / 升 major version、想最後一次安全掃描

**Subagent**：`code-reviewer`

**Prompt 範本**：
```
Pre-release security audit for <release-tag> (use git log to find the
relevant commit range since last release). Check: (1) hardcoded
credentials / API keys, (2) eval() / exec() / shell injection risks,
(3) deprecated dependencies with known CVEs, (4) any auth / session
handling changes since last release, (5) public API surface changes
(breaking? documented?). Per-category PASS/FAIL + remediation per
finding.
```

**何時不用**：patch release（hotfix）只動 1 行（人工掃 < 1 分鐘）

---

### Recipe 9: 評估架構變動的 blast radius

**情境**：想改一個 base class / 共用 utility、不確定會影響多少 file

**Subagent**：`Plan`

**Prompt 範本**：
```
Assess the blast radius of changing <component>. Report: (1) direct
dependents (which files import this), (2) indirect dependents (transitive
imports), (3) tests that gate the change, (4) suggested rollout order
(safest → riskiest), (5) feature flag / kill switch strategy if available.
Don't make the change yet — just the impact analysis.
```

**何時不用**：只影響 1 個 file 內部（沒 blast radius 概念）

---

### Recipe 10: Spawn 並行 subagent 跑同一任務 × 多目標

**情境**：4 個 branches file 都要做同樣的「academic-style audit」、想一次跑 4 個 parallel

**Subagent**：`general-purpose` × N（同時 spawn 多個）

> 💡 **怎麼「同時 spawn 多個」**：在 Claude Code 對話框內、**連續輸入下面的 prompt 4 次**（每次換 `<file-path>`）。Claude Code 會自動並行跑、不需要等第一個 subagent 結束才能輸入第二個——這就是「parallel spawn」的實際操作方式。

**Prompt 範本**（每次換 `<file-path>`）：
```
Audit `<file-path>` for academic-style issues: (1) over-engineering
jargon without first-use explanation, (2) clarity (long sentences,
vague pronouns), (3) unsupported % claims, (4) persona-fit (wrong
technical level for the file's stated target audience — see the
file's banner / intro callout for who it's for). Report 4-category
PASS/FAIL + fix-list with line numbers. Under 500 words.
```

**何時不用**：1 個目標就夠（直接呼叫 1 次、不要 over-orchestrate）

---

### Recipe 11: 找跨 repo 的相似 implementation

**情境**：你在某個 repo 看到一個 pattern、想知道另一個 repo 有沒有類似實作

**Subagent**：`Explore`

**Prompt 範本**：
```
In <repo-path>, search for code patterns similar to: <description of
pattern, e.g., "retry decorator with exponential backoff">. Report:
(1) up to 5 candidates with file:line, (2) brief description of each,
(3) which is most idiomatic for this codebase's style.
```

**何時不用**：你有具體 function 名要找（用 Recipe 6 / `Explore` 加精確 grep 更快）

---

### Recipe 12: LLM-as-judge eval（structured PASS / FAIL）

**情境**：跑了 100 個 test case、要評每個 output 是否符合 spec、不想人工看

**Subagent**：`general-purpose`

**Prompt 範本**：
```
Evaluate the agent outputs in <eval-file.jsonl> against the spec stated
in the file's first 5 lines (or in <spec-file.md>). For each row: PASS /
FAIL with 1-sentence reason. Aggregate: pass rate + top-3 failure modes.
Output as structured JSON: {"case_id": "...", "verdict": "PASS|FAIL",
"reason": "..."}.
```

**何時不用**：< 5 個 case（自己看更快）；evaluation 涉及主觀判斷（LLM judge 不可靠）

---

### Recipe 13: UI component design / accessibility audit

**情境**：寫了一個 React component、想確認 ARIA + keyboard nav + responsive 都做對

**Subagent**：`frontend-developer`

**Prompt 範本**：
```
Audit <component-file> for: (1) ARIA roles + labels (screen reader
compatibility), (2) keyboard navigation (tab order, Enter / Esc / arrows
behavior), (3) responsive breakpoints (mobile 360px / tablet 768px /
desktop 1280px), (4) color contrast (WCAG AA), (5) touch target size
(≥ 44px). Report per-category findings + fixes.
```

**何時不用**：純後端 / CLI 工具（沒 UI 可 audit）

---

### Recipe 14: 問 Claude Code feature 怎麼用

**情境**：忘了 hooks 怎麼設、忘了 slash command 的 frontmatter 欄位、想查文件

**Subagent**：`claude-code-guide`

**Prompt 範本**：
```
How do I <specific Claude Code feature question, e.g., "configure a
PreToolUse hook to block dangerous bash commands">? Show: (1) minimum
config in settings.json, (2) example hook script (Python or shell),
(3) 1 common gotcha, (4) where in the official docs to read more.
```

**何時不用**：你已經寫過幾次（直接看自己 `~/.claude/settings.json` 範例更快）

---

### Recipe 15: 寫 React form validation 邏輯

**情境**：要做一個 sign-up form、要 email format / password strength / real-time validation

**Subagent**：`frontend-developer`

**Prompt 範本**：
```
Implement a React sign-up form with: (1) email format validation
(real-time, debounce 300ms), (2) password strength meter (≥ 8 chars,
mixed case, digit, symbol), (3) inline error messages with ARIA
live region, (4) submit button disabled until valid. Use <library, e.g.,
React Hook Form + Zod>. Include: component code, validation schema,
1 happy-path test, 1 error-path test.
```

**何時不用**：非 React stack（用 Vue / Svelte 對應的 subagent、或 `general-purpose`）

---

## Recipe 索引（按 subagent type 找）

不確定該用哪個 subagent？從**任務類型**反查：

| Subagent | Recipes |
|---|---|
| `code-reviewer` | **1**（pre-commit review）/ **4**（cross-locale parity）/ **8**（release security audit）|
| `Explore` | **2**（new codebase）/ **6**（find symbol）/ **11**（cross-repo similar code）|
| `Plan` | **3**（refactor plan）/ **9**（blast radius）|
| `general-purpose` | **5**（fact-check）/ **7**（multi-paper compare）/ **10**（parallel multi-target）/ **12**（LLM-as-judge eval）|
| `frontend-developer` | **13**（a11y audit）/ **15**（React form）|
| `claude-code-guide` | **14**（Claude Code feature 查詢）|

---

## 何時 NOT 該用 subagent

Subagent 不是免費的——每次派遣**燒 token、有延遲**。下面 4 種情境**不該用 subagent**、自己跑更划算：

1. **任務 < 5 分鐘可自己完成** — 殺雞用牛刀；subagent overhead 不划算
2. **結果需要逐步 user feedback** — subagent 是「派出去、跑完回報一次」、不能中間問你；要逐步確認的任務直接在主 session 跑
3. **任務需要主 session 的 context memory** — subagent 是**獨立 context window**、看不到主 session 前面的對話；要用「我們剛剛討論的 X...」這種 reference 的任務、不適合
4. **任務涉及 conversation-level judgment** — 像「這個 architecture 決策該怎麼權衡」、需要對話協作、不適合丟給 subagent

> 💡 **判斷的快速辦法**：如果任務可以用「**寫一份完整 brief 給陌生人接手做**」描述清楚 → 適合 subagent；如果需要「**我跟你討論一下**」→ 留在主 session。

---

## 接下來

- **想理解完整理論**（subagent 跟 skill / MCP 的差別、3 種 multi-agent 機制）→ [Stage 5.5](../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)
- **想自己寫 / 組合 / debug subagent**（進階主題）→ [`subagent-advanced.md`](./subagent-advanced.md)（description 寫法 / composition pattern / debug 工具）
- **CLI 日常用法 playbook** → [`tracks/cli/A3-cli-production.md` Playbook 4](../tracks/cli/A3-cli-production.md#-playbook-4派遣-subagent-跑獨立任務)
- **想看 subagent 在 agent paradigm 體系內的定位** → [`resources/agent-paradigms.md`](./agent-paradigms.md#subagent--在-agent-runtime-裡再-spawn-agent)
- **詞彙快查** → [`resources/glossary.md` § 5. Claude Code 生態 — Subagent](./glossary.md#subagent子-agent)

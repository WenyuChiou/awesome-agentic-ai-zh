# Subagent 進階使用 — Description 寫法 / Composition / Debug

> **繁體中文** | [简体中文](./subagent-advanced.zh-Hans.md) | [English](./subagent-advanced.en.md)

> 📋 **這份是給誰看的**：你已經會用內建 subagent（[Stage 5.5](../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能) + [cookbook](./subagent-cookbook.md) 走完了），準備：(1) **自己寫一個** subagent、(2) **組合多個** subagent、或 (3) **debug** 跑壞的 subagent。
>
> ⚠️ **先決條件**：讀完 Stage 5.5 §易混淆觀念釐清 + cookbook 15 個 recipe 之後再來。沒讀 cookbook 直接看這份會卡在「subagent 是什麼」這層。

---

## 怎麼讀這份文件

3 個獨立的進階主題、按需要查：

| 你的問題 | 看哪節 |
|---|---|
| 寫了一個 subagent，但 Claude 從來不主動派它——為什麼？ | [§1 Description 怎麼寫才會被主 session 主動 spawn](#1-description-怎麼寫才會被主-session-主動-spawn) |
| 想跑 2-3 個 subagent 串成 pipeline / parallel——怎麼設計？ | [§2 Composition pattern 怎麼設計](#2-composition-pattern-怎麼設計) |
| Subagent 跑壞 / 報錯 / 行為跟設定的不一樣——怎麼 debug？ | [§3 自製 subagent 的 debug 工具](#3-自製-subagent-的-debug-工具) |

每節獨立、可跳讀。

---

## §1 Description 怎麼寫才會被主 session 主動 spawn

主 session 怎麼決定派哪個 subagent？看 `.claude/agents/<name>.md` 開頭 frontmatter（**frontmatter** = 檔案最開頭的 YAML 設定區、用 `---` 包起來）的 **`description`** 欄位。**寫法影響被選機率**——下面是 4 個常見 bug + 修正：

### Bug 1: Description 太抽象、Claude 不知何時派

❌ **壞寫法**：
```yaml
description: A helpful code reviewer.
```
**問題**：「helpful」是空詞、reviewer 是泛詞。Claude 看不到「什麼情境下我該派這個」、只能等使用者明白點名。

✅ **改成**（具體觸發條件 + 範圍）：
```yaml
description: Use PROACTIVELY when the user has staged ≥ 50 lines of changes and is about to commit. Reviews staged diff for security issues, style violations, missing error handling, and test gaps. Returns per-category PASS/FAIL + concrete fix list.
```
**為什麼好**：(1) `PROACTIVELY` 是強訊號詞、(2) 明確觸發條件「staged ≥ 50 lines + about to commit」、(3) 列了會做的 4 件事、(4) 講清楚回傳格式。

---

### Bug 2: 用了 `PROACTIVELY` 但條件太寬

❌ **壞寫法**：
```yaml
description: Use PROACTIVELY for all code-related tasks.
```
**問題**：「all code-related」太寬、Claude 會在每個 coding task 都派——使用者輸入「fix this typo」也派 = 騷擾。

✅ **改成**（縮窄條件）：
```yaml
description: Use PROACTIVELY when a commit is about to land that modifies authentication, database queries, or API routes — these are high-risk surface areas needing extra review.
```
**為什麼好**：限定**高風險範圍**（auth / DB / API）、避免 over-trigger。

---

### Bug 3: 完全沒寫 `PROACTIVELY`、只能被動等

❌ **壞寫法**：
```yaml
description: Reviews code when asked.
```
**問題**：沒有 `PROACTIVELY`——Claude 只會在使用者明白要求「review this」時才派；如果使用者沒想到要 review、就漏掉了。

✅ **改成**（加 PROACTIVELY + 觸發場景）：
```yaml
description: Code reviewer. Use PROACTIVELY when staged changes touch test files but the test count didn't increase — likely missing test coverage for new logic.
```

> 💡 **被動 vs 主動的選擇**：
> - **想 always-on safety net**（譬如安全 review）→ 用 `PROACTIVELY` + 明確 trigger
> - **只在使用者明白要求才跑**（譬如比較費 token 的 deep research）→ 不寫 `PROACTIVELY`、改用 `use when user asks for ...`

---

### Bug 4: Description 過長、超過 picker 偏好

❌ **壞寫法**（500+ 字、講太多無關細節）：
```yaml
description: This subagent performs comprehensive code review including security analysis, performance profiling, style enforcement, type checking, dependency auditing, license compliance, documentation completeness verification, test coverage assessment, accessibility validation, internationalization checks... (continues for paragraphs)
```
**問題**：雖然 Anthropic **目前沒公告字元上限**（截至 2026-05）、但 description 過長：(1) 佔 context budget、(2) Claude 在 dispatch 決策時讀到後段已經失去重點、(3) 多個 subagent 競爭時長的反而輸給短而精準的。

✅ **改成**（精簡到 2-3 句、留最重要的 trigger + 範圍）：
```yaml
description: Use PROACTIVELY before commits touching auth or payment code. Checks: hardcoded secrets, missing input validation, SQL injection risk. Returns issue list with file:line.
```

> 📌 **Description 寫法 cheatsheet**：
> 1. 開頭 `Use PROACTIVELY when X` 或 `Use when user asks for Y`
> 2. 列 2-4 個**具體會做的事**（不是「helpful」「comprehensive」這種空詞）
> 3. 講**回傳格式**（讓主 session 知道接到的會是什麼形狀）
> 4. **2-3 句就好**——精準 > 完整
> 5. **Description 是語意比對、不是精確關鍵字比對**——關鍵字有幫助、但觸發條件要寫清楚
>
> 💡 **語言選擇**：description 欄位**建議用英文**——Claude 用英文訓練、英文 trigger keyword（PROACTIVELY 等）效果最穩定。

---

## §2 Composition pattern 怎麼設計

要跑 2+ subagent 一起時、怎麼組合？下面 3 種 pattern 是社群歸納的常見組合：

![Subagent Composition — 3 種組合 Pattern](../resources/diagrams/subagent-composition-patterns.png)

> 📊 **上圖**：A 平行（最常用）/ B Pipeline（多 LLM 編排）/ C Meta-Agent（不推薦避坑）—— 先看全貌再讀細節。

### Pattern A — 平行隔離（最常用、最簡單）

**何時用**：3 個任務**獨立**、不需要互相溝通。例：

- 4 個 file 都要做同樣的 audit（spawn 4 個 `general-purpose`）
- 同時跑「code review」+「找相關 paper」+「寫 changelog」3 個獨立任務

**怎麼跑**：在**一個 prompt 裡**列出 N 個獨立任務（譬如「請同時 audit 這 4 個檔案：A.md / B.md / C.md / D.md」）——Claude 在單一 turn 內多次呼叫 **Agent tool**、自動並行。**不是**連續輸入 N 個 prompt（那是 sequential、要等前一個結束）。要長時間獨立背景跑用 `/bg`。

**成本**：低（不需 coordination）

**陷阱**：3 個 subagent 看不到對方結果——如果有依賴關係要走 Pattern B；另外**也不能讓多個 subagent 同時寫到同一份檔案**、會造成 write conflict / 檔案損毀。

---

### Pattern B — Pipeline 串接（多步驟協作）

**何時用**：任務需要**步驟順序**、前一個的 output 是後一個的 input。例：

- Multi-LLM workflow：Claude planner → Codex implementer → Gemini reviewer
- 文獻研究 pipeline：splitter 切題 → 多 researcher 跑各 sub-query → reconciler 合稿

**怎麼跑**：寫一個 skill / orchestrator（譬如 [agent-collab-workspace](https://github.com/WenyuChiou/agent-collab-skills) plugin）、它幫你按序派 subagent。**主 session 自己一個一個叫太累、會出錯**。

**成本**：中（要 coordination 邏輯、要管 `.coord/` 中介檔案）

**陷阱**：(1) 每多一步、容錯 surface 變大、(2) 一個 subagent 出錯整個 pipeline 卡住——所以每步都要寫 acceptance criteria。

---

### Pattern C — Meta-Agent（**不推薦**、列出來避坑）

**為什麼存在**：理論上「一個 subagent 寫出更多 subagent」聽起來很 elegant。

**為什麼不推薦**：

1. **Context explosion 風險**——subagent 寫的 subagent 寫的 subagent... 失控
2. **沒人 audit 新建的 agent**——可能寫出危險的 tools allowlist
3. **Anthropic 官方範例都不這樣用**——社群也未發展出可靠 pattern
4. **debug 噩夢**——出錯時不知該怪原始 prompt、meta-agent、還是被生成的 agent

**該怎麼辦**：你發現 task 重複很多、覺得「該寫個 meta」——**請用 skill 或 template 取代**、不要走 meta-agent 路線。

---

### 3 個 pattern 怎麼選

| 你的情境 | 用哪個 |
|---|---|
| 3 個獨立任務、結果各回主 session | **Pattern A** |
| 多步驟協作、有 input → output 依賴 | **Pattern B** |
| 想「自動生成 subagent」 | **不要做**（去想為什麼、通常 skill / template 更合適）|

**90% 的使用情境是 Pattern A**——上 Pattern B 之前先確認「真的需要 coordination」、別 over-engineer。

---

## §3 自製 subagent 的 debug 工具

> 📌 **跟 [Stage 5.5 §易混淆 5 條 Gotcha](../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能) 角度不同**——
> 5.5 Gotcha 是「**best-practice-oriented**」：寫 subagent 時就要注意的事
> 這節 5 切點是「**debug-oriented**」：subagent **已經跑壞了**該從哪裡查
> 內容有 3 條重疊（tools / model / memory）但視角不同、可分開讀

寫了 `.claude/agents/<name>.md`、結果不如預期——下面是 debug 的 5 個切點：

### 切點 1: 確認 Claude Code 看得到你的 agent

```bash
# 在 Claude Code 對話框內跑：
/agents
```
**期待**：列表裡有你寫的那個 name。**沒有**：

- 檔案位置錯（應該在 `~/.claude/agents/<name>.md` global 或 `<repo>/.claude/agents/<name>.md` project-level；**同名時 project-level 覆蓋 global**）
- YAML frontmatter 語法錯（譬如 `---` 沒包好、`name:` 欄位拼錯）
- 名字衝突（同名 agent 被覆蓋）

---

### 切點 2: 確認 description 寫得會被選

跑這個 prompt 測 Claude 會不會自主派：
```
描述 1 個會觸發你 subagent 的情境（不要明白叫名字）、看 Claude 派的是誰。
```

**Claude 沒派你 agent**：description 寫得 Claude 看不出「我該派這個」。

- 缺 `PROACTIVELY` keyword → 加上
- 條件太抽象 → 改成具體 trigger
- 跟其他 agent 描述重疊 → 寫出**獨特性**

---

### 切點 3: 確認工具權限正確

Subagent 派完報「I don't have access to X tool」——`tools:` 白名單漏寫。

```yaml
# 常忘的工具：
tools:
  - Read
  - Grep
  - Glob       # 找檔案
  - Bash       # 跑 git / pytest
  - WebFetch   # 讀外部 URL
  - WebSearch  # 上網搜
```

> ⚠️ **陷阱**：`tools:` 寫**空字串** `tools: ""` 或**省略整個欄位**、都不等於「沒工具」——兩種情況都**繼承主 session 全部工具**。要限制就**明寫清單**。

---

### 切點 4: 確認 model 不會默默燒大錢

Subagent 沒指定 `model:` = 跟主 session 用同一個。主 session 是 Opus、subagent 也 Opus、token 燒 4x。

```yaml
# 大多數任務 sonnet 就夠：
model: sonnet

# 簡單任務（找檔案、跑 grep）用 haiku 更省：
model: haiku

# 真的需要強推理才用 opus（自己評估）：
# model: opus
```

看 session 結束後 Claude Code 顯示的 token 統計（右下角 status bar 或 session summary），或用 `/clear` 後對比前後用量。

---

### 切點 5: 確認 prompt 是 self-contained

Subagent **看不到主 session 對話**——每次派遣是**全新 context**。

❌ **錯的 prompt**：
```
Review the changes we discussed.
```
Subagent 看不到「我們討論的」是啥、會自己亂猜。

✅ **對的 prompt**：
```
Review the staged changes in this repo (git diff --cached). Focus: security
issues, error handling gaps. Per-issue: file:line + suggested fix.
```
**全 self-contained**——subagent 可以靠這段 prompt 跑起來、不需要「之前的 context」。

---

### 5 切點 quick check

| 症狀 | 切點 |
|---|---|
| `/agents` 看不到 | 切點 1（檔案位置 / YAML 語法）|
| Claude 不主動派 | 切點 2（description 寫法）|
| Subagent 報「no access to X tool」 | 切點 3（tools 白名單）|
| Token 帳單暴增 | 切點 4（model 沒指定）|
| Subagent 跑亂、行為怪 | 切點 5（prompt 不 self-contained）|

---

## 接下來

- **想看更多 dispatch recipe** → [`subagent-cookbook.md`](./subagent-cookbook.md)（15 個複製即用的派遣 prompt）
- **想理解 subagent 跟 skill / MCP 的層次關係** → [Stage 5.5](../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)
- **想跑 multi-agent coordination**（Pattern B）→ [agent-collab-skills](https://github.com/WenyuChiou/agent-collab-skills) plugin
- **詞彙快查** → [`glossary.md` § 5. Claude Code 生態](./glossary.md#subagent子-agent)

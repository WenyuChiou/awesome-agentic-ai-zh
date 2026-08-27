# A2 — 讓 CLI agent 每次都照同一套方法做事

> **繁體中文** | [简体中文](./A2-cli-workflow.zh-Hans.md) | [English](./A2-cli-workflow.en.md)

> [← A1 — 安全完成第一個 CLI 任務](A1-cli-intro.md) · **Track A: CLI Power User** 第 2 站 · [下一站：A3](A3-cli-production.md)

這一站只解決一個問題：**怎麼讓 CLI agent 下次進到同一個 repo，還記得同一套做事方法？**

你會把每次都要知道的規則寫進專案規則檔，把常常重複的步驟做成 Skill。臨時任務才留在單次 prompt。這樣就像把「每天都要重新交代」改成「牆上有守則，工具箱裡有操作卡」。

## 先分清三種東西

<table>
<thead>
<tr><th scope="col">正確術語</th><th scope="col">白話說法</th><th scope="col">什麼時候用</th></tr>
</thead>
<tbody>
<tr><th scope="row">Project instructions<br>專案規則</th><td>每次進工作室都要看的守則</td><td>放專案用途、禁止事項、測試指令與交付格式</td></tr>
<tr><th scope="row">Skill</th><td>需要時才拿出的操作卡</td><td>放 review、release、整理文件等重複流程</td></tr>
<tr><th scope="row">One-off prompt<br>單次 prompt</th><td>今天才需要的一次性交代</td><td>放這次任務的範圍、輸入與成功條件</td></tr>
</tbody>
</table>

## 學習目標

- 用四個欄位寫出一份短而清楚的專案規則。
- 把重複的 review 流程做成一個只讀 Skill。
- 分清哪些內容可以共用，哪些檔名、權限與命令要跟著工具調整。

<details markdown="1">
<summary>展開時間、先備條件、環境與費用</summary>

- **時間**：先完成 CLI-5、CLI-6；CLI-7、CLI-8 可以之後再做，不必一次做完。
- **先備條件**：完成 [A1](A1-cli-intro.md)，會看 `git status`、`git diff`，並有一個不含秘密、可復原的 demo repo。
- **環境**：選一個主用 CLI agent。Claude Code、Codex、Gemini CLI、OpenCode 的檔名不完全相同，下方有對照。
- **費用**：寫規則檔與 Skill 不會產生模型費用；請 CLI 測試時可能使用額度或 API token。以當日官方 usage／pricing 頁為準。

還沒完成 A1 時，先回去跑一次「只讀取 → 看計畫 → 小改動 → `git diff` → 復原」。
</details>

<details markdown="1">
<summary>展開必修閱讀與建議順序</summary>

1. 先看你主用工具的 project-instructions 官方文件：Codex 看 [`AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)、Claude Code 看 [`CLAUDE.md`](https://code.claude.com/docs/en/memory)、Gemini CLI 看 [`GEMINI.md`](https://geminicli.com/docs/cli/gemini-md/)、OpenCode V2 看 [`AGENTS.md`](https://opencode.ai/v2/docs/instructions)。
2. 再看你主用工具的 Skill 文件：[Codex／ChatGPT](https://learn.chatgpt.com/docs/build-skills)、[Claude Code](https://code.claude.com/docs/en/slash-commands)、[Gemini CLI](https://geminicli.com/docs/cli/using-agent-skills/)、[OpenCode V2](https://opencode.ai/v2/docs/skills)。
3. 最後回看 [Stage 2 — Prompt 設計](../../stages/02-prompt-engineering.md)，把「任務、範圍、成功條件」補進單次 prompt。
</details>

<details markdown="1">
<summary>展開四個 CLI 的規則檔與 Skill 位置</summary>

官方資料查核日：**2026-08-27 UTC**。

<table>
<thead>
<tr><th scope="col">工具</th><th scope="col">專案規則</th><th scope="col">Project Skill</th><th scope="col">要注意什麼</th></tr>
</thead>
<tbody>
<tr><th scope="row">Codex</th><td><code>AGENTS.md</code></td><td><code>.agents/skills/&lt;name&gt;/SKILL.md</code></td><td>規則會依目錄分層；較近的規則較晚載入</td></tr>
<tr><th scope="row">Claude Code</th><td><code>CLAUDE.md</code></td><td><code>.claude/skills/&lt;name&gt;/SKILL.md</code></td><td>舊 <code>.claude/commands/</code> 仍相容，但新流程優先用 Skill</td></tr>
<tr><th scope="row">Gemini CLI</th><td><code>GEMINI.md</code></td><td><code>.agents/skills/&lt;name&gt;/SKILL.md</code> 或 <code>.gemini/skills/…</code></td><td>Skill 啟用時會要求同意；不要把秘密放進 Skill</td></tr>
<tr><th scope="row">OpenCode V2</th><td><code>AGENTS.md</code></td><td><code>.agents/skills/&lt;name&gt;/SKILL.md</code> 或 <code>.opencode/skills/…</code></td><td>V2 不使用舊文件寫的 <code>CLAUDE.md</code> fallback</td></tr>
</tbody>
</table>

共同的是「要交代哪些事」；不同的是檔名、搜尋位置、權限與額外設定。不要把一個工具的專屬功能當成所有 CLI 都有。
</details>

<a id="cli-5"></a>
### 動手練習 CLI-5：做一張最小專案規則卡

**成果：** CLI agent 每次進 repo，都知道這個專案做什麼、不能碰什麼、怎麼驗證，以及完成時要回報什麼。

先選上方對照表中屬於你工具的規則檔，再放入這四件事：

```markdown
# 專案規則

- 用途：這是一個練習用文件 repo。
- 不可做：不要刪檔、不要讀取秘密、不要自動 commit 或 push。
- 驗證：修改後執行 `git diff --check`。
- 回報：說明改了什麼、驗證結果，以及仍未處理的事。
```

這張卡只放「每次都要知道」的事。長篇教學、API 參考與偶爾才用的流程不要塞進來。

<details markdown="1">
<summary>展開 CLI-5 的建立與驗證步驟</summary>

1. 在乾淨的 demo repo 建立你主工具使用的規則檔。先執行 `git status --short`，不要蓋到別人的未完成修改。
2. 把上面的四欄換成這個 demo repo 的真實內容。指令必須可以複製執行；不要寫「把格式弄好」這種看不出成功與否的句子。
3. 開一個新的 CLI session，請它只讀規則並用自己的話重述。若它找不到檔案，先查官方的檔名與載入範圍。
4. 給一個會碰到禁止事項的測試，例如「直接 commit 這個改動」。正確結果是 agent 停下來或先詢問，而不是自行 commit。
5. 先用 `git status --short -- <規則檔路徑>` 看它是舊檔還是新檔。
   - 舊檔：用 `git diff -- <規則檔路徑>` 檢查。只有確認開始前該檔乾淨，才用 `git restore -- <規則檔路徑>` 復原。
   - 新檔：Git 會顯示 `??`；`git restore` 不能移除它。可以保留它當練習成果。若不要，先核對完整路徑，再用檔案管理員只刪除這一個檔案，最後重跑 `git status --short -- <規則檔路徑>`。

沒有任何行數能保證規則一定好。只保留會改變行為的內容；某段只在特定任務使用時，把它移到 Skill 或其他按需文件。
</details>

<a id="cli-6"></a>
### 動手練習 CLI-6：把重複 review 做成 Skill

**成果：** 你能叫 agent 執行同一套只讀 review，輸出 `PASS` 或具體問題，不會自己 commit、push 或部署。

Claude Code 使用 `.claude/skills/review-changes/SKILL.md`；Codex、Gemini CLI、OpenCode 可使用 `.agents/skills/review-changes/SKILL.md`。建立檔案後放入：

```markdown
---
name: review-changes
description: Review the current git diff and report concrete risks. Use when the user asks to review local changes.
---

1. Read `git diff --no-ext-diff HEAD` without changing files.
2. Check for secrets, unsafe commands, broken links, and missing verification.
3. Report `PASS` when no problem is found; otherwise list each problem with its file and reason.
4. Do not edit, commit, push, deploy, or send messages.
```

`name` 是操作卡名稱；`description` 告訴 agent 何時拿這張卡。正文才是要照著做的步驟。

<details markdown="1">
<summary>展開 CLI-6 的測試、權限與相容說明</summary>

1. 先讀完 `SKILL.md`，確認沒有下載陌生程式、讀取秘密或改變外部系統的步驟。
2. 在 demo repo 做一個小文件改動，但不要 commit。請 agent「review my local changes」，觀察它是否找到 Skill；也可依工具文件手動啟用。
3. 對照 `git diff` 檢查回報。測試後執行 `git status --short`，確認 Skill 沒有偷偷改檔。
4. 想在多個 CLI 共用時，先共用上面的核心內容，再依每個工具調整資料夾、權限與工具專屬 frontmatter。未知欄位可能被忽略，不要假設所有設定都有效。

Claude Code 的 `.claude/commands/<name>.md` 目前仍能建立同名 `/name`，但 Skills 已包含 custom commands，並支援附加檔案與按需載入。新教學使用 Skill；只有維護舊專案時才需要理解 legacy command。
</details>

<a id="cli-7"></a>
### 動手練習 CLI-7：把大任務切成看得見的小步驟

**成果：** 你能把一個可復原的文件任務拆成「盤點 → 計畫 → 修改 → 驗證」，每一步都有看得見的結果。

<details markdown="1">
<summary>展開 CLI-7 的比較練習與 multi-agent 延伸</summary>

選一個小任務，例如「替兩份 README 補上同一個執行指令」。第一次先請 agent 提計畫，不改檔；第二次請它依序盤點兩份檔案、列出差異、修改、跑 `git diff --check`，最後回報仍未處理的事。

比較兩次結果時，只問：有沒有漏檔、能不能復原、驗證是否真的執行。不要為了看起來厲害，把每個小步驟都分派給不同 agent。任務需要互相等待、會改同一批檔案，或你還說不清成功條件時，先用單一 agent。

完整的 subagent、agent team、背景工作與審查流程放在 [Stage 5.5](../../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)。A2 只練習把工作切清楚。
</details>

<a id="cli-8"></a>
### 動手練習 CLI-8：做一張 portable prompt 對照卡

**成果：** 你能保留同一個任務核心，並清楚標出換工具時要改的檔名、權限、命令與啟用方式。

<details markdown="1">
<summary>展開 CLI-8 的跨工具測試步驟</summary>

1. 共用核心只寫四欄：任務、範圍、禁止事項、成功條件。
2. 在第一個 CLI 的乾淨 demo repo 跑一次，記錄 CLI 版本、模型／provider、權限設定與 `git diff`。
3. 復原後再換第二個 CLI。不要讓兩個會寫檔的 session 同時操作同一個目錄。
4. 另外記下差異：project-instructions 檔名、Skill 位置、shell／sandbox 權限、工具名稱、登入與費用。

「Portable」代表核心意思容易搬，不代表整段文字與設定可以零修改複製。若第二個工具沒有同名功能，就回到成功條件，選它真正支援的方法。
</details>

## 進 A3 前的自我檢查

- [ ] 我能用自己的話分清專案規則、Skill、單次 prompt。
- [ ] 我的規則卡有用途、禁止事項、驗證指令、交付格式，而且 agent 能讀到。
- [ ] 我的 review Skill 只讀取變更，測試後 `git status --short` 沒有多出非預期修改。
- [ ] 我知道「共用核心」不等於「所有 CLI 的檔名與權限都一樣」。

四項都做到，就進入 [A3 — 把 CLI agent 接進安全的 production 流程](A3-cli-production.md)。若還沒做到，先回 demo repo 重跑 CLI-5 或 CLI-6，不必先讀完所有補充資料。

<details markdown="1">
<summary>展開完整學習資源表（16 筆）</summary>

下面按用途分成五組。同一組只顯示一次分類欄，避免重複文字把表格撐亂。

<table>
<thead>
<tr><th scope="col">類型</th><th scope="col">資源</th><th scope="col">先看什麼</th><th scope="col">適合何時使用</th><th scope="col">來源</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">官方專案規則</th><td>Codex <code>AGENTS.md</code></td><td>分層載入與優先順序</td><td>替 Codex 寫 repo 規則</td><td><a href="https://learn.chatgpt.com/docs/agent-configuration/agents-md">官方文件</a></td></tr>
<tr><td>Claude Code <code>CLAUDE.md</code></td><td>何時放規則、何時移到 Skill</td><td>替 Claude Code 寫持續規則</td><td><a href="https://code.claude.com/docs/en/memory">官方文件</a></td></tr>
<tr><td>Gemini CLI <code>GEMINI.md</code></td><td>目錄範圍與載入方式</td><td>替 Gemini CLI 放專案 context</td><td><a href="https://geminicli.com/docs/cli/gemini-md/">官方文件</a></td></tr>
<tr><td>OpenCode V2 <code>AGENTS.md</code></td><td>V2 的合併與 nested discovery</td><td>替 OpenCode V2 寫規則</td><td><a href="https://opencode.ai/v2/docs/instructions">官方文件</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">官方 Skill 文件</th><td>Codex／ChatGPT Build skills</td><td><code>SKILL.md</code> 結構與載入位置</td><td>做 Codex 可重用流程</td><td><a href="https://learn.chatgpt.com/docs/build-skills">官方文件</a></td></tr>
<tr><td>Claude Code Skills</td><td>按需載入、legacy commands、權限</td><td>做 Claude Code Skill</td><td><a href="https://code.claude.com/docs/en/slash-commands">官方文件</a></td></tr>
<tr><td>Gemini CLI Agent Skills</td><td>discovery、安裝同意與啟用同意</td><td>管理 Gemini CLI Skill</td><td><a href="https://geminicli.com/docs/cli/using-agent-skills/">官方文件</a></td></tr>
<tr><td>OpenCode V2 Agent Skills</td><td>支援位置、frontmatter、permission</td><td>做 OpenCode Skill</td><td><a href="https://opencode.ai/v2/docs/skills">官方文件</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">標準與可讀範例</th><td>Agent Skills specification</td><td>共同格式的最低要求</td><td>想讓核心內容較容易跨工具</td><td><a href="https://agentskills.io/specification">標準</a></td></tr>
<tr><td><code>anthropics/claude-plugins-official</code></td><td>官方 plugin 內的 Skills 與 commands</td><td>想看 Skill 如何被打包分享</td><td><a href="https://github.com/anthropics/claude-plugins-official">GitHub repo</a></td></tr>
<tr><td><code>mattpocock/skills</code></td><td>工程工作中使用的短 Skill 範例</td><td>想比較不同寫法</td><td><a href="https://github.com/mattpocock/skills">GitHub repo</a></td></tr>
<tr><td><code>obra/superpowers</code></td><td>真實 workflow 如何拆成 Skills</td><td>完成第一個 Skill 後再看</td><td><a href="https://github.com/obra/superpowers">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">索引與 prompt 練習</th><td><code>hesreallyhim/awesome-claude-code</code></td><td>按類型找 Claude Code 資源</td><td>已知道需求、想找更多範例</td><td><a href="https://github.com/hesreallyhim/awesome-claude-code">GitHub repo</a></td></tr>
<tr><td><code>anthropics/prompt-eng-interactive-tutorial</code></td><td>一步一步比較 prompt 寫法</td><td>CLI-8 卡在共用核心時</td><td><a href="https://github.com/anthropics/prompt-eng-interactive-tutorial">官方 GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Repo context 工具</th><td><code>yamadashy/repomix</code></td><td>產生一次性的 codebase 快照</td><td>需要把 repo 內容整理給 agent</td><td><a href="https://github.com/yamadashy/repomix">GitHub repo</a></td></tr>
<tr><td><code>langchain-ai/openwiki</code></td><td>建立可持續更新的 repo wiki</td><td>大型 repo 需要按需查文件</td><td><a href="https://github.com/langchain-ai/openwiki">GitHub repo</a></td></tr>
</tbody>
</table>
</details>

<details markdown="1">
<summary>展開常見問題與修正方式</summary>

- **規則寫很多，agent 還是漏掉**：先刪掉背景故事與重複句，只留可以觀察的行為。必須每次固定執行的安全檢查，應使用工具提供的 hook／policy，而不是只靠文字提醒。
- **Skill 沒出現**：檢查資料夾、`SKILL.md` 大小寫、YAML frontmatter 與工具支援的位置，再依官方方式 reload 或重開 session。
- **Skill 自己做了危險動作**：把 deploy、send、commit、push 改為只能由使用者明確啟用，並先用只讀版本測試。第三方 Skill 要先讀完內容和 scripts。
- **同一份 Skill 在另一個 CLI 壞掉**：保留共同的目標與步驟，重新對照那個工具承認的 frontmatter、permission 與 tool 名稱；不要用猜的。
- **專案資訊太多**：專案規則只當地圖，細節放在 `docs/`、Skill 的 `references/` 或其他按需文件。規則越長不代表越可靠。
</details>

> 安全底線：規則與 Skill 都是文字指令，不是絕對防護。不要放 API key、token 或個資；任何會寫檔、commit、push、部署或呼叫外部服務的流程，都要有可以看見的權限邊界與驗證步驟。

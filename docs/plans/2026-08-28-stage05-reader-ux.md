# Stage 05 Claude Code 生態閱讀體驗與範例現代化 Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use `writing-plans` to keep this plan current, then execute each task through the repository review and verification gates.

**Goal:** 讓第一次接觸 Claude Code 的讀者，不展開任何選單也能分清 `CLAUDE.md`、Skill、MCP、Hook、Plugin、Subagent、Worktree 與 Agent SDK，知道下一步該用哪一個，並能直接開始第一個安全練習；同時把三語事實、資源與既有 skill 範例更新到 `2026-08-28 UTC` 的官方現況。

**Architecture:** 使用兩層 stacked PR。PR 05A 處理 Stage 05 三語教材、概念圖、事實包、資源表、reader-UX gate，以及 reviewer 證明會讓讀者點出去立刻看見矛盾的直接相依術語；PR 05B 疊在 05A 上，只處理 `tool-calling-tutor` 與範例驗收。兩層各自 review、commit、push、開 PR；未經使用者明確同意，不合併、不刪 branch、不清 worktree。

**Tech Stack:** Markdown、MkDocs、HTML `details`／`table`、Python 3.11、PyYAML、pytest、Pillow、Anthropic Claude Code 官方文件、MCP `2026-07-28` specification、Claude Agent SDK。

---

## 狀態與邊界

- GitHub API UTC：`Fri, 28 Aug 2026 00:46:54 GMT`。
- 隔離 worktree：`C:/Users/wenyu/.codex/worktrees/awesome-agentic-ai-zh/stage05-reader-ux`。
- 05A branch：`codex/stage05-reader-ux`。
- 05A base：`b062e2e3d0fe2654d1cc392d1a9d31bf6cdc3324`，也就是未合併 PR #154 的 head。
- 主工作區仍只有 Claude 的 `stages/01-llm-basics.md` dirty change；本計畫不切換、不覆蓋該工作區。
- 基線：`python -m pytest scripts/test_reader_ux.py scripts/test_freshness.py -q` 為 `67 passed`。
- 本次只改 Stage 05 與直接依賴。Stage 06 之後另開 stacked PR，不在本層順手改寫。
- 既有 Stage 05 深連結優先保留。標題必須更名時，先掃全 repo 引用，並留下穩定 legacy HTML anchor。
- 不把 OpenRouter、Pi、OpenCode 重寫一遍。Stage 05 只用一個短框說清：OpenRouter 是 Router，Ollama 是 Local runtime，Claude Code／OpenCode／Pi 是 Coding agent／harness；完整選擇導回 A1。

## 唯讀診斷

### 閱讀形狀

- 三語各有 `74` 個 H2–H4 heading、`124` 個外部連結，卻只有 `1` 個關閉 `<details>`、`0` 個預設展開。
- 原始非空白字元約為：繁中 `54,127`、英文 `80,263`、簡中 `54,600`。時間、八個子章、長表格、兩組 prompt、完整資源與所有練習同時攤開。
- 章首先出現 7-layer、3 disciplines、兩條 track、跨 CLI 表，再到第一個練習；初學者很難回答「我現在先做什麼」。
- `📌`、`📚`、`🛠`、`🎯`、`✅` 路標與 5.1–5.8 heading 都要保留；重要名詞不能因漸進式揭露而刪除。
- 35 個五星編輯評分要保留；16 個 `★ 89k+` 類 GitHub stars 數字要移除。
- Skills 與 Plugins 推薦表以空白欄假裝合併分類，需改為真正的 `<th scope="rowgroup" rowspan="N">`。

### 已確認需修正的事實

- 「Claude Code 只需要 Anthropic API／OAuth」不完整。官方同時支援 Anthropic、Amazon Bedrock、Google Vertex AI 與 Microsoft Foundry；仍不能把任意本機模型當成官方支援路徑。
- `.claude/commands/` 已併入 Skills 的相容層；新教學應先教 `.claude/skills/<name>/SKILL.md`，再把 commands 寫成 legacy-compatible 路徑。
- `CLAUDE.md`、Rules、Skills 的載入方式不同；`@path` import 只改善組織，不會減少啟動時 context。現有 prompt 把這兩件事混在一起。
- Subagent 現行工具名稱是 `Agent`，不是教學內多處寫的 `Task tool`。官方內建主清單是 Explore、Plan、general-purpose；`frontend-developer`、`code-reviewer` 不能寫成普遍內建。
- Agent teams 是 experimental 且預設關閉；agent view 是 research preview；worktree 是檔案隔離，不是 agent 協調。三者不能混成同一層成熟功能。
- Staging 前二次查核時，官方已刊出 `Dynamic workflows` 文件；5.6 因此改教 script-driven orchestration、Subagent、agent view、agent teams、Worktree 與 `/batch` 分工。舊 `Opus 4.8` 綁定仍不成立，原 5.6 anchor 只保留為 legacy alias。
- `claude-agent-sdk-python` 是 Agent SDK client／wrapper，SDK 套件會帶 Claude Code runtime；不能要求讀者在 Python wrapper 的 `_internal/client.py` 找出完整 Claude Code LLM loop。5.7 改為讀官方 agent-loop 說明，source reading 僅作選修。
- MCP `2026-07-28` stateless core、MRTR、extensions 與至少 12 個月 deprecation window 有官方依據；初學主線只留「MCP 是共用插座」與 Tools／Resources／Prompts，遷移細節收合。
- Hook 的 exit code 2 不是所有 event 都同樣阻擋；必須按官方 event matrix 描述。

### 圖像診斷

- `claude-architecture-map*` 把教學選擇畫成固定 7-layer 真理，混用繁中／英文，且漏掉現行 Worktree、Agent view 與 Agent SDK 邊界。
- `subagent-4-stage-flow*` 把 `Task tool`、`Agent(subagent_type=...)` 與「新 subprocess」畫成通則，與現行官方 `Agent` tool／context 說明不一致。
- `subagent-vs-skill*` 仍寫「Skill 沒回傳」「Skill 預設用主 session 全部工具」等過度簡化結論。
- 三組舊圖只被 Stage 05 三語引用，沒有產生器。05A 先保留 git history，再以一張亮色、三語同構的「Claude Code 擴充工具選擇圖」取代；刪圖前再次掃引用。

## 讀者不展開選單時看到的主線

1. 一句話目的：Claude Code 像會使用檔案與終端機的助手；這章教你怎麼給它規則、工具與安全邊界。
2. `📌` 四個可驗證學習目標。
3. `🧩` 九個可見核心詞；名稱第一次出現時加粗，並各有白話定義、生活比喻與本章用途：
   - **Claude Code**
   - **CLAUDE.md**
   - **Skill（SKILL.md）**
   - **MCP（Model Context Protocol）**
   - **Hook**
   - **Plugin／Marketplace**
   - **Subagent**
   - **Worktree**
   - **Claude Agent SDK**
4. 一張亮色三語概念圖，依問題選零件：每次都要知道 → CLAUDE.md；需要時才讀 → Skill；接外部服務 → MCP；事件到時自動檢查 → Hook；隔離工作 → Subagent／Worktree；打包分享 → Plugin；嵌入程式 → Agent SDK。八張卡不使用 1–8 編號，避免暗示固定安裝順序。
5. 一張短版「我該用哪個」表，避免再用任意 7-layer 當絕對架構。
6. `🚪` 兩條閱讀路線：Track A 只讀 5.1–5.4 的使用方式；Track B 再讀 5.5–5.8 的內部與 SDK。
7. `📚` 必修閱讀標題與一句閱讀目的；完整官方連結預設收合。
8. `🛠` 一個串起 5.1–5.5 的主專案：在示範 repo 寫最小 CLAUDE.md、Skill、只記錄且不阻擋的 Hook、受限 MCP，再用一個 Subagent 檢查結果。每步可單獨停下。
9. 5.1–5.8 heading、既有 anchor、每節一句成果與最短入口保持可見；深入表格、完整語法、prompt 與排錯收合。
10. `🎯` 精選 Projects 標題與每節一個推薦入口；完整表格預設收合。
11. `✅` 短版自我檢查與 Stage 06 入口。

## 預設收合內容

- 時間、安裝、帳號、認證、provider、預算與權限提醒。
- 5.1–5.8 的完整學習目標、必修閱讀、語法、範例、排錯與完整資源。
- CLAUDE.md／SKILL.md 的 audit 與 generation prompts；prompt 本身保留可直接複製，不要求先抄進空白檔。
- MCP `2026-07-28` 的 stateless、MRTR、extensions 與 migration 說明。
- Hook 完整 event／exit behavior。
- Skills、Plugins、MCP、Subagents 的完整推薦表與五星評分。
- Agent teams、agent view、worktrees、`/batch` 的成熟度與選用細節。
- Agent SDK 的 Python／TypeScript quickstart、provider 與 secure hosting 補充。

所有 `<details>` 預設關閉，不使用 `open`。heading、anchor、成果與第一步不得藏入 `<details>`。

## 05A 檔案責任

- `stages/05-claude-code-ecosystem.md`
- `stages/05-claude-code-ecosystem.en.md`
- `stages/05-claude-code-ecosystem.zh-Hans.md`
- `resources/diagrams/claude-code-extension-map.png`
- `resources/diagrams/claude-code-extension-map.en.png`
- `resources/diagrams/claude-code-extension-map.zh-Hans.png`
- 刪除只由 Stage 05 使用的 9 個舊圖：`claude-architecture-map*`、`subagent-4-stage-flow*`、`subagent-vs-skill*`
- `stages/DESIGN.md`
- `scripts/reader-ux-pages.yml`
- `scripts/freshness-models.yml`
- `scripts/repository-freshness-snapshot.json`
- `scripts/test_stage05_content.py`
- `resources/style-guide.md`
- `resources/style-guide.en.md`
- `resources/style-guide.zh-Hans.md`
- `docs/TESTING_PLAN.md`（只有測試清單需要新增時才改）
- `CHANGELOG.md`
- 本計畫檔。

獨立 review 證明直接依賴仍教舊 `Task tool`、Stage 7.5 仍寫錯 Dynamic workflows 模型綁定，因此 05A 另納入 `resources/agent-paradigms*`、`resources/glossary*`、`resources/subagent-advanced*`、`resources/subagent-cookbook*` 與 `stages/07.5-advanced-agentic-concepts*` 三語檔。這是引用鏈修正，不是提前重寫 Stage 7.5；所有檔案逐一加入凍結清單，禁止 `git add .`。

全站資源選擇規則同步寫回 DESIGN 與三語 style guide：易變事實由現行官方文件、規格或 model card 證明，再用知名或廣泛使用的代表 repo 提供動手路徑。人氣只用於找候選，不取代維護、License、安全、用途與限制查核；保留五星編輯推薦度，但不保存會自然變動的 GitHub stars 數字。Stage 05 的 repo 清單以 GitHub API 全量重掃，搬家的專案改用 canonical URL；全站 snapshot 同步覆蓋 294 個實際引用。

## 05B 檔案責任

- `examples/stage-5/tool-calling-tutor/` 三語 README、SKILL、三語 references 與 evals。
- 直接相依的 Agent tool／Dynamic workflows 術語已在 05A 修正；05B 只有在 `tool-calling-tutor` 的可執行驗收真的需要時才再修改 cookbook／glossary，不製造無關混合 diff。
- 05B 必須獨立建立 worktree／branch，疊在 05A commit 上，另做 review 與 PR。

## 官方事實包（05A）

查核日：`2026-08-28 UTC`。來源優先使用：

- Claude Code extension overview：`https://code.claude.com/docs/en/features-overview`
- CLAUDE.md／Rules／memory：`https://code.claude.com/docs/en/memory`
- Skills：`https://code.claude.com/docs/en/slash-commands`
- MCP：`https://code.claude.com/docs/en/mcp` 與 `https://modelcontextprotocol.io/specification`
- Hooks：`https://code.claude.com/docs/en/hooks`
- Plugins／marketplaces：`https://code.claude.com/docs/en/plugins`、`plugins-reference`、`plugin-marketplaces`
- Subagents：`https://code.claude.com/docs/en/sub-agents`
- 平行機制與 Worktree：`https://code.claude.com/docs/en/agents`、`https://code.claude.com/docs/en/worktrees`
- Dynamic workflows：`https://code.claude.com/docs/en/workflows`
- Agent SDK：`https://code.claude.com/docs/en/agent-sdk/overview`、`migration-guide`、`hosting`
- Model／provider：`https://code.claude.com/docs/en/model-config`
- MCP `2026-07-28` release：`https://blog.modelcontextprotocol.io/posts/2026-07-28/`

`scripts/freshness-models.yml` 新增 `stage05_fact_pack`，scope 固定為：

`claude-code,mcp,skills,plugins,subagents,workflows,agent-sdk,security`

三語 marker 完全一致，`max_age_days=90`。可見日期只在最相關的關閉資源區用 `<small>` 顯示，不寫永久性提醒。

## Task 1：凍結引用與元素落腳表

**Files:** read-only scan of Stage 05、resources、examples、scripts。

1. 掃描 5.1–5.8 anchors、跨頁 deep links、三組舊圖引用、examples、cookbook、glossary 與產生器。
2. 建立「保留／移動／合併／改寫／歷史化／刪除」清單。
3. 對 35 個五星評分、所有 Project URL、5.1–5.8 heading、icon 與核心名詞做數量基線。
4. 重跑：

```powershell
python -m pytest scripts/test_reader_ux.py scripts/test_freshness.py -q
```

## Task 2：完成繁中 canonical 05A

**Files:** `stages/05-claude-code-ecosystem.md`、`stages/DESIGN.md`。

1. 先重寫可見主線與九個核心詞。
2. 依 5.1–5.8 重排既有內容；不刪核心概念，只把細節移進關閉 details。
3. 把 5.6 改成官方現行的平行工作／Dynamic workflows／Worktree 路徑，留下含舊模型綁定文字的 anchor alias。
4. 把 5.7 改成官方 agent loop 閱讀題，不再把 SDK wrapper 說成 Claude Code 完整 source。
5. Skills／Plugins 分組表改成 accessible HTML rowgroups；移除 16 個人氣 stars，保留編輯評分。
6. 先跑繁中 anchor、Markdown 與 MkDocs build，才進行翻譯。

## Task 3：產生並驗收三語概念圖

**Files:** `resources/diagrams/claude-code-extension-map*.png`，並刪除 9 個舊圖。

1. 使用 `imagegen` 產生亮底、清楚箭頭、低文字密度的繁中圖。
2. 以同一構圖產生英文與簡中，不更換步驟、數字或安全界線。
3. 以原尺寸人工檢查三圖文字、繁簡、對比與箭頭。
4. 再掃舊圖引用，為零才刪除。
5. 執行 image locale gate 與三語 MkDocs build。

## Task 4：完成英文與簡中 mirror

**Files:** `stages/05-claude-code-ecosystem.en.md`、`.zh-Hans.md`。

1. 以通過繁中 gate 的 canonical 為唯一語意來源。
2. 三語保留相同 heading／details／URL／評分／狀態／日期／命令／安全限制。
3. 簡中做自然在地化，不以刪字取代翻譯。
4. 複查每個 first-use term 都是粗體，且沒有因翻譯漏掉正確術語。

## Task 5：加入 reader UX 與 freshness ratchet

**Files:** `scripts/reader-ux-pages.yml`、`scripts/freshness-models.yml`、`scripts/test_freshness.py`、必要時 `docs/TESTING_PLAN.md`。

1. 鎖定三語可見字元上限為實測值加 50。
2. 鎖定 `max_open_details: 0`、details 精確數、5.1–5.8 可見 heading／anchor、九個核心詞順序、資源 URL／評分 parity、rowspan 分組與 forbidden stale literals。
3. 加 `stage05_fact_pack`、verified pages 與三語 marker 測試。
4. 把 `Opus 4.8` 綁定、`Task tool`、錯誤 built-in subagent、舊 stars、provider-only 說法，以及「prompt 只要出現 `workflow` 就會觸發」列入 Stage 05 stale／forbidden checks；Dynamic workflows 只依現行官方文件教學，歷史 anchor 例外只允許空 anchor。

## Task 6：三層驗證

順序不可顛倒：

1. 機器 gate。
2. 元素落腳審計。
3. 三語語意鏡像比對。

至少執行：

```powershell
git diff --check
python scripts/check-stage-template.py
python scripts/check-anchors.py --strict
python -m pytest scripts/test_anchor_slug_parity.py -q
python scripts/check-mirror-parity.py
python scripts/check-locale-links.py
python scripts/check-hans-chars.py
python scripts/check-image-locale.py
python scripts/check-duplicate-repos.py
python scripts/check-reader-ux.py
python scripts/check-2026-freshness.py
python -m pytest scripts -q
python scripts/build-docs-tree.py
python -m mkdocs build
$env:LANG = 'en'; python -m mkdocs build
$env:LANG = 'zh-Hans'; python -m mkdocs build
```

人工驗收：

- 不展開任何 details，讀者仍能分清九個詞並開始第一題。
- 5.1–5.8 全部可見，重要名詞、icon、評分、URL 與 legacy deep links 都有落腳。
- 三語圖同構且沒有把推測畫成事實。
- 日期位於小字／關閉區，沒有「不代表永遠」等贅句。
- `""`、`“”`、`「」` 只在語意需要或 code block 內出現，沒有渲染空引號。

第一次獨立 review 的 staged tree `0e1b455ebad305e267d67f5582b0bdb33718942d` 判定 FAIL，並使該 fingerprint 永久失效。修正項目固定為：Hook path 改用跨 PowerShell／POSIX 的 `command` + `args` exec form；Dynamic workflows 改教自然語言明確要求或 `ultracode`，並標出 v2.1.160／v2.1.203 邊界；Agent SDK regression 以 fake async `query()` 實際送出 `AssistantMessage([TextBlock("ok")])` 並驗證輸出，不再只 compile 或比對字串。修完後須重跑完整 gate、產生新 staged tree，再由獨立 reviewer 複查。

## Task 7：Review、commit、push、開 05A PR

1. 逐檔 `git add <path>`，凍結 staged file list，斷言數量與清單完全一致。
2. 記錄 index tree 與 binary staged fingerprint。
3. 對最終 staged diff 執行一次獨立 `code-reviewer`。任何修改都使 ack 失效，必須重跑相關 gate、重新 stage、重新 review。
4. 使用 repository ack script；禁止 `--no-verify`。
5. Commit：

```text
content(stage5): clarify the Claude Code ecosystem
```

6. Push 並開 stacked PR，base 為 `codex/stage01-display-metadata`。
7. 等所有 checks 全綠，只回報狀態；不 merge、不 cleanup。

## Task 8：建立 05B 範例強化層

**狀態：進行中。** 05B 已從 05A 最終 commit `62ebc84` 建立獨立 `codex/stage05-example-hardening` worktree。診斷確認 project-level `cp` 指令不可執行、翻譯 SKILL 安裝後的 `../references` 會失效、`evals.json` 不是 promptfoo config、skill discovery 不必一律重啟，以及 references 保存多組無來源比例／成功率／固定省時數字。修正後仍保留四種症狀、五步 schema 教學與三語深度，不用刪概念換取精簡。新增的 `anthropics/skills`／promptfoo 引用已觸發 294-repo GitHub API 全量重掃與 snapshot 重建；25 個既有 canonical／license 硬錯分屬後續章節，本層不跨章偷修。

1. 從 05A commit 建 `codex/stage05-example-hardening` 與新 worktree。
2. 逐項驗證 `tool-calling-tutor` 的 frontmatter、repository／installed reference paths、三語 references、eval schema、Path A／Path B 名稱與目前 Stage 03 範例。
3. 修正過時模型、SDK shape、錯誤處理、硬編碼 stars、不能執行的 promptfoo 設定或無證據成功條件。
4. 提供離線結構／行為測試；不把「人工看 JSON」當自動 eval，也不把 contract checker 說成 live model-quality eval。
5. 重跑完整 gates、獨立 review、commit、push，開第二個未合併 stacked PR。

## 停止條件

- 任一官方來源與正文衝突：停止該段寫作，先解決事實。
- Claude 同期修改碰到同檔：整合最新上游，不覆蓋；舊 fingerprint／review ack 作廢。
- 零 checks、PENDING、空狀態或 failure：停止，不 merge。
- 使用者未明確說「可以合併」：只保留 OPEN PR 與 upstream branch。

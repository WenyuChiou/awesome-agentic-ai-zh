# Stage 設計筆記

> 給 maintainer 的內部文件，不是讀者面向的內容。
>
> 為什麼是 8 個 stage、每個 stage 結構為什麼這樣切、動手練習 為什麼必跑、self-check 怎麼設計——這些設計決定的記錄。

---

## 全站唯一學習順序

- 共用基礎：`Stage 0 → Stage 1 → Stage 2`。
- Track A 建議順序：`A1 → A2 → Stage 5（只讀 Track A 核心 5.1–5.4）→ A3 → Stage 8`。
- Track B：`Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7 → Stage 7.5 → Stage 8`。
- Track A 做完 A3 就能開始 Capstone；Stage 8 建議完成，但不擋入場。

README、PROGRESS、CAPSTONE、章節頁首、章末下一站與路線圖必須使用同一順序。先改可存取的文字與測試，再重畫圖片；圖片不能成為唯一導航。

---

## Track A 跟 Track B 的 2-track 結構

從 Phase 7 開始 catalog 拆成兩條軌道。原本的線性 Stage 結構**還在**（現為 Stage 1-8，後來補了 Stage 7.5 進階概念 reading-map 跟 Stage 8 Agent Interfaces），但定位變成「**Track B — Agent Builder**」（從零打造 agent 的路線）。新增的 `tracks/cli/A1-A3` 是「**Track A — CLI Power User**」（用現成 CLI agent 把工作做完的路線）。

### 為什麼分軌

原本 7-stage 假設讀者都想「**從零打造 agent**」（寫 Python、選 framework、自己 deploy），但實際上：

- 多數 AI agent 使用者**沒在自己寫 agent**——他們是 Claude Code / Cursor / ChatGPT 重度使用者
- 「framework-heavy」內容（LangGraph / AutoGen / Smolagents 等 Stage 4 那塊）受眾比 CLI 工具小很多
- 但「打造 agent」這條路還是有受眾（研究者、ML 工程師、想懂內部的人）

所以 Phase 7 的決策：**不刪內容、加軌道**——保留 Track B 給 builder，新增 Track A 給 CLI user。

### Track A 的 sub-stage 為什麼是 3 個（不是 5 個）

**初版草稿（A1-A5）→ 合併後（A1-A3）**：

| 草稿 | 草稿主題 | 最終歸屬 |
|---|---|---|
| A1 | CLI 入門 + 選擇 | → 最終 A1 |
| A2 | Workflow（project instructions / Skill / 任務拆解 / portable prompt） | → 最終 A2 |
| A3 | MCP 接 CLI | → 最終 A3 |
| A4 | 多 CLI 並用 | → 移到最終 A1／A2 的工具比較與 portable prompt |
| A5 | Production CLI workflow（CI / cost / observability / team sharing） | → 最終 A3 |

合併邏輯：

- 草稿 A3 + A5 都是「**把 CLI 安全接到外部系統 / 團隊流程**」這同一件事，合併後仍是一條完整主線
- 草稿 A4 的工具比較放到 A1，跨工具可攜做法放到 A2；A3 不先教同時放出多個 agent，避免初學者在學會安全界線前把流程變複雜
- 草稿 A1 邊界清楚（入門 + 選擇），保留為最終 A1
- 草稿 A2 邊界清楚（一個人在 CLI 內部如何工作），保留為最終 A2

最終 3 個 stage：

- **A1**：入門 + 選擇（CLI 安裝、認證、第一個任務）
- **A2**：Workflow Patterns（project instructions / Skill / 多步拆解 / portable prompt）
- **A3**：Integration & Production（單一受限 MCP、唯讀 PR CI、usage / cost receipt、版本化 team Skill）

判準：**3 個 stage 邊界清楚、不互相浸蝕**，每個 stage 對應一個明確的「我能跑出什麼」outcome。

### A1 的固定閱讀形狀

- 第一遍先用五個可見核心詞分清 **LLM**、**Provider API**、**Router**、**Coding agent** 與 **Local runtime**。OpenRouter 放在 Router；OpenCode 與 Pi 放在 coding agent／harness；Ollama 放在 local runtime。
- `📌`、`📚`、`🛠`、`🎯`、`✅` 路標、必修閱讀與 11 筆五星工具表保持可見。時間、帳號、費用與完整步驟預設收合。
- CLI-1 的第一個請求使用可直接複製的完整 `text` block。CLI-1 至 CLI-4 的標題、anchor 與一句話成果保持可見。
- 11 筆工具表固定為 `4／5／2` 三組，保留既有五星編輯評分並移除會變動的 GitHub stars 數字。評分是路徑建議，不是總排名。

### A2 的固定閱讀形狀

- 第一遍只教三個可見核心詞：「Project instructions 像共同守則、Skill 像按需操作卡、One-off prompt 像臨時交代」，並保留 CLI-5 至 CLI-8 的標題、anchor、成果與 A3 入口。
- CLI-5 用「用途／禁止事項／驗證指令／交付格式」四欄做最小規則卡；不把 persona 或行數門檻當成跨 CLI 通則。
- CLI-6 教目前的 `SKILL.md`，只在相容說明提 `.claude/commands/`。核心內容可以共用，工具專屬的資料夾、frontmatter、permission 與 tool 名稱分開說。
- 必修閱讀與 16 筆五星資源表保持可見；時間、先備條件、完整工具位置、CLI-7／CLI-8 步驟、multi-agent 與疑難排解預設收合。
- `📌`、`📚`、`🛠`、`🎯`、`✅` 路標保持可見。完整資源表按語意分組；每組一個 `<tbody>`，分類欄用真正 `rowspan` 合併。三語的 rowgroup、URL、評分、命令、日期與安全限制必須一致。

### A3 的固定閱讀形狀

- 第一遍先用三個可見核心詞 **MCP**、**CI**、**Observability** 與一條安全階梯說清楚主線：唯讀 → 最小權限 → 示範 repo → 人工檢查 → 最後才考慮寫入。
- CLI-9 至 CLI-12 的標題、anchor、一句話成果、最短路徑、必修閱讀與 18 筆五星資源留在可見區；時間、完整步驟、疑難排解與 playbook 放進預設關閉的 `<details>`。
- Playbook 4 的標題與成果留在可見區，保護既有跨頁深連結；多 agent、fallback 與 failure injection 的理論導回 Stage 7.5，不在 A3 重寫一次。
- `📌`、`📚`、`🛠`、`🎯`、`✅` 路標保持可見。完整資源表固定為 18 筆、五個語意群組，`rowspan` 為 `4／5／4／3／2`。同類型只顯示一次分類名稱；保留五星編輯評分，不放 GitHub stars、排行榜或會自然變舊的數量。
- A3 的自動化預設只讀、最小權限、可留下 receipt，且必須有人檢查。不能把自動 merge、push、deploy 或未受限的 MCP 寫成初學者第一步。

### Cookbook 的固定閱讀形狀

- Cookbook 是從 Stage 5 連到可執行成果的實作入口，不是另一個 Stage。可見主線固定為「用途 → 六選一 → 六個核心詞 → 六份 recipe 的標題／成果／第一個動作 → 必修閱讀 → 精選 Projects 與學習資源 → 完成檢查」。
- 六份 recipe 固定涵蓋 Skill、MCP Server、Office 文件、Gemini Notebook、Zotero 與本機 LLM＋CLI Agent。每份完整步驟、替代路徑、費用、安全細節與排錯放進預設關閉的 `<details markdown="1">`；共九個 details，不使用 `open`。
- 必修閱讀、精選 Projects、編輯評分與成功條件保持可見。14 筆資源固定分成 `2／2／2／2／3／3` 六組，每組使用獨立 `<tbody>` 和 `<th scope="rowgroup" rowspan="N">`；不顯示 GitHub stars。
- 易變命令、產品名稱、授權、API 行為與安全限制使用官方來源和 90 天 freshness marker。社群整合必須明標非官方、可能失效與可用的官方 fallback；三語保留相同 URL、命令、日期、評分與風險。

### 為什麼 Stage 5 特別放在「兩軌共用」

Stage 5（Claude Code 生態）兩條軌都會碰到：

- Track A：A2 以多家官方 project-instructions／Skill 文件為主，Stage 5.1／5.3 只作 Claude Code 延伸；A3 用 5.2（MCP）+ 選擇性用到 5.3（Skills）跟 5.4（Plugins）。A3 的 CLI-12 教可版本化的 team Skill；plugin 是 Claude Code 的延伸選項，不假裝成每個 CLI 都通用的打包格式。讀的角度是「**怎麼用 CLI agent 把工作做好**」
- Track B：把整個 Stage 5 當「**Claude Code 內部運作**」的深度學，從 5.1 完整走到 5.7

但兩條軌**不需要重新讀整份 Stage 5**——Track A 看「用法」、Track B 看「內部結構」。同一份內容，兩種讀法。

**Stage 8（Agent Interfaces）是第二個兩軌共用 hub**，同樣的邏輯：Track A 學「怎麼用 Computer / Browser Use 委派任務」、Track B 學「怎麼把這些介面 embed 進自己的 agent」。Stage 5 + Stage 8 是整份 curriculum 的兩個 hub。

### Track A 跟 Track B 的 entry curation 差別

| | Track A（A1-A3） | Track B（Stage 3-8） |
|---|---|---|
| **entry 結構** | 大量 cross-link 到 Stage 5 / Stage 8 / cli-agents-guide | 完整獨立 entry（每個都有 schema 表格）|
| **entry 數** | ~24 個（多為 cross-link） | ~80 個（多為獨立 entry） |
| **新增 entry 標準** | 必須是 CLI agent 直接相關的工具 | framework / library / agent component |
| **更新頻率** | 高（CLI 工具迭代快） | 中（framework 更新慢一些） |

**判準**：Track A entry 出現的條件是「對 CLI workflow 有直接幫助」；Track B entry 出現的條件是「教讀者一個 agent design pattern」。

### 5 條 specialized branch 為什麼兩軌共用

走完 Track A 的 A3 或 Track B 的 Stage 7 後，都接到 5 條 branch（researcher / developer / teacher / knowledge-worker / everyday-users）。Branch entry 的 curation **不依軌道區分**——同一個工具不論是 Track A 用法還是 Track B 用法，都放在對應的 branch。

Branch 的可見主線沿用 Stage 的漸進式揭露規則：先定位角色、說清目標與核心詞，再給一個可直接複製的最小任務、三個起點、必修閱讀、精選 Projects／學習資源、完成條件與回到主路線的下一站。被稱為「必修」或「精選」的內容要直接可見；setup、帳號／費用、進階流程、替代方案與排錯才預設收合。研究人員與開發者頁另外以 `scripts/test_role_paths.py` 鎖住 citation 核對、私人資料、read-only plan、diff／test／rollback、工具身分與多 surface、三語資源表及 archived 狀態。

研究人員路線固定保留八個可見核心詞與「一篇 paper、三個問題、逐條回原文」的第一個練習。六份必修閱讀與 15 筆五星編輯評分資源表直接可見；資源分成 `3／4／5／2／1` 五組，使用真正 HTML `rowspan`，並由「可重現與證據」組補上文獻篩選、資料版本、實驗紀錄、可引用保存與環境重建。Gemini Notebook 名稱、隱私、citation、工具授權、封存狀態及研究服務轉型使用 90 天 freshness marker；GitHub stars 不進教材。OSF Projects 已宣布 2026-11-16 停止新建、2027-02-19 轉唯讀，因此不能再當成新研究專案的一般儲存預設；需要現行可引用保存入口時優先導向 Zenodo 或領域／機構核准 repository。

---

## 為什麼是 8 個 stage（不是 5 個或 10 個）

### 太少（5 stage）的問題
要把 9 個概念塞 5 個 stage：API 基礎 / prompt / tool use / framework / Claude Code 生態 / memory / RAG / multi-agent / agent 操作介面（Computer · Browser Use）。塞下去結果是有的 stage 太擠（譬如 framework + Claude Code 擠一起，3-4 週的內容硬塞 1 stage），讀者跳不過去。

### 太多（10+ stage）的問題
- 時程拉到 6+ 個月，多數人放棄
- stage 間的 dependency 複雜化——讀者看不懂為什麼要先學 X 再學 Y
- maintainer review cost 暴漲

### 8 是「每階段獨立可學完、互相銜接、不重複」的折衷
8 個真正的 stage（Stage 1-8），外加 1 個 Stage 0（prerequisite gateway、可跳）跟 1 個 Stage 7.5（進階概念 reading-map、不寫 code 的中繼）= 10 個 stage 檔案。其中 Stage 5 跟 Stage 8 是 Track A / Track B 共用的兩個 hub。

**判準**：每個 stage 應該對應 1 個**核心問題**（下一節）。若一個 stage 裡塞 2 個核心問題，就該拆；若 2 個 stage 在問同一個問題，就該合。

---

## 每個 stage 的「核心問題」

stage 的價值 = 讀者學完後**能回答這個問題**。

| Stage | 核心問題 | 回答方式 |
|---|---|---|
| **0** 基礎準備 | 「我的開發環境準備好了嗎？」 | 1 個整合練習：公開 GitHub API → JSON → terminal → Git |
| **1** LLM 入門 | 「LLM 是什麼、token 怎麼算、不同 LLM 的差別？」 | 從 API call 到本地 LLM，含 from-scratch 訓練 |
| **2** Prompt 設計 | 「怎麼讓 LLM 照我的意思做事，而且知道修改有沒有用？」 | 四格 prompt / few-shot / 固定 eval / 一次只改一件事 |
| **3** ⭐ 工具使用與第一個 Agent Loop | 「怎麼讓 LLM 呼叫外部工具，並重複做完一個有界 loop？」 | 完整 tool round trip + 有界 ReAct loop + 6 個動手練習 |
| **4** Workflow Graph 與 Agent 框架 | 「怎麼選 framework，把多個步驟接成看得見的 graph？」 | LangGraph / AutoGen / CrewAI / Smolagents 對比 |
| **5** ⭐⭐ Claude Code 生態 | 「Claude Code 生態系怎麼用？」 | 九個核心詞、五題累加練習、5.1–5.8 延伸入口 |
| **6** Memory · RAG | 「怎麼讓 agent 記得事情？怎麼讓它能查自家文件？」 | embedding / vector DB / RAG / contextual retrieval |
| **7** Agent Production Engineering | 「Harness、Loop、Graph 跟 production 怎麼一起？」 | Harness / Loop / Graph / orchestration / eval / observability |
| **7.5** 進階概念地圖 | 「multi-agent 之後還有哪些進階 pattern 要認得？」 | 12 個進階概念 + reading path（不寫 code）|
| **8** ⭐⭐ Agent 操作介面 | 「agent 怎麼操作 API 以外的真實環境（螢幕 / 瀏覽器 / sandbox）？」 | Computer Use / Browser Use / Code Sandbox |

每個 stage 結尾的 self-check 就是 **「能不能回答這個核心問題」** 的 measurable 版本。

---

## Stage 結構（dominant pattern，非絕對 invariant）

多數 stage 保留以下 section；**呈現順序採漸進式揭露**。Stage 1 是第一個完成遷移的 pilot，其他 stage 在各自內容更新時逐章遷移，不要求在同一個 PR 一次重寫：

Stage 2 的固定主線是「目標／資料／規則／輸出 → Zero-Shot／One-Shot／Few-Shot → Chain-of-Thought 的正確邊界 → 六筆固定案例 → 一次只改一件事 → 比較分數」。三語概念圖固定放在可見核心詞之後：先由正文定義，再用同構圖整理關係；圖片不能取代定義，也不能畫入正文已撤掉的固定數字。必修閱讀與 18 筆五星資源表保持可見；程式碼、模型比較與安全補充預設收合。CoT 必須先用白話解釋，但不當成要求模型公開完整內部推理的通用步驟。

Stage 3 的章名與固定主線都把 **Agent Loop** 當成入口：「八個可見核心詞 → Tool Use 六步亮色圖 → 一般回答／Structured Output／Function Calling 的選擇 → 五條安全底線 → schema → Tool Call → 程式執行 → Tool Result → final answer → 有界 Agent Loop」。正文必須直接寫出 `model → tool call → execute → tool result → model`，避免只看章名還不知道 loop 是什麼。三語同構圖要清楚畫出模型只提出請求、程式先驗證再執行，以及 allowlist、HITL、最大輪數三個安全邊界；圖片不取代正文定義。三份必修閱讀、六題的標題／成果／第一個可複製動作，以及完整 21 筆五星編輯評分資源表保持可見；先備條件、環境、時間、預算、完整程式、供應商差異、費用、排錯與 Reflection 路由預設收合。ReAct 使用可觀察的 action／observation loop 教學，不要求公開私人 Chain-of-Thought。

Stage 3 的六題也各有一個 `examples/stage-3/NN-*` 可執行資料夾。每題同時提供 Ollama Path A、Anthropic Path B，以及兩個不連網的 mock tests。模型產生的工具名稱、JSON 與欄位一律視為不可信輸入：程式先做 allowlist 與參數驗證，再執行工具；錯誤要帶回原本的 call ID，Anthropic client tool 使用 `is_error: true`。多輪迴圈必須有最大步數，並把正常完成、token 截斷、拒絕／其他停止原因分開。README 以 PowerShell 為第一條可複製路徑，再收合 macOS／Linux 指令；SDK 使用已查核的 major 範圍、雲端模型使用固定 ID，費用寫公式與查核日，不用沒有 token 假設的固定小數，也不用單次結果宣稱某模型一定更快或更穩。

Stage 4 的章名固定把 **Workflow Graph** 放在 **Agent Framework** 前面；它先教工作地圖，再教可用來實作的工具箱，不直接把整章叫成 Graph Engineering。固定主線是「八個可見核心詞 → Agent Loop／Workflow Graph／Agent Framework／Loop Engineering／Production orchestration 五項橋接 → workflow／agent × single／multi 選擇圖 → 先用最簡單能完成任務的形狀 → 五種協作 pattern → 依需求選工具 → 五題練習」。八個主核心詞是 **Workflow／Workflow Graph**、**Framework**、**Agent**、**Orchestration**、**State**、**Checkpoint**、**Handoff** 與 **Human-in-the-loop（HITL）**；Supervisor、Worker、CodeAct 與 Type-safe 也必須在第一次可見使用時粗體解釋，不能為了縮短頁面刪掉。橋接表必須說清楚：Agent Loop 是 Stage 3 的執行迴圈，Workflow Graph 是 node／edge／branch／state 組成的工作地圖，framework 是工具箱，Production orchestration 是 Stage 7 加入預算、驗證、復原、觀測與人工核准後的上線工作；**Graph Engineering** 只作新興替代稱呼，不宣稱是業界統一標準。Multi-Agent 是可選的系統形狀，不是 framework 的定義，也不是每張 graph 的必要條件。三語亮色圖只整理正文已先定義的關係，不放版本、價格、stars 或沒有通則的數字。

章節學習順序與五個工程控制問題必須分開說。章節依「先做出來，再看見結構，最後做穩」排列：Stage 2 Prompt → Stage 3 Agent Loop → Stage 4 Workflow Graph／Agent Framework → Stage 5 MCP／Skills／Plugins／Subagents 工具與規則 → Stage 6 Context 深化 → Stage 7 Agent Production Engineering 整合 Harness／Loop／Graph。`prompt → context → harness → loop → graph` 是五個檢查問題，不是嚴格軟體層或章節順序；Harness 可以包含 Agent Loop，Workflow Graph 也可以連接 Harness、固定程式、Loop 與人工核准。Stage 7 的三語完整章名固定為 `Agent Production Engineering：Harness、Loop 與 Graph`／`Agent Production Engineering: Harness, Loops, and Graphs`／`Agent Production Engineering：Harness、Loop 与 Graph`；README、首頁 index、PROGRESS、MkDocs／mdBook 導覽、Stage 6 出口、範例返回連結與補充資源若直接寫出完整章名，必須使用這組標題。這個章名是本學習地圖用來裝住三種責任的上位名稱，不宣稱所有供應商都採用同一個正式標準。檔名與既有 anchor 不因章名修正而更動。

Stage 4 的 4 個必修閱讀步驟（共 5 個官方連結）與 18 筆五星編輯評分資源表保持可見；時間、環境、研究證據、進階 tool patterns、五題完整步驟與疑難排解預設收合。`📌`、`🚪`、`📚`、`🛠`、`🎯`、`✅`，簡短進入條件、五題 heading／anchor、每題成果、第一個可複製 PowerShell 動作與預算提醒保持可見。資源表固定為五組 `4／6／4／3／1`，使用真正 HTML `rowspan`，保留編輯推薦星級、移除會變動的 GitHub stars；Preview、維護、凍結／歷史與遷移狀態依官方來源明寫。OpenAI Swarm 只作教育參考，不能再有 production 評分；框架版本、維護、授權與安全資訊使用 90 天 freshness marker。

Stage 4 使用兩層 stacked PR：第一層只定稿三語教材、官方事實包、圖、資源表與 reader-UX gate；第二層才更新五個 `examples/stage-4/` 資料夾的 current-major SDK、Ollama／Anthropic 雙路徑、安全邊界與離線測試。這讓閱讀設計和 executable API migration 可以各自回溯、review 與驗證。

Stage 4 的五個可執行資料夾必須各自建立 Python 3.11 `.venv`，不能把不同 framework 的 `requirements.txt` 合併安裝。每題的 Path A 與 Path B 測試都要實際走過核心行為；只確認 import 成功不算驗收。LangGraph 要測分支、checkpoint、`interrupt()` 與 `Command(resume=...)`；CrewAI 要測角色、handoff 與有界停止；CodeAct 只在受限 Docker executor 示範模型程式碼，Jupyter 控制埠只綁 loopback，並明說一般 bridge 仍可對外連線、不是 production sandbox；typed output 要明說格式正確不等於內容真實。

Stage 5 的固定主線是「九個可見核心詞 → 依問題選最小零件 → Track A／B 閱讀路線 → 五題累加式練習 → 5.1–5.8 延伸入口」。九個核心詞是 **Claude Code**、**CLAUDE.md**、**Skill**、**MCP**、**Hook**、**Plugin／Marketplace**、**Subagent**、**Worktree** 與 **Claude Agent SDK**。5.1–5.8 heading、練習標題、成果、第一個可複製動作、完整必修閱讀、推薦專案與 35 筆五星資源保持可見；時間、認證、費用、語法、prompt、排錯與補充原理預設收合。不得用「精簡」刪掉 MCP 的 Tools／Resources／Prompts、Skill／Subagent 差異、Hook 阻擋邊界、Worktree 檔案隔離或 Agent SDK hosting 安全。

Stage 5 的 35 筆學習資源固定分成 `4／8／8／7／4／4` 六組，使用真正 HTML `rowspan`；三語保留相同 URL、順序與五星編輯評分，移除會變動的 GitHub stars。Claude Code、MCP、Skills、Plugins、Subagents、Dynamic workflows、Agent SDK 與 security 使用 90 天 freshness marker；查核日期以小字放在對應可見資源區附近。

Stage 5 的第一張概念圖只回答「遇到哪種問題先用哪個零件」，不把 maintainer 的任意分層畫成產品架構真理。第二張關係圖固定放在 5.1 前，回答 CLAUDE.md／Skill 如何提供 context、Agent loop 如何經 MCP 交換 request／result、Hook 如何依 event 檢查、Subagent／Worktree 如何分開隔離 context 與檔案，以及 Plugin 如何只負責打包。三語圖同構、亮色、低文字密度；選擇圖不加 1–8 編號，關係圖明寫不是安裝順序。Worktree 不能畫成完整 sandbox，Plugin 不能畫成 runtime 必經步驟，**Plugin 不連到 Worktree**；Worktree 是另外選用的檔案樹隔離方式。Hook 不能畫成每次都阻擋。Subagent、agent view、agent teams、Dynamic workflows、Worktree 與 `/batch` 的成熟度與責任邊界以官方現行文件為準。Dynamic workflows 要教成可讀、可重跑的 JavaScript 編排，不得綁成某個 Claude 型號專屬功能；現行觸發方式是明說要 use／run a workflow 或使用 `ultracode`，literal `workflow` 只可放在 v2.1.160 前的歷史說明。找不到官方正式來源的功能名稱或模型綁定不得當成一般可用功能教學。Repo 或規格第一次在正文被點名時就要有官方超連結；完整資源表再補狀態、授權、限制與五星編輯評分。

Stage 5 使用兩層 stacked PR：第一層定稿三語教材、官方事實包、圖、資源表與 reader-UX gate，也必須同步修正正文直接連到的 cookbook／glossary／Stage 7.5 術語矛盾，不能讓讀者點出去立刻看見舊說法；第二層才更新 `examples/stage-5/tool-calling-tutor/` 的可執行實作。兩層都保留 branch 與 upstream，未經使用者明確同意不合併、不清理。

Stage 6 的固定主線是「七個可見核心詞 → RAG／Memory 選擇 → 五題累加式練習 → 一個同時檢索與記憶的小專案 → 精選資源 → Stage 7 檢查」。七個核心詞是 **Retrieval**、**RAG**、**Embedding**、**Vector Store／Vector Database**、**Chunk**、**Reranking** 與 **Memory**；BM25、Hybrid Search、GraphRAG、Contextual Retrieval、HyDE、Multi-Query、RAG Fusion、Self-RAG、CRAG、Adaptive RAG、RAPTOR、DSPy、episodic／semantic／procedural memory、CoALA、Generative Agents 與 Reflexion 仍要保留白話定義，但放在有明確 summary 的關閉區，不能在第一遍淹沒練習。

Stage 6 的可見亮色三語圖固定畫成三條同構路徑：文件進入知識庫的 ingest path、問題取回證據再回答的 query path，以及重要狀態的 Memory write／read loop。關閉的「RAG 基礎流水線」另放一張詳細三語圖，分成 index lane 與 query lane；Contextualization、query rewrite、fusion、reranking 必須標為可選，retrieve 連線只能落到候選檢索，不能跳到答案。圖與正文都要說清 vector database 不是唯一 retriever，並區分 Hybrid RAG（流程形狀）與 Hybrid Search（候選融合）。圖片只整理正文已定義的關係，不把 vendor benchmark、固定 chunk size、top-k、成本倍數或模型排名畫成通則。五題 heading、anchor、成果、第一個可複製 PowerShell 動作、資料／預算提醒、必修閱讀與五星學習資源表保持可見；時間、環境、進階 RAG、Memory taxonomy、Chunking、Reflection 與評測細節預設收合。

Stage 6 的 18 筆資源固定分成 `4／5／4／3／2` 五組，每組使用獨立 `<tbody>` 與真正 HTML `rowspan`。保留五星編輯評分，移除 GitHub stars 數字；官方文件、paper 與 canonical repo 負責證明事實，知名或活躍專案只負責提供動手入口。GraphRAG 維護狀態、Ragas canonical owner、Letta 現行開發入口、Zep Community Edition 歷史狀態，以及 RAG／retrieval／embedding／vector store／memory／evaluation／project status 使用 90 天 freshness marker。

Stage 6 同樣使用兩層 stacked PR：第一層定稿三語教材、官方事實包、圖、glossary 直接矛盾、資源表與 reader-UX gate；第二層才修正五個 `examples/stage-6/` 的 chunk 邊界、collection 隔離、真正 persistent memory、雙路徑與離線測試。兩層都保留 branch 與 upstream，未經使用者明確同意不合併、不清理。

Stage 7 的固定主線是「單一 Agent／Multi-Agent 決策 → 九個可見核心詞 → Prompt／Context／Harness／Loop／Graph 五個控制問題 → Harness／Loop／Graph 責任邊界圖 → Harness 八項 production 檢查 → Loop Engineering → Workflow Graph／Production orchestration → 工具角色辨識 → 五題可執行練習 → execution receipt 小專案 → benchmark 閱讀紀律 → 精選資源 → 自我檢查」。九個核心詞是 **Multi-Agent**、**Orchestration**、**Handoff**、**Harness**、**Eval**、**Observability**、**Guardrail**、**Loop Engineering** 與 **Graph Engineering**；先用白話和生活比喻定義，再保留正確術語，同時把 Loop Engineering 標成 emerging practice、Graph Engineering 標成尚未統一的新興稱呼。正文必須分清三種 loop：程式迴圈只重複指令，Agent Loop 在一次執行裡做「想／做／看」，Loop Engineering 則替一次長 run 或跨 session 的反覆工作加入目標、觸發、驗證、記憶、預算、停止與人工升級。**Loop 不淘汰 Harness**：Anthropic 的 Harness 定義本身包含呼叫模型與路由工具的 loop；IBM 的 Loop Engineering 範圍更廣，會納入目標、檢查、hooks、context、subagent 與持久狀態。正文教三個除錯問題，不把三者畫成互斥產品或嚴格替換世代。Agent Loop 是 Stage 3 的入門，Workflow Graph 是 Stage 4 的入門，Stage 7 才把兩者加上 production 邊界。控制問題圖必須畫出責任重疊，不再用垂直堆疊暗示唯一層級；Agent framework 是工具箱，Production orchestration 是上線工程，Graph Engineering 只作新興別名。OpenRouter 是模型 API 入口，Pi／OpenCode 是 Agent runtime／coding agent，Orca／QM 是多 Agent 協作層；不得把三層寫成可互換的同類產品。

Stage 7 的時間、環境、費用、安全提醒、延伸閱讀、Loop／Graph 補充、回饋與復原細節、練習步驟及 benchmark 長清單預設收合。五份必修閱讀、20 筆精選資源表、五題 heading／anchor／成果與第一個可複製測試命令保持可見；成本／延遲仍是 Harness 第八項與 SDK 練習的必要觀念，但沒有對應資料夾時不得虛構第六題。外部排行榜只能教讀法，不能凍結 SOTA 分數、模型名次或第三方「最強」結論。

Stage 7 的 20 筆資源固定分成 `4／6／5／5` 四組，每組使用獨立 `<tbody>`、`scope="rowgroup"` 與真正 HTML `rowspan`。保留五星編輯評分，移除 GitHub stars；已封存、Preview、Alpha、best-effort 或維護紀錄不足的專案必須在限制欄明寫。Stage 7 同樣拆成 content 與 example-hardening 兩層 stacked PR：第一層定稿三語教材、來源、圖、資源與 reader-UX gate；第二層才更新五個 `examples/stage-7/` 的 SDK、模型、直接執行步驟、安全邊界與離線測試。未經使用者明確同意不合併、不清理 branch。

五個 Stage 7 範例 README 的第一個可見動作固定是 PowerShell 建立該題自己的 Python 3.11 `.venv`，再直接跑 Ollama／Anthropic 兩份離線測試；不再要求讀者先改名完整解答或抄一份空白文字檔。實際模型路徑、macOS／Linux、程式走查、排錯與額外替代方案預設收合，但學習目標、核心詞、「只改一件事」、成功檢查，以及依 `3／6／7／4／5` 分布的 25 筆必讀／評分學習資源保持可見。共用模型選擇器必須按能力需求分段：目前 Stage 3–6 function-calling 題使用 `qwen2.5:3b`，Stage 7 的辯論、評測、觀測、串流與部署機制使用 `qwen3.5:4b`；不得用「Stage 3+」把兩者寫成同一個預設，也不得暗示換模型就一定更穩。Ollama 只能寫「沒有供應商模型 API 帳單」，仍要提醒硬體、電力、下載、時間以及裝置／log／權限安全；Anthropic 使用當期 input／output token 公式與保守 spend limit，不保存固定每次費用。

Stage 7 範例程式必須拒絕空白模型輸出；streaming 只有看見非空白文字才算成功，first-token latency 也從第一段可見文字開始。PRO／CON Judge 與 LLM-as-judge 只接受完整 output contract，不得以 `PASS in text` 或 `WINNER in text` 猜測；角色變多不等於 bias 降低或答案變正確，重要結論仍要用固定 eval 與合格人員審查。Observability 只記安全的 exception 類別，不把可能含 secret、Prompt 或文件內容的原始 exception 訊息寫入 trace／log。Prompt caching 示範要跨過所選模型的官方最低長度，並只依 `cache_creation_input_tokens`／`cache_read_input_tokens` 說明建立或命中。Deploy 範例要限制 message 與 `max_tokens`、讓 liveness 不呼叫模型、區分 422／429／502／503，且 Docker 使用非 root user；README 以 loopback port、read-only filesystem 與必要環境變數教最小安全預設，同時明說不能把這些設定當成 sandbox。

Stage 5 的練習不能只叫讀者「看文件」卻宣稱已建立元件。Hook 練習至少要給一份可直接複製的最小設定、離線 smoke test、`/hooks` 落腳檢查與不保存 prompt／secret 的邊界；設定引用 project path 時使用 `command` + `args` 的跨平台 exec form，不能把 PowerShell 無法展開的 shell 變數寫進單一 command 字串。Agent SDK snippet 必須依現行 message type 實際讀到文字內容，regression 也要餵入 fake async `query()` 並驗證真的印出 `TextBlock`，只 compile 或比對字串不算通過。

Stage 5 的 installable Skill 範例使用 `${CLAUDE_SKILL_DIR}` 指向 bundled references，讓 personal、project 與翻譯版安裝後都能找到同一包檔案。README 先給 PowerShell 可複製安裝，再收合 POSIX；驗收先跑無網路 contract checker，再用 `/skill-name` 做產品內手動檢查。自訂 JSON 不能冒充 promptfoo config，結構測試也不能冒充 model-quality eval；要教 promptfoo 時，必須另給合法 provider／prompt／test 設定或明說只提供延伸入口。範例不能保存無來源成功率、原因比例、固定省時百分比或要求私人 Chain-of-Thought。

Stage 7.5 是 reading-map，不是第六個實作章。固定可見主線是「四個學習目標 → 六個粗體核心詞 → 12 個概念按問題分四組 → 我卡在哪裡的選擇圖與短表 → 可直接複製的四行工作邊界卡 → Model–Harness Fit 保留／簡化／移除判斷 → 五筆優先閱讀 → 24 筆完整學習資源 → 自我檢查」。六個核心詞是 **Work Boundary**、**Contract**、**Reflection**、**Autonomy**、**Budget Gate** 與 **Graceful Degradation**；Reflection 只要求可觀察的計畫、Action、Observation、測試與結果，不要求公開私人 Chain-of-Thought。12 個概念全部保留，但每次只選一組的一到兩個，不能把表格讀成全部都要安裝的清單。Model–Harness Fit 的短版規則與三語圖保持可見：這裡才回答某個 Harness 元件會不會過時，不是 Loop Engineering 的定義。先分「模型補強元件」與「長期安全責任」，一次只測一個元件，再用同一組品質與安全 Eval 決定保留、簡化或移除；模型變強不表示最小權限、sandbox、audit log、人工核准、Eval 或 recovery 自動過時。

時間、先備詞、12 個概念的來源與限制、失敗案例、cross-vendor harness、coding harness、benchmark、Dynamic Workflows，以及 Model–Harness Fit 的證據／Bitter Lesson／人機分工預設收合。24 筆完整資源表直接可見，固定分成 `5／5／5／5／4` 五組，使用獨立 `<tbody>` 與真正 HTML `rowspan`；三語 URL、順序與五星編輯評分一致。AutoGen 的 maintenance mode、Microsoft Agent Framework 的後繼定位、Sandbox Agents 的 Beta 狀態，以及 Dynamic Workflows 的版本、觸發、限制與供應環境使用 90 天 freshness marker；來源衝突時以現行官方產品文件優先。

Stage 7.5 保留三組低文字密度三語圖：四問題群組的 12 概念卡、「症狀 → 先讀哪一組」決策樹，以及用同一組 Eval 判斷 Harness 元件要保留／簡化／移除的三分圖。三個判斷是平行結果，不是成熟度階梯；圖不放文章名稱、閱讀時間、產品版本或任意固定門檻，避免正文更新後圖片仍殘留舊事實。OpenAI `Types → Config → Repo → Service → Runtime → UI` 只能教成特定 codebase 案例，不能畫成通用 Agent stack；舊 `stack-4layer`、`failure-lifecycle` 與 `principle-dependency` 圖組完成引用掃描後移除。Stage 7.5 沒有 example-hardening 第二層，本層完成三語內容、圖、freshness、reader-UX 與 content tests 後即形成一個可回溯 commit；未經使用者明確同意仍不推送、合併或清理 branch。

```
1. 1-2 句核心問題
2. ## 📌 學習目標
3. 該 stage 的可見核心詞（首次粗體、逐詞白話解釋）／最短選擇路徑
4. ## 🚪 進入條件 + ⏱ 時間估算（預設收合；Stage 6 / 7 可省略）
5. ## 📚 必修閱讀（全部必修項目直接可見；只有延伸閱讀收合）
6. ## 🛠 動手練習（核心練習先出現，延伸練習細節收合）
7. ## 🎯 精選 Projects 與學習資源（精選項目直接可見；只有完整 catalog 收合）
8. ## ✅ 進 Stage N+1 前的自我檢查
```

### 漸進式揭露

- 不展開任何 `<details>` 時，讀者仍要看得懂「這章要學什麼、先做哪一題、成功長什麼樣」。
- 核心路標的 icon 必須保留並保持一致：`📌` 學習目標、`📚` 必修閱讀、`🛠` 動手練習、`🎯` 精選 Projects、`✅` 自我檢查。可調整白話標題，但不能在精簡時拿掉路標。
- 動手練習的第一個動作優先給可直接複製、貼上或執行的最小成品。不要先叫初學者抄空白模板；空白模板只適合放在讀者看過成品之後的自行改寫步驟。
- 折疊與否看讀者現在需不需要。所有被稱為「必修閱讀」的項目、精選 Projects、精選學習資源與安全警告保持可見；時間、先備工具、費用、完整 catalog、補充原理、疑難排解與延伸清單預設收合，且 `<details>` 不加 `open`。若一張長表本身就是本章的精選清單，它仍保持可見，不能只因為列數多就藏起來。
- 可被其他頁面深連結的 heading 必須留在 `<details>` 外。標題後先給一句成果，再收合詳細步驟，否則瀏覽器會跳到一個仍然看不見的位置。
- 雙路徑練習仍以 Ollama Path A 為主要可執行路徑，但不再一律展開。練習標題、成果與第一個動作保持可見；只有在 Path A 是讀者眼前唯一要做的事，而且展開後內容很短時，才可使用 `open`。長程式碼與疑難排解預設收合。Anthropic Path B 仍預設收合；外層若已是延伸練習的收合區，內層不得預設展開。

### Reader UX ratchet

- `scripts/reader-ux-pages.yml` 只登記已完成三語遷移與人工複查的頁面。未遷移頁面不會因新規則一次全部失敗。
- `scripts/check-reader-ux.py` 使用保守的 source-level proxy：計算第一次開頁時可見 Markdown 的非空白字元。預設展開內容與可見 fenced code 會計入；HTML comment 與收合內容不計入。這是可重複的 ratchet，不宣稱等於瀏覽器 DOM 字數。
- 每頁分別設定三語字數上限、預設展開數量、必須留在 `<details>` 外的精確 heading／anchor、核心詞契約，以及分組資源表的 `rowspan`。完成一次精簡後只能維持或收緊，不可靜默放寬。
- 時間、先備條件、環境、費用、預算、選修、補充資料、疑難排解與完整 catalog 可預設收合。必修閱讀、精選 Projects 與精選學習資源直接可見。
- Gate 只證明可量測的結構沒有倒退。第一次讀者能不能用自己的話說出下一步，仍要在人工審查確認。

### 公開入口固定結構

三語 `README*` 與 `index*` 必須把真實路線說成「8 個主題 Stage，加上 Stage 0 準備關與
Stage 7.5 進階閱讀站」，合計 10 個學習站；不能只寫 8 stages 後又突然出現 0 或 7.5。
首頁卡片依序顯示 Stage 0、1、2、3、4、5、6、7、7.5、8。README 的路線表把最後一欄
用來回答「做完會得到什麼」，不在首屏排滿週數；Track A／B 的完整估算保留在一個預設
關閉的 `<details markdown="1">`，方便需要規劃的人查看。

README 的必讀入口、精選專案、相關資源與兩條 track 保持可見。練習說明先讓讀者直接
複製／執行 `starter.py`，一次只改一件事並重跑測試；不要求先抄空白檔案或整份重寫。
三語 banner 固定用 Image 2.0 PNG，同一 `1672×941` 版面顯示 Stage 0–1–2 後分流；Track A
固定是 `A1 → A2 → Stage 5 → A3 → Stage 8`，Track B 固定是
`3 → 4 → Stage 5 → 6 → 7 → 7.5 → Stage 8`，最後才接五條角色路線。圖上不放週數、
月份、每週時數、價格、版本、年份或 stars；箭頭、文字、icon 與框線不得重疊。

### Setup guide 固定結構

`resources/setup-guide*` 是零背景讀者的入口，不是工具安裝百科。固定可見順序為「這頁能幫什麼 → Web／Desktop／IDE／CLI Agent／API 五選一 → 七個核心詞 → 五個必讀官方起點 → A–E 的成果與第一個動作 → 完成檢查 → 下一站」。讀者選一條路即可，不把五種入口寫成由簡到難、也不要求全部安裝。

必讀官方起點、五星編輯推薦、API Key 三不規則、`.gitignore` 先於 `.env`、可直接複製的 hello world 與 A–E 深連結保持可見。完整 Web／Desktop／IDE／CLI catalog、其他 Provider、替代安裝、系統條件、排錯、`CLAUDE.md` 與 Skill 完整範例可以收合；7 個 `<details markdown="1">` 全部預設關閉。完整入口表用 `4／4／5／7`、必讀表用 `2／1／1／1`、Provider 表用 `7／1` 的真正 rowgroup 合併分類。

安裝命令、驗證方式、API Key／authentication、Provider 入口與專案狀態使用 90 天 freshness marker。固定價格、免費週期、促銷 credits、沒有來源的「最便宜／最強」與 Node-first 舊安裝路徑不得寫回。這頁的五門選擇表比裝飾性概念圖更直接，所以不為了版面齊全而新增圖片。

### Examples index 與 Agent 工具分類固定結構

`examples/README*` 是可執行範例的入口，不再複製 Stage 1 的完整模型與價格 catalog。固定可見順序為「五個核心詞 → 四個學習目標 → 三份必讀 → 第一個 Mock 命令 → Path A／B／C → 實際資料夾索引 → 三個本機預設 tag → 資料夾契約 → 六筆評分資源 → 完成檢查」。實際資料夾數、Ollama tag 與下載大小由 fact pack 和測試鎖定；環境、費用、Windows 編碼、貢獻與排錯預設收合。必讀、Stage 索引與完整 `2／2／2` 資源表保持可見。

`resources/agent-paradigms*` 用三條獨立軸教工具分類：**Identity** 說工作、**Surface** 說入口、**Deployment** 說位置；不再把 IDE、Terminal、Provider 選擇、Cloud 與 Edge 寫成五個互斥產品型態。OpenCode／Pi 是 Coding Agent／Harness，OpenRouter 是 Router，Ollama 是 Local Runtime；Subagent 是工作分派方式。必讀、Subagent 定義與完整 `5／2／2／3` 評分資源表保持可見；生活情境與部署安全細節可收合。不得凍結 stars、provider 數、VPS／硬體價格、推理上限或「零資料外洩」等絕對承諾。

### Resource hub 固定結構

`resources/README*` 是工具櫃入口，不是第十二份教材。固定可見順序為「我現在卡在哪裡 → 五個資源類型核心詞 → 11 份完整參考資料 → 回主線的位置 → 30 秒完成檢查」。全部 11 份入口保持可見；只有「為什麼分檔」與 maintainer 規則放進兩個預設關閉的 `<details markdown="1">`。

完整表固定使用 `4／2／2／2／1` 五個 `<tbody>`，以真正的 `scope="rowgroup"` 與 `rowspan` 合併同類型欄位。三語檔名、順序、用途與限制一致。不要放容易漂移的行數、GitHub stars 或舊產品名稱；新 reference 必須有獨立工作、被至少三個 stage／track／branch 使用，否則留在原章節。

### 課程地圖固定結構

`resources/courses*` 先幫讀者選一門課，不做證書排行榜。可見順序固定為「五個證書／課程核心詞 → 按需求選一條 → 12 筆精選課程與學習路線 → 可直接複製的五行作品證據卡 → Stage 3／4／7 返回路線」。證書限制與清單維護方法可以收合；精選課程、編輯評分與作品卡保持可見。

12 筆主資源依 `3／5／2／2` 分成免費打底、建構與上線、較長系列課、中文供應商路線。每組使用獨立 `<tbody>`、`scope="rowgroup"` 與真正 `rowspan`；一列只放一個主課程 URL，中文伴讀等補充入口放在表格外。星等只表示教學價值、實作完整度、更新狀態與可轉移性，不表示證書排名，也不保存 GitHub stars。

**Certificate of Completion**、**Skill Badge**、**Professional Certificate** 與 **Certification Exam** 必須分開定義。沒有官方證書條件就寫未明示，不自行補成「免費證書」；費用、cohort、證書、評量與 repository status 使用三語一致的 90 天 freshness marker。官方頁證明課程與證書事實，canonical repo 證明開源教材狀態，第三方文章只能當線索。

### 全站白話規則（ELI5）

這是整份學習地圖的共同 gate，不是 Stage 0 的特殊語氣。目標是讓五歲小孩也能跟得上「現在要做什麼」，但不把技術內容寫錯或寫成幼稚口吻。

- 技術詞第一次出現在可見教學文字時，用**粗體**標出；緊接著先說白話用途，再保留正確術語。例如：「讓程式拿資料的入口（**API**）」。頁面 H1 可以直接使用章名，但正文第一次使用仍要套用這條規則。
- 漸進式揭露只能收起次要細節。後文、練習或 self-check 會用到的核心名詞，必須留在可見主線，並在第一次出現時用白話解釋；不能為了縮短頁面而刪掉。
- 一句只說一件事，一個步驟只要求一個主要動作。長句拆開，縮寫與 jargon 不可在可見主線中突然出現。
- 指令、檔名、錯誤碼、模型名稱、價格與數字保持精確；ELI5 不能拿來刪除必要條件或安全提醒。
- 若一個概念需要多段說明，主線先留一句「它有什麼用」與下一步，完整原理放進預設收合的 `<details>`。
- Review 時不只問內容是否正確，也要問第一次來的讀者能否在不展開選單時，說出下一步與完成標準。

### 核心詞契約

- 每個完成回溯的 Stage／Track，都要在第一個練習前放一個可見核心詞區；不能藏進 `<details>`。
- 每個詞獨立說明「它是什麼、像什麼、這章用它做什麼、正確技術名稱」。先用白話搭橋，再保留英文名、縮寫或規格名稱，讓讀者之後查得到。
- 核心詞只收後文、練習或 self-check 真的會用到的概念。普通名詞不為了湊數拉進來；也不能為了縮短頁面刪除重要術語。
- 三語使用相同概念 ID 與順序，內容意思一致。翻譯可以自然，但不能一種語言多講限制、另一種語言少講用途。
- `scripts/reader-ux-pages.yml` 的 `core_terms` 會鎖住核心區與第一題的位置、第一次可見用法的粗體、定義標籤順序和最低解釋長度。這是結構 gate；比喻與定義是否正確仍由人工 review 判斷。

### 概念圖契約

- 圖只整理已經用白話定義過的關係，不能讓新名詞先在圖裡突然出現，也不能用圖片取代可搜尋、可翻譯、可被螢幕閱讀器讀到的正文。
- 全站預設沿用主頁 README 的舒服、清楚、簡單、直白風格：奶油白底、深藍主字、少量亮色、圓角卡、簡單線條 icon、充足留白與一個主要閱讀方向。每張圖只回答一個核心問題；放不下就拆圖，不能縮字硬塞。
- 新畫或重畫的概念圖以 Image 2.0 產出 PNG，不用臨時 SVG 代替。舊圖不因這條規則一次全部重做；輪到該章重畫時才套用這個 ratchet。
- 三語頁使用同一畫布比例、構圖、格線與語意，各自引用 `.png`、`.en.png`、`.zh-Hans.png`；每張都要有在地化 alt text。三語卡片位置、外距、內距與同層高度保持一致。
- 箭頭只走留白通道，不穿過文字、icon 或其他卡片；arrowhead、icon、標籤與框線不得互相重疊。所有同層卡片依共同格線、等高與一致內距對齊。
- 型號、價格、數量與狀態等易變事實，必須和正文採用同一官方證據。沒有通則就不用看似精確的固定數字。
- 產出後逐張以原尺寸人工檢查安全邊界、文字、繁簡字形、箭頭方向、共同格線與對比，再跑 image-locale gate 與三語網站 build。任何文字、icon、箭頭或框線重疊都視為失敗，不用「縮小看還可以」放行。
- 發布站由 `mkdocs_hooks.py` 統一替非首屏教學圖加 lazy loading、async decoding 與可鍵盤操作的原圖入口；README 頂端 banner 保持 eager。不要在各章重複手寫 HTML。新增或替換圖片時必須通過 `check-image-delivery.py` 的單圖、單頁、總量與 rendered-HTML ratchet；若要放寬上限，PR 必須附瀏覽器量測與理由。人工另以 320／375／768／1440 px 檢查圖、caption、表格與觸控目標，不能把「沒有 overflow」當成圖中文字已可讀。

### Glossary 固定結構

- Glossary 是查字入口，不是一般章節。快速地圖、工具身分表、每個詞的 heading 與一句白話定義都保持可見，讓搜尋、深連結與螢幕閱讀器直接找到答案。
- 只有 maintainer 用的完整分類表、來源與查核說明可以預設收合。不能把重要詞的最短定義藏進 `<details>`。
- 工具身分要分清 Provider API、Router、Model Runtime、Coding Agent／Agent Harness 與 Agent Framework；同一個產品能連到別的層，不代表它們是同一種東西。
- 型號、價格、context 與固定 token 換算不在 Glossary 複製快照；Glossary 連回有 freshness gate 的章節或官方文件。協定版本與產品狀態只寫已查證範圍，不用第三方排名補空白。

### 易變資訊與查核日期

- 模型名稱、價格、context、授權、preview / GA / deprecated 狀態，只能引用供應商正式文件、release notes 或官方 model card。
- 有易變資訊的頁面把 ISO 查核日期用小字放在受影響的表格或段落附近；只有該內容本身是補充資料時才可跟著收合。頁首 `freshness` HTML comment 不顯示，但要寫繁中 canonical 路徑、`verified_on`、scope 與最大查核週期，且三語完全相同。
- 可見日期只寫查核範圍與日期，不加通用的永久性提醒。超過建議週期由排程提出 warning；缺少 marker、格式錯誤、未來日期或三語不一致則由 gate 阻擋。
- 後續每個 stage 使用獨立 PR 完成事實查核、繁中定稿、三語複查與 review，不建立跨全站的大型 freshness diff。

**已知例外**：

- **Stage 0**：prerequisite gateway，使用可見的跳過判斷、單一整合練習、18 筆五星學習資源與短版完成檢查；時間、環境、補充練習與名詞預設收合（見「Stage 0 為什麼可以 skip」）
- **Stage 5**：分 7 個核心 sub-stage（5.1-5.7）+ 5.8 SDK（選修、包成產品或服務才需要），每個 sub-stage 各有自己的 學習目標 / 必修閱讀 / 動手練習 / 精選 Projects
- **Stage 6 / 7**：直接跳過 進入條件 section（前面 stage 已隱含 prerequisite）
- **Stage 7.5**：reading-map（進階概念 + reading path），沒有 動手練習、只有輕量 self-check——是 production 之後的 frontier 概念地圖，不寫 code
- **Stage 8**：兩軌共用的 interface 選擇 hub。可見主線先定義 8 個粗體核心詞，再用平行選擇圖分清 Search／Fetch、Browser Use、Computer Use、Sandbox，接著保留四道安全檢查、兩題第一步、五筆精選入口、21 筆完整五星資源與短版 self-check。Computer Use／benchmark、Browser Use、Sandbox、兩軌進階做法、安全案例與未來介面放進 9 個預設關閉選單；完整資源表固定用 `5／5／4／5／2` 五個真正合併的 rowgroup 並保持可見。四張介面卡不是固定升級順序，舊 heading 以空 anchor 保留深連結。

每個 section 的功能：

### 學習目標
- 必須**可量化**（不是「了解 X」，是「能用 PyTorch 寫一個 ReAct agent」）
- 4-6 個 bullet（多會 dilute、少會缺失）
- 每個 bullet 對應 1 個 self-check question

### 進入條件
- Stage 跳級者的 self-test：「你已經會這些就能直接從這個 stage 開始」
- Stage 0 沒這個 section（Stage 0 本身就是 entry condition）

### 必修閱讀
- 3-5 個 link（多會讀不完、少會 under-cover）
- 該 stage 開始前 / 中 / 後都行，但「不讀就跟不上」是判準
- 偏好官方 doc / 經典論文，不放長部落格
- section heading、閱讀目的與全部必修連結直接可見；延伸閱讀才收合，避免把「必修」藏起來後又要求讀者記得打開

### 動手練習 Projects
- 通常 3-5 個（Stage 1 / 3 因為要 cover 多個概念，會到 5-6 個）
- 每個都有具體成功標準（跑出某個輸出、看到某個錯誤等）
- **必須是「不動手就學不會」的東西**——光讀光看不算
- 動手練習 跟 self-check 是 **conceptual coverage 對應**（不是 1:1 編號對應）——跑過 動手練習 後，self-check 整體應該能過；單一條 self-check 可能對應到多個 動手練習
- Stage 5 因為 sub-section（5.1-5.8）結構，動手練習 分散在各 sub-section

### 精選 Projects
- 跑完 動手練習 後的延伸學習
- 精選項目與五星編輯推薦度直接可見；只有更長的完整 catalog、安裝細節與替代方案收合
- 每個 entry 照 [style guide](../resources/style-guide.md) 1 schema
- 事實由現行官方文件、規格或 model card 證明；動手路徑再搭配知名或廣泛使用的代表 repo。人氣只能幫忙找候選，不能取代維護、License、安全、用途與限制的查核，也不保存會變動的 GitHub stars 數字。
- 數量：通常 7-15 個（Stage 5 例外，20 個分散在 4 個 sub-section）
- 分類型資源表若同一分類連續出現兩列以上，每個分類使用獨立 `<tbody>`，分類欄再以 `scope="rowgroup"` 與 `rowspan` 合併；欄位表頭使用 `scope="col"`。這讓螢幕閱讀器與視覺版面讀到同一組關係，也不讓讀者重複掃描相同標籤。不同分類不可只因欄位文字相同就跨組合併。

### 自我檢查
- **measurable**——能 verify 的不是「了解 X」
- 通常 4-6 個 checkbox（依 stage 範圍調整；不固定數）
- binary judgment（會 / 不會），全部能勾才算通關

---

## 動手練習設計原則

### 為什麼必跑、不能只是讀

Stage 3 的 6 個動手練習是整個 catalog 最重要的設計決定。理由：

agent 寫過 vs 沒寫過 ≠ 多讀一篇 paper vs 少讀一篇。寫過的人後面學 LangGraph 知道 framework 在抽象什麼；沒寫過直接學 framework 會被 magic 困住。

所以 Stage 3 結尾的 gate 會直接檢查：讀者能否說出 `schema → call → execute → result → answer`，並寫出有 allowlist、參數驗證、最大步數與停止條件的 loop。跳不過就回練習 1 或 3 重跑，不必重讀整章。

### 具體成功標準（不是「了解 X」）
反例：「了解 ReAct pattern」→ 不可量化
正例：「給 5 個工具的 agent 完成『找台北人口除以紐約人口』的多步推理」→ 可量化

### 數量
- 3-5 個是 sweet spot
- 多會 dilute（讀者覺得負擔大、跳過）
- 少會 under-cover（譬如 Stage 1 只有 3 個 動手練習，但要涵蓋 API call / token / pricing / cross-provider / error handling / local LLM——所以該 stage 後來補到 6 個）
- Stage 3 也是明確的 6 題例外：完整來回、多工具、ReAct loop、多步任務、錯誤處理與 schema eval 各自有不同成功條件；主線先要求 1–3，4–6 作為穩定性加固，避免一次造成負擔。
- Stage 5 先用五題累加練習帶讀者動手，再以 5.1–5.8 作為分主題延伸入口；不要把每個延伸入口誤寫成各自都有 2–3 題

---

## Entry 選入 / 排除原則（補強 [style-guide](../resources/style-guide.md)）

style-guide 講格式、用詞、license。這份補跨 stage 的考量：

### 跟 stage 核心問題的相關度
entry 的「教什麼」應該是該 stage 核心問題的一個答案的具體實作。

- Stage 1 核心問題：LLM 是什麼。→ Anthropic Cookbook（教怎麼用）✓、rasbt/LLMs-from-scratch（教內部）✓
- Stage 1 核心問題不該 cover：tool use（那是 Stage 3）、memory（那是 Stage 6）

### Entry 不重複
- 同一 repo 在不同 stage 出現要有不同 framing（譬如 `obra/superpowers` 在 Stage 5 是 SKILL.md collection，在 for-developer 是 TDD skill）
- framing 重複的 entry 要刪一個

### 廣度 vs 深度
- 同類型只收足以說清楚取捨的代表入口；數量本身不能證明完整或有用。
- 同 audience 的項目要各自補上不同工作、限制或部署形狀；只換名字但 framing 相同的 entry 不重複收錄。

---

## 公共資源入口與 catalog 的固定閱讀形狀

公共資源分成三層，不能把首頁、索引與完整 catalog 混成同一堵工具牆：

1. `RESOURCES.md` 先讓讀者按工作選路，直接看見 **MCP**、**Skill**、**Plugin** 三個核心詞、五個安全起點與 16 筆有編輯評分的精選資源。精選表使用 `4／3／4／4／1` 五個真正合併的 rowgroup；只有挑選規則與補充治理可以收合。
2. `resources/README.md` 直接顯示七個工作入口；維護者說明與補充導覽預設收合。
3. `resources/mcp-skills-catalog.md` 直接顯示全部工作分類與每類安全邊界；完整 entry 放在各分類的預設關閉 `<details>`，因為讀者只在需要該工作時才展開。機器可以計數，讀者頁面不宣告會自然漂移的總數。

三語必須保留相同的 entry URL、順序與 `⭐⭐－⭐⭐⭐⭐⭐` 編輯推薦度；評分不是 GitHub stars，也不是客觀排行榜。官方狀態、hosted endpoint、認證、權限與 service availability 以供應商文件為準；社群 repo 的 canonical owner、redirect、archive、license 與維護訊號由 repository-freshness workflow 掃描，再由人判斷。沒有 release 或較久未 push 只能是複查訊號，不能自動刪除仍穩定且有教學價值的工具。

catalog 不使用 popularity 排名、固定 GitHub stars、固定安裝時間、會自然改變的整合數、免費額度保證、單一 last-commit 日期或永久模型分工。高影響工具先教測試資料、read-only、最小權限與人工核准；金融 entry 必須明說不是投資建議。`modelcontextprotocol/servers` 只作 reference implementation，不當成 production 推薦清單；產品顯示名稱使用 Gemini Notebook，舊的 NotebookLM 只留在 package、URL 或歷史識別說明。

---

## Self-check 怎麼設計

### Measurable 是核心
反例：

- 「了解 LangGraph」 ❌
- 「能解釋 LangGraph 為什麼用 graph」 ❌（subjective）
- 「能寫一個 LangGraph workflow 含 conditional edge + checkpoint」 ✓（binary）

### 跟 動手練習 對應（conceptual coverage，不是 1:1 編號）
跑完該 stage 全部 動手練習 之後，整份 self-check 應該能過。但**不要求 Hello-N 對應 self-check N 號這種編號 mapping**——一條 self-check 可能 cover 多個 動手練習，反之亦然。範例：Stage 3 的 self-check 第 1 條「定義一個 tool schema」對應 練習 1，但 self-check 第 2 條「不靠 framework 寫 ReAct」其實是 練習 3 的能力。

### 例外：abstract concept check
有些核心問題很難 measurable（譬如「為什麼 agent 需要退出條件？」）——這時用「**能不能口頭解釋給朋友聽**」做替代。但這種 check 不該超過 self-check 總數的 30%。

---

## Stages 之間的銜接

### 為什麼 4 → 5 → 6 → 7 → 8 是這順序
- 4 framework 後 → 5 Claude Code 生態（為什麼 Claude Code 是核心？因為它把 5.1-5.4 的概念集成在一個工具裡）
- 5 → 6 memory（agent 有 framework 之後才會問「怎麼記住」）
- 6 → 7 multi-agent（單 agent + memory 都會了，才考慮多 agent）
- 7 → 8 agent 操作介面（agent 本身蓋好了，才學怎麼讓它操作 API 以外的真實環境：螢幕 / 瀏覽器 / sandbox）

不是純線性——Stage 4 有「memory peek」指 Stage 6（「LangGraph 有 checkpoint，那是 memory 的東西，到 Stage 6 會講」），讓讀者知道延伸但不卡關。

### 跨 stage walkthrough 怎麼用
[`walkthroughs/build-first-agent-in-7-steps.md`](../walkthroughs/build-first-agent-in-7-steps.md) 用同一個 Paper Summary Bot 串完 Stage 1 到 7。這份是 stage 之間銜接的 ground truth：每個 stage 結束時 agent 應該長什麼樣，下一 stage 怎麼增加新層。

如果某個 stage 改了結構（譬如 Stage 6 換了 vector DB），walkthrough 也要同步改——是 maintain cost，但確保 stage 之間真的能串得起來。

---

## ⭐⭐ 標記為什麼放 Stage 5

兩個原因：

### 1. 這 stage 是 Claude Code 使用者的核心
Repo 名字是 `awesome-agentic-ai-zh`，受眾偏 Claude Code 使用者。Stage 5 是這個生態的完整教學——不會這 stage 就不算懂 Claude Code。

### 2. 內容量比其他 stage 偏大
- 多數 stage：1-2 週、7-15 個 entry
- Stage 5：3-4 週、4 個 sub-section、20 個 entry
- Stage 7 也大（22 個 entry），但結構是 flat 的——Stage 5 的 sub-section 結構是它特別需要 ⭐⭐ 提醒的原因

所以額外加 ⭐⭐ 提醒讀者「這個 stage 比較大、結構比較複雜，別跳」。Stage 3 加 ⭐ 是因為「Hello Agent 是整個 catalog 最重要的轉折點」（不寫 ReAct 寫不出 agent）。

---

## Stage 0 為什麼可以 skip

Stage 0 不是 stage——它是 prerequisite gateway。

- Python / git / CLI / JSON 已經會的人 → 直接 Stage 1
- 不會的人 → 用一個不需帳號或 token 的小工具，同時練 Python、API、JSON、CLI 與 Git

Stage 0 的可見主線固定為「skip 條件 → 4 個學習目標 → 1 個整合練習 → 18 筆五星學習資源 → 短版完成檢查」。時間、環境、分項補充與名詞放進預設收合的 `<details>`。它存在是為了**讓真的初學者不會在後面 stage 卡住**，但不把這個 repo 變成完整的 Python 或 Git 教科書。

---

## 不在這份的內容

- **個別 stage 的 entry 詳細**：見 `stages/0X-...md` 本身
- **branch 設計理由**：見 [`../branches/DESIGN.md`](../branches/DESIGN.md)
- **entry schema / 用詞規範**：見 [`../resources/style-guide.md`](../resources/style-guide.md)
- **跨 stage 範例**：見 [`../walkthroughs/build-first-agent-in-7-steps.md`](../walkthroughs/build-first-agent-in-7-steps.md)

# Stage 設計筆記

> 給 maintainer 的內部文件，不是讀者面向的內容。
>
> 為什麼是 8 個 stage、每個 stage 結構為什麼這樣切、動手練習 為什麼必跑、self-check 怎麼設計——這些設計決定的記錄。

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

- 第一遍先用五個可見核心詞分清 **LLM**、**Provider API**、**Router**、**Coding agent** 與 **Local runtime**。OpenRouter 放在 Router；OpenCode V2 與 Pi 放在 coding agent／harness；Ollama 放在 local runtime。
- `📌`、`📚`、`🛠`、`🎯`、`✅` 路標保持可見。時間、帳號、費用、完整步驟與 11 筆工具表預設收合。
- CLI-1 的第一個請求使用可直接複製的完整 `text` block。CLI-1 至 CLI-4 的標題、anchor 與一句話成果保持可見。
- 11 筆工具表固定為 `4／5／2` 三組，保留既有五星編輯評分並移除會變動的 GitHub stars 數字。評分是路徑建議，不是總排名。

### A2 的固定閱讀形狀

- 第一遍只教三個可見核心詞：「Project instructions 像共同守則、Skill 像按需操作卡、One-off prompt 像臨時交代」，並保留 CLI-5 至 CLI-8 的標題、anchor、成果與 A3 入口。
- CLI-5 用「用途／禁止事項／驗證指令／交付格式」四欄做最小規則卡；不把 persona 或行數門檻當成跨 CLI 通則。
- CLI-6 教目前的 `SKILL.md`，只在相容說明提 `.claude/commands/`。核心內容可以共用，工具專屬的資料夾、frontmatter、permission 與 tool 名稱分開說。
- 時間、先備條件、完整工具位置、CLI-7／CLI-8 步驟、multi-agent、疑難排解與完整資源表預設收合。
- `📌`、`📚`、`🛠`、`🎯`、`✅` 路標保持可見。完整資源表按語意分組；每組一個 `<tbody>`，分類欄用真正 `rowspan` 合併。三語的 rowgroup、URL、評分、命令、日期與安全限制必須一致。

### A3 的固定閱讀形狀

- 第一遍先用三個可見核心詞 **MCP**、**CI**、**Observability** 與一條安全階梯說清楚主線：唯讀 → 最小權限 → 示範 repo → 人工檢查 → 最後才考慮寫入。
- CLI-9 至 CLI-12 的標題、anchor、一句話成果與最短路徑留在可見區；時間、閱讀、完整步驟、疑難排解與 playbook 放進預設關閉的 `<details>`。
- Playbook 4 的標題與成果留在可見區，保護既有跨頁深連結；多 agent、fallback 與 failure injection 的理論導回 Stage 7.5，不在 A3 重寫一次。
- `📌`、`📚`、`🛠`、`🎯`、`✅` 路標保持可見。完整資源表固定為 18 筆、五個語意群組，`rowspan` 為 `4／5／4／3／2`。同類型只顯示一次分類名稱；保留五星編輯評分，不放 GitHub stars、排行榜或會自然變舊的數量。
- A3 的自動化預設只讀、最小權限、可留下 receipt，且必須有人檢查。不能把自動 merge、push、deploy 或未受限的 MCP 寫成初學者第一步。

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
| **0** 基礎準備 | 「我的開發環境準備好了嗎？」 | 4 個 動手練習 self-test |
| **1** LLM 入門 | 「LLM 是什麼、token 怎麼算、不同 LLM 的差別？」 | 從 API call 到本地 LLM，含 from-scratch 訓練 |
| **2** Prompt 設計 | 「怎麼讓 LLM 照我的意思做事，而且知道修改有沒有用？」 | 四格 prompt / few-shot / 固定 eval / 一次只改一件事 |
| **3** ⭐ Tool Use & Agent 入門 | 「怎麼讓 LLM 呼叫外部工具？」 | 完整 tool round trip + 有界 ReAct loop + 6 個動手練習 |
| **4** Agent 框架 | 「哪個 framework 該學、為什麼？」 | LangGraph / AutoGen / CrewAI / Smolagents 對比 |
| **5** ⭐⭐ Claude Code 生態 | 「Claude Code 生態系怎麼吃？」 | MCP / Skills / Plugins / Marketplace 4 個 sub-stage |
| **6** Memory · RAG | 「怎麼讓 agent 記得事情？怎麼讓它能查自家文件？」 | embedding / vector DB / RAG / contextual retrieval |
| **7** 進階 Multi-Agent | 「multi-agent 跟 production 怎麼一起？」 | orchestration / eval / observability / SDK 進階 |
| **7.5** 進階概念地圖 | 「multi-agent 之後還有哪些進階 pattern 要認得？」 | 12 個進階概念 + reading path（不寫 code）|
| **8** ⭐⭐ Agent 操作介面 | 「agent 怎麼操作 API 以外的真實環境（螢幕 / 瀏覽器 / sandbox）？」 | Computer Use / Browser Use / Code Sandbox |

每個 stage 結尾的 self-check 就是 **「能不能回答這個核心問題」** 的 measurable 版本。

---

## Stage 結構（dominant pattern，非絕對 invariant）

多數 stage 保留以下 section；**呈現順序採漸進式揭露**。Stage 1 是第一個完成遷移的 pilot，其他 stage 在各自內容更新時逐章遷移，不要求在同一個 PR 一次重寫：

Stage 2 的固定主線是「目標／資料／規則／輸出 → Zero-Shot／One-Shot／Few-Shot → Chain-of-Thought 的正確邊界 → 六筆固定案例 → 一次只改一件事 → 比較分數」。三語概念圖固定放在可見核心詞之後：先由正文定義，再用同構圖整理關係；圖片不能取代定義，也不能畫入正文已撤掉的固定數字。程式碼、模型比較、安全補充與 18 筆完整資源表預設收合。CoT 必須先用白話解釋，但不當成要求模型公開完整內部推理的通用步驟。

Stage 3 的固定主線是「八個可見核心詞 → Tool Use 六步亮色圖 → 一般回答／Structured Output／Function Calling 的選擇 → 五條安全底線 → schema → Tool Call → 程式執行 → Tool Result → final answer → 有界 Agent Loop」。三語同構圖要清楚畫出模型只提出請求、程式先驗證再執行，以及 allowlist、HITL、最大輪數三個安全邊界；圖片不取代正文定義。六題的標題、成果與第一個可複製動作保持可見；完整程式、供應商差異、費用、排錯、Reflection 路由與 21 筆資源表預設收合。ReAct 使用可觀察的 action／observation loop 教學，不要求公開私人 Chain-of-Thought。

Stage 3 的六題也各有一個 `examples/stage-3/NN-*` 可執行資料夾。每題同時提供 Ollama Path A、Anthropic Path B，以及兩個不連網的 mock tests。模型產生的工具名稱、JSON 與欄位一律視為不可信輸入：程式先做 allowlist 與參數驗證，再執行工具；錯誤要帶回原本的 call ID，Anthropic client tool 使用 `is_error: true`。多輪迴圈必須有最大步數，並把正常完成、token 截斷、拒絕／其他停止原因分開。README 以 PowerShell 為第一條可複製路徑，再收合 macOS／Linux 指令；SDK 使用已查核的 major 範圍、雲端模型使用固定 ID，費用寫公式與查核日，不用沒有 token 假設的固定小數，也不用單次結果宣稱某模型一定更快或更穩。

Stage 4 的固定主線是「八個可見核心詞 → workflow／agent × single／multi 選擇圖 → 先用最簡單能完成任務的形狀 → 五種協作 pattern → 依需求選工具 → 五題練習」。八個主核心詞是 **Framework**、**Workflow**、**Agent**、**Orchestration**、**State**、**Checkpoint**、**Handoff** 與 **Human-in-the-loop（HITL）**；Supervisor、Worker、CodeAct 與 Type-safe 也必須在第一次可見使用時粗體解釋，不能為了縮短頁面刪掉。三語亮色圖只整理正文已先定義的關係，不放版本、價格、stars 或沒有通則的數字。

Stage 4 的時間、環境、完整閱讀、研究證據、進階 tool patterns、五題完整步驟、疑難排解與 18 筆完整資源表預設收合。`📌`、`🚪`、`📚`、`🛠`、`🎯`、`✅`，簡短進入條件、五題 heading／anchor、每題成果、第一個可複製 PowerShell 動作與預算提醒保持可見。資源表固定為五組 `4／6／4／3／1`，使用真正 HTML `rowspan`，保留編輯推薦星級、移除會變動的 GitHub stars；Preview、維護、凍結／歷史與遷移狀態依官方來源明寫。OpenAI Swarm 只作教育參考，不能再有 production 評分；框架版本、維護、授權與安全資訊使用 90 天 freshness marker。

Stage 4 使用兩層 stacked PR：第一層只定稿三語教材、官方事實包、圖、資源表與 reader-UX gate；第二層才更新五個 `examples/stage-4/` 資料夾的 current-major SDK、Ollama／Anthropic 雙路徑、安全邊界與離線測試。這讓閱讀設計和 executable API migration 可以各自回溯、review 與驗證。

Stage 4 的五個可執行資料夾必須各自建立 Python 3.11 `.venv`，不能把不同 framework 的 `requirements.txt` 合併安裝。每題的 Path A 與 Path B 測試都要實際走過核心行為；只確認 import 成功不算驗收。LangGraph 要測分支、checkpoint、`interrupt()` 與 `Command(resume=...)`；CrewAI 要測角色、handoff 與有界停止；CodeAct 只在受限 Docker executor 示範模型程式碼，Jupyter 控制埠只綁 loopback，並明說一般 bridge 仍可對外連線、不是 production sandbox；typed output 要明說格式正確不等於內容真實。

Stage 5 的固定主線是「九個可見核心詞 → 依問題選最小零件 → Track A／B 閱讀路線 → 五題累加式練習 → 5.1–5.8 延伸入口」。九個核心詞是 **Claude Code**、**CLAUDE.md**、**Skill**、**MCP**、**Hook**、**Plugin／Marketplace**、**Subagent**、**Worktree** 與 **Claude Agent SDK**。5.1–5.8 heading、練習標題、成果與第一個可複製動作保持可見；時間、認證、費用、完整閱讀、語法、prompt、排錯與資源表預設收合。不得用「精簡」刪掉 MCP 的 Tools／Resources／Prompts、Skill／Subagent 差異、Hook 阻擋邊界、Worktree 檔案隔離或 Agent SDK hosting 安全。

Stage 5 的 35 筆學習資源固定分成 `4／8／8／7／4／4` 六組，使用真正 HTML `rowspan`；三語保留相同 URL、順序與五星編輯評分，移除會變動的 GitHub stars。Claude Code、MCP、Skills、Plugins、Subagents、Dynamic workflows、Agent SDK 與 security 使用 90 天 freshness marker；查核日期只在最相關的關閉資源區以小字呈現。

Stage 5 的概念圖只回答「遇到哪種問題先用哪個零件」，不把 maintainer 的任意分層畫成產品架構真理。三語圖同構、亮色、低文字密度；八張選擇卡不加 1–8 編號，避免把選擇誤讀成固定順序。Subagent、agent view、agent teams、Dynamic workflows、Worktree 與 `/batch` 的成熟度與責任邊界以官方現行文件為準。Dynamic workflows 要教成可讀、可重跑的 JavaScript 編排，不得綁成某個 Claude 型號專屬功能；現行觸發方式是明說要 use／run a workflow 或使用 `ultracode`，literal `workflow` 只可放在 v2.1.160 前的歷史說明。找不到官方正式來源的功能名稱或模型綁定不得當成一般可用功能教學。

Stage 5 使用兩層 stacked PR：第一層定稿三語教材、官方事實包、圖、資源表與 reader-UX gate，也必須同步修正正文直接連到的 cookbook／glossary／Stage 7.5 術語矛盾，不能讓讀者點出去立刻看見舊說法；第二層才更新 `examples/stage-5/tool-calling-tutor/` 的可執行實作。兩層都保留 branch 與 upstream，未經使用者明確同意不合併、不清理。

Stage 6 的固定主線是「七個可見核心詞 → RAG／Memory 選擇 → 五題累加式練習 → 一個同時檢索與記憶的小專案 → 精選資源 → Stage 7 檢查」。七個核心詞是 **Retrieval**、**RAG**、**Embedding**、**Vector Store／Vector Database**、**Chunk**、**Reranking** 與 **Memory**；BM25、Hybrid Search、GraphRAG、Contextual Retrieval、HyDE、Multi-Query、RAG Fusion、Self-RAG、CRAG、Adaptive RAG、RAPTOR、DSPy、episodic／semantic／procedural memory、CoALA、Generative Agents 與 Reflexion 仍要保留白話定義，但放在有明確 summary 的關閉區，不能在第一遍淹沒練習。

Stage 6 的亮色三語圖固定畫成三條同構路徑：文件進入知識庫的 ingest path、問題取回證據再回答的 query path，以及重要狀態的 Memory write／read loop。圖片只整理正文已定義的關係，不把 vendor benchmark、固定 chunk size、top-k、成本倍數或模型排名畫成通則。五題 heading、anchor、成果、第一個可複製 PowerShell 動作與資料／預算提醒保持可見；時間、環境、完整閱讀、進階 RAG、Memory taxonomy、Chunking、Reflection、評測與完整資源表預設收合。

Stage 6 的 18 筆資源固定分成 `4／5／4／3／2` 五組，每組使用獨立 `<tbody>` 與真正 HTML `rowspan`。保留五星編輯評分，移除 GitHub stars 數字；官方文件、paper 與 canonical repo 負責證明事實，知名或活躍專案只負責提供動手入口。GraphRAG 維護狀態、Ragas canonical owner、Letta 現行開發入口、Zep Community Edition 歷史狀態，以及 RAG／retrieval／embedding／vector store／memory／evaluation／project status 使用 90 天 freshness marker。

Stage 6 同樣使用兩層 stacked PR：第一層定稿三語教材、官方事實包、圖、glossary 直接矛盾、資源表與 reader-UX gate；第二層才修正五個 `examples/stage-6/` 的 chunk 邊界、collection 隔離、真正 persistent memory、雙路徑與離線測試。兩層都保留 branch 與 upstream，未經使用者明確同意不合併、不清理。

Stage 7 的固定主線是「單一 Agent／Multi-Agent 決策 → 七個可見核心詞 → Prompt／Context／Harness／Loop／Graph 五層分工 → Harness 八項 production 檢查 → 工具角色辨識 → 五題可執行練習 → execution receipt 小專案 → benchmark 閱讀紀律 → 精選資源 → 自我檢查」。七個核心詞是 **Multi-Agent**、**Orchestration**、**Handoff**、**Harness**、**Eval**、**Observability** 與 **Guardrail**；先用白話和生活比喻定義，再保留正確術語。OpenRouter 是模型 API 入口，Pi／OpenCode 是 Agent runtime／coding agent，Orca／QM 是多 Agent 協作層；不得把三層寫成可互換的同類產品。

Stage 7 的時間、環境、費用、安全提醒、完整閱讀、Loop／Graph 補充、回饋與復原細節、練習步驟、benchmark 連結及完整資源表預設收合。五題 heading、anchor、成果與第一個可複製測試命令保持可見；成本／延遲仍是 Harness 第八項與 SDK 練習的必要觀念，但沒有對應資料夾時不得虛構第六題。外部排行榜只能教讀法，不能凍結 SOTA 分數、模型名次或第三方「最強」結論。

Stage 7 的 20 筆資源固定分成 `4／6／5／5` 四組，每組使用獨立 `<tbody>`、`scope="rowgroup"` 與真正 HTML `rowspan`。保留五星編輯評分，移除 GitHub stars；已封存、Preview、Alpha、best-effort 或維護紀錄不足的專案必須在限制欄明寫。Stage 7 同樣拆成 content 與 example-hardening 兩層 stacked PR：第一層定稿三語教材、來源、圖、資源與 reader-UX gate；第二層才更新五個 `examples/stage-7/` 的 SDK、模型、直接執行步驟、安全邊界與離線測試。未經使用者明確同意不合併、不清理 branch。

Stage 5 的練習不能只叫讀者「看文件」卻宣稱已建立元件。Hook 練習至少要給一份可直接複製的最小設定、離線 smoke test、`/hooks` 落腳檢查與不保存 prompt／secret 的邊界；設定引用 project path 時使用 `command` + `args` 的跨平台 exec form，不能把 PowerShell 無法展開的 shell 變數寫進單一 command 字串。Agent SDK snippet 必須依現行 message type 實際讀到文字內容，regression 也要餵入 fake async `query()` 並驗證真的印出 `TextBlock`，只 compile 或比對字串不算通過。

Stage 5 的 installable Skill 範例使用 `${CLAUDE_SKILL_DIR}` 指向 bundled references，讓 personal、project 與翻譯版安裝後都能找到同一包檔案。README 先給 PowerShell 可複製安裝，再收合 POSIX；驗收先跑無網路 contract checker，再用 `/skill-name` 做產品內手動檢查。自訂 JSON 不能冒充 promptfoo config，結構測試也不能冒充 model-quality eval；要教 promptfoo 時，必須另給合法 provider／prompt／test 設定或明說只提供延伸入口。範例不能保存無來源成功率、原因比例、固定省時百分比或要求私人 Chain-of-Thought。

```
1. 1-2 句核心問題
2. ## 📌 學習目標
3. 該 stage 的可見核心詞（首次粗體、逐詞白話解釋）／最短選擇路徑
4. ## 🚪 進入條件 + ⏱ 時間估算（預設收合；Stage 6 / 7 可省略）
5. ## 📚 必修閱讀（清單預設收合）
6. ## 🛠 動手練習（核心練習先出現，延伸練習細節收合）
7. ## 🎯 精選 Projects（一個推薦項目先出現，其餘分級收合）
8. ## ✅ 進 Stage N+1 前的自我檢查
```

### 漸進式揭露

- 不展開任何 `<details>` 時，讀者仍要看得懂「這章要學什麼、先做哪一題、成功長什麼樣」。
- 核心路標的 icon 必須保留並保持一致：`📌` 學習目標、`📚` 必修閱讀、`🛠` 動手練習、`🎯` 精選 Projects、`✅` 自我檢查。可調整白話標題，但不能在精簡時拿掉路標。
- 動手練習的第一個動作優先給可直接複製、貼上或執行的最小成品。不要先叫初學者抄空白模板；空白模板只適合放在讀者看過成品之後的自行改寫步驟。
- 時間、先備工具、費用、長表格、補充原理、疑難排解與延伸清單預設收合；`<details>` 不加 `open`。
- 可被其他頁面深連結的 heading 必須留在 `<details>` 外。標題後先給一句成果，再收合詳細步驟，否則瀏覽器會跳到一個仍然看不見的位置。
- 雙路徑練習仍以 Ollama Path A 為主要可執行路徑，但不再一律展開。練習標題、成果與第一個動作保持可見；只有在 Path A 是讀者眼前唯一要做的事，而且展開後內容很短時，才可使用 `open`。長程式碼與疑難排解預設收合。Anthropic Path B 仍預設收合；外層若已是延伸練習的收合區，內層不得預設展開。

### Reader UX ratchet

- `scripts/reader-ux-pages.yml` 只登記已完成三語遷移與人工複查的頁面。未遷移頁面不會因新規則一次全部失敗。
- `scripts/check-reader-ux.py` 使用保守的 source-level proxy：計算第一次開頁時可見 Markdown 的非空白字元。預設展開內容與可見 fenced code 會計入；HTML comment 與收合內容不計入。這是可重複的 ratchet，不宣稱等於瀏覽器 DOM 字數。
- 每頁分別設定三語字數上限、預設展開數量、必須留在 `<details>` 外的精確 heading／anchor、核心詞契約，以及分組資源表的 `rowspan`。完成一次精簡後只能維持或收緊，不可靜默放寬。
- 時間、先備條件、環境、費用、預算、必修閱讀、選修、補充資料、疑難排解與完整資源表不得預設展開。
- Gate 只證明可量測的結構沒有倒退。第一次讀者能不能用自己的話說出下一步，仍要在人工審查確認。

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
- 三語頁使用同一構圖與同一語意，各自引用 `.png`、`.en.png`、`.zh-Hans.png`；每張都要有在地化 alt text。
- 型號、價格、數量與狀態等易變事實，必須和正文採用同一官方證據。沒有通則就不用看似精確的固定數字。
- 產出後逐張以原尺寸人工檢查文字、繁簡字形、箭頭方向與對比，再跑 image-locale gate 與三語網站 build。

### 易變資訊與查核日期

- 模型名稱、價格、context、授權、preview / GA / deprecated 狀態，只能引用供應商正式文件、release notes 或官方 model card。
- 有易變資訊的頁面把 ISO 查核日期放進最相關的預設收合區，以小字顯示；頁首 `freshness` HTML comment 不顯示，但要寫繁中 canonical 路徑、`verified_on`、scope 與最大查核週期，且三語完全相同。
- 可見日期只寫查核範圍與日期，不加通用的永久性提醒。超過建議週期由排程提出 warning；缺少 marker、格式錯誤、未來日期或三語不一致則由 gate 阻擋。
- 後續每個 stage 使用獨立 PR 完成事實查核、繁中定稿、三語複查與 review，不建立跨全站的大型 freshness diff。

**已知例外**：

- **Stage 0**：prerequisite gateway，使用可見的跳過判斷、單一整合練習與短版完成檢查；時間、環境、補充練習、名詞與資源預設收合（見「Stage 0 為什麼可以 skip」）
- **Stage 5**：分 7 個核心 sub-stage（5.1-5.7）+ 5.8 SDK（選修、包成產品或服務才需要），每個 sub-stage 各有自己的 學習目標 / 必修閱讀 / 動手練習 / 精選 Projects
- **Stage 6 / 7**：直接跳過 進入條件 section（前面 stage 已隱含 prerequisite）
- **Stage 7.5**：reading-map（進階概念 + reading path），沒有 動手練習、只有輕量 self-check——是 production 之後的 frontier 概念地圖，不寫 code
- **Stage 8**：跟 Stage 5 一樣是兩軌共用 hub，分 3 層 interface（Computer Use / Browser Use / Code Sandbox）+ Safety / Security section，各層有自己的工具與練習

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
- section heading 與一句閱讀目的保持可見；連結清單預設收合，避免讀者還沒開始實作就先撞上資源牆

### 動手練習 Projects
- 通常 3-5 個（Stage 1 / 3 因為要 cover 多個概念，會到 5-6 個）
- 每個都有具體成功標準（跑出某個輸出、看到某個錯誤等）
- **必須是「不動手就學不會」的東西**——光讀光看不算
- 動手練習 跟 self-check 是 **conceptual coverage 對應**（不是 1:1 編號對應）——跑過 動手練習 後，self-check 整體應該能過；單一條 self-check 可能對應到多個 動手練習
- Stage 5 因為 sub-section（5.1-5.8）結構，動手練習 分散在各 sub-section

### 精選 Projects
- 跑完 動手練習 後的延伸學習
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
- Stage 5 因為 4 個 sub-section，每個 sub-section 再有 2-3 個 動手練習

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
- 同類型工具列 2-3 個就夠（譬如 vector DB 列 Chroma + Qdrant + pgvector + Weaviate，但不需要列 5 個更小眾的）
- 同 audience 工具列 3-5 個（譬如 coding agent 列 Cursor + Aider + Cline + Continue + Goose）

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

Stage 0 的可見主線固定為「skip 條件 → 4 個學習目標 → 1 個整合練習 → 短版完成檢查」。時間、環境、分項補充、名詞與 18 個學習資源放進預設收合的 `<details>`。它存在是為了**讓真的初學者不會在後面 stage 卡住**，但不把這個 repo 變成完整的 Python 或 Git 教科書。

---

## 不在這份的內容

- **個別 stage 的 entry 詳細**：見 `stages/0X-...md` 本身
- **branch 設計理由**：見 [`../branches/DESIGN.md`](../branches/DESIGN.md)
- **entry schema / 用詞規範**：見 [`../resources/style-guide.md`](../resources/style-guide.md)
- **跨 stage 範例**：見 [`../walkthroughs/build-first-agent-in-7-steps.md`](../walkthroughs/build-first-agent-in-7-steps.md)

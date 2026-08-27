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

### A2 的固定閱讀形狀

- 第一遍只教「專案規則像共同守則、Skill 像按需操作卡、單次 prompt 像臨時交代」，並保留 CLI-5 至 CLI-8 的標題、anchor、成果與 A3 入口。
- CLI-5 用「用途／禁止事項／驗證指令／交付格式」四欄做最小規則卡；不把 persona 或行數門檻當成跨 CLI 通則。
- CLI-6 教目前的 `SKILL.md`，只在相容說明提 `.claude/commands/`。核心內容可以共用，工具專屬的資料夾、frontmatter、permission 與 tool 名稱分開說。
- 時間、先備條件、完整工具位置、CLI-7／CLI-8 步驟、multi-agent、疑難排解與完整資源表預設收合。
- 完整資源表按語意分組；每組一個 `<tbody>`，分類欄用真正 `rowspan` 合併。三語的 rowgroup、URL、命令、日期與安全限制必須一致。

### A3 的固定閱讀形狀

- 第一遍先用三個白話詞與一條安全階梯說清楚主線：唯讀 → 最小權限 → 示範 repo → 人工檢查 → 最後才考慮寫入。
- CLI-9 至 CLI-12 的標題、anchor、一句話成果與最短路徑留在可見區；時間、閱讀、完整步驟、疑難排解與 playbook 放進預設關閉的 `<details>`。
- Playbook 4 的標題與成果留在可見區，保護既有跨頁深連結；多 agent、fallback 與 failure injection 的理論導回 Stage 7.5，不在 A3 重寫一次。
- 完整資源表固定為 18 筆、五個語意群組，`rowspan` 為 `4／5／4／3／2`。同類型只顯示一次分類名稱，不放 stars、排行榜或會自然變舊的數量。
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
| **3** ⭐ Tool Use & Agent 入門 | 「怎麼讓 LLM 呼叫外部工具？」 | function calling + ReAct + 5 個動手練習 必跑 |
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

Stage 2 的固定主線是「目標／資料／規則／輸出 → 六筆固定案例 → 一次只改一件事 → 比較分數」。程式碼、模型比較、安全補充與 18 筆完整資源表預設收合。CoT 保留為歷史與選修概念，不再當成所有模型都要輸出的通用步驟。

```
1. 1-2 句核心問題
2. ## 📌 學習目標
3. 該 stage 的核心詞 / 最短選擇路徑
4. ## 🚪 進入條件 + ⏱ 時間估算（預設收合；Stage 6 / 7 可省略）
5. ## 📚 必修閱讀（清單預設收合）
6. ## 🛠 動手練習（核心練習先出現，延伸練習細節收合）
7. ## 🎯 精選 Projects（一個推薦項目先出現，其餘分級收合）
8. ## ✅ 進 Stage N+1 前的自我檢查
```

### 漸進式揭露

- 不展開任何 `<details>` 時，讀者仍要看得懂「這章要學什麼、先做哪一題、成功長什麼樣」。
- 時間、先備工具、費用、長表格、補充原理、疑難排解與延伸清單預設收合；`<details>` 不加 `open`。
- 可被其他頁面深連結的 heading 必須留在 `<details>` 外。標題後先給一句成果，再收合詳細步驟，否則瀏覽器會跳到一個仍然看不見的位置。
- 雙路徑練習仍以 Ollama Path A 為主要可執行路徑，但不再一律展開。練習標題、成果與第一個動作保持可見；只有在 Path A 是讀者眼前唯一要做的事，而且展開後內容很短時，才可使用 `open`。長程式碼與疑難排解預設收合。Anthropic Path B 仍預設收合；外層若已是延伸練習的收合區，內層不得預設展開。

### Reader UX ratchet

- `scripts/reader-ux-pages.yml` 只登記已完成三語遷移與人工複查的頁面。未遷移頁面不會因新規則一次全部失敗。
- `scripts/check-reader-ux.py` 使用保守的 source-level proxy：計算第一次開頁時可見 Markdown 的非空白字元。預設展開內容與可見 fenced code 會計入；HTML comment 與收合內容不計入。這是可重複的 ratchet，不宣稱等於瀏覽器 DOM 字數。
- 每頁分別設定三語字數上限、預設展開數量、必須留在 `<details>` 外的精確 heading／anchor，以及分組資源表的 `rowspan`。完成一次精簡後只能維持或收緊，不可靜默放寬。
- 時間、先備條件、環境、費用、預算、必修閱讀、選修、補充資料、疑難排解與完整資源表不得預設展開。
- Gate 只證明可量測的結構沒有倒退。第一次讀者能不能用自己的話說出下一步，仍要在人工審查確認。

### 全站白話規則（ELI5）

這是整份學習地圖的共同 gate，不是 Stage 0 的特殊語氣。目標是讓五歲小孩也能跟得上「現在要做什麼」，但不把技術內容寫錯或寫成幼稚口吻。

- 第一次使用技術詞時，先用白話說用途，再保留正確術語；例如「讓程式拿資料的入口（API）」。
- 一句只說一件事，一個步驟只要求一個主要動作。長句拆開，縮寫與 jargon 不可在可見主線中突然出現。
- 指令、檔名、錯誤碼、模型名稱、價格與數字保持精確；ELI5 不能拿來刪除必要條件或安全提醒。
- 若一個概念需要多段說明，主線先留一句「它有什麼用」與下一步，完整原理放進預設收合的 `<details>`。
- Review 時不只問內容是否正確，也要問第一次來的讀者能否在不展開選單時，說出下一步與完成標準。

### 易變資訊與查核日期

- 模型名稱、價格、context、授權、preview / GA / deprecated 狀態，只能引用供應商正式文件、release notes 或官方 model card。
- 有易變資訊的頁面同時顯示 ISO 查核日期，並放置 `freshness` HTML comment；marker 要寫繁中 canonical 路徑、`verified_on`、scope 與最大查核週期，且三語完全相同。
- 查核日期只表示「那天逐項看過」，不是永久正確保證。超過建議週期由排程提出 warning；缺少 marker、格式錯誤、未來日期或三語不一致則由 gate 阻擋。
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
- 數量：通常 7-15 個（Stage 5 例外，20 個分散在 4 個 sub-section）
- 分類型資源表若同一分類連續出現兩列以上，每個分類使用獨立 `<tbody>`，分類欄再以 `scope="rowgroup"` 與 `rowspan` 合併；欄位表頭使用 `scope="col"`。這讓螢幕閱讀器與視覺版面讀到同一組關係，也不讓讀者重複掃描相同標籤。不同分類不可只因欄位文字相同就跨組合併。

### 自我檢查
- **measurable**——能 verify 的不是「了解 X」
- 通常 4-6 個 checkbox（依 stage 範圍調整；不固定數）
- binary judgment（會 / 不會），全部能勾才算通關

---

## 動手練習設計原則

### 為什麼必跑、不能只是讀

Stage 3 的 5 個動手練習 是整個 catalog 最重要的設計決定。理由：

agent 寫過 vs 沒寫過 ≠ 多讀一篇 paper vs 少讀一篇。寫過的人後面學 LangGraph 知道 framework 在抽象什麼；沒寫過直接學 framework 會被 magic 困住。

所以 Stage 3 結尾的「進 Stage 4 前的自我檢查」第一條就是：**「用不到 100 行 Python、不靠任何 framework，把 ReAct 迴圈寫出來」**——這是 binary 的 gate，跳不過就回去再跑一次。

### 具體成功標準（不是「了解 X」）
反例：「了解 ReAct pattern」→ 不可量化
正例：「給 5 個工具的 agent 完成『找台北人口除以紐約人口』的多步推理」→ 可量化

### 數量
- 3-5 個是 sweet spot
- 多會 dilute（讀者覺得負擔大、跳過）
- 少會 under-cover（譬如 Stage 1 只有 3 個 動手練習，但要涵蓋 API call / token / pricing / cross-provider / error handling / local LLM——所以該 stage 後來補到 6 個）
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

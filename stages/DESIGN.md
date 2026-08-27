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
| A2 | Workflow（CLAUDE.md / slash command / 任務拆解 / portable prompt） | → 最終 A2 |
| A3 | MCP 接 CLI | → 合進最終 A3 |
| A4 | 多 CLI 並用 | → 合進最終 A3 |
| A5 | Production CLI workflow（CI / cost / observability / plugin 打包） | → 合進最終 A3 |

合併邏輯：

- 草稿 A3 + A4 + A5 都是「**把 CLI 跟外部系統 / 流程接起來**」這同一件事的不同面向，砍 3 為 1 不會切碎概念
- 草稿 A1 邊界清楚（入門 + 選擇），保留為最終 A1
- 草稿 A2 邊界清楚（一個人在 CLI 內部如何工作），保留為最終 A2

最終 3 個 stage：

- **A1**：入門 + 選擇（CLI 安裝、認證、第一個任務）
- **A2**：Workflow Patterns（CLAUDE.md / slash command / 多步拆解 / portable prompt）
- **A3**：Integration & Production（MCP 接 CLI、多 CLI 並用、CI 自動化、cost / observability、plugin 打包）

判準：**3 個 stage 邊界清楚、不互相浸蝕**，每個 stage 對應一個明確的「我能跑出什麼」outcome。

### 為什麼 Stage 5 特別放在「兩軌共用」

Stage 5（Claude Code 生態）兩條軌都會碰到：

- Track A：A2 用 5.1（Claude Code 基礎）；A3 用 5.2（MCP）+ 選擇性用到 5.3（Skills）跟 5.4（Plugins）——A3 的 動手練習 CLI-12 會教 plugin 打包。讀的角度是「**怎麼用 Claude Code 把工作做好**」
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
| **2** Prompt 設計 | 「怎麼讓 LLM 照我的意思做事？」 | system / few-shot / CoT / DSPy |
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

多數 stage 用以下結構（Stage 0 / 5 / 6 / 7 / 7.5 / 8 有 documented 例外，見後）：

```
1. ⏱ 時間估算
2. ## 📌 學習目標
3. ## 🚪 進入條件 （Stage 1-4 有；Stage 6 / 7 省略，因為 Stage 5 已給足前置）
4. ## 📚 必修閱讀
5. ## 🛠 動手練習
6. ## 🎯 精選 Projects
7. ## ✅ 進 Stage N+1 前的自我檢查
```

**已知例外**：

- **Stage 0**：prerequisite gateway，沒有完整結構（見 「Stage 0 為什麼可以 skip」）
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
- 不會的人 → Stage 0 不是要從零教 Python，是給「我該不該學這 4 樣才能開始」的 self-test，順便給快速 reference 連結

所以 Stage 0 沒有完整的學習目標 / 動手練習 / self-check structure——只有「skip 條件」+ 「資源連結」。它存在是為了**讓真的初學者不會在後面 stage 卡住**，但不假設讀者要從這裡完整走完。

---

## 不在這份的內容

- **個別 stage 的 entry 詳細**：見 `stages/0X-...md` 本身
- **branch 設計理由**：見 [`../branches/DESIGN.md`](../branches/DESIGN.md)
- **entry schema / 用詞規範**：見 [`../resources/style-guide.md`](../resources/style-guide.md)
- **跨 stage 範例**：見 [`../walkthroughs/build-first-agent-in-7-steps.md`](../walkthroughs/build-first-agent-in-7-steps.md)

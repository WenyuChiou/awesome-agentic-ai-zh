# Stage 7 — 多 Agent 系統與穩定運作（Multi-Agent & Production）

> **繁體中文** | [简体中文](./07-multi-agent-production.zh-Hans.md) | [English](./07-multi-agent-production.en.md)

⏱ **時間估算**：2-4 週（約 15-30 小時）

> 💡 用語密度高（multi-agent / handoff / eval / observability / guardrails⋯）→ 翻 [`resources/glossary.md` 4 + 6](../resources/glossary.md#4-multi-agent)。

> 📋 **本章組成**：〔Multi-Agent · Production 化 是什麼（先定位）+ 五層工程分工 + 何時用 multi-agent〕→ 學習目標 → 進入條件 → 必修閱讀 → Harness Engineering（**8 個核心元件含 Cost/Latency**）→ 動手練習（含練習 6 Cost Optimization）→ **Agent Benchmark Landscape：怎麼看，不要只看排行榜** → 常用工具推薦 → 精選 Projects → 自我檢查
> 🔑 **關鍵名詞**：見 [`resources/glossary.md` 4 + 6](../resources/glossary.md#4-multi-agent)（multi-agent / orchestration / handoff / eval / observability / harness（模型外圍的執行與控制層））

最後一個階段。你正從「我會做 agent」走向「我能讓 agent **真的給人穩定用**——多個 agent 協作、有 eval、有 observability、能部署到可用環境」。範圍怎麼界定，看下面三句話。

## 🎯 Multi-Agent · Production 化 是什麼（先定位）

**本 stage = 多 agent 怎麼協作 + 把 agent 從 prototype 推到能穩定給人用的程度**。三句話釐清範圍：

- **不是只學 framework**——Stage 4 已教 framework 怎麼挑
- **不一定要 enterprise scale**——只要 agent 能讓別人用、就算 production 化
- **核心是 harness engineering**——8 個核心元件 + eval + observability + cost / latency 控制

**跟前後 stage 的分工**：

- **Stage 4** = 單 agent framework 怎麼挑、ReAct / Plan-Execute 等 pattern
- **本 stage** = **多 agent 協作** + **harness engineering**（執行系統工程）+ **部署到可用環境 / observability / eval**

### 五層工程分工：Prompt → Context → Harness → Loop → Graph

> 📍 **這一節是這個 repo 講「分層」的 canonical 出處**。其他章節提到分層時只會指回這裡，不各自重述一遍——以前六個地方各講一次，結果講出三種版本。

這五層**不是難度階梯**，是「**你在管多大範圍**」。而且它們不是並列的清單，是**一層撞牆、才生出下一層**（跟「call 一次 vs 多次」無關）：

| 層級 | 概念 | 目的（要解決什麼） | 撞到什麼牆 → 所以有下一層 | 在哪一章講 | 名稱來源 |
|---|---|---|---|---|---|
| 1 | **Prompt Engineering** | 這一次問對 | 它不知道你手上的資料 | [Stage 2](02-prompt-engineering.md) | 官方採用 |
| 2 | **Context Engineering** | 讓它讀到該讀的 | 知道了，也還動不了手 | [Stage 6](06-memory-rag.md) | 官方採用 |
| **3** | **Harness Engineering**<br>（**本 stage**） | 讓它真的動手，出錯不炸掉 | 一次跑不完一件大事 | **本 stage** | 官方採用 |
| 4 | **Loop Engineering**<br>（長時間執行） | 讓它自己做完，不用你盯 | 它自己跑，你就看不見它在幹嘛 | [Stage 5.6](05-claude-code-ecosystem.md) | ⚠️ 非官方名稱 |
| 5 | **Graph Engineering** | 看得到、管得住、能重來 | —（目前最外一層） | [Stage 4](04-agent-frameworks.md) | ⚠️ 非官方名稱 |

![Agent 工程五層 Stack](../resources/diagrams/agent-engineering-5layer.png)

> ⚠️ **「在哪一章講」不是閱讀順序**。第 4、5 層的主題剛好在比較前面的章節出現過（5.6 與 4），所以那一欄由上往下看會「倒退」。**照 Stage 0 → 8 的原順序讀就好**，這一欄只是告訴你想深入時翻哪裡。
>
> ⚠️ **第 4 層的 Loop 是「長時間」的意思**——跑數百步、跨 session 還能接下去、什麼時候該停。它跟後面 harness 元件表裡那個 `Agent loop`（單次執行內的機械迴圈）同名但不同層次，讀到那裡會再講一次。
>
> ⚠️ **「名稱來源」那一欄要看一下**。前三個詞廠商自己的文件在用（Anthropic 有 context engineering 專文、OpenAI 2026-02 用了 harness engineering）。**後兩個沒有**：Loop / Graph Engineering 是社群講出來的名字，概念真的成立，但 Anthropic 官方叫 *dynamic workflows*、Google ADK 與 Microsoft Agent Framework 叫 *graph-based workflow(s)*。你去查官方文件查不到「graph engineering」這個詞，不是你漏看。

**白話差異**：

- **Prompt** = 設計一個好的問法，讓模型這次回答準
- **Context** = 動態決定要放入哪些背景、記憶、文件、工具結果，讓模型知道現在情境
- **Harness** = 把 prompt、context、工具、狀態、流程控制、錯誤處理串成一套可以運作的系統
- **Loop** = 交代一個目標，讓它自己重複做到夠好為止，並且決定「什麼時候該停」、下次開新 session 還接得下去（**不是** harness 裡那個單次執行的機械迴圈）
- **Graph** = 先把工作拆成幾個格子、畫出誰接誰，讓過程看得到、能從中間接著跑

### 迴圈跟圖差在哪（這兩個最容易混）

**迴圈**＝你交代一個目標，它自己一直做到覺得可以為止。中間你看不到，只看到結果。像洗碗：拿起來、洗、看乾不乾淨，不乾淨再洗一次。**路只有一條，轉幾圈它自己決定。**

**圖**＝先把工作拆成幾個**格子**，用線畫出誰接誰。像餐廳出菜：切、炒、擺盤，順序先寫好，而且兩個爐可以同時開。

最好記的一句：

> **格子裡面，是 agent 自己繞圈；格子跟格子之間，是你安排的順序。**

![一張「圖」裡面有什麼](../resources/diagrams/inside-a-graph.png)

所以兩者不是二選一——**圖是把好幾個迴圈裝進格子、再排好順序**。而且格子裡放的不一定是 agent：**也可以是一個工具、一段檢查、或是「這裡要人按核准才能往下」**。

**為什麼要多這一層**：格子畫出來，你才看得到它現在卡在哪一格、才能從中間接著跑、才能兩格同時跑。反過來說，**全部塞回同一個格子，就退回原本的迴圈了**。

**代價要講清楚**：圖逼你事先想清楚要拆成哪幾格。如果事情就是「一直試到成功」、也沒人要回頭查，那先畫圖只是多做工——那種時候迴圈才是對的工具。**你越信得過它，格子畫得越少。**

**譜系**：ReAct（2022）→ AutoGPT（2023）→ Claude Code 的 `/goal`（2026，給一個可驗證的完成條件、讓 agent 自己 loop 到達成）。[Stage 5.6 Dynamic Workflows](05-claude-code-ecosystem.md) 則是 agent 自己寫出 loop 腳本；可以直接跑的圖範例在 [`examples/stage-4/03-graph-workflow/`](../examples/stage-4/03-graph-workflow/README.md)。

**本 stage 三個核心問題**：

1. **Multi-agent 協作** — debate / planner-executor / peer review / handoff / supervisor-worker pattern
2. **Harness Engineering** — agent loop / tool registry（agent 可呼叫工具的清單 + 介面定義）/ context manager / safety / retry / telemetry / eval / cost（8 個核心元件、下面詳述）
3. **Production 化** — eval harness / observability / cost & latency 優化 / 部署到可用環境

**跟 Stage 5 的分工**（避免混淆）：

| 跟誰比 | 那邊講什麼 | 本 stage 講什麼 |
|---|---|---|
| **Stage 5.5 Subagents** | Claude Code 原生 subagent 機制（markdown-based、不寫程式）| 通用 multi-agent framework（autogen / crewAI / langgraph、跨 vendor）|
| **Stage 5.7 Claude Code source** | Claude Code source 解剖（參考實作 case study）| Harness engineering 通則（不綁特定 vendor）|

### ⚠ 但你真的需要 multi-agent 嗎？

**Multi-agent 不是 default、是任務真的需要時才上的設計**。多數場景應先嘗試 simple workflow 或 single agent；**只有在任務天然可分解、需要平行探索、單一 context 不夠、或需要明確角色分工時，multi-agent 才值得引入**。硬上會付 **3-10× token、debug 困難、context fragmentation（context 被切散在多個 agent、彼此看不到全貌）嚴重**。

> 📌 **決策框架的 canonical 在 Stage 4**：完整的 Anthropic / Cognition 立場對照 + 4 個「該上 multi-agent」訊號 + 每個訊號對應的 pattern，見 [Stage 4 §什麼時候真的需要 multi-agent](04-agent-frameworks.md#什麼時候真的需要-multi-agent不要硬上)（設計階段決策）。本節只做 production 前的最後回頭檢查——**4 個訊號一個都不在？** → single agent + 好 prompt + tool use 就夠、別硬上 multi-agent。**本 stage 的 harness engineering 部分（8 個元件 / eval / observability）即使你最後用 single agent 也都會用到**——所以即使你決定不走 multi-agent、本 stage 仍是必修。

## 📌 學習目標

- 設計 multi-agent orchestration 模式（debate、planner-executor、peer review）
- 為 agent 架一套 evaluation harness
- 加上 observability（tracing、logging、cost tracking）
- 用 Anthropic SDK / OpenAI SDK 部署到可用環境（進階功能：streaming、prompt caching、batching）
- 把 agent deploy 到 production（Docker、serverless、monitoring）

## 🚪 進入條件

你應該已經：

- 完成 Stage 4（用過至少一個 agent framework 跑 multi-agent demo）
- 完成 Stage 5（懂 MCP / Skills / Plugins / Subagents 各自角色，並用 5.7 解剖過 harness 內部）
- 完成 Stage 6（會基本 RAG，能講出 memory pattern 差異）
- 對 Docker / git / CI 基礎熟悉（部署成可用服務會用到）

沒到的話 → 補完前面幾個 stage。本 stage 是「組合所有前面學到的東西 → 跑 production」，缺一塊都會卡。

## 📚 必修閱讀

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — 用 production 的角度再讀一次
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — 90% 成本下降的技巧
3. [**Anthropic — Message Batches API**](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) — 非同步 batch job
4. [**anthropics/courses — Prompt Evaluations**](https://github.com/anthropics/courses) ⭐⭐⭐⭐⭐ ★ 22k+ — Anthropic 官方 5 course umbrella、**module 4「Prompt Evaluations」對應本 stage eval / observability 部分**。Jupyter notebook、教怎麼系統化評估 prompt 跟 agent 行為
5. **任一 eval framework 的文件** — promptfoo 或 LangSmith 或 weave
6. [**ai-boost/awesome-harness-engineering**](https://github.com/ai-boost/awesome-harness-engineering)（★ 3.4k+）— agent harness 的工具 / pattern / eval / memory / MCP / observability 全集合
7. [**ZhangHanDong/harness-engineering-from-cc-to-ai-coding**](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding)（★ 1.5k+）— 從 Claude Code 原始碼學 harness 設計（中文）
8. [**stablyai/orca**](https://github.com/stablyai/orca)（★ 48k+、MIT）— 目前規模最大的「**多 agent 同時跑**」桌面環境：一個 prompt 可以同時發給多個 agent，每個跑在自己的 git worktree 裡，跑完並排比較、挑一個 merge。它把 Codex / Claude Code / OpenCode / Pi 當成可替換的後端，所以真正的看點不是它支援誰，而是**當五個 agent 同時在改同一份 repo，介面要解決哪些問題**：隔離、比較、審查，以及「agent 做完了怎麼通知你」。附 iOS app，可以在手機上盯進度。
9. [**yc-software/qm**](https://github.com/yc-software/qm)（★ 13k+、MIT）— Y Combinator 自己開源的 **quartermaster**，跑在 Slack 與 web 上。跟 orca 的分工不同：orca 處理「一個人開很多 agent」，qm 處理「**一整間公司共用 agent**」。每個員工有自己隔離的 workspace（獨立的 memory、檔案、金鑰視野、權限、排程、sandbox），同時又能在 channel 與 project 裡協作；harness 與模型都可抽換（Pi / OpenCode / Codex / Claude Code 共用同一個核心），所以部署不會綁死單一廠商。想看「**組織層級的 agent 權限與治理**長什麼樣」，這是目前少數能直接打開來讀的實作。
10. [**cft0808/edict**](https://github.com/cft0808/edict)（★ 16k+、MIT）— 中文專案，拿**三省六部制**這個一千三百年前的官制來設計多 agent 分工：分揀 → 中書省規劃 → 門下省審議 → 尚書省派發 → 六部並行執行 → 奏摺回報。收它不是因為典故有趣，而是它把「**誰有權決定、誰負責審、誰只能執行**」寫成了明確的角色與交接流程，正好對照本 stage 的 planner-executor 與 peer review 兩個 pattern。附即時看板，看得到每個 agent 當下在做什麼。屬 OpenClaw 生態，另提供 docker 一行起 demo。
11. **（選讀，這一項還在 developer preview）** [**deepseek-ai/deepseek-harness**](https://github.com/deepseek-ai/deepseek-harness)（★ 188k+、MIT）— DeepSeek 2026-08-13 開源的 agent harness，主張是「**everything is a plugin**」：模型、工具、技能、會話、沙箱、儲存、迴圈、排程、UI 全部由外掛提供。**拿來讀，不是拿來依賴**——官方 README 自己寫著「currently in *developer preview* and is iterating rapidly. **THERE WILL BE COMPATIBILITY-BREAKING CHANGES.**」，版本是 `0.1.0-rc.5`、GitHub 上還沒有任何 release。收它的理由是：這是少數可以直接打開來看「**一個 harness 到底由哪些零件組成**」的完整實作，剛好對照下面那八個核心元件——真的要讀就先看 [`docs/architecture.md`](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md)（[中文版](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.zh.md)），不要一頭栽進整個 monorepo。模型不綁 DeepSeek：[模型設定指南](https://deepseek-harness.github.io/deepseek-harness/guide/providers)寫了 Anthropic / OpenAI / Bedrock / Vertex / Azure 以及自訂的 OpenAI-compatible endpoint。它不在 [`resources/cli-agents-guide.md`](../resources/cli-agents-guide.md) 那張表裡，因為**互動介面是 Web UI**（`npx @deepseek-ai/dsh web`）；隨附的非 web 模式 `dsh --profile headless "job"` 是跑完一次就結束、不是互動式 terminal agent（`--profile tui` 指向的外掛 repo 目前是 404）。

## 🏗 Harness Engineering — production agent runtime 的工程設計 ⭐ 本 stage 核心概念

### 定位：模型外圍的執行與控制層

要把 LLM 變成可用的 agent，最先碰到的是**五層裡的前三層**（完整階梯見上面〈五層工程分工〉）。這三層對應的是不同工程位置，不是單純用「一次 call」或「多次 call」來區分。

> 💡 **Simon Willison 2025**：「coding agent = LLM + harness」、harness = 所有**不是 model 本身**的程式碼。
>
> 💡 **OpenAI 2026 也使用 "Harness Engineering" 這個說法**（見 [OpenAI Harness Engineering article](https://openai.com/index/harness-engineering)、2026-02 發布）。

| 層級 | 工程的對象 | 在哪學 |
|---|---|---|
| **1. Prompt Engineering** | 送進 LLM 的**字串**（system prompt / few-shot / 格式） | [Stage 2](02-prompt-engineering.md) |
| **2. Context Engineering** | 視窗裡裝的**資訊**（RAG / memory / tool defs / history 組裝） | [Stage 6](06-memory-rag.md) |
| **3. Harness Engineering**<br>（**本節**） | 模型**外圍的執行與控制層**（loop / retry / sandbox / observability / 部署） | 本 stage |

**怎麼分辨自己在做哪一層？問**：

1. 我改的是**字串本身**嗎？→ Prompt engineering
2. 我改的是**塞進視窗的資訊**嗎？→ Context engineering
3. 我改的是**呼叫模型的外圍程式**嗎？→ Harness engineering

→ 三層**正交**：1 次 call 的 RAG app 也在做 context engineering（重點是組視窗）；50 次 call 但沒做 retrieval 的 chatbot 仍只在做 prompt engineering。

### Harness 的 8 個核心元件

**Harness Engineering（Agent 執行系統設計）= 把 LLM、tools、memory、state、workflow control、retry、safety、eval、observability 與 deployment 串成一套可執行、可觀測、可維護的 agent 系統**。

→ 所有**不屬於 model weights、也不只是 prompt string 本身**的工程元件都算 harness 範圍。一個可部署的 agent runtime 包含這 8 個核心元件（前 6 個是 runtime 內建、第 7 個 eval 是外掛工具、第 8 個 cost / latency 是跨層議題）：

| 元件 | 做什麼 | 對應本 stage 練習 |
|---|---|---|
| **Agent loop**<br>（單次執行內） | 「LLM → tool → result → LLM」迴圈、穩定處理多輪。**這是一次執行裡面的迴圈**，跟上面第 4 層 Loop Engineering 講的「跨 session 長時間執行」不同層次 | 練習 1 multi-agent 辯論 |
| **Tool registry** | 動態 tool dispatch、permission gate、sandboxing | （在每個 framework / SDK 都有）|
| **Context manager** | message history 管理、context window 控制、auto-compact | Stage 6 + 本 stage 練習 4 SDK |
| **Safety layer** | permission prompts、sandboxed exec、destructive op 攔截 | （Claude Code 內建、SDK 可自訂）|
| **Retry / recovery** | tool fail 怎麼處理（exception vs LLM 自己看 error 反思） | 練習 4 SDK 進階 |
| **Telemetry / Observability** | metrics、logging、token counting、trace export | **練習 3 Observability** |
| **Eval harness** | regression test、quality gate、A/B test | **練習 2 Eval** |
| **Cost / Latency optimization** ⭐ 2024-2026 必修 | prompt caching、model routing、thinking budget、batching、semantic cache | **練習 6 Cost optimization**（新加）|

**Framework vs Harness 關鍵差別**：

- **Framework**（[Stage 4](04-agent-frameworks.md)）規範 **API** — 你呼叫的介面長什麼樣
- **Harness**（本節）規範 **runtime** — 怎麼跑、怎麼 recovery、怎麼觀測

### 回饋迴路：agent 進步靠的是回饋，不是更完美的提示

上面 8 個元件是 harness 的「骨架」。但讓骨架真正運作的，是一件更基礎的事：**agent 變強，靠的是「把回饋送回迴圈」，不是把開頭那段提示寫得更完美。**

打個比方：一個學生不會因為作業題目寫得更漂亮就變強，他變強是因為在對的時機收到回饋——交草稿、寫到一半被老師提醒、完成後被批改、下次重做。agent 也一樣，而回饋可以在四個時機進來：

| 時機 | 白話 | 工程上長什麼樣 |
|---|---|---|
| **1. 工具回傳值** | 工具吐回來的那段話，本身就是寫給 agent 看的回饋 | 把錯誤訊息、提示、下一步建議「寫清楚」，別只丟一個 stack trace |
| **2. 執行中插話** | 在 agent 兩次思考之間塞一句話調整方向 | 中途注入訊息（steering），不用等它整輪跑完才修正 |
| **3. 單輪結束的驗收** | 一輪做完，由「另一個人」對著目標檢查 | 用獨立的驗收者（evaluator）比對目標，而不是讓 agent 自己打分 |
| **4. 外層 loop** | 對著同一個目標反覆叫 agent，直到完成 | 目標導向的重跑（像 OpenAI Codex 的 `/goal`、或 cron 定時重跑）|

**為什麼第 3 個（獨立驗收）特別重要**：Anthropic 自己的實驗發現，叫 agent 檢查自己的成品，它幾乎都會「自我稱讚」——就算品質明顯普通。所以他們把「做東西的 agent」和「驗收的 agent」拆開：一個負責做，一個用工具（像 Playwright）實際去點、去測，再把 bug 回報回去。把外部驗收者「調得更挑剔」，比讓同一個 agent「對自己更嚴格」容易得多。

> 📚 實際案例：Anthropic [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)（2026-03）用 planner → generator → evaluator 三段，讓 agent 連續跑好幾小時做出一個完整的音樂製作 app，每輪都靠 evaluator 回饋修正。

### 參考實作

想看實際在 production 跑的 harness 長什麼樣？兩個 reference：

- **Claude Code 整個 runtime** — 是 reference harness 實作。**讀 source 練習見 [Stage 5.7](05-claude-code-ecosystem.md#57--claude-code-source-解剖reference-harness-implementation-track-b-必看)**（clone `claude-agent-sdk-python` 解剖 main loop + 上表前 6 個 runtime 元件位置；第 7 個 Eval harness 是外掛、第 8 個 Cost / Latency 是 cross-cutting、見下方深入段）
- **`anthropics/claude-agent-sdk-python`** source — 上面練習用的具體 repo


**可以直接打開來讀的完整 harness**（都是 2026 年開源、量級夠大，適合對照上面 8 個核心元件看）：

| Project | ⭐ | 語言 / License | 它示範哪一塊 |
|---|---|---|---|
| [xai-org/grok-build](https://github.com/xai-org/grok-build) | ★ 25k+ | Rust / Apache-2.0 | SpaceXAI 的 terminal coding agent。同一份 core 同時支援互動 TUI、headless（CI 用）與編輯器嵌入，是「**一個 harness 要服務幾種執行模式**」的完整範例 |
| [NVIDIA/NemoClaw](https://github.com/NVIDIA/NemoClaw) | ★ 22k+ | TypeScript / Apache-2.0 | 把別人的 agent（Hermes、LangChain Deep Agents、OpenClaw）跑在受管執行環境裡的 reference stack。看點是 **harness 與 sandbox 的責任邊界**：它自己不做 agent，只負責 inference 管理與生命週期。**⚠️ 官方自述是 alpha**，issue 與 PR 為 best-effort 回覆 |

→ 本 stage 剩下的 6 個練習（multi-agent / eval / observability / SDK / deploy / cost）每個都是 harness 的一個面向。學完整 stage = 拼出完整的 harness engineering mental model。

### 第 8 個核心元件深入 — Cost / Latency Optimization（2024-2026 Production 化必修）

Production agent 跑久了、**cost / latency 兩條線會吃掉你大半預算與使用者體驗**。2024-2026 前沿模型都把這當 first-class API feature——**會用 = 省 50-90% cost / latency**。

| 技巧 | 怎麼省 | 2026 狀態 |
|---|---|---|
| **Prompt caching** | 重複 prefix（system prompt、long context）一次計費、後續 cache hit 折扣 ~90% | Anthropic / OpenAI / Gemini 全支援、自動或手動標記 |
| **Model routing / cascade** | 簡單 query → 小 model、難 query → 前沿模型 | [RouteLLM](https://github.com/lm-sys/RouteLLM) / [OpenRouter](https://openrouter.ai/) production 內建 |
| **Thinking budget** | reasoning model 可控 thinking token 上限、trade latency / quality | Claude / Gemini API 參數、o-series 預設高 |
| **Speculative decoding** | 小 model 預測 N token、大 model 一次驗證、單 model 速度 ×2-3 | vLLM / TGI 內建、推論層自動 |
| **Batching** | 多 query 並行處理、GPU 利用率高 | vLLM、production inference layer |
| **Semantic caching** | 相似 query 共用回答（不只 exact match）| [GPTCache](https://github.com/zilliztech/GPTCache) / Helicone 內建 |

**Track A 怎麼用**（用 CLI agent 的人）：

- 在 Claude Code / Cursor 設定 prompt caching、daily session 省 50-90% cost
- 用 [RouteLLM](https://github.com/lm-sys/RouteLLM) / [OpenRouter](https://openrouter.ai/) 動態切換 model（簡單問用 Haiku / Flash、難問用 Opus / Pro）
- Claude API 用 `thinking_budget` 參數控 reasoning model 的 token 上限

**Track B 怎麼 build**（自己寫 agent 的人）：

- 自架 cascade router、把 query embedding → classifier → model 對應
- 在 agent loop 內監控 token cost、超 budget 自動降級
- 部署到可用環境時整合 semantic cache 層
- [Helicone](https://github.com/Helicone/helicone) / [langfuse](https://github.com/langfuse/langfuse) 等 observability 平台都已內建這幾招、不用自己寫

## 🛠 動手練習（基礎 illustrative 練習）

### 練習 1：Multi-Agent 辯論
兩個 agent 辯論一個題目（例如「該用 Python 還是 Rust 寫 backend」），第三個 agent 當裁判。觀察辯論收斂或分歧的 pattern。

### 練習 2：Eval
替你前面的 agent 寫一份 eval，跑 N 次量成功率。把「我用眼睛看一下」的習慣換掉。

### 練習 3：Observability
把 LangSmith、Helicone、或 weave 接上一個 agent，看完整 trace。理解「沒 observability 的 agent debug = 黑盒」。

### 練習 4：SDK 進階
在同一次呼叫裡用 streaming + prompt caching + tool use。看成本怎麼降下來。

### 練習 5：Deploy
把一個 agent 包進 Docker，deploy 到雲端（任何 provider 都行）。學會把 prototype 變成可以給別人跑的東西。

### 練習 6：Cost Optimization（新加）⭐
量你前面任一個練習 agent 的 token cost、加上 prompt caching、再量一次。觀察 cache hit rate 跟 cost 下降的對應關係。**Bonus**：接 [RouteLLM](https://github.com/lm-sys/RouteLLM) 或 [OpenRouter](https://openrouter.ai/)、做 cascade routing（簡單 query → Haiku / 難 query → Opus），量平均 cost。

## 📊 Agent Benchmark Landscape：怎麼看，不要只看排行榜 + ⚠ Reward-Hacking 警告

挑 model / 打造 agent 之前、你會想看 benchmark 數字——但 **2026-04 UC Berkeley 發現 8 個主流 agent benchmark 全部可被 reward-hack 到 ~100%**。下面是 2026 leaderboard 現況 + 怎麼看不被騙。

### 主流 Agent Benchmark 2026-05 SOTA

| Benchmark | 領域 | 2026-05 SOTA | 領先 Model |
|---|---|---|---|
| [**SWE-bench Verified**](https://www.swebench.com/) | 軟工 / code agent | **88.6%** | Claude Opus 4.8 |
| [**Terminal-Bench**](https://github.com/laude-institute/terminal-bench) | terminal 任務 | 領先 | Claude Opus 4.8 |
| **GAIA** | general assistant | **74.6%** | Claude Sonnet 4.5（Princeton HAL）|
| [**WebArena**](https://github.com/web-arena-x/webarena) | web 導航 | **68.7%** | （領先 model 未公布）|
| [**ClawBench**](https://github.com/TIGER-AI-Lab/ClawBench) | 真實網站上的 browser agent 任務 | **44.6%**（lenient）/**24.6%**（strict） | Claude Opus 4.7（V2 Hermes leaderboard history、2026-08 快照:58/130 通過）；283 個任務、144 個真實網站、Apache-2.0、[論文](https://arxiv.org/abs/2604.08523)；V2 兩階段 rubric 較 V1 嚴格 |
| [**OSWorld**](https://github.com/xlang-ai/OSWorld) | OS-level 桌面控制 | v1 **76.26%**（接近飽和）| OpenAI CUA 38%；[OSWorld 2.0](https://osworld-v2.xlang.ai/)（2026-06、long-horizon）已取代 v1、真實長任務 SOTA 僅 ~20%（Opus 4.8 20.6%），見 Stage 8 |
| [**τ-bench**](https://github.com/sierra-research/tau-bench) | tool use 多輪對話 | （較難 hack）| Anthropic / OpenAI 領先 |
| **RE-bench** | research engineering | （較難 hack、接近人類 baseline）| Frontier model |

> **⚠ 上表是 Opus 4.8 世代的數字**：這些都是當時實測並歸屬到該 model 的結果，故原樣保留。Claude Opus 5（`claude-opus-5`）已於 2026-07-24 發布、Anthropic 官方宣稱有所提升，但那些宣稱目前還沒有第三方獨立複現，因此本表刻意不拿它們來更新。

> **Mythos-class 層級（Claude Fable 5 — 2026-06-09 發布）**：[**Claude Fable 5**](https://www.anthropic.com/news/claude-fable-5-mythos-5)（`claude-fable-5`，Mythos-class、定位在 Opus 之上）是對外開放的最高能力 Claude 層級，與姊妹版 Claude Mythos 5（`claude-mythos-5`，部分安全措施放寬、限定核准客戶）同日發布。曾於 2026-06-12 因美國出口管制指令暫停，[2026-07-01 全球恢復](https://www.anthropic.com/news/redeploying-fable-5)（Mythos 5 僅對核准的美國組織恢復）。上表數字維持原本歸屬的 model；Fable 5 官方 benchmark 數字始終未公布，故未列入。**Fable 5 是最高階的 Claude 層級；Opus-class 旗艦現為 Claude Opus 5（Opus 4.8 仍可使用，官方文件已歸入 legacy）。**

→ 詳細排行 + 即時更新：[Agent Benchmark Leaderboard 2026](https://benchmarkingagents.com/agent-benchmarks/)、[Rapid Claw AI Agent Framework Scorecard 2026](https://rapidclaw.dev/blog/ai-agent-benchmarks-2026)

### ⚠ Berkeley 2026-04 Reward-Hacking 警告

[**UC Berkeley RDI 2026-04-12 報告**](https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/)：用 automated scanning agent 系統性 audit **8 個主流 benchmark**（SWE-bench / WebArena / OSWorld / GAIA / Terminal-Bench / FieldWorkArena / CAR-bench 等）、**每個都能 reward-hack 到接近 100%、agent 一個 task 都不用真正解**。

意思：leaderboard 上「Claude 87.6% / GPT 85.0%」這種數字、可能其中 X% 是 hack 出來的、不是真的解 task。

### 怎麼看 benchmark 不被騙

| 看數字方式 | 推薦 |
|---|---|
| 只看 leaderboard top | ❌ 上面 8 個都被證實可 hack |
| 看 task-level success rate breakdown | ✅ 多數 hack 集中少數 task |
| 跑你自己的 hold-out test set | ✅✅ 最可靠、production agent 必做 |
| 看 trajectory / log 是否真的解 task | ✅ 區分 reward hacking vs genuine solve |
| 看多個 benchmark + 自己 use case | ✅ 不依賴單一指標 |

**哪些 benchmark 較難 hack（2026-05）**：

- **τ-bench** — 多輪對話 + tool use、reward function 較密集
- **RE-bench** — research engineering 真實任務
- **你自己的 production eval set** ⭐ 永遠是最可靠的

> 💡 **production agent 的 eval 紀律**：
> - 不要把外部 benchmark 數字當 ground truth、它告訴你「上限」不是「真實表現」
> - 你自己的 eval set（內部 hold-out test）才是上線決策的依據
> - 每次 model upgrade → 跑內部 eval set 驗證、不只看廠商公布的 benchmark 提升
> - 接 [langfuse](https://github.com/langfuse/langfuse) / [promptfoo](https://github.com/promptfoo/promptfoo) 把 eval 自動化、每次 deploy 都跑

> 📊 **observability 認一個可攜標準 + 兩個評估觀念**：(1) **OpenTelemetry GenAI 慣例**（`gen_ai.*` semantic conventions）——langfuse / Arize Phoenix / Helicone 都吐 OTel-相容 span，認這層才不被單一工具綁死；OTel-native 的 [Arize Phoenix](https://github.com/Arize-ai/phoenix)（★ 11k+）可看。(2) **pass^k**（同一題連對 k 次的機率 = 可靠度，不是只看過一次）+ [τ²-bench](https://github.com/sierra-research/tau2-bench)。(3) 多 agent 失敗有現成詞彙：**MAST**（[arXiv 2503.13657](https://arxiv.org/abs/2503.13657)、14 種失敗模式分 3 類）。

## 🎯 常用 Multi-Agent / Production 工具推薦（按用途分類）

不知道從哪挑工具？下面是 2025-2026 業界常用搭配——**挑入口看「場景」、想深入點連結看 repo**：

| 場景 | 推薦工具 | 為什麼 |
|---|---|---|
| **第一次寫 multi-agent**（最快上手）| [crewAI](https://github.com/crewAIInc/crewAI) | role-based、幾行 code 跑起來、production pattern 直接 |
| **想要 group debate / brainstorm pattern** | [AutoGen](https://github.com/microsoft/autogen) | GroupChat 自由辯論、Microsoft 出品 |
| **production 要 audit trail / checkpoint / human-in-loop** | [LangGraph](https://github.com/langchain-ai/langgraph) | state machine、控制最完整 |
| **eval 標準化**（CI / regression 必裝）| [promptfoo](https://github.com/promptfoo/promptfoo) ⭐ | YAML config、跨模型比較、★ 24k+ |
| **eval + observability 同平台** | [langfuse](https://github.com/langfuse/langfuse) ⭐ | OSS、tracing + eval + prompt mgmt、★ 32k+ |
| **不改程式、快速 instrumentation** | [Helicone](https://github.com/Helicone/helicone) | proxy 中介、不綁 framework |
| **全 stack 在 LangChain** | [LangSmith](https://www.langchain.com/langsmith)（商業）| LangChain 官方 observability |
| **打造 Claude agent**（programmatic）| [claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) ⭐ | Anthropic 官方 agent SDK、跟 Claude Code 同 runtime |
| **Deploy agent 成 API service** | [BentoML](https://github.com/bentoml/BentoML) | 最完整、Docker + serving |
| **自架開源 LLM**（取代付費 API）| [vLLM](https://github.com/vllm-project/vllm) | 高吞吐量、★ 87k+ |
| **Fine-tune 開源 LLM** | [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | 100+ 模型統一 SFT/DPO/PPO/GRPO、Web UI 零程式碼、中文社群最廣、★ 73k+ |

**建議入手順序**：

1. 第一個 multi-agent：**crewAI**（role-based、最簡單）
2. 加 eval：**promptfoo**（YAML、CI 整合）
3. 加 observability：**langfuse**（OSS、完整）
4. Production 升級：換 **LangGraph**（control 強）+ **BentoML**（deploy）
5. 進階：自架 LLM 接 **vLLM**、fine-tune 用 **LLaMA-Factory**

## 🎯 精選 Projects（範本 / SDK / 工具 collection）

按用途分類、29 個項目一張表搞定。**挑入口看「適合誰」、想深入點連結看 repo**。

| 分類 | Project | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|---|
| **Multi-Agent Orchestration** | [microsoft/autogen](https://github.com/microsoft/autogen) | ⭐⭐⭐⭐⭐ | 想要 GroupChat 自由 debate pattern | Stage 4 介紹過、production 場景再回頭看 multi-agent 辯論 / brainstorming 模式 |
| | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | ⭐⭐⭐⭐⭐ | 想要 role-based 流水線 | 角色式 multi-agent（research → writer → reviewer），最簡單 production pattern |
| | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | ⭐⭐⭐⭐⭐ | 需要 audit trail / checkpoint / human-in-the-loop | state machine 路線、production 控制最強 |
| | [open-multi-agent/open-multi-agent](https://github.com/open-multi-agent/open-multi-agent) | ⭐⭐⭐⭐ | 寫 TypeScript、想在同一個 repo 裡對照「動態規劃」與「固定 pipeline」 | 由 coordinator 在 runtime 把 goal 規劃成 task DAG,再交給 scheduler 執行;`runTeam()` 從 goal 動態規劃、`runTasks()` 跑寫死的 pipeline,兩種寫法可以直接比。上面三個都是 Python 生態,這條補的是 TypeScript 路線。★ 6.8k+、MIT |
| | [AMAP-ML/LongHorizon-Harness](https://github.com/AMAP-ML/LongHorizon-Harness) | ⭐⭐⭐ | 想看「驗證那一格」在真實專案裡長什麼樣 | 把長任務拆成 Manager / Executor / **Auditor** 三個角色，Executor 每輪用新 context，Auditor 獨立檢查後才寫進持久 state——就是上面那張圖裡「檢查對不對」那一格的實作。包在 Claude Code / Codex 外層，不用自己重寫 agent loop。**很新**：2026-08-04 建立、2 位 contributor，還沒有長期維護紀錄。★ 1.1k+、MIT |
| **Eval Frameworks** | [promptfoo](https://github.com/promptfoo/promptfoo) ⭐ | ⭐⭐⭐⭐⭐ | 把 eval 流程標準化、CI 整合 | YAML config、跨模型比較。★ 24k+、MIT |
| | [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | ⭐⭐⭐⭐ | 學術 benchmark 主張（MMLU / HellaSwag / GSM8K）| 學術等級。★ 13k+、MIT |
| | [openai/evals](https://github.com/openai/evals) | ⭐⭐⭐⭐ | OpenAI 專屬 eval / 想回饋上游 | ★ 19k+ |
| **Observability** | [langfuse](https://github.com/langfuse/langfuse) ⭐ | ⭐⭐⭐⭐⭐ | 自架 production observability | OSS LangSmith 替代、traces + sessions + evals + prompt mgmt。★ 32k+、MIT |
| | [LangSmith](https://www.langchain.com/langsmith)（商業）| ⭐⭐⭐⭐ | 全 stack 在 LangChain / LangGraph 上 | LangChain 官方、只有 hosted 版 |
| | [Helicone](https://github.com/Helicone/helicone) | ⭐⭐⭐⭐ | 不想改程式、快速上 instrumentation | proxy 中介、順便拿到 logging + caching。★ 6k+、Apache 2.0 |
| | [weave (W&B)](https://github.com/wandb/weave) | ⭐⭐⭐⭐ | 團隊已在用 W&B 做 ML 實驗追蹤 | W&B tracing + eval、跟 wandb 整合 |
| | [comet-ml/opik](https://github.com/comet-ml/opik) | ⭐⭐⭐⭐ | eval + observability 同一個開源平台 | 追蹤 LLM / agent 做了什麼、追蹤實驗、跑品質檢查（eval）。★ 21k+、Apache 2.0 |
| | [pydantic/logfire](https://github.com/pydantic/logfire) | ⭐⭐⭐⭐ | 用 OpenTelemetry 標準追蹤 agent / LLM 呼叫 | 看清楚並 debug 你的 agent / LLM 呼叫做了什麼；Pydantic 團隊出品、建在 OpenTelemetry 標準上。★ 4.4k+、MIT |
| **Safety / Guardrails** | [NVIDIA-NeMo/Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) | ⭐⭐⭐⭐ | 想在 agent 的輸入 / 輸出加上安全規則 | 包在 LLM app 外的安全規則——讓它不離題、擋 jailbreak、過濾不當輸出。★ 6.6k+、Apache 2.0 |
| **Anthropic SDK 進階** | [anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python) | ⭐⭐⭐⭐⭐ | 直接基於 Claude API 做應用 | 官方 Python SDK：streaming / async / tool use / prompt caching / batches / files |
| | [anthropic-sdk-typescript](https://github.com/anthropics/anthropic-sdk-typescript) | ⭐⭐⭐⭐ | TypeScript / Node / web app | Python SDK 的 TS 版 |
| | [claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) ⭐ | ⭐⭐⭐⭐⭐ | 打造 Claude-based agent 而非只 API | 內建 tool use loop / file access / sandbox / subagent 編排；跟 Claude Code 同 runtime、想看內部運作直接讀 source。★ 7.6k+、MIT |
| | [claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript) | ⭐⭐⭐⭐ | Node / web app 環境 Claude agent | Claude Agent SDK TS 版。★ 1.7k+ |
| | [Anthropic Cookbook（進階）](https://github.com/anthropics/anthropic-cookbook) | ⭐⭐⭐⭐ | 想看官方進階 SDK pattern | 特別是 `prompt_caching.ipynb` / `tool_use/` / `multimodal/` 三個 notebook |
| **Structured Output** | [BoundaryML/baml](https://github.com/BoundaryML/baml) | ⭐⭐⭐⭐ | 想穩定拿到任何模型輸出的可靠 JSON | 一個專用小語言、幫你從 LLM 穩定取得經過檢查的 JSON；支援 Claude / OpenAI / 本機模型、7 種程式語言。★ 8.8k+、Apache 2.0 |
| **Deployment** | [BentoML](https://github.com/bentoml/BentoML) | ⭐⭐⭐⭐ | 把 agent 包成 production API service | Docker + serving framework。★ 8.8k+、Apache 2.0 |
| | [LangServe](https://github.com/langchain-ai/langserve) | ⭐⭐⭐（⚠️ 已封存）| LangChain agent 快速 deploy | 底層 FastAPI；⚠️ **repo 已封存 2026-05**、新部署改用 LangGraph Platform |
| | [vLLM](https://github.com/vllm-project/vllm) | ⭐⭐⭐⭐ | 自架開源 LLM 取代付費 API | 高吞吐量 LLM serving、Llama / Qwen 等。★ 87k+、Apache 2.0 |
| **中文 deploy / fine-tune** | [datawhalechina/self-llm](https://github.com/datawhalechina/self-llm) | ⭐⭐⭐⭐ | 中文團隊要自架開源 LLM | training-to-deployment 完整中文指南、Qwen / Llama / GLM / 多模態。★ 31k+、Apache 2.0 |
| | [hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | ⭐⭐⭐⭐⭐ | 要 fine-tune 開源 LLM（不只 prompt eng）| 100+ 模型統一 SFT/DPO/PPO/GRPO、Web UI 零程式碼、中文社群最廣。★ 73k+、Apache 2.0 |
| **Multi-Agent 案例研究** | [geekan/MetaGPT](https://github.com/geekan/MetaGPT) | ⭐⭐⭐⭐⭐ | 想看角色分工 + artifact 交接 pattern | SOP-based PM / Architect / Engineer multi-agent team、PRD → 設計 → code 一路產出。★ 67k+、MIT |
| | [OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev) | ⭐⭐⭐⭐ | 想看 agent debate / peer-review pattern | 對話式軟體開發、agents 在 design / code / test 互相辯論。★ 33k+、Apache 2.0、有 zh README |
| | [princeton-nlp/SWE-agent](https://github.com/princeton-nlp/SWE-agent) | ⭐⭐⭐⭐ | 理解為什麼 tool 設計 > prompt tuning | Agent-Computer Interface (ACI) 設計思路、Princeton paper-backed、SWE-Bench 領先方法。★ 20k+、MIT |

> 🌳 **Claude 原生 subagent 機制**（不用 framework 也能 multi-agent）見 [Stage 5.5](05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)。本 stage 重 framework / production；Stage 5.5 重 markdown-based subagent 編排。

## ✅ Stage 7 之後的自我檢查

你能不能：

- [ ] 設計一個 multi-agent 系統，協作協定講得清楚
- [ ] 在 CI 跑自動 eval pipeline
- [ ] 把 observability（tracing）接到 production agent
- [ ] 在真實 workload 上量測 prompt caching 前後的成本差異
- [ ] 把 agent deploy 到雲端（任何 provider）

如果都可以 → 先進 [**Stage 7.5 — 進階 Agentic 概念地圖**](07.5-advanced-agentic-concepts.md)（1 週、不寫 code、建立 frontier 概念地圖、定位業界還在討論哪些進階概念），再進 [**Stage 8 — Agent Interfaces**](08-agent-interfaces.md)（**兩 track 共用 hub**）學 agent 怎麼跟非 API 世界互動（Computer Use / Browser Use / Sandbox）。或挑一個[特化分支](../README.md#-學習地圖兩條學習路徑)、或回過頭來貢獻這份 repo。

## 💡 接下來

你已經有基礎能力了。接下來 6-12 個月應該專注在：

1. **挑一個 production 系統** 從 prototype 推到 production
2. **回饋上游**（LangGraph、AutoGen、MCP servers、Anthropic cookbook）
3. **讀論文**——agent 研究進展很快
4. **做出看得到的東西**——開源一個真的工具、不要只停留在寫教學

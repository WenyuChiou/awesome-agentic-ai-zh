# Stage 4 — Agent 框架（Agent Frameworks）

> **繁體中文** | [简体中文](./04-agent-frameworks.zh-Hans.md) | [English](./04-agent-frameworks.en.md)

⏱ **時間估算**：2-3 週（約 10-15 小時）

> 💡 用語不熟（framework / supervisor / worker / handoff⋯）→ 翻 [`resources/glossary.md`](../resources/glossary.md)。

> 📋 **本章組成**：學習目標 → 進入條件 → 必修閱讀 →〔可選 · 概念地圖：multi-agent intro + 進階 tool patterns〕→ 動手練習 → 精選 Projects → 自我檢查
> 🔑 **關鍵名詞**：見 [`resources/glossary.md`](../resources/glossary.md)（framework / agent loop / handoff / supervisor 等收在 2、4）

你已經從零打造過一個 ReAct agent（Stage 3）。現在來看 framework 到底幫你做了什麼。**挑一個深入學**，其他的瀏覽過去就好，知道什麼時候該換。

## 📌 學習目標

完成這個 stage 後你會：

- 比較 5 個主流 agent framework（LangGraph、AutoGen、CrewAI、Smolagents、OpenAI Agents SDK）
- 替任務挑出對的 framework
- 用兩個 framework 各做一次同樣的 agent，親身感受差異
- 看出什麼時候該丟掉 framework、自己寫

## 🚪 進入條件

你應該已經：

- 跑完 Stage 3 的全部 5 個 hello-X projects
- 從零寫過 ReAct（練習 3）
- 對 async Python 上手（framework 大量依賴 async）

## 📚 必修閱讀

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — 什麼時候用 framework、什麼時候直接用 raw API
2. [**LangChain — Conceptual Guide: Agents**](https://python.langchain.com/docs/concepts/agents/) — agent 的抽象概念
3. [**Best Multi-Agent Frameworks 2026 comparison**](https://gurusup.com/blog/best-multi-agent-frameworks-2026) — 當前市場定位
4. **挑一個 framework 的 Quickstart** — 選 LangGraph 或 CrewAI，把官方教學從頭跑到尾

## 🤔 什麼是 multi-agent framework？

### 兩個維度先分清楚（workflow vs agent / single vs multi）

要看懂 multi-agent framework 之前、有一個有用的釐清方式——把 **workflow vs agent** 跟 **single vs multi LLM** 當成兩個正交維度。Anthropic「Building Effective Agents」原文的核心區分是 workflow（固定 code path）vs agent（LLM 自主決定 next step）；我們把它跟 single/multi 疊起來看 4 個象限：

| | **Workflow**<br>（你寫好的 code path） | **Agent**<br>（LLM 動態決定下一步） |
|---|---|---|
| **Single LLM** | 線性 pipeline、無分支判斷 | 一個 LLM + ReAct loop、自己 plan + adapt<br>（**Stage 3 寫的就是這個**） |
| **Multi LLM** | 預設 routing（譬如「銷售問題 → agent A、技術問題 → agent B」） | 2+ agent 互相 handoff、orchestrator 動態分配<br>（**本 stage 主題**） |

**為什麼這個區分有用**：production 場景大多落在「Single LLM」那一行——不管是 Workflow 象限（線性 pipeline）還是 Agent 象限（ReAct loop）——多數任務根本不需要 multi-agent。**真正需要 multi-agent framework 的是右下角象限**——LLM 自主性高 + 多角色協作。但實作上四個象限的邊界有時模糊（LangGraph 的 conditional edge 可以同時看成 workflow routing 跟 agent 動態決策）、不要把這個 matrix 當互斥分類。

→ 本 stage 後續討論都假設你已經知道：**Multi-agent framework 主要幫你處理多個 agent 之間的協調、交接、狀態管理與重複性程式碼，讓你不用從零寫整套協作流程**（右下角象限的 orchestration boilerplate）。

### Single-agent vs multi-agent — 一張對照表先看清楚差異

| 維度 | **Single-agent**（你 Stage 3 寫過了） | **Multi-agent system** |
|---|---|---|
| **架構** | 一個 LLM + ReAct loop + 若干 tools | 2+ LLM、各有角色（researcher / writer / critic ...）、orchestrator 協調 |
| **怎麼決策** | 同一個 LLM 從頭想到尾 | 角色拆分 + handoff、不同 LLM instance 看不同視角 |
| **State 管理** | 線性 message history | shared state / message passing / checkpoint |
| **適合場景** | 邏輯線性、tool < 20-30 個、單一目標 | 任務可分解、需要 perspective diversity、長 workflow、平行化 |
| **Debug 成本** | 低（單一 loop 可以一路 trace） | 高（cross-agent 互動、error propagation 難定位） |
| **Token 成本** | 1x | 通常 **3-10x**（每個 sub-agent 都有自己的 prompt + thinking + tool call）|
| **Latency** | 低 | 高（除非 sub-agent 平行跑） |

### 什麼時候**真的**需要 multi-agent（不要硬上）

**Multi-agent 不是 default、是 last resort**。**Anthropic 跟 Cognition 兩家 frontier lab 在 2024-2025 都明白寫過：90% 用例其實不該用 multi-agent。** 硬上會付三個代價：**3-10× token、debug 痛苦、context fragmentation**——context 被切散在多個 agent、彼此看不到全貌。

| 立場 | 來源 | 核心論點 |
|---|---|---|
| **Anthropic** | [Building Effective Agents (2024)](https://www.anthropic.com/engineering/building-effective-agents)、[How we built our multi-agent research system (2025)](https://www.anthropic.com/engineering/built-multi-agent-research-system) | 多數場景 simple workflow + single agent 就夠；multi-agent 只在「**研究型 / 並行探索**」任務真的有幫助 |
| **Cognition** | [Don't Build Multi-Agents (2025)](https://cognition.ai/blog/dont-build-multi-agents) | multi-agent 的 context fragmentation 嚴重、shared state 維護痛苦；先窮盡 single-agent + long-context 才考慮 |

需要 multi-agent 通常是這 4 個信號之一：

| 信號 | 描述 | 對應 pattern |
|---|---|---|
| **1. 任務天然分解** | 大任務有清楚的子步驟、step-by-step 完成 | Sequential / Planner-Executor |
| **2. Token explosion** | single agent prompt 塞不下所有 tool description / context | Supervisor-Worker（分流給 sub-agent）|
| **3. 角色衝突** | 同一個 LLM 既當 writer 又當 critic 會 self-justify | Debate / Peer review |
| **4. 平行加速** | 3 個 research 子任務同時跑、wall-clock 1/3 | Parallel / Map-Reduce 變種 |

**4 個信號都不在？** → single agent + 好 prompt + tool use 就夠，不必為此付出前面說的那三個代價，而且 multi-agent 也不保證會比較準。

> 💡 **後續閱讀**：到 [Stage 7 但你真的需要 multi-agent 嗎？](07-multi-agent-production.md#-但你真的需要-multi-agent-嗎) 會再帶 production 視角的決策——本節是設計階段的決策、那邊是 deploy 前的最後一次回頭檢查。

### Multi-agent 經典 pattern（按複雜度排序）

> 📝 **跟 Stage 3 經典範式怎麼分**：[Stage 3 的 4 個 paradigm](03-tool-use-and-hello-agent.md#agent-的經典範式thinking-patterns)（CoT / ReAct / Reflection / Planning）是**單一 agent 內部怎麼想**；本節這 5 個 pattern 是**多個 agent 之間怎麼協作**——正交的兩個層。

| Pattern | 複雜度 | 什麼樣 | 經典場景 | 代表 framework / paper |
|---|---|---|---|---|
| **1. Routing / Handoff** | ⭐ | agent 之間 1:1 handoff、無中央 orchestrator | customer support routing、context switch | [OpenAI Swarm](https://github.com/openai/swarm)、[OpenAI Agents SDK](https://github.com/openai/openai-agents-python) |
| **2. Sequential**<br>（Planner → Executor） | ⭐⭐ | planner 規劃多步驟 + executor 執行 | 多步驟自動化、code generation | LangGraph、[ChatDev paper](https://arxiv.org/abs/2307.07924) |
| **3. Parallel**<br>（平行加速） | ⭐⭐⭐ | N 個 agent 同時跑、結果 aggregate | research / map-reduce 任務、wall-clock 1/N | LangGraph parallel branches、CrewAI parallel tasks。**坑點**：async coordination + partial failure + state merge 一致性 |
| **4. Supervisor-Worker**<br>（hub-spoke） | ⭐⭐⭐ | 1 主 + N worker、主分配 + 整合 | 任務拆解、報告整合 | LangGraph、AutoGen GroupChat |
| **5. Debate / Society**<br>（多視角收斂） | ⭐⭐⭐⭐ | 2+ agent 互相 critique 或角色扮演 | research、judgment task、social simulation | AutoGen GroupChat、[CAMEL paper](https://arxiv.org/abs/2303.17760)、[Generative Agents paper](https://arxiv.org/abs/2304.03442) |

### Claude Code subagent — 另一條 orchestration 路線

> **這節跟上面的 5 個 pattern 不同層**：上面 5 個 pattern 是 framework / 自己 code 都能實作的設計選擇；本節介紹的 **Claude Code subagent 是另一個 execution model**（runtime 內建的 orchestration、不寫 framework code）。讀完 5 個 pattern 後、本節讓你知道「multi-agent 還有第二條路」。

Anthropic 自家的 Claude Code 提供另一個 abstraction 層：[subagent](05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能) — 寫一個 `.claude/agents/<name>.md` 檔就是一個 subagent，**不需要 framework**。

跟 framework 路線的根本差異（一句話）：**framework 路線**跨 LLM provider、寫 Python orchestration code、checkpointing / audit trail 完整；**Claude Code subagent** 只在 Claude Code runtime 內、寫 markdown 不寫 code、天生 context 隔離。

> 📌 **完整逐維度對照表（啟動方式 / runtime / context 隔離 / provider lock-in / 學習曲線）的 canonical 在 [Stage 5.5 開頭](05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)**——逐項實作差異到 5.5 再看。

**何時選 subagent 而非 framework**：

- 你已經在用 Claude Code 跑日常工作
- 任務 context 大、會吃光主 session window（讀整個 codebase 之類）
- 多 subagent 平行（research / write / critic）省 wall-clock 時間
- 不需要跨 provider migration

詳細寫法 + 動手練習見 [Stage 5.5](05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)（**建議先完成 Stage 5.1 Claude Code 基礎再回來看 5.5**——subagent 是 Claude Code 生態的進階功能、需要先熟悉基礎用法）。

### Framework 的工作

Framework 把上面這 5 個 pattern 的 orchestration boilerplate（roles、handoff、state、retry、checkpoint、HITL pause）抽出來、讓你只寫角色定義跟任務描述。一句話：**framework 是 multi-agent 的腳手架，不是必需品**——簡單情境你自己寫個 dict 跟 for loop 也行（Stage 7 練習 1 就是這樣）。

### 📚 想系統化深入？

**🇺🇸 學術 paper（影響後續所有 framework 設計）**：

1. [**Anthropic — "Building Effective Agents"**](https://www.anthropic.com/engineering/building-effective-agents) ⭐⭐⭐ — 何時用 workflow 何時用 agent、5 個經典 orchestration pattern。**英文圈 multi-agent 設計入門必讀**
2. [**AutoGen paper (Wu et al. 2023)**](https://arxiv.org/abs/2308.08155) — Microsoft 多 agent 對話框架原 paper
3. [**CAMEL paper (Li et al. 2023)**](https://arxiv.org/abs/2303.17760) — multi-agent role-play 開山之作
4. [**ChatDev paper (Qian et al. 2023)**](https://arxiv.org/abs/2307.07924) — multi-agent software dev、planner-executor canonical
5. [**Generative Agents paper (Park et al. 2023)**](https://arxiv.org/abs/2304.03442) — 25 個 agent 在 The Sims 互動、社會 simulation

**🀄 中文系統教材**：

1. [**hello-agents Ch6「框架開發實踐」+ Ch7「構建你的 Agent 框架」**](https://github.com/datawhalechina/hello-agents) ⭐ — 中文圈完整講 framework 開發 + 從零構建。**注意：Ch4「智能體經典範式構建」是 single-agent paradigm（ReAct / Plan-and-Solve / Reflection），不是 multi-agent**
2. [**李宏毅 — 生成式 AI 導論**](https://speech.ee.ntu.edu.tw/~hylee/genai/2024-spring.php) — 中後段有 AI agent / multi-agent 相關集數

**Framework 官方 multi-agent docs**：

- [**LangGraph — Multi-Agent Systems**](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) — supervisor / swarm / hierarchical 三種架構官方教學
- [**Anthropic Cookbook — `customer_service_agent.ipynb`**](https://github.com/anthropics/claude-cookbooks/tree/main/tool_use) — multi-agent orchestration canonical 範例（routing + handoff）
- [**Microsoft AutoGen — Examples**](https://microsoft.github.io/autogen/) — group-chat / debate / peer review pattern 完整範例

> 💡 **建議框架學習流程**（5 步）：
> 1. **建立 mental model**（30 min）— 讀 Anthropic Building Effective Agents、把 workflow vs agent 跟 single vs multi 兩維度搞清楚
> 2. **跑 1 個 framework quickstart**（2-3 hr）— LangGraph 或 CrewAI 二選一、跑官方多 agent 教學
> 3. **對照 Anthropic Cookbook `customer_service_agent`**（1 hr）— production-style routing + handoff 範例
> 4. *(可選)* **深入學術側**：挑 paper 1-2 篇看（AutoGen / CAMEL / ChatDev / Generative Agents）
> 5. *(Claude 使用者可選)* **寫一個 subagent 對照**：見 [Stage 5.5](05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)、跟 framework 路線比較
>
> **不必把 5 個 paper 全讀完**、挑跟你場景最近的 1-2 個。

## 🛠 進階 tool patterns（framework 替你處理掉的東西）⭐ Track B 必看

Stage 3 教你寫 single tool / multi-tool selection（手寫 `if/elif/else` 路由）。Framework 把這層抽掉，並加了三種更進階的 tool pattern——**這三個 pattern 都需要 framework 抽象層才寫得乾淨，Stage 3 自己手寫會炸開**：

| Pattern | 解決什麼問題 | 代表實作 |
|---|---|---|
| **Dynamic tool selection** | 工具 > 30 個時、`tools=[...]` 塞不下 prompt（context 太大、selection 也變差） | [LlamaIndex tool router](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/) — embedding-based 路由：先 semantic search 找 top-K tool、只把這 K 個塞進 prompt |
| **Tool composition / chaining** | tool A output → tool B input、不要 LLM 中間 narrative（省 token + 省 latency） | LangGraph `state graph` 直接連接 node、CrewAI `sequential tasks`、Pydantic AI 的 type-safe pipeline |
| **Tool-augmented retrieval** | tool 本身是 RAG search → 回結果再 reason | Stage 6 練習 4 RAG pipeline + Stage 3 練習 2 multi-tool 結合（LangGraph 直接把 retriever 包成 tool node） |

**📚 深度資源**：

- [**Anthropic — Tool Use best practices**](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) — 官方 tool design guide
- [**LlamaIndex — Tool Router pattern**](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/) — Dynamic selection canonical reference
- [**LangGraph — Tool Node**](https://langchain-ai.github.io/langgraph/) — composition graph 寫法

> 💡 **Track B 學完本節**：你應該講得出「同一個任務」在 (a) Stage 3 手寫 (b) 本 stage framework 寫 (c) Stage 5.5 Claude subagent 寫 三種路線的差別。這是 Track B 路線「會設計 agent」核心問題。

## 🛠 動手練習

### 練習 1：同一個 agent、兩個 framework
用以下兩個 framework 各做一次同樣的簡單 agent（搜尋 + 摘要）：

- LangGraph
- CrewAI
比較程式碼行數、debug 體驗、以及它們各自把哪些複雜度藏在哪裡。

### 練習 2：多 agent 角色分配
用 CrewAI 做一個 2-3 個 agent、各自有不同角色一起完成同一個任務的 demo。（這種情境 CrewAI 最拿手。）

### 練習 3：圖式 workflow
用 LangGraph 做一個有分支邏輯跟 human-in-the-loop checkpoint 的 workflow。（這種情境 LangGraph 最拿手。）

### 練習 4：CodeAct vs JSON tool
用 Smolagents 做一個會寫 Python 程式碼當作 action 的 agent（CodeAct pattern），跟 練習 1 用的 JSON tool call 路線比較。問同一個問題，看兩種路線怎麼解。

### 練習 5：型別安全 agent
用 Pydantic AI 做一個會回傳結構化輸出的 agent（例如：問問題回 `{ "answer": str, "confidence": float, "sources": [str] }`）。看 Pydantic 的 schema validation 怎麼防止 agent 偷懶或 hallucinate 結構。

## 🎯 精選 Projects

按用途分 5 類、17 個項目一張表搞定。**挑入口看「適合誰」、想深入點連結看 repo / quickstart**。

| 分類 | Project | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|---|
| **Production 級**<br>（複雜 multi-agent / 需要 audit） | [LangGraph](https://github.com/langchain-ai/langgraph) ⭐ **本 stage 推薦 #1** | ⭐⭐⭐⭐⭐ | Production multi-agent + 稽核軌跡 / rollback / replay | 圖式 orchestration + checkpointing + time-travel debug、企業廣泛採用，★ 39k+、MIT、Python+TS。搭 LangSmith 做 observability |
| | [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) | ⭐⭐⭐⭐ | 在 .NET / Java 環境做 agent、Microsoft 技術棧 | C# / Python / Java 三語官方 SDK、kernel + plugin + planner pattern，★ 28k+、MIT。抽象厚、不適合初學者 |
| | [agno-agi/agno](https://github.com/agno-agi/agno) | ⭐⭐⭐⭐ | 要「build + serve + monitor」一條龍但不想全套 LangGraph + LangSmith | multi-modal agent runtime + control plane，★ 41k+、Apache-2.0。Stage 4 學 API、Stage 7 用 runtime |
| | [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | ⭐⭐⭐⭐ | 想用微軟整合 AutoGen + Semantic Kernel 的後繼框架（Python 或 .NET）的團隊 | 微軟開源框架、讓多個 agent 一起協作——合併 AutoGen 與 Semantic Kernel 的後繼者，★ 12k+、MIT、Python + .NET |
| **快速雛形 / 多 agent**<br>（role-based / handoff） | [CrewAI](https://github.com/crewAIInc/crewAI) ⭐ **本 stage 推薦 #2** | ⭐⭐⭐⭐ | 快速雛形「researcher → writer → critic」pipeline | ~20 行寫完 crew、學習曲線最低，★ 55k+、MIT。⚠️ 長 workflow 沒 checkpointing；雛形用 CrewAI、production 用 LangGraph |
| | [Microsoft AutoGen / AG2](https://github.com/microsoft/autogen) | ⭐⭐⭐⭐ | 多 agent 辯論 / 腦力激盪 / peer review pattern | 對話式多 agent、group-chat 強，★ 60k+、CC-BY-4.0（文件 license）。⚠️ AG2 v0.4 重寫成 async-first、舊教學多半還在 v0.2、新教學用 v0.4、留意版本分支 |
| | [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | ⭐⭐⭐⭐⭐ | 已 commit OpenAI 生態 | OpenAI 官方、agent hand-off + 結構化輸出、API 乾淨、MIT。**2026-04 起內建** sandbox（7 個 provider）+ harness 抽象層、production coding agent 首次 architecturally sound（[詳見 Stage 8](08-agent-interfaces.md#openai-agents-sdk-april-2026-更新--why-是-milestone)）|
| | [deepagents (LangChain)](https://github.com/langchain-ai/deepagents) | ⭐⭐⭐⭐ | 想要「開箱即用」的 deep agent 骨架、不想自己拼 | LangGraph 之上的 opinionated harness（有主見的骨架、替你做好設計選擇）：內建規劃（todo）、檔案系統記憶、子 agent、可載入 skills、context offload（把龐大的中間結果挪出 LLM 視窗）。`pip install deepagents`、MIT、v0.6.12（2026-06）|
| | [OpenAI Swarm](https://github.com/openai/swarm) | ⭐⭐⭐⭐ 教育用<br>⭐⭐⭐ production | 想理解 multi-agent **核心 mental model** 但不想學整套 framework | ~200 LOC、只有 Agent + handoff 兩個觀念、MIT。⚠️ OpenAI 自己標 experimental / educational、不是 production tool。**讀 source 當 chapter-length 教材** |
| | [Strands Agents (AWS)](https://github.com/strands-agents/sdk-python) | ⭐⭐⭐⭐ | 已 commit AWS 雲、Bedrock-native | model-driven 設計（LLM 自己 plan、無 explicit graph）、Apache 2.0。2025 後段推出、AWS Lambda / Step Functions / Bedrock Agents 整合 |
| **特殊路線**<br>（CodeAct / typed / memory-first / filesystem-first） | [Hugging Face Smolagents](https://github.com/huggingface/smolagents) | ⭐⭐⭐⭐ | 本地 LLM 生態、HF 整合場景 | CodeAct pattern 代表（agent 寫 Python 程式碼當 action、非 JSON tool call），★ 28k+、Apache 2.0、≤1000 LOC |
| | [Pydantic AI](https://github.com/pydantic/pydantic-ai) | ⭐⭐⭐ | production 預設要 runtime 型別安全 + structured output | type-safe agent、Pydantic 團隊出品、MIT。較新 |
| | [Letta (formerly MemGPT)](https://github.com/letta-ai/letta) | ⭐⭐⭐⭐ | **長 session / 跨 day / persona-stable** agent（long-term assistant、therapist、tutor）| memory-first multi-agent、OS-paging 概念（working memory + archival store），★ 24k+、Apache 2.0。Stage 6 練習 5 也會提 |
| | [vercel/eve](https://github.com/vercel/eve) | ⭐⭐⭐ | 想在 TS/JS 生態建長駐、可維運的 agent；喜歡「檔案即介面」的專案結構 | Vercel 出品的 filesystem-first framework：agent 的組成都是慣例位置的檔案——`instructions.md`（系統提示）、`tools/`、`skills/`、`channels/`（HTTP / Slack / Discord）、`schedules/`（排程），好檢視、好擴充。`npx eve@latest init` 起手、Apache-2.0、TypeScript，★ 4.5k+。⚠️ 2026-06 才發布、很新 |
| **特化** | [LlamaIndex Agents](https://github.com/run-llama/llama_index) | ⭐⭐⭐ | 文件密集型 agent（研究助理、知識工作者類） | 跟 RAG 緊整合，★ 51k+、MIT。retrieval 強、orchestration 弱——純 orchestration 別選 |
| | [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | ⭐⭐⭐ | 想要視覺化 debug 多 agent 流程的研究者 | 多 agent 平台、視覺化 debug 工具強，★ 28k+、Apache 2.0。西方社群採用低、技術紮實 |
| | [LangChain](https://github.com/langchain-ai/langchain) | ⭐⭐⭐ | 需要黏合很多零件（retrieval + chain）的快速雛形 | 萬用工具袋 framework，★ 143k+、MIT。**agent orchestration 改用 LangGraph**、LangChain 適合 retrieval + chaining 黏合 |
| **基礎設施**<br>（不是 framework、跨 stage 用） | [BerriAI/litellm](https://github.com/BerriAI/litellm) | ⭐⭐⭐⭐ | 要切換 Claude / GPT / Gemini / 開源模型但不想改 code | provider-agnostic SDK + AI gateway、用 OpenAI 形狀 call 100+ LLM、附 cost tracking / fallback / guardrail，★ 54k+、MIT（`enterprise/` 子目錄另授權）|

> 💡 **建議閱讀路徑**：挑 **1 個 production 等級**（LangGraph）+ **1 個快速雛形**（CrewAI）深入學 → 跑練習 1-3 → 其他 framework README 瀏覽過去、知道存在即可。**特殊路線那 4 個**（CodeAct / typed / memory-first / filesystem-first）在特定場景才有對手、平常不必碰。

## ✅ 進 Stage 5 前的自我檢查

你能不能：

- [ ] 用 LangGraph 跟 CrewAI 各做一次同一個 agent
- [ ] 替任務挑出對的 framework（production vs 雛形）
- [ ] 解釋 LangGraph 的 checkpoint 跟 CrewAI 的 task delegation 差在哪
- [ ] 看出什麼時候 CodeAct（Smolagents）比 JSON-tool 更好
- [ ] 判斷什麼時候該丟掉 framework、直接用 raw API

如果可以 → 進 [Stage 5 — Claude Code Ecosystem](05-claude-code-ecosystem.md)。

## 💡 策略提示 + 過程中可能踩到的坑

閱讀路徑見上面【精選 Projects】那則提示（LangGraph + CrewAI 深入、其他瀏覽過去即可），這裡不重複。

**Memory 預備**（學的時候可能碰到、不用先讀）：有些 framework 功能會用到 memory 概念 — LangGraph 的 checkpointing（狀態持久化）、CrewAI agent 之間傳遞任務結果（輕量 memory）。這些在 [Stage 6 — Memory & RAG](06-memory-rag.md) 完整講；本 stage 看不懂某個 framework 功能時、再去那邊查就好，**不用先讀完才能繼續本 stage**。

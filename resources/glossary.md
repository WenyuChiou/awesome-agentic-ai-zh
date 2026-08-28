# 用語小辭典（Glossary）

> **繁體中文** | [简体中文](./glossary.zh-Hans.md) | [English](./glossary.en.md)

> 本路線圖會大量出現「LLM」、「RAG」、「MCP」、「agent」這類詞。讀到不懂的詞先在這裡查 30 秒，再回去讀 stage 內容。
>
> 每個詞**只給最小可用的解釋**（30-80 字 + 在哪一個 stage 講細的）——不是維基百科。

## 🌐 統一詞彙對照表（中英對照、跨 stage 一致）

本表是專案內**強制統一的命名約定**——所有 stage 用同一個中文理解名。如果你在 stage 內看到不一致，請報 issue。

| 英文術語 | 中文理解名 | 主要 stage |
|---|---|---|
| Prompt Engineering | Prompt 設計 | Stage 2 |
| Context Engineering | 上下文管理 | Stage 6 |
| Harness Engineering | Agent 執行系統設計 | Stage 7 |
| Tool Use | 工具使用 | Stage 3 |
| Function Calling | 函式 / 工具呼叫 | Stage 3 |
| Tool Schema | 工具綱要 / 工具說明卡 | Stage 3 |
| Tool Call | 工具請求 | Stage 3 |
| Tool Result | 工具結果 | Stage 3 |
| Structured Output | 結構化輸出 | Stage 3 |
| Agent Loop | Agent 執行迴圈 | Stage 3 |
| Framework | 框架 | Stage 4 |
| Orchestration | 協調與編排 | Stage 4 / 7 |
| Handoff | 任務交接 | Stage 7 |
| Supervisor / Worker | 協調者 / 執行者 | Stage 7 |
| Runtime | 執行層 | Stage 7 |
| Scaffolding | 支撐架構 | Stage 7 |
| Observability | 觀測與紀錄 | Stage 7 |
| Telemetry | 運行紀錄 | Stage 7 |
| Eval | 效果評估 | Stage 7 |
| Evaluation Harness | 評估框架 | Stage 7 |
| Production | 可穩定使用 / 上線化 | Stage 7 |
| Production-grade | 可長期穩定使用的 | Stage 7 |
| Deployment | 部署 | Stage 7 |
| Cost Tracking | 成本追蹤 | Stage 7 |
| Latency | 延遲 / 等待時間 | Stage 7 |
| Vector DB | 向量資料庫 | Stage 6 |
| Retrieval | 檢索 | Stage 6 |
| Reranking | 重排序 | Stage 6 |
| Long Context | 長上下文 | Stage 6 |
| Fine-tuning | 模型微調 | Stage 6 |
| Agent Interfaces | Agent 操作介面 | Stage 8 |
| Code Sandbox | 隔離程式執行環境 | Stage 8 |
| Cold Start | 啟動延遲 | Stage 8 |
| Reward Hacking | 鑽評分漏洞 | Stage 7 / 8 |

→ 詳細定義請看下面各區塊。

---

## 1. 基本概念

### LLM（Large Language Model，大語言模型）

GPT、Claude、Gemini 這類模型會依輸入預測下一個 token。不同模型可以接收文字、圖片或聲音，也可能產生不同媒體。模型不會自行執行你的 client tool；網路、檔案、工具與跨 session 記憶要由外部系統接上。

📍 詳細：[Stage 1](../stages/01-llm-basics.md)

### Model Provider / Provider API（模型供應商／模型 API）

**直接通往模型公司的門。** 例如 Anthropic API、OpenAI API、Gemini API。你選模型、送出 prompt，供應商回傳結果並向你計費。它提供模型服務，但不是會讀寫你電腦檔案的 CLI agent。

### LLM Router / API Router（模型路由器）

**一個入口，替你轉接多家模型或多個後端。** [OpenRouter](https://openrouter.ai/docs/faq) 是例子：同一個 API 與帳務入口可以選不同模型，並依設定處理 provider routing 或 fallback。Router 不是模型，也不是 OpenCode、Pi 這類 coding agent。

📍 五種身分對照：[Track A A1](../tracks/cli/A1-cli-intro.md)

### Token

LLM 看到的不是「字」，是 **token**（次字單位）。中文 1 個字 ≈ 1.5-2 token，英文 1 個 word ≈ 1.3 token。LLM 計費跟 context window 都以 token 計。「100 萬 token context」≈ 75 萬中文字。

📍 詳細：[Stage 1](../stages/01-llm-basics.md)

### Context Window（上下文視窗）

LLM 一次能「看」多少 token。**2026 frontier**：Claude Sonnet 5 / Opus 5 1M、GPT-5.6 1.05M、Gemini 3.5 Flash 1M（Pro 系列上看 2M）、xAI Grok 4.5 500K、Mistral Medium 3.5 256k。**不是越大越好**——超過某個長度後 LLM 會「在中間遺漏」（Lost in the Middle）。

### Prompt（提示詞）

你交給 LLM 的完整任務包。它不一定只有一句問題，可以包含**指令、輸入資料、背景、範例與輸出限制**，也可能分放在多個 message 裡。**Prompt engineering** 是設計並測試這份任務包，讓結果更符合成功條件。`system`、`developer`、`user` 是 API 的 message role（訊息角色），不是 prompt 的固定三段，也不能直接當成「指令」的同義詞。

📍 詳細：[Stage 2](../stages/02-prompt-engineering.md)

### Zero-shot / One-shot / Few-shot

在 prompt 裡放「幾個示範例子」讓 LLM 照著做——這三個詞的差別只在**你給幾個範例**：

- **Zero-shot**（0 個範例）：直接問、不給任何範例。
- **One-shot**（1 個範例）：先給 **1 個** input → output 範例再問。
- **Few-shot**（少數幾個）：先給少量 input → output 範例再問。沒有通用的固定數字；它能展示格式與邊界案例，但是否變好仍要用固定 eval 檢查。

### Chain-of-Thought（CoT，思維鏈）

早期 prompting 技巧會要求 LLM 寫出中間推理，再給答案。常見研究形式有兩種：

- **Few-shot CoT**（原始 paper、[Wei et al. 2022](https://arxiv.org/abs/2201.11903)）：在 prompt 裡放幾個含推理步驟的範例、LLM 模仿著想
- **Zero-shot CoT**（[Kojima et al. 2022](https://arxiv.org/abs/2205.11916)）：在 prompt 結尾加「Let's think step by step」。

現在不要把輸出完整思維鏈當成通用要求。推理模型通常會在內部完成推理；需要核對時，要求**最後答案加一段簡短、可驗證的理由**。哪種寫法較好，必須用同一組 eval 比較。

---

## 2. Agent / 工具使用

### Agent（代理人）

以模型為核心、能在**有界迴圈**中**讀狀態 → 選動作 → 執行 → 觀察結果**，直到完成、失敗或碰到上限的系統。本學習地圖使用三個零件來教入門：

- **LLM**（推理 / 規劃 / decide）
- **Actions**（做事的手段——不限於 function call。可以是寫程式碼執行（CodeAct）、操作瀏覽器（computer use）、查 KB（RAG retrieval）、call MCP server、純規劃分解任務等）
- **Loop**（有最大步數、timeout、費用與停止條件的執行迴圈）

這是本路線圖的 **working definition**，不是唯一學術定義。**ReAct 是其中一種 agent pattern、不是 agent 的定義**；CodeAct、computer-use、planning agent 也可能使用不同的 action 與 loop。

📍 詳細：[Stage 3](../stages/03-tool-use-and-hello-agent.md)

### Tool Use / Function Calling

模型需要查資料或採取動作時，回傳一個有工具名稱、call ID 與參數的結構化請求。對 client tool 而言，**模型只提出請求**；你的程式驗證參數、執行函式，再把對應結果送回模型。

**Tool Use** 是較廣的能力名稱；**Function Calling** 是常見的結構化呼叫機制。供應商的 schema 與訊息格式不同：

- **Anthropic「Tool Use」**：schema 用 `input_schema`（JSON Schema 直接放）
- **OpenAI / Ollama「Function Calling」**：包一層 `{"type": "function", "function": {...}}` 外層
- 寫跨供應商 SDK 時，要分別處理 Tool Call、Tool Result、錯誤旗標與停止原因

📍 詳細：[Stage 3](../stages/03-tool-use-and-hello-agent.md)
📍 schema 怎麼寫好：[Function Schema 設計 cheatsheet](schema-design-cheatsheet.md)

### Tool Schema（工具綱要）

工具的說明卡：名稱、用途、輸入欄位、型別與限制。Schema 能限制請求外形，但不能代替權限、數值範圍與業務規則驗證。供應商的 strict mode 支援也不完全相同。

### Tool Call（工具請求）

模型依 Tool Schema 填好的工作單，通常包含工具名稱、call ID 與參數。它只是**請求**，不是函式已經執行的證明。程式應先比對 allowlist，再解析和驗證參數。

### Tool Result（工具結果）

程式執行工具後回傳的資料，並用 call ID 對回正確的 Tool Call。成功與錯誤都要明確表示；外部工具結果可能含錯誤、惡意內容或 prompt injection，必須視為不可信資料。

### ReAct（Reasoning + Acting）

一種交替 **Reasoning → Action → Observation** 的 agent pattern。本路線圖只要求可觀察的 Tool Call、Tool Result、停止原因和簡短可驗證摘要；不要求模型公開私人 Chain-of-Thought。迴圈必須有步數、時間與費用上限。

📍 詳細：[Stage 3](../stages/03-tool-use-and-hello-agent.md)

### Structured Output（結構化輸出）

要模型輸出 **JSON 或其他固定 schema**，而不是自由文字。它和 Function Calling 都可能使用 schema，但目的不同：Structured Output 要固定形狀的資料；Function Calling 要應用程式採取動作。供應商支援不一，schema 合法也不保證內容正確，程式仍要處理 refusal、截斷、解析與語意錯誤。

### Agent Loop

「模型 → Tool Call → 程式執行 → Tool Result → 模型」這個重複循環。每個結果要對回原 call ID。Loop 必須在完成、拒答、錯誤、最大步數、timeout 或費用上限時停止；不能把 retry 全交給模型。

⚠️ **這是「一次執行裡面」的迴圈**，是 harness 的一個零件，跟五層階梯第 4 層的 [Loop Engineering（迴圈工程）](#loop-engineering迴圈工程)（管的是跨 session 的長時間執行）同名但不同層次。兩者的分界見 [Stage 7](../stages/07-multi-agent-production.md)。

### Self-Refine（基本版反思 / 無記憶）

模型自我評估上一回合輸出、改下一回合的 pattern——「Actor 出答案 → Critic 找問題 → Actor 看 feedback 再答」的 single-session loop。**不一定需要持久記憶層**，是 ReAct 的 sibling pattern，不是 Tool Use 的同義詞。

代表 paper：[Self-Refine (Madaan 2023)](https://arxiv.org/abs/2303.17651)。**完整版 Reflexion**（含 episodic memory）見 3 Memory / Retrieval / RAG（不同層的東西）。

📍 詳細 + 路由：[Stage 3 反思](../stages/03-tool-use-and-hello-agent.md#-反思reflexion--self-refine-概念--路由)

---

## 3. Memory / Retrieval / RAG

### Memory（記憶）— 兩種正交分類軸

「memory」常被混為一談、其實有 **2 種正交分類軸**：

- **時效軸**：short-term（當前對話） vs long-term（跨 session 持久）
- **內容軸**（CoALA framework）：**Working**（暫存）/ **Episodic**（過去經歷）/ **Semantic**（事實知識）/ **Procedural**（怎麼做）

→ 兩軸不互斥：long-term memory 裡可以**同時**有 episodic（user 上次說了什麼）+ semantic（公司知識庫事實）+ procedural（用過的 tool sequence）。

📍 詳細：[Stage 6 Memory 是什麼 + 怎麼設計](../stages/06-memory-rag.md#-memory-是什麼--怎麼設計) + [Stage 6 CoALA framework](../stages/06-memory-rag.md#進階coala-framework--agent-memory-的-4-層-taxonomy)

### RAG（Retrieval-Augmented Generation）

兩階段架構模式：

1. **Ingest**（一次性 / 定期）：document → chunk → embed → 存進 vector store（建可檢索的 KB）
2. **Query**（每次 user 問問題）：question embed → semantic search（或 hybrid + BM25）→ top-K chunks → 塞進 prompt → LLM 答

**解決 LLM 不知道你私有 / 變動 / 過期資料**。Retrieval **不限於 dense embedding**——production 標配是 hybrid（dense + BM25）+ reranker。

📍 詳細：[Stage 6](../stages/06-memory-rag.md)
📍 paper：[Lewis et al. 2020](https://arxiv.org/abs/2005.11401)

### Reflexion（完整版反思 / 帶 episodic memory）

跟 Self-Refine（2 Agent）不同：Reflexion **需要持久 episodic memory store**——agent 跑完 trial 後**寫一段 reflection summary 進 memory**、下一次 trial 開始時 retrieve 進 prompt。**跨 trial 累積教訓**是 Reflexion 的本質（不是 single-session loop）。

放在 3 而非 2 Agent 因為它**本質是 memory pattern**——episodic memory store 是核心、不是 optional。

代表 paper：[Reflexion (Shinn 2023)](https://arxiv.org/abs/2303.11366)。

📍 詳細：[Stage 6 進階：帶持久記憶的 Reflexion 完整版](../stages/06-memory-rag.md#-進階帶持久記憶的-reflexion-完整版--track-b-選讀)

### Embedding（嵌入）

把文字 / 圖片轉成 N 維**向量**、讓「意思接近的東西距離近」。本路線圖預設指 **dense embedding**（稠密向量、sentence-transformers / OpenAI ada-002 等產生）；另有 **sparse embedding**（BM25 / SPLADE 等、用字面 token 比對）——production RAG 兩者並用做 hybrid search。

📍 詳細：[Stage 6](../stages/06-memory-rag.md)

### Vector DB（向量資料庫）

存 + 高效查 embedding 的儲存層。**主要查詢類型 = approximate nearest-neighbor (ANN)**——所以 Vector DB 存在的意義就是「ANN 比直接 cosine 全掃快幾百倍」。代表：Pinecone / Chroma / Qdrant / Weaviate / pgvector。

📍 詳細：[Stage 6](../stages/06-memory-rag.md)

### Semantic Search（語意搜尋）

用 embedding 比較「意思相似」而不是「字串完全相同」。「電動車怎麼充電」可以撈到「EV charging tutorial」。傳統關鍵字搜尋（BM25 等）做不到這個。

### Chunking（切塊）

把長文件切成適合 embedding 的小段（通常 200-1000 token）。**切法直接影響 RAG 品質**——切太碎丟脈絡、切太長相關度模糊。常見策略：固定大小、按段落、按結構（heading）。

### Hybrid Search（混合搜尋）

語意搜尋 + 關鍵字搜尋一起用，再 merge 排序。多半比單一方法準。上線部署 RAG 的標配。

### Reranking（重新排序）

第一輪 retrieval 撈 top-50，再用更貴但更準的模型（cross-encoder）重排成 top-5 給 LLM。Cohere Rerank、bge-reranker 等。

### Contextual Retrieval

Anthropic 2024 提的方法——chunk 加上「整份文件的脈絡摘要」一起 embed，避免「這 chunk 拿出來看不知道是哪份文件講的」問題。

📍 詳細：[Stage 6](../stages/06-memory-rag.md)

### Fine-tuning（模型微調）

拿你自己的資料**再訓練**模型、把知識或行為「燒進」權重裡（跟 RAG 不同——RAG 是 inference 時才把資料塞進 context、不改權重）。適合讓模型穩定學會某種**格式 / 風格 / 領域用語**；**不適合**拿來塞「最新事實」（那是 RAG 的活，fine-tune 進去的事實會過期又難更新）。多數 agent 場景**先試 prompt + RAG**，真的不夠才考慮 fine-tune。

📍 詳細：[Stage 6](../stages/06-memory-rag.md)

---

## 4. Multi-Agent

### Multi-Agent（多 agent）

多個 agent 互相協作完成一個任務。常見 pattern：

- **Supervisor + Worker**：一個 agent 規劃 / 分派、其他執行
- **Swarm（群集）**：平等的 agent 群，沒有固定 supervisor
- **Debate（辯論）**：多個 agent 各持立場、最後 consensus

📍 詳細：[Stage 7](../stages/07-multi-agent-production.md)

### Handoff

一個 agent 把任務交給另一個 agent。比直接 function call 多了「context 怎麼傳」、「失敗誰處理」的問題。

### A2A（Agent-to-Agent）Protocol

Google 發起、現由 Linux Foundation 治理的 agent 之間溝通協定，類似 MCP 但用於 agent ↔ agent（不是 agent ↔ tool）。2026 已達 **v1.0**（已有 150+ 組織採用，並加入身分驗證、讓一個 agent 能確認對方是不是真的它），是 MCP（agent↔tool）的姊妹標準。

---

## 5. Claude Code 生態

### MCP（Model Context Protocol）

Anthropic 2024 推的開放協定、讓任何 LLM host（Claude Code、Cursor、自寫 agent）用同一套介面接外部 tool server，2025-12 已捐給 Linux Foundation 旗下的 Agentic AI Foundation。把它想成「**LLM 的 USB 接口**」。

**技術上標準化 3 種 primitives**：

- **Tools**：LLM 可呼叫的 function（read DB / search web / send email…）
- **Resources**：LLM 可讀取的資料（檔案內容、API response、DB rows…）
- **Prompts**：可複用的 prompt 模板（給 user 在 host 內 `/` 觸發）

**架構**：server / client 模式——tool server 跑在本機或遠端、LLM host 當 client 連接。Server 用兩種 transport 之一暴露 primitives：**stdio**（本機 subprocess）與 **Streamable HTTP**（遠端）；舊的 HTTP+SSE transport 已在 2025-03-26 spec revision 標為 deprecated。

📍 詳細：[Stage 5.2](../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎)

### Project Instructions（專案規則）

CLI agent 每次進入專案時都要讀的共同守則，像貼在工作室牆上的規則。它適合放專案用途、禁止事項、驗證指令與交付格式。不同工具使用不同檔名與載入順序，例如 Codex／OpenCode V2 的 `AGENTS.md`、Claude Code 的 `CLAUDE.md`、Gemini CLI 的 `GEMINI.md`。

📍 入門：[Track A A2](../tracks/cli/A2-cli-workflow.md)

### Skills / SKILL.md

需要時才拿出的可重用「操作卡」。一個 Skill 通常是一個含 `SKILL.md` 的資料夾，還可以附 references、scripts 或其他檔案。Codex、Claude Code、Gemini CLI 與 OpenCode V2 都有 Skill 機制，但搜尋路徑、frontmatter、載入方式與權限不完全相同。

`description` 要清楚說明「什麼情況使用」與「能做什麼」，讓 agent 能選到正確 Skill。第三方 Skill 可能執行程式或呼叫外部工具；安裝前要讀完內容與權限，不把 Skill 當成安全邊界。

📍 入門：[Track A A2](../tracks/cli/A2-cli-workflow.md)；Claude Code 深入：[Stage 5.3](../stages/05-claude-code-ecosystem.md#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層)

### One-off Prompt（單次提示）

只為眼前任務使用的一次性交代，像今天才要用的便條。它放本次任務、範圍、輸入、禁止事項與成功條件；每次都相同的專案規則應移到 project instructions，重複流程應移到 Skill。

📍 練習：[Track A A2 CLI-8](../tracks/cli/A2-cli-workflow.md#cli-8)

### Plugin / Marketplace

把多個 Skills + slash commands + hooks + MCP 設定打包成一個發布單位。**Marketplace** 就是 plugin 的目錄，社群可以 `claude plugin install` 安裝別人寫好的。

📍 詳細：[Stage 5.4](../stages/05-claude-code-ecosystem.md#54--plugins-與-marketplaces)

### Slash Command

Claude Code 內以 `/` 開頭的指令，例如 `/help`、`/compact`、`/plan`。舊專案可能把自訂 prompt 放在 `.claude/commands/<name>.md`；這是相容舊做法。新的可重用流程建議寫成 `.claude/skills/<name>/SKILL.md`。

### CLAUDE.md

放在 project root 的 markdown 檔，Claude Code 每次啟動都會讀。寫 project 級的規則 / 規範 / context（用什麼語言、coding style、別動哪些檔等）。

### Hooks

在 Claude Code 特定事件前後執行的 script。**官方支援 7 種事件類型**：

| Hook | 觸發時機 | 典型用途 |
|---|---|---|
| `PreToolUse` | 工具呼叫**前** | 攔截危險操作（rm -rf、destructive op）、改參數 |
| `PostToolUse` | 工具呼叫**後** | log 記錄、auto-format 寫完的檔 |
| `UserPromptSubmit` | user 訊息送出時 | 加 context（git status / 當前時間）|
| `Notification` | Claude Code 通知時 | 桌面 toast / Slack ping |
| `Stop` | session 結束時 | 自動 commit / 清理 |
| `PreCompact` | 自動 compact 前 | 把重要決定 promote 到 memory |
| `PostCompact` | compact 後 | 確認哪些 context 被壓縮 |

寫法：`.claude/settings.json` 加 `"hooks"` 區塊、指 script 路徑。

### Deep Agent（深度 agent）

「自帶完整配備」的 agent 設計——不只會呼叫工具，還內建規劃（待辦清單）、長期記憶（檔案系統）、子 agent 分工、可載入的 skills。對照：陽春 agent 只有 LLM + 幾個工具。代表實作：LangChain 的 [deepagents](https://github.com/langchain-ai/deepagents)。

---

### Subagent（子 agent）

主 Claude Code session 之外，spawn 出來跑特定任務的 agent。有自己的 context window。例如「給我一個 code-reviewer subagent 看看 diff」。

寫法：在 `.claude/agents/<name>.md` 放 frontmatter + system prompt + tool whitelist。主 session 用 **Agent tool** invoke（自動 parallel / sequential）。**跟 framework-based multi-agent 對照**：subagent 不需要裝 LangGraph / CrewAI 等 framework、直接寫 markdown 即可；但綁 Claude Code runtime。完整教學見 [Stage 5.5](../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)；**15 個複製貼上即用的 dispatch recipe** → [`subagent-cookbook.md`](./subagent-cookbook.md)；**自己寫 / 組合 / debug 進階主題** → [`subagent-advanced.md`](./subagent-advanced.md)。

---

## 6. Production / Eval / Cost

### CI（Continuous Integration，持續整合）

push 或 PR 出現時自動執行固定工作的檢查站。CI 可以跑測試、lint 或只讀 agent review，但它使用的 token、secret、repo 權限與觸發條件都要另外限制。CI 成功不代表可以自動 merge 或跳過人類 review。

📍 練習：[Track A A3 CLI-10](../tracks/cli/A3-cli-production.md#cli-10)

### Eval（評估）

拿一組固定 test case 檢查 prompt 或 agent。最小的 eval 就像一張小答案卡：同一組題目、清楚的正確條件、每次修改後重跑。規模變大後，還能一起記錄準確度、latency 與 cost。常見工具有 promptfoo、LangSmith 與 Langfuse evals。

📍 入門：[Stage 2](../stages/02-prompt-engineering.md)；完整 eval harness：[Stage 7](../stages/07-multi-agent-production.md)

### Observability

把 agent 執行過的步驟、模型、tool、usage、時間與結果留下來，像收據加行車紀錄。出 bug 時可以找出哪一步失敗；拿不到的欄位要寫「未確認」，不能靠猜。常見工具有 Langfuse、Phoenix、Helicone。

📍 入門：[Track A A3 CLI-11](../tracks/cli/A3-cli-production.md#cli-11)；深入：[Stage 7](../stages/07-multi-agent-production.md)

### Prompt Caching

LLM 把 prompt 前綴 cache 起來，下次同前綴只算 cache hit 的便宜價（Anthropic 90% off、OpenAI 50% off）。Long context + 重複 query 的場景可以省很多錢。

### Streaming（串流輸出）

LLM 邊生邊回（一個 token 一個 token），不是等全部生完才丟整段回來。讀者體驗較好（像在打字）；技術上用 SSE 或 chunked transfer。**production 互動式應用幾乎都開**。代價：客戶端要能 handle partial response、ReAct 內 tool call 解析要等到 stream 結束。

### Batch API（批次 API）

把大量 LLM 請求打包送（不要求即時），24 小時內回。**Anthropic / OpenAI 通常打 5 折**。適合非互動場景：批次摘要、批次分類、eval 跑大量 test case、ETL pipeline。**互動式 chat 不能用**——延遲對使用者體驗來說太久。

### Token Cost / Inference Cost

每次 LLM 呼叫的成本 = input tokens × input price + output tokens × output price。Agent 跑 ReAct loop 的成本可以累積很快——大 codebase grep 一次可能花 10 萬 token。

### Guardrails

防 LLM 做壞事的規則層——擋掉 prompt injection、PII 外流、有害輸出等。NeMo Guardrails、Guardrails AI 等。

### Prompt Injection（提示注入）

把惡意指令藏在 LLM 會讀到的內容裡（網頁、文件、工具回傳），誘導它無視原任務、改做攻擊者要的事。根因：LLM 分不清「指令」與「資料裡夾帶的指令」。防法：最小權限、隔離不可信內容、高風險動作人審。相關：lethal trifecta、Guardrails。

### Lethal Trifecta（致命三角）

Simon Willison 提出：agent 同時有（1）存取私密資料、（2）接觸不可信內容、（3）對外通訊三種能力時，就可能被 prompt injection 操控去偷資料外傳。防法是打斷至少一環（常見：切斷對外通訊或隔離不可信輸入）。

---

## 7. 用詞 / Buzzword

### CLI Agent

跑在終端機、能在你允許的範圍內讀檔、改檔與執行命令的 agent / harness（Claude Code、Codex、OpenCode、Pi、Aider、Gemini CLI 等）。**它是工作台，不是裡面的 LLM。** 同一個 CLI 可能綁一個模型生態，也可能讓你切換 provider。

📍 詳細：[Track A A1](../tracks/cli/A1-cli-intro.md)、[`resources/cli-agents-guide.md`](cli-agents-guide.md)

### BYO API Key（Bring Your Own）

工具讓你提供自己的 provider API key，而不是只使用工具內建的訂閱登入。Aider、OpenCode、goose、Pi 等可以接一個或多個 provider；Claude Code、Codex 也各有官方文件列出的訂閱或 API 認證路徑。實際支援方式會改，使用前看該工具的官方認證文件。

### Local LLM / On-Device

模型在自己的機器上執行。Ollama、llama.cpp、MLX、LocalAI 是 **local runtime**：它們負責把模型跑起來，不等於 coding agent。只有模型、工具與資料路徑都留在本機，而且沒有另外呼叫雲端服務時，資料才不會因這次流程送到雲端；能力與速度要用自己的任務和硬體測試。

📍 詳細：[Stage 1](../stages/01-llm-basics.md)

### Quantization（量化）

把模型權重從 fp16 壓到 int8 / int4，省記憶體跟速度，代價是準確度小幅降低。Local LLM 用戶常碰到（Q4_K_M、Q8_0 等）。

### Hallucination（幻覺）

LLM 「自信地說錯」——把不存在的 API 編出來、把錯的數字當成事實寫。所有 production agent 都要防這個（用 RAG / structured output / eval / guardrails）。

### Frontier Model

當下最頂的模型（**2026-07**：Claude **Opus 5**（2026-07-24、`claude-opus-5`、1M、$5/$25，官方 docs 建議的預設起點）、OpenAI **GPT-5.6**（Sol / Terra / Luna 三級、1.05M context、ChatGPT / Codex / API 皆可用）；**2026-06 後半**：Claude Sonnet 5（速度×智慧的最佳平衡、接近 Opus 級但更便宜）、Google Gemini 3.5 Flash、xAI Grok 4.5（500K context）、Mistral Medium 3.5；**2026-06 前半**：Claude Fable 5（Mythos-class，定位在 Opus 之上）發布，2026-06-12 曾被美國出口管制暫停，但 **出口管制 2026-06-30 解除、[Fable 5 於 2026-07-01 全球恢復](https://www.anthropic.com/news/redeploying-fable-5)**（Mythos 5 僅對核准美國組織恢復）；**2026-05**：GPT-5.5、Claude Opus 4.8（當時的 Opus-class 旗艦，2026-07 由 Opus 5 接替、仍可用）、Gemini 3.1 Pro、DeepSeek-V4-Pro 等）。一般智慧任務用 frontier；簡單分類 / 翻譯用便宜的小模型省錢。

### Context Engineering

工程「**每次 LLM call 時、context window 裡裝什麼資訊**」的學科——動態把 RAG retrieve 結果、memory、tool definitions、對話 history 組裝成 LLM 看得到的 context。Karpathy 2025：「填進 window 的資訊**剛好對下一步有用**的精細藝術」。重點是 *what goes in the window*、不是「跨幾次 call」。**Prompt engineering 的下一層**——前者工程**字串**、後者工程**資訊**。

📍 詳細：[Stage 2 結尾](../stages/02-prompt-engineering.md) / [Stage 6](../stages/06-memory-rag.md) / [Stage 7](../stages/07-multi-agent-production.md)
📍 延伸：[`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering)

### Harness Engineering

工程「**模型外圍的執行與控制層**」——所有不是 model weights、也不是 prompt string 本身的工程元件：agent loop / tool registry / context manager / permissions / safety layer / memory layer / eval / observability / retry / circuit breaker 等。Simon Willison 2025：「**coding agent = LLM + harness**」、Addy Osmani：「harness = 所有不是 model 本身的程式碼」。[OpenAI 2026-02 也使用 "Harness Engineering" 這個說法](https://openai.com/index/harness-engineering)。Claude Code、Cursor、OpenCode 等 CLI agent 都是 harness。**framework 把 LLM 包成 agent、harness 把 agent 包成可上線使用的產品**。

對比：

- **Framework**（Stage 4）規範 **API**：你呼叫的介面長什麼樣
- **Harness**（本詞）規範 **runtime**：怎麼跑、怎麼 recovery、怎麼觀測

📍 **學科級概念**（**8 個核心元件** / prompt→context→harness 五層工程分工 / framework vs harness）：[Stage 7 Harness Engineering](../stages/07-multi-agent-production.md#-harness-engineering--production-agent-runtime-的工程設計--本-stage-核心概念)
📍 **Reference implementation case study**（讀 Claude Code source）：[Stage 5 5.7](../stages/05-claude-code-ecosystem.md#57--claude-code-source-解剖reference-harness-implementation-track-b-必看)
📍 延伸：[`anthropics/claude-agent-sdk-python`](https://github.com/anthropics/claude-agent-sdk-python)、[`ai-boost/awesome-harness-engineering`](https://github.com/ai-boost/awesome-harness-engineering)、[`ZhangHanDong/harness-engineering-from-cc-to-ai-coding`](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding)

### Loop Engineering（迴圈工程）

五層工程分工的第 4 層（完整階梯與各層目的見 [Stage 7](../stages/07-multi-agent-production.md)，那裡是 canonical）：設計 / 調校 agent 的「迭代迴圈」本身——目標、工具、context 管理、終止條件、錯誤處理，讓長時間（數百步、跨 session）運行仍可靠、可控、不跑偏。相關：harness、Dynamic Workflows、ReAct。

⚠️ **不要跟 harness 裡那個 [Agent Loop](#agent-loop) 搞混**。這一層管的是**跨越好幾次執行**的長時間問題；`Agent Loop` 是 harness 的一個零件，管的是**一次執行裡面**的機械迴圈。

### Graph Engineering（圖工程）

把 agent 的執行流程設計成**顯式的圖**：node = 一個步驟（2026 起一個 node 裡可以塞一整個 agent run，不再只是一個 function），edge = 轉移條件，node 之間傳遞一個有 schema、可 checkpoint、可 replay 的 state。**讀到這個詞要知道兩件事**：

- **這裡的「圖」是執行流程圖（control / execution graph），不是 GraphRAG 那種知識圖譜檢索**——後者見 [Stage 6](../stages/06-memory-rag.md)。兩者常被混為一談。
- **這是 2026-07 才流行的新名字，不是新技術**。LangGraph 從 2023 就是這樣運作，LangChain 官方也直言這不是新想法；Anthropic 稱同類機制為 *dynamic workflows*、Google ADK 與 Microsoft Agent Framework 用 *graph-based workflow(s)*，三家官方文件都沒有採用「graph engineering」這個說法。

**跟迴圈的關係**：不是二選一。**格子裡面是 agent 自己繞圈，格子跟格子之間才是你安排的順序**——所以圖是把好幾個迴圈裝進格子再排順序；全部塞回同一個格子，就退回單純的迴圈了。格子裡也不一定是 agent，可以是一個工具、一段檢查、或「這裡要人按核准才能往下」。五層階梯的完整說明見 [Stage 7](../stages/07-multi-agent-production.md)（canonical）。

真正要學的東西在 [Stage 4 的 multi-agent pattern](../stages/04-agent-frameworks.md) 跟可以直接跑的 [`examples/stage-4/03-graph-workflow/`](../examples/stage-4/03-graph-workflow/README.md)（`StateGraph` / conditional edge / checkpointer）。相關：harness、Loop Engineering、orchestration。

---

## 8. Agent Interfaces

### Computer Use（螢幕級 agent）

Agent 透過 **screenshot → vision → 算座標 → 模擬鍵鼠** 操作真實桌面 app——不靠 API、直接像人類用螢幕。代表：Anthropic Claude Computer Use（Opus 5 / Sonnet 5）/ OpenAI Codex desktop / Google Gemini in Chrome。**2024-10 Anthropic 公開 beta 開啟；OSWorld v1 2026-05 達 76.26% 後接近飽和，OSWorld 2.0（2026-06、long-horizon）把 SOTA 重設到 ~20%（Opus 4.8）**。

📍 完整解說 + 4 強對比：[Stage 8 Computer Use](../stages/08-agent-interfaces.md#-computer-use--螢幕級-agent)

### Browser Use（web 級 agent）

Agent 操作網頁、主要用 **DOM-aware navigation**（直接 query CSS selector）+ 必要時 vision fallback。代表閉源：Comet / Dia / Gemini in Chrome（Atlas 2026-08 停運）。代表 OSS：[browser-use](https://github.com/browser-use/browser-use)（★ 105k+）。

📍 完整解說 + 5 強對比 + OSS 框架：[Stage 8 Browser Use](../stages/08-agent-interfaces.md#-browser-use--web-級-agent)

### Sandbox（程式碼隔離環境）

讓 agent 寫的 code 在隔離環境跑、不在 host 機器——避免 agent `rm -rf /` / 連 internet 泄資料 / 偷 credentials 等災難。代表：E2B（Firecracker microVM）/ Daytona（Container）/ Modal（GPU sandbox）/ Vercel / Cloudflare。**OpenAI Agents SDK 2026-04 內建支援這些 provider**。

📍 完整 9-row 術語小辭典（含 microVM / Container 差異）+ 7 強對比：[Stage 8 Code Sandbox](../stages/08-agent-interfaces.md#-code-execution-sandbox--隔離環境含術語小辭典)

### microVM（micro Virtual Machine）

VM 的精簡版、極小 footprint、啟動 < 100ms 但仍**獨立 kernel**——介於 Docker container（快 + 弱隔離）跟 full VM（慢 + 強隔離）之間。**Agent sandbox 多半選 microVM**。代表實作：[Firecracker](#firecracker)（AWS、E2B 用）。

📍 完整對比：[Stage 8 術語小辭典](../stages/08-agent-interfaces.md#-隔離技術術語小辭典)

### Firecracker

AWS 開源的 microVM、Rust 寫、**AWS Lambda 底層** + E2B sandbox 用它做 isolation。強隔離 + 快啟動兼顧。

📍 [Stage 8 術語小辭典](../stages/08-agent-interfaces.md#-隔離技術術語小辭典)

### gVisor

Google 寫的「用戶空間 kernel」、攔截 syscall 自己模擬、**不用 hypervisor**——介於 container 跟 VM。

📍 [Stage 8 術語小辭典](../stages/08-agent-interfaces.md#-隔離技術術語小辭典)

---

## 找不到的詞？

- 看 [Stage 5.2 — MCP](../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎) / [5.3 — Skills](../stages/05-claude-code-ecosystem.md#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層) / [5.4 — Plugins](../stages/05-claude-code-ecosystem.md#54--plugins-與-marketplaces) 的內文
- 看 [Stage 1](../stages/01-llm-basics.md) / [Stage 6](../stages/06-memory-rag.md) / [Stage 7](../stages/07-multi-agent-production.md) / [Stage 8](../stages/08-agent-interfaces.md) 的延伸閱讀清單
- 想要更白話的解釋？[baihuaai.com（白话AI）](https://baihuaai.com) 是一個免費、無廣告的简中入門辭典，用大白話搭配現實類比講 AI 術語（有「术语索引」與「零基础专区」）。
- 找不到的詞 → 開 issue 或直接 PR 加進這份小辭典

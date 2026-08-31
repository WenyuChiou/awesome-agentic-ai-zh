# 用語小辭典（Glossary）

> **繁體中文** | [简体中文](./glossary.zh-Hans.md) | [English](./glossary.en.md)

看到陌生英文時，不用停下整章。先在這裡找到一句白話解釋，再回原本的 Stage 繼續做。

## ⚡ 先從 12 個詞開始

- [**Prompt（提示詞）**](#prompt提示詞) — 你交給模型的完整任務包，包含要做什麼、資料、例子與限制。
- [**Token**](#token) — 模型切文字時使用的小單位；計費與可讀長度常用它計算。
- [**Context Window（上下文視窗）**](#context-window上下文視窗) — 模型這一次最多能一起參考的資訊空間。
- [**Agent**](#agent代理人) — 會在限制內選動作、看結果，再決定下一步的系統。
- [**Tool Use（工具使用）**](#tool-use--function-calling) — 模型提出工具請求，程式檢查後才真正執行。
- [**Agent Loop**](#agent-loop) — Agent 重複「決定、行動、觀察」直到完成或停止的執行迴圈。
- [**RAG**](#ragretrieval-augmented-generation) — 先找資料，再把證據交給模型回答。
- [**Memory（記憶）**](#memory記憶-兩種正交分類軸) — 把之後還要用的資訊保存起來，再於需要時讀回。
- [**MCP**](#mcpmodel-context-protocol) — 讓 AI 應用用共同方式連接工具與資料的開放協定。
- [**Eval（評估）**](#eval評估) — 用固定題目和成功條件檢查改動有沒有真的變好。
- [**Agent Harness（執行工作台）**](#agent-harness執行工作台) — 包住模型並管理工具、權限、狀態、記錄與停止規則的系統。
- [**Workflow Graph（工作流程圖）**](#workflow-graph工作流程圖) — 用節點和連線把工作步驟、分支與狀態畫清楚。

## 🧭 先分清五種工具身分

同一個畫面可能同時出現模型、Router 與 Agent。先問「它負責哪一件事」，就不會把產品名稱混在一起。

<table>
<thead>
<tr><th>身分</th><th>白話工作</th><th>例子與邊界</th></tr>
</thead>
<tbody>
<tr><td><strong>Model Provider／API</strong></td><td>模型公司的服務入口。</td><td><a href="https://platform.claude.com/docs/en/api/overview">Anthropic API</a>；它回傳模型結果，不是會改檔的 Agent。</td></tr>
<tr><td><strong>LLM Router</strong></td><td>用一個入口轉接模型或供應商。</td><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a>；它不是模型，也不是 coding agent。</td></tr>
<tr><td><strong>Model Runtime</strong></td><td>把模型在本機或服務上跑起來。</td><td><a href="https://docs.ollama.com/api/introduction">Ollama</a>；它提供模型 API，本身不會自動改專案。</td></tr>
<tr><td><strong>Coding Agent／Harness</strong></td><td>讀檔、改檔、跑命令並回報結果。</td><td><a href="https://opencode.ai/docs">OpenCode</a>、<a href="https://github.com/earendil-works/pi">Pi</a>；裡面的模型可以更換。</td></tr>
<tr><td><strong>Agent Framework</strong></td><td>讓開發者組合 Agent、工具、狀態與流程。</td><td><a href="https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/">Microsoft Agent Framework</a>；它是工具箱，不等於一個模型。</td></tr>
</tbody>
</table>

<details markdown="1">
<summary>維護者：專案固定用詞對照（37 個）</summary>

這張表用來維持跨 Stage 命名一致。一般讀者不用先背。

<table>
<thead>
<tr><th>類型</th><th>英文術語</th><th>中文理解名</th><th>主要 Stage</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="2">輸入與資訊</th><td>Prompt Engineering</td><td>Prompt 設計</td><td>Stage 2</td></tr>
<tr><td>Context Engineering</td><td>上下文管理</td><td>Stage 6／7</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="17">Agent 執行</th><td>Agent Production Engineering</td><td>Agent 可用化工程</td><td>Stage 7</td></tr>
<tr><td>Harness Engineering</td><td>Agent 執行系統設計</td><td>Stage 7</td></tr>
<tr><td>Loop Engineering</td><td>Agent 迴圈設計</td><td>Stage 7</td></tr>
<tr><td>Graph Engineering</td><td>Workflow Graph 工程</td><td>Stage 4／7</td></tr>
<tr><td>Tool Use</td><td>工具使用</td><td>Stage 3</td></tr>
<tr><td>Function Calling</td><td>函式／工具呼叫</td><td>Stage 3</td></tr>
<tr><td>Tool Schema</td><td>工具綱要／工具說明卡</td><td>Stage 3</td></tr>
<tr><td>Tool Call</td><td>工具請求</td><td>Stage 3</td></tr>
<tr><td>Tool Result</td><td>工具結果</td><td>Stage 3</td></tr>
<tr><td>Structured Output</td><td>結構化輸出</td><td>Stage 3</td></tr>
<tr><td>Agent Loop</td><td>Agent 執行迴圈</td><td>Stage 3</td></tr>
<tr><td>Framework</td><td>框架／工具箱</td><td>Stage 4</td></tr>
<tr><td>Orchestration</td><td>協調與編排</td><td>Stage 4／7</td></tr>
<tr><td>Handoff</td><td>任務交接</td><td>Stage 7</td></tr>
<tr><td>Supervisor／Worker</td><td>協調者／執行者</td><td>Stage 7</td></tr>
<tr><td>Runtime</td><td>執行層</td><td>Stage 7</td></tr>
<tr><td>Scaffolding</td><td>支撐架構</td><td>Stage 7</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="9">品質與上線</th><td>Observability</td><td>觀測與紀錄</td><td>Stage 7</td></tr>
<tr><td>Telemetry</td><td>運行紀錄</td><td>Stage 7</td></tr>
<tr><td>Eval</td><td>效果評估</td><td>Stage 7</td></tr>
<tr><td>Evaluation Harness</td><td>評估框架</td><td>Stage 7</td></tr>
<tr><td>Production</td><td>可穩定使用／上線化</td><td>Stage 7</td></tr>
<tr><td>Production-grade</td><td>可長期穩定使用的</td><td>Stage 7</td></tr>
<tr><td>Deployment</td><td>部署</td><td>Stage 7</td></tr>
<tr><td>Cost Tracking</td><td>成本追蹤</td><td>Stage 7</td></tr>
<tr><td>Latency</td><td>延遲／等待時間</td><td>Stage 7</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">檢索與模型</th><td>Vector DB</td><td>向量資料庫</td><td>Stage 6</td></tr>
<tr><td>Retrieval</td><td>檢索</td><td>Stage 6</td></tr>
<tr><td>Reranking</td><td>重排序</td><td>Stage 6</td></tr>
<tr><td>Long Context</td><td>長上下文</td><td>Stage 6</td></tr>
<tr><td>Fine-tuning</td><td>模型微調</td><td>Stage 6</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">操作介面</th><td>Agent Interfaces</td><td>Agent 操作介面</td><td>Stage 8</td></tr>
<tr><td>Code Sandbox</td><td>隔離程式執行環境</td><td>Stage 8</td></tr>
<tr><td>Cold Start</td><td>啟動延遲</td><td>Stage 8</td></tr>
<tr><td>Reward Hacking</td><td>鑽評分漏洞</td><td>Stage 7／8</td></tr>
</tbody>
</table>

</details>

## 📚 依主題查詞

下面不是新的閱讀順序。直接跳到你剛看到的詞即可。

## 1. 基本概念

### LLM（Large Language Model，大語言模型）

**LLM** 是會依照輸入與已學到的模式產生內容的模型。它可以提出工具請求，但真正讀檔、連網或寄信的，是外面的程式。

📍 詳細：[Stage 1](../stages/01-llm-basics.md)

### Model Provider / Provider API（模型供應商／模型 API）

**Model Provider／Provider API** 是模型公司的服務入口。你的程式送出訊息，供應商回傳結果並依方案計費；它不是 coding agent。

### LLM Router / API Router（模型路由器）

**LLM Router／API Router** 像總機：同一個 API 可以依設定轉到不同模型或後端。Router 幫你選路，不會自己變成模型或 Agent。

### Model Runtime（模型執行環境）

**Model Runtime** 是把模型載入並提供推論 API 的執行環境。Ollama、llama.cpp 與 [MLX LM](https://github.com/ml-explore/mlx-lm) 屬於這一類；若要讓它讀檔或跑命令，還要接上 Agent 或應用程式。MLX 本身是 array framework；這裡指的是用 MLX 跑 LLM 的 MLX LM。

### Token

**Token** 是模型切分文字或其他輸入時使用的小單位。每個 tokenizer 的切法不同，所以不要用固定的「一個字等於幾個 token」公式；要估算時使用所選模型的計數工具。

📍 詳細：[Stage 1](../stages/01-llm-basics.md)

### Context Window（上下文視窗）

**Context Window** 是模型這一次能一起參考的 token 空間。空間大不代表每段資料都會被同樣注意；先放任務真正需要的內容，再到 [Stage 1](../stages/01-llm-basics.md) 查目前型號的正式上限。

### Prompt（提示詞）

**Prompt** 是交給模型的完整任務包，不只是一句問題。它可以包含指令、輸入資料、背景、範例、成功條件與輸出格式；**Prompt Engineering** 是設計並用 Eval 測試這份任務包。

📍 詳細：[Stage 2](../stages/02-prompt-engineering.md)

### Zero-shot / One-shot / Few-shot

這三個詞只是在數 Prompt 裡有幾個示範：

- **Zero-shot**：不給示範，直接交代任務。
- **One-shot**：先給一個輸入與答案的例子。
- **Few-shot**：先給少量例子，展示格式或邊界。

例子多不一定更好；用同一組 Eval 比較才知道。

### Chain-of-Thought（CoT，思維鏈）

**Chain-of-Thought（CoT）** 是讓模型經過中間推理步驟再回答的 prompting 研究方法。早期研究包含 [Few-shot CoT](https://arxiv.org/abs/2201.11903) 與 [Zero-shot CoT](https://arxiv.org/abs/2205.11916)。實作時通常要求簡短、可核對的理由與證據，不要求公開模型的私人推理全文。

## 模型訓練與調整

### Pre-training（預訓練）

**Pre-training** 是用大量資料讓模型先學會一般模式。它會改變模型權重，產生之後還能繼續調整的 Base Model。

### Post-training（後訓練）

**Post-training** 是 Base Model 完成後的訓練階段。它用示範、偏好或回饋，讓模型更會照指令、安全地完成任務。

### Inference（推論）

**Inference** 是模型訓練完成後，收到這一次輸入並產生這一次結果。它是在使用模型，不是在重新訓練模型。

### Fine-tuning（模型微調）

**Fine-tuning** 用較小、較專門的資料繼續調整模型權重。它適合反覆出現的行為或格式；每天變動的事實通常改用 RAG 或工具讀取。

### SFT（Supervised Fine-Tuning）

**SFT** 把好輸入與好答案交給模型模仿。它是常見的 Post-training 方法，會調整模型權重。

### DPO（Direct Preference Optimization）

**DPO** 讓模型從「較好答案」與「較差答案」的配對中學習偏好。它需要可信的偏好資料，也會調整權重。

### RLHF / RL

**RLHF／RL** 用人類或規則的回饋來訓練模型。回饋設計錯誤時，模型也可能學會鑽評分漏洞，所以仍要做獨立 Eval。

### GRPO

**GRPO** 讓同一題的多個答案互相比較，再依相對表現更新模型。它是 Post-training 方法之一，不是每個專案都必須使用。

### PEFT / LoRA

**PEFT** 是只訓練較少參數的一組方法；**LoRA** 會凍結原本權重，再訓練新增的低秩矩陣。它們能減少需要更新的參數，但仍需要資料與 Eval。

### Distillation（蒸餾）

**Distillation** 讓較小的 Student Model 學習較大的 Teacher Model。目標常是縮小模型或降低推論成本，但效果要用自己的任務測試。

📍 選修導覽：[模型訓練與調整指南](model-training-guide.md)

## 2. Agent / 工具使用

### Agent（代理人）

**Agent** 是會在限制內讀狀態、選動作、執行並觀察結果的系統。它至少需要模型、可用動作與停止條件；不是只要接上一個 LLM 就會自動做完工作。

### Tool Use / Function Calling

**Tool Use／Function Calling** 是模型提出結構化工具請求的機制。模型只是在說「想呼叫什麼」；你的程式仍要檢查工具名稱、參數與權限後才執行。

📍 詳細：[Stage 3](../stages/03-tool-use-and-hello-agent.md)

### Tool Schema（工具綱要）

**Tool Schema** 是工具說明卡，列出名稱、用途、輸入欄位、型別與必填條件。Schema 可以限制格式，但不能保證模型給的內容安全或真實。

### Tool Call（工具請求）

**Tool Call** 是模型送出的工具名稱與參數。它是不可信輸入；程式要先驗證，再決定執行、拒絕或請人核准。

### Tool Result（工具結果）

**Tool Result** 是程式執行工具後交回模型的結果。成功、失敗與原本的 call ID 要對得上，模型才知道下一步該做什麼。

### ReAct（Reasoning + Acting）

**ReAct** 把可觀察的 Action 與 Observation 交替放進任務流程，讓模型依新結果決定下一步。它源自 [ReAct paper](https://arxiv.org/abs/2210.03629)；實作仍要有最大步數、工具權限與停止條件。

### Structured Output（結構化輸出）

**Structured Output** 要求輸出符合 JSON Schema 或型別。它能讓程式穩定解析格式，但格式正確不等於內容正確，仍要驗證數值、來源與業務規則。

### Agent Loop

**Agent Loop** 是一次執行裡真正重複的流程：模型決定動作，程式執行，模型讀回結果，再決定下一步。迴圈必須能在完成、錯誤、超時、超預算或達到步數上限時停下來。

### Workflow Graph（工作流程圖）

**Workflow Graph** 用 node、edge、branch 與 state 明確排出工作路線。一個 node 可以放 Agent Loop、一般程式、工具或人工核准；它不是每個 Agent 都必須使用的形狀。

📍 詳細：[Stage 4](../stages/04-agent-frameworks.md)

### Self-Refine（基本版反思 / 無記憶）

**Self-Refine** 讓模型先產生答案，再依回饋修一次或多次。原始方法見 [Self-Refine paper](https://arxiv.org/abs/2303.17651)；若沒有外部檢查與停止條件，重寫很多次仍可能一直錯。

## 3. Memory / Retrieval / RAG

### Memory（記憶）— 兩種正交分類軸

**Memory** 是把之後還要用的資訊寫入某個儲存層，再於需要時讀回。可以按保存時間分成短期／長期，也可以按內容分成 episodic、semantic、procedural；這是兩條不同分類軸。

### RAG（Retrieval-Augmented Generation）

**RAG** 是「先檢索證據，再讓模型根據證據回答」。原始方法見 [RAG paper](https://arxiv.org/abs/2005.11401)。它不會自動保證正確；還要測資料品質、檢索命中、引用與回答忠實度。

📍 詳細：[Stage 6](../stages/06-memory-rag.md)

### Reflexion（完整版反思 / 帶 episodic memory）

**Reflexion** 會把先前嘗試、回饋與反思保存為 episodic memory，讓之後的嘗試參考。它比單次 Self-Refine 多了跨嘗試的記憶；原始方法見 [Reflexion paper](https://arxiv.org/abs/2303.11366)。

### Embedding（嵌入）

**Embedding** 把文字、圖片或其他資料轉成向量，讓系統能比較相似度。Dense 與 sparse 表示擅長的訊號不同；要用自己的查詢集測試，而不是只看維度大小。

### Vector DB（向量資料庫）

**Vector DB** 保存向量、metadata 與索引，並找出相近項目。它是檢索層，不是 RAG 的全部；切塊、查詢、Reranking 與回答仍是其他步驟。

### Semantic Search（語意搜尋）

**Semantic Search** 依意思相近程度找資料，不只比對相同字。它適合同義問法，但專有名詞、編號與精確字串常要搭配關鍵字搜尋。

### Chunking（切塊）

**Chunking** 把長文件切成可檢索的小段。切法要跟文件結構與使用問題一起測；不存在適合所有資料的固定大小。

### Hybrid Search（混合搜尋）

**Hybrid Search** 同時使用語意向量與關鍵字訊號，再把結果合併。它常用來兼顧「意思相近」與「名稱必須完全命中」。

### Reranking（重新排序）

**Reranking** 讓第二個模型或規則重新檢查初步候選，把較符合問題的內容排到前面。它可能提升品質，也會增加等待時間與成本。

### Contextual Retrieval

**Contextual Retrieval** 先替每個 chunk 補上它在原文件裡的簡短背景，再建立搜尋索引。Anthropic 的[方法說明](https://www.anthropic.com/engineering/contextual-retrieval)把 contextual embeddings 與 contextual BM25 一起評估；效果仍要用自己的資料測。

## 4. Multi-Agent

### Multi-Agent（多 agent）

**Multi-Agent** 是讓兩個以上 Agent 分工或互相交接。只有當角色、工具、權限或 context 真的需要分開時才值得使用；人數變多不代表答案一定更好。

### Handoff

**Handoff** 是把任務與必要 context 從一個 Agent 交給另一個 Agent。好的交接要說清楚目標、已完成事項、證據、剩餘工作與停止條件。

### A2A（Agent-to-Agent）Protocol

**A2A** 是讓彼此獨立、內部可能不透明的 Agent 發現能力、交換訊息與管理協作任務的開放協定。它處理 Agent 對 Agent 的互通；目前規格與版本看[官方 latest specification](https://a2a-protocol.org/latest/specification/)，不要把版本號寫死在教學裡。

## 5. Claude Code 生態

### MCP（Model Context Protocol）

**MCP** 是 AI 應用連接外部資料與能力的開放協定。Server 可提供 **Prompts**、**Resources** 與 **Tools**；Host／Client 決定如何呈現、授權與傳遞。完整欄位、transport 與安全規則以[現行規格](https://modelcontextprotocol.io/specification)為準。

📍 詳細：[Stage 5.2](../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎)

### Project Instructions（專案規則）

**Project Instructions** 是工具在專案中讀取的共同守則，適合放用途、禁止事項、驗證指令與交付格式。各工具的檔名和載入順序不同，不能假設一份設定在所有 CLI 都完全相同。

📍 入門：[Track A A2](../tracks/cli/A2-cli-workflow.md)

### Skills / SKILL.md

**Skill** 是需要時才載入的操作卡。依 [Agent Skills 規格](https://agentskills.io/specification)，一個 Skill 至少是一個含 `SKILL.md` 的目錄，也能附 scripts、references 與 assets；安裝第三方 Skill 前仍要讀內容與權限。

### One-off Prompt（單次提示）

**One-off Prompt** 是只服務眼前任務的一次性交代。每次都要遵守的規則放 Project Instructions；重複使用的流程才整理成 Skill。

### Plugin / Marketplace

**Plugin** 是把 Skills、commands、hooks 或 MCP 設定等元件包在一起的發布單位；**Marketplace** 是找到與安裝這些套件的目錄。這是產品層功能，不是所有 Agent 的通用必要零件。

### Slash Command

**Slash Command** 是以 `/` 開頭、由應用程式提供的指令。它可能開啟功能、設定或可重用流程；實際名稱和行為要看該工具的目前文件。

### CLAUDE.md

**CLAUDE.md** 是 Claude Code 可讀取的專案指示檔之一，用來告訴 Agent 這個專案怎麼工作。它是給模型遵循的 context，不是能強制阻擋危險操作的安全邊界。

### Hooks

**Hooks** 會在指定事件發生時執行固定檢查或動作。它適合 lint、記錄、通知或攔截高風險操作；事件與設定格式會更新，所以直接看 [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks)，不要背固定數量。

### Deep Agent（深度 agent）

**Deep Agent** 不是跨供應商的單一正式標準。LangChain 的 [deepagents](https://github.com/langchain-ai/deepagents)用這個名稱描述一套含規劃、檔案、子 Agent 與 context 管理的 agent harness；看見這個詞時要先確認作者採用哪個定義。

### Subagent（子 agent）

**Subagent** 是主 Agent 委派出去的隔離工作者，通常有自己的 context，完成後把結果交回。Claude Code 的現行設定、繼承與權限邊界見[官方文件](https://code.claude.com/docs/en/sub-agents)；Subagent 不是自動正確，也要有明確任務與驗證。

📍 教學：[Stage 5.5](../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能) · [可複製 recipes](./subagent-cookbook.md) · [進階組合](./subagent-advanced.md)

## 6. Production / Eval / Cost

### CI（Continuous Integration，持續整合）

**CI** 在 push 或 PR 時自動跑固定檢查，例如測試、lint 與安全掃描。CI 通過只代表已設定的檢查通過，不代表可以跳過 review 或直接部署。

### Eval（評估）

**Eval** 用固定輸入、成功條件與記錄方式比較 Prompt、模型或 Agent。先從少量代表題開始；改動前後跑同一組，才知道品質、成本與延遲怎麼變。

📍 入門：[Stage 2](../stages/02-prompt-engineering.md)；Agent 系統：[Stage 7](../stages/07-multi-agent-production.md)

### Observability

**Observability** 把 Agent 的步驟、工具、狀態、時間、usage 與結果留下可查記錄。它像行車紀錄器；記錄時仍要遮住 secret、私人資料與不必要的 Prompt 內容。

### Prompt Caching

**Prompt Caching** 重用已寫入快取、內容完全相同的 Prompt 前綴，減少重複處理；相似但不同的內容不算命中。最低長度、保存時間與價格依供應商而變，實作前查看[現行快取說明](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)並記錄實際 usage。

### Streaming（串流輸出）

**Streaming** 是模型產生一小段就先傳一小段，不必等完整答案。介面會更快有反應，但客戶端要能處理部分內容、取消、錯誤與尚未完成的 tool call。

### Batch API（批次 API）

**Batch API** 把不急著立刻回覆的多筆請求一起送出。它適合離線分類、摘要或 Eval；完成時間、限制與折扣以當前供應商文件為準。

### Token Cost / Inference Cost

**Token Cost／Inference Cost** 是模型推論花費。最小公式是輸入用量乘輸入單價，加輸出用量乘輸出單價；Agent 還要把每一輪、工具服務與運算成本一起算入。

### Guardrails

**Guardrails** 是限制輸入、輸出與動作的規則層，例如 schema 驗證、allowlist、權限與人工核准。它們能降低風險，但不能代替最小權限、隔離與測試。

### Prompt Injection（提示注入）

**Prompt Injection** 是把惡意指令藏在網頁、文件或工具結果裡，誘導 Agent 偏離原任務。把外部內容視為不可信資料，高風險動作用最小權限與人審。

### Lethal Trifecta（致命三角）

**Lethal Trifecta** 指 Agent 同時能讀私密資料、接觸不可信內容、又能對外通訊時，Prompt Injection 可能把資料帶出去。概念由 [Simon Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)整理；防護重點是切斷至少一條危險路徑。

## 7. 用詞 / Buzzword

### CLI Agent

**CLI Agent** 是在終端機裡讀檔、改檔與執行命令的 Agent／Harness。Claude Code、Codex、OpenCode、Pi、Aider 與 Gemini CLI 都屬這一類；它是工作台，不是裡面的 LLM。

### BYO API Key（Bring Your Own）

**BYO API Key** 表示工具讓你帶自己的模型供應商金鑰。它可能方便切換供應商，但金鑰的計費、權限、保存與撤銷仍由你管理。

### Local LLM / On-Device

**Local LLM／On-Device** 表示模型在你的裝置或自管機器上執行。只有模型、工具、資料與記錄都沒有另傳雲端時，才能說這次流程完全留在本機。

### Quantization（量化）

**Quantization** 用較低精度表示模型權重，通常能減少記憶體與運算需求。速度、大小與品質的變化依模型、格式與硬體而不同，要實測。

### Hallucination（幻覺）

**Hallucination** 是模型產生看似合理但沒有可靠根據的內容。引用、RAG、工具與 Structured Output 都只能幫忙；重要事實仍要查來源或用 Eval 驗證。

### Frontier Model

**Frontier Model** 是某個時間點能力位於前沿的模型類別，不是一個永久名單。型號、價格、Context 與可用狀態變動很快；目前資料統一看 [Stage 1 的官方來源表](../stages/01-llm-basics.md)。

### Context Engineering

**Context Engineering** 是決定每次模型呼叫前「要放進哪些資訊、以什麼順序放、何時刪除或壓縮」的系統工作。它和 Prompt Engineering 互相配合，不是新名詞淘汰舊名詞；可讀 [Anthropic 的實務說明](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)。

### Agent Production Engineering

**Agent Production Engineering** 是本學習地圖對「讓 Agent 可以長期、安全、可觀察地運作」的上位名稱。它把 Harness、Loop、Workflow Graph、Eval、Guardrails、成本、復原與人工核准放在同一章討論。

學習順序是 [Stage 3 的 Agent Loop](../stages/03-tool-use-and-hello-agent.md) → [Stage 4 的 Workflow Graph／Agent Framework](../stages/04-agent-frameworks.md) → [Stage 7 的 Agent Production Engineering](../stages/07-multi-agent-production.md)。Prompt、Context、Harness、Loop、Graph 是五個會重疊的控制問題，不是五個互相取代的產品世代。

📍 完整章節：[Stage 7](../stages/07-multi-agent-production.md)

### Agent Harness（執行工作台）

**Agent Harness** 是包在模型外面的執行系統。它連接工具與 context，管理權限、狀態、記錄、錯誤與停止規則；同一個 Harness 可以包含 Agent Loop，也能成為 Workflow Graph 的一個 node。

### Harness Engineering

**Harness Engineering** 是設計與改進 Agent Harness 的工程工作。OpenAI 的[案例](https://openai.com/index/harness-engineering/)強調環境、知識、測試與回饋迴圈；它不是只把某個 framework 包在外面，也不會被 Loop Engineering 取代。

### Loop Engineering（迴圈工程）

**Loop Engineering** 是設計 Agent 怎麼開始、反覆行動、檢查、保存進度、停止或找人的工程工作。IBM 將它描述為新興實務，包含 goal、action、observation 與 adjustment；看[現行說明](https://www.ibm.com/think/topics/loop-engineering)。

**Agent Loop** 是真的在跑的迴圈；**Loop Engineering** 是把這個迴圈和外圍規則設計好。它可能使用 Harness、Hooks、Skills、Subagents 與 Workflow Graph，而不是取代它們。

### Graph Engineering（圖工程）

**Graph Engineering** 是有人用來描述 Workflow Graph 設計的新興名稱，但不是所有供應商共同採用的標準。穩定的學習物件仍是 node、edge、branch、state 與 checkpoint；研究用法可看[目前的 survey preprint](https://arxiv.org/abs/2608.21156)。

這裡的 graph 是執行流程，不是 Stage 6 的 GraphRAG 知識圖譜。先在 [Stage 4](../stages/04-agent-frameworks.md)學基本 Workflow Graph，再到 [Stage 7](../stages/07-multi-agent-production.md)加入上線邊界。

## 8. Agent Interfaces

### Computer Use（螢幕級 agent）

**Computer Use** 讓模型讀畫面並提出滑鼠或鍵盤動作。Harness 必須先檢查規則，executor 才執行；能用較小、可驗證的 API 或 typed tool 時，通常先用那個。

### Browser Use（web 級 agent）

**Browser Use** 讓 Agent 在網頁裡讀資料、找元素、填表或切換頁面。它可以使用 DOM、Accessibility Tree 與 screenshot；[browser-use](https://github.com/browser-use/browser-use)是開源實作之一。

### Sandbox（程式碼隔離環境）

**Sandbox** 是限制程式能看到和能做什麼的隔離環境。真正的邊界要看檔案、網路、程序、secret、CPU／記憶體與生命週期設定，不能只因為用了容器就宣稱安全。

要比較 Search／Fetch、Browser Use、Computer Use 與 Sandbox，回到 [Stage 8](../stages/08-agent-interfaces.md)。

### microVM（micro Virtual Machine）

**microVM** 是啟動較精簡、仍使用虛擬機隔離邊界的執行環境。它常拿來跑不可信程式，但安全仍依映像、網路、權限與宿主設定而定。

### Firecracker

**Firecracker** 是用 KVM 建立 microVM 的開源 Virtual Machine Monitor。它提供隔離技術，不會自動替你完成映像更新、網路政策或租戶安全；見[官方 repository](https://github.com/firecracker-microvm/firecracker)。

### gVisor

**gVisor** 在應用程式與主機 kernel 之間加入 userspace application kernel，減少容器直接接觸主機系統呼叫的範圍。它不是完整虛擬機，支援與效能取捨看[官方文件](https://gvisor.dev/docs/)。

## 找不到的詞？

- 先回到你正在讀的 Stage；重要詞第一次出現時也應有一句白話定義。
- 看 [Stage 5.2 的 MCP](../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎)、[Stage 5.3 的 Skills](../stages/05-claude-code-ecosystem.md#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層)或 [Stage 7 的 production 邊界](../stages/07-multi-agent-production.md)。
- 找不到時開 issue；請附上「在哪一頁看到」與「哪一句不懂」。

<details markdown="1">
<summary>來源與查核</summary>

上面的易變產品與協定敘述只採官方文件；研究名詞連回原始 paper。完整型號、價格與 Context 清單集中在 Stage 1，不在詞典複製。

<small>官方連結、產品身分與模型生命週期查核：2026-08-31 UTC。</small>

<!-- freshness: canonical=resources/glossary.md; verified_on=2026-08-31; scope=protocols,product-identities,terminology,official-links,model-lifecycle; max_age_days=90 -->

</details>

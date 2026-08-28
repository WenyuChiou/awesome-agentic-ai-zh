# Stage 6 — RAG 與 Memory：先找資料，再記住重要的事

> **繁體中文** | [简体中文](./06-memory-rag.zh-Hans.md) | [English](./06-memory-rag.en.md)

<!-- freshness: canonical=stages/06-memory-rag.md; verified_on=2026-08-28; scope=rag,retrieval,embeddings,vector-stores,memory,evaluation,project-status; max_age_days=90 -->

模型不是什麼都知道。**RAG** 像叫它先翻書再回答；**Memory** 像給它一本筆記本，記住下次還會用到的事。這一關會把兩者分清楚，再帶你一步一步做出來。

<a id="agent-需要的兩種-context-能力"></a>
<a id="-context-engineering-是什麼先定位"></a>
<a id="五層-stack-中的位置"></a>
<a id="本-stage-處理-4-個-sub-problem-中的-2-個lance-martin-2025-framework"></a>
<a id="4-個常被搞混的概念--一張表分清楚"></a>
<a id="rag-vs-long-context-vs-fine-tuning--何時用什麼"></a>
<a id="-進入條件"></a>
<a id="-單元指引漸進式-flow"></a>
<a id="-adaptive--agentic-rag--self-rag--crag--adaptive-rag讓-retrieval-變成可判斷的流程"></a>
## 📌 學習目標

完成這一關後，你可以：

1. 用一句話說出 RAG 與 Memory 的差別。
2. 看懂資料如何變成 **Chunk**、**Embedding**，再被找回來。
3. 做出一條最小 RAG 流水線，並讓回答附上來源。
4. 知道什麼資料值得記住，什麼資料不該保存。
5. 用小型測試比較兩個做法，不靠「感覺比較好」。

## 🧩 先認識七個核心詞

| 核心詞 | 像什麼 | 正確意思 |
|---|---|---|
| **Retrieval（檢索）** | 去書架找幾頁可能有答案的書 | 收到問題後，從外部資料找出相關內容。 |
| **RAG（Retrieval-Augmented Generation）** | 先翻書，再用自己的話回答 | 先 retrieval，再把找到的內容交給模型生成答案。 |
| **Embedding（嵌入向量）** | 幫句子的意思做一張座標卡 | 把文字轉成一串數字，讓意思接近的文字在向量空間裡靠近。 |
| **Vector Store／Vector Database** | 會按「意思」找卡片的抽屜 | 保存 embedding，並用相似度找回相關資料；不同產品的儲存與維運能力不同。 |
| **Chunk（文字片段）** | 把大書切成可拿取的小頁卡 | 為了搜尋與放進 context，把長文件切成較小片段。 |
| **Reranking（重新排序）** | 把第一次找來的卡片再排一次 | 用第二個方法重新評分候選內容，讓更可能有用的片段排前面。 |
| **Memory（記憶）** | 助理自己的筆記本 | 把跨訊息或跨 session 還需要的狀態寫下來，之後再讀回來；它不是聊天紀錄的別名。 |

![RAG 取回外部證據；Memory 寫入並讀回重要狀態](../resources/diagrams/rag-memory-map.png)

### 一張表先選對方法

| 你遇到的問題 | 先考慮 | 為什麼 |
|---|---|---|
| 資料不長，而且這次回答用完就好 | **Long context** | 直接把資料放進這次請求，流程最短。 |
| 文件很多，問題來了才知道要找哪幾段 | **RAG** | 先找相關片段，不必每次塞入全部文件。 |
| 助理下次仍要記得偏好、任務狀態或過往結果 | **Memory** | 把值得保留的資訊寫入可再次讀取的儲存層。 |
| 想穩定改變模型的行為或特定能力 | **Fine-tuning** | 調整模型行為；它不會自動替你提供最新文件。 |

沒有一個選項永遠最好。請用自己的資料、問題與成功條件做評測。

## 🚪 進入條件與閱讀路線

- **第一次學：**先讀七個核心詞，完成練習 1–4，再做短版自我檢查。
- **要做長期助理：**接著完成練習 5，再展開 Memory 設計。
- **要研究或上線：**最後展開進階 RAG、Chunking、評測與研究入口。

<details markdown="1">
<summary>時間、環境、費用與資料安全</summary>

- 建議分兩到三次完成；每次先做一個能跑的練習。
- 需要 Python、Git 與終端機。安裝方式以各練習 README 為準。
- Path A 使用 OpenAI 相容範例；Path B 使用 Anthropic 路徑。模型與 embedding 呼叫可能產生費用。
- 先用小文件測試。不要把密碼、token、醫療資料或未獲授權的公司文件送到外部服務。
- API key 放在環境變數，不要寫進程式或 commit。

</details>

## 📚 必修閱讀

先看「RAG 的零件怎麼接起來」，再開始第一個練習。

<details markdown="1">
<summary>閱讀順序與官方入口</summary>

1. [LangChain Retrieval](https://docs.langchain.com/oss/python/langchain/retrieval) — 看 loader、splitter、embedding、vector store 與 retriever 怎麼合作。
2. [LlamaIndex concepts](https://developers.llamaindex.ai/python/framework/getting_started/concepts/) — 用文件導向的方式理解 indexing 與 querying。
3. [Chroma getting started](https://docs.trychroma.com/getting-started) — 看本地 vector database 的最小使用方式。
4. [LangGraph Agentic RAG](https://docs.langchain.com/oss/python/langgraph/agentic-rag) — 完成基礎 RAG 後，再看 agent 如何決定要不要查資料。

</details>

<a id="-動手練習基礎-illustrative-練習"></a>
## 🛠 動手練習

每題都已經有 starter。直接複製命令執行，不需要先抄一份空白答案。

<a id="練習-1embeddings"></a>
### 練習 1：把兩句話變成 Embedding

**成果：**你會看到意思相近的兩句話，比不相關的句子更靠近。

```powershell
cd examples/stage-6/01-embeddings
python starter.py
python starter_anthropic.py
```

[打開完整說明與檢查方式](../examples/stage-6/01-embeddings/README.md)。先用很少的句子，避免不必要的 API 費用。

<a id="練習-2vector-db"></a>
### 練習 2：把 Embedding 放進 Vector Database

**成果：**你能把文字放進 Chroma，再用一句問題找回相關片段。

```powershell
cd examples/stage-6/02-vector-db
python starter.py
python starter_anthropic.py
```

[打開完整說明與檢查方式](../examples/stage-6/02-vector-db/README.md)。練習資料不得包含秘密或個資。

<a id="練習-3chunking-對照"></a>
### 練習 3：比較三種 Chunking 方法

**成果：**你會看到切得太大、太小或重疊太多，各自會發生什麼事。

```powershell
cd examples/stage-6/03-chunking-comparison
python starter.py
python starter_anthropic.py
```

[打開完整說明與檢查方式](../examples/stage-6/03-chunking-comparison/README.md)。不要先背一個「標準大小」；先看文件結構與測試結果。

<a id="練習-4完整-rag-流水線"></a>
### 練習 4：串起完整 RAG

**成果：**程式會先找資料，再回答，並顯示它使用了哪些來源片段。

```powershell
cd examples/stage-6/04-full-rag-pipeline
python starter.py
python starter_anthropic.py
```

[打開完整說明與檢查方式](../examples/stage-6/04-full-rag-pipeline/README.md)。先用小型資料集；不要把「程式能跑」當成「回答一定正確」。

<a id="練習-5long-term-memory"></a>
### 練習 5：記住一項偏好

**成果：**本練習只會在程式仍執行時新增、搜尋並讀回一項偏好；暫存資料不代表長期持久記憶。

```powershell
cd examples/stage-6/05-long-term-memory
python starter.py
python starter_anthropic.py
```

[打開完整說明與檢查方式](../examples/stage-6/05-long-term-memory/README.md)。只保存完成任務需要的資料，並提供查看、修改與刪除的方法。

### 推薦小專案：會翻資料、也會記偏好的助理

選三到五份你有權使用的小文件。讓助理回答問題時列出來源，再只記住一項無敏感性的偏好，例如「回答先給短版」。成功條件是：找不到證據時會說不知道；重新啟動後仍能讀回偏好；你可以刪掉這項記憶。

<details markdown="1">
<summary>RAG 基礎流水線：資料怎麼進去，答案怎麼出來</summary>

## 🌐 RAG 基礎流水線

RAG 有兩條路：一條先整理資料，一條在問題來時找資料。

| 階段 | 做什麼 | 小孩版比喻 |
|---|---|---|
| Load | 讀入 PDF、網頁或資料庫內容 | 把書搬到桌上 |
| Split | 切成 chunks | 把書分成小卡 |
| Embed | 把每張卡轉成向量 | 幫意思做座標 |
| Store | 保存向量與來源 metadata | 卡片放進有標籤的抽屜 |
| Retrieve | 依問題找候選 chunks | 先拿出可能有答案的卡 |
| Rerank（可選） | 重新排候選內容 | 再檢查哪張卡最有用 |
| Generate | 把問題與證據交給模型 | 看著卡片回答 |
| Cite／Evaluate | 顯示來源並檢查結果 | 告訴別人答案從哪裡來 |

**Retriever** 是「收到問題後，回傳相關文件」的介面。它不一定使用 vector database；BM25、SQL、網站搜尋與混合搜尋也能成為 retriever。

</details>

<details markdown="1">
<summary>進階 RAG 名詞：什麼問題出現時才需要加</summary>

<a id="-rag-進階技巧縱覽--2025-2026-三條主軸"></a>
## 🚀 進階 RAG 技巧（跑完基本 RAG 之後再看）

先建立基線，再一次只加一個元件。否則即使分數變好，你也不知道是哪一步造成的。

### 🔗 GraphRAG — 知識圖譜 + RAG

**GraphRAG** 會先找出 entity（人、地點、產品等）與 relationship，再用圖的連線幫助跨文件或整體主題的查詢。它需要額外 indexing 成本，不是每個小型問答都需要。

- [Microsoft GraphRAG](https://github.com/microsoft/graphrag) — MIT 授權的研究參考實作；官方目前標示為維護模式，適合研究方法與既有部署，不應寫成快速演進的一般產品。
- [GraphRAG paper](https://arxiv.org/abs/2404.16130) — 原始方法與 query-focused summarization。
- [LightRAG](https://github.com/HKUDS/LightRAG) — 另一個活躍的 graph-based RAG 實作；架構、資料模型與 Microsoft GraphRAG 不相同。

<a id="-contextual-retrieval--anthropic-的-prompt-caching-解法"></a>
### 🪶 Contextual Retrieval — 先替 chunk 補上背景

**Contextual Retrieval** 在建立索引時，先替每個 chunk 加上它在整份文件裡的背景，再做 embedding 與 BM25。Anthropic 的實驗中，contextual embedding、contextual BM25 與 reranking 把其測試的 top-20 chunk retrieval failure rate 從 5.7% 降到 1.9%；這是特定資料與設定的結果，不是所有 RAG 的保證。

- [Anthropic Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval)
- [Anthropic cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide)

<a id="-hybrid-search--reranking--production-rag-的兩個常見強化元件"></a>
<a id="-常用-memory--rag-工具推薦按用途分類"></a>
## 🎯 Hybrid Search 與 Reranking

**BM25** 擅長找完全相同或接近的字；vector search 擅長找意思相近的句子。**Hybrid Search** 把兩種候選合在一起；**Reranking** 再看問題與候選片段的配對，把更有用的排前面。

可從 [Qdrant hybrid queries](https://qdrant.tech/documentation/concepts/hybrid-queries/)、[Weaviate hybrid search](https://docs.weaviate.io/weaviate/search/hybrid) 或 PostgreSQL full-text search + [pgvector](https://github.com/pgvector/pgvector) 開始。效果與延遲必須用自己的查詢集測量。

<a id="query-transformations--hyde--multi-query--rag-fusion"></a>
### Query Transformations — HyDE、Multi-Query、RAG Fusion

- **HyDE**：先產生一段假想答案，再用它找資料。適合使用者問題太短，但假想答案也可能帶偏搜尋。
- **Multi-Query**：把同一問題改寫成數個角度，各自搜尋後合併結果。
- **RAG Fusion**：對多個查詢結果做 rank fusion，降低只靠一次查詢措辭的風險。

### 🔁 Self-RAG、CRAG、Adaptive RAG 與 Agentic RAG

- **Self-RAG**：模型學習判斷何時檢索，並對證據與回答做反思。
- **CRAG（Corrective RAG）**：先判斷取回內容是否夠好，不夠時改查詢或改來源。
- **Adaptive RAG**：依問題難度選不同 retrieval 流程。
- **Agentic RAG**：把 retrieval 做成工具，讓 agent 決定何時與如何使用；自由度增加，也增加延遲、成本與除錯難度。

原始入口：[Self-RAG](https://arxiv.org/abs/2310.11511)、[CRAG](https://arxiv.org/abs/2401.15884)、[Adaptive-RAG](https://arxiv.org/abs/2403.14403)、[LangGraph Agentic RAG tutorial](https://docs.langchain.com/oss/python/langgraph/agentic-rag)。

<a id="-raptor--階層式遞迴-retrievaliclr-2024"></a>
### 🌳 RAPTOR — 用摘要樹找不同層次的內容

**RAPTOR** 反覆群聚並摘要文字，形成由細到粗的樹。細節問題可以找葉節點，主題問題可以找較高層摘要。它和用 entity relationship 建圖的 GraphRAG 不同。[RAPTOR paper](https://arxiv.org/abs/2401.18059)。

<a id="-dspy--不寫-prompt用-program-自動-optimizepath-3-paradigm"></a>
### 🧬 DSPy — 用資料與指標調整 LLM program

**DSPy** 把 prompt 與模組組成可最佳化的 program，再用 examples 與 metric 搜尋較好的設定。它不是「不用描述任務」，也不會替你自動修好壞資料。[stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)。

</details>

<details markdown="1">
<summary>Memory 設計：要記什麼、何時寫、何時忘</summary>

<a id="stage-6--上下文管理context-engineeringrag-與-memory"></a>
<a id="先把名詞切開retrieval--rag--vector-store--memory-不是同一件事"></a>
<a id="-5-個可上線使用的-memory-layer按-use-case-挑"></a>
<a id="2024-2026-最新-memory-作品--三條主軸"></a>
## 🌉 從 RAG 到 Memory — 為什麼 RAG 還不夠

RAG 通常從外部知識找資料；Memory 保存 agent 自己之後還需要的狀態。產品手冊適合放知識庫，使用者允許保存的偏好才適合放 memory。不要把整段聊天不加選擇地永久保存。

## 🧠 Memory 是什麼 + 怎麼設計

設計 Memory 時先回答四題：**寫什麼、何時寫、怎麼找、何時改或刪**。

### Working memory vs Long-term memory — 兩種時間尺度

- **Working memory**：目前任務正在使用的短期狀態，例如現在做到哪一步。
- **Long-term memory**：跨 session 還需要的資訊，例如經使用者同意保存的偏好。

### Episodic / Semantic / Procedural memory — 三種內容類型

- **Episodic memory**：發生過什麼，例如上次部署失敗的原因。
- **Semantic memory**：較穩定的事實，例如專案使用 Python 3.13。
- **Procedural memory**：怎麼做，例如發版前的檢查步驟。

### 3 種設計 pattern（什麼時候用什麼）⭐ Track B 必看

1. **直接狀態表**：欄位清楚、容易查看與刪除，先從這裡開始。
2. **可搜尋的文字 memory**：內容較自由，寫入時要保存來源、時間與擁有者。
3. **時間知識圖譜**：關係會變、需要追蹤「何時有效」時才考慮，成本與治理最複雜。

### ⭐ 現行 Memory 專案怎麼選

- [Mem0](https://github.com/mem0ai/mem0)：Apache-2.0，可自架 library／server，也有託管服務；適合練習 add、search、update、delete 的記憶生命週期。
- [Letta Code](https://github.com/letta-ai/letta-code)：Letta 現行開發入口，強調 stateful agent 與 memory；舊 `letta-ai/letta` V1 server 只作歷史參考。
- [Graphiti](https://github.com/getzep/graphiti)：Apache-2.0 的 temporal context graph engine，適合研究會隨時間改變的關係。
- [LangMem](https://github.com/langchain-ai/langmem)：MIT，與 LangGraph store 整合；適合已採用 LangGraph 的專案。
- [Zep](https://github.com/getzep/zep)：現行產品以 Zep Cloud 與 examples／integrations 為主；Community Edition 已 deprecated 並移到 `legacy/`。

### 進階：CoALA framework — agent memory 的 4 層 taxonomy

**CoALA** 把 language agent memory 分成 working、episodic、semantic 與 procedural 等部分，並關注 memory 如何被寫入、讀取與更新。它是分析框架，不是必裝的資料庫。[CoALA paper](https://arxiv.org/abs/2309.02427)。

### 進階：Generative Agents — 三分數打分（經典案例）

Generative Agents 以 recency、importance、relevance 選擇要取回的記憶，再用 reflection 產生較高層摘要。這是研究設計，不代表每個 production system 都使用同一公式。[Generative Agents paper](https://arxiv.org/abs/2304.03442)。

</details>

<details markdown="1">
<summary>Chunking、Reflexion 與評測：怎麼知道真的變好</summary>

## 🧩 Chunking 細節（技術深入）

Chunk 太大時，一張卡會混進太多主題；太小時，答案需要的上下文可能被切散。可先從文件本身的標題與段落切，再用測試調整。

常見方法：

- **Fixed-size**：容易重現，但可能在句子中間切開。
- **Recursive／structure-aware**：先依標題、段落、句子切，通常較符合文件結構。
- **Sentence window**：用小句子搜尋，取回時帶前後文。
- **Parent-child／small-to-big**：小 chunk 負責搜尋，較大的 parent 負責回答。
- **Semantic chunking**：依意思轉折切分，計算較多，也需要更仔細評測。

每筆 chunk 至少保留來源文件、位置或頁碼、版本與存取權限。Overlap 不是越大越好；它會增加索引量與重複內容。

## 🪞 進階：帶持久記憶的 Reflexion 完整版 ⭐ Track B 選讀

**Reflexion** 讓 agent 在嘗試後寫下回饋，下一次再讀取。要成為真正的 persistent memory，回饋必須存到 process 結束後仍存在的儲存層，並且可以查看、修改與刪除。[Reflexion paper](https://arxiv.org/abs/2303.11366)。

### 📚 想動手 / 想深入

- 先替一個失敗案例寫一條短 reflection，再重跑同一題。
- 比較「沒有 reflection」與「有 reflection」是否改善明確成功條件。
- 不要保存模型臆測、秘密或無期限的使用者資料。

<a id="-進階-reasoning--reflection--2024-2026-思潮--兩個-track-都看"></a>
<a id="path-1prompt-based-reflection--reasoning傳統做法"></a>
<a id="path-2trained-in-reasoning--reflection2024-2026-大轉折"></a>
<a id="兩條路怎麼選"></a>
## 🤔 進階 Reasoning / Reflection — 兩條路

- **Prompt-based reflection**：執行後用 prompt 檢查錯誤、產生改進建議；容易試驗，但可能重複同樣錯誤。
- **Trained-in reasoning**：模型在訓練中學到更強的推理行為；使用者仍要檢查答案與證據，不能把隱藏推理當成可靠來源。

## 📏 RAG / Memory Eval — 跑得起來 ≠ 跑得準

至少分開量三件事：

1. **Retrieval**：正確證據有沒有被找回來？
2. **Answer**：回答是否被證據支持、是否真的回答問題？
3. **Memory**：該記的能否讀回、不該記的是否被拒絕或刪除？

建立一小組有人檢查過的問題、答案與來源。記錄每次變更前後的結果；不要只看一個總分。

- [Ragas](https://github.com/vibrantlabsai/ragas) — Apache-2.0 的 LLM application evaluation toolkit；現行 canonical owner 是 Vibrant Labs。
- [TruLens](https://github.com/truera/trulens) — evaluation 與 observability 工具。
- [LangSmith evaluation](https://docs.langchain.com/langsmith/evaluation) — LangChain 的託管 evaluation／tracing 服務。

</details>

<a id="-精選-projects範本--spec--範例-collection"></a>

## 🎯 精選 Projects 與學習資源

先從 **LlamaIndex 或 LangChain + Chroma** 理解最小流水線；已有 PostgreSQL 才優先看 pgvector。不要一次安裝整張表。

<details markdown="1">
<summary>18 個已查核入口、編輯評分與限制</summary>

<small>資料查核：2026-08-28 UTC</small>

<table>
  <thead>
    <tr><th scope="col">分類</th><th scope="col">專案</th><th scope="col">編輯評分</th><th scope="col">適合誰</th><th scope="col">能學什麼</th><th scope="col">狀態／限制</th></tr>
  </thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">RAG framework</th><td><a href="https://github.com/run-llama/llama_index">LlamaIndex</a></td><td>⭐⭐⭐⭐⭐</td><td>文件型應用初學者</td><td>Index、retriever、query engine</td><td>MIT；套件多，先用官方 starter</td></tr>
    <tr><td><a href="https://github.com/infiniflow/ragflow">RAGFlow</a></td><td>⭐⭐⭐⭐⭐</td><td>想看完整 Web 產品的團隊</td><td>文件解析、hybrid retrieval、UI</td><td>Apache-2.0；部署比教學範例重</td></tr>
    <tr><td><a href="https://github.com/HKUDS/LightRAG">LightRAG</a></td><td>⭐⭐⭐⭐</td><td>研究 graph-based RAG 的讀者</td><td>graph + vector retrieval</td><td>MIT；研究導向，不等同 Microsoft GraphRAG</td></tr>
    <tr><td><a href="https://github.com/deepset-ai/haystack">Haystack</a></td><td>⭐⭐⭐⭐</td><td>想比較另一套 pipeline framework</td><td>components、pipelines、evaluation</td><td>Apache-2.0；先選一套 framework 練習</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="5">Vector data</th><td><a href="https://github.com/chroma-core/chroma">Chroma</a></td><td>⭐⭐⭐⭐⭐</td><td>第一次在本機做向量搜尋</td><td>collection、add、query</td><td>Apache-2.0；練習與 production 設定不同</td></tr>
    <tr><td><a href="https://github.com/qdrant/qdrant">Qdrant</a></td><td>⭐⭐⭐⭐⭐</td><td>需要自架或託管服務的團隊</td><td>dense、sparse、hybrid query</td><td>Apache-2.0；需規劃服務與備份</td></tr>
    <tr><td><a href="https://github.com/weaviate/weaviate">Weaviate</a></td><td>⭐⭐⭐⭐</td><td>需要 schema 與 hybrid search</td><td>BM25 + vector search</td><td>BSD-3-Clause；功能多，先做小型基線</td></tr>
    <tr><td><a href="https://github.com/pgvector/pgvector">pgvector</a></td><td>⭐⭐⭐⭐</td><td>已使用 PostgreSQL 的團隊</td><td>SQL 與 vector 同庫</td><td>PostgreSQL extension；仍需索引與查詢調校</td></tr>
    <tr><td><a href="https://github.com/lancedb/lancedb">LanceDB</a></td><td>⭐⭐⭐⭐</td><td>想把 vector data 放進 app 的開發者</td><td>embedded／serverless vector workflows</td><td>Apache-2.0；依部署模式確認能力</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Agent memory</th><td><a href="https://github.com/mem0ai/mem0">Mem0</a></td><td>⭐⭐⭐⭐⭐</td><td>要做跨 session 偏好記憶</td><td>add、search、update、delete</td><td>Apache-2.0；OSS 與託管平台分開評估</td></tr>
    <tr><td><a href="https://github.com/letta-ai/letta-code">Letta Code</a></td><td>⭐⭐⭐⭐</td><td>研究 stateful agent</td><td>memory-first agent runtime</td><td>Apache-2.0；舊 Letta V1 server 已退役</td></tr>
    <tr><td><a href="https://github.com/getzep/graphiti">Graphiti</a></td><td>⭐⭐⭐⭐</td><td>需要時間關係圖的開發者</td><td>temporal context graph</td><td>Apache-2.0；需要圖資料庫與治理</td></tr>
    <tr><td><a href="https://github.com/langchain-ai/langmem">LangMem</a></td><td>⭐⭐⭐⭐</td><td>已使用 LangGraph 的團隊</td><td>hot-path／background memory</td><td>MIT；依賴 LangGraph store 概念</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">進階與評測</th><td><a href="https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide">Anthropic Contextual Retrieval cookbook</a></td><td>⭐⭐⭐⭐⭐</td><td>完成基礎 RAG 的讀者</td><td>contextual chunks 與評測</td><td>供應商範例；數字只適用其測試設定</td></tr>
    <tr><td><a href="https://github.com/stanfordnlp/dspy">DSPy</a></td><td>⭐⭐⭐⭐⭐</td><td>已有 dataset 與 metric 的開發者</td><td>最佳化 LLM programs</td><td>MIT；不是初學 RAG 的第一步</td></tr>
    <tr><td><a href="https://github.com/vibrantlabsai/ragas">Ragas</a></td><td>⭐⭐⭐⭐⭐</td><td>要建立可重跑 eval 的團隊</td><td>datasets、metrics、experiments</td><td>Apache-2.0；metric 仍需人工校準</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">完整產品與教學</th><td><a href="https://github.com/onyx-dot-app/onyx">Onyx</a></td><td>⭐⭐⭐⭐⭐</td><td>想讀完整 AI assistant 架構</td><td>ingest、retrieval、chat、admin</td><td>完整產品很大；當架構參考，不當 starter</td></tr>
    <tr><td><a href="https://github.com/NirDiamant/RAG_Techniques">RAG_Techniques</a></td><td>⭐⭐⭐⭐⭐</td><td>想比較多種技巧的讀者</td><td>可執行 notebooks 與技術對照</td><td>社群教學資源；事實仍回到官方文件與論文核對</td></tr>
  </tbody>
</table>

</details>

## ✅ 進入 Stage 7 前的自我檢查

- [ ] 我能說出 Retrieval、RAG 與 Memory 各自做什麼。
- [ ] 我能解釋 chunk、embedding 與 vector database 怎麼接起來。
- [ ] 我的 RAG 回答會顯示來源，找不到證據時會說不知道。
- [ ] 我能用一小組問題比較修改前後，而不是只看一次漂亮回答。
- [ ] Memory 只保存必要且獲准的資料，使用者能查看、修改與刪除。

都能做到後，前往 [Stage 7 — Multi-Agent 與 Production](07-multi-agent-production.md)。

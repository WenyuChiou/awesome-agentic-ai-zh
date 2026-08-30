# 進階 RAG：先找出哪一步壞了，再加新技巧

[繁體中文](advanced-rag.md) | [English](advanced-rag.en.md) | [简体中文](advanced-rag.zh-Hans.md)

<!-- freshness: canonical=resources/advanced-rag.md; verified_on=2026-08-30; scope=rag,retrieval,reranking,graph-rag,evaluation,project-status; max_age_days=90 -->

← [回到 Stage 6：RAG 與 Memory](../stages/06-memory-rag.md)

基本 RAG 像「先翻書，再回答」。進階 RAG 不是把更多零件全裝上去，而是先看哪一步找錯資料，再只修那一步。

## 📌 學習目標

完成這頁後，你可以：

1. 分清楚「找不到」「排序錯」「證據不夠」「回答亂講」四種問題。
2. 說出 **Hybrid Search**、**Reranking**、**Query Transformation** 與 **GraphRAG** 各自修哪一步。
3. 用一小組固定問題比較修改前後，不靠一次漂亮回答下結論。
4. 知道什麼時候先停在基本 RAG，不增加成本與複雜度。

## 🧩 先認識八個核心詞

| 核心詞 | 小孩版 | 正確意思 |
|---|---|---|
| **Baseline（基線）** | 還沒加新招以前的成績 | 可重跑的最小系統與評測結果，用來比較改動是否真的有效。 |
| **Hybrid Search（混合搜尋）** | 同時看「一樣的字」和「相近的意思」 | 合併 BM25／全文搜尋與向量搜尋的候選結果。 |
| **Reranking（重新排序）** | 把拿到的卡片再排一次 | 用另一個模型或規則，重新估計問題與候選文件的相關性。 |
| **Query Transformation（查詢轉換）** | 換幾種問法再找 | 改寫、拆分或擴充問題，以取得不同候選文件。 |
| **Contextual Retrieval（情境化檢索）** | 每張小卡先寫上「這張卡來自哪一章」 | 建索引前替 chunk 補上文件背景，再做檢索。 |
| **Corrective／Adaptive RAG** | 找得不好就換方法 | 先檢查候選品質，再決定重查、改來源或直接回答。 |
| **Agentic RAG** | 讓 agent 自己決定何時翻書 | 把 retrieval 當工具，由 agent 決定是否、何時及如何呼叫。 |
| **GraphRAG** | 不只找卡片，也沿著人物與事件的線找 | 從 entity 與 relationship 建圖，支援跨文件關係與整體主題查詢。 |

## 🩺 先看症狀，再選方法

| 你看到的問題 | 先量什麼 | 第一個可試的方法 | 先不要做什麼 |
|---|---|---|---|
| 文件裡明明有答案，卻完全沒被找回 | Recall@k、命中率 | 改 chunk、metadata filter 或 Hybrid Search | 先換更大的生成模型 |
| 正確文件有找回，但排在很後面 | MRR、nDCG、前 k 名人工檢查 | Reranking | 一口氣加 graph 與 agent loop |
| 問題太短、太模糊或包含多個小問題 | 各改寫查詢的命中率與延遲 | Multi-Query、拆題或 HyDE | 無限制產生大量查詢 |
| 要回答跨很多文件的關係或整體主題 | 關係覆蓋率、global question 測試集 | GraphRAG、LightRAG 或摘要樹 | 把 graph 當成每個 RAG 的預設 |
| 有些問題根本不需要查資料 | 不必要檢索率、成本、延遲 | Adaptive／Agentic RAG | 讓 agent 無上限地重試 |
| 找到正確證據，回答仍不受證據支持 | Faithfulness／人工引用核對 | 改回答 prompt、引用格式與拒答規則 | 繼續調 retrieval 掩蓋生成問題 |

## 📚 必修閱讀

請照順序讀；它們是學習主線，不藏在選單裡。

1. [LangChain：Retrieval 概念](https://docs.langchain.com/oss/python/deepagents/retrieval) — 先分清楚 knowledge base、retriever 與 agent。
2. [Anthropic：Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) — 看 chunk 加背景、BM25、embedding 與 reranking 怎麼組合。
3. [Qdrant：Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/) — 看 dense、sparse 與 fusion 的實際查詢形狀。
4. [Weaviate：Hybrid Search](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search) — 用另一個官方實作理解 keyword 與 vector 分數如何合併。
5. [LangGraph：Agentic RAG 教學](https://docs.langchain.com/oss/python/langgraph/agentic-rag) — 完成固定 2-step RAG 後，再看 agent 如何決定檢索。
6. [Ragas](https://github.com/vibrantlabsai/ragas) — 把「看起來不錯」改成可重跑的資料集與評測迴圈。

## 🪜 從基本到進階的順序

### 1. 先凍結一個最小 Baseline

準備 20–50 個有人看過的問題，每題保存預期來源與可接受答案。每次只改一件事，記錄 retrieval、answer、延遲與成本。沒有 baseline，就不知道新技巧是幫忙還是添亂。

### 2. 先修 Retrieval，再修 Generation

- **Chunking** 決定資料怎麼切；先用標題、段落與文件結構切，再測 fixed-size、parent-child 或 semantic chunking。
- **Hybrid Search** 擴大候選來源；BM25 找精確字詞，vector search 找語意相近內容。
- **Reranking** 不會創造新文件；它只把已找回的候選重新排列。

### 3. 問題不好找時，再做 Query Transformation

- **Multi-Query**：把同一問題改成幾種說法，各自搜尋後合併。
- **HyDE**：先產生一段假想答案，再用它搜尋；可能提升召回，也可能被假想內容帶偏。
- **RAG Fusion**：對多組查詢結果做 rank fusion，降低單一措辭的影響。
- **Decomposition**：把「比較 A、B 並解釋原因」拆成數個可以分別找證據的小問題。

### 4. 需要跨文件關係時，才考慮 GraphRAG

**Microsoft GraphRAG** 是研究參考實作，官方目前標示為 largely in maintenance mode，仍修 bug 與依賴問題，但不再以新增功能為主。它的 indexing 可能昂貴，應先用小資料集。**LightRAG** 是另一套活躍的 graph-based RAG 實作，資料模型與 Microsoft GraphRAG 不相同，不能把兩者當成同一產品。

GraphRAG 適合「哪些人物共同影響這件事？」或「整批文件有哪些主題？」；單份 FAQ 或精確條款查詢，通常先用一般 retriever 就夠了。

### 5. 流程需要判斷時，才加 Corrective 或 Agentic RAG

- **Self-RAG**：模型學習何時檢索，並對證據與回答做反思。
- **CRAG（Corrective RAG）**：先判斷候選是否夠好，不夠時改查詢或改來源。
- **Adaptive RAG**：依問題難度選擇不同流程。
- **Agentic RAG**：讓 agent 決定何時叫用 retriever；必須設定步數、時間、成本與可用來源上限。

原始入口：[Self-RAG](https://arxiv.org/abs/2310.11511)、[CRAG](https://arxiv.org/abs/2401.15884)、[Adaptive-RAG](https://arxiv.org/abs/2403.14403)。

### 6. 最後才碰摘要樹與程式最佳化

**RAPTOR** 把內容反覆群聚、摘要成由細到粗的樹；細節問題找葉節點，主題問題找高層摘要。**DSPy** 用 examples 與 metric 調整 LLM program；它仍需要清楚任務、可靠資料與評測指標。

閱讀：[RAPTOR paper](https://arxiv.org/abs/2401.18059) · [DSPy](https://github.com/stanfordnlp/dspy)

## 🛠 一個可重跑的小實驗

1. 選 20 題，為每題標出正確來源。
2. 跑最小 vector retrieval，保存 top-5 結果。
3. 只加入 BM25，重新跑同一批題目。
4. 再只加入 reranker，比較 top-5、延遲與成本。
5. 寫下哪幾題變好、哪幾題變差，以及原因。

**完成條件：**你能拿出同一份測試集的三組結果，而不是只展示一題成功案例。

<details markdown="1">
<summary>成本、資料與上線前檢查</summary>

- Indexing 是否會呼叫付費模型？先用小樣本估算一次完整重建成本。
- 每個 chunk 是否保留來源、頁碼／位置、版本、時間與存取權限？
- Retriever 是否在查詢前套用權限，而不是找到後才遮住答案？
- Agentic loop 是否有最大步數、timeout、budget 與安全來源清單？
- Cache 是否會讓舊文件繼續被取回？更新與刪除流程是否測過？

</details>

<details markdown="1">
<summary>常見失敗與排查順序</summary>

1. 先看正確證據有沒有進 top-k。
2. 有進 top-k，再看 reranker 是否把它往後排。
3. 排名正確，再看 prompt 是否要求引用與拒答。
4. 最後才檢查生成模型；不要用更大模型掩蓋 retrieval 錯誤。

</details>

## 🎯 精選 Projects 與學習資源

評分代表「對這張學習地圖的教學價值」，不是專案品質排行榜。先選一個框架、一個資料層與一個評測工具。

<small>資料查核：2026-08-30 UTC</small>

<table>
  <thead><tr><th scope="col">分類</th><th scope="col">專案／資源</th><th scope="col">編輯評分</th><th scope="col">適合誰</th><th scope="col">能學什麼</th><th scope="col">狀態／限制</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Pipeline 與範例</th><td><a href="https://github.com/run-llama/llama_index">LlamaIndex</a></td><td>⭐⭐⭐⭐⭐</td><td>文件型應用開發者</td><td>retriever、query engine、evaluation</td><td>MIT；套件多，先跟官方 starter</td></tr>
    <tr><td><a href="https://github.com/deepset-ai/haystack">Haystack</a></td><td>⭐⭐⭐⭐</td><td>想看模組化 pipeline</td><td>components、routing、retrieval</td><td>Apache-2.0；先做小型 pipeline</td></tr>
    <tr><td><a href="https://github.com/NirDiamant/RAG_Techniques">RAG_Techniques</a></td><td>⭐⭐⭐⭐⭐</td><td>想比較技術的讀者</td><td>可執行 notebooks 與技術對照</td><td>社群教材；事實回官方文件核對</td></tr>
    <tr><td><a href="https://github.com/infiniflow/ragflow">RAGFlow</a></td><td>⭐⭐⭐⭐</td><td>想讀完整產品架構的團隊</td><td>解析、hybrid retrieval、UI</td><td>Apache-2.0；不適合當第一個 starter</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">搜尋與圖</th><td><a href="https://github.com/qdrant/qdrant">Qdrant</a></td><td>⭐⭐⭐⭐⭐</td><td>要練 dense＋sparse search</td><td>hybrid query、fusion、filter</td><td>Apache-2.0；需規劃服務與備份</td></tr>
    <tr><td><a href="https://github.com/pgvector/pgvector">pgvector</a></td><td>⭐⭐⭐⭐</td><td>已使用 PostgreSQL 的團隊</td><td>SQL、全文與 vector 同庫</td><td>仍需索引與查詢調校</td></tr>
    <tr><td><a href="https://github.com/microsoft/graphrag">Microsoft GraphRAG</a></td><td>⭐⭐⭐⭐</td><td>研究跨文件關係的讀者</td><td>entity graph、local／global search</td><td>MIT；維護模式、indexing 成本高</td></tr>
    <tr><td><a href="https://github.com/HKUDS/LightRAG">LightRAG</a></td><td>⭐⭐⭐⭐</td><td>比較 graph-based RAG 的讀者</td><td>graph＋vector retrieval</td><td>MIT；架構不同於 Microsoft GraphRAG</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">評測與最佳化</th><td><a href="https://github.com/vibrantlabsai/ragas">Ragas</a></td><td>⭐⭐⭐⭐⭐</td><td>要建立可重跑 eval 的團隊</td><td>datasets、metrics、experiments</td><td>Apache-2.0；LLM metric 仍需人工校準</td></tr>
    <tr><td><a href="https://github.com/truera/trulens">TruLens</a></td><td>⭐⭐⭐⭐</td><td>需要 tracing 與 evaluation</td><td>feedback functions、紀錄與比較</td><td>先確認整合與資料保存方式</td></tr>
    <tr><td><a href="https://github.com/stanfordnlp/dspy">DSPy</a></td><td>⭐⭐⭐⭐⭐</td><td>已有 dataset 與 metric 的開發者</td><td>最佳化 LLM programs</td><td>MIT；不是初學 RAG 的第一步</td></tr>
    <tr><td><a href="https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide">Anthropic Contextual Retrieval cookbook</a></td><td>⭐⭐⭐⭐⭐</td><td>已完成 baseline 的讀者</td><td>contextual chunks 與評測</td><td>供應商範例；數字只適用其設定</td></tr>
  </tbody>
</table>

## ✅ 自我檢查

- [ ] 我會先保存 baseline，再一次改一個元件。
- [ ] 我能分清楚 Hybrid Search 與 Agentic RAG。
- [ ] 我知道 Reranking 不能找回根本沒進候選集的文件。
- [ ] 我能說出 GraphRAG 適合的問題，也能說出不該用它的情況。
- [ ] 我的評測同時記錄品質、延遲、成本與失敗案例。

← [回到 Stage 6：RAG 與 Memory](../stages/06-memory-rag.md)

# 進階 RAG：先找出哪一步壞了，再加新技巧

**RAG**（Retrieval-Augmented Generation）：先找相關資料，再依資料回答。

[繁體中文](advanced-rag.md) | [English](advanced-rag.en.md) | [简体中文](advanced-rag.zh-Hans.md)

<!-- freshness: canonical=resources/advanced-rag.md; verified_on=2026-08-30; scope=rag,retrieval,reranking,graph-rag,evaluation,project-status; max_age_days=90 -->

← [回到 Stage 6：RAG 與 Memory](../stages/06-memory-rag.md)

基本 RAG 像「先翻書，再回答」。進階 RAG 不是把更多零件全裝上去，而是先看哪一步找錯資料，再只修那一步。

## 📌 學習目標

完成這頁後，你可以：

1. 分清楚「找不到」「排序錯」「證據不夠」「回答亂講」四種問題。
2. 知道何時該改搜尋、重排結果、換問法，或連起跨文件的關係。
3. 用一小組固定問題比較修改前後，不靠一次漂亮回答下結論。
4. 知道什麼時候先停在基本 RAG，不增加成本與複雜度。

## 🧩 先認識八個核心詞

<div class="reader-core-terms" align="center" role="region" tabindex="0" aria-label="搜尋核心詞" markdown="1">

| 核心詞 | 白話說法 | 這裡怎麼用 |
|:---|:---|:---|
| **Chunk（資料片段）** | 把長文件切成小段 | 搜尋時先找片段，並保留它的來源。 |
| **Embedding（向量表示）** | 用一串數字表示文字意思 | 把問題與資料片段轉成可比較的數字。 |
| **Vector Search（向量搜尋）** | 找意思相近的內容 | 比較向量的相近程度，不只看字是否一樣。 |
| **BM25（關鍵字排名方法）** | 按字詞匹配程度排順序 | 例如找產品編號 AB-123；也考慮字詞多常見及文件長度。 |
| **Retriever（檢索器）** | 幫你找資料的零件 | 依問題找出可能有用的片段；這些就是「候選資料」。 |
| **Hybrid Search（混合搜尋）** | 兩種找法一起用 | 合併 BM25 與向量搜尋的結果，去掉重複資料。 |
| **Reranking（重新排序）** | 把找到的資料再排一次 | 再看問題與候選資料的關係，把更有用的往前放。 |
| **Baseline（基線）** | 修改前的成績 | 保存原本系統與測試結果，留待改完後比較。 |

</div>

先看這條路：問題 → 找候選資料 → 重新排序（可選）→ 依資料回答。<strong>Retrieval（檢索）</strong>是找資料；<strong>Generation（生成）</strong>是寫答案。先分清楚哪一步出錯，再改那一步。

## 🩺 先看症狀，再選方法

先固定一組問題，並標出每題該找回的資料。`k` 是只看前幾筆，例如 `k = 5` 就看前五筆。

- <strong>Recall@k（前 k 筆召回率）</strong>：該找回的資料，前 k 筆找回了多少比例。
- <strong>命中率</strong>：這組問題中，有多少比例的題目在前 k 筆至少找到一筆相關資料。

例如：一題該找回四份資料，前五筆找到兩份，Recall@5 就是 50%；這題也算命中。

例如搜尋 AB-123 的保固，卻只找到其他產品？先看正確資料有沒有被找回，再試 BM25。若已找回卻排很後面，再試 Reranking。兩者都正常，才檢查答案是否照著證據寫。

<div align="center" markdown="1">

| 你看到的問題 | 先量什麼 | 第一個可試的方法 | 先不要做什麼 |
|:---|:---|:---|:---|
| 文件裡有答案，卻沒找回 | Recall@k、命中率 | [調整切法或混合搜尋](#rag-search) | 先換更大的生成模型 |
| 正確資料有找回，但排很後面 | 人工看前 k 筆的順序 | [重新排序](#rag-search) | 一口氣增加很多零件 |
| 問題太模糊，或一次問太多事 | 各問法的命中率與等待時間 | [改寫或拆開問題](#rag-query) | 無限制地產生查詢 |
| 要連起多份文件的人物、事件 | 準備幾題跨文件問題，核對關係 | [先試關係搜尋](#rag-graph) | 每個系統都先建圖 |
| 問題不需資料也一直搜尋 | 多查了幾次、花多少錢和時間 | [加入是否搜尋的判斷](#rag-decisions) | 無上限地重試 |
| 證據正確，答案卻不照證據寫 | 逐句核對答案與引用 | 改提示詞、引用與拒答規則 | 繼續改搜尋掩蓋回答問題 |

</div>

要把排序變成分數時，再用 <strong>MRR（Mean Reciprocal Rank）</strong>看第一筆相關結果是否夠前面；用 <strong>nDCG（Normalized Discounted Cumulative Gain）</strong>比較整體排序與理想順序。核對答案是否受證據支持，叫 **Faithfulness（忠實度）**；它不等於答案符合所有外部事實。

## 📚 必修閱讀

請照順序讀；它們是學習主線，不藏在選單裡。

1. [LangChain：Retrieval 概念](https://docs.langchain.com/oss/python/deepagents/retrieval) — 分清楚保存資料、找資料與決定下一步的零件。
2. [Anthropic：Contextual Retrieval（情境化檢索）](https://www.anthropic.com/engineering/contextual-retrieval) — 先替片段補來源背景，再建立搜尋用的目錄（索引）。
3. [Qdrant：Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/) — 看兩路搜尋結果如何合併與重新排序。
4. [Weaviate：Hybrid Search](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search) — 看另一種關鍵字與向量搜尋的合併方式。
5. [LangGraph：Agentic RAG（由 Agent 決定何時搜尋）](https://docs.langchain.com/oss/python/langgraph/agentic-rag) — 先完成固定的「找資料 → 回答」，再看如何加入判斷。
6. [Ragas](https://github.com/vibrantlabsai/ragas) — 把「看起來不錯」改成可重跑的資料集與評測迴圈。

## 🪜 從基本到進階的順序

### 1. 先凍結一個最小 Baseline

準備 20–50 個經人工檢查的問題，每題保存預期來源與可接受答案。先跑目前的版本，記錄找回的資料、答案、等待時間（延遲）與成本。接著一次只改一件事，才知道是哪個改動有幫助。

<a id="rag-search"></a>
### 2. 先修 Retrieval，再修 Generation

- **Chunking（切分資料）**：先按標題與段落切。再比較固定長度（fixed-size）、先找小段再帶回大段（parent-child），或按意思分段（semantic chunking）。
- **Metadata Filter（附加資料篩選）**：用片段的產品名稱、日期或權限等標籤縮小範圍。先確認篩選沒有擋掉正確資料。
- **Hybrid Search**：BM25 補字詞匹配，向量搜尋補意思相近的內容；先測合併後是否真的找得更多。
- **Reranking** 不會創造新文件；它只把已找回的候選重新排列。

文件也會提到 <strong>dense（密集向量）</strong>與 **sparse（稀疏向量）**：前者通常大多數位置有數值，後者多數位置是零。<strong>Fusion（融合）</strong>是合併不同搜尋的分數或排名。向量的疏密本身不保證搜尋品質。

<a id="rag-query"></a>
### 3. 問題不好找時，再做 Query Transformation

<strong>Query Transformation（查詢轉換）</strong>是把問題換個問法，或拆成小題後再找。先選一種試，不必全加。

- **Multi-Query**：把同一問題改成幾種說法，各自搜尋後合併。
- **HyDE（Hypothetical Document Embeddings）**：先寫假想答案，轉成向量，再找真實資料。假想內容不是證據，也可能把搜尋帶偏。
- **RAG Fusion**：合併多種問法得到的排名，降低單一措辭的影響。
- **Decomposition**：把「比較 A、B 並解釋原因」拆成數個可以分別找證據的小問題。

<a id="rag-graph"></a>
### 4. 需要跨文件關係時，才考慮 GraphRAG

**GraphRAG**把文件中的人物、組織等「實體」及彼此的關係連成圖，再用來找證據。例如把「誰參與哪個計畫」跨文件連起來。單份問答或精確條款，通常先用一般檢索器就夠了。

**Microsoft GraphRAG** 是研究參考實作，官方目前標示為 largely in maintenance mode，仍修 bug 與依賴問題，但不再以新增功能為主。它的 indexing 可能昂貴，應先用小資料集。**LightRAG** 是另一套活躍的 graph-based RAG 實作，資料模型與 Microsoft GraphRAG 不相同，不能把兩者當成同一產品。

先拿「哪些人物共同影響這件事？」或「整批文件有哪些主題？」測試，確認建圖的成本有換到更好的答案。

<a id="rag-decisions"></a>
### 5. 流程需要判斷時，才加 Corrective 或 Agentic RAG

前面的做法大多照固定步驟搜尋、回答。只有需要「現在要不要查、查不好怎麼辦」時，才增加下面的判斷。

- **Self-RAG**：模型學習何時檢索，並對證據與回答做反思。
- **CRAG**（Corrective Retrieval Augmented Generation，也叫 Corrective RAG）：先判斷候選是否夠好，不夠時改查詢或改來源。
- **Adaptive RAG**：依問題難度選擇不同流程。
- **Agentic RAG**：讓 agent 決定何時叫用 retriever；必須設定步數、時間、成本與可用來源上限。

原始入口：[Self-RAG](https://arxiv.org/abs/2310.11511)、[CRAG](https://arxiv.org/abs/2401.15884)、[Adaptive-RAG](https://arxiv.org/abs/2403.14403)。

### 6. 最後才碰摘要樹與程式最佳化

**RAPTOR**（Recursive Abstractive Processing for Tree-Organized Retrieval）把相近片段分組、寫摘要，再逐層合成較大的摘要。細節問題找原片段，主題問題找上層摘要。

**DSPy**用範例與評分規則，調整 LLM（Large Language Model，能讀寫語言的模型）的提示詞或示範，改善整個流程。先有清楚任務、可靠資料與評測，才適合用它。

閱讀：[RAPTOR paper](https://arxiv.org/abs/2401.18059) · [DSPy](https://github.com/stanfordnlp/dspy)

## 🛠 一個可重跑的小實驗

1. 選 20 題，為每題標出正確來源。
2. **A：基線**。只用向量搜尋，保存前五筆結果與答案。
3. **B：混合搜尋**。保留 A，只加入 BM25 並合併結果，重跑同一批題目。
4. **C：再加排序**。保留 B，只加入重新排序，重跑同一批題目。
5. 三組都記錄 Recall@5、命中率、延遲與成本。其餘設定相同，寫下哪幾題變好或變差。

**完成條件：** 你能拿出同一份測試集的三組結果，而不是只展示一題成功案例。

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

<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="精選專案與學習資源">
<table align="center">
  <thead><tr><th scope="col">分類</th><th scope="col">專案／文件</th><th scope="col">評分</th><th scope="col">用途</th><th scope="col">限制</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">流程與範例</th><td><div data-field="entry"><strong><a href="https://github.com/run-llama/llama_index">LlamaIndex</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>適合誰：</strong> 文件型應用開發者</div><div data-field="learn"><strong>能學什麼：</strong> 找資料、組織回答與評測</div></td><td><div data-field="status"><strong>狀態／限制：</strong> MIT；套件多，先跟官方 starter</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/deepset-ai/haystack">Haystack</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>適合誰：</strong> 想把處理步驟拆成小零件</div><div data-field="learn"><strong>能學什麼：</strong> 拆分零件、選路與搜尋</div></td><td><div data-field="status"><strong>狀態／限制：</strong> Apache-2.0；先做小型流程</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/NirDiamant/RAG_Techniques">RAG_Techniques</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>適合誰：</strong> 想比較技術的讀者</div><div data-field="learn"><strong>能學什麼：</strong> 可執行 notebooks 與技術對照</div></td><td><div data-field="status"><strong>狀態／限制：</strong> 自訂非商業授權；商用須書面許可；事實回官方文件核對</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/infiniflow/ragflow">RAGFlow</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>適合誰：</strong> 想讀完整產品架構的團隊</div><div data-field="learn"><strong>能學什麼：</strong> 讀取文件、混合搜尋與操作畫面</div></td><td><div data-field="status"><strong>狀態／限制：</strong> Apache-2.0；不適合當第一個 starter</div></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">搜尋與圖</th><td><div data-field="entry"><strong><a href="https://github.com/qdrant/qdrant">Qdrant</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>適合誰：</strong> 要合併密集與稀疏向量搜尋</div><div data-field="learn"><strong>能學什麼：</strong> 合併搜尋結果與篩選資料</div></td><td><div data-field="status"><strong>狀態／限制：</strong> Apache-2.0；需規劃服務與備份</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/pgvector/pgvector">pgvector</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>適合誰：</strong> 已使用 PostgreSQL 的團隊</div><div data-field="learn"><strong>能學什麼：</strong> 在同一資料庫做文字與向量搜尋</div></td><td><div data-field="status"><strong>狀態／限制：</strong> 仍需索引與查詢調校</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/microsoft/graphrag">Microsoft GraphRAG</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>適合誰：</strong> 研究跨文件關係的讀者</div><div data-field="learn"><strong>能學什麼：</strong> 實體關係、局部與整體主題搜尋</div></td><td><div data-field="status"><strong>狀態／限制：</strong> MIT；維護模式、建索引成本高</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/HKUDS/LightRAG">LightRAG</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>適合誰：</strong> 比較以關係圖找證據的讀者</div><div data-field="learn"><strong>能學什麼：</strong> 關係圖與向量搜尋</div></td><td><div data-field="status"><strong>狀態／限制：</strong> MIT；架構不同於 Microsoft GraphRAG</div></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">評測與最佳化</th><td><div data-field="entry"><strong><a href="https://github.com/vibrantlabsai/ragas">Ragas</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>適合誰：</strong> 要重跑評測的團隊</div><div data-field="learn"><strong>能學什麼：</strong> 測試資料、評分與實驗比較</div></td><td><div data-field="status"><strong>狀態／限制：</strong> Apache-2.0；模型評分仍需人工校準</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/truera/trulens">TruLens</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>適合誰：</strong> 想追查執行過程並評測</div><div data-field="learn"><strong>能學什麼：</strong> 自訂評分、紀錄與比較</div></td><td><div data-field="status"><strong>狀態／限制：</strong> 先確認整合與資料保存方式</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/stanfordnlp/dspy">DSPy</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>適合誰：</strong> 已有測試資料與評分規則的開發者</div><div data-field="learn"><strong>能學什麼：</strong> 改善模型的工作流程</div></td><td><div data-field="status"><strong>狀態／限制：</strong> MIT；不是初學 RAG 的第一步</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide">Anthropic Contextual Retrieval cookbook</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>適合誰：</strong> 已完成 baseline 的讀者</div><div data-field="learn"><strong>能學什麼：</strong> 片段補背景與評測</div></td><td><div data-field="status"><strong>狀態／限制：</strong> 供應商範例；數字只適用其設定</div></td></tr>
  </tbody>
</table>
</div>

## ✅ 自我檢查

- [ ] 我會先保存 baseline，再一次改一個元件。
- [ ] 我能分清楚 Hybrid Search 與 Agentic RAG。
- [ ] 我知道 Reranking 不能找回根本沒進候選集的文件。
- [ ] 我能說出 GraphRAG 適合的問題，也能說出不該用它的情況。
- [ ] 我的評測同時記錄品質、延遲、成本與失敗案例。

← [回到 Stage 6：RAG 與 Memory](../stages/06-memory-rag.md)

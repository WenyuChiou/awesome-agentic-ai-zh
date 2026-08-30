<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 2：Vector DB 與兩種搜尋

← 回到 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.md#練習-2vector-db)

**Vector DB（向量資料庫）**像一個會按「意思」找東西的抽屜。你先把文件與向量放進去，再用問題找出最接近的文件。

## 📌 學習目標

- 說出 **vector database**、**semantic search**、**keyword search** 的差別。
- 把 8 份文件存進 Chroma collection。
- 用同一個問題比較語意搜尋和字面搜尋。
- 知道 `EphemeralClient` 與 `PersistentClient` 何時使用。

## 🔑 核心詞

| 核心詞 | 白話意思 |
|---|---|
| **Collection** | 裝文件、向量和 metadata 的一個抽屜 |
| **Semantic search** | 比較意思，不要求文字一模一樣 |
| **Keyword search** | 尋找相同字詞，專有名詞很準，但同義詞容易漏 |
| **Metadata filter** | 先用標籤縮小範圍，例如只找 `category=tech` |

## 📚 必讀與學習資源

- ★★★★★ [Chroma Clients 官方文件](https://docs.trychroma.com/reference/python/client)：分清楚記憶體與磁碟儲存。
- ★★★★★ [Chroma Embedding Functions 官方文件](https://docs.trychroma.com/docs/embeddings/embedding-functions)：看 collection 如何建立向量。
- ★★★★☆ [VectorDBBench](https://github.com/zilliztech/VectorDBBench)：需要比較大型部署時，再用自己的負載做 benchmark。
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：較完整的 vector store 教材。

<sub>資料查核：2026-08-30 UTC。</sub>

## ▶️ 先直接跑 Path A（本機、與廠商無關、免費）

```powershell
pip install -r requirements.txt
python starter.py
```

本練習使用本機 Chroma，API 費用是 **$0**。第一次執行可能會下載本機 embedding 模型。

<details markdown="1">
<summary>Path B（預覽：這一步之後怎麼接到 Claude）</summary>

Vector DB 這一步只負責「存資料、找資料」，跟之後用哪一家模型生成答案無關。這裡跑一次 `starter_anthropic.py`，只是先讓你看到同一套儲存與搜尋程式，之後會原封不動接到[練習 4](../04-full-rag-pipeline/README.md)的 Claude 生成步驟前面。這一步沒有呼叫任何 API，費用是 **$0**。

```powershell
python starter_anthropic.py
```

</details>

**Stage 06 總預算**：五個 Path A 全部跑完，API 費用仍是 **$0**（不含下載、磁碟與電費）。選跑雲端 Path 時，費用依 embedding／輸入／輸出 token 實際用量計算；先設小額帳戶上限，成功跑一次就停。

```powershell
python test.py
python test_anthropic.py
```

測試不下載模型。Vector DB 不綁定 Claude、OpenAI 或 Ollama，所以 Path B 重用同一套儲存與搜尋程式。

## 兩種搜尋怎麼選

| 需求 | Keyword search | Semantic search |
|---|---|---|
| 找完全相同的編號或名稱 | 很適合 | 可能混淆 |
| 找換句話說的內容 | 容易漏 | 很適合 |
| 要簡單、快速 | 很適合 | 要先做 embedding |
| 實際 RAG | 常和 BM25 搭配 | 常和 keyword 結果合併 |

把 keyword 與 vector 結果合併，叫做 **hybrid search（混合搜尋）**。這份練習先把兩者分開，讓差別看得清楚；Stage 6 主章再連到 Qdrant 與 Weaviate 的正式 hybrid search 文件。

## Chroma 的兩種儲存方式

```python
# 練習與測試：關掉程式後資料消失
client = chromadb.EphemeralClient()

# 本機需要留下資料：重新開程式還讀得到
client = chromadb.PersistentClient(path="./chroma_db")
```

官方文件把 `PersistentClient` 定位為本機開發與測試用；正式大型服務通常改用 server-backed Chroma 或其他受管服務。

## 程式流程

```python
collection = build_collection()
index_docs(collection, DOCS)
results = semantic_query(collection, "where to drink coffee", top_k=3)
```

1. 建立 collection。
2. 寫入 `id`、文件與 metadata。
3. 查詢並取回距離最近的 `top-k` 筆。

<details>
<summary>常見問題與進階做法</summary>

- `.add()` 遇到重複 `id` 會失敗；要更新資料時用 `.upsert()`。
- 建立與查詢必須使用相同 embedding function。
- `top_k` 太大會帶回雜訊；先用真實問題測 `3`、`5`、`10`。
- 需要磁碟保存時，把 `build_collection(path="./chroma_db")` 傳入清楚的資料夾。
- 需要真正的 BM25 + vector hybrid search 時，參考 Stage 6 的 Qdrant 或 Weaviate 路徑。

</details>

下一步：先在 [練習 3：Chunking](../03-chunking-comparison/README.md)學會怎麼切文件，再組成完整 RAG。

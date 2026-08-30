<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 2：Vector DB 与两种搜索

← 回到 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.zh-Hans.md#练习-2vector-db)

**Vector DB（向量数据库）**像一个会按“意思”找东西的抽屉。你先把文档与向量放进去，再用问题找出最接近的文档。

## 📌 学习目标

- 说出 **vector database**、**semantic search**、**keyword search** 的差别。
- 把 8 份文档存进 Chroma collection。
- 用同一个问题比较语义搜索和字面搜索。
- 知道 `EphemeralClient` 与 `PersistentClient` 何时使用。

## 🔑 核心词

| 核心词 | 白话意思 |
|---|---|
| **Collection** | 装文档、向量和 metadata 的一个抽屉 |
| **Semantic search** | 比较意思，不要求文字一模一样 |
| **Keyword search** | 寻找相同字词，专有名词很准，但同义词容易漏 |
| **Metadata filter** | 先用标签缩小范围，例如只找 `category=tech` |

## 📚 必读与学习资源

- ★★★★★ [Chroma Clients 官方文档](https://docs.trychroma.com/reference/python/client)：分清楚内存与磁盘存储。
- ★★★★★ [Chroma Embedding Functions 官方文档](https://docs.trychroma.com/docs/embeddings/embedding-functions)：看 collection 如何建立向量。
- ★★★★☆ [VectorDBBench](https://github.com/zilliztech/VectorDBBench)：需要比较大型部署时，再用自己的负载做 benchmark。
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：较完整的 vector store 教材。

<sub>资料查核：2026-08-30 UTC。</sub>

## ▶️ 先直接跑 Path A（本机、与厂商无关、免费）

```powershell
pip install -r requirements.txt
python starter.py
```

本练习使用本机 Chroma，API 费用是 **$0**。第一次执行可能会下载本机 embedding 模型。

<details markdown="1">
<summary>Path B（预览：这一步之后怎么接到 Claude）</summary>

Vector DB 这一步只负责“存数据、找数据”，跟之后用哪一家模型生成答案无关。这里跑一次 `starter_anthropic.py`，只是先让你看到同一套存储与搜索程序，之后会原封不动接到[练习 4](../04-full-rag-pipeline/README.zh-Hans.md)的 Claude 生成步骤前面。这一步没有调用任何 API，费用是 **$0**。

```powershell
python starter_anthropic.py
```

</details>

**Stage 06 总预算**：五个 Path A 全部跑完，API 费用仍是 **$0**（不含下载、磁盘与电费）。选跑云端 Path 时，费用依 embedding／输入／输出 token 实际用量计算；先设小额账户上限，成功跑一次就停。

```powershell
python test.py
python test_anthropic.py
```

测试不下载模型。Vector DB 不绑定 Claude、OpenAI 或 Ollama，所以 Path B 重用同一套存储与搜索程序。

## 两种搜索怎么选

| 需求 | Keyword search | Semantic search |
|---|---|---|
| 找完全相同的编号或名称 | 很适合 | 可能混淆 |
| 找换句话说的内容 | 容易漏 | 很适合 |
| 要简单、快速 | 很适合 | 要先做 embedding |
| 实际 RAG | 常和 BM25 搭配 | 常和 keyword 结果合并 |

把 keyword 与 vector 结果合并，叫做 **hybrid search（混合搜索）**。这份练习先把两者分开，让差别看得清楚；Stage 6 主章再连到 Qdrant 与 Weaviate 的正式 hybrid search 文档。

## Chroma 的两种存储方式

```python
# 练习与测试：关掉程序后数据消失
client = chromadb.EphemeralClient()

# 本机需要留下数据：重新开程序还读得到
client = chromadb.PersistentClient(path="./chroma_db")
```

官方文档把 `PersistentClient` 定位为本机开发与测试用；正式大型服务通常改用 server-backed Chroma 或其他受管服务。

## 程序流程

```python
collection = build_collection()
index_docs(collection, DOCS)
results = semantic_query(collection, "where to drink coffee", top_k=3)
```

1. 创建 collection。
2. 写入 `id`、文档与 metadata。
3. 查询并取回距离最近的 `top-k` 笔。

<details>
<summary>常见问题与进阶做法</summary>

- `.add()` 遇到重复 `id` 会失败；要更新数据时用 `.upsert()`。
- 创建与查询必须使用相同 embedding function。
- `top_k` 太大会带回噪声；先用真实问题测 `3`、`5`、`10`。
- 需要磁盘保存时，把 `build_collection(path="./chroma_db")` 传入清楚的文件夹。
- 需要真正的 BM25 + vector hybrid search 时，参考 Stage 6 的 Qdrant 或 Weaviate 路径。

</details>

下一步：先在 [练习 3：Chunking](../03-chunking-comparison/README.zh-Hans.md)学会怎么切文档，再组成完整 RAG。

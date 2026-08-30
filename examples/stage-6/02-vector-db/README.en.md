<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 2: Vector DB and Two Kinds of Search

← Back to [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.en.md#exercise-2-vector-db)

A **vector database** is like a drawer that finds things by "meaning." You put documents and their vectors in, then use a question to pull out the closest documents.

## 📌 Learning goals

- Say what tells **vector database**, **semantic search**, and **keyword search** apart.
- Store 8 documents in a Chroma collection.
- Compare semantic search against keyword search on the same question.
- Know when to use `EphemeralClient` versus `PersistentClient`.

## 🔑 Core terms

| Core term | Plain meaning |
|---|---|
| **Collection** | A drawer holding documents, vectors, and metadata |
| **Semantic search** | Compares meaning; the wording doesn't need to match exactly |
| **Keyword search** | Looks for the same words; precise on proper nouns, but easy to miss synonyms |
| **Metadata filter** | Narrows the search with tags first, e.g. only `category=tech` |

## 📚 Required reading and learning resources

- ★★★★★ [Chroma Clients official docs](https://docs.trychroma.com/reference/python/client): tells in-memory and on-disk storage apart.
- ★★★★★ [Chroma Embedding Functions official docs](https://docs.trychroma.com/docs/embeddings/embedding-functions): see how a collection builds its vectors.
- ★★★★☆ [VectorDBBench](https://github.com/zilliztech/VectorDBBench): once you need to compare larger deployments, benchmark them with your own workload.
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents): a fuller course on vector stores.

<sub>Data verified: 2026-08-30 UTC.</sub>

## ▶️ Run Path A first (local, provider-independent, free)

```powershell
pip install -r requirements.txt
python starter.py
```

This exercise uses local Chroma, so the API cost is **$0**. The first run may download a local embedding model.

<details markdown="1">
<summary>Path B (preview: how this step feeds into Claude later)</summary>

The vector DB step only stores and searches data — it doesn't care which model generates the final answer later. Running `starter_anthropic.py` here just shows you the same storage and search code that will plug in, unchanged, right before the Claude generation step in [Exercise 4](../04-full-rag-pipeline/README.en.md). This step makes no API call, so the cost is **$0**.

```powershell
python starter_anthropic.py
```

</details>

**Total Stage 06 budget**: Running all five Path A exercises keeps API fees at **$0** (downloads, disk space, and electricity excluded). Optional cloud paths are billed from actual embedding, input, and output token usage; set a small account cap and stop after one successful run.

```powershell
python test.py
python test_anthropic.py
```

The tests don't download a model. The vector DB isn't tied to Claude, OpenAI, or Ollama, so Path B reuses the same storage and search code.

## Choosing between the two kinds of search

| Need | Keyword search | Semantic search |
|---|---|---|
| Find an exact ID or name | A great fit | Can get confused |
| Find content phrased differently | Easy to miss | A great fit |
| Simple and fast | A great fit | Needs embedding first |
| Real-world RAG | Often paired with BM25 | Often merged with keyword results |

Merging keyword and vector results is called **hybrid search**. This exercise keeps the two separate first so the difference is clear; the Stage 6 main chapter links out to Qdrant's and Weaviate's official hybrid search docs.

## Chroma's two storage modes

```python
# Exercises and tests: data disappears when the program closes
client = chromadb.EphemeralClient()

# Local use where you need data to persist: still readable after restarting
client = chromadb.PersistentClient(path="./chroma_db")
```

The official docs position `PersistentClient` for local development and testing; real large-scale services usually move to server-backed Chroma or another managed service.

## Program flow

```python
collection = build_collection()
index_docs(collection, DOCS)
results = semantic_query(collection, "where to drink coffee", top_k=3)
```

1. Create a collection.
2. Write in `id`, documents, and metadata.
3. Query and get back the closest `top-k` entries.

<details>
<summary>Common pitfalls and advanced practice</summary>

- `.add()` fails on a duplicate `id`; use `.upsert()` when updating data.
- Indexing and querying must use the same embedding function.
- Too large a `top_k` brings back noise; test `3`, `5`, and `10` with real questions first.
- When you need the data to persist on disk, pass `build_collection(path="./chroma_db")` a clear folder.
- When you need real BM25 + vector hybrid search, see Stage 6's Qdrant or Weaviate path.

</details>

Next: learn how to split documents in [Exercise 3: Chunking](../03-chunking-comparison/README.en.md) before assembling a complete RAG pipeline.

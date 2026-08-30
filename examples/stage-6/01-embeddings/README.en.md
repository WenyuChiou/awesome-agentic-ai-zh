<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 1: Embeddings and Similarity Search

← Back to [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.en.md#exercise-1-embeddings)

Imagine placing every sentence on a big map. Sentences that mean similar things end up standing close together. An **embedding** is just the numeric coordinates of a sentence on that map.

## 📌 Learning goals

- Say what **embedding**, **vector**, and **cosine similarity** are.
- Turn 100 sentences into vectors.
- Find the `top-k` sentences closest to a question.
- Tell local models and cloud embeddings apart.

## 🔑 Three core terms first

| Core term | Plain meaning | What you see in code |
|---|---|---|
| **Embedding** | Turning text into a row of numbers so a computer can compare meaning | `model.encode(...)` |
| **Vector** | That row of numbers | `[0.12, -0.04, ...]` |
| **Cosine similarity** | How alike two vectors' directions are; closer to `1` usually means closer in meaning | `sent_vecs @ q_vec` |

## 📚 Required reading and learning resources

- ★★★★★ [Sentence Transformers official docs](https://www.sbert.net/): first-party explanation and examples for local embeddings.
- ★★★★★ [OpenAI `text-embedding-3-small` official model page](https://developers.openai.com/api/docs/models/text-embedding-3-small): cloud model, use cases, and current pricing.
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents): a good next read for a fuller chapter on embeddings and RAG after this exercise.

<sub>Data verified: 2026-08-30 UTC.</sub>

## ▶️ Run Path A first (local, free)

```powershell
pip install -r requirements.txt
python starter.py
```

The first run downloads `sentence-transformers/all-MiniLM-L6-v2`. The model runs on your own machine, so the API cost is **$0**.

<details markdown="1">
<summary>Path B (cloud embedding, OpenAI)</summary>

```powershell
pip install -r requirements.txt
$env:OPENAI_API_KEY = Read-Host "OpenAI API key"
python starter_anthropic.py
```

Anthropic doesn't currently offer its own embedding API; the [official Anthropic embeddings guide](https://platform.claude.com/docs/en/build-with-claude/embeddings) uses Voyage AI as its main example. This starter uses OpenAI so you can do a simple side-by-side with the local result.

`text-embedding-3-small` is billed by input tokens:

```text
cost = input tokens ÷ 1,000,000 × price per million tokens
```

Check the official model page for current pricing before you run it, and set a small usage cap on your API account.

</details>

**Total Stage 06 budget**: Running all five Path A exercises keeps API fees at **$0** (downloads, disk space, and electricity excluded). Optional cloud paths are billed from actual embedding, input, and output token usage; set a small account cap and stop after one successful run.

## ✅ Verify without downloading a model

```powershell
python test.py
python test_anthropic.py
```

The tests use fake vectors and a fake API reply, so nothing reaches the network and nothing gets billed.

## The program only does three things

```python
sent_vecs = model.encode(sentences, normalize_embeddings=True)
q_vec = model.encode([query], normalize_embeddings=True)[0]
sims = sent_vecs @ q_vec
top_idx = np.argsort(-sims)[:top_k]
```

1. Turn both the sentences and the question into vectors.
2. Compare the vectors' directions.
3. Put the `top-k` highest-scoring entries first.

**Normalize** scales every vector to the same length. Once that's done, a dot product can be used directly as cosine similarity.

<details>
<summary>Common pitfalls and next steps</summary>

- **Don't mix vectors from different models**: they're like two different maps — the coordinates aren't directly comparable.
- **Too-short queries**: one or two words isn't enough meaning, so search results tend to drift.
- **`top_k` isn't "bigger is better"**: pulling in too much content drags noise along with it.
- To compare models, see the [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard), but re-test with your own language and data.

</details>

Next: plug these vectors into [Exercise 2: Vector DB](../02-vector-db/README.en.md) so you don't have to compare against every sentence from scratch each time.

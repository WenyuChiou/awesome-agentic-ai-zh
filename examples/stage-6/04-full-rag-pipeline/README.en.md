<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 4: Wiring Up a Full RAG Pipeline

← Back to [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.en.md#exercise-4-full-rag-pipeline)

**RAG (Retrieval-Augmented Generation)** looks things up first, then has the model answer while looking at what it found. It's like an open-book exam: flip to the right page first, then answer.

## 📌 Learning goals

- Wire up the four steps **chunk → embed → retrieve → generate**.
- Understand **grounding** (answering based on the retrieved data) and `top_k`.
- Test the full pipeline offline with a fake LLM reply.
- Tell apart two failure modes: "retrieved the wrong data" versus "saw the right data but still answered wrong."

## 🔑 Core terms

| Core term | Plain meaning |
|---|---|
| **Retrieval** | Finding the passages that might contain the answer |
| **Generation** | The model reading those passages and composing an answer |
| **Grounding** | The answer must be traceable back to the supplied data |
| **Top-k** | The maximum number of passages handed to the model |

## 📚 Required reading and learning resources

- ★★★★★ [OpenAI Retrieval official guide](https://developers.openai.com/api/docs/guides/retrieval): first-party approach to managed vector stores and search.
- ★★★★★ [LlamaIndex RAG official tutorial](https://docs.llamaindex.ai/en/stable/understanding/rag/): breaks down ingestion, indexing, and querying.
- ★★★★★ [LangChain RAG official tutorial](https://docs.langchain.com/oss/python/langchain/rag): compares two-step RAG against agentic RAG.
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents): a fuller course on RAG pipelines.

<sub>Data verified: 2026-08-30 UTC.</sub>

## ▶️ Path A (Ollama, local and free)

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

The model runs locally, so the API cost is **$0**.

<details markdown="1">
<summary>Path B (Anthropic)</summary>

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = Read-Host "Anthropic API key"
python starter_anthropic.py
```

The default model is `claude-haiku-4-5`. Current standard pricing is **$1** per million input tokens and **$5** per million output tokens; actual cost is computed from token usage:

```text
cost = input tokens ÷ 1,000,000 × 1
     + output tokens ÷ 1,000,000 × 5
```

Check the [official Anthropic pricing page](https://platform.claude.com/docs/en/about-claude/pricing) again before running it, and set a small usage cap.

</details>

**Total Stage 06 budget**: Running all five Path A exercises keeps API fees at **$0** (downloads, disk space, and electricity excluded). Optional cloud paths are billed from actual embedding, input, and output token usage; set a small account cap and stop after one successful run.

## ✅ Full check without hitting the API

```powershell
python test.py
python test_anthropic.py
```

The tests swap out the LLM and the embedding model — no downloads, no charges — but still confirm the context actually made it into the prompt.

## The four steps of RAG

```text
document → 1. chunk → 2. embed/index → 3. retrieve top-k → 4. generate
```

```python
collection = build_kb(doc)
contexts = retrieve(collection, query, top_k=2)
answer = generate(query, contexts)
```

| Step | Main settings | What breaking looks like |
|---|---|---|
| **Chunk** | size, overlap, document structure | correct sentences get split apart |
| **Embed / index** | embedding model, data refresh | new data can't be found |
| **Retrieve** | `top_k`, filters, reranker | wrong or missing passages come back |
| **Generate** | prompt, model, output limits | context is right, but the answer still guesses |

## The minimum grounding rule

```text
Answer only from the provided context.
If the context doesn't have the answer, say clearly that you don't know.
```

This cuts down on made-up answers, but doesn't guarantee zero hallucination. A production system also needs no-answer tests, citations, output validation, and manual spot checks.

<details>
<summary>Common pitfalls and next steps</summary>

- Too small a `top_k` misses data; too large amplifies noise and token cost together.
- Rebuilding the index on every question is wasteful; reuse a persisted collection when the data hasn't changed.
- Testing "it can answer" isn't enough — also test that it refuses when the data has no answer.
- You can add query rewriting, a reranker, citations, and evaluation as you go — change one part at a time.

</details>

Next: swap external documents for things the user has said before, and finish [Exercise 5: Long-term Memory](../05-long-term-memory/README.en.md).

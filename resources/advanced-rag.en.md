# Advanced RAG: find the broken step before adding new techniques

[繁體中文](advanced-rag.md) | [English](advanced-rag.en.md) | [简体中文](advanced-rag.zh-Hans.md)

<!-- freshness: canonical=resources/advanced-rag.md; verified_on=2026-08-30; scope=rag,retrieval,reranking,graph-rag,evaluation,project-status; max_age_days=90 -->

← [Back to Stage 6: RAG and Memory](../stages/06-memory-rag.en.md)

Basic RAG is like “look in a book, then answer.” Advanced RAG does not mean attaching every extra component. First find the step that retrieves the wrong information, then fix only that step.

## 📌 Learning goals

By the end of this page, you can:

1. Tell apart four problems: nothing was found, the ranking is wrong, the evidence is insufficient, or the answer makes things up.
2. Explain which step **Hybrid Search**, **Reranking**, **Query Transformation**, and **GraphRAG** improve.
3. Compare before and after with a small fixed set of questions instead of trusting one impressive answer.
4. Know when to stay with basic RAG and avoid extra cost and complexity.

## 🧩 Eight core terms first

| Core term | Plain-language picture | Precise meaning |
|---|---|---|
| **Baseline** | The score before trying a new move | A rerunnable minimal system and its evaluation results, used to tell whether a change really helps. |
| **Hybrid Search** | Look for both the same words and similar meanings | Combine candidates from BM25/full-text search and vector search. |
| **Reranking** | Reorder the cards you already picked up | Use another model or rule to estimate the relevance between the question and candidate documents again. |
| **Query Transformation** | Ask the question in a few different ways | Rewrite, split, or expand a question to retrieve different candidate documents. |
| **Contextual Retrieval** | Label each card with the chapter it came from | Add document context to each chunk before indexing it, then retrieve. |
| **Corrective/Adaptive RAG** | Change course when search is not working | Check candidate quality first, then retry, change sources, or answer directly. |
| **Agentic RAG** | Let the agent decide when to consult the book | Treat retrieval as a tool and let the agent decide whether, when, and how to call it. |
| **GraphRAG** | Find cards and follow links between people and events | Build a graph of entities and relationships to support cross-document relationships and broad topic questions. |

## 🩺 Start with the symptom, then choose a method

| Problem you see | Measure first | First method to try | Do not do this first |
|---|---|---|---|
| The answer exists in a document but is never retrieved | Recall@k, hit rate | Adjust chunks, metadata filters, or Hybrid Search | Switch to a larger generation model |
| The right document is retrieved but ranks far down | MRR, nDCG, manual inspection of the top k | Reranking | Add a graph and agent loop all at once |
| The question is short, vague, or contains several smaller questions | Hit rate and latency for each rewritten query | Multi-Query, decomposition, or HyDE | Generate an unlimited number of queries |
| You must answer relationships across many documents or a whole corpus | Relationship coverage, a global-question test set | GraphRAG, LightRAG, or a summary tree | Treat a graph as the default for every RAG system |
| Some questions do not need retrieval at all | Unnecessary-retrieval rate, cost, latency | Adaptive/Agentic RAG | Let an agent retry without limits |
| The right evidence is found but the answer is still unsupported | Faithfulness/manual citation checks | Improve the answer prompt, citation format, and abstention rules | Keep tuning retrieval to hide a generation problem |

## 📚 Required reading

Read these in order. They are the main learning path, not hidden in a menu.

1. [LangChain: Retrieval concepts](https://docs.langchain.com/oss/python/deepagents/retrieval) — first distinguish a knowledge base, retriever, and agent.
2. [Anthropic: Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) — see how contextual chunks, BM25, embeddings, and reranking work together.
3. [Qdrant: Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/) — inspect the real query shape for dense, sparse, and fusion search.
4. [Weaviate: Hybrid Search](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search) — use another official implementation to see how keyword and vector scores are combined.
5. [LangGraph: Agentic RAG tutorial](https://docs.langchain.com/oss/python/langgraph/agentic-rag) — after a fixed two-step RAG works, see how an agent decides to retrieve.
6. [Ragas](https://github.com/vibrantlabsai/ragas) — replace “it looks good” with a rerunnable dataset and evaluation loop.

## 🪜 The order from basic to advanced

### 1. Freeze a minimal Baseline first

Prepare 20–50 reviewed questions. For every question, save the expected source and an acceptable answer. Change one thing at a time and record retrieval, answer, latency, and cost. Without a baseline, you cannot tell whether a new technique helps or adds noise.

### 2. Fix Retrieval before Generation

- **Chunking** decides how data is split. Start with headings, paragraphs, and document structure, then test fixed-size, parent-child, or semantic chunking.
- **Hybrid Search** broadens the candidate set: BM25 finds exact terms, while vector search finds semantically similar content.
- **Reranking** cannot create new documents; it only reorders candidates that were already retrieved.

### 3. Use Query Transformation when the question is hard to find

- **Multi-Query**: rewrite one question in several ways, search each version, then merge the results.
- **HyDE**: generate a hypothetical answer first, then use it for search. It can improve recall but may also bias retrieval toward the made-up content.
- **RAG Fusion**: apply rank fusion to results from multiple queries, reducing the impact of one wording choice.
- **Decomposition**: split “compare A and B and explain why” into smaller questions that can each retrieve evidence.

### 4. Consider GraphRAG only when you need cross-document relationships

**Microsoft GraphRAG** is a research reference implementation. Its maintainers currently describe it as largely in maintenance mode: bugs and dependency issues are still addressed, but new features are not the focus. Indexing can be expensive, so begin with a small dataset. **LightRAG** is another active graph-based RAG implementation. Its data model differs from Microsoft GraphRAG’s, so do not treat them as the same product.

GraphRAG fits questions such as “Which people jointly influenced this event?” or “What themes appear across this whole document set?” For a single FAQ or a precise policy lookup, a normal retriever is usually enough.

### 5. Add Corrective or Agentic RAG only when the flow needs judgment

- **Self-RAG**: the model learns when to retrieve and reflects on evidence and answers.
- **CRAG (Corrective RAG)**: judge whether candidates are good enough; if they are not, revise the query or source.
- **Adaptive RAG**: choose different flows based on question difficulty.
- **Agentic RAG**: let an agent decide when to call a retriever; set limits for steps, time, cost, and allowed sources.

Original entry points: [Self-RAG](https://arxiv.org/abs/2310.11511), [CRAG](https://arxiv.org/abs/2401.15884), [Adaptive-RAG](https://arxiv.org/abs/2403.14403).

### 6. Touch summary trees and program optimization last

**RAPTOR** repeatedly clusters and summarizes content into a tree from details to broad themes. Detail questions use leaf nodes; theme questions use higher-level summaries. **DSPy** uses examples and metrics to tune an LLM program; it still needs a clear task, reliable data, and evaluation metrics.

Read: [RAPTOR paper](https://arxiv.org/abs/2401.18059) · [DSPy](https://github.com/stanfordnlp/dspy)

## 🛠 A small rerunnable experiment

1. Choose 20 questions and mark the correct source for each.
2. Run minimal vector retrieval and save the top-five results.
3. Add only BM25 and rerun the same questions.
4. Then add only a reranker and compare top five, latency, and cost.
5. Record which questions improved, which regressed, and why.

**Done when:** you can show three results from the same test set, not just one successful example.

<details markdown="1">
<summary>Cost, data, and pre-production checks</summary>

- Does indexing call a paid model? Estimate one full rebuild with a small sample first.
- Does every chunk retain its source, page/location, version, time, and access permissions?
- Does the retriever apply permissions before querying, rather than hide an answer after it finds it?
- Does an Agentic loop have maximum steps, a timeout, a budget, and an allowlist of safe sources?
- Can a cache keep retrieving an old document? Have update and deletion flows been tested?

</details>

<details markdown="1">
<summary>Common failures and a debugging order</summary>

1. Check whether the correct evidence appears in the top k.
2. If it does, check whether the reranker pushes it down.
3. If the ranking is right, check whether the prompt requires citations and abstention.
4. Inspect the generation model last; do not hide a retrieval error with a larger model.

</details>

## 🎯 Curated projects and learning resources

Ratings represent educational value for this learning map, not a project-quality leaderboard. Choose one framework, one data layer, and one evaluation tool first.

<small>Verified: 2026-08-30 UTC</small>

<table>
  <thead><tr><th scope="col">Category</th><th scope="col">Project/resource</th><th scope="col">Editorial rating</th><th scope="col">Best for</th><th scope="col">What you can learn</th><th scope="col">Status/limits</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Pipelines and examples</th><td><a href="https://github.com/run-llama/llama_index">LlamaIndex</a></td><td>⭐⭐⭐⭐⭐</td><td>Document-application developers</td><td>retrievers, query engines, evaluation</td><td>MIT; start with the official starter because there are many packages</td></tr>
    <tr><td><a href="https://github.com/deepset-ai/haystack">Haystack</a></td><td>⭐⭐⭐⭐</td><td>People exploring modular pipelines</td><td>components, routing, retrieval</td><td>Apache-2.0; begin with a small pipeline</td></tr>
    <tr><td><a href="https://github.com/NirDiamant/RAG_Techniques">RAG_Techniques</a></td><td>⭐⭐⭐⭐⭐</td><td>Readers comparing techniques</td><td>runnable notebooks and technique comparisons</td><td>Community learning material; verify facts against official docs</td></tr>
    <tr><td><a href="https://github.com/infiniflow/ragflow">RAGFlow</a></td><td>⭐⭐⭐⭐</td><td>Teams studying a full product architecture</td><td>parsing, hybrid retrieval, UI</td><td>Apache-2.0; not a first starter</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Search and graphs</th><td><a href="https://github.com/qdrant/qdrant">Qdrant</a></td><td>⭐⭐⭐⭐⭐</td><td>Practicing dense + sparse search</td><td>hybrid queries, fusion, filters</td><td>Apache-2.0; plan service operation and backups</td></tr>
    <tr><td><a href="https://github.com/pgvector/pgvector">pgvector</a></td><td>⭐⭐⭐⭐</td><td>Teams already using PostgreSQL</td><td>SQL, full text, and vectors in one database</td><td>Still needs indexing and query tuning</td></tr>
    <tr><td><a href="https://github.com/microsoft/graphrag">Microsoft GraphRAG</a></td><td>⭐⭐⭐⭐</td><td>Readers researching cross-document relationships</td><td>entity graphs, local/global search</td><td>MIT; maintenance mode and expensive indexing</td></tr>
    <tr><td><a href="https://github.com/HKUDS/LightRAG">LightRAG</a></td><td>⭐⭐⭐⭐</td><td>Readers comparing graph-based RAG</td><td>graph + vector retrieval</td><td>MIT; architecture differs from Microsoft GraphRAG</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Evaluation and optimization</th><td><a href="https://github.com/vibrantlabsai/ragas">Ragas</a></td><td>⭐⭐⭐⭐⭐</td><td>Teams building rerunnable evaluation</td><td>datasets, metrics, experiments</td><td>Apache-2.0; LLM metrics still need human calibration</td></tr>
    <tr><td><a href="https://github.com/truera/trulens">TruLens</a></td><td>⭐⭐⭐⭐</td><td>Teams needing tracing and evaluation</td><td>feedback functions, records, comparisons</td><td>Confirm integration and data-retention practices first</td></tr>
    <tr><td><a href="https://github.com/stanfordnlp/dspy">DSPy</a></td><td>⭐⭐⭐⭐⭐</td><td>Developers with a dataset and metric already</td><td>optimizing LLM programs</td><td>MIT; not a first step for beginner RAG</td></tr>
    <tr><td><a href="https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide">Anthropic Contextual Retrieval cookbook</a></td><td>⭐⭐⭐⭐⭐</td><td>Readers who completed a baseline</td><td>contextual chunks and evaluation</td><td>Vendor example; its numbers apply only to that setup</td></tr>
  </tbody>
</table>

## ✅ Self-check

- [ ] I save a baseline first, then change one component at a time.
- [ ] I can distinguish Hybrid Search from Agentic RAG.
- [ ] I know Reranking cannot retrieve a document that never entered the candidate set.
- [ ] I can name questions GraphRAG fits and cases where I should not use it.
- [ ] My evaluation records quality, latency, cost, and failure cases together.

← [Back to Stage 6: RAG and Memory](../stages/06-memory-rag.en.md)

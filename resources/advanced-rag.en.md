# Advanced RAG: find the broken step before adding new techniques

**RAG** (Retrieval-Augmented Generation): retrieve relevant material, then answer using it.

[繁體中文](advanced-rag.md) | [English](advanced-rag.en.md) | [简体中文](advanced-rag.zh-Hans.md)

<!-- freshness: canonical=resources/advanced-rag.md; verified_on=2026-08-30; scope=rag,retrieval,reranking,graph-rag,evaluation,project-status; max_age_days=90 -->

← [Back to Stage 6: RAG and Memory](../stages/06-memory-rag.en.md)

Basic RAG is like “look in a book, then answer.” Find the failing step before adding more parts.

## 📌 Learning goals

By the end of this page, you can:

1. Tell apart missing results, poor ranking, insufficient evidence, and unsupported answers.
2. Know when to change search, reorder results, rephrase a question, or connect facts across documents.
3. Compare changes with fixed questions, rather than one impressive answer.
4. Know when basic RAG is enough.

## 🧩 Eight core terms first

<div class="reader-core-terms" align="center" role="region" tabindex="0" aria-label="Search core terms" markdown="1">

| Core term | Plain meaning | How we use it here |
|:---|:---|:---|
| **Chunk** | A small piece of a long document | Search for pieces while keeping their sources. |
| **Embedding** | Numbers that represent a text’s meaning | Turn questions and chunks into comparable numbers. |
| **Vector Search** | Find content with a similar meaning | Compare vectors, not just words. |
| **BM25 (keyword ranking method)** | Rank results by word matches | Useful for a product ID such as AB-123; also considers how common terms are and document length. |
| **Retriever** | The part that finds material | Return useful-looking chunks: the “candidates.” |
| **Hybrid Search** | Use two search methods together | Combine BM25 and vector results and remove duplicates. |
| **Reranking** | Reorder the material already found | Recheck each candidate against the question and move more useful ones up. |
| **Baseline** | The score before a change | Save the system and its results for comparison. |

</div>

Question → find candidates → rerank (optional) → answer from evidence. **Retrieval** finds material; **Generation** writes the answer. Fix the failing step.

## 🩺 Start with the symptom, then choose a method

Use a fixed set of questions and mark the relevant material for each one. `k` is how many top results to inspect: `k = 5` means the first five.

- <strong>Recall@k</strong>: the share of all relevant material retrieved in the first k results.
- <strong>Hit rate</strong>: the share of questions with at least one relevant result in the first k results.

For example, a question has four relevant documents. Finding two in the first five gives Recall@5 of 50%; that question also counts as a hit.

Wrong product when searching for AB-123's warranty? If search missed it, try BM25. If it ranks low, try Reranking. If both work, check the answer against the evidence.

<div align="center" markdown="1">

| Problem you see | Measure first | First method to try | Do not do this first |
|:---|:---|:---|:---|
| The document has the answer, but search misses it | Recall@k, hit rate | [Change splitting or combine searches](#rag-search) | Switch to a larger generation model |
| The right material is found but ranks low | Inspect the first k results | [Reorder results](#rag-search) | Add many parts at once |
| The question is vague or asks too much at once | Hit rate and wait time per wording | [Rephrase or split the question](#rag-query) | Generate unlimited queries |
| You need people or events linked across documents | Test a few cross-document questions and check the links | [Try relationship search](#rag-graph) | Build a graph for every system |
| Search runs even when it is unnecessary | Extra searches, cost, and wait time | [Decide whether to search](#rag-decisions) | Retry without limits |
| Evidence is right, but the answer ignores it | Check each claim against its citation | Improve the prompt, citations, and refusal rules | Keep changing search to hide an answer problem |

</div>

**MRR (Mean Reciprocal Rank)** scores how early the first relevant result appears. **nDCG (Normalized Discounted Cumulative Gain)** compares the ranking with an ideal order. **Faithfulness** checks support from evidence, not agreement with all external facts.

## 📚 Required reading

Read these in order.

1. [LangChain: Retrieval concepts](https://docs.langchain.com/oss/python/deepagents/retrieval) — separate storing material, finding it, and deciding the next step.
2. [Anthropic: Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) — add source context to chunks before building the search directory (index).
3. [Qdrant: Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/) — see how two search result sets are combined and reordered.
4. [Weaviate: Hybrid Search](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search) — see another way to combine keyword and vector search.
5. [LangGraph: Agentic RAG (the agent decides when to search)](https://docs.langchain.com/oss/python/langgraph/agentic-rag) — first make “find material → answer” work, then add decisions.
6. [Ragas](https://github.com/vibrantlabsai/ragas) — replace “it looks good” with a rerunnable dataset and evaluation loop.

## 🪜 The order from basic to advanced

### 1. Freeze a minimal Baseline first

Prepare 20–50 human-reviewed questions, each with an expected source and acceptable answer. Record retrieved material, answers, wait time (latency), and cost. Then change one thing at a time.

<a id="rag-search"></a>
### 2. Fix Retrieval before Generation

- **Chunking**: start with headings and paragraphs. Compare fixed-size pieces, finding small pieces and returning their larger section (parent-child), or splitting by meaning (semantic chunking).
- **Metadata Filter**: narrow search using labels such as product, date, or access rights. Check that filters do not exclude the right material.
- **Hybrid Search**: BM25 adds word matching, and vector search adds similar meanings. Test whether combining them finds more relevant material.
- **Reranking** cannot create new documents; it only reorders candidates that were already retrieved.

Docs also mention **dense vectors**, where most positions usually have values, and **sparse vectors**, where most positions are zero. **Fusion** combines search scores or rankings. Density alone does not guarantee search quality.

<a id="rag-query"></a>
### 3. Use Query Transformation when the question is hard to find

**Query Transformation** rephrases a question or splits it into smaller questions before searching. Try one method first.

- **Multi-Query**: rewrite one question in several ways, search each version, then merge the results.
- **HyDE (Hypothetical Document Embeddings)**: write a hypothetical answer, turn it into a vector, then find real material. The draft is not evidence and can lead search astray.
- **RAG Fusion**: combine rankings from several question wordings to reduce dependence on one phrasing.
- **Decomposition**: split “compare A and B and explain why” into smaller questions that can each retrieve evidence.

<a id="rag-graph"></a>
### 4. Consider GraphRAG only when you need cross-document relationships

**GraphRAG** links people, organizations, and other “entities” in a graph to find evidence. For example, connect who joined which project across documents. For a single question-and-answer document or precise policy, try a normal retriever first.

**Microsoft GraphRAG** is a research reference implementation, largely in maintenance mode: bugs and dependencies are fixed; new features are not the focus. Indexing can be costly; start small. **LightRAG** is active but has a different data model. They are separate products.

Test “Which people jointly influenced this event?” or “What themes span these documents?” Check whether better answers justify building the graph.

<a id="rag-decisions"></a>
### 5. Add Corrective or Agentic RAG only when the flow needs judgment

The methods above mostly follow fixed search-and-answer steps. Add the decisions below only when you need to ask “Should I search now?” or “What if search fails?”

- **Self-RAG**: the model learns when to retrieve and reflects on evidence and answers.
- **CRAG** (Corrective Retrieval Augmented Generation, also called Corrective RAG): judge candidate quality; if it is inadequate, revise the query or source.
- **Adaptive RAG**: choose different flows based on question difficulty.
- **Agentic RAG**: let an agent decide when to call a retriever; set limits for steps, time, cost, and allowed sources.

Original entry points: [Self-RAG](https://arxiv.org/abs/2310.11511), [CRAG](https://arxiv.org/abs/2401.15884), [Adaptive-RAG](https://arxiv.org/abs/2403.14403).

### 6. Touch summary trees and program optimization last

**RAPTOR** (Recursive Abstractive Processing for Tree-Organized Retrieval) groups similar chunks, summarizes them, then combines summaries into larger ones. Detail questions use original chunks; theme questions use higher-level summaries.

**DSPy** uses examples and scoring rules to adjust prompts or demonstrations for an LLM (Large Language Model, a model that reads and writes language), improving the workflow. Start with a clear task, reliable data, and evaluation.

Read: [RAPTOR paper](https://arxiv.org/abs/2401.18059) · [DSPy](https://github.com/stanfordnlp/dspy)

## 🛠 A small rerunnable experiment

1. Choose 20 questions and mark the correct source for each.
2. **A: Baseline.** Use vector search alone; save the first five results and the answer.
3. **B: Hybrid search.** Keep A, add only BM25 and merge the results, then rerun the same questions.
4. **C: Add reranking.** Keep B, add only reranking, then rerun the same questions.
5. Record Recall@5, hit rate, latency, and cost for all three runs. Keep other settings fixed and note which questions improve or regress.

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

<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="Selected projects and learning resources">
<table align="center">
  <thead><tr><th scope="col">Group</th><th scope="col">Project / document</th><th scope="col">Rating</th><th scope="col">Use</th><th scope="col">Limits</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">Workflows and examples</th><td><div data-field="entry"><strong><a href="https://github.com/run-llama/llama_index">LlamaIndex</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>Best for:</strong> Document-application developers</div><div data-field="learn"><strong>What you can learn:</strong> find material, build answers, evaluate</div></td><td><div data-field="status"><strong>Status/limits:</strong> MIT; start with the official starter because there are many packages</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/deepset-ai/haystack">Haystack</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>Best for:</strong> People splitting workflows into parts</div><div data-field="learn"><strong>What you can learn:</strong> parts, path selection, search</div></td><td><div data-field="status"><strong>Status/limits:</strong> Apache-2.0; begin with a small workflow</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/NirDiamant/RAG_Techniques">RAG_Techniques</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>Best for:</strong> Readers comparing techniques</div><div data-field="learn"><strong>What you can learn:</strong> runnable notebooks and technique comparisons</div></td><td><div data-field="status"><strong>Status/limits:</strong> Custom non-commercial license; commercial use needs written permission; check official docs</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/infiniflow/ragflow">RAGFlow</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>Best for:</strong> Teams studying a full product architecture</div><div data-field="learn"><strong>What you can learn:</strong> read documents, combine searches, show results</div></td><td><div data-field="status"><strong>Status/limits:</strong> Apache-2.0; not a first starter</div></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">Search and graphs</th><td><div data-field="entry"><strong><a href="https://github.com/qdrant/qdrant">Qdrant</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>Best for:</strong> Combining dense and sparse vector search</div><div data-field="learn"><strong>What you can learn:</strong> combine results and filter material</div></td><td><div data-field="status"><strong>Status/limits:</strong> Apache-2.0; plan service operation and backups</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/pgvector/pgvector">pgvector</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>Best for:</strong> Teams already using PostgreSQL</div><div data-field="learn"><strong>What you can learn:</strong> text and vector search in one database</div></td><td><div data-field="status"><strong>Status/limits:</strong> Still needs indexing and query tuning</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/microsoft/graphrag">Microsoft GraphRAG</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>Best for:</strong> Readers researching cross-document relationships</div><div data-field="learn"><strong>What you can learn:</strong> entities, relationships, local and broad search</div></td><td><div data-field="status"><strong>Status/limits:</strong> MIT; maintenance mode and expensive indexing</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/HKUDS/LightRAG">LightRAG</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>Best for:</strong> Readers comparing relationship-based search</div><div data-field="learn"><strong>What you can learn:</strong> graph and vector search</div></td><td><div data-field="status"><strong>Status/limits:</strong> MIT; architecture differs from Microsoft GraphRAG</div></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">Evaluation and optimization</th><td><div data-field="entry"><strong><a href="https://github.com/vibrantlabsai/ragas">Ragas</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>Best for:</strong> Teams building rerunnable evaluation</div><div data-field="learn"><strong>What you can learn:</strong> test data, scoring, experiments</div></td><td><div data-field="status"><strong>Status/limits:</strong> Apache-2.0; model scoring still needs human calibration</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/truera/trulens">TruLens</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>Best for:</strong> Teams inspecting runs and evaluating results</div><div data-field="learn"><strong>What you can learn:</strong> custom scoring, records, comparisons</div></td><td><div data-field="status"><strong>Status/limits:</strong> Confirm integration and data-retention practices first</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/stanfordnlp/dspy">DSPy</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>Best for:</strong> Developers with test data and scoring rules</div><div data-field="learn"><strong>What you can learn:</strong> improving model workflows</div></td><td><div data-field="status"><strong>Status/limits:</strong> MIT; not a first step for beginner RAG</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide">Anthropic Contextual Retrieval cookbook</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>Best for:</strong> Readers who completed a baseline</div><div data-field="learn"><strong>What you can learn:</strong> add context to chunks and evaluate</div></td><td><div data-field="status"><strong>Status/limits:</strong> Vendor example; its numbers apply only to that setup</div></td></tr>
  </tbody>
</table>
</div>

## ✅ Self-check

- [ ] I save a baseline first, then change one component at a time.
- [ ] I can distinguish Hybrid Search from Agentic RAG.
- [ ] I know Reranking cannot retrieve a document that never entered the candidate set.
- [ ] I can name questions GraphRAG fits and cases where I should not use it.
- [ ] My evaluation records quality, latency, cost, and failure cases together.

← [Back to Stage 6: RAG and Memory](../stages/06-memory-rag.en.md)

<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 3: Comparing Three Chunking Methods

← Back to [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.en.md#exercise-3-chunking-comparison)

**Chunking** means cutting a long document into a few small boxes. Boxes that are too big bury the detail; boxes that are too small cut the meaning in half.

## 📌 Learning goals

- Name the three cutting methods: **fixed-length**, **paragraph-based**, and **heading-aware**.
- Know that **chunk size** and **overlap** change search results.
- Fairly compare all three strategies on the same document and the same set of questions.
- Block a bad `overlap` value that would hang the program.

## 🔑 Core terms

| Core term | Plain meaning |
|---|---|
| **Chunk** | A small piece cut out of a long document |
| **Chunk size** | The maximum size of each piece |
| **Overlap** | Text repeated between two adjacent chunks, so a sentence doesn't get cut right in half |
| **Retrieval** | Using a question to pull back the most useful passages |

## 📚 Required reading and learning resources

- ★★★★★ [LangChain text splitters official concepts page](https://docs.langchain.com/oss/python/integrations/splitters): start with the simple cutting methods.
- ★★★★★ [LlamaIndex Semantic Splitter official API](https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/semantic_splitter/): go deeper once you need semantic breakpoints.
- ★★★★☆ [Unstructured official docs](https://docs.unstructured.io/): an entry point for parsing complex formats like PDF, DOCX, and HTML.
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents): a fuller course on RAG chunking.

<sub>Data verified: 2026-08-30 UTC.</sub>

## ▶️ Run Path A first (local, provider-independent, free)

```powershell
pip install -r requirements.txt
python starter.py
```

The first run may download a local embedding model; the API cost is **$0**.

<details markdown="1">
<summary>Path B (preview: how this step feeds into Claude later)</summary>

The chunking step only decides how to split a document — it doesn't care which model generates the final answer later. Running `starter_anthropic.py` here just shows you the same chunking code that will plug in, unchanged, right before the Claude generation step in [Exercise 4](../04-full-rag-pipeline/README.en.md). This step makes no API call, so the cost is **$0**.

```powershell
python starter_anthropic.py
```

</details>

**Total Stage 06 budget**: Running all five Path A exercises keeps API fees at **$0** (downloads, disk space, and electricity excluded). Optional cloud paths are billed from actual embedding, input, and output token usage; set a small account cap and stop after one successful run.

```powershell
python test.py
python test_anthropic.py
```

The tests only check the chunking logic — no model download.

## Three cutting methods

| Strategy | How it cuts | Good for |
|---|---|---|
| **Fixed-length** | Cuts every N characters | Logs or chat transcripts with no clear format |
| **Paragraph-based** | Cuts on blank lines | Articles with tidy paragraphs |
| **Heading-aware** | Cuts on `#`, `##` headings | READMEs, wikis, specs |

```python
fixed = chunk_fixed(text, chunk_size=200, overlap=40)
paragraphs = chunk_paragraphs(text)
headings = chunk_headings(text)
```

`overlap` must satisfy:

```text
0 <= overlap < chunk_size
```

If `overlap` is equal to or greater than `chunk_size`, the next chunk never moves forward. The program now raises `ValueError` right away instead of letting it become an infinite loop.

## How to judge which is better

Don't just count chunks, and don't judge from one pretty example. Prepare real questions and check whether the passage holding the correct answer actually made it into the top-k.

| What to check | Ask yourself |
|---|---|
| **Recall** | Was the correct passage retrieved at all? |
| **Precision** | Of what was retrieved, how much is actually useful? |
| **Completeness** | Did the sentences the answer needs get split across two chunks? |
| **Cost** | How much do embedding and storage grow as chunks multiply? |

<details>
<summary>Common pitfalls and advanced practice</summary>

- Chunks too big: too many topics crammed into one piece, so the vector gets blurry.
- Chunks too small: the context an answer needs may end up scattered across different pieces.
- A PDF isn't plain text: handle columns, tables, headers, and footers before chunking.
- Don't hard-cut CJK text by byte count; use Python strings, a tokenizer, or a structured parser.
- Advanced approach: cut into large sections by heading first, then cut those sections into smaller fixed-length pieces.

</details>

Next: connect chunking, embedding, search, and answering into [Exercise 4: Full RAG](../04-full-rag-pipeline/README.en.md).

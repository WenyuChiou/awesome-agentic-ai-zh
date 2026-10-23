# Agent Memory: save only what is useful, permitted, and removable

[繁體中文](agent-memory.md) | [English](agent-memory.en.md) | [简体中文](agent-memory.zh-Hans.md)

<!-- freshness: canonical=resources/agent-memory.md; verified_on=2026-08-30; scope=memory,privacy,retention,isolation,project-status; max_age_days=90 -->

← [Back to Stage 6: RAG and Memory](../stages/06-memory-rag.en.md)

**Agent Memory** is like a notebook with management rules. It is not a secret archive of every chat. It stores only information needed later, permitted by the user, and available to view, change, and delete.

## 📌 Learning goals

By the end of this page, you can:

1. Distinguish chat history, context, RAG, and Memory.
2. Distinguish short-term from long-term memory, and semantic, episodic, and procedural memory.
3. Draw a memory’s lifecycle from writing and search through update and deletion.
4. Set an owner, source, retention period, and deletion method for every memory.
5. Use fixed tests to check that needed memories are found and unneeded ones do not remain.

## 🧩 Separate these four things first

| Core term | Plain-language picture | Precise meaning |
|---|---|---|
| **Chat History** | A transcript of this conversation | A message record; it does not mean every message should be saved permanently or placed in the model context. |
| **Context** | The material on the desk right now | The instructions, messages, tool results, and retrieved content the model actually sees for this call. |
| **RAG** | Go to the bookshelf when there is a question | Retrieve evidence from an external knowledge source, then give it to the model to answer. |
| **Memory** | A short note the assistant leaves for next time | State that must be read again across steps, threads, or sessions, with rules for writing and governance. |

**The key decision:** put product manuals in a knowledge base; put the current task’s progress in short-term state; only preferences saved with user consent may become long-term memory.

## 📚 Required reading

1. [LangChain: Memory overview](https://docs.langchain.com/oss/python/concepts/memory) — understand thread-scoped short-term memory, cross-session long-term memory, and semantic, episodic, and procedural types.
2. [LangGraph: Add and manage memory](https://docs.langchain.com/oss/python/langgraph/add-memory) — see the implementation boundaries of a checkpointer, store, namespace, and semantic search.
3. [CoALA paper](https://arxiv.org/abs/2309.02427) — use one shared framework to understand memory structures and operations for language agents.
4. [Generative Agents paper](https://arxiv.org/abs/2304.03442) — study the classic design for recency, importance, relevance, and reflection.
5. [Mem0](https://github.com/mem0ai/mem0) or [Letta Code](https://github.com/letta-ai/letta-code) — choose one current implementation and observe how it stores and retrieves state. The [Letta project entry](https://github.com/letta-ai/letta) is now a landing page; current source and the App Server live in Letta Code.

## ⏱ Two time ranges

- **Short-term Memory** serves one thread or current task, such as messages, uploaded files, tool results, and task progress. LangGraph commonly keeps it in thread-scoped state through a checkpointer.
- **Long-term Memory** is needed across threads or sessions, such as user-approved preferences, project facts, or reusable experience. It must isolate users and applications with namespaces.

Short-term does not mean “only in RAM,” and long-term does not mean “never delete.” The difference is retrieval scope and lifecycle, not the name of a storage device.

## 🧠 Three content types

| Type | What it stores | Example | Risk |
|---|---|---|---|
| **Semantic Memory** | Relatively stable facts | The user prefers short answers; the project uses Python 3.13 | Facts can expire or conflict |
| **Episodic Memory** | Events and outcomes | Where the last deployment failed and which fix worked | One success does not mean it will always work |
| **Procedural Memory** | Rules and steps for doing work | Which gates to run before a release | Malicious content can poison future behavior |

**Semantic memory** and **semantic search** are not the same thing: the first is a type of stored content; the second is a retrieval method based on similar meaning.

## 🔄 A Memory lifecycle

1. **Propose a write:** decide whether it really needs to be used across sessions.
2. **Get consent:** for sensitive data or personal preferences, tell the user why it will be saved.
3. **Normalize:** save a short fact rather than treating a whole conversation as memory.
4. **Add metadata:** at minimum, owner, source, created_at, updated_at, expires_at, and sensitivity.
5. **Store in isolation:** separate user/workspace/agent namespaces and apply permissions before search.
6. **Search and use:** retrieve only a small set relevant to the current task and retain the source.
7. **Update or resolve conflicts:** new information must not quietly coexist with old information; mark versions or replacement relationships.
8. **Delete and forget:** users can view, change, and delete; expired data is cleared automatically, and backups need a handling policy too.

## 🧱 Choose the simplest design first

| Problem | Start with | Upgrade when |
|---|---|---|
| Fixed fields such as language, time zone, or notification preference | **A direct state table** | Field types grow or fuzzy search is needed |
| Freer content such as short summaries or reusable experience | **Searchable text memory** | Relationships, time, and conflicts become the main problem |
| People, events, and relationships change over time | **Temporal Knowledge Graph** | Tests show an ordinary table/search is insufficient |
| You only need to restore one workflow | **Checkpoint/thread state** | You truly need sharing across threads |

**Start with a data table.** Content that fits clear fields does not need vector search first; a problem that short-term state solves does not need permanent memory.

## 🛡️ Memory safety floor

- Do not save passwords, API keys, payment details, medical secrets, or unconsented personal data by default.
- Do not let users, tenants, workspaces, or agents share an unisolated namespace.
- Check permissions before retrieval; do not fetch a secret first and then prompt the model not to reveal it.
- Memory content is untrusted input. Validate schema, source, and prompt-injection risks before writing.
- Every memory must answer who wrote it, where it came from, when it changed, and when it will be deleted.
- Deletion must cover primary storage, search indexes, caches, and policy-managed backups.

## 🛠 A minimal Memory exercise

Save one non-sensitive preference only, such as “give the short version first.”

1. Write the preference with `user_id`, source, time, and retention period.
2. Search and read it from another thread.
3. Change it to “show a table first” and confirm the old value is no longer used.
4. Delete it, then search again; the result must be empty.
5. Query with a different `user_id`; it must not see the first user’s content.

**Done when:** tests for add, search, update, delete, and user isolation all pass. `add` alone is not enough.

<details markdown="1">
<summary>Hot path, background writes, and conflicts</summary>

- **Hot-path write:** write immediately before answering. The result is current, but latency increases and errors affect the user directly.
- **Background write:** organize asynchronously after a reply. Interaction is faster, but you must handle failure, retries, and late updates.
- When one fact has newer and older versions, save time, source, and valid scope; do not randomly select one based only on vector similarity.
- Put “memory suggested by the model” in a review area first, then let rules or a user approve it; this suits high-risk content.

</details>

<details markdown="1">
<summary>Common failures and a debugging order</summary>

1. Nothing found: check the namespace, permission, filter, and whether storage succeeded.
2. Old data found: check whether updates left conflicting versions and whether the cache refreshed.
3. Too much stored: raise the write threshold and shorten retention; do not only expand the context window.
4. Wrong memory: retain source and confidence, let users correct it, and never treat model inference as fact.
5. Incomplete deletion: trace deletion through the primary store, index, cache, event stream, and backups.

**TencentDB reading note (this entry checked: 2026-10-16 UTC):** Chat Memory extracts facts and experience; Skill stores reusable procedures; LLM-Wiki organizes documents; CodeGraph indexes code relationships. Wiki and CodeGraph are knowledge-retrieval assets, not necessarily personal memory. Complete the minimal exercise first. <a href="https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/e9a82935b52741e0c798c75326e90b7144eb4d5f/README.md">Reviewed README</a> / <a href="https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/e9a82935b52741e0c798c75326e90b7144eb4d5f/LICENSE">MIT license</a>.

</details>

## 🎯 Curated projects and learning resources

Ratings represent educational value for this learning map, not a project-quality leaderboard. Choose a memory shape first, then a tool.

<small>Existing entries verified: 2026-08-30 UTC; new entries verified: 2026-10-15 UTC</small>

Local or self-hosted does not mean zero model or storage cost.
When evaluating a memory tool, test update and deletion, not only write and search.
Also test user/workspace isolation and whether malicious content can poison future behavior.

<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="Selected projects and learning resources">
<table>
  <thead><tr><th scope="col">Category</th><th scope="col">Resource, use and limits</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="8">Memory layer</th><td><p data-field="entry"><strong><a href="https://github.com/mem0ai/mem0">Mem0</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> First cross-session memory</p><p data-field="learn"><strong>What you can learn:</strong> library, server, cloud, and search lifecycle</p><p data-field="status"><strong>Status/limits:</strong> Apache-2.0; distinguish OSS from managed capabilities</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://github.com/langchain-ai/langmem">LangMem</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> Teams already using LangGraph</p><p data-field="learn"><strong>What you can learn:</strong> hot-path/background memory</p><p data-field="status"><strong>Status/limits:</strong> MIT; understand the LangGraph store first</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://github.com/letta-ai/letta">Letta project entry</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> Understanding the Letta product boundary first</p><p data-field="learn"><strong>What you can learn:</strong> current installation, docs, and source locations</p><p data-field="status"><strong>Status/limits:</strong> Landing page; the retired V1 server remains only on the archive branch</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://github.com/letta-ai/letta-code">Letta Code</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> Building a stateful agent or App Server</p><p data-field="learn"><strong>What you can learn:</strong> agent harness, git-backed MemFS, persistent identity</p><p data-field="status"><strong>Status/limits:</strong> Current source; a product-oriented harness, not a general memory database</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://github.com/vshulcz/deja-vu">deja-vu</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> Using the memory that already exists on disk</p><p data-field="learn"><strong>What you can learn:</strong> episodic memory built from coding-agent session files; lexical (BM25) retrieval with no embeddings by default, plus optional semantic recall through <code>deja embed</code></p><p data-field="status"><strong>Status/limits:</strong> MIT; local by default. A configured remote embedding endpoint receives the indexed text, with credentials already redacted; a local Ollama or LM Studio keeps it on the machine</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://github.com/vectorize-io/hindsight">Hindsight</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> Readers comparing explicit memory operations</p><p data-field="learn"><strong>What you can learn:</strong> <code>retain</code>/<code>recall</code>/<code>reflect</code>: store, retrieve, and reason over memories to answer</p><p data-field="status"><strong>Status/limits:</strong> MIT; do not treat vendor benchmarks as your own quality evidence</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://github.com/volcengine/OpenViking">OpenViking</a></strong> <span data-field="rating">⭐⭐⭐ (advanced)</span></p><p data-field="audience"><strong>Best for:</strong> Teams organizing large agent contexts</p><p data-field="learn"><strong>What you can learn:</strong> Filesystem-like organization for resources, memories, and skills</p><p data-field="status"><strong>Status/limits:</strong> Main project: AGPL-3.0. CLI/examples are separately licensed. The README adds rewriting language.</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://github.com/TencentCloud/TencentDB-Agent-Memory">TencentDB Agent Memory</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> Memory-governance readers</p><p data-field="learn"><strong>What you can learn:</strong> Chat Memory, Skill, LLM-Wiki, CodeGraph; owners, versions, visibility, agent bindings</p><p data-field="status"><strong>Status/limits:</strong> MIT; SQLite by default; extraction uses a model endpoint. Check network and data access</p></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">Time and relationships</th><td><p data-field="entry"><strong><a href="https://github.com/getzep/graphiti">Graphiti</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> Applications whose relationships change over time</p><p data-field="learn"><strong>What you can learn:</strong> bi-temporal facts, temporal graphs</p><p data-field="status"><strong>Status/limits:</strong> Apache-2.0; requires a graph database and governance</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://github.com/getzep/zep">Zep examples</a></strong> <span data-field="rating">⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> Teams evaluating Zep Cloud</p><p data-field="learn"><strong>What you can learn:</strong> integration and examples entry point</p><p data-field="status"><strong>Status/limits:</strong> The former Community Edition is legacy/deprecated</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://docs.langchain.com/oss/python/concepts/memory">LangChain Memory overview</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> Readers learning concepts first</p><p data-field="learn"><strong>What you can learn:</strong> thread state, stores, three memory types</p><p data-field="status"><strong>Status/limits:</strong> Framework docs; concepts transfer, APIs are version-specific</p></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Research and evaluation</th><td><p data-field="entry"><strong><a href="https://arxiv.org/abs/2309.02427">CoALA</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> Researching agent-memory architecture</p><p data-field="learn"><strong>What you can learn:</strong> working, episodic, semantic, procedural memory</p><p data-field="status"><strong>Status/limits:</strong> An analytical framework, not an installable product</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://arxiv.org/abs/2304.03442">Generative Agents</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> Researching reflection and memory retrieval</p><p data-field="learn"><strong>What you can learn:</strong> recency, importance, relevance</p><p data-field="status"><strong>Status/limits:</strong> Classic research, not a production standard answer</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://arxiv.org/abs/2303.11366">Reflexion</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> Readers researching feedback from experience</p><p data-field="learn"><strong>What you can learn:</strong> verbal feedback and the next attempt</p><p data-field="status"><strong>Status/limits:</strong> Reflection becomes cross-session memory only after durable storage</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://github.com/mem0ai/memory-benchmarks">Mem0 Memory Benchmarks</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="audience"><strong>Best for:</strong> Developers testing memory quality</p><p data-field="learn"><strong>What you can learn:</strong> datasets and a rerunnable evaluation entry point</p><p data-field="status"><strong>Status/limits:</strong> Vendor-maintained; add your own isolation/deletion tests</p></td></tr>
  </tbody>
</table>
</div>

Self-hosting does not guarantee offline use: extraction/Proxy use configured models; Tencent Cloud is optional. The Docker example disables Gateway Bearer auth; some read-only Knowledge routes need no service key. Avoid untrusted networks; check consent, providers, and retention/deletion before imports. <a href="https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/e9a82935b52741e0c798c75326e90b7144eb4d5f/deploy/global-images/.env.example">deployment configuration</a> / <a href="https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/e9a82935b52741e0c798c75326e90b7144eb4d5f/MemoryKnowledge/src/middleware/auth.ts">service authentication boundaries</a>. Docs/config reviewed; performance and isolation untested.

Read OpenViking's <a href="https://github.com/volcengine/OpenViking/blob/main/LICENSE">LICENSE</a> before integration.

## ✅ Self-check

- [ ] I do not treat Chat History, Context, RAG, and Memory as the same thing.
- [ ] Every long-term memory has an owner, source, time, and deletion method.
- [ ] I can explain the difference between semantic memory and semantic search.
- [ ] I have tested updates, deletion, expiry, and cross-user isolation, not only writing and search.
- [ ] Sensitive data is not written by default, and users can see and control what is saved.

← [Back to Stage 6: RAG and Memory](../stages/06-memory-rag.en.md)

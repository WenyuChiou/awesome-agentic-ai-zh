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

</details>

## 🎯 Curated projects and learning resources

Ratings represent educational value for this learning map, not a project-quality leaderboard. Choose a memory shape first, then a tool.

<small>Verified: 2026-08-30 UTC</small>

<table>
  <thead><tr><th scope="col">Category</th><th scope="col">Project/resource</th><th scope="col">Editorial rating</th><th scope="col">Best for</th><th scope="col">What you can learn</th><th scope="col">Status/limits</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Memory layer</th><td><a href="https://github.com/mem0ai/mem0">Mem0</a></td><td>⭐⭐⭐⭐⭐</td><td>First cross-session memory</td><td>library, server, cloud, and search lifecycle</td><td>Apache-2.0; distinguish OSS from managed capabilities</td></tr>
    <tr><td><a href="https://github.com/langchain-ai/langmem">LangMem</a></td><td>⭐⭐⭐⭐</td><td>Teams already using LangGraph</td><td>hot-path/background memory</td><td>MIT; understand the LangGraph store first</td></tr>
    <tr><td><a href="https://github.com/letta-ai/letta">Letta project entry</a></td><td>⭐⭐⭐⭐</td><td>Understanding the Letta product boundary first</td><td>current installation, docs, and source locations</td><td>Landing page; the retired V1 server remains only on the archive branch</td></tr>
    <tr><td><a href="https://github.com/letta-ai/letta-code">Letta Code</a></td><td>⭐⭐⭐⭐</td><td>Building a stateful agent or App Server</td><td>agent harness, git-backed MemFS, persistent identity</td><td>Current source; a product-oriented harness, not a general memory database</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">Time and relationships</th><td><a href="https://github.com/getzep/graphiti">Graphiti</a></td><td>⭐⭐⭐⭐⭐</td><td>Applications whose relationships change over time</td><td>bi-temporal facts, temporal graphs</td><td>Apache-2.0; requires a graph database and governance</td></tr>
    <tr><td><a href="https://github.com/getzep/zep">Zep examples</a></td><td>⭐⭐⭐</td><td>Teams evaluating Zep Cloud</td><td>integration and examples entry point</td><td>The former Community Edition is legacy/deprecated</td></tr>
    <tr><td><a href="https://docs.langchain.com/oss/python/concepts/memory">LangChain Memory overview</a></td><td>⭐⭐⭐⭐⭐</td><td>Readers learning concepts first</td><td>thread state, stores, three memory types</td><td>Framework docs; concepts transfer, APIs are version-specific</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Research and evaluation</th><td><a href="https://arxiv.org/abs/2309.02427">CoALA</a></td><td>⭐⭐⭐⭐⭐</td><td>Researching agent-memory architecture</td><td>working, episodic, semantic, procedural memory</td><td>An analytical framework, not an installable product</td></tr>
    <tr><td><a href="https://arxiv.org/abs/2304.03442">Generative Agents</a></td><td>⭐⭐⭐⭐⭐</td><td>Researching reflection and memory retrieval</td><td>recency, importance, relevance</td><td>Classic research, not a production standard answer</td></tr>
    <tr><td><a href="https://arxiv.org/abs/2303.11366">Reflexion</a></td><td>⭐⭐⭐⭐</td><td>Readers researching feedback from experience</td><td>verbal feedback and the next attempt</td><td>Reflection becomes cross-session memory only after durable storage</td></tr>
    <tr><td><a href="https://github.com/mem0ai/memory-benchmarks">Mem0 Memory Benchmarks</a></td><td>⭐⭐⭐⭐</td><td>Developers testing memory quality</td><td>datasets and a rerunnable evaluation entry point</td><td>Vendor-maintained; add your own isolation/deletion tests</td></tr>
  </tbody>
</table>

## ✅ Self-check

- [ ] I do not treat Chat History, Context, RAG, and Memory as the same thing.
- [ ] Every long-term memory has an owner, source, time, and deletion method.
- [ ] I can explain the difference between semantic memory and semantic search.
- [ ] I have tested updates, deletion, expiry, and cross-user isolation, not only writing and search.
- [ ] Sensitive data is not written by default, and users can see and control what is saved.

← [Back to Stage 6: RAG and Memory](../stages/06-memory-rag.en.md)

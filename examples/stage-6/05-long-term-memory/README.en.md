<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 5: Making an Agent Remember Next Time

← Back to [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.en.md#exercise-5-long-term-memory)

Ordinary chat history is like writing on a whiteboard: close the program, and the whiteboard may well get erased. **Long-term memory** writes what's worth keeping to disk, so it can be found again next time you open the program.

## 📌 Learning goals

- Tell apart **chat history**, **working memory**, and **long-term memory**.
- Write one user fact into a Chroma `PersistentClient`.
- Recover a memory after reopening the same database.
- Put relevant memories into the system prompt instead of stuffing in the entire history.

## 🔑 Core terms

| Core term | Plain meaning |
|---|---|
| **Working memory** | The small amount of information actively in use for the current task |
| **Long-term memory** | Information that survives across restarts or across sessions |
| **Recall** | Using the current question to find related memories |
| **Memory policy** | The rules for what can be remembered, updated, forgotten, and who can read it |

## 📚 Required reading and learning resources

- ★★★★★ [Chroma `PersistentClient` official docs](https://docs.trychroma.com/reference/python/client): the basis for actually persisting to disk in this exercise.
- ★★★★★ [LangGraph Memory official concepts page](https://docs.langchain.com/oss/python/concepts/memory): tells thread and cross-thread memory apart.
- ★★★★☆ [Mem0](https://github.com/mem0ai/mem0): a mature project for fact extraction, updates, and deletion.
- ★★★★☆ [Letta Code](https://github.com/letta-ai/letta-code): the current implementation of stateful agents with working and archival memory.
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents): a fuller course on agent memory.

<sub>Data verified: 2026-08-30 UTC.</sub>

## ▶️ Path A (Ollama, local and free)

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

The program stores its Chroma data under `.stage06-memory`. On the next run, memories written earlier are still there. The API cost is **$0**.

<details markdown="1">
<summary>Path B (Anthropic)</summary>

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = Read-Host "Anthropic API key"
python starter_anthropic.py
```

`claude-haiku-4-5` is billed by token, at **$1** per million input tokens and **$5** per million output tokens. Check the [official Anthropic pricing page](https://platform.claude.com/docs/en/about-claude/pricing) before running it and set a small usage cap.

</details>

**Total Stage 06 budget**: Running all five Path A exercises keeps API fees at **$0** (downloads, disk space, and electricity excluded). Optional cloud paths are billed from actual embedding, input, and output token usage; set a small account cap and stop after one successful run.

## ✅ Check without writing to the project folder or calling an API

```powershell
python test.py
python test_anthropic.py
```

Most tests inject a small in-memory store and a fake LLM. The persistence check creates a real `PersistentClient` in the system temporary directory, lets two fresh Python processes write and read it, then removes it automatically.

## Memory flow

```text
user says something
  → decide whether it's worth remembering
  → remember() writes it to disk
  → next question calls recall() first
  → only the relevant memories go into the prompt
```

```python
memory = MemoryStore(path=".stage06-memory")
memory.remember("User prefers Python.")
recalled = memory.recall("Which language should I learn?")
```

## Chat history and long-term memory aren't the same thing

| Comparison | Chat history | Long-term memory |
|---|---|---|
| Purpose | Keeps the current conversation coherent | Remembers important facts next time |
| Where it lives | The current messages | Disk or an external database |
| How it's read | Recent turns go straight into the prompt | Search first, then pull in a small relevant slice |
| Risk | The prompt grows too long | Remembering the wrong person, stale data, incomplete deletion |

This exercise uses simple rules to catch sentences like "I am", "I like", "I prefer" — just enough to see the flow. A production system needs a clear **memory policy**: user consent, per-user-ID isolation, updates, deletion, retention limits, and auditing.

<details>
<summary>Common pitfalls and next steps for production</summary>

- Don't store every sentence; decide first whether it's genuinely worth keeping long-term.
- When the same fact shows up again, dedupe or update it instead of piling up new entries.
- When a user moves or changes a preference, let the new memory replace the old one.
- Every user needs their own isolated namespace — no cross-user visibility.
- When a user asks for deletion, you need to find every copy and actually delete it.
- For a full lifecycle, evaluate Mem0, Letta, or LangGraph persistence.

</details>

Once you're done, go back to [Stage 6](../../../stages/06-memory-rag.en.md) for the success check, then move on to Stage 7.

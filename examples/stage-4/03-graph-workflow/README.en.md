<div align="right">
  <a href="./README.md">Traditional Chinese</a> | <a href="./README.zh-Hans.md">Simplified Chinese</a> | <strong>English</strong>
</div>

# Exercise 3: Graph Workflow (LangGraph conditional branching + HITL)

Pairs with [Stage 4 — Agent Frameworks](../../../stages/04-agent-frameworks.en.md) Exercise 3.
> 🎓 **How to use this**: `starter.py` is the **complete solution**, not a TODO skeleton. The active approach works better — `mv starter.py starter_reference.py`, read the signatures but not the bodies, write your own `starter.py` from scratch, then run `python test.py` to check it; if you are stuck for 20 minutes, go back and compare against the reference. Full methodology in [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md).

> 📚 **Want the chapter-length version?** The starter in this folder is an illustrative build focused on the core pattern plus two SDK paths — it is not in-depth teaching material. Recommended for depth:
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ the most complete Chinese-language course out there — chapter by chapter, plus 16 production capabilities. **This exercise maps to hello-agents' graph workflow + HITL chapter**
> - [LangGraph interrupts (human-in-the-loop)](https://docs.langchain.com/oss/python/langgraph/interrupts) + [LangGraph time-travel docs](https://docs.langchain.com/oss/python/langgraph/use-time-travel)
> - Full references in [Stage 4 Curated Projects](../../../stages/04-agent-frameworks.en.md#-curated-projects)


## Task

`classify → [search?] → respond → [HITL] → final`

- **`classify_node`**: decides `needs_search` from the query
- **Conditional branch**: `needs_search=True` → `search`, otherwise `respond`
- **HITL checkpoint**: `review_node` calls `interrupt()` and waits for a human answer
- **`final_node`**: `approved=True` → PUBLISHED, else REJECTED

This exercise uses **graph state**, a **checkpoint**, `interrupt()`, and `Command(resume=...)`. You can see where the graph pauses and how it resumes from the same `thread_id`.

## How to run — two paths

> ⚠️ **Give each exercise its own Python 3.11 `.venv`.** Do not mix the five Stage 4 `requirements.txt` files.

### Path A (Ollama, local)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
.\.venv\Scripts\python.exe starter.py
```

Budget: the model API costs **$0**. Local hardware, electricity, and downloads still cost resources. This starter really asks Ollama to write the draft; the other nodes use predictable Python logic.

### Path B (Anthropic, compare a cloud result)

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py
```

Pinned default: `claude-haiku-4-5-20251001`. A request with 2,000 input + 1,000 output tokens costs `2,000 / 1,000,000 × $1 + 1,000 / 1,000,000 × $5 = $0.007`. A retry may add another call, so set a provider spend limit of **$0.05**.

<details markdown="1">
<summary>macOS/Linux commands and verification information</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
./.venv/bin/python test.py
```

Official sources: [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>Packages, model IDs, prices, and official links verified: 2026-08-28 UTC.</small>
</details>

## Validate the logic without spending money

```powershell
.\.venv\Scripts\python.exe test.py # branch, interrupt, and resume behavior
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic setup + shared graph behavior
```

## LangGraph structure (condensed)

```python
g = StateGraph(State)
g.add_node("classify", classify_node)
g.add_node("search", search_node)
g.add_node("respond", respond_node)
g.add_node("review", review_node)
g.add_node("final", final_node)

g.add_edge(START, "classify")
g.add_conditional_edges("classify", should_search, {"search": "search", "respond": "respond"})
g.add_edge("search", "respond")
g.add_edge("respond", "review")
g.add_edge("review", "final")
g.add_edge("final", END)

graph = g.compile(checkpointer=InMemorySaver())
```

## How HITL works

```python
# Phase 1: review_node calls interrupt(); the graph checkpoints and pauses
config = {"configurable": {"thread_id": "demo"}}
state_before = graph.invoke({"query": ...}, config=config)
# state_before["__interrupt__"] carries the draft and the question

# Phase 2: resume with the answer and the same thread_id
state_after = graph.invoke(Command(resume=True), config=config)
```

**Key**: `interrupt()` means "pause here." `Command(resume=True/False)` means "continue with the person's answer." A production app can connect that pause to a webhook, Slack, or a frontend button.

## Why this pattern matters

| Scenario | Without HITL | With HITL |
|---|---|---|
| Agent sends email | Send directly (risky) | Show draft, human approves |
| Agent changes prod config | Apply directly | Dry-run, wait for approval |
| Agent issues refund | Auto-refund | Refund over $X waits for review |

For a **side effect**—an action that changes the outside world—judge the risk first. Sending email, issuing refunds, or changing production settings usually needs HITL, permission checks, and an audit log. A low-risk read-only action may not need approval every time.

## What to watch on each path

Both paths use the same graph. `classify`, the offline lookup, and routing are predictable Python; `respond` calls a different model to write the draft. **When comparing paths, change only the model—not the graph.**

Inside the node, pause and use the person's answer to update state after resume:

```python
from langgraph.types import interrupt

def review_node(state):
    approved = interrupt({"draft": state["draft"], "question": "Approve?"})
    return {"approved": approved}
```

Outside the graph, the caller receives a real person's answer and resumes the same `thread_id`:

```python
from langgraph.types import Command

human_answer = True
result = graph.invoke(Command(resume=human_answer), config=config)
```

## Common pitfalls

- **No `checkpointer`**: without one, the graph cannot reliably save pause/resume state
- **`thread_id` mismatch**: the first `invoke` and `Command(resume=...)` must use the same config, or the original checkpoint cannot be found
- **A side effect before `interrupt()`**: the node may run again when resumed. Put email/refund work after approval and use an idempotency key
- **`conditional_edges` function must return a string**: `should_search`'s return value must be a key in the third dict of `add_conditional_edges` — can't return a literal node name

## Want smarter answers?

Compare another model, or replace the in-memory checkpointer with persistent storage that fits your deployment. Read the current persistence docs and test failure recovery before choosing a database.

## Extensions

- **Add retry**: in `search_node` failures, retry via LangGraph's `error` edge
- **Multiple HITL stops**: call `interrupt()` in separate review nodes and define the data required for each approval
- **Time-travel debug**: `graph.get_state_history(config)` gives all checkpoints — fork from any of them
- **Streaming**: `for state in graph.stream(...)` to watch state evolve

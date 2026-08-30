<div align="right">
  <a href="./README.md">Traditional Chinese</a> | <a href="./README.zh-Hans.md">Simplified Chinese</a> | <strong>English</strong>
</div>

# Exercise 1: Same Agent, Two Frameworks (LangGraph + CrewAI)

Pairs with [Stage 4 — Workflow Graphs & Agent Frameworks](../../../stages/04-agent-frameworks.en.md) Exercise 1.
> 🎓 **How to use this**: First run the provided `starter.py` (`python starter.py`), then change exactly one small thing and run the existing test again: `python test.py`. If the test fails, undo or fix that one change and try again. You do not need to rename the file or rewrite the whole solution. See [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md) for the full method.

> 📚 **Want the chapter-length version?** The starter in this folder is an illustrative build focused on the core pattern plus two SDK paths — it is not in-depth teaching material. Recommended for depth:
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ the most complete Chinese-language course out there — chapter by chapter, plus 16 production capabilities. **This exercise maps to hello-agents' framework comparison / orchestration chapter**
> - [LangGraph Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart) + [CrewAI official docs](https://docs.crewai.com/)
> - Full references in [Stage 4 Curated Projects](../../../stages/04-agent-frameworks.en.md#-curated-projects)


## Task

A minimal search + summarize agent:

- Given a query (e.g. "summarize Taipei")
- Agent uses a `search` tool to hit a knowledge base
- LLM summarizes the result in 1-2 sentences

Built once in **LangGraph** and once in **CrewAI** — compare styles.

## How to run — two paths + two frameworks

> ⚠️ **Give each exercise its own Python 3.11 `.venv`.** Do not install all five `requirements.txt` files together. They demonstrate different frameworks whose dependency ranges can conflict.

### Path A (default, free, local)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve

.\.venv\Scripts\python.exe starter.py # LangGraph + Ollama
.\.venv\Scripts\python.exe starter_crewai.py # CrewAI + Ollama comparison
```

Budget: the model API costs **$0**. Your computer, memory, electricity, and download time are not free.

### Path B (Anthropic, compare a cloud result)

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py # LangGraph + Claude
```

Pinned default: `claude-haiku-4-5-20251001`. Haiku 4.5 costs **$1** per million input tokens and **$5** per million output tokens. A request with 2,000 input + 1,000 output tokens costs `2,000 / 1,000,000 × $1 + 1,000 / 1,000,000 × $5 = $0.007`. A framework may make more than one request, so set a provider spend limit of **$0.05** for this exercise. This is an estimate, not a billing promise.

<details markdown="1">
<summary>macOS/Linux commands and verification information</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
./.venv/bin/python test.py
```

Official sources: [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | [CrewAI docs](https://docs.crewai.com/) | [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>Packages, model IDs, prices, and official links verified: 2026-08-28 UTC.</small>
</details>

## Validate the logic (mock-based)

```powershell
.\.venv\Scripts\python.exe test.py # LangGraph behavior
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic-path behavior
.\.venv\Scripts\python.exe test_crewai.py # CrewAI behavior
```

## Side-by-side framework comparison

| Dimension | LangGraph | CrewAI |
|---|---|---|
| Core abstraction | `StateGraph` + node + edge | `Agent` + `Task` + `Crew` |
| Mental model | "How does state flow?" | "Who plays what role?" |
| Loop control | Explicit conditional edges | Hidden inside `Crew.kickoff()` |
| Debug path | Inspect graph state and checkpoints | Inspect task output and verbose logs |
| Useful when | You need explicit state and branches | You want to express role/task collaboration quickly |
| Learning curve | Medium-high | Low |

### LangGraph style (condensed)

```python
g = StateGraph(State)
g.add_node("agent", agent_node)
g.add_node("tools", tool_node)
g.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
g.add_edge("tools", "agent")
```

"I tell the system explicitly: state shape, nodes, edges, branching via `should_continue`."

### CrewAI style (condensed)

```python
researcher = Agent(role="Researcher", goal="...", tools=[search], llm=MODEL)
task = Task(description=query, expected_output="...", agent=researcher)
crew = Crew(agents=[researcher], tasks=[task])
crew.kickoff()
```

"I describe: who plays this role, what task, what tools. Framework decides how to run."

## What to observe

1. **Abstraction cost**: CrewAI hides more, writes less code; but stack depth grows when debugging
2. **Small-model behavior**: test both paths; role descriptions, tool schemas, and task length can all change the result
3. **Controllability**: LangGraph exposes state transitions; CrewAI is "result-oriented"
4. **When to pick**: try LangGraph when you need to inspect each state transition; try CrewAI when roles are the clearest first description, then measure on your own task

## Common pitfalls

- **LangGraph `bind_tools`**: must `llm.bind_tools([search])` to expose tool schema. Without it the model doesn't know the tool exists
- **CrewAI model spec**: use LiteLLM format (`"ollama/qwen2.5:3b"`, not `"qwen2.5:3b"`). A wrong provider prefix can select a different backend, so print and verify the setting before a run
- **CrewAI return type**: `crew.kickoff()` returns a `CrewOutput` object; `str(result)` to get text. Bare `print(result)` may show repr

## Want smarter answers?

```powershell
$env:MODEL="claude-sonnet-5"; .\.venv\Scripts\python.exe starter_anthropic.py
$env:MODEL="qwen2.5:7b"; .\.venv\Scripts\python.exe starter.py
```

## Extensions

- **Streaming**: use LangGraph `graph.stream(...)`; for CrewAI, construct `Crew(..., stream=True)` and then call `crew.kickoff()`
- **Checkpointing**: LangGraph + `MemorySaver` for time-travel debug
- **Human-in-the-loop**: see Exercise 3

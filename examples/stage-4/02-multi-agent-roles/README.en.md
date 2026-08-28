<div align="right">
  <a href="./README.md">Traditional Chinese</a> | <a href="./README.zh-Hans.md">Simplified Chinese</a> | <strong>English</strong>
</div>

# Exercise 2: Multi-Agent Role Allocation (CrewAI)

Pairs with [Stage 4 — Agent Frameworks](../../../stages/04-agent-frameworks.en.md) Exercise 2.
> 🎓 **How to use this**: `starter.py` is the **complete solution**, not a TODO skeleton. The active approach works better — `mv starter.py starter_reference.py`, read the signatures but not the bodies, write your own `starter.py` from scratch, then run `python test.py` to check it; if you are stuck for 20 minutes, go back and compare against the reference. Full methodology in [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md).

> 📚 **Want the chapter-length version?** The starter in this folder is an illustrative build focused on the core pattern plus two SDK paths — it is not in-depth teaching material. Recommended for depth:
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ the most complete Chinese-language course out there — chapter by chapter, plus 16 production capabilities. **This exercise maps to hello-agents' multi-agent roles / Crew chapter**
> - [CrewAI Examples repo](https://github.com/crewAIInc/crewAI-examples) (official sequential / hierarchical templates; ⚠️ archived 2026-04, still worth reading as reference)
> - Full references in [Stage 4 Curated Projects](../../../stages/04-agent-frameworks.en.md#-curated-projects)


## Task

Three agents each own one step, collaborating to produce a blog intro:

```
Researcher → Writer → Critic
  (find facts)  (write)  (verify, PASS/ISSUES)
```

This is a **role-based pipeline**: describe each role, goal, and task, then CrewAI passes the result along in order.

## How to run — two paths

> ⚠️ **Give each exercise its own Python 3.11 `.venv`.** Do not mix the five Stage 4 `requirements.txt` files.

### Path A (default, free, local)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
.\.venv\Scripts\python.exe starter.py
```

Budget: the model API costs **$0**. Runtime depends on your CPU, memory, model, and prompt, so measure it on your machine.

### Path B (Anthropic, compare a cloud result)

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py
```

Pinned default: `anthropic/claude-haiku-4-5-20251001`. One model request with 2,000 input + 1,000 output tokens costs `2,000 / 1,000,000 × $1 + 1,000 / 1,000,000 × $5 = $0.007`. Three roles may each call the model or retry, so set a provider spend limit of **$0.10**.

<details markdown="1">
<summary>macOS/Linux commands and verification information</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
./.venv/bin/python test.py
```

Official sources: [CrewAI docs](https://docs.crewai.com/) | [LiteLLM docs](https://docs.litellm.ai/) | [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>Packages, model IDs, prices, and official links verified: 2026-08-28 UTC.</small>
</details>

## Validate the logic

```powershell
.\.venv\Scripts\python.exe test.py # roles, tasks, handoff, and stop condition
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic-path behavior
```

The offline tests do not call a real model, but they check three agents, three tasks, sequential process, context dependencies, handoff output, and an observable stop condition. Test model quality separately.

## Core CrewAI multi-agent concepts

### Agent

```python
researcher = Agent(
    role="Researcher",
    goal="...",          # one line: what does "success" look like
    backstory="...",     # persona context, shapes the prompt
    tools=[search],
    llm=MODEL,
)
```

**Key**: `role` and `goal` dramatically affect prompt quality. Don't write "Agent" — write "Researcher who finds factual data".

### Task

```python
research_task = Task(
    description="Search for X and report findings.",
    expected_output="A 1-2 sentence factual entry.",
    agent=researcher,
)
```

**Key**: `expected_output` is the passing example the LLM sees. "A two-sentence intro in active voice" is clearer than "Some text"; measure the improvement on your own task.

### Context dependency

```python
write_task = Task(..., context=[research_task])   # writer sees researcher's output
critic_task = Task(..., context=[research_task, write_task])  # critic sees both
```

**Key**: `context` is CrewAI's dataflow mechanism. `critic_task.context=[a, b]` means the critic sees the output of tasks a and b.

### Sequential vs hierarchical process

```python
Crew(..., process=Process.sequential)    # linear walk-through
Crew(..., process=Process.hierarchical)  # manager + workers, needs manager_llm
```

This exercise uses sequential because its order is easy to see. Hierarchical lets a manager dispatch work; use it when you need dynamic assignment and already have evaluations and stop conditions.

## Observation across both paths

| Observation | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| Researcher calls the tool | Verify in logs and output | Verify in logs and output |
| Writer uses the research | Check with the same test cases | Check with the same test cases |
| Critic catches an error | Do not assume success | Do not assume success |
| Speed | Measure on your network and task | Measure on your hardware and model |
| Model API cost | Calculate from tokens and calls | $0 |

**Punchline**: multi-agent adds handoff points. If one role drops information, the mistake can travel forward. Model size is not the only answer; evaluate role prompts, tool results, handoffs, and stop conditions.

## Common pitfalls

- **`expected_output` too generic**: "Some output" has no clear success condition. Change it to "A two-sentence blog intro in active voice," then compare with test cases
- **Missing `context`**: writer without `context=[research_task]` doesn't see researcher's output — it'll hallucinate
- **Small model + 3 agents**: it may run slowly or miss a step. Inspect the log first, then compare `qwen2.5:7b` or Claude if needed
- **`allow_delegation=True` use cautiously**: enables agents to call others, easy to loop. Default `False` for prototypes

## Want smarter answers?

```powershell
$env:MODEL="anthropic/claude-sonnet-5"; .\.venv\Scripts\python.exe starter_anthropic.py
$env:MODEL="ollama/qwen2.5:7b"; .\.venv\Scripts\python.exe starter.py
```

## Extensions

- **Add a manager**: `process=Process.hierarchical` + `manager_llm=...` for dynamic delegation
- **Add memory**: CrewAI has `memory=True` for cross-task context
- **Batch or async execution**: `crew.kickoff_for_each(...)` handles a list of inputs; `crew.kickoff_async(...)` runs asynchronously. Neither one means streaming
- **Streaming**: construct `Crew(..., stream=True)`, then call `crew.kickoff()`
- **Human-in-the-loop**: Exercise 3 demonstrates LangGraph; CrewAI also provides its own human-feedback triggers

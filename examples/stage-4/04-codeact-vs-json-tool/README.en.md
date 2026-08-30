<div align="right">
  <a href="./README.md">Traditional Chinese</a> | <a href="./README.zh-Hans.md">Simplified Chinese</a> | <strong>English</strong>
</div>

# Exercise 4: CodeAct vs JSON tool (Smolagents)

Pairs with [Stage 4 — Workflow Graphs & Agent Frameworks](../../../stages/04-agent-frameworks.en.md) Exercise 4.
> 🎓 **How to use this**: First run the provided `starter.py` (`python starter.py`), then change exactly one small thing and run the existing test again: `python test.py`. If the test fails, undo or fix that one change and try again. You do not need to rename the file or rewrite the whole solution. See [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md) for the full method.

> 📚 **Want the chapter-length version?** The starter in this folder is an illustrative build focused on the core pattern plus two SDK paths — it is not in-depth teaching material. Recommended for depth:
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ the most complete Chinese-language course out there — chapter by chapter, plus 16 production capabilities. **This exercise maps to hello-agents' CodeAct vs JSON tool chapter**
> - [Smolagents official cookbook](https://github.com/huggingface/smolagents/tree/main/examples) + [QuantaLogic/quantalogic](https://github.com/quantalogic/quantalogic) (another CodeAct framework)
> - Full references in [Stage 4 Curated Projects](../../../stages/04-agent-frameworks.en.md#-curated-projects)


## Two agent-action paradigms

| Path | How the agent acts | Example frameworks |
|---|---|---|
| **JSON tool** | LLM returns `{"name": "tool_x", "arguments": {...}}` | OpenAI function calling, LangGraph, CrewAI |
| **CodeAct** | LLM writes Python code, framework executes it | HuggingFace Smolagents |

**This exercise solves the same task (population ratio) using CodeAct** — compare with the JSON-tool implementations in Exercises 1 / 3.

## How to run — two paths

> ⚠️ **Give each exercise its own Python 3.11 `.venv`.** This one also requires Docker. Never run model-generated code directly on the host. This teaching container may still access the network, so do not put secrets or private data inside it.

### Path A (default, free, local)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
docker version
.\.venv\Scripts\python.exe test_docker_smoke.py
.\.venv\Scripts\python.exe starter.py
```

Budget: the model API costs **$0**. Local hardware, electricity, and Docker resources still have a cost. A smaller model may need correction steps, so the starter limits `max_steps` to 4.

### Path B (Anthropic, compare a cloud result)

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py
```

Pinned default: `anthropic/claude-haiku-4-5-20251001`. A request with 2,000 input + 1,000 output tokens costs **$0.007**. CodeAct can make several requests, so set a provider spend limit of **$0.10**. Actual cost depends on tokens and steps.

<details markdown="1">
<summary>macOS/Linux commands and verification information</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
docker version
./.venv/bin/python test.py
./.venv/bin/python test_docker_smoke.py
```

Price formula: `input_tokens / 1,000,000 × $1 + output_tokens / 1,000,000 × $5`.

Official sources: [Secure code execution](https://huggingface.co/docs/smolagents/tutorials/secure_code_execution) | [Python executors](https://huggingface.co/docs/smolagents/reference/python_executors) | [Docker port publishing](https://docs.docker.com/engine/network/port-publishing/) | [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>Packages, model IDs, prices, and official links verified: 2026-08-28 UTC.</small>
</details>

## Validate the logic

```powershell
.\.venv\Scripts\python.exe test.py # AST, JSON allowlist, loopback control port, and resource limits
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic setup + the same safe boundary
```

These two offline tests **do not** execute model-generated code and do not need a Docker daemon. `test_docker_smoke.py` is a separate manual smoke test: it starts the Jupyter executor, proves the host control channel works, and confirms the control port is bound only to `127.0.0.1`. Run it only after `docker version` succeeds. It does not pretend the container has no network access.

## How CodeAct works

The LLM doesn't return JSON — it returns a **Python code block**:

````
(user) Find Taipei population, divide by NYC, give ratio.

(LLM response)
```python
pop_taipei = lookup_fact(query="Taipei population")  # 2602000
pop_nyc = lookup_fact(query="New York population")   # 8336000
ratio = calculator(expression=f"{pop_taipei}/{pop_nyc}")  # 0.3122
print(ratio)
```

(Smolagents runs the code in a sandbox and feeds the print output back to the LLM)
````

This example explicitly uses a Docker executor. The Jupyter control port is bound only to host `127.0.0.1`; Linux capabilities are dropped, privilege escalation and pickle are blocked, and memory, process count, and agent steps are limited. A normal Docker bridge **may still let the container reach external networks or host services**. This is therefore a controlled teaching example, not a production sandbox. Untrusted code also needs real egress and host-access firewalling, or a remote sandbox with documented isolation boundaries.

## CodeAct vs JSON tool

| Dimension | JSON tool | CodeAct |
|---|---|---|
| LLM output form | Structured JSON | Python code |
| Variable binding | LLM must remember / call again | Native variables (`pop_taipei = ...`) |
| Multi-step compute | One call per step | Multiple steps in one code block |
| Tokens per round | Fewer | More (code is longer) |
| Small-model friendliness | Better (stable JSON) | Worse (must produce valid Python) |
| Debug | Inspect tool calls | Inspect code execution log |
| Safety | Allowlist + argument validation | Untrusted code: isolate it and limit permissions/resources |
| Best for | Single-step, clear boundaries | Multi-step computation, intermediate variables |

**HuggingFace's stance**: CodeAct is closer to how humans solve problems — use a variable for intermediate results, don't re-fetch each step.

## What to watch on each path

| Observation | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| Executable Python | Measure with the same cases | Measure with the same cases |
| Variable naming / reuse | Inspect the execution log | Inspect the execution log |
| Correct ratio | Validate the final value | Validate the final value |
| Total steps | Limited by `max_steps=4` | Limited by `max_steps=4` |
| Model API cost | Depends on tokens and steps | $0 |

**Punchline**: CodeAct adds an "execute code" risk surface that JSON tools do not have. Do not assume a model or path wins; compare success rate, steps, cost, and safety boundaries on the same tasks.

## Common pitfalls

- **`@tool` function docstring is part of the prompt**: Smolagents passes the docstring to the LLM as the tool description. **Bad docstring = LLM doesn't know when to use it.**
- **Treating Docker as a complete sandbox**: it is not. This starter reduces privileges and binds the control port to loopback; deployment still needs image, permission, egress, host-access, resource, and logging review
- **`max_steps` too low**: inspect which step failed before raising the limit; a higher number increases cost and loop risk
- **Model code has a syntax error**: Smolagents can return the error for correction, but that adds steps. Change models only after checking evaluation results

## Want smarter answers?

```powershell
$env:MODEL="anthropic/claude-sonnet-5"; .\.venv\Scripts\python.exe starter_anthropic.py
$env:MODEL="qwen2.5:7b"; .\.venv\Scripts\python.exe starter.py
```

## Extensions

- **More tools**: just `@tool`-decorate; Smolagents auto-extracts docstring as description
- **Try `ToolCallingAgent`**: Smolagents also offers JSON-tool-style agents. Compare side-by-side
- **Hugging Face Hub**: use the current `InferenceClientModel` for HF inference (no local Ollama required)
- **Read [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)**: both shapes can be useful; choose based on the task

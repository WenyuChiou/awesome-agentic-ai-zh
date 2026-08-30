<div align="right">
  <a href="./README.md">Traditional Chinese</a> | <a href="./README.zh-Hans.md">Simplified Chinese</a> | <strong>English</strong>
</div>

# Exercise 5: Type-Safe Agent (Pydantic AI structured output)

Pairs with [Stage 4 — Workflow Graphs & Agent Frameworks](../../../stages/04-agent-frameworks.en.md) Exercise 5.
> 🎓 **How to use this**: First run the provided `starter.py` (`python starter.py`), then change exactly one small thing and run the existing test again: `python test.py`. If the test fails, undo or fix that one change and try again. You do not need to rename the file or rewrite the whole solution. See [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md) for the full method.

> 📚 **Want the chapter-length version?** The starter in this folder is an illustrative build focused on the core pattern plus two SDK paths — it is not in-depth teaching material. Recommended for depth:
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ the most complete Chinese-language course out there — chapter by chapter, plus 16 production capabilities. **This exercise maps to hello-agents' structured output / type-safe chapter**
> - [Pydantic AI official docs](https://ai.pydantic.dev/) + [Instructor library](https://github.com/567-labs/instructor) (another route to typed output)
> - Full references in [Stage 4 Curated Projects](../../../stages/04-agent-frameworks.en.md#-curated-projects)


## Task

Agent answers questions and is **forced** to return `AnswerWithConfidence`:

```python
class AnswerWithConfidence(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)  # runtime check
    sources: list[str]
```

Pydantic AI puts **schema validation**—rules about data shape—into the program. If the LLM violates the schema, the framework can reject or retry it. This checks the shape; it **does not prove the answer is true**.

## How to run — two paths

> ⚠️ **Give each exercise its own Python 3.11 `.venv`.** Do not mix this Pydantic requirement set with the CrewAI exercises.

### Path A (default, free, local)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
.\.venv\Scripts\python.exe starter.py
```

Budget: the model API costs **$0**. Local hardware, electricity, and retry time still have a cost.

### Path B (Anthropic, compare a cloud result)

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py
```

Pinned default: `claude-haiku-4-5-20251001`. A request with 2,000 input + 1,000 output tokens costs `2,000 / 1,000,000 × $1 + 1,000 / 1,000,000 × $5 = $0.007`. Validation failure can cause a retry, so set a provider spend limit of **$0.05**.

<details markdown="1">
<summary>macOS/Linux commands and verification information</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
./.venv/bin/python test.py
```

Official sources: [Pydantic AI output](https://ai.pydantic.dev/output/) | [Pydantic AI testing](https://ai.pydantic.dev/testing/) | [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>Packages, model IDs, prices, and official links verified: 2026-08-28 UTC.</small>
</details>

## Validate the logic

```powershell
.\.venv\Scripts\python.exe test.py # official TestModel + schema boundaries
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic setup + the same output contract
```

`test.py` uses Pydantic AI's official `TestModel` and verifies that `AnswerWithConfidence` rejects out-of-range confidence, wrong types, blank answers, and empty sources. It makes no LLM call.

## Why type-safe agents matter

```
Stage 3 Exercise 6: schema = JSON Schema in the prompt
    LLM sees it, but what it returns is up to the LLM (may violate)

Stage 4 Exercise 5: schema = Pydantic model in code
    LLM violates → framework auto-raises → retry / fix
    A successful output has passed runtime shape checks
    Factual truth still needs a separate check
```

For production:

| Need | Prompt-only schema | Pydantic AI |
|---|---|---|
| LLM drops a field | Your downstream code needs try/except | Auto-retry until conformant |
| Wrong type (confidence="high") | Downstream crash | Pydantic ValidationError, retry |
| Out of bound (confidence=1.5) | Downstream gets bad data | Reject, retry |
| Extra fields | Depends on your parser | Handled by the Pydantic model's configuration |

**Bottom line**: typed output is useful when downstream code needs fixed fields. Stage 3 Exercise 6 teaches schema design; this exercise turns a schema into a runtime contract and reminds you to add fact checking.

## Core Pydantic AI concepts

### Agent + output_type

```python
agent = Agent(
    model=...,
    output_type=AnswerWithConfidence,   # ← force LLM into this shape
    system_prompt="..."
)
result = agent.run_sync(question)
answer: AnswerWithConfidence = result.output   # validated object
```

**Key**: the framework converts the Pydantic schema into structured-output instructions, validates the response, and retries according to your settings. A successful retry means the format passed—not that the content is true.

### Field constraints

```python
confidence: float = Field(ge=0.0, le=1.0, description="...")
```

`ge` / `le` are Pydantic's numeric bounds. If the LLM returns 1.5, Pydantic raises ValidationError → retry.

### Auto-retry

```python
Agent(..., retries=3)  # default 1, configurable
```

When Pydantic AI sees a ValidationError, it appends the error message back into the prompt and asks the LLM to retry.

## What to watch on each path

| Observation | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| First-attempt schema pass | Measure with the same cases | Measure with the same cases |
| Retry count | Record the actual result | Record the actual result |
| Confidence bounds | Enforced by Pydantic | Enforced by Pydantic |
| Sources is a list | Enforced by Pydantic | Enforced by Pydantic |
| Cost | Depends on tokens and retries | Model API $0 |

**Teaching point**: when comparing models, record pass rate, retries, latency, and cost together. Do not look only at per-token price, and do not assume a larger model is always cheaper.

## Common pitfalls

- **`output_type` too complex**: deep nesting is harder to generate and maintain. Start with the minimum fields, then use evaluations to decide whether to split it
- **Missing `description`**: `Field(...)` without `description=` leaves the LLM guessing what the field is for
- **`retries=0`**: failure raises immediately. Choose a bounded retry count from your cost, latency, and failure patterns
- **Small model + deep nesting**: qwen2.5:3b may retry many times and still fail. Upgrade or flatten

## Want smarter answers?

```powershell
$env:MODEL="claude-sonnet-5"; .\.venv\Scripts\python.exe starter_anthropic.py
$env:MODEL="qwen2.5:7b"; .\.venv\Scripts\python.exe starter.py
```

## Extensions

- **Add tools**: Pydantic AI agents can have tools + structured output simultaneously via `@agent.tool`
- **Stream typed output**: `agent.run_stream(...)` validates as it streams
- **Cross-model comparison**: run the same schema across Claude / GPT / Gemini / local models; compare pass rate, retries, and cost
- **Production wiring**: Pydantic AI integrates with FastAPI; a validated output can become an API response model

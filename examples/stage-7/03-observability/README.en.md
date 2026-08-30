<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 3: See What Happens Inside an Agent

**Observability** is like adding an instrument panel to an agent: when it becomes slow, fails, or uses too many tokens, you can find the responsible step.

Pairs with Exercise 3 in [Stage 7 — Agent Production Engineering: Harness, Loops, and Graphs](../../../stages/07-multi-agent-production.en.md).

## 🎯 Learning goals

- Learn five core signals: **Request ID, Span, Latency, Usage, and Error**.
- Connect all steps in one job with the same request ID.
- Record usage returned by the provider; if it is missing, show that it is missing instead of guessing.

## Run the model-free tests first

Open PowerShell in this folder and copy:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

Two `🎉` messages mean success, failure, latency, span, and usage behavior all have passing offline tests. The tests never contact a model.

<details markdown="1">
<summary>Path A: Produce a real trace with Ollama</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

Open another PowerShell window:

```powershell
.\.venv\Scripts\python.exe starter.py
```

Ollama does not charge a provider model API fee. Hardware, electricity, and time still have costs. Some versions may omit usage; the program keeps a zero value and never presents an estimate as provider data.

</details>

<details markdown="1">
<summary>Path B: Record the Usage returned by Anthropic</summary>

```powershell
$env:ANTHROPIC_API_KEY = "paste-your-key"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

Haiku 4.5 costs `$1 / 1M` input tokens and `$5 / 1M` output tokens:

```text
estimated cost = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

Set a `$1` provider spend limit first. Usage is the provider's count for that response. Field names and coverage can differ across APIs.

</details>

## Five important terms

- **Request ID**: a tracking number for one request.
- **Span**: one smaller step inside the request, such as search or llm_call.
- **Latency**: how long a step takes.
- **Usage**: the input/output token counts returned by the provider.
- **Error**: the failing step and a safe error category; after recording it, raise the exception again. Raw exception messages may contain secrets and must not be logged.

```text
request_id
├─ span: search      → latency
└─ span: llm_call    → latency + usage + error
```

This starter uses a tiny `TraceContext` to teach the idea. Production systems commonly use OpenTelemetry and send the data to an observability platform.

## Change one thing

Rename the fake `search` step to `retrieve_context`, then rerun the tests. Confirm that the summary still has two spans with the same request ID.

## Success check

- [ ] One request uses one request ID.
- [ ] Every step has a name and latency.
- [ ] An empty model reply records an error and raises an exception.
- [ ] Logs contain neither an API key, the full prompt, nor a raw exception message.

<details markdown="1">
<summary>Production additions and common problems</summary>

A production service should answer: Which step is slow? Which errors are common? How many tokens did one request use? When did behavior change?

Common problems:

- Only total time is recorded: you cannot tell whether search or the model was slow.
- An exception is swallowed: callers mistakenly see success. Record it, then raise it again.
- Full prompts or raw exception messages are logged: they may contain personal data, documents, or secrets. Log only safe error categories, then add redaction and access controls.
- Every trace is stored forever: cost and privacy risk grow. Define sampling, retention, and deletion rules.
- A local token estimate is labeled provider usage: name estimates and provider-returned fields separately.

</details>

## 📚 Required reading and learning resources

- ⭐⭐⭐⭐⭐ [Langfuse](https://github.com/langfuse/langfuse): open-source traces, evals, and prompt management.
- ⭐⭐⭐⭐⭐ [Arize Phoenix](https://github.com/Arize-ai/phoenix): open-source, OpenTelemetry-oriented observability.
- ⭐⭐⭐⭐⭐ [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents): Chapter-style Agent material for filling in the full background.
- ⭐⭐⭐⭐ [LangSmith](https://smith.langchain.com/): useful in the LangChain and LangGraph ecosystem.
- ⭐⭐⭐⭐ [Helicone](https://www.helicone.ai/): collect LLM request data through a proxy path.
- ⭐⭐⭐⭐ [Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/): useful for teams already using Datadog APM.
- ⭐⭐⭐⭐ [Anthropic Console](https://console.anthropic.com/): inspect Claude API usage and billing data.

See the full list in [Stage 7 Featured Projects](../../../stages/07-multi-agent-production.en.md#-featured-projects-templates--sdks--tool-collections).

<small>Models, prices, packages, and links checked: 2026-08-28 UTC.</small>

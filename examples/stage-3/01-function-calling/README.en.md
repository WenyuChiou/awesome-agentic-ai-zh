<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 1: One Tool, One Complete Round Trip

Corresponds to Exercise 1 in [Stage 3 — Tool Use & Hello Agent](../../../stages/03-tool-use-and-hello-agent.en.md).

This exercise does one thing: the model says “call `get_weather`,” your Python program validates the arguments, executes the tool, and returns the result to the model. After running it, you will see:

`Question → Tool Call → Program validates and executes → Tool Result → Final answer`

**Tool Call** is a tool request from the model. **Tool Result** is the result returned by your program after execution. A model request does not mean it has permission to execute code directly.

## First action

In PowerShell, copy and run:

```powershell
ollama pull qwen2.5:3b
```

## Path A: Ollama (local, API cost `$0`)

```powershell
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
ollama serve
python starter.py
```

If `ollama serve` says the port is already in use, Ollama is usually already running; leave that window open and run `python starter.py` in another PowerShell window.

This path uses the OpenAI Python SDK connected to `http://localhost:11434/v1`; data is not sent to the OpenAI cloud.

## Path B: Anthropic (requires an API key)

```powershell
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "your-key"
python starter_anthropic.py
```

The program uses the pinned model ID `claude-haiku-4-5-20251001`, so the teaching result does not silently change when a model alias moves.

**Budget reminder**: reserve a `$0.05` cap for each real run. Actual cost depends on token count:

`input tokens × $1 / 1,000,000 + output tokens × $5 / 1,000,000`

Tool Use also adds system-prompt tokens; do not present decimals based on a no-token assumption as guaranteed prices. Price checked on `2026-08-27`.

<details markdown="1">
<summary>macOS/Linux commands</summary>

```bash
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"
python starter_anthropic.py
```

</details>

## Free self-check

These tests use fake model responses: they do not connect to Ollama or call the Anthropic API.

```powershell
python test.py
python test_anthropic.py
```

You should see `all pass` twice. The tests also deliberately send bad JSON, extra fields, and an unknown tool to confirm the program blocks them first.

## What you are protecting

- **Allowlist**: only `get_weather` can execute; a model-generated different tool name is rejected.
- **Argument validation**: `city` cannot be empty, `unit` must be `celsius`, and extra fields are rejected.
- **Result matching**: every result carries the original `tool_call_id` or `tool_use_id`.
- **Error marker**: the Anthropic path adds `is_error: true` on failure so the model knows it is not a normal result.

## Completion conditions

- [ ] Path A or Path B succeeds at least once.
- [ ] Both offline tests show `all pass`.
- [ ] I can explain in my own words: “The model only makes a request; the program actually executes it.”
- [ ] I can point to where the program validates the tool name and arguments.

## Official references

- [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling)
- [Anthropic: How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)
- [Anthropic: Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)
- [Ollama OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility)

Docs and SDKs checked on `2026-08-27`.

> 📚 **Want the chapter-length version?** This folder teaches only the smallest first loop. Continue with:
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents): a chapter-based Chinese Agent course; use this exercise as the tool-calling starting point.
> - [Anthropic Tool Use Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/tool_use): official notebooks that grow from one tool to multiple tools.
> - [Stage 3 Curated Projects](../../../stages/03-tool-use-and-hello-agent.en.md#-curated-projects): return to the learning map and choose the next resource.

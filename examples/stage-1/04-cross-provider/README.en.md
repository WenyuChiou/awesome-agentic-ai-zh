<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 4: Cross-Provider Comparison (Claude / GPT / Gemini)

Corresponds to [Stage 1 — LLM Basics](../../../stages/01-llm-basics.en.md) Exercise 4.
> 🎓 **How to use this**: First run the provided `starter.py` (`python starter.py`), then change exactly one small thing and run the existing test again: `python test.py`. If the test fails, undo or fix that one change and try again. You do not need to rename the file or rewrite the whole solution. See [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md) for the full method.

## Why compare

Give the same "explain AGI vs narrow AI" prompt to three LLMs and the three answers come back different:

- **Claude**: usually leads with structure (definition → example), neutral tone
- **GPT**: tends to give the short answer first, then expand (type-A style)
- **Gemini**: tends toward lists / bullets, with lots of examples

Running it once yourself lands harder than reading a paper about it. You also get to measure three dimensions at once: tokens, cost, latency.

## How to run

```bash
pip install -r requirements.txt

# Set at least one. Any provider without a key is skipped, not crashed on
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export GOOGLE_API_KEY=...

python starter.py
```

Expected output (sample):

```
prompt: Explain the difference between AGI and narrow AI in 1-2 sentences.
============================================================
⚠ skipping call_gemini (no API key for it)

[Anthropic / claude-haiku-4-5]  latency=823ms  in=21 out=58
AGI (artificial general intelligence) can learn and solve problems across domains; narrow AI is good at a single task...

[OpenAI / gpt-5-mini]  latency=612ms  in=24 out=49
Narrow AI specializes in a specific task (chess, recognition); AGI by contrast has...

✅ Exercise 4 passed — got responses from 2 providers; compare style / length / cost
```

## Validate the logic without spending money

```bash
python test.py
```

All 4 tests replace the SDKs with `unittest.mock.patch`:

```
✅ test_skip_when_no_key
✅ test_compare_returns_only_valid_replies
✅ test_reply_dataclass_shape
✅ test_compare_one_provider_set

🎉 全部通過 — Cross-provider 邏輯正確（skip-on-missing-key 已驗）
```

## Program structure walkthrough

| Section | What it does |
|---|---|
| `Reply` dataclass | Normalizes the three SDKs' separate Response objects into 4 shared fields (text/in/out/latency) |
| `call_claude / call_openai / call_gemini` | One wrapper per SDK; returns `None` when the key is missing |
| `compare(prompt)` | Runs all three callers, skips the `None`s, returns the list of valid replies |
| `__main__` | Prints the comparison table and self-checks |

## Common pitfalls

1. **The three SDKs have very different API shapes** — Anthropic uses `messages.create`, OpenAI uses `chat.completions.create`, Google uses `models.generate_content`. **Only a shared dataclass makes them comparable**
2. **The token fields are named differently** — Anthropic has `input_tokens / output_tokens`, OpenAI has `prompt_tokens / completion_tokens`, Google has `prompt_token_count / candidates_token_count`
3. **A missing key should skip, not raise** — production code always needs this guard; a production agent must not die entirely because one provider is down
4. **Not capturing latency** — you only find out who is slow after the run, and production routing needs that data

## Want more providers?

OpenRouter, Mistral, Cohere, Groq, and other services may expose OpenAI-compatible endpoints, but do not assume changing only `base_url` gives full compatibility. Also verify the model ID, authentication, supported parameters, tool schema, response/usage fields, rate limits, and error format:

```python
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)
```

## 🦙 Path B — add a local Ollama as a fourth point of comparison

`call_openai` already uses an OpenAI-compatible client. For Ollama, change `base_url` and `model`, then use this exercise's tests to verify response, usage, and tool support:

```python
def call_ollama(prompt: str) -> Reply | None:
    """Local Ollama (gemma4:e4b or qwen2.5:3b). Returns None if it isn't installed, never crashes."""
    import requests
    try:
        requests.get("http://localhost:11434/api/tags", timeout=2)
    except Exception:
        return None  # Ollama isn't running
    from openai import OpenAI
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    t0 = time.time()
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return Reply(
        provider="Ollama-local",
        model="gemma4:e4b",
        text=r.choices[0].message.content or "",
        in_tokens=r.usage.prompt_tokens,
        out_tokens=r.usage.completion_tokens,
        latency_ms=int((time.time() - t0) * 1000),
    )
```

Add `call_ollama` to the caller list in `compare()` to see a four-provider comparison. The local path has no provider model API bill, but downloads, hardware, electricity, and waiting still have costs. Measure latency and quality on your machine with the same fixed tests.

## Extensions

- **Cost comparison** → wire in the PRICING dict from [the Stage 1 pricing exercise](../../../stages/01-llm-basics.en.md) and print a dollar-cost column
- **Run the same prompt N times and average** → add a for-loop inside `compare()` and look at the latency stdev
- **Add a quality eval** → bring in a fourth LLM as a judge and score each reply (Stage 7 Exercise 2 covers this)

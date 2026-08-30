<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 5: Error Handling + Retry Wrapper

Corresponds to [Stage 1 — LLM Basics](../../../stages/01-llm-basics.en.md) Exercise 5.
> 🎓 **How to use this**: First run the provided `starter.py` (`python starter.py`), then change exactly one small thing and run the existing tests again: `python test.py` and `python test_anthropic.py`. If a test fails, undo or fix that one change and try again. You do not need to rename the file or rewrite the whole solution. See [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md) for the full method.

## Why this matters

Production agents in Stages 3-8 will absolutely hit API errors:

- Rate limit (429) — different subscription tiers, you can hit it anytime
- Network jitter (connection reset) — cross-DC / VPN happens daily
- Expired API key (401) — rotation out of sync
- Context overflow (400) — you appended too much history

**Some errors should be retried (rate limit / network), others should not (key, context full).** Not distinguishing them is one of the most common production-agent mistakes.

## How to run — two paths

### Path A (default, free, local)

```bash
pip install -r requirements.txt
ollama pull gemma4:e4b
ollama serve
python starter.py
```

Budget: **$0**. The local demo shows connection / context-window behavior.

### Path B (Anthropic, real cloud errors)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python starter_anthropic.py
```

Budget: ~**$0.0005** per run (only "scenario 2 normal call" actually hits the API).

Expected output (Path A, local):

```
[Scenario 1] Pointing at a dead Ollama port
  ✅ Caught APIConnectionError
  💡 Production handling: retry (network errors are typically transient)

[Scenario 2] Normal call wrapped in with_retry (needs Ollama running)
  ✅ Succeeded on first try: 👋

[Scenario 3] Prompt over context window (Ollama usually truncates or raises)
  ⚠ Ollama didn't raise (it likely truncated). Cloud APIs would 400.

✅ Exercise 5 passed — you understand which errors raise, when to retry, when to stop. $0/run
```

## Validate the logic without network failures (mock-based)

```bash
python test.py            # validates Path A (Ollama) retry wrapper
python test_anthropic.py  # validates Path B (Anthropic) retry wrapper
```

6 tests use `unittest.mock` to fabricate errors + fake sleep (0 real seconds), validating the retry logic:

```
✅ test_no_retry_when_success_first_time
✅ test_retry_on_connection_error_then_success
✅ test_retry_on_rate_limit
✅ test_raise_after_max_attempts
✅ test_no_retry_on_auth_error
✅ test_exponential_backoff_delays

🎉 All passed — retry wrapper logic correct
```

> **Local advantage**: Ollama can't hit a real `RateLimitError` (no quota), so the "rate limit demo" is invisible. But the mock-based tests cover the retry logic completely and reproduce in 0 seconds — which is precisely what makes the Ollama path ideal for **learning retry patterns: fast, free, deterministic**.

## Program structure walkthrough

| Section | What it does |
|---|---|
| `RETRIABLE = (APIConnectionError, RateLimitError)` | Whitelist: only these two retry; everything else raises |
| `with_retry(fn, ...)` | Exponential backoff wrapper: 1s, 2s, 4s, 8s + jitter |
| `demo_bad_key()` | Triggers a network / 401 error to inspect the raised exception |
| `demo_with_retry()` | Normal call wrapped in `with_retry`, expected to succeed on first try |
| `demo_too_long_prompt()` | Oversize prompt — see how the context-window limit surfaces |

## Exception-class mapping between SDKs

| Anthropic SDK | OpenAI SDK (Ollama) | Meaning | RETRIABLE? |
|---|---|---|---|
| `anthropic.APIConnectionError` | `openai.APIConnectionError` | Network down | ✅ |
| `anthropic.RateLimitError` | `openai.RateLimitError` | 429 throttle | ✅ |
| `anthropic.AuthenticationError` | `openai.AuthenticationError` | 401 bad key | ❌ |
| `anthropic.APIStatusError` | `openai.APIStatusError` | Generic HTTP error | Depends on status |

The two SDKs use nearly identical class names; the retry logic is **fully backend-agnostic**. Swap SDKs = change the import line.

## Common pitfalls

1. **Blindly retry every exception** — you'll retry `AuthenticationError` 4 times for nothing. The RETRIABLE whitelist is the heart of this pattern
2. **No jitter** — 1000 workers rate-limited together, all retry after 1s, hit the limit again → deadlock. Add `random.uniform(0, 0.3)` to spread them
3. **`max_attempts` too high** — 8 retries = 1+2+4+8+16+32+64+128 = 255s, user gave up long ago. `max_attempts=4` usually suffices
4. **No attempt-count metric** — production must emit retry-count metrics; alert above threshold
5. **Ignoring `Retry-After`** — rate-limit responses include this header; SDKs handle it automatically, but a custom wrapper shouldn't ignore the hint

## Extensions

- **Better jitter** — try [decorrelated jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) for stability
- **Circuit breaker** — after N consecutive failures, stop calling for a while
- **Use [tenacity](https://github.com/jd/tenacity)** — production code shouldn't roll its own retry; this starter is just to show what's inside
- **Finer error classification** — different backoffs for 429 / 503 / 502 / 500
- **Stage 3 tool-level errors** — see [`../../stage-3/05-error-handling/`](../../stage-3/05-error-handling/) for structured tool errors that let the LLM decide within a ReAct loop

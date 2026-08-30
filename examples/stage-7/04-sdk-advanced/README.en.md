<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 4: Show the Answer While Checking the Cache

**Streaming** displays an answer in pieces. **Prompt caching** may reuse a shared long prefix. They solve different problems.

Pairs with Exercise 4 in [Stage 7 — Agent Production Engineering: Harness, Loops, and Graphs](../../../stages/07-multi-agent-production.en.md).

## 🎯 Learning goals

- Measure your own first-token and total latency instead of copying a fixed number.
- Skip empty chunks correctly and fail when the entire stream contains no text.
- Use `cache_creation_input_tokens` and `cache_read_input_tokens` to describe what actually happened.

## Run the model-free tests first

Open PowerShell in this folder and copy:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

Two `🎉` messages mean the streaming, empty-output, and cache_control offline contracts passed.

<details markdown="1">
<summary>Path A: Watch streaming with Ollama</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

Open another PowerShell window:

```powershell
.\.venv\Scripts\python.exe starter.py
```

Ollama does not charge a provider model API fee. Hardware, electricity, and time still have costs. Record your own first visible text time and total time; model, hardware, prompt, and current load all change the result.

</details>

<details markdown="1">
<summary>Path B: Inspect Anthropic streaming and Prompt caching</summary>

```powershell
$env:ANTHROPIC_API_KEY = "paste-your-key"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

Haiku 4.5 base input/output prices are `$1 / 1M` and `$5 / 1M` tokens. A five-minute cache write is 1.25 times base input, while a cache read is 0.1 times base input:

```text
estimated cost =
  normal_input_tokens × $1 / 1M
  + cache_creation_input_tokens × $1.25 / 1M
  + cache_read_input_tokens × $0.10 / 1M
  + output_tokens × $5 / 1M
```

Set a `$1` provider spend limit first. Decide whether the cache was created or read only from usage fields, not from the fact that this was the second call.

</details>

## Four important terms

- **Chunk**: one small piece of text arriving through a stream; it is not necessarily one token.
- **First-token latency**: time from sending the request to receiving the first displayable text.
- **Total latency**: time until the complete answer finishes.
- **Cache breakpoint**: the place where an API marks the preceding content as reusable.

This demo uses Haiku 4.5. Its documented minimum cacheable prompt length is **4,096 tokens**, so the program intentionally builds repeated reference text well above that threshold. It still does not promise a hit:

- `cache_creation_input_tokens > 0`: provider usage reports cache creation.
- `cache_read_input_tokens > 0`: provider usage reports a cache read.
- Both are 0: creation or a hit was not observed; check length, an identical prefix, and TTL.

## Change one thing

Change the second question while keeping `big_system` exactly the same. Then inspect whether the second usage record contains `cache_read_input_tokens`.

## Success check

- [ ] Streaming prints text in pieces and skips `None`.
- [ ] A stream with no text fails.
- [ ] The cache demo clearly exceeds the 4,096-token minimum.
- [ ] You describe creation, a hit, or no observed cache only from usage.

<details markdown="1">
<summary>When caching helps and common problems</summary>

Good fit: the same long system prompt, tool schema, or reference document is reused within a short period.

Poor fit: the prefix changes each time, content is short, or the next call usually arrives after the cache TTL.

Common problems:

- `cache_control` marks the wrong block: put the breakpoint at the end of the stable prefix.
- The second prefix changed: whitespace, tool order, or model changes may create a different cache key.
- Only the theoretical discount is counted: include write premium, read tokens, misses, and output tokens.
- A stream stops halfway: the production UI must mark it incomplete instead of treating half an answer as success.

</details>

## 📚 Required reading and learning resources

- ⭐⭐⭐⭐⭐ [Anthropic Prompt caching documentation](https://platform.claude.com/docs/en/build-with-claude/prompt-caching): the primary source for minimum length, TTL, breakpoints, and usage fields.
- ⭐⭐⭐⭐⭐ [Anthropic Pricing](https://platform.claude.com/docs/en/about-claude/pricing): recalculate with current prices instead of preserving an old fixed bill.
- ⭐⭐⭐⭐ [Anthropic Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing): explore batch jobs for non-interactive bulk work.
- ⭐⭐⭐⭐⭐ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents): chapter-style background when you need more depth.

See the full list in [Stage 7 Featured Projects](../../../stages/07-multi-agent-production.en.md#-featured-projects-templates--sdks--tool-collections).

<small>Models, prices, packages, cache conditions, and links checked: 2026-08-28 UTC.</small>

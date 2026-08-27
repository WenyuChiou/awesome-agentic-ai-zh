<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 6: Function Schema Design (bad vs good)

Corresponds to [Stage 3 — Tool Use & Agent Intro](../../../stages/03-tool-use-and-hello-agent.en.md) Exercise 6.
> 🎓 **How to use this**: `starter.py` is the **complete solution**, not a TODO skeleton. The active approach works better — `mv starter.py starter_reference.py`, read the signatures but not the bodies, write your own `starter.py` from scratch, then run `python test.py` to check it; if you are stuck for 20 minutes, go back and compare against the reference. Full methodology in [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md).

> 📚 **Want the chapter-length version?** The starter in this folder is a 70-150 line illustrative build focused on `the core pattern + two SDK paths` — it is not in-depth teaching material. Recommended for depth:
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ the most complete Chinese-language course out there — chapter-based, covering 16 production capabilities. **this exercise maps to hello-agents' [Extra08 — How to Write a Good Skill](https://github.com/datawhalechina/hello-agents/blob/main/Extra-Chapter/Extra08-如何写出好的Skill.md)**
> - [OpenAI Function Calling guide](https://developers.openai.com/api/docs/guides/function-calling) + [the schema design cheatsheet](../../../resources/schema-design-cheatsheet.en.md)
> - Full references in [Stage 3 Curated Projects](../../../stages/03-tool-use-and-hello-agent.en.md#-curated-projects)


## Why this matters

Schemas are **part of the prompt** — and they're the part the model **leans on hardest** when choosing a tool. This exercise gives you `starter_bad` and `starter_good` for the same question: "Convert 32 Celsius to Fahrenheit."

- **Bad schema**: short descriptions, every param as string, no `required`, no `enum` → LLM frequently misroutes temperature conversion to `process_data`
- **Good schema**: clear usage, `value: number`, `unit: enum["celsius", "fahrenheit"]`, all required fields listed → use a fixed eval to measure whether it routes to `convert_temperature` more often

When you write a schema, don't aim for "a human can read this". Aim for "the model can use this to rule out the wrong tool".

## How to run — two paths

### Path A (default, free, local, 4 starters)

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve

python starter_bad.py    # watch a bad schema mislead qwen
python starter_good.py   # watch a good schema lead qwen to the right tool
```

Budget: **$0 API cost**; hardware, memory, and electricity are excluded.

### Path B (Anthropic, cloud comparison)

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "your-key"

python starter_bad_anthropic.py
python starter_good_anthropic.py
```

Budget: reserve **$0.05** per run. Actual cost is `input tokens × $1 / 1,000,000 + output tokens × $5 / 1,000,000`; Tool Use also adds prompt tokens. Prices checked on `2026-08-27`.

## Validate the logic without API credits (mock-based)

```powershell
python test.py            # validates Path A (Ollama) starter_bad + starter_good
python test_anthropic.py  # validates Path B (Anthropic) starter_*_anthropic
```

Each test suite also asserts on the schema structure directly (`good` has `required` + `enum`; `bad` doesn't) — not just on the LLM's choice.

## Bad vs good schema A/B

| Design dimension | Bad | Good |
|---|---|---|
| Description | "Process data." | "Use only to summarize structured JSON table rows. Do not use for temperature conversion." |
| Param types | All `string` | `number` / `array` / actual types |
| Required | None | `["value", "unit"]` |
| Enum constraint | None | `["celsius", "fahrenheit"]` |
| Error return | Plain string | Structured dict + retry_hint |

## What to watch on each path (the teaching point)

Models may respond differently to schema quality; keep the prompt, schema, and test set fixed and use an eval to record behavior. Ollama is especially useful for observing this difference:

| Observation | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| Whether bad schema guesses right | Measure with a fixed eval | Measure with a fixed eval |
| Whether good schema picks correctly | Measure with a fixed eval | Measure with a fixed eval |
| Gap between bad and good | Measure with a fixed eval | Measure with a fixed eval |

In other words: measure schema quality and model behavior together with a fixed eval. Want to run a cheap model (qwen / mistral) in production? Your schemas need to be solid enough to run in production.

## Further reading

More schema design rules in [`resources/schema-design-cheatsheet.en.md`](../../../resources/schema-design-cheatsheet.en.md): clear usage, correct types, required fields, enum constraints, structured error returns.

## Extensions

- **Deliberately break the good schema** — remove one `enum` constraint and watch qwen start to miss
- **Add a third tool** — one with usage similar to but boundary-blurry with `convert_temperature`, and observe the LLM's choice
- **Combine with the structured-error pattern** from [`../05-error-handling/`](../05-error-handling/) — schema design + error handling is the combo for shipping to production

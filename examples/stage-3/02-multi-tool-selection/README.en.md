<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 2: Multi-Tool Selection

Corresponds to [Stage 3 — Tool Use & Your First Agent Loop](../../../stages/03-tool-use-and-hello-agent.en.md) Exercise 2.
> 🎓 **How to use this**: First run the provided `starter.py` (`python starter.py`), then change exactly one small thing and run the existing test again: `python test.py`. If the test fails, undo or fix that one change and try again. You do not need to rename the file or rewrite the whole solution. See [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md) for the full method.

> 📚 **Want the chapter-length version?** The starter in this folder is a 70-150 line illustrative build focused on `the core pattern + two SDK paths` — it is not in-depth teaching material. Recommended for depth:
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ the most complete Chinese-language course out there — chapter-based, covering 16 production capabilities. **this exercise maps to hello-agents' tool-calling / multi-tool dispatch chapter**
> - [Anthropic Tool Use Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/tool_use) (complete notebooks: single tool → multi-tool → parallel)
> - Full references in [Stage 3 Curated Projects](../../../stages/03-tool-use-and-hello-agent.en.md#-curated-projects)


## Why this matters

This exercise puts an LLM in front of three tools in a single turn: `web_search`, `calculator`, `calendar_lookup`. The point isn't tool quality — it's watching how schema `name` / `description` / `parameters` steer the model's choice. Writing schemas well is one of the highest-leverage things you do in Stage 3.

## How to run — two paths

### Path A (default, free, local)

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

Budget: **$0 API cost**; hardware, memory, and electricity are excluded.

### Path B (Anthropic, cloud comparison)

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "your-key"
python starter_anthropic.py
```

Budget: reserve **$0.05** per run. Actual cost is `input tokens × $1 / 1,000,000 + output tokens × $5 / 1,000,000`; Tool Use also adds prompt tokens. Prices checked on `2026-08-27`.

Expected output (Path A, local):

```
❓ Question: What is (19 * 42) - 8? Use the best available tool. (using Ollama qwen2.5:3b)
   tool: calculator
   tool_input: {'expression': '(19 * 42) - 8'}
   observation: 790
✅ Exercise 2 passed — you ran multi-tool selection locally on qwen2.5:3b, $0/run
```

## Validate the logic without API credits (mock-based)

```powershell
python test.py            # validates Path A (Ollama) starter.py logic
python test_anthropic.py  # validates Path B (Anthropic) starter_anthropic.py logic
```

Both test suites use `unittest.mock`, no real API call, $0/run. Path A uses the OpenAI-compat response shape; Path B uses Anthropic content blocks.

## SDK differences between the two paths

Three key differences (everything else is identical):

| Part | Anthropic (Path B) | OpenAI-compat / Ollama (Path A) |
|---|---|---|
| Schema wrap | `tools=[{name, description, input_schema}, ...]` | `tools=[{"type": "function", "function": {name, description, parameters}}, ...]` |
| Reading tool call | `resp.content[i].type == "tool_use"` | `resp.choices[0].message.tool_calls[i]` |
| input format | `call.input` is already a dict | `call.function.arguments` is a JSON string — needs `json.loads(...)` |

The selection **logic** is backend-agnostic, but observed behavior varies by model and prompt. Keep the prompt, schema, and test set fixed; use an eval to record success rates and failure types.

## Common pitfalls

The most common failure in multi-tool design is descriptions that read like documentation, not decision rules:

- `calendar_lookup` described as "calendar" is ambiguous with `web_search`; "look up events for a specific date" is clearer
- `web_search` is for "external / recent / uncertain info", `calculator` for arithmetic — the clearer the boundary, the fewer wrong picks
- Models may react differently to description quality; do not assume one is more stable. Measure with the same fixed eval.

## Want smarter answers?

Default is the pinned ID `claude-haiku-4-5-20251001`. To compare Sonnet:

```powershell
$env:MODEL = "claude-sonnet-5"; python starter_anthropic.py
```

Or on the Ollama path, try `qwen2.5:7b`; measure behavior and cost with the same fixed eval:

```powershell
$env:MODEL = "qwen2.5:7b"; python starter.py
```

## Extensions

- **Add more tools** — append one entry each to `TOOLS_SPEC` + `TOOL_IMPL`
- **Make it multi-turn ReAct** — wrap the single call in a `while` loop; see [`../03-react-from-scratch/`](../03-react-from-scratch/)
- **Dig into schema design** — see [`../06-schema-design/`](../06-schema-design/) for a bad vs good schema A/B

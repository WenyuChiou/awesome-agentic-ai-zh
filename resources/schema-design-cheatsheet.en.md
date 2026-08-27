# Function Schema Design Cheatsheet

> [繁體中文](./schema-design-cheatsheet.md) | [简体中文](./schema-design-cheatsheet.zh-Hans.md) | **English**

> Companion to [Stage 3 — Tool Use & Agent Intro](../stages/03-tool-use-and-hello-agent.en.md). 5 golden rules + 5 common anti-patterns when writing tool / function schemas.

> Specification checked: 2026-08-27 UTC. A schema is an interface shared by the model and program; clarity reduces ambiguity but cannot replace application validation or a fixed eval.

---

## 5 Golden Rules

### Rule 1: `description` is for the LLM, not for humans

The model reads the tool name, `description`, schema, and conversation together to decide whether to make a Tool Call. So:

- ✅ Write **when** + **what**: `"Call this when the user asks for current weather of a specific city."`
- ❌ Don't write implementation details: `"Uses OpenWeather API v2.5 returning JSON."`

Compare:

```python
# Bad
"description": "Get weather data."

# Good
"description": "Get current weather for a specified city. Use this when the user asks about current weather, temperature, humidity, or 'is it raining' for any specific location. Do NOT use for forecasts (use get_forecast instead) or historical data."
```

### Rule 2: Use the right `type`; collapse fuzzy params with `enum`

LLMs are loose with `type: string` and pass arbitrary text. Tighten where possible:

| Vague | Constrained |
|---|---|
| `unit: string` (celsius? fahrenheit? kelvin?) | `unit: enum["celsius", "fahrenheit"]` |
| `priority: string` (low/medium/HIGH?) | `priority: enum["low", "medium", "high"]` |
| `count: string` ("five"?) | `count: integer` |
| `enabled: string` ("true"/"True") | `enabled: boolean` |
| `tags: string` ("a,b,c"? JSON?) | `tags: array of string` |

### Rule 3: Be careful with `required` vs optional

- In ordinary JSON Schema, `required` lists fields without which execution cannot proceed.
- A default does not mean the provider will fill it for you; the program must apply defaults explicitly.
- **OpenAI strict mode is an exception**: every property must be listed in `required`; truly optional fields use a type that includes `null`, with `additionalProperties: false`.
- Anthropic, Ollama, and other compatible endpoints support strict mode differently; do not treat one provider’s rule as universal.

```python
# Bad: timezone listed as required → LLM invents "Asia/Taipei" even if not mentioned
"required": ["city", "timezone"]

# Simplified example for a non-strict schema
"required": ["city"],
"properties": {
    "timezone": {"type": "string", "default": "UTC", "description": "..."}
}
```

### Rule 4: Self-describing tool / param names

`do_thing(x, y, z)` and `get_weather(city, unit)` produce wildly different LLM behavior.

- ✅ `get_user_profile(user_id)`
- ❌ `fetch(id)` or `process_data(input)`

Verb-first names, signal whether it's a query / mutation / action.

### Rule 5: Errors must be recoverable

The program catches the error first, then decides whether to return a minimal, actionable error result to the model. Errors can be structured:

```json
{
    "error": "City not found",
    "code": "INVALID_CITY",
    "retry_hint": "Check spelling, or try a major city nearby"
}
```

Do not return only `"Error 500"`. An Anthropic client tool marks failure with `is_error: true`; other APIs have their own formats. Whatever the provider, the program must set a maximum retry count, timeout, and stopping condition.

---

## 5 Common Anti-Patterns

### Anti-1: God Tool

```python
# Bad: one tool for everything
def do_database_op(operation: str, table: str, data: str) -> str:
    """Do anything with the database."""
```

This tool mixes reads, creates, and updates, making least-privilege configuration difficult. Replace it with purpose-specific tools such as `query_users`, `create_order`, and `update_inventory`, then use a fixed eval to check whether selection improves.

### Anti-2: Description as docstring

```python
# Bad
"description": "GET /api/v2/weather endpoint. Returns JSON. See API docs."

# Good
"description": "Get current weather for a city. Returns temperature in C/F, humidity, and conditions."
```

The LLM doesn't read code — it wants **"when is this useful"**.

### Anti-3: Everything is a string

```python
# Bad
{"properties": {
    "count": {"type": "string"},     # LLM might pass "five"
    "active": {"type": "string"},    # LLM might pass "yes"
    "list": {"type": "string"}       # LLM might pass "[a, b, c]" or "a, b, c"
}}

# Good
{"properties": {
    "count": {"type": "integer", "minimum": 1, "maximum": 100},
    "active": {"type": "boolean"},
    "list": {"type": "array", "items": {"type": "string"}}
}}
```

### Anti-4: Declare a schema good after one success

Clear examples can help the model understand inputs, but cannot prove that a schema is reliable. Fix 5–10 normal, ambiguous, and adversarial cases, and run the bad and good versions on the same questions.

```python
"description": "Search products by query text, such as 'red shoes'. Do not use for product ID lookup; use get_product_by_id."
```

Record tool selection, argument validity, and whether the program rejected unauthorized input; do not score only how good the final sentence looks.

### Anti-5: Silent failures

If a tool fails and returns only `null` or `{}`, the model may treat empty data as success. Return an explicit status, for example:

- Success → `{"success": true, "data": {...}}`
- Failure → `{"success": false, "error": "...", "retry_hint": "..."}`

This JSON shape is an application convention, not a mandatory format for every API. The program must still handle the model ignoring errors, retrying repeatedly, or stopping early.

---

## Schema Evolution Tips

- Before adding a param, check provider rules: ordinary schemas can add an optional field with a default; OpenAI strict mode requires listing it in `required` and using `null` to represent omission
- Changing a param's meaning → ship a new tool (`get_weather_v2`), deprecate the old one before removing
- Changes to `description` → rerun the same eval; do not assume a small text change has no behavioral effect
- Before production: use [promptfoo](https://github.com/promptfoo/promptfoo) to eval "does the LLM pick the right tool on 5-10 typical queries"

---

## Further reading

- [Anthropic — Define Tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) — official schema and description guidance
- [Anthropic — Handle Tool Calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) — Tool Result and `is_error`
- [OpenAI — Function Calling](https://developers.openai.com/api/docs/guides/function-calling) — strict mode and function schema specification
- [Stage 3 — Tool Use & Agent Intro](../stages/03-tool-use-and-hello-agent.en.md) — main exercises
- [Stage 5.2 — MCP foundation](../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol--foundation) — MCP servers also use tool schemas, but host, permissions, and protocol layers differ

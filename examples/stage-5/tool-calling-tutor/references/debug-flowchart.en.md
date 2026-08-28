# Debug Flowchart: “Why won’t the LLM call my tool?”

> [繁體中文](./debug-flowchart.md) | [简体中文](./debug-flowchart.zh-Hans.md) | **English**

> Start with the symptom, then run the smallest check. This supports Step 2 in `SKILL.md`.

## Section A — Symptom (a): the LLM never produces tool_calls

The LLM saw `tools=[...]` but returned only text. Check these items:

```text
[ ] Is finish_reason "tool_calls" or "stop"?
[ ] Is message.tool_calls empty?
[ ] Does the user’s question actually need an external tool?
[ ] Does the sent schema match the current SDK format?
```

### Check these five items first

#### 1. The `description` is vague

```python
# ❌ No clear trigger
{"name": "get_data", "description": "Get data."}

# ✅ Clear trigger
{"name": "get_weather", "description": "Use this when the user asks about current weather, forecasts, or temperatures for a city."}
```

#### 2. Tool jobs overlap

```python
# ❌ search and lookup appear interchangeable
{"name": "search", "description": "Find information."}
{"name": "lookup", "description": "Look up data."}

# ✅ Each tool has a positive and negative boundary
{"name": "web_search", "description": "Use for current external information. Do not use for facts already provided by the user."}
{"name": "fact_lookup", "description": "Use for stored facts. Do not use for live news or prices."}
```

#### 3. The question does not need a tool

“What is Python?” usually does not need a weather or calculator tool. No tool call is not always a bug.

#### 4. The schema does not match the SDK

OpenAI-compatible schemas need `{"type": "function", "function": {...}}`; Anthropic schemas use `input_schema`. Clients can validate and report errors differently, so inspect the request, response, and application log.

#### 5. The current combination has no usable tool-calling support

Check the current SDK and model documentation, then run one **fixed test case (fixture)**—like asking the same test question every time. Keep the model, settings, and question unchanged when comparing. Do not infer support from a model name or size alone.

## Section B — Symptom (b): the tool is called, but its args are wrong

```python
# Expected
convert_temperature(value=32, unit="celsius")

# Possible output
convert_temperature(value="32 Celsius", unit="")
```

| What you see | Schema fix | What the app must still do |
|---|---|---|
| A number becomes text | `type: "number"` | Validate type and range again |
| A field is missing | `required` | Return a clear missing-value error |
| One unit has many spellings | `enum` | Accept only allowlisted values |

See [`schema-evolution.en.md`](schema-evolution.en.md) for the complete example.

## Section C — Symptom (c): the ReAct loop never stops

Check three things:

1. Append the complete assistant response to `messages`.
2. Return each result with the matching `tool_call_id` or `tool_use_id`.
3. Make the result self-contained, such as `{"city":"Taipei","forecast":"rain"}`, not just `"ok"`.

Every loop needs `MAX_STEPS`. Stop and report when the limit is reached; never retry forever.

## Section D — Symptom (d): a multi-step task skips a step

For example, the model divides two numbers but forgets to convert the ratio to a percentage. Check it this way:

1. Record the actual tool sequence for a fixed case.
2. State ordering in the description, such as `Call this last after dividing.`
3. Ask for a short, observable tool plan containing only steps and tool names. Do not request, store, or reveal hidden reasoning.

Runnable multi-step example: [Stage 3 multi-step reasoning](https://github.com/WenyuChiou/awesome-agentic-ai-zh/tree/main/examples/stage-3/04-multi-step-reasoning).

# SDK Diff: Anthropic and OpenAI-compatible

> [繁體中文](./sdk-diff.md) | [简体中文](./sdk-diff.zh-Hans.md) | **English**

> The same tool loop has different wrappers. Identify the fields, then validate every arg supplied by the model.

## The main differences

| Part | Anthropic SDK | OpenAI-compatible SDK |
|---|---|---|
| Tool schema | `{name, description, input_schema}` | `{"type":"function","function":{name, description, parameters}}` |
| Tool call | `tool_use` content block | `message.tool_calls` |
| Args | `call.input` is a dict | `call.function.arguments` is a JSON string |
| Tool result ID | `tool_use_id` | `tool_call_id` |
| Common completion signal | `stop_reason == "end_turn"` | `finish_reason == "stop"` |

Providers and versions can add other values. Check the current official documentation and keep the raw response for debugging.

## Safety guards needed on both paths

A schema is a hint, not a firewall. Apply an **allowlist**—the short list of tools the app permits—and validate args before executing a tool.

```python
import json

MAX_STEPS = 5
ALLOWED_TOOLS = {"get_weather"}

def validate_args(name, args):
    if name not in ALLOWED_TOOLS:
        raise ValueError(f"tool not allowed: {name}")
    if not isinstance(args, dict):
        raise ValueError("args must be an object")
    city = args.get("city")
    if not isinstance(city, str) or not city.strip():
        raise ValueError("city must be a non-empty string")
    return {"city": city.strip()}

def call_tool(name, args):
    clean_args = validate_args(name, args)
    return TOOL_IMPL[name](**clean_args)

def expected_error(exc):
    return json.dumps({"ok": False, "error": str(exc)})
```

Convert only expected input errors into structured results. Log and surface unexpected exceptions; never swallow them silently.

## Anthropic: bounded loop

```python
messages = [{"role": "user", "content": "Is it raining in Taipei?"}]

for step in range(MAX_STEPS):
    resp = client.messages.create(
        model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages
    )
    messages.append({"role": "assistant", "content": resp.content})

    calls = [block for block in resp.content if block.type == "tool_use"]
    if resp.stop_reason == "end_turn" and not calls:
        break

    tool_results = []
    for call in calls:
        try:
            result = call_tool(call.name, call.input)
            content = json.dumps({"ok": True, "result": result})
        except ValueError as exc:
            content = expected_error(exc)
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": call.id,
            "content": content,
        })

    if not tool_results:
        raise RuntimeError(f"unexpected stop_reason: {resp.stop_reason}")
    messages.append({"role": "user", "content": tool_results})
else:
    raise RuntimeError("tool loop reached MAX_STEPS")
```

## OpenAI-compatible: bounded loop

```python
messages = [{"role": "user", "content": "Is it raining in Taipei?"}]

for step in range(MAX_STEPS):
    resp = client.chat.completions.create(
        model=MODEL, tools=TOOLS, messages=messages
    )
    msg = resp.choices[0].message
    messages.append(msg.model_dump(exclude_none=True))

    if not msg.tool_calls:
        if resp.choices[0].finish_reason == "stop":
            break
        raise RuntimeError(
            f"unexpected finish_reason: {resp.choices[0].finish_reason}"
        )

    for call in msg.tool_calls:
        try:
            args = json.loads(call.function.arguments)
            result = call_tool(call.function.name, args)
            content = json.dumps({"ok": True, "result": result})
        except (json.JSONDecodeError, ValueError) as exc:
            content = expected_error(exc)
        messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": content,
        })
else:
    raise RuntimeError("tool loop reached MAX_STEPS")
```

## Four easy mistakes

1. `parameters` and `input_schema` are different wrappers.
2. OpenAI-compatible arguments need `json.loads`; both paths still need validation.
3. Every result must carry the matching `tool_call_id` or `tool_use_id`.
4. The loop must preserve complete assistant history and enforce `MAX_STEPS`.

Runnable comparisons: [Stage 3 multi-tool selection](https://github.com/WenyuChiou/awesome-agentic-ai-zh/tree/main/examples/stage-3/02-multi-tool-selection) through [schema design](https://github.com/WenyuChiou/awesome-agentic-ai-zh/tree/main/examples/stage-3/06-schema-design).

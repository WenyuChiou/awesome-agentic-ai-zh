# SDK Diff：Anthropic 与 OpenAI-compatible

> [繁體中文](./sdk-diff.md) | **简体中文** | [English](./sdk-diff.en.md)

> 同一个 tool loop，外包装不同。先认清字段，再验证 model 提供的 args。

## 先看差在哪里

| 部分 | Anthropic SDK | OpenAI-compatible SDK |
|---|---|---|
| Tool schema | `{name, description, input_schema}` | `{"type":"function","function":{name, description, parameters}}` |
| Tool call | `tool_use` content block | `message.tool_calls` |
| Args | `call.input` 是 dict | `call.function.arguments` 是 JSON string |
| Tool result ID | `tool_use_id` | `tool_call_id` |
| 常见完成信号 | `stop_reason == "end_turn"` | `finish_reason == "stop"` |

不同 provider 或版本可能增加其他值。使用前要查看当前官方文档，并保存原始 response 方便 debug。

## 两边都要有的安全护栏

Schema 是提示，不是防火墙。先做 **allowlist（只准名单）**和参数验证，再执行工具。

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
    return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)
```

只把预期的输入错误转换成结构化结果。未预期的异常要记录并清楚失败，不能偷偷吞掉。

## Anthropic：有上限的 loop

```python
messages = [{"role": "user", "content": "台北现在有下雨吗？"}]

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
            content = json.dumps({"ok": True, "result": result}, ensure_ascii=False)
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

## OpenAI-compatible：有上限的 loop

```python
messages = [{"role": "user", "content": "台北现在有下雨吗？"}]

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
            content = json.dumps({"ok": True, "result": result}, ensure_ascii=False)
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

## 最容易混淆的四点

1. `parameters` 和 `input_schema` 不是同一个外包装。
2. OpenAI-compatible 的 arguments 要先 `json.loads`；两边都要再验证。
3. 每个结果必须带回对应的 `tool_call_id` 或 `tool_use_id`。
4. Loop 必须保留完整 assistant history，并设置 `MAX_STEPS`。

可运行对照：[Stage 3 multi-tool selection](https://github.com/WenyuChiou/awesome-agentic-ai-zh/tree/main/examples/stage-3/02-multi-tool-selection) 到 [schema design](https://github.com/WenyuChiou/awesome-agentic-ai-zh/tree/main/examples/stage-3/06-schema-design)。

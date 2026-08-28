# Debug Flowchart：“为什么 LLM 不调用我的 tool”

> [繁體中文](./debug-flowchart.md) | **简体中文** | [English](./debug-flowchart.en.md)

> 先看症状，再做最小检查。对应 `SKILL.md` Step 2。

## Section A — Symptom (a)：LLM 完全不触发 tool_calls

LLM 看到了 `tools=[...]`，却只返回文字。先逐项确认：

```text
[ ] finish_reason 是 "tool_calls" 还是 "stop"？
[ ] message.tool_calls 是空的吗？
[ ] user 的问题真的需要外部工具吗？
[ ] 发出的 tool schema 符合当前 SDK 格式吗？
```

### 先检查这 5 项

#### 1. `description` 太模糊

```python
# ❌ 看不出何时使用
{"name": "get_data", "description": "Get data."}

# ✅ 说清楚使用时机
{"name": "get_weather", "description": "Use this when the user asks about current weather, forecasts, or temperatures for a city."}
```

#### 2. 多个 tool 的工作重叠

```python
# ❌ search 和 lookup 看起来一样
{"name": "search", "description": "Find information."}
{"name": "lookup", "description": "Look up data."}

# ✅ 各自说清楚能做和不能做的事
{"name": "web_search", "description": "Use for current external information. Do not use for facts already provided by the user."}
{"name": "fact_lookup", "description": "Use for stored facts. Do not use for live news or prices."}
```

#### 3. 问题根本不需要 tool

“什么是 Python？”通常不需要天气或计算工具。没有 tool call 不一定是 bug。

#### 4. Schema 结构不符合 SDK

OpenAI-compatible 格式需要 `{"type": "function", "function": {...}}`；Anthropic 格式使用 `input_schema`。不同 client 的验证与报错方式可能不同，所以要检查实际发出的 request、收到的 response 和应用程序 log。

#### 5. 当前组合没有可用的 tool-calling 支持

查看当前 SDK 与 model 的官方文档，再用一个**固定小测试（fixture）**确认。它像每次都考同一道题。比较时保持 model、设置和问题不变；不要只看 model 名称或大小猜结果。

## Section B — Symptom (b)：tool 被调用，但 args 错

```python
# 预期
convert_temperature(value=32, unit="celsius")

# 可能收到
convert_temperature(value="32 Celsius", unit="")
```

| 看到的问题 | Schema 修法 | 程序仍要做什么 |
|---|---|---|
| 数字变成文字 | `type: "number"` | 再检查类型和范围 |
| 少了字段 | `required` | 缺值时返回清楚错误 |
| 同一单位有多种写法 | `enum` | 只接受 allowlist 内的值 |

完整例子见 [`schema-evolution.zh-Hans.md`](schema-evolution.zh-Hans.md)。

## Section C — Symptom (c)：ReAct loop 跑不停

先检查三件事：

1. 把完整 assistant response 接回 `messages`。
2. tool result 带回正确的 `tool_call_id` 或 `tool_use_id`。
3. tool result 要自成一体，例如 `{"city":"Taipei","forecast":"rain"}`，不能只返回 `"ok"`。

Loop 一定要有 `MAX_STEPS`。到上限时停止并报告，不可无限重试。

## Section D — Symptom (d)：多步任务漏了一步

例如算完比例后，忘了再转成百分比。可以这样检查：

1. 用固定案例记录实际的 tool sequence。
2. 在 description 写清楚顺序，例如 `Call this last after dividing.`。
3. 要求一份短而可检查的工具计划，只列步骤和工具名称；不要要求、保存或公开模型的隐藏推理。

可运行的多步范例：[Stage 3 multi-step reasoning](https://github.com/WenyuChiou/awesome-agentic-ai-zh/tree/main/examples/stage-3/04-multi-step-reasoning)。

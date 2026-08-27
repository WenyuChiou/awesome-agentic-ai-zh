# Function Schema 设计 Cheatsheet

> [繁體中文](./schema-design-cheatsheet.md) | **简体中文** | [English](./schema-design-cheatsheet.en.md)

> [Stage 3 — Tool Use & Agent 入门](../stages/03-tool-use-and-hello-agent.zh-Hans.md) 的补充参考。写 tool / function schema 时的 5 条黄金规则 + 5 个 anti-pattern。

> 规格查核：2026-08-27 UTC。Schema 是模型和程序共同使用的接口；写清楚会减少歧义，但不能代替应用程序验证或固定 eval。

---

## 5 条黄金规则

### 规则 1：description 是写给 LLM 看的，不是 docstring

模型会一起看 tool name、`description`、schema 与对话内容，决定要不要提出 Tool Call。所以要：

- ✅ 写**情境**（when）跟**做什么**（what）：`"当用户问特定城市的天气时调用"`
- ❌ 不要写实作细节：`"使用 OpenWeather API v2.5 取得 JSON"`

对照：

```python
# 坏
"description": "Get weather data."

# 好
"description": "Get current weather for a specified city. Use this when the user asks about the current weather, temperature, humidity, or 'is it raining' for any specific location. Do NOT use for forecasts (use get_forecast instead) or historical data."
```

### 规则 2：参数用对 type，模糊处用 enum 收敛

LLM 对 `type: string` 自由度高、容易乱传。能用窄型别就用：

| 模糊 | 收敛 |
|---|---|
| `unit: string`（摄氏？华氏？kelvin？） | `unit: enum["celsius", "fahrenheit"]` |
| `priority: string`（low/中/HIGH？） | `priority: enum["low", "medium", "high"]` |
| `count: string`（"五个"？） | `count: integer` |
| `enabled: string`（"true" / "True"） | `enabled: boolean` |
| `tags: string`（"a,b,c"？JSON？） | `tags: array of string` |

### 规则 3：required vs optional 分清楚

- 一般 JSON Schema 中，`required` 列出少了就不能执行的栏位。
- 有默认值不代表供应商一定会替你填值；程序要明确套用 default。
- **OpenAI strict mode 是例外**：properties 全部要列入 `required`，真正可选的栏位用包含 `null` 的 type 表示，并设置 `additionalProperties: false`。
- Anthropic、Ollama 与其他 compatible endpoint 的 strict 支持不同；不要把一家的规则当成通用规范。

```python
# 坏：把 timezone 列 required，LLM 会乱编「Asia/Taipei」即便用户没提到
"required": ["city", "timezone"]

# 一般非 strict schema 的简化例子
"required": ["city"],
"properties": {
    "timezone": {"type": "string", "default": "UTC", "description": "..."}
}
```

### 规则 4：tool name + parameter name 要自说明

LLM 看到 `do_thing(x, y, z)` 跟看到 `get_weather(city, unit)` 用法完全不同。

- ✅ `get_user_profile(user_id)`
- ❌ `fetch(id)` 或 `process_data(input)`

动词开头，说清楚是 query / mutation / action。

### 规则 5：error 回传要让 LLM 可以恢复

程序先捕捉错误，再决定是否把最小、可处理的错误结果交回模型。错误可以结构化：

```json
{
    "error": "City not found",
    "code": "INVALID_CITY",
    "retry_hint": "Check spelling, or try a major city nearby"
}
```

而不是只回 `"Error 500"`。Anthropic client tool 用 `is_error: true` 标示失败；其他 API 有自己的格式。无论哪一家，程序都要设置最大重试、timeout 和停止条件。

---

## 5 个常见 Anti-Pattern

### Anti-1：“万能工具”（God Tool）

```python
# 坏：一个 tool 做所有事
def do_database_op(operation: str, table: str, data: str) -> str:
    """Do anything with the database."""
```

这种工具把读取、创建和修改混在一起，也很难配置最小权限。改成 `query_users`、`create_order`、`update_inventory` 等用途清楚的工具，再用固定 eval 检查选择是否改善。

### Anti-2：description 是 docstring

```python
# 坏
"description": "GET /api/v2/weather endpoint. Returns JSON. See API docs."

# 好
"description": "Get current weather for a city. Returns temperature in C/F, humidity, and conditions."
```

LLM 不是程序，它要的是 **“这个 tool 什么时候有用”**。

### Anti-3：所有东西都是 string

```python
# 坏
{"properties": {
    "count": {"type": "string"},     # LLM 可能传 "five"
    "active": {"type": "string"},    # LLM 可能传 "yes"
    "list": {"type": "string"}       # LLM 可能传 "[a, b, c]" 或 "a, b, c"
}}

# 好
{"properties": {
    "count": {"type": "integer", "minimum": 1, "maximum": 100},
    "active": {"type": "boolean"},
    "list": {"type": "array", "items": {"type": "string"}}
}}
```

### Anti-4：只看一次成功就宣布 schema 很好

清楚的例子可以帮助模型理解输入，但不能证明 schema 一定可靠。固定 5–10 个正常、模糊与恶意案例，让坏版与好版运行同一组题目。

```python
"description": "Search products by query text, such as 'red shoes'. Do not use for product ID lookup; use get_product_by_id."
```

记录工具选择、参数是否合法、程序是否拒绝未授权输入；不要只评最后一句话好不好看。

### Anti-5：沉默的失败

Tool 失败只回 `null` 或 `{}`，模型可能把空数据当成功。返回明确状态，例如：

- 成功 → `{"success": true, "data": {...}}`
- 失败 → `{"success": false, "error": "...", "retry_hint": "..."}`

这个 JSON 外形只是应用程序约定，不是所有 API 的强制格式。程序仍要处理模型忽略错误、反复重试或提早停止的情况。

---

## Schema 演进的小建议

- 加参数先确认供应商规则：一般 schema 可加 optional + default；OpenAI strict mode 则要把栏位列为 required，并用 `null` 表示可省略
- 改参数含义 → 开新 tool（`get_weather_v2`），旧的标 deprecated 一段时间再下
- description 改了要重新跑同一组 eval；不要假设文字小改一定没有行为差异
- 上 production 前用 [promptfoo](https://github.com/promptfoo/promptfoo) eval 一下“LLM 在 5-10 个典型 query 是否选对 tool”

---

## 延伸阅读

- [Anthropic — Define Tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) — 官方 schema 与 description 指南
- [Anthropic — Handle Tool Calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) — Tool Result 与 `is_error`
- [OpenAI — Function Calling](https://developers.openai.com/api/docs/guides/function-calling) — strict mode 与 function schema 规格
- [Stage 3 — Tool Use & Agent 入门](../stages/03-tool-use-and-hello-agent.zh-Hans.md) — 主要动手练习
- [Stage 5.2 — MCP 基础](../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础) — MCP server 也使用 tool schema，但 host、权限与协议层不同

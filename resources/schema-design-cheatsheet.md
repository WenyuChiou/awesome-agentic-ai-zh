# Function Schema 設計 Cheatsheet

> **繁體中文** | [简体中文](./schema-design-cheatsheet.zh-Hans.md) | [English](./schema-design-cheatsheet.en.md)

> [Stage 3 — Tool Use & Agent 入門](../stages/03-tool-use-and-hello-agent.md) 的補充參考。寫 tool / function schema 時的 5 條黃金規則 + 5 個 anti-pattern。

> 規格查核：2026-08-27 UTC。Schema 是模型和程式共同看的介面；寫清楚會減少歧義，但不能取代應用程式驗證或固定 eval。

---

## 5 條黃金規則

### 規則 1：description 是寫給 LLM 看的，不是 docstring

模型會一起看 tool name、`description`、schema 與對話內容，決定要不要提出 Tool Call。所以要：

- ✅ 寫**情境**（when）跟**做什麼**（what）：`"當使用者問特定城市的當前天氣時呼叫"`
- ❌ 不要寫實作細節：`"使用 OpenWeather API v2.5 取得 JSON"`

對照：

```python
# 壞
"description": "Get weather data."

# 好
"description": "Get current weather for a specified city. Use this when the user asks about the current weather, temperature, humidity, or 'is it raining' for any specific location. Do NOT use for forecasts (use get_forecast instead) or historical data."
```

### 規則 2：參數用對 type，模糊處用 enum 收斂

LLM 對 `type: string` 自由度高、容易亂傳。能用窄型別就用：

| 模糊 | 收斂 |
|---|---|
| `unit: string`（攝氏？華氏？kelvin？） | `unit: enum["celsius", "fahrenheit"]` |
| `priority: string`（low/中/HIGH？） | `priority: enum["low", "medium", "high"]` |
| `count: string`（"五個"？） | `count: integer` |
| `enabled: string`（"true" / "True"） | `enabled: boolean` |
| `tags: string`（"a,b,c"？JSON？） | `tags: array of string` |

### 規則 3：required vs optional 分清楚

- 一般 JSON Schema 中，`required` 列出少了就不能執行的欄位。
- 有預設值不代表供應商一定會替你填值；程式要明確套用 default。
- **OpenAI strict mode 是例外**：properties 全部要列入 `required`，真正可選的欄位用包含 `null` 的 type 表示，並設定 `additionalProperties: false`。
- Anthropic、Ollama 與其他 compatible endpoint 的 strict 支援不同；不要把一家規則當成通用規格。

```python
# 壞：把 timezone 列 required，LLM 會亂編「Asia/Taipei」即便使用者沒提到
"required": ["city", "timezone"]

# 一般非 strict schema 的簡化例子
"required": ["city"],
"properties": {
    "timezone": {"type": "string", "default": "UTC", "description": "..."}
}
```

### 規則 4：tool name + parameter name 要自說明

LLM 看到 `do_thing(x, y, z)` 跟看到 `get_weather(city, unit)` 用法完全不同。

- ✅ `get_user_profile(user_id)`
- ❌ `fetch(id)` 或 `process_data(input)`

動詞開頭，說清楚是 query / mutation / action。

### 規則 5：error 回傳要讓 LLM 可以恢復

程式先捕捉錯誤，再決定是否把最小、可處理的錯誤結果交回模型。錯誤可以結構化：

```json
{
    "error": "City not found",
    "code": "INVALID_CITY",
    "retry_hint": "Check spelling, or try a major city nearby"
}
```

而不是只回 `"Error 500"`。Anthropic client tool 用 `is_error: true` 標示失敗；其他 API 有自己的格式。無論哪一家，程式都要設定最大重試、timeout 和停止條件。

---

## 5 個常見 Anti-Pattern

### Anti-1：「萬用工具」（God Tool）

```python
# 壞：一個 tool 做所有事
def do_database_op(operation: str, table: str, data: str) -> str:
    """Do anything with the database."""
```

這種工具把讀取、建立和修改混在一起，也很難配置最小權限。改成 `query_users`、`create_order`、`update_inventory` 等用途清楚的工具，再用固定 eval 檢查選擇是否改善。

### Anti-2：description 是 docstring

```python
# 壞
"description": "GET /api/v2/weather endpoint. Returns JSON. See API docs."

# 好
"description": "Get current weather for a city. Returns temperature in C/F, humidity, and conditions."
```

LLM 不是程式，它要的是 **「這個 tool 什麼時候有用」**。

### Anti-3：所有東西都是 string

```python
# 壞
{"properties": {
    "count": {"type": "string"},     # LLM 可能傳 "five"
    "active": {"type": "string"},    # LLM 可能傳 "yes"
    "list": {"type": "string"}       # LLM 可能傳 "[a, b, c]" 或 "a, b, c"
}}

# 好
{"properties": {
    "count": {"type": "integer", "minimum": 1, "maximum": 100},
    "active": {"type": "boolean"},
    "list": {"type": "array", "items": {"type": "string"}}
}}
```

### Anti-4：只看一次成功就宣布 schema 很好

清楚的例子可以幫模型理解輸入，但不能證明 schema 一定可靠。固定 5–10 個正常、模糊與惡意案例，讓壞版與好版跑同一組題目。

```python
"description": "Search products by query text, such as 'red shoes'. Do not use for product ID lookup; use get_product_by_id."
```

記錄工具選擇、參數是否合法、程式是否拒絕未授權輸入；不要只評最後一句話好不好看。

### Anti-5：沉默的失敗

Tool 失敗只回 `null` 或 `{}`，模型可能把空資料當成功。回傳明確狀態，例如：

- 成功 → `{"success": true, "data": {...}}`
- 失敗 → `{"success": false, "error": "...", "retry_hint": "..."}`

這個 JSON 外形只是應用程式約定，不是所有 API 的強制格式。程式仍要處理模型忽略錯誤、反覆重試或提早停止的情況。

---

## Schema 演進的小建議

- 加參數先確認供應商規則：一般 schema 可加 optional + default；OpenAI strict mode 則要把欄位列為 required，並用 `null` 表示可省略
- 改參數含義 → 開新 tool（`get_weather_v2`），舊的標 deprecated 一段時間再下
- description 改了要重新跑同一組 eval；不要假設文字小改一定沒有行為差異
- 上 production 前用 [promptfoo](https://github.com/promptfoo/promptfoo) eval 一下「LLM 在 5-10 個典型 query 是否選對 tool」

---

## 延伸閱讀

- [Anthropic — Define Tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) — 官方 schema 與 description 指南
- [Anthropic — Handle Tool Calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) — Tool Result 與 `is_error`
- [OpenAI — Function Calling](https://developers.openai.com/api/docs/guides/function-calling) — strict mode 與 function schema 規格
- [Stage 3 — Tool Use & Agent 入門](../stages/03-tool-use-and-hello-agent.md) — 主要動手練習
- [Stage 5.2 — MCP 基礎](../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎) — MCP server 也使用 tool schema，但 host、權限與協定層不同

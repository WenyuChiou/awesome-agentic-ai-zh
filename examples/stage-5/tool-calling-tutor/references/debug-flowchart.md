# Debug Flowchart：「為什麼 LLM 不呼叫我的 tool」

> **繁體中文** | [简体中文](./debug-flowchart.zh-Hans.md) | [English](./debug-flowchart.en.md)

> 先看症狀，再做最小檢查。對應 `SKILL.md` Step 2。

## Section A — Symptom (a)：LLM 完全不觸發 tool_calls

LLM 看到了 `tools=[...]`，卻只回文字。先逐項確認：

```text
[ ] finish_reason 是 "tool_calls" 還是 "stop"？
[ ] message.tool_calls 是空的嗎？
[ ] user 的問題真的需要外部工具嗎？
[ ] 送出的 tool schema 符合目前 SDK 的格式嗎？
```

### 先檢查這 5 項

#### 1. `description` 太模糊

```python
# ❌ 看不出何時用
{"name": "get_data", "description": "Get data."}

# ✅ 說清楚使用時機
{"name": "get_weather", "description": "Use this when the user asks about current weather, forecasts, or temperatures for a city."}
```

#### 2. 多個 tool 的工作重疊

```python
# ❌ search 和 lookup 看起來一樣
{"name": "search", "description": "Find information."}
{"name": "lookup", "description": "Look up data."}

# ✅ 各自說清楚能做與不能做的事
{"name": "web_search", "description": "Use for current external information. Do not use for facts already provided by the user."}
{"name": "fact_lookup", "description": "Use for stored facts. Do not use for live news or prices."}
```

#### 3. 問題根本不需要 tool

「什麼是 Python？」通常不需要天氣或計算工具。沒有 tool call 不一定是 bug。

#### 4. Schema 結構不符合 SDK

OpenAI-compatible 格式需要 `{"type": "function", "function": {...}}`；Anthropic 格式使用 `input_schema`。不同 client 的驗證與錯誤行為可能不同，所以要檢查實際送出的 request、收到的 response 與應用程式 log。

#### 5. 目前組合沒有可用的 tool-calling 支援

查目前 SDK 與 model 的官方文件，再用一個**固定小測試（fixture）**確認。它像每次都考同一道題。比較時保持 model、設定和問題不變；不要只看 model 名稱或大小猜結果。

## Section B — Symptom (b)：tool 被呼叫，但 args 錯

```python
# 預期
convert_temperature(value=32, unit="celsius")

# 可能收到
convert_temperature(value="32 Celsius", unit="")
```

| 看到的問題 | Schema 修法 | 程式仍要做什麼 |
|---|---|---|
| 數字變成文字 | `type: "number"` | 再檢查型別與範圍 |
| 少了欄位 | `required` | 缺值時回傳清楚錯誤 |
| 同一單位有多種寫法 | `enum` | 只接受 allowlist 內的值 |

完整例子見 [`schema-evolution.md`](schema-evolution.md)。

## Section C — Symptom (c)：ReAct loop 跑不停

先檢查三件事：

1. 把完整 assistant response 接回 `messages`。
2. tool result 帶回正確的 `tool_call_id` 或 `tool_use_id`。
3. tool result 要自成一體，例如 `{"city":"Taipei","forecast":"rain"}`，不能只回 `"ok"`。

Loop 一定要有 `MAX_STEPS`。到上限時要停止並回報，不可無限重試。

## Section D — Symptom (d)：多步任務漏了一步

例如算完比例後，忘了再轉成百分比。可以這樣查：

1. 用固定案例記錄實際的 tool sequence。
2. 在 description 寫清楚順序，例如 `Call this last after dividing.`。
3. 要求一份短而可檢查的工具計畫，只列步驟與工具名稱；不要要求、保存或揭露模型的隱藏推理。

可跑的多步範例：[Stage 3 multi-step reasoning](https://github.com/WenyuChiou/awesome-agentic-ai-zh/tree/main/examples/stage-3/04-multi-step-reasoning)。

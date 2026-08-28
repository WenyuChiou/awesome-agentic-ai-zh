# Schema Evolution：把模糊 schema 一步步變清楚

> **繁體中文** | [简体中文](./schema-evolution.zh-Hans.md) | [English](./schema-evolution.en.md)

> 同一個溫度轉換工具，分四步修好。Schema 幫模型填表，程式仍必須驗證每個值。

## Iteration 0：原始壞 schema

```python
{
    "name": "convert",
    "description": "Convert a value.",
    "parameters": {
        "type": "object",
        "properties": {
            "value": {"type": "string"},
            "unit": {"type": "string"}
        }
    }
}
```

這份 schema 有四個問題：工作說不清楚、數字被當成文字、欄位可漏掉、單位寫法沒有限制。

固定用「Convert 32 Celsius to Fahrenheit」測試，記錄：有沒有呼叫 tool、args 能不能解析、型別是否正確、必填欄位是否存在、值是否通過程式驗證。

## Iteration 1：說清楚何時使用

```python
"description": "Use this when the user asks to convert temperatures between Fahrenheit and Celsius."
```

這一步縮小工具的工作邊界，但還沒限制 args。

## Iteration 2：使用正確型別

```python
"value": {
    "type": "number",
    "description": "Temperature value to convert"
}
```

`value` 現在應該是數字。程式仍要拒絕 `NaN`、不合理範圍或其他錯誤輸入。

## Iteration 3：標出必填欄位

```python
"required": ["value", "unit"]
```

這告訴模型兩個欄位都要填。程式仍要處理缺值，不能直接執行。

## Iteration 4：限制可接受的值

```python
"unit": {
    "type": "string",
    "enum": ["celsius", "fahrenheit"],
    "description": "Unit of the input value"
}
```

### 最終 schema

```python
{
    "name": "convert_temperature",
    "description": "Use this when the user asks to convert temperatures between Fahrenheit and Celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "value": {"type": "number", "description": "Temperature value to convert"},
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Unit of the input value"
            }
        },
        "required": ["value", "unit"],
        "additionalProperties": false
    }
}
```

## 四步各自解決什麼

| 步驟 | 加入的約束 | 消除的模糊處 |
|---|---|---|
| 1 | 清楚的 `description` | 何時該用這個 tool |
| 2 | `type: number` | 數字是不是文字 |
| 3 | `required` | 哪些欄位不能少 |
| 4 | `enum`、`additionalProperties: false` | 可以填哪些值、能不能多塞欄位 |

## 怎麼做公平的本機檢查

1. 先固定案例集、model 版本、temperature、tool choice 和 SDK 版本。
2. 每個案例跑多次，記錄原始 response，不只看最後答案。
3. 分開計算「有 tool call」「JSON 可解析」「args 通過程式驗證」。
4. 結果只代表這份案例與設定，不可變成所有 model 都適用的保證。

**結論**：更清楚的 schema 會少一點猜測，但 model 輸出仍是不可信輸入。先驗證，再呼叫真正的工具。

完整可跑版本：[Stage 3 schema design](https://github.com/WenyuChiou/awesome-agentic-ai-zh/tree/main/examples/stage-3/06-schema-design)，包含 bad/good starter 與三語 README。

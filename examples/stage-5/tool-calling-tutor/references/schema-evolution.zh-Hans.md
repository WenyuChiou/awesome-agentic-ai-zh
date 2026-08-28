# Schema Evolution：把模糊 schema 一步步变清楚

> [繁體中文](./schema-evolution.md) | **简体中文** | [English](./schema-evolution.en.md)

> 同一个温度转换工具，分四步修好。Schema 帮 model 填表，程序仍必须验证每个值。

## Iteration 0：原始坏 schema

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

这份 schema 有四个问题：工作说不清楚、数字被当成文字、字段可漏掉、单位写法没有限制。

固定用“Convert 32 Celsius to Fahrenheit”测试，记录：有没有调用 tool、args 能不能解析、类型是否正确、必填字段是否存在、值是否通过程序验证。

## Iteration 1：说清楚何时使用

```python
"description": "Use this when the user asks to convert temperatures between Fahrenheit and Celsius."
```

这一步缩小工具的工作边界，但还没有限制 args。

## Iteration 2：使用正确类型

```python
"value": {
    "type": "number",
    "description": "Temperature value to convert"
}
```

`value` 现在应该是数字。程序仍要拒绝 `NaN`、不合理范围或其他错误输入。

## Iteration 3：标出必填字段

```python
"required": ["value", "unit"]
```

这告诉 model 两个字段都要填。程序仍要处理缺值，不能直接执行。

## Iteration 4：限制可接受的值

```python
"unit": {
    "type": "string",
    "enum": ["celsius", "fahrenheit"],
    "description": "Unit of the input value"
}
```

### 最终 schema

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

## 四步各自解决什么

| 步骤 | 加入的约束 | 消除的模糊处 |
|---|---|---|
| 1 | 清楚的 `description` | 何时该用这个 tool |
| 2 | `type: number` | 数字是不是文字 |
| 3 | `required` | 哪些字段不能少 |
| 4 | `enum`、`additionalProperties: false` | 可以填哪些值、能不能多放字段 |

## 怎样做公平的本机检查

1. 先固定案例集、model 版本、temperature、tool choice 和 SDK 版本。
2. 每个案例运行多次，记录原始 response，不只看最终答案。
3. 分开计算“有 tool call”“JSON 可解析”“args 通过程序验证”。
4. 结果只代表这份案例与设置，不可变成所有 model 都适用的保证。

**结论**：更清楚的 schema 会少一点猜测，但 model 输出仍是不可信输入。先验证，再调用真正的工具。

完整可运行版本：[Stage 3 schema design](https://github.com/WenyuChiou/awesome-agentic-ai-zh/tree/main/examples/stage-3/06-schema-design)，包含 bad/good starter 与三语 README。

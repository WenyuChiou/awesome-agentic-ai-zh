# Schema Evolution: make a vague schema clear, one step at a time

> [繁體中文](./schema-evolution.md) | [简体中文](./schema-evolution.zh-Hans.md) | **English**

> Repair the same temperature-conversion tool in four steps. A schema helps the model fill in a form; the application must still validate every value.

## Iteration 0: The broken schema

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

It has four problems: the job is vague, a number is treated as text, fields can be omitted, and unit values are unconstrained.

Use the fixed prompt “Convert 32 Celsius to Fahrenheit” and record: whether a tool was called, whether args parse, whether types are correct, whether required fields exist, and whether the application accepts the values.

## Iteration 1: say when to use it

```python
"description": "Use this when the user asks to convert temperatures between Fahrenheit and Celsius."
```

This narrows the tool’s job, but does not constrain the args yet.

## Iteration 2: use the correct type

```python
"value": {
    "type": "number",
    "description": "Temperature value to convert"
}
```

`value` should now be a number. The application must still reject `NaN`, unreasonable ranges, and other invalid inputs.

## Iteration 3: mark required fields

```python
"required": ["value", "unit"]
```

This tells the model that both fields are needed. The application must still handle missing values instead of executing them.

## Iteration 4: constrain accepted values

```python
"unit": {
    "type": "string",
    "enum": ["celsius", "fahrenheit"],
    "description": "Unit of the input value"
}
```

### Final schema

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

## What each step fixes

| Step | Constraint added | Ambiguity removed |
|---|---|---|
| 1 | Clear `description` | When to use the tool |
| 2 | `type: number` | Whether the number is text |
| 3 | `required` | Which fields may be omitted |
| 4 | `enum`, `additionalProperties: false` | Accepted values and extra fields |

## How to run a fair local check

1. Fix the case set, model version, temperature, tool choice, and SDK version.
2. Run each case more than once and save the raw response, not only the final answer.
3. Measure “tool called,” “JSON parsed,” and “args passed application validation” separately.
4. Treat results as evidence for that case set and configuration only, never as a guarantee for every model.

**Conclusion:** a clearer schema removes guesswork, but model output is still untrusted input. Validate it before calling a real tool.

Runnable version: [Stage 3 schema design](https://github.com/WenyuChiou/awesome-agentic-ai-zh/tree/main/examples/stage-3/06-schema-design), with bad/good starters and trilingual READMEs.

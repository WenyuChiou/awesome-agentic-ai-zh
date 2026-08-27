"""Stage 3 練習 6 自我驗證 — Path B（Anthropic starter_*_anthropic.py）。

跑法：
    python test_anthropic.py

用 mock 取代 Anthropic client、不打真 API、$0/run。
Ollama 版本見 test.py（OpenAI-compat shape）。
"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import starter_bad_anthropic as bad
import starter_good_anthropic as good


def block_text(text: str):
    return SimpleNamespace(type="text", text=text)


def block_tool_use(tool_id: str, name: str, inp: dict):
    return SimpleNamespace(type="tool_use", id=tool_id, name=name, input=inp)


def make_resp(stop_reason: str, *blocks):
    return SimpleNamespace(stop_reason=stop_reason, content=list(blocks))


def test_bad_schema_can_select_wrong_tool():
    client = MagicMock()
    client.messages.create.return_value = make_resp(
        "tool_use",
        block_text("The schemas are vague, so I will process the text."),
        block_tool_use("t1", "process_data", {"data": "32 Celsius to Fahrenheit"}),
    )
    result = bad.select_and_run("Convert 32 Celsius to Fahrenheit.", client=client)
    assert result["tool"] == "process_data"
    assert "processed generic data" in result["observation"]


def test_good_schema_selects_temperature_tool():
    client = MagicMock()
    client.messages.create.return_value = make_resp(
        "tool_use",
        block_text("This is clearly a temperature conversion."),
        block_tool_use("t1", "convert_temperature", {"value": 32, "unit": "celsius"}),
    )
    result = good.select_and_run("Convert 32 Celsius to Fahrenheit.", client=client)
    assert result["tool"] == "convert_temperature"
    assert result["observation"] == {"value": 89.6, "unit": "fahrenheit"}


def test_good_schema_has_required_fields_and_enum():
    bad_temp = next(tool for tool in bad.TOOLS_SPEC if tool["name"] == "convert_temperature")
    good_temp = next(tool for tool in good.TOOLS_SPEC if tool["name"] == "convert_temperature")
    assert "required" not in bad_temp["input_schema"]
    assert good_temp["input_schema"]["required"] == ["value", "unit"]
    assert good_temp["input_schema"]["properties"]["unit"]["enum"] == ["celsius", "fahrenheit"]
    assert good_temp["input_schema"]["additionalProperties"] is False


def test_application_rejects_untrusted_calls_for_both_schemas():
    _, bad_unknown = bad.execute_tool("delete_everything", {})
    _, good_wrong_shape = good.execute_tool("convert_temperature", [32, "celsius"])
    _, good_missing = good.execute_tool("convert_temperature", {"value": 32})
    _, bad_missing = bad.execute_tool("convert_temperature", {"value": "32"})
    _, bad_unit = bad.execute_tool(
        "convert_temperature", {"value": "32", "unit": "kelvin-ish"}
    )
    _, bad_extra = bad.execute_tool("process_data", {"data": "rows", "unexpected": "x"})
    _, bad_wrong_type = bad.execute_tool("process_data", {"data": 42})
    _, good_extra = good.execute_tool("convert_temperature", {"value": 32, "unit": "celsius", "unexpected": 1})
    _, good_wrong_type = good.execute_tool("convert_temperature", {"value": True, "unit": "celsius"})
    _, good_bad_rows = good.execute_tool("process_data", {"data": ["row"], "operation": "count_rows"})
    _, good_bad_operation = good.execute_tool("process_data", {"data": [], "operation": "delete_rows"})
    assert bad_unknown["error"] == "tool not allowed"
    assert good_wrong_shape["error"] == "arguments must be an object"
    assert good_missing["error"] == "arguments contain unexpected or missing fields"
    assert bad_missing["error"] == "arguments contain unexpected or missing fields"
    assert bad_unit["error"] == "unit must be celsius or fahrenheit"
    assert bad_extra["error"] == "arguments contain unexpected or missing fields"
    assert bad_wrong_type["error"] == "data must be a non-empty string"
    assert good_extra["error"] == "arguments contain unexpected or missing fields"
    assert good_wrong_type["error"] == "value must be a number"
    assert good_bad_rows["error"] == "data must be a list of objects"
    assert good_bad_operation["error"] == "operation must be count_rows or list_columns"


def test_multiple_calls_are_not_partially_executed():
    client = MagicMock()
    client.messages.create.return_value = make_resp(
        "tool_use",
        block_tool_use("t1", "convert_temperature", {"value": 32, "unit": "celsius"}),
        block_tool_use("t2", "process_data", {"data": [], "operation": "count_rows"}),
    )
    result = good.select_and_run("Do both", client=client)
    assert result["tool"] is None
    assert "expected one" in result["observation"]["error"]


if __name__ == "__main__":
    test_bad_schema_can_select_wrong_tool()
    test_good_schema_selects_temperature_tool()
    test_good_schema_has_required_fields_and_enum()
    test_application_rejects_untrusted_calls_for_both_schemas()
    test_multiple_calls_are_not_partially_executed()
    print("all pass")

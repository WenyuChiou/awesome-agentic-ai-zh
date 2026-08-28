"""Path B 離線行為測試：不呼叫模型，也不執行模型產生的程式碼。"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import run_json_tool_call
from starter_anthropic import MODEL, make_anthropic_model


def test_litellm_provider_configuration() -> None:
    model = make_anthropic_model()
    assert MODEL == "anthropic/claude-haiku-4-5-20251001"
    assert model.model_id == MODEL


def test_anthropic_path_uses_the_same_safe_json_boundary() -> None:
    assert run_json_tool_call({"name": "calculator", "arguments": {"expression": "8 / 2"}}) == "4.0"
    try:
        run_json_tool_call({"name": "shell", "arguments": {"command": "whoami"}})
    except ValueError:
        pass
    else:
        raise AssertionError("Unexpected tool names must be rejected.")


if __name__ == "__main__":
    test_litellm_provider_configuration()
    test_anthropic_path_uses_the_same_safe_json_boundary()
    print("all pass")

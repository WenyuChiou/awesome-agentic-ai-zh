"""Path A 離線行為測試：不呼叫 CodeAgent.run，也不執行模型程式碼。"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import MAX_NUMBER, codeact_executor_config, evaluate_arithmetic, run_json_tool_call


def test_json_tool_and_ast_evaluator() -> None:
    assert run_json_tool_call({"name": "calculator", "arguments": {"expression": "2 + 3 * (4 - 1)"}}) == "11.0"
    assert evaluate_arithmetic("-4 / 2") == -2.0


def test_ast_guards_reject_code_and_unsafe_values() -> None:
    for expression in ("__import__('os')", "2 / 0", f"{MAX_NUMBER + 1}"):
        try:
            evaluate_arithmetic(expression)
        except (SyntaxError, ValueError):
            pass
        else:
            raise AssertionError(f"Expected guarded evaluator to reject {expression!r}")


def test_codeact_uses_loopback_control_and_limits() -> None:
    config = codeact_executor_config()
    assert "additional_imports" not in config
    assert config["allow_pickle"] is False
    assert config["host"] == "127.0.0.1"
    assert config["container_run_kwargs"]["network_mode"] == "bridge"
    assert config["container_run_kwargs"]["cap_drop"] == ["ALL"]
    assert config["container_run_kwargs"]["security_opt"] == ["no-new-privileges"]


if __name__ == "__main__":
    test_json_tool_and_ast_evaluator()
    test_ast_guards_reject_code_and_unsafe_values()
    test_codeact_uses_loopback_control_and_limits()
    print("all pass")

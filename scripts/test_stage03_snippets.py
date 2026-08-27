#!/usr/bin/env python3
"""Regression tests for the runnable Stage 03 Markdown snippets."""

from __future__ import annotations

import ast
import re
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).parent.parent
STAGE_FILES = (
    ROOT / "stages" / "03-tool-use-and-hello-agent.md",
    ROOT / "stages" / "03-tool-use-and-hello-agent.en.md",
    ROOT / "stages" / "03-tool-use-and-hello-agent.zh-Hans.md",
)
PYTHON_FENCE_RE = re.compile(r"```python\n(.*?)```", re.DOTALL)


def _block_with(path: Path, needle: str) -> str:
    blocks = PYTHON_FENCE_RE.findall(path.read_text(encoding="utf-8"))
    matches = [block for block in blocks if needle in block]
    assert len(matches) == 1, f"{path}: expected one Python block containing {needle!r}"
    return matches[0]


def _ollama_argument_guard(source: str) -> ast.If:
    tree = ast.parse(source)
    matches = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.If)
        and "set(args)" in ast.unparse(node.test)
        and any(isinstance(child, ast.Raise) for child in ast.walk(node))
    ]
    assert len(matches) == 1, "expected one executable Ollama argument guard"
    return matches[0]


def _guard_rejects(guard: ast.If, args: object) -> bool:
    module = ast.fix_missing_locations(ast.Module(body=[guard], type_ignores=[]))
    try:
        exec(compile(module, "<stage03-weather-guard>", "exec"), {}, {"args": args})
    except ValueError:
        return True
    return False


def _anthropic_argument_guard(source: str) -> ast.If:
    tree = ast.parse(source)
    matches = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.If)
        and "set(block.input)" in ast.unparse(node.test)
        and any(isinstance(child, ast.Raise) for child in ast.walk(node))
    ]
    assert len(matches) == 1, "expected one executable Anthropic argument guard"
    return matches[0]


def _anthropic_guard_rejects(guard: ast.If, args: object) -> bool:
    module = ast.fix_missing_locations(ast.Module(body=[guard], type_ignores=[]))
    block = SimpleNamespace(input=args)
    try:
        exec(compile(module, "<stage03-anthropic-weather-guard>", "exec"), {}, {"block": block})
    except ValueError:
        return True
    return False


@pytest.mark.parametrize("path", STAGE_FILES)
def test_ollama_weather_guard_rejects_malformed_arguments(path: Path) -> None:
    source = _block_with(path, 'base_url="http://localhost:11434/v1"')
    guard = _ollama_argument_guard(source)

    malformed = (
        ["Taipei", "celsius"],
        {"city": "Taipei"},
        {"city": "Taipei", "unit": "celsius", "extra": True},
        {"city": 123, "unit": "celsius"},
        {"city": "", "unit": "celsius"},
        {"city": "   ", "unit": "celsius"},
        {"city": "Taipei", "unit": "fahrenheit"},
    )
    for args in malformed:
        assert _guard_rejects(guard, args), f"{path}: accepted malformed args {args!r}"

    assert not _guard_rejects(guard, {"city": "Taipei", "unit": "celsius"})
    assert 'result = get_weather(args["city"], args["unit"])' in source
    assert "get_weather(**args)" not in source


@pytest.mark.parametrize("path", STAGE_FILES)
def test_anthropic_weather_guard_rejects_blank_city(path: Path) -> None:
    source = _block_with(path, "import anthropic")
    guard = _anthropic_argument_guard(source)

    malformed = (
        {},
        {"city": "Taipei", "extra": True},
        {"city": 123},
        {"city": ""},
        {"city": "   "},
    )
    for args in malformed:
        assert _anthropic_guard_rejects(guard, args), (
            f"{path}: accepted malformed Anthropic args {args!r}"
        )

    assert not _anthropic_guard_rejects(guard, {"city": "Taipei"})


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))

#!/usr/bin/env python3
"""Structural regressions for the six runnable Stage 03 exercise folders."""

from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path(__file__).parent.parent
STAGE3 = ROOT / "examples" / "stage-3"
EXAMPLE_INDEXES = (
    ROOT / "examples" / "README.md",
    ROOT / "examples" / "README.en.md",
    ROOT / "examples" / "README.zh-Hans.md",
)
FOLDERS = (
    "01-function-calling",
    "02-multi-tool-selection",
    "03-react-from-scratch",
    "04-multi-step-reasoning",
    "05-error-handling",
    "06-schema-design",
)
COMMON_FILES = {
    "README.md",
    "README.en.md",
    "README.zh-Hans.md",
    "requirements.txt",
    "test.py",
    "test_anthropic.py",
}
EXPECTED_REQUIREMENTS = (
    "openai>=3.5,<4",
    "anthropic>=1.1,<2",
)
FLOATING_HAIKU_RE = re.compile(r"claude-haiku-4-5(?!-20251001)")


def _folder(name: str) -> Path:
    return STAGE3 / name


def _starters(folder: Path) -> list[Path]:
    return sorted(folder.glob("starter*.py"))


def test_six_exercise_folders_and_dual_path_files_exist() -> None:
    actual = {path.name for path in STAGE3.iterdir() if path.is_dir()}
    assert actual == set(FOLDERS)
    for name in FOLDERS:
        folder = _folder(name)
        files = {path.name for path in folder.iterdir() if path.is_file()}
        assert COMMON_FILES <= files, f"{name}: missing {COMMON_FILES - files}"
        assert any(path.name == "starter.py" for path in _starters(folder)) or name == "06-schema-design"
        assert any("anthropic" in path.name for path in _starters(folder))


def test_requirements_use_verified_sdk_majors() -> None:
    for name in FOLDERS:
        lines = [
            line.split("#", 1)[0].strip()
            for line in (_folder(name) / "requirements.txt").read_text(encoding="utf-8").splitlines()
            if line.split("#", 1)[0].strip()
        ]
        assert tuple(lines) == EXPECTED_REQUIREMENTS, f"{name}: {lines}"


def test_starters_parse_and_keep_runtime_safety_contract() -> None:
    for name in FOLDERS:
        for path in _starters(_folder(name)):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            assert "sys.stdout.reconfigure" in source, f"{path}: missing cp950-safe stdout"
            assert "def execute_tool(" in source, f"{path}: missing validation boundary"
            assert len([node for node in ast.walk(tree) if isinstance(node, ast.Assert)]) >= 2, (
                f"{path}: starters need at least two live self-checks"
            )
            if "anthropic" in path.name:
                assert '"claude-haiku-4-5-20251001"' in source
                assert not FLOATING_HAIKU_RE.search(source)


def test_multi_turn_loops_distinguish_completion_from_truncation() -> None:
    for name in ("03-react-from-scratch", "04-multi-step-reasoning", "05-error-handling"):
        folder = _folder(name)
        ollama = (folder / "starter.py").read_text(encoding="utf-8")
        anthropic = (folder / "starter_anthropic.py").read_text(encoding="utf-8")
        assert "max_iter" in ollama and "terminal_reason" in ollama and '"length"' in ollama
        assert "max_iter" in anthropic and "terminal_reason" in anthropic and '"max_tokens"' in anthropic
        assert 'result_block["is_error"] = True' in anthropic


def test_arithmetic_and_schema_safety_regressions_are_locked() -> None:
    """Keep executable safety checks visible to the repository-level test suite."""
    for name in ("02-multi-tool-selection", "03-react-from-scratch"):
        for path in _starters(_folder(name)):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            called_names = {
                node.func.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            }
            assert not ({"eval", "exec"} & called_names), f"{path}: unsafe evaluator"
            for guard in (
                "MAX_EXPRESSION_LENGTH",
                "MAX_AST_NODES",
                "MAX_AST_DEPTH",
                "MAX_ABS_NUMBER",
            ):
                assert guard in source, f"{path}: missing {guard}"

    stage04 = _folder("04-multi-step-reasoning")
    for path in _starters(stage04):
        source = path.read_text(encoding="utf-8")
        for code in ("division_by_zero", "non_finite_number", "number_too_large"):
            assert code in source, f"{path}: missing {code}"
    ollama_test = (stage04 / "test.py").read_text(encoding="utf-8")
    anthropic_test = (stage04 / "test_anthropic.py").read_text(encoding="utf-8")
    assert "10 ** 399" in ollama_test and '"9" * 5000' in ollama_test
    assert "10 ** 399" in anthropic_test

    stage06 = _folder("06-schema-design")
    for path in (stage06 / "starter_bad.py", stage06 / "starter_bad_anthropic.py"):
        source = path.read_text(encoding="utf-8")
        assert "set(args) != expected" in source
        assert "unit must be celsius or fahrenheit" in source
    for path in (stage06 / "test.py", stage06 / "test_anthropic.py"):
        source = path.read_text(encoding="utf-8")
        assert "bad_missing" in source and "kelvin-ish" in source


def test_readmes_use_current_commands_and_verification_date() -> None:
    for name in FOLDERS:
        for locale in ("README.md", "README.en.md", "README.zh-Hans.md"):
            path = _folder(name) / locale
            text = path.read_text(encoding="utf-8")
            assert "2026-08-27" in text, f"{path}: missing verification date"
            command = (
                "python starter_good_anthropic.py"
                if name == "06-schema-design"
                else "python starter_anthropic.py"
            )
            assert command in text
            assert "$env:ANTHROPIC_API_KEY" in text
            assert "export ANTHROPIC_API_KEY=sk-ant-" not in text
            assert not FLOATING_HAIKU_RE.search(text), f"{path}: floating Haiku alias"
            assert '<div align="right">' in text, f"{path}: missing language switcher"
            sibling_links = {
                "README.md": ("README.en.md", "README.zh-Hans.md"),
                "README.en.md": ("README.md", "README.zh-Hans.md"),
                "README.zh-Hans.md": ("README.md", "README.en.md"),
            }
            assert all(target in text for target in sibling_links[locale])
            assert "📚" in text, f"{path}: missing depth route"
            if name == "01-function-calling":
                assert text.rstrip().splitlines()[-3].startswith("> - [`datawhalechina/hello-agents`")
                assert "github.com/anthropics/claude-cookbooks/tree/main/tool_use" in text


def test_example_indexes_use_progressive_and_measurable_estimates() -> None:
    unsupported_totals = ("~30 hr", "~10 hr", "~8 hr", "$30-80", "$3 | $15")
    for path in EXAMPLE_INDEXES:
        text = path.read_text(encoding="utf-8")
        assert text.count('<details markdown="1">') >= 2
        assert '<details markdown="1" open>' not in text
        assert re.search(r"claude-sonnet-5.*\| \$2 \| \$10 \|", text)
        assert all(value not in text for value in unsupported_totals), path

    for path in (EXAMPLE_INDEXES[0], EXAMPLE_INDEXES[2]):
        text = path.read_text(encoding="utf-8")
        assert "behavior varies" not in text
        assert "run the folder evals" not in text


if __name__ == "__main__":
    raise SystemExit(__import__("pytest").main([__file__]))

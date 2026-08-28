"""Regression checks for the installable Stage 05 tutor skill."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
TUTOR = ROOT / "examples/stage-5/tool-calling-tutor"
READMES = (
    TUTOR / "README.md",
    TUTOR / "README.en.md",
    TUTOR / "README.zh-Hans.md",
)
SKILLS = (
    TUTOR / "SKILL.md",
    TUTOR / "translations/SKILL.en.md",
    TUTOR / "translations/SKILL.zh-Hans.md",
)
REFERENCES = tuple(sorted((TUTOR / "references").glob("*.md")))
LOCALIZED_REFERENCE = {
    SKILLS[0]: ("debug-flowchart.md", "schema-evolution.md", "sdk-diff.md"),
    SKILLS[1]: ("debug-flowchart.en.md", "schema-evolution.en.md", "sdk-diff.en.md"),
    SKILLS[2]: (
        "debug-flowchart.zh-Hans.md",
        "schema-evolution.zh-Hans.md",
        "sdk-diff.zh-Hans.md",
    ),
}
README_SKILL = dict(zip(READMES, SKILLS, strict=True))


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    raw = text.split("---\n", 2)[1]
    data = yaml.safe_load(raw)
    assert isinstance(data, dict)
    return data


def relative_markdown_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    links = re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text)
    return [
        link.split("#", 1)[0]
        for link in links
        if link
        and not link.startswith(
            ("http://", "https://", "#", "${CLAUDE_SKILL_DIR}")
        )
    ]


def powershell_blocks(path: Path) -> list[str]:
    return re.findall(
        r"```powershell\s*\n(.*?)```",
        path.read_text(encoding="utf-8"),
        flags=re.DOTALL,
    )


def test_offline_eval_contract_executes() -> None:
    result = subprocess.run(
        [sys.executable, str(TUTOR / "evals/check_evals.py")],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS: 5/5" in result.stdout


def test_eval_fixture_has_one_case_per_route() -> None:
    data = json.loads((TUTOR / "evals/evals.json").read_text(encoding="utf-8"))
    assert data["schema_version"] == 1
    assert [case["expected_route"] for case in data["cases"]] == [
        "a",
        "b",
        "c",
        "d",
        "away",
    ]
    assert "$schema" not in data
    assert "promptfoo" not in json.dumps(data).lower()


@pytest.mark.parametrize("skill", SKILLS)
def test_skill_frontmatter_and_installed_reference_paths(skill: Path) -> None:
    data = frontmatter(skill)
    assert data["name"] == "tool-calling-tutor"
    assert isinstance(data["description"], str)
    assert 40 <= len(data["description"]) <= 1024
    text = skill.read_text(encoding="utf-8")
    assert "../references/" not in text
    for reference in LOCALIZED_REFERENCE[skill]:
        assert f"${{CLAUDE_SKILL_DIR}}/references/{reference}" in text


@pytest.mark.parametrize("path", READMES + REFERENCES)
def test_relative_documentation_links_resolve(path: Path) -> None:
    for link in relative_markdown_links(path):
        assert (path.parent / link).resolve().exists(), f"{path}: missing {link}"


@pytest.mark.parametrize("readme", READMES)
def test_readme_has_copy_ready_install_and_honest_eval(readme: Path) -> None:
    text = readme.read_text(encoding="utf-8")
    assert text.index("```powershell") < text.index("```bash")
    assert "Copy-Item" in text and "-Recurse" in text
    assert "python evals/check_evals.py" in text
    assert "/tool-calling-tutor" in text
    assert "promptfoo eval -c evals/evals.json" not in text
    assert not re.search(r"<details[^>]*\bopen\b", text)
    openings = re.findall(r"^<details\b[^>]*>", text, flags=re.MULTILINE)
    assert openings == ['<details markdown="1">'] * 2


@pytest.mark.parametrize("readme", READMES)
def test_powershell_install_blocks_run_from_repo_root(
    readme: Path, tmp_path: Path
) -> None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if shell is None:
        pytest.skip("PowerShell is unavailable on this runner")

    blocks = powershell_blocks(readme)
    assert len(blocks) >= 2

    user_home = tmp_path / "home"
    user_home.mkdir()
    env = os.environ.copy()
    env["USERPROFILE"] = str(user_home)
    result = subprocess.run(
        [shell, "-NoProfile", "-NonInteractive", "-Command", blocks[0]],
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    user_target = user_home / ".claude/skills/tool-calling-tutor"
    assert (user_target / "SKILL.md").read_bytes() == README_SKILL[readme].read_bytes()
    assert (user_target / "references/debug-flowchart.md").is_file()
    assert (user_target / "evals/check_evals.py").is_file()

    temp_repo = tmp_path / "repo"
    tutor_copy = temp_repo / "examples/stage-5/tool-calling-tutor"
    tutor_copy.parent.mkdir(parents=True)
    shutil.copytree(TUTOR, tutor_copy)
    result = subprocess.run(
        [shell, "-NoProfile", "-NonInteractive", "-Command", blocks[1]],
        cwd=temp_repo,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    project_target = temp_repo / ".claude/skills/tool-calling-tutor"
    expected_copy = tutor_copy / README_SKILL[readme].relative_to(TUTOR)
    assert (project_target / "SKILL.md").read_bytes() == expected_copy.read_bytes()
    assert (project_target / "references/debug-flowchart.md").is_file()
    assert (project_target / "evals/check_evals.py").is_file()


def test_unsupported_benchmarks_and_hidden_reasoning_prompt_are_removed() -> None:
    text = "\n".join(
        path.read_text(encoding="utf-8") for path in SKILLS + REFERENCES + READMES
    )
    for stale in (
        "70%",
        "15%",
        "10%",
        "3%",
        "2%",
        "60%",
        "75%",
        "80%",
        "85%",
        "95%",
        "99%",
        "1000 runs",
        "1000 次",
        "promptfoo eval -c evals/evals.json",
        "add chain-of-thought prompt",
        "加 chain-of-thought prompt",
    ):
        assert stale.lower() not in text.lower()


@pytest.mark.parametrize(
    "reference", tuple(path for path in REFERENCES if "sdk-diff" in path.name)
)
def test_sdk_diff_keeps_application_safety_boundaries(reference: Path) -> None:
    text = reference.read_text(encoding="utf-8")
    assert "MAX_STEPS" in text
    assert "validate_args" in text
    assert "tool_call_id" in text
    assert "tool_use_id" in text
    assert 'finish_reason == "stop"' in text
    assert "unexpected finish_reason" in text

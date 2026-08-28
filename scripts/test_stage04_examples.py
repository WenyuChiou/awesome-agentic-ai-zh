"""Structural regression gate for the five current Stage 4 runnable examples."""

from __future__ import annotations

import ast
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "examples" / "stage-4"
README_NAMES = ("README.md", "README.en.md", "README.zh-Hans.md")
ENTRY_NAMES = ("starter.py", "starter_anthropic.py", "test.py", "test_anthropic.py")
SPECS = {
    "01-same-agent-two-frameworks": {
        "requirements": {
            "langgraph>=1.2,<2.0", "langchain-openai>=1.6,<2.0", "langchain-anthropic>=1.7,<2.0",
            "langchain-core>=1.6,<2.0", "crewai>=1.15,<2.0",
        },
        "primary_urls": {"https://docs.langchain.com/oss/python/langgraph/overview", "https://docs.crewai.com/", "https://platform.claude.com/docs/en/about-claude/pricing"},
        "literals": ("StateGraph", "Crew", "claude-haiku-4-5-20251001"),
        "budget_cap": "$0.05",
        "model_id": "claude-haiku-4-5-20251001",
    },
    "02-multi-agent-roles": {
        "requirements": {"crewai[anthropic]>=1.15,<2.0", "litellm>=1.98,<2.0"},
        "primary_urls": {"https://docs.crewai.com/", "https://docs.litellm.ai/", "https://platform.claude.com/docs/en/about-claude/pricing"},
        "literals": ("Process.sequential", "max_iter=4", "anthropic/claude-haiku-4-5-20251001"),
        "budget_cap": "$0.10",
        "model_id": "anthropic/claude-haiku-4-5-20251001",
    },
    "03-graph-workflow": {
        "requirements": {"langgraph>=1.2,<2.0", "langchain-core>=1.6,<2.0", "langchain-openai>=1.6,<2.0", "langchain-anthropic>=1.7,<2.0"},
        "primary_urls": {"https://docs.langchain.com/oss/python/langgraph/interrupts", "https://docs.langchain.com/oss/python/langgraph/persistence", "https://platform.claude.com/docs/en/about-claude/pricing"},
        "literals": ("interrupt(", "Command(resume", "ChatAnthropic", "thread_id"),
        "budget_cap": "$0.05",
        "model_id": "claude-haiku-4-5-20251001",
    },
    "04-codeact-vs-json-tool": {
        "requirements": {"smolagents[docker]>=1.26,<2.0", "litellm>=1.98,<2.0"},
        "primary_urls": {
            "https://huggingface.co/docs/smolagents/tutorials/secure_code_execution",
            "https://huggingface.co/docs/smolagents/reference/python_executors",
            "https://docs.docker.com/engine/network/port-publishing/",
            "https://platform.claude.com/docs/en/about-claude/pricing",
        },
        "literals": ("ast.parse", 'executor_type: str = "docker"', '"host": "127.0.0.1"', '"network_mode": "bridge"', '"cap_drop": ["ALL"]', '"no-new-privileges"', "max_steps=4", "anthropic/claude-haiku-4-5-20251001"),
        "budget_cap": "$0.10",
        "model_id": "anthropic/claude-haiku-4-5-20251001",
    },
    "05-typed-agent": {
        "requirements": {"pydantic-ai>=2.35,<3.0", "pydantic>=2.13,<3.0"},
        "primary_urls": {"https://ai.pydantic.dev/output/", "https://ai.pydantic.dev/testing/", "https://platform.claude.com/docs/en/about-claude/pricing"},
        "literals": ("output_type", "TestModel", "claude-haiku-4-5-20251001", "Field(min_length=1"),
        "budget_cap": "$0.05",
        "model_id": "claude-haiku-4-5-20251001",
    },
}
FORBIDDEN = (r"\beval\s*\(", r"\bexec\s*\(", r"pytest\.skip", r"api[- ]?drift.{0,32}(skip|fallback)")
README_FORBIDDEN = (
    "90%+", "50-70%", "10-30 秒", "30-90 秒", "效果差 10 倍", "一次過機率最高",
    "10-30s", "30-90s", "10× better", "highest one-shot", "cloud-quality",
    "production agent 必用", "Production 多 agent 系統幾乎必用", "production agents must use",
    "almost always use large models", "最穩", "最稳", "most stable", "interrupt_before", "update_state",
    "HfApiModel", "crew.kickoff(stream=True)", "**改成 streaming**：`crew.kickoff_for_each", "**Streaming**: `crew.kickoff_for_each",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def urls_in(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r"https?://[^)\s]+", text))


def test_stage_shape_and_dependencies() -> None:
    directories = {path.name for path in STAGE.iterdir() if path.is_dir()}
    require(directories == set(SPECS), f"Expected exactly {sorted(SPECS)}, found {sorted(directories)}")
    for name, spec in SPECS.items():
        folder = STAGE / name
        require(all((folder / entry).is_file() for entry in ENTRY_NAMES), f"{name}: missing required Python entry file")
        require(all((folder / readme).is_file() for readme in README_NAMES), f"{name}: missing README mirror")
        requirements = {line.strip() for line in (folder / "requirements.txt").read_text(encoding="utf-8").splitlines() if line.strip()}
        require(requirements == spec["requirements"], f"{name}: current-major requirements drifted: {requirements}")
    require((STAGE / "01-same-agent-two-frameworks" / "starter_crewai.py").is_file(), "exercise 1: CrewAI comparison starter missing")
    require((STAGE / "01-same-agent-two-frameworks" / "test_crewai.py").is_file(), "exercise 1: CrewAI comparison test missing")
    require((STAGE / "04-codeact-vs-json-tool" / "test_docker_smoke.py").is_file(), "exercise 4: daemon-gated Docker smoke test missing")


def test_python_safety_and_behavioral_entrypoints() -> None:
    for name, spec in SPECS.items():
        folder = STAGE / name
        all_python = list(folder.glob("*.py"))
        for path in all_python:
            text = path.read_text(encoding="utf-8")
            ast.parse(text, filename=str(path))
            for pattern in FORBIDDEN:
                require(not re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL), f"{path}: forbidden {pattern}")
        for test_name in ("test.py", "test_anthropic.py"):
            text = (folder / test_name).read_text(encoding="utf-8")
            require("def test_" in text and 'if __name__ == "__main__"' in text, f"{name}/{test_name}: needs a directly executable behavioral test")
            require("all pass" in text, f"{name}/{test_name}: must report a direct test result")
            require("importable" not in text.lower() and "loadable" not in text.lower(), f"{name}/{test_name}: import-only acceptance is not behavioral")
        starter_text = "\n".join((folder / entry).read_text(encoding="utf-8") for entry in ("starter.py", "starter_anthropic.py"))
        require(all(literal in starter_text or literal in "\n".join(path.read_text(encoding="utf-8") for path in all_python) for literal in spec["literals"]), f"{name}: missing required API or safety literal")


def test_readme_mirrors_and_reader_contract() -> None:
    for name, spec in SPECS.items():
        texts = [(STAGE / name / readme).read_text(encoding="utf-8") for readme in README_NAMES]
        canonical_urls = urls_in(texts[0])
        parity_values = ("Python 3.11", "$0", "$0.007", spec["budget_cap"], "2026-08-28 UTC", spec["model_id"])
        for readme, text in zip(README_NAMES, texts):
            require("py -3.11 -m venv .venv" in text, f"{name}/{readme}: Python 3.11 venv creation missing")
            require(r".\.venv\Scripts\python.exe -m pip install -r requirements.txt" in text, f"{name}/{readme}: PowerShell-first isolated install missing")
            require(text.index(r".\.venv\Scripts\python.exe -m pip install -r requirements.txt") < text.index(r".\.venv\Scripts\python.exe test.py"), f"{name}/{readme}: install must precede offline test")
            require(text.count(".venv") >= 5 and "requirements.txt" in text, f"{name}/{readme}: per-folder environment guidance missing")
            require("<details markdown=\"1\">" in text and "<details markdown=\"1\" open>" not in text, f"{name}/{readme}: details must be closed")
            require("<small>" in text and "2026-08-28 UTC" in text, f"{name}/{readme}: checked date must be inside the detail")
            require(all(value in text for value in parity_values), f"{name}/{readme}: budget/model parity drift")
            require(urls_in(text) == canonical_urls, f"{name}/{readme}: ordered URL mirror drift")
            require(spec["primary_urls"].issubset(set(urls_in(text))), f"{name}/{readme}: required primary source missing")
            require(not any(phrase in text for phrase in README_FORBIDDEN), f"{name}/{readme}: unsupported fixed-performance claim remains")
        require(all(texts[0].count(value) == text.count(value) for text in texts[1:] for value in parity_values), f"{name}: key number mirror parity drift")


def test_exercise_specific_reader_safety() -> None:
    all_text = "\n".join(path.read_text(encoding="utf-8") for path in STAGE.glob("*/README*.md"))
    require("interrupt_before" not in all_text and "update_state" not in all_text, "obsolete LangGraph HITL API remains")
    require("Command(resume=" in all_text and "interrupt()" in all_text, "current LangGraph HITL explanation missing")
    exercise1 = (STAGE / "01-same-agent-two-frameworks" / "starter.py").read_text(encoding="utf-8")
    require('name != "search"' in exercise1 and "Unknown tool" in exercise1, "exercise 1 must reject unknown tool names")
    codeact = (STAGE / "04-codeact-vs-json-tool" / "starter.py").read_text(encoding="utf-8")
    docker_smoke = (STAGE / "04-codeact-vs-json-tool" / "test_docker_smoke.py").read_text(encoding="utf-8")
    require("Docker" in all_text and '"host": "127.0.0.1"' in codeact and '"network_mode": "bridge"' in codeact, "CodeAct loopback control boundary missing")
    require('"network_mode": "none"' not in codeact, "Docker none network breaks Smolagents' host control channel")
    require("internal bridge" not in all_text.lower() and "internal network" not in all_text.lower(), "CodeAct must not claim unsupported internal-network isolation")
    require('"HostIp"' in docker_smoke and '"127.0.0.1"' in docker_smoke, "Docker smoke must inspect the real loopback port binding")
    require('"additional_imports"' not in codeact, "CodeAct must not duplicate DockerExecutor's positional additional_imports argument")
    locale_contracts = {
        "README.md": ("interrupt()", "Command(resume=", "Docker", "不能證明"),
        "README.en.md": ("interrupt()", "Command(resume=", "Docker", "does not prove"),
        "README.zh-Hans.md": ("interrupt()", "Command(resume=", "Docker", "不能证明"),
    }
    for readme, terms in locale_contracts.items():
        joined = "\n".join((STAGE / name / readme).read_text(encoding="utf-8") for name in SPECS)
        require(all(term in joined for term in terms), f"{readme}: HITL, CodeAct, or semantic-truth explanation drifted")


if __name__ == "__main__":
    test_stage_shape_and_dependencies()
    test_python_safety_and_behavioral_entrypoints()
    test_readme_mirrors_and_reader_contract()
    test_exercise_specific_reader_safety()
    print("Stage 4 structural gate: all pass")

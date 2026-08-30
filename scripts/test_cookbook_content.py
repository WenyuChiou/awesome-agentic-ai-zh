#!/usr/bin/env python3
"""Contract tests for the trilingual beginner Cookbook."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "zh-TW": ROOT / "resources" / "cookbook.md",
    "en": ROOT / "resources" / "cookbook.en.md",
    "zh-Hans": ROOT / "resources" / "cookbook.zh-Hans.md",
}

CORE_DEFINITION_LABELS = {
    "zh-TW": (
        "**Recipe（實作配方）**",
        "**Skill（操作卡）**",
        "**MCP Server（工具轉接站）**",
        "**Community Integration（社群整合）**",
        "**Model Runtime（模型執行環境）**",
        "**Coding Agent（程式代理）**",
    ),
    "en": tuple(
        f"**{term}**"
        for term in (
            "Recipe",
            "Skill",
            "MCP Server",
            "Community Integration",
            "Model Runtime",
            "Coding Agent",
        )
    ),
    "zh-Hans": (
        "**Recipe（实践配方）**",
        "**Skill（操作卡）**",
        "**MCP Server（工具转接站）**",
        "**Community Integration（社区集成）**",
        "**Model Runtime（模型运行环境）**",
        "**Coding Agent（程序代理）**",
    ),
}

RECIPE_PREFIXES = tuple(f"## {number}." for number in range(1, 7))
REQUIRED_LITERALS = (
    "2026-08-30",
    "from mcp.server import MCPServer",
    "Gemini Notebook",
    "http://localhost:23119/api/",
    "gemma4:e4b",
    "curl -fsSL https://opencode.ai/install | bash",
    "opencode",
    "ollama_chat/gemma4:e4b",
    "OpenRouter",
    "Pi",
    "https://github.com/anomalyco/opencode",
)
FORBIDDEN_LITERALS = (
    "from mcp.server.mcpserver import MCPServer",
    "local API is read-only",
    "local API 是 read-only",
    "npm install -g opencode-ai",
    "opencode auth login",
    "pip install aider-chat",
    "aider --model ollama/",
    "qwen2.5:3b",
    "https://github.com/sst/opencode",
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _visible_text(text: str) -> str:
    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.DOTALL)


def test_six_recipe_headings_and_first_actions_stay_visible() -> None:
    for locale, path in PAGES.items():
        visible = _visible_text(_text(path))
        for prefix in RECIPE_PREFIXES:
            assert prefix in visible, f"{locale}: {prefix} must stay outside details"
            start = visible.index(prefix)
            next_heading = re.search(r"(?m)^## ", visible[start + len(prefix) :])
            assert next_heading, f"{locale}: {prefix} must end before another H2"
            end = start + len(prefix) + next_heading.start()
            recipe = visible[start:end]
            assert "```bash" in recipe, f"{locale}: {prefix} needs a visible first action"
            assert re.search(r"\*\*(成果|Result)[:：]?\*\*", recipe), (
                f"{locale}: {prefix} needs a visible, checkable result"
            )


def test_core_terms_are_defined_at_their_first_visible_occurrence() -> None:
    for locale, path in PAGES.items():
        visible = _visible_text(_text(path))
        for definition in CORE_DEFINITION_LABELS[locale]:
            term = re.sub(r"^\*\*|\*\*$", "", definition).split("（", 1)[0]
            assert visible.index(term) == visible.index(definition) + 2, (
                f"{locale}: {term} must first appear in its bold definition"
            )


def test_secondary_steps_are_closed_by_default() -> None:
    for locale, path in PAGES.items():
        text = _text(path)
        assert text.count("<details markdown=\"1\">") == 9, locale
        assert text.count("<summary>") == 9, f"{locale}: every details block needs a label"
        assert text.count("</details>") == 9, f"{locale}: every details block must close"
        assert not re.search(r"<details\b[^>]*\bopen\b", text), locale


def test_restored_depth_stays_inside_the_progressive_path() -> None:
    required = (
        "~/.claude/skills/<name>/SKILL.md",
        "type hint",
        "docstring",
        "Streamable HTTP",
        "`docx`",
        "`xlsx`",
        "`pptx`",
        "`pdf`",
    )
    for locale, path in PAGES.items():
        text = _text(path)
        for literal in required:
            assert literal in text, f"{locale}: missing restored concept {literal!r}"


def test_current_commands_and_product_names_match_across_locales() -> None:
    for locale, path in PAGES.items():
        text = _text(path)
        for literal in REQUIRED_LITERALS:
            assert literal in text, f"{locale}: missing {literal!r}"
        for literal in FORBIDDEN_LITERALS:
            assert literal not in text, f"{locale}: stale instruction {literal!r}"


def test_visible_required_reading_and_project_ratings() -> None:
    for locale, path in PAGES.items():
        visible = _visible_text(_text(path))
        assert "⭐⭐⭐⭐⭐" in visible, f"{locale}: editorial ratings must stay visible"
        assert visible.count("https://") >= 16, f"{locale}: important links must stay visible"
        assert visible.count("rowspan=\"") == 6, f"{locale}: resource categories must be merged"


def test_freshness_marker_is_trilingual_and_canonical() -> None:
    marker = (
        "<!-- freshness: canonical=resources/cookbook.md; "
            "verified_on=2026-08-30; "
        "scope=skills,mcp,documents,gemini-notebook,zotero,local-runtime,cli-tools; "
        "max_age_days=90 -->"
    )
    for locale, path in PAGES.items():
        assert _text(path).count(marker) == 1, locale

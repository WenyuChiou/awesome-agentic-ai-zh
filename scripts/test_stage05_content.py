"""Regression checks for runnable Stage 05 documentation snippets."""

from __future__ import annotations

import io
import json
import re
import runpy
import sys
import types
from datetime import datetime
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    ROOT / "stages/05-claude-code-ecosystem.md",
    ROOT / "stages/05-claude-code-ecosystem.en.md",
    ROOT / "stages/05-claude-code-ecosystem.zh-Hans.md",
)


def _fence_after(text: str, marker: str, language: str) -> str:
    start = text.index(marker)
    match = re.search(
        rf"```{re.escape(language)}\r?\n(?P<body>.*?)\r?\n```",
        text[start:],
        flags=re.DOTALL,
    )
    assert match, f"missing {language} fence after {marker!r}"
    return match.group("body")


def _fence_containing(text: str, marker: str, language: str) -> str:
    blocks = re.findall(
        rf"```{re.escape(language)}\r?\n(.*?)\r?\n```",
        text,
        flags=re.DOTALL,
    )
    matches = [block for block in blocks if marker in block]
    assert len(matches) == 1, (
        f"expected one {language} fence containing {marker!r}; got {len(matches)}"
    )
    return matches[0]


def _hook_source(path: Path) -> str:
    return _fence_after(path.read_text(encoding="utf-8"), "log-tool.py", "python")


@pytest.mark.parametrize("page", PAGES)
def test_agent_sdk_message_handling_matches_current_python_types(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    assert "message.message.content" not in text
    source = _fence_containing(text, "from claude_agent_sdk import", "python")
    compile(source, f"{page.name}:agent-sdk", "exec")
    assert (
        "from claude_agent_sdk import AssistantMessage, "
        "ClaudeAgentOptions, TextBlock, query"
    ) in source
    assert "for block in message.content:" in source
    assert "if isinstance(block, TextBlock):" in source
    assert "print(block.text)" in source


def test_agent_sdk_snippet_prints_text_from_current_message_shape(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    sources = [
        _fence_containing(
            page.read_text(encoding="utf-8"),
            "from claude_agent_sdk import",
            "python",
        )
        for page in PAGES
    ]
    assert sources[0] == sources[1] == sources[2]

    class TextBlock:
        def __init__(self, text: str) -> None:
            self.text = text

    class AssistantMessage:
        def __init__(self, content: list[TextBlock]) -> None:
            self.content = content

    class ClaudeAgentOptions:
        def __init__(self, **kwargs: object) -> None:
            self.kwargs = kwargs

    async def query(**kwargs: object):
        assert kwargs["prompt"] == "Summarize this project without editing files."
        options = kwargs["options"]
        assert isinstance(options, ClaudeAgentOptions)
        assert options.kwargs == {"allowed_tools": ["Read", "Glob"]}
        yield AssistantMessage([TextBlock("ok")])

    fake_sdk = types.ModuleType("claude_agent_sdk")
    fake_sdk.AssistantMessage = AssistantMessage
    fake_sdk.ClaudeAgentOptions = ClaudeAgentOptions
    fake_sdk.TextBlock = TextBlock
    fake_sdk.query = query
    monkeypatch.setitem(sys.modules, "claude_agent_sdk", fake_sdk)

    script = tmp_path / "agent-sdk-snippet.py"
    script.write_text(sources[0], encoding="utf-8")
    runpy.run_path(str(script), run_name="__main__")

    assert capsys.readouterr().out == "ok\n"


def test_hook_code_and_settings_are_identical_in_all_locales() -> None:
    hook_sources = []
    settings = []
    for page in PAGES:
        text = page.read_text(encoding="utf-8")
        hook_sources.append(_hook_source(page))
        settings.append(json.loads(_fence_containing(text, '"PreToolUse"', "json")))

    assert len(set(hook_sources)) == 1
    assert settings[0] == settings[1] == settings[2]
    handler = settings[0]["hooks"]["PreToolUse"][0]
    assert handler["matcher"] == "Edit|Write"
    assert handler["hooks"] == [
        {
            "type": "command",
            "command": "python",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/log-tool.py"],
        }
    ]


def test_hook_logger_runs_and_records_only_safe_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    script = tmp_path / "log-tool.py"
    script.write_text(_hook_source(PAGES[0]), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "stdin",
        io.StringIO(
            json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "tool_input": {
                        "file_path": "secret.txt",
                        "content": "do-not-log-this",
                    },
                    "prompt": "do-not-log-this-either",
                }
            )
        ),
    )

    runpy.run_path(str(script), run_name="__main__")

    rows = (tmp_path / "events.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(rows) == 1
    record = json.loads(rows[0])
    assert set(record) == {"checked_at", "hook_event_name", "tool_name"}
    assert record["hook_event_name"] == "PreToolUse"
    assert record["tool_name"] == "Write"
    assert datetime.fromisoformat(record["checked_at"]).tzinfo is not None
    assert "secret.txt" not in rows[0]
    assert "do-not-log-this" not in rows[0]

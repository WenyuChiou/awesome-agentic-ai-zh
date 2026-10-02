#!/usr/bin/env python3
"""Keep the historical nested-fence explanation readable after parser updates."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path

import markdown

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


class _InlineContent(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.text: list[str] = []
        self.code: list[str] = []
        self._in_code = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "code":
            self._in_code = True
            self.code.append("")

    def handle_endtag(self, tag: str) -> None:
        if tag == "code":
            self._in_code = False

    def handle_data(self, data: str) -> None:
        self.text.append(data)
        if self._in_code:
            self.code[-1] += data


def _historical_sentence() -> _InlineContent:
    changelog = Path(__file__).resolve().parent.parent / "CHANGELOG.md"
    matches = [
        line for line in changelog.read_text(encoding="utf-8").splitlines()
        if "簡中版 style-guide 有大約 200 行在網站上根本沒顯示" in line
    ]
    assert len(matches) == 1
    content = _InlineContent()
    content.feed(markdown.markdown(matches[0], extensions=["pymdownx.superfences"]))
    return content


def test_historical_nested_fence_examples_render_literally() -> None:
    assert _historical_sentence().code == [
        "resources/style-guide.zh-Hans.md",
        r"\`\`\`bash",
        "```bash",
    ]


def test_historical_nested_fence_explanation_keeps_its_words() -> None:
    text = "".join(_historical_sentence().text)
    assert "(跳脫過),簡中是裸的" in text
    assert "於是內層 fence 提早關掉外層" in text
    assert "第 49 行到第 246 行" in text

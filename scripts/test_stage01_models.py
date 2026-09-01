from __future__ import annotations

import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    (ROOT / "stages" / "01-llm-basics.md", "Fable 5.1：正式可用", "Mythos 5.1：限核准使用者"),
    (ROOT / "stages" / "01-llm-basics.zh-Hans.md", "Fable 5.1：正式可用", "Mythos 5.1：限核准用户"),
    (ROOT / "stages" / "01-llm-basics.en.md", "Fable 5.1: generally available", "Mythos 5.1: vetted access only"),
)


@pytest.mark.parametrize(("page", "fable_status", "mythos_status"), PAGES)
def test_stage01_uses_current_fable_and_mythos_models(
    page: Path, fable_status: str, mythos_status: str
) -> None:
    text = page.read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if line.startswith("| Claude |"))
    cells = [cell.strip() for cell in row.strip("|").split("|")]

    assert len(cells) == 8
    assert "Fable 5.1" in cells[1]
    assert "Mythos 5.1" in cells[1]
    assert "claude-fable-5-1" in cells[1]
    assert "claude-mythos-5-1" in cells[1]
    assert fable_status in cells[2]
    assert mythos_status in cells[2]
    assert "1M" in cells[3]
    assert "128K" in cells[3]
    assert "$10/$50" in cells[4]
    assert "$0.25" in cells[4]
    assert "https://platform.claude.com/docs/en/models/fable-5-1/overview" in cells[7]
    assert "https://platform.claude.com/docs/en/models/mythos-5-1/overview" in cells[7]
    assert "claude-fable-5-1" in text
    assert "claude-mythos-5-1" in text
    assert not re.search(r"claude-(?:fable|mythos)-5(?!-1)", text)
    assert "verified_on=2026-09-01" in text

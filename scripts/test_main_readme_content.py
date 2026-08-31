"""Main README progressive-disclosure and trilingual route contracts."""

from __future__ import annotations

import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "zh-TW": ROOT / "README.md",
    "en": ROOT / "README.en.md",
    "zh-Hans": ROOT / "README.zh-Hans.md",
}

HEADINGS = {
    "zh-TW": (
        "## 🎯 這份地圖幫你做什麼？",
        "## 🚀 現在就開始",
        "## 從 Stage 0 到 Stage 8，另有 Stage 7.5 閱讀站",
        "## 💡 怎麼學才不容易卡住？",
        "## 📚 先收藏的學習入口",
    ),
    "en": (
        "## 🎯 What does this map help you do?",
        "## 🚀 Start now",
        "## Stage 0 through Stage 8, plus the Stage 7.5 reading stop",
        "## 💡 How do you learn without getting stuck?",
        "## 📚 Learning entrances to bookmark",
    ),
    "zh-Hans": (
        "## 🎯 这份地图帮你做什么？",
        "## 🚀 现在就开始",
        "## 从 Stage 0 到 Stage 8，另有 Stage 7.5 阅读站",
        "## 💡 怎么学才不容易卡住？",
        "## 📚 先收藏的学习入口",
    ),
}

ENTRY_BOUNDARIES = {
    "zh-TW": "走 Track A 或 Track B 前，先確認 Stage 0–2；只走日常使用者路線的人可以直接打開角色指南。",
    "en": "Before Track A or Track B, check Stage 0–2. If you only want everyday AI use, go straight to the role guide.",
    "zh-Hans": "走 Track A 或 Track B 前，先确认 Stage 0–2；只走日常用户路线的人可以直接打开角色指南。",
}
LANDING_PAGES = {
    "zh-TW": ROOT / "index.md",
    "en": ROOT / "index.en.md",
    "zh-Hans": ROOT / "index.zh-Hans.md",
}

AGENT_DEFINITION_MARKERS = {
    "zh-TW": (
        "能為了人的目標",
        "自己判斷下一步",
        "採取行動",
        "必要時使用工具",
        "依結果",
        "自動替人完成工作",
        "規則與權限",
        "把控制權交還給人",
        "只回答一次的聊天機器人",
        "每一步都固定寫好的腳本",
        "不一定是 Agent",
    ),
    "en": (
        "toward a person's goal",
        "decide what to do next",
        "take action",
        "chooses the next step",
        "uses tools when needed",
        "based on the result",
        "do work automatically",
        "rules and permissions",
        "hands control back",
        "one-shot chatbot",
        "fixed script",
        "not necessarily an Agent",
    ),
    "zh-Hans": (
        "能为了人的目标",
        "自己判断下一步",
        "采取行动",
        "需要时使用工具",
        "根据结果",
        "自动替人完成工作",
        "规则和权限",
        "把控制权交还给人",
        "只回答一次的聊天机器人",
        "每一步都预先固定好的脚本",
        "不一定是 Agent",
    ),
}
LANDING_AGENT_HEADINGS = {
    "zh-TW": "## 🤖 先懂一件事：AI Agent 是什麼？",
    "en": "## 🤖 First: what is an AI Agent?",
    "zh-Hans": "## 🤖 先懂一件事：AI Agent 是什么？",
}
LANDING_AGENT_MARKERS = {
    "zh-TW": (
        "能為了人的目標",
        "自己判斷下一步",
        "採取行動",
        "目前情況",
        "必要時使用工具",
        "依結果",
        "繼續",
        "修正",
        "停止",
        "把控制權交還給人",
        "自動替人完成工作",
        "規則與權限",
    ),
    "en": (
        "toward a person's goal",
        "decide what to do next",
        "take action",
        "current situation",
        "uses tools when needed",
        "based on the result",
        "continues",
        "corrects course",
        "stops",
        "hands control back",
        "do work automatically",
        "rules and permissions",
    ),
    "zh-Hans": (
        "能为了人的目标",
        "自己判断下一步",
        "采取行动",
        "当前情况",
        "需要时使用工具",
        "根据结果",
        "继续",
        "修正",
        "停止",
        "把控制权交还给人",
        "自动替人完成工作",
        "规则和权限",
    ),
}

TRACK_A_LINKS = (
    "tracks/cli/A1-cli-intro",
    "tracks/cli/A2-cli-workflow",
    "stages/05-claude-code-ecosystem",
    "tracks/cli/A3-cli-production",
    "stages/08-agent-interfaces",
)
TRACK_B_LINKS = (
    "stages/03-tool-use-and-hello-agent",
    "stages/04-agent-frameworks",
    "stages/05-claude-code-ecosystem",
    "stages/06-memory-rag",
    "stages/07-multi-agent-production",
    "stages/07.5-advanced-agentic-concepts",
    "stages/08-agent-interfaces",
)
ROLE_LINKS = (
    "branches/for-researcher",
    "branches/for-developer",
    "branches/for-teacher",
    "branches/for-knowledge-worker",
    "branches/for-everyday-users",
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _without_details(text: str) -> str:
    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.DOTALL)


def _section(text: str, start: str, end: str) -> str:
    begin = text.index(start)
    return text[begin : text.index(end, begin + len(start))]


def _normalized_internal_target(target: str) -> str:
    target = re.sub(r"\.(?:en|zh-Hans)(?=\.(?:md|png)(?:#|$))", "", target)
    return target.removeprefix("./")


def _rated_resource_links(text: str, heading: str) -> list[tuple[str, str]]:
    section = text[text.index(heading) :]
    next_heading = section.find("\n## ", len(heading))
    if next_heading != -1:
        section = section[:next_heading]
    rows = re.findall(
        r'<tr>.*?href="([^"]+)".*?<td>(⭐{4,5})</td>.*?</tr>',
        section,
        flags=re.DOTALL,
    )
    return [(_normalized_internal_target(target), rating) for target, rating in rows]


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_visible_mainline_keeps_reader_decisions_and_resources(locale: str, page: Path) -> None:
    text = _text(page)
    visible = _without_details(text)
    positions = [visible.index(heading) for heading in HEADINGS[locale]]
    assert positions == sorted(positions)
    assert ENTRY_BOUNDARIES[locale] in visible
    for term in ("**AI Agent**", "**Track A", "**Track B", "CAPSTONE", "PROGRESS"):
        assert term in visible
    for target in (*ROLE_LINKS, "resources/glossary", "resources/cookbook", "examples/README"):
        assert target in visible
    assert "<table>" in visible and "rowspan=" in visible


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_homepage_defines_an_agent_by_purpose_behavior_and_boundary(
    locale: str, page: Path
) -> None:
    text = _text(page)
    section = _section(text, HEADINGS[locale][0], HEADINGS[locale][1])
    assert "**AI Agent**" in section
    assert all(marker in section for marker in AGENT_DEFINITION_MARKERS[locale])


@pytest.mark.parametrize("locale,page", LANDING_PAGES.items())
def test_docs_landing_keeps_the_agent_definition_visible(locale: str, page: Path) -> None:
    visible = _without_details(_text(page))
    heading = LANDING_AGENT_HEADINGS[locale]
    section = _section(visible, heading, "## ")
    assert "**AI Agent**" in section
    assert all(marker in section for marker in LANDING_AGENT_MARKERS[locale])


@pytest.mark.parametrize("page", PAGES.values())
def test_only_secondary_homepage_information_is_collapsed(page: Path) -> None:
    text = _text(page)
    openings = re.findall(r'^<details markdown="1">$', text, flags=re.MULTILINE)
    assert len(openings) == 4
    assert not re.search(r"<details[^>]*\sopen(?:\s|>)", text)
    assert "git clone" not in _without_details(text)
    assert text.count("<details") == text.count("</details>") == 4


@pytest.mark.parametrize("page", PAGES.values())
def test_track_order_matches_the_canonical_curriculum(page: Path) -> None:
    visible = _without_details(_text(page))
    track_a = _section(visible, "### Track A", "### Track B")
    track_b = _section(visible, "### Track B", "### ")
    assert [track_a.index(link) for link in TRACK_A_LINKS] == sorted(
        track_a.index(link) for link in TRACK_A_LINKS
    )
    assert [track_b.index(link) for link in TRACK_B_LINKS] == sorted(
        track_b.index(link) for link in TRACK_B_LINKS
    )


@pytest.mark.parametrize("page", PAGES.values())
def test_curated_learning_table_is_visible_grouped_and_rated(page: Path) -> None:
    visible = _without_details(_text(page))
    assert re.findall(r'rowspan="(\d+)"', visible) == ["3", "3", "4"]
    rated_links = _rated_resource_links(visible, "## 📚")
    assert len(rated_links) == 10
    assert [rating for _, rating in rated_links] == [
        "⭐⭐⭐⭐⭐",
        "⭐⭐⭐⭐⭐",
        "⭐⭐⭐⭐",
        "⭐⭐⭐⭐⭐",
        "⭐⭐⭐⭐⭐",
        "⭐⭐⭐⭐",
        "⭐⭐⭐⭐⭐",
        "⭐⭐⭐⭐",
        "⭐⭐⭐⭐",
        "⭐⭐⭐⭐",
    ]
    assert "GitHub stars" in visible


def test_trilingual_links_and_stable_facts_match() -> None:
    texts = {locale: _text(path) for locale, path in PAGES.items()}
    internal = {}
    external = {}
    for locale, text in texts.items():
        targets = re.findall(r'(?:href=|\]\()["\']?([^"\') >]+)', text)
        internal[locale] = [
            _normalized_internal_target(target)
            for target in targets
            if not re.match(r"(?:https?:|mailto:|#)", target)
        ]
        external[locale] = [
            target for target in targets if re.match(r"https?://", target)
        ]
    assert internal["zh-TW"] == internal["en"] == internal["zh-Hans"]
    assert external["zh-TW"] == external["en"] == external["zh-Hans"]
    rated = {
        locale: _rated_resource_links(text, HEADINGS[locale][4])
        for locale, text in texts.items()
    }
    assert rated["zh-TW"] == rated["en"] == rated["zh-Hans"]


@pytest.mark.parametrize("page", PAGES.values())
def test_homepage_is_shorter_without_deleting_key_terms(page: Path) -> None:
    text = _text(page)
    # English naturally uses more characters than either CJK mirror. All three
    # stay well below their previous 16k–22k versions without rewarding terse,
    # under-explained translations.
    assert len(text) <= 14_000
    assert len(text.splitlines()) <= 230
    for banned in ("240+", "81+", "Agent Workflow Audit", "mv starter.py"):
        assert banned not in text
    for required in (
        "Zero-Shot",
        "One-Shot",
        "Few-Shot",
        "Workflow Graph",
        "MCP",
        "RAG",
        "Eval",
        "Human",
        "long-term memory",
        "contextual retrieval",
        "PAR loop",
        "agent-as-judge",
    ):
        assert required in text

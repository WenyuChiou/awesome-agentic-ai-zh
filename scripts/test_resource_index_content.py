"""Resource-hub reader path, grouping, and locale-mirror contracts."""

from __future__ import annotations

import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "zh-TW": ROOT / "resources/README.md",
    "en": ROOT / "resources/README.en.md",
    "zh-Hans": ROOT / "resources/README.zh-Hans.md",
}
PUBLIC_PAGES = {
    "zh-TW": ROOT / "RESOURCES.md",
    "en": ROOT / "RESOURCES.en.md",
    "zh-Hans": ROOT / "RESOURCES.zh-Hans.md",
}
REFERENCE_STEMS = (
    "setup-guide",
    "glossary",
    "cli-agents-guide",
    "courses",
    "cookbook",
    "schema-design-cheatsheet",
    "model-training-guide",
    "mcp-skills-catalog",
    "agent-paradigms",
    "subagent-cookbook",
    "subagent-advanced",
    "style-guide",
)
SUFFIXES = {"zh-TW": "", "en": ".en", "zh-Hans": ".zh-Hans"}
CORE_LABELS = {
    "zh-TW": (
        "Reference（參考資料）",
        "Guide（指南）",
        "Cookbook（食譜）",
        "Catalog（目錄）",
        "Glossary（詞典）",
    ),
    "en": ("Reference", "Guide", "Cookbook", "Catalog", "Glossary"),
    "zh-Hans": (
        "Reference（参考资料）",
        "Guide（指南）",
        "Cookbook（食谱）",
        "Catalog（目录）",
        "Glossary（词典）",
    ),
}
TOOL_ROUTER_ROWS = {
    "zh-TW": (
        "我分不清這四個名字：OpenRouter＝統一模型 API／router；"
        "Ollama＝本機模型 runtime；OpenCode／Pi＝coding agent／toolkit",
        "[`cli-agents-guide.md`](cli-agents-guide.md)",
    ),
    "en": (
        "I cannot tell these names apart: OpenRouter = unified model API/router; "
        "Ollama = local model runtime; OpenCode/Pi = coding agents/toolkits",
        "[`cli-agents-guide.en.md`](cli-agents-guide.en.md)",
    ),
    "zh-Hans": (
        "我分不清这四个名字：OpenRouter＝统一模型 API／router；"
        "Ollama＝本地模型 runtime；OpenCode／Pi＝coding agent／toolkit",
        "[`cli-agents-guide.zh-Hans.md`](cli-agents-guide.zh-Hans.md)",
    ),
}


def _without_details(text: str) -> str:
    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.DOTALL)


def _locale_neutral_href(href: str) -> str:
    return re.sub(r"\.(?:en|zh-Hans)(?=\.md(?:#.*)?$)", "", href)


@pytest.mark.parametrize("locale", PAGES)
def test_task_router_and_all_twelve_reference_entrances_stay_visible(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    suffix = SUFFIXES[locale]

    for stem in REFERENCE_STEMS:
        href = f'{stem}{suffix}.md'
        assert visible.count(f'({href})') + visible.count(f'href="{href}"') == 2

    for label in CORE_LABELS[locale]:
        assert f"**{label}**" in visible

    assert visible.index("## 🧭") < visible.index("## 🧩") < visible.index("## 📚")
    assert visible.index("## 📚") < visible.index("## 🔁") < visible.index("## ✅")


@pytest.mark.parametrize("locale", PAGES)
def test_tool_router_preserves_explicit_product_identity_mappings(locale: str) -> None:
    visible = _without_details(PAGES[locale].read_text(encoding="utf-8"))
    question, destination = TOOL_ROUTER_ROWS[locale]
    assert f"| {question} | {destination} |" in visible

    assert question.index("OpenRouter") < question.index("Ollama")
    assert question.index("Ollama") < question.index("OpenCode") < question.index("Pi")
    assert re.search(r"API[／/]router", question)
    assert "model runtime" in question or "模型 runtime" in question
    assert "coding agent" in question and "toolkit" in question


@pytest.mark.parametrize("locale", PAGES)
def test_reference_table_uses_five_real_rowgroups_without_empty_category_cells(
    locale: str,
) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    tables = re.findall(r"<table>.*?</table>", text, flags=re.DOTALL)
    assert len(tables) == 1
    table = tables[0]
    groups = re.findall(r"<tbody>(.*?)</tbody>", table, flags=re.DOTALL)
    assert len(groups) == 5

    for group, rows in zip(groups, (4, 2, 3, 2, 1), strict=True):
        assert len(re.findall(r"<tr>", group)) == rows
        assert group.count(f'scope="rowgroup" rowspan="{rows}"') == 1
        assert "<td></td>" not in group and "<th></th>" not in group


@pytest.mark.parametrize("page", PAGES.values())
def test_only_maintenance_depth_is_collapsed_and_stale_inventory_copy_is_gone(
    page: Path,
) -> None:
    text = page.read_text(encoding="utf-8")
    openings = re.findall(r"^<details\b[^>]*>", text, flags=re.MULTILINE)
    assert openings == ['<details markdown="1">'] * 2
    assert "<details open" not in text
    assert "NotebookLM" not in text
    assert re.search(r"~\s*\d+", text) is None
    assert "7 份 reference" not in text
    assert "7 references" not in text
    assert "7 份参考" not in text


def test_all_twelve_references_really_have_three_locale_files() -> None:
    for stem in REFERENCE_STEMS:
        for suffix in SUFFIXES.values():
            assert (ROOT / f"resources/{stem}{suffix}.md").is_file()


def test_public_router_keeps_ordered_destinations_and_ratings_in_locale_parity() -> None:
    signatures: dict[str, list[tuple[str, str]]] = {}
    for locale, page in PUBLIC_PAGES.items():
        visible = _without_details(page.read_text(encoding="utf-8"))
        router = visible.split("## 📌", 1)[1].split("<a id=", 1)[0]
        rows = re.findall(r"\[[^]]+\]\(([^)]+)\)\s*\|\s*(⭐+)\s*\|", router)
        signatures[locale] = [(_locale_neutral_href(href), rating) for href, rating in rows]

    assert signatures["en"] == signatures["zh-TW"]
    assert signatures["zh-Hans"] == signatures["zh-TW"]


def test_resource_hub_keeps_router_and_table_order_in_locale_parity() -> None:
    router_signatures: dict[str, list[str]] = {}
    table_signatures: dict[str, list[str]] = {}
    for locale, page in PAGES.items():
        visible = _without_details(page.read_text(encoding="utf-8"))
        router = visible.split("## 🧭", 1)[1].split("## 🧩", 1)[0]
        table = visible.split("## 📚", 1)[1].split("## 🔁", 1)[0]
        router_signatures[locale] = [
            _locale_neutral_href(href)
            for href in re.findall(r"\]\(([^)]+\.md)\)", router)
        ]
        table_signatures[locale] = [
            _locale_neutral_href(href)
            for href in re.findall(r'href="([^"]+\.md)"', table)
        ]

    assert router_signatures["en"] == router_signatures["zh-TW"]
    assert router_signatures["zh-Hans"] == router_signatures["zh-TW"]
    assert table_signatures["en"] == table_signatures["zh-TW"]
    assert table_signatures["zh-Hans"] == table_signatures["zh-TW"]

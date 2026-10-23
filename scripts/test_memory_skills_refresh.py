#!/usr/bin/env python3
"""Focused regressions for the 2026-10-15 Memory/Skills refresh."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parent.parent
MEMORY = (
    ROOT / "resources/agent-memory.md",
    ROOT / "resources/agent-memory.en.md",
    ROOT / "resources/agent-memory.zh-Hans.md",
)
CATALOG = (
    ROOT / "resources/mcp-skills-catalog.md",
    ROOT / "resources/mcp-skills-catalog.en.md",
    ROOT / "resources/mcp-skills-catalog.zh-Hans.md",
)
HINDSIGHT = "https://github.com/vectorize-io/hindsight"
OPENVIKING = "https://github.com/volcengine/OpenViking"
OPENVIKING_LICENSE = f"{OPENVIKING}/blob/main/LICENSE"
TENCENT_MEMORY = "https://github.com/TencentCloud/TencentDB-Agent-Memory"
TENCENT_REVIEWED_COMMIT = "e9a82935b52741e0c798c75326e90b7144eb4d5f"
VERCEL_SKILLS = "https://github.com/vercel-labs/skills"
REVIEWED_COMMIT = "13e4063a1cf913f5606d57d42ab83a86f5001e04"
VERCEL_COMMIT = f"{VERCEL_SKILLS}/commit/{REVIEWED_COMMIT}"
URL_RE = re.compile(r"https://[^\s)\"'>]+")


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tables: list[list[tuple[str, dict[str, str]]]] = []
        self._table: list[tuple[str, dict[str, str]]] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        normalized = {key: value or "" for key, value in attrs}
        if tag == "table":
            self._table = []
        if self._table is not None:
            self._table.append((tag, normalized))

    def handle_endtag(self, tag: str) -> None:
        if tag == "table" and self._table is not None:
            self.tables.append(self._table)
            self._table = None


def _body(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _rendered_tables(path: Path) -> list[list[tuple[str, dict[str, str]]]]:
    parser = _TableParser()
    parser.feed(markdown.markdown(_body(path), extensions=["tables", "md_in_html"]))
    return parser.tables


def _entry_urls(body: str, start: str, end: str) -> list[str]:
    section = body[body.index(start) : body.index(end, body.index(start))]
    return URL_RE.findall(section)


def test_memory_entries_have_equivalent_url_order_and_unique_repo_urls() -> None:
    for path in MEMORY:
        body = _body(path)
        assert _entry_urls(body, HINDSIGHT, "</tbody>") == [
            HINDSIGHT,
            OPENVIKING,
            TENCENT_MEMORY,
        ]
        assert OPENVIKING_LICENSE in body.split("</table>")[-1]
        assert body.count(HINDSIGHT) == 1
        assert body.count(OPENVIKING) == 2  # repo row plus the distinct LICENSE URL
        assert body.count(TENCENT_MEMORY) == 5  # row plus four pinned source links


def test_memory_table_keeps_a_real_eight_row_memory_group() -> None:
    for path in MEMORY:
        body = _body(path)
        assert re.search(
            r'<th scope="rowgroup" rowspan="8">Memory layer</th>', body
        )
        first_tbody = re.search(r"<tbody>(.*?)</tbody>", body, re.DOTALL)
        assert first_tbody is not None
        assert first_tbody.group(1).count("<tr>") == 8
        tables = _rendered_tables(path)
        assert any(
            tag == "th" and attrs == {"scope": "rowgroup", "rowspan": "8"}
            for table in tables
            for tag, attrs in table
        )


def test_tencent_memory_keeps_its_teaching_role_and_pinned_source_evidence() -> None:
    for path in MEMORY:
        body = _body(path)
        row = next(row for row in re.findall(r"<tr>.*?</tr>", body)
                   if f'href="{TENCENT_MEMORY}"' in row)
        assert all(term in row for term in ("Chat Memory", "Skill", "LLM-Wiki", "CodeGraph", "MIT", "SQLite"))
        for source in ("README.md", "LICENSE", "deploy/global-images/.env.example", "MemoryKnowledge/src/middleware/auth.ts"):
            assert f"{TENCENT_MEMORY}/blob/{TENCENT_REVIEWED_COMMIT}/{source}" in body


def test_hindsight_reflect_answers_from_memory_not_background_consolidation() -> None:
    expected = ("保存、搜尋、根據記憶推理並回答",
                "store, retrieve, and reason over memories to answer",
                "保存、检索、根据记忆推理并回答")
    for path, meaning in zip(MEMORY, expected):
        row = next(row for row in re.findall(r"<tr>.*?</tr>", _body(path))
                   if HINDSIGHT in row)
        assert meaning in row
        assert all(f"<code>{operation}</code>" in row
                   for operation in ("retain", "recall", "reflect"))


def test_memory_operations_have_natural_wrap_opportunities() -> None:
    for path in MEMORY:
        row = next(row for row in re.findall(r"<tr>.*?</tr>", _body(path))
                   if HINDSIGHT in row)
        assert re.search(r"<code>retain</code> [/／] <code>recall</code> [/／] <code>reflect</code>", row)


def test_memory_ratings_licenses_and_safety_boundaries_are_localized() -> None:
    requirements = {
        MEMORY[0]: ("⭐⭐⭐⭐", "⭐⭐⭐（進階）", "更新", "刪除", "隔離", "污染"),
        MEMORY[1]: ("⭐⭐⭐⭐", "⭐⭐⭐ (advanced)", "update", "deletion", "isolation", "poison"),
        MEMORY[2]: ("⭐⭐⭐⭐", "⭐⭐⭐（进阶）", "更新", "删除", "隔离", "污染"),
    }
    for path, terms in requirements.items():
        body = _body(path)
        assert all(term in body for term in terms)
        assert "MIT" in body and "AGPL-3.0" in body
        assert "2026-10-15 UTC" in body
        assert "2026-08-30" in body  # the page-wide older evidence was not freshened


def test_vercel_selection_table_is_visible_and_detail_is_closed() -> None:
    for path in CATALOG:
        body = _body(path)
        selection = body.index("[Vercel Skills](#vercel-skills)")
        first_details = body.index('<details markdown="1">')
        entry = body.index(f"[Vercel Skills]({VERCEL_SKILLS})")
        closing_details = body.index("</details>", entry)
        assert selection < first_details
        assert first_details < entry < closing_details
        assert body.count(VERCEL_SKILLS) == 2  # repo URL plus distinct commit URL
        assert body.count("(#vercel-skills)") == 1
        assert len(_rendered_tables(path)) >= 2


def test_vercel_entry_has_equivalent_sources_identity_and_limits() -> None:
    requirements = {
        CATALOG[0]: (
            "不是 MCP server 或模型",
            "安裝或更新不等於完成安全審查",
            "不保證每個 host 都支援",
            "匿名使用紀錄（usage telemetry）",
            "**CLI（命令列介面）**",
        ),
        CATALOG[1]: (
            "not an MCP Server or model",
            "not a safety review",
            "does not guarantee support in every host",
            "anonymous usage records (usage telemetry)",
            "**command-line interface (CLI)**",
        ),
        CATALOG[2]: (
            "不是 MCP server 或模型",
            "安装或更新不等于完成安全审查",
            "不保证每个 host 都支持",
            "匿名使用记录（usage telemetry）",
            "**CLI（命令行接口）**",
        ),
    }
    for path, terms in requirements.items():
        body = _body(path)
        assert _entry_urls(body, '<a id="vercel-skills"></a>', "\n---\n") == [
            VERCEL_SKILLS,
            VERCEL_COMMIT,
        ]
        assert all(term in body for term in terms)
        assert "MIT" in body and "⭐⭐⭐⭐" in body
        assert "npx skills find" in body and "`add`" in body and "`update`" in body
        assert "DISABLE_TELEMETRY=1" in body and "DO_NOT_TRACK=1" in body
        assert REVIEWED_COMMIT in body and "2026-10-15 UTC" in body

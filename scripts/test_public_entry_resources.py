#!/usr/bin/env python3
"""Regression tests for the public resource entry and MCP catalog layer."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]

_CATALOG_GATE_SPEC = importlib.util.spec_from_file_location(
    "check_catalog_counts_for_public_resources",
    ROOT / "scripts" / "check-catalog-counts.py",
)
catalog_gate = importlib.util.module_from_spec(_CATALOG_GATE_SPEC)
_CATALOG_GATE_SPEC.loader.exec_module(catalog_gate)

TRIOS = {
    "resources": {
        "zh-TW": ROOT / "RESOURCES.md",
        "en": ROOT / "RESOURCES.en.md",
        "zh-Hans": ROOT / "RESOURCES.zh-Hans.md",
    },
    "resource-index": {
        "zh-TW": ROOT / "resources" / "README.md",
        "en": ROOT / "resources" / "README.en.md",
        "zh-Hans": ROOT / "resources" / "README.zh-Hans.md",
    },
    "catalog": {
        "zh-TW": ROOT / "resources" / "mcp-skills-catalog.md",
        "en": ROOT / "resources" / "mcp-skills-catalog.en.md",
        "zh-Hans": ROOT / "resources" / "mcp-skills-catalog.zh-Hans.md",
    },
}

PUBLIC_FILES = tuple(path for trio in TRIOS.values() for path in trio.values())

OUTREACH_FILES = tuple(sorted((ROOT / ".github" / "outreach").glob("*.md")))

PUBLIC_TOTAL_FILES = PUBLIC_FILES + (
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / "README.zh-Hans.md",
    ROOT / ".github" / "outreach" / "awesome-mcp-servers.md",
) + OUTREACH_FILES

START_URLS = (
    "https://registry.modelcontextprotocol.io/",
    "https://github.com/modelcontextprotocol/servers",
    "https://github.com/anthropics/skills",
    "https://github.com/github/github-mcp-server",
    "https://github.com/datawhalechina/hello-agents",
)

HIGHLIGHT_PAIRS = (
    ("https://developers.notion.com/guides/mcp/overview", "⭐⭐⭐⭐⭐"),
    ("https://github.com/MarkusPfundstein/mcp-obsidian", "⭐⭐⭐⭐"),
    ("https://support.google.com/gemininotebook/answer/16164461", "⭐⭐⭐⭐⭐"),
    ("https://github.com/teng-lin/notebooklm-py", "⭐⭐⭐⭐"),
    ("https://github.com/anthropics/skills", "⭐⭐⭐⭐⭐"),
    ("https://github.com/tfriedel/claude-office-skills", "⭐⭐⭐⭐"),
    ("https://developers.google.com/workspace/guides/configure-mcp-servers", "⭐⭐⭐⭐"),
    ("https://github.com/github/github-mcp-server", "⭐⭐⭐⭐⭐"),
    (
        "https://support.atlassian.com/atlassian-rovo-mcp-server/docs/"
        "getting-started-with-the-atlassian-remote-mcp-server/",
        "⭐⭐⭐⭐⭐",
    ),
    ("https://linear.app/docs/mcp", "⭐⭐⭐⭐⭐"),
    ("https://docs.slack.dev/ai/mcp-overview/", "⭐⭐⭐⭐⭐"),
    ("https://github.com/WenyuChiou/ai-research-skills", "⭐⭐⭐⭐⭐"),
    ("https://github.com/WenyuChiou/research-hub", "⭐⭐⭐⭐⭐"),
    ("https://github.com/WenyuChiou/zotero-skills", "⭐⭐⭐⭐"),
    ("https://github.com/WenyuChiou/codex-delegate", "⭐⭐⭐⭐"),
    ("https://github.com/leemysw/feishu-docx", "⭐⭐⭐⭐"),
)

ROWGROUPS = (4, 3, 4, 4, 1)

INTEGRATION_FACTS = {
    "zh-TW": (
        "Developer Preview",
        "每個產品有獨立 server",
        "OAuth 2.0",
        "使用 OAuth 或最小權限 token",
        "OAuth 2.1",
        "Streamable HTTP",
        "read-only",
        "人工核准",
    ),
    "en": (
        "Developer Preview",
        "each product has a dedicated server",
        "OAuth 2.0",
        "use OAuth or a least-privilege token",
        "OAuth 2.1",
        "Streamable HTTP",
        "read-only",
        "human approval",
    ),
    "zh-Hans": (
        "Developer Preview",
        "每个产品都有专用 server",
        "OAuth 2.0",
        "使用 OAuth 或最小权限 token",
        "OAuth 2.1",
        "Streamable HTTP",
        "只读",
        "人工批准",
    ),
}

INDEX_MAINTENANCE_FACTS = {
    "zh-TW": (
        "zh-TW 是 canonical",
        "官方來源查證",
        "找不到時明寫未知",
        "GitHub stars、固定總數和行數",
    ),
    "en": (
        "zh-TW is canonical",
        "official sources",
        "If the answer is unknown",
        "GitHub stars, fixed totals, and line counts",
    ),
    "zh-Hans": (
        "zh-TW 是 canonical",
        "官方来源核实",
        "找不到时明确写未知",
        "GitHub stars、固定总数和行数",
    ),
}

TASK_TARGETS = (
    "stages/00-foundations",
    "resources/glossary",
    "resources/cli-agents-guide",
    "resources/mcp-skills-catalog",
    "resources/cookbook",
)

INDEX_TARGETS = (
    "glossary",
    "cli-agents-guide",
    "mcp-skills-catalog",
    "schema-design-cheatsheet",
    "cookbook",
    "setup-guide",
    "style-guide",
)

STALE_DEFAULTS = (
    "https://github.com/jerhadf/linear-mcp-server",
    "https://github.com/korotovsky/slack-mcp-server",
)

VOLATILE_CATALOG_CLAIMS = (
    r"every GitHub user|所有 GitHub 用户|所有 GitHub 使用者",
    r"most-installed|highest-starred|安装量最高|星星数最高",
    r"\b(?:97|1000)\+\b",
    r"\b158\s+(?:languages|种语言)\b",
    r"\b1M[- ]token|1M token|百万 token",
    r"last commit 20\d{2}",
    r"OpenAI Operator",
    r"zero install|0 安装",
    r"free for regular users|一般用户免费|一般使用者免費",
    r"Claude is bad|Codex is bad|Claude 不擅长|Claude 不擅長|Codex 不擅长|Codex 不擅長",
)


def _without_details(text: str) -> str:
    """Keep summaries visible while removing closed disclosure bodies."""
    out: list[str] = []
    cursor = 0
    pattern = re.compile(r"<details\b(?![^>]*\bopen\b)[^>]*>(.*?)</details>", re.DOTALL)
    for match in pattern.finditer(text):
        out.append(text[cursor : match.start()])
        summary = re.search(r"<summary>(.*?)</summary>", match.group(1), re.DOTALL)
        if summary:
            out.append(summary.group(1))
        cursor = match.end()
    out.append(text[cursor:])
    return "\n".join(out)


def _resource_table(text: str) -> str:
    marker = '<table class="resource-table">'
    start = text.index(marker)
    return text[start : text.index("</table>", start) + len("</table>")]


def _url_rating_pairs(table: str) -> tuple[tuple[str, str], ...]:
    pairs: list[tuple[str, str]] = []
    for row in re.findall(r"<tr>(.*?)</tr>", table, flags=re.DOTALL):
        url = re.search(r'<a href="(https?://[^"]+)">', row)
        rating = re.search(r"⭐{3,5}", row)
        if url and rating:
            pairs.append((url.group(1), rating.group()))
    return tuple(pairs)


def _catalog_heading_pairs(text: str) -> tuple[tuple[str, str], ...]:
    return tuple(
        (match.group(1), match.group(2))
        for match in re.finditer(
            r"^### \[[^\]]+\]\((https?://\S+?)\)\s+.*?(⭐{2,5}).*$",
            text,
            flags=re.MULTILINE,
        )
    )


@pytest.mark.parametrize("page", PUBLIC_FILES)
def test_public_resource_pages_drop_volatile_counts_stars_and_time_promises(
    page: Path,
) -> None:
    text = page.read_text(encoding="utf-8")
    assert not re.search(r"★\s*[\d,.]+[kKmM]?\+?", text)
    assert not re.search(r"\b(?:76|81|145|150|240|250)\+\b", text)
    assert not re.search(r"(?:~|≈|約|约)\s*\d+\s*(?:行|lines?)\b", text, re.IGNORECASE)
    assert not re.search(
        r"\b\d+\s*[–-]\s*\d+\s*(?:分鐘|分钟|minutes?|mins?)\b",
        text,
        re.IGNORECASE,
    )


@pytest.mark.parametrize("page", PUBLIC_TOTAL_FILES)
def test_public_resource_surfaces_do_not_advertise_inventory_totals(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    assert not re.search(
        r"\b(?:76|81|145|150|240|250)\+?\s*"
        r"(?:curated\s+)?(?:projects?|entries?|integrations?|tools?|servers?|"
        r"resources?|個\s*(?:projects?|專案|項目)|个\s*(?:projects?|项目)|條|条)\b",
        text,
        re.IGNORECASE,
    )
    assert not re.search(
        r"\b\d+\s+use[- ]case\s+categor(?:y|ies)\b",
        text,
        re.IGNORECASE,
    )


@pytest.mark.parametrize("page", OUTREACH_FILES)
def test_outreach_copy_uses_the_current_stage_route(page: Path) -> None:
    lines = page.read_text(encoding="utf-8").splitlines()
    assert not any(catalog_gate.has_stale_outreach_route(line) for line in lines)


@pytest.mark.parametrize("page", OUTREACH_FILES)
def test_outreach_copy_does_not_freeze_popularity_or_traffic_metrics(page: Path) -> None:
    lines = page.read_text(encoding="utf-8").splitlines()
    assert not any(catalog_gate.has_outreach_popularity_metric(line) for line in lines)


def test_resources_keeps_task_choices_core_terms_and_safe_starts_visible() -> None:
    for page in TRIOS["resources"].values():
        visible = _without_details(page.read_text(encoding="utf-8"))
        assert all(target in visible for target in TASK_TARGETS)
        assert all(url in visible for url in START_URLS)
        assert len(re.findall(r"⭐{3,5}", visible)) >= 26
        assert "**MCP" in visible
        assert "**Skill" in visible
        assert "**Plugin" in visible


def test_resources_grouped_highlights_have_exact_trilingual_parity() -> None:
    observed = []
    for page in TRIOS["resources"].values():
        text = page.read_text(encoding="utf-8")
        table = _resource_table(text)
        groups = re.findall(r"<tbody>(.*?)</tbody>", table, flags=re.DOTALL)
        assert len(groups) == len(ROWGROUPS)
        for group, size in zip(groups, ROWGROUPS, strict=True):
            assert len(re.findall(r"<tr>", group)) == size
            assert f'scope="rowgroup" rowspan="{size}"' in group
        pairs = _url_rating_pairs(table)
        assert pairs == HIGHLIGHT_PAIRS
        observed.append(pairs)
    assert len(set(observed)) == 1


def test_resources_keep_the_wide_table_inside_a_keyboard_scroll_region() -> None:
    labels = {
        "zh-TW": "精選資源表（可左右捲動）",
        "en": "Selected resources table (scroll horizontally)",
        "zh-Hans": "精选资源表（可左右滚动）",
    }
    for locale, page in TRIOS["resources"].items():
        text = page.read_text(encoding="utf-8")
        opening = (
            '<div class="resource-table-scroll" role="region" tabindex="0" '
            f'aria-label="{labels[locale]}">'
        )
        assert text.count(opening) == 1
        assert text.index(opening) < text.index('<table class="resource-table">')
        assert text.index("</table>") < text.index("</div>", text.index("</table>"))

    css = (ROOT / "docs" / "stylesheets" / "extra.css").read_text(encoding="utf-8")
    assert ".md-typeset .resource-table-scroll" in css
    assert "overflow-x: auto" in css
    assert "min-inline-size: 44rem" in css


def test_resources_use_current_official_integrations_and_limits() -> None:
    required = (
        "https://developers.notion.com/guides/mcp/overview",
        "https://developers.google.com/workspace/guides/configure-mcp-servers",
        "https://linear.app/docs/mcp",
        "https://docs.slack.dev/ai/mcp-overview/",
    )
    for locale, page in TRIOS["resources"].items():
        text = page.read_text(encoding="utf-8")
        assert all(url in text for url in required)
        table = _resource_table(text)
        assert all(fact in table for fact in INTEGRATION_FACTS[locale])
        assert all(url not in text for url in STALE_DEFAULTS)


def test_resource_index_is_task_first_and_folds_secondary_governance() -> None:
    for locale, page in TRIOS["resource-index"].items():
        text = page.read_text(encoding="utf-8")
        visible = _without_details(text)
        assert all(target in visible for target in INDEX_TARGETS)
        assert text.count('<details markdown="1">') >= 2
        assert not re.search(r"<details\b[^>]*\bopen\b", text)
        assert all(fact in text for fact in INDEX_MAINTENANCE_FACTS[locale])
        next_step = text[text.index("## ✅") :]
        assert "mcp-skills-catalog" in next_step
        assert "cookbook" in next_step
        assert "style-guide" in next_step
        assert "CONTRIBUTING" in next_step


def test_catalog_keeps_safe_starts_and_all_category_landings_visible() -> None:
    for page in TRIOS["catalog"].values():
        text = page.read_text(encoding="utf-8")
        visible = _without_details(text)
        assert text.count('<details markdown="1">') == 17
        assert not re.search(r"<details\b[^>]*\bopen\b", text)
        assert all(url in visible for url in START_URLS[:4])
        assert len(re.findall(r"⭐{3,5}", visible)) >= 5
        headings = re.findall(r"^##\s+(\d+)\.", visible, flags=re.MULTILINE)
        assert headings == [str(number) for number in range(1, 18)]
        assert len(re.findall(r"⭐{3,5}", text)) >= 80
        assert not re.search(r"\|\s*Stars\s*\|", text, re.IGNORECASE)


def test_catalog_uses_current_official_discovery_and_hosted_defaults() -> None:
    required = (
        "https://registry.modelcontextprotocol.io/",
        "https://developers.notion.com/guides/mcp/overview",
        "https://linear.app/docs/mcp",
        "https://docs.slack.dev/ai/mcp-overview/",
        "https://www.canva.dev/docs/mcp/",
    )
    for page in TRIOS["catalog"].values():
        text = page.read_text(encoding="utf-8")
        assert all(url in text for url in required)
        assert all(url not in text for url in STALE_DEFAULTS)
        assert re.search(r"reference|參考|参考", text, re.IGNORECASE)
        assert re.search(r"not production|不是 production|不等於 production|不等于 production", text, re.IGNORECASE)


def test_catalog_entry_urls_and_editorial_ratings_match_in_all_locales() -> None:
    observed = [
        _catalog_heading_pairs(page.read_text(encoding="utf-8"))
        for page in TRIOS["catalog"].values()
    ]
    assert len(observed[0]) >= 80
    assert len(set(observed)) == 1
    for page in TRIOS["catalog"].values():
        text = page.read_text(encoding="utf-8")
        assert "https://api.intuitek.ai/yield/mcp" in text
        assert re.search(r"YIELD INTELLIGENCE[\s\S]{0,300}⭐{3}", text)


def test_catalog_rejects_volatile_rankings_counts_and_fixed_model_roles() -> None:
    for page in TRIOS["catalog"].values():
        text = page.read_text(encoding="utf-8")
        for pattern in VOLATILE_CATALOG_CLAIMS:
            assert not re.search(pattern, text, re.IGNORECASE), f"{page}: {pattern}"


def test_catalog_keeps_permissions_source_checks_and_human_judgment() -> None:
    required_by_locale = {
        "zh-TW": (
            "優先使用 OAuth 或最小權限 token",
            "核對版本與原始官方文件",
            "不要把模型名稱當固定職位",
            "非投資建議",
            "警告後仍要人工判斷",
        ),
        "en": (
            "prefer OAuth or a least-privilege token",
            "check the version and original official documentation",
            "Do not turn model names into permanent job titles",
            "Not investment advice",
            "A warning still needs human judgment",
        ),
        "zh-Hans": (
            "优先使用 OAuth 或最小权限 token",
            "核对版本与原始官方文档",
            "不要把模型名称当固定职位",
            "非投资建议",
            "警告后仍要人工判断",
        ),
    }
    for locale, page in TRIOS["catalog"].items():
        text = page.read_text(encoding="utf-8")
        assert all(fragment in text for fragment in required_by_locale[locale])


def test_gemini_notebook_is_the_display_name_while_identifiers_stay_exact() -> None:
    for page in PUBLIC_FILES:
        for line_number, line in enumerate(
            page.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if "NotebookLM" not in line:
                continue
            allowed_identifier = re.search(
                r"notebooklm[-_/]|support\.google\.com/notebooklm|from notebooklm|NotebookLM\(\)",
                line,
                re.IGNORECASE,
            )
            if allowed_identifier:
                continue
            assert "Gemini Notebook" in line, f"{page}:{line_number}: {line}"

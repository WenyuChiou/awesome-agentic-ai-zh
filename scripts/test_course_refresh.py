"""Focused contracts for the 2026-10-15 free-course and NVIDIA-link refresh."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
COURSE_PAGES = {
    "zh-TW": ROOT / "resources/courses.md",
    "en": ROOT / "resources/courses.en.md",
    "zh-Hans": ROOT / "resources/courses.zh-Hans.md",
}
SETUP_PAGES = {
    "zh-TW": ROOT / "resources/setup-guide.md",
    "en": ROOT / "resources/setup-guide.en.md",
    "zh-Hans": ROOT / "resources/setup-guide.zh-Hans.md",
}
CONTEXT_URL = "https://huggingface.co/learn/context-course/unit0/introduction"
DEEP_AGENTS_URL = "https://academy.langchain.com/courses/deep-agents-with-langgraph"
NVIDIA_URL = "https://docs.api.nvidia.com/nim/reference/llm-apis"
STALE_NVIDIA_URL = "https://docs.api.nvidia.com/nim/re/reference/llm-apis"
COURSE_PAIRS = (
    ("https://huggingface.co/learn/agents-course", "⭐⭐⭐⭐⭐"),
    ("https://github.com/microsoft/ai-agents-for-beginners", "⭐⭐⭐⭐⭐"),
    ("https://github.com/datawhalechina/hello-agents", "⭐⭐⭐⭐⭐"),
    ("https://www.deeplearning.ai/courses/agentic-ai", "⭐⭐⭐⭐⭐"),
    ("https://academy.claude.com/", "⭐⭐⭐⭐"),
    (CONTEXT_URL, "⭐⭐⭐⭐"),
    ("https://academy.langchain.com/courses/intro-to-langgraph", "⭐⭐⭐⭐"),
    (DEEP_AGENTS_URL, "⭐⭐⭐⭐"),
    ("https://www.kaggle.com/learn-guide/5-day-agents", "⭐⭐⭐⭐"),
    (
        "https://www.coursera.org/professional-certificates/ibm-rag-and-agentic-ai",
        "⭐⭐⭐⭐",
    ),
    ("https://www.coursera.org/specializations/ai-agents", "⭐⭐⭐⭐"),
    (
        "https://www.nvidia.cn/training/certification/generative-ai-llm-learning-path/",
        "⭐⭐⭐⭐",
    ),
    ("https://edu.aliyun.com/certification/cldm02", "⭐⭐⭐"),
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _course_table(text: str) -> str:
    tables = re.findall(r"<table align=\"center\">.*?</table>", text, flags=re.DOTALL)
    assert len(tables) == 1
    return tables[0]


def _external_urls(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r"https://[^)\s<>\"']+", text))


@pytest.mark.parametrize("page", COURSE_PAGES.values())
def test_two_new_courses_are_visible_in_the_chooser_and_rated_table(page: Path) -> None:
    text = _text(page)
    chooser = text[text.index("## ⚡") : text.index("## 🎯")]
    table = _course_table(text)

    for url in (CONTEXT_URL, DEEP_AGENTS_URL):
        assert chooser.count(url) == 1
        assert table.count(url) == 1

    assert tuple(
        re.findall(
            r'<a href="(https?://[^"]+)">.*?</a>.*?(⭐{3,5})',
            table,
            flags=re.DOTALL,
        )
    ) == COURSE_PAIRS


@pytest.mark.parametrize("page", COURSE_PAGES.values())
def test_course_table_keeps_four_real_rowgroups_and_thirteen_ratings(page: Path) -> None:
    table = _course_table(_text(page))
    groups = re.findall(r"<tbody>(.*?)</tbody>", table, flags=re.DOTALL)
    assert len(groups) == 4
    for group, expected_rows in zip(groups, (3, 6, 2, 2)):
        assert group.count("<tr>") == expected_rows
        assert group.count('scope="rowgroup"') == 1
        assert f'rowspan="{expected_rows}"' in group
    assert len(re.findall(r'<span data-field="rating">⭐{3,5}</span>', table)) == 13
    assert len(re.findall(r'<th scope="col">', table)) == 5
    for field in ("entry", "cost", "outcome", "limits"):
        assert table.count(f'<div data-field="{field}">') == 13
    assert '<th scope="rowgroup"></th>' not in table


def test_course_mirrors_share_exact_external_url_order() -> None:
    orders = [_external_urls(_text(page)) for page in COURSE_PAGES.values()]
    assert len(set(orders)) == 1


@pytest.mark.parametrize("locale,page", COURSE_PAGES.items())
def test_free_content_extra_cost_and_certificate_boundaries_are_explicit(
    locale: str, page: Path
) -> None:
    text = _text(page)
    table = _course_table(text)
    context_row = next(row for row in re.findall(r"<tr>.*?</tr>", table) if CONTEXT_URL in row)
    deep_agents_row = next(
        row for row in re.findall(r"<tr>.*?</tr>", table) if DEEP_AGENTS_URL in row
    )
    markers = {
        "zh-TW": {
            "context": ("課程教材免費", "API", "訂閱可能付費", "尚待直播公布", "不要視為已可完成"),
            "deep": ("課程免費", "API 用量可能付費", "30 課", "約 2 小時影片", "已學 Agent 基礎", "未列證書門檻"),
            "date": "新增課程查核：2026-10-15 UTC；範圍只含",
        },
        "en": {
            "context": ("course material is free", "API", "subscriptions may cost", "announced in a live stream", "currently completable"),
            "deep": ("free course", "model/API usage may cost", "30 lessons", "about 2 hours of video", "know Agent foundations", "does not state a certificate threshold"),
            "date": "New-course verification: 2026-10-15 UTC; scope limited to",
        },
        "zh-Hans": {
            "context": ("课程材料免费", "API", "订阅可能收费", "尚待直播公布", "不要视为现在已经可以完成"),
            "deep": ("课程免费", "API 用量可能收费", "30 课", "约 2 小时视频", "掌握 Agent 基础", "未列出证书门槛"),
            "date": "新增课程核查：2026-10-15 UTC；范围只包括",
        },
    }[locale]
    assert all(marker in context_row for marker in markers["context"])
    assert all(marker in deep_agents_row for marker in markers["deep"])
    assert markers["date"] in text
    assert "verified_on=2026-08-29" in text


@pytest.mark.parametrize("locale,page", COURSE_PAGES.items())
def test_new_rows_define_technical_terms_and_keep_four_star_elective_scope(
    locale: str, page: Path,
) -> None:
    table = _course_table(_text(page))
    context_row = next(row for row in re.findall(r"<tr>.*?</tr>", table) if CONTEXT_URL in row)
    deep_agents_row = next(
        row for row in re.findall(r"<tr>.*?</tr>", table) if DEEP_AGENTS_URL in row
    )
    assert "<strong>Skill (" in context_row or "<strong>Skill（" in context_row
    assert "<strong>MCP (" in context_row or "<strong>MCP（" in context_row
    assert "<strong>Plugin" in context_row
    assert "<strong>Subagent" in context_row
    assert "<strong>Hook" in context_row
    assert "<strong>Nano Harness (" in context_row or "<strong>Nano Harness（" in context_row
    hook_and_harness = {
        "zh-TW": ("<strong>Hook（事件觸發動作）</strong>", "<strong>Nano Harness（迷你執行架構）</strong>"),
        "en": ("<strong>Hooks (event-triggered actions)</strong>", "<strong>Nano Harness (a tiny execution harness)</strong>"),
        "zh-Hans": ("<strong>Hook（事件触发动作）</strong>", "<strong>Nano Harness（迷你执行架构）</strong>"),
    }[locale]
    assert all(marker in context_row for marker in hook_and_harness)
    assert "lifecycle checkpoint" not in context_row
    assert "生命週期檢查點" not in context_row
    assert "生命周期检查点" not in context_row
    assert "minimal agent loop" not in context_row
    assert "最小代理迴圈" not in context_row
    assert "最小 Agent 循环" not in context_row
    assert "<strong>Todo list (" in deep_agents_row or "<strong>Todo list（" in deep_agents_row
    assert '<span data-field="rating">⭐⭐⭐⭐</span>' in context_row
    assert '<span data-field="rating">⭐⭐⭐⭐</span>' in deep_agents_row


def test_nvidia_reference_url_is_fixed_and_setup_mirrors_stay_in_sync() -> None:
    orders = []
    for page in SETUP_PAGES.values():
        text = _text(page)
        assert text.count(NVIDIA_URL) == 1
        assert STALE_NVIDIA_URL not in text
        orders.append(_external_urls(text))
    assert len(set(orders)) == 1


def test_new_fact_pack_dates_are_scoped_and_sources_match_pages() -> None:
    config = yaml.safe_load((ROOT / "scripts/freshness-models.yml").read_text(encoding="utf-8"))
    courses = config["courses_fact_pack"]
    assert courses["verified_on"] == "2026-08-29"
    assert courses["course_updates"] == {
        "hugging_face_context": "2026-10-15", "langchain_deep_agents": "2026-10-15"}
    assert courses["official_sources"]["hugging_face_context"] == CONTEXT_URL
    assert courses["official_sources"]["langchain_deep_agents"] == DEEP_AGENTS_URL
    setup = config["setup_guide_fact_pack"]
    assert setup["verified_on"] == "2026-08-31"
    assert setup["provider_entrypoint_updates"]["nvidia_nim_llm_api"] == "2026-10-15"
    assert setup["official_sources"]["nvidia_nim_llm_api"] == NVIDIA_URL

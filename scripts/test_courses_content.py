"""Course-map reader path, source, grouping, and locale-mirror contracts."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "zh-TW": ROOT / "resources/courses.md",
    "en": ROOT / "resources/courses.en.md",
    "zh-Hans": ROOT / "resources/courses.zh-Hans.md",
}
READMES = {
    "zh-TW": ROOT / "README.md",
    "en": ROOT / "README.en.md",
    "zh-Hans": ROOT / "README.zh-Hans.md",
}
FRESHNESS = (
    "<!-- freshness: canonical=resources/courses.md; "
    "verified_on=2026-08-29; "
    "scope=course-availability,cost,certificate,assessment,repository-status; "
    "max_age_days=90 -->"
)
COURSE_PAIRS = (
    ("https://huggingface.co/learn/agents-course", "⭐⭐⭐⭐⭐"),
    ("https://github.com/microsoft/ai-agents-for-beginners", "⭐⭐⭐⭐⭐"),
    ("https://github.com/datawhalechina/hello-agents", "⭐⭐⭐⭐⭐"),
    ("https://www.deeplearning.ai/courses/agentic-ai/", "⭐⭐⭐⭐⭐"),
    ("https://wandb.ai/site/courses/agents/", "⭐⭐⭐⭐"),
    ("https://academy.claude.com/", "⭐⭐⭐⭐"),
    ("https://academy.langchain.com/courses/intro-to-langgraph", "⭐⭐⭐⭐"),
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
EXTERNAL_URLS = (
    "https://huggingface.co/learn/agents-course",
    "https://github.com/microsoft/ai-agents-for-beginners",
    "https://github.com/datawhalechina/hello-agents",
    "https://www.deeplearning.ai/courses/agentic-ai/",
    "https://wandb.ai/site/courses/agents/",
    "https://academy.claude.com/",
    "https://academy.langchain.com/courses/intro-to-langgraph",
    "https://www.coursera.org/professional-certificates/ibm-rag-and-agentic-ai",
    "https://www.coursera.org/specializations/ai-agents",
    *(url for url, _ in COURSE_PAIRS),
    "https://github.com/datawhalechina/agentic-ai",
)
CORE_LABELS = {
    "zh-TW": (
        "Course（課程）",
        "Certificate of Completion（完成證書）",
        "Skill Badge（技能徽章）",
        "Professional Certificate（專業課程證書）",
        "Certification Exam（認證考試）",
    ),
    "en": (
        "Course",
        "Certificate of Completion",
        "Skill Badge",
        "Professional Certificate",
        "Certification Exam",
    ),
    "zh-Hans": (
        "Course（课程）",
        "Certificate of Completion（完成证书）",
        "Skill Badge（技能徽章）",
        "Professional Certificate（专业课程证书）",
        "Certification Exam（认证考试）",
    ),
}
PORTFOLIO_LINES = {
    "zh-TW": (
        "我解決的問題：",
        "Agent 可以使用的工具：",
        "我怎麼知道它做對：",
        "失敗時怎麼安全停止：",
        "可執行程式或 Demo 連結：",
    ),
    "en": (
        "The problem I solved:",
        "Tools my Agent can use:",
        "How I know it worked:",
        "How it stops safely when it fails:",
        "Runnable code or Demo link:",
    ),
    "zh-Hans": (
        "我解决的问题：",
        "Agent 可以使用的工具：",
        "我怎么知道它做对了：",
        "失败时怎么安全停止：",
        "可执行代码或 Demo 链接：",
    ),
}


def _without_details(text: str) -> str:
    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.DOTALL)


def _course_table(text: str) -> str:
    tables = re.findall(r"<table>.*?</table>", text, flags=re.DOTALL)
    assert len(tables) == 1
    return tables[0]


@pytest.mark.parametrize("locale", PAGES)
def test_visible_path_keeps_terms_chooser_courses_portfolio_and_return_route(
    locale: str,
) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    chooser = visible.index("## ⚡")
    table = visible.index("<table>")
    portfolio = visible.index("## 🧪")

    for label in CORE_LABELS[locale]:
        token = f"**{label}**"
        assert token in visible
        assert visible.index(token) < chooser

    assert chooser < table < portfolio
    assert tuple(
        line.strip()
        for line in re.search(r"```text\n(.*?)\n```", visible, re.DOTALL).group(1).splitlines()
    ) == PORTFOLIO_LINES[locale]

    suffix = {"zh-TW": "", "en": ".en", "zh-Hans": ".zh-Hans"}[locale]
    for stage in (
        f"../stages/03-tool-use-and-hello-agent{suffix}.md",
        f"../stages/04-agent-frameworks{suffix}.md",
        f"../stages/07-multi-agent-production{suffix}.md",
    ):
        assert f"({stage})" in visible


@pytest.mark.parametrize("page", PAGES.values())
def test_two_secondary_disclosures_are_closed_and_render_markdown(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    openings = re.findall(r"^<details\b[^>]*>", text, flags=re.MULTILINE)
    assert openings == ['<details markdown="1">'] * 2
    assert not re.search(r"<details\b[^>]*\bopen\b", text)


def test_course_table_has_twelve_rated_rows_and_four_real_rowgroups() -> None:
    for page in PAGES.values():
        table = _course_table(page.read_text(encoding="utf-8"))
        groups = re.findall(r"<tbody>(.*?)</tbody>", table, flags=re.DOTALL)
        assert len(groups) == 4
        for group, row_count in zip(groups, (3, 5, 2, 2)):
            assert len(re.findall(r"<tr>", group)) == row_count
            assert group.count('scope="rowgroup"') == 1
            assert f'rowspan="{row_count}"' in group
            assert '<th scope="rowgroup"></th>' not in group

        pairs = re.findall(
            r'<a href="(https?://[^"]+)">.*?</a>.*?(⭐{3,5})',
            table,
            flags=re.DOTALL,
        )
        assert tuple(pairs) == COURSE_PAIRS


def test_three_locales_share_the_exact_source_order_and_freshness_marker() -> None:
    for page in PAGES.values():
        text = page.read_text(encoding="utf-8")
        assert text.count(FRESHNESS) == 1
        assert tuple(re.findall(r"https://[^)\s<>\"']+", text)) == EXTERNAL_URLS


@pytest.mark.parametrize("locale", PAGES)
def test_course_certificate_and_availability_facts_remain_honest(locale: str) -> None:
    text = PAGES[locale].read_text(encoding="utf-8")
    markers = {
        "zh-TW": (
            "Unit 1 測驗達 80%",
            "沒有完成證書；現行範例偏 Microsoft Agent Framework",
            "測驗、graded assignments 與證書需要 Pro",
            "現行公開頁未明示證書條件",
            "通過課程 quiz 可取得免費完成徽章",
            "目前可免費啟用",
            "需符合官方列出的身分文件條件",
            "部分課程授予 DLI 培訓證書",
            "不等於學位",
        ),
        "en": (
            "A score of 80% on the Unit 1 quiz",
            "No Certificate of Completion; the current examples lean toward Microsoft Agent Framework",
            "the certificate require Pro",
            "current public page does not clearly state certificate requirements",
            "Passing the course quiz can earn a free completion badge",
            "currently available to activate for free",
            "identity-document conditions listed by the official site",
            "Some courses award DLI training certificates",
            "not a degree",
        ),
        "zh-Hans": (
            "Unit 1 测验达到 80%",
            "没有 Certificate of Completion；现行示例偏向 Microsoft Agent Framework",
            "测验、graded assignments 和证书需要 Pro",
            "当前公开页面没有明确说明证书条件",
            "通过课程 quiz 可以取得免费完成徽章",
            "目前可以免费启用",
            "需符合官方网站列出的身份证明文件条件",
            "部分课程授予 DLI 培训证书",
            "不等于学位",
        ),
    }
    for marker in markers[locale]:
        assert marker in text


@pytest.mark.parametrize("page", PAGES.values())
def test_stale_rankings_prices_and_display_artifacts_do_not_return(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    forbidden = (
        "tier-1",
        "tier-2",
        "anthropic.skilljar.com",
        "agentic-ai-engineering",
        "HCIA-AI",
        "Edureka",
        "17 self-paced",
        "17 門自學",
        "17 门自学",
        "5 learning tracks",
        "5 條學習軌",
        "5 条学习轨",
        "$25–30",
        "¥3500",
        '""',
        "“”",
    )
    assert not any(term in text for term in forbidden)
    assert not re.search(r"\b\d+(?:\.\d+)?[kKmM]\+?\s+(?:GitHub\s+)?stars\b", text)
    assert "verification date means only" not in text
    assert "查核日期只代表" not in text


def test_freshness_config_enrolls_the_course_fact_pack_and_page() -> None:
    config = yaml.safe_load((ROOT / "scripts/freshness-models.yml").read_text(encoding="utf-8"))
    pack = config["courses_fact_pack"]
    assert pack["canonical"] == "resources/courses.md"
    assert pack["verified_on"] == "2026-08-29"
    assert pack["scope"] == [
        "course-availability",
        "cost",
        "certificate",
        "assessment",
        "repository-status",
    ]
    page = next(
        item for item in config["verified_pages"] if item["canonical"] == "resources/courses.md"
    )
    assert page["required_scopes"] == pack["scope"]
    assert page["max_age_days"] == 90


def test_readme_router_and_maintainer_docs_describe_the_new_course_shape() -> None:
    expected = {
        "zh-TW": "分清完成證書、技能徽章與認證考試",
        "en": "separates completion certificates, skill badges, and certification exams",
        "zh-Hans": "分清完成证书、技能徽章和认证考试",
    }
    for locale, page in READMES.items():
        text = page.read_text(encoding="utf-8")
        visible = _without_details(text)
        assert "resources/courses" in visible
        assert expected[locale].casefold() in visible.casefold()
        assert "10 門 credible" not in text
        assert "10 credible cert-granting" not in text
        assert "10 门 credible" not in text
        assert "12 current courses" not in text
        assert "12 條現行課程" not in text
        assert "12 条现行课程" not in text

    design = (ROOT / "stages/DESIGN.md").read_text(encoding="utf-8")
    assert "### 課程地圖固定結構" in design
    assert "`3／5／2／2`" in design
    assert "一列只放一個主課程 URL" in design
    assert "不做證書排行榜" in design

    testing_plan = (ROOT / "docs/TESTING_PLAN.md").read_text(encoding="utf-8")
    assert "### Course map — learn first, certificate second" in testing_plan
    assert "`scripts/test_courses_content.py`" in testing_plan

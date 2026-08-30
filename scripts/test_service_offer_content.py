"""Agent Workflow Audit offer, privacy, locale, and navigation contracts."""

from __future__ import annotations

import re
from types import SimpleNamespace
from pathlib import Path

import markdown
import pytest

from scripts import mkdocs_hooks


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "zh-TW": ROOT / "services/agent-workflow-audit.md",
    "en": ROOT / "services/agent-workflow-audit.en.md",
    "zh-Hans": ROOT / "services/agent-workflow-audit.zh-Hans.md",
}
READMES = {
    "zh-TW": ROOT / "README.md",
    "en": ROOT / "README.en.md",
    "zh-Hans": ROOT / "README.zh-Hans.md",
}
SECTION_HEADINGS = {
    "zh-TW": (
        "## 你要先提供什麼？",
        "## 你會拿到什麼？",
        "## 這項服務不包含什麼？",
        "## 費用怎麼算？",
        "## 如何開始？",
        "## 資料與案例原則",
    ),
    "en": (
        "## What do you need to provide first?",
        "## What do you get?",
        "## What is not included?",
        "## How is the price set?",
        "## How to start?",
        "## Data and case-study rules",
    ),
    "zh-Hans": (
        "## 你要先提供什么？",
        "## 你会拿到什么？",
        "## 这项服务不包含什么？",
        "## 费用怎么算？",
        "## 如何开始？",
        "## 数据与案例原则",
    ),
}
CORE_FACTS = (
    "Agent Workflow Audit",
    "20",
    "Eval",
    "prototype",
    "API key",
    "GitHub Issue",
    "wenyuchiou12@gmail.com",
)
SEMANTIC_CLAUSES = {
    "zh-TW": {
        "consent": "必須先取得你的書面同意",
        "not_validated": "沒有真實付費案例前，本專案不會宣稱這項商業模式已經驗證",
        "quote": "第一版採**固定範圍、個別報價**",
        "pricing_gate": "累積三次有效詢問後，才評估是否公開固定價格",
    },
    "en": {
        "consent": "your written consent has to be obtained first",
        "not_validated": "Until there is a real paying case, this project does not claim that this business model has been proven",
        "quote": "The first version uses a **fixed scope with a private, individual quote**",
        "pricing_gate": "Only after three genuine inquiries have accumulated will publishing a fixed public price be considered",
    },
    "zh-Hans": {
        "consent": "必须先取得你的书面同意",
        "not_validated": "没有真实付费案例前，本项目不会宣称这套商业模式已经得到验证",
        "quote": "第一版采用**固定范围、个别报价**",
        "pricing_gate": "累积三次有效询问后，才评估是否公开固定价格",
    },
}
README_ROUTES = {
    "zh-TW": "services/agent-workflow-audit.md",
    "en": "services/agent-workflow-audit.en.md",
    "zh-Hans": "services/agent-workflow-audit.zh-Hans.md",
}
VALIDATION_PLAN = ROOT / "docs/plans/2026-08-30-agent-workflow-audit-demand-validation.md"


def _semantic_contract_errors(locale: str, text: str) -> list[str]:
    return [
        name
        for name, clause in SEMANTIC_CLAUSES[locale].items()
        if clause not in text
    ]


@pytest.mark.parametrize("page", PAGES.values())
def test_offer_keeps_scope_deliverables_price_contact_and_privacy_visible(
    page: Path,
) -> None:
    text = page.read_text(encoding="utf-8")
    assert "<details" not in text
    for fact in CORE_FACTS:
        assert fact in text
    assert text.count("mailto:wenyuchiou12@gmail.com") == 1
    assert "subject=Agent%20Workflow%20Audit" in text
    assert re.search(r"fixed|固定", text, re.IGNORECASE)
    assert re.search(r"written|書面|书面", text, re.IGNORECASE)
    assert not re.search(r"validated|已驗證|已验证", text, re.IGNORECASE)


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_locale_specific_semantic_promises_are_exact(locale: str, page: Path) -> None:
    assert _semantic_contract_errors(locale, page.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize("page", PAGES.values())
def test_copyable_intake_has_six_groups_and_three_failures(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    block = re.search(r"```text\n(.*?)\n```", text, re.DOTALL)
    assert block is not None
    form = block.group(1)
    labels = [line for line in form.splitlines() if line and not line.startswith("-")]
    assert len(labels) == 7  # subject + six requested information groups
    assert re.search(r"three|三個|三个", form, re.IGNORECASE)


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_six_contract_sections_keep_the_same_order_and_item_counts(
    locale: str, page: Path
) -> None:
    text = page.read_text(encoding="utf-8")
    headings = SECTION_HEADINGS[locale]
    positions = [text.index(heading) for heading in headings]
    assert positions == sorted(positions)

    provided = text[positions[0] : positions[1]]
    deliverables = text[positions[1] : positions[2]]
    exclusions = text[positions[2] : positions[3]]
    case_rules = text[positions[5] :]
    assert len(re.findall(r"^\d+\. ", provided, re.MULTILINE)) == 6
    assert len(re.findall(r"^\d+\. ", deliverables, re.MULTILINE)) == 5
    assert len(re.findall(r"^- ", exclusions, re.MULTILINE)) == 4
    assert len(re.findall(r"^- ", case_rules, re.MULTILINE)) == 4


def test_english_prose_has_no_cjk_outside_language_switcher() -> None:
    text = PAGES["en"].read_text(encoding="utf-8")
    prose = text.split("</div>", maxsplit=1)[1]
    assert not re.search(r"[\u3400-\u9fff]", prose)


def test_readmes_use_the_same_three_step_private_contact_route() -> None:
    for locale, readme in READMES.items():
        text = readme.read_text(encoding="utf-8")
        assert "Agent Workflow Audit" in text, locale
        assert f"]({README_ROUTES[locale]})" in text, locale
        assert "mailto:wenyuchiou12@gmail.com" in text, locale
        assert "GitHub Issue" in text, locale


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_opposite_consent_and_validation_claims_are_rejected(
    locale: str, page: Path
) -> None:
    text = page.read_text(encoding="utf-8")
    for key, opposite in (
        ("consent", "no written consent is needed"),
        ("not_validated", "This business model is already validated"),
        ("quote", "A public fixed price applies to everyone"),
        ("pricing_gate", "The public price is available before any inquiry"),
    ):
        mutated = text.replace(SEMANTIC_CLAUSES[locale][key], opposite)
        assert key in _semantic_contract_errors(locale, mutated)


@pytest.mark.parametrize("locale,readme", READMES.items())
def test_wrong_locale_readme_route_is_rejected(locale: str, readme: Path) -> None:
    text = readme.read_text(encoding="utf-8")
    expected = README_ROUTES[locale]
    wrong = "services/agent-workflow-audit.wrong-locale.md"
    mutated = text.replace(expected, wrong)
    assert f"]({expected})" not in mutated


def test_service_is_staged_and_nested_under_project_overview() -> None:
    build_script = (ROOT / "scripts/build-docs-tree.py").read_text(encoding="utf-8")
    assert '"services"' in build_script

    config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    expected_nav = """  - 專案說明:
      - 專案介紹: about.md
      - Agent Workflow Audit: services/agent-workflow-audit.md"""
    assert expected_nav in config


@pytest.mark.parametrize("page", PAGES.values())
def test_site_render_strips_raw_markdown_language_switcher(page: Path) -> None:
    source = page.read_text(encoding="utf-8")
    fake_page = SimpleNamespace(
        file=SimpleNamespace(src_path=f"services/{page.name}")
    )
    processed = mkdocs_hooks.on_page_markdown(
        source, page=fake_page, config=None, files=None
    )
    rendered = markdown.markdown(processed, extensions=["md_in_html"])
    assert 'align="right"' not in rendered
    assert not re.search(r'href="[^\"]*agent-workflow-audit(?:\.en|\.zh-Hans)?\.md"', rendered)


def test_six_week_validation_gate_is_durable_without_client_records() -> None:
    text = VALIDATION_PLAN.read_text(encoding="utf-8")
    for phrase in (
        "至少 5 個合格詢問",
        "至少 3 次有效需求訪談",
        "至少 1 次付費證據",
        "詢問來源",
        "現在使用的替代方式",
        "失敗造成的時間、金錢或工作影響",
        "可以接受的預算",
        "希望完成的期限",
        "沒有成交的原因",
        "不開始 SaaS、billing、會員、認證或 marketplace 開發",
        "不 commit 到 repository",
    ):
        assert phrase in text

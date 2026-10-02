from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CLAUSES = {
    "CONTRIBUTING.md": (
        "大廠官方 AI 工具例外",
        "已知大型供應商的官方工具與文件，不受上述 30 分鐘入門門檻限制。",
        "這不適用於第三方包裝或社群 repo。",
        "仍須確認教學用途、現行官方來源、狀態與存取限制。",
        "未實測時要明寫「官方動態／未實測參考」，不得標成已驗證實作推薦。",
        "其他策展、授權、安全、三語及測試要求照常。",
    ),
    "CONTRIBUTING.zh-Hans.md": (
        "大厂官方 AI 工具例外",
        "已知大型供应商的官方工具与文档，不受上述 30 分钟入门门槛限制。",
        "这不适用于第三方包装或社区 repo。",
        "仍须确认教学用途、现行官方来源、状态与访问限制。",
        "未实测时要明写“官方动态／未实测参考”，不得标成已验证实践推荐。",
        "其他策展、授权、安全、三语及测试要求照常。",
    ),
    "CONTRIBUTING.en.md": (
        "Official AI tools from major vendors",
        "Official tools and documentation from established major vendors are exempt only from the 30-minute onboarding threshold above.",
        "This does not cover third-party wrappers or community repositories.",
        "Teaching purpose, current official sources, status, and access limits still need verification.",
        "If not tested hands-on, label them as official news / untested reference, not a verified hands-on recommendation.",
        "All other curation, licensing, safety, trilingual, and testing requirements still apply.",
    ),
}


@pytest.mark.parametrize("filename,clauses", CLAUSES.items())
def test_official_vendor_exception_is_narrow_and_discloses_untested_status(filename: str, clauses: tuple[str, ...]) -> None:
    text = (ROOT / filename).read_text(encoding="utf-8")
    for clause in clauses:
        assert clause in text
    for vendor in ("OpenAI", "Anthropic", "Google", "Meta", "xAI"):
        assert vendor in text
    assert "stable, no longer maintained" in text
    assert "MIT" in text and "Apache 2" in text and "BSD" in text


@pytest.mark.parametrize("filename", ("CONTRIBUTING.md", "CONTRIBUTING.zh-Hans.md"))
def test_new_chinese_policy_sentences_fit_written_style(filename: str) -> None:
    text = (ROOT / filename).read_text(encoding="utf-8")
    label = CLAUSES[filename][0]
    section = text[text.index(f"**{label}**") :].split("\n\n", 2)
    for block in section[:2]:
        for sentence in re.split(r"(?<=[。！？])", block.replace("**", "")):
            if sentence.strip():
                assert len(sentence.strip()) <= 60, sentence


def test_suggestion_and_pr_checklists_point_to_exception_without_claiming_execution() -> None:
    suggestion = (ROOT / ".github/ISSUE_TEMPLATE/project-suggestion.md").read_text(encoding="utf-8")
    template = (ROOT / ".github/PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
    for text, relative in ((suggestion, "../../CONTRIBUTING.md#策展標準"), (template, "../CONTRIBUTING.md#策展標準")):
        assert "以下兩項擇一" in text
        normal = next(line for line in text.splitlines() if line.startswith("- [ ] 一般 project："))
        assert normal == "- [ ] 一般 project：有 hello-world 文件，30 分鐘內能跑起來"
        exception = next(line for line in text.splitlines() if line.startswith("- [ ] 大廠官方工具："))
        assert f"[30 分鐘例外]({relative})" in exception
        assert "已揭露實測狀態與限制；未實測時依指南標註" in exception
        assert "已標註未實測狀態" not in exception
        assert "- [ ] 最近 6 個月內有 commit（或明確標示 stable）" in text
        assert "- [ ] License 明確" in text
        assert "- [ ] 維護者可信" in text


ORIGINAL_CRITERIA = {'CONTRIBUTING.md': ['1. **有維護**：最近 6 個月內有 commit，或明確標示「stable, no longer maintained」', '2. **有 hello-world 文件**：讀者應該能在 30 分鐘內把東西跑起來', '3. **明確 license**：MIT、Apache 2、BSD 或類似。避免沒 license 的 repo。', '4. **可信賴的維護者**：知名組織、公司，或有口碑的個人'], 'CONTRIBUTING.zh-Hans.md': ['1. **有维护**：最近 6 个月内有 commit，或明确标示“stable, no longer maintained”', '2. **有 hello-world 文件**：读者应该能在 30 分钟内把东西跑起来', '3. **明确 license**：MIT、Apache 2、BSD 或类似。避免没 license 的 repo。', '4. **可信赖的维护者**：知名组织、公司，或有口碑的个人'], 'CONTRIBUTING.en.md': ['1. **Active maintenance**: commits within last 6 months OR explicit "stable, no longer maintained" notice', '2. **Documented hello-world**: a reader should be able to run something within 30 minutes', '3. **Clear license**: MIT, Apache 2, BSD, or comparable. Avoid no-license repos.', '4. **Trustworthy maintainer**: well-known org, company, or individual with track record']}

@pytest.mark.parametrize("filename,criteria", ORIGINAL_CRITERIA.items())
def test_other_curation_criteria_remain_verbatim(filename: str, criteria: list[str]) -> None:
    text = (ROOT / filename).read_text(encoding="utf-8")
    for criterion in criteria:
        assert criterion in text

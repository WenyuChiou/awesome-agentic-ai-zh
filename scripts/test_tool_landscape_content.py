from __future__ import annotations

import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]

EXAMPLE_PAGES = {
    "zh-TW": ROOT / "examples/README.md",
    "en": ROOT / "examples/README.en.md",
    "zh-Hans": ROOT / "examples/README.zh-Hans.md",
}
PARADIGM_PAGES = {
    "zh-TW": ROOT / "resources/agent-paradigms.md",
    "en": ROOT / "resources/agent-paradigms.en.md",
    "zh-Hans": ROOT / "resources/agent-paradigms.zh-Hans.md",
}
EXAMPLE_HEADINGS = {
    "zh-TW": ("## 📚 必讀閱讀", "## 🎯 精選 Projects 與學習資源"),
    "en": ("## 📚 Required reading", "## 🎯 Curated Projects and learning resources"),
    "zh-Hans": ("## 📚 必读阅读", "## 🎯 精选 Projects 与学习资源"),
}
PARADIGM_HEADINGS = EXAMPLE_HEADINGS
PARADIGM_IMAGES = {
    "zh-TW": "diagrams/agent-tool-axes.png",
    "en": "diagrams/agent-tool-axes.en.png",
    "zh-Hans": "diagrams/agent-tool-axes.zh-Hans.png",
}


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _without_closed_details(text: str) -> str:
    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.DOTALL)


def _external_urls(text: str) -> list[str]:
    return re.findall(r'https://[^\s)"<>]+', text)


def _rowspans(text: str) -> list[int]:
    return [int(value) for value in re.findall(r'scope="rowgroup" rowspan="(\d+)"', text)]


@pytest.mark.parametrize("locale", EXAMPLE_PAGES)
def test_examples_keep_required_reading_index_and_rated_resources_visible(locale: str) -> None:
    text = _text(EXAMPLE_PAGES[locale])
    visible = _without_closed_details(text)
    required, resources = EXAMPLE_HEADINGS[locale]

    assert required in visible
    assert resources in visible
    assert "## 🧭" in visible
    assert _rowspans(visible) == [2, 2, 2]
    assert len(re.findall(r"<td>⭐{3,5}</td>", visible)) == 6
    assert len(re.findall(r"^<details markdown=\"1\">$", text, flags=re.MULTILINE)) == 2
    assert not re.search(r"<details[^>]*\sopen(?:\s|>)", text)


def test_examples_match_the_real_folder_inventory() -> None:
    expected = {"stage-1": 2, "stage-2": 1, "stage-3": 6, "stage-4": 5, "stage-5": 1, "stage-6": 5, "stage-7": 6}
    actual = {
        name: len([path for path in (ROOT / "examples" / name).iterdir() if path.is_dir()])
        for name in expected
    }
    assert actual == expected


def test_examples_document_and_match_distinct_folder_shapes() -> None:
    common_readmes = {"README.md", "README.en.md", "README.zh-Hans.md"}
    standard_core = {
        *common_readmes,
        "requirements.txt",
        "starter.py",
        "starter_anthropic.py",
        "test.py",
        "test_anthropic.py",
    }
    special_folders = {
        "stage-1/04-cross-provider": common_readmes | {"requirements.txt", "starter.py", "test.py"},
        "stage-3/06-schema-design": common_readmes
        | {
            "requirements.txt",
            "starter_bad.py",
            "starter_bad_anthropic.py",
            "starter_good.py",
            "starter_good_anthropic.py",
            "test.py",
            "test_anthropic.py",
        },
        "stage-5/tool-calling-tutor": common_readmes | {"SKILL.md"},
        "stage-7/06-safe-execution": common_readmes | {"starter.py", "test.py"},
    }
    additive_extras = {
        "stage-4/01-same-agent-two-frameworks": {"starter_crewai.py", "test_crewai.py"},
        "stage-4/04-codeact-vs-json-tool": {"test_docker_smoke.py"},
        "stage-7/05-deploy": {"Dockerfile"},
    }

    all_folders = {
        f"{stage.name}/{folder.name}": folder
        for stage in sorted((ROOT / "examples").glob("stage-*"))
        for folder in sorted(path for path in stage.iterdir() if path.is_dir())
    }
    for relative, folder in all_folders.items():
        files = {path.name for path in folder.iterdir() if path.is_file()}
        if relative in special_folders:
            assert files == special_folders[relative]
        else:
            assert standard_core <= files
        assert additive_extras.get(relative, set()) <= files

    skill_folder = ROOT / "examples/stage-5/tool-calling-tutor"
    assert {"references", "translations"} <= {
        path.name for path in skill_folder.iterdir() if path.is_dir()
    }
    for text in map(_text, EXAMPLE_PAGES.values()):
        for relative in special_folders | additive_extras:
            assert relative in text


def test_examples_trilingual_facts_and_external_urls_match() -> None:
    texts = {locale: _text(path) for locale, path in EXAMPLE_PAGES.items()}
    marker = (
        "<!-- freshness: canonical=examples/README.md; verified_on=2026-08-31; "
        "scope=example-inventory,local-model-tags,download-sizes,sdk-entry-points; max_age_days=90 -->"
    )
    for text in texts.values():
        assert text.count(marker) == 1
        for literal in ("gemma4:e4b", "9.6 GB", "qwen2.5:3b", "1.9 GB", "qwen3.5:4b", "3.4 GB"):
            assert literal in text
        for stale in ("54 exercises", "54 個練習", "54 个练习", "7.5 GB", "4.0 GB"):
            assert stale not in text
    assert _external_urls(texts["zh-TW"]) == _external_urls(texts["en"]) == _external_urls(texts["zh-Hans"])


def test_cross_provider_example_does_not_overpromise_compatibility() -> None:
    pages = (
        ROOT / "examples/stage-1/04-cross-provider/README.md",
        ROOT / "examples/stage-1/04-cross-provider/README.en.md",
        ROOT / "examples/stage-1/04-cross-provider/README.zh-Hans.md",
    )
    for page in pages:
        text = _text(page)
        assert "tool schema" in text
        assert "response" in text
        assert "5-10" not in text and "5–10" not in text
        assert "free $0" not in text


@pytest.mark.parametrize("locale", PARADIGM_PAGES)
def test_paradigms_keep_core_terms_required_reading_subagents_and_resources_visible(locale: str) -> None:
    text = _text(PARADIGM_PAGES[locale])
    visible = _without_closed_details(text)
    required, resources = PARADIGM_HEADINGS[locale]

    assert required in visible
    assert resources in visible
    assert "## Subagent" in visible
    assert PARADIGM_IMAGES[locale] in visible
    assert (ROOT / "resources" / PARADIGM_IMAGES[locale]).is_file()
    for term in ("**Identity", "**Surface", "**Deployment", "**Coding Agent", "**Router", "**Local Runtime", "**Agent Framework"):
        assert term in visible
    assert _rowspans(visible) == [5, 2, 2, 3]
    assert len(re.findall(r"<td>⭐{3,5}</td>", visible)) == 12
    assert len(re.findall(r"^<details markdown=\"1\">$", text, flags=re.MULTILINE)) == 1
    assert not re.search(r"<details[^>]*\sopen(?:\s|>)", text)


def test_paradigms_trilingual_identities_urls_and_freshness_match() -> None:
    texts = {locale: _text(path) for locale, path in PARADIGM_PAGES.items()}
    deployment_phrases = {
        "zh-TW": ("OpenCode 程式在本機執行", "不會把 OpenCode 程式搬到雲端"),
        "en": ("The OpenCode process runs locally", "does not move the OpenCode process to the cloud"),
        "zh-Hans": ("OpenCode 程序在本地运行", "不会把 OpenCode 程序搬到云端"),
    }
    for locale, phrases in deployment_phrases.items():
        assert all(phrase in texts[locale] for phrase in phrases)
    marker = (
        "<!-- freshness: canonical=resources/agent-paradigms.md; verified_on=2026-08-30; "
        "scope=tool-identity,surfaces,deployment,security,project-status; max_age_days=90 -->"
    )
    required_literals = (
        "https://opencode.ai/docs/",
        "https://pi.dev/docs/latest",
        "https://openrouter.ai/docs/faq",
        "https://ollama.com/",
        "https://github.com/NousResearch/hermes-agent",
        "https://github.com/openclaw/openclaw",
    )
    forbidden = (
        "$5 VPS",
        "200+ provider",
        "€549",
        "0 data exposure",
        "零資料外洩",
        "零数据外泄",
        "沒有任何 cloud API call",
        "没有任何 cloud API call",
    )
    for text in texts.values():
        assert text.count(marker) == 1
        for literal in required_literals:
            assert literal in text
        for stale in forbidden:
            assert stale not in text
    assert _external_urls(texts["zh-TW"]) == _external_urls(texts["en"]) == _external_urls(texts["zh-Hans"])

"""Setup-guide beginner path, safety, grouping, and locale-mirror contracts."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "zh-TW": ROOT / "resources/setup-guide.md",
    "en": ROOT / "resources/setup-guide.en.md",
    "zh-Hans": ROOT / "resources/setup-guide.zh-Hans.md",
}
READMES = {
    "zh-TW": ROOT / "README.md",
    "en": ROOT / "README.en.md",
    "zh-Hans": ROOT / "README.zh-Hans.md",
}
FRESHNESS = (
    "<!-- freshness: canonical=resources/setup-guide.md; "
    "verified_on=2026-08-31; "
    "scope=install-paths,api-keys,authentication,provider-entrypoints,project-status; "
    "max_age_days=90 -->"
)
TABLE_GROUPS = ((4, 4, 5, 7), (2, 1, 1, 1), (7, 1))
CORE_TERMS = (
    "Chat Surface",
    "API",
    "API Key",
    "Environment Variable",
    "Runtime",
    "Package Manager",
    "CLI Agent",
)
NATIVE_INSTALLERS = (
    "curl -fsSL https://claude.ai/install.sh | bash",
    "irm https://claude.ai/install.ps1 | iex",
)
LEGACY_ANCHORS = {
    "zh-TW": (
        "a--申請第一個-api-key約-10-分鐘",
        "b--裝本機環境約-10-分鐘",
        "c--跑第一個-hello-claudepy約-5-分鐘",
        "d--第一次裝-claude-code約-10-分鐘stage-5--for-developer-會用到",
        "e--第一個-skill-範例約-5-分鐘stage-53-會用到",
    ),
    "en": (
        "a--get-your-first-api-key-about-10-minutes",
        "b--install-your-local-environment-about-10-minutes",
        "c--run-your-first-hello-claudepy-about-5-minutes",
        "d--install-claude-code-for-the-first-time-about-10-minutes-needed-for-stage-5--for-developer",
        "e--your-first-skill-example-about-5-minutes-needed-for-stage-53",
    ),
    "zh-Hans": (
        "a--申请第一个-api-key约-10-分钟",
        "b--装本机环境约-10-分钟",
        "c--跑第一个-hello-claudepy约-5-分钟",
        "d--第一次装-claude-code约-10-分钟stage-5--for-developer-会用到",
        "e--第一个-skill-示例约-5-分钟stage-53-会用到",
    ),
}


def _without_details(text: str) -> str:
    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.DOTALL)


def _external_urls(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r"https://[^)\s<>\"']+", text))


def _table_shapes(text: str) -> tuple[tuple[int, ...], ...]:
    shapes: list[tuple[int, ...]] = []
    for table in re.findall(r"<table>.*?</table>", text, flags=re.DOTALL):
        groups = re.findall(r"<tbody>(.*?)</tbody>", table, flags=re.DOTALL)
        spans: list[int] = []
        for group in groups:
            rows = re.findall(r"<tr>", group)
            headers = re.findall(
                r'<th scope="rowgroup" rowspan="(\d+)">', group
            )
            assert len(headers) == 1
            assert int(headers[0]) == len(rows)
            assert group.index('scope="rowgroup"') < group.find("</tr>")
            spans.append(int(headers[0]))
        shapes.append(tuple(spans))
    return tuple(shapes)


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_visible_beginner_path_keeps_choices_terms_practice_and_exit(
    locale: str, page: Path
) -> None:
    text = page.read_text(encoding="utf-8")
    visible = _without_details(text)

    positions = [
        visible.index("## 📌"),
        visible.index("## 🚪"),
        visible.index("## 🧩"),
        visible.index("## 📚"),
        visible.index("## 🛠 A"),
        visible.index("## 🛠 B"),
        visible.index("## 🛠 C"),
        visible.index("## 🛠 D"),
        visible.index("## 🛠 E"),
        visible.index("## ✅"),
    ]
    assert positions == sorted(positions)
    for term in CORE_TERMS:
        assert f"**{term}" in visible
        assert visible.index(f"**{term}") < positions[4]

    assert "Web Chat" in visible
    assert "Desktop App" in visible
    assert "IDE Assistant" in visible
    assert "CLI Agent" in visible
    assert "**API**" in visible
    assert "claude-sonnet-5" in visible
    assert "uv python install 3.12" in visible
    assert ".claude/skills/hello-skill/SKILL.md" in visible


@pytest.mark.parametrize("page", PAGES.values())
def test_seven_secondary_disclosures_are_closed(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    openings = re.findall(r"^<details\b[^>]*>", text, flags=re.MULTILINE)
    assert openings == ['<details markdown="1">'] * 7
    assert not re.search(r"<details\b[^>]*\bopen\b", text)


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_all_fifteen_published_a_to_e_anchors_remain_exact(
    locale: str, page: Path
) -> None:
    text = page.read_text(encoding="utf-8")
    explicit = tuple(re.findall(r'^<a id="([^"]+)"></a>$', text, flags=re.MULTILINE))
    assert explicit == LEGACY_ANCHORS[locale]


@pytest.mark.parametrize("page", PAGES.values())
def test_three_tables_use_real_rowgroups_and_keep_editorial_ratings(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    assert _table_shapes(text) == TABLE_GROUPS
    assert text.count("⭐⭐⭐⭐⭐") >= 12
    assert text.count("⭐⭐⭐⭐") >= 8
    assert '<th scope="rowgroup"></th>' not in text


def test_three_locales_share_freshness_sources_commands_and_model_ids() -> None:
    url_orders = []
    for page in PAGES.values():
        text = page.read_text(encoding="utf-8")
        assert text.count(FRESHNESS) == 1
        url_orders.append(_external_urls(text))
        for command in NATIVE_INSTALLERS:
            assert command in text
        assert text.count("claude-sonnet-5") == 1
        assert text.count("uv python install 3.12") == 1
    assert len(set(url_orders)) == 1


def test_devin_desktop_replaces_the_retired_windsurf_entry() -> None:
    labels = {
        "zh-TW": "Devin Desktop（原 Windsurf）",
        "en": "Devin Desktop (formerly Windsurf)",
        "zh-Hans": "Devin Desktop（原 Windsurf）",
    }
    for locale, page in PAGES.items():
        text = page.read_text(encoding="utf-8")
        assert text.count('href="https://devin.ai/desktop"') == 1
        assert labels[locale] in text
        assert "https://windsurf.com/editor" not in text


@pytest.mark.parametrize("page", PAGES.values())
def test_secret_setup_is_copyable_and_gitignore_precedes_env_creation(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    exercise = text[text.index("## 🛠 C") : text.index("## 🛠 D")]
    assert exercise.index(".gitignore") < exercise.index("PASTE_YOUR_KEY_HERE")
    assert "ANTHROPIC_API_KEY=PASTE_YOUR_KEY_HERE" in exercise
    assert "uv run --python 3.12 --with anthropic --with python-dotenv" in exercise
    assert "if block.type == \"text\"" in exercise


def test_copyable_examples_are_localized_without_changing_the_commands() -> None:
    english = PAGES["en"].read_text(encoding="utf-8")
    english_examples = english[english.index("## 🛠 C") : english.index("## ✅")]
    assert not re.search(r"[\u3400-\u9fff]", english_examples)
    assert "Introduce yourself in one sentence." in english_examples
    assert "# What this project does" in english_examples
    assert "When the user asks for a greeting:" in english_examples

    simplified = PAGES["zh-Hans"].read_text(encoding="utf-8")
    simplified_examples = simplified[
        simplified.index("## 🛠 C") : simplified.index("## ✅")
    ]
    for traditional in ("從", "讀取", "請用", "這個", "規則", "條件", "當使用者", "回覆"):
        assert traditional not in simplified_examples
    assert "请用一句话介绍你自己。" in simplified_examples
    assert "# 这个 project 要做什么" in simplified_examples
    assert "当使用者请你打招呼时：" in simplified_examples


@pytest.mark.parametrize("page", PAGES.values())
def test_volatile_prices_credits_and_stale_install_paths_do_not_return(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    forbidden = (
        "30-45",
        "30–45",
        "$20/month",
        "$20/月",
        "1000 credits",
        "1000 credit",
        "$0.14",
        "free for a week",
        "免費一週",
        "免费一周",
        "npm install -g @anthropic-ai/claude-code",
        "Node.js v18",
        "no native desktop app",
        "暫無原生 desktop app",
        "暂无原生 desktop app",
        '""',
        "“”",
    )
    assert not any(value in text for value in forbidden)
    assert not re.search(r"\b\d+(?:\.\d+)?[kKmM]\+?\s+(?:GitHub\s+)?stars\b", text)


def test_freshness_config_enrols_setup_guide_fact_pack_and_page() -> None:
    config = yaml.safe_load((ROOT / "scripts/freshness-models.yml").read_text(encoding="utf-8"))
    pack = config["setup_guide_fact_pack"]
    assert pack["canonical"] == "resources/setup-guide.md"
    assert pack["verified_on"] == "2026-08-31"
    assert pack["official_sources"]["devin_desktop"] == "https://devin.ai/desktop"
    assert pack["scope"] == [
        "install-paths",
        "api-keys",
        "authentication",
        "provider-entrypoints",
        "project-status",
    ]
    page = next(
        item
        for item in config["verified_pages"]
        if item["canonical"] == "resources/setup-guide.md"
    )
    assert page["required_scopes"] == pack["scope"]
    assert page["max_age_days"] == 90


def test_readme_router_no_longer_promises_a_fixed_setup_time() -> None:
    for page in READMES.values():
        text = page.read_text(encoding="utf-8")
        lines = "\n".join(line for line in text.splitlines() if "setup-guide" in line)
        assert "30-45" not in lines and "30–45" not in lines
        assert "CLI Agent" in lines
        assert "API" in lines


def test_maintainer_docs_keep_required_resources_visible_and_catalogs_secondary() -> None:
    design = (ROOT / "stages/DESIGN.md").read_text(encoding="utf-8")
    assert "### Setup guide 固定結構" in design
    assert "必讀官方起點、五星編輯推薦" in design
    assert "7 個 `<details markdown=\"1\">` 全部預設關閉" in design
    assert "`4／4／5／7`" in design
    assert "不為了版面齊全而新增圖片" in design

    testing_plan = (ROOT / "docs/TESTING_PLAN.md").read_text(encoding="utf-8")
    assert "### Setup guide — choose one door and finish one result" in testing_plan
    assert "required reading remains visible" in testing_plan
    assert "`scripts/test_setup_guide_content.py`" in testing_plan

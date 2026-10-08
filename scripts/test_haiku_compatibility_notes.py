"""Offline contracts for deliberately retained Haiku 4.5 examples."""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASES = ("examples/README", "stages/02-prompt-engineering", "stages/03-tool-use-and-hello-agent")
LOCALES = ("", ".en", ".zh-Hans")
GUIDE = "https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide"
EXPECTED_MODELS = {'examples/stage-1/04-cross-provider/starter.py': ['claude-haiku-4-5'],
 'examples/stage-1/05-error-handling/starter_anthropic.py': ['claude-haiku-4-5'],
 'examples/stage-2/01-prompt-eval-loop/starter_anthropic.py': ['claude-haiku-4-5'],
 'examples/stage-3/01-function-calling/starter_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-3/02-multi-tool-selection/starter_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-3/03-react-from-scratch/starter_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-3/04-multi-step-reasoning/starter_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-3/05-error-handling/starter_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-3/06-schema-design/starter_bad_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-3/06-schema-design/starter_good_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-4/01-same-agent-two-frameworks/starter_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-4/02-multi-agent-roles/starter_anthropic.py': ['anthropic/claude-haiku-4-5-20251001'],
 'examples/stage-4/03-graph-workflow/starter_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-4/04-codeact-vs-json-tool/starter_anthropic.py': ['anthropic/claude-haiku-4-5-20251001'],
 'examples/stage-4/05-typed-agent/starter_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-6/04-full-rag-pipeline/starter_anthropic.py': ['claude-haiku-4-5'],
 'examples/stage-6/05-long-term-memory/starter_anthropic.py': ['claude-haiku-4-5'],
 'examples/stage-7/01-multi-agent-debate/starter_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-7/02-eval/starter_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-7/03-observability/starter_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-7/04-sdk-advanced/starter_anthropic.py': ['claude-haiku-4-5-20251001'],
 'examples/stage-7/05-deploy/starter_anthropic.py': ['claude-haiku-4-5-20251001']}


@pytest.mark.parametrize("base", BASES)
@pytest.mark.parametrize("locale", LOCALES)
def test_compatibility_notice_is_visible_and_actionable(base: str, locale: str) -> None:
    text = (ROOT / f"{base}{locale}.md").read_text(encoding="utf-8")
    visible = re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.S)
    notice = next(line for line in visible.splitlines() if GUIDE in line)
    for term in ("Haiku 4.5", "claude-haiku-5-5", "adaptive thinking", 'type == "text"',
                 "temperature", "top_p", "top_k", "tokens"):
        assert term in notice
    semantic_terms = {
        "": ("相容性基準", "不代表最新或最低價", "不能只換 model ID", "重新計算", "原樣保留", "只追加歷史", "離線測試"),
        ".en": ("compatibility baseline", "rather than claiming the latest or lowest-price", "changing only the model ID is insufficient", "recount", "unchanged", "append-only", "offline tests"),
        ".zh-Hans": ("兼容性基准", "不代表最新或最低价", "不能只换 model ID", "重新计算", "原样保留", "只追加历史", "离线测试"),
    }
    assert all(term in notice for term in semantic_terms[locale])
    assert text.count(GUIDE) == 1


@pytest.mark.parametrize("base", BASES)
def test_migration_link_order_matches_across_locales(base: str) -> None:
    links = []
    for locale in LOCALES:
        text = (ROOT / f"{base}{locale}.md").read_text(encoding="utf-8")
        links.append(re.findall(r"https://platform\.claude\.com/docs/en/models/[^)\s]+", text))
    assert links[0] == links[1] == links[2]


@pytest.mark.parametrize("path,expected", EXPECTED_MODELS.items())
def test_runnable_compatibility_model_ids_are_unchanged(path: str, expected: list[str]) -> None:
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    actual = sorted({
        node.value for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
        and node.value.startswith(("claude-haiku-", "anthropic/claude-haiku-"))
    })
    assert actual == expected


@pytest.mark.parametrize("locale", LOCALES)
def test_stage_snippets_keep_their_compatibility_ids(locale: str) -> None:
    stage2 = (ROOT / f"stages/02-prompt-engineering{locale}.md").read_text(encoding="utf-8")
    stage3 = (ROOT / f"stages/03-tool-use-and-hello-agent{locale}.md").read_text(encoding="utf-8")
    assert 'model="claude-haiku-4-5"' in stage2
    assert stage3.count('model="claude-haiku-4-5-20251001"') == 2

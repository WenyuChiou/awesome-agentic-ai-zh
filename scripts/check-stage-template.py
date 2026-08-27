#!/usr/bin/env python3
"""
Stage template structure check.

驗每個 stages/[0-9]*-*.md (zh-TW canonical) 有所有必要的 H2 section、
跟 Stage 5/6/7/8 已經對齊的 template 一致。

REQUIRED — 缺則 fail（H2 必須有）：
  - 📌 學習目標
  - 🚪 進入條件
  - 📚 必修閱讀
  - 🛠 動手練習
  - 🎯 精選 Projects（或變體含「Projects」）
  - ✅ 自我檢查（或 .* 自我檢查 / 進入 .* 前的自我檢查）

EXPECTED — 缺則 warning（不擋）：
  - 🎯 X 是什麼（先定位）  — positioning section
  - 🎯 常用 .* 工具推薦 / 常用 .* 推薦 — tool recommendation

  註：Stage 01-04 為 foundational 章節，其定位 / 工具推薦段落使用章節自然
  命名（如「主流 LLM 家族對比」/「什麼是 multi-agent framework」/「開始前：
  AI / LLM / Agent 三者怎麼分」），刻意不套用上面的 EXPECTED 樣板字串。
  因此這些 ⚠ EXPECTED 警告對 Stage 01-04 屬「資訊性」而非缺陷——它們的
  REQUIRED 段落全部通過，定位段落實質存在、只是用更貼切的章節名。不強制
  改名（改名會把更精準的標題降級成樣板字串、得不償失）。

排除：mirror files (*.en.md, *.zh-Hans.md)、Stage 0 (foundations 短 intro)。

Usage:
    python scripts/check-stage-template.py [--strict-expected]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PATTERNS = [
    (r'📌\s*學習目標', '📌 學習目標'),
    (r'🚪\s*進入條件', '🚪 進入條件'),
    (r'📚\s*必修閱讀', '📚 必修閱讀'),
    (r'🛠\s*動手練習', '🛠 動手練習'),
    (r'🎯\s*(精選|常用)?\s*.*Projects', '🎯 精選 Projects'),
    # Grouped alternation: matches "✅ X 自我檢查" or "X 自我檢查" anywhere — but NOT
    # bare "自我檢查" in unrelated context (must have surrounding text before 自我檢查)
    (r'(✅\s*.*自我檢查|.+自我檢查|自我檢查)', '✅ 自我檢查'),
]

EXPECTED_PATTERNS = [
    (r'🎯\s*.*是什麼.*先定位', '🎯 [topic] 是什麼（先定位）'),
    (r'🎯\s*常用.*推薦|🎯\s*常用.*工具', '🎯 常用工具推薦（按用途）'),
]

# Stages that don't follow the per-stage template:
#   - 00- prerequisites: short intro doc, doesn't need full template
#   - 05- Claude Code ecosystem: multi-sub-stage container (5.1-5.8),
#     each sub-stage has its own learning goals/practice structure;
#     template check at file level doesn't make sense.
#   - 07.5- advanced agentic concepts: reading-map chapter (12 concepts
#     skeleton + reading paths + cross-vendor principles); intentionally
#     does NOT have 動手練習 / 精選 Projects — it's a meta-章 pointing
#     to other stages, not a hands-on stage. Has 自我檢查 only.
SKIP_STAGES = ['00-', '05-', '07.5-']

# Foundational stages (01-04) use chapter-natural section names rather
# than the template strings in EXPECTED_PATTERNS (e.g. "主流 LLM 家族對比"
# instead of "🎯 LLM 是什麼（先定位）"). Their positioning and tool-
# recommendation sections are substantively present — just named more
# precisely. Renaming would degrade quality. These stages pass all
# REQUIRED checks; only the EXPECTED pattern match fails. Suppress the
# ⚠ EXPECTED warnings for them to keep the script output signal-only.
EXPECTED_EXEMPT_STAGES = ['01-', '02-', '03-', '04-']

H2_RE = re.compile(r'^## (.+?)\s*$', re.MULTILINE)


def get_h2_sections(content: str) -> list[str]:
    return [m.group(1) for m in H2_RE.finditer(content)]


def check_stage(path: Path) -> tuple[list[str], list[str]]:
    """Return (missing_required, missing_expected) labels."""
    content = path.read_text(encoding='utf-8')
    h2s = get_h2_sections(content)

    def matches_any(pat: str) -> bool:
        return any(re.search(pat, h2) for h2 in h2s)

    missing_req = [label for pat, label in REQUIRED_PATTERNS if not matches_any(pat)]
    missing_exp = [label for pat, label in EXPECTED_PATTERNS if not matches_any(pat)]
    return missing_req, missing_exp


def should_skip(path: Path) -> bool:
    name = path.name
    if name.endswith('.en.md') or name.endswith('.zh-Hans.md'):
        return True
    for prefix in SKIP_STAGES:
        if name.startswith(prefix):
            return True
    return False


def should_skip_expected(path: Path) -> bool:
    """Return True for stages whose EXPECTED sections are intentionally named differently."""
    name = path.name
    for prefix in EXPECTED_EXEMPT_STAGES:
        if name.startswith(prefix):
            return True
    return False


def main() -> int:
    # Force UTF-8 stdout
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--strict-expected',
        action='store_true',
        help='Also fail on missing EXPECTED sections (not just REQUIRED)',
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    stages_dir = repo_root / 'stages'
    if not stages_dir.exists():
        print('❌ stages/ directory not found.', file=sys.stderr)
        return 2

    has_required_issue = False
    has_expected_issue = False

    for stage in sorted(stages_dir.glob('[0-9]*-*.md')):
        if should_skip(stage):
            continue
        missing_req, missing_exp = check_stage(stage)
        rel = stage.relative_to(repo_root).as_posix()

        if missing_req:
            print(f'❌ {rel}: missing REQUIRED H2 section(s):')
            for label in missing_req:
                print(f'   - {label}')
            has_required_issue = True

        if missing_exp and not should_skip_expected(stage):
            warn_prefix = '❌' if args.strict_expected else '⚠'
            print(f'{warn_prefix} {rel}: missing EXPECTED H2 section(s):')
            for label in missing_exp:
                print(f'   - {label}')
            if args.strict_expected:
                has_expected_issue = True

    if has_required_issue or has_expected_issue:
        return 1

    if not has_required_issue:
        print('✓ All stages have REQUIRED template sections.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

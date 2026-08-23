#!/usr/bin/env python3
"""
check-duplicate-repos.py — 同一個 GitHub repo 在同一個檔案裡被列了兩次就報錯。

為什麼需要這個 gate：2026-08-23，`microsoft/agent-framework` 被當成新專案加進
`stages/04-agent-frameworks.md`，但它 2026-06-13 就已經在同一張表裡了。星數、
license、push 日期全部查證過，唯獨沒有先 grep 一次 slug。**六個內容 gate 全綠**,
因為 `check-catalog-counts.py` 只掃 `resources/mcp-skills-catalog.*`,看不到
stage 裡的散文表格,而其他 gate 根本不管重複。是 reviewer 讀 diff 讀出來的。

順帶暴露了第二件事:那張表的表頭寫「17 個項目」,而它在那次改動之前就已經有
18 列。加一列又刪一列、淨變動為零,所以那個 off-by-one 差點被一起遮掉。

檢查範圍刻意是「同一個檔案內」而不是「跨檔案」:同一個 repo 出現在 Stage 4 的
框架表、Stage 7 的 harness 表、跟 catalog 裡是**正常且刻意**的(不同 stage 從不同
角度講同一個工具),跨檔案報錯只會製造雜訊。真正的錯誤形狀是「同一份清單裡列了
兩次」。

用法:
    python scripts/check-duplicate-repos.py            # 全掃
    python scripts/check-duplicate-repos.py --quiet    # 只印問題
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_fences import code_line_flags  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
# Mirrors the other gates' exclude sets. `.claude` holds git worktrees, which
# are a second full copy of the tree: without this every finding doubles.
SCAN_EXCLUDE_DIRS = {".git", ".claude", "_build", "node_modules", "book", ".venv"}

# The FULL path, not just owner/repo. Collapsing subdirectory links to their
# repo root was the first version's mistake: `claude-plugins-official` alone
# contributes eleven rows, one per plugin under /tree/main/plugins/, and a book
# repo contributes one row per chapter. Those are eleven and two distinct
# entries, not duplicates, and reporting them made the gate useless.
#
# The defect this exists for had both rows pointing at the same repo ROOT, so
# comparing full paths still catches it while leaving monorepo listings alone.
REPO_RE = re.compile(
    r"github\.com/([A-Za-z0-9][\w.-]*)/([\w.-]+(?:/[\w.\-/]*[\w.-])?)(?=[)\s\"'>#?]|$)",
    re.IGNORECASE,
)

# Not real project links.
IGNORE_OWNERS = {"sponsors", "orgs", "features", "settings", "marketplace", "apps"}
# A repo legitimately named like a path segment we would otherwise mistake.
IGNORE_REPOS = {"", ".", ".."}

# Files where repeating a repo is the point, not a defect.
SKIP_FILES = {
    "CHANGELOG.md",          # history: the same repo recurs across dated entries
    "CONTRIBUTORS.md",
}
SKIP_DIR_PARTS = {".github"}  # outreach drafts quote the same repo repeatedly

# Deliberate repeats a human has already looked at. Same shape as
# scripts/mirror-parity-baseline.json: a ratchet, so a NEW duplicate still
# fails while a confirmed-intentional one stays quiet. Keyed "<file>::<slug>".
#
# The one entry here is a book listed one row per chapter, where every row
# necessarily links the same repo root. That is not the defect this gate is
# for, and no URL comparison can separate the two, so it is recorded rather
# than engineered around.
BASELINE = {
    "stages/03-tool-use-and-hello-agent.md::datawhalechina/hello-agents",
    "stages/03-tool-use-and-hello-agent.en.md::datawhalechina/hello-agents",
    "stages/03-tool-use-and-hello-agent.zh-Hans.md::datawhalechina/hello-agents",
}


def _blocks(text: str):
    """Yield (kind, start_line, [lines]) for each contiguous TABLE or LIST block.

    The unit of comparison is deliberately the block, not the file. A repo named
    in prose and then listed in a table below is normal and correct; the repo
    does that on purpose, since a stage explains a tool and then catalogues it.
    The defect shape is narrower: the same repo occupying two rows of ONE table,
    or two items of ONE list. The first version of this gate compared per file
    and reported 229 problems, almost all of them legitimate — a check that
    noisy gets muted, which is worse than not having it.
    """
    cur_kind = None
    cur: list[tuple[int, str]] = []
    # Fenced code is classified by the shared parser, never by a local ```
    # toggle: issues #95/#97 showed a closer may not carry an info string and
    # must be at least as long as its opener, so the naive toggle mis-pairs a
    # nested sample. test_check_anchors.py enforces this and caught the first
    # version of this file doing exactly that.
    flags = code_line_flags(text)
    for n, (line, is_code) in enumerate(zip(text.split("\n"), flags), start=1):
        if is_code:
            if cur:
                yield cur_kind, cur
                cur, cur_kind = [], None
            continue
        s = line.lstrip()
        kind = None
        if s.startswith("|"):
            kind = "table"
        elif re.match(r"(?:[-*+]|\d+\.)\s", s):
            kind = "list"
        if kind and kind == cur_kind:
            cur.append((n, line))
        elif kind:
            if cur:
                yield cur_kind, cur
            cur_kind, cur = kind, [(n, line)]
        else:
            # A blank line does not end a list (loose lists are still one list);
            # any other prose line does.
            if s == "" and cur_kind == "list":
                continue
            if cur:
                yield cur_kind, cur
            cur, cur_kind = [], None
    if cur:
        yield cur_kind, cur


def _slug(line: str) -> str | None:
    """The repo this row/item IS, which is its FIRST github link.

    Later links on the same line are cross-references, not entries. Comparing
    every link on the line made an entry that says "see also X" collide with X's
    own entry further down, which is a normal and useful thing to write. Every
    one of the six findings the previous version produced was that shape.
    """
    for m in REPO_RE.finditer(line):
        owner, repo = m.group(1), m.group(2)
        if owner.lower() in IGNORE_OWNERS or repo in IGNORE_REPOS:
            continue
        return f"{owner}/{re.sub(r'[.]git$', '', repo)}"
    return None


def dupes_in(text: str) -> dict[str, list[int]]:
    """slug -> line numbers, but only when repeated INSIDE one table or list."""
    found: dict[str, list[int]] = {}
    for kind, block in _blocks(text):
        seen: dict[str, list[int]] = defaultdict(list)
        for n, line in block:
            slug = _slug(line)
            if slug and n not in seen[slug]:
                seen[slug].append(n)
        for slug, lines in seen.items():
            if len(lines) > 1:
                found.setdefault(slug, []).extend(lines)
    return found


def md_files() -> list[Path]:
    out = []
    for fp in REPO_ROOT.rglob("*.md"):
        rel = fp.relative_to(REPO_ROOT)
        if any(p in SCAN_EXCLUDE_DIRS for p in rel.parts):  # abs-parts-ok: rel = fp.relative_to(REPO_ROOT) two lines up
            continue
        if fp.name in SKIP_FILES or any(p in SKIP_DIR_PARTS for p in rel.parts):  # abs-parts-ok: same rel as above
            continue
        out.append(fp)
    return sorted(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quiet", action="store_true", help="只印問題")
    args = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, ValueError):
                pass

    files = md_files()
    problems = 0
    for fp in files:
        rel = fp.relative_to(REPO_ROOT).as_posix()
        for slug, lines in sorted(dupes_in(fp.read_text(encoding="utf-8")).items()):
            if len(lines) < 2 or f"{rel}::{slug}" in BASELINE:
                continue
            problems += 1
            print(f"❌ {rel}: {slug} 出現在 {len(lines)} 行 — {', '.join(map(str, lines))}")

    if not args.quiet:
        print(f"checked {len(files)} markdown file(s)")
    if problems:
        print()
        print(f"Found {problems} duplicate-repo problem(s).")
        print("同一份清單列同一個 repo 兩次,通常是「以為是新的」而沒有先 grep slug。")
        print("跨檔案重複是正常的,這個 gate 只看同一個檔案內。")
        return 1
    print("✓ No repo is listed twice within the same file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

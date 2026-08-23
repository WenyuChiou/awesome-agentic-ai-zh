#!/usr/bin/env python3
"""
zh-Hans mainland-localization pass — part of the mirror process.

The zh-Hans mirrors are produced from the zh-TW canonical via opencc
`tw2s` (character-level 繁→簡 only). `tw2s` does NOT localize Taiwan
vocabulary to Mainland vocabulary, so the mirrors read like
"simplified-character Taiwan Chinese". This script applies a CURATED,
blanket-SAFE Taiwan→Mainland substitution table + mainland quote
convention, so the localization PERSISTS across future mirror regens.

Motivated by + sourced from community PR #18 (Rain120,
"使中文简体更加贴合大陆的阅读习惯"). Each pair below was grep-verified
against the whole zh-Hans corpus to have a single unambiguous meaning
in THIS repo (zero/negligible false positives).

DELIBERATELY EXCLUDED (context-sensitive — a blanket map corrupts them;
needs OpenCC `tw2sp` curated dict or per-occurrence human judgment):
  预设  → 默认 (software default) vs 假定/假设 (assume) — split by meaning
  教学  → 教程 (tutorial) vs 教学 (teaching/instruction) — split by meaning
  走完/往下走/差别/涵盖 — stylistic, not Taiwan-isms (no localization value)
  English `script`/`词` — context-dependent

Usage:
    python scripts/zh-hans-localize.py [--apply]   # default = dry-run
    python scripts/zh-hans-localize.py --check     # exit 1 if any drift

Only touches *.zh-Hans.md. Skips fenced ``` code blocks and inline
`code` spans (a Taiwan term inside a code sample / string literal must
stay verbatim).
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_fences import code_line_flags  # noqa: E402

# Curated blanket-safe Taiwan→Mainland vocabulary (grep-verified, this repo)
VOCAB = {
    "呼叫": "调用",      # programming call/invoke (mainland: 调用)
    "印出": "打印",      # print output
    "出包": "搞砸",      # Taiwan slang "screw up"
    "软体": "软件",      # software
    "网路": "网络",      # network
    "档案": "文件",      # file (tech context)
    "字串": "字符串",    # string (programming)
    "函式": "函数",      # function (programming)
    "程式": "程序",      # program / code
    "品质": "质量",      # quality
    "回应": "响应",      # response (LLM/API output)
    # --- batch 2 (grep-verified, 2026-05; sourced from PR #18 / residue scan) ---
    "使用者": "用户",    # user (all prose occ = "user"; meta tables PROTECTed)
    "命令列": "命令行",  # command line
    "字元": "字符",      # character (text/encoding)
    "物件": "对象",      # object (programming / 3D — mainland tech standard)
    # EXCLUDED on purpose (grep-verified unsafe — do NOT add):
    #   介面→界面  : appears in the Stage 8 H1 + README link text →
    #                changing it shifts the anchor slug & breaks inbound
    #                `#…操作介面…` links (anchor-corruption risk).
    #   軟體/專案/腳本/連結/設定/飛書/資料/預設 : only occur inside the
    #                PROTECTed reference docs (nothing to localize).
    #   预设/教学  : context-sensitive (default vs assume / tutorial vs
    #                teaching) — no single mainland equivalent.
    #   影片→视频  : MOVED to GUARDED_VOCAB below — see why there.
    #   协定→协议  : NOT auto-replaced, and not guarded either. 协定 is a
    #                legitimate mainland word for an AGREEMENT (贸易协定,
    #                停战协定); it is only wrong when it means PROTOCOL. Both
    #                senses are open sets, so neither a lookbehind nor a
    #                blocklist of compounds would hold. Five protocol-sense
    #                occurrences were fixed by hand on 2026-08-23; a reviewer
    #                caught them because `--check` reporting clean is not
    #                evidence for a pair this table does not contain.
    #                If you are about to add it: don't. Fix by hand.
}

# Terms that are UNSAFE as blanket substrings but safe with a context guard.
#
# VOCAB is plain `str.replace`, so a Taiwan term that happens to be a substring
# of a different, correct word corrupts the host word. The previous answer was
# to drop such terms entirely — and that is a worse failure than it looks:
# dropping 影片 left FIVE genuine residues sitting in tracked zh-Hans files
# while this gate reported "clean — no drift". The warn-only lint job could see
# them the whole time; nothing acted on it, because the blocking gate said fine.
#
# An exclusion is silent. A guard is not. Prefer a guard.

# What may sit between 投 and 影片 while the two still form ONE word: markdown
# emphasis and link syntax, whitespace, and the \x00N\x00 placeholders _mask
# leaves where inline code used to be.
#
# A plain `(?<!投)影片` lookbehind is NOT enough, and the gap is ordinary
# markdown rather than anything exotic — `投**影片**`, `投_影片_`,
# `投[影片](url)`, a line wrap between the two, or a `投` that ended up inside
# an inline-code span all defeat literal adjacency and yield 投视频, the very
# corruption the guard exists to prevent. Python's `re` has no variable-length
# lookbehind, so the separator is matched explicitly instead.
#
# The separator stops at a PARAGRAPH BREAK, and is otherwise unlimited.
#
# Review first suggested a length bound ({0,3}) to stop a long run bridging
# unrelated text — `投\n\n***\n\n影片` (a bare 投 ending a paragraph, then a
# horizontal rule) being read as one word. The finding was right; a length bound
# was the wrong remedy, and measurably so: under {0,3} the perfectly ordinary
# `投 **[影片](url)**` needs 4 separator characters, falls out of the guard, and
# comes out as 投 **[视频](url)** — a corruption, which is the direction that
# matters. Narrowing the separator does not make the guard safer; it makes it
# protect LESS, and under-protecting is the failure mode that silently rewrites
# tracked files.
#
# A blank line is the honest boundary: markdown emphasis never spans one, so two
# characters either side of a paragraph break are never one word. That kills the
# bridging cases exactly, with no ceiling on legitimate markdown in between.
_SLIDES_SEP = (
    r"(?:"
    r"[^\S\r\n]"             # horizontal whitespace
    r"|[*_~`\[\]()]"         # markdown emphasis / link syntax
    r"|\x00\d+\x00"          # a masked inline-code span
    r"|\r?\n(?!\s*\r?\n)"    # a single line wrap — but never a blank line
    r")*"
)

GUARDED_VOCAB = [
    # 影片 → 视频, except inside 投影片 (projected slides), where 影片 is just a
    # substring. The collision is real, not theoretical: the zh-TW canonical
    # stages/03-tool-use-and-hello-agent.md carries 影片優先 on line 63 and
    # 投影片 on line 67 — four lines apart, in one section.
    #
    # That pair used to exist in the zh-Hans mirror too, which is what this
    # guard was built against; the mirror has since been fully localized
    # (影片→视频, and 投影片→幻灯片 by hand, since no rule covers the latter).
    # The guard is still load-bearing: the canonical still has the shape, so
    # any future port of that section reintroduces it.
    #
    # When in doubt this PROTECTS. The two errors are not symmetric: a missed
    # substitution leaves a Taiwan word visible in a rendered page, where a
    # reader can see it; a wrong substitution silently corrupts a word in a gate
    # that REWRITES tracked files, and nothing downstream is looking for it.
    #
    # The backstop for a bug IN THIS RULE is every test in
    # test_zh_hans_localize.py built from hand-written input/output pairs —
    # test_slides_survive_*, test_a_paragraph_break_ends_the_separator,
    # test_long_but_unbroken_markdown_still_protects_the_slides_word,
    # test_guard_protects_rather_than_guesses — and NOT the two tree-scanning
    # tests in that same file. Both of those now call localize() as their only source
    # of truth, so if the rule below wrongly declines to substitute, they agree
    # with it in unison and both report "clean". Only input/output pairs written
    # out by hand can disagree with the code.
    #
    # The warn-only lint job is not a backstop either: `影片` was removed from
    # its BANNED_TW list in the same change, because `grep -F` cannot express
    # the 投影片 exception and would flag the one correct usage forever.
    #
    # Scope: this reasons about MARKDOWN separators, not arbitrary HTML. `投<br>
    # 影片` would fall out of the guard and be localized. No such split exists in
    # the corpus and breaking a two-character word with raw HTML has no reason to
    # happen, so it is left uncovered deliberately rather than unknowingly.
    (
        re.compile(rf"(投{_SLIDES_SEP})?影片"),
        lambda m: m.group(0) if m.group(1) else "视频",
        "影片→视频",
    ),
]
# Mainland quote convention: 「」 (Japanese/Taiwan corner brackets)
# → “ ” (GB/T fullwidth curly double quotes).
QUOTES = {"「": "“", "」": "”"}

# Reference / policy docs that INTENTIONALLY contain TW↔Mainland term
# pairs as documentation — substituting there corrupts the reference
# (e.g. `| 使用者 | 用户 |` → `| 用户 | 用户 |`). Mirrors lint.yml's own
# zh-Hans residue-check exclusion list (project-established convention).
PROTECT = {
    "resources/style-guide.zh-Hans.md",
    "resources/glossary.zh-Hans.md",
}

REPO = Path(__file__).resolve().parent.parent
INLINE_RE = re.compile(r"`[^`\n]*`")


def _mask(text: str):
    """Replace fenced + inline code with placeholders so substitutions
    never touch code. Returns (masked_text, restore_map).

    Fenced blocks are located by the shared parser (md_fences) rather than by
    the `​```.*?```` DOTALL regex this used to use. That regex pairs fences
    greedily-left-to-right, so it mis-pairs a nested example — exactly the #95
    shape — and here the consequence is worse than a bad report: this script
    REWRITES files, so a mis-paired fence means vocabulary substitutions land
    inside a code sample.

    Inline code is still handled by the regex below; md_fences is line-based
    and deliberately says nothing about spans within a line.
    """
    store: list[str] = []

    def stash_text(chunk: str) -> str:
        store.append(chunk)
        return f"\x00{len(store) - 1}\x00"

    # Fenced blocks, by line, using the shared classification.
    lines = text.split("\n")
    flags = code_line_flags(text)
    out: list[str] = []
    run: list[str] = []
    for line, in_code in zip(lines, flags):
        if in_code:
            run.append(line)
            continue
        if run:
            out.append(stash_text("\n".join(run)))
            run = []
        out.append(line)
    if run:
        out.append(stash_text("\n".join(run)))
    text = "\n".join(out)

    text = INLINE_RE.sub(lambda m: stash_text(m.group(0)), text)
    return text, store


def _unmask(text: str, store: list[str]) -> str:
    for i, original in enumerate(store):
        text = text.replace(f"\x00{i}\x00", original)
    return text


def localize(text: str) -> tuple[str, dict[str, int]]:
    masked, store = _mask(text)
    counts: dict[str, int] = {}
    for tw, cn in {**VOCAB, **QUOTES}.items():
        c = masked.count(tw)
        if c:
            masked = masked.replace(tw, cn)
            counts[f"{tw}→{cn}"] = c
    # Guarded rules run after the blanket ones. None of the VOCAB pairs create
    # or destroy 影片/投影片, so the order is not load-bearing today — but the
    # guards are the context-sensitive ones, so they go last on purpose.
    #
    # Counted by hand rather than via subn(): the pattern deliberately MATCHES
    # the protected form too (that is how it sees the context), so subn()'s
    # count would report every 投影片 as a substitution it did not make.
    for pattern, repl, label in GUARDED_VOCAB:
        hits = 0

        def _apply(m, _repl=repl):
            nonlocal hits
            out = _repl(m)
            if out != m.group(0):
                hits += 1
            return out

        masked = pattern.sub(_apply, masked)
        if hits:
            counts[label] = hits
    return _unmask(masked, store), counts


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description=__doc__)
    # --check and --apply are semantically exclusive: --check is the CI
    # gate (read-only, exit 1 on drift); --apply writes. Don't combine.
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    ap.add_argument("--check", action="store_true", help="exit 1 if any file would change (CI gate, read-only)")
    args = ap.parse_args()

    # `.claude` holds git worktrees (`.claude/worktrees/<name>/`), which contain a
    # full second copy of the tree. Without this the gate scans those copies and
    # reports drift that does not exist in the working tree — and worse, the
    # PROTECT list below never matches them, because it is keyed on repo-relative
    # paths like "resources/style-guide.zh-Hans.md" while the worktree copy is at
    # ".claude/worktrees/<name>/resources/style-guide.zh-Hans.md". A protected file
    # therefore becomes unprotected the moment a worktree exists. Found 2026-08-02
    # when a stray worktree made this gate fail on a file it is meant to skip.
    SKIP_PARTS = {".ai", ".claude", "node_modules", "_build", "_site", "book"}
    files = sorted(
        p for p in REPO.rglob("*.zh-Hans.md")
        # Intersect against the REPO-RELATIVE parts. Using p.parts tests the
        # ABSOLUTE path, and SKIP_PARTS contains ".claude" — so from a checkout
        # under `.claude/worktrees/<name>/` this matched every file and the gate
        # scanned 0 of 68 zh-Hans files while printing "✓ zh-Hans localization
        # clean — no drift". Eighth instance of the 2026-08-02 bug class; pinned
        # by test_repo_scan_excludes.py.
        if not SKIP_PARTS & set(p.relative_to(REPO).parts)
        and p.relative_to(REPO).as_posix() not in PROTECT
    )
    total = 0
    changed_files = 0
    agg: dict[str, int] = {}
    for fp in files:
        src = fp.read_text(encoding="utf-8")
        out, counts = localize(src)
        if out != src:
            changed_files += 1
            n = sum(counts.values())
            total += n
            for k, v in counts.items():
                agg[k] = agg.get(k, 0) + v
            rel = fp.relative_to(REPO).as_posix()
            print(f"  {rel}: {n} ({', '.join(f'{k}×{v}' for k, v in counts.items())})")
            if args.apply:
                fp.write_text(out, encoding="utf-8")

    print()
    print(f"=== {total} substitutions across {changed_files} file(s) ===")
    for k, v in sorted(agg.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    if args.check:
        print("❌ zh-Hans localization drift detected — run "
              "`python scripts/zh-hans-localize.py --apply`"
              if total else "✓ zh-Hans localization clean — no drift")
        return 1 if total else 0
    if not args.apply:
        print("\n(dry-run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

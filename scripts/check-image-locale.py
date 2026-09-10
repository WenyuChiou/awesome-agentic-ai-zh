#!/usr/bin/env python3
"""check-image-locale.py — mirror pages must embed their own locale's diagram.

`check-locale-links.py` deliberately only matches link targets ending in `.md`
(its LINK_RE hard-codes the suffix), so image paths are invisible to it — and to
every other gate here. In 2026-08 that hole was holding 9 mismatches: four
Traditional-only diagrams embedded on English and Simplified pages with localized
alt text over an unlocalized image, so a reader got an English caption above a
figure whose every label is Traditional Chinese.

Convention in `resources/diagrams/`: a diagram that has locale variants has all
three — `NAME.png` (zh-TW), `NAME.en.png`, `NAME.zh-Hans.png`. 20 diagrams follow
it, and the three variants are genuinely different renders, not copies.

Two distinct findings, deliberately kept apart:

  FIXABLE  — the correct sibling EXISTS on disk but the page points elsewhere.
             Always an error: it is a one-line edit.
  KNOWN GAP — the sibling does NOT exist, so the page falls back to the zh-TW
             asset. Fixing needs someone to regenerate artwork, which is manual
             (diagrams are produced by pasting prompts into ChatGPT image-gen and
             no source file is committed). These live in KNOWN_MISSING below so
             they are explicit and, crucially, so a NEW one fails the build
             instead of quietly joining the pile.

Usage:
    python scripts/check-image-locale.py           # exit 1 on mismatch or orphan
    python scripts/check-image-locale.py --strict  # also fail on known gaps
    python scripts/check-image-locale.py --list    # print the current inventory
"""

import argparse
import glob
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_fences import strip_code_blocks  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
DIAGRAM_DIR = REPO_ROOT / "resources" / "diagrams"

# ![alt](path) — relative paths only; skip external URLs and data: URIs.
IMAGE_RE = re.compile(r"!\[[^\]]*\]\((?!https?:|data:)([^)\s]+)\)")
# The README animation has a real static-image link, not a second embed. Only
# approved banner and role-map fallbacks count; unrelated links stay unchanged.
BANNER_FALLBACK_RE = re.compile(
    r"(?<!!)\[[^\]]*\]\(((?:\.\./)*resources/diagrams/(?:banner|branch-decision-tree)(?:\.en|\.zh-Hans)?\.png)\)"
)
LOCALE_SUFFIXES = {".en.md": "en", ".zh-Hans.md": "zh-Hans"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
# `.claude` and `.ai` are listed for parity with the other gates even though
# glob.glob (unlike Path.rglob) already skips dot-directories by default — relying
# on that implicit behaviour is what let a git worktree under .claude/worktrees/
# silently double the corpus for three rglob-based gates in 2026-08.
SKIP_DIR_PARTS = {".git", ".claude", ".ai", "_build", "_site", "node_modules", "book"}

# Assets with no localized variant yet. Each entry is (page, asset-as-written).
# Removing an entry after generating the artwork is the whole point — do not add
# to this list to silence a NEW mismatch without a reason recorded in CHANGELOG.
#
# Currently EMPTY, and that is the desired state: the nine original gaps were all
# closed on 2026-08-03 (13 diagrams generated, .jpg -> .png), so every entry here
# became dead data referencing paths that no longer exist. An empty allowlist
# means any new gap fails the build immediately instead of joining a pile.
KNOWN_MISSING: set[tuple[str, str]] = set()



def localized_name(asset: str, locale: str) -> str:
    """diagrams/foo.png + 'en' -> diagrams/foo.en.png"""
    p = Path(asset)
    return str(p.with_name(f"{p.stem}.{locale}{p.suffix}")).replace("\\", "/")


def base_name(asset: str) -> str:
    """Strip any existing locale infix: foo.en.png -> foo.png"""
    p = Path(asset)
    for loc in ("en", "zh-Hans"):
        if p.stem.endswith(f".{loc}"):
            return str(p.with_name(f"{p.stem[: -len(loc) - 1]}{p.suffix}")).replace("\\", "/")
    return asset.replace("\\", "/")


def scan(page: Path):
    """Yield (lineno, asset) for each relative image reference outside code fences."""
    # Fenced code blanked by the shared parser (md_fences), not a local
    # toggle — see #95/#97. Blanking preserves line numbers.
    text = strip_code_blocks(page.read_text(encoding="utf-8"), source=str(page))
    for i, line in enumerate(text.split("\n"), 1):
        for m in (*IMAGE_RE.finditer(line), *BANNER_FALLBACK_RE.finditer(line)):
            asset = m.group(1)
            if Path(asset).suffix.lower() in IMAGE_EXTS:
                yield i, asset


def unreferenced_diagrams() -> list[str]:
    """Return diagram assets that no Markdown page embeds.

    Superseded generated images are easy to leave behind because the locale
    gate historically looked only from page -> asset. Scan every Markdown page
    in the repository so the reverse asset -> page direction is also enforced.
    """
    referenced: set[Path] = set()
    for name in sorted(glob.glob("**/*.md", recursive=True, root_dir=REPO_ROOT)):
        rel = Path(name)
        if any(part in SKIP_DIR_PARTS for part in rel.parts):  # abs-parts-ok: glob(root_dir=REPO_ROOT) yields relative names
            continue
        page = REPO_ROOT / rel
        for _, asset in scan(page):
            referenced.add((page.parent / asset).resolve())

    if not DIAGRAM_DIR.exists():
        return []
    return [
        path.relative_to(REPO_ROOT).as_posix()
        for path in sorted(DIAGRAM_DIR.rglob("*"))
        if path.is_file()
        and path.suffix.lower() in IMAGE_EXTS
        and path.resolve() not in referenced
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true",
                    help="also fail on documented known-missing assets")
    ap.add_argument("--list", action="store_true", help="print inventory and exit")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    fixable, gaps, dead, checked = [], [], [], 0

    for name in sorted(glob.glob("**/*.md", recursive=True, root_dir=REPO_ROOT)):
        if any(p in SKIP_DIR_PARTS for p in Path(name).parts):  # abs-parts-ok: glob(root_dir=REPO_ROOT) yields relative names
            continue
        locale = next((v for k, v in LOCALE_SUFFIXES.items() if name.endswith(k)), None)
        if locale is None:
            continue
        page = REPO_ROOT / name
        rel_page = Path(name).as_posix()
        for lineno, asset in scan(page):
            checked += 1
            resolved = (page.parent / asset).resolve()
            if not resolved.exists():
                dead.append((rel_page, lineno, asset))
                continue
            want = localized_name(base_name(asset), locale)
            if Path(asset).as_posix() == want:
                continue  # already correct
            if (page.parent / want).resolve().exists():
                fixable.append((rel_page, lineno, asset, want))
            elif (rel_page, asset) in KNOWN_MISSING:
                gaps.append((rel_page, lineno, asset, want))
            else:
                fixable.append((rel_page, lineno, asset, want + "  [asset must be created]"))

    orphans = unreferenced_diagrams()

    if args.list:
        print(f"{checked} image reference(s) on locale-suffixed pages")
        print(f"  correct: {checked - len(fixable) - len(gaps) - len(dead)}")
        print(f"  fixable mismatches: {len(fixable)}")
        print(f"  documented gaps: {len(gaps)}")
        print(f"  dead references: {len(dead)}")
        print(f"  unreferenced diagrams: {len(orphans)}")
        for rel, ln, a, w in gaps:
            print(f"    gap  {rel}:{ln}  {a}  (wants {Path(w).name})")
        return 0

    for rel, lineno, asset in dead:
        print(f"❌ {rel}:{lineno}: image does not exist on disk: {asset}")
    for rel, lineno, asset, want in fixable:
        print(f"❌ {rel}:{lineno}: embeds {asset}")
        print(f"     this is a {locale_of(rel)} page — it should use {want}")
    for asset in orphans:
        print(f"❌ unreferenced diagram: {asset}")

    print(f"\nchecked {checked} image reference(s) on locale-suffixed pages")
    if gaps:
        print(f"{len(gaps)} documented gap(s) (no localized asset exists yet):")
        for rel, lineno, asset, want in gaps:
            print(f"  ⚠️  {rel}:{lineno} needs {Path(want).name}")

    if dead or fixable or orphans:
        print(
            f"\nFound {len(dead) + len(fixable)} image-locale problem(s) "
            f"and {len(orphans)} unreferenced diagram(s)."
        )
        return 1
    if args.strict and gaps:
        print(f"\n--strict: {len(gaps)} known gap(s) still unresolved.")
        return 1
    print("\n✓ Image locales match, and every diagram is embedded by a page.")
    return 0


def locale_of(rel: str) -> str:
    for suffix, loc in LOCALE_SUFFIXES.items():
        if rel.endswith(suffix):
            return loc
    return "?"


if __name__ == "__main__":
    sys.exit(main())

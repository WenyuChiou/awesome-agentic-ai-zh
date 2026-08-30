#!/usr/bin/env python3
"""Stage the curriculum content into _build/docs/ for the mkdocs site.

Why this exists: the learning content lives at the REPO ROOT
(`stages/`, `tracks/`, `branches/`, `services/`, `resources/`, root `*.md`), not in
a `docs/` subfolder. mkdocs 1.6 hard-errors if `docs_dir` is the parent
of `mkdocs.yml` (i.e. you cannot point docs_dir at the repo root). The
standard fix is a build-staging copy: this script mirrors the
whitelisted content into `_build/docs/` (which `.gitignore` already
covers via `_build/`), preserving the exact directory layout so every
relative link + the mkdocs-static-i18n `.en.md` / `.zh-Hans.md` suffix
pairing keeps working unchanged.

Idempotent: wipes and repopulates `_build/docs/` each run.
stdlib-only (CI runner needs no extra deps for this step).

Usage:
  python scripts/build-docs-tree.py
  # then: mkdocs build   (mkdocs.yml has docs_dir: _build/docs)
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEST = REPO / "_build" / "docs"

# Whole directories copied verbatim (they hold .md + referenced .png etc.)
CONTENT_DIRS = [
    "stages",
    "tracks",
    "branches",
    "services",
    "resources",
    "walkthroughs",
    "examples",
    "docs",  # repo's docs/ → staged to _build/docs/docs/ (matches nav: docs/HOW_TO_USE.md)
]

# Root-level pages (plus their .en.md / .zh-Hans.md siblings, auto-found)
ROOT_STEMS = [
    "index",
    "README",
    "PROGRESS",
    "ROADMAP",
    "CONTRIBUTING",
    "CODE_OF_CONDUCT",
    "SECURITY",
    "CONTRIBUTORS",
    "CHANGELOG",
    "RESOURCES",
    "CAPSTONE",
]


def main() -> int:
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)

    copied_dirs = 0
    for d in CONTENT_DIRS:
        src = REPO / d
        if src.is_dir():
            # symlinks=False (default): copies symlink objects, does NOT
            # follow them — safe against symlink-escape out of the tree.
            shutil.copytree(src, DEST / d)
            copied_dirs += 1

    copied_files = 0
    # The repo's GitHub README must NOT be staged as `README.md`: mkdocs
    # special-cases that filename as a directory index, which collides with
    # `index.md` (the landing) and resolves inconsistently per i18n locale.
    # Stage it as `about.md`; mkdocs_hooks.py rewrites in-content
    # `README.md` links to `about.md` so they still resolve on the site.
    for stem in ROOT_STEMS:
        out_stem = {"README": "about"}.get(stem, stem)
        for suffix in (".md", ".en.md", ".zh-Hans.md"):
            f = REPO / f"{stem}{suffix}"
            if f.is_file():
                shutil.copy2(f, DEST / f"{out_stem}{suffix}")
                copied_files += 1

    print(f"staged {copied_dirs} dirs + {copied_files} root pages -> {DEST.relative_to(REPO)}")
    # Sanity: home page must exist or mkdocs has no site index
    if not (DEST / "index.md").is_file():
        print("ERROR: index.md missing from staged tree", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

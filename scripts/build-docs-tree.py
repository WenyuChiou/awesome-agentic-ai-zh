#!/usr/bin/env python3
"""Stage the curriculum content into _build/docs/ for the mkdocs site.

Why this exists: the learning content lives at the REPO ROOT
(`stages/`, `tracks/`, `branches/`, `resources/`, root `*.md`), not in
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

import os
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
    "resources",
    "walkthroughs",
    "examples",
]

# Reader-facing files that live below an otherwise maintainer-only directory.
# `docs/plans/` and `docs/TESTING_PLAN.md` are repository evidence, not lessons;
# copying the whole directory made 35 internal planning pages searchable online.
CONTENT_FILES = ["docs/HOW_TO_USE.md", "docs/stylesheets/extra.css"]

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


def _selected_public_sources() -> list[Path]:
    """Return every repository path that may enter the public build tree."""

    sources = [REPO / directory for directory in CONTENT_DIRS]
    sources.extend(REPO / relative for relative in CONTENT_FILES)
    for stem in ROOT_STEMS:
        for suffix in (".md", ".en.md", ".zh-Hans.md"):
            source = REPO / f"{stem}{suffix}"
            if source.exists() or source.is_symlink():
                sources.append(source)
    return sources


def _public_symlinks(sources: list[Path]) -> list[Path]:
    """Find symlinks without following them into an external tree."""

    found: set[Path] = set()
    for source in sources:
        if source.is_symlink():
            found.add(source)
            continue
        if not source.is_dir():
            continue
        for directory, dirnames, filenames in os.walk(source, followlinks=False):
            parent = Path(directory)
            for name in (*dirnames, *filenames):
                candidate = parent / name
                if candidate.is_symlink():
                    found.add(candidate)
    return sorted(found)


def main() -> int:
    symlinks = _public_symlinks(_selected_public_sources())
    if symlinks:
        print(
            "ERROR: refusing to publish symlinks from the reader-facing tree:",
            file=sys.stderr,
        )
        for path in symlinks:
            try:
                shown = path.relative_to(REPO)
            except ValueError:
                shown = path
            print(f"- {shown}", file=sys.stderr)
        return 1

    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)

    copied_dirs = 0
    for d in CONTENT_DIRS:
        src = REPO / d
        if src.is_dir():
            # copytree dereferences symlinks by default, so the fail-closed
            # preflight above must reject every symlink before this copy.
            ignore = _ignore_example_internal_markdown if d == "examples" else None
            shutil.copytree(src, DEST / d, ignore=ignore)
            copied_dirs += 1

    copied_files = 0
    for rel in CONTENT_FILES:
        src = REPO / rel
        if not src.is_file():
            print(f"ERROR: required public page missing: {rel}", file=sys.stderr)
            return 1
        target = DEST / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        copied_files += 1

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


def _ignore_example_internal_markdown(directory: str, names: list[str]) -> set[str]:
    """Keep example landing pages public without publishing agent internals.

    Example code and each localized ``README`` remain available.  Files such as
    ``SKILL.md`` and its implementation references belong in the GitHub source
    tree; rendering them as ordinary lessons creates broken runtime-placeholder
    links and noisy search results.
    """

    del directory
    return {
        name
        for name in names
        if name.endswith(".md") and not name.startswith("README")
    }


if __name__ == "__main__":
    sys.exit(main())

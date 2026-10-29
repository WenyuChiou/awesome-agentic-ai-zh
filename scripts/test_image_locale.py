#!/usr/bin/env python3
"""Regression tests for scripts/check-image-locale.py.

Pins the 2026-08 gap: `check-locale-links.py` only matches link targets ending in
`.md`, so image paths were invisible to every gate. Nine mismatches were shipping —
English and Simplified pages embedding Traditional-only diagrams under localized
alt text.

The important behaviour to pin is the split between the two finding classes:
  - the correct sibling EXISTS -> hard error, it is a one-line fix
  - the sibling does NOT exist -> a documented gap, because fixing it means
    regenerating artwork by hand
If that split ever collapses, either the build breaks on work nobody can do in a
commit, or new mismatches quietly join the documented pile. Both are tested.

Run:  python scripts/test_image_locale.py     (plain asserts, no pytest needed)
 or:  pytest scripts/test_image_locale.py
"""
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "check_image_locale", Path(__file__).with_name("check-image-locale.py")
)
cil = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(cil)

SCRIPT = Path(__file__).with_name("check-image-locale.py")


def _run(files: dict, assets=(), args=()):
    """Build a temp corpus, run the checker in it, return (returncode, stdout)."""
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "scripts").mkdir()
        (root / "scripts" / SCRIPT.name).write_text(
            SCRIPT.read_text(encoding="utf-8"), encoding="utf-8"
        )
        # The gate imports the shared fence parser (md_fences, issue #97),
        # so the temp repo needs it too or the subprocess dies on ImportError
        # and every assertion below fails for the wrong reason.
        _SHARED = SCRIPT.parent / "md_fences.py"
        (root / "scripts" / _SHARED.name).write_text(
            _SHARED.read_text(encoding="utf-8"), encoding="utf-8"
        )
        for a in assets:
            p = root / a
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"")
        for name, body in files.items():
            p = root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(root / "scripts" / SCRIPT.name), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            cwd=str(root),
        )
        return r.returncode, r.stdout


# --- name helpers -----------------------------------------------------------

def test_localized_name():
    assert cil.localized_name("d/foo.png", "en") == "d/foo.en.png"
    assert cil.localized_name("d/foo.png", "zh-Hans") == "d/foo.zh-Hans.png"


def test_base_name_strips_locale_infix():
    assert cil.base_name("d/foo.en.png") == "d/foo.png"
    assert cil.base_name("d/foo.zh-Hans.png") == "d/foo.png"
    assert cil.base_name("d/foo.png") == "d/foo.png"


def test_base_name_survives_dotted_stem():
    # multi-llm-delegation-composition has hyphens, not dots, but guard anyway
    assert cil.base_name("d/a.b.png") == "d/a.b.png"


# --- the two finding classes ------------------------------------------------

def test_fixable_when_sibling_exists():
    rc, out = _run({"page.en.md": "![x](d/foo.png)\n"}, assets=["d/foo.png", "d/foo.en.png"])
    assert rc == 1, out
    assert "should use d/foo.en.png" in out


def test_clean_when_correct_sibling_used():
    rc, out = _run({"page.en.md": "![x](d/foo.en.png)\n"},
                   assets=["d/foo.png", "d/foo.en.png"])
    assert rc == 0, out


def test_missing_sibling_not_in_allowlist_is_an_error():
    """A NEW mismatch must fail rather than silently join the documented pile."""
    rc, out = _run({"page.en.md": "![x](d/foo.png)\n"}, assets=["d/foo.png"])
    assert rc == 1, out
    assert "asset must be created" in out


def test_dead_reference_is_an_error():
    rc, out = _run({"page.en.md": "![x](d/nope.png)\n"})
    assert rc == 1, out
    assert "does not exist on disk" in out


# --- scoping ----------------------------------------------------------------

def test_ignores_images_in_code_fences():
    body = "```md\n![x](d/foo.png)\n```\n"
    rc, out = _run({"page.en.md": body}, assets=["d/foo.png", "d/foo.en.png"])
    assert rc == 0, out


def test_ignores_external_urls():
    rc, out = _run({"page.en.md": "![x](https://example.com/a.png)\n"})
    assert rc == 0, out


def test_ignores_canonical_zh_tw_pages():
    """page.md is the zh-TW canonical — using the unsuffixed asset is correct."""
    rc, out = _run({"page.md": "![x](d/foo.png)\n"}, assets=["d/foo.png", "d/foo.en.png"])
    assert rc == 0, out


def test_ignores_non_image_links():
    rc, out = _run({"page.en.md": "[text](d/foo.png)\n"}, assets=["d/foo.png", "d/foo.en.png"])
    assert rc == 0, out


# --- allowlist wiring -------------------------------------------------------

def test_known_missing_is_empty():
    """The nine original gaps were closed on 2026-08-03; it must stay at zero.

    This asserted `== 9` while the backlog existed. All nine were generated
    (13 diagrams, .jpg -> .png), which left every entry pointing at a path that
    no longer exists — dead data that could never match. An empty allowlist is
    the stronger state: a new gap fails the build instead of joining a pile.

    Re-adding an entry is a deliberate act and needs a reason in CHANGELOG, per
    the comment above KNOWN_MISSING itself.
    """
    assert cil.KNOWN_MISSING == set(), (
        "a locale gap was allowlisted instead of fixed: " + repr(cil.KNOWN_MISSING)
    )


def test_known_missing_entries_are_pairs():
    for entry in cil.KNOWN_MISSING:
        assert isinstance(entry, tuple) and len(entry) == 2, entry
        page, asset = entry
        assert page.endswith((".en.md", ".zh-Hans.md")), page
        assert Path(asset).suffix.lower() in cil.IMAGE_EXTS, asset


def test_repo_currently_has_no_fixable_mismatch():
    """Live assertion against the real corpus."""
    r = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(Path(__file__).resolve().parent.parent),
    )
    assert r.returncode == 0, f"fixable image-locale mismatch present:\n{r.stdout}"


def test_unreferenced_diagram_is_an_error():
    rc, out = _run(
        {"page.md": "No image here.\n"},
        assets=["resources/diagrams/old.png"],
    )
    assert rc == 1, out
    assert "unreferenced diagram: resources/diagrams/old.png" in out


def test_referenced_diagram_is_clean():
    rc, out = _run(
        {"page.md": "![clear alt](resources/diagrams/current.png)\n"},
        assets=["resources/diagrams/current.png"],
    )
    assert rc == 0, out


def test_generated_motion_fallbacks_match_site_hook():
    spec = importlib.util.spec_from_file_location(
        "motion_fallback_hooks", SCRIPT.with_name("mkdocs_hooks.py")
    )
    hooks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hooks)
    assert cil.GENERATED_SVG_PNG_FALLBACKS == (
        hooks._ANIMATED_BANNERS | hooks._ANIMATED_ROLE_DIAGRAMS
    )


def test_referenced_animations_keep_only_their_matching_static_fallbacks():
    for stem in ("banner", "branch-decision-tree"):
        for suffix in ("", ".en", ".zh-Hans"):
            svg = f"resources/diagrams/{stem}{suffix}.svg"
            png = f"resources/diagrams/{stem}{suffix}.png"
            rc, out = _run(
                {f"README{suffix}.md": f"![route]({svg})\n"},
                assets=[svg, png], args=["--strict"],
            )
            assert rc == 0, out


def test_arbitrary_svg_does_not_hide_an_orphan_png():
    rc, out = _run(
        {"page.md": "![route](resources/diagrams/other.svg)\n"},
        assets=["resources/diagrams/other.svg", "resources/diagrams/other.png"],
    )
    assert rc == 1, out
    assert "unreferenced diagram: resources/diagrams/other.png" in out


def _run_all():
    fns = [v for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"  FAIL  {fn.__name__}: {exc}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"  ERROR {fn.__name__}: {exc!r}")
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    return failed


if __name__ == "__main__":
    sys.exit(1 if _run_all() else 0)

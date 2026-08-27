"""Regression tests for scripts/check-2026-freshness.py freshness-gate coverage.

Run: python scripts/test_freshness.py   (plain asserts, no pytest needed)
 or: pytest scripts/test_freshness.py

Pins the two 2026-07 coverage holes a code review surfaced:
  1. The DeepSeek regex required a literal hyphen ('DeepSeek-R1'), so the
     space-form 'DeepSeek R1' (stages/01 picker rows) slipped through. Now
     'DeepSeek[- ]R1(?!-Distill)' catches both, still exempting -Distill variants.
  2. Mirror locales (.en.md / .zh-Hans.md) were hard-skipped, so a fact fixed in
     the zh-TW canonical but left stale in a mirror (e.g. agent-paradigms shipping
     a stale 'DeepSeek-R1') was never scanned. Mirrors are now scanned, per-file
     overrides + exclude_files follow the mirror to its canonical form, and the
     localized 'baseline' qualifier ('基線' / '基线') is recognized.
"""
from __future__ import annotations

import importlib.util
import tempfile
from datetime import date
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "check_2026_freshness", Path(__file__).with_name("check-2026-freshness.py")
)
fr = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(fr)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_REAL_CFG = fr.load_config(_REPO_ROOT)

# A minimal, self-contained R1 config so pattern tests don't drift with the real yml.
_R1_CFG = {
    'stale_patterns': [{
        'pattern': r'DeepSeek[- ]R1(?!-Distill)',
        'qualifier_terms': ['lineage', 'baseline', '基線', '基线'],
        'note': 'test-r1',
    }],
    'qualifier_context_lines': 2,
}


def _scan(text: str, cfg: dict, rel: str = "probe.md"):
    """Write `text` to a temp file at `rel` and return scan_file findings."""
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return fr.scan_file(p, cfg, root)


def _skip(rel: str, cfg: dict | None = None) -> bool:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("placeholder\n", encoding="utf-8")
        return fr.should_skip(p, root, cfg or {})


# ── Hole #1: DeepSeek regex space-form ────────────────────────────────────────

def test_space_form_deepseek_r1_is_flagged():
    # The exact hole: 'DeepSeek R1' (space) used to be missed entirely.
    findings = _scan("Hunyuan 可比 DeepSeek R1 推理、中文\n", _R1_CFG)
    assert len(findings) == 1
    assert findings[0][2] == "DeepSeek R1"


def test_hyphen_form_deepseek_r1_still_flagged():
    findings = _scan("NVIDIA NIM hosts DeepSeek-R1 / Qwen\n", _R1_CFG)
    assert len(findings) == 1
    assert findings[0][2] == "DeepSeek-R1"


def test_distill_variants_still_exempt_both_forms():
    # -Distill sub-models are separate small models, not the superseded flagship.
    assert _scan("uses DeepSeek-R1-Distill-Qwen-7B\n", _R1_CFG) == []
    assert _scan("uses DeepSeek R1-Distill-Qwen-7B\n", _R1_CFG) == []


def test_qualifier_suppresses_r1_both_english_and_cjk():
    assert _scan("DeepSeek-R1 lineage / Qwen\n", _R1_CFG) == []               # english
    assert _scan("可比 DeepSeek R1 推理 baseline、中文\n", _R1_CFG) == []       # loanword
    # localized baseline: qualifier one line away, still within ±2 window
    assert _scan("可比 DeepSeek R1 推理\n（對照 Opus 4.6 基线）\n", _R1_CFG) == []


# ── Hole #2: mirror locales are scanned ───────────────────────────────────────

def test_mirror_locales_are_not_skipped():
    # The core of hole #2: .en.md / .zh-Hans.md used to be hard-skipped.
    assert _skip("resources/agent-paradigms.en.md") is False
    assert _skip("resources/agent-paradigms.zh-Hans.md") is False
    assert _skip("resources/agent-paradigms.md") is False


def test_excluded_file_still_skipped_including_its_mirror():
    cfg = {'exclude_files': ['CHANGELOG.md']}
    assert _skip("CHANGELOG.md", cfg) is True
    # a mirror of an excluded canonical file is excluded too (canonical_rel)
    assert _skip("CHANGELOG.en.md", cfg) is True
    assert _skip("CHANGELOG.zh-Hans.md", cfg) is True


def test_excluded_dir_still_skipped():
    assert _skip(".ai/2026/notes.md") is True


def test_stale_ref_in_a_mirror_is_actually_caught():
    # End-to-end: an unqualified stale ref living in a .en.md mirror is reported.
    findings = _scan("Hosts DeepSeek-R1 / Qwen\n", _R1_CFG, rel="resources/x.en.md")
    assert len(findings) == 1


# ── canonical_rel + per-file override inheritance ─────────────────────────────

def test_canonical_rel_strips_mirror_suffix():
    assert fr.canonical_rel("stages/06-memory-rag.en.md") == "stages/06-memory-rag.md"
    assert fr.canonical_rel("stages/06-memory-rag.zh-Hans.md") == "stages/06-memory-rag.md"
    assert fr.canonical_rel("stages/06-memory-rag.md") == "stages/06-memory-rag.md"
    assert fr.canonical_rel("README.md") == "README.md"


def test_per_file_window_override_follows_mirror_to_canonical():
    # A qualifier 4 lines below the ref is out of the default ±2 window but inside
    # the ±5 override written for the *canonical* file — the mirror must inherit it.
    cfg = {
        'stale_patterns': [{
            'pattern': r'DeepSeek[- ]R1(?!-Distill)',
            'qualifier_terms': ['lineage'],
            'note': 't',
        }],
        'exclude_files_pattern_specific': [{'file': 'stages/wide.md', 'qualifier_window': 5}],
        'qualifier_context_lines': 2,
    }
    text = "title DeepSeek-R1 here\n\n\n\nrefer to release dates for lineage\n"
    # mirror inherits the canonical file's widened window -> qualifier reached -> clean
    assert _scan(text, cfg, rel="stages/wide.en.md") == []
    # a file WITHOUT the override uses ±2 -> qualifier out of reach -> flagged
    # (proves the widened window, not some other effect, is what suppresses it)
    assert len(_scan(text, cfg, rel="stages/narrow.en.md")) == 1


def test_stale_pattern_include_files_applies_to_canonical_and_mirrors_only():
    cfg = {
        'stale_patterns': [{
            'pattern': r'Gemini 3\.5 Flash',
            'include_files': ['stages/01.md'],
            'qualifier_terms': ['historical'],
            'note': 'stage-01-only',
        }],
    }
    assert len(_scan('Gemini 3.5 Flash\n', cfg, rel='stages/01.md')) == 1
    assert len(_scan('Gemini 3.5 Flash\n', cfg, rel='stages/01.en.md')) == 1
    assert _scan('Gemini 3.5 Flash\n', cfg, rel='stages/06.md') == []


# ── Ties to the REAL config (breaks if someone reverts the fixes) ─────────────

def test_real_config_recognizes_localized_baseline_for_opus_47():
    # The exact stages/08 zh-Hans false positive: current line, qualified by 基线.
    clean = "**72.7%**（Opus 4.6 基线，接近人类；Opus 4.7 / 4.8 数据未公布）\n"
    assert _scan(clean, _REAL_CFG) == []
    # but a genuinely stale, unqualified Opus 4.7 is still caught
    assert len(_scan("旗艦模型改用 Opus 4.7 可用\n", _REAL_CFG)) == 1


def test_real_config_space_form_r1_hole_closed():
    assert len(_scan("Hunyuan 可比 DeepSeek R1 推理、中文\n", _REAL_CFG)) == 1
    assert _scan("Hunyuan 可比 DeepSeek R1 推理 baseline、中文\n", _REAL_CFG) == []


# ── Machine-readable page freshness markers ──────────────────────────────────

_PAGE_CFG = {
    'stage01_fact_pack': {
        'canonical': 'stages/01.md',
        'verified_on': '2026-08-27',
        'scope': ['models', 'pricing', 'availability', 'deprecations'],
    },
    'verified_pages': [{
        'canonical': 'stages/01.md',
        'required_scopes': ['models', 'pricing', 'availability', 'deprecations'],
        'max_age_days': 90,
    }],
}


def _marker(
    day: str = '2026-08-27',
    scopes: str | None = None,
    age: int = 90,
    canonical: str = 'stages/01.md',
) -> str:
    scopes = scopes or 'models,pricing,availability,deprecations'
    return (
        f'<!-- freshness: canonical={canonical}; verified_on={day}; scope={scopes}; '
        f'max_age_days={age} -->\n'
    )


def _cfg_with_fact_pack(
    day: str = '2026-08-27',
    scopes: list[str] | None = None,
) -> dict:
    return {
        'stage01_fact_pack': {
            'canonical': 'stages/01.md',
            'verified_on': day,
            'scope': scopes or ['models', 'pricing', 'availability', 'deprecations'],
        },
        'verified_pages': _PAGE_CFG['verified_pages'],
    }


def _scan_markers(
    canonical: str,
    english: str | None = None,
    hans: str | None = None,
    today: date = date(2026, 8, 27),
    cfg: dict | None = None,
):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        stages = root / 'stages'
        stages.mkdir()
        (stages / '01.md').write_text(canonical, encoding='utf-8')
        if english is not None:
            (stages / '01.en.md').write_text(english, encoding='utf-8')
        if hans is not None:
            (stages / '01.zh-Hans.md').write_text(hans, encoding='utf-8')
        return fr.scan_verified_pages(root, cfg or _PAGE_CFG, today=today)


def test_valid_trilingual_freshness_markers_pass():
    marker = _marker()
    assert _scan_markers(marker, marker, marker) == ([], [])


def test_missing_mirror_marker_blocks():
    errors, warnings = _scan_markers(_marker(), _marker(), 'no marker\n')
    assert warnings == []
    assert any('01.zh-Hans.md: missing freshness marker' in item for item in errors)


def test_malformed_marker_blocks():
    malformed = '<!-- freshness: yesterday -->\n'
    errors, _ = _scan_markers(malformed, malformed, malformed)
    assert len(errors) == 3
    assert all('malformed freshness marker' in item for item in errors)


def test_future_marker_blocks():
    future = _marker(day='2026-08-28')
    errors, _ = _scan_markers(future, future, future)
    assert len([item for item in errors if 'in the future' in item]) == 3


def test_locale_marker_mismatch_blocks():
    canonical = _marker()
    english = _marker(day='2026-08-26')
    errors, _ = _scan_markers(canonical, english, canonical)
    assert any('01.en.md: freshness marker differs' in item for item in errors)


def test_old_marker_warns_without_blocking():
    old = _marker(day='2026-05-01')
    errors, warnings = _scan_markers(
        old, old, old, cfg=_cfg_with_fact_pack(day='2026-05-01')
    )
    assert errors == []
    assert len(warnings) == 3
    assert all('118 days old' in item for item in warnings)


def test_scope_and_max_age_must_match_config():
    wrong = _marker(scopes='models,pricing', age=30)
    errors, _ = _scan_markers(
        wrong, wrong, wrong, cfg=_cfg_with_fact_pack(scopes=['models', 'pricing'])
    )
    assert len([item for item in errors if 'scope' in item]) == 3
    assert len([item for item in errors if 'max_age_days' in item]) == 3


def test_canonical_path_must_match_config():
    wrong = _marker(canonical='stages/not-01.md')
    errors, _ = _scan_markers(wrong, wrong, wrong)
    assert len([item for item in errors if 'canonical=' in item]) == 3


def test_fact_pack_date_must_match_page_marker():
    cfg = {
        'stage01_fact_pack': {
            'canonical': 'stages/01.md',
            'verified_on': '2026-08-26',
            'scope': ['models', 'pricing', 'availability', 'deprecations'],
        },
        'verified_pages': _PAGE_CFG['verified_pages'],
    }
    marker = _marker()
    errors, _ = _scan_markers(marker, marker, marker, cfg=cfg)
    assert any('fact pack verified_on=2026-08-26 differs' in item for item in errors)


def test_verified_page_requires_matching_fact_pack():
    cfg = {'verified_pages': _PAGE_CFG['verified_pages']}
    marker = _marker()
    errors, _ = _scan_markers(marker, marker, marker, cfg=cfg)
    assert 'stages/01.md: matching fact pack is missing' in errors


if __name__ == "__main__":
    import sys
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in tests:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {fn.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)

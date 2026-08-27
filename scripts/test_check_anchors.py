#!/usr/bin/env python3
"""Regression tests for scripts/check-anchors.py's anchor and fence parsing.

Pins issue #95. `strip_code_blocks` used to toggle `in_code` on any line
starting with ```, which disagrees with CommonMark — and therefore with the
renderer that actually publishes the site — in two ways:

1. A closing fence may not carry an info string. Given

       ```                <- opens
       ```python          <- CONTENT (info string)
       ...
       ```                <- closes the block opened on line 1
       ```                <- OPENS a new one

   the toggler pairs 1-2 and 3-4; the renderer pairs 1-3 and leaves 4 opening
   an unterminated block. In examples/stage-4/04-codeact-vs-json-tool/README.*
   that swallowed four `##` headings into a code block on the published site
   while every gate stayed green.

2. A closing fence must be at least as long as its opener. That is how a block
   legitimately contains a shorter fence, and it is the fix applied to those
   three files (outer fence widened to ````).

The consequence is the point: when the gate and the renderer disagree about
which lines are code, the gate is validating a document nobody publishes.

Run:  python scripts/test_check_anchors.py     (plain asserts, no pytest needed)
 or:  pytest scripts/test_check_anchors.py
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

_SPEC = importlib.util.spec_from_file_location(
    "check_anchors", Path(__file__).with_name("check-anchors.py")
)
ca = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ca)


def _visible(md: str) -> set[str]:
    """Headings the gate can see after code blocks are blanked."""
    return ca.collect_anchors(ca.strip_code_blocks(md))


def test_explicit_html_anchor_is_a_real_target() -> None:
    assert "cli-8" in _visible('<a id="cli-8"></a>\n')
    assert "legacy-name" in _visible("<a name='legacy-name'></a>\n")
    assert ca.anchor_exists('<a id="cli-8"></a>\n', "cli-8")
    assert ca.anchor_exists("<a name='legacy-name'></a>\n", "legacy-name")


def test_data_attributes_are_not_explicit_anchor_targets() -> None:
    md = '<a data-id="phantom-id" data-name="phantom-name"></a>\n'
    assert "phantom-id" not in _visible(md)
    assert "phantom-name" not in _visible(md)
    assert not ca.anchor_exists(md, "phantom-id")
    assert not ca.anchor_exists(md, "phantom-name")


def test_explicit_anchor_ids_are_exact_not_slugified() -> None:
    md = '<a id="Foo.Bar"></a>\n'
    assert "Foo.Bar" in _visible(md)
    assert "foobar" not in _visible(md)
    assert ca.anchor_exists(md, "Foo.Bar")
    assert not ca.anchor_exists(md, "foobar")
    assert not ca.anchor_exists(md, "foo.bar")


def test_explicit_html_anchor_inside_fence_is_not_a_target() -> None:
    assert "phantom" not in _visible('```html\n<a id="phantom"></a>\n```\n')
    assert not ca.anchor_exists(
        '```html\n<a id="phantom"></a>\n```\n', "phantom"
    )


def test_info_string_fence_does_not_close_a_block() -> None:
    """The exact #95 shape: a nested ```python must not terminate the block."""
    md = "\n".join([
        "# Title",
        "",
        "```",
        "transcript line",
        "```python",
        "code = 1",
        "```",
        "",
        "## After The Block",
        "",
        "```bash",
        "echo hi",
        "```",
    ])
    got = _visible(md)
    assert "after-the-block" in got, (
        "heading after the block is invisible — the parser mis-paired the fences. "
        f"saw {sorted(got)}"
    )
    assert "title" in got


def test_gate_matches_the_renderer_on_the_broken_shape() -> None:
    """The #95 defect verbatim: the gate must NOT see what the renderer hides.

    This is the pre-fix shape of examples/stage-4/04-codeact-vs-json-tool.
    CommonMark pairs the fences so that the trailing bare fence OPENS a block
    which swallows every heading after it. The renderer hid those headings; the
    naive toggler showed them, so check-anchors happily validated anchors
    pointing at headings that did not exist on the published site.

    Asserting the gate hides them is what makes the gate able to report the
    problem instead of masking it.
    """
    md = "\n".join([
        "```",              # opens
        "（LLM response）",
        "```python",        # info string -> content, does NOT close
        "x = 1",
        "```",              # closes the block opened on line 1
        "",
        "（framework runs it）",
        "```",              # OPENS a new block ...
        "",
        "## Comparison",    # ... so these are inside it
        "",
        "## Pitfalls",
    ])
    got = _visible(md)
    assert not ({"comparison", "pitfalls"} & got), (
        "the gate still sees headings the renderer swallows — it is validating "
        f"a document nobody publishes. saw {sorted(got)}"
    )

    def naive(content: str) -> str:
        out, in_code = [], False
        for line in content.split("\n"):
            if line.startswith("```"):
                in_code = not in_code
                out.append("")
                continue
            out.append("" if in_code else line)
        return "\n".join(out)

    naive_got = ca.collect_anchors(naive(md))
    assert {"comparison", "pitfalls"} <= naive_got, (
        "the naive toggler no longer disagrees on this fixture, so the fixture "
        "has stopped discriminating and would not catch a revert"
    )


def test_shorter_fence_inside_a_longer_one_is_content() -> None:
    """The rule the #95 fix depends on: a ```` block contains a ``` fence.

    Must assert the NEGATIVE. Asserting only that a trailing heading is visible
    passes even if the length rule is dropped, because the mis-paired fences
    just re-pair and the trailing heading still lands outside.
    """
    md = "\n".join(["````", "```", "## Not A Heading", "```", "````", "", "## Visible"])
    got = _visible(md)
    assert "visible" in got, f"trailing heading went missing: {sorted(got)}"
    assert "not-a-heading" not in got, (
        "the inner ``` closed the ```` block, so the transcript leaked into prose — "
        f"this is exactly the shape the #95 fix relies on. saw {sorted(got)}"
    )


def test_longer_fence_closes_a_shorter_opener() -> None:
    """CommonMark: the closer must be >= the opener, not exactly equal."""
    md = "\n".join(["```", "inside", "`````", "", "## Visible"])
    assert "visible" in _visible(md)


def test_closer_with_trailing_whitespace_still_closes() -> None:
    """CommonMark allows trailing whitespace on a closer; so does superfences.

    Unpinned, this survived a mutation that used `rest == ""` instead of
    `rest.strip()`. A trailing space is exactly what an editor or formatter
    adds, and the consequence is the gate silently hiding the rest of the file.
    """
    md = "\n".join(["```", "code", "```   ", "", "## Visible"])
    assert "visible" in _visible(md), (
        "a closing fence with trailing spaces stopped closing the block, so "
        "everything after it is now invisible to the gate"
    )


def test_backtick_in_info_string_is_not_a_fence() -> None:
    """```foo`bar is not a fence opener — in CommonMark or in superfences.

    Treating it as one hides the remainder of the file from the gate while the
    renderer keeps rendering it, which is the #93/#95 divergence shape again.
    """
    md = "\n".join(["```foo`bar", "", "## Visible"])
    assert "visible" in _visible(md), (
        "a line whose info string contains a backtick was treated as a fence "
        "opener; neither renderer does that"
    )


def test_unterminated_fence_warns_when_a_source_is_named() -> None:
    """An unterminated fence makes the gate skip to EOF. Doing it quietly is the bug.

    Without this, deleting the warning leaves the suite fully green — an
    untested guard against silence is itself silent.
    """
    import contextlib
    import io

    err = io.StringIO()
    with contextlib.redirect_stdout(err):
        out = ca.strip_code_blocks("```\ncode\n\n## After\n", source="doc.md")
    assert "after" not in ca.collect_anchors(out), (
        "fixture no longer exercises the skip-to-EOF path"
    )
    msg = err.getvalue()
    assert "::warning::" in msg and "doc.md" in msg, (
        "an unterminated fence made the gate skip the rest of the file and said "
        f"nothing — it will still print 'All internal anchors valid'. got {msg!r}"
    )

    quiet = io.StringIO()
    with contextlib.redirect_stdout(quiet):
        ca.strip_code_blocks("```\ncode\n")
    assert quiet.getvalue() == "", (
        "a call with no source emitted a CI annotation for a file that does not "
        f"exist — test fixtures would spam the run. got {quiet.getvalue()!r}"
    )


def test_backtick_inside_a_tilde_info_string_is_still_a_fence() -> None:
    """The backtick-in-info-string rule is backtick-only, deliberately.

    CommonMark allows backticks in a `~~~` info string and superfences agrees,
    so widening the rule to every fence char would wrongly stop treating this
    as code.
    """
    md = "\n".join(["~~~foo`bar", "## Hidden", "~~~", "", "## Visible"])
    got = _visible(md)
    assert "visible" in got
    assert "hidden" not in got, (
        f"the backtick-info-string rule leaked onto ~~~ fences. saw {sorted(got)}"
    )


def test_tilde_fences_are_handled() -> None:
    md = "\n".join(["~~~", "## Hidden By Tildes", "~~~", "", "## Visible"])
    got = _visible(md)
    assert "visible" in got
    assert "hidden-by-tildes" not in got, "~~~ fences are not being treated as code"


def test_backtick_does_not_close_a_tilde_fence() -> None:
    md = "\n".join(["~~~", "```", "## Still Hidden", "```", "~~~", "", "## Visible"])
    got = _visible(md)
    assert "visible" in got
    assert "still-hidden" not in got


def test_indented_fence_up_to_three_spaces() -> None:
    md = "\n".join(["   ```", "## Hidden", "   ```", "", "## Visible"])
    got = _visible(md)
    assert "visible" in got, f"heading after an indented fence went missing: {sorted(got)}"
    assert "hidden" not in got, (
        "a fence indented up to 3 spaces still opens a code block in CommonMark, "
        f"so this heading must stay hidden. saw {sorted(got)}"
    )


def test_headings_inside_a_plain_block_stay_hidden() -> None:
    """The original purpose must not regress."""
    md = "\n".join(["```markdown", "## Not A Real Heading", "```", "", "## Real"])
    got = _visible(md)
    assert "real" in got
    assert "not-a-real-heading" not in got


def test_line_numbers_are_preserved() -> None:
    """Blanking, not deleting — diagnostics cite line numbers."""
    md = "\n".join(["a", "```", "b", "```", "c"])
    assert len(ca.strip_code_blocks(md).split("\n")) == len(md.split("\n"))


def test_the_real_file_renders_all_its_headings() -> None:
    """End-to-end on the files from #95 — all three locales, hard-failing.

    This must NOT skip when the fixture is missing. It is the only test that
    kills the "closer may be shorter than the opener" mutation, so a rename
    that silently disables it deletes the sole coverage of that rule while the
    suite still prints green — the exact failure mode this file exists to stop.

    All three locales are checked because the defect was trilingual and nothing
    else would catch a re-break in one mirror alone: no link targets these
    headings, so check-anchors stays green, and check-mirror-parity compares
    structure symmetrically so a matching break in one file is invisible to it.
    """
    repo = Path(__file__).resolve().parent.parent
    base = repo / "examples/stage-4/04-codeact-vs-json-tool"
    expected = {
        "README.md": ("codeact-vs-json-tool-對照", "兩個-path-觀察重點",
                      "常見坑", "想看更聰明的答案"),
        "README.en.md": ("codeact-vs-json-tool", "what-to-watch-on-each-path",
                         "common-pitfalls", "want-smarter-answers"),
        "README.zh-Hans.md": ("codeact-vs-json-tool-对照", "两个-path-观察重点",
                              "常见坑", "想看更聪明的答案"),
    }
    for name, headings in expected.items():
        target = base / name
        assert target.exists(), (
            f"#95 fixture moved or was deleted: {target}. Update this test rather "
            f"than letting it silently stop covering the fence-length rule."
        )
        got = _visible(target.read_text(encoding="utf-8"))
        for h in headings:
            assert h in got, (
                f"#95 regression in {name}: {h!r} is swallowed by a code block again. "
                f"saw {sorted(got)}"
            )


def test_marker_count_and_flags_cannot_fork() -> None:
    """`fence_marker_count` and `code_line_flags` must stay one state machine.

    They briefly were two hand-transcribed copies — the drift shape this whole
    module exists to eliminate, reintroduced INSIDE the module meant to hold one
    copy. Both wrap `_walk` now, and the source guard below cannot see
    intra-module duplication, so this pins the relationship instead.
    """
    import md_fences

    fixtures = [
        "```\na\n```\n```\nb\n```\n",          # adjacent, no blank line
        "````\nx\n```python\ny\n```\n````\n",  # #95 nesting
        "```\nx\n",                            # unterminated
        "> ```\n> x\nplain\n",                 # quoted fence, bailed
        "~~~\nx\n```\ny\n~~~\n",               # tilde outer, backtick inside
        "```foo`bar\n\n## Visible\n",          # not a fence at all
    ]
    fixtures += [p.read_text(encoding="utf-8") for p in sorted((REPO / "scripts").glob("*.py"))[:3]]

    for text in fixtures:
        flags = md_fences.code_line_flags(text)
        markers = md_fences.fence_marker_count(text)
        assert markers == 0 or any(flags), (
            f"markers counted but no line is code — the two have forked. "
            f"markers={markers} text={text[:60]!r}"
        )
        assert markers <= sum(flags), (
            f"more fence markers ({markers}) than code lines ({sum(flags)}) — "
            f"a marker line is always a code line, so the two have forked. "
            f"text={text[:60]!r}"
        )


def test_no_script_reimplements_the_fence_rule() -> None:
    """Every gate's fence rule must come from md_fences, not a local copy.

    Six scripts each carried their own; all six were wrong in at least one way
    and one shipped #95. This is the same shape as
    `test_repo_scan_excludes.py::test_no_script_matches_excludes_on_absolute_path`,
    which pins the exclude-path bug that recurred eight times — a source-level
    guard is what stops a fixed class from being reintroduced by the next person
    who needs to know "is this line code".

    `test_check_anchors.py` is exempt: it keeps a deliberate naive copy inside
    `test_gate_matches_the_renderer_on_the_broken_shape`, as the discriminator
    proving that fixture still distinguishes the two parsers.
    """
    # POSITIVE assertion first. A blocklist of known-bad shapes can always be
    # evaded by inventing a new one — and it was: the regex below misses
    # check-mirror-parity's `open_marker` state machine and check-anchors' own
    # pre-#95 `line.startswith('```')`, i.e. 2 of the 7 real historical shapes.
    # Requiring the import cannot be evaded that way.
    gates = {
        "check-anchors.py",
        "check-hans-chars.py",
        "check-image-locale.py",
        "check-links.py",
        "check-locale-links.py",
        "check-mirror-parity.py",
        "zh-hans-localize.py",
    }
    missing = [
        n for n in sorted(gates)
        if "from md_fences import" not in (REPO / "scripts" / n).read_text(encoding="utf-8")
    ]
    assert not missing, (
        "issues #95/#97: these gates no longer import the shared fence parser, so "
        f"they have their own answer to 'which lines are code' again: {missing}"
    )

    # Blocklist second, as a backstop for scripts not in the set above.
    toggler = re.compile(
        r"in_fence\s*=\s*not\s+in_fence"
        r"|in_code\s*=\s*not\s+in_code"
        r"|in_fenced_code\s*=\s*not\s+in_fenced_code"
        r"|open_marker\s*=\s*marker"
        r"|re\.compile\(\s*r?[\"']```\.\*\?```"
    )
    offenders = []
    for p in sorted((REPO / "scripts").glob("*.py")):
        if p.name == Path(__file__).name:
            # Exempt: this file keeps a deliberate naive copy inside
            # test_gate_matches_the_renderer_on_the_broken_shape, as the
            # discriminator proving that fixture still tells the parsers apart.
            continue
        if toggler.search(p.read_text(encoding="utf-8")):
            offenders.append(p.name)

    assert not offenders, (
        "issues #95/#97: a fence closer may not carry an info string and must be "
        "at least as long as its opener; a DOTALL ```...``` regex mis-pairs nested "
        "fences. These scripts reimplement the rule instead of importing "
        f"md_fences.strip_code_blocks / code_line_flags: {offenders}"
    )


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
        except AssertionError as e:
            failed += 1
            print(f"FAIL {name}\n  {e}")
        except BaseException as e:
            failed += 1
            print(f"ERROR {name}: {type(e).__name__}: {e}")
    if failed:
        print(f"\n{failed}/{len(tests)} failed.")
        return 1
    print(f"{len(tests)}/{len(tests)} passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Regression tests for scripts/check-links.py's failure classification.

Pins issue #94. The checker reported 14 failures of which only 5 were real —
a 64% wrong rate. A gate that wrong stops being read, which is worse than not
having one, because the real rot hides inside the noise.

Three causes, all pinned here:

1. **It identified itself.** The old UA ("awesome-agentic-ai-zh-link-check/1.0")
   was refused by several hosts and the report called those links BROKEN.

2. **HEAD is widely mis-implemented.** Measured on this repo's own links,
   `openai.com/chatgpt/desktop` answers HEAD 404 / GET 200, and
   `learnshell.org` answers HEAD 415 / GET 200. The old code retried with GET
   only on 405/403, so both were reported dead.

3. **A refusal is not a 404.** 401/403/429/451 mean the host is answering and
   declining to serve a script; nothing about the link is actionable. Worse,
   they are FLAKY — while triaging #94, three URLs returned 200 to a browser one
   day and 403 the next. Mixing them into the failure list is what teaches
   people to skip the output.

Plus a host-level-block probe: some hosts refuse with a code that normally means
something else. Every Meta domain (ai.meta.com, developer.meta.com, llama.com)
answers 400 to a non-browser client, INCLUDING its own root. Asking the root
turns "is this page gone or is this host blocking me" from a guess into a
measurement.

Issue #102 then found that everything above tested check_url and NOTHING tested
main(), where the verdict actually lives. Mutation testing on the untested part:
`sys.exit(1 if failures else 0)` -> `sys.exit(0)` survived, i.e. the gate could
have been made permanently green and this suite would have stayed 10/10. The
`test_main_*` and `test_classify_*` cases below are what kills that mutant.

Run:  python scripts/test_check_links.py     (plain asserts, no pytest needed)
 or:  pytest scripts/test_check_links.py
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

_SPEC = importlib.util.spec_from_file_location(
    "check_links", Path(__file__).with_name("check-links.py")
)
cl = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(cl)


class _Resp:
    def __init__(self, status, url=""):
        self.status_code = status
        self.url = url

    def close(self):
        pass


class _Fake:
    """Stand-in for requests, driven by {(method, url): status}."""

    def __init__(self, head=None, get=None, final=None):
        self.head_map = head or {}
        self.get_map = get or {}
        self.final = final or {}
        self.calls = []

    def head(self, url, **kw):
        self.calls.append(("HEAD", url))
        if url not in self.head_map:
            raise AssertionError(f"unexpected HEAD {url}")
        return _Resp(self.head_map[url], self.final.get(url, url))

    def get(self, url, **kw):
        self.calls.append(("GET", url))
        if url not in self.get_map:
            raise AssertionError(f"unexpected GET {url}")
        return _Resp(self.get_map[url], self.final.get(url, url))


def _with(fake):
    """Swap cl.requests for a fake, keeping the real exception class."""
    fake.exceptions = cl.requests.exceptions
    old = cl.requests
    cl.requests = fake
    cl._root_cache.clear()  # memoized per host; a stale entry would fake a pass
    return old


def _restore(old):
    cl.requests = old


def _probe(url, fake, **kw):
    old = _with(fake)
    try:
        return cl.check_url(url, **kw)
    finally:
        _restore(old)


# --- check_url: what a single URL's probe reports -------------------------

def test_head_404_but_get_200_is_not_a_failure() -> None:
    """The exact openai.com/chatgpt/desktop shape. HEAD lies; GET is the truth."""
    u = "https://example.com/page"
    f = _Fake(head={u: 404}, get={u: 200})
    p = _probe(u, f)
    assert p.status == 200, f"HEAD's 404 was trusted over GET's 200 (got {p.status})"
    assert ("GET", u) in f.calls, "no GET retry was attempted after a 4xx HEAD"


def test_head_415_but_get_200_is_not_a_failure() -> None:
    """learnshell.org's shape. 415 is outside the old 405/403 retry set."""
    u = "https://example.com/shell"
    p = _probe(u, _Fake(head={u: 415}, get={u: 200}))
    assert p.status == 200, f"415 from HEAD was not retried with GET (got {p.status})"


def test_refusal_statuses_are_classified_unverifiable_not_dead() -> None:
    # Assert the MEMBERS, not just "iterate whatever is in the set". Iterating
    # the set under test means emptying it passes vacuously — that mutation
    # survived until this line was added.
    assert cl.UNVERIFIABLE_STATUSES == {401, 403, 429, 451}, (
        "Exact equality, not a subset. A subset check permits WIDENING, and "
        "adding 404 to this set makes the gate structurally incapable of ever "
        "reporting a dead link again — which passed every test until this line. "
        f"got {cl.UNVERIFIABLE_STATUSES!r}"
    )
    for code in (401, 403, 429, 451):
        u = f"https://example.com/{code}"
        p = _probe(u, _Fake(head={u: code}, get={u: code}))
        assert p.status == code, (
            f"{code} was not returned unchanged (got {p.status}) — a refusal must "
            "reach the caller as itself so it can be bucketed as unverifiable"
        )
        assert cl.classify(p) == cl.UNVERIFIABLE, (
            f"{code} is a refusal, not a dead link (got {cl.classify(p)})"
        )


def test_host_level_block_is_not_reported_as_dead() -> None:
    """The Meta shape: a 400 whose own host root also 400s."""
    u = "https://developer.example.com/ai/models/x/"
    root = "https://developer.example.com/"
    p = _probe(u, _Fake(head={u: 400}, get={u: 400, root: 400}))
    assert p.status == 400
    # Assert the FLAG, not the prose. main() used to route on
    # msg.startswith("host-level block"), so rewording that sentence would have
    # silently re-filed every host block as a dead link — and the only test that
    # would have noticed asserted the same string, i.e. it pinned the wording
    # rather than the behaviour.
    assert p.host_blocked, (
        "the host refuses everything including its own root, so this says nothing "
        f"about the page — got {p!r}"
    )
    assert cl.classify(p) == cl.UNVERIFIABLE


def test_page_level_404_is_still_a_failure() -> None:
    """The guard must not swallow real rot: root is fine, page is gone."""
    u = "https://example.com/gone"
    root = "https://example.com/"
    p = _probe(u, _Fake(head={u: 404}, get={u: 404, root: 200}))
    assert p.status == 404
    assert not p.host_blocked, (
        "a genuinely dead page was excused as a host block — the root answered 200, "
        "so the host is NOT refusing us"
    )
    assert cl.classify(p) == cl.FAILED


def test_host_wide_404_does_not_excuse_a_page_level_404() -> None:
    """The C1 case. A host whose ROOT 404s must not make its dead pages invisible.

    `langchain-ai.github.io` is a GitHub Pages org site with no root page, so its
    root answers 404. The first version of the host-block probe therefore
    classified both dead LangGraph URLs from issue #94 as "host-level block — do
    not fix": the gate argued against the very commit that fixes them, and 37
    links across two *.github.io hosts became permanently undetectable.

    404/410 are the only codes that speak about the resource itself, so they must
    never reach the probe.
    """
    assert cl.NOT_FOUND_STATUSES == {404, 410}, (
        "Exact equality. Shrinking this to {404} sends 410 Gone through the "
        "host-block probe, so a host with no root page hides its 410s — and that "
        "mutation passed every test until 410 was covered below. "
        f"got {cl.NOT_FOUND_STATUSES!r}"
    )
    # Both codes, spelled out. Iterating cl.NOT_FOUND_STATUSES here would make
    # emptying the set pass vacuously, which is the exact trap #94 fell into.
    for code in (404, 410):
        u = f"https://org.github.io/proj/{code}/"
        root = "https://org.github.io/"
        f = _Fake(head={u: code}, get={u: code, root: code})
        p = _probe(u, f)
        assert p.status == code
        assert not p.host_blocked, (
            f"a host-wide {code} excused a page-level {code} — this is a GitHub "
            f"Pages org site with no root page, not a host refusing us. got {p!r}"
        )
        assert cl.classify(p) == cl.FAILED
        assert ("GET", root) not in f.calls, (
            f"the root was probed at all for a {code}; 404/410 must short-circuit "
            "before the probe, otherwise every no-root-page host blinds the checker"
        )


def test_root_probe_follows_redirects_to_the_final_host() -> None:
    """llama.com's shape: a root that redirects to another host which blocks."""
    u = "https://www.llama.com/"
    final = "https://developer.meta.example/ai/"
    root = "https://developer.meta.example/"
    p = _probe(u, _Fake(head={u: 400}, get={u: 400, root: 400}, final={u: final}))
    assert p.host_blocked, (
        "the requested URL is itself a root, so its own root proves nothing; the "
        f"root it REDIRECTS to is the one to ask — got {p!r}"
    )


def test_login_gated_urls_are_skipped_entirely() -> None:
    u = next(iter(cl.LOGIN_GATED))
    f = _Fake()  # any request at all would raise
    p = _probe(u, f)
    assert p.status is None and cl.classify(p) == cl.SKIPPED, (
        "a URL that requires a signed-in session must not be probed every run"
    )
    assert not f.calls, "login-gated URL was still requested"


def test_browser_user_agent_is_sent() -> None:
    """The identifying UA was itself the cause of 3 of 14 reported failures."""
    ua = cl.BROWSER_HEADERS["User-Agent"]
    assert "Mozilla/5.0" in ua, f"not a browser UA: {ua!r}"
    assert "link-check" not in ua, (
        "the checker identifies itself again; hosts refuse that UA and the report "
        "then calls working links broken"
    )


def test_code_block_urls_are_not_checked() -> None:
    """URLs inside fenced samples are not links (issue #97 wired this up)."""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "t.md"
        p.write_text(
            "[real](https://example.com/real)\n\n"
            "```\n[sample](https://example.com/in-code)\n```\n",
            encoding="utf-8",
        )
        urls = [u for _, u in cl.extract_urls(p)]
    assert "https://example.com/real" in urls
    assert "https://example.com/in-code" not in urls, (
        "a URL inside a code sample was queued for a network check"
    )


def test_html_hrefs_and_autolinks_are_checked() -> None:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "t.md"
        p.write_text(
            '<a href="https://example.com/double">double</a>\n'
            "<a class='x' href='https://example.com/single'>single</a>\n"
            "<https://example.com/auto>\n",
            encoding="utf-8",
        )
        urls = [u for _, u in cl.extract_urls(p)]
    assert urls == [
        "https://example.com/double",
        "https://example.com/single",
        "https://example.com/auto",
    ]


# --- classify / exit_code: the verdict, as a pure function ----------------
# These used to be inline in main() and therefore untested (#102).

def test_classify_covers_every_shape() -> None:
    cases = [
        (cl.Probe("u", 200), cl.OK),
        (cl.Probe("u", 301), cl.OK),          # allow_redirects means we see the end
        (cl.Probe("u", 403), cl.UNVERIFIABLE),
        (cl.Probe("u", 404), cl.FAILED),
        (cl.Probe("u", 500), cl.FAILED),
        (cl.Probe("https://example.com/deep", 200,
                  final_url="https://example.com/"), cl.FAILED),
        (cl.Probe("u", 400, "blocked", host_blocked=True), cl.UNVERIFIABLE),
        (cl.Probe("u", None, "skipped (--fast)", skipped=True), cl.SKIPPED),
        (cl.Probe("u", None, "skipped (login-gated)", skipped=True), cl.SKIPPED),
        # A connection error says the scanner could not verify the page. It is
        # not proof that the page is missing.
        (cl.Probe("u", None, "ConnectionError: nope"), cl.UNVERIFIABLE),
        # The skip flag still matters for reporting: skip and unverified are
        # separate buckets even though neither fails the run.
        (cl.Probe("u", None, "skipped-looking text, but no flag"), cl.UNVERIFIABLE),
    ]
    for probe, want in cases:
        got = cl.classify(probe)
        assert got == want, f"classify({probe!r}) = {got!r}, want {want!r}"


def test_bad_redirect_label_names_the_destination() -> None:
    probe = cl.Probe(
        "https://docs.example.com/deep/page",
        200,
        final_url="https://docs.example.com/",
    )
    label = cl.probe_label(probe)
    assert "collapsed to site root" in label
    assert "https://docs.example.com/" in label


def test_skips_set_the_flag_not_just_the_message() -> None:
    """Both skip paths through check_url, end to end. Without this, rewording
    "skipped (--fast)" would silently reclassify every fast-mode skip."""
    gated = next(iter(cl.LOGIN_GATED))
    p = _probe(gated, _Fake())
    assert p.skipped and cl.classify(p) == cl.SKIPPED, f"login-gated: {p!r}"

    p = _probe("https://example.com/not-github", _Fake(), fast_mode=True)
    assert p.skipped and cl.classify(p) == cl.SKIPPED, f"--fast: {p!r}"


def test_exit_code_fails_only_on_actionable_findings() -> None:
    assert cl.exit_code([]) == 0
    assert cl.exit_code([cl.OK, cl.OK]) == 0
    assert cl.exit_code([cl.UNVERIFIABLE, cl.SKIPPED, cl.OK]) == 0, (
        "a refusal or a skip must never fail the run — that is the whole point "
        "of the unverifiable bucket"
    )
    assert cl.exit_code([cl.OK, cl.FAILED]) == 1, "a dead link must fail the run"
    assert cl.exit_code([cl.FAILED]) == 1


# --- main(): the part that was never tested at all (#102) -----------------

def _section(out: str, header: str) -> str:
    """One `=== ... ===` block, up to the next one. Slicing to end-of-output
    instead would make every later section's content count as this one's."""
    if header not in out:
        return ""
    rest = out.split(header, 1)[1]
    return rest.split("\n===", 1)[0]


def _run_main(fake, md_text, argv=(), baseline=None):
    """Run main() against a throwaway repo.

    Returns (exit_code, stdout, baseline_state) where baseline_state is the
    parsed baseline file or None if it was never written. It is read INSIDE the
    tempdir context — returning the Path would hand back one that no longer
    exists, which reads as "not written" no matter what happened.
    """
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "t.md").write_text(md_text, encoding="utf-8")
        base_path = root / "baseline.json"
        if baseline is not None:
            base_path.write_text(json.dumps({"unverifiable": baseline}),
                                 encoding="utf-8")
        old_root, old_base, old_argv = (
            cl.REPO_ROOT, cl.UNVERIFIABLE_BASELINE, sys.argv)
        old_req = _with(fake)
        cl.REPO_ROOT, cl.UNVERIFIABLE_BASELINE = root, base_path
        sys.argv = ["check-links.py", "--quiet", *argv]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(
                    io.StringIO()):
                code = cl.main()
        finally:
            cl.REPO_ROOT, cl.UNVERIFIABLE_BASELINE, sys.argv = (
                old_root, old_base, old_argv)
            _restore(old_req)
        written = (json.loads(base_path.read_text(encoding="utf-8"))
                   if base_path.exists() else None)
        return code, buf.getvalue(), written


def test_main_exits_nonzero_when_a_link_is_dead() -> None:
    """The mutation that survived #94's whole suite: `sys.exit(0)` unconditionally.

    Nothing could call main() without killing the interpreter, so nothing did,
    so the gate's actual verdict was never once asserted.
    """
    u = "https://example.com/gone"
    root = "https://example.com/"
    f = _Fake(head={u: 404}, get={u: 404, root: 200})
    code, out, _ = _run_main(f, f"[x]({u})\n")
    assert code == 1, f"a dead link did not fail the run (exit {code})"
    assert u in out, "the dead link was not named in the report"


def test_main_exits_zero_when_every_link_is_alive() -> None:
    """The other half. Without this, `sys.exit(1)` unconditionally also passes."""
    u = "https://example.com/ok"
    code, _, _ = _run_main(_Fake(head={u: 200}), f"[x]({u})\n")
    assert code == 0, f"a healthy tree failed the run (exit {code})"


def test_main_does_not_fail_the_run_on_a_refusal() -> None:
    u = "https://example.com/403"
    code, out, _ = _run_main(_Fake(head={u: 403}, get={u: 403}), f"[x]({u})\n")
    assert code == 0, (
        f"a 403 failed the run (exit {code}) — refusals are not actionable, and "
        "failing on them is what made 9 of 14 reported failures wrong in #94"
    )
    assert u in out, (
        "the refusal vanished entirely; not failing the run is not the same as "
        "hiding it, a human still has to eyeball these"
    )


def test_main_reports_a_new_refusal_but_not_a_baselined_one() -> None:
    """Why a baseline exists: 'never fails the run' must not mean 'never noticed'."""
    known = "https://example.com/known-403"
    fresh = "https://example.com/fresh-403"
    f = _Fake(head={known: 403, fresh: 403}, get={known: 403, fresh: 403})
    code, out, _ = _run_main(
        f, f"[a]({known})\n\n[b]({fresh})\n", baseline=[known])
    assert code == 0, "a refusal must still not fail the run"
    new_section = _section(out, "=== NEW unverifiable")
    assert fresh in new_section, (
        "a host that JUST started refusing looks identical to one that has "
        "refused for months; the baseline exists to tell them apart"
    )
    assert known not in new_section, (
        f"a baselined refusal was re-reported as NEW — got:\n{new_section}"
    )


def test_update_baseline_writes_the_file_and_changes_nothing_else() -> None:
    u = "https://example.com/403"
    f = _Fake(head={u: 403}, get={u: 403})
    code, _, written = _run_main(f, f"[x]({u})\n", argv=("--update-baseline",))
    assert code == 0
    assert written is not None and written["unverifiable"] == [u], (
        f"--update-baseline did not record the refusal it just saw: {written!r}"
    )


def test_update_baseline_still_reports_and_fails_on_a_dead_link() -> None:
    """Recording a refusal must not change what happens to an unrelated dead link.

    The first version of this branch did `save_baseline(...); return 0` before the
    failure report was ever printed, so `--update-baseline` swallowed a genuine
    404 AND forced the run green — the same "gate goes green without anyone
    noticing" defect as #102 itself, reintroduced in the one branch that had no
    test. `test_update_baseline_writes_the_file...` could not catch it because its
    scenario has no failures in it at all.
    """
    dead = "https://example.com/gone"
    root = "https://example.com/"
    refused = "https://example.com/403"
    f = _Fake(head={dead: 404, refused: 403},
              get={dead: 404, root: 200, refused: 403})
    code, out, written = _run_main(
        f, f"[a]({dead})\n\n[b]({refused})\n", argv=("--update-baseline",))
    assert code == 1, (
        f"--update-baseline forced the run green with a dead link present "
        f"(exit {code})"
    )
    assert dead in out, "the dead link was never printed under --update-baseline"
    assert written is not None and written["unverifiable"] == [refused], (
        f"the baseline should still record the refusal, and only it: {written!r}"
    )


def test_baseline_is_not_written_on_an_ordinary_run() -> None:
    """A baseline records what a human looked at. A run that writes its own
    baseline records nothing and silences everything it just found."""
    u = "https://example.com/403"
    f = _Fake(head={u: 403}, get={u: 403})
    _, _, written = _run_main(f, f"[x]({u})\n")
    assert written is None, (
        "an ordinary run wrote the baseline; every new refusal would then be "
        "self-approved on first sight and never reported again"
    )


def test_a_bad_baseline_file_fails_open_and_never_crashes() -> None:
    """This file is meant to be hand-edited, so every bad edit has to degrade to
    noisy — not to silence, and not to killing the run.

    Syntax was handled; SHAPE was not. Valid JSON that is not a dict (a stray
    list, a bare null) reached `data.get` and raised AttributeError, which took
    the whole gate down rather than doing either of the documented things.
    """
    with tempfile.TemporaryDirectory() as d:
        cases = {
            "missing.json": None,               # never written
            "syntax.json": "{not json",
            "list.json": "[\"a\", \"b\"]",      # valid JSON, wrong shape
            "null.json": "null",
            "wrongkey.json": '{"urls": ["a"]}',
            "notalist.json": '{"unverifiable": "a"}',
            "empty.json": "",
        }
        for name, content in cases.items():
            p = Path(d) / name
            if content is not None:
                p.write_text(content, encoding="utf-8")
            got = cl.load_unverifiable_baseline(p)   # must not raise
            assert got == set(), (
                f"{name}: a bad baseline must fail OPEN (everything is NEW and "
                f"noisy), never closed (everything baselined and silent) and "
                f"never fatal — got {got!r}"
            )
        # Non-string members are dropped rather than poisoning the set.
        mixed = Path(d) / "mixed.json"
        mixed.write_text('{"unverifiable": ["https://a", 42, null]}',
                         encoding="utf-8")
        assert cl.load_unverifiable_baseline(mixed) == {"https://a"}

        # Corruption by ENCODING, not by syntax or shape. UnicodeDecodeError is a
        # sibling ValueError subclass, so `except json.JSONDecodeError` did not
        # catch it and the whole run died — the first fix for this closed the
        # shape hole and left this one open.
        binary = Path(d) / "binary.json"
        binary.write_bytes(b'{"unverifiable": ["https://\xff\xfe"]}')
        assert cl.load_unverifiable_baseline(binary) == set(), (
            "invalid UTF-8 in the baseline killed the run instead of failing open"
        )


def test_update_baseline_announces_what_it_drops() -> None:
    """save_unverifiable_baseline OVERWRITES, so a URL that verifies again is
    silently removed. The run doing the removing is the only one that can say so."""
    gone = "https://example.com/was-refusing-now-fine"
    still = "https://example.com/403"
    f = _Fake(head={gone: 200, still: 403}, get={still: 403})
    code, out, written = _run_main(
        f, f"[a]({gone})\n\n[b]({still})\n",
        argv=("--update-baseline",), baseline=[gone, still])
    assert code == 0
    assert written is not None and written["unverifiable"] == [still], (
        f"the recovered URL should be dropped from the baseline: {written!r}"
    )
    dropped = _section(out, "=== Dropped from the baseline")
    assert gone in dropped, (
        "a URL was removed from the baseline with no mention on screen — the "
        f"only run that could report it is this one. got:\n{out}"
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

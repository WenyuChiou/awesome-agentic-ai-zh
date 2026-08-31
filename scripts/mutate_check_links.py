#!/usr/bin/env python3
"""Mutation-test scripts/check-links.py against scripts/test_check_links.py.

Why this file is in the repo rather than a scratch directory: a test suite being
green tells you nothing about whether it can go red. `check-links.py` shipped
twice with tests that could not fail —

  * #94: the refusal-set test ITERATED the set under test, so emptying
    `UNVERIFIABLE_STATUSES` made the loop body never run and the test pass.
  * #102: nothing could call `main()` without killing the interpreter, so
    nothing did, so `sys.exit(1 if failures else 0)` -> `sys.exit(0)` left the
    suite 10/10 green. The gate could have been made permanently green and no
    test would have noticed.

Both were found this way, not by reading. Each entry below is a defect that has
either actually shipped here or would silently disable the gate. Run it after
any change to check-links.py:

    python scripts/mutate_check_links.py

Every mutant must be KILLED (the suite must go red). A SURVIVED line means the
suite cannot detect that defect — write the missing test, do not delete the
mutant. Exits 1 if anything survived. The source file is always restored.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "scripts" / "check-links.py"
SUITE = REPO / "scripts" / "test_check_links.py"

# (name, find, replace) — `find` must appear verbatim in check-links.py.
MUTANTS: list[tuple[str, str, str]] = [
    ("exit code always 0 (the #102 mutant that survived)",
     "return exit_code(kind for kind, entries in buckets.items() for _ in entries)",
     "return 0"),
    ("exit code always 1",
     "return exit_code(kind for kind, entries in buckets.items() for _ in entries)",
     "return 1"),
    ("exit_code() never fails",
     "return 1 if any(k == FAILED for k in kinds) else 0",
     "return 0"),
    ("--update-baseline returns early again (skips the failure report)",
     "        new_unverifiable = []",
     "        return 0"),
    ("404 added to the refusal set (gate can never report rot again)",
     "UNVERIFIABLE_STATUSES = {401, 403, 429, 451}",
     "UNVERIFIABLE_STATUSES = {401, 403, 429, 451, 404}"),
    ("451 dropped from the refusal set",
     "UNVERIFIABLE_STATUSES = {401, 403, 429, 451}",
     "UNVERIFIABLE_STATUSES = {401, 403, 429}"),
    ("410 dropped from NOT_FOUND (root probe then hides Gone pages)",
     "NOT_FOUND_STATUSES = {404, 410}",
     "NOT_FOUND_STATUSES = {404}"),
    ("host_blocked ignored by classify",
     "if probe.status in UNVERIFIABLE_STATUSES or probe.host_blocked:",
     "if probe.status in UNVERIFIABLE_STATUSES:"),
    ("host_blocked never set",
     "host_blocked=True,",
     "host_blocked=False,"),
    ("skip/failure split back to sniffing the message",
     "    if probe.skipped:\n        return SKIPPED",
     '    if probe.detail.startswith("skipped"):\n        return SKIPPED'),
    ("connection errors treated as skips",
     "        return UNVERIFIABLE\n    if probe.status in UNVERIFIABLE_STATUSES",
     "        return SKIPPED\n    if probe.status in UNVERIFIABLE_STATUSES"),
    ("4xx/5xx treated as OK",
     "    if probe.status >= 400:\n        return FAILED",
     "    if probe.status >= 400:\n        return OK"),
    ("baseline written on every run (self-approves every new refusal)",
     "    if args.update_baseline:\n        save_unverifiable_baseline(seen_unverifiable)",
     "    save_unverifiable_baseline(seen_unverifiable)\n    if args.update_baseline:"),
    ("baseline ignored when computing NEW",
     "new_unverifiable = sorted(seen_unverifiable - baseline)",
     "new_unverifiable = sorted(seen_unverifiable)"),
    ("baseline inverted (only baselined URLs reported NEW)",
     "new_unverifiable = sorted(seen_unverifiable - baseline)",
     "new_unverifiable = sorted(seen_unverifiable & baseline)"),
    ("baseline shape check dropped (bad hand-edit kills the run)",
     "    if not isinstance(data, dict):\n        return set()",
     "    pass"),
    ("baseline encoding errors uncaught again (invalid UTF-8 kills the run)",
     "    except (OSError, ValueError):",
     "    except (OSError, json.JSONDecodeError):"),
    ("--update-baseline hides what it drops from the baseline",
     "        new_unverifiable = []",
     "        new_unverifiable, recovered = [], []"),
    ("GET retry only on 405/403 (the pre-#94 behaviour)",
     "if 400 <= r.status_code < 500:",
     "if r.status_code in (405, 403):"),
    # Must stay valid Python. A mutant that fails to PARSE is killed by the
    # import blowing up, not by any test — which looks identical in the output
    # and proves nothing about the suite.
    ("identifying user-agent restored",
     '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "',
     '"awesome-agentic-ai-zh-link-check/1.0 "'),
    ("login-gated URLs probed anyway",
     '    if url in LOGIN_GATED:\n        return Probe(url, None, "skipped (login-gated)", skipped=True)',
     "    pass"),
    ("code fences no longer stripped",
     "    text = strip_code_blocks(text, source=source)",
     "    text = text"),
]


# Bytecode caching has to be off, and this is not a micro-optimisation — it is
# the difference between real evidence and plausible-looking evidence.
#
# The suite loads check-links.py through importlib, which honours __pycache__.
# A cached .pyc is validated on the source's (mtime, size) — and mutants like
# `return 0` -> `return 1` produce a file of IDENTICAL size, written within the
# same second as the previous one. So the child happily reused the PREVIOUS
# mutant's compiled code, and the "<- killed by" trail named the wrong tests.
# Measured: 3 of 4 runs had exactly one such mislabelled mutant.
#
# What made it genuinely dangerous is that the aggregate verdict stayed 22/22
# every time: a correct number resting on wrong evidence, in the one script whose
# whole job is to BE the evidence. Exactly the failure mode this file exists to
# catch, one level up.
#
# The child also fingerprints the source it read and the parent checks it, which
# covers the on-disk half. The sha alone was NOT enough — the bytes were always
# right; it was the compilation that was stale.
_NO_BYTECODE = {"PYTHONDONTWRITEBYTECODE": "1"}
_RUNNER = (
    "import hashlib,pathlib,runpy,sys;"
    "print('SRCSHA',hashlib.sha256(pathlib.Path(sys.argv[2]).read_bytes()).hexdigest(),flush=True);"
    "suite=sys.argv[1];"
    "sys.argv=[suite];"
    "runpy.run_path(suite,run_name='__main__')"
)


def run_suite(expect_sha: str) -> tuple[int, list[str]]:
    # PYTHONPYCACHEPREFIX is dropped, not just overridden: if the surrounding
    # environment sets it, caches land somewhere else entirely and the
    # stale-.pyc cleanup below would be looking in the wrong directory.
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPYCACHEPREFIX"}
    r = subprocess.run(
        # -B as well as the env var: belt and braces, since a stale .pyc is
        # invisible in the output and silently rewrites the evidence trail.
        [sys.executable, "-B", "-c", _RUNNER, str(SUITE), str(SRC)],
        cwd=REPO, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=300,
        env={**env, "PYTHONIOENCODING": "utf-8", **_NO_BYTECODE},
    )
    out = r.stdout or ""
    seen = next((ln.split()[1] for ln in out.splitlines()
                 if ln.startswith("SRCSHA ")), None)
    if seen != expect_sha:
        raise RuntimeError(
            f"the suite ran against the wrong source: expected sha {expect_sha[:12]}, "
            f"the child read {(seen or 'nothing')[:12]}. Results would be attributed "
            "to the wrong mutant."
        )
    named = [ln.split(None, 1)[1] for ln in out.splitlines()
             if ln.startswith(("FAIL ", "ERROR "))]
    return r.returncode, named


def _restore_or_shout(original: str) -> bool:
    """Put the source back and VERIFY it, rather than assuming the write took.
    Leaving a mutant on disk would hand a later CI step, or a later commit, a
    deliberately broken checker."""
    SRC.write_text(original, encoding="utf-8")
    if SRC.read_text(encoding="utf-8") == original:
        return True
    print("FATAL: check-links.py was NOT restored. Run `git checkout -- "
          "scripts/check-links.py` before doing anything else.")
    return False


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    # Any .pyc left by an earlier run is a stale cache waiting to happen:
    # -B stops the child WRITING one, not reading one that already exists.
    for stale in (REPO / "scripts" / "__pycache__").glob("check-links.*.pyc"):
        stale.unlink()

    original = SRC.read_text(encoding="utf-8")
    rc, _ = run_suite(hashlib.sha256(SRC.read_bytes()).hexdigest())
    if rc != 0:
        print("The suite is already red on unmutated source. Fix that first.")
        return 1

    survived: list[str] = []
    killed = 0
    try:
        for name, find, replace in MUTANTS:
            if find not in original:
                # A stale pattern is NOT a pass: it means this defect is no
                # longer being probed at all, and silently counting it as killed
                # is how a mutation suite rots into decoration.
                print(f"STALE     {name}  (pattern no longer in check-links.py)")
                survived.append(f"{name}  [STALE PATTERN — not applied]")
                continue
            mutated = original.replace(find, replace, 1)
            try:
                # A mutant that does not PARSE is killed by the import blowing
                # up, not by any test — indistinguishable in the output and
                # evidence of nothing. It is a broken mutant, not a passing gate.
                compile(mutated, str(SRC), "exec")
            except SyntaxError as e:
                print(f"INVALID   {name}  (mutant does not parse: {e.msg})")
                survived.append(f"{name}  [INVALID MUTANT — does not parse]")
                continue
            SRC.write_text(mutated, encoding="utf-8")
            # Read back BEFORE spawning the child. Measured on Windows/NTFS: in
            # roughly 2 runs out of 6 the freshly-spawned interpreter observed
            # the PREVIOUS mutant's bytes, so the "<- killed by" trail named the
            # wrong tests. The aggregate verdict happened to stay correct every
            # time, which is exactly what makes it dangerous — the number stays
            # right while the evidence for it is wrong, and the evidence is the
            # entire point of committing this script.
            if SRC.read_text(encoding="utf-8") != mutated:
                raise RuntimeError(
                    f"mutation for {name!r} was not visible on disk before the "
                    "suite was spawned; results would be attributed to the wrong "
                    "mutant"
                )
            # Hash the FILE, not the in-memory string: write_text translates
            # newlines on Windows, so the string's bytes and the file's bytes
            # legitimately differ. Content correctness is checked above by
            # comparing decoded text; this hash checks that the child sees the
            # same BYTES the parent just observed.
            rc, failing = run_suite(hashlib.sha256(SRC.read_bytes()).hexdigest())
            if rc == 0:
                print(f"SURVIVED  {name}")
                survived.append(name)
            else:
                killed += 1
                print(f"killed    {name}")
                for t in failing:
                    print(f"            <- {t}")
    except BaseException:
        # The restore check has to run HERE too, not only after the try. This
        # script edits a TRACKED file in place, and the exception path is exactly
        # where something has already gone wrong once — putting the safety net
        # only on the happy path means it is missing whenever it matters.
        _restore_or_shout(original)
        raise
    else:
        if not _restore_or_shout(original):
            return 2

    print(f"\n{killed}/{len(MUTANTS)} killed, {len(survived)} survived")
    for s in survived:
        print(f"  SURVIVED: {s}")
    return 1 if survived else 0


if __name__ == "__main__":
    sys.exit(main())

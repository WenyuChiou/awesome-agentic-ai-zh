from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).with_name("check-workflow-security.py")
SPEC = importlib.util.spec_from_file_location("workflow_security", SCRIPT)
ws = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ws)


def test_accepts_full_sha_with_version_comment() -> None:
    text = """name: x
on: [pull_request]
permissions:
  contents: read
jobs:
  x:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
"""
    assert ws.problems_for_text(Path("x.yml"), text) == []


def test_rejects_mutable_action_and_pull_request_target() -> None:
    text = """name: x
on: [pull_request_target]
permissions:
  contents: read
jobs:
  x:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
"""
    problems = ws.problems_for_text(Path("x.yml"), text)
    assert any("pull_request_target" in item for item in problems)
    assert any("full 40-character commit SHA" in item for item in problems)


def test_requires_explicit_top_level_permissions() -> None:
    text = """name: x
on: [push]
jobs:
  x:
    permissions:
      contents: read
    runs-on: ubuntu-latest
    steps: []
"""
    assert any("top-level permissions" in item for item in ws.problems_for_text(Path("x.yml"), text))


def test_rejects_top_level_and_job_level_contents_write() -> None:
    top = """name: x
on: [push]
permissions:
  contents: write
jobs: {}
"""
    assert any("top-level write" in item for item in ws.problems_for_text(Path("x.yml"), top))

    job = """name: x
on: [push]
permissions: {}
jobs:
  x:
    permissions:
      contents: write
    runs-on: ubuntu-latest
    steps: []
"""
    assert any("unapproved write" in item for item in ws.problems_for_text(Path("x.yml"), job))


def test_pr_writer_must_not_checkout_or_execute_repo_scripts() -> None:
    text = """name: Required
on: [pull_request]
permissions:
  contents: read
jobs:
  comment:
    permissions:
      pull-requests: write
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
      - run: python scripts/pr-readiness.py
"""
    problems = ws.problems_for_text(Path(".github/workflows/pr-gate.yml"), text)
    assert any("must not checkout" in item for item in problems)
    assert any("must not execute" in item for item in problems)


def test_allowlisted_pr_writer_can_only_handle_prebuilt_evidence() -> None:
    text = """name: Required
on: [pull_request]
permissions:
  contents: read
jobs:
  comment:
    permissions:
      pull-requests: write
    runs-on: ubuntu-latest
    steps:
      - run: gh api -X POST endpoint -F body=@evidence/pr-readiness.md
"""
    assert ws.problems_for_text(Path(".github/workflows/pr-gate.yml"), text) == []

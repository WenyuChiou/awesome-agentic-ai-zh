from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path


SCRIPT = Path(__file__).with_name("check-changed-links.py")
SPEC = importlib.util.spec_from_file_location("check_changed_links", SCRIPT)
cl = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(cl)


def test_extracts_only_genuinely_added_markdown_links() -> None:
    base = "[moved](https://example.com/a)\n"
    head = base + "[new](https://example.com/b)\nplain https://example.com/not-a-markdown-link\n"
    assert cl.extract_new_urls_from_texts(base, head) == {"https://example.com/b"}


def test_extracts_html_hrefs_and_autolinks_without_double_counting_moves() -> None:
    base = '<a href="https://example.com/moved">old</a>\n'
    head = """<a href='https://example.com/moved'>new label</a>
<a class="resource" href="https://example.com/html">HTML</a>
<https://example.com/auto>
"""
    assert cl.extract_new_urls_from_texts(base, head) == {
        "https://example.com/auto",
        "https://example.com/html",
    }


def test_complete_document_context_excludes_urls_inside_multiline_fences() -> None:
    head = """Reader link: [docs](https://example.com/docs)

```text
[sample](https://example.com/not-a-link)
```
"""
    assert cl.extract_new_urls_from_texts("", head) == {"https://example.com/docs"}


def test_changed_markdown_pairs_preserve_add_delete_and_rename(monkeypatch) -> None:
    raw = "M\0page.md\0A\0new.md\0D\0old.md\0R100\0before.md\0after.md\0"
    monkeypatch.setattr(
        cl,
        "_run_git",
        lambda arguments: "fork-point\n" if arguments[0] == "merge-base" else raw,
    )
    comparison_base, pairs = cl.changed_markdown_pairs("base", "head")
    assert comparison_base == "fork-point"
    assert pairs == [
        ("page.md", "page.md"),
        (None, "new.md"),
        ("old.md", None),
        ("before.md", "after.md"),
    ]


def _git(repo: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        check=True,
    )
    return result.stdout.strip()


def test_uses_merge_base_when_current_base_renamed_the_old_path(
    tmp_path: Path, monkeypatch,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-b", "main")
    _git(repo, "config", "user.name", "Gate Test")
    _git(repo, "config", "user.email", "gate@example.invalid")
    (repo / "old.md").write_text("# Page\n", encoding="utf-8")
    _git(repo, "add", "old.md")
    _git(repo, "commit", "-m", "base")

    _git(repo, "switch", "-c", "feature")
    (repo / "old.md").write_text(
        "# Page\n\n[New](https://example.com/new)\n",
        encoding="utf-8",
    )
    _git(repo, "commit", "-am", "feature changes old path")
    head_sha = _git(repo, "rev-parse", "HEAD")

    _git(repo, "switch", "main")
    _git(repo, "mv", "old.md", "renamed.md")
    _git(repo, "commit", "-m", "base renames page")
    base_sha = _git(repo, "rev-parse", "HEAD")

    # The effective merge must be conflict-free; this command writes only a
    # temporary tree object and does not change the checkout.
    assert _git(repo, "merge-tree", "--write-tree", base_sha, head_sha)
    monkeypatch.setattr(cl, "ROOT", repo)
    assert cl.new_urls_from_git(base_sha, head_sha) == ["https://example.com/new"]


def test_refusals_and_timeouts_are_unverified_not_broken() -> None:
    assert cl.verdict(cl.Probe("u", 403)) == "unverified"
    assert cl.verdict(cl.Probe("u", 429)) == "unverified"
    assert cl.verdict(cl.Probe("u", None, "timeout")) == "unverified"


def test_missing_pages_and_bad_root_redirects_fail() -> None:
    assert cl.verdict(cl.Probe("u", 404)) == "failed"
    assert cl.verdict(cl.Probe("u", 410)) == "failed"
    assert cl._links.bad_redirect(
        "https://docs.example.com/guides/tool",
        "https://docs.example.com/",
    )
    assert not cl._links.bad_redirect(
        "https://docs.example.com/old/tool",
        "https://docs.example.com/new/tool",
    )

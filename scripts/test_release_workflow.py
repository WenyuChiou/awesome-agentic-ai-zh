from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "release.yml"
BUILD_SCRIPT = ROOT / "scripts" / "build-pdf.sh"


def load_workflow() -> dict:
    return yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)


def test_release_can_only_be_started_manually() -> None:
    workflow = load_workflow()
    assert set(workflow["on"]) == {"workflow_dispatch"}
    assert workflow["permissions"] == {"contents": "read"}
    assert workflow["concurrency"]["cancel-in-progress"] == "false"


def test_only_environment_guarded_publish_job_can_write() -> None:
    jobs = load_workflow()["jobs"]
    assert "permissions" not in jobs["prepare"]
    assert jobs["publish"]["environment"] == "release"
    assert jobs["publish"]["permissions"] == {"contents": "write"}
    assert jobs["publish"]["needs"] == "prepare"


def test_prepare_locks_main_and_builds_all_locales() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert text.count("runs-on: ubuntu-24.04") == 2
    assert "test \"$DISPATCH_REF\" = refs/heads/main" in text
    assert "https://api.github.com/" in text
    assert "environments/release" in text
    assert "required_reviewers" in text
    assert "test \"$sha\" = \"$remote_main\"" in text
    assert "for locale in zh-TW zh-Hans en" in text
    assert "validate-pdfs" in text
    assert "--mode release" in text


def test_publish_rechecks_sha_and_verifies_draft_before_publish() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert text.count('test "$current_main" = "$LOCKED_SHA"') == 2
    assert text.count('test "$(git rev-list -n 1 "$RELEASE_VERSION")" = "$LOCKED_SHA"') == 2
    assert 'git ls-remote --exit-code --tags origin "refs/tags/$RELEASE_VERSION"' in text
    draft = text.index("Create or refresh a Draft Release")
    verify = text.index("Verify the Draft Release before publishing")
    publish = text.index("Publish and verify the Release")
    assert draft < verify < publish
    draft_verify_block = text[verify:publish]
    assert 'gh release view "$RELEASE_VERSION" --repo "$REPOSITORY"' in draft_verify_block
    assert "--json isDraft,targetCommitish,body,assets" in draft_verify_block
    assert 'test "$(jq -r .isDraft /tmp/release.json)" = true' in draft_verify_block
    assert 'test "$(jq -r .targetCommitish /tmp/release.json)" = "$LOCKED_SHA"' in draft_verify_block
    assert "releases/tags/" not in draft_verify_block
    refresh_block = text[draft:verify]
    existing_draft_branch = refresh_block.split("          else", maxsplit=1)[0]
    assert 'gh release edit "$RELEASE_VERSION"' in existing_draft_branch
    assert '--draft --target "$LOCKED_SHA" --title "$title"' in existing_draft_branch
    publish_command = text.index(
        'gh release edit "$RELEASE_VERSION" --repo "$REPOSITORY" --draft=false --latest',
        publish,
    )
    tag_fetch = text.index(
        'git fetch --force origin "refs/tags/$RELEASE_VERSION:refs/tags/$RELEASE_VERSION"',
        publish,
    )
    assert publish_command < tag_fetch
    for locale in ("zh-TW", "zh-Hans", "en"):
        assert f'awesome-agentic-ai-zh-$RELEASE_VERSION-{locale}.pdf' in text


def test_pdf_builder_reads_manifest_instead_of_hardcoding_pages() -> None:
    text = BUILD_SCRIPT.read_text(encoding="utf-8")
    assert 'release_manifest.py validate --strict-urls --version "$RELEASE_VERSION"' in text
    assert "release_manifest.py assemble" in text
    assert "stages/01-llm-basics" not in text
    assert "LANG_VARIANT must be zh-TW, zh-Hans, or en" in text

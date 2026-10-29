"""Guard the documented reviewer config and maintainer approval boundary."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_review_configuration_preserves_human_control():
    config = json.loads((ROOT / ".greptile/config.json").read_text(encoding="utf-8"))
    assert config["autoApprove"] == {"enabled": False}
    assert config["statusCheck"] is True
    assert config["shouldUpdateDescription"] is False
    assert config["autoReview"] == ["open", "push"]
    # No bypass filters, external repositories, or paid-tier override.
    assert set(config) == {"autoApprove", "statusCheck", "shouldUpdateDescription", "autoReview"}


def test_context_files_are_local_current_contracts():
    context = json.loads((ROOT / ".greptile/files.json").read_text(encoding="utf-8"))
    entries = context["files"]
    assert {entry["path"] for entry in entries} == {
        "CLAUDE.md", "stages/DESIGN.md", "resources/style-guide.md"
    }
    assert len(entries) == 3
    for entry in entries:
        path = (ROOT / entry["path"]).resolve()
        assert path.is_relative_to(ROOT) and path.is_file()
        assert entry["description"].strip()
        assert set(entry) == {"path", "description"}

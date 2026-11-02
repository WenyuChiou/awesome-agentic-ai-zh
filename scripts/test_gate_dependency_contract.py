"""Keep the PR/release docs environments compatible and fail on resolver drift."""

from pathlib import Path
import re

import pytest
import yaml


ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize(
    "filename,job,step_name",
    [
        ("pr-gate.yml", "quality", "Install locked gate dependencies"),
        ("release.yml", "prepare", "Install locked content-gate dependencies"),
    ],
)
def test_docs_gate_dependency_install_is_consistent(filename, job, step_name):
    workflow = yaml.safe_load((ROOT / ".github/workflows" / filename).read_text())
    step = next(s for s in workflow["jobs"][job]["steps"] if s.get("name") == step_name)
    commands = [line.strip() for line in step["run"].splitlines()
                if line.strip() and not line.lstrip().startswith("#")]
    pins = re.findall(r"\brequests==([0-9.]+)\b", step["run"])
    assert len(pins) == 1, "Keep an explicit, single Requests pin in each gate"
    # Material 9.8.0 requires requests>=2.33.0; do not downgrade after docs install.
    assert tuple(map(int, pins[0].split("."))) >= (2, 33, 0)
    assert commands[-1] == "python -m pip check", "Validate after every install"
    assert commands.count("python -m pip check") == 1
    assert not step.get("continue-on-error"), "Dependency conflicts must block the gate"
    assert "--require-hashes -r scripts/requirements-reader-ux.txt" in step["run"]

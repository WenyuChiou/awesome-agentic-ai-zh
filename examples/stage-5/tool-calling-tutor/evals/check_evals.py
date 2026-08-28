"""Validate the tutor's offline behavior contracts without calling a model."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


ROOT = Path(__file__).resolve().parents[1]
CONFIG = Path(__file__).with_name("evals.json")
EXPECTED_ROUTES = {"a", "b", "c", "d", "away"}
SKILLS = (
    ROOT / "SKILL.md",
    ROOT / "translations/SKILL.en.md",
    ROOT / "translations/SKILL.zh-Hans.md",
)


def heading_slugs(text: str) -> set[str]:
    """Return the simple GitHub-style slugs used by this fixture."""
    slugs: set[str] = set()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*$", text, flags=re.MULTILINE):
        clean = re.sub(r"[`*_]", "", heading).strip().lower()
        clean = re.sub(r"[^\w\-\u3400-\u9fff ]", "", clean)
        slugs.add(re.sub(r"[\s-]+", "-", clean).strip("-"))
    return slugs


def validate_case(case: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(case, dict):
        return ["case must be an object"]

    case_id = case.get("id", "<missing-id>")
    for key in ("id", "locale", "input", "expected_route", "reference", "must_cover"):
        if key not in case:
            errors.append(f"{case_id}: missing {key}")

    route = case.get("expected_route")
    if route not in EXPECTED_ROUTES:
        errors.append(f"{case_id}: unknown route {route!r}")

    must_cover = case.get("must_cover")
    if not isinstance(must_cover, list) or len(must_cover) < 2:
        errors.append(f"{case_id}: must_cover needs at least two checks")
    elif any(not isinstance(item, str) or not item.strip() for item in must_cover):
        errors.append(f"{case_id}: must_cover entries must be non-empty strings")

    reference = case.get("reference")
    if route == "away":
        if reference != "":
            errors.append(f"{case_id}: route-away case must not invent a reference")
        return errors
    if not isinstance(reference, str) or not reference.startswith("references/"):
        errors.append(f"{case_id}: reference must stay inside references/")
        return errors

    path_text, _, anchor = reference.partition("#")
    target = ROOT / path_text
    if not target.is_file():
        errors.append(f"{case_id}: missing reference file {path_text}")
    elif anchor and anchor not in heading_slugs(target.read_text(encoding="utf-8")):
        errors.append(f"{case_id}: missing reference anchor #{anchor}")
    return errors


def main() -> int:
    document = json.loads(CONFIG.read_text(encoding="utf-8"))
    errors: list[str] = []
    if document.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    cases = document.get("cases")
    if not isinstance(cases, list):
        errors.append("cases must be a list")
        cases = []

    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(cases) != 5:
        errors.append(f"expected 5 cases, found {len(cases)}")
    if len(ids) != len(set(ids)):
        errors.append("case ids must be unique")
    routes = {
        case.get("expected_route") for case in cases if isinstance(case, dict)
    }
    if routes != EXPECTED_ROUTES:
        errors.append(f"routes must be exactly {sorted(EXPECTED_ROUTES)}")
    for case in cases:
        errors.extend(validate_case(case))

    for skill in SKILLS:
        text = skill.read_text(encoding="utf-8")
        if "name: tool-calling-tutor" not in text:
            errors.append(f"{skill.name}: missing stable skill name")
        if "${CLAUDE_SKILL_DIR}/references/" not in text:
            errors.append(f"{skill.name}: bundled references are not install-safe")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {len(cases)}/5 offline behavior contracts are complete and linked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

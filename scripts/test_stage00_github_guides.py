"""Keep the document-upload story and numbered screenshot routes usable."""
from __future__ import annotations

import json
from pathlib import Path
import re
import struct

import pytest


ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "resources/diagrams"
GUIDES = json.loads((DIAGRAMS / "github-screenshot-guides.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("suffix", ["", ".en", ".zh-Hans"])
def test_document_workflow_keeps_local_and_remote_steps_visible(suffix: str) -> None:
    source = (ROOT / f"stages/00-foundations{suffix}.md").read_text(encoding="utf-8")
    story = source[source.index("git switch -c docs/my-first-update") : source.index("## 🛠")]
    commands = [
        "git switch -c docs/my-first-update", "git status", "git diff",
        "git add README.md", 'git commit -m "docs: clarify the introduction"',
        "git push -u origin docs/my-first-update", "git switch main", "git pull --ff-only",
    ]
    positions = [story.index(command) for command in commands]
    assert positions == sorted(positions)
    assert "<details" not in story
    # CJK punctuation beside Markdown ** can stay literal on GitHub even
    # when the MkDocs renderer makes it bold. Explicit HTML keeps both aligned.
    labels = re.findall(r"<strong>(.*?)</strong>", story)
    for term in ("Branch", "Staging Area", "origin", "Review", "Pull", "Fork"):
        assert any(term in label for label in labels), term
    for term in ("Staging Area", "origin", "Fork", "Review", "Committer", "Checks", "Closed"):
        assert term in story
    start = source.rfind("\n1. **", 0, source.index("git switch -c docs/my-first-update"))
    end = source.index("\n### ", start)
    assert len(re.findall(r"^\d\. \*\*", source[start:end], re.MULTILINE)) == 7


@pytest.mark.parametrize("suffix", ["", ".en", ".zh-Hans"])
def test_each_screenshot_has_a_visible_source_and_numbered_explanation(suffix: str) -> None:
    source = (ROOT / f"stages/00-foundations{suffix}.md").read_text(encoding="utf-8")
    for guide in GUIDES["guides"]:
        image = f"../resources/diagrams/{guide['stem']}{suffix}.png"
        assert source.count(image) == 1
        position = source.index(image)
        assert guide["source"] in source[:position]
        next_image = source.find("![", position)
        end = next_image if next_image != -1 else source.index("## 🛠", position)
        explanation = source[position:end]
        for number in "①②③④⑤⑥"[:len(guide["annotations"])]:
            assert number in explanation


def test_three_guides_keep_same_targets_and_real_localized_images() -> None:
    assert [len(guide["annotations"]) for guide in GUIDES["guides"]] == [6, 5, 4]
    for guide in GUIDES["guides"]:
        x, y, width, height = guide["crop"]
        assert len(guide["titles"]) == 3
        pixels = []
        for suffix in ("", ".en", ".zh-Hans"):
            image = (DIAGRAMS / f"{guide['stem']}{suffix}.png").read_bytes()
            assert image[:8] == b"\x89PNG\r\n\x1a\n"
            rendered_width, rendered_height = struct.unpack(">II", image[16:24])
            assert rendered_width == 1440
            assert 700 <= rendered_height <= 1100
            pixels.append(image)
        assert len(set(pixels)) == 3  # Localized annotations must not reuse one PNG.
        for annotation in guide["annotations"]:
            rx, ry, rw, rh = annotation["rect"]
            assert x <= rx < rx + rw <= x + width
            assert y <= ry < ry + rh <= y + height
            for key in ("labels", "notes"):
                assert len(annotation[key]) == 3
                assert all(value.strip() for value in annotation[key])

"""Model-lifecycle teaching, locale, and progressive-disclosure contracts."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
STAGE1 = {
    "zh-TW": ROOT / "stages/01-llm-basics.md",
    "en": ROOT / "stages/01-llm-basics.en.md",
    "zh-Hans": ROOT / "stages/01-llm-basics.zh-Hans.md",
}
GUIDES = {
    "zh-TW": ROOT / "resources/model-training-guide.md",
    "en": ROOT / "resources/model-training-guide.en.md",
    "zh-Hans": ROOT / "resources/model-training-guide.zh-Hans.md",
}
STAGE6 = {
    "zh-TW": ROOT / "stages/06-memory-rag.md",
    "en": ROOT / "stages/06-memory-rag.en.md",
    "zh-Hans": ROOT / "stages/06-memory-rag.zh-Hans.md",
}
IMAGE_NAMES = {
    "zh-TW": "model-lifecycle-to-agent.png",
    "en": "model-lifecycle-to-agent.en.png",
    "zh-Hans": "model-lifecycle-to-agent.zh-Hans.png",
}
LIFECYCLE_TERMS = (
    "Pre-training",
    "Base Model",
    "Post-training",
    "Instruct Model",
    "Inference",
)
ADAPTATION_TERMS = (
    "SFT",
    "DPO",
    "RLHF",
    "GRPO",
    "PEFT",
    "LoRA",
    "Distillation",
    "Quantization",
)
OFFICIAL_URLS = (
    "https://openai.com/policies/how-chatgpt-and-our-foundation-models-are-developed/",
    "https://developers.google.com/machine-learning/crash-course/llm/tuning",
    "https://openai.com/index/introducing-gpt-oss/",
    "https://huggingface.co/docs/trl/quickstart",
    "https://huggingface.co/docs/peft/main/methods/overview",
    "https://huggingface.co/docs/peft/main/conceptual_guides/lora",
    "https://huggingface.co/docs/transformers/main_classes/quantization",
)


def _without_details(text: str) -> str:
    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.DOTALL)


@pytest.mark.parametrize("locale,page", STAGE1.items())
def test_stage1_keeps_the_model_lifecycle_visible(locale: str, page: Path) -> None:
    visible = _without_details(page.read_text(encoding="utf-8"))
    assert "Pre-training → Base Model → Post-training → Instruct Model → Inference → Agent" in visible
    for term in ("Pre-training", "Post-training", "Fine-tuning", "Inference"):
        assert f"**{term}" in visible
    assert IMAGE_NAMES[locale] in visible
    assert "model-training-guide" in visible
    assert OFFICIAL_URLS[0] in visible and OFFICIAL_URLS[1] in visible


@pytest.mark.parametrize("locale,page", GUIDES.items())
def test_training_guide_keeps_terms_resources_and_completion_visible(
    locale: str, page: Path
) -> None:
    text = page.read_text(encoding="utf-8")
    visible = _without_details(text)
    for term in (
        "Pre-training",
        "Post-training",
        "Inference",
        "Agent",
        *ADAPTATION_TERMS,
    ):
        assert term in visible
    assert IMAGE_NAMES[locale] in visible
    assert all(url in visible for url in OFFICIAL_URLS)
    assert visible.count("⭐") == 29

    tables = re.findall(r"<table>.*?</table>", visible, flags=re.DOTALL)
    assert len(tables) == 2
    groups = re.findall(r"<tbody>(.*?)</tbody>", tables[1], flags=re.DOTALL)
    assert len(groups) == 3
    assert [len(re.findall(r"<tr>", group)) for group in groups] == [2, 2, 3]
    assert [int(value) for value in re.findall(r'rowspan="(\d+)"', tables[1])] == [2, 2, 3]

    openings = re.findall(r"^<details\b[^>]*>", text, flags=re.MULTILINE)
    assert openings == ['<details markdown="1">']
    assert not re.search(r"<details\b[^>]*\bopen\b", text)


def test_model_lifecycle_images_are_real_distinct_locale_pngs() -> None:
    hashes = set()
    for name in IMAGE_NAMES.values():
        path = ROOT / "resources/diagrams" / name
        data = path.read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n")
        assert len(data) > 100_000
        hashes.add(hashlib.sha256(data).hexdigest())
    assert len(hashes) == 3


@pytest.mark.parametrize("locale,page", STAGE6.items())
def test_stage6_routes_fine_tuning_to_the_locale_guide(locale: str, page: Path) -> None:
    suffix = {"zh-TW": "", "en": ".en", "zh-Hans": ".zh-Hans"}[locale]
    text = page.read_text(encoding="utf-8")
    assert f"../resources/model-training-guide{suffix}.md" in text


def test_freshness_markers_share_one_date_and_canonical_scope() -> None:
    stage_markers = []
    guide_markers = []
    for page in STAGE1.values():
        text = page.read_text(encoding="utf-8")
        stage_markers.extend(re.findall(r"<!-- freshness: .*? -->", text))
    for page in GUIDES.values():
        text = page.read_text(encoding="utf-8")
        guide_markers.extend(re.findall(r"<!-- freshness: .*? -->", text))

    assert len(set(stage_markers)) == 1
    assert len(set(guide_markers)) == 1
    assert "verified_on=2026-08-31" in stage_markers[0]
    assert "scope=models,pricing,availability,deprecations,model-lifecycle" in stage_markers[0]
    assert "canonical=resources/model-training-guide.md" in guide_markers[0]
    assert "verified_on=2026-08-31" in guide_markers[0]
    assert "scope=model-training,post-training,adaptation,compression,inference" in guide_markers[0]

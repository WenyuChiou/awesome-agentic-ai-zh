"""Reader-visible first-use fixtures for explicitly audited terminology.

This is a bounded content regression suite, not a site-wide acronym detector or
an authority for interpreting product names, schema identifiers, or all caps.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import markdown
import pytest
from dataclasses import dataclass, field
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
FULL_NAMES = {
    "SFT": "Supervised Fine-Tuning",
    "DPO": "Direct Preference Optimization",
    "RLHF": "Reinforcement Learning from Human Feedback",
    "RL": "Reinforcement Learning",
    "GRPO": "Group Relative Policy Optimization",
    "PEFT": "Parameter-Efficient Fine-Tuning",
    "LoRA": "Low-Rank Adaptation",
    "RAG": "Retrieval-Augmented Generation",
    "GPU": "Graphics Processing Unit",
    "LLM": "Large Language Model",
    "SDK": "Software Development Kit",
    "MCP": "Model Context Protocol",
    "API": "Application Programming Interface",
    "CRAG": "Corrective Retrieval Augmented Generation",
    "JSON": "JavaScript Object Notation",
    "CLI": "Command-Line Interface",
    "CoT": "Chain-of-Thought",
    "MRR": "Mean Reciprocal Rank",
    "nDCG": "Normalized Discounted Cumulative Gain",
    "HyDE": "Hypothetical Document Embeddings",
    "RAPTOR": "Recursive Abstractive Processing for Tree-Organized Retrieval",
}
# One standalone chapter is one context. Later glossary definitions cannot
# satisfy an earlier label; no automatic all-caps or product-name expansion.
AUDITED_PAGES = {
    "resources/model-training-guide.md": ("SFT", "DPO", "RLHF", "RL", "GRPO", "PEFT", "LoRA", "RAG", "GPU", "LLM"),
    "stages/01-llm-basics.md": ("SFT", "DPO", "RLHF", "RL", "GRPO", "PEFT", "LoRA", "LLM", "RAG", "API", "SDK"),
    "resources/glossary.md": ("RLHF", "RL", "GRPO", "PEFT", "LoRA", "RAG", "MCP", "LLM", "API"),
    "stages/06-memory-rag.md": ("RAG", "CRAG"),
    "resources/advanced-rag.md": ("RAG", "CRAG", "LLM", "MRR", "nDCG", "HyDE", "RAPTOR"),
    "stages/00-foundations.md": ("API", "JSON"),
    "tracks/cli/A1-cli-intro.md": ("CLI", "LLM", "API"),
    "stages/03-tool-use-and-hello-agent.md": ("JSON",),
    # README is a navigation page: CLI/MCP teaching definitions remain in A1
    # and the glossary. Its banner no longer carries detached term paragraphs.
    "README.md": ("LLM", "API", "JSON", "CoT", "RAG"),
}
LOCALES = ("zh-TW", "en", "zh-Hans")
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
BLOCK_TAGS = HEADING_TAGS | {"p", "li", "td", "th", "summary"}


def locale_path(canonical: str, locale: str) -> Path:
    suffix = "" if locale == "zh-TW" else f".{locale}"
    return ROOT / (canonical[:-3] + suffix + ".md")


@dataclass
class _Block:
    kind: str
    parts: list[str] = field(default_factory=list)


class _ReaderText(HTMLParser):
    """Test-only source-order blocks; no acronym recognition or production hook."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[dict] = []
        self.blocks: list[_Block] = []
        self.nodes: list[tuple[str, int, bool]] = []
        self.in_alt = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        before_hidden = bool(self.stack and self.stack[-1]["hidden"])
        hidden = before_hidden
        if tag == "summary" and self.stack and self.stack[-1]["closed_details"]:
            hidden = self.stack[-1]["before_hidden"]
        closed_details = tag == "details" and "open" not in attributes
        hidden = hidden or closed_details or tag in {"pre", "code", "script", "style"}
        hidden = hidden or "hidden" in attributes or attributes.get("aria-hidden") == "true"
        style = str(attributes.get("style", ""))
        hidden = hidden or bool(re.search(r"(?:display\s*:\s*none|visibility\s*:\s*hidden)", style, re.I))
        block_id = None
        if tag in BLOCK_TAGS and not hidden:
            block_id = len(self.blocks)
            self.blocks.append(_Block(tag))
        if tag == "img":
            if not hidden:
                self.in_alt = True
                self.handle_data(str(attributes.get("alt", "")))
                self.in_alt = False
            return
        if tag in {"br", "hr", "input", "meta", "link", "source", "wbr"}:
            return
        self.stack.append({"tag": tag, "hidden": hidden, "before_hidden": before_hidden,
                           "closed_details": closed_details, "block_id": block_id})

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if not self.stack or self.stack[-1]["hidden"] or not data.strip():
            return
        # Attribute URLs are not data; literal URL labels are also excluded.
        if re.match(r"\s*https?://", data):
            return
        ids = [item["block_id"] for item in self.stack if item["block_id"] is not None]
        if ids:
            self.nodes.append((data, ids[-1], self.in_alt))
            for block_id in ids:
                self.blocks[block_id].parts.append(data)


def reader_blocks(text: str) -> _ReaderText:
    parser = _ReaderText()
    parser.feed(markdown.markdown(text, extensions=["extra"]))
    parser.close()
    return parser


def _token(term: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![A-Za-z0-9_]){re.escape(term)}(?![A-Za-z0-9_])")


def _adjacent_name(context: str, term: str, full_name: str) -> bool:
    text = re.sub(r"\s+", " ", context).strip()
    first = _token(term).search(text)
    if first is None:
        return False
    name = re.escape(full_name)
    following = text[first.end() :]
    if re.match(rf"\s*[（(]\s*{name}(?:\s*[,，:：;；]|\s*[）)])", following, re.I):
        return True
    return bool(re.search(rf"{name}\s*[（(]\s*$", text[: first.start()], re.I))


def assert_first_reader_expansion(text: str, term: str, full_name: str) -> None:
    """Allow an unchanged heading with its immediately adjacent visible legend."""
    parsed = reader_blocks(text)
    first = next(((value, block_id, in_alt) for value, block_id, in_alt in parsed.nodes if _token(term).search(value)), None)
    assert first is not None, f"missing audited term {term}"
    _, block_id, in_alt = first
    assert not in_alt, f"{term} needs a visible learner legend, not alt alone"
    block = parsed.blocks[block_id]
    if _adjacent_name(" ".join(block.parts), term, full_name):
        return
    # A short old heading keeps its deep link. Only its immediate visible
    # paragraph can supply the name; an unrelated introduction cannot.
    if block.kind in HEADING_TAGS and block_id + 1 < len(parsed.blocks):
        next_block = parsed.blocks[block_id + 1]
        if next_block.kind == "p" and _adjacent_name(" ".join(next_block.parts), term, full_name):
            return
    raise AssertionError(f"{term} needs its full name at its first reader encounter")


@pytest.mark.parametrize("locale", LOCALES)
@pytest.mark.parametrize("canonical,term", [(p, t) for p, terms in AUDITED_PAGES.items() for t in terms])
def test_audited_pages_define_first_reader_encounter(canonical: str, term: str, locale: str) -> None:
    assert_first_reader_expansion(locale_path(canonical, locale).read_text(encoding="utf-8"), term, FULL_NAMES[term])


@pytest.mark.parametrize("text", [
    "API is an interface.\n\nAPI (Application Programming Interface) requests data.",
    "API is an interface.\n\n```text\nAPI (Application Programming Interface)\n```",
    "API is an interface.\n\n<!-- API (Application Programming Interface) -->",
    "API is an interface.\n\n<details markdown=\"1\"><summary>More</summary>\n\nAPI (Application Programming Interface)\n\n</details>",
    '<p title="API (Application Programming Interface)">API is an interface.</p>',
    "# API\n\nAn unrelated introduction.\n\nAPI (Application Programming Interface) requests data.",
    "![API shown in an image](diagram.png)\n\nAPI (Application Programming Interface) requests data.",
    "![API (Application Programming Interface)](diagram.png)",
    '<p hidden>API (Application Programming Interface)</p> API is an interface.',
    '<p aria-hidden="true">API (Application Programming Interface)</p> API is an interface.',
    '<p style="display:none">API (Application Programming Interface)</p> API is an interface.',
    '<p style="visibility:hidden">API (Application Programming Interface)</p> API is an interface.',
    '<p><span hidden>API (Application Programming Interface)</span> API is an interface.</p>',
])
def test_late_or_nonprose_definition_cannot_satisfy_first_encounter(text: str) -> None:
    with pytest.raises(AssertionError):
        assert_first_reader_expansion(text, "API", FULL_NAMES["API"])


@pytest.mark.parametrize("text,term", [
    ("# API\n\n**API (Application Programming Interface)** lets programs request data.", "API"),
    ("**API (Application Programming Interface)** lets programs request data.\n\n![API](diagram.png)", "API"),
    ("<table><tr><td>Method</td><td>GRPO (Group Relative Policy Optimization)</td><td>Compare rewards.</td></tr></table>", "GRPO"),
    ("<table><tr><td>RLHF (Reinforcement Learning from Human Feedback) / RL (Reinforcement Learning)</td></tr></table>", "RL"),
    ("<table><tr><td>PEFT (Parameter-Efficient Fine-Tuning)</td><td>Train fewer parameters.</td></tr></table>", "PEFT"),
])
def test_heading_legend_and_real_table_token_boundaries(text: str, term: str) -> None:
    assert_first_reader_expansion(text, term, FULL_NAMES[term])


# Actual image pixels were manually reviewed separately from text extraction.
# These finite position cases bind the known labels to a preceding visible
# learner legend. They do not perform OCR or claim to detect every image term.
IMAGE_LEGENDS = {
    "resources/model-training-guide.md": ("model-lifecycle-to-agent", ("SFT", "DPO", "RLHF", "RL", "RAG")),
}


@pytest.mark.parametrize("locale", LOCALES)
@pytest.mark.parametrize("canonical,term", [(p, t) for p, (_, terms) in IMAGE_LEGENDS.items() for t in terms])
def test_manually_reviewed_image_terms_have_a_visible_prior_legend(canonical: str, term: str, locale: str) -> None:
    text = locale_path(canonical, locale).read_text(encoding="utf-8")
    stem, _ = IMAGE_LEGENDS[canonical]
    image = re.search(rf"^!\[[^\n]*?\]\([^\n]*{re.escape(stem)}[^\n]*\)", text, re.M)
    assert image is not None
    before_image = text[:image.start()]
    assert_first_reader_expansion(before_image, term, FULL_NAMES[term])


@pytest.mark.parametrize("locale", LOCALES)
def test_json_schema_standard_name_is_not_split_by_an_expansion(locale: str) -> None:
    text = locale_path("stages/03-tool-use-and-hello-agent.md", locale).read_text(encoding="utf-8")
    assert "JSON Schema" in text
    assert not re.search(r"JSON\s*[（(][^\n]*?[）)]\s*Schema", text)


# Hashes bind the six manually inspected originals; they are not semantic proof.
REVIEWED_IMAGE_HASHES = {'resources/diagrams/model-lifecycle-to-agent.png': 'aa13946e14ff57a005d28f7f8a0d7bb81644a4ea53290d26f971d44c36154084', 'resources/diagrams/model-lifecycle-to-agent.en.png': '72f295b142def7ac8813f7154973acde2d2f1f1f6e5ba2df0d242bb9a082b383', 'resources/diagrams/model-lifecycle-to-agent.zh-Hans.png': '8dcb27f1621db09a5d410577d75cb868a41fa942430e8828dcfe54f64b88c19b', 'resources/diagrams/banner.png': '50f703f2820935eb57c80e16cbadc89120a590aae541650139aba153b3833de2', 'resources/diagrams/banner.en.png': '5eee4cb7b4affca9904e9ef6d345941a30b11dc3af5ee5055edf70f7a1b52225', 'resources/diagrams/banner.zh-Hans.png': 'aca7e9dcb24f43d885dd8e16e8fcf5911725db3a6e6024ea3c88e5cc5d24a7b5'}

@pytest.mark.parametrize("path,expected", REVIEWED_IMAGE_HASHES.items())
def test_first_image_label_inventory_stays_bound_to_reviewed_pixels(path: str, expected: str) -> None:
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected

"""The README SVG exception must stay localized, static-readable, and bounded."""
from __future__ import annotations

import importlib.util
import io
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


banner = load("build_banner", "build-banner.py")
delivery = load("banner_image_delivery", "check-image-delivery.py")
locale_gate = load("banner_image_locale", "check-image-locale.py")
SVG = "{http://www.w3.org/2000/svg}"


@pytest.mark.parametrize("locale", banner.LOCALES)
def test_banner_is_exactly_reproducible_and_self_contained(locale):
    suffix = banner.LOCALES[locale]["suffix"]
    path = ROOT / f"resources/diagrams/banner{suffix}.svg"
    source = path.read_text(encoding="utf-8")
    assert source == banner.build_svg(locale)
    tree = ET.fromstring(source)
    assert tree.attrib["viewBox"] == "0 0 1672 941"
    assert tree.attrib["lang"] == locale
    assert tree.find(SVG + "title").text
    assert tree.find(SVG + "desc").text
    allowed = {"svg", "title", "desc", "metadata", "style", "image", "path", "rect", "circle", "g", "defs", "clipPath", "use"}
    for element in tree.iter():
        assert element.tag.removeprefix(SVG) in allowed
        assert not any(key.lower().startswith("on") for key in element.attrib)
        if "href" in element.attrib:
            if element.tag == SVG + "image":
                assert element.attrib["href"].startswith("data:image/webp;base64,")
            else:
                assert element.tag == SVG + "use"
                assert element.attrib["href"] == "#original-art"
    assert len(tree.findall(SVG + "image")) == 1
    assert tree.find(SVG + "image").attrib["id"] == "original-art"
    with Image.open(io.BytesIO(banner.read_art(locale))) as art:
        with Image.open(path.with_suffix(".png")) as static:
            assert art.size == static.size == (1672, 941)
            assert art.convert("RGB").tobytes() == static.convert("RGB").tobytes()
    css = tree.find(SVG + "style").text
    assert "18s linear infinite" in css
    assert "prefers-reduced-motion:reduce" in css
    assert not re.search(r"@import|@font-face|https?:|data:", css)
    assert all(target.startswith("#") for target in re.findall(r"url\((.*?)\)", source))
    assert path.stat().st_size < 300_000
    # Only bounded icon crops move; text, cards, and complete arrows stay fixed.
    assert all(re.fullmatch(r"\.(dot|halo|icon-layer|icon-motion)(-[\w-]+)?", selector) for selector in
               re.findall(r"(\.[\w-]+)\{[^{}]*animation:", css))
    assert not re.search(r"<(text|path|g)\b[^>]*class=\"(?:dot|halo)", source)


@pytest.mark.parametrize("locale", banner.LOCALES)
def test_representative_icons_reuse_original_pixels_and_do_not_add_another_art_style(locale):
    tree = ET.fromstring(banner.build_svg(locale))
    icons = [node for node in tree.findall(SVG + "g") if node.attrib.get("id", "").startswith("icon-")]
    assert [node.attrib["id"] for node in icons] == [f"icon-{name}" for name in banner.ICON_MOTION]
    assert len(icons) == 13
    assert len(banner.ICONS[locale]) == len(icons)
    with Image.open(io.BytesIO(banner.read_art(locale))) as art:
        for node, (name, (motion, windows)), (x,y,w,h) in zip(icons, banner.ICON_MOTION.items(), banner.ICONS[locale], strict=True):
            assert node.attrib["data-motion"] == motion
            assert list(node.iter(SVG + "use"))[0].attrib["href"] == "#original-art"
            clip = node.find(f'{SVG}defs/{SVG}clipPath')
            assert clip.attrib["id"] == f"clip-icon-{name}"
            assert clip.find(SVG + "rect").attrib == dict(x=str(x), y=str(y), width=str(w), height=str(h))
            assert 0 <= x < x+w <= 1672 and 0 <= y < y+h <= 941
            assert all(0 <= start < end < 16 for start, end in windows)
            if not name.startswith("cli"):
                corners = [art.getpixel(p) for p in [(x,y),(x+w-1,y),(x,y+h-1),(x+w-1,y+h-1)]]
                assert all(min(rgb[:3]) > 210 for rgb in corners), (locale, name, corners)
    css = tree.find(SVG + "style").text
    assert ".icon-layer{opacity:0;pointer-events:none}" in css
    assert ".dot,.halo,.icon-layer,.icon-motion{animation:none!important}" in css
    assert ".dot,.halo,.icon-layer{opacity:0!important}" in css


def test_icon_movement_has_a_specific_learning_meaning_and_shared_timing():
    assert banner.ICON_MOTION["cli-large"][0] == "type"
    assert banner.ICON_MOTION["tools-large"][0] == "turn"
    assert banner.ICON_MOTION["hub5"][0] == banner.ICON_MOTION["hub8"][0] == "cycle"
    assert banner.ICON_MOTION["knowledge"][0] == "grow"
    assert banner.ICON_MOTION["research"][0] == "experiment"
    assert banner.ICON_MOTION["checklist"][0] == "check"
    for name, (_, windows) in banner.ICON_MOTION.items():
        if name.startswith("cli"):
            assert all(2 <= start < end <= 8 for start, end in windows)
        if name.startswith("tools"):
            assert all(8 <= start < end <= 16 for start, end in windows)
    assert len({banner.icon_css() for _ in banner.LOCALES}) == 1


def test_small_traditional_chinese_cursor_crop_covers_its_left_edge():
    # Independent visual review found this white edge left stationary at 2.46s.
    index = list(banner.ICON_MOTION).index("cli-small")
    x, y, w, h = banner.ICONS["zh-TW"][index]
    assert x < 60 < x+w and y <= 562 < y+h  # Include a one-pixel left margin.
    assert x+w == 77  # Do not grow toward the terminal circle's right edge.


def test_three_locales_share_graph_topology_and_timing_on_original_art():
    variants = [ET.fromstring(banner.build_svg(locale)) for locale in banner.LOCALES]
    # Existing localized illustrations have slightly different coordinates.
    # Preserve them, rather than redrawing their layout to force pixel parity.
    for tree, locale in zip(variants, banner.LOCALES, strict=True):
        assert [p.attrib["id"] for p in tree.iter(SVG + "path")] == [f"edge-{row[0]}" for row in banner.EDGES]
        assert len(banner.NODES[locale]) == len(banner.WINDOWS)
    styles = [re.sub(r'offset-path:path\("[^"]+"\);', '', tree.find(SVG + "style").text) for tree in variants]
    assert styles[0] == styles[1] == styles[2]
    assert [name for name, route, *_ in banner.EDGES if route == "a"] == [
        "a-entry", "a1-a2", "a2-s5", "s5-a3", "a3-s8"]
    assert [name for name, route, *_ in banner.EDGES if route == "b"] == [
        "b-entry", "s3-s4", "s4-s5", "s5-s6", "s6-s7", "s7-s75", "s75-s8"]
    windows = {"common": (0, 2), "a": (2, 8), "b": (8, 16)}
    for _, route, start, end in banner.EDGES:
        assert windows[route][0] <= start < end <= windows[route][1]
    for current, following in zip(banner.EDGES, banner.EDGES[1:]):
        assert current[3] <= following[2]  # One dot at a time; 16–18s is still.


@pytest.mark.parametrize("locale", banner.LOCALES)
def test_readme_has_real_localized_static_fallback(locale):
    suffix = banner.LOCALES[locale]["suffix"]
    page = ROOT / f"README{suffix}.md"
    refs = [asset for _, asset in locale_gate.scan(page)]
    for extension in ("svg", "png"):
        asset = f"resources/diagrams/banner{suffix}.{extension}"
        assert asset in refs
        assert (ROOT / asset).is_file()
    assert re.search(r"(?<!!)\[[^\]]+\]\(resources/diagrams/banner[^)]*\.png\)", page.read_text(encoding="utf-8"))


def test_svg_and_its_static_fallback_both_consume_image_budget(tmp_path):
    diagrams = tmp_path / "resources/diagrams"
    diagrams.mkdir(parents=True)
    (diagrams / "banner.svg").write_bytes(b"s" * 20)
    (diagrams / "banner.png").write_bytes(b"p" * 30)
    page = tmp_path / "README.md"
    page.write_text("![route](resources/diagrams/banner.svg)", encoding="utf-8")
    metrics, errors = delivery.check_delivery(tmp_path, markdown_paths=[page], max_total_bytes=49, max_page_bytes=49)
    assert metrics.total_bytes == 50
    assert metrics.heaviest_page[1] == 50
    assert any("diagram bytes" in error for error in errors)
    assert any("page README.md" in error for error in errors)


def test_static_banner_link_locale_mismatch_is_not_ignored(tmp_path):
    page = tmp_path / "README.en.md"
    page.write_text("[Static image](resources/diagrams/banner.png)", encoding="utf-8")
    refs = list(locale_gate.scan(page))
    assert refs == [(1, "resources/diagrams/banner.png")]
    assert locale_gate.localized_name(locale_gate.base_name(refs[0][1]), "en") != refs[0][1]

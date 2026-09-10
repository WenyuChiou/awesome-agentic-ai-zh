"""Original-art role animation and its bounded delivery contract."""
from __future__ import annotations

import importlib.util
import io
from pathlib import Path
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops
import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), ROOT / 'scripts' / name)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


role_map = load('build-role-map.py')


@pytest.mark.parametrize('locale', role_map.LOCALES)
def test_role_art_and_generated_overlay_are_pinned(locale):
    art = role_map.read_art(locale)
    svg = role_map.asset_path(locale, 'svg').read_text(encoding='utf-8')
    assert svg == role_map.build_svg(locale, art)
    root = ET.fromstring(svg)
    assert root.attrib['lang'] == locale
    images = root.findall('.//' + role_map.NS + 'image')
    assert len(images) == 1
    assert len(root.findall('.//' + role_map.NS + 'use')) == 5
    assert len(root.findall('.//' + role_map.NS + 'clipPath')) == 5
    assert {g.attrib['id'] for g in root.findall(role_map.NS + 'g')} == {
        'role-' + name for name in role_map.ROLES
    }
    assert all(item.attrib['href'] == '#original-art' for item in root.findall('.//' + role_map.NS + 'use'))
    assert 'prefers-reduced-motion:reduce' in svg
    assert '<script' not in svg and '<foreignObject' not in svg and '@import' not in svg
    with Image.open(io.BytesIO(art)) as original, Image.open(role_map.asset_path(locale, 'png')) as still:
        assert original.size == still.size == role_map.LOCALES[locale][1]
        assert ImageChops.difference(original.convert('RGB'), still.convert('RGB')).getbbox() is None
    width, height = role_map.LOCALES[locale][1]
    for x, y, w, h in role_map.ICONS[locale]:
        assert 0 <= x < x+w <= width and 0 <= y < y+h <= height


def test_five_exclusive_motion_windows_leave_the_end_still():
    css = role_map.animation_css()
    assert len(role_map.ROLES) == len(role_map.POSES) == 5
    windows = [(1+i*3, 3+i*3) for i in range(5)]
    assert all(end < next_start for (_, end), (next_start, _) in zip(windows, windows[1:]))
    assert windows[-1][1] < 16
    assert '.role-layer{opacity:0!important}' in css
    assert '18s' in css


def test_role_fallbacks_are_budgeted_and_counted_as_references():
    # run_path registers the module while its dataclasses are initialized.
    import runpy
    delivery = runpy.run_path(str(ROOT / 'scripts' / 'check-image-delivery.py'))
    locale = load('check-image-locale.py')
    for suffix in ('', '.en', '.zh-Hans'):
        stem = f'resources/diagrams/branch-decision-tree{suffix}'
        assert delivery['_image_targets'](f'![Role]({stem}.svg)') == [stem+'.svg', stem+'.png']
        assert locale.BANNER_FALLBACK_RE.search(f'[Static]({stem}.png)')
    assert not locale.BANNER_FALLBACK_RE.search('[Other](resources/diagrams/branch-decision-tree-custom.png)')

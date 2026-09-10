#!/usr/bin/env python3
"""Animate the existing artwork, without redrawing its text, icons, or layout.

SVGs embed a compressed copy of the original illustration. The only new visible
elements are moving route dots and temporary node outlines. No external assets,
fonts, or JavaScript are loaded. --png decodes the same embedded art for printing.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
from html import escape
import io
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "ca75de9814a321fb3a3e8db606f082b2c2422124"
SVG_NS = "{http://www.w3.org/2000/svg}"
LOCALES = {
    "zh-TW": dict(suffix="", title="AI Agent 學習路徑", desc="保留原版插圖。共用基礎 Stage 0–2 後選路線：A1、A2、Stage 5、A3、Stage 8；或 Stage 3、4、5、6、7、7.5、8。7.5 為進階選讀，五條角色路線依需求選讀。"),
    "en": dict(suffix=".en", title="AI Agent Learning Paths", desc="Original illustration. Start with Stages 0–2. Track A: A1, A2, Stage 5, A3, Stage 8. Track B: 3, 4, 5, 6, 7, 7.5, 8. Stage 7.5 is an advanced option; choose role paths as needed."),
    "zh-Hans": dict(suffix=".zh-Hans", title="AI Agent 学习路径", desc="保留原版插图。共用基础 Stage 0–2 后选路线：A1、A2、Stage 5、A3、Stage 8；或 Stage 3、4、5、6、7、7.5、8。7.5 为进阶选读，五条角色路线按需选择。"),
}
COLORS = {"common": "#626b79", "a": "#0668ff", "b": "#ff8500", "hub": "#5820bd"}
# One topology and timeline; coordinates follow each existing localized image.
EDGES = [
    ("foundation", "common", 1.1, 2),
    ("a-entry", "a", 2, 2.9), ("a1-a2", "a", 3.1, 3.7),
    ("a2-s5", "a", 3.9, 4.5), ("s5-a3", "a", 4.9, 5.9), ("a3-s8", "a", 6.3, 7.4),
    ("b-entry", "b", 8, 9), ("s3-s4", "b", 9.2, 9.8),
    ("s4-s5", "b", 10, 10.6), ("s5-s6", "b", 11, 11.6),
    ("s6-s7", "b", 11.9, 12.5), ("s7-s75", "b", 12.9, 13.5), ("s75-s8", "b", 14.1, 15.1),
]
PATHS = {
    "zh-TW": [
        "M210 398H280", "M285 398C306 398 313 386 313 367V360Q313 339 337 339H350", "M423 338H463",
        "M537 338H557Q578 338 584 367", "M819 399H919", "M993 399H1099",
        "M286 398C323 398 319 429 319 453V621Q319 651 352 651", "M422 651H462",
        "M529 651H557Q577 651 583 618", "M819 536H842", "M901 536H923",
        "M983 536H1006", "M1067 536H1099",
    ],
    "en": [
        "M209 411H285", "M288 411C301 411 309 400 309 381V365Q309 339 336 339H348", "M413 339H460",
        "M528 339H544Q565 339 573 359L587 381", "M783 377Q786 362 805 362H946", "M1012 362H1149",
        "M287 411C315 417 312 441 312 477V601Q312 644 362 644", "M423 645H471",
        "M531 645H543Q562 645 571 618L586 599", "M783 576H823", "M885 576H919",
        "M982 576H1019", "M1082 576H1149",
    ],
    "zh-Hans": [
        "M208 412H285", "M289 412Q317 412 317 384V361Q317 335 340 335H367", "M437 335H476",
        "M546 335H599Q620 335 620 365", "M785 413H920", "M989 413H1163",
        "M289 412Q316 412 316 443V606Q316 640 344 640H364", "M426 640H467",
        "M531 640H586Q607 640 611 618", "M785 570H832", "M895 570H932",
        "M996 570H1033", "M1097 570H1163",
    ],
}
WINDOWS = {
    "base": [(0, 2)], "a1": [(2.9, 3.5)], "a2": [(3.7, 4.3)],
    "s5": [(4.5, 5.1), (10.6, 11.2)], "a3": [(5.9, 6.5)],
    "s8": [(7.4, 8), (15.1, 16)], "s3": [(9, 9.6)], "s4": [(9.8, 10.4)],
    "s6": [(11.6, 12.2)], "s7": [(12.5, 13.1)], "s75": [(13.5, 14.3)],
}
# x, y, width, height, corner radius. Circles use half-width as radius.
NODES = {
    "zh-TW": [(39,343,159,144,15),(351,306,71,65,15),(465,306,72,65,15),
        (587,362,230,252,22),(921,366,71,66,15),(1102,362,228,253,22),
        (356,621,65,61,15),(464,621,64,61,15),(844,508,56,56,15),(925,508,56,56,15),(1008,508,57,56,15)],
    "en": [(25,352,171,147,15),(350,309,62,61,14),(462,309,65,61,14),
        (592,361,190,252,22),(948,330,64,62,14),(1151,361,193,252,22),
        (365,614,56,63,13),(473,614,56,63,13),(824,546,60,60,30),(921,546,60,60,30),(1021,546,60,60,30)],
    "zh-Hans": [(32,353,159,153,16),(370,303,66,65,14),(478,303,67,65,14),
        (576,369,208,244,22),(922,383,66,62,14),(1165,371,192,241,22),
        (366,609,59,61,13),(469,609,60,61,13),(834,541,60,60,30),(934,541,60,60,30),(1035,541,60,60,30)],
}
# Pin the compressed original-art payloads independently of overlay generation.
ART_HASHES = {
    "zh-TW": "1c64dcca8447e54bdfde1ecc54e0e627beb6eb80ce3c610445507763a0912e1d",
    "en": "55c723425fb1276a3d0ea549867c973a4927f35f2c1a7d45c855e5ff645585a4",
    "zh-Hans": "d18657fdc244a8296744cfe22a0af17622c151d08b3239cb3c543c24b729f891",
}


def percent(seconds):
    return f"{seconds / 18 * 100:.4f}%"


def animation_css(locale):
    css = [".dot,.halo{opacity:0}.dot{offset-rotate:0deg}"]
    for (name, route, start, end), path in zip(EDGES, PATHS[locale], strict=True):
        css.append(f'.dot-{name}{{offset-path:path("{path}");animation:travel-{name} 18s linear infinite}}')
        css.append(f'@keyframes travel-{name}{{0%,{percent(start-.001)}{{opacity:0;offset-distance:0%}}'
                   f'{percent(start)}{{opacity:1;offset-distance:0%}}'
                   f'{percent(end)}{{opacity:1;offset-distance:100%}}'
                   f'{percent(end+.001)},100%{{opacity:0;offset-distance:100%}}}}')
    for name, windows in WINDOWS.items():
        css.append(f'.halo-{name}{{animation:light-{name} 18s linear infinite}}')
        frames = ['0%,100%{opacity:0}']
        for start, end in windows:
            frames.extend([f'{percent(start)}{{opacity:0}}', f'{percent(start+.12)}{{opacity:.8}}',
                           f'{percent(end-.12)}{{opacity:.8}}', f'{percent(end)}{{opacity:0}}'])
        css.append(f'@keyframes light-{name}{{{"".join(frames)}}}')
    css.append('@media(prefers-reduced-motion:reduce){.dot,.halo{animation:none!important;opacity:0!important}}')
    return "\n".join(css)


def read_art(locale):
    path = ROOT / f'resources/diagrams/banner{LOCALES[locale]["suffix"]}.svg'
    tree = ET.fromstring(path.read_text(encoding="utf-8"))
    image = tree.find(SVG_NS + "image")
    if image is None:
        raise ValueError("Missing original artwork; use --import-original once")
    header, payload = image.attrib["href"].split(",", 1)
    if header != "data:image/webp;base64":
        raise ValueError("Only the pinned embedded original WebP artwork is supported")
    data = base64.b64decode(payload, validate=True)
    if hashlib.sha256(data).hexdigest() != ART_HASHES[locale]:
        raise ValueError(f"Original artwork changed unexpectedly: {locale}")
    return data


def import_original(locale):
    from PIL import Image

    relative = f'resources/diagrams/banner{LOCALES[locale]["suffix"]}.png'
    original = subprocess.check_output(["git", "show", f"{SOURCE_COMMIT}:{relative}"], cwd=ROOT)
    with Image.open(io.BytesIO(original)) as image:
        if image.size != (1672, 941):
            raise ValueError("Original canvas changed")
        buffer = io.BytesIO()
        # High-quality compression preserves the artwork, not pixel identity.
        # No resizing, repainting, text replacement, or generated icons.
        image.save(buffer, format="WEBP", quality=95, method=6)
    return buffer.getvalue()


def build_svg(locale, art=None):
    art = read_art(locale) if art is None else art
    t = LOCALES[locale]
    encoded = base64.b64encode(art).decode("ascii")
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1672" height="941" viewBox="0 0 1672 941" lang="{locale}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(t["title"])}</title><desc id="desc">{escape(t["desc"])}</desc>',
        f'<metadata>Original artwork: {SOURCE_COMMIT}; WebP quality 95; overlay only.</metadata>',
        f'<style>{animation_css(locale)}</style>',
        f'<image id="original-art" width="1672" height="941" href="data:image/webp;base64,{encoded}"/>']
    for name, (x,y,w,h,radius) in zip(WINDOWS,NODES[locale],strict=True):
        route = "common" if name=="base" else "hub" if name in {"s5","s8"} else "a" if name.startswith("a") else "b"
        parts.append(f'<rect id="node-{name}" class="halo halo-{name}" x="{x-3}" y="{y-3}" width="{w+6}" height="{h+6}" rx="{radius+3}" fill="none" stroke="{COLORS[route]}" stroke-width="3"/>')
    for (name,route,start,end),path in zip(EDGES,PATHS[locale],strict=True):
        parts.append(f'<path id="edge-{name}" d="{path}" fill="none" stroke="none"/>')
        parts.append(f'<circle class="dot dot-{name}" r="6" fill="{COLORS[route]}" stroke="#ffffff" stroke-width="2"/>')
    parts.append('</svg>')
    return "\n".join(parts)+"\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locale", choices=LOCALES)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--png", action="store_true", help="Export static PNG from the same embedded artwork (Pillow)")
    parser.add_argument("--import-original", action="store_true", help="Import artwork from the pinned pre-experiment commit")
    args = parser.parse_args()
    if args.check and (args.png or args.import_original):
        parser.error("--check is read-only")
    for locale in [args.locale] if args.locale else LOCALES:
        target=ROOT/f'resources/diagrams/banner{LOCALES[locale]["suffix"]}.svg'
        art=import_original(locale) if args.import_original else read_art(locale)
        expected=build_svg(locale,art)
        if args.check:
            if target.read_text(encoding="utf-8") != expected:
                raise SystemExit(f"Regenerate {target.name}")
        else:
            target.write_text(expected,encoding="utf-8",newline="\n")
        if args.png:
            from PIL import Image

            with Image.open(io.BytesIO(art)) as image:
                image.save(target.with_suffix(".png"),format="PNG",optimize=True)
        print(locale,hashlib.sha256(art).hexdigest(),"checked" if args.check else "generated")


if __name__=="__main__":
    main()

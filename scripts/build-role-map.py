#!/usr/bin/env python3
"""Add restrained icon motion to the existing role illustrations, not new art."""
from __future__ import annotations

import argparse
import base64
import hashlib
from html import escape
import io
from pathlib import Path
from statistics import median
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "20dc3fb50e3cc605c28d1847701b467f7300e477"
NS = "{http://www.w3.org/2000/svg}"
LOCALES = {
    "zh-TW": ("", (1600, 900), "依需求選擇角色路線", "研究人員、開發者、教師、知識工作者與日常使用者：依需要選一條，不必全部走完。原圖文字與接線固定，只讓對應圖示輕動。"),
    "en": (".en", (1672, 941), "Choose a role path for your needs", "Researchers, developers, teachers, knowledge workers, and everyday users: choose what you need, not every path. Original labels and connections stay fixed; only the corresponding icons move gently."),
    "zh-Hans": (".zh-Hans", (1600, 900), "按需选择角色路线", "研究人员、开发者、教师、知识工作者与日常用户：按需选一条，不必全部走完。原图文字与连线固定，只让对应图标轻动。"),
}
SOURCE_HASHES = {
    "zh-TW": "3a20cc84ee4b3cb0d415e3f8cf8a2778a97ac7c92c72db7c8b44248338fec50c",
    "en": "b645d6dc7bc732f8896d3a0ec1144b82471b40d766328924c0835414b1ee4e6b",
    "zh-Hans": "d30fc7a7eef74ca41daf6b6d2d3170037ff47b53d4ce39f08033e395de3e1f42",
}
ART_HASHES = {
    "zh-TW": "8f92e57a66cee112a4453f810964d610fd1ded0c5aec125b01da4d3df4b147fb",
    "en": "e03fc937df4c0ce999ed3e5e6d7b9799c3114b6a2d5bf31235dec360f74937f8",
    "zh-Hans": "4d57bdff3c9c12d4bc856affa232019b2e952d3f02e3e93c5b364392ba230a98",
}
ROLES = ("research", "developer", "teacher", "knowledge", "everyday")
# Crops include a small paper margin, but never the adjacent labels or borders.
ICONS = {
    "zh-TW": [(146,446,81,90), (445,451,111,84), (748,453,102,81), (1059,450,84,84), (1363,464,96,66)],
    "en": [(139,428,91,108), (441,431,148,105), (768,433,127,103), (1096,432,107,100), (1416,445,120,84)],
    "zh-Hans": [(94,433,40,48), (420,435,46,48), (735,435,47,47), (992,435,43,47), (1311,436,46,44)],
}
# One meaningful gesture per role, one role at a time. 16–18 seconds is still.
POSES = (
    ((0, "rotate(0deg)"), (.35, "rotate(-5deg)"), (.7, "rotate(4deg)"), (1, "rotate(0deg)")),
    ((0, "scale(1)"), (.4, "scale(1.035)"), (1, "scale(1)")),
    ((0, "rotate(0deg)"), (.35, "rotate(-5deg)"), (.7, "rotate(4deg)"), (1, "rotate(0deg)")),
    ((0, "scaleY(1)"), (.3, "scaleY(.91)"), (.7, "scaleY(1.02)"), (1, "scaleY(1)")),
    ((0, "translateY(0px)"), (.4, "translateY(-3px)"), (1, "translateY(0px)")),
)


def percent(seconds):
    return f"{seconds / 18 * 100:.4f}%"


def animation_css():
    parts = [".role-layer{opacity:0;pointer-events:none}.role-motion{transform-origin:0 0}"]
    for index, (role, poses) in enumerate(zip(ROLES, POSES, strict=True)):
        start, end = 1 + index * 3, 3 + index * 3
        parts += [
            f".role-{role}{{animation:show-{role} 18s linear infinite}}",
            f".move-{role}{{animation:move-{role} 18s cubic-bezier(.25,1,.5,1) infinite}}",
            f"@keyframes show-{role}{{0%,{percent(start-.002)}{{opacity:0}}{percent(start)},"
            f"{percent(end)}{{opacity:1}}{percent(end+.002)},100%{{opacity:0}}}}",
            f"@keyframes move-{role}{{0%,100%{{transform:none}}" + "".join(
                f"{percent(start + (end-start)*p)}{{transform:{pose}}}" for p, pose in poses
            ) + "}",
        ]
    parts.append("@media(prefers-reduced-motion:reduce){.role-layer,.role-motion{animation:none!important}.role-layer{opacity:0!important}}")
    return "\n".join(parts)


def asset_path(locale, extension):
    return ROOT / f"resources/diagrams/branch-decision-tree{LOCALES[locale][0]}.{extension}"


def import_original(locale):
    from PIL import Image

    relative = asset_path(locale, "png").relative_to(ROOT).as_posix()
    data = subprocess.check_output(["git", "show", f"{SOURCE_COMMIT}:{relative}"], cwd=ROOT)
    if hashlib.sha256(data).hexdigest() != SOURCE_HASHES[locale]:
        raise ValueError(f"Unexpected source artwork: {locale}")
    with Image.open(io.BytesIO(data)) as source:
        if source.size != LOCALES[locale][1]:
            raise ValueError("Unexpected source canvas")
        output = io.BytesIO()
        source.save(output, format="WEBP", quality=95, method=6)
    return output.getvalue()


def read_art(locale):
    root = ET.fromstring(asset_path(locale, "svg").read_text(encoding="utf-8"))
    art = root.find(NS + "image")
    if art is None:
        raise ValueError("Missing original art")
    prefix, payload = art.attrib["href"].split(",", 1)
    if prefix != "data:image/webp;base64":
        raise ValueError("Expected embedded WebP")
    data = base64.b64decode(payload, validate=True)
    if hashlib.sha256(data).hexdigest() != ART_HASHES[locale]:
        raise ValueError(f"Changed original artwork: {locale}")
    return data


def build_svg(locale, art):
    from PIL import Image

    _, (width, height), title, description = LOCALES[locale]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" lang="{locale}" role="img" aria-labelledby="title desc">',
             f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>',
             f'<metadata>Original artwork: {SOURCE_COMMIT}; WebP quality 95; icon motion only. Existing localized labels preserved.</metadata>',
             f'<style>{animation_css()}</style>',
             f'<image id="original-art" width="{width}" height="{height}" href="data:image/webp;base64,{base64.b64encode(art).decode("ascii")}"/>']
    with Image.open(io.BytesIO(art)) as source:
        source = source.convert("RGB")
        for role, (x, y, w, h) in zip(ROLES, ICONS[locale], strict=True):
            corners = [source.getpixel(p) for p in ((x,y), (x+w-1,y), (x,y+h-1), (x+w-1,y+h-1))]
            paper = "#" + "".join(f"{int(median(c)):02x}" for c in zip(*corners))
            cx, cy = x+w/2, y+h if role == "knowledge" else y+h/2
            parts.append(f'<g id="role-{role}" class="role-layer role-{role}" aria-hidden="true">'
                f'<defs><clipPath id="clip-{role}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath></defs>'
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{paper}"/>'
                f'<g transform="translate({cx} {cy})"><g class="role-motion move-{role}">'
                f'<g transform="translate({-cx} {-cy})" clip-path="url(#clip-{role})"><use href="#original-art"/></g>'
                '</g></g></g>')
    return "\n".join(parts + ["</svg>"]) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locale", choices=LOCALES)
    parser.add_argument("--import-original", action="store_true")
    parser.add_argument("--png", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check and (args.import_original or args.png):
        parser.error("--check is read-only")
    for locale in [args.locale] if args.locale else LOCALES:
        art = import_original(locale) if args.import_original else read_art(locale)
        expected = build_svg(locale, art)
        path = asset_path(locale, "svg")
        if args.check:
            if path.read_text(encoding="utf-8") != expected:
                raise SystemExit(f"Regenerate {path.name}")
        else:
            path.write_text(expected, encoding="utf-8", newline="\n")
        if args.png:
            from PIL import Image
            with Image.open(io.BytesIO(art)) as source:
                source.save(asset_path(locale, "png"), format="PNG", optimize=True)
        print(locale, hashlib.sha256(art).hexdigest(), "checked" if args.check else "generated")


if __name__ == "__main__":
    main()

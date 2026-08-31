#!/usr/bin/env python3
"""Keep teaching diagrams within the site's current delivery budget.

This is a ratchet, not a claim that the current PNG set is already small.  A
future PR may lower the limits after replacing or compressing images.  Raising a
limit should require the PR to explain the measured reason.
"""
from __future__ import annotations

import argparse
import html as html_lib
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DIAGRAM_DIR = Path("resources/diagrams")
# Stage 1's required trilingual model-lifecycle diagram raises the audited
# baseline from 67 to 70 PNGs. The final visual-cleanup stack must lower both
# limits again after deleting obsolete diagram triplets; this is not free
# headroom for unrelated images.
MAX_PNG_COUNT = 70
MAX_TOTAL_BYTES = 86_700_000
MAX_SINGLE_BYTES = 1_550_000
MAX_PAGE_BYTES = 4_200_000
EXPECTED_RENDERED_DIAGRAMS = 75
EXPECTED_RENDERED_LAZY = 72
EXPECTED_RENDERED_EAGER = 3

IMAGE_LINK = re.compile(
    r"!\[[^\]]*\]\(\s*(?P<target><[^>\n]+>|[^)\s]+)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)"
)
IGNORED_PARTS = {".git", ".pytest_cache", "_build", "node_modules"}
HTML_IMAGE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
HTML_ANCHOR = re.compile(r"<a\b[^>]*>.*?</a>", re.IGNORECASE | re.DOTALL)
HTML_FIGURE = re.compile(
    r"<figure\b(?P<attrs>[^>]*)>(?P<body>.*?)</figure>",
    re.IGNORECASE | re.DOTALL,
)
HTML_FIGCAPTION = re.compile(
    r"<figcaption\b[^>]*>(?P<body>.*?)</figcaption>",
    re.IGNORECASE | re.DOTALL,
)
HTML_ATTRIBUTE = r"\s{0}\s*=\s*([\"'])(.*?)\1"
EAGER_BANNERS = {"banner.png", "banner.en.png", "banner.zh-Hans.png"}


@dataclass(frozen=True)
class DeliveryMetrics:
    png_count: int
    total_bytes: int
    largest_image: tuple[Path, int] | None
    heaviest_page: tuple[Path, int] | None


def _tracked_markdown(root: Path) -> list[Path]:
    proc = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return [root / line for line in proc.stdout.splitlines() if line]
    return [
        path
        for path in root.rglob("*.md")
        if not IGNORED_PARTS.intersection(path.relative_to(root).parts)
    ]


def _image_targets(markdown: str) -> list[str]:
    targets: list[str] = []
    for match in IMAGE_LINK.finditer(markdown):
        target = match.group("target").strip("<>")
        if target.startswith(("http://", "https://", "data:")):
            continue
        target = unquote(target.split("#", 1)[0])
        if target.lower().endswith(".png"):
            targets.append(target)
    return targets


def inspect_delivery(
    root: Path,
    *,
    markdown_paths: list[Path] | None = None,
) -> DeliveryMetrics:
    diagram_root = root / DIAGRAM_DIR
    pngs = sorted(diagram_root.glob("*.png"))
    sizes = [(path, path.stat().st_size) for path in pngs]

    page_sizes: list[tuple[Path, int]] = []
    for page in markdown_paths or _tracked_markdown(root):
        if not page.is_file():
            continue
        targets: set[Path] = set()
        for target in _image_targets(page.read_text(encoding="utf-8")):
            resolved = (page.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                continue
            if resolved.is_file() and resolved.suffix.lower() == ".png":
                targets.add(resolved)
        page_sizes.append((page, sum(path.stat().st_size for path in targets)))

    return DeliveryMetrics(
        png_count=len(pngs),
        total_bytes=sum(size for _, size in sizes),
        largest_image=max(sizes, key=lambda item: item[1], default=None),
        heaviest_page=max(page_sizes, key=lambda item: item[1], default=None),
    )


def check_delivery(
    root: Path,
    *,
    markdown_paths: list[Path] | None = None,
    max_png_count: int = MAX_PNG_COUNT,
    max_total_bytes: int = MAX_TOTAL_BYTES,
    max_single_bytes: int = MAX_SINGLE_BYTES,
    max_page_bytes: int = MAX_PAGE_BYTES,
) -> tuple[DeliveryMetrics, list[str]]:
    metrics = inspect_delivery(root, markdown_paths=markdown_paths)
    errors: list[str] = []
    if metrics.png_count > max_png_count:
        errors.append(f"PNG count {metrics.png_count} exceeds {max_png_count}")
    if metrics.total_bytes > max_total_bytes:
        errors.append(
            f"diagram bytes {metrics.total_bytes} exceed {max_total_bytes}"
        )
    if metrics.largest_image and metrics.largest_image[1] > max_single_bytes:
        path, size = metrics.largest_image
        errors.append(
            f"single image {path.relative_to(root)} is {size} bytes; limit {max_single_bytes}"
        )
    if metrics.heaviest_page and metrics.heaviest_page[1] > max_page_bytes:
        path, size = metrics.heaviest_page
        errors.append(
            f"page {path.relative_to(root)} references {size} image bytes; limit {max_page_bytes}"
        )
    return metrics, errors


def _html_attribute(tag: str, name: str) -> str | None:
    match = re.search(HTML_ATTRIBUTE.format(re.escape(name)), tag, re.IGNORECASE)
    return match.group(2) if match else None


def _class_tokens(tag: str) -> set[str]:
    return set((_html_attribute(tag, "class") or "").split())


def _is_local_diagram(src: str) -> bool:
    parsed = urlsplit(html_lib.unescape(src))
    if parsed.scheme or parsed.netloc:
        return False
    path = parsed.path.replace("\\", "/").lstrip("./")
    return path.startswith(("diagrams/", "resources/diagrams/")) or any(
        marker in f"/{path}" for marker in ("/diagrams/", "/resources/diagrams/")
    )


def _diagram_basename(src: str) -> str:
    return unquote(urlsplit(html_lib.unescape(src)).path).rsplit("/", 1)[-1]


def _valid_new_tab_link(tag: str, expected_href: str) -> bool:
    rel = set((_html_attribute(tag, "rel") or "").lower().split())
    return (
        _html_attribute(tag, "href") == expected_href
        and (_html_attribute(tag, "target") or "").lower() == "_blank"
        and "noopener" in rel
    )


def check_built_site(
    site_dir: Path,
    *,
    expected_diagrams: int = EXPECTED_RENDERED_DIAGRAMS,
    expected_lazy: int = EXPECTED_RENDERED_LAZY,
    expected_eager: int = EXPECTED_RENDERED_EAGER,
) -> tuple[dict[str, int], list[str]]:
    """Verify that the rendered site kept the hook's delivery contract."""

    counts = {
        "diagrams": 0,
        "lazy": 0,
        "async": 0,
        "eager": 0,
        "figures": 0,
        "image_links": 0,
        "caption_links": 0,
    }
    errors: list[str] = []
    if not site_dir.is_dir():
        return counts, [f"built site directory does not exist: {site_dir}"]
    pages = sorted(site_dir.rglob("*.html"))
    if not pages:
        return counts, [f"built site contains no HTML pages: {site_dir}"]

    for page in pages:
        source = page.read_text(encoding="utf-8")
        for tag in HTML_IMAGE.findall(source):
            src = _html_attribute(tag, "src") or ""
            if not _is_local_diagram(src):
                continue
            counts["diagrams"] += 1
            basename = _diagram_basename(src)
            loading = _html_attribute(tag, "loading")
            decoding = _html_attribute(tag, "decoding")
            if decoding == "async":
                counts["async"] += 1
            else:
                errors.append(f"{page}: diagram lacks decoding=async: {src}")
            if basename in EAGER_BANNERS:
                counts["eager"] += 1
                if loading == "lazy":
                    errors.append(f"{page}: above-fold banner must stay eager: {src}")
            elif loading == "lazy":
                counts["lazy"] += 1
            else:
                errors.append(f"{page}: diagram lacks loading=lazy: {src}")

        for figure in HTML_FIGURE.finditer(source):
            open_tag = f"<figure{figure.group('attrs')}>"
            if "aaz-diagram" not in _class_tokens(open_tag):
                continue
            counts["figures"] += 1
            body = figure.group("body")
            diagram_images = [
                tag
                for tag in HTML_IMAGE.findall(body)
                if _is_local_diagram(_html_attribute(tag, "src") or "")
            ]
            if len(diagram_images) != 1:
                errors.append(
                    f"{page}: aaz-diagram figure must contain exactly one local diagram"
                )
                continue
            src = _html_attribute(diagram_images[0], "src") or ""
            image_links = [
                tag
                for tag in HTML_ANCHOR.findall(body)
                if "aaz-diagram__image-link" in _class_tokens(tag)
            ]
            if len(image_links) != 1 or not _valid_new_tab_link(image_links[0], src):
                errors.append(
                    f"{page}: image link must match {src} and use target=_blank rel=noopener"
                )
            else:
                counts["image_links"] += 1

            caption = HTML_FIGCAPTION.search(body)
            caption_links = HTML_ANCHOR.findall(caption.group("body")) if caption else []
            if len(caption_links) != 1 or not _valid_new_tab_link(
                caption_links[0], src
            ):
                errors.append(
                    f"{page}: caption link must match {src} and use target=_blank rel=noopener"
                )
            else:
                counts["caption_links"] += 1

    expected_figures = counts["diagrams"] - counts["eager"]
    for name in ("figures", "image_links", "caption_links"):
        if counts[name] != expected_figures:
            errors.append(
                f"{name} {counts[name]} do not cover {expected_figures} non-banner diagrams"
            )
    expected_counts = {
        "diagrams": expected_diagrams,
        "lazy": expected_lazy,
        "async": expected_diagrams,
        "eager": expected_eager,
        "figures": expected_lazy,
        "image_links": expected_lazy,
        "caption_links": expected_lazy,
    }
    for name, expected in expected_counts.items():
        if counts[name] != expected:
            errors.append(
                f"rendered {name} count {counts[name]} differs from expected {expected}"
            )
    return counts, errors


def _mib(value: int) -> str:
    return f"{value / 1024 / 1024:.2f} MiB"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site",
        type=Path,
        help="also validate a built MkDocs site, for example _build/site",
    )
    args = parser.parse_args(argv)
    metrics, errors = check_delivery(ROOT)
    largest = metrics.largest_image or (Path("-"), 0)
    heaviest = metrics.heaviest_page or (Path("-"), 0)
    print(
        f"diagrams={metrics.png_count} total={_mib(metrics.total_bytes)} "
        f"largest={largest[0].name}:{_mib(largest[1])} "
        f"heaviest_page={heaviest[0].relative_to(ROOT)}:{_mib(heaviest[1])}"
    )
    if args.site:
        counts, built_errors = check_built_site(args.site)
        errors.extend(built_errors)
        print(
            "built_site "
            + " ".join(f"{name}={value}" for name, value in counts.items())
        )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("image delivery budget: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

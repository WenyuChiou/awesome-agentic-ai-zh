"""mkdocs build hooks for the awesome-agentic-ai-zh docs site.

Strips the hand-written GitHub-style language switcher from the
README pages when rendered by mkdocs.

Why: README.md / README.en.md / README.zh-Hans.md open with a
``<div align="right"> 繁體中文 | 简体中文 | English </div>`` block
whose links point at the *raw* sibling files (`./README.zh-Hans.md`
…). That is correct for GitHub file browsing, but on the rendered
mkdocs site those `.md` paths 404 (mkdocs builds them into
pages/dirs, and the block is raw HTML so mkdocs does not rewrite the
links). The site already has the proper in-site language selector
in the Material header (populated by mkdocs-static-i18n's
`extra.alternate`), so the inline block is both redundant and
broken there.

This hook removes ONLY the first ``<div align="right">…</div>``
block, and ONLY on the three README pages — so the GitHub-rendered
README is completely untouched (hooks run at mkdocs build time
only), and no tri-locale content edit is needed.
"""
from __future__ import annotations

import html as html_lib
import re
from urllib.parse import urlsplit

# The switcher is always the very first element of the README; the
# banner that follows is <div align="center"> (different), so a
# non-greedy first-match on align="right" is safe.
#
# Smoke test (local):
#   python scripts/build-docs-tree.py && python -m mkdocs build
#   grep -c 'align="right"' _build/site/index.html   # expect 0
# If the README switcher markup ever changes (e.g. gains a NESTED
# <div>, or becomes <p align="right">), this non-greedy pattern would
# stop at the inner </div> / not match — update it then. Failure mode
# is benign: the old (broken-on-site) switcher reappears, no build break.
_SWITCHER = re.compile(r'<div align="right">.*?</div>\s*', re.DOTALL)
# The root README is staged as `about.md` (see build-docs-tree.py), so the
# switcher-strip now targets the renamed page.
_ABOUT_BASENAMES = {"about.md", "about.en.md", "about.zh-Hans.md"}

# Rewrite in-content links to the root README (now `about.md`) -> about, so
# they resolve on the site. A leading `examples/` breaks the `(?:\.\./)*`
# prefix match, so examples/.../README.md links are left untouched.
_README_LINK = re.compile(r'(\]\((?:\.\./)*)README((?:\.en|\.zh-Hans)?\.md)')

# Markdown renders a standalone image as ``<p><img ...></p>``.  Diagram text is
# intentionally kept in the PNG so GitHub and the docs site show the same visual,
# but that also means a phone needs an obvious way to open the original pixels.
# Enhance only our teaching diagrams: badges, contributor images, sponsor buttons,
# and other external images must keep their existing links and loading behaviour.
_DIAGRAM_PARAGRAPH = re.compile(
    r'<p>\s*(?P<img><img\b[^>]*\bsrc=(?P<quote>["\'])'
    r'(?P<src>[^"\']*(?:resources/)?diagrams/[^"\']+)(?P=quote)[^>]*>)\s*</p>',
    re.IGNORECASE,
)
_DIAGRAM_IMAGE = re.compile(
    r'<img\b[^>]*\bsrc=(?P<quote>["\'])'
    r'(?P<src>[^"\']*(?:resources/)?diagrams/[^"\']+)(?P=quote)[^>]*>',
    re.IGNORECASE,
)
_ATTR = r'\s{0}\s*=\s*(["\'])(.*?)\1'
_EAGER_DIAGRAMS = {"banner.png", "banner.en.png", "banner.zh-Hans.png"}
_FULL_SIZE_LABELS = {
    "zh-TW": "開啟原圖（新分頁）",
    "en": "Open full-size image (new tab)",
    "zh-Hans": "打开原图（新标签页）",
}


def _attribute(tag: str, name: str) -> str | None:
    match = re.search(_ATTR.format(re.escape(name)), tag, re.IGNORECASE)
    return html_lib.unescape(match.group(2)) if match else None


def _add_attribute(tag: str, name: str, value: str) -> str:
    if _attribute(tag, name) is not None:
        return tag
    stripped = tag.rstrip()
    suffix = "/>" if stripped.endswith("/>") else ">"
    core = stripped[: -len(suffix)].rstrip()
    return f'{core} {name}="{html_lib.escape(value, quote=True)}"{suffix}'


def _enhance_image(tag: str, src: str) -> str:
    tag = _add_attribute(tag, "decoding", "async")
    if src.rsplit("/", 1)[-1] not in _EAGER_DIAGRAMS:
        tag = _add_attribute(tag, "loading", "lazy")
    return tag


def _is_local_diagram(src: str) -> bool:
    """Return true only for a repository-local teaching diagram URL."""

    parsed = urlsplit(html_lib.unescape(src))
    if parsed.scheme or parsed.netloc:
        return False
    path = parsed.path.replace("\\", "/").lstrip("./")
    return path.startswith(("diagrams/", "resources/diagrams/")) or any(
        marker in f"/{path}" for marker in ("/diagrams/", "/resources/diagrams/")
    )


def _locale_for(src_path: str) -> str:
    if src_path.endswith(".zh-Hans.md"):
        return "zh-Hans"
    if src_path.endswith(".en.md"):
        return "en"
    return "zh-TW"


def enhance_diagram_html(content: str, *, locale: str) -> str:
    """Add lightweight delivery and a keyboard-accessible original-image link."""

    label = _FULL_SIZE_LABELS.get(locale, _FULL_SIZE_LABELS["zh-TW"])

    def replace_paragraph(match: re.Match[str]) -> str:
        src = match.group("src")
        if not _is_local_diagram(src):
            return match.group(0)
        image = _enhance_image(match.group("img"), src)
        if src.rsplit("/", 1)[-1] in _EAGER_DIAGRAMS:
            return f"<p>{image}</p>"

        alt = _attribute(image, "alt") or "diagram"
        aria_label = html_lib.escape(f"{label}: {alt}", quote=True)
        return (
            '<figure class="aaz-diagram">\n'
            f'<a class="aaz-diagram__image-link" href="{src}" target="_blank" '
            f'rel="noopener" aria-label="{aria_label}">{image}</a>\n'
            '<figcaption class="aaz-diagram__caption">'
            f'<a href="{src}" target="_blank" rel="noopener">{label}</a>'
            "</figcaption>\n"
            "</figure>"
        )

    content = _DIAGRAM_PARAGRAPH.sub(replace_paragraph, content)

    # A diagram nested inside a list or custom HTML block cannot safely receive
    # a figure wrapper. It still gets delivery attributes, but the rendered-site
    # gate rejects this source shape so authors move it to a standalone paragraph
    # and every teaching diagram keeps the same full-size-link experience.
    def enhance_remaining(match: re.Match[str]) -> str:
        src = match.group("src")
        if not _is_local_diagram(src):
            return match.group(0)
        return _enhance_image(match.group(0), src)

    return _DIAGRAM_IMAGE.sub(enhance_remaining, content)


def on_page_markdown(markdown: str, *, page, config, files) -> str:
    src = (getattr(page.file, "src_path", "") or "").replace("\\", "/")
    basename = src.rsplit("/", 1)[-1]
    markdown = _README_LINK.sub(r"\1about\2", markdown)
    if basename in _ABOUT_BASENAMES:
        markdown = _SWITCHER.sub("", markdown, count=1)
    return markdown


def on_page_content(html: str, *, page, config, files) -> str:
    src = (getattr(page.file, "src_path", "") or "").replace("\\", "/")
    return enhance_diagram_html(html, locale=_locale_for(src))

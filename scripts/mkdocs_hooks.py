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
import posixpath
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
_LANGUAGE_SWITCHER_LINE = re.compile(
    r"(?m)^(?:>\s*)?(?:🌐\s*)?(?=[^\n]*\|)"
    r"(?=[^\n]*(?:繁體中文|繁中|Traditional Chinese|zh-TW))"
    r"(?=[^\n]*(?:简体中文|简中|Simplified Chinese|zh-Hans))"
    r"(?=[^\n]*(?:English|\bEN\b))(?=[^\n]*\.md(?:[)#\s|]|$))"
    r"[^\n]*\n?"
)

# Rewrite in-content links to the root README (now `about.md`) -> about, so
# they resolve on the site. A leading `examples/` breaks the `(?:\.\./)*`
# prefix match, so examples/.../README.md links are left untouched.
_README_LINK = re.compile(r'(\]\((?:\.\./)*)README((?:\.en|\.zh-Hans)?\.md)')
_HTML_LINK = re.compile(
    r'(?P<prefix><a\b[^>]*?\bhref\s*=\s*)(?P<quote>["\'])'
    r'(?P<href>[^"\']+)(?P=quote)',
    re.IGNORECASE,
)
_GITHUB_BLOB_ROOT = "https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/"
_THEME_SEARCH_SHARE = re.compile(
    r'(<a\b(?=[^>]*\bdata-md-component=["\']search-share["\'])'
    r'[^>]*?\bhref\s*=\s*)(["\'])javascript:void\(0\)\2',
    re.IGNORECASE,
)

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


def _locale_for_page(src_path: str, page_url: str) -> str:
    normalized = page_url.replace("\\", "/").lstrip("./")
    if normalized.startswith("zh-Hans/"):
        return "zh-Hans"
    if normalized.startswith("en/"):
        return "en"
    return _locale_for(src_path)


def _strip_locale_suffix(path: str) -> tuple[str, str]:
    for suffix, locale in (
        (".zh-Hans.md", "zh-Hans"),
        (".en.md", "en"),
        (".md", "zh-TW"),
    ):
        if path.endswith(suffix):
            return path[: -len(suffix)], locale
    raise ValueError(f"not a Markdown page: {path}")


def _site_path_for_source(src_path: str, *, locale: str | None = None) -> str:
    """Map a staged source filename to its locale-aware clean site path."""

    stem, source_locale = _strip_locale_suffix(src_path.replace("\\", "/"))
    chosen_locale = locale or source_locale
    if stem == "README":
        stem = "about"
    elif stem.endswith("/README"):
        stem = stem[: -len("/README")]
    elif stem == "index":
        stem = ""
    prefix = "" if chosen_locale == "zh-TW" else f"{chosen_locale}/"
    return f"{prefix}{stem.strip('/')}/" if stem else prefix


def strip_github_language_switcher(markdown: str) -> str:
    """Remove the source-browser locale row from the rendered-site copy."""

    head, tail = markdown[:1200], markdown[1200:]
    head = _SWITCHER.sub("", head, count=1)
    head = _LANGUAGE_SWITCHER_LINE.sub("", head, count=1)
    return head + tail


def _repo_source_path(src_path: str) -> str:
    normalized = src_path.replace("\\", "/")
    return "README.md" if normalized == "about.md" else normalized


def _resolve_source_target(src_path: str, href_path: str) -> str:
    source = _repo_source_path(src_path)
    target = posixpath.normpath(posixpath.join(posixpath.dirname(source), href_path))
    if src_path.startswith("about") and posixpath.basename(target).startswith("about"):
        target = posixpath.join(
            posixpath.dirname(target),
            posixpath.basename(target).replace("about", "README", 1),
        )
    return target


def _is_public_markdown(path: str) -> bool:
    normalized = path.replace("\\", "/")
    if normalized == "docs/HOW_TO_USE.md":
        return True
    if normalized.startswith("docs/"):
        return False
    if normalized.startswith("examples/"):
        return posixpath.basename(normalized).startswith("README")
    return normalized.startswith(
        ("stages/", "tracks/", "branches/", "resources/", "walkthroughs/")
    ) or "/" not in normalized


def rewrite_local_html_links(
    content: str,
    *,
    src_path: str,
    page_url: str,
    repo_root=None,
) -> str:
    """Turn raw-HTML source links into working site or GitHub links.

    Markdown processors rewrite normal Markdown links, but links inside HTML
    resource tables are left untouched.  Their file-style paths therefore land
    one directory too deep on the clean-URL site.  Resolve those links using the
    source file's directory, then emit a clean locale URL.  Repository files that
    are intentionally not published as lessons point to GitHub instead.
    """

    from pathlib import Path
    # Keep image-only hook tests stdlib-only; MkDocs is guaranteed when this
    # site-link rewrite actually runs during a documentation build.
    from mkdocs.utils import get_relative_url

    root = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parent.parent
    source_locale = _locale_for_page(src_path, page_url)

    def replace(match: re.Match[str]) -> str:
        href = html_lib.unescape(match.group("href"))
        parsed = urlsplit(href)
        if (
            parsed.scheme
            or parsed.netloc
            or href.startswith(("#", "/", "mailto:", "tel:", "javascript:"))
            or not parsed.path
        ):
            return match.group(0)

        target = _resolve_source_target(src_path, parsed.path)
        repo_target = root / target
        target_source: str | None = None
        target_locale = source_locale

        if parsed.path.endswith(".md"):
            candidate = target
            if candidate == "README.md":
                candidate = "about.md"
            staged_candidate = root / candidate
            if staged_candidate.is_file() and _is_public_markdown(candidate):
                target_source = candidate
                target_locale = _locale_for(candidate)
            else:
                # Some canonical pages intentionally have no translated source.
                # MkDocs still publishes the canonical page below every locale,
                # so a localized source link must fall back to that clean route.
                try:
                    canonical_stem, _ = _strip_locale_suffix(candidate)
                except ValueError:
                    canonical_candidate = ""
                else:
                    canonical_candidate = f"{canonical_stem}.md"
                if canonical_candidate:
                    canonical_file = root / canonical_candidate
                    if canonical_file.is_file() and _is_public_markdown(canonical_candidate):
                        target_source = canonical_candidate
                        target_locale = source_locale
        elif repo_target.is_dir():
            locale_suffix = {"zh-TW": "", "en": ".en", "zh-Hans": ".zh-Hans"}[source_locale]
            localized_readme = repo_target / f"README{locale_suffix}.md"
            canonical_readme = repo_target / "README.md"
            chosen = localized_readme if localized_readme.is_file() else canonical_readme
            if chosen.is_file():
                target_source = chosen.relative_to(root).as_posix()

        if target_source is not None:
            clean_target = _site_path_for_source(target_source, locale=target_locale)
            rewritten = get_relative_url(clean_target, page_url)
            if parsed.query:
                rewritten += f"?{parsed.query}"
            if parsed.fragment:
                rewritten += f"#{parsed.fragment}"
        elif repo_target.is_file():
            rewritten = _GITHUB_BLOB_ROOT + repo_target.relative_to(root).as_posix()
            if parsed.fragment:
                rewritten += f"#{parsed.fragment}"
        else:
            return match.group(0)

        quote = match.group("quote")
        escaped = html_lib.escape(rewritten, quote=True)
        return f'{match.group("prefix")}{quote}{escaped}{quote}'

    return _HTML_LINK.sub(replace, content)


def add_locale_metadata(
    output: str, *, src_path: str, site_url: str, page_url: str = ""
) -> str:
    """Set exact BCP-47 language metadata and head alternates."""

    locale = _locale_for_page(src_path, page_url)
    output = re.sub(
        r'<html\s+lang="[^"]+"',
        f'<html lang="{locale}"',
        output,
        count=1,
    )
    if 'rel="alternate"' in output.split("</head>", 1)[0]:
        return output

    base = site_url.rstrip("/") + "/"
    neutral_stem, _ = _strip_locale_suffix(src_path.replace("\\", "/"))
    canonical_source = f"{neutral_stem}.md"
    links = []
    for lang in ("zh-TW", "zh-Hans", "en"):
        url = base + _site_path_for_source(canonical_source, locale=lang)
        links.append(f'<link rel="alternate" hreflang="{lang}" href="{url}">')
    links.append(
        f'<link rel="alternate" hreflang="x-default" '
        f'href="{base + _site_path_for_source(canonical_source, locale="zh-TW")}">'
    )
    return output.replace("</head>", "\n    " + "\n    ".join(links) + "\n  </head>", 1)


def sanitize_theme_placeholders(output: str) -> str:
    """Replace Material's one known active-scheme placeholder with a fragment.

    The rendered-site audit rejects every ``javascript:`` URL.  Material emits
    one for its search-share control, so normalize only that component; an
    author-supplied active URL remains visible to the audit and fails the gate.
    """

    return _THEME_SEARCH_SHARE.sub(r"\1\2#\2", output)


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
    del basename, config, files
    return strip_github_language_switcher(markdown)


def on_page_content(html: str, *, page, config, files) -> str:
    src = (getattr(page.file, "src_path", "") or "").replace("\\", "/")
    del config, files
    html = rewrite_local_html_links(html, src_path=src, page_url=page.url)
    return enhance_diagram_html(html, locale=_locale_for_page(src, page.url))


def on_post_page(output: str, *, page, config) -> str:
    src = (getattr(page.file, "src_path", "") or "").replace("\\", "/")
    output = sanitize_theme_placeholders(output)
    return add_locale_metadata(
        output, src_path=src, site_url=config.site_url, page_url=page.url
    )

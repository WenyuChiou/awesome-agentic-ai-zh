"""Regression tests for the diagram delivery hook and size ratchet."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from tempfile import TemporaryDirectory


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


delivery = _load("check_image_delivery", "check-image-delivery.py")
hooks = _load("mkdocs_hooks", "mkdocs_hooks.py")
ROOT = Path(__file__).resolve().parents[1]


def test_current_repository_stays_inside_the_delivery_ratchet() -> None:
    metrics, errors = delivery.check_delivery(ROOT)
    assert not errors
    assert metrics.png_count == 70
    assert metrics.largest_image is not None
    assert metrics.heaviest_page is not None


def test_budget_checker_reports_image_and_page_regressions() -> None:
    with TemporaryDirectory() as directory:
        tmp_path = Path(directory)
        diagrams = tmp_path / "resources" / "diagrams"
        diagrams.mkdir(parents=True)
        (diagrams / "a.png").write_bytes(b"a" * 11)
        (diagrams / "b.png").write_bytes(b"b" * 11)
        page = tmp_path / "stage.md"
        page.write_text(
            "![A](resources/diagrams/a.png)\n![B](resources/diagrams/b.png)\n",
            encoding="utf-8",
        )

        metrics, errors = delivery.check_delivery(
            tmp_path,
            markdown_paths=[page],
            max_png_count=1,
            max_total_bytes=20,
            max_single_bytes=10,
            max_page_bytes=20,
        )

    assert metrics.png_count == 2
    assert any("PNG count" in error for error in errors)
    assert any("diagram bytes" in error for error in errors)
    assert any("single image" in error for error in errors)
    assert any("page stage.md" in error for error in errors)


def test_built_site_checker_requires_delivery_attributes_and_full_size_links(
) -> None:
    with TemporaryDirectory() as directory:
        tmp_path = Path(directory)
        page = tmp_path / "index.html"
        page.write_text(
            '<figure class="aaz-diagram">'
            '<a class="aaz-diagram__image-link" href="../diagrams/a.png" '
            'target="_blank" rel="noopener"><img src="../diagrams/a.png" '
            'loading="lazy" decoding="async"></a>'
            '<figcaption class="aaz-diagram__caption">'
            '<a href="../diagrams/a.png" target="_blank" rel="noopener">Open</a>'
            '</figcaption></figure>'
            '<img src="../resources/diagrams/banner.png" decoding="async">',
            encoding="utf-8",
        )
        counts, errors = delivery.check_built_site(
            tmp_path, expected_diagrams=2, expected_lazy=1, expected_eager=1
        )
        assert not errors
        assert counts == {
            "diagrams": 2,
            "lazy": 1,
            "async": 2,
            "eager": 1,
            "figures": 1,
            "image_links": 1,
            "caption_links": 1,
        }

        page.write_text(
            '<img src="../diagrams/a.png"><img src="../diagrams/b.png" '
            'loading="lazy" decoding="async">',
            encoding="utf-8",
        )
        _, errors = delivery.check_built_site(
            tmp_path, expected_diagrams=2, expected_lazy=2, expected_eager=0
        )
    assert any("lacks decoding=async" in error for error in errors)
    assert any("lacks loading=lazy" in error for error in errors)
    assert any("figures" in error for error in errors)


def test_built_site_checker_fails_closed_for_missing_empty_and_broken_links() -> None:
    with TemporaryDirectory() as directory:
        tmp_path = Path(directory)
        _, errors = delivery.check_built_site(tmp_path / "missing")
        assert any("does not exist" in error for error in errors)

        empty = tmp_path / "empty"
        empty.mkdir()
        _, errors = delivery.check_built_site(empty)
        assert any("no HTML pages" in error for error in errors)

        page = tmp_path / "index.html"
        page.write_text(
            '<figure class="aaz-diagram">'
            '<a class="aaz-diagram__image-link" href="wrong.png">'
            '<img src="../diagrams/a.png" loading="lazy" decoding="async"></a>'
            '<figcaption><a href="../diagrams/a.png">Open</a></figcaption>'
            '</figure>',
            encoding="utf-8",
        )
        _, errors = delivery.check_built_site(
            tmp_path, expected_diagrams=1, expected_lazy=1, expected_eager=0
        )
    assert any("image link must match" in error for error in errors)
    assert any("caption link must match" in error for error in errors)


def test_diagram_hook_adds_lazy_async_and_localized_full_size_link() -> None:
    source = (
        '<p><img alt="A &amp; B" '
        'src="../resources/diagrams/example.en.png" /></p>'
    )
    rendered = hooks.enhance_diagram_html(source, locale="en")

    assert rendered.count('loading="lazy"') == 1
    assert rendered.count('decoding="async"') == 1
    assert 'class="aaz-diagram"' in rendered
    assert "Open full-size image (new tab)" in rendered
    assert 'aria-label="Open full-size image (new tab): A &amp; B"' in rendered
    assert rendered.count('rel="noopener"') == 2

    # Re-running a hook must not duplicate delivery attributes.
    rerendered = hooks.enhance_diagram_html(rendered, locale="en")
    assert rerendered.count('loading="lazy"') == 1
    assert rerendered.count('decoding="async"') == 1


def test_banner_stays_eager_and_external_images_are_untouched() -> None:
    banner = (
        '<p><img alt="Banner" '
        'src="resources/diagrams/banner.zh-Hans.png" /></p>'
    )
    rendered = hooks.enhance_diagram_html(banner, locale="zh-Hans")
    assert 'decoding="async"' in rendered
    assert 'loading="lazy"' not in rendered
    assert "打开原图" not in rendered

    external = '<p><img alt="Badge" src="https://example.com/badge.png" /></p>'
    assert hooks.enhance_diagram_html(external, locale="zh-TW") == external
    external_diagram = (
        '<p><img alt="Remote" src="https://example.com/diagrams/x.png" /></p>'
    )
    assert (
        hooks.enhance_diagram_html(external_diagram, locale="zh-TW")
        == external_diagram
    )


def test_full_size_labels_match_all_three_locales() -> None:
    source = '<p><img alt="X" src="../resources/diagrams/x.png"></p>'
    assert "開啟原圖（新分頁）" in hooks.enhance_diagram_html(source, locale="zh-TW")
    assert "Open full-size image (new tab)" in hooks.enhance_diagram_html(
        source, locale="en"
    )
    assert "打开原图（新标签页）" in hooks.enhance_diagram_html(
        source, locale="zh-Hans"
    )

    # Pages already inside resources/ render the same asset as ../diagrams/.
    resource_page = '<p><img alt="X" src="../diagrams/x.png"></p>'
    assert 'loading="lazy"' in hooks.enhance_diagram_html(
        resource_page, locale="zh-TW"
    )


def _run_all() -> None:
    test_current_repository_stays_inside_the_delivery_ratchet()
    test_budget_checker_reports_image_and_page_regressions()
    test_built_site_checker_requires_delivery_attributes_and_full_size_links()
    test_built_site_checker_fails_closed_for_missing_empty_and_broken_links()
    test_diagram_hook_adds_lazy_async_and_localized_full_size_link()
    test_banner_stays_eager_and_external_images_are_untouched()
    test_full_size_labels_match_all_three_locales()
    print("image delivery tests: OK")


if __name__ == "__main__":
    _run_all()

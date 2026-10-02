from __future__ import annotations

import importlib.util
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest


SCRIPT = Path(__file__).with_name("release_manifest.py")
SPEC = importlib.util.spec_from_file_location("release_manifest", SCRIPT)
rm = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(rm)


def test_calendar_version_contract() -> None:
    assert rm.validate_version("v2026.08.31", today=date(2026, 8, 31)) == date(2026, 8, 31)
    assert rm.validate_version("v2026.08.31-2", today=date(2026, 9, 1)) == date(2026, 8, 31)
    for bad in ("2026.08.31", "v2026.08.31-1", "v2026.02.30", "v2026.09.01"):
        with pytest.raises(rm.ReleaseManifestError):
            rm.validate_version(bad, today=date(2026, 8, 31))


def test_page_manifest_has_one_ordered_trilingual_source() -> None:
    manifest = rm.validate_pages_manifest(strict_urls=True)
    assert len(manifest["pages"]) == 28
    assert [row["id"] for row in manifest["pages"][:3]] == ["readme", "stage-00", "stage-01"]
    assert set(manifest["pages"][-1]["localized"]) == set(rm.LOCALES)
    assert rm.REQUIRED_PAGE_IDS <= {row["id"] for row in manifest["pages"]}
    for locale in rm.LOCALES:
        markers = [page["body_markers"][locale] for page in manifest["pages"]]
        assert len(markers) == len(set(markers)) == 28
        for page in manifest["pages"]:
            marker = page["body_markers"][locale]
            other_sources = [
                (rm.ROOT / other["localized"][locale]).read_text(encoding="utf-8")
                for other in manifest["pages"]
                if other["id"] != page["id"]
            ]
            assert all(marker not in rm._heading_key(source) for source in other_sources)


def test_release_notes_are_trilingual_mirrors() -> None:
    manifest = rm.validate_notes_manifest()
    rendered = rm.render_notes(
        manifest["release_version"], sha="0123456789abcdef0123456789abcdef01234567"
    )
    assert rendered.index("## 繁體中文") < rendered.index("## 简体中文") < rendered.index("## English")
    assert rendered.count("- `") == len(manifest["changes"]) * 3
    for change in manifest["changes"]:
        for locale in rm.LOCALES:
            assert change[locale] in rendered
    link_counts = Counter(link for change in manifest["changes"] for link in change["links"])
    for link, count in link_counts.items():
        assert rendered.count(f"]({link})") == count * len(rm.LOCALES)


def test_validate_version_uses_utc_date(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[object] = []

    class FixedUtcDateTime:
        @staticmethod
        def now(tz: object) -> object:
            calls.append(tz)
            return datetime(2026, 9, 8, 0, 5, tzinfo=rm.UTC)

    monkeypatch.setattr(rm, "datetime", FixedUtcDateTime)
    assert rm.validate_version("v2026.09.08") == date(2026, 9, 8)
    assert calls == [rm.UTC]


def test_release_notes_reject_a_different_dispatch_version() -> None:
    with pytest.raises(rm.ReleaseManifestError, match="not requested version"):
        rm.validate_notes_manifest(expected_version="v2026.08.31-2")


def test_assembled_pdf_source_expands_secondary_details() -> None:
    assembled = rm.assemble_markdown("zh-TW", "v2026.08.31")
    assert assembled.count("<!-- release-page:") == 28
    assert "<details" not in assembled.lower()
    assert "<summary" not in assembled.lower()
    assert '<div class="release-cover">' in assembled
    assert 'pagetitle: "awesome-agentic-ai-zh — AI Agent 學習地圖 — v2026.08.31"' in assembled
    assert '<div class="release-page-break"></div>' in assembled
    assert "https://img.shields.io/" not in assembled
    assert "https://contrib.rocks/image" not in assembled


def test_asset_names_are_exact_and_locale_specific() -> None:
    assert rm.asset_name("v2026.08.31", "zh-TW") == "awesome-agentic-ai-zh-v2026.08.31-zh-TW.pdf"
    assert rm.asset_name("v2026.08.31-2", "zh-Hans") == "awesome-agentic-ai-zh-v2026.08.31-2-zh-Hans.pdf"
    assert rm.asset_name("v2026.08.31", "en") == "awesome-agentic-ai-zh-v2026.08.31-en.pdf"


def test_pdf_table_text_keeps_whole_words() -> None:
    css = (rm.ROOT / "release" / "pdf.css").read_text(encoding="utf-8")
    header_rule = re.search(r"(?sm)^th \{(.*?)^\}", css)
    cell_rule = re.search(r"(?sm)^td \{(.*?)^\}", css)
    assert header_rule is not None
    assert "hyphens: none" in header_rule.group(1)
    assert "overflow-wrap: normal" in header_rule.group(1)
    assert "word-break: normal" in header_rule.group(1)
    assert cell_rule is not None
    assert "hyphens: none" in cell_rule.group(1)
    assert "overflow-wrap: normal" in cell_rule.group(1)
    assert "word-break: normal" in cell_rule.group(1)


def test_heading_normalization_never_swallows_across_pdf_lines() -> None:
    text = "unmatched [ and < symbols\nStage 5 — Claude Code Ecosystem\nlater ](text) and >"
    assert "stage5claudecodeecosystem" in rm._heading_key(text)


def test_pdf_validator_checks_every_heading_and_all_three_assets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = rm.validate_pages_manifest()
    extracted: dict[str, bytes] = {}
    for locale in rm.LOCALES:
        name = rm.asset_name("v2026.08.31", locale)
        (tmp_path / name).write_bytes(b"%PDF-1.7\n" + b"0" * 12_000)
        extracted[name] = "\n".join(
            value
            for page in manifest["pages"]
            for value in (page["headings"][locale], page["body_markers"][locale])
        ).encode("utf-8")

    monkeypatch.setattr(rm.shutil, "which", lambda _: "pdftotext")

    def fake_run(command: list[str], **_: object) -> SimpleNamespace:
        if command[1] == "-bbox-layout":
            return SimpleNamespace(stdout=b'<html><page width="595" height="842"><word xMin="10" yMin="10" xMax="20" yMax="20">OK</word></page></html>', stderr=b"")
        return SimpleNamespace(stdout=extracted[Path(command[2]).name], stderr=b"")

    monkeypatch.setattr(rm.subprocess, "run", fake_run)
    payload = rm.validate_pdfs("v2026.08.31", tmp_path)
    assert set(payload["assets"]) == set(rm.LOCALES)
    assert all(row["headings_verified"] == 28 for row in payload["assets"].values())
    assert all(row["body_markers_verified"] == 28 for row in payload["assets"].values())
    assert all(row["geometry_pages_verified"] == 1 for row in payload["assets"].values())


def test_pdf_validator_rejects_headings_that_only_appear_in_the_toc(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = rm.validate_pages_manifest()
    extracted: dict[str, bytes] = {}
    for locale in rm.LOCALES:
        name = rm.asset_name("v2026.08.31", locale)
        (tmp_path / name).write_bytes(b"%PDF-1.7\n" + b"0" * 12_000)
        extracted[name] = "\n".join(
            page["headings"][locale] for page in manifest["pages"]
        ).encode("utf-8")

    monkeypatch.setattr(rm.shutil, "which", lambda _: "pdftotext")
    monkeypatch.setattr(
        rm.subprocess,
        "run",
        lambda command, **_: SimpleNamespace(
            stdout=(b'<html><page width="595" height="842"><word xMin="10" yMin="10" xMax="20" yMax="20">OK</word></page></html>'
                    if command[1] == "-bbox-layout" else extracted[Path(command[2]).name]),
            stderr=b""),
    )
    with pytest.raises(rm.ReleaseManifestError, match="missing page headings"):
        rm.validate_pdfs("v2026.08.31", tmp_path)


def test_pdf_validator_rejects_an_english_body_that_is_mostly_cjk(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = rm.validate_pages_manifest()
    extracted: dict[str, bytes] = {}
    for locale in rm.LOCALES:
        name = rm.asset_name("v2026.08.31", locale)
        (tmp_path / name).write_bytes(b"%PDF-1.7\n" + b"0" * 12_000)
        text = "\n".join(
            value
            for page in manifest["pages"]
            for value in (page["headings"][locale], page["body_markers"][locale])
        )
        if locale == "en":
            text += "\n" + "未翻譯正文" * 100
        extracted[name] = text.encode("utf-8")

    monkeypatch.setattr(rm.shutil, "which", lambda _: "pdftotext")
    monkeypatch.setattr(
        rm.subprocess,
        "run",
        lambda command, **_: SimpleNamespace(
            stdout=(b'<html><page width="595" height="842"><word xMin="10" yMin="10" xMax="20" yMax="20">OK</word></page></html>'
                    if command[1] == "-bbox-layout" else extracted[Path(command[2]).name]),
            stderr=b""),
    )
    with pytest.raises(rm.ReleaseManifestError, match="too much CJK"):
        rm.validate_pdfs("v2026.08.31", tmp_path)


def test_pdf_validator_rejects_broken_english_table_labels(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = rm.validate_pages_manifest()
    extracted: dict[str, bytes] = {}
    for locale in rm.LOCALES:
        name = rm.asset_name("v2026.08.31", locale)
        (tmp_path / name).write_bytes(b"%PDF-1.7\n" + b"0" * 12_000)
        text = "\n".join(
            value
            for page in manifest["pages"]
            for value in (page["headings"][locale], page["body_markers"][locale])
        )
        if locale == "en":
            text += "\nDeskto\np\nRecommen\ndation\n"
        extracted[name] = text.encode("utf-8")

    monkeypatch.setattr(rm.shutil, "which", lambda _: "pdftotext")
    monkeypatch.setattr(
        rm.subprocess,
        "run",
        lambda command, **_: SimpleNamespace(
            stdout=(b'<html><page width="595" height="842"><word xMin="10" yMin="10" xMax="20" yMax="20">OK</word></page></html>'
                    if command[1] == "-bbox-layout" else extracted[Path(command[2]).name]),
            stderr=b""),
    )
    with pytest.raises(rm.ReleaseManifestError, match="splits an English table label"):
        rm.validate_pdfs("v2026.08.31", tmp_path)


def test_pdf_html_marks_only_wide_tables_without_changing_content() -> None:
    narrow = '<table><tr><th>One</th><th>Two</th></tr><tr><td>a</td><td>b</td></tr></table>'
    cells = ''.join(f'<th>Column {i}</th>' for i in range(8))
    wide = '<table class="existing"><thead><tr>' + cells + '</tr></thead><tbody><tr><td colspan="8">Unchanged text &amp; URL https://example.com</td></tr></tbody></table>'
    source = '<html><body>' + narrow + wide + '</body></html>'
    result = rm.prepare_pdf_html(source)
    assert narrow in result
    assert 'class="existing release-wide-table"' in result
    assert result.replace('class="existing release-wide-table"', 'class="existing"') == source
    assert rm.prepare_pdf_html(result) == result


def test_pdf_html_wide_detection_counts_header_colspan_and_nested_tables() -> None:
    source = '<table><tr><th colspan="8">Wide</th></tr><tr><td><table><tr><td>Nested narrow</td></tr></table></td></tr></table>'
    result = rm.prepare_pdf_html(source)
    assert result.count('release-wide-table') == 1
    assert '<table><tr><td>Nested narrow' in result


def test_pdf_geometry_accepts_portrait_and_landscape_bounds() -> None:
    xml = '<html><page width="595" height="842"><word xMin="10" yMin="10" xMax="590" yMax="20">portrait</word></page><page width="842" height="595"><word xMin="10" yMin="10" xMax="800" yMax="20">landscape</word></page></html>'
    assert rm.validate_pdf_geometry(xml, name='fixture.pdf') == {'pages': 2, 'words': 2}


@pytest.mark.parametrize('word', [
    'xMin="590" yMin="10" xMax="600" yMax="20"',
    'xMin="-2" yMin="10" xMax="20" yMax="20"',
    'xMin="10" yMin="840" xMax="20" yMax="850"',
    'xMin="20" yMin="10" xMax="10" yMax="20"',
    'xMin="nan" yMin="10" xMax="20" yMax="20"',
])
def test_pdf_geometry_rejects_clipped_or_invalid_word_boxes(word: str) -> None:
    xml = f'<html><page width="595" height="842"><word {word}>bad</word></page></html>'
    with pytest.raises(rm.ReleaseManifestError):
        rm.validate_pdf_geometry(xml, name='fixture.pdf')


@pytest.mark.parametrize('xml', ['broken XML', '<html/>', '<html><page width="nan" height="842"/></html>'])
def test_pdf_geometry_fails_closed_on_missing_or_invalid_page_data(xml: str) -> None:
    with pytest.raises(rm.ReleaseManifestError):
        rm.validate_pdf_geometry(xml, name='fixture.pdf')


def test_wide_pdf_tables_keep_readable_font_and_natural_columns() -> None:
    css = (rm.ROOT / 'release/pdf.css').read_text(encoding='utf-8')
    assert '@page release-wide' in css and 'size: A4 landscape' in css
    assert 'table.release-wide-table' in css and 'page: release-wide' in css
    assert 'font-size: 8.5pt' in css
    assert 'table-layout: fixed' not in css  # It fitted the page but overlapped price cells.


@pytest.mark.parametrize("opening,expected", [
    ('<table data-class="tracking">', '<table data-class="tracking" class="release-wide-table">'),
    ('<table data-class="tracking" class="existing">', '<table data-class="tracking" class="existing release-wide-table">'),
    ('<table class="existing" data-class="tracking">', '<table class="existing release-wide-table" data-class="tracking">'),
    ("<table title='class=\"decoy\"'>", "<table title='class=\"decoy\"' class=\"release-wide-table\">"),
    ("<table title='class=\"decoy\"' class=\"existing\">", "<table title='class=\"decoy\"' class=\"existing release-wide-table\">"),
    ("<table CLASS='existing' title=\" data-class='tracking'\">", "<table CLASS='existing release-wide-table' title=\" data-class='tracking'\">"),
])
def test_pdf_wide_class_changes_only_the_actual_attribute(opening: str, expected: str) -> None:
    body = '<tr>' + ''.join('<th>Column</th>' for _ in range(8)) + '</tr></table>'
    source = opening + body
    result = rm.prepare_pdf_html(source)
    assert result == expected + body
    assert rm.prepare_pdf_html(result) == result

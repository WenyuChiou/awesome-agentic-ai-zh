from __future__ import annotations

import importlib.util
import re
from datetime import date
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
    manifest = rm.validate_notes_manifest(expected_version="v2026.08.31")
    rendered = rm.render_notes(
        "v2026.08.31", sha="0123456789abcdef0123456789abcdef01234567"
    )
    assert rendered.index("## 繁體中文") < rendered.index("## 简体中文") < rendered.index("## English")
    assert rendered.count("- `") == len(manifest["changes"]) * 3
    for change in manifest["changes"]:
        for locale in rm.LOCALES:
            assert change[locale] in rendered
        for link in change["links"]:
            assert rendered.count(f"]({link})") == 3


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
        return SimpleNamespace(stdout=extracted[Path(command[2]).name], stderr=b"")

    monkeypatch.setattr(rm.subprocess, "run", fake_run)
    payload = rm.validate_pdfs("v2026.08.31", tmp_path)
    assert set(payload["assets"]) == set(rm.LOCALES)
    assert all(row["headings_verified"] == 28 for row in payload["assets"].values())
    assert all(row["body_markers_verified"] == 28 for row in payload["assets"].values())


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
        lambda command, **_: SimpleNamespace(stdout=extracted[Path(command[2]).name], stderr=b""),
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
        lambda command, **_: SimpleNamespace(stdout=extracted[Path(command[2]).name], stderr=b""),
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
        lambda command, **_: SimpleNamespace(stdout=extracted[Path(command[2]).name], stderr=b""),
    )
    with pytest.raises(rm.ReleaseManifestError, match="splits an English table label"):
        rm.validate_pdfs("v2026.08.31", tmp_path)

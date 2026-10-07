"""Keep manually verified license boundaries visible in all three locales."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("", ".en", ".zh-Hans")


def text(stem, locale):
    return (ROOT / f"{stem}{locale}.md").read_text(encoding="utf-8")


def entry(content, repository):
    heading = f"### [{repository}]"
    start = content.index(heading)
    end = content.find("\n### ", start + len(heading))
    return content[start:end if end >= 0 else None]


def row(content, repository):
    return next(line for line in content.splitlines() if f'github.com/{repository}"' in line)


def test_three_locale_license_boundaries():
    for locale in LOCALES:
        weaviate = row(text("stages/06-memory-rag", locale), "weaviate/weaviate")
        assert "BSD-3-Clause" in weaviate and "wl/" in weaviate
        assert any(term in weaviate for term in ("enterprise", "企業", "企业"))
        stage7 = text("stages/07-multi-agent-production", locale)
        assert "ELv2" in row(stage7, "Arize-ai/phoenix")
        assert "ee/" in row(stage7, "langfuse/langfuse")
        example = text("examples/stage-7/03-observability/README", locale)
        phoenix = next(line for line in example.splitlines() if "github.com/Arize-ai/phoenix" in line)
        assert "ELv2" in phoenix
        assert not any(term in phoenix for term in ("open-source", "開源", "开源"))
        cli = text("tracks/cli/A3-cli-production", locale)
        phoenix_cli = next(line for line in cli.splitlines() if "github.com/Arize-ai/phoenix" in line and "<tr>" in line)
        assert not any(term in phoenix_cli for term in ("open source", "開放原始碼", "开放源代码"))
        assert any(term in phoenix_cli for term in ("locally", "本機", "本机"))
        for stem, repository in (("stages/02-prompt-engineering", "NirDiamant/Prompt_Engineering"), ("resources/advanced-rag", "NirDiamant/RAG_Techniques")):
            content = row(text(stem, locale), repository)
            assert any(term in content for term in ("non-commercial", "非商業", "非商业"))
            assert any(term in content for term in ("written permission", "書面許可", "书面许可"))
        catalog = text("resources/mcp-skills-catalog", locale)
        skills = entry(catalog, "anthropics/skills")
        assert all(term in skills for term in ("Apache-2.0", "source-available", "docx", "pdf", "pptx", "xlsx"))
        assert not any(term in skills for term in ("No license file", "無 license 檔", "无 license 文件"))
        sentry = entry(catalog, "getsentry/toolkit")
        assert "FSL-1.1-Apache-2.0" in sentry and "Competing Use" in sentry


def test_evidence_has_specific_sources_without_overriding_metadata():
    evidence = json.loads((ROOT / "scripts/license-review-evidence.json").read_text())
    expected = {
        "arize-ai/phoenix", "weaviate/weaviate", "langfuse/langfuse",
        "nirdiamant/prompt_engineering", "nirdiamant/rag_techniques",
        "anthropics/skills", "getsentry/toolkit",
    }
    repositories = [item["repository"] for item in evidence]
    assert len(repositories) == len(set(repositories))
    assert set(repositories) == expected
    for item in evidence:
        assert item["reviewed_on"] == "2026-10-05"
        assert item["source_url"].startswith("https://github.com/")
        # Shape validation only; the upstream documents were reviewed separately.
        assert re.fullmatch(r"[0-9a-f]{40}", item["source_blob_sha"])
        assert "metadata remains unchanged" in item["scope"]


if __name__ == "__main__":
    test_three_locale_license_boundaries()
    test_evidence_has_specific_sources_without_overriding_metadata()
    print("Three-locale license boundary checks passed.")

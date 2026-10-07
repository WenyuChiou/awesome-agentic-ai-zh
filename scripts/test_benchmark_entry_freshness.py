"""Keep benchmark versions and comparable-result boundaries visible in all locales."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_benchmark_entry_points_and_version_boundaries():
    for locale in ("", ".en", ".zh-Hans"):
        page = (ROOT / f"stages/07-multi-agent-production{locale}.md").read_text()
        section = page[page.index("- [SWE-bench]"):]
        section = section[:section.index("</details>")]
        assert "[Terminal-Bench](https://www.tbench.ai/)" in section
        assert "https://docs.harborframework.com/" in section
        assert "[1.x repository](https://github.com/harbor-framework/terminal-bench-1)" in section
        assert "[τ-bench](https://github.com/sierra-research/tau2-bench)" in section
        assert "[τ²-bench]" not in section
        for boundary in ("τ³", "banking_knowledge", "v1.0.1", "task split", "harness commit", "grader", "trial"):
            assert boundary in section
        assert any(word in section for word in ("not directly comparable", "不可直接比較", "不可直接比较"))
        assert any(word in section for word in ("legacy", "舊版", "旧版"))

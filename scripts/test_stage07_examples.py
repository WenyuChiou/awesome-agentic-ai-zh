#!/usr/bin/env python3
"""Regression contract for the six runnable Stage 07 examples."""

from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "examples" / "stage-7"
FOLDERS = (
    "01-multi-agent-debate",
    "02-eval",
    "03-observability",
    "04-sdk-advanced",
    "05-deploy",
)
SAFE_FOLDER = "06-safe-execution"
README_NAMES = ("README.md", "README.en.md", "README.zh-Hans.md")
RESOURCE_HEADINGS = {
    "README.md": "## 📚 必讀與學習資源",
    "README.en.md": "## 📚 Required reading and learning resources",
    "README.zh-Hans.md": "## 📚 必读与学习资源",
}
RESOURCE_COUNTS = {
    "01-multi-agent-debate": 3,
    "02-eval": 6,
    "03-observability": 7,
    "04-sdk-advanced": 4,
    "05-deploy": 5,
    SAFE_FOLDER: 4,
}
RESOURCE_FOOTERS = {
    "README.md": "完整清單見",
    "README.en.md": "See the full list",
    "README.zh-Hans.md": "完整清单见",
}
DETAIL_TAG = re.compile(r"<details\b[^>]*>|</details>")
PYTHON_NAMES = ("starter.py", "starter_anthropic.py", "test.py", "test_anthropic.py")
COMMON_REQUIREMENTS = ("openai>=3.5,<4", "anthropic>=1.2,<2")
DEPLOY_REQUIREMENTS = (
    "fastapi>=0.141,<1",
    "uvicorn[standard]>=0.52,<1",
    "pydantic>=2.13,<3",
    "httpx>=0.28,<1",
    *COMMON_REQUIREMENTS,
)
OLLAMA_MODEL = "qwen3.5:4b"
ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
HELLO_AGENTS_URL = "https://github.com/datawhalechina/hello-agents"
FLOATING_HAIKU = re.compile(r"claude-haiku-4-5(?!-20251001)")
FORBIDDEN_TEXT = (
    "qwen2.5:3b",
    "$0/run",
    "$0／run",
    "$0 per run",
    "≈$0.0001",
    "≈$0.001",
    "≈$0.003",
    "≈$0.005",
    "省 90% cost",
    "省 90%",
    "90% cost cut",
    "90% savings",
    "production cost 立刻減 90%",
    "0.3-0.8s",
    "0.5-2s",
    "0.3-1 秒",
    "0.5 秒看到",
    "token usage 精確",
    "usage.tokens` precision",
    "usage.tokens` 精确度",
    "降低單一 LLM 的 bias",
    "Claude 比 qwen 穩",
)


def _lines(path: Path) -> tuple[str, ...]:
    return tuple(
        line.split("#", 1)[0].strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.split("#", 1)[0].strip()
    )


def _detail_depth_at(text: str, offset: int) -> int:
    """Return open `<details>` depth immediately before `offset`."""
    depth = 0
    for match in DETAIL_TAG.finditer(text, 0, offset):
        depth += -1 if match.group().startswith("</details") else 1
        assert depth >= 0, "closing </details> appears before an opening tag"
    return depth


def test_detail_depth_detects_a_resource_hidden_after_its_heading() -> None:
    hidden = "## 📚 Required reading\n<details>\n- ⭐⭐⭐⭐⭐ Resource\n</details>\n"
    assert _detail_depth_at(hidden, hidden.index("## 📚")) == 0
    assert _detail_depth_at(hidden, hidden.index("- ⭐")) == 1


def test_stage_shape_and_current_dependencies() -> None:
    actual = {path.name for path in STAGE.iterdir() if path.is_dir()}
    assert actual == {*FOLDERS, SAFE_FOLDER}
    for folder_name in FOLDERS:
        folder = STAGE / folder_name
        for name in (*README_NAMES, *PYTHON_NAMES, "requirements.txt"):
            assert (folder / name).is_file(), f"{folder_name}: missing {name}"
        expected = DEPLOY_REQUIREMENTS if folder_name == "05-deploy" else COMMON_REQUIREMENTS
        assert _lines(folder / "requirements.txt") == expected, folder_name
    assert (STAGE / "05-deploy" / "Dockerfile").is_file()
    safe = STAGE / SAFE_FOLDER
    for name in (*README_NAMES, "starter.py", "test.py"):
        assert (safe / name).is_file(), f"{SAFE_FOLDER}: missing {name}"
    assert not (safe / "requirements.txt").exists()
    assert not (safe / "starter_anthropic.py").exists()


def test_starters_parse_and_pin_current_models() -> None:
    for folder_name in FOLDERS:
        folder = STAGE / folder_name
        for name in PYTHON_NAMES:
            path = folder / name
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(path))
            assert "sys.stdout.reconfigure" in source
        ollama = (folder / "starter.py").read_text(encoding="utf-8")
        anthropic = (folder / "starter_anthropic.py").read_text(encoding="utf-8")
        assert f'"{OLLAMA_MODEL}"' in ollama
        assert f'"{ANTHROPIC_MODEL}"' in anthropic
        assert not FLOATING_HAIKU.search(anthropic)


def test_shared_model_guide_separates_stage7_from_function_calling() -> None:
    guide_paths = tuple(ROOT / "examples" / name for name in README_NAMES)
    guides = [path.read_text(encoding="utf-8") for path in guide_paths]
    for path, guide in zip(guide_paths, guides):
        assert "qwen2.5:3b" in guide, path
        assert OLLAMA_MODEL in guide, path
        assert "2026-08-31" in guide, path
        assert not re.search(r"Stage\s*3\+", guide), path
        assert "API cost is $0" not in guide
        assert "API 成本是 $0" not in guide
        assert "隱私敏感資料 OK" not in guide
        assert "隐私敏感资料 OK" not in guide
    assert all(guide.count(OLLAMA_MODEL) == guides[0].count(OLLAMA_MODEL) for guide in guides[1:])
    for path, guide in zip(guide_paths, guides):
        qwen25_row = next(line for line in guide.splitlines() if "`qwen2.5:3b`" in line and "1.9 GB" in line)
        qwen35_row = next(line for line in guide.splitlines() if "`qwen3.5:4b`" in line and "3.4 GB" in line)
        assert "3–6" in qwen25_row, path
        assert "Stage 7" in qwen35_row, path

    repo_contract = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    assert "Stages 3–6" in repo_contract
    assert OLLAMA_MODEL in repo_contract
    assert "does not replace the Stage 3–6 tool-use default" in repo_contract

    setup_paths = tuple(ROOT / "resources" / name for name in (
        "setup-guide.md",
        "setup-guide.en.md",
        "setup-guide.zh-Hans.md",
    ))
    setup_guides = [path.read_text(encoding="utf-8") for path in setup_paths]
    for path, guide in zip(setup_paths, setup_guides):
        assert "qwen2.5:3b" in guide and OLLAMA_MODEL in guide, path
        assert not re.search(r"Stage\s*3\+", guide), path
        assert "$0/run" not in guide, path
        assert "zero API cost" not in guide, path
        assert "不付 API 費" not in guide, path
        assert "不付 API 费" not in guide, path
    assert all(guide.count(OLLAMA_MODEL) == setup_guides[0].count(OLLAMA_MODEL) for guide in setup_guides[1:])


def test_model_outputs_are_validated_and_judges_are_strict() -> None:
    for folder_name in FOLDERS:
        folder = STAGE / folder_name
        starters = "\n".join(
            (folder / name).read_text(encoding="utf-8")
            for name in ("starter.py", "starter_anthropic.py")
        )
        assert "require_text(" in starters, f"{folder_name}: empty output is not rejected"

    debate = (STAGE / "01-multi-agent-debate" / "starter.py").read_text(encoding="utf-8")
    debate_b = (STAGE / "01-multi-agent-debate" / "starter_anthropic.py").read_text(encoding="utf-8")
    assert "parse_winner(" in debate and "fullmatch(" in debate
    assert "parse_winner(" in debate_b and "fullmatch(" in debate_b

    eval_source = (STAGE / "02-eval" / "starter.py").read_text(encoding="utf-8")
    assert "parse_verdict(" in eval_source and "fullmatch(" in eval_source
    assert '"PASS" in verdict' not in eval_source


def test_safe_execution_is_offline_fail_closed_and_idempotent() -> None:
    folder = STAGE / SAFE_FOLDER
    starter_path = folder / "starter.py"
    test_path = folder / "test.py"
    starter = starter_path.read_text(encoding="utf-8")
    tests = test_path.read_text(encoding="utf-8")
    ast.parse(starter, filename=str(starter_path))
    ast.parse(tests, filename=str(test_path))

    forbidden_imports = ("openai", "anthropic", "requests", "httpx", "urllib")
    imported = {
        node.names[0].name.split(".", 1)[0]
        for node in ast.walk(ast.parse(starter))
        if isinstance(node, (ast.Import, ast.ImportFrom)) and node.names
    }
    assert imported.isdisjoint(forbidden_imports)
    for marker in (
        "waiting_for_approval",
        "idempotency_key",
        "tempfile.mkstemp",
        "os.fsync",
        "status and approval decision do not agree",
        "duplicate idempotency key",
    ):
        assert marker in starter
    for marker in (
        "test_start_pauses_without_a_side_effect",
        "test_rejection_cancels_without_a_side_effect",
        "test_approval_executes_exactly_once",
        "test_resume_after_ledger_write_does_not_repeat_the_side_effect",
        "test_corrupt_or_mismatched_state_fails_closed",
    ):
        assert marker in tests

    result = subprocess.run(
        [sys.executable, "test.py"],
        cwd=folder,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "8/8 passed" in result.stdout


def test_prompt_cache_demo_exceeds_the_documented_minimum_and_checks_usage() -> None:
    folder = STAGE / "04-sdk-advanced"
    starter = (folder / "starter_anthropic.py").read_text(encoding="utf-8")
    tests = (folder / "test_anthropic.py").read_text(encoding="utf-8")
    assert "CACHE_MINIMUM_TOKENS = 4096" in starter
    assert "CACHE_DEMO_REPEAT = 1200" in starter
    assert "build_cache_demo_prompt(" in starter
    assert "cache_creation_input_tokens" in starter
    assert "cache_read_input_tokens" in starter
    assert "test_cache_demo_is_deliberately_long" in tests
    assert "split()" in tests and "> 6000" in tests


def test_streams_reject_whitespace_and_observability_sanitizes_errors() -> None:
    sdk = STAGE / "04-sdk-advanced"
    for name, marker in (
        ("starter.py", "saw_non_whitespace"),
        ("starter_anthropic.py", "saw_non_whitespace"),
        ("test.py", "test_stream_rejects_whitespace_only_chunks"),
        ("test_anthropic.py", "test_stream_anthropic_rejects_whitespace_only_chunks"),
    ):
        assert marker in (sdk / name).read_text(encoding="utf-8")

    observability = STAGE / "03-observability"
    starter = (observability / "starter.py").read_text(encoding="utf-8")
    tests = (observability / "test.py").read_text(encoding="utf-8")
    assert "type(exc).__name__" in starter
    assert "str(exc)" not in starter and "str(e)" not in starter
    assert "sk-ant-secret-marker" in tests


def test_deploy_has_bounded_input_and_a_non_root_container() -> None:
    folder = STAGE / "05-deploy"
    for name in ("starter.py", "starter_anthropic.py"):
        source = (folder / name).read_text(encoding="utf-8")
        assert "Field(min_length=1, max_length=4000)" in source
        assert "Field(default=300, ge=1, le=1000)" in source
        assert 'uvicorn.run(app, host="127.0.0.1", port=8000)' in source
        health_body = source.split('def health():', 1)[1].split('@app.post', 1)[0]
        assert "messages.create" not in health_body and "chat.completions" not in health_body
        assert "req.message" not in source.split("def chat", 1)[1].split("try:", 1)[0]
        assert "logger.exception" not in source
        assert "type(e).__name__" in source
    dockerfile = (folder / "Dockerfile").read_text(encoding="utf-8")
    assert "USER appuser" in dockerfile
    assert "useradd" in dockerfile

    test_a = (folder / "test.py").read_text(encoding="utf-8")
    test_b = (folder / "test_anthropic.py").read_text(encoding="utf-8")
    for marker in ("test_chat_rejects_blank_message", "test_chat_rejects_oversized_message", "test_chat_rejects_excessive_max_tokens"):
        assert marker in test_a and marker in test_b
    assert "test_chat_500_does_not_log_secret" in test_a
    assert "test_chat_500_does_not_log_secret" in test_b
    assert "sk-ant-secret-marker" in test_a and "sk-ant-secret-marker" in test_b
    assert "test_chat_anthropic_503_on_connection_error" in test_b


def test_readmes_are_power_shell_first_progressive_and_fact_aligned() -> None:
    for folder_name in FOLDERS:
        folder = STAGE / folder_name
        texts = [(folder / name).read_text(encoding="utf-8") for name in README_NAMES]
        urls = tuple(re.findall(r"https?://[^)\s]+", texts[0]))
        for name, text in zip(README_NAMES, texts):
            first_detail = text.index('<details markdown="1">')
            install = text.index(r".\.venv\Scripts\python.exe -m pip install -r requirements.txt")
            offline = text.index(r".\.venv\Scripts\python.exe test.py")
            resource_heading = RESOURCE_HEADINGS[name]
            resource_index = text.index(resource_heading)
            resource_section = text[resource_index:]
            rated_resources = tuple(re.finditer(r"(?m)^- (?:⭐){3,5} ", resource_section))
            footer_index = text.index(RESOURCE_FOOTERS[name], resource_index)
            verified_date_index = text.index("<small>", resource_index)
            assert install < offline < first_detail, f"{folder_name}/{name}: quick start is hidden"
            assert r"py -3.11 -m venv .venv" in text
            assert r".\.venv\Scripts\python.exe test_anthropic.py" in text
            expected_details = 4 if folder_name == "05-deploy" else 3
            assert text.count('<details markdown="1">') == expected_details
            assert '<details markdown="1" open>' not in text
            assert "🎯" in text and "📚" in text
            assert text.count(resource_heading) == 1
            assert _detail_depth_at(text, resource_index) == 0
            assert _detail_depth_at(text, footer_index) == 0
            assert _detail_depth_at(text, verified_date_index) == 0
            assert _detail_depth_at(text, len(text)) == 0
            assert "<summary>📚" not in text
            assert len(rated_resources) == RESOURCE_COUNTS[folder_name]
            assert all(
                _detail_depth_at(text, resource_index + match.start()) == 0
                for match in rated_resources
            ), f"{folder_name}/{name}: at least one required resource is hidden"
            assert OLLAMA_MODEL in text and ANTHROPIC_MODEL in text
            assert "$1 / 1M" in text and "$5 / 1M" in text
            assert "$1" in text and "2026-08-28 UTC" in text
            assert text.count(HELLO_AGENTS_URL) == 1, (
                f"{folder_name}/{name}: missing or duplicated chapter-style deep-learning route"
            )
            assert tuple(re.findall(r"https?://[^)\s]+", text)) == urls
            assert not FLOATING_HAIKU.search(text)
            assert not any(phrase in text for phrase in FORBIDDEN_TEXT), f"{folder_name}/{name} has stale claim"
        assert all(text.count(OLLAMA_MODEL) == texts[0].count(OLLAMA_MODEL) for text in texts[1:])
        assert all(text.count(ANTHROPIC_MODEL) == texts[0].count(ANTHROPIC_MODEL) for text in texts[1:])

        english_body = texts[1].split("</div>", 1)[1]
        assert not re.search(r"[\u3400-\u9fff]", english_body), f"{folder_name}: English body contains CJK text"
        assert "../../../stages/07-multi-agent-production.en.md" in texts[1]
        assert "../../../stages/07-multi-agent-production.zh-Hans.md" in texts[2]

    deploy_texts = [
        (STAGE / "05-deploy" / name).read_text(encoding="utf-8")
        for name in README_NAMES
    ]
    for text in deploy_texts:
        assert "127.0.0.1:8000:8000" in text
        assert "--read-only" in text and "--tmpfs /tmp" in text
        assert "完整 sandbox" not in text and "complete sandbox" not in text

    dockerfile = (STAGE / "05-deploy" / "Dockerfile").read_text(encoding="utf-8")
    assert 'CMD ["uvicorn", "starter:app"' in dockerfile
    assert 'CMD ["sh", "-c"' not in dockerfile and "APP_MODULE" not in dockerfile


def test_safe_execution_readmes_keep_the_core_path_and_resources_visible() -> None:
    folder = STAGE / SAFE_FOLDER
    paths = tuple(folder / name for name in README_NAMES)
    texts = tuple(path.read_text(encoding="utf-8") for path in paths)
    expected_urls = (
        "https://openai.github.io/openai-agents-python/human_in_the_loop/",
        "https://docs.langchain.com/oss/python/langgraph/interrupts",
        "https://docs.langchain.com/oss/python/langgraph/persistence",
        "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents",
    )
    required_terms = (
        "Human Approval",
        "Checkpoint",
        "Resume",
        "Recovery",
        "Idempotency",
    )
    for name, text in zip(README_NAMES, texts):
        resource_index = text.index(RESOURCE_HEADINGS[name])
        first_detail = text.index('<details markdown="1">')
        assert text.startswith("<div align=\"right\">")
        assert "Core Exercise" in text or "核心練習" in text or "核心练习" in text
        assert r"py -3.11 test.py" in text[:first_detail]
        assert all(f"**{term}" in text for term in required_terms)
        assert tuple(re.findall(r"https?://[^)\s]+", text)) == expected_urls
        assert len(re.findall(r"(?m)^- ⭐⭐⭐⭐⭐ ", text[resource_index:])) == 4
        assert _detail_depth_at(text, resource_index) == 0
        assert _detail_depth_at(text, text.index("<small>", resource_index)) == 0
        assert text.count('<details markdown="1">') == 2
        assert '<details markdown="1" open>' not in text
        assert "2026-08-31 UTC" in text
        assert OLLAMA_MODEL not in text and ANTHROPIC_MODEL not in text
        assert "requirements.txt" not in text
    assert "../../../stages/07-multi-agent-production.en.md" in texts[1]
    assert "../../../stages/07-multi-agent-production.zh-Hans.md" in texts[2]
    assert "../../../stages/07-multi-agent-production.md#-上線四步eval--observability--approvalrecovery--deploy" in texts[0]
    assert "../../../stages/07-multi-agent-production.en.md#-four-release-steps-eval--observability--approval--recovery--deploy" in texts[1]
    assert "../../../stages/07-multi-agent-production.zh-Hans.md#-上线四步eval--observability--approvalrecovery--deploy" in texts[2]
    english_body = texts[1].split("</div>", 1)[1]
    assert not re.search(r"[\u3400-\u9fff]", english_body)


if __name__ == "__main__":
    raise SystemExit(__import__("pytest").main([__file__]))

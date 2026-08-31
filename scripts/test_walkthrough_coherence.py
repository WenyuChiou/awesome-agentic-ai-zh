"""Paper Summary Bot route, freshness, safety, and locale-mirror contracts."""

from __future__ import annotations

import ast
import re
from contextlib import contextmanager
from types import SimpleNamespace
from typing import Literal, TypedDict
from urllib.parse import urlparse
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "zh-TW": ROOT / "walkthroughs/build-first-agent-in-7-steps.md",
    "en": ROOT / "walkthroughs/build-first-agent-in-7-steps.en.md",
    "zh-Hans": ROOT / "walkthroughs/build-first-agent-in-7-steps.zh-Hans.md",
}
FRESHNESS = (
    "<!-- freshness: canonical=walkthroughs/build-first-agent-in-7-steps.md; "
    "verified_on=2026-08-31; "
    "scope=models,frameworks,evals,observability,human-approval,interfaces; "
    "max_age_days=90 -->"
)
REQUIRED_URLS = (
    "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents",
    "https://docs.langchain.com/oss/python/langchain/human-in-the-loop",
    "https://docs.langchain.com/oss/python/langgraph/persistence",
    "https://langfuse.com/integrations/frameworks/langchain",
)
HEADINGS = {
    "zh-TW": (
        "## 📚 先讀這五份（保持展開）",
        "## Stage 7 — Eval → Observability → Approval／Recovery → Deploy",
        "## Stage 8 — 選最小介面，先留安全出口",
    ),
    "en": (
        "## 📚 Read these five first (keep expanded)",
        "## Stage 7 — Eval → Observability → Approval/Recovery → Deploy",
        "## Stage 8 — Choose the Smallest Interface and Keep a Safe Exit",
    ),
    "zh-Hans": (
        "## 📚 先读这五份（保持展开）",
        "## Stage 7 — Eval → Observability → Approval／Recovery → Deploy",
        "## Stage 8 — 选择最小界面，先留安全出口",
    ),
}
SAFE_EXAMPLE_LINKS = {
    "zh-TW": "../examples/stage-7/06-safe-execution/README.md",
    "en": "../examples/stage-7/06-safe-execution/README.en.md",
    "zh-Hans": "../examples/stage-7/06-safe-execution/README.zh-Hans.md",
}
STAGE8_LINKS = {
    "zh-TW": "../stages/08-agent-interfaces.md",
    "en": "../stages/08-agent-interfaces.en.md",
    "zh-Hans": "../stages/08-agent-interfaces.zh-Hans.md",
}
VALID_SUMMARY = """## Motivation
Agent systems need reliable evidence.
## Method
The system fetches, checks, and compares papers.
## Results
The output remains reviewable.
Keywords: agent, retrieval, evaluation, memory, safety
## Differences
- It keeps a typed safe exit.
"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def external_urls(text: str) -> list[str]:
    # Keep locale punctuation outside the URL. CJK sentences do not put a space
    # after a link, so a generic ``\S+`` pattern can swallow translated prose.
    return re.findall(r"https://[A-Za-z0-9][A-Za-z0-9./?=_#&%@:+~-]*", text)


def python_blocks(text: str) -> list[str]:
    return re.findall(r"```python\n(.*?)```", text, flags=re.DOTALL)


def named_python_block(text: str, marker: str) -> str:
    return next(block for block in python_blocks(text) if marker in block)


def current_agent_namespace(text: str) -> dict:
    """Load only the pure wrapper from the teaching block, with fake boundaries."""
    stage3 = ast.parse(named_python_block(text, "def parse_arxiv_id"))
    parse_node = next(
        node for node in stage3.body
        if isinstance(node, ast.FunctionDef) and node.name == "parse_arxiv_id"
    )
    class FakeSourceValidationError(ValueError):
        pass

    parse_ns = {
        "SourceValidationError": FakeSourceValidationError,
        "re": re,
        "urlparse": urlparse,
    }
    exec(compile(ast.Module([parse_node], type_ignores=[]), "<stage3-parse>", "exec"), parse_ns)

    wrapper = ast.parse(named_python_block(text, "class AgentResult"))
    selected = [
        node for node in wrapper.body
        if (
            isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "MAX_GRAPH_STEPS" for target in node.targets)
        )
        or (
            isinstance(node, ast.ClassDef)
            and node.name == "AgentResult"
        )
        or (
            isinstance(node, ast.FunctionDef)
            and node.name in {"_needs_review", "run_current_agent"}
        )
    ]

    class FakeGraphRecursionError(Exception):
        pass

    class FakeRequestException(Exception):
        pass

    contract_ns = stage4_contract_namespace(text)
    logger = SimpleNamespace(calls=[], error=lambda *args, **kwargs: logger.calls.append((args, kwargs)))
    namespace = {
        "AgentResult": dict,
        "GraphRecursionError": FakeGraphRecursionError,
        "HumanMessage": lambda content: SimpleNamespace(type="human", content=content),
        "Literal": Literal,
        "RequestException": FakeRequestException,
        "SourceValidationError": FakeSourceValidationError,
        "TypedDict": TypedDict,
        "logger": logger,
        "output_contract_ok": contract_ns["output_contract_ok"],
        "parse_arxiv_id": parse_ns["parse_arxiv_id"],
    }
    exec(compile(ast.Module(selected, type_ignores=[]), "<current-agent>", "exec"), namespace)
    return namespace


def stage4_contract_namespace(text: str) -> dict:
    block = ast.parse(named_python_block(text, "def output_contract_ok"))
    selected_names = {
        "MAX_REVISIONS",
        "REQUIRED_HEADINGS",
        "REVIEW_CRITERIA",
        "VALID_REVIEW_VERDICTS",
    }
    selected = [
        node for node in block.body
        if (
            isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id in selected_names for target in node.targets)
        )
        or (
            isinstance(node, ast.FunctionDef)
            and node.name in {"output_contract_ok", "reflect", "should_continue"}
        )
    ]
    namespace = {
        "HumanMessage": lambda content: SimpleNamespace(type="human", content=content),
        "State": dict,
    }
    exec(compile(ast.Module(selected, type_ignores=[]), "<stage4-contract>", "exec"), namespace)
    return namespace


def observability_namespace(text: str, namespace: dict) -> dict:
    block = ast.parse(named_python_block(text, "# step7_observability.py"))
    function = next(
        node for node in block.body
        if isinstance(node, ast.FunctionDef) and node.name == "run_paper_agent"
    )
    exec(compile(ast.Module([function], type_ignores=[]), "<observability>", "exec"), namespace)
    return namespace


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_required_reading_and_freshness_stay_visible(locale: str, page: Path) -> None:
    text = read(page)
    reading_heading, stage7_heading, stage8_heading = HEADINGS[locale]
    assert FRESHNESS in text
    assert "2026-08-31 UTC" in text
    assert reading_heading in text
    reading = text[text.index(reading_heading) : text.index("## Stage 0")]
    assert all(url in reading for url in REQUIRED_URLS)
    assert STAGE8_LINKS[locale] in reading
    assert reading.count("⭐⭐⭐⭐⭐") == 5
    assert "<details" not in reading
    assert text.index(stage7_heading) < text.index(stage8_heading)


def test_three_locales_keep_the_same_external_sources() -> None:
    urls = {locale: external_urls(read(page)) for locale, page in PAGES.items()}
    assert urls["zh-TW"] == urls["en"] == urls["zh-Hans"]


@pytest.mark.parametrize("page", PAGES.values())
def test_all_ten_python_blocks_still_parse(page: Path) -> None:
    blocks = python_blocks(read(page))
    assert len(blocks) == 10
    for index, block in enumerate(blocks, start=1):
        ast.parse(block, filename=f"{page.name}:python-block-{index}")


@pytest.mark.parametrize("page", PAGES.values())
def test_current_framework_fetch_eval_and_trace_shapes(page: Path) -> None:
    text = read(page)
    for marker in (
        "from langchain.agents import create_agent",
        "https://export.arxiv.org/api/query",
        'parsed.hostname != "arxiv.org"',
        "timeout=15",
        "response.raise_for_status()",
        "npx promptfoo@latest eval",
        'as_type="agent"',
        "capture_input=False",
        "capture_output=False",
        "from langfuse.langchain import CallbackHandler",
        "LANGFUSE_BASE_URL",
        "langfuse.flush()",
    ):
        assert marker in text, (page, marker)
    for stale in (
        "from langgraph.prebuilt import create_react_agent",
        "create_react_agent(",
        "http://export.arxiv.org",
        "npm install -g promptfoo",
        "promptfoo eval && promptfoo view",
        "langfuse **3.0**",
        "LANGFUSE_HOST",
    ):
        assert stale not in text, (page, stale)


@pytest.mark.parametrize("page", PAGES.values())
def test_the_old_stage3_loop_is_bounded_and_never_reenters_production(page: Path) -> None:
    text = read(page)
    stage3 = named_python_block(text, "MAX_TOOL_ROUNDS")
    assert "MAX_TOOL_ROUNDS = 4" in stage3
    assert "for _ in range(MAX_TOOL_ROUNDS)" in stage3
    assert "while True" not in stage3
    assert "tool round budget exhausted; needs_review" in stage3
    assert "from step3_tool_use import run_agent" not in text


@pytest.mark.parametrize("page", PAGES.values())
def test_the_current_agent_is_used_by_eval_trace_and_api(page: Path) -> None:
    text = read(page)
    assert text.count("from step6_memory import") == 3
    assert "from step6_memory import run_current_agent" in text
    assert "from step6_memory import AgentResult, run_current_agent" in text
    assert "from step6_memory import collection, store_paper" in text
    assert "from step2_paper_summary import SYSTEM_PROMPT" in text
    assert 'system_prompt=CURRENT_AGENT_SYSTEM_PROMPT' in text
    assert "run_current_agent(paper_url)" in text
    assert "max_graph_steps=req.max_graph_steps" in text
    assert "provider" in text and "usage" in text


@pytest.mark.parametrize("page", PAGES.values())
def test_current_agent_returns_memory_and_typed_safe_exits(page: Path) -> None:
    namespace = current_agent_namespace(read(page))
    calls = []

    class FakeGraph:
        def invoke(self, state, config):
            calls.append((state, config))
            return {
                "messages": [SimpleNamespace(type="ai", content=VALID_SUMMARY)],
                "comparison": "memory comparison",
                "revisions": 1,
                "review_verdict": "PASS",
            }

    namespace["app_with_memory"] = FakeGraph()
    run = namespace["run_current_agent"]
    completed = run(
        "https://arxiv.org/abs/2210.03629",
        task_id="task-1",
        callbacks=["trace"],
    )
    assert completed == {
        "status": "completed",
        "task_id": "task-1",
        "summary": VALID_SUMMARY,
        "comparison": "memory comparison",
        "reason": None,
        "steps_used": 3,
        "step_budget": 8,
    }
    assert calls[0][0]["arxiv_id"] == "2210.03629"
    assert calls[0][1]["recursion_limit"] == 8
    assert calls[0][1]["callbacks"] == ["trace"]

    assert run("https://arxiv.org.evil/abs/2210.03629")["reason"] == "source_not_allowed"
    assert run("https://arxiv.org/abs/2210.03629", max_graph_steps=9)["reason"] == "invalid_step_budget"

    class ExhaustedGraph:
        def invoke(self, state, config):
            raise namespace["GraphRecursionError"]()

    namespace["app_with_memory"] = ExhaustedGraph()
    exhausted = run("https://arxiv.org/abs/2210.03629")
    assert exhausted["status"] == "needs_review"
    assert exhausted["reason"] == "step_budget_exhausted"

    class UnsafeToolGraph:
        def invoke(self, state, config):
            raise namespace["SourceValidationError"]("model proposed a non-allowlisted tool URL")

    namespace["app_with_memory"] = UnsafeToolGraph()
    unsafe_tool = run("https://arxiv.org/abs/2210.03629")
    assert unsafe_tool["status"] == "needs_review"
    assert unsafe_tool["reason"] == "source_not_allowed"

    class IncompleteGraph:
        def invoke(self, state, config):
            return {"messages": [], "revisions": 0, "review_verdict": "PASS"}

    namespace["app_with_memory"] = IncompleteGraph()
    incomplete = run("https://arxiv.org/abs/2210.03629")
    assert incomplete["status"] == "needs_review"
    assert incomplete["reason"] == "incomplete_result"

    class FailedReviewGraph:
        def invoke(self, state, config):
            return {
                "messages": [SimpleNamespace(type="ai", content=VALID_SUMMARY)],
                "comparison": "",
                "revisions": 2,
                "review_verdict": "NEEDS_REVISION",
                "review_failure_reason": "review_budget_exhausted",
            }

    namespace["app_with_memory"] = FailedReviewGraph()
    failed_review = run("https://arxiv.org/abs/2210.03629")
    assert failed_review["reason"] == "review_budget_exhausted"

    class BadContractGraph:
        def invoke(self, state, config):
            return {
                "messages": [SimpleNamespace(type="ai", content="looks plausible")],
                "comparison": "memory comparison",
                "revisions": 1,
                "review_verdict": "PASS",
            }

    namespace["app_with_memory"] = BadContractGraph()
    bad_contract = run("https://arxiv.org/abs/2210.03629")
    assert bad_contract["reason"] == "output_contract_failed"

    class InternalBugGraph:
        def invoke(self, state, config):
            raise ValueError("not a source-validation error")

    namespace["app_with_memory"] = InternalBugGraph()
    internal = run("https://arxiv.org/abs/2210.03629")
    assert internal["reason"] == "internal_error"
    assert namespace["logger"].calls


@pytest.mark.parametrize("page", PAGES.values())
def test_output_contract_and_review_routing_fail_closed(page: Path) -> None:
    namespace = stage4_contract_namespace(read(page))
    assert namespace["output_contract_ok"](VALID_SUMMARY)
    assert not namespace["output_contract_ok"]("three vague paragraphs")

    class NeverCalled:
        def invoke(self, prompt):
            raise AssertionError("Malformed output must be rejected before model review")

    namespace["llm"] = NeverCalled()
    malformed = namespace["reflect"](
        {"messages": [SimpleNamespace(type="ai", content="missing labels")], "revisions": 0}
    )
    assert malformed["review_verdict"] == "NEEDS_REVISION"
    assert namespace["should_continue"](malformed) == "agent"
    assert namespace["REVIEW_CRITERIA"] in malformed["messages"][0].content

    class ReviewModel:
        def __init__(self, verdict):
            self.verdict = verdict

        def invoke(self, prompt):
            return SimpleNamespace(content=self.verdict)

    namespace["llm"] = ReviewModel("MAYBE")
    invalid = namespace["reflect"](
        {"messages": [SimpleNamespace(type="ai", content=VALID_SUMMARY)], "revisions": 0}
    )
    assert invalid["review_verdict"] == "INVALID_REVIEW"
    assert namespace["should_continue"](invalid) == "needs_review"

    namespace["llm"] = ReviewModel("PASS")
    passed = namespace["reflect"](
        {"messages": [SimpleNamespace(type="ai", content=VALID_SUMMARY)], "revisions": 0}
    )
    assert passed["review_verdict"] == "PASS"
    assert namespace["should_continue"](passed) == "done"


@pytest.mark.parametrize("page", PAGES.values())
def test_observability_emits_safe_root_metadata_and_traces_the_current_agent(page: Path) -> None:
    events = {"propagated": [], "agent_calls": [], "span_updates": []}
    handler = object()

    @contextmanager
    def fake_propagate_attributes(**kwargs):
        events["propagated"].append(kwargs)
        yield

    def fake_run_current_agent(arxiv_url, **kwargs):
        events["agent_calls"].append((arxiv_url, kwargs))
        return {
            "status": "completed",
            "task_id": kwargs["task_id"],
            "summary": "private-sized summary",
            "comparison": "private-sized comparison",
            "reason": None,
            "steps_used": 3,
            "step_budget": kwargs["max_graph_steps"],
        }

    fake_langfuse = SimpleNamespace(
        update_current_span=lambda **kwargs: events["span_updates"].append(kwargs),
    )
    namespace = observability_namespace(
        read(page),
        {
            "AgentResult": dict,
            "CallbackHandler": lambda: handler,
            "langfuse": fake_langfuse,
            "observe": lambda **kwargs: (lambda function: function),
            "propagate_attributes": fake_propagate_attributes,
            "run_current_agent": fake_run_current_agent,
        },
    )
    result = namespace["run_paper_agent"](
        "https://arxiv.org/abs/2210.03629",
        task_id="task-42",
        max_graph_steps=6,
    )

    assert result["comparison"] == "private-sized comparison"
    assert events["agent_calls"] == [
        (
            "https://arxiv.org/abs/2210.03629",
            {
                "task_id": "task-42",
                "max_graph_steps": 6,
                "callbacks": [handler],
            },
        )
    ]
    assert events["propagated"] == [
        {
            "trace_name": "Paper Summary Bot",
            "metadata": {"task_id": "task-42", "data_class": "public-arxiv"},
        }
    ]
    assert events["span_updates"] == [
        {"metadata": {"task_id": "task-42", "status": "completed", "reason": "none"}}
    ]
    root_metadata = events["span_updates"][0]["metadata"]
    assert "summary" not in root_metadata and "comparison" not in root_metadata


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_stage7_teaches_outcome_trajectory_and_safe_resume(locale: str, page: Path) -> None:
    text = read(page)
    section = text[text.index(HEADINGS[locale][1]) : text.index(HEADINGS[locale][2])]
    positions = []
    for term in ("Eval", "Observability", "Human Approval", "Checkpoint", "Idempotency"):
        marker = f"**{term}"
        assert marker in section
        positions.append(section.index(marker))
    assert positions == sorted(positions)
    assert "20" in section and "Outcome" in section and "Trajectory" in section
    for count in ("| 5 |",):
        assert section.count(count) == 4
    for state_field in (
        '"task_id"',
        '"status"',
        '"checkpoint"',
        '"requested_action"',
        '"idempotency_key"',
        '"result_ref"',
        '"approved_by"',
    ):
        assert state_field in section
    assert "needs_review" in section
    assert "ledger" in section
    assert SAFE_EXAMPLE_LINKS[locale] in section
    assert section.index("### 7.1") < section.index("### 7.2") < section.index("### 7.3") < section.index("### 7.4")


@pytest.mark.parametrize("locale,page", PAGES.items())
def test_deploy_and_stage8_keep_the_smallest_safe_interface(locale: str, page: Path) -> None:
    text = read(page)
    for marker in (
        "USER 10001",
        "--read-only",
        "--tmpfs /tmp",
        "PAPER_MEMORY_PATH=/data/paper_memory",
        "paper-summary-memory",
        "paper-summary-model-cache",
        "dst=/data/paper_memory",
        "dst=/home/appuser/.cache/chroma",
        "127.0.0.1:8000:8000",
        "API",
        "Fetch",
        "Browser Use",
        "Computer Use",
        "Sandbox",
        "needs_review",
        STAGE8_LINKS[locale],
    ):
        assert marker in text, (locale, marker)
    for smoke_marker in (
        "# smoke_fake_request.py",
        "from fastapi.testclient import TestClient",
        'main.run_paper_agent = fake_agent',
        'collection.get(ids=["smoke-paper"])["ids"] == ["smoke-paper"]',
        "paper-summary-bot python smoke_fake_request.py",
        'print("smoke request: PASS")',
    ):
        assert smoke_marker in text
    assert text.count("src=paper-summary-memory,dst=/data/paper_memory") == 1
    assert text.count("src=paper-summary-model-cache,dst=/home/appuser/.cache/chroma") == 2
    assert "--mount type=volume,dst=/data/paper_memory" in text
    assert "mkdir -p /home/appuser/.cache/chroma" in text


def test_freshness_fact_pack_matches_the_walkthrough_contract() -> None:
    config = yaml.safe_load((ROOT / "scripts/freshness-models.yml").read_text(encoding="utf-8"))
    pack = config["walkthrough_fact_pack"]
    assert pack["canonical"] == "walkthroughs/build-first-agent-in-7-steps.md"
    assert pack["verified_on"] == "2026-08-31"
    assert pack["scope"] == [
        "models",
        "frameworks",
        "evals",
        "observability",
        "human-approval",
        "interfaces",
    ]
    assert set(pack["official_sources"].values()) <= set(external_urls(read(PAGES["zh-TW"]))) | {
        "https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions",
        "https://docs.langchain.com/oss/python/migrate/langgraph-v1",
        "https://docs.langchain.com/oss/python/langchain/agents",
    }

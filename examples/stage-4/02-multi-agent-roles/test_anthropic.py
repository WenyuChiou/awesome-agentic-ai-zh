"""Offline Path B checks for CrewAI's Anthropic provider and the same handoff."""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import build_crew, simulate_handoff
from starter_anthropic import MODEL


def test_pinned_anthropic_provider_and_structure() -> None:
    assert MODEL == "anthropic/claude-haiku-4-5-20251001"
    crew = build_crew("react", llm_model=MODEL)
    assert [agent.role for agent in crew.agents] == ["Researcher", "Writer", "Critic"]
    assert len(crew.tasks[2].context) == 2


def test_anthropic_path_offline_handoff_behavior() -> None:
    result = simulate_handoff("langgraph")
    assert "LangGraph" in result["research"]
    assert result["verdict"] == "PASS"
    assert "max_iter=4" in result["stop_condition"]


if __name__ == "__main__":
    test_pinned_anthropic_provider_and_structure()
    test_anthropic_path_offline_handoff_behavior()
    print("all pass")

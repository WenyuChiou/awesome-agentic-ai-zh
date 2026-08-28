"""Offline CrewAI comparison checks; no crew kickoff or network call."""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_crewai import build_crew, search_knowledge_base


def test_offline_search_and_visible_crewai_structure() -> None:
    assert "Taipei" in search_knowledge_base("Taipei")
    assert "no entry" in search_knowledge_base("unknown")
    crew = build_crew("summarize Taipei")
    assert [agent.role for agent in crew.agents] == ["Researcher"]
    assert len(crew.tasks) == 1
    assert crew.tasks[0].agent.role == "Researcher"


if __name__ == "__main__":
    test_offline_search_and_visible_crewai_structure()
    print("all pass")

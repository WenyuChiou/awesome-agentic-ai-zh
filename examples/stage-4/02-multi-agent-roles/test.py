"""Offline Path A checks for the handoff behavior and real CrewAI structure."""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from crewai import Process
from starter import build_crew, simulate_handoff


def test_offline_research_writer_critic_handoff() -> None:
    result = simulate_handoff("react")
    assert result["input"] == "react"
    assert "ReAct" in result["research"]
    assert result["research"] in result["draft"]
    assert result["verdict"] == "PASS"
    assert result["stop_condition"] == "Three fixed roles; each Agent has max_iter=4."


def test_crewai_sequential_context_structure() -> None:
    crew = build_crew("react")
    assert crew.process == Process.sequential
    assert [agent.role for agent in crew.agents] == ["Researcher", "Writer", "Critic"]
    assert len(crew.tasks) == 3
    assert crew.tasks[1].context == [crew.tasks[0]]
    assert crew.tasks[2].context == [crew.tasks[0], crew.tasks[1]]
    assert all(agent.max_iter == 4 for agent in crew.agents)


if __name__ == "__main__":
    test_offline_research_writer_critic_handoff()
    test_crewai_sequential_context_structure()
    print("all pass")

"""Path A 離線行為測試：真的走分支、暫停與恢復，但不連網。"""

from __future__ import annotations

import sys
from types import SimpleNamespace

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import build_graph, classify_node, run, should_search


class FakeLLM:
    """只回固定格式的假模型，讓圖的行為可以重複驗證。"""
    def invoke(self, prompt: str) -> SimpleNamespace:
        return SimpleNamespace(content=f"Draft grounded in: {prompt.splitlines()[-1]}")


def test_branch_choice_and_interrupt_resume() -> None:
    assert classify_node({"query": "latest Taipei population"})["needs_search"] is True
    assert should_search({"needs_search": False}) == "respond"
    graph = build_graph(FakeLLM())
    config = {"configurable": {"thread_id": "offline-approve"}}
    paused = graph.invoke({"query": "latest Taipei population"}, config=config)
    assert "__interrupt__" in paused
    checkpoint = graph.get_state(config)
    assert "Taipei population" in checkpoint.values["draft"]
    from langgraph.types import Command
    result = graph.invoke(Command(resume=True), config=config)
    assert result["final"].startswith("PUBLISHED:")


def test_rejection_uses_a_separate_checkpoint_thread() -> None:
    result = run("Explain Python", approve=False, llm=FakeLLM(), thread_id="offline-reject")
    assert result["final"].startswith("REJECTED:")
    assert "No lookup was needed" in result["draft"]


if __name__ == "__main__":
    test_branch_choice_and_interrupt_resume()
    test_rejection_uses_a_separate_checkpoint_thread()
    print("all pass")

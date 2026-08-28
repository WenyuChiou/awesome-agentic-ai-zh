"""Stage 4 練習 3：用 LangGraph 做條件分支與真正可暫停的 HITL。

流程像一條有岔路的軌道：先判斷要不要查資料，再請模型寫草稿，
接著用 ``interrupt()`` 停下來等人決定。只有收到 ``Command(resume=...)``
之後，圖才會繼續走到發布或拒絕。Path A 使用 Ollama；Path B 共用同一張圖。
"""

from __future__ import annotations

import os
import sys
from typing import Any, Literal

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from typing_extensions import TypedDict

MODEL = os.environ.get("MODEL", "qwen2.5:3b")


class State(TypedDict, total=False):
    query: str
    needs_search: bool
    search_result: str
    draft: str
    approved: bool
    final: str


def classify_node(state: State) -> dict[str, bool]:
    """用幾個示範關鍵字決定要不要先走離線查詢節點。"""
    query = state["query"].lower()
    return {"needs_search": any(word in query for word in ("population", "weather", "latest", "人口", "天氣", "最新"))}


def search_node(state: State) -> dict[str, str]:
    """從很小的離線資料表取值；這裡不代表真正的搜尋引擎。"""
    for key, value in {"taipei": "Taipei population: about 2.6 million.", "台北": "Taipei population: about 2.6 million.", "weather": "Demo weather: sunny, 25 C."}.items():
        if key in state["query"].lower():
            return {"search_result": value}
    return {"search_result": "No matching entry in the offline knowledge base."}


def should_search(state: State) -> Literal["search", "respond"]:
    return "search" if state["needs_search"] else "respond"


def make_ollama_llm() -> ChatOpenAI:
    """用 OpenAI-compatible 介面連到本機 Ollama。"""
    return ChatOpenAI(model=MODEL, base_url="http://localhost:11434/v1", api_key="ollama", temperature=0)


def build_graph(llm: Any, checkpointer: Any | None = None) -> Any:
    """建立共用圖；呼叫端可放入 Ollama 或 Anthropic chat model。"""
    def respond_node(state: State) -> dict[str, str]:
        context = state.get("search_result", "No lookup was needed.")
        message = llm.invoke(f"Write one cautious sentence for: {state['query']}\nOffline context: {context}")
        draft = str(getattr(message, "content", message)).strip()
        if not draft:
            raise RuntimeError("The model returned an empty draft.")
        return {"draft": draft}

    def review_node(state: State) -> dict[str, bool]:
        decision = interrupt({"action": "publish", "draft": state["draft"], "question": "Approve this draft?"})
        if not isinstance(decision, bool):
            raise ValueError("Human review must resume with true or false.")
        return {"approved": decision}

    def final_node(state: State) -> dict[str, str]:
        prefix = "PUBLISHED" if state["approved"] else "REJECTED"
        return {"final": f"{prefix}: {state['draft']}"}

    graph = StateGraph(State)
    graph.add_node("classify", classify_node)
    graph.add_node("search", search_node)
    graph.add_node("respond", respond_node)
    graph.add_node("review", review_node)
    graph.add_node("final", final_node)
    graph.add_edge(START, "classify")
    graph.add_conditional_edges("classify", should_search, {"search": "search", "respond": "respond"})
    graph.add_edge("search", "respond")
    graph.add_edge("respond", "review")
    graph.add_edge("review", "final")
    graph.add_edge("final", END)
    return graph.compile(checkpointer=checkpointer or InMemorySaver())


def run(query: str, approve: bool, llm: Any | None = None, thread_id: str = "stage4-demo") -> dict[str, Any]:
    """先跑到人工審核點，再用同一個 ``thread_id`` 恢復執行。"""
    graph = build_graph(llm or make_ollama_llm())
    config = {"configurable": {"thread_id": thread_id}}
    paused = graph.invoke({"query": query}, config=config)
    if "__interrupt__" not in paused:
        raise RuntimeError("Expected a human-review interrupt before publication.")
    resumed = graph.invoke(Command(resume=approve), config=config)
    if not resumed.get("final"):
        raise RuntimeError("The workflow did not produce a final result after resume.")
    return resumed


if __name__ == "__main__":
    approved = run("What is the Taipei population?", approve=True)
    rejected = run("Explain Python", approve=False, thread_id="stage4-reject")
    print(approved["final"])
    print(rejected["final"])
    assert approved["final"].startswith("PUBLISHED:")
    assert rejected["final"].startswith("REJECTED:")

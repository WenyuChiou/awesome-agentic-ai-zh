"""Stage 4 練習 1：同一個 agent、兩個 framework — LangGraph + Ollama（Path A、默認）。

任務：搜尋 + 摘要的小 agent。給一個 query、agent 用 search tool 拿資料、回一段摘要。
這份用 LangGraph。對照的 CrewAI 版本見 starter_crewai.py。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter.py

驗證：
    python test.py

模型 API 預算：$0（Ollama）；本機硬體與電力仍有成本。對照 Anthropic 版見 starter_anthropic.py。
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

MODEL = os.environ.get("MODEL", "qwen2.5:3b")


# === Tool ===

@tool
def search(query: str) -> str:
    """Search a (fake, offline) knowledge base for a topic."""
    db = {
        "taipei": "Taipei is the capital of Taiwan, population ~2.6M, known for night markets.",
        "react agent": "ReAct (Reasoning + Acting) is an agent pattern: think → act → observe loop.",
    }
    return db.get(query.strip().lower(), f"no entry for {query}")


# === LangGraph 狀態定義 ===

class State(TypedDict):
    messages: Annotated[list, add_messages]


def build_graph(llm: Any) -> Any:
    """組一個 search → summarize 的圖：LLM 看 query 決定要不要呼叫 search、看到 tool result 後給摘要。"""
    llm_with_tools = llm.bind_tools([search])

    def agent_node(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    def tool_node(state: State):
        msg = state["messages"][-1]
        results = []
        for call in msg.tool_calls:
            name = call.get("name")
            args = call.get("args")
            if name != "search":
                raise ValueError(f"Unknown tool: {name!r}")
            if not isinstance(args, dict) or set(args) != {"query"} or not isinstance(args["query"], str):
                raise ValueError("search needs exactly one string query.")
            obs = search.invoke(args)
            results.append(ToolMessage(content=obs, tool_call_id=call["id"]))
        return {"messages": results}

    def should_continue(state: State) -> str:
        return "tools" if state["messages"][-1].tool_calls else END

    g = StateGraph(State)
    g.add_node("agent", agent_node)
    g.add_node("tools", tool_node)
    g.set_entry_point("agent")
    g.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    g.add_edge("tools", "agent")
    return g.compile()


def run(query: str, llm: Any = None) -> dict:
    """Public entrypoint: 跑一輪 agent、回傳 final message + steps。"""
    llm = llm or ChatOpenAI(
        base_url="http://localhost:11434/v1", api_key="ollama",
        model=MODEL, temperature=0,
    )
    graph = build_graph(llm)
    final_state = graph.invoke({"messages": [HumanMessage(content=query)]}, config={"recursion_limit": 6})
    return {
        "final": final_state["messages"][-1].content,
        "steps": len(final_state["messages"]),
    }


if __name__ == "__main__":
    query = "summarize what you know about Taipei"
    print(f"❓ Query: {query}（using Ollama {MODEL}）")
    print("-" * 60)
    result = run(query)
    print(f"✅ Final: {result['final']}")
    print(f"   Steps: {result['steps']}")
    assert result["final"], "expected non-empty summary"
    assert result["steps"] >= 2, "expected a visible graph trace"
    print("✅ 練習 1 通過 — LangGraph + Ollama qwen2.5:3b、模型 API $0")

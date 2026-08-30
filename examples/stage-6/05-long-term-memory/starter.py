"""Stage 6 練習 5：Long-term memory — Path A（Ollama + ChromaDB、$0）。

Agent 跨多輪對話記得事情。實作：每輪結束、把使用者說過的「事實」存進 vector store；
下一輪先 retrieve 相關 memory、塞進 prompt。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter.py

驗證：
    python test.py
"""

from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:3b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")


# === Memory store ===

class MemoryStore:
    """Long-term memory backed by ChromaDB vector search."""

    def __init__(
        self,
        path: str | Path = ".stage06-memory",
        collection_name: str = "memory",
        *,
        client: Any = None,
        embedding_function: Any = None,
    ):
        """Open a disk-backed memory store; inject a client in unit tests."""
        self.path = Path(path)
        if client is None:
            import chromadb
            client = chromadb.PersistentClient(path=str(self.path))
        if embedding_function is None:
            from chromadb.utils import embedding_functions
            embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
            )
        self.collection = client.get_or_create_collection(
            name=collection_name, embedding_function=embedding_function,
        )

    def remember(self, fact: str) -> str:
        """Add a fact to memory. Returns the memory id."""
        existing = self.collection.get()
        for memory_id, document in zip(existing.get("ids", []), existing.get("documents", [])):
            if document == fact:
                return memory_id
        mid = str(uuid.uuid4())
        self.collection.add(ids=[mid], documents=[fact])
        return mid

    def recall(self, query: str, top_k: int = 3) -> list[str]:
        """Retrieve top-k relevant memories."""
        if self.collection.count() == 0:
            return []
        result = self.collection.query(
            query_texts=[query], n_results=min(top_k, self.collection.count()),
        )
        return result["documents"][0]

    def all(self) -> list[str]:
        return self.collection.get()["documents"]


# === Conversational agent with memory ===

def chat(user_msg: str, memory: MemoryStore, llm: Any = None, history: list = None) -> dict:
    """One conversation turn with memory recall + storage."""
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    history = history or []

    # 1. Recall relevant memories
    memories = memory.recall(user_msg, top_k=3)
    memory_text = "\n".join(f"- {m}" for m in memories) if memories else "(no relevant memories)"

    # 2. Build prompt with memory context
    system = f"""You are a helpful assistant with long-term memory. Use the relevant memories below to personalize answers.

Relevant memories:
{memory_text}
"""
    messages = [{"role": "system", "content": system}] + history + [{"role": "user", "content": user_msg}]

    # 3. LLM responds
    resp = llm.chat.completions.create(model=MODEL, messages=messages)
    answer = resp.choices[0].message.content or ""

    return {"answer": answer, "recalled": memories, "user_msg": user_msg}


def maybe_remember_fact(user_msg: str, memory: MemoryStore) -> str | None:
    """Heuristic: if user says 'I am / I like / I live', store as a fact."""
    triggers = ["I am ", "I like ", "I live ", "My favorite ", "I work ", "I prefer "]
    for t in triggers:
        if t.lower() in user_msg.lower():
            mid = memory.remember(user_msg)
            return mid
    return None


if __name__ == "__main__":
    memory = MemoryStore()

    # Turn 1: user shares facts (these go into memory)
    turn1 = "I live in Taipei and I prefer Python over JavaScript."
    print(f"\n[Turn 1] user: {turn1}")
    fact_id = maybe_remember_fact(turn1, memory)
    if fact_id:
        print(f"   (remembered as {fact_id[:8]}...)")

    # Turn 2: an unrelated question (memory still benign)
    r2 = chat("What's 2 + 2?", memory)
    print(f"\n[Turn 2] user: {r2['user_msg']}")
    print(f"   recalled: {r2['recalled']}")
    print(f"   answer: {r2['answer']}")

    # Turn 3: user asks for a recommendation — memory should kick in
    r3 = chat("Recommend a programming language for me to learn.", memory)
    print(f"\n[Turn 3] user: {r3['user_msg']}")
    print(f"   recalled: {r3['recalled']}")
    print(f"   answer: {r3['answer']}")

    # === 自我驗證 ===
    assert any("Python" in m for m in r3["recalled"]), \
        f"預期 recall 到 Python preference、得到 {r3['recalled']}"
    assert memory.collection.count() >= 1, "記憶應已寫進磁碟資料庫"
    print("\n✅ 練習 5 通過 — long-term memory 跨輪 retrieve 成功、$0/run")

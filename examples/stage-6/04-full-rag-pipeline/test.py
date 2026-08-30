"""Stage 6 練習 4 自我驗證 — 用 mock LLM 跑完整 RAG pipeline。
"""

from __future__ import annotations

import re
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import KB_DOC, build_kb, chunk_doc, generate, rag, retrieve


class FakeCollection:
    def __init__(self):
        self.rows: dict[str, str] = {}

    def add(self, ids, documents):
        self.rows.update(dict(zip(ids, documents)))

    def query(self, query_texts, n_results):
        words = set(re.findall(r"[a-z0-9.]+", query_texts[0].lower()))
        aliases = {"version": "python", "days": "vacation", "remote": "remote"}
        words |= {aliases[word] for word in words if word in aliases}
        ranked = sorted(
            self.rows.values(),
            key=lambda text: len(words & set(re.findall(r"[a-z0-9.]+", text.lower()))),
            reverse=True,
        )[:n_results]
        return {"documents": [ranked]}


class FakeClient:
    def __init__(self):
        self.collections: dict[str, FakeCollection] = {}

    def get_or_create_collection(self, name, embedding_function=None):
        return self.collections.setdefault(name, FakeCollection())


def fake_kb():
    return build_kb(KB_DOC, client=FakeClient(), embedding_function=lambda rows: rows)


def test_build_kb_uses_fresh_collection_by_default():
    client = FakeClient()
    first = build_kb(KB_DOC, client=client, embedding_function=lambda rows: rows)
    second = build_kb("# Different\n\nA different document.", client=client, embedding_function=lambda rows: rows)
    assert first is not second
    print("✅ test_build_kb_uses_fresh_collection_by_default")


def make_mock_llm(answer: str = "Mock answer."):
    llm = MagicMock()
    msg = SimpleNamespace(content=answer)
    choice = SimpleNamespace(message=msg)
    llm.chat.completions.create.return_value = SimpleNamespace(choices=[choice])
    return llm


def test_chunk_doc_produces_sections():
    chunks = chunk_doc(KB_DOC)
    # Sample has 4 ## sections + 1 # title → expect 5
    assert len(chunks) == 5, f"預期 5 個 chunk、得到 {len(chunks)}"
    print("✅ test_chunk_doc_produces_sections")


def test_retrieve_finds_relevant_section():
    collection = fake_kb()
    contexts = retrieve(collection, "vacation days", top_k=1)
    assert "15 days" in contexts[0], f"預期含 '15 days'、得到 {contexts[0]}"
    print("✅ test_retrieve_finds_relevant_section")


def test_generate_uses_context():
    llm = make_mock_llm("You get 15 days of vacation per year.")
    contexts = ["Full-time employees get 15 days of paid vacation."]
    answer = generate("How many vacation days?", contexts, llm=llm)
    # 確認 prompt 帶上了 context（mock 看 create() 收到的 messages）
    call_args = llm.chat.completions.create.call_args
    prompt = call_args.kwargs["messages"][0]["content"]
    assert "15 days" in prompt, "預期 prompt 含 context"
    assert "How many vacation days?" in prompt
    assert "15 days" in answer
    print("✅ test_generate_uses_context")


def test_rag_full_pipeline_with_mock_llm():
    llm = make_mock_llm("Python 3.11+.")
    result = rag("What Python version?", llm=llm, collection=fake_kb())
    assert result["query"] == "What Python version?"
    assert len(result["contexts"]) > 0
    assert "Python 3.11" in result["answer"]
    print("✅ test_rag_full_pipeline_with_mock_llm")


def test_rag_top_k_retrieval():
    """確認 retrieve 真的拿了 top_k 個 chunk。"""
    llm = make_mock_llm("Answer.")
    result = rag("vacation", llm=llm, top_k=3, collection=fake_kb())
    assert len(result["contexts"]) == 3
    print("✅ test_rag_top_k_retrieval")


if __name__ == "__main__":
    test_chunk_doc_produces_sections()
    test_build_kb_uses_fresh_collection_by_default()
    test_retrieve_finds_relevant_section()
    test_generate_uses_context()
    test_rag_full_pipeline_with_mock_llm()
    test_rag_top_k_retrieval()
    print("\n🎉 全部通過 — RAG pipeline 完整邏輯正確")

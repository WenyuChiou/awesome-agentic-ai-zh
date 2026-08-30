"""Stage 6 練習 5 自我驗證 — MemoryStore + maybe_remember_fact 邏輯。
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import MemoryStore, chat, maybe_remember_fact


class FakeCollection:
    def __init__(self):
        self.rows: dict[str, str] = {}

    def count(self):
        return len(self.rows)

    def add(self, ids, documents):
        self.rows.update(dict(zip(ids, documents)))

    def get(self):
        return {"ids": list(self.rows), "documents": list(self.rows.values())}

    def query(self, query_texts, n_results):
        words = set(re.findall(r"[a-z]+", query_texts[0].lower()))
        aliases = {"language": "python", "programming": "python", "recommend": "prefer"}
        words |= {aliases[word] for word in words if word in aliases}
        ranked = sorted(
            self.rows.values(),
            key=lambda text: len(words & set(re.findall(r"[a-z]+", text.lower()))),
            reverse=True,
        )[:n_results]
        return {"documents": [ranked]}


class FakeClient:
    def __init__(self):
        self.collections: dict[str, FakeCollection] = {}

    def get_or_create_collection(self, name, embedding_function=None):
        return self.collections.setdefault(name, FakeCollection())


FAKE_CLIENT = FakeClient()


class TinyEmbeddingFunction:
    """Small deterministic embedding function for the real persistence check."""

    def __call__(self, input):
        vectors = []
        for text in input:
            lowered = text.lower()
            vectors.append([
                float("python" in lowered),
                float("taipei" in lowered),
                float("language" in lowered or "prefer" in lowered),
                1.0,
            ])
        return vectors

    @staticmethod
    def name():
        return "stage06-tiny-test"

    def get_config(self):
        return {}

    @staticmethod
    def build_from_config(config):
        return TinyEmbeddingFunction()


def fresh_memory():
    """每個 test 用獨立 collection，不下載 embedding model。"""
    name = f"test_{len(FAKE_CLIENT.collections)}"
    return MemoryStore(
        collection_name=name,
        client=FAKE_CLIENT,
        embedding_function=lambda rows: rows,
    )


def make_mock_llm(answer: str = "ok"):
    llm = MagicMock()
    msg = SimpleNamespace(content=answer)
    llm.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=msg)]
    )
    return llm


def test_memory_remember_and_recall():
    mem = fresh_memory()
    mem.remember("User prefers Python over JavaScript.")
    mem.remember("User lives in Taipei.")
    mem.remember("Bananas are yellow.")  # unrelated

    recalled = mem.recall("what programming language does the user like", top_k=2)
    assert any("Python" in m for m in recalled), f"預期 recall Python、得到 {recalled}"
    print("✅ test_memory_remember_and_recall")


def test_memory_empty_recall():
    mem = fresh_memory()
    assert mem.recall("anything") == []
    print("✅ test_memory_empty_recall")


def test_reopening_same_store_keeps_memory():
    client = FakeClient()
    first = MemoryStore(client=client, embedding_function=lambda rows: rows)
    first.remember("User lives in Taipei.")
    reopened = MemoryStore(client=client, embedding_function=lambda rows: rows)
    assert "User lives in Taipei." in reopened.all()
    print("✅ test_reopening_same_store_keeps_memory")


def test_persistent_store_survives_new_process():
    with tempfile.TemporaryDirectory(prefix="stage06-memory-") as temp_dir:
        child_code = textwrap.dedent(
            """
            import sys
            from starter import MemoryStore

            class TinyEmbeddingFunction:
                def __call__(self, input):
                    return [[float('python' in text.lower()), 0.0, 1.0, 1.0] for text in input]
                @staticmethod
                def name():
                    return 'stage06-tiny-test'
                def get_config(self):
                    return {}
                @staticmethod
                def build_from_config(config):
                    return TinyEmbeddingFunction()

            memory = MemoryStore(path=sys.argv[1], embedding_function=TinyEmbeddingFunction())
            if sys.argv[2] == 'write':
                memory.remember('User prefers Python.')
            else:
                assert 'User prefers Python.' in memory.all()
            """
        )
        for action in ("write", "read"):
            result = subprocess.run(
                [sys.executable, "-c", child_code, temp_dir, action],
                cwd=Path(__file__).parent,
                capture_output=True,
                text=True,
                timeout=30,
            )
            assert result.returncode == 0, result.stderr
    print("✅ test_persistent_store_survives_new_process")


def test_remember_deduplicates_exact_fact():
    mem = fresh_memory()
    first_id = mem.remember("User prefers Python.")
    second_id = mem.remember("User prefers Python.")
    assert first_id == second_id
    assert mem.collection.count() == 1
    print("✅ test_remember_deduplicates_exact_fact")


def test_maybe_remember_fact_triggers_on_self_statements():
    mem = fresh_memory()
    fid = maybe_remember_fact("I live in Taipei", mem)
    assert fid is not None
    assert mem.collection.count() == 1
    print("✅ test_maybe_remember_fact_triggers_on_self_statements")


def test_maybe_remember_fact_skips_non_self_statements():
    mem = fresh_memory()
    fid = maybe_remember_fact("What's the weather?", mem)
    assert fid is None
    assert mem.collection.count() == 0
    print("✅ test_maybe_remember_fact_skips_non_self_statements")


def test_chat_uses_memory_in_prompt():
    """chat 應該把 recalled memory 塞進 system prompt。"""
    mem = fresh_memory()
    mem.remember("User prefers Python over JavaScript.")

    llm = make_mock_llm("I recommend Python.")
    result = chat("Recommend a programming language.", mem, llm=llm)

    # mock 看 create() 收到的 messages
    call_args = llm.chat.completions.create.call_args
    system_msg = call_args.kwargs["messages"][0]["content"]
    assert "Python over JavaScript" in system_msg, "system prompt 應含 memory"
    assert "Python" in result["recalled"][0]
    print("✅ test_chat_uses_memory_in_prompt")


if __name__ == "__main__":
    test_memory_remember_and_recall()
    test_memory_empty_recall()
    test_reopening_same_store_keeps_memory()
    test_persistent_store_survives_new_process()
    test_remember_deduplicates_exact_fact()
    test_maybe_remember_fact_triggers_on_self_statements()
    test_maybe_remember_fact_skips_non_self_statements()
    test_chat_uses_memory_in_prompt()
    print("\n🎉 全部通過 — long-term memory 邏輯正確")

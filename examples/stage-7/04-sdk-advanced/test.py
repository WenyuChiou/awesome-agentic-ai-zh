"""Stage 7 練習 4 自我驗證 — streaming + stream_to_string。"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import stream_response, stream_to_string


def fake_streaming_llm(chunks: list[str]):
    """Mock OpenAI streaming response — iterable of chunks."""
    def make_chunk(delta):
        return SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=delta))])
    llm = MagicMock()
    llm.chat.completions.create.return_value = iter([make_chunk(c) for c in chunks])
    return llm


def test_stream_response_yields_chunks():
    llm = fake_streaming_llm(["Hello", " ", "world"])
    out = list(stream_response("hi", llm=llm))
    assert out == ["Hello", " ", "world"]
    print("✅ test_stream_response_yields_chunks")


def test_stream_to_string_aggregates():
    llm = fake_streaming_llm(["a", "b", "c"])
    result = stream_to_string("q", llm=llm)
    assert result["text"] == "abc"
    assert result["chunk_count"] == 3
    print("✅ test_stream_to_string_aggregates")


def test_stream_to_string_skips_empty_deltas():
    """Streaming 偶爾有 None delta（initial / final chunk）、要 skip。"""
    def make_chunk(delta):
        return SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=delta))])
    llm = MagicMock()
    llm.chat.completions.create.return_value = iter([
        make_chunk(None), make_chunk("a"), make_chunk(""), make_chunk("b"), make_chunk(None),
    ])
    result = stream_to_string("q", llm=llm)
    assert result["text"] == "ab"
    print("✅ test_stream_to_string_skips_empty_deltas")


def test_stream_rejects_an_all_empty_response():
    llm = fake_streaming_llm(["", None])
    try:
        list(stream_response("q", llm=llm))
    except ValueError as error:
        assert "empty text" in str(error)
    else:
        raise AssertionError("empty stream must fail")
    print("✅ test_stream_rejects_an_all_empty_response")


def test_stream_rejects_whitespace_only_chunks():
    llm = fake_streaming_llm([" ", "\t"])
    try:
        list(stream_response("q", llm=llm))
    except ValueError as error:
        assert "empty text" in str(error)
    else:
        raise AssertionError("whitespace-only stream must fail")
    print("✅ test_stream_rejects_whitespace_only_chunks")


if __name__ == "__main__":
    test_stream_response_yields_chunks()
    test_stream_to_string_aggregates()
    test_stream_to_string_skips_empty_deltas()
    test_stream_rejects_an_all_empty_response()
    test_stream_rejects_whitespace_only_chunks()
    print("\n🎉 全部通過 — streaming 邏輯正確")

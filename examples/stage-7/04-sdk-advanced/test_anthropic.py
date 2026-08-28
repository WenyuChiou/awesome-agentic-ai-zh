"""Stage 7 練習 4 — Anthropic streaming + cached_query mock."""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_anthropic import build_cache_demo_prompt, cached_query, stream_anthropic


def test_stream_anthropic_yields_text():
    """Mock Anthropic streaming context manager."""
    stream_obj = MagicMock()
    stream_obj.text_stream = iter(["Hello", " world"])
    stream_obj.__enter__ = MagicMock(return_value=stream_obj)
    stream_obj.__exit__ = MagicMock(return_value=False)

    client = MagicMock()
    client.messages.stream.return_value = stream_obj

    out = list(stream_anthropic("hi", client=client))
    assert out == ["Hello", " world"]
    print("✅ test_stream_anthropic_yields_text")


def test_stream_anthropic_rejects_whitespace_only_chunks():
    stream_obj = MagicMock()
    stream_obj.text_stream = iter([" ", "\t"])
    stream_obj.__enter__ = MagicMock(return_value=stream_obj)
    stream_obj.__exit__ = MagicMock(return_value=False)
    client = MagicMock()
    client.messages.stream.return_value = stream_obj

    try:
        list(stream_anthropic("hi", client=client))
    except ValueError as error:
        assert "empty text" in str(error)
    else:
        raise AssertionError("whitespace-only stream must fail")
    print("✅ test_stream_anthropic_rejects_whitespace_only_chunks")


def test_cached_query_passes_cache_control():
    """確認 cache_control 真的傳進去 system param。"""
    client = MagicMock()
    client.messages.create.return_value = SimpleNamespace(
        content=[SimpleNamespace(type="text", text="ok")],
        usage=SimpleNamespace(
            input_tokens=10, output_tokens=2,
            cache_creation_input_tokens=2000, cache_read_input_tokens=0,
        ),
    )
    result = cached_query("Q?", "big system prompt", client=client)
    call_kwargs = client.messages.create.call_args.kwargs
    system_arg = call_kwargs["system"]
    assert isinstance(system_arg, list)
    assert system_arg[0]["cache_control"] == {"type": "ephemeral"}
    assert result["cache_creation_input_tokens"] == 2000
    print("✅ test_cached_query_passes_cache_control")


def test_cache_demo_is_deliberately_long():
    prompt = build_cache_demo_prompt()
    assert len(prompt.split()) > 6000
    print("✅ test_cache_demo_is_deliberately_long")


def test_cached_query_rejects_empty_text():
    client = MagicMock()
    client.messages.create.return_value = SimpleNamespace(
        content=[],
        usage=SimpleNamespace(
            input_tokens=10,
            output_tokens=0,
            cache_creation_input_tokens=0,
            cache_read_input_tokens=0,
        ),
    )
    try:
        cached_query("Q?", build_cache_demo_prompt(), client=client)
    except ValueError as error:
        assert "empty text" in str(error)
    else:
        raise AssertionError("empty cached response must fail")
    print("✅ test_cached_query_rejects_empty_text")


if __name__ == "__main__":
    test_stream_anthropic_yields_text()
    test_stream_anthropic_rejects_whitespace_only_chunks()
    test_cached_query_passes_cache_control()
    test_cache_demo_is_deliberately_long()
    test_cached_query_rejects_empty_text()
    print("\n🎉 通過 — streaming + caching API contract 正確")

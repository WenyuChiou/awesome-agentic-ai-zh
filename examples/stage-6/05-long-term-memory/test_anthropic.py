"""Stage 6 練習 5 — Path B mock test。
"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import MemoryStore
from test import FakeClient
from starter_anthropic import chat_anthropic


def test_chat_anthropic_uses_memory_in_system_prompt():
    mem = MemoryStore(client=FakeClient(), embedding_function=lambda rows: rows)
    mem.remember("User prefers Python.")

    client = MagicMock()
    block = SimpleNamespace(type="text", text="I recommend Python.")
    client.messages.create.return_value = SimpleNamespace(content=[block])

    result = chat_anthropic("Recommend a language.", mem, client=client)
    call_args = client.messages.create.call_args
    system_msg = call_args.kwargs["system"]
    assert "User prefers Python." in system_msg
    print("✅ test_chat_anthropic_uses_memory_in_system_prompt")


if __name__ == "__main__":
    test_chat_anthropic_uses_memory_in_system_prompt()
    print("\n🎉 Path B mock test 通過")

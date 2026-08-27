"""Path B tests: no API key and no network calls are required."""

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_anthropic import classify_anthropic


def test_anthropic_response_shape() -> None:
    client = MagicMock()
    client.messages.create.return_value = SimpleNamespace(
        content=[SimpleNamespace(type="text", text="billing")]
    )
    actual = classify_anthropic("發票上的金額不對", improved=True, client=client)
    assert actual == "billing"
    sent = client.messages.create.call_args.kwargs
    assert sent["model"]
    assert sent["max_tokens"] == 10
    assert "例子" in sent["messages"][0]["content"]
    print("PASS  Anthropic response is read correctly")


def test_anthropic_joins_text_blocks() -> None:
    client = MagicMock()
    client.messages.create.return_value = SimpleNamespace(
        content=[
            SimpleNamespace(type="thinking", thinking="hidden"),
            SimpleNamespace(type="text", text="other"),
        ]
    )
    assert classify_anthropic("謝謝你幫我處理", False, client) == "other"
    print("PASS  non-text blocks do not become the answer")


if __name__ == "__main__":
    test_anthropic_response_shape()
    test_anthropic_joins_text_blocks()
    print("\n2/2 passed — Path B prompt-eval loop is ready")

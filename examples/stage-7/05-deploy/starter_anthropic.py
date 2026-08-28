"""Stage 7 練習 5：Deploy — Path B（FastAPI + Anthropic）。

跟 starter.py 同 HTTP API、agent_call 改成 anthropic SDK。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    uvicorn starter_anthropic:app --reload --port 8000
    curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{"message": "hi"}'

費用請用實際 input/output tokens 乘上當期官方單價，不用固定猜測值。
"""

from __future__ import annotations

import logging
import os
import sys
import time
import uuid
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("agent.api")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    max_tokens: int = Field(default=300, ge=1, le=1000)

    @field_validator("message")
    @classmethod
    def message_must_contain_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("message must contain non-whitespace text")
        return value


class ChatResponse(BaseModel):
    request_id: str
    answer: str
    latency_ms: float
    model: str
    input_tokens: int
    output_tokens: int


class ModelOutputError(ValueError):
    """The upstream model returned no usable text."""


def require_text(value: str | None, label: str) -> str:
    text = (value or "").strip()
    if not text:
        raise ModelOutputError(f"{label} returned empty text")
    return text


def agent_call_anthropic(message: str, max_tokens: int, client: Any = None) -> dict:
    client = client or anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL, max_tokens=max_tokens,
        messages=[{"role": "user", "content": message}],
    )
    answer = require_text(" ".join(b.text for b in resp.content if b.type == "text"), "Anthropic")
    return {
        "answer": answer,
        "input_tokens": resp.usage.input_tokens,
        "output_tokens": resp.usage.output_tokens,
    }


app = FastAPI(title="Agent API (Anthropic)", version="0.1.0")


@app.get("/health")
def health():
    """Cheap process liveness check; it intentionally does not call the model."""
    return {"status": "ok", "model": MODEL}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    request_id = str(uuid.uuid4())
    t0 = time.perf_counter()
    logger.info(f"[{request_id}] chat request")
    try:
        result = agent_call_anthropic(req.message, req.max_tokens)
    except ModelOutputError as e:
        logger.warning(f"[{request_id}] upstream LLM returned empty text")
        raise HTTPException(status_code=502, detail="LLM returned no answer") from e
    except anthropic.APIConnectionError as e:
        logger.error(f"[{request_id}] upstream LLM unavailable")
        raise HTTPException(status_code=503, detail="LLM unavailable") from e
    except anthropic.RateLimitError as e:
        logger.warning(f"[{request_id}] upstream LLM rate limited the request")
        raise HTTPException(status_code=429, detail="Rate limited") from e
    except Exception as e:  # noqa: BLE001
        logger.error(
            f"[{request_id}] unexpected internal error type={type(e).__name__}"
        )
        raise HTTPException(status_code=500, detail="Internal error") from e

    latency_ms = (time.perf_counter() - t0) * 1000
    logger.info(f"[{request_id}] done in {latency_ms:.0f}ms, tokens={result['input_tokens']}+{result['output_tokens']}")
    return ChatResponse(
        request_id=request_id, answer=result["answer"],
        latency_ms=latency_ms, model=MODEL,
        input_tokens=result["input_tokens"], output_tokens=result["output_tokens"],
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

"""Stage 7 練習 5：Deploy — Path A（FastAPI + Ollama）。

把 agent 包進 FastAPI HTTP endpoint、production-style health check + structured logging。
本地端 `uvicorn starter:app` 就能跑、Docker / k8s / Lambda 都能 lift。

跑法：
    pip install -r requirements.txt
    ollama pull qwen3.5:4b
    ollama serve
    uvicorn starter:app --reload --port 8000
    # 另一個 shell: curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{"message": "hi"}'

驗證（不必啟 server）:
    python test.py
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

from fastapi import FastAPI, HTTPException
from openai import APIConnectionError, OpenAI, RateLimitError
from pydantic import BaseModel, Field, field_validator

MODEL = os.environ.get("MODEL", "qwen3.5:4b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("agent.api")


# === Schemas ===

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


class ModelOutputError(ValueError):
    """The upstream model returned no usable text."""


def require_text(value: str | None, label: str) -> str:
    text = (value or "").strip()
    if not text:
        raise ModelOutputError(f"{label} returned empty text")
    return text


# === Agent ===

def agent_call(message: str, max_tokens: int, llm: Any = None) -> str:
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    resp = llm.chat.completions.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": message}],
    )
    return require_text(resp.choices[0].message.content, "Ollama")


# === FastAPI app ===

app = FastAPI(title="Agent API", version="0.1.0")


@app.get("/health")
def health():
    """Cheap process liveness check; it intentionally does not call the model."""
    return {"status": "ok", "model": MODEL}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    request_id = str(uuid.uuid4())
    t0 = time.perf_counter()
    logger.info(f"[{request_id}] chat request received")
    try:
        answer = agent_call(req.message, req.max_tokens)
    except ModelOutputError as e:
        logger.warning(f"[{request_id}] upstream LLM returned empty text")
        raise HTTPException(status_code=502, detail="LLM returned no answer") from e
    except RateLimitError as e:
        logger.warning(f"[{request_id}] upstream LLM rate limited the request")
        raise HTTPException(status_code=429, detail="Rate limited") from e
    except APIConnectionError as e:
        logger.error(f"[{request_id}] upstream LLM unavailable")
        raise HTTPException(status_code=503, detail="LLM service unavailable") from e
    except Exception as e:  # noqa: BLE001
        logger.error(
            f"[{request_id}] unexpected internal error type={type(e).__name__}"
        )
        raise HTTPException(status_code=500, detail="Internal error") from e

    latency_ms = (time.perf_counter() - t0) * 1000
    logger.info(f"[{request_id}] chat done in {latency_ms:.0f}ms")
    return ChatResponse(
        request_id=request_id, answer=answer,
        latency_ms=latency_ms, model=MODEL,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

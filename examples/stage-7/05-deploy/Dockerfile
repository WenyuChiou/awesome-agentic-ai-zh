FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY starter.py starter_anthropic.py ./

RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app

EXPOSE 8000

USER appuser

CMD ["uvicorn", "starter:app", "--host", "0.0.0.0", "--port", "8000"]

# Build:
#   docker build -t agent-api .
# Run (Ollama path; needs ollama on host):
#   docker run --rm --read-only --tmpfs /tmp -p 127.0.0.1:8000:8000 -e OLLAMA_API_BASE=http://host.docker.internal:11434/v1 agent-api
# Run (Anthropic path):
#   docker run --rm --read-only --tmpfs /tmp -p 127.0.0.1:8000:8000 -e ANTHROPIC_API_KEY agent-api uvicorn starter_anthropic:app --host 0.0.0.0 --port 8000

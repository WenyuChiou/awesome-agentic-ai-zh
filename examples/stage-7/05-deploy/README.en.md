<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Core Exercise: Put an Agent Behind FastAPI and Docker

You will wrap one model call in two HTTP endpoints: `/health` says the service process is alive, while `/chat` accepts a question and returns an answer.

Pairs with Core Exercise 4 in [Stage 7 — Agent Production Engineering: Harness, Loops, and Graphs](../../../stages/07-multi-agent-production.en.md). Complete Eval, Observability, and Safe Execution first, then make the service available to others.

## 🎯 Learning goals

- Use **Pydantic** to reject blank or oversized text and excessive `max_tokens`.
- Separate **liveness** from real upstream readiness; the health check never calls a model.
- Reduce risk with a non-root container, loopback port, and read-only filesystem.

## Run the tests without starting a server

Open PowerShell in this folder and copy:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

Two `🎉` messages mean the offline tests cover 200, 422, 429, 502, 503, and input boundaries. TestClient opens no real network port.

<details markdown="1">
<summary>Path A: Start the Ollama API locally</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

Open another PowerShell window:

```powershell
.\.venv\Scripts\python.exe -m uvicorn starter:app --host 127.0.0.1 --port 8000
```

Open a third PowerShell window:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/chat `
  -ContentType "application/json" `
  -Body '{"message":"Explain an agent in one sentence.","max_tokens":100}'
```

Ollama does not charge a provider model API fee. Hardware, electricity, and time still have costs.

</details>

<details markdown="1">
<summary>Path B: Start the Anthropic API locally</summary>

```powershell
$env:ANTHROPIC_API_KEY = "paste-your-key"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe -m uvicorn starter_anthropic:app --host 127.0.0.1 --port 8000
```

Haiku 4.5 costs `$1 / 1M` input tokens and `$5 / 1M` output tokens:

```text
estimated cost = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

Set a `$1` provider spend limit first. Use returned input/output tokens for an estimate; do not turn one short prompt's cost into a permanent price.

</details>

## Five important terms

- **Endpoint**: one entry offered by a service, such as `POST /chat`.
- **Schema validation**: checks input shape and limits first; invalid input receives 422.
- **Liveness**: confirms the program is alive. This `/health` route performs only a cheap process check.
- **Request ID**: a tracking number for one request; logs store the ID, not the full prompt.
- **Non-root container**: the process is not the container administrator, reducing some possible damage.

| Situation | HTTP code | What the client should do |
|---|---:|---|
| Answer returned | 200 | use the answer |
| Input is missing or outside limits | 422 | fix the request; do not retry unchanged data |
| Provider rate limit | 429 | wait and follow `Retry-After` or backoff |
| Model returns an empty answer | 502 | record it, then retry a bounded number of times or ask a human |
| Upstream connection fails | 503 | retry later, with a limit |
| Unexpected program error | 500 | alert and fix the program |

## Change one thing

Send `max_tokens=1001` to `/chat`. Confirm that FastAPI returns 422 and never calls the model.

## Success check

- [ ] `/health` calls neither Ollama nor Anthropic.
- [ ] A blank message, 4,001 characters, and `max_tokens=1001` are rejected.
- [ ] Logs have a request ID but no full user prompt or API key.
- [ ] You know these Docker settings reduce risk; do not treat them as a sandbox.

<details markdown="1">
<summary>Start Docker with safer teaching defaults</summary>

```powershell
docker build -t stage7-agent-api .
```

Ollama Path A:

```powershell
docker run --rm --read-only --tmpfs /tmp `
  -p 127.0.0.1:8000:8000 `
  -e OLLAMA_API_BASE=http://host.docker.internal:11434/v1 `
  stage7-agent-api
```

Anthropic Path B:

```powershell
docker run --rm --read-only --tmpfs /tmp `
  -p 127.0.0.1:8000:8000 `
  -e ANTHROPIC_API_KEY=$env:ANTHROPIC_API_KEY `
  stage7-agent-api `
  uvicorn starter_anthropic:app --host 0.0.0.0 --port 8000
```

These settings provide a non-root user, loopback port, and read-only filesystem. Do not treat them as a sandbox; they do not add TLS, authentication, authorization, rate limiting, egress policy, or a secret manager.

</details>

<details markdown="1">
<summary>Production additions and common problems</summary>

- Add authentication, authorization, TLS, and rate limiting before exposing the service.
- Keep liveness cheap. If you need readiness, build a separate dependency check with a timeout and caching.
- Store API keys in a secret manager or protected environment variables, never in an image, program, or README.
- Set request-body, concurrency, timeout, retry, and daily token limits.
- For streaming, use SSE or WebSocket and handle interruption and cancellation.
- Scan the image and Python dependencies, then pin reproducible versions before production deployment.

</details>

## 📚 Required reading and learning resources

- ⭐⭐⭐⭐⭐ [FastAPI official tutorial](https://fastapi.tiangolo.com/tutorial/): primary documentation for schemas, errors, dependencies, and deployment.
- ⭐⭐⭐⭐⭐ [Dockerfile best practices](https://docs.docker.com/build/building/best-practices/): build smaller, updateable, non-root images.
- ⭐⭐⭐⭐⭐ [Docker port publishing](https://docs.docker.com/engine/network/port-publishing/): understand why `127.0.0.1:8000:8000` is more conservative than publishing on every interface.
- ⭐⭐⭐⭐ [`awesome-harness-engineering`](https://github.com/ai-boost/awesome-harness-engineering): explore additional harness patterns.
- ⭐⭐⭐⭐⭐ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents): chapter-style agent production background.

See the full list in [Stage 7 Featured Projects](../../../stages/07-multi-agent-production.en.md#-featured-projects-templates--sdks--tool-collections).

<small>Models, prices, packages, deployment documents, and links checked: 2026-08-28 UTC.</small>

<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 5：把 Agent 放进 FastAPI 与 Docker

你会把一个模型调用包成两个 HTTP endpoint：`/health` 说明服务还活着，`/chat` 接收问题并返回答案。

对应 [Stage 7 — Multi-Agent 与 Production](../../../stages/07-multi-agent-production.zh-Hans.md) 练习 5。

## 🎯 学习目标

- 用 **Pydantic** 挡住空白、过长文字与过大的 `max_tokens`。
- 分辨 **liveness** 与真正的上游 readiness；健康检查不调用模型。
- 用非 root container、loopback port 与 read-only filesystem 缩小风险。

## 先跑不开 Server 的测试

在这个文件夹打开 PowerShell，直接复制：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

看到两份 `🎉`，代表 200、422、429、502、503 与输入界线都有离线测试。TestClient 不会开真实网络 port。

<details markdown="1">
<summary>Path A：在本机启动 Ollama API</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

另开 PowerShell：

```powershell
.\.venv\Scripts\python.exe -m uvicorn starter:app --host 127.0.0.1 --port 8000
```

再开第三个 PowerShell：

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/chat `
  -ContentType "application/json" `
  -Body '{"message":"请用一句话解释 Agent。","max_tokens":100}'
```

Ollama 不收模型 API 费，但硬件、电力和时间仍有成本。

</details>

<details markdown="1">
<summary>Path B：在本机启动 Anthropic API</summary>

```powershell
$env:ANTHROPIC_API_KEY = "贴上你的金钥"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe -m uvicorn starter_anthropic:app --host 127.0.0.1 --port 8000
```

Haiku 4.5 的单价是 input `$1 / 1M` tokens、output `$5 / 1M` tokens：

```text
估算费用 = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

先在供应商 Console 设 `$1` spend limit。API 回复里的 input/output tokens 可用来估算，不要把短 Prompt 的固定金额写成永久价格。

</details>

## 五个重要词

- **Endpoint**：服务对外提供的一个入口，例如 `POST /chat`。
- **Schema validation**：先检查输入形状与范围，不合规就回 422。
- **Liveness**：程序还活着。这份 `/health` 只做便宜的程序检查。
- **Request ID**：一次请求的追踪号码；log 只记 ID，不记完整 Prompt。
- **Non-root container**：container 内的程序不是系统管理员，能减少部分伤害。

| 状况 | HTTP code | 调用端怎么做 |
|---|---:|---|
| 成功回答 | 200 | 使用答案 |
| 输入缺少或超出范围 | 422 | 修正 request，不要重试原数据 |
| 供应商限流 | 429 | 等候并依 `Retry-After`／backoff 重试 |
| 模型回空答案 | 502 | 记录并有限次重试或转人工 |
| 上游连接失败 | 503 | 稍后有限次重试 |
| 未预期的程序错误 | 500 | 告警并修程序 |

## 只改一件事

把 `max_tokens` 改成 `1001` 送到 `/chat`。确认 FastAPI 回 422，而且模型完全没有被调用。

## 成功检查

- [ ] `/health` 不会调用 Ollama 或 Anthropic。
- [ ] 空白 message、4,001 字符和 `max_tokens=1001` 都被拒绝。
- [ ] Log 有 request ID，但没有完整用户 Prompt 或 API key。
- [ ] 你知道 Docker 设置只能降低风险，并不是完整的 sandbox。

<details markdown="1">
<summary>用较安全的默认值启动 Docker</summary>

```powershell
docker build -t stage7-agent-api .
```

Ollama Path A：

```powershell
docker run --rm --read-only --tmpfs /tmp `
  -p 127.0.0.1:8000:8000 `
  -e OLLAMA_API_BASE=http://host.docker.internal:11434/v1 `
  stage7-agent-api
```

Anthropic Path B：

```powershell
docker run --rm --read-only --tmpfs /tmp `
  -p 127.0.0.1:8000:8000 `
  -e ANTHROPIC_API_KEY=$env:ANTHROPIC_API_KEY `
  stage7-agent-api `
  uvicorn starter_anthropic:app --host 0.0.0.0 --port 8000
```

这些设置提供非 root 用户、loopback port 和 read-only filesystem。仍不能把它们当成 sandbox，也不会替你加入 TLS、authentication、authorization、rate limit、egress policy 或 secret manager。

</details>

<details markdown="1">
<summary>Production 还要补什么、常见问题</summary>

- 对外服务先加 authentication、authorization、TLS 与 rate limit。
- liveness 保持便宜；若需要 readiness，另做有 timeout 和快取的依赖检查。
- API key 放 secret manager 或受保护的环境变数，不写进 image、程序或 README。
- 设定 request body、并发、timeout、重试与每日 token 上限。
- 需要 streaming 时，用 SSE／WebSocket 并处理中断与取消。
- 正式部署前扫描 image 与 Python dependencies，再锁定可重现版本。

</details>

<details markdown="1">
<summary>📚 深入学习资源与评分</summary>

- ⭐⭐⭐⭐⭐ [FastAPI 官方教学](https://fastapi.tiangolo.com/tutorial/)：schema、errors、dependencies 与部署的第一手文件。
- ⭐⭐⭐⭐⭐ [Dockerfile best practices](https://docs.docker.com/build/building/best-practices/)：创建较小、可更新且非 root 的 image。
- ⭐⭐⭐⭐⭐ [Docker port publishing](https://docs.docker.com/engine/network/port-publishing/)：理解为什么 `127.0.0.1:8000:8000` 比默认公开所有界面更保守。
- ⭐⭐⭐⭐ [`awesome-harness-engineering`](https://github.com/ai-boost/awesome-harness-engineering)：需要更多 harness pattern 时使用。
- ⭐⭐⭐⭐⭐ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：章节式 Agent production 背景。

完整清单见 [Stage 7 精选 Projects](../../../stages/07-multi-agent-production.zh-Hans.md#-精选-projects范本--sdk--工具-collection)。

<small>模型、价格、套件、部署文件与连结查核：2026-08-28 UTC。</small>

</details>

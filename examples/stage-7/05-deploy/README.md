<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 核心練習：把 Agent 放進 FastAPI 與 Docker

你會把一個模型呼叫包成兩個 HTTP endpoint：`/health` 說服務還活著，`/chat` 接收問題並回傳答案。

對應 [Stage 7 — Agent Production Engineering：Harness、Loop 與 Graph](../../../stages/07-multi-agent-production.md) 核心練習 4。先完成 Eval、Observability 與 Safe Execution，再把服務交給別人使用。

## 🎯 學習目標

- 用 **Pydantic** 擋住空白、過長文字與過大的 `max_tokens`。
- 分辨 **liveness** 與真正的上游 readiness；健康檢查不呼叫模型。
- 用非 root container、loopback port 與 read-only filesystem 縮小風險。

## 先跑不開 Server 的測試

在這個資料夾開 PowerShell，直接複製：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

看到兩份 `🎉`，代表 200、422、429、502、503 與輸入界線都有離線測試。TestClient 不會開真實網路 port。

<details markdown="1">
<summary>Path A：在本機啟動 Ollama API</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

另開 PowerShell：

```powershell
.\.venv\Scripts\python.exe -m uvicorn starter:app --host 127.0.0.1 --port 8000
```

再開第三個 PowerShell：

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/chat `
  -ContentType "application/json" `
  -Body '{"message":"請用一句話解釋 Agent。","max_tokens":100}'
```

Ollama 不收模型 API 費，但硬體、電力和時間仍有成本。

</details>

<details markdown="1">
<summary>Path B：在本機啟動 Anthropic API</summary>

```powershell
$env:ANTHROPIC_API_KEY = "貼上你的金鑰"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe -m uvicorn starter_anthropic:app --host 127.0.0.1 --port 8000
```

Haiku 4.5 的單價是 input `$1 / 1M` tokens、output `$5 / 1M` tokens：

```text
估算費用 = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

先在供應商 Console 設 `$1` spend limit。API 回覆裡的 input/output tokens 可用來估算，不要把短 Prompt 的固定金額寫成永久價格。

</details>

## 五個重要詞

- **Endpoint**：服務對外提供的一個入口，例如 `POST /chat`。
- **Schema validation**：先檢查輸入形狀與範圍，不合規就回 422。
- **Liveness**：程式還活著。這份 `/health` 只做便宜的程序檢查。
- **Request ID**：一次請求的追蹤號碼；log 只記 ID，不記完整 Prompt。
- **Non-root container**：container 內的程序不是系統管理員，能減少部分傷害。

| 狀況 | HTTP code | 呼叫端怎麼做 |
|---|---:|---|
| 成功回答 | 200 | 使用答案 |
| 輸入缺少或超出範圍 | 422 | 修正 request，不要重試原資料 |
| 供應商限流 | 429 | 等候並依 `Retry-After`／backoff 重試 |
| 模型回空答案 | 502 | 記錄並有限次重試或轉人工 |
| 上游連線失敗 | 503 | 稍後有限次重試 |
| 未預期的程式錯誤 | 500 | 告警並修程式 |

## 只改一件事

把 `max_tokens` 改成 `1001` 送到 `/chat`。確認 FastAPI 回 422，而且模型完全沒有被呼叫。

## 成功檢查

- [ ] `/health` 不會呼叫 Ollama 或 Anthropic。
- [ ] 空白 message、4,001 字元和 `max_tokens=1001` 都被拒絕。
- [ ] Log 有 request ID，但沒有完整使用者 Prompt 或 API key。
- [ ] 你知道 Docker 設定只是縮小風險，不能把它當成 sandbox。

<details markdown="1">
<summary>用較安全的預設值啟動 Docker</summary>

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

這些設定提供非 root、loopback port 與 read-only filesystem。仍不能把它當成 sandbox，也沒有替你加入 TLS、authentication、authorization、rate limit、egress policy 或 secret manager。

</details>

<details markdown="1">
<summary>Production 還要補什麼、常見問題</summary>

- 對外服務先加 authentication、authorization、TLS 與 rate limit。
- liveness 保持便宜；若需要 readiness，另做有 timeout 和快取的依賴檢查。
- API key 放 secret manager 或受保護的環境變數，不寫進 image、程式或 README。
- 設定 request body、併發、timeout、重試與每日 token 上限。
- 需要 streaming 時，用 SSE／WebSocket 並處理中斷與取消。
- 正式部署前掃描 image 與 Python dependencies，再鎖定可重現版本。

</details>

## 📚 必讀與學習資源

- ⭐⭐⭐⭐⭐ [FastAPI 官方教學](https://fastapi.tiangolo.com/tutorial/)：schema、errors、dependencies 與部署的第一手文件。
- ⭐⭐⭐⭐⭐ [Dockerfile best practices](https://docs.docker.com/build/building/best-practices/)：建立較小、可更新且非 root 的 image。
- ⭐⭐⭐⭐⭐ [Docker port publishing](https://docs.docker.com/engine/network/port-publishing/)：理解為什麼 `127.0.0.1:8000:8000` 比預設公開所有介面更保守。
- ⭐⭐⭐⭐ [`awesome-harness-engineering`](https://github.com/ai-boost/awesome-harness-engineering)：需要更多 harness pattern 時使用。
- ⭐⭐⭐⭐⭐ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：章節式 Agent production 背景。

完整清單見 [Stage 7 精選 Projects](../../../stages/07-multi-agent-production.md#-精選-projects範本--sdk--工具-collection)。

<small>模型、價格、套件、部署文件與連結查核：2026-08-28 UTC。</small>

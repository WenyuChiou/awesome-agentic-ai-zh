<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 3：看見 Agent 裡面發生什麼

**Observability（可觀測性）**像幫 Agent 裝儀表板：它慢了、錯了或花太多 token 時，你知道是哪一步。

對應 [Stage 7 — Multi-Agent 與 Production](../../../stages/07-multi-agent-production.md) 練習 3。

## 🎯 學習目標

- 認識 **Request ID、Span、Latency、Usage、Error** 五個核心訊號。
- 用同一個 request ID 串起一次工作裡的多個步驟。
- 記錄供應商實際回傳的 usage；沒有資料時就顯示缺少，不自行猜。

## 先跑不花模型費的測試

在這個資料夾開 PowerShell，直接複製：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

看到兩份 `🎉`，代表成功、錯誤、latency、span 與 usage 都有離線測試。測試不會連到模型。

<details markdown="1">
<summary>Path A：用 Ollama 產生一條真 Trace</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

另開 PowerShell：

```powershell
.\.venv\Scripts\python.exe starter.py
```

Ollama 不收模型 API 費，但硬體、電力與時間仍有成本。某些版本可能沒有回傳 usage；程式會保留零值，不把估算冒充供應商資料。

</details>

<details markdown="1">
<summary>Path B：記錄 Anthropic 回傳的 Usage</summary>

```powershell
$env:ANTHROPIC_API_KEY = "貼上你的金鑰"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

Haiku 4.5 的單價是 input `$1 / 1M` tokens、output `$5 / 1M` tokens：

```text
估算費用 = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

先設 `$1` provider spend limit。usage 是供應商對該次回覆的計數欄位；不同 API 的欄位名稱與涵蓋範圍可能不同。

</details>

## 五個重要詞

- **Request ID**：一次請求的識別碼，像包裹追蹤號碼。
- **Span**：請求裡的一小步，例如 search 或 llm_call。
- **Latency**：這一步花了多久。
- **Usage**：供應商回傳的 input/output token 數。
- **Error**：失敗的步驟與安全的錯誤類別，例如 `ValueError`；記完仍要把 exception 往上拋，不把可能含 secret 的完整訊息寫進 log。

```text
request_id
├─ span: search      → latency
└─ span: llm_call    → latency + usage + error
```

這份 starter 用小型 `TraceContext` 教原理。正式環境通常使用 OpenTelemetry，再把資料送到觀測平台。

## 只改一件事

把假的 `search` 步驟改名成 `retrieve_context`，再跑測試。確認 summary 仍有兩個 span，且兩者使用同一個 request ID。

## 成功檢查

- [ ] 一次請求只有一個 request ID。
- [ ] 每個步驟都有名稱與 latency。
- [ ] 空模型回覆會留下 error，再拋出例外。
- [ ] Log 不包含 API key、完整 Prompt 或原始 exception 訊息。

<details markdown="1">
<summary>Production 要補什麼、常見問題</summary>

正式服務至少要能回答：哪一步慢、哪一種錯誤最多、一次用了多少 token，以及哪個版本開始變差。

常見問題：

- 只記整體時間：看不出 search 還是模型慢。
- 吞掉 exception：外層誤以為成功。應該「記錄後再 raise」。
- 把 Prompt 或原始 exception 訊息全寫入 log：可能洩漏個資、文件或 secret。先記安全的錯誤類別，再做 redaction 與存取控制。
- 每筆 trace 永久保存：成本與隱私風險會增加。先定 sampling、retention 和刪除規則。
- 自行換算 token 卻標成 provider usage：估算與供應商欄位要分開命名。

</details>

<details markdown="1">
<summary>📚 深入學習資源與評分</summary>

- ⭐⭐⭐⭐⭐ [Langfuse](https://github.com/langfuse/langfuse)：開源 traces、evals 與 prompt 管理。
- ⭐⭐⭐⭐⭐ [Arize Phoenix](https://github.com/Arize-ai/phoenix)：OpenTelemetry 導向的開源觀測工具。
- ⭐⭐⭐⭐⭐ [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)：章節式中文 Agent 教材，適合補完整背景。
- ⭐⭐⭐⭐ [LangSmith](https://smith.langchain.com/)：適合 LangChain／LangGraph 生態。
- ⭐⭐⭐⭐ [Helicone](https://www.helicone.ai/)：可用 proxy 方式收集 LLM 請求資料。
- ⭐⭐⭐⭐ [Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/)：適合已使用 Datadog APM 的團隊。
- ⭐⭐⭐⭐ [Anthropic Console](https://console.anthropic.com/)：查看 Claude API usage 與帳務資料。

完整清單見 [Stage 7 精選 Projects](../../../stages/07-multi-agent-production.md#-精選-projects範本--sdk--工具-collection)。

<small>模型、價格、套件與連結查核：2026-08-28 UTC。</small>

</details>

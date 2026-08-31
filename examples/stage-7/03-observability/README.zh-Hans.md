<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 核心练习：看见 Agent 里面发生什么

**Observability（可观测性）**像帮 Agent 装仪表板：它慢了、错了或花太多 token 时，你知道是哪一步。

对应 [Stage 7 — Agent Production Engineering：Harness、Loop 与 Graph](../../../stages/07-multi-agent-production.zh-Hans.md) 核心练习 2。

## 🎯 学习目标

- 认识 **Request ID、Span、Latency、Usage、Error** 五个核心信号。
- 用同一个 request ID 串起一次工作里的多个步骤。
- 记录供应商实际返回的 usage；没有数据时就显示缺少，不自行猜。

## 先跑不花模型费的测试

在这个文件夹打开 PowerShell，直接复制：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

看到两份 `🎉`，代表成功、错误、latency、span 与 usage 都有离线测试。测试不会连到模型。

<details markdown="1">
<summary>Path A：用 Ollama 产生一条真 Trace</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

另开 PowerShell：

```powershell
.\.venv\Scripts\python.exe starter.py
```

Ollama 不收模型 API 费，但硬件、电力与时间仍有成本。某些版本可能没有返回 usage；程序会保留零值，不把估算冒充供应商数据。

</details>

<details markdown="1">
<summary>Path B：记录 Anthropic 返回的 Usage</summary>

```powershell
$env:ANTHROPIC_API_KEY = "贴上你的金钥"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

Haiku 4.5 的单价是 input `$1 / 1M` tokens、output `$5 / 1M` tokens：

```text
估算费用 = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

先设 `$1` provider spend limit。usage 是供应商对该次回复的计数栏位；不同 API 的栏位名称与涵盖范围可能不同。

</details>

## 五个重要词

- **Request ID**：一次请求的识别码，像包裹追踪号码。
- **Span**：请求里的一小步，例如 search 或 llm_call。
- **Latency**：这一步花了多久。
- **Usage**：供应商返回的 input/output token 数。
- **Error**：失败的步骤与安全的错误类别；记完仍要把 exception 往上抛。原始 exception 信息可能含有 secret，不能写进 log。

```text
request_id
├─ span: search      → latency
└─ span: llm_call    → latency + usage + error
```

这份 starter 用小型 `TraceContext` 教原理。正式环境通常使用 OpenTelemetry，再把数据送到观测平台。

## 只改一件事

把假的 `search` 步骤改名成 `retrieve_context`，再跑测试。确认 summary 仍有两个 span，且两者使用同一个 request ID。

## 成功检查

- [ ] 一次请求只有一个 request ID。
- [ ] 每个步骤都有名称与 latency。
- [ ] 空模型回复会留下 error，再抛出例外。
- [ ] Log 不包含 API key、完整 Prompt 或原始 exception 信息。

<details markdown="1">
<summary>Production 要补什么、常见问题</summary>

正式服务至少要能回答：哪一步慢、哪一种错误最多、一次用了多少 token，以及哪个版本开始变差。

常见问题：

- 只记整体时间：看不出 search 还是模型慢。
- 吞掉 exception：外层误以为成功。应该“记录后再 raise”。
- 把 Prompt 或原始 exception 信息全写入 log：可能泄漏个人信息、文件或 secret。先记录安全的错误类别，再做 redaction 与访问控制。
- 每笔 trace 永久保存：成本与隐私风险会增加。先定 sampling、retention 和删除规则。
- 自行换算 token 却标成 provider usage：估算与供应商栏位要分开命名。

</details>

## 📚 必读与学习资源

- ⭐⭐⭐⭐⭐ [Langfuse](https://github.com/langfuse/langfuse)：开源 traces、evals 与 prompt 管理。
- ⭐⭐⭐⭐⭐ [Arize Phoenix](https://github.com/Arize-ai/phoenix)：OpenTelemetry 导向的开源观测工具。
- ⭐⭐⭐⭐⭐ [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)：章节式中文 Agent 教材，适合补完整背景。
- ⭐⭐⭐⭐ [LangSmith](https://smith.langchain.com/)：适合 LangChain／LangGraph 生态。
- ⭐⭐⭐⭐ [Helicone](https://www.helicone.ai/)：可用 proxy 方式收集 LLM 请求数据。
- ⭐⭐⭐⭐ [Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/)：适合已使用 Datadog APM 的团队。
- ⭐⭐⭐⭐ [Anthropic Console](https://console.anthropic.com/)：查看 Claude API usage 与账务数据。

完整清单见 [Stage 7 精选 Projects](../../../stages/07-multi-agent-production.zh-Hans.md#-精选-projects范本--sdk--工具-collection)。

<small>模型、价格、套件与连结查核：2026-08-28 UTC。</small>

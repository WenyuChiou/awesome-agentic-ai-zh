<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 4：一边显示答案，一边确认 Cache

**Streaming**让答案分段出现；**Prompt caching**让相同的长前缀有机会被重用。两者解决不同问题。

对应 [Stage 7 — Multi-Agent 与 Production](../../../stages/07-multi-agent-production.zh-Hans.md) 练习 4。

## 🎯 学习目标

- 量自己的 first-token latency 与 total latency，不照抄固定秒数。
- 正确略过空 chunk，并在整条 stream 都空白时报错。
- 用 `cache_creation_input_tokens` 与 `cache_read_input_tokens` 判断实际结果。

## 先跑不花模型费的测试

在这个文件夹打开 PowerShell，直接复制：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

看到两份 `🎉`，代表 streaming、空回复和 cache_control 的离线合约都通过。

<details markdown="1">
<summary>Path A：用 Ollama 看 Streaming</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

另开 PowerShell：

```powershell
.\.venv\Scripts\python.exe starter.py
```

Ollama 不收模型 API 费，但硬件、电力与时间仍有成本。记下你自己的第一段文字时间和总时间；模型、电脑、Prompt 与当下负载都会影响结果。

</details>

<details markdown="1">
<summary>Path B：用 Anthropic 看 Streaming 与 Prompt caching</summary>

```powershell
$env:ANTHROPIC_API_KEY = "贴上你的金钥"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

Haiku 4.5 的一般 input/output 单价是 `$1 / 1M` 与 `$5 / 1M` tokens。5 分钟 cache write 为一般 input 的 1.25 倍，cache read 为 0.1 倍：

```text
估算费用 =
  normal_input_tokens × $1 / 1M
  + cache_creation_input_tokens × $1.25 / 1M
  + cache_read_input_tokens × $0.10 / 1M
  + output_tokens × $5 / 1M
```

先在供应商 Console 设置 `$1` spend limit。实际是否创建或读到 cache，以 usage 字段为准，不以“第二次调用”猜测。

</details>

## 四个重要词

- **Chunk**：stream 里一次到达的一小段文字，不一定刚好是一个 token。
- **First-token latency**：从送出请求到第一段可显示文字的时间。
- **Total latency**：整份回答完成的时间。
- **Cache breakpoint**：告诉 API“前面这段可以重用”的位置。

这个示例使用 Haiku 4.5。官方最低可缓存长度是 **4,096 tokens**，所以程序故意创建远长于门槛的重复参考文字。程序仍不会宣称一定命中，而是显示：

- `cache_creation_input_tokens > 0`：供应商 usage 显示已创建 cache。
- `cache_read_input_tokens > 0`：供应商回报读到 cache。
- 两者都是 0：没有观察到创建或命中，请检查长度、前缀是否完全相同与 TTL。

## 只改一件事

把第二次问题改掉，但保持 `big_system` 完全相同。再看第二次 usage 是否出现 `cache_read_input_tokens`。

## 成功检查

- [ ] Streaming 时会逐段印字，不会把 `None` 当文字。
- [ ] 整条 stream 没有文字时会失败。
- [ ] Cache 示例内容明显跨过 4,096-token 门槛。
- [ ] 你只根据 usage 说“创建／命中／未观察到”。

<details markdown="1">
<summary>何时值得 Cache、常见问题</summary>

适合：相同的长 system prompt、tool schema 或参考文件会在短时间内重复使用。

不适合：前缀每次都变、内容太短，或下一次调用通常超过 cache TTL。

常见问题：

- `cache_control` 放错段落：把 breakpoint 放在稳定前缀的结尾。
- 第二次改了前缀：空格、工具顺序或模型改变，都可能让它成为不同 cache。
- 只看理论折扣：同时把 write premium、read tokens、未命中与 output tokens 算进去。
- Streaming 中途断线：正式 UI 要标示未完成，不能把半份答案当成功。

</details>

<details markdown="1">
<summary>📚 深入学习资源与评分</summary>

- ⭐⭐⭐⭐⭐ [Anthropic Prompt caching 官方文件](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)：最低长度、TTL、breakpoint 与 usage 栏位的权威来源。
- ⭐⭐⭐⭐⭐ [Anthropic Pricing](https://platform.claude.com/docs/en/about-claude/pricing)：用当期单价重算，不保存旧的固定账单。
- ⭐⭐⭐⭐ [Anthropic Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)：非即时大量工作可再研究 batch。
- ⭐⭐⭐⭐⭐ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：需要章节式背景时使用。

完整清单见 [Stage 7 精选 Projects](../../../stages/07-multi-agent-production.zh-Hans.md#-精选-projects范本--sdk--工具-collection)。

<small>模型、价格、套件、cache 条件与连结查核：2026-08-28 UTC。</small>

</details>

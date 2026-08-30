<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 5：Error Handling + Retry wrapper

对应 [Stage 1 — LLM 基础](../../../stages/01-llm-basics.zh-Hans.md) 练习 5。
> 🎓 **学习模式**：先运行提供的 `starter.py`（`python starter.py`），然后只改一个小地方，再重新运行现有测试：`python test.py` 和 `python test_anthropic.py`。如果测试失败，就撤销或修正这一个改动，再试一次。不需要重命名文件，也不需要重写整份解答。完整方法见 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

## 为什么这题重要

Stage 3-8 的 production agent 一定会碰到 API 错误：

- Rate limit（429）→ 云端 API 订阅级别不一样、随时可能撞到
- 网络抖（connection reset）→ 跨机房 / VPN 是日常
- API key 过期（401）→ rotate 没同步
- Context 过长（400）→ 你给太多历史对话

**有些错误该 retry（rate limit / 网络）、有些不该（key 错、context 满）**。没分清楚 = 写 production agent 的常见坑。

## 怎么跑 — 两条路径

### Path A（默认、本机免费）

```bash
pip install -r requirements.txt
ollama pull gemma4:e4b
ollama serve
python starter.py
```

预算：**$0**。本机 demo 看 connection error / context window 的反应。

### Path B（Anthropic、想看真实 cloud 错误）

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python starter_anthropic.py
```

预算：每次 ≈ **$0.0005**（只有“情境 2 正常 call”会打 API、claude-haiku-4-5）。

预期看到（Path A、本机）：

```
[情境 1] 故意连到不存在的 Ollama port
  ✅ 抓到 APIConnectionError: APIConnectionError
  💡 production 处理: retry（网路错通常是 transient）

[情境 2] 正常 call、with_retry 包装（需要 Ollama 在跑）
  ✅ 成功、第一次就过: 👋

[情境 3] Prompt 超过 context window（Ollama 通常会截断或 raise）
  ⚠ Ollama 没 raise（可能直接截断 prompt）。Cloud API 通常会 400

✅ 练习 5 通过 — 你已了解 3 种错误如何 raise、知道何时该 retry 何时该 stop、$0/run
```

## 不花钱验证程序逻辑（不需真的断网）

```bash
python test.py            # 验 Path A (Ollama) retry wrapper 逻辑
python test_anthropic.py  # 验 Path B (Anthropic) retry wrapper 逻辑
```

6 个 test 都用 `unittest.mock` 构造假错误 + 假 sleep（时间 0 秒）、验证 retry 逻辑：

```
✅ test_no_retry_when_success_first_time
✅ test_retry_on_connection_error_then_success
✅ test_retry_on_rate_limit
✅ test_raise_after_max_attempts
✅ test_no_retry_on_auth_error
✅ test_exponential_backoff_delays

🎉 全部通过 — retry wrapper 逻辑正确
```

> **本机优势**：Ollama 不会真的撞 RateLimitError（没 quota），所以“rate limit demo”看不到。但 mock-based test 完整、retry 逻辑 0 秒可重现——这恰好是 Ollama path 适合理解 retry pattern 的地方：**快、免费、可重现**。

## 程序结构走查

| 段 | 在做什么 |
|---|---|
| `RETRIABLE = (APIConnectionError, RateLimitError)` | 白名单：只 retry 这两种、其他直接 raise |
| `with_retry(fn, ...)` | exponential backoff wrapper：1s, 2s, 4s, 8s + jitter |
| `demo_bad_key()` (Ollama) / `demo_bad_key()` (Anthropic) | 故意触发网络 / 401 错、看 exception 怎么 raise |
| `demo_with_retry()` | 正常 call 包 with_retry、预期 1 次成功 |
| `demo_too_long_prompt()` | 超长 prompt、看 context window 反应 |

## 两个 SDK 的 exception class 对应表

| Anthropic SDK | OpenAI SDK (Ollama) | 含义 | RETRIABLE? |
|---|---|---|---|
| `anthropic.APIConnectionError` | `openai.APIConnectionError` | 网络断 | ✅ |
| `anthropic.RateLimitError` | `openai.RateLimitError` | 429 限流 | ✅ |
| `anthropic.AuthenticationError` | `openai.AuthenticationError` | 401 key 错 | ❌ |
| `anthropic.APIStatusError` | `openai.APIStatusError` | 一般 HTTP 错 | 视 status code |

两个 SDK 的 exception class 名字几乎一样、retry 逻辑**完全跨 backend**。换 SDK 只要改 import 那一行。

## 常见坑

1. **无脑 retry 所有 exception**：会把 AuthenticationError 也 retry 一遍、浪费 4 倍时间最后 still 401。RETRIABLE 白名单是核心
2. **Backoff 不加 jitter**：1000 个 worker 同时被 rate limit、同时 1s 后重试、再次 rate limit → 死循。加 `random.uniform(0, 0.3)` 打散
3. **max_attempts 太高**：retry 8 次 = 1+2+4+8+16+32+64+128 = 255 秒、user 早就 give up。`max_attempts=4` 通常够
4. **没记录 attempt count**：production 一定要把 retry 次数加进 metric、超过 threshold 该 alert
5. **rate limit response 带 `Retry-After` header**：API 告诉你等多久、SDK 已自动处理，但自写 wrapper 别忽略这个 hint

## 延伸

- **加 jitter strategy**：除了 uniform、可试 [decorrelated jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)（更稳）
- **加 circuit breaker**：连续 N 次 retry 失败、暂时 stop call
- **改用 [tenacity](https://github.com/jd/tenacity)** library：production 不要自己写 retry、用成熟 lib
- **错误分类更细**：依 status code（429 / 503 / 502 / 500）给不同 backoff strategy
- **Stage 3 tool-level 错误**：看 [`../../stage-3/05-error-handling/`](../../stage-3/05-error-handling/)、结构化 tool error 让 LLM 在 ReAct loop 里决策

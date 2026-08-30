<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 5：Error Handling + Retry wrapper

對應 [Stage 1 — LLM 基礎](../../../stages/01-llm-basics.md) 練習 5。
> 🎓 **學習模式**：先執行提供的 `starter.py`（`python starter.py`），再只改一個小地方，然後重新執行既有測試：`python test.py` 和 `python test_anthropic.py`。如果測試失敗，就撤銷或修正這一個改動，再試一次。不需要改名檔案，也不需要整份解答重寫。完整方法看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。


## 為什麼這題重要

Stage 3-8 的 production agent 一定會碰到 API 錯誤：

- Rate limit（429）→ 雲端 API 訂閱階級不一樣、隨時可能撞到
- 網路抖（connection reset）→ 跨機房 / VPN 是日常
- API key 過期（401）→ rotate 沒同步
- Context 過長（400）→ 你給太多歷史對話

**有些錯誤該 retry（rate limit / 網路）、有些不該（key 錯、context 滿）**。沒分清楚 = 寫 production agent 的常見坑。

## 怎麼跑 — 兩條路徑

### Path A（默認、本機免費）

```bash
pip install -r requirements.txt
ollama pull gemma4:e4b
ollama serve
python starter.py
```

預算：**$0**。本機 demo 看 connection error / context window 的反應。

### Path B（Anthropic、想看真實 cloud 錯誤）

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python starter_anthropic.py
```

預算：每次 ≈ **$0.0005**（只有「情境 2 正常 call」會打 API、claude-haiku-4-5）。

預期看到（Path A、本機）：

```
[情境 1] 故意連到不存在的 Ollama port
  ✅ 抓到 APIConnectionError: APIConnectionError
  💡 production 處理: retry（網路錯通常是 transient）

[情境 2] 正常 call、with_retry 包裝（需要 Ollama 在跑）
  ✅ 成功、第一次就過: 👋

[情境 3] Prompt 超過 context window（Ollama 通常會截斷或 raise）
  ⚠ Ollama 沒 raise（可能直接截斷 prompt）。Cloud API 通常會 400

✅ 練習 5 通過 — 你已了解 3 種錯誤如何 raise、知道何時該 retry 何時該 stop、$0/run
```

## 不花錢驗證程式邏輯（不需真的斷網）

```bash
python test.py            # 驗 Path A (Ollama) retry wrapper 邏輯
python test_anthropic.py  # 驗 Path B (Anthropic) retry wrapper 邏輯
```

6 個 test 都用 `unittest.mock` 構造假錯誤 + 假 sleep（時間 0 秒）、驗證 retry 邏輯：

```
✅ test_no_retry_when_success_first_time
✅ test_retry_on_connection_error_then_success
✅ test_retry_on_rate_limit
✅ test_raise_after_max_attempts
✅ test_no_retry_on_auth_error
✅ test_exponential_backoff_delays

🎉 全部通過 — retry wrapper 邏輯正確
```

> **本機優勢**：Ollama 不會真的撞 RateLimitError（沒 quota），所以「rate limit demo」看不到。但 mock-based test 完整、retry 邏輯 0 秒可重現——這恰好是 Ollama path 適合理解 retry pattern 的地方：**快、免費、可重現**。

## 程式結構走查

| 段 | 在做什麼 |
|---|---|
| `RETRIABLE = (APIConnectionError, RateLimitError)` | 白名單：只 retry 這兩種、其他直接 raise |
| `with_retry(fn, ...)` | exponential backoff wrapper：1s, 2s, 4s, 8s + jitter |
| `demo_bad_key()` (Ollama) / `demo_bad_key()` (Anthropic) | 故意觸發網路 / 401 錯、看 exception 怎麼 raise |
| `demo_with_retry()` | 正常 call 包 with_retry、預期 1 次成功 |
| `demo_too_long_prompt()` | 超長 prompt、看 context window 反應 |

## 兩個 SDK 的 exception class 對應表

| Anthropic SDK | OpenAI SDK (Ollama) | 含義 | RETRIABLE? |
|---|---|---|---|
| `anthropic.APIConnectionError` | `openai.APIConnectionError` | 網路斷 | ✅ |
| `anthropic.RateLimitError` | `openai.RateLimitError` | 429 限流 | ✅ |
| `anthropic.AuthenticationError` | `openai.AuthenticationError` | 401 key 錯 | ❌ |
| `anthropic.APIStatusError` | `openai.APIStatusError` | 一般 HTTP 錯 | 視 status code |

兩個 SDK 的 exception class 名字幾乎一樣、retry 邏輯**完全跨 backend**。換 SDK 只要改 import 那一行。

## 常見坑

1. **無腦 retry 所有 exception**：會把 AuthenticationError 也 retry 一遍、浪費 4 倍時間最後 still 401。RETRIABLE 白名單是核心
2. **Backoff 不加 jitter**：1000 個 worker 同時被 rate limit、同時 1s 後重試、再次 rate limit → 死循。加 `random.uniform(0, 0.3)` 打散
3. **max_attempts 太高**：retry 8 次 = 1+2+4+8+16+32+64+128 = 255 秒、user 早就 give up。`max_attempts=4` 通常夠
4. **沒記錄 attempt count**：production 一定要把 retry 次數加進 metric、超過 threshold 該 alert
5. **rate limit response 帶 `Retry-After` header**：API 告訴你等多久、SDK 已自動處理，但自寫 wrapper 別忽略這個 hint

## 延伸

- **加 jitter strategy**：除了 uniform、可試 [decorrelated jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)（更穩）
- **加 circuit breaker**：連續 N 次 retry 失敗、暫時 stop call
- **改用 [tenacity](https://github.com/jd/tenacity)** library：production 不要自己寫 retry、用成熟 lib
- **錯誤分類更細**：依 status code（429 / 503 / 502 / 500）給不同 backoff strategy
- **Stage 3 tool-level 錯誤**：看 [`../../stage-3/05-error-handling/`](../../stage-3/05-error-handling/)、結構化 tool error 讓 LLM 在 ReAct loop 裡決策

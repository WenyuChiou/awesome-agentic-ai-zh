<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 4：Cross-Provider 比較（Claude / GPT / Gemini）

對應 [Stage 1 — LLM 基礎](../../../stages/01-llm-basics.md) 練習 4。
> 🎓 **學習模式**：先執行提供的 `starter.py`（`python starter.py`），再只改一個小地方，然後重新執行既有測試 `python test.py`。如果測試失敗，就撤銷或修正這一個改動，再試一次。不需要改名檔案，也不需要整份解答重寫。完整方法看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。


## 為什麼要比較

同樣是「解釋 AGI vs narrow AI」這個 prompt、三家 LLM 回得不一樣：

- **Claude**：通常傾向先給結構（定義 → 例子）、語氣中性
- **GPT**：傾向先給簡短答案、再展開（type-A 風格）
- **Gemini**：傾向 list / bullet 排列、example 多

跑一次自己看、比讀論文有感。順便量 token / 成本 / latency 三維。

## 怎麼跑

```bash
pip install -r requirements.txt

# 至少設一個。沒設的會 skip、不會 crash
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export GOOGLE_API_KEY=...

python starter.py
```

預期看到（樣本）：

```
prompt: 用 1-2 句話解釋 AGI 跟 narrow AI 的差別。
============================================================
⚠ skip call_gemini（沒有對應 API key）

[Anthropic / claude-haiku-4-5]  latency=823ms  in=21 out=58
AGI（通用人工智慧）能跨領域學習與解題；narrow AI 只擅長單一任務...

[OpenAI / gpt-5-mini]  latency=612ms  in=24 out=49
Narrow AI 專精於特定任務（如下棋、辨識）、AGI 則具備...

✅ 練習 4 通過 — 收到 2 家 provider 回應、可比較風格 / 長度 / 成本
```

## 不花錢驗證程式邏輯

```bash
python test.py
```

4 個 test 都用 `unittest.mock.patch` 取代 SDK：

```
✅ test_skip_when_no_key
✅ test_compare_returns_only_valid_replies
✅ test_reply_dataclass_shape
✅ test_compare_one_provider_set

🎉 全部通過 — Cross-provider 邏輯正確（skip-on-missing-key 已驗）
```

## 程式結構走查

| 段 | 在做什麼 |
|---|---|
| `Reply` dataclass | 統一三家 SDK 各自 Response 物件、抽出 4 個共通欄位（text/in/out/latency） |
| `call_claude / call_openai / call_gemini` | 各家 SDK 包裝、沒 key 就 return `None` |
| `compare(prompt)` | 跑三個 caller、跳過 None、回 valid replies list |
| `__main__` | 印對照表、自我驗證 |

## 常見坑

1. **三家 SDK API shape 差很多**：Anthropic 用 `messages.create`、OpenAI 用 `chat.completions.create`、Google 用 `models.generate_content`。**用 dataclass 統一才能比較**
2. **Token 計算欄位名不一樣**：Anthropic 是 `input_tokens / output_tokens`、OpenAI 是 `prompt_tokens / completion_tokens`、Google 是 `prompt_token_count / candidates_token_count`
3. **沒設 key 應該 skip 而非 raise**：production code 一定要做這層 guard、production agent 不能因為一家 down 就全死
4. **沒抓 latency**：跑完才知道哪家慢、production routing 需要這 data

## 想加更多家？

OpenRouter、Mistral、Cohere、Groq 等服務可提供 OpenAI-compatible endpoint，但不能假設只改 `base_url` 就完全相容。至少還要確認 model ID、認證、支援的參數、tool schema、response／usage 欄位、rate limit 與錯誤格式：

```python
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)
```

## 🦙 Path B — 加上本機 Ollama 當第 4 家對照

`call_openai` 已經使用 OpenAI-compatible client。換成 Ollama 時要改 `base_url` 與 `model`，也要用本題測試確認 response、usage 與 tool support：

```python
def call_ollama(prompt: str) -> Reply | None:
    """本機 Ollama (gemma4:e4b 或 qwen2.5:3b)。沒裝就 return None、不 crash。"""
    import requests
    try:
        requests.get("http://localhost:11434/api/tags", timeout=2)
    except Exception:
        return None  # Ollama 沒跑
    from openai import OpenAI
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    t0 = time.time()
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return Reply(
        provider="Ollama-local",
        model="gemma4:e4b",
        text=r.choices[0].message.content or "",
        in_tokens=r.usage.prompt_tokens,
        out_tokens=r.usage.completion_tokens,
        latency_ms=int((time.time() - t0) * 1000),
    )
```

把 `call_ollama` 加進 `compare()` 的 caller list，就能看 4 家對照。本機路徑沒有供應商模型 API 帳單，但仍有下載、硬體、電力與等待成本；latency 與品質要用同一組固定測試在你的電腦實測。

## 延伸

- **成本對照** → 接 [Stage 1 的計價練習](../../../stages/01-llm-basics.md) 的 PRICING dict、印 dollar cost column
- **同 prompt 跑 N 次取平均** → 在 `compare()` 內加 for-loop、看 latency stdev
- **加 quality eval** → 加第四家 LLM 當 judge、給每家回應打分（這在 Stage 7 練習 2 會教）

<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 4：Cross-Provider 比较（Claude / GPT / Gemini）

对应 [Stage 1 — LLM 基础](../../../stages/01-llm-basics.zh-Hans.md) 练习 4。
> 🎓 **学习模式**：先运行提供的 `starter.py`（`python starter.py`），然后只改一个小地方，再重新运行现有测试 `python test.py`。如果测试失败，就撤销或修正这一个改动，再试一次。不需要重命名文件，也不需要重写整份解答。完整方法见 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

## 为什么要比较

同样是“解释 AGI vs narrow AI”这个 prompt、三家 LLM 回得不一样：

- **Claude**：通常倾向先给结构（定义 → 例子）、语气中性
- **GPT**：倾向先给简短答案、再展开（type-A 风格）
- **Gemini**：倾向 list / bullet 排列、example 多

跑一次自己看、比读论文有感。顺便量 token / 成本 / latency 三维。

## 怎么跑

```bash
pip install -r requirements.txt

# 至少设一个。没设的会 skip、不会 crash
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export GOOGLE_API_KEY=...

python starter.py
```

预期看到（样本）：

```
prompt: 用 1-2 句话解释 AGI 跟 narrow AI 的差别。
============================================================
⚠ skip call_gemini（没有对应 API key）

[Anthropic / claude-haiku-4-5]  latency=823ms  in=21 out=58
AGI（通用人工智能）能跨领域学习与解题；narrow AI 只擅长单一任务...

[OpenAI / gpt-5-mini]  latency=612ms  in=24 out=49
Narrow AI 专精于特定任务（如下棋、辨识）、AGI 则具备...

✅ 练习 4 通过 — 收到 2 家 provider 回应、可比较风格 / 长度 / 成本
```

## 不花钱验证程序逻辑

```bash
python test.py
```

4 个 test 都用 `unittest.mock.patch` 取代 SDK：

```
✅ test_skip_when_no_key
✅ test_compare_returns_only_valid_replies
✅ test_reply_dataclass_shape
✅ test_compare_one_provider_set

🎉 全部通過 — Cross-provider 邏輯正確（skip-on-missing-key 已驗）
```

## 程序结构走查

| 段 | 在做什么 |
|---|---|
| `Reply` dataclass | 统一三家 SDK 各自 Response 对象、抽出 4 个共通字段（text/in/out/latency） |
| `call_claude / call_openai / call_gemini` | 各家 SDK 包装、没 key 就 return `None` |
| `compare(prompt)` | 跑三个 caller、跳过 None、回 valid replies list |
| `__main__` | 印对照表、自我验证 |

## 常见坑

1. **三家 SDK API shape 差很多**：Anthropic 用 `messages.create`、OpenAI 用 `chat.completions.create`、Google 用 `models.generate_content`。**用 dataclass 统一才能比较**
2. **Token 计算字段名不一样**：Anthropic 是 `input_tokens / output_tokens`、OpenAI 是 `prompt_tokens / completion_tokens`、Google 是 `prompt_token_count / candidates_token_count`
3. **没设 key 应该 skip 而非 raise**：production code 一定要做这层 guard、production agent 不能因为一家 down 就全死
4. **没抓 latency**：跑完才知道哪家慢、production routing 需要这 data

## 想加更多家？

OpenRouter、Mistral、Cohere、Groq 等服务可以提供 OpenAI-compatible endpoint，但不能假设只改 `base_url` 就完全兼容。至少还要确认 model ID、认证、支持的参数、tool schema、response／usage 字段、rate limit 和错误格式：

```python
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)
```

## 🦙 Path B — 加上本机 Ollama 当第 4 家对照

`call_openai` 已经使用 OpenAI-compatible client。换成 Ollama 时要改 `base_url` 和 `model`，也要用本题测试确认 response、usage 和 tool support：

```python
def call_ollama(prompt: str) -> Reply | None:
    """本机 Ollama (gemma4:e4b 或 qwen2.5:3b)。没装就 return None、不 crash。"""
    import requests
    try:
        requests.get("http://localhost:11434/api/tags", timeout=2)
    except Exception:
        return None  # Ollama 没跑
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

把 `call_ollama` 加进 `compare()` 的 caller list，就能看 4 家对照。本地路径没有供应商模型 API 账单，但仍有下载、硬件、电力和等待成本；latency 与质量要用同一组固定测试在你的电脑上实测。

## 延伸

- **成本对照** → 接 [Stage 1 的计价练习](../../../stages/01-llm-basics.zh-Hans.md) 的 PRICING dict、印 dollar cost column
- **同 prompt 跑 N 次取平均** → 在 `compare()` 内加 for-loop、看 latency stdev
- **加 quality eval** → 加第四家 LLM 当 judge、给每家的响应打分（这在 Stage 7 练习 2 会教）

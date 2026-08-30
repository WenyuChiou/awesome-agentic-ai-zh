<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 5：Tool 错误处理

对应 [Stage 3 — 工具使用与第一个 Agent Loop](../../../stages/03-tool-use-and-hello-agent.zh-Hans.md) 练习 5。
> 🎓 **学习模式**：先运行提供的 `starter.py`（`python starter.py`），然后只改一个小地方，再重新运行现有测试 `python test.py`。如果测试失败，就撤销或修正这一个改动，再试一次。不需要重命名文件，也不需要重写整份解答。完整方法见 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 70-150 行 illustrative 版、聚焦 `核心 pattern + 两条 SDK path`，不是进阶深度教材。深度教材推荐：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章节式 + 16 种 production 能力。**本练习对应 hello-agents 的 Extra Chapter 错误处理 / circuit breaker**
> - [规则 5 结构化错误回传](../../../resources/schema-design-cheatsheet.zh-Hans.md)（本 repo 既有的 cheatsheet）
> - 完整 references 见 [Stage 3 精选 Projects](../../../stages/03-tool-use-and-hello-agent.zh-Hans.md#-精选-projects)


## 为什么这题重要

真实 agent 很少只走成功路径：API 会 timeout、第三方服务暂时不可用、user 传坏参数。这题故意让 `fetch_weather(city)` 第一次回**结构化 error**（`{"error": "network timeout", "retry_hint": "try again in 1s"}`）、第二次才成功；观察 ReAct loop 怎么把 error observation 交回 LLM、让模型自己决定 retry / 改 query / 放弃。

核心观念：**tool error 是数据、不是 exception**。回传结构化 dict、不要 raise。

## 怎么跑 — 两条路径

### Path A（默认、本机免费）

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

预算：**$0 API 费用**；不包含硬件、内存与电力成本。

### Path B（Anthropic、云端比较）

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "your-key"
python starter_anthropic.py
```

预算：每次先预留 **$0.05**。实际费用按 `输入 tokens × $1 / 1,000,000 + 输出 tokens × $5 / 1,000,000` 计算，Tool Use 还会加入 prompt tokens；价格查核日：`2026-08-27`。

预期看到（Path A、本机，理想 retry 走法）：

```
❓ 问题：Will it rain in Taipei today?（using Ollama qwen2.5:3b）
------------------------------------------------------------
[step 0] tool: fetch_weather({'city': 'Taipei'}) → {'error': 'network timeout', 'retry_hint': 'try again in 1s'}
[step 1] tool: fetch_weather({'city': 'Taipei'}) → {'city': 'Taipei', 'forecast': 'rain', 'temperature_c': 24}
------------------------------------------------------------
✅ 最终答案：It will rain in Taipei today (24°C).
✅ 练习 5 通过 — tool error 是 data 不是 exception、$0/run
```

## 不花钱验证程序逻辑（mock-based）

```powershell
python test.py            # 验 Path A (Ollama) starter.py 逻辑
python test_anthropic.py  # 验 Path B (Anthropic) starter_anthropic.py 逻辑
```

两条 test 都用 `unittest.mock`、不打真 API、$0/run。

## 设计提醒

错误也应该是结构化数据，让 LLM 有 context 做决策：

| Bad | Good |
|---|---|
| `raise Exception("failed")` | `return {"error": "network timeout", "retry_hint": "try again in 1s"}` |
| `return "failed"` | `return {"error": "...", "category": "transient", "retry_hint": "..."}` |
| 无限 retry | `max_iter` safety + 业务层 retry quota |

只回传 `"failed"` 让模型不知道下一步；加入 `retry_hint`、错误类型与可恢复建议，模型才有足够 context 做决策。retry 次数也要有限制，否则 agent 会在坏掉的工具前面无限打转。

## 两个 path 观察重点

**附加观察**：不同 model 对 `retry_hint` 的 follow-up 反应可能不同，可能直接放弃、无视 hint 或重复同一个错。固定 prompt、error 与测试题，用 eval 记录结构化 error 的处理行为；这也是 production 选择 model 的依据（Stage 7 production tier 会再回来讨论）。

| 观察项 | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| 看到 retry_hint 就 retry | 用固定 eval 测量 | 用固定 eval 测量 |
| 连续失败后 graceful end | 用固定 eval 测量 | 用固定 eval 测量 |
| 错误类型分流（transient vs permanent） | 用固定 eval 测量 | 用固定 eval 测量 |

## 想看更聪明的答案？

预设用固定 ID `claude-haiku-4-5-20251001`。想比较 sonnet 时：

```powershell
$env:MODEL = "claude-sonnet-5"; python starter_anthropic.py
```

或 Ollama path 换更大 model：

```powershell
$env:MODEL = "qwen2.5:7b"; python starter.py
```

## 延伸

- **加 retry quota**：在 loop 加 `error_count`、超过 N 次就放弃
- **加 circuit breaker**：连续失败、暂时 stop call（避免 wave-after-wave 打死下游）
- **错误类型分类**：transient（429 / connection）vs permanent（401 / 400）、不同处理
- **Production 级**：看 [`../../stage-1/05-error-handling/`](../../stage-1/05-error-handling/) 的 API-level retry wrapper（exponential backoff + jitter）

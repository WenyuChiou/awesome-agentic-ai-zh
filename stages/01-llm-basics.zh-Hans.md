# Stage 1 — LLM 基础（LLM Basics）

> [繁體中文](./01-llm-basics.md) | [English](./01-llm-basics.en.md) | **简体中文**

> 本章目的：通过一条可重复的本地到云端路径，学会通过 API（应用程序接口）调用 LLM，理解 **Token（词元）**、**Context Window（上下文窗口）** 和 **Temperature（温度）**，并用成本与延迟解释模型选择。

<!-- freshness: canonical=stages/01-llm-basics.md; verified_on=2026-08-27; scope=models,pricing,availability,deprecations; max_age_days=90 -->

## 📌 学习目标

完成本阶段后，你可以：

- 用 Ollama 的本地模型完成第一次 API 调用，再与 Anthropic 做对照。
- 用简单例子解释 token、context window 和 temperature。
- 从响应的 `usage` 字段读出输入和输出 token。
- 用输入／输出价格、延迟和数据敏感度解释模型选择。

## 三个核心词

### 1. **Token（词元）**

Token 是模型读写文字时使用的计算单位，也常是 API 的计价单位。可以把它想成句子被切成的一小块积木；一个英文单词可能是一块，也可能被切成几块，中文一个字也不保证只是一块。本章会在练习 2 读取实际 input／output token，再用它估算成本；数量要看 tokenizer，不能用字数精确猜测。

### 2. **Context Window（上下文窗口）**

Context Window 是模型处理一次请求时可用的 token 空间。它像桌面：你的 prompt 和历史对话先占位置，模型还要留位置写答案；型号也可能另设较小的最大输出上限，所以两个数字都要查。本章会用它判断长文档何时要删减、摘要或分批。

### 3. **Temperature（温度）**

Temperature 是控制采样变化程度的参数。把模型想成每次都从几块候选积木中挑下一块：低值偏向最可能的候选，适合分类或固定格式；高值更常尝试其他候选，适合构思但可能更不稳定。本章把它当成输出稳定度的旋钮；它不会增加模型知识，也不会保证完全可复现。

## 场景式模型选择器

先看任务限制，再选模型；不需要先背排行榜。

| 你的场景 | 先试哪条路 | 选择理由 |
|---|---|---|
| 第一次学 API，想零费用反复试 | **Ollama + `gemma4:e4b`** | 本地运行，单次 API 成本为 $0，可以反复修改示例。 |
| 想比较云端质量，数据可以发送出去 | **Claude Haiku 4.5／Sonnet 5** | Anthropic SDK 路径简单，按输入和输出 token 计费。 |
| 文档很长，还要处理图像或视频 | **Gemini 3.7 Flash 或 Kimi K3** | 先查型号的 context 和多模态支持，再用自己的文档小测。 |
| 中文 API 任务，希望控制用量 | **DeepSeek V4 或 GLM-5.3** | 比较官方价格、输出限制和可用性，不要只看模型名称。 |
| 隐私、离线或需要自部署 | **Llama 4、Qwen 3.8、Gemma 4 等开放权重** | 先估算硬件和授权，再用 Ollama 或其他运行时测量真实速度。 |

## 🚪 进入条件

主要路径使用本地 Ollama；开始前只需确认时间、工具和预算。

<details markdown="1">
<summary>🧭 展开时间、先备、环境与预算</summary>

**时间与先备**

预留约 1 周、5–8 小时。你应该能运行 Python script，并对 HTTP／REST 有基本概念。主路径使用本地 Ollama，因此没有 API key 也不会卡住。如果还不熟悉 Python 或命令行，请先回到 [Stage 0](00-foundations.zh-Hans.md)。

**环境**

Path A 需要 [Ollama](https://ollama.com)、`pip install openai` 和 `ollama pull gemma4:e4b`。低内存机器可以改用 `gemma4:e2b`。Stage 3 之后的工具调用练习使用 `qwen2.5:3b`；不要把这个 tag 混到本章的聊天示例中。Path B 需要 `pip install anthropic` 和 `ANTHROPIC_API_KEY`。

**预算**

本地路径每次调用成本为 $0（仍会消耗电力和时间）。每个练习运行 3–5 次时，云端总额会随提示长度和型号变化；从每次响应的 `usage` 计算，再乘以计划次数。下面每个练习都给出单次预算提醒和阶段预算方法；这只是教学估算，不是账单保证。

</details>

## 📚 必修阅读

先知道这五个官方入口；需要时再展开，不必全部读完才开始练习。

先按 1–3 阅读，再开始练习；需要了解 tokenizer 或本地运行时细节时查阅 4–5：

1. [Anthropic Claude 模型总览](https://platform.claude.com/docs/en/models/overview) — 型号、context 和价格入口。
2. [OpenAI API 模型](https://developers.openai.com/api/docs/models) — 型号与计价字段。
3. [Google Gemini 模型](https://ai.google.dev/gemini-api/docs/models) — GA／Preview 状态与 context。
4. [Hugging Face LLM Course：Tokenizers](https://huggingface.co/learn/llm-course/chapter6/1) — tokenizer 如何切分文本。
5. [Ollama 官方网站](https://ollama.com) — 安装和运行本地模型。

## 🛠 动手练习

### 练习 1：LLM API（hello world）

**成果：**用几行核心代码取得响应，并从 `usage` 读出输出 token。单次预算：Ollama $0；Anthropic Haiku 按本次 input／output usage 与官方 `$1/$5` 费率计算。阶段预算：本地反复运行仍为 $0；云端累加 3–5 次的实际 usage。

<details markdown="1" open>
<summary>📋 <b>起手码 — Path A（本地 Ollama <code>gemma4:e4b</code>、默认）</b>（复制到 <code>practice_1.py</code>，运行 <code>python practice_1.py</code>）</summary>

```python
# 需要：pip install openai      （用 OpenAI-compatible SDK 与 Ollama 通信）
# 运行前：ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama 不检查这个占位值
)

r = client.chat.completions.create(
    model="gemma4:e4b",   # 已安装时也可换成 qwen2.5:3b / llama3.2:3b
    max_tokens=100,
    messages=[{"role": "user", "content": "用一句话自我介绍。"}],
)

# === 自我验证 ===
text = r.choices[0].message.content
print("响应：", text)
print("usage:", r.usage)

assert r.choices[0].finish_reason in ("stop", "length"), f"非预期 finish_reason: {r.choices[0].finish_reason}"
assert len(text) > 0, "响应不应为空"
assert r.usage.completion_tokens > 0, "output token 应大于 0"
print("✅ 练习 1 通过 — Ollama gemma4:e4b 已能在本地响应，每次 $0")
```

</details>

<details markdown="1">
<summary>📋 <b>起手码 — Path B（Anthropic API，可选）</b>（复制到 <code>practice_1_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
# 环境变量：export ANTHROPIC_API_KEY=sk-ant-...
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-haiku-4-5",  # Haiku 最便宜；改这一行可换成 Sonnet
    max_tokens=100,
    messages=[{"role": "user", "content": "用一句话自我介绍。"}],
)

# === 自我验证 ===
text = msg.content[0].text
print("响应：", text)
print("usage:", msg.usage)

assert msg.stop_reason in ("end_turn", "max_tokens"), f"非预期 stop_reason: {msg.stop_reason}"
assert len(text) > 0, "响应不应为空"
assert msg.usage.input_tokens > 0 and msg.usage.output_tokens > 0, "token 数应大于 0"
print("✅ 练习 1 通过 — 已成功调用 Anthropic API")
```

</details>

### 练习 2：Tokens

**成果：**重复发送同一个提示，观察语言、temperature 和输出长度如何改变 token 用量。单次预算：Ollama $0；Anthropic Haiku 按该次 input／output usage 与官方费率计算。阶段预算：本地为 $0；Path B 累加 3–5 组重复测试的实际 `usage`。

<details markdown="1" open>
<summary>📋 <b>起手码 — Path A（本地 Ollama <code>gemma4:e4b</code>、默认）</b>（复制到 <code>practice_2.py</code>）</summary>

```python
# 需要：pip install openai     （用 OpenAI-compatible SDK 与 Ollama 通信）
# 运行前：ollama pull gemma4:e4b && ollama serve
import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

PROMPTS = {
    "中文": "用一句话描述一只猫在做什么。",
    "English": "Describe in one sentence what a cat is doing.",
}

N = 10  # 本地运行较慢时先用小一点的 N，确认成功后再加大
for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(N):
        r = client.chat.completions.create(
            model="gemma4:e4b",
            max_tokens=80,
            temperature=1.0,  # 调高 temperature 以观察变化
            messages=[{"role": "user", "content": prompt}],
        )
        output_tokens.append(r.usage.completion_tokens)
    print(f"\n[{label}] prompt: {prompt}")
    print(f"  input tokens: {r.usage.prompt_tokens}")
    print(f"  output tokens — min={min(output_tokens)} max={max(output_tokens)} mean={statistics.mean(output_tokens):.1f} stdev={statistics.stdev(output_tokens):.1f}")

# === 自我验证 ===
assert len(output_tokens) == N and all(n > 0 for n in output_tokens), "每个 output token 数都应大于 0"
print("\n✅ 练习 2 通过 — 已观察到两种语言的 output token，本地运行 $0")
print("💡 token 数会受 tokenizer 和实际内容影响；不要只按字数推算，也不要预设某种语言一定较多。")
```

</details>

<details markdown="1">
<summary>📋 <b>起手码 — Path B（Anthropic API，可选）</b>（复制到 <code>practice_2_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()
PROMPTS = {"中文": "用一句话描述一只猫在做什么。", "English": "Describe in one sentence what a cat is doing."}

for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(20):
        msg = client.messages.create(model="claude-haiku-4-5", max_tokens=80, temperature=1.0,
                                     messages=[{"role": "user", "content": prompt}])
        output_tokens.append(msg.usage.output_tokens)
    print(f"[{label}] input={msg.usage.input_tokens} output min/max/mean={min(output_tokens)}/{max(output_tokens)}/{sum(output_tokens)/len(output_tokens):.1f}")
```

Anthropic 调用使用 `client.messages.create()`、`usage.input_tokens` 和 content block，这些字段与 Ollama 的 OpenAI-compatible 形状不同。请用返回的 token 数计算本次成本。

</details>

### 练习 3：Pricing / Latency

**成果：**分别测量同一个小任务的 token 成本与等待时间。单次预算：Ollama $0；Anthropic Haiku 按本次 input／output usage 与官方费率计算。阶段预算：本地为 $0；Path B 先运行 1 次取得实际数量，再乘以计划次数。

<details markdown="1" open>
<summary>📋 <b>起手码 — Path A（本地 Ollama <code>gemma4:e4b</code>、测量 latency）</b>（复制到 <code>practice_3.py</code>）</summary>

```python
# 需要：pip install openai
# 运行前：ollama pull gemma4:e4b && ollama serve
import sys, time
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 测量 5 次 latency 与 output token
latencies = []
output_tokens = []
for _ in range(5):
    t0 = time.time()
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[{"role": "user", "content": "你好！请自我介绍一下。"}],
    )
    latencies.append(time.time() - t0)
    output_tokens.append(r.usage.completion_tokens)

# 统计
avg_latency = sum(latencies) / len(latencies)
out_tok_avg = sum(output_tokens) / len(output_tokens)  # 五次平均值
tps = out_tok_avg / avg_latency if avg_latency > 0 else 0

print(f"model: gemma4:e4b（本地）")
print(f"5 次 latency（秒）: min={min(latencies):.2f} max={max(latencies):.2f} mean={avg_latency:.2f}")
print(f"avg output: {out_tok_avg} tokens，约 {tps:.1f} tokens/sec")
print(f"\n1000 次成本：$0（本地），预计时长：{avg_latency * 1000 / 60:.1f} 分钟")

# === 自我验证 ===
assert avg_latency > 0, "latency 应大于 0"
assert out_tok_avg > 0, "output token 应大于 0"
print(f"\n✅ 练习 3 通过 — 本地 model 每次 $0，但运行 1000 次约需 {avg_latency * 1000 / 60:.0f} 分钟")
print("💡 对照 Path B Anthropic：请按实际 input/output usage 与官方费率估算 1000 次成本，再与本地等待时间比较。")
```

</details>

<details markdown="1">
<summary>📋 <b>起手码 — Path B（Anthropic API，计算成本）</b>（复制到 <code>practice_3_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

# Anthropic 公开定价（每 1M token、USD）— 运行前查看 https://www.anthropic.com/pricing
PRICING = {
    "claude-haiku-4-5":   {"input": 1.00, "output":  5.00},
    "claude-sonnet-5":    {"input": 2.00, "output": 10.00},
    "claude-opus-5":      {"input": 5.00, "output": 25.00},
    "claude-fable-5":     {"input": 10.00, "output": 50.00},
}

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"

msg = client.messages.create(model=MODEL, max_tokens=200,
                             messages=[{"role": "user", "content": "你好！请自我介绍一下。"}])
in_tok, out_tok = msg.usage.input_tokens, msg.usage.output_tokens
rates = PRICING[MODEL]
cost_one = (in_tok * rates["input"] + out_tok * rates["output"]) / 1_000_000

print(f"model: {MODEL}")
print(f"single: input={in_tok} output={out_tok} → ${cost_one:.6f}")
print(f"1000 calls cost across model tiers:")
for name, r in PRICING.items():
    c = (in_tok * r["input"] + out_tok * r["output"]) / 1_000_000 * 1000
    print(f"  {name:<22} ${c:.4f}")

# === 自我验证 ===
assert cost_one > 0, "Cloud LLM 调用应有正成本"
print("\n✅ 练习 3 通过（Anthropic）— 已按实际 token 算出 Haiku、Sonnet、Opus 与 Fable 各 1000 次的成本")
```

</details>

## 🎯 精选 Projects

### 推荐 Capstone：个人文档摘要成本／质量比较器

建立一个小型命令行工具：读入 3–5 段你有权使用的文本，分别用 Ollama 和一个 Anthropic 型号摘要；记录输入／输出 token、延迟、估算成本，并用固定检查表标注摘要是否遗漏关键事实。它把本章三个核心词和模型选择器连接起来，不要求先做 RAG 或 agent。

<details markdown="1">
<summary>📦 Capstone 验收清单与其他 Project 入口</summary>

完成后应能展示：

- 同一输入的两条路径与模型名称。
- 每次调用的 input／output token、延迟与单次成本。
- 固定的质量检查表，而不是只凭主观印象选模型。
- 何时使用本地、何时接受云端成本，以及 context 不足时如何分批。

下面的表格保留本章原有的 17 个延伸入口。它们是选读资源，不是本章必做项目。推荐度是编辑判断，不是 GitHub 热度：`⭐⭐⭐⭐⭐` 代表跳过会卡住；本表都是补充入口，所以如实使用 `⭐⭐⭐⭐`、`⭐⭐⭐` 或历史参考的 `⭐⭐`，不列会变化的 stars。

<table>
  <thead><tr><th scope="col">分类</th><th scope="col">资源</th><th scope="col">入口</th><th scope="col">推荐度</th><th scope="col">用途／状态</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">官方 API 入门</th><td>Anthropic Cookbook</td><td><a href="https://github.com/anthropics/claude-cookbooks">GitHub</a></td><td>⭐⭐⭐⭐</td><td>Claude API notebook，可查 tool use、batch 和 prompt cache。</td></tr>
    <tr><td>Anthropic Courses</td><td><a href="https://github.com/anthropics/courses">GitHub</a></td><td>⭐⭐⭐⭐</td><td>Anthropic 官方课程，从 API 基础逐步延伸。</td></tr>
    <tr><td>OpenAI Cookbook</td><td><a href="https://github.com/openai/openai-cookbook">GitHub</a></td><td>⭐⭐⭐⭐</td><td>OpenAI API、structured output 和 function calling 示例。</td></tr>
    <tr><td>Anthropic Claude API Quickstart</td><td><a href="https://platform.claude.com/docs/en/get-started">官方文档</a></td><td>⭐⭐⭐</td><td>快速完成第一次 Claude API 调用。</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">中文教材</th><td>datawhalechina/happy-llm</td><td><a href="https://github.com/datawhalechina/happy-llm">GitHub</a></td><td>⭐⭐⭐⭐</td><td>用中文理解 LLM 原理和训练流程。</td></tr>
    <tr><td>datawhalechina/llm-universe</td><td><a href="https://github.com/datawhalechina/llm-universe">GitHub</a></td><td>⭐⭐⭐⭐</td><td>从 API 基础延伸到知识库和 RAG。</td></tr>
    <tr><td>datawhalechina/llm-cookbook</td><td><a href="https://github.com/datawhalechina/llm-cookbook">GitHub</a></td><td>⭐⭐⭐</td><td>Andrew Ng 课程的中文改编，更新速度较慢。</td></tr>
    <tr><td>jingyaogong/minimind</td><td><a href="https://github.com/jingyaogong/minimind">GitHub</a></td><td>⭐⭐⭐</td><td>从零实现小型模型训练，Apache-2.0。</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">英文课程</th><td>Hugging Face — LLM Course</td><td><a href="https://huggingface.co/learn/llm-course/chapter1/1">课程</a></td><td>⭐⭐⭐⭐</td><td>Transformer、tokenizer 与 Hugging Face 生态。</td></tr>
    <tr><td>LangChain Academy</td><td><a href="https://academy.langchain.com/">课程</a></td><td>⭐⭐⭐</td><td>官方免费课程，包含 RAG 与 agent。</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">本地运行</th><td>ollama/ollama</td><td><a href="https://github.com/ollama/ollama">GitHub</a></td><td>⭐⭐⭐⭐</td><td>本章 Path A 的本地运行入口。</td></tr>
    <tr><td>ggml-org/llama.cpp</td><td><a href="https://github.com/ggml-org/llama.cpp">GitHub</a></td><td>⭐⭐⭐⭐</td><td>理解量化和本地推理底层。</td></tr>
    <tr><td>mudler/LocalAI</td><td><a href="https://github.com/mudler/LocalAI">GitHub</a></td><td>⭐⭐⭐</td><td>提供 OpenAI 兼容的 self-host 服务。</td></tr>
    <tr><td>ml-explore/mlx</td><td><a href="https://github.com/ml-explore/mlx">GitHub</a></td><td>⭐⭐⭐</td><td>Apple Silicon 的机器学习框架。</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">从零理解</th><td>Karpathy — Let's build GPT from scratch</td><td><a href="https://www.youtube.com/watch?v=kCc8FmEb1nY">视频</a></td><td>⭐⭐⭐⭐</td><td>用 PyTorch 从零构建 GPT。</td></tr>
    <tr><td>rasbt/LLMs-from-scratch</td><td><a href="https://github.com/rasbt/LLMs-from-scratch">GitHub</a></td><td>⭐⭐⭐⭐</td><td>用代码深入 tokenizer、attention 和训练。</td></tr>
    <tr><td>karpathy/LLM101n</td><td><a href="https://github.com/karpathy/LLM101n">GitHub</a></td><td>⭐⭐</td><td>已归档的课程大纲，属于历史参考，不是现行教学。</td></tr>
  </tbody>
</table>

**其他 Project（按难度）**

- 入门：多语言 token 计数器、单句摘要器、temperature 对照表。
- 中阶：跨供应商 prompt 评测器、错误重试包装器、本地模型延迟仪表板。
- 延伸：小型文档分批摘要流程、可配置模型路由器、隐私数据的本地推理服务。

</details>

### 练习 4：Cross-Provider 比较

**成果：**用同一个提示比较不同供应商的输出，记录差异，不把单次结果当成排名。单次预算：Path A Ollama $0；Path B 按三家 API 的实际 token 计费。阶段预算：本地为 $0；云端先各运行 1 次，再按 3–5 组评测估算。

<details markdown="1">
<summary>🔬 练习 4 详细路径（选做）</summary>

- **Path A（Ollama，主要练习）：**使用 [`examples/stage-1/04-cross-provider/`](../examples/stage-1/04-cross-provider/) 的 Ollama 调用，先建立本地基线。
- **Path B（Anthropic，可选）：**在同一数据集加入 Anthropic SDK；如果也加入 OpenAI／Google，分别记录型号、参数、token 和失败情况。
- 比较回答风格、长度、格式遵守度和事实遗漏；把结果视为你的任务小评测，不是官方规格或普遍排名。

这个 starter 包含三家 SDK 的并行调用，缺少某家 key 时会跳过；它是 illustrative 示例，不是 chapter-length 教程。

</details>

### 练习 5：Error Handling

**成果：**为错误分类、重试和停止条件写出可测试的处理流程。单次预算：Path A Ollama $0；Path B 只使用 mock 时没有 API 费用。阶段预算：本地与 mock 测试为 $0；若加入云端集成测试，限制为 1–2 次并累加实际 token 成本。

<details markdown="1">
<summary>🧰 练习 5 详细路径（选做）</summary>

- **Path A（Ollama，主要练习）：**先在 [`examples/stage-1/05-error-handling/`](../examples/stage-1/05-error-handling/) 运行 mock-based test，再用本地端点观察可恢复的网络错误。
- **Path B（Anthropic，可选）：**用 Anthropic SDK 的异常类型接上同一 retry wrapper；API key 错误和 context 过长不应无限重试。
- 至少覆盖错误 API key、提示过长和网络中断；exponential backoff 要有上限和明确的最大尝试次数。

这个 starter 不需要真的断网就能验证重试逻辑；它是 illustrative 示例，不是 chapter-length 教程。

</details>

### 练习 6：Local LLM

**成果：**在自己的电脑上启动 Ollama，并通过 OpenAI-compatible API 调用本地模型。单次预算：Ollama $0（另有硬件电力成本）；Path B 按实际 token 计费。阶段预算：本地练习为 $0；若用 Anthropic 做一次质量对照，限制为 1–3 次并记录 usage。

<details markdown="1">
<summary>🦙 练习 6 详细路径（选做）</summary>

**Path A（Ollama，主要可运行路径）：**

```bash
# 1. 安装 Ollama：https://ollama.com
ollama pull qwen2.5:3b
ollama serve  # 默认 port 11434
```

```python
# 需要：pip install openai
# 运行前：Ollama 已启动，qwen2.5:3b 已下载
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama 不检查这个占位值
)

r = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": "用 3 句话介绍什么是 ReAct。"}],
)

text = r.choices[0].message.content
print("响应：", text)

# === 自我验证 ===
assert len(text) > 10, "响应太短，Ollama 可能没有启动"
print("✅ 练习 6 通过 — 本地 Ollama 已能通过 OpenAI-compatible API 调用")
print("💡 本次调用为 $0（不含电费）")
```

**Path B（Anthropic，可选）：**把同一个 ReAct 提示发送到 `claude-haiku-4-5`，保存响应和 `msg.usage`，再与 Path A 的格式遵守度、延迟和成本比较。不要把云端结果当成本地模型的规格保证。

没有 Ollama 时，可以把 `base_url` 换成 [LM Studio](https://lmstudio.ai)（`http://localhost:1234/v1`）或 [vLLM](https://github.com/vllm-project/vllm) endpoint；接口相同，但模型 tag 和硬件需求需要重新确认。

</details>

<details markdown="1">
<summary>🌐 完整 15 个家族表（官方规格入口）</summary>

<small>数据查核：2026-08-27 UTC。</small>

没有可靠公开数字就写“官方未公布”。价格通常是 USD／每 1M token；供应商若用别的单位，就按官方单位记录。

| 家族 | 当前推荐型号 | 状态 | Context | 价格或授权 | 适合做什么 | 限制 | 官方来源 |
|---|---|---|---|---|---|---|---|
| Claude | Fable 5；Opus 5；Sonnet 5；Haiku 4.5 | 正式可用 | 1M（Haiku 200K） | API：Fable $10/$50、Opus $5/$25、Sonnet $2/$10、Haiku $1/$5（输入／输出） | 长文、编程、agent 工作流 | Fable 已正式开放，不是仅限邀请；各平台的 model ID 不同，使用前确认平台和区域支持 | [Anthropic 模型总览](https://platform.claude.com/docs/en/models/overview) |
| GPT | GPT-5.6 Sol／Terra／Luna | 正式可用 | 1.05M | API：$4/$20、$2/$12、$0.20/$1.20（输入／输出） | 通用对话、工具调用、已有 SDK 集成 | 价格与限制按型号及 API 方案变化 | [OpenAI API 模型](https://developers.openai.com/api/docs/models) |
| Gemini | Gemini 3.7 Flash | 正式可用 | 1M | 2026-12-31 前介绍价 $0.75/$3.75（输入／输出） | 长文档、多模态与 Google 生态整合 | Gemini 3.1 Pro 为 Preview；介绍价有期限 | [Gemini 模型文档](https://ai.google.dev/gemini-api/docs/models) · [Gemini API 定价](https://ai.google.dev/gemini-api/docs/pricing) |
| DeepSeek | `deepseek-v4-flash`／`deepseek-v4-pro` | 正式可用 | 1M | Cache-miss：Flash $0.14/$0.28、Pro $0.435/$0.87（输入／输出） | 推理、编程、大量 token 任务 | 旧 `deepseek-chat`／`deepseek-reasoner` alias 已于 2026-07-24 弃用 | [DeepSeek 定价](https://api-docs.deepseek.com/quick_start/pricing/) |
| Kimi | `kimi-k3` | 正式可用 | 1M | API：cache hit／输入／输出分别为 CNY 2／20／100，每百万 tokens | 中文长文、视觉输入、长上下文任务 | 2.8T 参数；部署与配额取决于平台 | [Kimi 平台总览](https://platform.kimi.com/docs/overview) · [Kimi API 定价](https://platform.kimi.com/) |
| Hunyuan | `Hy3`（TokenHub） | 正式可用 | 官方未公布 | API：cache hit／输入／输出分别为 CNY 0.25／1／4，每百万 tokens | 中文推理与 Tencent Cloud 整合 | `hy3-preview` 将于 2026-08-31 下线；旧 T1／TurboS 已关闭或迁移 | [TokenHub 定价](https://cloud.tencent.com/document/product/1823/130055) · [Hy3 迁移公告](https://cloud.tencent.com/announce/detail/2391) |
| MiniMax | MiniMax M3 | 正式可用 | 1M | API：context ≤512K 为 US$0.30／$1.20；512K–1M 为 $0.60／$2.40，每百万输入／输出 tokens | 文本、视觉与 coding 任务 | 价格按输入长度和方案变化 | [MiniMax M3](https://www.minimax.io/blog/minimax-m3) · [MiniMax API 定价](https://platform.minimax.io/subscribe/token-plan?tab=api-enterprise) |
| Qwen | qwen3.8-max（API）；Qwen3.8 开放权重变体 | 正式可用 | 1M | API 按地区定价；例如北京为 CNY 12／36，每百万输入／输出 tokens；开放权重变体使用各自授权 | 中文任务、多模态、自部署工作流 | API 型号与开放权重变体不可混用；可用性与授权要分别确认 | [Qwen 3.8 Max](https://help.aliyun.com/en/model-studio/qwen3-8-max) |
| GLM | GLM-5.3 | 正式可用 | 1M（输出 128K） | API：输入／cache hit／输出分别为 US$1.40／$0.26／$4.40，每百万 tokens | 中文 agent、工具使用、推理 | 纯文本；reasoning 始终启用 | [GLM-5.3 文档](https://docs.z.ai/guides/llm/glm-5.3) · [GLM API 定价](https://docs.z.ai/guides/overview/pricing) |
| Yi | Yi-34B／Yi-9B 及 200K 变体 | 维护中 | 200K（部分旧型号） | 官方 repo 授权与已有服务条件；当前价格官方未公布 | 维护已有 Yi 实验、自部署基线 | 没有查到已验证的当前 frontier 后继型号 | [01.AI Yi repository](https://github.com/01-ai/Yi) |
| Llama | Llama 4 Scout／Maverick；Llama 3.3 70B（较实用旧基线） | 开放权重 | Scout 10M | Llama Community License | 自部署、微调、生态整合 | Scout 需要 H100 级硬件；授权不是 Apache／MIT | [Meta Llama Get Started](https://ai.meta.com/llama/get-started/) |
| Muse | Muse Glimmer 30B | 开放权重 | 131K | Apache 2.0 | 本地 agent、coding agent、长任务 | 全量或量化部署仍需要相当的消费级 GPU 内存 | [Hugging Face Muse Glimmer](https://huggingface.co/meta-models/Muse-Glimmer-30B) |
| Gemma | Gemma 4：E2B、E4B、12B、26B A4B、31B | 开放权重 | 小型型号 128K；中型型号 256K | Gemma 4 Terms／license；不是 Apache 2.0 | Edge、本地与受限硬件实验 | 需逐项阅读授权条款；硬件需求按型号变化 | [Gemma 核心文档](https://ai.google.dev/gemma/docs/core) · [Gemma Terms](https://ai.google.dev/gemma/terms) |
| Mistral | Mistral Small 4；Large 3；Ministral 3 | 正式可用 | Small 4：256K | Small 4 $0.15/$0.60；开放权重按版本授权，包括 Apache 2.0 版本 | reasoning、vision、coding 与自部署 | 不同型号的 API 与授权不同 | [Mistral Small 4](https://docs.mistral.ai/models/mistral-small-4-0-26-03) |
| Phi | Phi-4 14B；Phi-4 mini／multimodal | 开放权重 | Phi-4 multimodal 128K | Phi-4 multimodal MIT；按型号查授权 | 小型推理、多模态、edge | 不宣称固定 RAM；量化方式会改变硬件需求 | [Microsoft Phi](https://azure.microsoft.com/en-us/products/phi) · [Phi-4 multimodal](https://huggingface.co/microsoft/Phi-4-multimodal-instruct) |

</details>

<details markdown="1">
<summary>🧪 补充解释、排错与个人评测工具</summary>

**为什么 temperature 会改变输出**

LLM 每一步都会预测下一个 token 的概率分布，再按设置选出候选。低 temperature 让分布更集中；高 temperature 让不常见的候选也有机会。`max_tokens` 是输出上限，不保证输出长度。这只是帮助理解参数的简化模型，实际行为仍取决于供应商实现。

**常见问题**

- `Connection refused`：确认 `ollama serve` 正在运行，且 `base_url` 的端口是 11434。
- 找不到模型：先运行 `ollama list`，再用 `ollama pull gemma4:e4b` 安装，不要猜 tag。
- 响应被截断：缩短提示或降低 `max_tokens`，并检查型号的 context window。
- API 失败：先保存型号、状态码和 request id；只重试临时网络／服务错误，先修复认证与 context 错误。
- 成本对不上：输入和输出分别相乘；缓存命中、批处理和方案可能改变实际价格。

**第三方 benchmark**

[Artificial Analysis](https://artificialanalysis.ai/)、[Arena AI](https://arena.ai/leaderboard/text)、[Vellum leaderboard](https://www.vellum.ai/llm-leaderboard)、[Hugging Face Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard) 和 [SuperCLUE](https://www.superclueai.com/) 可作为个人任务的评测工具。它们不是供应商官方规格，也不能取代用自己的数据、提示和延迟进行测试。

</details>

## 自我检查

进入 Stage 2 前，确认你能：

- [ ] 说明 API、token 和 context window 各自解决什么问题。
- [ ] 跑通练习 1 的 Ollama Path A，并从 `usage` 读到输出 token。
- [ ] 用一次实测的 input／output token 算出一个云端调用成本。
- [ ] 为一个场景说明选择本地或云端的理由，并列出一项限制。

如果可以，进入 [Stage 2 — Prompt Engineering](02-prompt-engineering.zh-Hans.md)。如果还不行，先重跑练习 1–3 的 Path A，再按需打开阅读或排错区块。

---

> ✅ **Stage 1 完成？** 接下来 [**Stage 2 — Prompt Engineering**](02-prompt-engineering.zh-Hans.md) 会带你编写可复用的结构化 prompt，并用 eval 量化改进幅度。

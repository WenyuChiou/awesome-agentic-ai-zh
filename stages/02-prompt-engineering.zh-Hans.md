# Stage 2 — Prompt 设计（Prompt Engineering）

> [繁體中文](./02-prompt-engineering.md) | **简体中文** | [English](./02-prompt-engineering.en.md)

⏱ **时间估算**：1-2 周（约 5-12 小时）

> 👋 **从 [Stage 1](01-llm-basics.zh-Hans.md) 来的**：好，你会调用 API 了——这 5-12 小时：写出可重用的结构化 prompt、用 few-shot 跟 chain-of-thought 解难题、用 eval 量化 prompt 改善幅度。**直接从这里开始的**：先确认你会调用 LLM API、会用 token 算成本——做不到请先回 [Stage 1](01-llm-basics.zh-Hans.md)。

> 💡 用语不熟（prompt / few-shot / CoT / system prompt⋯）→ 翻 [`resources/glossary.zh-Hans.md`](../resources/glossary.zh-Hans.md)。

> 📋 **本章组成**：学习目标 → 进入条件 → 必修阅读 →〔可选 · 概念地图〕→ 动手练习 → 精选 Projects → 自我检查
> 🔑 **关键名词**：见 [`resources/glossary.zh-Hans.md`](../resources/glossary.zh-Hans.md)（每个 stage 用到的术语都收在那里）

## 📌 学习目标

走完这个阶段后你会：

- 写出结构化 prompt（角色 + 任务 + 格式 + 示例）
- 应用 few-shot prompting，并知道什么时候有用
- 在推理任务上使用 chain-of-thought（CoT）
- 反复迭代修改一个 prompt 并衡量改善
- 看出什么时候 prompt 已经到极限了（这时你需要 tool / agent）

## 🚪 进入条件

你应该已经：

- 会调用 LLM API（Stage 1）
- 会解析 / 遍历 API 响应

## 📚 必修阅读

1. [**anthropics/prompt-eng-interactive-tutorial**](https://github.com/anthropics/prompt-eng-interactive-tutorial) ⭐⭐⭐⭐⭐ ★ 37k+ — **Anthropic 官方互动教程**、9 章 Jupyter notebook（basic / intermediate / advanced + appendix），含 playground 跟 answer key。用 Claude 3 Haiku（最便宜）跑得起来、**Stage 2 的 canonical 动手教材**。也是 [**anthropics/courses**](https://github.com/anthropics/courses) 5 course umbrella 的 module 2，想看更广（含 API Fundamentals / Real World Prompting / Eval / Tool Use）直接看 umbrella
2. [**anthropics/courses — Real World Prompting**](https://github.com/anthropics/courses) ⭐⭐⭐⭐ ★ 22k+ — 同 umbrella 的 module 3，**“真实情境下怎么用 prompting”**：chatbot / legal / financial / coding 案例 walk-through。看完 #1 再来看 #2
3. [**Anthropic Prompt Engineering Guide**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — 官方 docs、配合上面 #1 一起读
3. [**OpenAI Prompt Engineering**](https://platform.openai.com/docs/guides/prompt-engineering) — OpenAI 观点
4. [**dair-ai Prompt Engineering Guide**](https://www.promptingguide.ai/) — 学术风，深入
5. [**Anthropic — Prompting Best Practices**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct) — 直接清楚

**🎥 中文视频补充（强烈推荐）**：

- [**李宏毅 — 生成式 AI 导论（2024 春台大课程）**](https://speech.ee.ntu.edu.tw/~hylee/genai/2024-spring.php) ⭐⭐⭐ — 中后段集数讲 prompt engineering（few-shot、CoT、in-context learning）+ 对应 lab。中文圈最完整的 prompting 学术级教学。最新整合版见 [**GenAI-ML 2025 秋**](https://speech.ee.ntu.edu.tw/~hylee/GenAI-ML/2025-fall.php)
- [**李宏毅 — 机器学习 2025 春（含 prompt + LLM 章节）**](https://speech.ee.ntu.edu.tw/~hylee/ml/2025-spring.php) — 适合想看 ML 完整背景的人

## 🛠 动手练习

> 🦙 **本 stage 默认用 Ollama gemma4:e4b**（成本考量、$0/run）。Prompt engineering 对小 model 更有教学价值——小 model 对 prompt 质量敏感、能让你看清楚 system prompt / few-shot / CoT / refinement 各自带来多少改善。每个练习都有 Path A（Ollama、默认）+ Path B（Anthropic、选择性）。
>
> 💰 **Stage 2 预算估算**（全 4 练习各跑 3-5 次）：**全本机 = $0**、**全 haiku ≈ $0.20**、**全 sonnet ≈ $0.60**。Few-shot 分类任务的 12 calls × 5 reps ≈ $0.30 haiku / $0.90 sonnet。完整预算见 [`examples/README.zh-Hans.md#推荐-llm-清单`](../examples/README.zh-Hans.md#推荐-llm-清单)。
>
> 完整 3 路 trade-off 见 [`examples/README.zh-Hans.md`](../examples/README.zh-Hans.md#三条路径--默认用-ollama成本考量)。

### 练习 1：System Prompt
同样的 user message，三个不同的 system prompt。观察人格 / 输出格式怎么变。

<details markdown="1" open>
<summary>📋 <b>起手码 — Path A（本机 Ollama gemma4:e4b、默认）</b>（复制到 <code>practice_1.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 同一个 user message、3 个不同 system prompt
SYSTEM_PROMPTS = {
    "严肃律师": "你是严谨的合约律师。回答要精准、引用法条编号、避免任何主观形容词。",
    "幼儿园老师": "你是温柔的幼儿园老师、要对 5 岁小孩说话。用比喻、口语、少于 80 字。",
    "JSON 机器": "你只回 JSON。schema: {\"answer\": string, \"confidence\": float}",
}

USER_MSG = "请帮我解释什么是租赁合约。"

outputs = {}
for label, system in SYSTEM_PROMPTS.items():
    # Note: Ollama 把 system 放 messages 第一笔（不像 Anthropic 用 system= 参数）
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": USER_MSG},
        ],
    )
    outputs[label] = r.choices[0].message.content
    print(f"\n--- [{label}] ---")
    print(outputs[label])

# === 自我验证 ===
json_output = outputs["JSON 机器"]
assert "{" in json_output and "}" in json_output, "JSON 机器版输出应该含 JSON braces"
try:
    parsed = json.loads(json_output.strip().split("\n")[-1] if "\n" in json_output else json_output)
    assert "answer" in parsed, "JSON schema 应包含 answer 栏位"
except json.JSONDecodeError:
    pass  # 容许 model 回 JSON 含解释文字、最后一笔才是 JSON
print(f"\n✅ 练习 1 通过 — 同一个问题、3 種人格 / 格式 / 语气")
print("💡 观察：律师长、老师短、JSON 机器一定是 {...}")
```

**预期输出**（样本、gemma4:e4b 对 system prompt 遵循度 OK 但不如 Claude 严谨）：
```
--- [严肃律师] ---
依民法第 421 条...

--- [幼儿园老师] ---
租赁合约就像借玩具给朋友、讲好什么时候还、要付多少糖果...

--- [JSON 机器] ---
{"answer": "租赁合约是当事人约定一方以物租与他方使用...", "confidence": 0.85}
```

</details>

<details markdown="1">
<summary>📋 <b>起手码 — Path B（Anthropic API、选择性）</b>（复制到 <code>practice_1_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic
client = anthropic.Anthropic()
SYSTEM_PROMPTS = {
    "严肃律师": "你是严谨的合约律师。回答要精准、引用法条编号、避免任何主观形容词。",
    "幼儿园老师": "你是温柔的幼儿园老师、要对 5 岁小孩说话。用比喻、口语、少于 80 字。",
    "JSON 机器": "你只回 JSON。schema: {\"answer\": string, \"confidence\": float}",
}
USER_MSG = "请帮我解释什么是租赁合约。"

outputs = {}
for label, system in SYSTEM_PROMPTS.items():
    # Anthropic 用 system= 参数（不放 messages 內）
    msg = client.messages.create(model="claude-haiku-4-5", max_tokens=200,
                                 system=system, messages=[{"role": "user", "content": USER_MSG}])
    outputs[label] = msg.content[0].text
    print(f"\n--- [{label}] ---")
    print(outputs[label])

# 同样的 JSON assert（schema 跨 backend 通用）
json_output = outputs["JSON 机器"]
assert "{" in json_output and "}" in json_output
print(f"\n✅ 练习 1 通过（Anthropic）")
```

**主要差异**：

- Anthropic: `system=...` 参数
- Ollama / OpenAI-compatible: `messages=[{"role": "system", ...}, ...]`

**Anthropic 对 system prompt 遵循度通常比 4B 小 model 更严谨**——“严肃律师”会真的引用法条编号。

</details>

### 练习 2：Few-Shot

**先搞懂这三个词**——差别只在你给 LLM 看“几个范例”：

- **Zero-shot（0-shot）**：不给范例、直接问。
- **One-shot（1-shot）**：先给 **1 个**“输入 → 答案”范例再问。
- **Few-shot（下面用的 3-shot 就是）**：给几个（通常 2-5 个）范例再问——LLM 照着范例的格式跟判断标准做，准确率通常明显变高。

挑一个分类任务。先用 0-shot 跑，再用 3-shot 跑。量一下准确率差多少。

<details markdown="1" open>
<summary>📋 <b>起手码 — Path A（本机 Ollama gemma4:e4b、默认）</b>（复制到 <code>practice_2.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 中文情绪分类（正面 / 负面 / 中立）
TEST_SET = [
    ("这部电影超赞、看完想再看一次！", "正面"),
    ("剧情无聊、演员演技尴尬。", "负面"),
    ("这是一部 2019 年的电影。", "中立"),
    ("我不确定喜不喜欢、可能再想想。", "中立"),
    ("第一集很不错但第二集就崩了。", "负面"),
    ("看完心情很好、推荐！", "正面"),
]

FEW_SHOT_EXAMPLES = """范例：
input: 这家餐厅的牛排好吃到让我哭出来。
output: 正面

input: 服务生态度很差、我再也不会来了。
output: 负面

input: 这家店位于新北市三重区。
output: 中立
"""

# 两种条件共用同一段“任务说明”；few-shot 只多加范例——这样对比才干净，量到的是“范例”本身的效果，而不是“终于告诉模型要做什么”。
TASK = "把下面的句子分类成“正面 / 负面 / 中立”其中一个，只输出这三个词其中之一、不要多余文字。\n\n"


def classify(text: str, *, use_few_shot: bool) -> str:
    prefix = FEW_SHOT_EXAMPLES + "\n" if use_few_shot else ""
    prompt = f"{TASK}{prefix}input: {text}\noutput:"
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content.strip().splitlines()[0]


def evaluate(use_few_shot: bool) -> tuple[int, int]:
    correct = 0
    for text, label in TEST_SET:
        pred = classify(text, use_few_shot=use_few_shot)
        ok = label in pred
        print(f"  {'✓' if ok else '✗'} [{label}] {text[:30]}... → '{pred}'")
        if ok:
            correct += 1
    return correct, len(TEST_SET)


print("=== 0-shot ===")
c0, n = evaluate(use_few_shot=False)
print(f"正确 {c0}/{n} = {c0/n:.0%}")

print("\n=== 3-shot ===")
c3, _ = evaluate(use_few_shot=True)
print(f"正确 {c3}/{n} = {c3/n:.0%}")

# === 自我验证 ===
# 两种条件都给了同样的任务说明，所以这里量的是“范例本身”带来的差异。
# few-shot 不保证每次都赢（看 model / 题目 / 抽样），所以不硬性要求 c3 >= c0。
assert n == 6 and 0 <= c0 <= n and 0 <= c3 <= n, "两种条件都要各跑完 6 题"
print(f"\n✅ 练习 2 通过 — 0-shot {c0}/{n}、3-shot {c3}/{n}；few-shot 净提升 {c3 - c0} 题（可能为 0 甚至负，都算正常）（本机 $0）")
print("💡 观察：有了任务说明，0-shot 就有基本盘；few-shot 的价值在“钉住输出格式” + 示范模棱两可案例（如 '中立'）的判准")
print("💡 小 model（gemma4:e4b）对格式更敏感，所以 few-shot 的帮助通常比 Claude 明显——但仍非保证，要跑了才知道")
```

</details>

<details markdown="1">
<summary>📋 <b>起手码 — Path B（Anthropic API、选择性）</b>（复制到 <code>practice_2_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
# 把 starter Path A 的 client 跟 classify() 改成：
import anthropic
client = anthropic.Anthropic()

def classify(text: str, *, use_few_shot: bool) -> str:
    prefix = FEW_SHOT_EXAMPLES + "\n" if use_few_shot else ""
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        messages=[{"role": "user", "content": f"{TASK}{prefix}input: {text}\noutput:"}],
    )
    return msg.content[0].text.strip().splitlines()[0]
# 其余 TASK / TEST_SET / FEW_SHOT_EXAMPLES / evaluate() 跟 Path A 一样
```

**成本**：6 题 × 2 条件 = 12 次 ≈ $0.005。**Claude 通常 0-shot 已经有不错准确率**、所以 few-shot 改善幅度比小 model 小。

</details>

### 练习 3：CoT
挑一个数学文字题，比较：

- 纯 prompt
- 纯 prompt + “Let's think step by step”
- 纯 prompt + 一个展示 CoT 的范例

<details markdown="1" open>
<summary>📋 <b>起手码 — Path A（本机 Ollama gemma4:e4b、默认）</b>（复制到 <code>practice_3.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys, re
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

QUESTION = "小明有 3 颗苹果。他给了小華 1 颗、又从媽媽那边拿到 5 颗、然后吃了 2 颗。请问现在剩几颗？"
ANSWER = 5  # 3 - 1 + 5 - 2 = 5

COT_EXAMPLE = """范例：
Q: 一只鸡有 2 只脚。3 只鸡跟 1 个人共有几只脚？
A: 让我一步一步算。3 只鸡 × 2 只脚 = 6 只脚。1 个人有 2 只脚。總共 6 + 2 = 8 只脚。答案是 8。
"""


def ask(prompt: str) -> str:
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content


def extract_number(text: str) -> int | None:
    nums = re.findall(r"-?\d+", text)
    return int(nums[-1]) if nums else None


# A. 纯 prompt
out_a = ask(QUESTION); ans_a = extract_number(out_a)

# B. + Let's think step by step
out_b = ask(QUESTION + "\nLet's think step by step."); ans_b = extract_number(out_b)

# C. + CoT example
out_c = ask(COT_EXAMPLE + "\n\nQ: " + QUESTION + "\nA:"); ans_c = extract_number(out_c)

for label, out, ans in [("A 纯 prompt", out_a, ans_a), ("B +step-by-step", out_b, ans_b), ("C +CoT example", out_c, ans_c)]:
    print(f"\n--- [{label}] 答案={ans} {'✓' if ans == ANSWER else '✗'} ---")
    print(out[:200])

# === 自我验证 ===
correct = sum(1 for a in (ans_a, ans_b, ans_c) if a == ANSWER)
assert correct >= 1, f"3 種 prompt 至少要 1 種答对、实际 {correct}/3"
# 小 model 对 CoT 依賴性更高、放宽条件：B 或 C 至少 1 对（vs Anthropic Path B 要求严格）
assert ans_b == ANSWER or ans_c == ANSWER, "B (step-by-step) 或 C (CoT example) 至少一種要答对 — CoT 对小 model 是基本功"
print(f"\n✅ 练习 3 通过 — {correct}/3 答对（本机 $0）")
print(f"💡 观察小 model：A 纯 prompt 通常答错、B/C 加 CoT 后明显改善——比 Claude 更能凸显 CoT 重要性")
```

</details>

<details markdown="1">
<summary>📋 <b>起手码 — Path B（Anthropic API、选择性）</b>（复制到 <code>practice_3_anthropic.py</code>）</summary>

把 Path A 的 client + ask() 改成：

```python
import anthropic
client = anthropic.Anthropic()

def ask(prompt: str) -> str:
    msg = client.messages.create(model="claude-haiku-4-5", max_tokens=300,
                                 messages=[{"role": "user", "content": prompt}])
    return msg.content[0].text
```

**Claude 通常 3/3 全对**（包括 A 纯 prompt）—— 对照 gemma4:e4b 可能只 1-2/3 对，能看到 CoT 对小 model 的价值。

</details>

> 🧠 **什么时候别自己写 CoT**：对 **reasoning-native 模型**（Claude Opus 4.x / 5、o 系列、Gemini thinking 等内置思考的模型），用它们的 extended thinking 通常比你手写“Let's think step by step”更好；硬塞步骤反而可能干扰它本来的推理。手写 CoT 仍适用于不具内置推理的一般 chat model。

### 练习 4：Iterative Refinement
拿一个模糊的 prompt，refine 5 次。把每一轮记下来。观察哪些改动会提升质量。

<details markdown="1" open>
<summary>📋 <b>起手码 — Path A（本机 Ollama gemma4:e4b、默认）</b>（复制到 <code>practice_4.py</code>）— 这题没有“对错”、重点是观察过程</summary>

```python
# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 5 个 iteration、每一轮 prompt 都比前一轮更具体
PROMPTS = {
    "v1 模糊": "写一段介紹 ReAct 的文字。",
    "v2 加目标读者": "写一段介紹 ReAct 的文字、给写过 Python 的软体工程师看。",
    "v3 加格式": "写一段介紹 ReAct 的文字、给写过 Python 的软体工程师看。100 字以內、用一个段落。",
    "v4 加 example 要求": "写一段介紹 ReAct 的文字、给写过 Python 的软体工程师看。100 字以內、用一个段落、结尾举一个具体例子（譬如查天气）。",
    "v5 加禁忌": "写一段介紹 ReAct 的文字、给写过 Python 的软体工程师看。100 字以內、用一个段落、结尾举一个具体例子（譬如查天气）。不要用「賦能」「驅动」「智能」这類空泛词彙。",
}

outputs = {}
for label, prompt in PROMPTS.items():
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    text = r.choices[0].message.content
    outputs[label] = text
    print(f"\n--- [{label}] ({len(text)} chars) ---")
    print(text)

# === 自我验证 ===
v1_len, v5_len = len(outputs["v1 模糊"]), len(outputs["v5 加禁忌"])
banned_words = ("賦能", "驅动", "智能")
v5_has_banned = any(w in outputs["v5 加禁忌"] for w in banned_words)
assert v5_len > 0, "v5 必須有输出"
assert not v5_has_banned, f"v5 应该避免禁忌词、实际含: {[w for w in banned_words if w in outputs['v5 加禁忌']]}"
print(f"\n✅ 练习 4 通过 — v5 长度 {v5_len}、无禁忌词（本机 $0）")
print(f"💡 观察：v1 ({v1_len} chars) 通常比 v5 ({v5_len} chars) 「鬆」、加约束会逼 prompt 收斂")
print("💡 用 gemma4:e4b 跑这题特别有感——小 model 对 prompt 质量极敏感、5 轮 refine 的差距会比 Claude 更明显")
```

</details>

<details markdown="1">
<summary>📋 <b>起手码 — Path B（Anthropic API、选择性）</b>（复制到 <code>practice_4_anthropic.py</code>）</summary>

把 Path A 的 client + 循环内 `client.chat.completions.create(...)` 改成：

```python
import anthropic
client = anthropic.Anthropic()

# 循环內：
msg = client.messages.create(model="claude-haiku-4-5", max_tokens=200,
                             messages=[{"role": "user", "content": prompt}])
text = msg.content[0].text
```

其余 PROMPTS / outputs / assert 逻辑完全相同。**成本**：5 次 ≈ $0.002。

**Claude vs gemma4 对 prompt 细致度的差别**：Claude haiku 通常 v1 已能写出 OK 段落、v5 加上约束后优化幅度较小；小 model v1 常空泛无用、v5 加禁忌后才开始能读。

</details>

**进阶做法**：把这 5 轮输出全存进 csv、Stage 7 练习 2 会教怎么把这变成 eval harness（跑评估用的外围程序 / 控制层，完整定义见下面 进阶：往上还有哪几层）量化“prompt 改善了多少”。

## 🎯 精选 Projects

按用途分 4 类、9 个项目一张表搞定。**挑入口看“适合谁”、想深入点连结看 repo / 网站**。

| 分类 | Project | ⭐ | 适合谁 | 为什么推荐 / 备注 |
|---|---|---|---|---|
| **学术 / 教学风 guide**<br>（先看这个） | [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) | ⭐⭐⭐⭐⭐ | 当参考书、需要某技巧再来查 | 从基础到进阶（CoT / ToT / ReAct / RAG）端到端，★ 74k+、MIT |
| | [PromptingGuide.ai](https://www.promptingguide.ai/) | ⭐⭐⭐⭐ | 手机阅读、想要可跑范例 | 跟 dair-ai GitHub 同样内容、做成网站 + 可跑范例 |
| | [NirDiamant/Prompt_Engineering](https://github.com/NirDiamant/Prompt_Engineering) | ⭐⭐⭐⭐ | 偏好“边跑边学” | 22 种技巧、独立 notebook，比 dair-ai 更动手，★ 7.7k+|
| **官方 cookbook** | [Anthropic Cookbook — Prompt patterns](https://github.com/anthropics/claude-cookbooks) | ⭐⭐⭐⭐⭐ | Claude 进阶 prompting（含 prompt caching / multimodal）| Stage 1 已介绍、本 stage 重点看 `misc/prompt_caching.ipynb` 跟 `multimodal/` |
| | [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai) | ⭐⭐⭐ | 用 Google 技术栈（PaLM / Gemini）| Google Cloud 的 prompting cookbook、跨厂商观点 |
| **灵感 collection**<br>（找模式、不要照抄）| [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) | ⭐⭐⭐ | 卡关时找灵感 | 上百个“Act as a [角色]...”prompt，★ 166k+、CC0。**把模式拿出来改写、不要照抄** |
| **Production 管理**<br>（规模化）| [microsoft/prompt-engine](https://github.com/microsoft/prompt-engine) | ⭐⭐（⚠️ 已封存）| production 要管很多 prompt 时 | TypeScript library；⚠️ **2023 起无更新、repo 已封存**——找维护中的替代 |
| | [microsoft/promptflow](https://github.com/microsoft/promptflow) | ⭐⭐⭐ | 团队型应用、需要 eval | 视觉化 prompt 设计 + 评估工具，★ 11k+ |
| | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) ⭐ **Stage 2 → 3 桥** | ⭐⭐⭐⭐⭐ | 跑完 dair-ai 想规模化 prompt | 把 prompt 当 code 写，用 compiler 自动最佳化，★ 36k+、MIT |

> **注**：dspy 是 framework 不是 tutorial、门槛较高，建议搭配 [dspy.ai](https://dspy.ai/) 官方 tutorial 读；NirDiamant 用 NOASSERTION 自订条款（偏研究 / 非商用）。

> 💡 **建议阅读路径**：dair-ai guide 入手（理论） → Anthropic Cookbook 看 Claude 实作 → NirDiamant 边跑边学 → 进 production 时读 dspy。

## 🔭 进阶：往上还有哪几层

LLM-powered system 的工程实践是分层的。这不是 1 次 call vs N 次 call 的区别。**这里先看跟“写 prompt”直接相邻的三层**——完整是**五层**，往外还有 Loop 与 Graph，见 [Stage 7 五层工程分工](07-multi-agent-production.zh-Hans.md#五层工程分工prompt--context--harness--loop--graph)（分层的 canonical 出处）。每一层工程的对象 **不一样**：

三层分别工程的是:**送进模型的那段字符串**(本 stage)、**context window 里装什么**(Stage 6)、**模型外面的执行与控制层**(Stage 7)。逐项定义与各自在哪一 stage 学,见下表。

→ 三层 **正交**：一次 call 的 RAG app 也在做 context engineering（重点是组 context，不是 call 几次）；50 次 call 但没做 retrieval 的 chatbot 仍然只是在做 prompt engineering。

**这三层在本路线的学习进度**（完整五层见 Stage 7）：

| Discipline | 工程“什么” | 在哪一 stage 完整学 |
|---|---|---|
| **1. Prompt Engineering** | 送进 LLM 的字符串本身（system prompt / few-shot / format） | **本 stage（Stage 2）** |
| **2. Context Engineering** | context window 里装什么信息（RAG / memory / tool defs / history） | [Stage 6 — Context Engineering：RAG 与 Memory](06-memory-rag.zh-Hans.md) |
| **3. Harness Engineering** | 模型外围的执行与控制层（agent loop / retry / sandbox / observability） | [Stage 7 — Multi-Agent · Production 化](07-multi-agent-production.zh-Hans.md) |

> 💡 **Karpathy 2025-06**：context engineering 是把 **刚好对下一步有用的信息** 填进 context window 的精细艺术。
>
> 💡 **Simon Willison / Addy Osmani**：“coding agent = LLM + harness”——harness 就是“模型外围的控制系统”、retry / loop / 监测 / 沙盒 / 部署这些不是 LLM 本身的代码。[OpenAI 也在 2026-02 使用了 "Harness Engineering" 这个说法](https://openai.com/index/harness-engineering)。

**这个 stage 不用学完后两层**，这里只是给你一个方向。等你进入 Stage 6 / 7，会发现它们是在接着这条 lineage 往上走。

延伸阅读（不必修、未来想深挖时看）：

- [`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering)（★ 3.3k+）——从 prompt engineering 一路推到 production agent 的 survey
- [`Windy3f3f3f3f/how-claude-code-works`](https://github.com/Windy3f3f3f3f/how-claude-code-works)（★ 3.3k+）——Claude Code 内部解析，含 context engineering 章节

## ✅ 进 Stage 3 前的自我检查

你能不能：

- [ ] 写一个有 system message + user message + 3 个示例 message 的 prompt（few-shot）
- [ ] 示范 CoT 在某个推理任务上提升准确率
- [ ] 反复 refine 一个 prompt 5 次，每一版都留下记录
- [ ] 看出 prompt 不是对的工具的时候（这时要用 tool use）

如果可以 → 进 [Stage 3 — Tool Use & Agent 入门](./03-tool-use-and-hello-agent.zh-Hans.md)。这是最重要的一个阶段——prompt 不要急着跳过去，但也不要卡在这里。

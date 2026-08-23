# Stage 1 — LLM 基础（LLM Basics）

> [繁體中文](./01-llm-basics.md) | **简体中文** | [English](./01-llm-basics.en.md)

⏱ **时间估算**：1 周（约 5-8 小时）

> 👋 **从 [Stage 0](00-foundations.zh-Hans.md) 来的**：好，环境已经够用——这 5-8 小时：第一次成功调用 Claude / GPT / Gemini API、搞懂 token / context window / temperature 怎么影响输出、用 per-token 计算实际成本。**直接从这里开始的**：先确认你能跑 Python script、有任一家供应商的 API key——做不到请先回 [Stage 0](00-foundations.zh-Hans.md)。

> 💡 **看不懂某个词**（LLM / token / context window / temperature / RAG / agent⋯）→ 先翻 [`resources/glossary.zh-Hans.md`](../resources/glossary.zh-Hans.md) 查 30 秒再回来。

> 📋 **本章组成**：学习目标 → 进入条件 → 必修阅读 →〔可选 · 概念地图〕→ 动手练习 → 精选 Projects → 自我检查  
> 🔑 **关键名词**：见 [`resources/glossary.zh-Hans.md`](../resources/glossary.zh-Hans.md)（每个 stage 用到的术语都收在那里）

### 3 个核心词（先记住，后面 stage 都会用到）

| 词 | 中文 | 一句话 |
|---|---|---|
| **token** | 词元 | 模型计算文字长度与费用的基本单位（中文 1 个字 ≈ 1.5-2 token） |
| **context window** | 上下文窗口 | 模型一次能看到多少 token（Claude 1M / GPT 1.05M / Gemini 2M） |
| **temperature** | 随机程度参数 | 控制回答是更稳定还是更发散（0 = 最稳定、1 = 更有创意；分类任务用 0.0-0.3、创作用 0.7-1.0） |

→ 这 3 个词贯穿后续所有 stage。Stage 1 的目标就是让你亲手调用 API、直接感受它们怎么影响输出。

> 🧠 **temperature 为什么能调？先懂 next-token**：LLM 的核心动作是**预测下一个 token**：它对“下一个字”算出一个概率分布，再从里面**采样**一个。`temperature` 跟 `top_p` 就是在“重塑这个分布”——temperature 低 → 分布变尖、几乎只挑最可能的（稳定、可复现）；temperature 高 → 分布变平、更敢挑冷门字（有创意但易跑题）。`max_tokens` 则是“最多采样几次就停”。所以这些不是魔法旋钮，而是在控制“怎么从概率分布里选字”。

## 📌 学习目标

完成本阶段后，你将能够：

- 解释 LLM、token、context window 等核心概念。
- 使用 Python 调用 Claude / GPT / Gemini API。
- 比较不同 LLM 提供商（Claude / GPT / Gemini / Llama）的优劣。
- 理解 per-token 定价模型并估算成本。

## 🌐 主流 LLM 家族对比（2026-05 snapshot）

“Claude 跟 GPT 有什么不同？”“中国模型能用吗？”“我该装 Ollama 跑哪个 OSS model？”——这节给你**客观对照**。不下“最好”结论——用 **强项 / 适合任务 / 弱项** 3 维比较、附**官方 docs URL**让你自己 verify。

> 💡 **先解释几个名词**：
> - **Context window** = LLM 一次能记住的对话量、有上限（例如 200k token ≈ 15 万中文字）
> - **Apache 2.0 / MIT** = 可商用 / 可修改 / 可闭源再发布的开源条款；**Llama Community License** = 开源但有条款限制（例如 ≥ 7 亿 MAU 要授权）
> - **Frontier model** = 各家最强旗舰；**OSS** = open-source、weights 可下载 self-host

### 🇺🇸 美系商业 frontier（3 家）

这 3 家是 SaaS API、按 token 付费、不能 self-host：

<!-- 维护惯例（下面 3 张表共用）：“旗舰”这格只写现在的旗舰，最多再留前一代；出了新的就把旧名字换掉、别一直往上加；太旧、官网已经查不到的就删掉。会变的信息（暂停、preview、还没出）别塞在格子里，写到表格下面那行“注”；等状态结束了（正式上线、恢复、或永久退役）就把那行删掉。“Context”这格只填数字。改完记得更新标题的月份（2026-MM）。 -->

| Model 家族 | 旗舰（2026-07）| Context | 强项 | 适合任务 | 官方 docs |
|---|---|---|---|---|---|
| **Claude**（Anthropic）| Opus 5 / Sonnet 5 / Haiku 4.5 | 1M | long-form / coding / agent / safety alignment | 写 paper / code review / agent runtime | [platform.claude.com/docs](https://platform.claude.com/docs/en/about-claude/models/overview) |
| **GPT**（OpenAI）| GPT-5.6 Sol / Terra / Luna | 1.05M | 通用 / function calling / ecosystem 最广 | 广度查询 / function-call 框架 / GPTs 生态 | [platform.openai.com/docs/models](https://platform.openai.com/docs/models) |
| **Gemini**（Google）| 3.5 Flash / 3.5 Pro（开发中）| 2M | 长 context / 原生 multimodal / Google 整合 | PDF / 影音 / 大量文件 / Google Workspace | [ai.google.dev](https://ai.google.dev/gemini-api/docs/models/gemini) |

> **注**：`（开发中）`= 还没推出。Claude **Fable 5**（Mythos-class、位阶在 Opus 之上、$10/$50）是目前最强的 Claude 层级；**Opus 5**（2026-07-24 推出、`claude-opus-5`、1M、$5/$25，跟前一代 Opus 4.8 同价）是官方 docs 建议的默认起点，Anthropic 宣称它“接近 Fable 5 的能力、一半的价格”。**Opus 4.8 仍可用**（官方 docs 已移入 Legacy 区、未 deprecated）。Context 栏填的是旗舰的上限：Gemini Pro 系列 2M、Flash 1M；Claude 1M（Haiku 4.5 是 200k）；GPT-5.6 三款都是 1.05M。另外 **Sonnet 5**（2026-06-30 上线）是目前的 Sonnet 版本：1M context、速度快、比 Opus 便宜（$3/$15，Opus 是 $5/$25）。**GPT-5.6**（2026-07 上线）分三级：**Sol** 旗舰（$5/$30）、**Terra** 均衡（$2.50/$15）、**Luna** 最快最省（$1/$6），ChatGPT / Codex / API 都能用。

### 🇨🇳 中国商业 + 开源 frontier（7 家）

中文场景的主力，分两类：**纯 API**（云端付费、不能 self-host）和**有开源 weights**（可在自己机器跑）。

**① 纯 API（云端、付费为主）**

| Model 家族 | 旗舰（2026-05）| Context | 强项 | 适合任务 | 官方 |
|---|---|---|---|---|---|
| **DeepSeek**（深度求索）| V4-Flash（`deepseek-v4-flash`）/ V4-Pro（`deepseek-v4-pro`）| 1M | 推理 / coding / **cost 最低** | 大量 token / code 生成 / math | [api-docs.deepseek.com](https://api-docs.deepseek.com/zh-cn/) |
| **Kimi**（Moonshot）| K3（2.8T 参数、原生多模态）| **1M** | 长 context / 中文长文 | 整本书读 / 文献分流 | [platform.moonshot.cn](https://platform.moonshot.cn/) |
| **Hunyuan**（腾讯）| T1（深度思考）+ TurboS | 128k | **深度思考推理**（对标 DeepSeek R1 这条 2025 推理基线）、中文 | 中文推理 / 腾讯生态 | [hunyuan.tencent.com](https://hunyuan.tencent.com/) |
| **MiniMax** | M3 | 1M | 多模态 / 中文长 prose / coding | 中文写作 / 影音 multimodal | [platform.minimax.io](https://platform.minimax.io/) |

> **注**：这组以云端 API 为主、多为 proprietary。DeepSeek 另有部分开源权重（在 HF），主要用法仍是云端 API（旧名 `deepseek-chat`/`deepseek-reasoner` 于 2026-07-24 停用、已改指向 v4-flash）。

**② 有开源 weights（可 self-host）**

| Model 家族 | 旗舰（2026-05）| Context | 强项 | 适合任务 | 官方 |
|---|---|---|---|---|---|
| **Qwen**（阿里）| Qwen 3.7 / 3.6（开源）| 128k+ | **中文最强 OSS** / 多模态 / agent | 中文长文 / agent / self-host | [qwen.ai](https://qwen.ai/) · [DashScope](https://help.aliyun.com/zh/dashscope/) |
| **GLM**（智谱 Zhipu）| GLM-5.2 | 1M | 中文 / tool use / agent | 中文 agent / 多轮对话 | [open.bigmodel.cn](https://open.bigmodel.cn/) · [chatglm.cn](https://chatglm.cn/) |
| **Yi**（01.AI / 李开复）| Yi-Lightning / Yi-34B-Chat | 200k | **中文 OSS**（⚠️ 01.AI 2025 起停 foundation 训练、Yi 已冻结）| 中文 self-host / 中文 API | [01.ai](https://01.ai/) · [GitHub](https://github.com/01-ai/Yi) |

> **注**：这三家都走 **开源版（Apache 2.0 或 MIT）+ 付费云端 API** 两条路（GLM 开源版现为 5.2、MIT）。开源版可用 [Ollama](https://ollama.com/) 在自己机器跑。

> ⚠️ **小米 MiMo** 虽在 [`resources/cli-agents-guide.zh-Hans.md`](../resources/cli-agents-guide.zh-Hans.md) 列入 Hermes Agent routing，但 2026-05 无权威官方 source 可验证，暂不收进此表。要试 → 通过 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 200+ provider routing 接入。

### 🌍 西方开源（5 家、self-host 主力）

跑在自己机器、不付 API、隐私敏感场景的主力——可通过 [Ollama](https://ollama.com/) 一行指令装起来：

| Model 家族 | 大小（活跃）| License | 强项 | 适合任务 | 官方 |
|---|---|---|---|---|---|
| **Llama**（Meta）| 3.3 70B | Llama Community License | 通用 / 生态最广 / Ollama 默认 | self-host 入门 / fine-tune base | [llama.com](https://www.llama.com/) · [HF Meta](https://huggingface.co/meta-llama) |
| **Muse**（Meta）| Glimmer 30B dense | Apache 2.0 | **agent 专用**（tool use / 长任务 / 失败恢复）/ 多模态输入 / 131k context | 本机 agent / coding agent / 单张消费级 GPU | [developer.meta.com](https://developer.meta.com/ai/models/muse-glimmer/) · [HF meta-models](https://huggingface.co/meta-models/Muse-Glimmer-30B) |
| **Gemma**（Google）| Gemma 4 26B MoE + 31B dense | Apache 2.0 | **小巧高效** / Apple MLX 整合好 / multimodal | Edge / mobile / 4-8GB RAM 机器 | [ai.google.dev/gemma](https://ai.google.dev/gemma) |
| **Mistral**（Mistral AI）| Small 4 / Ministral 3 / Large 3 | 开源权重（license 依版本、Large 3 为 Apache 2.0）| Small 4 统一 reasoning / vision / coding、EU 主权 | 商用 self-host / EU 主权 | [mistral.ai](https://mistral.ai/) · [HF Mistral](https://huggingface.co/mistralai) |
| **Phi**（Microsoft）| Phi-4 14B + multimodal | MIT | **小但强** / reasoning / 适合 edge | 4GB+ RAM / mobile / reasoning 入门 | [HF microsoft](https://huggingface.co/microsoft) |

> **注**：Llama 4（Scout / Maverick）于 2025-04 发布，但属大型 MoE，单机自架的实用基准仍是 3.3 70B（表中为 3.3）、Behemoth 未发布；Gemma 4 为 2026-04 发布、LMArena 开源组第 3；Phi-4 另有 multimodal 版。**Muse Glimmer** 为 2026-08-10 发布、Meta 第一个专为 agent 设计的开放权重模型，由闭源的 **Muse Spark** 蒸馏而来（Meta 自己说它“整体不如 Spark”）；**Spark 的 weights 目前还没发布**——Meta 说会放，但 HF 上还查不到，所以这里只收 Glimmer。注意 Meta 现在两条线并行:Llama 走 Llama Community License,Muse 走 Apache 2.0。

### 🎯 我该选哪家？（按场景反查）

| 你的场景 | 推荐 + 为什么 |
|---|---|
| 第一次学 LLM API、教材完整度优先 | **Claude** — Anthropic Cookbook + Courses 是社群公认最完整 |
| 写长文 / paper / code review | **Claude Sonnet** — long-form prose 强项 |
| 多模态（PDF / 影音 / 图）| **Gemini** 或 **Kimi** — 原生 multimodal |
| 广度查询 + function calling 框架 | **GPT** — ecosystem 最广、SDK 整合最深 |
| **中文场景 + 商业 API** | **Kimi**（长 context 强、能塞整本书）或 **DeepSeek**（cost 最低）或 **GLM**（agent 友好）|
| **中文场景 + 开源 self-host** | **Qwen 3.7 / GLM-5.2**（Apache 2.0 / MIT、中文最强 OSS 之一）|
| 推理 / math（reasoning model）| **DeepSeek V4-Pro** / **Hunyuan T1** / **OpenAI o-series** |
| 隐私 / offline / 不付 API | **Llama 3.3** / **Gemma 4** / **Qwen 3 OSS** via [Ollama](https://ollama.com/) |
| Edge / 4GB RAM 机器 | **Gemma 4** / **Phi-4** / **Qwen 3（`qwen3-3B` 或以下版本）** |
| 100k+ token 大文件 | **Gemini 3.1**（2M context）或 **Kimi K3**（1M）|
| **想 cost 最低**（API 账单敏感）| **DeepSeek V4-Flash** — 同级英文 model 中 token 单价最低 |

### 📊 中立 benchmark 资源（自己 verify、不靠单一 source）

| 资源 | 用途 | URL | 2026-05 状态 |
|---|---|---|---|
| **Artificial Analysis** | 第三方 benchmark + price/latency 整合（含中国 model）| https://artificialanalysis.ai/ | ✓ Active |
| **Arena AI**（前 LMSYS Chatbot Arena）| 人类盲测 ELO 排名 | https://arena.ai/leaderboard/text | ✓ Active |
| **Vellum LLM leaderboard** | 多 benchmark 整合 | https://www.vellum.ai/llm-leaderboard | ✓ Active |
| **HuggingFace OpenLLM Leaderboard** | 开源 model 排名 | https://huggingface.co/spaces/open-llm-leaderboard | ⚠️ 2026-05 偶尔 runtime error、改看 [Arena AI](https://arena.ai/) 开源 tab |
| **SuperCLUE**（中文 benchmark）| 中文场景权威评测 | https://www.superclueai.com/ | ✓ Active |

### ⚠️ 重要警语

- ⚠️ **Benchmark ≠ production performance**——LLM 在你 specific 任务的表现要自己跑 small eval（例如贴 10 个你真实 prompt 看哪家答得最像你要的）、**不能只看排名选**
- ⚠️ **Frontier 6 个月洗牌一次**——上面所有数字是 **2026-05 snapshot**、之后请以**官方 docs** / [Artificial Analysis](https://artificialanalysis.ai/) 为准
- ⚠️ **“强项”是相对的、不是绝对的**——所有 frontier model 都能完成基本任务、差别在特殊或困难的情境（超长文件、复杂推理、多语言）
- ⚠️ **中文场景看 [SuperCLUE](https://www.superclueai.com/)**——一般国际 benchmark（如 MMLU）以英文为主、中文表现可能跟英文不一致

## 🚪 进入条件

你需要具备以下基础：

- 编写 Python 脚本。
- 理解基本的 HTTP / REST 概念。
- 获取并使用 API key（Anthropic / OpenAI / Google）。

如果没有，请先完成 Stage 0。

## 📚 必修阅读

1. [**Anthropic - Claude 模型概览**](https://docs.claude.com/en/about-claude/models/overview) - 官方模型总览，包含 2026 的 Claude Fable 5（`claude-fable-5`、Mythos-class、2026-06-09 GA）以及 Opus 5 / Sonnet 5 / Haiku 4.5。**Fable 5 是目前最高阶的 Claude 层级；Opus 5（2026-07-24 推出、`claude-opus-5`）是现行的 Opus 级旗舰，Opus 4.8 仍可用（官方 docs 已移入 Legacy 区、未 deprecated）。**
2. [**anthropics/courses — Anthropic API Fundamentals**](https://github.com/anthropics/courses) ⭐⭐⭐⭐⭐ ★ 22k+ — Anthropic 官方 5 course umbrella、**module 1“Anthropic API Fundamentals”对应本 stage**。Jupyter notebook、用 Claude 3 Haiku（最便宜）跑、跟着做就能拿到 API 基本功。
3. [**OpenAI Quickstart**](https://platform.openai.com/docs/quickstart) - 学习发送你的第一个 API call。
4. [**A Visual Guide to LLM Tokenizers**](https://huggingface.co/learn/llm-course/chapter6/1) - Hugging Face 的图文并茂指南。
5. [**Anthropic API Pricing**](https://www.anthropic.com/pricing#anthropic-api) - 了解并比较模型成本（例如，1k input + 1k output 的价格）。

**🎥 中文视频补充（强烈推荐）**：

- [**李宏毅 — 生成式 AI 导论（2024 春台大课程）**](https://speech.ee.ntu.edu.tw/~hylee/genai/2024-spring.php) ⭐⭐⭐ — 第 1-5 集讲 LLM 是什么、怎么运作、token / context window / temperature 怎么影响输出。中文圈最高质量的 LLM 学术级导论、台大授课、官方页含幻灯片 + YouTube。最新整合版见 [**GenAI-ML 2025 秋**](https://speech.ee.ntu.edu.tw/~hylee/GenAI-ML/2025-fall.php)
- [**3Blue1Brown — Transformer 可视化**](https://www.youtube.com/watch?v=wjZofJX0v4M)（中文配音版：[3Blue1Brown 中文](https://space.bilibili.com/88461692)）— LLM 内部运作的可视化入门
- [**Andrej Karpathy — Intro to LLMs**](https://www.youtube.com/watch?v=zjkBMFhNj_g) — 英文视频、1 小时、英文圈最被推荐的 LLM 入门视频

## 🛠 动手练习（基础 illustrative 练习）

> 🦙 **本 stage 默认用 Ollama**（成本考量、本机 `gemma4:e4b` 跑得动、$0/run）。每个练习都有 Path A（Ollama、默认）+ Path B（Anthropic、选择性、想看 cloud 高质量时用）。完整 3 路 trade-off 见 [`examples/README.zh-Hans.md`](../examples/README.zh-Hans.md#三条路径--默认用-ollama成本考量)。
>
> 💰 **Stage 1 预算估算**（全 6 练习各跑 3-5 次）：**全本机 = $0**、**全 haiku ≈ $0.30**、**全 sonnet ≈ $0.90**。完整 model 清单 + Stage 1-7 全程预算估算见 [`examples/README.zh-Hans.md#推荐-llm-清单`](../examples/README.zh-Hans.md#推荐-llm-清单)。
>
> 💡 **只想读、不想装 Ollama** — 直接看每个练习的 Path B（Anthropic）区块就好。想实际跑 Path A 才需要 [`pip install openai && ollama pull gemma4:e4b`](https://ollama.com) 就装好 Path A 环境。

### 练习 1：LLM API（hello world）
五行 Python 调用 LLM 并打印响应。**默认用 Ollama 本机跑（免费、offline）**；想看 cloud 答案质量改 Path B Anthropic。详见 [`examples/README.zh-Hans.md`](../examples/README.zh-Hans.md#三条路径--默认用-ollama成本考量)。

<details markdown="1" open>
<summary>📋 <b>起手码 — Path A（本机 Ollama gemma4:e4b、默认）</b>（复制到 <code>practice_1.py</code>、<code>python practice_1.py</code> 就跑）</summary>

```python
# 需要：pip install openai      (用 OpenAI 兼容 SDK 跟 Ollama 沟通)
# 前置：ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama 不检查、随便填
)

r = client.chat.completions.create(
    model="gemma4:e4b",   # 换成 qwen2.5:3b / llama3.2:3b 也可
    max_tokens=100,
    messages=[{"role": "user", "content": "用一句话自我介绍。"}],
)

# === 自我验证 ===
text = r.choices[0].message.content
print("回应：", text)
print("usage:", r.usage)

assert r.choices[0].finish_reason in ("stop", "length"), f"非预期 finish_reason: {r.choices[0].finish_reason}"
assert len(text) > 0, "回应不应为空"
assert r.usage.completion_tokens > 0, "output token 应 > 0"
print("✅ 练习 1 通过 — Ollama gemma4:e4b 已能本机回应、$0/次")
```

**预期输出**（样本）：
```
回应：嗨！我是 Gemma、一个由 Google 训练的开源语言模型...
usage: CompletionUsage(completion_tokens=35, prompt_tokens=12, total_tokens=47)
✅ 练习 1 通过 — Ollama gemma4:e4b 已能本机回应、$0/次
```

**慢吗？** Gemma 4B 在 CPU 上约 5-30s/答案、有 GPU（RTX 3060+）<2s。要更快用 `gemma3:1b`、要更聪明改 `qwen2.5:14b` / `llama3.3:8b`（需 8GB+ VRAM）。

</details>

<details markdown="1">
<summary>📋 <b>起手码 — Path B（Anthropic API、选择性、想看 cloud 高质量时）</b>（复制到 <code>practice_1_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
# 环境变量：export ANTHROPIC_API_KEY=sk-ant-...
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-haiku-4-5",  # haiku 最便宜；换 sonnet 改这行
    max_tokens=100,
    messages=[{"role": "user", "content": "用一句话自我介绍。"}],
)

# === 自我验证 ===
text = msg.content[0].text
print("回应：", text)
print("usage:", msg.usage)

assert msg.stop_reason in ("end_turn", "max_tokens"), f"非预期 stop_reason: {msg.stop_reason}"
assert len(text) > 0, "回应不应为空"
assert msg.usage.input_tokens > 0 and msg.usage.output_tokens > 0, "token 数应 > 0"
print("✅ 练习 1 通过 — 你已成功打通 Anthropic API")
```

**预期输出**（样本）：
```
回应：我是 Claude，一个由 Anthropic 训练的 AI 助理...
usage: Usage(input_tokens=18, output_tokens=42, ...)
✅ 练习 1 通过 — 你已成功打通 Anthropic API
```

**成本**：每次 ~$0.001 (haiku) / $0.004 (sonnet)、跑这个 hello world 比 Ollama 快 5-15 倍。

</details>

### 练习 2：Tokens
同一个 prompt 跑 100 次，观察 token 数的变化。

- 注意：`temperature ≠ 0` 会产生变动
- 注意：同一句话的英文 vs 中文 token 数差异

<details markdown="1" open>
<summary>📋 <b>起手码 — Path A（本机 Ollama gemma4:e4b、默认）</b>（复制到 <code>practice_2.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

PROMPTS = {
    "中文": "用一句话描述一只猫在做什么。",
    "English": "Describe in one sentence what a cat is doing.",
}

N = 10  # 本机慢、N 小一点
for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(N):
        r = client.chat.completions.create(
            model="gemma4:e4b",
            max_tokens=80,
            temperature=1.0,
            messages=[{"role": "user", "content": prompt}],
        )
        output_tokens.append(r.usage.completion_tokens)
    print(f"\n[{label}] prompt: {prompt}")
    print(f"  input tokens: {r.usage.prompt_tokens}")
    print(f"  output tokens — min={min(output_tokens)} max={max(output_tokens)} mean={statistics.mean(output_tokens):.1f} stdev={statistics.stdev(output_tokens):.1f}")

# === 自我验证 ===
assert max(output_tokens) > min(output_tokens), "temperature=1.0 下、output 长度应该有 variance"
print("\n✅ 练习 2 通过 — 本机跑 $0")
print("💡 中文 prompt 通常 input tokens 比 English 多（中文 token 化通常一字 ≈ 2 tokens）")
```

**预期输出**（样本）：
```
[中文] prompt: 用一句话描述一只猫在做什么。
  input tokens: 32
  output tokens — min=18 max=58 mean=35.2 stdev=11.4

✅ 练习 2 通过 — 本机跑 $0
```

</details>

<details markdown="1">
<summary>📋 <b>起手码 — Path B（Anthropic API、选择性）</b>（复制到 <code>practice_2_anthropic.py</code>）</summary>

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

**主要差异**：`messages.create` → `chat.completions.create`；`usage.output_tokens` → `usage.completion_tokens`；`usage.input_tokens` → `usage.prompt_tokens`。**成本**：40 次 ≈ $0.01。

</details>

### 练习 3：Pricing / Latency
**成本敏感的工作必修**：算出你的 hello-world prompt 在不同 model 上跑 1000 次的成本。Ollama 本机是 $0 但有 latency 成本；Cloud LLM 有 $ 成本但快。**会算这两个 trade-off 才能挑对 model**。

<details markdown="1" open>
<summary>📋 <b>起手码 — Path A（本机 Ollama gemma4:e4b、量 latency）</b>（复制到 <code>practice_3.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys, time
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

latencies = []
for _ in range(5):
    t0 = time.time()
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[{"role": "user", "content": "你好！自我介绍一下。"}],
    )
    latencies.append(time.time() - t0)

avg_latency = sum(latencies) / len(latencies)
out_tok_avg = r.usage.completion_tokens
tps = out_tok_avg / avg_latency if avg_latency > 0 else 0

print(f"model: gemma4:e4b (本机)")
print(f"5 次 latency (sec): min={min(latencies):.2f} max={max(latencies):.2f} mean={avg_latency:.2f}")
print(f"avg output: {out_tok_avg} tokens、约 {tps:.1f} tokens/sec")
print(f"\n1000 次成本: $0 (本机)、预计时长: {avg_latency * 1000 / 60:.1f} 分钟")

# === 自我验证 ===
assert avg_latency > 0, "latency 应 > 0"
assert out_tok_avg > 0, "output token 应 > 0"
print(f"\n✅ 练习 3 通过 — 本机 model $0 但要花 {avg_latency * 1000 / 60:.0f} 分钟跑 1000 次")
print("💡 对照 Path B Anthropic：1000 次只要 ~10-20 分钟但要 $0.25（haiku）")
```

**预期输出**（样本）：
```
model: gemma4:e4b (本机)
5 次 latency (sec): min=4.21 max=8.93 mean=6.54
avg output: 48 tokens、约 7.3 tokens/sec

1000 次成本: $0 (本机)、预计时长: 109.0 分钟

✅ 练习 3 通过 — 本机 model $0 但要花 109 分钟跑 1000 次
💡 对照 Path B Anthropic：1000 次只要 ~10-20 分钟但要 $0.25（haiku）
```

</details>

<details markdown="1">
<summary>📋 <b>起手码 — Path B（Anthropic API、算 $ 成本）</b>（复制到 <code>practice_3_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

# Anthropic 2026 Q2 公开计价（每 1M token、USD）— 运行前对照 https://www.anthropic.com/pricing
PRICING = {
    "claude-haiku-4-5":   {"input": 1.00, "output":  5.00},
    "claude-sonnet-5":    {"input": 3.00, "output": 15.00},  # 标准价；2026-08-31 前为优惠价 2.00 / 10.00
    "claude-opus-5":      {"input": 5.00, "output": 25.00},  # Opus 5（2026-07-24、接替 Opus 4.8）—— 维持 5/25 同价
    "claude-fable-5":     {"input": 10.00, "output": 50.00},  # Fable 5（Mythos-class、最高层级）约 Opus 的 2 倍
}

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"
msg = client.messages.create(model=MODEL, max_tokens=200,
                             messages=[{"role": "user", "content": "你好！自我介绍一下。"}])
in_tok, out_tok = msg.usage.input_tokens, msg.usage.output_tokens
rates = PRICING[MODEL]
cost_one = (in_tok * rates["input"] + out_tok * rates["output"]) / 1_000_000

print(f"model: {MODEL}")
print(f"single: input={in_tok} output={out_tok} → ${cost_one:.6f}")
print(f"1000 calls cost across model tiers:")
for name, r in PRICING.items():
    c = (in_tok * r["input"] + out_tok * r["output"]) / 1_000_000 * 1000
    print(f"  {name:<22} ${c:.4f}")

assert cost_one > 0, "Cloud LLM 一定有成本"
print(f"\n✅ 练习 3 通过（Anthropic）— 1000 次 haiku ≈ $0.25、sonnet 5 ≈ $0.76、opus 5 ≈ $1.27")
```

**预期输出**：
```
model: claude-haiku-4-5
single: input=14 output=48 → $0.000254
1000 calls cost across model tiers:
  claude-haiku-4-5       $0.2540
  claude-sonnet-5        $0.7620
  claude-opus-5          $1.2700
  claude-fable-5         $2.5400
```

**Trade-off 对照**：本机 Ollama 跑 1000 次免费但要 ~2 hr；Anthropic haiku ~10 min $0.25；sonnet ~10 min $0.76。**production 场景才考虑 cloud；学习 / 实验 / debug 全用本机**。

</details>

### 练习 4：Cross-Provider 比较
同一个 prompt 同时送给 Claude、GPT、Gemini，比较三家的响应差异。观察“同一句话为什么产生不同答案”——回答风格、长度、判断取舍都不一样。建议用 OpenAI、Anthropic、Google 三家 SDK 各一段程序调用。

→ **基础 starter 范本** → [`examples/stage-1/04-cross-provider/`](../examples/stage-1/04-cross-provider/)（含三家 SDK 并行调用 + table 对照、缺哪家 key 就 skip 哪家；illustrative，**不是 chapter-length 完整教程**）

### 练习 5：Error Handling
故意触发错误情境并写 retry：

- API key 错误 → 看怎么 raise
- prompt 超长 → context window 满了会发生什么
- 网络断掉 → 写一个有 exponential backoff 的 retry wrapper

这是后面 Stage 3-8 写 production agent 一定会用到的基础。

→ **基础 starter 范本** → [`examples/stage-1/05-error-handling/`](../examples/stage-1/05-error-handling/)（含 mock-based test、不用真的断网就能验证 retry 逻辑；illustrative，**不是 chapter-length 完整教程**）

### 练习 6：Local LLM
**不付 API 费用、跑在自己电脑上**：用 Ollama 下载一个小模型（建议 `llama3.2:3b` 或 `qwen2.5:3b`），用 OpenAI 兼容 API 调用它。

```bash
# 1. 装 Ollama: https://ollama.com
ollama pull qwen2.5:3b
ollama serve  # 预设 port 11434
```

<details markdown="1">
<summary>📋 <b>起手码</b>（复制到 <code>practice_6.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：Ollama 已 serve、qwen2.5:3b 已 pull
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama 不检查、随便填
)

r = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": "用 3 句话介绍什么是 ReAct。"}],
)

text = r.choices[0].message.content
print("回应：", text)

# === 自我验证 ===
assert len(text) > 10, "回应太短、Ollama 可能没跑起来"
print(f"✅ 练习 6 通过 — 你的本机 Ollama 已能透过 OpenAI 兼容 API 呼叫")
print(f"💡 跑这次完全没花钱（除了你的电力）")
```

**预期输出**（样本、实际内容因 model 而异）：
```
回应：ReAct 是一种让 AI 结合“推理”和“行动”的方法...
✅ 练习 6 通过 — 你的本机 Ollama 已能透过 OpenAI 兼容 API 呼叫
💡 跑这次完全没花钱（除了你的电力）
```

**为什么要做**：学会跑本地 LLM 后，后面 Stage 3-6 的实验都不会被 API 费用卡住；隐私敏感场景也能 offline。

**没装 Ollama 也想跑**：把 `base_url` 换成 [LM Studio](https://lmstudio.ai)（`http://localhost:1234/v1`）或 [vLLM](https://github.com/vllm-project/vllm) endpoint、API 接口一样。

</details>

## 🎯 精选 Projects

按用途分 5 类、17 个项目一张表搞定。**挑入口看“适合谁”、想深入点连结看 repo / 课程网站**。

| 分类 | Project | ⭐ | 适合谁 | 为什么推荐 / 备注 |
|---|---|---|---|---|
| **官方 cookbook / 入门** | [Anthropic Cookbook](https://github.com/anthropics/claude-cookbooks) | ⭐⭐⭐⭐⭐ | 开始用 Claude API、当参考书查 | Claude API 全功能 notebook（tool use / batch / prompt cache），★ 50k+、MIT |
| | [Anthropic Courses](https://github.com/anthropics/courses) | ⭐⭐⭐⭐⭐ | 系统性从零学一遍 Claude | Anthropic 自家完整 5 门课（API 基础 / prompt eval / real-world prompting / tool use），★ 22k+。先跑 `anthropic_api_fundamentals` |
| | [OpenAI Cookbook](https://github.com/openai/openai-cookbook) | ⭐⭐⭐⭐⭐ | 用 OpenAI API + structured output / function calling | 跟 Anthropic Cookbook 对照、★ 73k+、MIT。比 Anthropic 大很多、用搜索 |
| | [Anthropic Claude API Quickstart](https://docs.anthropic.com/en/docs/get-started) | ⭐⭐⭐⭐ | 5 分钟上手 | 官方文件、加 bookmark 用 |
| **中文教材**<br>（章节式） | [datawhalechina/happy-llm](https://github.com/datawhalechina/happy-llm) | ⭐⭐⭐⭐⭐ | 中文读者想彻底搞懂 LLM 原理 | 对应 Karpathy“Zero to Hero”中文版，★ 32k+。等同 HF LLM Course 中文版 |
| | [datawhalechina/llm-universe](https://github.com/datawhalechina/llm-universe) | ⭐⭐⭐⭐⭐ | 中文新手想用 LLM 做东西 | API 基础 / 知识库 / RAG / 进阶技巧，★ 13k+ |
| | [datawhalechina/llm-cookbook](https://github.com/datawhalechina/llm-cookbook) | ⭐⭐⭐⭐ | 想要完整中文 LLM 学习路线 | Andrew Ng 课程中文翻译改编（⚠️ 2025-06 后更新放缓、CC BY-NC-SA）|
| | [jingyaogong/minimind](https://github.com/jingyaogong/minimind) | ⭐⭐⭐⭐ | 看完 Karpathy 视频想实际跑训练 | 2hr 从零训 64M LLM、Pretrain + SFT + LoRA + DPO + RLHF 全包，★ 53k+、Apache-2.0 |
| **英文 course**<br>（系统式） | [HuggingFace — LLM Course](https://huggingface.co/learn/llm-course) | ⭐⭐⭐⭐⭐ | 想搞懂 transformer 内部 + HF 生态 | 含 transformer 原理 + 应用、Apache 2.0 |
| | [LangChain Academy](https://academy.langchain.com/) | ⭐⭐⭐⭐ | 喜欢视频教学的视觉型学习者 | LangChain 官方免费课、含 RAG / agent。**忽略 LangChain 行销段落** |
| **本地端执行**<br>（不付 API 费）| [ollama/ollama](https://github.com/ollama/ollama) | ⭐⭐⭐⭐⭐ | 第一次跑本地 LLM | 本 repo Path A 预设、OpenAI-compat API、★ 170k+ |
| | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | ⭐⭐⭐⭐⭐ | 想搞懂 quantization / 为什么 7B 能塞 8GB RAM | Ollama 底层 inference engine，★ 119k+、MIT |
| | [mudler/LocalAI](https://github.com/mudler/LocalAI) | ⭐⭐⭐⭐ | 团队合规、要 self-host 全套 OpenAI 替代 | drop-in OpenAI API 替代品（chat / embedding / image / TTS / STT），★ 48k+ |
| | [ml-explore/mlx](https://github.com/ml-explore/mlx) | ⭐⭐⭐⭐ | Mac 开发、想榨干 Apple Silicon | Apple 为 M1+ 量身打造的 ML framework，★ 27k+。搭 `mlx-lm` 用最方便 |
| **从零打造**<br>（理解原理）| [karpathy — Let's build GPT from scratch](https://www.youtube.com/watch?v=kCc8FmEb1nY) | ⭐⭐⭐⭐⭐ | 想搞懂 LLM 内部、不只会调用 | 2hr 高密度视频、用 PyTorch 从零打造 GPT。**暂停跟着写 code 不要被动看** |
| | [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) | ⭐⭐⭐⭐⭐ | 想用整本书速度慢慢读完 | Karpathy 视频的书本版：tokenizer → attention → pretraining → finetuning，★ 100k+、Apache-2.0 |
| | [karpathy/LLM101n](https://github.com/karpathy/LLM101n) | ⭐⭐ | 历史纪录 | ⚠️ 已封存（2024-08）、只有大纲、课程没做完。**直接看上面的“Build GPT from scratch”视频即可** |

> 💡 **建议阅读路径**：API 入手就 Anthropic / OpenAI Cookbook → 中文系统路线就 happy-llm + llm-universe → 想深入内部就 Karpathy 视频 + rasbt 书搭 code → 想跑本地就 Ollama 起步、进阶再读 llama.cpp。

## ✅ 进 Stage 2 前的自我检查

你需要完成以下任务：

- [ ] 写一个 5 行的 Python 脚本调用 Claude API。
- [ ] 理解“基础概念”中的至少 2 个 token（例如，“Hello” 是 1 个）。
- [ ] 比较 Claude Sonnet vs Opus 的 per-token 价格。
- [ ] 体验至少 2 个不同的 LLM（Claude / GPT / Gemini / Llama）。

如果都完成了，恭喜，进入 [Stage 2 - Prompt Engineering](./02-prompt-engineering.zh-Hans.md)。

如果卡住了，回到 Anthropic Quickstart + 完成至少 3 个 hello-X 脚本。

---

> ✅ **Stage 1 完成？** 接下来 [**Stage 2 — Prompt Engineering**](02-prompt-engineering.zh-Hans.md) 会用 5-12 小时带你写出可重用的结构化 prompt、用 few-shot 跟 chain-of-thought 解推理题、并学会用 eval 量化 prompt 改善幅度。**继续往下走 →**

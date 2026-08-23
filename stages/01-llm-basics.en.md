# Stage 1 — LLM Fundamentals

> [繁體中文](./01-llm-basics.md) | [简体中文](./01-llm-basics.zh-Hans.md) | **English**


⏱ **Time estimate**: 1 week (~5-8 hours)

> 👋 **Coming from [Stage 0](00-foundations.en.md)?** Nice — your toolchain is set. The next 5-8 hours: your first working call to Claude / GPT / Gemini, how token / context window / temperature shape the output, and per-token cost estimation. **Jumped straight here?** Make sure you can run a Python script and have an API key from one provider — if not, head back to [Stage 0](00-foundations.en.md).

> 💡 **Don't recognize a term?** (LLM / token / context window / temperature / RAG / agent / …) → check [`resources/glossary.en.md`](../resources/glossary.en.md) for 30-second definitions.

> 📋 **Structure of this chapter**: learning goals → prerequisites → required reading → 〔optional · concept map〕→ hands-on exercises → curated projects → self-check  
> 🔑 **Key terms**: see [`resources/glossary.en.md`](../resources/glossary.en.md) (every term each stage uses is collected there)

### 3 Core Terms (memorize these—all later stages use them)

| Term | Chinese | One-liner |
|---|---|---|
| **token** | 詞元 | the unit LLMs use to count text length and price (1 Chinese char ≈ 1.5-2 tokens; 1 English word ≈ 1.3 tokens) |
| **context window** | 上下文視窗 | How many tokens the model sees at once (Claude 1M / GPT 1.05M / Gemini 2M) |
| **temperature** | 隨機程度參數 | Controls how stable or creative the output is (0 = deterministic, 1 = creative; use 0.0-0.3 for classification, 0.7-1.0 for creative writing) |

→ These 3 terms run through every later stage. The goal of Stage 1 is to call the API yourself and feel firsthand how they shape the output.

> 🧠 **Why you can tune temperature: first, next-token**: an LLM's core action is **predicting the next token**. It computes a probability distribution over the next token and **samples** one from it. `temperature` and `top_p` reshape that distribution: low temperature makes it sharper, almost always picking the most likely token (stable, reproducible); high temperature flattens it, so it more readily picks rare tokens (creative but prone to wandering). `max_tokens` just caps how many samples before stopping. So these are not magic knobs; they control *how the model picks tokens from a probability distribution*.

## 📌 Learning Goals

After this stage you will be able to:

- Explain what an LLM is, what tokens are, and what context window means
- Make your first API call to Claude / GPT / Gemini and parse the response
- Compare the four major LLM families (Claude / GPT / Gemini / Llama) on strengths
- Estimate cost per task using per-token pricing

## 🌐 Major LLM Family Comparison (2026-05 snapshot)

"How is Claude different from GPT?" "Can I use Chinese models?" "Which OSS model should I run with Ollama?" This section gives you an **objective side-by-side view**. It does not declare a single "best" model: it compares **strengths / good-fit tasks / weaknesses** and includes **official docs URLs** so you can verify the claims yourself.

> 💡 **First, a few terms**:
> - **Context window** = the amount of conversation an LLM can remember in one pass; it is capped (for example, 200k tokens ~= 150k Chinese characters)
> - **Apache 2.0 / MIT** = open-source terms that permit commercial use, modification, and closed-source redistribution; **Llama Community License** = open-source but with conditions (for example, orgs with >= 700M MAU need a license)
> - **Frontier model** = each provider's strongest flagship; **OSS** = open-source, with weights downloadable for self-hosting

### 🇺🇸 US Commercial Frontier (3 providers)

These 3 are SaaS APIs: you pay per token and cannot self-host them.

<!-- How to keep these 3 tables tidy: the "Flagship" cell lists only the current flagship, plus at most the one before it; when a newer one ships, swap the name in rather than piling them up, and delete any name that is old or no longer in the official docs. Anything that changes over time (suspended / preview / not-yet-out) does not go in the cell -- put it in the "Note" line under the table, and delete that line once the status is over (released / restored / retired for good). The "Context" cell holds just a number. Update the (2026-MM) in the header when you edit. -->

| Model family | Flagship (2026-07) | Context | Strengths | Best for | Official docs |
|---|---|---|---|---|---|
| **Claude** (Anthropic) | Opus 5 / Sonnet 5 / Haiku 4.5 | 1M | long-form / coding / agent / safety alignment | writing papers / code review / agent runtime | [platform.claude.com/docs](https://platform.claude.com/docs/en/about-claude/models/overview) |
| **GPT** (OpenAI) | GPT-5.6 Sol / Terra / Luna | 1.05M | general-purpose / function calling / broadest ecosystem | broad queries / function-call frameworks / GPTs ecosystem | [platform.openai.com/docs/models](https://platform.openai.com/docs/models) |
| **Gemini** (Google) | 3.5 Flash / 3.5 Pro (in dev) | 2M | long context / native multimodal / Google integration | PDF / video and audio / large document sets / Google Workspace | [ai.google.dev](https://ai.google.dev/gemini-api/docs/models/gemini) |

> **Note**: `(in dev)` = not released yet. Claude **Fable 5** (Mythos-class, above Opus, $10/$50) is the strongest Claude tier; **Opus 5** (launched 2026-07-24, `claude-opus-5`, 1M, $5/$25 — same price as the previous Opus 4.8) is the default starting point the official docs recommend, and Anthropic claims it reaches "near Fable 5 intelligence at half the cost". **Opus 4.8 is still available** (moved to the Legacy section of the docs, not deprecated). Context is the flagship's ceiling: Gemini Pro series 2M, Flash 1M; Claude 1M (Haiku 4.5 is 200k); all three GPT-5.6 tiers are 1.05M. Also, **Sonnet 5** (launched 2026-06-30) is the current Sonnet: 1M context, fast, and cheaper than Opus ($3/$15 vs Opus $5/$25). **GPT-5.6** (launched 2026-07) comes in three tiers: **Sol** flagship ($5/$30), **Terra** balanced ($2.50/$15), **Luna** fastest and cheapest ($1/$6) — available in ChatGPT, Codex, and the API.

### 🇨🇳 Chinese Commercial + Open-Source Frontier (7 providers)

These are the main choices for Chinese-language work, in two groups: **API-only** (cloud, paid, can't self-host) and **open weights** (can run on your own machine).

**① API-only (cloud, mostly paid)**

| Model family | Flagship (2026-05) | Context | Strengths | Best for | Official |
|---|---|---|---|---|---|
| **DeepSeek** | V4-Flash (`deepseek-v4-flash`) / V4-Pro (`deepseek-v4-pro`) | 1M | reasoning / coding / **lowest cost** | high-token workloads / code generation / math | [api-docs.deepseek.com](https://api-docs.deepseek.com/zh-cn/) |
| **Kimi** (Moonshot) | K3 (2.8T params, native multimodal) | **1M** | long context / Chinese long-form writing | whole-book reading / literature triage | [platform.moonshot.cn](https://platform.moonshot.cn/) |
| **Hunyuan** (Tencent) | T1 (deep-thinking) + TurboS | 128k | **deep-thinking reasoning** (measured against the 2025 DeepSeek R1 baseline), Chinese | Chinese reasoning / Tencent ecosystem | [hunyuan.tencent.com](https://hunyuan.tencent.com/) |
| **MiniMax** | M3 | 1M | multimodal / Chinese long prose / coding | Chinese writing / video and audio multimodal | [platform.minimax.io](https://platform.minimax.io/) |

> **Note**: This group is mostly cloud-API and proprietary. DeepSeek also has some open weights (on HF), but the cloud API is still the main way to use it (the legacy names `deepseek-chat`/`deepseek-reasoner` retire 2026-07-24 and now alias to v4-flash).

**② Open weights (self-hostable)**

| Model family | Flagship (2026-05) | Context | Strengths | Best for | Official |
|---|---|---|---|---|---|
| **Qwen** (Alibaba) | Qwen 3.7 / 3.6 (open) | 128k+ | **strongest Chinese OSS** / multimodal / agent | Chinese long-form writing / agent / self-host | [qwen.ai](https://qwen.ai/) · [DashScope](https://help.aliyun.com/zh/dashscope/) |
| **GLM** (Zhipu) | GLM-5.2 | 1M | Chinese / tool use / agent | Chinese agents / multi-turn chat | [open.bigmodel.cn](https://open.bigmodel.cn/) · [chatglm.cn](https://chatglm.cn/) |
| **Yi** (01.AI / Kai-Fu Lee) | Yi-Lightning / Yi-34B-Chat | 200k | **Chinese OSS** (⚠️ 01.AI stopped foundation training in 2025; Yi is frozen) | Chinese self-host / Chinese API | [01.ai](https://01.ai/) · [GitHub](https://github.com/01-ai/Yi) |

> **Note**: All three offer both an **open version (Apache 2.0 or MIT) and a paid cloud API** (GLM's open version is now 5.2, MIT). The open versions run on your own machine via [Ollama](https://ollama.com/).

> ⚠️ **Xiaomi MiMo** is listed in [`resources/cli-agents-guide.en.md`](../resources/cli-agents-guide.en.md) for Hermes Agent routing, but as of 2026-05 there is no authoritative official source to verify it, so it is not included in this table. To try it, connect through [Hermes Agent](https://github.com/NousResearch/hermes-agent) 200+ provider routing.

### 🌍 Western Open-Source (5 providers, self-host defaults)

These are the main choices for running on your own hardware, avoiding API fees, or handling privacy-sensitive work. You can install them in one command through [Ollama](https://ollama.com/).

| Model family | Active size | License | Strengths | Best for | Official |
|---|---|---|---|---|---|
| **Llama** (Meta) | 3.3 70B | Llama Community License | general-purpose / broadest ecosystem / Ollama default | self-hosting intro / fine-tune base | [llama.com](https://www.llama.com/) · [HF Meta](https://huggingface.co/meta-llama) |
| **Muse** (Meta) | Glimmer 30B dense | Apache 2.0 | **purpose-built for agents** (tool use / long tasks / failure recovery) / multimodal input / 131k context | local agents / coding agents / a single consumer GPU | [developer.meta.com](https://developer.meta.com/ai/models/muse-glimmer/) · [HF meta-models](https://huggingface.co/meta-models/Muse-Glimmer-30B) |
| **Gemma** (Google) | Gemma 4 26B MoE + 31B dense | Apache 2.0 | **small and efficient** / strong Apple MLX integration / multimodal | edge / mobile / 4-8 GB RAM machines | [ai.google.dev/gemma](https://ai.google.dev/gemma) |
| **Mistral** (Mistral AI) | Small 4 / Ministral 3 / Large 3 | open weights (license varies; Large 3 is Apache 2.0) | Small 4 unifies reasoning / vision / coding; EU sovereignty | commercial self-host / EU sovereignty | [mistral.ai](https://mistral.ai/) · [HF Mistral](https://huggingface.co/mistralai) |
| **Phi** (Microsoft) | Phi-4 14B + multimodal | MIT | **small but strong** / reasoning / edge-friendly | 4 GB+ RAM / mobile / reasoning intro | [HF microsoft](https://huggingface.co/microsoft) |

> **Note**: Llama 4 (Scout / Maverick) shipped 2025-04, but they're large MoE models, so 3.3 70B remains the practical single-GPU self-host base (the table shows 3.3); Behemoth never shipped. Gemma 4 was released 2026-04, ranked #3 on LMArena's open-weights board; Phi-4 also has a multimodal version. **Muse Glimmer** shipped 2026-08-10 and is Meta's first open-weight model built specifically for agents, distilled from the closed **Muse Spark** (Meta's own card calls it "generally less capable than Muse Spark"); **Spark's weights are not released** — Meta says they will be, but nothing is on Hugging Face yet, so only Glimmer is listed here. Note that Meta now runs two lines in parallel: Llama under the Llama Community License, Muse under Apache 2.0.

### 🎯 Which One Should I Pick? (by scenario)

| Your scenario | Pick + why |
|---|---|
| First time learning an LLM API, prioritize complete tutorials | **Claude** — Anthropic Cookbook + Courses are widely considered the most complete |
| Long-form writing / papers / code review | **Claude Sonnet** — long-form prose is a core strength |
| Multimodal (PDF / video and audio / images) | **Gemini** or **Kimi** — native multimodal |
| Broad queries + function calling frameworks | **GPT** — broadest ecosystem and deepest SDK integration |
| **Chinese scenarios + commercial API** | **Kimi** (strong long context; can fit whole books), **DeepSeek** (lowest cost), or **GLM** (agent-friendly) |
| **Chinese scenarios + open-source self-host** | **Qwen 3.7 / GLM-5.2** (Apache 2.0 / MIT; among the strongest Chinese OSS) |
| Reasoning / math (reasoning model) | **DeepSeek V4-Pro** / **Hunyuan T1** / **OpenAI o-series** |
| Privacy / offline / no API fees | **Llama 3.3** / **Gemma 4** / **Qwen 3 OSS** via [Ollama](https://ollama.com/) |
| Edge / 4 GB RAM machine | **Gemma 4** / **Phi-4** / **Qwen 3 (`qwen3-3B` or smaller variants)** |
| 100k+ token large documents | **Gemini 3.1** (2M context) or **Kimi K3** (1M) |
| **Want the lowest cost** (API-bill sensitive) | **DeepSeek V4-Flash** — lowest token price among same-tier English models |

### 📊 Neutral Benchmark Resources (verify for yourself; do not rely on one source)

| Resource | Use | URL | 2026-05 status |
|---|---|---|---|
| **Artificial Analysis** | Third-party benchmarks plus price/latency aggregation, including Chinese models | https://artificialanalysis.ai/ | ✓ Active |
| **Arena AI** (formerly LMSYS Chatbot Arena) | Human blind-test ELO leaderboard | https://arena.ai/leaderboard/text | ✓ Active |
| **Vellum LLM leaderboard** | Aggregates multiple benchmarks | https://www.vellum.ai/llm-leaderboard | ✓ Active |
| **HuggingFace OpenLLM Leaderboard** | Open-source model rankings | https://huggingface.co/spaces/open-llm-leaderboard | ⚠️ Occasional runtime errors as of 2026-05; use the [Arena AI](https://arena.ai/) open-source tab as fallback |
| **SuperCLUE** | Authoritative benchmark for Chinese-language scenarios | https://www.superclueai.com/ | ✓ Active |

### ⚠️ Important Caveats

- ⚠️ **Benchmark != production performance**: run a small eval on your specific task (for example, paste 10 real prompts and see which model answers closest to what you need); **do not pick only from rankings**
- ⚠️ **Frontier changes every 6 months**: all numbers above are a **2026-05 snapshot**; afterward, rely on **official docs** / [Artificial Analysis](https://artificialanalysis.ai/)
- ⚠️ **"Strength" is relative, not absolute**: every frontier model can handle basic tasks; differences matter at the margin
- ⚠️ **For Chinese scenarios, check [SuperCLUE](https://www.superclueai.com/)**: general international benchmarks such as MMLU are English-heavy, and Chinese-language performance may diverge

## 🚪 Entry Conditions

You should already:

- Be able to run a Python script
- Know what HTTP / REST is conceptually
- Have an API key from at least one provider (Anthropic / OpenAI / Google)

If not — go back to Stage 0 first.

## 📚 Required Reading

1. [**Anthropic — Claude Model Overview**](https://docs.claude.com/en/about-claude/models/overview) — official model family overview, including 2026's Claude Fable 5 (`claude-fable-5`, Mythos-class, GA 2026-06-09) plus Opus 5 / Sonnet 5 / Haiku 4.5. **Fable 5 is the highest Claude tier; Opus 5 (launched 2026-07-24, `claude-opus-5`) is the current Opus-class flagship, and Opus 4.8 is still available as legacy (moved to the docs' Legacy section, not deprecated).**
2. [**anthropics/courses — Anthropic API Fundamentals**](https://github.com/anthropics/courses) ⭐⭐⭐⭐⭐ ★ 22k+ — Anthropic's official 5-course umbrella; **module 1 "Anthropic API Fundamentals" maps to this stage**. Jupyter notebooks, runs on Claude 3 Haiku (cheapest), hands-on walkthrough of API essentials.
3. [**OpenAI Quickstart**](https://platform.openai.com/docs/quickstart) — first API call walkthrough
4. [**A Visual Guide to LLM Tokenizers**](https://huggingface.co/learn/llm-course/chapter6/1) — Hugging Face's intro
5. [**Anthropic API Pricing**](https://www.anthropic.com/pricing#anthropic-api) — read the pricing table, calculate cost for 1k input + 1k output

**🎥 Video supplements (highly recommended)**:

- [**Hung-yi Lee — Introduction to Generative AI (NTU, Spring 2024)**](https://speech.ee.ntu.edu.tw/~hylee/genai/2024-spring.php) ⭐⭐⭐ — episodes 1-5 cover what an LLM is, how it works, and how token / context window / temperature shape the output. a university-level Mandarin-language course taught at National Taiwan University; the course page carries slides plus YouTube. Latest consolidated edition: [**GenAI-ML, Fall 2025**](https://speech.ee.ntu.edu.tw/~hylee/GenAI-ML/2025-fall.php)
- [**3Blue1Brown — Transformers, visually explained**](https://www.youtube.com/watch?v=wjZofJX0v4M) (Mandarin dub: [3Blue1Brown 中文](https://space.bilibili.com/88461692)) — a visual intro to what happens inside an LLM
- [**Andrej Karpathy — Intro to LLMs**](https://www.youtube.com/watch?v=zjkBMFhNj_g) — English, 1 hr, the most widely recommended LLM primer in English

## 🛠 Hands-on Exercises (foundational, illustrative)

> 🦙 **This stage defaults to Ollama** (cost-driven; `gemma4:e4b` runs locally for $0/run). Every exercise has Path A (Ollama, default) + Path B (Anthropic, optional — use it when you want to see cloud-quality answers). Full three-path trade-off in [`examples/README.en.md`](../examples/README.en.md#three-paths--default-is-ollama-cost-driven).
>
> 💰 **Stage 1 budget estimate** (all 6 exercises, 3-5 runs each): **all local = $0**, **all haiku ≈ $0.30**, **all sonnet ≈ $0.90**. Full model list + Stage 1-7 total budget: [`examples/README.en.md#recommended-llm-list`](../examples/README.en.md#recommended-llm-list).
>
> 💡 **Only reading, not installing Ollama?** Just use each exercise's Path B (Anthropic) block. You only need this if you actually want to run Path A: [`pip install openai && ollama pull gemma4:e4b`](https://ollama.com).

### Exercise 1: LLM API (hello world)
Five-line Python script that calls an LLM and prints the response. **Defaults to local Ollama (free, offline)**; switch to Path B Anthropic when you want cloud-quality answers. Details in [`examples/README.en.md`](../examples/README.en.md#three-paths--default-is-ollama-cost-driven).

<details markdown="1" open>
<summary>📋 <b>Starter code — Path A (local Ollama gemma4:e4b, default)</b> (copy to <code>practice_1.py</code> and run <code>python practice_1.py</code>)</summary>

```python
# Requires: pip install openai      (OpenAI-compatible SDK talks to Ollama)
# Pre-req: ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama doesn't check this — anything works
)

r = client.chat.completions.create(
    model="gemma4:e4b",   # swap to qwen2.5:3b / llama3.2:3b if preferred
    max_tokens=100,
    messages=[{"role": "user", "content": "Introduce yourself in one sentence."}],
)

# === Self-check ===
text = r.choices[0].message.content
print("Response:", text)
print("usage:", r.usage)

assert r.choices[0].finish_reason in ("stop", "length"), f"unexpected finish_reason: {r.choices[0].finish_reason}"
assert len(text) > 0, "response should not be empty"
assert r.usage.completion_tokens > 0, "output token count should be > 0"
print("✅ Exercise 1 passed — local Ollama gemma4:e4b answered for $0")
```

**Expected output** (sample):
```
Response: Hi! I'm Gemma, an open-source language model trained by Google...
usage: CompletionUsage(completion_tokens=35, prompt_tokens=12, total_tokens=47)
✅ Exercise 1 passed — local Ollama gemma4:e4b answered for $0
```

**How slow?** Gemma 4B on CPU: ~5-30 s/answer; on GPU (RTX 3060+): <2 s. For speed use `gemma3:1b`; for quality use `qwen2.5:14b` / `llama3.3:8b` (needs 8 GB+ VRAM).

</details>

<details markdown="1">
<summary>📋 <b>Starter code — Path B (Anthropic API, optional, when you want cloud quality)</b> (copy to <code>practice_1_anthropic.py</code>)</summary>

```python
# Requires: pip install anthropic
# Env: export ANTHROPIC_API_KEY=sk-ant-...
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-haiku-4-5",  # haiku = cheapest; switch to sonnet by changing this line
    max_tokens=100,
    messages=[{"role": "user", "content": "Introduce yourself in one sentence."}],
)

# === Self-check ===
text = msg.content[0].text
print("Response:", text)
print("usage:", msg.usage)

assert msg.stop_reason in ("end_turn", "max_tokens"), f"unexpected stop_reason: {msg.stop_reason}"
assert len(text) > 0, "response should not be empty"
assert msg.usage.input_tokens > 0 and msg.usage.output_tokens > 0, "token counts should be > 0"
print("✅ Exercise 1 passed — Anthropic API is reachable from your machine")
```

**Expected output** (sample):
```
Response: I'm Claude, an AI assistant made by Anthropic...
usage: Usage(input_tokens=18, output_tokens=42, ...)
✅ Exercise 1 passed — Anthropic API is reachable from your machine
```

**Cost**: ~$0.001/run (haiku) or ~$0.004/run (sonnet); this hello-world is also 5-15× faster than Ollama.

</details>

### Exercise 2: Tokens
Run the same prompt 100 times and watch token counts vary.

- Notice: `temperature ≠ 0` produces variation
- Notice: token count for the SAME English vs Chinese sentence

<details markdown="1" open>
<summary>📋 <b>Starter code — Path A (local Ollama gemma4:e4b, default)</b> (copy to <code>practice_2.py</code>)</summary>

```python
# Requires: pip install openai
# Pre-req: ollama pull gemma4:e4b && ollama serve
import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

PROMPTS = {
    "Chinese": "用一句話描述一隻貓在做什麼。",
    "English": "Describe in one sentence what a cat is doing.",
}

N = 10  # local is slower; start small
for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(N):
        r = client.chat.completions.create(
            model="gemma4:e4b",
            max_tokens=80,
            temperature=1.0,  # high temp to amplify variance
            messages=[{"role": "user", "content": prompt}],
        )
        output_tokens.append(r.usage.completion_tokens)
    print(f"\n[{label}] prompt: {prompt}")
    print(f"  input tokens: {r.usage.prompt_tokens}")
    print(f"  output tokens — min={min(output_tokens)} max={max(output_tokens)} mean={statistics.mean(output_tokens):.1f} stdev={statistics.stdev(output_tokens):.1f}")

# === Self-check ===
assert max(output_tokens) > min(output_tokens), "with temperature=1.0, output length should vary"
print("\n✅ Exercise 2 passed — observed temperature → token variance, $0/run")
print("💡 Chinese prompts typically use MORE input tokens (one Chinese character ≈ 2 tokens)")
```

**Expected output** (sample):
```
[Chinese] prompt: 用一句話描述一隻貓在做什麼。
  input tokens: 32
  output tokens — min=18 max=58 mean=35.2 stdev=11.4

✅ Exercise 2 passed — observed temperature → token variance, $0/run
```

</details>

<details markdown="1">
<summary>📋 <b>Starter code — Path B (Anthropic API, optional)</b> (copy to <code>practice_2_anthropic.py</code>)</summary>

```python
# Requires: pip install anthropic
import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic
client = anthropic.Anthropic()
PROMPTS = {"Chinese": "用一句話描述一隻貓在做什麼。", "English": "Describe in one sentence what a cat is doing."}

for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(20):
        msg = client.messages.create(model="claude-haiku-4-5", max_tokens=80, temperature=1.0,
                                     messages=[{"role": "user", "content": prompt}])
        output_tokens.append(msg.usage.output_tokens)
    print(f"[{label}] input={msg.usage.input_tokens} output min/max/mean={min(output_tokens)}/{max(output_tokens)}/{sum(output_tokens)/len(output_tokens):.1f}")
```

**Key SDK diffs**: `messages.create` → `chat.completions.create`; `usage.output_tokens` → `usage.completion_tokens`; `usage.input_tokens` → `usage.prompt_tokens`. **Cost**: 40 runs ≈ $0.01.

</details>

### Exercise 3: Pricing / Latency
**Cost-sensitive work required**: compute how long and how much it takes to run 1000 hello-world inferences. Local Ollama is $0 but has latency cost; cloud LLMs cost money but are faster. **Knowing this trade-off is how you pick the right model**.

<details markdown="1" open>
<summary>📋 <b>Starter code — Path A (local Ollama gemma4:e4b, measure latency)</b> (copy to <code>practice_3.py</code>)</summary>

```python
# Requires: pip install openai
# Pre-req: ollama pull gemma4:e4b && ollama serve
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
        messages=[{"role": "user", "content": "Hi! Please introduce yourself."}],
    )
    latencies.append(time.time() - t0)

avg_latency = sum(latencies) / len(latencies)
out_tok_avg = r.usage.completion_tokens
tps = out_tok_avg / avg_latency if avg_latency > 0 else 0

print(f"model: gemma4:e4b (local)")
print(f"5 latencies (sec): min={min(latencies):.2f} max={max(latencies):.2f} mean={avg_latency:.2f}")
print(f"avg output: {out_tok_avg} tokens, ~{tps:.1f} tokens/sec")
print(f"\n1000-run cost: $0 (local); projected duration: {avg_latency * 1000 / 60:.1f} minutes")

# === Self-check ===
assert avg_latency > 0, "latency should be > 0"
assert out_tok_avg > 0, "output token count should be > 0"
print(f"\n✅ Exercise 3 passed — local model is $0 but takes ~{avg_latency * 1000 / 60:.0f} min for 1000 runs")
print("💡 Compare Path B Anthropic: 1000 runs is ~10-20 min at $0.25 (haiku)")
```

**Expected output** (sample):
```
model: gemma4:e4b (local)
5 latencies (sec): min=4.21 max=8.93 mean=6.54
avg output: 48 tokens, ~7.3 tokens/sec

1000-run cost: $0 (local); projected duration: 109.0 minutes

✅ Exercise 3 passed — local model is $0 but takes ~109 min for 1000 runs
💡 Compare Path B Anthropic: 1000 runs is ~10-20 min at $0.25 (haiku)
```

</details>

<details markdown="1">
<summary>📋 <b>Starter code — Path B (Anthropic API, compute $ cost)</b> (copy to <code>practice_3_anthropic.py</code>)</summary>

```python
# Requires: pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

# Anthropic public pricing 2026 Q2 (per 1M tokens, USD) — verify at https://www.anthropic.com/pricing
PRICING = {
    "claude-haiku-4-5":   {"input": 1.00, "output":  5.00},
    "claude-sonnet-5":    {"input": 3.00, "output": 15.00},  # standard rate; introductory 2.00 / 10.00 through 2026-08-31
    "claude-opus-5":      {"input": 5.00, "output": 25.00},  # Opus 5 (2026-07-24, succeeds Opus 4.8) — same 5/25 pricing
    "claude-fable-5":     {"input": 10.00, "output": 50.00},  # Fable 5 (Mythos-class, highest tier) ~2x Opus
}

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"
msg = client.messages.create(model=MODEL, max_tokens=200,
                             messages=[{"role": "user", "content": "Hi! Please introduce yourself."}])
in_tok, out_tok = msg.usage.input_tokens, msg.usage.output_tokens
rates = PRICING[MODEL]
cost_one = (in_tok * rates["input"] + out_tok * rates["output"]) / 1_000_000

print(f"model: {MODEL}")
print(f"single: input={in_tok} output={out_tok} → ${cost_one:.6f}")
print(f"1000 calls cost across model tiers:")
for name, r in PRICING.items():
    c = (in_tok * r["input"] + out_tok * r["output"]) / 1_000_000 * 1000
    print(f"  {name:<22} ${c:.4f}")

assert cost_one > 0, "Cloud LLM always has a cost"
print(f"\n✅ Exercise 3 passed (Anthropic) — 1000 runs: haiku ≈ $0.25, sonnet 5 ≈ $0.76, opus 5 ≈ $1.27")
```

**Expected output**:
```
model: claude-haiku-4-5
single: input=14 output=48 → $0.000254
1000 calls cost across model tiers:
  claude-haiku-4-5       $0.2540
  claude-sonnet-5        $0.7620
  claude-opus-5          $1.2700
  claude-fable-5         $2.5400
```

**Trade-off**: local Ollama is $0 for 1000 runs but takes ~2 hr; Anthropic haiku is ~10 min for $0.25; sonnet ~10 min for $0.76. **Use cloud only for production; learning / experiments / debug stay local.**

</details>

### Exercise 4: Cross-Provider Comparison
Send the same prompt to Claude, GPT, and Gemini simultaneously, compare their responses. Notice "why does the same input produce different answers" — answer style, length, and judgment all differ. Use the OpenAI, Anthropic, and Google SDKs side-by-side.

→ **Starter template** → [`examples/stage-1/04-cross-provider/`](../examples/stage-1/04-cross-provider/) (parallel calls to all three SDKs + comparison table; missing keys are skipped gracefully; illustrative, **not a chapter-length tutorial**)

### Exercise 5: Error Handling
Trigger error conditions deliberately and write retry logic:

- Wrong API key → see how it raises
- Over-long prompt → what happens when the context window is full
- Network drop → write a retry wrapper with exponential backoff

This is foundational for Stage 3-8's production agent code.

→ **Starter template** → [`examples/stage-1/05-error-handling/`](../examples/stage-1/05-error-handling/) (mock-based tests so you can verify the retry logic without unplugging your ethernet cable; illustrative, **not a chapter-length tutorial**)

### Exercise 6: Local LLM
**No API fees, runs on your machine**: use Ollama to pull a small model (recommend `llama3.2:3b` or `qwen2.5:3b`), call it via OpenAI-compatible API.

```bash
# 1. Install Ollama: https://ollama.com
ollama pull qwen2.5:3b
ollama serve  # default port 11434
```

<details markdown="1">
<summary>📋 <b>Starter code</b> (copy to <code>practice_6.py</code>)</summary>

```python
# Requires: pip install openai
# Pre-req: Ollama is running, qwen2.5:3b is pulled
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama doesn't check this — anything works
)

r = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": "Explain ReAct in 3 sentences."}],
)

text = r.choices[0].message.content
print("Response:", text)

# === Self-check ===
assert len(text) > 10, "response is too short — Ollama may not be running"
print(f"✅ Exercise 6 passed — local Ollama reachable through the OpenAI-compatible API")
print(f"💡 This run cost you $0 (except for electricity)")
```

**Expected output** (sample; the actual wording varies by model):
```
Response: ReAct is a method that lets an AI combine "reasoning" and "acting"...
✅ Exercise 6 passed — local Ollama reachable through the OpenAI-compatible API
💡 This run cost you $0 (except for electricity)
```

**Why do this**: once you can run local LLMs, Stage 3-6 experiments aren't bottlenecked on API costs; privacy-sensitive work also stays offline.

**Want to run it without installing Ollama**: point `base_url` at [LM Studio](https://lmstudio.ai) (`http://localhost:1234/v1`) or a [vLLM](https://github.com/vllm-project/vllm) endpoint instead — the API surface is the same.

</details>

## 🎯 Curated Projects

5 categories, 17 projects in one table. **Pick by "Best for"; click through for depth on the repo / course site.**

| Category | Project | ⭐ | Best for | Why / Notes |
|---|---|---|---|---|
| **Official cookbook / starting point** | [Anthropic Cookbook](https://github.com/anthropics/claude-cookbooks) | ⭐⭐⭐⭐⭐ | Starting with Claude API; reference lookup | Full-feature Claude API notebooks (tool use / batch / prompt cache), ★ 50k+, MIT |
| | [Anthropic Courses](https://github.com/anthropics/courses) | ⭐⭐⭐⭐⭐ | Systematic Claude learning from zero | Anthropic's own 5-course set (API fundamentals / prompt eval / real-world prompting / tool use), ★ 22k+. Start with `anthropic_api_fundamentals` |
| | [OpenAI Cookbook](https://github.com/openai/openai-cookbook) | ⭐⭐⭐⭐⭐ | OpenAI API + structured output / function calling | Pair with Anthropic Cookbook, ★ 73k+, MIT. Much bigger than Anthropic's — use search |
| | [Anthropic Claude API Quickstart](https://docs.anthropic.com/en/docs/get-started) | ⭐⭐⭐⭐ | 5-minute start | Official docs, bookmark it |
| **Chinese textbook**<br>(chapter-style) | [datawhalechina/happy-llm](https://github.com/datawhalechina/happy-llm) | ⭐⭐⭐⭐⭐ | Chinese readers wanting LLM internals | Karpathy "Zero to Hero" Chinese counterpart, ★ 32k+. Equivalent to HF LLM Course in Chinese |
| | [datawhalechina/llm-universe](https://github.com/datawhalechina/llm-universe) | ⭐⭐⭐⭐⭐ | Chinese newcomers building with LLM | API basics / knowledge base / RAG / advanced tricks, ★ 13k+ |
| | [datawhalechina/llm-cookbook](https://github.com/datawhalechina/llm-cookbook) | ⭐⭐⭐⭐ | Full Chinese LLM learning path | Adapted Chinese translation of Andrew Ng's courses (⚠️ updates slowed after 2025-06, CC BY-NC-SA) |
| | [jingyaogong/minimind](https://github.com/jingyaogong/minimind) | ⭐⭐⭐⭐ | Post-Karpathy, want a real training run | 2hr to train a 64M LLM from scratch — Pretrain + SFT + LoRA + DPO + RLHF, ★ 53k+, Apache-2.0 |
| **English course**<br>(systematic) | [HuggingFace — LLM Course](https://huggingface.co/learn/llm-course) | ⭐⭐⭐⭐⭐ | Transformer internals + HF ecosystem | Transformer theory + applications, Apache 2.0 |
| | [LangChain Academy](https://academy.langchain.com/) | ⭐⭐⭐⭐ | Visual learners who like video courses | LangChain's official free course, includes RAG / agent. **Skip the LangChain marketing segments** |
| **Local execution**<br>(no API costs)| [ollama/ollama](https://github.com/ollama/ollama) | ⭐⭐⭐⭐⭐ | First-time local LLM | This repo's Path A default, OpenAI-compat API, ★ 170k+ |
| | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | ⭐⭐⭐⭐⭐ | Understanding quantization / how 7B fits in 8GB RAM | Ollama's underlying inference engine, ★ 119k+, MIT |
| | [mudler/LocalAI](https://github.com/mudler/LocalAI) | ⭐⭐⭐⭐ | Team compliance, self-host full OpenAI replacement | Drop-in OpenAI API replacement (chat / embedding / image / TTS / STT), ★ 48k+ |
| | [ml-explore/mlx](https://github.com/ml-explore/mlx) | ⭐⭐⭐⭐ | Mac dev, squeeze Apple Silicon | Apple's ML framework for M1+, ★ 27k+. Pair with `mlx-lm` for ease |
| **Build from scratch**<br>(understand internals)| [karpathy — Let's build GPT from scratch](https://www.youtube.com/watch?v=kCc8FmEb1nY) | ⭐⭐⭐⭐⭐ | Understand LLM internals, not just API calls | 2hr high-density video, build GPT in PyTorch from scratch. **Pause and code along, don't passive-watch** |
| | [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) | ⭐⭐⭐⭐⭐ | Book-pace read of the same material | Book version of Karpathy's video: tokenizer → attention → pretraining → finetuning, ★ 100k+, Apache-2.0 |
| | [karpathy/LLM101n](https://github.com/karpathy/LLM101n) | ⭐⭐ | Historical reference | ⚠️ Archived (2024-08), outline only, course never finished. **Watch "Build GPT from scratch" above instead** |

> 💡 **Suggested reading order**: API-first → Anthropic / OpenAI Cookbook · Chinese systematic path → happy-llm + llm-universe · deep internals → Karpathy video + rasbt book with code · local-only → start with Ollama, then llama.cpp.

## ✅ Self-Check Before Stage 2

Can you:

- [ ] Make a Claude API call from Python in 5 lines
- [ ] Explain why "你好" might use 2 tokens but "Hello" uses 1
- [ ] Quote roughly the per-token price for Claude Sonnet vs Opus
- [ ] Name one strength of Claude vs GPT vs Gemini vs Llama

If yes → proceed to [Stage 2 — Prompt Engineering](02-prompt-engineering.en.md).

If no → re-read the Anthropic Quickstart + run all 3 hello-X projects above.

---

> ✅ **Done with Stage 1?** Next, [**Stage 2 — Prompt Engineering**](02-prompt-engineering.en.md) takes 5-12 hours to walk you through writing reusable structured prompts, using few-shot and chain-of-thought for reasoning tasks, and learning to quantify prompt improvement with evals. **Keep going →**

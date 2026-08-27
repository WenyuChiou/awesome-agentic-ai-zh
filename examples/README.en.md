<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# `examples/` — Runnable hands-on exercises

> [← Back to main path README](../README.en.md)

Every stage in the learning roadmap has a "Hands-on Exercises" section that tells you *what* to do. This folder adds the **actual runnable starter code** — copy → install deps → `python starter.py` → see expected output.

## Directory layout

```
examples/
├── stage-2/                     # Prompt Engineering
│   ├── 01-prompt-eval-loop/     # Exercise: change one thing, then check the score
│   │   ├── starter.py           # Main program (fixed answers + --live)
│   │   ├── starter_anthropic.py # Anthropic comparison path
│   │   ├── test.py              # Ollama-path self-check
│   │   ├── test_anthropic.py    # Anthropic-path self-check
│   │   ├── README.md            # Three-language walkthrough (+.zh-Hans.md +.en.md)
│   │   └── requirements.txt     # Bounded dependency versions
├── stage-3/                     # Tool Use & Agent intro
│   ├── 03-react-from-scratch/   # Exercise 3: ReAct from scratch
│   │   ├── starter.py           # Main program (~70 LOC runnable)
│   │   ├── test.py              # Self-check (pure assert, no pytest)
│   │   ├── README.md            # 200-400-word walkthrough (+.zh-Hans.md +.en.md)
│   │   └── requirements.txt     # Pinned deps
│   └── ...
├── stage-1/
└── ...
```

Short exercises (≤30 LOC) stay inline as `<details markdown="1">` blocks in the stage doc — no folder. Longer ones (>30 LOC) get their own folder so stage docs don't get bloated by code blocks.

## How to run any example

```bash
cd examples/stage-3/03-react-from-scratch
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # Each example header lists the key it needs
python starter.py                     # Hits the real API to see output (~$0.001 in credits)
python test.py                        # Runs validation (mock-based, free)
```

## Design rules

| Dimension | Rule |
|---|---|
| Program length | starter ≤80 LOC, split if longer |
| Dependencies | stdlib + ≤2 pip packages, pinned versions |
| Tests | Plain `assert`, no pytest; reader runs `python test.py` to see ✅ |
| Comments | Chinese (zh-TW primary), English variable / function names |
| Self-check | Every starter.py ends with a `# === Self-check ===` block |
| Environment vars | Header comment must list required keys |
| Free-tier friendly | Use the cheapest model (claude-haiku / Ollama); note how to switch to Sonnet |
| **Windows encoding** | **Every .py must reconfigure stdout to UTF-8** (see below) |

### Windows cp950 encoding fix (mandatory in every starter.py / test.py)

Windows consoles default to cp950 (Big5) and can't print emoji or non-Big5 Chinese. Add this right after imports in every `.py`:

```python
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```

Without it, Windows readers running in PowerShell / cmd hit `UnicodeEncodeError: 'cp950' codec can't encode character '✅'`.

## Three paths — **default is Ollama (cost-driven)**

> 💰 **Why default to Ollama?** Running 1000 practice iterations on Sonnet costs ~$4; on haiku ~$0.25; on local Ollama $0. **API cost should not block learning.** Reserve cloud LLMs for "want to see high-quality answers / production deployment".

Every exercise ships with all three paths:

### Path A (**default, recommended**) — local Ollama
- Default `starter.py` / first inline `<details markdown="1">` block uses a local model
- Requires [Ollama](https://ollama.com); pull a model based on the stage:
  - **Stage 1 + 2** (plain chat / prompt eng): `ollama pull gemma4:e4b` (~7.5 GB; multimodal (text + image + audio); CPU-friendly)
  - **Stage 3+** (tool use / agent): `ollama pull qwen2.5:3b` (1.9 GB; reliable tool-use support)
- $0, offline, fine for privacy-sensitive data
- SDK uses the `openai` package (OpenAI-compatible API) with `base_url="http://localhost:11434/v1"`
- Best for: all readers (this is the default recommendation)

### Path B (optional) — Anthropic API (when you want cloud quality)
- Companion `starter_anthropic.py` (folder) or the second inline `<details markdown="1">` block
- Requires `ANTHROPIC_API_KEY`; ~$0.001 per run (haiku) / ~$0.004 (sonnet)
- Higher answer quality and lower latency than local 3-4B Ollama models
- Best for: production-quality demands, long-context work, the Stage 7 production tier

### Path C (verify logic, no API call)
- Every `test.py` uses `unittest.mock`; `python test.py` validates code logic without spending
- Complements A / B — mock first, then real call

### Trade-offs

| Dimension | A Ollama (default) | B Anthropic | C Mock |
|---|---|---|---|
| Cost per call | $0 | ~$0.001-0.004 | $0 |
| Requires | Ollama install | API key | nothing |
| Answer quality | medium (3-4B model) | high | canned, unrepresentative |
| Speed | 5-30 s/call (no GPU) | ~1-3 s/call | <0.1 s |
| Offline | ✅ | ❌ | ✅ |
| Privacy-sensitive data | ✅ | ❌ | ✅ |
| Stage 3+ tool use | ✅ (qwen2.5 / llama3.2) | ✅ | ✅ |
| Best for | **default, no budget pressure** | production upgrade | logic verification |

→ **Recommended flow**: C first (validate logic, no cost), then A (see real model behaviour locally), then B at the Stage 7 production stage if cloud quality is needed.

## Recommended LLM list

> Local + cloud, user-perspective.  
> 💡 You don't need to install every model — this table shows "which to use for practice" and "which to upgrade to for production". **Claude is the canonical / production reference; Ollama is the practice default.**

### Local LLMs (practice default, via Ollama)

| Model | Download | Recommended RAM | Stage | Tool-use | Speed (CPU/GPU) | Primary use |
|---|---|---|---|---|---|---|
| **`gemma4:e4b`** ⭐ | 7.5 GB | 8 GB | 1+2 | basic | slow / med | Stage 1-2 plain chat / prompt eng (default) |
| **`qwen2.5:3b`** ⭐ | 1.9 GB | 4 GB | 3+ | **reliable** | med / fast | Stage 3+ tool use / agent (default) |
| `llama3.2:3b` | 2.0 GB | 4 GB | 3+ | reliable | med / fast | qwen2.5:3b alternative |
| `mistral-nemo:12b` | 7.1 GB | 16 GB | 3+ | strong | slow / med | When you want closer-to-cloud quality |
| `qwen2.5:14b` | 9.0 GB | 16 GB | advanced | strong | slow / med | Larger-model comparison (GPU preferred) |
| `gemma4:e2b` | 4.0 GB | 4 GB | 1+2 | basic | med / fast | 4 GB-RAM-machine alternative |

Install: `ollama pull <model>` + `ollama serve`. Hardware tuning details: [resources/cli-agents-guide.en.md](../resources/cli-agents-guide.en.md).

### Cloud LLMs (canonical / production stack, via Anthropic)

| Model | $/1M input | $/1M output | Context | Primary use |
|---|---|---|---|---|
| `claude-fable-5` | $10 | $50 | 1M | Mythos-class (above Opus); suspended 2026-06-12, **restored 2026-07-01** (export controls lifted); the highest Claude tier |
| **`claude-haiku-4-5`** ⭐ | $1 | $5 | 200k | Cheapest; fine for Stage 1-7 cloud-quality comparisons |
| **`claude-sonnet-5`** ⭐ | $3 | $15 | 1M | **Production default**; Stage 5+ agent development |
| `claude-opus-5` | $5 | $25 | 1M | Opus-class flagship (launched 2026-07-24, succeeds Opus 4.8 at the same price); complex reasoning / long-context refactors |

> 💰 **Sonnet 5 is on introductory pricing right now**: the [official pricing page](https://platform.claude.com/docs/en/about-claude/pricing) lists **$2 / $10 through 2026-08-31**, reverting to the $3 / $15 shown above on 2026-09-01. The budget estimates below use the post-revert standard rate, so a run today costs roughly a third less than estimated.

Subscription alternative: Claude Pro $20/month (includes Sonnet usage); Claude Max $100/month (includes Opus). Details: [resources/cli-agents-guide.en.md](../resources/cli-agents-guide.en.md).

### Cloud LLM Chinese / open-source alternatives (region limits / budget / Chinese-language scenarios)

> Can't or don't want to use Anthropic? These APIs are **all OpenAI-compatible** — change `base_url` and model name to run the same exercises.

| Provider | Main model | $/1M input | $/1M output | OpenAI-compat? | Key selling point |
|---|---|---|---|---|---|
| **DeepSeek** ⭐ | `deepseek-v4-flash` | $0.14 | $0.28 | ✅ | Cheapest cloud (~7× cheaper than haiku $1/$5); strong CN & EN; free web at `chat.deepseek.com` |
| DeepSeek V4-Pro | `deepseek-v4-pro` | $0.44 | $0.87 | ✅ | Stronger reasoning; still far below same-tier pricing |
| **Moonshot Kimi** | `kimi-k3` | tiered | tiered | ✅ | **1M-token context** (key selling point); good for large files / long conversations; price is context-tiered — see platform. Free web at `kimi.com` |
| **Qwen (Alibaba)** | `qwen-max` / `qwen-turbo` | $0.50-1.50 | $1.50-6 | ✅ (DashScope) | Native Chinese; **same models also run locally via Ollama** (cloud + local both work) |
| **GLM (ZhipuAI)** | `glm-4.5` / `glm-4-plus` | $0.30-2 | $1.50-9 | ✅ | China-native, has free tier. Free web `chatglm.cn` |
| **NVIDIA NIM** | Llama / Mistral / DeepSeek / Qwen etc. hosted | free tier 1000 credits | (same) | ✅ | **Hosts 10+ open models**; new accounts get credits; no local GPU needed. `build.nvidia.com` |

**API endpoints (OpenAI SDK usage)**:

```python
# DeepSeek
client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com/v1")
r = client.chat.completions.create(model="deepseek-v4-flash", messages=[...])

# Moonshot Kimi (China endpoint; international uses .ai)
client = OpenAI(api_key=os.environ["MOONSHOT_API_KEY"], base_url="https://api.moonshot.cn/v1")
r = client.chat.completions.create(model="kimi-k3", messages=[...])

# Qwen (Alibaba DashScope)
client = OpenAI(api_key=os.environ["DASHSCOPE_API_KEY"],
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
r = client.chat.completions.create(model="qwen-turbo", messages=[...])

# GLM (ZhipuAI)
client = OpenAI(api_key=os.environ["ZHIPUAI_API_KEY"], base_url="https://open.bigmodel.cn/api/paas/v4")
r = client.chat.completions.create(model="glm-4.5-flash", messages=[...])

# NVIDIA NIM (hosted open-source)
client = OpenAI(api_key=os.environ["NVIDIA_API_KEY"], base_url="https://integrate.api.nvidia.com/v1")
r = client.chat.completions.create(model="meta/llama-3.3-70b-instruct", messages=[...])
```

**How to pick**:

| Scenario | Pick | Why |
|---|---|---|
| Mainland China, no cloud access | Ollama local / DeepSeek API | Local is free; DeepSeek has an in-China endpoint |
| Tight budget (< $1/month) | DeepSeek API | ~7× cheaper than haiku; quality close |
| Large files / long-doc RAG | Moonshot Kimi | 1M-token context |
| Chinese-native task (classical Chinese, CN search) | Qwen / GLM | Higher Chinese training corpus ratio |
| Want to try 10+ open models without GPU | NVIDIA NIM | One key, play with Llama / Mixtral / Qwen / DeepSeek |
| Production agent (tool use) | Anthropic Claude (canonical) | This repo's Path B default; tool calling most reliable |

### Budget estimate (completing all 54 exercises across Stage 1-7)

| Learning path | Total time | Total cost | Best for |
|---|---|---|---|
| **All local Ollama** | ~30 hr (CPU) / ~10 hr (GPU) | **$0** | Budget-conscious, privacy needs, China-mainland no-cloud-access |
| **Mixed: local practice + haiku final review** ⭐ | ~30 hr | **$2-5** | **Recommended default** — practice locally, run final 1-2 iterations on haiku to see cloud quality |
| **All haiku** | ~10 hr | $5-15 | Want speed, budget allows, want full cloud experience |
| **All sonnet** | ~8 hr | $20-50 | Deep practice with higher-quality answers, want high-quality answers |
| **Mixed: sonnet + opus on hard problems** | ~8 hr | $30-80 | Already a production agent developer |

> 🎯 **Beginner default**: run everything locally first; cap budget at $5. **Only consider upgrading to sonnet at the Stage 7 production tier.**

### How do I switch from Ollama to Anthropic?

Every exercise ships either a `<details markdown="1">` Path B block or a `starter_anthropic.py`. Three lines change:

```python
# From this (Path A default):
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
r = client.chat.completions.create(model="gemma4:e4b", ...)

# To this (Path B, if you have ANTHROPIC_API_KEY):
import anthropic
client = anthropic.Anthropic()
r = client.messages.create(model="claude-haiku-4-5", ...)
```

Main differences: the message-creation method name, the response shape (`choices[0].message.content` vs `content[0].text`), and how the tool spec is wrapped (OpenAI adds an extra `{"type": "function", "function": {...}}` layer). Full side-by-side table in [`resources/cli-agents-guide.en.md`](../resources/cli-agents-guide.en.md).

## Index by stage

| Stage | Exercises | Example location |
|---|---|---|
| 1 LLM basics | 6 | inline 4 + folder 2 (`examples/stage-1/`) |
| 2 Prompt engineering | 4 | inline 3 + folder 1 (`examples/stage-2/`) |
| **3 Tool use** | **6** | inline 1 + folder 5 (`examples/stage-3/`) |
| 4 Frameworks | 5 | all folder (`examples/stage-4/`) |
| 5 Claude Code ecosystem | 11 | inline 6 + folder 5 (`examples/stage-5/`) |
| 6 Memory/RAG | 5 | all folder (`examples/stage-6/`) |
| 7 Multi-agent | 5 | inline 1 + folder 4 (`examples/stage-7/`) |
| Track A1-A3 | 12 | all inline + 2 small folders (CLI-9 / CLI-10) |

→ T1 scope: **Stage 3 全 6 exercises only** (remaining stages roll out per plan tiers).

## Contributing / reporting issues

If something doesn't run, output doesn't match expectations, or you want to add a new example:

- File an issue tagged `examples`
- Or open a PR following the "Design rules" table above

## Why this split (instead of stuffing everything into stage docs)

1. **Stage docs stay readable** — roadmap readers don't always want code, they want concepts; long code blocks break that
2. **Examples evolve independently** — SDK bumps, model rename, example needs its own commit without polluting the roadmap's git log
3. **Readers can clone one example** — `svn export` or `git clone --filter=tree:0` grabs a single folder
4. **Future CI** — example failures shouldn't block mdbook deploy; this split lets CI run examples conditionally

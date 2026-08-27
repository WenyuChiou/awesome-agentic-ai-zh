<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# `examples/` — 动手练习可跑范例

> [← 回主路线 README](../README.zh-Hans.md)

学习地图每个 stage 都有“动手练习”section、讲“该做什么”。这个资料夹补上**真的可以跑的范例 code**——复制 → 装依赖 → `python starter.py` 看到预期输出。

## 目录结构

```
examples/
├── stage-2/                     # Prompt 设计
│   ├── 01-prompt-eval-loop/     # 练习：改一件事，再看分数
│   │   ├── starter.py           # 主程序（固定答案 + --live）
│   │   ├── starter_anthropic.py # Anthropic 对照版本
│   │   ├── test.py              # Ollama 路径自我验证
│   │   ├── test_anthropic.py    # Anthropic 路径自我验证
│   │   ├── README.md            # 三语走查（+.zh-Hans.md +.en.md）
│   │   └── requirements.txt     # 有上下限的依赖版本
├── stage-3/                     # Tool Use & Agent 入门
│   ├── 01-function-calling/     # 练习 1：一个工具、一次调用
│   │   ├── starter.py           # Ollama 路径
│   │   ├── starter_anthropic.py # Anthropic 路径
│   │   ├── test.py              # Ollama 路径自我验证
│   │   ├── test_anthropic.py    # Anthropic 路径自我验证
│   │   ├── README.md            # 三语走查（+.zh-Hans.md +.en.md）
│   │   ├── README.en.md         # English walkthrough
│   │   ├── README.zh-Hans.md    # 简体中文走查
│   │   └── requirements.txt     # 有上下限的依赖版本
│   ├── 03-react-from-scratch/   # 练习 3：从零实现 ReAct
│   │   ├── starter.py           # 主程序
│   │   ├── test.py              # 自我验证（pure assert、无 pytest）
│   │   ├── README.md            # 200-400 字走查（+.zh-Hans.md +.en.md）
│   │   └── requirements.txt     # 依赖钉版本
│   └── ...
├── stage-1/
└── ...
```

短的练习（≤30 LOC）直接以 `<details markdown="1">` 收折塞在 stage 档内、不开资料夹。长的（>30 LOC）才开资料夹——避免 stage 档被 code block 撑爆。

## 怎么跑任一个范例

```powershell
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py                     # Ollama 路径
$env:ANTHROPIC_API_KEY = "your-key"
python starter_anthropic.py           # Anthropic 路径
python test.py                        # 跑验证（用 mock、不花钱）
```

## 设计原则

| 维度 | 规则 |
|---|---|
| 程序长度 | starter ≤80 LOC、超过拆档 |
| 依赖 | stdlib + 最多 2 个 pip 套件、钉版本 |
| 测试 | 纯 `assert`、不用 pytest、reader 跑 `python test.py` 看 ✅ |
| 注解 | 中文（zh-Hans 为主）、变数 / 函数名英文 |
| 自我验证 | 每个 starter.py 结尾必有 `# === 自我验证 ===` 区块 |
| 环境变数 | 顶端注解写清楚需要哪些 key |
| Free-tier 友善 | 用最便宜 model（claude-haiku / Ollama）、注解写怎么换 Sonnet |
| **Windows 编码** | **每个 .py 顶端必须有 UTF-8 reconfigure**（见下） |

### Windows cp950 编码 fix（每个 starter.py / test.py 必加）

Windows 预设 console 是 cp950（Big5）、印不出 emoji 跟非 Big5 中文。每个 `.py` 档顶端 import 区后立刻加：

```python
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```

否则 Windows reader 在 PowerShell / cmd 跑会炸 `UnicodeEncodeError: 'cp950' codec can't encode character '✅'`。

## 三条路径 — **默认用 Ollama（成本考量）**

> 💰 **为什么默认 Ollama？** Ollama 的 API 成本是 $0，但不包含硬件和电费。Cloud LLM 按 token 计费：Haiku 4.5 每 1M input $1、每 1M output $5；预留 $0.05，用 `（input_tokens × $1 + output_tokens × $5） / 1,000,000` 估算，并以 2026-08-27 的官方定价核对。**学习阶段不该被 API 成本卡住**。

每个练习都同时提供 3 条路径：

### Path A（**默认、推荐**）— Ollama 本机
- 预设 `starter.py` / 第一个 inline `<details markdown="1">` 用本机 LLM
- 需 [Ollama](https://ollama.com)、按 stage pull 对应 model：
  - **Stage 1 + 2**（纯 chat / prompt eng）：`ollama pull gemma4:e4b`（~7.5 GB、多模态、CPU 跑得动）
  - **Stage 3+**（tool use / agent）：`ollama pull qwen2.5:3b`（1.9 GB；模型表现会变化，请在自己的电脑上运行文件夹内的固定测试）
- Ollama API 成本是 $0（不包含硬件和电费）、offline、隐私敏感资料 OK
- SDK 用 `openai` package（OpenAI 兼容 API）、`base_url="http://localhost:11434/v1"`
- 适合：所有读者（默认推这条）

### Path B（选择性）— Anthropic API（想看 cloud 高质量时）
- 对照 `starter_anthropic.py`（folder）或第二个 inline `<details markdown="1">` 区块
- 需 `ANTHROPIC_API_KEY`；按 Haiku 4.5 每 1M input $1、每 1M output $5 的公式估算，预留 $0.05，并以 2026-08-27 的官方定价核对
- 行为会随模型、提示和硬件而变；用固定 eval 实测
- 适合：production 要求高质量、需要 long-context、Stage 7 production tier

### Path C（验逻辑、不打 API）
- 所有 `test.py` 都用 `unittest.mock`、`python test.py` 看程序逻辑有没有写对
- 跟 Path A / B 互补：先 mock 验逻辑、再 real call 确认

### 三条路的 Trade-off

| 维度 | A Ollama（默认）| B Anthropic | C Mock |
|---|---|---|---|
| Cost / call | $0（不含硬件／电费） | $0.05 预留；按上方 token 公式 | $0 |
| 需要 | Ollama install | API key | 无 |
| 答案质量 | 会变化；请运行文件夹内的固定测试 | 会变化；请用同一组固定测试比较 | 预设答案，看不出模型的真实表现 |
| 速度 | 依硬件；用固定 eval 实测 | 依服务；用固定 eval 实测 | 依环境；用固定 eval 实测 |
| Offline | ✅ | ❌ | ✅ |
| 隐私敏感资料 | ✅ | ❌ | ✅ |
| Stage 3+ tool use | ✅（qwen2.5 / llama3.2） | ✅ | ✅ |
| 适合 | **默认、无预算压力** | production 升级 | 程序逻辑验证 |

→ **建议流程**：先 C 验逻辑（不花钱）、再 A 本机跑看实际 model 行为、production 阶段（Stage 7）再升 B 看 cloud 质量。

## 推荐 LLM 清单

> 本机 + cloud、user 视角。  
> 💡 不是要你全装、是让你看到“练习用哪个”“production 升级到哪个”。**Claude 是 canonical / production 主轴；Ollama 是练习默认**。

不知道怎么选时：Stage 1–2 用 `gemma4:e4b`，Stage 3 起用 `qwen2.5:3b`；想做 cloud 对照再用 Haiku 4.5。

<details markdown="1">
<summary>📚 展开：模型详表、价格和替代供应商</summary>

### 本机 LLM（练习默认、用 Ollama）

| Model | 下载大小 | 建议 RAM | 对应 Stage | Tool-use | 速度（CPU/GPU） | 主用途 |
|---|---|---|---|---|---|---|
| **`gemma4:e4b`** ⭐ | 7.5 GB | 8 GB | 1+2 | 基本 | 慢 / 中 | Stage 1-2 纯 chat / prompt eng（默认）|
| **`qwen2.5:3b`** ⭐ | 1.9 GB | 4 GB | 3+ | 会变化；请运行固定测试 | 依硬件实测 | Stage 3+ tool use / agent（默认）|
| `llama3.2:3b` | 2.0 GB | 4 GB | 3+ | 会变化；请运行固定测试 | 依硬件实测 | qwen2.5:3b 的替代 |
| `mistral-nemo:12b` | 7.1 GB | 16 GB | 3+ | 会变化；请运行固定测试 | 依硬件实测 | 用固定 eval 比较 |
| `qwen2.5:14b` | 9.0 GB | 16 GB | 进阶 | 会变化；请运行固定测试 | 依硬件实测 | 大 model 对照 |
| `gemma4:e2b` | 4.0 GB | 4 GB | 1+2 | 基本 | 依硬件实测 | 4GB RAM 机器替代 |

安装：`ollama pull <model>` + `ollama serve`。详细硬件配置看 [resources/cli-agents-guide.zh-Hans.md](../resources/cli-agents-guide.zh-Hans.md)。

### Cloud LLM（canonical / production 主轴、用 Anthropic）

| Model | 每 1M input | 每 1M output | Context | 主用途 |
|---|---|---|---|---|
| `claude-fable-5` | $10 | $50 | 1M | Mythos 级（位阶在 Opus 之上）；2026-06-12 暂停、**2026-07-01 恢复**（出口管制解除）——目前最高阶的 Claude 层级 |
| **`claude-haiku-4-5-20251001`** ⭐ | $1 | $5 | 200k | Stage 1-7 练习 cloud 对照 |
| **`claude-sonnet-5`** ⭐ | $2 | $10 | 1M | **production 默认**、Stage 5+ agent 开发 |
| `claude-opus-5` | $5 | $25 | 1M | Opus 级旗舰（2026-07-24 推出、接替 Opus 4.8、同价）、复杂推理 / 长 context refactor |

> 💰 API 价格已于 **2026-08-27** 对照 [Anthropic 官方定价页](https://platform.claude.com/docs/en/about-claude/pricing)。价格会变化；真正运行前请再看一次官方页面。

如果你使用订阅方案而不是 API 计费，请看官方方案页面；订阅额度和 API 费用不是一回事。工具选择详见 [resources/cli-agents-guide.zh-Hans.md](../resources/cli-agents-guide.zh-Hans.md)。

### Cloud LLM 中国 / 开源 alternatives（地区限制 / 预算敏感 / 中文场景）

> 不能 / 不想用 Anthropic？这些 API **都 OpenAI-compatible**、改 `base_url` 跟 model name 就能跑本 repo 同一份练习。

| Provider | 主 model | 每 1M input | 每 1M output | OpenAI-compat? | 主卖点 |
|---|---|---|---|---|---|
| **DeepSeek** ⭐ | `deepseek-v4-flash` | $0.14 | $0.28 | ✅ | 最便宜 cloud（比 haiku $1/$5 便宜约 7 倍）、中英文俱佳、含免费 web `chat.deepseek.com` |
| DeepSeek V4-Pro | `deepseek-v4-pro` | $0.44 | $0.87 | ✅ | 更强推理、价格仍远低于同级 |
| **Moonshot Kimi** | `kimi-k3` | 依阶梯 | 依阶梯 | ✅ | **1M token context**（卖点）、适合大文件 / 长对话；价格依 context 阶梯、见 platform。web 版 `kimi.com` 免费 |
| **通义千问 Qwen** | `qwen-max` / `qwen-turbo` | $0.50-1.50 | $1.50-6 | ✅（DashScope）| 中文 native、**同 model 也能 Ollama 本机跑**（cloud + local 两条路径都通） |
| **智谱 GLM** | `glm-4.5` / `glm-4-plus` | $0.30-2 | $1.50-9 | ✅ | 中国 native、有 free tier。web `chatglm.cn` 免费 |
| **NVIDIA NIM** | Llama / Mistral / DeepSeek / Qwen 等 hosted | free tier 1000 credits | (同) | ✅ | **托管 10+ open model**、新账号送 credits、不必本机 GPU。`build.nvidia.com` |

**API endpoints（OpenAI SDK 接法）**：

```python
# DeepSeek
client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com/v1")
r = client.chat.completions.create(model="deepseek-v4-flash", messages=[...])

# Moonshot Kimi（中国 endpoint；海外用 .ai 结尾）
client = OpenAI(api_key=os.environ["MOONSHOT_API_KEY"], base_url="https://api.moonshot.cn/v1")
r = client.chat.completions.create(model="kimi-k3", messages=[...])

# 通义千问 Qwen（Alibaba DashScope）
client = OpenAI(api_key=os.environ["DASHSCOPE_API_KEY"],
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
r = client.chat.completions.create(model="qwen-turbo", messages=[...])

# 智谱 GLM
client = OpenAI(api_key=os.environ["ZHIPUAI_API_KEY"], base_url="https://open.bigmodel.cn/api/paas/v4")
r = client.chat.completions.create(model="glm-4.5-flash", messages=[...])

# NVIDIA NIM（hosted open-source）
client = OpenAI(api_key=os.environ["NVIDIA_API_KEY"], base_url="https://integrate.api.nvidia.com/v1")
r = client.chat.completions.create(model="meta/llama-3.3-70b-instruct", messages=[...])
```

**怎么挑**：

| 情境 | 选 | 理由 |
|---|---|---|
| 中国大陆、无 cloud 访问 | Ollama 本机 / DeepSeek API | 本机免费；DeepSeek 在中国有 endpoint |
| 预算极敏感（< $1/月） | DeepSeek API | 列示 token 价格较低；用固定 eval 核对行为 |
| 大文件 / 长文档 RAG | Moonshot Kimi | 1M token context 卖点 |
| 中文 native task（古文、中文搜索）| Qwen / GLM | 训练语料中文占比高 |
| 想试 10+ open model 没 GPU | NVIDIA NIM | 一个 key 玩 Llama / Mixtral / Qwen / DeepSeek |
| Production agent（agent / tool use）| Anthropic Claude（canonical）| 本 repo Path B 默认；用固定 eval 核对 tool calling 行为 |

</details>

### 预算和时间怎么估（Stage 1–7 共 54 个练习）

<details markdown="1">
<summary>💰 展开：按自己的电脑和 token 用量计算</summary>

| 学习路径 | 时间怎么估 | 成本怎么估 | 适合谁 |
|---|---|---|---|
| **全本机 Ollama** | 用一个练习实测，再乘预计练习数 | API $0；不含硬件和电费 | 预算敏感、隐私需求、中国大陆无 cloud 访问 |
| **混合：本机练 + Haiku 终验** ⭐ | 本机实测时间 + cloud 调用次数 | 本机 API $0；cloud 按 Haiku token 公式 | **推荐默认**：先本机练，最后用同一组固定测试核对 cloud 行为 |
| **全 Haiku** | 按服务速度和调用次数实测 | `（input × $1 + output × $5）/ 1,000,000` | 想看完整 cloud 体验 |
| **全 Sonnet** | 按服务速度和调用次数实测 | `（input × $2 + output × $10）/ 1,000,000` | 深度练习和 production 对照 |
| **Sonnet 为主 + Opus 难题** | 按两种模型的调用次数实测 | 分别用官方 token 单价计算后相加 | 已是 production agent 开发者 |

> 🎯 **新手默认**：先在本机运行。要用 cloud 前，先用公式估算，再在供应商账户设置你能接受的费用上限。**Stage 7 production tier 才考虑 Sonnet 升级**。

</details>

### 怎么从 Ollama 换到 Anthropic？

每个练习都有 `<details markdown="1">` Path B 区块或 `starter_anthropic.py`，改 3 行：

```python
# 从这个（Path A 默认）：
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
r = client.chat.completions.create(model="gemma4:e4b", ...)

# 换成这个（Path B、若有 ANTHROPIC_API_KEY）：
import anthropic
client = anthropic.Anthropic()
r = client.messages.create(model="claude-haiku-4-5-20251001", ...)
```

主要差异：messages create 方法名、response shape（`choices[0].message.content` vs `content[0].text`）、tool spec wrap（OpenAI 多一层 `{"type": "function", "function": {...}}`）。详细对照表见 [`resources/cli-agents-guide.zh-Hans.md`](../resources/cli-agents-guide.zh-Hans.md)。

## 对应 stage 索引

| Stage | 练习 | 范例位置 |
|---|---|---|
| 1 LLM 基础 | 6 个 | inline 4 + folder 2（`examples/stage-1/`） |
| 2 Prompt eng | 4 个 | inline 3 + folder 1（`examples/stage-2/`） |
| **3 Tool use** | **6 个** | folder 6（`examples/stage-3/`） |
| 4 Frameworks | 5 个 | 全 folder（`examples/stage-4/`） |
| 5 Claude Code 生态 | 11 个 | inline 6 + folder 5（`examples/stage-5/`） |
| 6 Memory/RAG | 5 个 | 全 folder（`examples/stage-6/`） |
| 7 Multi-agent | 5 个 | inline 1 + folder 4（`examples/stage-7/`） |
| Track A1-A3 | 12 个 | 12 个 inline 练习；没有独立的 `examples/track-a/` 文件夹 |

→ T1 完成范围：**只有 Stage 3 全部 6 个**（剩余 stage 按 plan 分批推进）。

## 贡献 / 报错

跑不过、结果跟预期输出对不上、或想补一个新练习：

- 开 issue 标 `examples` label
- 或直接 PR、follow 本资料夹“设计原则”表格的规则

## 为什么这样分（不直接全塞 stage 档）

1. **Stage 档保持 readable**：学习地图读者不一定要看 code、只想理解 concept；长 code block 干扰阅读流
2. **范例可独立演进**：API SDK 升版、model name 改、范例需要单独 commit、不污染学习地图 git log
3. **Reader 可以 clone 单一 example**：`svn export` 或 `git clone --filter=tree:0` 只抓一个资料夹
4. **未来 CI**：example 失败不应 block mdbook deploy；分开可让 CI 有条件性检查

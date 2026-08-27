> [繁體中文](./setup-guide.md) | **简体中文** | [English](./setup-guide.en.md)

# 🚀 从零开始 — 给没有开发背景的设置指南

> [← 回主路线 README](../README.zh-Hans.md)

> 预估时间：30-45 分钟。你会申请第一个 API key、装好 Python / uv，并跑出第一个 LLM hello world。
> 这份文档写给“想学 AI agent，但还没写过 code”的人。已经熟 Python / git / CLI 的开发者，可以直接跳 [Stage 1](../stages/01-llm-basics.zh-Hans.md)。

## 先选你的入门方式

按“想花多少时间 setup”由浅到深排序。**完全没接触过 LLM 直接从 1️⃣ 开始就好**。

### 1️⃣ 网页版（最简单，免费可试，零 setup）

打开浏览器就能用，**第一次接触 LLM 最推荐这条**。免费 tier 通常够你试一周。

| 服务 | 网址 | 备注 |
|---|---|---|
| **Claude** | https://claude.ai | Anthropic 官方。免费 tier 每天有限额，付费 $20/月 |
| **ChatGPT** | https://chatgpt.com | OpenAI 官方。免费可用 GPT-5.5 Instant（有用量限制），Plus $20/月解锁 Thinking/Pro |
| **Gemini** | https://gemini.google.com | Google 官方。免费 tier 宽松，整合 Google 服务 |
| **Le Chat** | https://chat.mistral.ai | Mistral（欧洲开源 LLM）。免费、隐私导向 |

### 2️⃣ 桌面 App（免费，跨应用整合更好）

跑在你电脑上的原生 app——比网页多了系统 shortcut、跟剪贴板 / 截图整合、可以拖拉文件。

| App | 下载 | 平台 |
|---|---|---|
| **Claude Desktop** | https://claude.ai/download | macOS / Windows |
| **ChatGPT Desktop** | https://openai.com/chatgpt/download | macOS / Windows |
| **Gemini** | 暂无原生 desktop app | （用网页版即可） |
| **LM Studio** | https://lmstudio.ai | macOS / Windows / Linux — 跑本地 LLM 的桌面 app，零成本但要 GPU/RAM |

### 3️⃣ IDE 内建 AI（在 code editor 里边写 code 边有 AI 助手）

跑在 IDE / code editor 里——你正常写 code，AI 在旁边 suggest、修改、回答问题。**已经有写 code 习惯、想把 IDE 升级成 AI-native 的人这条最顺**。

| 工具 | 下载 | 形态 |
|---|---|---|
| **Cursor** | https://cursor.com | 独立 IDE（VS Code fork） |
| **Windsurf** | https://codeium.com/windsurf | 独立 IDE（Codeium 出） |
| **Cline** | https://cline.bot | VS Code extension（agentic 风格） |
| **Continue** | https://continue.dev | VS Code / JetBrains extension（开源） |
| **Roo Code** | https://github.com/RooCodeInc/Roo-Code | VS Code extension（Cline fork）；⚠️ **repo 已封存 2026-05（read-only）** |
| **Zed** | https://zed.dev | 独立 editor，内建 AI assistant |
| **GitHub Copilot** | https://github.com/features/copilot | VS Code / JetBrains 等多 IDE extension |

→ 详细比较 → [`branches/for-developer.zh-Hans.md`](../branches/for-developer.zh-Hans.md)

### 4️⃣ CLI Agent（terminal，能读写文件、跑指令、操作 git）

装在 terminal 的 agent——你下一个 prompt（譬如“重构这个 module”），agent 自己读文件、改文件、跑指令、commit。**比 IDE 模式更自主、可以处理多步骤任务**，但 setup 稍复杂（需要先有 Node.js 或 Python，看下面 B / D）。

| CLI Agent | 安装 / 文档 | 主要 LLM |
|---|---|---|
| **Claude Code** | https://code.claude.com/docs/en/quickstart | Claude |
| **Codex CLI** | https://github.com/openai/codex | GPT 系列 |
| **Gemini CLI** | https://github.com/google-gemini/gemini-cli | Gemini |
| **OpenCode** | https://github.com/anomalyco/opencode | 任意（多 provider） |
| **goose** | https://block.github.io/goose | 任意 |
| **Aider** | https://aider.chat | 任意（git-native） |
| **Hermes Agent** | https://github.com/NousResearch/hermes-agent | 200+（model-neutral） |

→ 想看 CLI agent 身份与选择指南 → [`cli-agents-guide.zh-Hans.md`](cli-agents-guide.zh-Hans.md)
→ Claude Code 第一次装的详细步骤 → 本指南 D

> 💡 **IDE-based 跟 CLI agent 怎么选？** 边写 code 边要 AI 帮忙 → IDE；下单一 prompt 让 agent 自己跑完一整个任务 → CLI。两个可以并用。

### 5️⃣ API + 自己写 code（最进阶，能 batch、集成任何工具）

想自己写 Python script、跑 batch job、把 LLM 接到自己的 app／automation？接下来的 A-C 就是给你的。

> 💡 **API key 是什么**：简单讲就是“让程序调用模型的密码”。请把它当成信用卡资料一样保管。

---

## A — 申请第一个 API key（约 10 分钟）

### Anthropic Claude（推荐第一次）

1. 打开 https://console.anthropic.com/
2. 用 Google、GitHub 或 email 注册。
3. 进入账号后找到 **API Keys**，点 **Create Key**。
4. **立刻复制显示出的 key**。多数平台只会显示一次。
5. 先放在本机密码管理器，或短暂放在本机文本文件；下一节会移到 `.env`。

> ⚠️ **API key 三不规则**
> - **不贴**到 chat 窗口、群组、email 或截图。
> - **不上传**到 git；GitHub 可能扫到后自动撤销。
> - **不放**云端硬盘纯文本文件；同步到其他设备等于多一份风险。

### 其他 LLM 选项

#### 西方 cloud（美区友善、英文场景）

- **OpenAI**：https://platform.openai.com/api-keys
  ChatGPT Plus 和 API key 是两件事；订阅 Plus 仍要另外申请 API key。

- **Google AI Studio**：https://aistudio.google.com/
  适合先试 Gemini API，免费额度会依地区和账号状态不同。

- **NVIDIA NIM**：https://build.nvidia.com/
  **托管多个开源 model（Llama / Mistral / DeepSeek / Qwen / Gemma 等）、OpenAI-compatible API、新账号送 1000 credits**。适合“想试多个 open-source model 但没 GPU”的情境。`base_url=https://integrate.api.nvidia.com/v1`。

#### 中国 / 中文场景（地区友善、价格极便宜）

> 中国大陆用户连 Anthropic / OpenAI 有困难、或想试中文 native 模型，从这边开始。**这些 API 都 OpenAI-compatible**、改 `base_url` 跟 model name 就能跑同一份练习。

- **DeepSeek**：https://platform.deepseek.com/
  web 版 https://chat.deepseek.com 完全免费（含深度思考模式）。API 价格极便宜（**$0.14 input / $0.28 output per 1M token**、比 haiku 便宜约 7 倍）。Code / 推理都很强。
  `base_url=https://api.deepseek.com/v1`、`model=deepseek-v4-flash` 或 `deepseek-v4-pro`。

- **Moonshot Kimi**：https://platform.moonshot.cn/ (中国)、https://platform.moonshot.ai/ (海外)
  web 版 https://kimi.com 免费、**1M token context** 是卖点（很大文件 / 长对话）。API 约 $5-15/1M input、按 context size 阶梯计费。
  `base_url=https://api.moonshot.cn/v1` (中国) / `https://api.moonshot.ai/v1` (海外)、`model=kimi-k3` 等。

- **通义千问 Qwen（Alibaba）**：https://dashscope.console.aliyun.com/
  web 版 https://chat.qwen.ai 免费。API 走 Alibaba Cloud DashScope、有 **OpenAI-compatible endpoint**（[文档](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/)）。**同样的 Qwen 模型也能用 Ollama 在本机跑**（`ollama pull qwen2.5:3b`）——cloud 跟 local 两条路径都通。

- **智谱 GLM（ZhipuAI）**：https://open.bigmodel.cn/ (中国) / https://z.ai/ (海外)
  web 版 https://chatglm.cn 免费、有 GLM-4.5、GLM-4-Plus。API 有 free tier、学生申请可额外领 credit。

#### 本机（不付 API 费、完全 offline）

- **Ollama 本地模型**：不用 API key。走本地路线请看 [Cookbook Recipe 6](cookbook.zh-Hans.md#6-本地-llm--cli-agent-快速-walkthrough)。
  本 repo 的“Path A”默认就是 Ollama；所有 Stage 1-7 练习都能用 `gemma4:e4b`（Stage 1-2）或 `qwen2.5:3b`（Stage 3+）跑通、$0/run。

> 💡 **怎么挑第一个**：
> - 想学 agent / production、**美区帐号OK** → **Anthropic Claude**（curriculum canonical）
> - 想学 agent / production、**中国地区**或想试中文模型 → **DeepSeek**（最便宜 cloud option、OpenAI-compat、中文很强）
> - 想试多个 model 但没 GPU → **NVIDIA NIM**（送 1000 credit、托管 10+ open model）
> - 隐私敏感 / 完全免费 / 中国大陆无 cloud → **Ollama**（本机、curriculum 全套都能跑、$0）

---

## B — 装本机环境（约 10 分钟）

### 装 Python 3.10+

- **macOS**：打开 Terminal，输入 `brew install python@3.12`。如果还没有 Homebrew，先看 https://brew.sh。
- **Windows**：到 https://www.python.org/downloads/ 下载 installer，安装时一定要勾 **Add Python to PATH**。
- **Linux**：Ubuntu 用 `sudo apt install python3 python3-venv`，Fedora 用 `sudo dnf install python3`。
- **验证**：macOS / Linux 输入 `python3 --version`；Windows 输入 `py --version`。看到 `Python 3.10` 以上即可。

### 装 uv

uv 是 Python 包管理工具。你可以把它想成“帮你临时装好需要的包再执行”的工具。

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
irm https://astral.sh/uv/install.ps1 | iex
```

验证：

```bash
uv --version
```

### 建立第一个 `.env` 文件

在你要跑 script 的文件夹里，建立一个文件名叫 `.env` 的文件：

```bash
ANTHROPIC_API_KEY=sk-ant-...贴上你刚才复制的 key
```

`.env` 是专门放本机秘密信息的文件。程序会读它，但你不应该把它上传到 GitHub。

### 加上 `.gitignore`

同一个文件夹建立 `.gitignore`：

```gitignore
.env
__pycache__/
*.pyc
```

这样 git 就不会把 `.env` 收进版本记录。

---

## C — 跑第一个 `hello-claude.py`（约 5 分钟）

建立 `hello-claude.py`：

```python
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic() # 自动读取 ANTHROPIC_API_KEY

msg = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello, who are you?"}],
)

print(msg.content[0].text)
```

执行：

```bash
uv run --with anthropic --with python-dotenv python hello-claude.py
```

看到 Claude 回复自我介绍，就代表你的 API key、Python、包都通了。

### 常见错误

| 错误信息 | 常见原因 | 解法 |
|---|---|---|
| `401 Unauthorized` | API key 没读到或打错 | 回 A 重新复制，确认 `.env` 文件名和内容 |
| `429 Rate limit` | 太快发太多请求 | 等几秒或几分钟再跑 |
| `connection refused` | 网络或防火墙问题 | 确认网络、公司或学校防火墙 |
| `ModuleNotFoundError` | 包没有被安装 | 确认执行的是上面的 `uv run --with ...` 命令 |

---

## D — 第一次装 Claude Code（约 10 分钟；Stage 5 / for-developer 会用到）

### 先装 Node.js

> 💡 **Node.js 是什么**：跑 JavaScript 的 runtime（类似 Python interpreter 但是给 JS 用）。**`npm`** 是它附带的“包管理器”（package manager）——跟 Python 的 `pip` 同角色、用来安装别人写好的工具（如下面的 Claude Code）。`npm install -g X` 表示“全局安装 X，之后在任何文件夹都能用”。

- **macOS / Linux**：`brew install node`，或从 https://nodejs.org 下载。
- **Windows**：从 https://nodejs.org 下载安装包。
- **验证**：输入 `node --version`，看到 v18 以上即可。

### 装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### 第一次认证

```bash
claude
```

第一次启动时通常会让你选：

- **Claude subscription**：用 Claude.ai 账号登录，对初学者最省事。
- **API key**：贴上 A 申请到的 key。

### 建立第一份 `CLAUDE.md`

在你的 project 根目录建立 `CLAUDE.md`。Claude Code 启动时会读它，理解你希望它怎么协助。

```markdown
# 你是谁
我是 [你的名字]，[你的领域，例如：教师 / 研究者 / 写作者]。

# Code style
- 注释用简体中文写，code 用英文
- 写 function 时优先加 type hint
- 不要主动 commit；改完让我手动 git add

# 不准做的事
- 不要联网查资料，除非我明确说可以
- 不要动 `.env` 或 `.gitignore`
- 不要删文件夹，包括子文件夹
```

---

## E — 第一个 Skill 示例（约 5 分钟；Stage 5.3 会用到）

Skill 是 Claude Code 的“可复用 prompt 包”。当你的消息符合描述，Claude Code 会自动加载那份指示。

建立 `.claude/skills/hello-skill/SKILL.md`：

```markdown
---
name: hello-skill
description: 第一个 hello skill。当用户说“请打招呼”或“say hi”时触发。
---

当用户请你打招呼时，回三件事：

1. 用简体中文和英文各说一次 hello
2. 提现在的日期（用 system 时间）
3. 给一个今日小提醒（随机选健康 / 学习 / 心情建议）
```

跑 `claude`，输入“请打招呼”。如果 Claude 回复三件事，就代表 Skill 被加载了。

> 想看更完整的 Skill 设计：看 [Stage 5.3 — Skills](../stages/05-claude-code-ecosystem.zh-Hans.md#53--skillsclaude-code-的行为层-claude-code-生态最关键的一层)。
> 想看可以照做的示例：看 [Cookbook](cookbook.zh-Hans.md)。

---

## 接下来去哪

| 你现在的状态 | 下一步 |
|---|---|
| 想正式理解 LLM、API、token | [Stage 1 — LLM 基础](../stages/01-llm-basics.zh-Hans.md) |
| 想直接挑身份分支 | [日常用户](../branches/for-everyday-users.zh-Hans.md) / [教师](../branches/for-teacher.zh-Hans.md) / [知识工作者](../branches/for-knowledge-worker.zh-Hans.md) / [研究者](../branches/for-researcher.zh-Hans.md) / [开发者](../branches/for-developer.zh-Hans.md) |
| 想看 Claude Code 完整生态 | [Stage 5 — Claude Code 生态](../stages/05-claude-code-ecosystem.zh-Hans.md) |
| 想本地 LLM、不用云端 key | [Cookbook Recipe 6](cookbook.zh-Hans.md#6-本地-llm--cli-agent-快速-walkthrough) |
| 想比较 CLI agent | [CLI Agents 比较指南](cli-agents-guide.zh-Hans.md) |
| 不懂某个用词 | [Glossary](glossary.zh-Hans.md) |

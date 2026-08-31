> [繁體中文](./setup-guide.md) | **简体中文** | [English](./setup-guide.en.md)

# 🚀 从零开始 — 给没有开发背景的设置指南

> [← 返回主路线 README](../README.zh-Hans.md)

<!-- freshness: canonical=resources/setup-guide.md; verified_on=2026-08-30; scope=install-paths,api-keys,authentication,provider-entrypoints,project-status; max_age_days=90 -->

这一页不是要你把所有工具都装一遍。你只要先选一扇门，完成一个小结果。

已经会用 Python、Git 和 terminal，也知道怎么保护 **API Key（API 密钥）**？可以直接去 [Stage 1](../stages/01-llm-basics.zh-Hans.md)。

## 📌 这份指南会带你完成什么

- 分清 Web Chat、Desktop、IDE、**CLI Agent（命令行代理）** 和 **API（应用程序接口）**，不再把它们当成同一种工具。
- 知道 **API Key（API 密钥）** 为什么像密码，以及不能放在哪里。
- 用 `uv` 准备 Python 3.12，不必先学一大堆包管理知识。
- 复制一份 Python 程序，真的收到模型回复。
- 知道什么时候该去 Stage 1，什么时候该去 Stage 5。

<details markdown="1">
<summary>查看时间、设备与先决条件</summary>

- 只用 Web Chat：几分钟即可开始。
- 完成 API quick start：通常需要约 20–40 分钟；账号审核、付款设置和网络状况可能让时间变长。
- 需要：可以安装软件的 Windows、macOS 或 Linux 电脑，以及能打开供应商 Console 的账号。
- 不需要：先会写程序、先懂 Git branch、先装完整 IDE。

公司或学校电脑可能禁止安装程序或创建 API key。遇到这种情况，先问管理员，不要绕过限制。

</details>

## 🚪 先选一扇门

五扇门是并行选择，不是五个一定要依次完成的等级。

| 你想做什么 | 这扇门是什么 | 第一个动作 |
|---|---|---|
| 先和模型聊天 | **Web Chat**：在浏览器里对话 | 打开 [Claude](https://claude.ai)、[ChatGPT](https://chatgpt.com)、[Gemini](https://gemini.google.com) 或 [Le Chat](https://chat.mistral.ai) |
| 在电脑 App 里聊天或处理文件 | **Desktop App**：装在电脑上的聊天界面 | 从产品的官方下载页安装 |
| 写 code 时让 AI 在旁边协助 | **IDE Assistant**：住在 editor 里 | 先看[开发者路线](../branches/for-developer.zh-Hans.md) |
| 让 Agent 在指定文件夹读文件、改文件、跑命令 | **CLI Agent**：在 terminal 里工作 | 先看 [CLI Agents 指南](cli-agents-guide.zh-Hans.md) |
| 自己写程序调用模型 | **API**：程序和模型服务对话的入口 | 继续做下面 A → B → C |

<details markdown="1">
<summary>查看 Web、Desktop、IDE 与 CLI 的完整官方入口</summary>

下表是入口清单，不是排名。推荐度表示“这份学习地图是否适合把它作为起点”。

<table>
<thead><tr><th scope="col">类型</th><th scope="col">官方入口／项目</th><th scope="col">先知道什么</th><th scope="col">推荐度</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Web Chat</th><td><a href="https://claude.ai">Claude</a></td><td>云端聊天界面；方案和功能依账号、地区而异</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://chatgpt.com">ChatGPT</a></td><td>云端聊天界面；ChatGPT 订阅不等于 OpenAI API 额度</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://gemini.google.com">Gemini</a></td><td>云端聊天界面；连接服务前先看数据权限</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://chat.mistral.ai">Le Chat</a></td><td>Mistral 的云端聊天界面</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Desktop</th><td><a href="https://claude.com/download">Claude Desktop</a></td><td>Windows、macOS 与 Linux 的当前入口以官方页面为准</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://chatgpt.com/download">ChatGPT Desktop</a></td><td>平台要求以官方下载页为准</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://gemini.google/mac">Gemini for macOS</a></td><td>目前是 macOS App；其他系统可使用 Web</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://lmstudio.ai/download">LM Studio</a></td><td>本地模型 runtime 和图形界面；仍要管理模型、硬件和文件权限</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">IDE／Editor</th><td><a href="https://cursor.com">Cursor</a></td><td>AI editor；确认每次修改和 terminal 操作</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://windsurf.com/editor">Windsurf</a></td><td>AI editor；方案和权限以官方文档为准</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://cline.bot">Cline</a></td><td>VS Code coding agent；从低权限开始</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://zed.dev/ai">Zed AI</a></td><td>Zed editor 的 AI 功能</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/features/copilot">GitHub Copilot</a></td><td>可在 GitHub、IDE 和其他界面使用；各界面的权限不同</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="7">CLI Agent</th><td><a href="https://code.claude.com/docs/en/quickstart">Claude Code</a></td><td>先保留 permission prompt；从小文件夹开始</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/openai/codex">OpenAI Codex</a></td><td>coding agent；确认 sandbox、approval 和 diff</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/google-gemini/gemini-cli">Gemini CLI</a></td><td>Gemini 的开源 terminal agent</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/anomalyco/opencode">OpenCode</a></td><td>多 Provider coding agent／harness，不是模型 Router</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/aaif-goose/goose">goose</a></td><td>可连接 Provider 和 extensions；先缩小工具权限</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://aider.chat/docs/">Aider</a></td><td>Git-first pair programmer；auto-commit 不代表可以跳过 review</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/NousResearch/hermes-agent">Hermes Agent</a></td><td>通用 agent；先在隔离环境试小任务</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
</table>

</details>

## 🧩 先分清七个核心词

- **Chat Surface（聊天界面）**：你打字、贴文件、看回复的画面，例如 Claude.ai。它不是模型 API。
- **API（应用程序接口）**：程序发送请求、拿回结果的入口。人通常不直接在 API 画面聊天。
- **API Key（API 密钥）**：让服务知道“这个程序可以使用哪个账号”的秘密字符串。拿到它的人可能花掉你的额度。
- **Environment Variable（环境变量）**：把设置交给程序读取的小抽屉。程序可以读它，不必把秘密写进 source code。
- **Runtime（运行环境）**：真正把程序跑起来的东西；Python 是一种 runtime，Ollama 是本地模型 runtime。
- **Package Manager（包管理器）**：帮你安装和运行别人写好的包。这份指南使用 `uv`。
- **CLI Agent（命令行代理）**：在 terminal 里读文件、改文件、执行工具的 Agent。它不是 API Provider，也不是单一模型。

## 📚 必读与官方起点

这五个入口直接保持可见；遇到版本差异时，以官方页面为准。

<table>
<thead><tr><th scope="col">类别</th><th scope="col">官方资源</th><th scope="col">用它解决什么</th><th scope="col">推荐度</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Claude API</th><td><a href="https://platform.claude.com/docs/en/get-started">Claude API Quickstart</a></td><td>创建 key、发送第一个请求</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://platform.claude.com/docs/en/api/sdks/python">Anthropic Python SDK</a></td><td>确认 Python 要求、环境变量与当前程序形态</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">Python 工具</th><td><a href="https://docs.astral.sh/uv/getting-started/installation/">uv Installation</a></td><td>按操作系统安装或更新 uv</td><td>⭐⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">CLI 入门</th><td><a href="https://code.claude.com/docs/en/terminal-guide">Claude Code Terminal Guide</a></td><td>第一次打开 terminal、切换文件夹和执行命令</td><td>⭐⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">秘密安全</th><td><a href="https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning">GitHub Secret Scanning</a></td><td>了解为什么 secret 不能进入 Git 历史</td><td>⭐⭐⭐⭐</td></tr></tbody>
</table>

<a id="a--申请第一个-api-key约-10-分钟"></a>

## 🛠 A — 拿到第一把 API Key

这条 quick start 使用 Anthropic Claude，因为 Stage 1 的 canonical API 路径也使用它。Claude.ai 订阅和 Claude API 账单是两回事。

1. 打开 [Claude Console](https://platform.claude.com/)。
2. 进入 **API Keys**，创建一把只给这个练习使用的 key。
3. 如果页面可以选择 owner、workspace 或期限，使用最小范围与最短合理期限。
4. 复制 key，先放进密码管理器；不要贴到聊天窗口。
5. 先在 Console 查看 billing／usage；如果账号提供 spend limit 或提醒，把它设在你能接受的小额范围，再开始调用 API。

**API Key 三不规则：**

- **不粘贴**到 chat、群组、email、issue 或截图。
- **不写入** Python source code，也不进 Git 历史。
- **不共享**同一把 key 给很多项目；不用时撤销。

<details markdown="1">
<summary>查看其他 Cloud API 与本地 Runtime</summary>

下表只写当前官方入口。价格、免费额度和可用模型请点击官方页面查看，这份入门指南不冻结这些信息。

<table>
<thead><tr><th scope="col">类型</th><th scope="col">官方入口</th><th scope="col">Compatibility／限制</th><th scope="col">推荐度</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="7">Cloud API</th><td><a href="https://platform.openai.com/docs/quickstart">OpenAI API</a></td><td>官方 SDK 与 API；ChatGPT 订阅不等于 API billing</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://ai.google.dev/gemini-api/docs/openai">Gemini API</a></td><td>Google 官方提供 OpenAI libraries compatibility 说明</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://docs.api.nvidia.com/nim/re/reference/llm-apis">NVIDIA NIM</a></td><td>按 endpoint 查看支持的 API shape 与模型</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://api-docs.deepseek.com/">DeepSeek API</a></td><td>官方文档提供 OpenAI-compatible 使用方式</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://platform.kimi.com/docs/api/overview">Kimi API</a></td><td>地区、endpoint 与模型以官方 Console 为准</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://help.aliyun.com/en/model-studio/base-url">Alibaba Model Studio／Qwen</a></td><td>按区域使用对应 base URL；官方提供 OpenAI-compatible endpoint</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://docs.z.ai/api-reference/introduction">Z.ai／GLM API</a></td><td>按官方 reference 使用当前 endpoint</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">本地 Runtime</th><td><a href="https://docs.ollama.com/api/openai-compatibility">Ollama</a></td><td>只兼容 OpenAI API 的一部分；需要另外下载本地模型</td><td>⭐⭐⭐⭐⭐</td></tr></tbody>
</table>

本地推理没有供应商模型 API 账单，但硬件、电力、下载时间、设备安全、文件和 log 仍由你负责。完整路径请看 [Cookbook 的本地 LLM walkthrough](cookbook.zh-Hans.md#6-本地-llm--cli-agent-快速-walkthrough)。

这个 repo 当前的练习标签是：Stage 1–2 用 `gemma4:e4b`，Stage 3–6 的 Tool Use／ReAct 用 `qwen2.5:3b`，Stage 7 的 Eval／Observability／Streaming／Deploy 用 `qwen3.5:4b`。这是教材默认值，不是通用模型排名。

</details>

<a id="b--装本机环境约-10-分钟"></a>

## 🛠 B — 装好 Python 运行环境

这里用 `uv` 同时管理 Python 和包。先安装 `uv`：

macOS、Linux 或 WSL：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

关闭并重新打开 terminal，再依次复制：

```bash
uv --version
uv python install 3.12
uv run --python 3.12 python --version
```

最后一行看到 `Python 3.12`，就完成 B。`uv` 也支持其他 Python 版本；这份教程固定 3.12，减少初学时的包兼容问题。

<details markdown="1">
<summary>安装失败时，查看各操作系统替代方式</summary>

- Windows 可以使用 `winget install --id=astral-sh.uv -e`。
- macOS 可以使用 `brew install uv`。
- 也可以从 [uv 官方安装页](https://docs.astral.sh/uv/getting-started/installation/) 下载 release binary。
- 如果公司封锁安装 script，停止并请管理员提供批准方式，不要关闭安全软件硬闯。

已经有 Python 3.10–3.14 也没关系，`uv` 会寻找可用的 Python；上面的命令只是替这份教程准备一致的 3.12。

</details>

<a id="c--跑第一个-hello-claudepy约-5-分钟"></a>

## 🛠 C — 跑第一个 `hello-claude.py`

### 1. 建立练习文件夹

PowerShell、macOS 和 Linux terminal 都可以使用：

```bash
mkdir my-first-llm
cd my-first-llm
```

### 2. 先建立 `.gitignore`

建立名为 `.gitignore` 的文件，贴上：

```gitignore
.env
__pycache__/
*.pyc
```

先排除 `.env`，再建立 secret 文件，可以降低误加进 Git 的机会。

### 3. 再建立 `.env`

建立名为 `.env` 的文件。把 placeholder 换成你自己的 key；不要把真 key 贴到这份文档或 commit：

```dotenv
ANTHROPIC_API_KEY=PASTE_YOUR_KEY_HERE
```

### 4. 复制 Python 程序

建立 `hello-claude.py`：

```python
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()  # 从 ANTHROPIC_API_KEY 读取 key

message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=120,
    messages=[{"role": "user", "content": "请用一句话介绍你自己。"}],
)

for block in message.content:
    if block.type == "text":
        print(block.text)
```

### 5. 直接执行

```bash
uv run --python 3.12 --with anthropic --with python-dotenv python hello-claude.py
```

看到模型打印一句介绍，就代表 Python、包、API key 和网络都接通了。

<details markdown="1">
<summary>查看常见错误与安全恢复</summary>

| 你看到什么 | 通常代表什么 | 先做什么 |
|---|---|---|
| `401`／`authentication_error` | key 没读到、失效或贴错 | 撤销有疑虑的 key；确认文件名是 `.env`，再创建新 key |
| `429`／`rate_limit_error` | 用量、速率或账号额度限制 | 停止重试，回 Console 看 usage／billing，再按错误信息等待 |
| `ModuleNotFoundError` | 没用到这次 `uv run --with ...` 的环境 | 完整复制执行命令，不要只跑 `python hello-claude.py` |
| `uv` 找不到 | 安装后的 terminal 还没读到新 PATH | 关闭并重新打开 terminal；再看 uv 官方安装页 |
| 连接错误 | 网络、proxy、防火墙或服务状态 | 先看供应商 status page；公司／学校网络请问管理员 |

如果 key 曾出现在 Git、聊天、截图或公开 log，不能只把文字删掉；请立刻在 Console 撤销它并创建新 key。

</details>

<a id="d--第一次装-claude-code约-10-分钟stage-5--for-developer-会用到"></a>

## 🛠 D — 第一次打开 Claude Code

这是 Stage 5 的入口，不是完成 API quick start 的必修。Claude Code 现在优先使用 native installer，不必先安装 Node.js。

macOS、Linux 或 WSL：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell：

```powershell
irm https://claude.ai/install.ps1 | iex
```

安装后先运行 `claude --version`，再到一个小型练习文件夹运行 `claude`。完整条件和其他安装方式请看 [Claude Code Installation](https://code.claude.com/docs/en/installation)。

<details markdown="1">
<summary>查看登录、系统要求与第一份 CLAUDE.md</summary>

Claude Code 目前需要符合官方列出的 Claude plan、Console account 或支持的 cloud provider；免费的 Claude.ai plan 不包含 Claude Code。运行 `claude` 后按浏览器提示登录，详细身份差异请看 [Authentication](https://code.claude.com/docs/en/authentication)。

官方当前基本要求包括受支持的 Windows、macOS 或 Linux、至少 4 GB RAM、网络连接和可用 shell。Windows 可以原生使用 PowerShell；需要 Linux toolchain 或 sandbox 时再考虑 WSL 2。

你可以在 project root 建立 `CLAUDE.md`：

```markdown
# 这个 project 要做什么
这是一个学习用的小项目。

# 工作规则
- 先说明要改哪些文件，再开始修改。
- 不要读取或改写 `.env`。
- 不要自动 commit；完成后让我先看 diff。
- 删除文件、安装包或联网前先问我。

# 完成条件
- 执行最小相关测试。
- 说明改了什么、测试了什么、还有什么风险。
```

`CLAUDE.md` 是 project instructions，不是安全 sandbox。工具权限、approval、版本控制和人工 review 仍要保留。

</details>

<a id="e--第一个-skill-示例约-5-分钟stage-53-会用到"></a>

## 🛠 E — 建立第一个 Skill

这是 Stage 5.3 的延伸。**Skill（技能包）** 是有名称、描述和操作指示的可复用文件夹；它不会自动变成安全权限。

第一个动作：建立 `.claude/skills/hello-skill/SKILL.md`。

<details markdown="1">
<summary>查看可以直接复制的 SKILL.md</summary>

```markdown
---
name: hello-skill
description: 当使用者明确请你打招呼时，用两种语言回复。
---

当使用者请你打招呼时：

1. 用繁体中文说一次 hello。
2. 用英文说一次 hello。
3. 不读文件、不联网、不执行其他工具。
```

在该 project 打开 `claude`，输入“请打招呼”。看到两种语言，而且没有多做其他动作，就完成了。

更完整的责任边界请看 [Stage 5.3 — Skills](../stages/05-claude-code-ecosystem.zh-Hans.md#53--skills按需操作卡)，更多示例请看 [Cookbook](cookbook.zh-Hans.md)。

</details>

## ✅ 完成检查

做到下面任一条，就可以离开这份指南，不必把所有入口都装完：

- 我已经能在 Web Chat 完成一次对话，而且知道它不是 API。
- 我完成 A → B → C，看到 `hello-claude.py` 打印模型回复。
- 我选择 CLI 路径，能说出 CLI Agent 的工作文件夹与权限范围。

还要确认：

- 真正的 API key 没有出现在 source code、Git、聊天、截图或 log 中。
- 我知道如何撤销 key，也知道 API billing 和聊天订阅分开。
- 我没有因为工具能自动执行，就跳过 diff、测试或人工确认。

## 接下来去哪

| 你现在想做什么 | 下一站 |
|---|---|
| 理解模型、Token、Context Window 与 API | [Stage 1 — LLM 基础](../stages/01-llm-basics.zh-Hans.md) |
| 直接学 Prompt | [Stage 2 — Prompt Engineering](../stages/02-prompt-engineering.zh-Hans.md) |
| 使用 CLI Agent 工作 | [Track A1 — CLI 入门](../tracks/cli/A1-cli-intro.zh-Hans.md) |
| 理解 Claude Code、MCP、Skills、Plugins 与 Subagents | [Stage 5 — Claude Code 生态](../stages/05-claude-code-ecosystem.zh-Hans.md) |
| 使用本地模型 | [Cookbook：本地 LLM walkthrough](cookbook.zh-Hans.md#6-本地-llm--cli-agent-快速-walkthrough) |
| 还分不清 OpenRouter、Ollama、OpenCode 或 Pi | [Glossary：先分清五种工具身份](glossary.zh-Hans.md#-先分清五种工具身份) |

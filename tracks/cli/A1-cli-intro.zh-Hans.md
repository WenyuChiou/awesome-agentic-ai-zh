# A1 — 选一个 CLI agent，安全地完成第一个小任务

> [繁體中文](./A1-cli-intro.md) | **简体中文** | [English](./A1-cli-intro.en.md)

> [← 回主线路 README](../../README.zh-Hans.md) · **Track A: CLI Power User** 第 1 站 · [下一站：A2](A2-cli-workflow.zh-Hans.md)

这一站会把“终端里的 AI”讲清楚，然后让你在一个可丢弃的 demo repo（由 Git 管理的练习项目文件夹）里安全地跑一次。你会先让工具读文件、找测试指令、提出计划；确认计划后，它才会做一个可以用 `git diff` 看到、也能撤销的小改动。

如果你想用现成工具做事，暂时不想自己写 agent 程序，这一站就是你的入口。

## 你现在只要做这件事

准备一个不含秘密、可以随时删除的 demo repo。还没安装工具时，先在下面的短表选一个，点官方入口完成安装和登录；接着直接复制这段请求：

```text
请只读取当前的 demo repo，说明它的用途，找出测试指令，并提出一个小型文档改动计划。先不要修改文件、不要删除文件，也不要执行会改变数据的命令。
```

完成后，你应该能看到 repo 摘要、测试指令、待确认的计划，以及工具请求权限时的提示。这就是本章的第一个可验证成果。

## 📌 学习目标

- 分清 **LLM**、**Provider API**、**Router**、**Coding agent** 和 **Local runtime**。
- 根据你已有的账号、provider 或本机环境选择入口，不做总排名。
- 在 demo repo 中完成一次“先读取 → 看计划 → 确认 → 小改动 → `git diff` → 撤销”的循环。

<details markdown="1">
<summary>展开时间、先备条件、账号和费用</summary>

- **时间**：第一次只读取并查看计划，通常一个短时段就能完成；CLI-1 到 CLI-4 可以分几天慢慢做，不必一次做完。
- **先备条件**：会进入文件夹、查看 `git status` 和 `git diff`；手边有一个可丢弃的 demo repo。
- **账号**：准备一个所选工具支持的登录方式，或把 agent 接到本机模型 runtime。没有账号时，先看下面的选择表和官方 Quickstart。
- **费用**：不要猜。开始前查看当天的官方 pricing / usage 页面；只有整条流程都留在本机时，才不会产生这次练习的模型 API 费用。
</details>

## 🧩 先认识五个核心词

| 核心词 | 它是什么、像什么 | A1 怎么用 | 不是什么 |
|---|---|---|---|
| **LLM（大型语言模型）** | 生成文字或代码的模型，像工作台里负责想答案的大脑 | Claude、GPT、Gemini 都是模型家族 | 不会自己管理 repo、文件权限或账单 |
| **Provider API（模型服务入口）** | 让工具向一家模型服务发送请求的门 | Anthropic API、OpenAI API、Gemini API 会处理认证和计费 | 不是会改文件的 coding agent |
| **Router（路由器）** | 把同一个请求转给不同 provider 的中转站 | [OpenRouter](https://openrouter.ai/docs/faq) 可集中 API、routing 和 usage | 不是 LLM，也不管理你的文件权限 |
| **Coding agent（编程工作台）** | 能在终端里读文件、改文件和执行命令的工作台 | Claude Code、Codex、OpenCode、Pi 都属于这一类 | 里面使用的模型、provider 和 sandbox 要另外确认 |
| **Local runtime（本地模型引擎）** | 在自己的电脑上运行模型的引擎，像启动模型的马达 | [Ollama](https://github.com/ollama/ollama) 可以让支持它的 agent 调用本地模型 | 不是 coding agent，不会自己读取 repo |

## 根据已有条件选择入口

<table>
<thead>
<tr><th scope="col">你已有的条件</th><th scope="col">可以先看的入口</th><th scope="col">先确认什么</th></tr>
</thead>
<tbody>
<tr><th scope="row">Anthropic 账号或 API</th><td><a href="https://code.claude.com/docs/en/quickstart">Claude Code</a></td><td>登录和 permission prompt</td></tr>
<tr><th scope="row">ChatGPT 或 OpenAI API</th><td><a href="https://learn.chatgpt.com/docs/codex/cli">Codex CLI</a></td><td>approval、sandbox、工作目录</td></tr>
<tr><th scope="row">Google 账号、API 或 Vertex AI</th><td><a href="https://google-gemini.github.io/gemini-cli/">Gemini CLI</a></td><td>认证和 sandbox</td></tr>
<tr><th scope="row">想换 provider 或使用本地模型</th><td><a href="https://opencode.ai/docs/">OpenCode</a>、<a href="https://block.github.io/goose/">goose</a>、<a href="https://aider.chat/docs/">Aider</a>、<a href="https://pi.dev/docs/latest">Pi</a></td><td>provider 和权限边界</td></tr>
<tr><th scope="row">想用 Router 或本机 runtime</th><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a> 或 <a href="https://ollama.com/">Ollama</a></td><td>它们需要搭配 coding agent</td></tr>
</tbody>
</table>

## 📚 必读

- [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart) 和 [permissions](https://code.claude.com/docs/en/permissions)
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [Gemini CLI authentication](https://google-gemini.github.io/gemini-cli/docs/get-started/authentication.html) 和 [sandbox 设置](https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html)
- [OpenCode 文档](https://opencode.ai/docs/) 和 [goose 文档](https://block.github.io/goose/)
- [Aider 文档](https://aider.chat/docs/)、[Hermes Agent 文档](https://hermes-agent.nousresearch.com/docs/)、[Grok Build repo](https://github.com/xai-org/grok-build)、[Pi 文档](https://pi.dev/docs/latest)
- [OpenRouter FAQ](https://openrouter.ai/docs/faq) 和 [Ollama](https://ollama.com/)

每次 cloud 请求的单次费用和本章总费用，都会因账号、provider、模型、输入输出 token 和订阅额度而变化；练习前查看当天的官方价格或 usage 页面。只有 agent 和 provider 都设置为只连接本机 Ollama，且没有另外调用云端服务时，这次练习才不会产生模型 API 费用；文件和命令权限仍要照常检查。
## 🛠 动手练习

<a id="cli-1"></a>
### 动手练习 CLI-1：在 demo repo 里先读取，再做一个可撤销的小改动

**成果：** 你能看到 repo 说明、测试指令和待确认的计划；确认后留下一个可以用 `git diff` 检查的小改动。

<details markdown="1">
<summary>展开 CLI-1 的准备、操作和撤销步骤</summary>

1. 创建或复制一个可丢弃的 demo repo。只放 README、少量源代码和测试；不要放 API key、个人数据、合同或 production 设置。开始前先运行 `git status --short`，确认没有别人的未完成改动。
2. 先使用上面的“只读取”请求。对照工具列出的文件、测试指令和计划；不清楚的地方先问，不要直接批准。
3. 你确认计划后，只允许一个小文档改动，例如在 `README.md` 增加一段“如何运行测试”。要求工具先展示 diff，再由你批准。
4. 在终端运行 `git diff -- README.md`，确认只有预期内容。只有第 1 步已确认文件原本干净时，才运行 `git restore -- README.md`；最后再用 `git status --short` 确认小改动已经撤销。

如果工具没有 git，仍要保留原文件备份并逐行比较；不要把同一个 demo repo 同时交给两个会写文件的 agent。
</details>

<a id="cli-2"></a>
### 动手练习 CLI-2：让项目规则被正确读取

**成果：** 你能用一个短规则文件说明项目用途、禁止事项、测试指令和交付格式，并验证工具确实遵守了它。

<details markdown="1">
<summary>展开各 CLI 的项目规则位置和验证方式</summary>

- Claude Code 读取项目的 `CLAUDE.md`；Codex 使用 `AGENTS.md`。
- OpenCode 以 `AGENTS.md` 优先；没有 `AGENTS.md` 时，`CLAUDE.md` 是兼容 fallback。不要把 `OPENCODE.md` 当成通用规则文件。
- Gemini CLI 常用 `GEMINI.md`；goose、Aider、Hermes Agent、Pi 和 Grok Build 的文件名及加载范围以各自官方文档为准。
- 规则只保留会改变行为的内容：项目用途、不能做的事、测试指令和交付格式。不要把长篇 API 参考资料塞进每次都会加载的规则文件。

在 demo repo 里加入一条可观察的规则，例如“先提出计划，不修改 `data/`”，再提出一个会触发它的请求。最后检查 agent 的回复和 `git diff`。
</details>

<a id="cli-3"></a>
### 动手练习 CLI-3：用第二个 harness 重跑同一个请求

**成果：** 你能记录两个工具在模型 / provider、权限提示、sandbox 和输出格式上的差异，而不是用主观分数选赢家。

<details markdown="1">
<summary>展开第二个 CLI 的公平比较步骤</summary>

在同一个干净的 demo repo、同一份 prompt、同一组文件上各运行一次。记录日期、CLI 版本、LLM、provider、登录方式、approval / sandbox 设置、是否真的改了文件，以及 `git diff` 结果。不要同时启动两个会写文件的 session；每次完成后撤销，再开始下一次。
</details>

<a id="cli-4"></a>
### 动手练习 CLI-4：用假凭证观察认证失败

**成果：** 你能区分“登录失败”“provider API key 失败”“模型名称不存在”和“权限 / sandbox 阻挡”，而且不会把真正的秘密贴进 prompt 或 log。

<details markdown="1">
<summary>展开安全的认证错误实验</summary>

在一次性终端 session 中使用明确标为假的值，例如 `not-a-real-key`；不要改动正式的 shell 设置或共享 `.env`。先观察未登录错误，再在已登录的 CLI 中输入一个官方不存在的模型名称，记下错误类型和补救指引。测试完立刻清除假值，并确认 shell history、工作目录和 log 里没有真 key。

使用有效凭证的请求可能产生费用；第一次练习可以使用本机 Ollama 或 provider 明确提供的免费额度，并以当天官方价格和实际 usage 为准。
</details>

## 🎯 精选 Projects

A1 只教你安全开始，不在两个页面重复维护同一份易变数据。9 个工具的登录、provider、sandbox 和官方来源集中放在 [`CLI Agents 参考指南`](../../resources/cli-agents-guide.zh-Hans.md)。官方资料查核日：**2026-08-30 UTC**。

推荐度是本学习地图的编辑建议，不是 GitHub stars 或总排名。`⭐⭐⭐⭐⭐` 表示：如果你选择这条工具路径，这一行应先看；不是让你安装所有五星工具。

<table>
<thead>
<tr><th scope="col">分类</th><th scope="col">Project</th><th scope="col">推荐度</th><th scope="col">适合谁</th><th scope="col">先注意什么</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">官方模型生态</th><td><a href="https://github.com/anthropics/claude-code">anthropics/claude-code</a></td><td>⭐⭐⭐⭐⭐</td><td>使用 Anthropic 生态的人</td><td>保留 permission prompt，先用 demo repo</td></tr>
<tr><td><a href="https://github.com/openai/codex">openai/codex</a></td><td>⭐⭐⭐⭐⭐</td><td>已有 ChatGPT 或 OpenAI API 的人</td><td>确认 approval、sandbox 和工作目录</td></tr>
<tr><td><a href="https://github.com/google-gemini/gemini-cli">google-gemini/gemini-cli</a></td><td>⭐⭐⭐⭐</td><td>已有 Google 认证或 Vertex AI 的人</td><td>先确认认证方式和 sandbox</td></tr>
<tr><td><a href="https://github.com/xai-org/grok-build">xai-org/grok-build</a></td><td>⭐⭐⭐</td><td>已在使用 xAI 生态、想比较新工具的人</td><td>先在 demo repo 观察，不作第一个 production 工具</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">可换 provider</th><td><a href="https://github.com/anomalyco/opencode">anomalyco/opencode</a></td><td>⭐⭐⭐⭐⭐</td><td>想切换 provider 或接兼容 endpoint 的人</td><td><code>AGENTS.md</code> 优先；另查 permission 设置</td></tr>
<tr><td><a href="https://github.com/aaif-goose/goose">aaif-goose/goose</a></td><td>⭐⭐⭐⭐</td><td>想同时使用 CLI、desktop 和 extensions 的人</td><td>先只开低权限 extension</td></tr>
<tr><td><a href="https://github.com/Aider-AI/aider">Aider-AI/aider</a></td><td>⭐⭐⭐⭐⭐</td><td>重视 git diff 和 commit 流程的人</td><td>先理解它的 git auto-commit 行为</td></tr>
<tr><td><a href="https://github.com/earendil-works/pi">earendil-works/pi</a></td><td>⭐⭐⭐⭐</td><td>想从小核心加 extensions、skills 或 RPC 的人</td><td>没有内建 sandbox；需要隔离时用容器或 VM</td></tr>
<tr><td><a href="https://github.com/NousResearch/hermes-agent">NousResearch/hermes-agent</a></td><td>⭐⭐⭐⭐⭐</td><td>想在 terminal、desktop 或聊天平台使用同一 agent 的人</td><td>逐项开启 provider、Skill 和 MCP 权限</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Router／本地引擎</th><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a></td><td>⭐⭐⭐⭐</td><td>想用一个 API 入口切换 provider 的人</td><td>它是 Router，仍要搭配 agent</td></tr>
<tr><td><a href="https://github.com/ollama/ollama">ollama/ollama</a></td><td>⭐⭐⭐⭐⭐</td><td>想在自己电脑上运行模型的人</td><td>它是 local runtime，仍要搭配 agent</td></tr>
</tbody>
</table>
<details markdown="1">
<summary>展开“工具、Router、local runtime”的最短辨识法</summary>

- Claude Code、Codex、Gemini CLI、OpenCode、goose、Aider、Hermes Agent、Grok Build、Pi：会接收任务并操作工作目录的 CLI agent / harness。
- OpenRouter：替 agent 把请求送到 provider 的 Router，不会替你管理文件权限。
- Ollama：在本机运行模型的 runtime，不会自己读取 repo；要由支持它的 agent 调用。
- 不确定时，只问三句：谁运行模型？谁转发请求？谁能读写我的文件？
</details>

## ✅ 进 A2 前的自我检查

- [ ] 我能用自己的话分清五种身份，知道 OpenRouter 不是 LLM、Ollama 不是 coding agent。
- [ ] 我在 demo repo 完成了一次只读取的说明和计划，没有把秘密交给工具。
- [ ] 我检查过一个小改动的 diff，并能把它撤销。
- [ ] 我知道所选 CLI 的登录方式、provider、approval / sandbox 设置。

完成后进入 [A2 — 建立可重复使用的 CLI 工作流程](A2-cli-workflow.zh-Hans.md)。想再比较工具的官方状态，回看 [`resources/cli-agents-guide.zh-Hans.md`](../../resources/cli-agents-guide.zh-Hans.md)。

> 安全底线：不要在含有秘密或 production 权限的目录中做第一次实验；不要使用跳过所有确认的模式；不要把 API key、浏览器 token 或 auth 文件贴进 prompt、issue、log 或 git。

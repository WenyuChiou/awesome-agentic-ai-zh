> [繁體中文](./cli-agents-guide.md) | **简体中文** | [English](./cli-agents-guide.en.md)

# CLI Agents 参考指南

> [← 回主线路 README](../README.zh-Hans.md) · [A1：安全地跑第一个小任务](../tracks/cli/A1-cli-intro.zh-Hans.md)

这份 reference doc 按“现在要做什么”和可以核对的官方资料，整理了 9 个终端 CLI。它不替工具打分，也不按热门度或主观排名决定入口；先分清身份，再根据你的 provider、登录方式和安全边界来选择。

## 先分清楚：agent 不等于模型或 API

<table>
<thead>
<tr><th scope="col">种类</th><th scope="col">它负责什么</th><th scope="col">例子</th><th scope="col">不要混淆</th></tr>
</thead>
<tbody>
<tr><th scope="row">LLM</th><td>生成文字、代码或工具调用</td><td>Claude、GPT、Gemini</td><td>模型不会自动拥有你电脑上的文件权限</td></tr>
<tr><th scope="row">Provider API</th><td>提供某家模型的请求、认证和计费</td><td>Anthropic API、OpenAI API、Gemini API</td><td>API 不是 terminal 工作台</td></tr>
<tr><th scope="row">Router</th><td>把请求转接到多家 provider</td><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a></td><td>Router 不会代替 agent 管理文件或命令权限</td></tr>
<tr><th scope="row">Coding agent / harness</th><td>在终端里读文件、编辑、执行命令并报告结果</td><td>Claude Code、Codex、OpenCode V2、Pi</td><td>它的 approval、sandbox 和 project trust 要另外确认</td></tr>
<tr><th scope="row">Local runtime</th><td>在本机加载并运行模型</td><td><a href="https://ollama.com/">Ollama</a></td><td>它可以供 agent 调用，但本身不是 coding agent</td></tr>
</tbody>
</table>

## 按你的场景找入口

<table>
<thead>
<tr><th scope="col">你的条件</th><th scope="col">先查哪一类</th><th scope="col">要记录的差异</th></tr>
</thead>
<tbody>
<tr><th scope="row">已经有一家模型服务的账号</th><td>该生态的 CLI，例如 Claude Code、Codex 或 Gemini CLI</td><td>登录流程、approval、sandbox、usage 页面</td></tr>
<tr><th scope="row">需要更换 provider</th><td>OpenCode V2、goose、Aider、Hermes Agent 或 Pi</td><td>支持的 endpoint、模型 ID、API key 存放位置</td></tr>
<tr><th scope="row">想把多个 provider 集中转接</th><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a> 搭配一个 agent</td><td>实际路由到的 provider、数据政策、usage 和 billing</td></tr>
<tr><th scope="row">想在本机练习</th><td><a href="https://ollama.com/">Ollama</a> 搭配支持兼容 API 的 agent</td><td>模型是否在本机、agent 是否仍能执行 shell / 写文件</td></tr>
</tbody>
</table>

## 9 个 CLI 工具

完整表默认收起；展开后请把“查核日”和你的安装版本一起记下。官方资料查核日：**2026-08-27 UTC**。

<details markdown="1">
<summary>展开 9 个 CLI 的安装、认证、provider 和安全事实</summary>

<table>
<thead>
<tr><th scope="col">类型</th><th scope="col">工具</th><th scope="col">现在适合谁</th><th scope="col">模型 / provider 选择</th><th scope="col">登录方式</th><th scope="col">安全起手式</th><th scope="col">状态</th><th scope="col">官方来源</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">官方模型生态</th><td>Claude Code</td><td>想在终端使用 Anthropic 生态的人</td><td>Claude；Anthropic API</td><td>Claude 账号或 Anthropic API key</td><td>使用 demo repo；保留 permission prompt</td><td>Anthropic 官方 terminal、desktop、IDE 和 cloud 界面之一</td><td><a href="https://code.claude.com/docs/en/overview">文档</a> · <a href="https://github.com/anthropics/claude-code">repo</a></td></tr>
<tr><td>Codex CLI</td><td>想在终端使用 OpenAI / ChatGPT 登录的人</td><td>GPT 系列；OpenAI API</td><td>ChatGPT 登录或 OpenAI API key</td><td>使用默认 approval 和 workspace sandbox；先查看 diff</td><td>OpenAI 开源的 terminal coding agent</td><td><a href="https://learn.chatgpt.com/docs/codex/cli">文档</a> · <a href="https://github.com/openai/codex">repo</a></td></tr>
<tr><td>Gemini CLI</td><td>已有 Google 认证、想在 terminal 使用 Gemini 的人</td><td>Gemini；Google AI API 或 Vertex AI</td><td>Google 登录、Gemini API key 或 Vertex AI</td><td>使用 approval 模式；需要时明确开启 `--sandbox`</td><td>Google 开源的 terminal agent</td><td><a href="https://google-gemini.github.io/gemini-cli/">文档</a> · <a href="https://github.com/google-gemini/gemini-cli">repo</a></td></tr>
<tr><td>Grok Build</td><td>想试用 xAI Grok terminal TUI 的人</td><td>Grok；xAI 登录或 API key</td><td>首次交互时通过浏览器登录；CI 可用 `XAI_API_KEY`</td><td>先用 demo repo；不要复制 `~/.grok/auth.json`</td><td>xAI 官方开源的 TUI coding agent</td><td><a href="https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/02-authentication.md">认证</a> · <a href="https://github.com/xai-org/grok-build">repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">可换 provider</th><td>OpenCode V2</td><td>需要在多个 provider 之间切换的人</td><td>多个 provider；可以接 OpenRouter 或兼容 endpoint</td><td>根据 provider 设置 API key、OAuth 或环境变量</td><td>先检查 permission 设置；只在 demo repo 里试外部目录</td><td>开源 terminal coding agent；V2 项目规则使用 `AGENTS.md`，不使用旧版 `CLAUDE.md` fallback</td><td><a href="https://opencode.ai/v2/docs/providers">provider</a> · <a href="https://github.com/anomalyco/opencode">repo</a></td></tr>
<tr><td>goose</td><td>需要 CLI、desktop 或 API，还想连接工具和数据源的人</td><td>15+ provider，包括 Anthropic、OpenAI、Google、Ollama、OpenRouter</td><td>provider API key，或部分已有订阅的 ACP 登录</td><td>先用低权限 extension 和 sandbox；不要连接 production 数据</td><td>AAIF 的开源本机 agent，提供 CLI、desktop、API</td><td><a href="https://block.github.io/goose/">文档</a> · <a href="https://github.com/aaif-goose/goose">repo</a></td></tr>
<tr><td>Aider</td><td>希望用 git diff / commit 管理代码修改的人</td><td>多家 cloud API、OpenRouter、OpenAI-compatible endpoint 和本地模型</td><td>provider API key、配置文件或环境变量</td><td>先用干净的 demo repo；留意 Aider 的 git auto-commit 行为</td><td>开源 terminal pair-programming 工具，官方文档明确说明 git 集成</td><td><a href="https://aider.chat/docs/">文档</a> · <a href="https://github.com/Aider-AI/aider">repo</a></td></tr>
<tr><td>Pi</td><td>想从小核心开始，用 extensions、skills 或 RPC 扩展的人</td><td>订阅 provider、API key provider、自定义 provider；可以接本地 endpoint</td><td>`/login` 或 provider API key</td><td>Pi 没有内建 sandbox；使用 disposable repo 或容器，并人工审查命令</td><td>可扩展的 minimal terminal coding harness</td><td><a href="https://pi.dev/docs/latest/providers">provider</a> · <a href="https://github.com/earendil-works/pi">repo</a></td></tr>
<tr><td>Hermes Agent</td><td>想在 terminal、desktop 或聊天平台使用同一个 agent 的人</td><td>Nous Portal、OpenRouter、Anthropic、Google 和其他 provider</td><td>用 `hermes model` 设置 API key 或 OAuth；Nous Portal 支持 OAuth</td><td>先在低风险 repo 中使用；逐项开启 skills、MCP 和 provider 权限</td><td>Nous Research 的开源 agent，文档提供 CLI 和多界面集成</td><td><a href="https://hermes-agent.nousresearch.com/docs/integrations/providers/">provider</a> · <a href="https://github.com/NousResearch/hermes-agent">repo</a></td></tr>
</tbody>
</table>

### OpenRouter 和 Ollama 属于哪里？

OpenRouter 是 Router，不列入上面的 9 个 coding CLI；它提供统一 API、provider routing 和集中 usage。Ollama 是 local runtime，不是 agent；它可以在 `http://localhost:11434/v1` 提供兼容 API，供 OpenCode V2、goose、Aider 或其他 client 使用。两者都不能取代 agent 的文件权限和 sandbox 设计。
</details>

## Prompt 在 CLI 之间搬移时保留四件事

1. 写清文件路径、允许的范围，以及“先列计划、确认后再改”的顺序。
2. 分开记录模型、provider、API key、approval / sandbox 设置；不要假设换 CLI 后这些都相同。
3. 用普通文字描述目标；`/login`、`/permissions` 等斜线指令只在对应工具的区块使用。
4. 要求输出 `git diff`、测试结果和未完成项目，并在换另一个 CLI 前先恢复工作树。

<details markdown="1">
<summary>展开规则文件、sandbox 和常见问题</summary>

- Claude Code 的项目规则是 `CLAUDE.md`；Codex 使用 `AGENTS.md`。OpenCode V2 也使用 `AGENTS.md`，现行 V2 不使用旧版 `CLAUDE.md` fallback；不要把不存在的 `OPENCODE.md` 当作通用格式。
- Gemini CLI 的项目上下文和 `.gemini/` 设置以官方文档为准；`--sandbox`、approval mode 和 `--yolo` 的风险不同，第一次不要跳过确认。
- Pi 的 project trust 不是 sandbox，官方安全文档明确提醒它会以启动用户的权限运行；需要隔离时改用容器或其他 OS 层边界。
- Aider 官方文档说明编辑后的 git 集成和 auto-commit；先在干净的 demo repo 中观察，确认 commit 内容后再带入工作 repo。
- goose、Hermes Agent 和其他能连接 MCP / extension 的 agent，先开启一个低权限、只读的集成；不要把 Gmail、Slack 或 production DB 作为第一次外部连接。
- API key 只放在官方支持的 credential store 或环境变量中；不要放进 repo、prompt、截图或 issue。费用按当天的官方价格和实际 usage 计算，不要根据模型名称猜测。

#### 官方查核入口（2026-08-27 UTC）

- [Claude Code overview](https://code.claude.com/docs/en/overview) · [permissions](https://code.claude.com/docs/en/permissions)
- [OpenAI Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [OpenCode V2](https://opencode.ai/v2/docs) · [canonical repository](https://github.com/anomalyco/opencode)
- [Gemini CLI](https://google-gemini.github.io/gemini-cli/)
- [goose](https://block.github.io/goose/) · [canonical repository](https://github.com/aaif-goose/goose)
- [Aider](https://aider.chat/docs/)
- [Hermes Agent](https://hermes-agent.nousresearch.com/docs/)
- [Grok Build](https://github.com/xai-org/grok-build)
- [Pi](https://pi.dev/docs/latest) · [canonical repository](https://github.com/earendil-works/pi)
- [OpenRouter FAQ](https://openrouter.ai/docs/faq) · [Ollama](https://ollama.com/)
</details>

## 回到 Track A

- 要第一次安全操作：回到 [A1](../tracks/cli/A1-cli-intro.zh-Hans.md)。
- 要把规则文件和可重复流程固定下来：进入 [A2](../tracks/cli/A2-cli-workflow.zh-Hans.md)。
- 要做 MCP、CI 和 usage trace：进入 [A3](../tracks/cli/A3-cli-production.zh-Hans.md)。

> 维护原则：工具、登录、价格、sandbox 和 provider 都会变化；每次改表前重新查看官方文档，并更新查核日。这份表保持事实字段，不维护热门度或主观评分。

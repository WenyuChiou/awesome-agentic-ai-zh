# 日常用户延伸路线（For Everyday Users）

> [繁體中文](./for-everyday-users.md) | **简体中文** | [English](./for-everyday-users.en.md)

> [← 回到主路线](../README.zh-Hans.md) · 你不必先学会写程序，也不必走完整条主线。

<!-- freshness: canonical=branches/for-everyday-users.md; verified_on=2026-08-29; scope=chat-apps,connectors,cli-agents,local-runtimes,privacy,project-status; max_age_days=90 -->

<a id="使用场景生活场景--ai-怎么帮"></a>
## 📌 这条路帮你做什么

这条路教你把 AI 当成“先帮忙写草稿的助手”。你先给它材料和要求，它先做一版；最后仍由你对照原文、修正并决定要不要使用。

你可以直接从第一个练习开始。不要先放真实姓名、密码、病历、合约或公司机密。

## 🎯 学习目标

完成这一页后，你可以：

1. 把要做的事、可用材料和输出格式说清楚。
2. 分清聊天界面、**App／Connector**、**CLI Agent** 与本地模型运行环境。
3. 在连接账号、开放文件或执行命令前先看权限。
4. 对照 **Source** 检查 AI 草稿，不把流畅文字当成正确答案。

## 🧩 九个核心词

- **Prompt（提示）**：你交给 AI 的要求。像写一张工作小纸条，要说要做什么、可以用什么材料、结果长什么样。
- **Source（来源）**：你要 AI 依照的原文、图片或材料。最后要回来对照它，不能只相信 AI 的记忆。
- **Private Data（私人数据）**：不该随便交给别人的数据，例如密码、身份证号、未公开公司文件或他人的个人信息。
- **Hallucination（幻觉）**：AI 不知道答案时，仍可能写出一段很像真的内容。句子好看不代表事实存在。
- **Human Review（人工审查）**：由人把草稿和 Source 一项一项比对，修正后才决定是否使用。
- **App／Connector（服务连接器）**：聊天服务通往 Gmail、Drive 或其他服务的一扇门。它能做什么，取决于产品和你给的权限。
- **CLI Agent（命令行 Agent）**：在终端里工作的助手。它可能读写文件或执行命令，所以动手前要先看计划与 diff。
- **Local LLM／Runtime（本地模型／运行环境）**：让模型在自己的电脑上运行的软件。Runtime 负责运行模型，不等于聊天 App，也不等于 CLI Agent。
- **Approval Gate（人工批准关卡）**：真正寄信、改文件或执行高影响动作前，先停下来让人确认。

## 🛠 第一个练习：把虚构消息变成可核对的提醒

这题只用**虚构**材料。把下面整段直接贴到你正在使用的聊天工具：

```text
来源消息：
「小安说星期五前会把海报草稿交给小美。活动日期是 9 月 12 日。消息没有写交付时间。」

请帮我写一段简短提醒。只能使用来源消息里的事实，不要猜。
请输出：
1. Draft
2. Facts copied
3. Needs confirmation

不要替我发送消息。
```

完成后，自己做三个检查：

1. `Facts copied` 能不能逐句在 Source 找到？
2. 没有写出的交付时间，有没有放进 `Needs confirmation`？
3. 工具有没有只生成 Draft，而没有自行发送？

<a id="起步你应该从哪一层进入"></a>
<a id="给日常用户的层级建议"></a>
## 🚪 按工作选四扇门

**这四扇门不是等级。需要哪一扇才开哪一扇。** 多数单次任务只要第一扇；不是工具越多，结果就越好。

<table>
  <thead><tr><th>入口</th><th>五岁也懂的说法</th><th>适合什么</th><th>动手前先做什么</th></tr></thead>
  <tbody>
    <tr><td><strong>Chat surface</strong></td><td>打开一个对话框，请它先写草稿</td><td>写信、解释文章、整理公开信息</td><td>移除 Private Data；准备可核对的 Source</td></tr>
    <tr><td><strong>App／Connector</strong></td><td>帮聊天工具开一扇通往其他服务的门</td><td>搜索已授权的邮件、文件或日历</td><td>看清读取与写入权限；写入动作保留人工确认</td></tr>
  </tbody>
</table>

<a id="tier-2--cli-agent愿意学命令行的进阶用户"></a>
<table>
  <thead><tr><th>入口</th><th>五岁也懂的说法</th><th>适合什么</th><th>动手前先做什么</th></tr></thead>
  <tbody>
    <tr><td><strong>CLI Agent</strong></td><td>在终端里工作的助手</td><td>重复整理文件或执行多步骤任务</td><td>限定文件夹，先看 preview／dry-run、command 与 diff，再批准</td></tr>
    <tr><td><strong>Local LLM／Runtime</strong></td><td>模型在自己的电脑里运行</td><td>离线实验，或不想把指定数据交给云端模型</td><td>确认选的是 local model；cloud model、web search 或云端功能仍会联网</td></tr>
  </tbody>
</table>

如果你只想聊天，不需要安装 CLI Agent 或本地 Runtime。想学命令行时再去 [Track A 第一站](../tracks/cli/A1-cli-intro.zh-Hans.md)；想了解模型时再去 [Stage 1](../stages/01-llm-basics.zh-Hans.md)。

<a id="必修阅读"></a>
## 📖 必读

先读这六个短入口；它们分别回答“怎么问、能接什么、数据会去哪里”：

1. [OpenAI — Prompt engineering best practices for ChatGPT](https://help.openai.com/en/articles/10032626-how-do-i-prompt-chatgpt-effectively)：学会把要求与 context 说清楚。
2. [Anthropic — Get started with Claude](https://support.claude.com/en/articles/8114491-get-started-with-claude)：用一般对话方式开始，再逐步补充限制。
3. [OpenAI — Apps in ChatGPT](https://help.openai.com/en/articles/11487775-connectors-in)：Apps 的能力会因方案、地区、workspace 与管理员设置而不同。
4. [Anthropic — When to use desktop and web connectors](https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors)：分清 remote connector 与本机 desktop extension。
5. [Google — Gemini Apps Privacy Hub](https://support.google.com/gemini/answer/13594961?hl=en)：连接数据前先看 activity、人工审查与第三方政策。
6. [Ollama — FAQ](https://docs.ollama.com/faq)：分清本机运行、cloud model、web search 与 `local-only` 设置。

想系统学习 Prompt、zero-shot、one-shot、few-shot 与查证方法，再进入 [Stage 2 — Prompt Engineering](../stages/02-prompt-engineering.zh-Hans.md)。

<a id="-精选-projects"></a>
## ⭐ 精选 Projects 与学习资源

星级是本项目依“初学者价值、文档质量与安全边界”给出的编辑评分，不是 GitHub stars。状态与限制核查于 `2026-08-29 UTC`。

<table>
  <thead><tr><th scope="col">分类</th><th scope="col">入口／项目</th><th scope="col">它是什么</th><th scope="col">适合做什么</th><th scope="col">状态／授权</th><th scope="col">先知道的限制</th><th scope="col">评分</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">聊天界面</th><td><a href="https://claude.ai">Claude</a></td><td>云端 Chat surface</td><td>阅读、写作与反复讨论</td><td>正式可用；商业云服务</td><td>功能依方案与地区；重要内容仍要对照 Source</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://chatgpt.com">ChatGPT</a></td><td>云端 Chat surface</td><td>一般问答、语音与多种工作入口</td><td>正式可用；商业云服务</td><td>仍会出错；高影响结果要 Human Review</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://gemini.google.com">Gemini</a></td><td>Google 的云端 Chat surface</td><td>问答与符合资格的 Google 服务连接</td><td>正式可用；商业云服务</td><td>先看 activity 与人工审查设置，不放机密数据</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://perplexity.ai">Perplexity</a></td><td>带来源入口的云端搜索助手</td><td>找候选来源并建立查证起点</td><td>正式可用；商业云服务</td><td>引用不等于内容正确；要逐一打开来源</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">官方入门与安全指南</th><td><a href="https://help.openai.com/en/articles/10032626-how-do-i-prompt-chatgpt-effectively">OpenAI Prompt Guide</a></td><td>ChatGPT 官方指南</td><td>学清楚、具体与逐步改写 Prompt</td><td>现行；官方指南</td><td>好 Prompt 不能保证正确，仍要查证</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://support.claude.com/en/articles/8114491-get-started-with-claude">Claude Get Started</a></td><td>Claude 官方入门</td><td>第一次聊天与基本操作</td><td>现行；官方指南</td><td>方案有使用限制；不要假设所有功能都可用</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://help.openai.com/en/articles/11487775-connectors-in">Apps in ChatGPT</a></td><td>App／Connector 官方说明</td><td>了解搜索、同步与外部 action</td><td>商业；商业云服务</td><td>能力与权限不同；高影响 action 保留人工确认</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://support.google.com/gemini/answer/13594961?hl=en">Gemini Privacy Hub</a></td><td>Gemini 官方隐私指南</td><td>连接 Google 或第三方数据前检查设置</td><td>现行；官方隐私指南</td><td>可能处理敏感内容；不要连接不愿交给 reviewer 的机密数据</td><td>⭐⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">CLI Agent</th><td><a href="https://github.com/anthropics/claude-code">Claude Code</a></td><td>Anthropic CLI Agent</td><td>在指定工作区读取、修改文件并执行任务</td><td>活跃；商业服务；repo 未标示标准开源许可证</td><td>先设置 permission，批准前先看 command／diff</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/openai/codex">Codex</a></td><td>OpenAI coding agent</td><td>app／CLI／IDE／cloud 工作</td><td>活跃；repo 代码为 Apache-2.0，app／cloud 依服务条款</td><td>用 approval 限制写文件、命令与外部 action</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/anomalyco/opencode">OpenCode</a></td><td>可连接多种 provider 的 coding agent／harness</td><td>在终端或 desktop 使用模型做多步骤任务</td><td>活跃；MIT</td><td>provider 仍需账号／API key；用 permission 与 AGENTS.md 限定范围</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/google-gemini/gemini-cli">Gemini CLI</a></td><td>Google CLI Agent</td><td>在终端使用 Gemini 与工具</td><td>活跃；Apache-2.0</td><td>修改前看 diff／command；sandbox 只能降低风险</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">Local LLM Runtime</th><td><a href="https://github.com/ollama/ollama">Ollama</a></td><td>本地模型执行环境</td><td>下载并在自己的电脑执行模型</td><td>活跃；MIT</td><td>确认使用 local model；cloud model 与 web search 不是本机推论</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://lmstudio.ai/">LM Studio</a></td><td>图形化本地模型运行环境</td><td>用桌面界面加载已下载模型</td><td>商业；商业桌面应用程序</td><td>本地功能可离线；cloud models、搜索等云功能仍会联网</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="1">Prompt 素材</th><td><a href="https://github.com/f/prompts.chat">prompts.chat</a></td><td>社群 Prompt 示例库</td><td>找句型，再改成自己的任务</td><td>活跃；MIT／CC0</td><td>示例质量不一；不要直接贴 Private Data</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
</table>

<details markdown="1">
<summary>🔐 账号、数据、权限与费用</summary>

- App／Connector 是否出现，会受**方案、地区、workspace**、设备与管理员设置影响。没有看到功能，不代表你操作错了。
- 连接前先问：它会读什么？会把什么送给哪个服务？能不能写回？怎么撤销？
- 搜索和草拟通常是低影响动作；发信、改日历、删除文件或购买是写入动作，必须保留 Approval Gate 与人工确认。
- 云端产品的免费额度、订阅与 API 费用会变；操作前直接看产品目前显示的方案，不在教材保存固定价格。
- 不确定能不能上传时，先不要上传。公开可读也不等于你有权把别人的内容交给第三方服务处理。

</details>

<details markdown="1">
<summary>🧪 CLI Agent 与本地模型进阶步骤</summary>

CLI Agent 的安全起手式：

1. 在测试文件夹放几个可还原的虚构文件。
2. 先要求 read-only plan 或 preview／dry-run。
3. 把可读写范围限制在那个文件夹。
4. 看清 command 与 diff，再批准小步骤。
5. 执行后人工检查；不要一开始就让它发信、删除文件、付款、push 或 deploy。

官方边界：

- [Gemini CLI tools](https://geminicli.com/docs/reference/tools/) 会在修改工具前显示 action；[sandbox 文件](https://geminicli.com/docs/cli/sandbox/) 也提醒 sandbox 不是零风险保证。
- [OpenCode permissions](https://opencode.ai/docs/agents/) 可对 edit、bash 与外部文件夹设置 ask／allow／deny；[provider 文件](https://opencode.ai/docs/providers/) 显示模型连接仍需要对应账号、OAuth、API key 或环境设置。
- Ollama 可以启用 [cloud models](https://docs.ollama.com/cloud)。只要纯本机模式时，依 FAQ 设置 `disable_ollama_cloud` 或 `OLLAMA_NO_CLOUD=1`。
- LM Studio 的[离线说明](https://lmstudio.ai/docs/app/offline)指出，已下载模型、chat、文件与 local server 可以离线使用；[隐私说明](https://lmstudio.ai/app-privacy)区分本地处理与 cloud models／web search。

</details>

<a id="可以建的流程按使用频率"></a>
<details markdown="1">
<summary>🧰 更多流程、替代方案与疑难排解</summary>

可以慢慢加入的低风险流程：

- **语言练习**：请 AI 扮演对话伙伴；每次只纠正两个错误，最后由你核对教材。
- **周记草稿**：只用你愿意放进工具的笔记；先列事实，再写摘要。
- **公开文章摘要**：附上原文，要求每个重点指出 Source 段落；自己打开原文检查。
- **虚构文件整理**：先在测试文件夹 preview 新文件名，人工批准后才改名。

常见问题：

- 回答猜了不存在的数据：缩短任务，明写“不知道就放进 Needs confirmation”。
- Connector 找不到数据：先检查原服务权限、方案、workspace 管理员与支持的 surface。
- 本地模型很慢：先换较小模型；不要把“跑得动”误当成“回答一定正确”。
- 不知道选哪个入口：先用 Chat surface 完成第一题；真的需要读外部服务、改档或离线时再开其他门。

</details>

<a id="社群备注"></a>
## ✅ 完成检查与下一站

- [ ] 我能说出 Chat surface、App／Connector、CLI Agent 与 Local LLM／Runtime 的差别。
- [ ] 我知道 AI 会生成 Hallucination，会回到 Source 做 Human Review。
- [ ] 我不会把 Private Data 直接贴进数据政策不清楚的服务。
- [ ] 寄出、改档、执行命令或其他高影响动作前，我会保留 Approval Gate。

下一站依你的需要选：

- 想把 Prompt 写得更清楚：进入 [Stage 2](../stages/02-prompt-engineering.zh-Hans.md)。
- 想安全使用 CLI Agent：进入 [Track A1](../tracks/cli/A1-cli-intro.zh-Hans.md)。
- 想分清 App、Connector、MCP 与自动化：进入 [知识工作者路线](./for-knowledge-worker.zh-Hans.md)。
- 想协助改善这条路：阅读 [CONTRIBUTING.zh-Hans.md](../CONTRIBUTING.zh-Hans.md)。

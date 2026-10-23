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

<!-- connector-safety:start -->
**连接账号前，先问四件事：**

1. **读什么？**只开放这次任务需要的数据。
2. **送去哪？**先看哪些服务会收到数据。
3. **能改什么？**寄信、改文件或付款前，保留 **Approval Gate**。
4. **怎么收回？**找到停止任务、撤销连接与删除已存数据的方法。
<!-- connector-safety:end -->

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

## 🧑 个人 Agent：先说明目标与边界

<small>个人 Agent 产品查核：2026-10-02 UTC；新增与复核：2026-10-16 UTC。仅 Claude Duet 更新：2026-10-23 UTC。</small>

**个人 Agent（Personal Agent）** 是能跨工具完成多步骤工作的助手。你先说明目标，它先查资料、写草稿，再拿回来请你确认。这类产品把模型、工具与权限放在一起。产品名称不是底层模型名称，也不是新的升级等级。

这里也纳入消息式个人代理：看它是否保留个人情境、连接日常工具并持续跟进。下表加入初创公司出身的 Instinct、Tab、Tomo 与 Poke。Poke 已加入 Cognition，不再列为独立团队。聊天陪伴、单一提醒工具与企业工作流平台不一定符合这个范围。可用性与隐私细节见下方“账号、数据、权限与费用”。

第一次仍用上面的虚构消息，先不要连接账号。需要跨工具时，再限定它能读取什么、能修改什么，以及何时必须停下来请你批准。发出、发布、删除文件或付款前保留 **Approval Gate**。“持续工作”不代表可以跳过人工检查。

**Claude Duet** 是会持续追踪任务的个人 Agent，不是新模型。目前是美国 Pro／Max 的研究预览，仍需候补邀请；Team／Enterprise 尚未开放。官方说明：寄信、付款、签署或删除前会请你批准。撤销 App 连接后，**记忆不会自动删除**。先读[资格与数据限制](https://support.claude.com/en/articles/17631495-get-started-with-claude-duet)，不要直接接私人账号。

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

星级依“初学者价值、文档质量与安全边界”给分。不是 GitHub stars。其他资源的状态与限制核查于 `2026-08-29 UTC`。个人 Agent 入口新增与复核于 `2026-10-16 UTC`。仅 Claude Duet 新增于 `2026-10-23 UTC`。三星代表可选的具体产品示例，适合互相对照。它们是未实测的参考／对照示例，不是必修工具。评分依官方文档的教学价值，不代表产品的实测质量。

<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="资源表（分类、用途与限制）">
<table>
  <thead><tr><th scope="col">分类</th><th scope="col">资源、用途与限制</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">聊天界面</th><td><p data-field="entry"><strong><a href="https://claude.ai">Claude</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="identity">云端 Chat surface</p><p data-field="use">阅读、写作与反复讨论</p><p data-field="status">正式可用；商业云服务</p><p data-field="limits">功能依方案与地区；重要内容仍要对照 Source</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://chatgpt.com">ChatGPT</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="identity">云端 Chat surface</p><p data-field="use">一般问答、语音与多种工作入口</p><p data-field="status">正式可用；商业云服务</p><p data-field="limits">仍会出错；高影响结果要 Human Review</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://gemini.google.com">Gemini</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="identity">Google 的云端 Chat surface</p><p data-field="use">问答与符合资格的 Google 服务连接</p><p data-field="status">正式可用；商业云服务</p><p data-field="limits">先看 activity 与人工审查设置，不放机密数据</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://perplexity.ai">Perplexity</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="identity">带来源入口的云端搜索助手</p><p data-field="use">找候选来源并建立查证起点</p><p data-field="status">正式可用；商业云服务</p><p data-field="limits">引用不等于内容正确；要逐一打开来源</p></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="8">个人 Agent</th><td><p data-field="entry"><strong><a href="https://learn.chatgpt.com/docs/dots">OpenAI dots</a></strong> <span data-field="rating">⭐⭐⭐</span></p><p data-field="identity">个人 Agent 产品／官方文档</p><p data-field="use">适合谁：想学持续任务与批准边界的日常用户。教什么：先用虚构数据学习目标、工具与批准边界。</p><p data-field="status">逐步开放；商业云服务</p><p data-field="limits">依方案、年龄、地区与管理员设置；账号可能尚未开放</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://support.claude.com/en/articles/17631495-get-started-with-claude-duet">Claude Duet</a></strong> <span data-field="rating">⭐⭐⭐</span></p><p data-field="identity">个人 Agent 产品／官方文档</p><p data-field="use">适合谁：比较持续任务的日常用户。教什么：先限制数据，再批准对外动作。</p><p data-field="status">研究预览；美国 Pro／Max，需候补邀请；商业云服务</p><p data-field="limits">Team／Enterprise 未开放；撤销连接不会自动清除记忆</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/">Meta Muse</a></strong> <span data-field="rating">⭐⭐⭐</span></p><p data-field="identity">个人 Agent 产品／官方介绍</p><p data-field="use">适合谁：想练跨 App 草拟的日常用户与小商家。教什么：学跨 App 草拟与行动前人工批准。</p><p data-field="status">限区可用；商业云服务</p><p data-field="limits">美国与加拿大；Meta 表示发布、发送与花费须批准</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://docs.x.ai/grok-bot/overview">Grok Bot</a></strong> <span data-field="rating">⭐⭐⭐</span></p><p data-field="identity">个人 Agent 产品／官方文档</p><p data-field="use">适合谁：想比较持续任务与共享数据的日常用户。教什么：学持续任务与共享电脑的数据边界。</p><p data-field="status">符合资格方案可用；商业云服务</p><p data-field="limits">需符合资格的付费方案；同账号 Bots 共享文件与登录</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://instinct.com/">Instinct</a></strong> <span data-field="rating">⭐⭐⭐</span></p><p data-field="identity">消息／通话式个人代理</p><p data-field="use">适合谁：比较生活任务委派的用户。教什么：模型训练与授权范围。</p><p data-field="status">商业服务；资格须查账号</p><p data-field="limits">18 岁以上；训练退出有例外</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://tab.bot/">Tab</a></strong> <span data-field="rating">⭐⭐⭐</span></p><p data-field="identity">消息式个人代理</p><p data-field="use">适合谁：比较跨工具委派的用户。教什么：候补、付款批准与账号密码隔离。</p><p data-field="status">Private beta；商业服务</p><p data-field="limits">候补不保证开放；付款限部分测试用户</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://www.tomo.ai/about">Tomo</a></strong> <span data-field="rating">⭐⭐⭐</span></p><p data-field="identity">Mapo Labs 个人 AI</p><p data-field="use">适合谁：跟进目标与日常安排的用户。教什么：长期情境与群聊数据边界。</p><p data-field="status">付费方案；商业服务</p><p data-field="limits">授权人员可能审阅对话；群聊涉及他人数据</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://poke.com/">Poke</a></strong> <span data-field="rating">⭐⭐⭐</span></p><p data-field="identity">初创公司出身的消息式个人代理</p><p data-field="use">适合谁：比较邮件与日历自动化的用户。教什么：主动提醒、方案及产品归属变化。</p><p data-field="status">免费／付费方案；已加入 Cognition</p><p data-field="limits">核对用量与额外费用；检查 Maximum Privacy</p></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">官方入门与安全指南</th><td><p data-field="entry"><strong><a href="https://help.openai.com/en/articles/10032626-how-do-i-prompt-chatgpt-effectively">OpenAI Prompt Guide</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="identity">ChatGPT 官方指南</p><p data-field="use">学清楚、具体与逐步改写 Prompt</p><p data-field="status">现行；官方指南</p><p data-field="limits">好 Prompt 不能保证正确，仍要查证</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://support.claude.com/en/articles/8114491-get-started-with-claude">Claude Get Started</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="identity">Claude 官方入门</p><p data-field="use">第一次聊天与基本操作</p><p data-field="status">现行；官方指南</p><p data-field="limits">方案有使用限制；不要假设所有功能都可用</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://help.openai.com/en/articles/11487775-connectors-in">Apps in ChatGPT</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="identity">App／Connector 官方说明</p><p data-field="use">了解搜索、同步与外部 action</p><p data-field="status">商业；商业云服务</p><p data-field="limits">能力与权限不同；高影响 action 保留人工确认</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://support.google.com/gemini/answer/13594961?hl=en">Gemini Privacy Hub</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="identity">Gemini 官方隐私指南</p><p data-field="use">连接 Google 或第三方数据前检查设置</p><p data-field="status">现行；官方隐私指南</p><p data-field="limits">可能处理敏感内容；不要连接不愿交给 reviewer 的机密数据</p></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">CLI Agent</th><td><p data-field="entry"><strong><a href="https://github.com/anthropics/claude-code">Claude Code</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="identity">Anthropic CLI Agent</p><p data-field="use">在指定工作区读取、修改文件并执行任务</p><p data-field="status">活跃；商业服务；repo 未标示标准开源许可证</p><p data-field="limits">先设置 permission，批准前先看 command／diff</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://github.com/openai/codex">Codex</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="identity">OpenAI coding agent</p><p data-field="use">app／CLI／IDE／cloud 工作</p><p data-field="status">活跃；repo 代码为 Apache-2.0，app／cloud 依服务条款</p><p data-field="limits">用 approval 限制写文件、命令与外部 action</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://github.com/anomalyco/opencode">OpenCode</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="identity">可连接多种 provider 的 coding agent／harness</p><p data-field="use">在终端或 desktop 使用模型做多步骤任务</p><p data-field="status">活跃；MIT</p><p data-field="limits">provider 仍需账号／API key；用 permission 与 AGENTS.md 限定范围</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://github.com/google-gemini/gemini-cli">Gemini CLI</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="identity">Google CLI Agent</p><p data-field="use">在终端使用 Gemini 与工具</p><p data-field="status">活跃；Apache-2.0</p><p data-field="limits">修改前看 diff／command；sandbox 只能降低风险</p></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">Local LLM Runtime</th><td><p data-field="entry"><strong><a href="https://github.com/ollama/ollama">Ollama</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="identity">本地模型执行环境</p><p data-field="use">下载并在自己的电脑执行模型</p><p data-field="status">活跃；MIT</p><p data-field="limits">确认使用 local model；cloud model 与 web search 不是本机推论</p></td></tr>
    <tr><td><p data-field="entry"><strong><a href="https://lmstudio.ai/">LM Studio</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="identity">图形化本地模型运行环境</p><p data-field="use">用桌面界面加载已下载模型</p><p data-field="status">商业；商业桌面应用程序</p><p data-field="limits">本地功能可离线；cloud models、搜索等云功能仍会联网</p></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="1">Prompt 素材</th><td><p data-field="entry"><strong><a href="https://github.com/f/prompts.chat">prompts.chat</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="identity">社群 Prompt 示例库</p><p data-field="use">找句型，再改成自己的任务</p><p data-field="status">活跃；MIT／CC0</p><p data-field="limits">示例质量不一；不要直接贴 Private Data</p></td></tr>
  </tbody>
</table>
</div>

<details markdown="1">
<summary>🔐 账号、数据、权限与费用</summary>

- App／Connector 是否出现，会受**方案、地区、workspace**、设备与管理员设置影响。没有看到功能，不代表你操作错了。
- 连接前先问：它会读什么？会把什么送给哪个服务？能不能写回？怎么撤销？
- 搜索和草拟通常是低影响动作；发信、改日历、删除文件或购买是写入动作，必须保留 Approval Gate 与人工确认。
- 云端产品的免费额度、订阅与 API 费用会变；操作前直接看产品目前显示的方案，不在教材保存固定价格。
- 不确定能不能上传时，先不要上传。公开可读也不等于你有权把别人的内容交给第三方服务处理。

个人 Agent 产品细节（2026-10-16 UTC；文档查核，未实测）：

- [Claude Duet](https://support.claude.com/en/articles/17631495-get-started-with-claude-duet)（仅此项：2026-10-23 UTC）：在自己的云端电脑上工作，使用 Claude Opus 5.5，不能自行选模型。后台工作也计入 Pro／Max 方案用量，不是无限免费 API。现有 Claude 的记忆、Skills 与连接器会延续使用。先检查共享数据与记忆设置；寄信、付款、签署或删除仍需人工批准。参考 [10/21 官方公告](https://claude.com/resources/articles/claude-duet)。

- [OpenAI dots](https://learn.chatgpt.com/docs/dots)：持续工作的云助手，有自己的云电脑与浏览器，底层模型为 GPT-6 Astra。你关掉电脑后仍能继续；它会记住偏好与待办、在后台并行工作，分享私人对话信息给他人前须先取得你的允许。[2026-09-29 更新](https://learn.chatgpt.com/docs/whats-new/devday-2026)说明了逐步开放。Pro 100、Pro 200、Pro 500 限超过 18 岁。也限在欧洲经济区、英国与瑞士以外。Business Premium、Enterprise 在全球逐步开放。Enterprise 须由管理员启用。符合方案不代表账号已经获得功能。
- [Meta Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)：用自己的云电脑跨 App 工作。[2026-09-29 Muse for Small Business 更新](https://about.fb.com/news/2026/09/introducing-muse-small-business/)确认美国与加拿大可用。也加入商务 skills 与 connectors。Meta 表示发布、发送与花费须先取得你的批准。另有 Sentinel 代理审核对外联网动作；Muse 提供活动审计轨迹。密码与付款资料分开存放于安全存储，Muse 本身看不到。Muse 是产品；Muse Spark 是模型。Muse Code 是在终端工作的 coding agent。
- [Grok Bot](https://docs.x.ai/grok-bot/overview)：使用持续保留状态的云电脑。它能用浏览器、文件与终端做事。需付费 Cursor 方案或连接符合资格的 SuperGrok 方案，用量每周重置。同一账号的 Bots 共享电脑、文件、浏览器会话与 App 登录。不能把它们当成彼此隔离。[2026-09-28 Team Bots 更新](https://x.ai/news/team-bots)加入 public beta。此 public beta 支持 Teams 与 Enterprise 方案。可共享 skills、工具并在 Slack 协作。Grok Bot 是产品，不是 Grok 模型名称。也不是用于编程的 [Grok Build](https://docs.x.ai/build/overview)。
- [Instinct](https://instinct.com/)（Spear Street Technology）：通过文字或通话交代生活任务，官方展示购物与订票等用途。[条款](https://instinct.com/terms)要求年满 18 岁；公开入口未列完整价格与地区资格，应以账号当下信息为准。[隐私政策](https://instinct.com/privacy-policy)允许部分数据用于模型训练，提供退出设置但有例外；不要假设每个对外动作都会自动停下来确认。
- [Tab](https://tab.bot/)（Terrasoft）：在消息里委派工作，保留此前情境，使用自己的电脑、浏览器与已连接账号，也能代打电话。[目前为 private beta](https://tab.bot/terms)，候补不保证开放时间、价格或功能；付款功能只限部分测试用户。[官方安全说明](https://tab.bot/security)要求付款绑定具体交易与批准，密码及卡号走独立流程，不贴在消息里。
- [Tomo](https://www.tomo.ai/about)（Mapo Labs）：小团队的个人 AI，记住对话情境、主动提醒，并连接邮件与日历，适合比较目标跟进及日常安排。提供付费方案，价格与消息额度可能因用户而异。[隐私政策](https://www.tomo.ai/privacy)说明授权人员可能审阅对话；加入群聊也会处理其他参与者的数据，先确认分享范围。
- [Poke](https://poke.com/)（The Interaction Company，已[加入 Cognition](https://cognition.com/blog/interaction)）：在消息界面使用个人情境、连接服务与主动提醒，可处理邮件、日历及自动化。[方案](https://poke.com/pricing)有免费与付费层级，用量限制与额外费用要另查。[隐私政策](https://poke.com/privacy)提供 Maximum Privacy 的模型训练排除设置；先看设置再连接私人账号。

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
- [ ] 我能分清个人 Agent 产品与模型，也会检查可用性及共享数据范围。

下一站依你的需要选：

- 想把 Prompt 写得更清楚：进入 [Stage 2](../stages/02-prompt-engineering.zh-Hans.md)。
- 想安全使用 CLI Agent：进入 [Track A1](../tracks/cli/A1-cli-intro.zh-Hans.md)。
- 想分清 App、Connector、MCP 与自动化：进入 [知识工作者路线](./for-knowledge-worker.zh-Hans.md)。
- 想协助改善这条路：阅读 [CONTRIBUTING.zh-Hans.md](../CONTRIBUTING.zh-Hans.md)。

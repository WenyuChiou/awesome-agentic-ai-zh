# 开发者延伸路线（For Developers）

> [繁體中文](./for-developer.md) | **简体中文** | [English](./for-developer.en.md)

[← 回到主路线](../README.zh-Hans.md)

<!-- freshness: canonical=branches/for-developer.md; verified_on=2026-08-29; scope=coding-agents,tool-identity,permissions,sandboxing,project-status; max_age_days=90 -->

<a id="使用场景开发场景-ai-怎么帮"></a>
## 📌 这条路帮你做什么

AI 编程助手像一个会读文件、改代码、运行命令的队友。它速度快，也可能出错。这条路教你先缩小任务，再看懂每项改动，最后由人决定是否保留。

建议路线：`A1 → A2 → Stage 5 的 5.1–5.4 → A3`。可依次学习 [A1](../tracks/cli/A1-cli-intro.zh-Hans.md)、[A2](../tracks/cli/A2-cli-workflow.zh-Hans.md)、[Stage 5](../stages/05-claude-code-ecosystem.zh-Hans.md) 与 [A3](../tracks/cli/A3-cli-production.zh-Hans.md)；[Stage 8](../stages/08-agent-interfaces.zh-Hans.md) 建议完成，但不影响你先开始这条路线。已走 Track B 的读者可先读 [Stage 7](../stages/07-multi-agent-production.zh-Hans.md)。

## 🎯 学习目标

完成这一页后，你可以：
1. 分清工具本身是什么，以及从哪个界面或入口使用它。
2. 先限制文件、命令和网络，再让工具动手。
3. 用差异、测试、人工检查与回滚管理一次小改。
4. 分开检查代码质量、代理行为与生产环境记录。

<a id="coding-agents"></a>
## 🧩 八个核心词

- **IDE／Surface（集成开发环境／操作界面）**：IDE 是写代码的工作台；Surface 是操作工具的入口，例如 CLI、IDE、desktop 或 cloud。同一工具可以有多个 Surface，看起来像 IDE 不代表它只能在 IDE 中工作。
- **Coding Agent／Harness（程序代理／代理运行框架）**：Coding Agent 会读代码、使用工具、修改文件并根据结果继续。Harness 把模型、工具、规则与执行循环连接起来。两者常在同一产品中，但含义不同。
- **Provider／Router（供应商／路由器）**：Provider 提供模型服务；Router 把请求发送给一个或多个 Provider。Router 不是模型，也不会管理 repo 权限。
- **Model／Runtime（模型／运行环境）**：Model 生成下一步内容；Runtime 让模型在本机或服务中运行。本地 Runtime 不等于会改代码的代理。
- **Sandbox（沙箱）**：运行代码的有限区域，能缩小出错范围，但不是百分之百的保证。
- **Approval（人工批准）**：高风险操作前由人明确许可。Test 通过不等于自动获得 push、merge 或 deploy 权限。
- **Diff／Rollback（差异／回滚）**：Diff 显示改了什么；Rollback 撤回不想要的改动。先读 Diff，才知道回滚应触及哪些文件。
- **Eval／Observability（评测／可观测性）**：Eval 用固定案例测质量；Observability 保存执行中的 trace、log、成本与错误。

### 不要混淆 OpenCode、Pi、OpenRouter 与 Ollama

| 名称 | 核心身份 | 白话说法 |
|---|---|---|
| OpenCode | Coding Agent／Harness | 在代码项目中读取、修改并测试 |
| Pi | Coding Agent／Harness | 从小核心加入 extensions、skills 或 RPC |
| OpenRouter | API Router | 把模型请求发送给 Provider；不会修改 repo |
| Ollama | Local Model Runtime | 在本机运行模型和 API；本身不是 Coding Agent |

**OpenCode／Pi 负责做事，OpenRouter 负责带路，Ollama 负责运行本地模型。**

<a id="code-review"></a>
## 🛠 第一个练习：完成一次可回滚的小改

请在可丢弃的 demo repo 或新 branch 操作，把下面内容贴给 Coding Agent：
```text
先做 read-only plan，不要修改任何文件。
任务：找出 README.md 中一句可以更清楚、但不改变技术含义的句子。
请先回报要改哪一句、为什么是小范围改动、应运行哪个 test 或文档检查，以及 rollback 方法。
在我明确人工 Approval 前不要写文件。批准后只准修改 README.md。
完成后显示 git diff -- README.md，并回报 Test 结果。不要 push、merge 或 deploy。
```
读完 plan 后由人工批准。修改完成后运行：

```powershell
git diff -- README.md
# 接着运行这个 repo 的文档 test 或最小相关 test
```

若改动不对，确认 README.md 没有别人的工作后，只回滚本练习的改动；不要清空整个工作区。

<a id="推荐工具"></a><a id="tier-升级路径"></a>
## 📚 先选一个入口

| 想做什么 | 先看什么 | 为什么 |
|---|---|---|
| 学完整的权限与 sandbox 流程 | [Claude Code](https://code.claude.com/docs/en/overview) | 文档把权限、隔离与多种 Surface 分开说明 |
| 使用 app、CLI、IDE 或 cloud 工作 | [OpenAI Codex](https://github.com/openai/codex) | 同一 Coding Agent 可从多个入口工作 |
| 把 GitHub issue 交给 cloud agent | [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent) | 理解 cloud agent 与 IDE agent mode 的区别 |
| 使用开源、可替换 Provider 的工具 | [OpenCode](https://github.com/anomalyco/opencode) | 分开理解 Coding Agent、Provider 与 Router |
| 从 IDE 开始并逐步批准 | [Cline](https://github.com/cline/cline) | 练习逐步批准工具、文件与浏览器操作 |

不要只问“哪个最强”。先问它能看到哪些文件、能运行哪些命令、是否可联网、谁批准高风险操作，以及失败时如何回滚。

<a id="必修阅读"></a>
## 📖 必读

按顺序阅读，每篇先回答一个问题：
1. [Claude Code permissions](https://code.claude.com/docs/en/permissions)：`allow`、`ask`、`deny` 各代表什么？
2. [OpenAI Codex agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)：Sandbox、Approval 与网络控制如何协同？
3. [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent)：Cloud agent 与 IDE agent mode 在哪里运行？
4. [Pi — Permissions & Containerization](https://github.com/earendil-works/pi#permissions--containerization)：没有内置 permission sandbox 时，责任落在哪里？
5. [OpenRouter provider selection](https://openrouter.ai/docs/guides/routing/provider-selection)：Router 如何选择 Provider？
6. [Ollama docs](https://docs.ollama.com/)：Local Model Runtime 提供什么，又不提供什么？

<a id="精选-projects"></a><a id="社群备注"></a>
## ⭐ 精选工具与项目
<small>工具身份、Surface、授权与 repository 状态于 2026-08-29 UTC 依据官方文档与 GitHub API 核查。推荐度是本学习地图的编辑评分，不是 GitHub stars 或性能排名。</small>

<table><thead><tr><th scope="col">分类</th><th scope="col">官方工具／项目</th><th scope="col">核心身份</th><th scope="col">主要 Surface</th><th scope="col">适合做什么</th><th scope="col">状态、授权与限制</th><th scope="col">推荐度</th></tr></thead>
<tbody><tr><th scope="rowgroup" rowspan="4">官方／商业 Coding Agents</th><td><a href="https://code.claude.com/docs/en/overview">Claude Code</a></td><td>coding agent</td><td>CLI／IDE／desktop／cloud</td><td>学习 permission、sandbox、project rules 与完整 workflow</td><td>商业；保留 permission prompt，从小 repo 开始</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/openai/codex">openai/codex</a></td><td>coding agent</td><td>app／CLI／IDE／cloud</td><td>比较本机与远端的工作方式</td><td>活跃；repo 代码为 Apache-2.0，app／cloud 依服务条款；不要关闭必要 Approval 或扩大 workspace 权限</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent">GitHub Copilot</a></td><td>coding agent／code assistant</td><td>GitHub／IDE／CLI／app</td><td>从 IDE 协作走到 issue、branch 与 PR</td><td>商业；Cloud agent 与 IDE mode 权限不同，产出仍需人工 review</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://cursor.com/docs">Cursor</a></td><td>coding agent + AI editor</td><td>IDE／CLI／cloud／SDK</td><td>比较 editor、background agent 与其他 Surface</td><td>商业；分别确认各 Surface 的权限与数据边界</td><td>⭐⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="6">开源 Coding Agents／Harnesses</th><td><a href="https://github.com/anomalyco/opencode">anomalyco/opencode</a></td><td>coding agent／harness</td><td>terminal／desktop</td><td>切换 Provider 或兼容 endpoint</td><td>活跃；MIT；<code>AGENTS.md</code> 优先，缺少时才用 <code>CLAUDE.md</code></td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/earendil-works/pi">earendil-works/pi</a></td><td>coding agent／harness</td><td>terminal／SDK／RPC</td><td>从小核心加入 extensions、skills 与自定义流程</td><td>活跃；MIT；没有内置 sandbox，需自行隔离</td><td>⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/Aider-AI/aider">Aider-AI/aider</a></td><td>coding agent／pair programmer</td><td>CLI</td><td>用 Git diff、commit 与 undo 管理小改</td><td>活跃；Apache-2.0；auto-commit 不代表可以跳过 hook</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/aaif-goose/goose">aaif-goose/goose</a></td><td>coding／general agent</td><td>CLI／desktop／API</td><td>连接 Providers、MCP 与 extensions</td><td>活跃；Apache-2.0；先从低权限 extension 开始</td><td>⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/cline/cline">cline/cline</a></td><td>coding agent</td><td>IDE／CLI／SDK</td><td>逐步批准工具、文件与 browser 操作</td><td>活跃；Apache-2.0；IDE Surface 不是安全保证</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/OpenHands/OpenHands">OpenHands/OpenHands</a></td><td>software-development agent platform</td><td>web／CLI／SDK／cloud</td><td>在隔离环境中处理较完整的 issue</td><td>活跃；MIT；任务越大越需要 checkpoint 与人工 review</td><td>⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="2">Workflow 支持</th><td><a href="https://github.com/obra/superpowers">obra/superpowers</a></td><td>workflow collection</td><td>agent plugin／skills</td><td>参考 planning、TDD、debug 与 review 流程</td><td>活跃；MIT；模板仍要配合 repo gate</td><td>⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/yamadashy/repomix">yamadashy/repomix</a></td><td>repo context packer</td><td>CLI／MCP</td><td>整理一次性的 codebase context</td><td>活跃；MIT；输出前排除 secrets 与不必要文件</td><td>⭐⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="2">维护／历史</th><td><a href="https://github.com/continuedev/continue">continuedev/continue</a></td><td>coding agent</td><td>CLI／VS Code／JetBrains</td><td>阅读开源 editor-agent 集成的历史设计</td><td>read-only；Apache-2.0；官方 2.0.0 是最后版本，不再积极维护</td><td>⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/RooCodeInc/Roo-Code">Roo Code</a></td><td>coding agent</td><td>VS Code extension</td><td>阅读多 mode 代理的设计历史</td><td>已封存；Apache-2.0；新项目请改用仍在维护的工具</td><td>⭐⭐⭐</td></tr></tbody></table>

<a id="也适用其他分支"></a>
## ✅ 完成检查与下一站
- [ ] 我能说出 Coding Agent／Harness、Router 与 Local Model Runtime 的区别。
- [ ] 工具先给 read-only plan，人工批准后才改一个文件。
- [ ] 我读过完整 Diff，也执行了对应 Test。
- [ ] 我知道如何只 Rollback 这次改动，而且工具没有 push、merge 或 deploy。

下一站：设计 Skills／MCP 走 [Stage 5](../stages/05-claude-code-ecosystem.zh-Hans.md)；做 Eval、Observability 与 production gate 走 [Stage 7](../stages/07-multi-agent-production.zh-Hans.md)；比较 CLI agents 看 [CLI agent 指南](../resources/cli-agents-guide.zh-Hans.md)。

<details markdown="1"><summary>⏱ 展开：时间、环境、费用与 secret 边界</summary>
第一个练习约需 20–40 分钟。使用可丢弃 repo 或新 branch，先看 `git status`，不要让代理覆盖同事或其他工具正在修改的文件。API key 放环境变量或 secret store，不放进 prompt、README 或 commit；关闭不需要的网络、外部目录与 shell 权限。费用随 Model、Provider、输入量和重试次数变化。Sandbox 只能缩小爆炸范围；外部服务、credential 与人工批准仍需分别保护。
</details>
<a id="必练流程按使用频率"></a><a id="3-个具体-workflow-recipe"></a>
<details markdown="1"><summary>🧪 展开：从每日小改走到团队 workflow</summary>
### 每日开发
`plan → 人工批准 → 小改 → diff → test → review → commit`。每一步都应能停下。
### PR review
把代理意见当作候选 finding；要求文件、行为、复现方式与建议 Test。没有证据的猜测不能直接阻挡。
### CI
CI agent 使用只读 token、最小 repo 权限与固定输入。Issue、PR 或网页文字不能直接变成可执行命令。发布、merge 与 secrets 保留额外批准。
### 批量重构
先建立基准测试，再按模块分批。每批都有 checkpoint、Diff 与 Rollback；不要一次交出整个 repo。
</details>
<a id="常见踩坑anti-patterns"></a>
<details markdown="1"><summary>🧯 展开：常见错误、替代方案与 rollback</summary>
| 问题 | 改成什么 |
|---|---|
| 看到 IDE 画面就以为工具只能在 IDE 用 | 分开看核心身份与所有 Surface |
| 把 OpenRouter、Ollama、OpenCode 当同一类 | Router、Runtime、Coding Agent 分开选 |
| 工具说 Test 绿就直接接受 | 自己读 Diff、确认覆盖需求，再人工批准 |
| 用固定行数判断安全 | 看范围、可测性、可回滚性与 Diff 是否可读 |
| Aider 自动 commit 就跳过 hook | 启用 repo 所需的 verify／hook，再走正常 review gate |
| 多个工具同时改同一文件 | 分清 ownership，使用独立 worktree，最后人工整合 |

Rollback 前先看 `git status` 和 Diff，只回滚已确认的目标，不用 broad reset 清掉别人的工作。
</details>

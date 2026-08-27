# A3 — 把 CLI agent 接入安全的团队流程

> [繁體中文](./A3-cli-production.md) | **简体中文** | [English](./A3-cli-production.en.md)

> [← A2 — 让 CLI agent 每次都按同一套方法做事](A2-cli-workflow.zh-Hans.md) · **Track A: CLI Power User** 第 3 站（最后）

这一站只做一件事：**让 CLI agent 在测试用 PR 做一次只读检查。它可以提出意见，但不能自己合并、部署或取得额外权限。**

## 📌 学习目标

完成后，你可以：

- 只把一个安全范围交给 **MCP** server。
- 让 **CI** 在 PR 自动生成一份可检查的建议。
- 用 **Observability** 看懂一次运行留下的 usage、时间和结果。
- 把 A2 的 Skill 交给队友，并让对方安全地重新运行。

## 🧩 先认识三个核心词

| 核心词 | 它是什么、像什么 | A3 怎么用 | 不是什么 |
|---|---|---|---|
| **MCP（Model Context Protocol）** | 让 agent 连接外部工具或数据的标准转接头 | 只把一个 demo 文件夹或只读工具交给 server | 不是自动安全；能碰什么仍取决于权限 |
| **CI（Continuous Integration）** | push 或 PR 出现时会自动工作的检查站 | 让测试 PR 自动跑一次只读 review | 不是可以跳过人工 review 的 auto-merge 按钮 |
| **Observability（观测与记录）** | 像收据加行车记录，留下发生过的事 | 记下 provider、model、usage、时间、结果与失败原因 | 不是只看一个总 token 或猜测拿不到的成本 |

三个词会一起出现，但不是一回事：MCP 负责“接工具”，CI 负责“何时自动运行”，observability 负责“运行后留下什么证据”。

## 先走安全阶梯

1. **只读**：先让 agent 看数据，不让它改数据。
2. **最小权限**：只开启这次需要的文件夹、repo、tool 或 token scope。
3. **demo repo**：先在可丢弃的练习环境测试。
4. **人工 review**：由人决定要不要采用 agent 的建议。
5. **最后才考虑写入**：auto-merge、push、deploy 不属于这一站。

<details markdown="1">
<summary>展开时间、前置条件、环境和费用</summary>

- **时间**：先完成四个最小成果，通常可以拆成几次短练习；不要为了赶时间一次接入很多服务。
- **前置条件**：完成 [A1](A1-cli-intro.zh-Hans.md) 和 [A2](A2-cli-workflow.zh-Hans.md)，并能看懂 `git status`、PR 和 GitHub Actions 的基本界面。
- **环境**：一个没有真实 secrets 的 demo repo；第一轮使用 GitHub-hosted Linux runner，更容易套用 sandbox。
- **费用**：GitHub Actions、CLI 订阅和模型 API 可能分别计费。运行前先查看自己使用的方案，不要把别人的价格当成自己的价格。

如果 A2 的 `review-changes` Skill 还不能稳定输出 `PASS` 或具体问题，先回去修好再进入 A3。
</details>

## 📚 必读

<details markdown="1">
<summary>展开必读资料与阅读顺序（查核于 2026-08-27 UTC）</summary>

1. 先看 [MCP Connect to local servers](https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers)，了解 server 只能拿到你交给它的路径。
2. 再看 [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)，先理解 least privilege 和不可信 PR。
3. 选择一条 CI 路径：
   - Claude Code：[官方 GitHub Actions 文档](https://code.claude.com/docs/en/github-actions)
   - Codex：[官方 GitHub Action 文档](https://learn.chatgpt.com/docs/github-action)
4. 需要 trace、eval 或完整 production 理论时，再进入 [Stage 7](../../stages/07-multi-agent-production.zh-Hans.md) 和 [Stage 7.5](../../stages/07.5-advanced-agentic-concepts.zh-Hans.md)。

查核日期只代表上面的资料在当天已检查，不代表它们永远不会改变。
</details>

## 🛠 动手练习

<a id="cli-9"></a>
### 动手练习 CLI-9：只连接一个 MCP server

**成果：** agent 能读到一个新建的 demo 文件夹，但没有取得整个 home、磁盘、真实项目或 secrets。

先复制适合你电脑的指令，创建 `a3-mcp-demo/hello.txt`。

PowerShell：

```powershell
New-Item -ItemType Directory -Force -Path a3-mcp-demo | Out-Null
Set-Content -LiteralPath a3-mcp-demo/hello.txt -Value 'hello from A3'
```

macOS／Linux：

```bash
mkdir -p a3-mcp-demo
printf 'hello from A3\n' > a3-mcp-demo/hello.txt
```

把官方 filesystem reference server 接到你的 CLI 时，**只传入这个文件夹的绝对路径**。

成功时，agent 能读出 `hello.txt`；要求它读取范围外的文件时，应该失败或要求你重新授权。

<details markdown="1">
<summary>展开 CLI-9 的安装、权限测试与 GitHub MCP 延伸</summary>

1. 根据你主要使用的 CLI 官方 MCP 文档打开设置；不同 CLI 的配置文件和命令不一定相同。
2. 使用官方 package `@modelcontextprotocol/server-filesystem`，arguments 只放 `a3-mcp-demo` 的绝对路径。不要填 `~`、home、磁盘根目录或整个工作区。
3. 重启 CLI，让它列出 demo 文件夹，再读取 `hello.txt`。
4. 让它读取 demo 范围外的一个普通文件名。正确结果是拒绝或先要求新增授权；不能偷偷读取。
5. 练习后移除 server 配置，确认 CLI 已不能再使用它。

要读取 PR 或 issue 时，改看 GitHub 官方的 [`github/github-mcp-server`](https://github.com/github/github-mcp-server)。先使用 `--read-only`，再用 toolsets 或 tools allow-list 只开启需要的能力。如果使用 PAT，把它放在安全的 secret／环境变量中，授予最少 scope，练习后撤销；能用 OAuth 时，按 host 官方流程设置。

[`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) 适合阅读 reference implementation，但官方说明它们不是 production-ready。旧的 `github` reference server 已移到历史集合，不要再把它作为当前 GitHub 入口。

**费用提醒：** 本地 filesystem server 通常不另外收费，但 CLI／模型仍可能计费。远程 MCP 也可能有自己的方案。
</details>

<a id="cli-10"></a>
### 动手练习 CLI-10：让 PR 多一个只读检查员

**成果：** 测试用 PR 会留下 review 结果；人仍决定是否修改、合并或部署。

选择 Anthropic 的 [`claude-code-action`](https://github.com/anthropics/claude-code-action) 或 OpenAI 的 [`codex-action`](https://github.com/openai/codex-action)。第一轮只在自己控制的 demo repo 和 branch 执行，沿用 A2 的 [`review-changes` Skill](A2-cli-workflow.zh-Hans.md#cli-6)。

成功标准不是“几分钟内完成”，而是 workflow 成功结束，并通过 PR comment、job summary 或 artifact 留下可阅读的结果。

<details markdown="1">
<summary>展开 CLI-10 的安全设置与验证步骤</summary>

1. 根据供应商的官方示例建立 workflow，不要复制来源不明的 YAML。
2. 把 API key 放入 GitHub Actions secret。不要写进 workflow、prompt、repo 或 log。
3. `GITHUB_TOKEN` 从 `contents: read` 起步。只有需要发布 PR comment 时，才给该 job 增加必要的 pull-request 权限。
4. Codex 的只读工作使用当前官方 action 支持的 `permission-profile: ":read-only"`；不要同时设置互斥的 legacy sandbox 字段。Claude Code 依据官方 action 的 permissions／allowed tools 限制可用能力。
5. prompt 只要求读取 diff、列出问题、输出 `PASS` 或具体建议。明确写出：不得 edit、commit、push、merge、deploy 或发送额外消息。
6. 先使用自己创建的 same-repo test branch。不要使用 `pull_request_target` checkout 不可信的 PR code；这可能让不可信内容接触 secrets 或写入权限。
7. 检查 Actions log、review 结果和 repo diff。任何 secret 泄露迹象都要立即删除 log、撤销并轮换 secret。

GitHub 建议 production workflow 把第三方 Action pin 到完整 commit SHA，因为 tag 可能移动。官方文档中的 `@v1`／`@v5` 适合辨认产品版本；正式使用时再查证并固定当时可信的完整 SHA。

**费用提醒：** 设置 job timeout 和 concurrency，避免卡住或重复触发。模型 API、供应商方案和 GitHub Actions minutes 要分开看。
</details>

<a id="cli-11"></a>
### 动手练习 CLI-11：看一次运行的收据

**成果：** 你留下 provider／model、input usage、output usage、时间和结果；拿不到的字段会清楚写“未确认”，不会猜。

先分清你用的是订阅方案，还是按 API usage 计费。如果官方提供 token 和单价，成本才使用这个算式：

`input tokens × input price + output tokens × output price`

<details markdown="1">
<summary>展开 CLI-11 的记录卡、停止规则与 observability</summary>

先用一个小 task 填这张卡：

| 字段 | 要记录什么 |
|---|---|
| Task | 这次请 agent 做什么 |
| Provider／model | 实际使用的供应商和型号；拿不到就写未确认 |
| Usage | input／output usage；不要只写模糊的“总 token” |
| 时间 | workflow 或 CLI 显示的实际耗时 |
| 结果 | `PASS`、问题清单或失败原因 |
| 成本 | 只有能对上官方单价时才计算；否则写计费方式或未确认 |

再设置一个工具真正支持的停止规则，例如 job timeout、最大重试、provider spend limit，或每次进入付费步骤前人工确认。不要创建工具不会读取的设置来制造安全感。

要比较多次运行时，可以选择 [Langfuse](https://github.com/langfuse/langfuse)、[Phoenix](https://github.com/Arize-ai/phoenix)、[Helicone](https://github.com/Helicone/helicone) 或 [promptfoo](https://github.com/promptfoo/promptfoo)。先确认数据会发送到哪里、是否包含原始 prompt／code／PII，再决定能不能接入。

Prompt caching 的 TTL、资格和价格因 provider／model 而异。Anthropic 当前文档同时提供默认 5 分钟和可选 1 小时 TTL；把它当作要查询的产品设置，不要当成所有 CLI 的固定规则。
</details>

<a id="cli-12"></a>
### 动手练习 CLI-12：安全地把 Skill 交给队友

**成果：** 第二个干净的 demo repo 能找到 `review-changes` Skill；运行后没有非预期修改。

把 A2 的 `review-changes` Skill 放进可版本控制的 team repo，附上四件事：安装位置、需要的权限、测试方法、移除方法。Claude Code 可以再按照官方 plugin 格式打包；其他 CLI 按各自的 Skill 文档安装。

<details markdown="1">
<summary>展开 CLI-12 的分享、安装与撤销步骤</summary>

1. 分享前读完 `SKILL.md` 和附带的 scripts，确认没有下载陌生程序、读取 secrets 或改变外部系统。
2. 保留 plugin 根目录的 `skills/review-changes/SKILL.md`；不要把项目自己的 `CLAUDE.md`、`AGENTS.md` 或 secrets 一起打包。
3. 在第二个干净的 demo repo 中按照工具文档安装。Claude Code 可以参考 [Plugins 文档](https://code.claude.com/docs/en/plugins)和 [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official)。
4. 做一个小的文档 diff，运行 Skill，再用 `git status --short` 确认它只 review、没有修改文件。
5. 记录版本或 commit SHA。更新前先看 diff；不再使用时，按照文档移除 plugin／Skill，并确认 agent 找不到它。

Skill 的核心意思可以共用，但文件夹、权限、frontmatter 和安装方式不一定相同。不要把某一家工具的 plugin 格式说成所有 CLI 都通用。

**费用提醒：** 分享文件本身通常不收模型费用，但每位队友运行 Skill 时可能使用自己的订阅或 API 额度。
</details>

## 只记住这个 production 安全循环

`圈定范围 → 只读运行 → 留下记录 → 人工判断 → 能够恢复`

如果没有范围、证据或恢复方法，就先不要提高权限。这比记住很多工具名称更重要。

### 📋 Playbook 4：派遣 subagent 跑独立任务

**成果：** 先列出当前工具真正提供哪些 agent，再把独立、可验证的工作交出去；不要假设每台电脑都有同名 agent。

<details markdown="1">
<summary>展开 Playbook 4 与其余六个进阶 playbook</summary>

**Playbook 4 — subagent：** subagent 是主 session 派出的独立小帮手。Claude Code 目前有 `Explore`、`Plan`、`general-purpose` 等 built-in subagent；可用清单仍会受版本、session 和设置影响。`code-reviewer` 是官方文档提供的**自定义示例**，不是每个安装都固定存在的内置 agent。先运行工具的 agent list，再选择 read-only agent 或创建受限 reviewer。

其余情况只记一个动作，理论放在 [Stage 7.5](../../stages/07.5-advanced-agentic-concepts.zh-Hans.md)：

- **范围不清：** 明确写出可动和不可动的路径，先要求计划，不先改文件。
- **多人／多 agent 并行：** 分开 ownership 和 commit，最后再整合；不要同时修改同一批文件。
- **Review agent 输出：** reviewer 只提供证据，不取代测试、branch protection 或人类判断。
- **在 CI 运行 agent：** 从只读和可信 trigger 开始；模型 fallback 必须明确设置并重新验证，不能偷偷切换。
- **控制成本：** 使用实际 usage、timeout、重试和 provider limit；拿不到数据就说拿不到。
- **防止规则 drift：** 故意做一个安全的小失败，确认 gate 确实会拦住；规则文字本身不是证据。

延伸阅读：[`resources/subagent-cookbook.zh-Hans.md`](../../resources/subagent-cookbook.zh-Hans.md)和 [Stage 5.5](../../stages/05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能)。这些页面之后会在自己的 layer 重新查核；使用 agent 名称前，仍以你当下的官方文档和实际清单为准。
</details>

## 🎯 精选 Projects

推荐度是本学习地图的编辑建议，不是 GitHub stars。`⭐⭐⭐⭐⭐` 表示这条学习路径的必读／必做入口；它不代表工具永远安全，也不代表 production 可以跳过自己的 threat model。

<details markdown="1">
<summary>展开完整学习资源表（18 项，查核于 2026-08-27 UTC）</summary>

<table>
<thead>
<tr><th scope="col">类型</th><th scope="col">资源</th><th scope="col">先看什么</th><th scope="col">何时使用</th><th scope="col">推荐度</th><th scope="col">来源</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">安全连接 MCP</th><td>MCP Connect to local servers</td><td>allowed directories 和明确授权</td><td>第一次连接本地 server</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers">官方文档</a></td></tr>
<tr><td>MCP Security Best Practices</td><td>least privilege、scope 和 token handling</td><td>要连接账户或远程服务前</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices">官方文档</a></td></tr>
<tr><td><code>github/github-mcp-server</code></td><td><code>--read-only</code>、toolsets 和 tools allow-list</td><td>要读取 GitHub PR／issue</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/github/github-mcp-server">GitHub repo</a></td></tr>
<tr><td><code>modelcontextprotocol/servers</code></td><td>reference implementation 和非 production-ready 警告</td><td>学习协议或阅读示例代码</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/modelcontextprotocol/servers">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">CI 与 PR review</th><td>GitHub Actions Secure Use</td><td>最小权限、不可信输入、pin SHA</td><td>编写任何带 secrets 的 workflow 前</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://docs.github.com/en/actions/reference/security/secure-use">官方文档</a></td></tr>
<tr><td>Claude Code GitHub Actions</td><td>官方 setup、permissions 和 troubleshooting</td><td>使用 Claude Code 运行 CI</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://code.claude.com/docs/en/github-actions">官方文档</a></td></tr>
<tr><td><code>anthropics/claude-code-action</code></td><td>官方示例和 action inputs</td><td>从可执行模板开始</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/anthropics/claude-code-action">GitHub repo</a></td></tr>
<tr><td>Codex GitHub Action</td><td>permission profile、trigger 和输出</td><td>使用 Codex 运行 CI</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://learn.chatgpt.com/docs/github-action">OpenAI 官方文档</a></td></tr>
<tr><td><code>openai/codex-action</code></td><td><code>:read-only</code> 和 safety strategy</td><td>核对最新 inputs 和示例</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/openai/codex-action">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">观察与评估</th><td><code>langfuse/langfuse</code></td><td>traces、usage 和 eval</td><td>想把多次运行放在一起看</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/langfuse/langfuse">GitHub repo</a></td></tr>
<tr><td><code>Arize-ai/phoenix</code></td><td>tracing 和 evaluation</td><td>想用开放源代码观察 AI 系统</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/Arize-ai/phoenix">GitHub repo</a></td></tr>
<tr><td><code>Helicone/helicone</code></td><td>proxy／gateway 的数据流与隐私边界</td><td>想从 gateway 收集 request 记录</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/Helicone/helicone">GitHub repo</a></td></tr>
<tr><td><code>promptfoo/promptfoo</code></td><td>eval cases 和 CI regression</td><td>要比较改动前后是否退步</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/promptfoo/promptfoo">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="3">分享 Skill／plugin</th><td>Claude Code Plugins</td><td>plugin 结构、安装和 marketplace</td><td>要为 Claude Code 打包</td><td>⭐⭐⭐⭐</td><td><a href="https://code.claude.com/docs/en/plugins">官方文档</a></td></tr>
<tr><td><code>anthropics/claude-plugins-official</code></td><td>官方管理的 plugin 目录</td><td>寻找可读的正式示例</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/anthropics/claude-plugins-official">GitHub repo</a></td></tr>
<tr><td><code>obra/superpowers-marketplace</code></td><td>最小 marketplace 外壳</td><td>理解 curator-only 结构</td><td>⭐⭐⭐</td><td><a href="https://github.com/obra/superpowers-marketplace">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">目录与完整示例</th><td><code>wong2/awesome-mcp-servers</code></td><td>先分类，再逐一检查来源和权限</td><td>官方资源没有需要的 server 时</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/wong2/awesome-mcp-servers">GitHub repo</a></td></tr>
<tr><td><code>obra/superpowers</code></td><td>Skill、规则和 workflow 如何组合</td><td>完成最小流程后看完整示例</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/obra/superpowers">GitHub repo</a></td></tr>
</tbody>
</table>

目录只帮你“找到候选项”，不替候选项保证安全。安装任何 MCP、Action、Skill 或 plugin 前，都要再查看 source、权限、最近维护状态和移除方法。
</details>

## ✅ Track A 完成检查

- [ ] MCP 只拿到 demo 文件夹或最小的 read-only toolset。
- [ ] PR workflow 只提出意见，没有 auto-merge、push 或 deploy。
- [ ] secrets 不在 repo、prompt 或 log 中；workflow 使用最小权限。
- [ ] 我能指出一次运行的结果和 usage；拿不到的数据没有乱猜。
- [ ] 队友能在干净的 demo repo 运行 Skill，之后 `git status` 没有非预期修改。

五项都做到，就完成 Track A。接着按目的选择路径：想做应用，回到 [Stage 3](../../stages/03-tool-use-and-hello-agent.zh-Hans.md)；想研究 production 系统，进入 [Stage 7](../../stages/07-multi-agent-production.zh-Hans.md)；想更深入理解 agent 概念，再读 [Stage 7.5](../../stages/07.5-advanced-agentic-concepts.zh-Hans.md)。

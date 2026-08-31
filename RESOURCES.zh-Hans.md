# 相关资源

> [繁體中文](./RESOURCES.md) | **简体中文** | [English](./RESOURCES.en.md)

> [← 返回主路线 README](README.zh-Hans.md)

## 📌 先选你现在要做的事

不用把整份清单读完。先选择你现在要做的事：

| 我现在想要…… | 从这里开始 | 编辑评分 |
|---|---|---|
| 从头学习 AI Agent | [Stage 0](stages/00-foundations.zh-Hans.md) | ⭐⭐⭐⭐⭐ |
| 分清模型怎么学会与怎么被使用 | [模型训练与调整指南](resources/model-training-guide.zh-Hans.md) | ⭐⭐⭐⭐⭐ |
| 查一个不懂的词 | [Glossary](resources/glossary.zh-Hans.md) | ⭐⭐⭐⭐ |
| 选择一个 CLI Agent | [CLI Agents Guide](resources/cli-agents-guide.zh-Hans.md) | ⭐⭐⭐⭐⭐ |
| 把 Agent 接到外部工具 | [MCP / Skills Catalog](resources/mcp-skills-catalog.zh-Hans.md) | ⭐⭐⭐⭐⭐ |
| 跟着步骤做一个小项目 | [Cookbook](resources/cookbook.zh-Hans.md) | ⭐⭐⭐⭐⭐ |

<a id="三个核心用语mcp--skills--plugins"></a>
## 🧩 三个核心词：MCP、Skill、Plugin

**MCP（Model Context Protocol）**：让 AI 应用用共同方法连接外部数据和工具的开放协议。它能做什么仍取决于 server、账号权限和用户批准。

**Skill**：一包可重复使用的做事方法，也可以包含脚本、模板和参考资料。不同产品放置和加载 Skill 的方式可能不同。

**Plugin**：某个 host 提供的安装包，可以一起带入 Skill、命令、hook 或 MCP 设置；Plugin 不是 MCP 规范的一部分。

想亲手做一次，前往 [Stage 5](stages/05-claude-code-ecosystem.zh-Hans.md)。想先分清 App / Connector、CLI Agent 和 MCP Server，查看 [CLI Agents Guide](resources/cli-agents-guide.zh-Hans.md)。

## 📚 五个安全起点

先从官方入口或完整教材开始，再评估社群项目。这里是本项目的编辑评分，不是 GitHub stars。

| 起点 | 先学什么 | 编辑评分 |
|---|---|---|
| [Official MCP Registry](https://registry.modelcontextprotocol.io/) | 找已发布的 MCP Server；安装前仍要检查维护者、权限和来源 | ⭐⭐⭐⭐⭐ |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | 看 MCP 功能如何实现；这是教学用 reference implementations，不等于 production 推荐 | ⭐⭐⭐⭐⭐ |
| [anthropics/skills](https://github.com/anthropics/skills) | 看 Agent Skill 的文件夹、指令和资源如何组合 | ⭐⭐⭐⭐⭐ |
| [github/github-mcp-server](https://github.com/github/github-mcp-server) | 通过官方实现了解 OAuth、工具组和 repository 权限 | ⭐⭐⭐⭐⭐ |
| [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) | 用中文教材系统学习 Agent 原理和实现 | ⭐⭐⭐⭐⭐ |

> ⚠️ **先少给钥匙**：MCP Server 可能读取、创建、发送或删除真实数据。先用只读、最小权限和测试 workspace；write、send、delete 前保留 **Human Approval（人工批准）**。

<a id="daily-tool-integrations"></a>
<a id="接日常工具常用-mcp-server--skill"></a>
## 🔌 常用集成分类

下面直接显示精选项目和官方入口。从你需要的分类开始看；只有更长的补充清单才会收合。

<table class="resource-table">
<thead><tr><th scope="col">分类</th><th scope="col">资源</th><th scope="col">能帮你什么</th><th scope="col">状态 / 限制</th><th scope="col">编辑评分</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">笔记 / 知识库</th><td><a href="https://developers.notion.com/guides/mcp/overview">Notion MCP</a></td><td>搜索、创建和更新 Notion 内容</td><td>官方 hosted MCP；需要用户 OAuth，权限跟随登录用户</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/MarkusPfundstein/mcp-obsidian">MarkusPfundstein/mcp-obsidian</a></td><td>通过 Obsidian REST API 读写 vault</td><td>社群项目；只授予需要的 vault 和写入范围</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://support.google.com/gemininotebook/answer/16164461">Gemini Notebook（旧名 NotebookLM）</a></td><td>用自己的来源做摘要、提问和学习</td><td>Google 服务；地区、账号和功能可用性会变化</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/teng-lin/notebooklm-py">teng-lin/notebooklm-py</a></td><td>用 Python / CLI 操作 Gemini Notebook</td><td>非官方接口；Google 改版时可能失效</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="3">办公文件</th><td><a href="https://github.com/anthropics/skills">anthropics/skills</a></td><td>阅读 Agent Skill 示例与文档工作流</td><td>官方示例；不同 Claude surface 可用的内建 Skill 不完全相同</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/tfriedel/claude-office-skills">tfriedel/claude-office-skills</a></td><td>补充 Office 文件自动化流程</td><td>社群 Skills；写入前先备份文件并核对输出</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://developers.google.com/workspace/guides/configure-mcp-servers">Google Workspace MCP</a></td><td>连接 Gmail、Drive、Docs、Sheets、Slides、Calendar 和 Chat</td><td>官方 <strong>Developer Preview</strong>；每个产品都有专用 server，并遵循 OAuth 2.0 和用户 / 组织治理</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">开发协作</th><td><a href="https://github.com/github/github-mcp-server">GitHub MCP Server</a></td><td>查询和处理 issue、PR 与 repository</td><td>官方 MCP；使用 OAuth 或最小权限 token，高影响写入需人工批准</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/">Atlassian Rovo MCP</a></td><td>搜索或更新 Jira、Confluence 和 Bitbucket 工作</td><td>官方 hosted remote MCP；使用 OAuth 2.1，权限跟随登录用户；写入真实数据前要人工批准</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://linear.app/docs/mcp">Linear MCP</a></td><td>搜索和更新 Linear issue / project</td><td>官方 hosted remote MCP，使用 Streamable HTTP；提供官方只读选项</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://docs.slack.dev/ai/mcp-overview/">Slack MCP</a></td><td>搜索 Slack、发送消息并管理 canvas</td><td>官方 MCP；它不只是读操作，发送或修改内容前要先确认</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">研究工作流</th><td><a href="https://github.com/WenyuChiou/ai-research-skills">WenyuChiou/ai-research-skills</a></td><td>把研究步骤整理成可复用的 Skill</td><td>社群项目；只安装与当前任务有关的 Skill</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/WenyuChiou/research-hub">WenyuChiou/research-hub</a></td><td>连接 Zotero、Obsidian 和研究工作流</td><td>社群 workspace；先检查数据位置、备份和权限</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/WenyuChiou/zotero-skills">WenyuChiou/zotero-skills</a></td><td>用 Skill 整理 Zotero 数据</td><td>社群 Skill；批量修改前先备份 library</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/WenyuChiou/codex-delegate">WenyuChiou/codex-delegate</a></td><td>把范围清楚的重复工作交给另一个 Agent</td><td>社群工具；委派前锁定文件、验收标准和停止条件</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="1">中文生态</th><td><a href="https://github.com/leemysw/feishu-docx">leemysw/feishu-docx</a></td><td>在飞书（Lark）文档和 Markdown 之间转换</td><td>社群工具；先确认文档分享和写入权限</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
</table>

<a id="research-workflow"></a>
<a id="研究工作流本-repo-维护者出品"></a>
<a id="topic-awesome-lists"></a>
<a id="同主题的清单型-awesome-lists"></a>
<details markdown="1">
<summary>展开更多清单、课程和设计工具</summary>

- [MCP Registry](https://registry.modelcontextprotocol.io/)：已发布 Server 的官方 discovery 入口。
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)：按分类浏览社群 Server；安装前自行审查。
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)：Claude Code 社群资源。
- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)：Agent Skills 社群清单。
- [Canva MCP](https://www.canva.dev/docs/mcp/)：官方 remote MCP；功能、方案和权限取决于账号，不写固定工具数。
- [课程清单](resources/courses.zh-Hans.md)：按学习目标挑课程，不把证书当成学位。
- [Agent paradigms](resources/agent-paradigms.zh-Hans.md)：用图比较常见 Agent 形态。

</details>

<a id="what-else"></a>
## ✅ 下一站

- 不懂名词：打开 [`resources/glossary.zh-Hans.md`](resources/glossary.zh-Hans.md)。
- 想直接做：打开 [`resources/cookbook.zh-Hans.md`](resources/cookbook.zh-Hans.md)。
- 想了解训练选择：打开 [`resources/model-training-guide.zh-Hans.md`](resources/model-training-guide.zh-Hans.md)。
- 想贡献或翻译：先看 [`resources/style-guide.zh-Hans.md`](resources/style-guide.zh-Hans.md) 和 [`CONTRIBUTING.zh-Hans.md`](CONTRIBUTING.zh-Hans.md)。

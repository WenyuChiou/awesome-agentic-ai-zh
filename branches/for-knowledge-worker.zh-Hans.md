# 知识工作者延伸路线（For Knowledge Workers）

> [繁體中文](./for-knowledge-worker.md) | **简体中文** | [English](./for-knowledge-worker.en.md)

<!-- freshness: canonical=branches/for-knowledge-worker.md; verified_on=2026-08-29; scope=apps,connectors,mcp,workflow-automation,permissions,project-status; max_age_days=90 -->

> [← 回到主路线](../README.zh-Hans.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 后从这里接续。没有开发背景也没关系：先做一次性任务，需要重复时再接工具。

<a id="使用场景办公场景--ai-怎么帮"></a>
## 📌 这条路帮你做什么
把散乱的会议记录、Email、文件与待办，整理成“看得懂、找得到、有人负责”的工作成果。AI 可以帮你先整理；来源、权限与最终决定仍由人负责。

常见工作包括：Email 分流、会议转行动项目、每周报告、产品需求整理、研究摘要与知识库整理。

## 🎯 学习目标
1. 从原文找出决定、负责人、期限与证据，不让 AI 猜空白。
2. 分清一次性聊天、**App／Connector**、**MCP Server** 与 **Workflow Automation**。
3. 先检查数据与权限，再让工具读取或修改公司系统。
4. 让寄信、改数据或建立任务的流程先停在 **Approval Gate**。

## 🧩 九个核心词
- **Source（来源）**：原始 Email、逐字稿、文件或数据列，答案要能指回它。
- **Action Item（行动项目）**：有人要完成的一件事，写清做什么、谁负责、何时完成。
- **Knowledge Base（知识库）**：把可复用资料放在固定地方，让人和工具找得到。
- **Private Data（私人数据）**：公司、客户、员工或个人数据；没有政策和权限前不要交给新工具。
- **Human Review（人工审查）**：人对照 Source，检查内容、语气、收件人和缺漏，再决定能否使用。
- **App／Connector（服务内连接器）**：AI 服务连接 Gmail、Drive、Slack 等来源的桥。ChatGPT 已把 Connector 改称 App；其他服务仍可能使用 Connector。
- **MCP Server（MCP 服务器）**：按 MCP 规范把数据或工具交给兼容 client 的服务，不是 ChatGPT App，也不代表公司已核准。
- **Workflow Automation（工作流自动化）**：看到 trigger 后按固定步骤执行 action。
- **Approval Gate（人工核准关卡）**：流程暂停，等人确认后才寄信、发帖、改数据或删除内容。

**三者不要混在一起：App／Connector 是服务里的桥；MCP Server 是协议端点；Workflow Automation 是会反复执行 trigger、条件与 action 的流程。** 同一产品可以同时包含它们，但名称不能互换。

## 🛠 第一个练习：把会议记录变成可核对的行动表
只用 fictional（虚构）数据，不要放 **Private Data**：
```text
你是会议整理助手。只能使用下方会议记录，不要补猜没有写出的名字或日期。
请输出 Markdown 表格，字段固定为：
Decision | Action Item | Owner | Due date | Source sentence | Needs confirmation
规则：
1. 每一列都抄一小段 Source sentence，让我能回头核对。
2. Owner 或 Due date 不清楚时填“未知”，并在 Needs confirmation 填“是”。
3. 不要寄出、贴到群组或写回任何系统，只产生草稿。
4. 最后加入 Human Review 清单：来源、负责人、期限、敏感数据、收件人。
fictional meeting note：“团队决定周五先发布说明页。小林会整理常见问题，但没有写期限。客服主管要在 9 月 3 日前确认回复范本。是否寄信给全部客户，会议后再决定。”
```
逐句对照 Source sentence；若 AI 补出期限或寄信决定，就退回修改，这就是 **Human Review**。

<a id="层级建议"></a>
## 📚 先选一个入口
| 你的需求 | 先用什么 | 何时升级 |
|---|---|---|
| 偶尔整理公开或已核准的文字 | **一次性聊天** | 同一件事开始反复做时 |
| 从公司 Gmail、Drive、Slack 或 Microsoft 365 找来源 | 组织核准的 **App／Connector** | 现成连接器做不到且管理员同意自定义连接时 |
| 每次新 Email／表单都跑相同步骤 | **Workflow Automation** | 测试数据跑通后加入 Approval Gate |

不要因为看见 MCP 就先安装 MCP。先问：“现有服务里的 App／Connector 能不能安全完成？”只有需要自定义工具或跨 client 复用时，才进入 [Stage 5.2 — MCP 基础](../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础)。

<a id="阅读"></a>
## 📖 必读
1. [OpenAI — Apps in ChatGPT](https://help.openai.com/en/articles/11487775-connectors-in)：认识 App 能搜索、同步与执行哪些动作，以及方案、地区与管理员限制。
2. [Anthropic — Skills、Connectors 与 Plugins 目录](https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory)：先分清三种东西，不把安装当成安全核准。
3. [Google — Gemini Connected Apps](https://support.google.com/gemini/answer/14959807?co=GENIE.Platform%3DDesktop&hl=en)：确认管理员、账号与 Source 限制，并核对可能过时的回答。
4. [Microsoft — Understand Copilot connectors](https://support.microsoft.com/en-us/microsoft-365-copilot/understand-copilot-connectors)：确认 connector 只会看到用户原本有权限的内容。
5. [Model Context Protocol — Registry](https://modelcontextprotocol.io/registry/about)：Registry 目前是 Preview；metadata 与 namespace 验证不是代码安全审查。
6. [Zapier — workflow quick start](https://help.zapier.com/hc/en-us/articles/22234847450893-Zap-workflows-quick-start-guide)：用 trigger、action、测试与发布理解自动化的基本形状。

<a id="精选-projects"></a>
## ⭐ 精选工具、项目与官方入口
星星是本项目的教学适配评分，不是 GitHub stars。云服务先问管理员；自托管工具仍要处理更新、备份、权限与数据流。

<small>数据核查：2026-08-29 UTC</small>

<a id="工作流工具"></a><strong>工作流工具：</strong>重复工作才需要，第一版停在草稿或 Approval Gate。<br>
<a id="知识工作者-skills"></a><strong>知识工作者 Skills：</strong>Skill 是可复用做法，不会自动取得公司系统权限。<br>
<a id="知识管理--个人-ai"></a><strong>知识管理／个人 AI：</strong>自托管不等于数据一定留在本机。<br>
<a id="对知识工作者有用的-mcp-server"></a><strong>MCP Server：</strong>使用前检查来源、代码、权限、凭证和 action。

<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="资源表（分类、用途与限制）">
<table><thead><tr><th scope="col">类型</th><th scope="col">资源、用途与限制</th></tr></thead>
<tbody><tr><th scope="rowgroup" rowspan="4">AI 工作空间与组织内 App</th><td><p data-field="entry"><strong><a href="https://help.openai.com/en/articles/11487775-connectors-in">ChatGPT Apps</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">搜索来源或执行允许的动作</p><p data-field="status">商业；商业云服务</p><p data-field="limits">方案、地区与管理员决定功能；外部动作保留人工确认</p></td></tr><tr><td><p data-field="entry"><strong><a href="https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory">Claude directory</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">寻找 Skills、Connectors 与 Plugins</p><p data-field="status">商业；商业云服务</p><p data-field="limits">三者用途不同；组织数据先由管理员核准</p></td></tr><tr><td><p data-field="entry"><strong><a href="https://support.google.com/gemini/answer/14959807?co=GENIE.Platform%3DDesktop&hl=en">Gemini Connected Apps</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">使用 Gmail、Drive、Calendar 等来源</p><p data-field="status">商业；商业云服务</p><p data-field="limits">取决于账号与管理员；回答要回到来源核对</p></td></tr><tr><td><p data-field="entry"><strong><a href="https://support.microsoft.com/en-us/microsoft-365-copilot/understand-copilot-connectors">Microsoft 365 Copilot connectors</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">搜索 Microsoft 365 与核准的外部内容</p><p data-field="status">商业；商业云服务</p><p data-field="limits">只能看到原本有权限的内容；需要管理员设置</p></td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="4">工作流自动化</th><td><p data-field="entry"><strong><a href="https://github.com/n8n-io/n8n">n8n</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">自托管或云端连接服务与 AI</p><p data-field="status">活跃；Sustainable Use License</p><p data-field="limits">不是 MIT；自架安全、更新、备份与凭证由你负责</p></td></tr><tr><td><p data-field="entry"><strong><a href="https://academy.make.com/courses/FoundationC01?pc=workflow">Make</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">用可视化 scenario 连接云服务</p><p data-field="status">商业；商业云服务</p><p data-field="limits">用测试数据；监控运行量、重试与费用</p></td></tr><tr><td><p data-field="entry"><strong><a href="https://learn.microsoft.com/en-us/training/powerplatform/power-automate">Power Automate</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">在 Microsoft 生态建立 trigger 与 action</p><p data-field="status">商业；商业云服务</p><p data-field="limits">方案、connector 与数据政策由管理员控制</p></td></tr><tr><td><p data-field="entry"><strong><a href="https://help.zapier.com/hc/en-us/articles/22234847450893-Zap-workflows-quick-start-guide">Zapier</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">快速建立云端 App 间的重复流程</p><p data-field="status">商业；商业云服务</p><p data-field="limits">发布前逐步测试；写回 trigger 来源可能造成无限循环</p></td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="2">可视化 AI builder</th><td><p data-field="entry"><strong><a href="https://github.com/langflow-ai/langflow">Langflow</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">把 AI、数据与工具流程画成节点</p><p data-field="status">活跃；MIT</p><p data-field="limits">Demo 能跑不等于 production 安全；仍需 auth、secret 与监控</p></td></tr><tr><td><p data-field="entry"><strong><a href="https://github.com/langgenius/dify">Dify</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">用界面建立 AI workflow、知识库与应用</p><p data-field="status">活跃；修改版 Apache-2.0</p><p data-field="limits">多租户与移除品牌有额外商用条件</p></td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="3">知识工作空间</th><td><p data-field="entry"><strong><a href="https://github.com/khoj-ai/khoj">Khoj</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">自托管个人知识助手与文档问答</p><p data-field="status">活跃；AGPL-3.0</p><p data-field="limits">确认 AGPL 与数据设置；自托管后仍要管理模型与备份</p></td></tr><tr><td><p data-field="entry"><strong><a href="https://github.com/lobehub/lobehub">LobeHub</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">部署聊天、知识库与团队 AI workspace</p><p data-field="status">活跃；LobeHub Community License</p><p data-field="limits">开发和分发衍生作品前确认商业授权</p></td></tr><tr><td><p data-field="entry"><strong><a href="https://github.com/Mintplex-Labs/anything-llm">AnythingLLM</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">自托管文档问答、workspace 与 agent</p><p data-field="status">活跃；MIT</p><p data-field="limits">数据是否外发取决于模型供应商、embedder 与 connector 设置</p></td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="2">Skill 与协议入口</th><td><p data-field="entry"><strong><a href="https://github.com/obra/superpowers">obra/superpowers</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">把头脑风暴、规划与检查做成可复用 Skill</p><p data-field="status">活跃；MIT</p><p data-field="limits">不是公司的 Approval Gate，需改成自己的规则</p></td></tr><tr><td><p data-field="entry"><strong><a href="https://modelcontextprotocol.io/registry/about">官方 MCP Registry</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">查询公开 MCP Server 的标准 metadata</p><p data-field="status">Preview；官方 metadata 服务</p><p data-field="limits">namespace 验证不是安全审查，也不是推荐</p></td></tr></tbody></table>
</div>

<a id="可以建的流程按使用频率"></a>
<details markdown="1"><summary>🧪 展开：进阶办公流程与产品经理用法</summary>
| 工作 | 安全的第一版 | 之后再自动化 |
|---|---|---|
| Email 分流 | 去标识测试信，只生成分类与回信草稿 | 管理员核准 inbox；寄出前保留 Approval Gate |
| 会议 → Action Item | 逐字稿生成可回查 Source sentence 的表格 | 写入 task 系统前确认 Owner 与 Due date |
| Weekly report | 人工提供核准指标 | 保留来源链接与发送前审查 |
| 产品需求 | 将虚构 feedback 分成问题、证据、假设、下一步 | 连接工单前限制项目、字段与 action |
| Knowledge Base | 先对少量文件做分类草稿 | 批量改标签前备份并抽查 |
</details>
<details markdown="1"><summary>🔐 展开：账号、数据、权限与费用检查</summary>
- 询问组织是否核准工具、账号、地区和数据用途。
- 只开放工作所需的最小权限；读写分开核准。
- Secret 放 credential store 或环境变量，不贴进 prompt、文件或截图。
- 用虚构或去标识数据测试；高风险 action 保留 Approval Gate。
- 查看方案、运行次数、模型与存储费用并设置预算提醒；不用时停止 workflow、撤销连接、删除测试数据。
</details>
<details markdown="1"><summary>🧯 展开：替代方案与排错</summary>
- 找不到资料：先确认能否直接打开 Source，再查账号、日期、同步与管理员设置。
- 重复建任务：检查 action 是否再次触发自身，加入唯一 ID 或去重条件。
- AI 补猜 Owner／Due date：要求每行附 Source sentence，缺资料就填 Needs confirmation。
- 不确定要不要 MCP：先用服务内 App／Connector。
- 自托管太重：先用组织核准的云服务；自托管不是隐私捷径。
</details>

## ✅ 完成检查与下一站
- [ ] 我能从 fictional 会议记录做 Decision／Action Item 表，并逐行核对 Source sentence。
- [ ] 我不会把 App／Connector、MCP Server 与 Workflow Automation 当成同一件事。
- [ ] 我知道 Private Data 先看政策与权限；写入外部系统的 action 要有 Approval Gate。
- [ ] 我已选一个入口，不会一次安装所有工具。

下一步：自定义连接看 [Stage 5.2 — MCP](../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础)；长流程看 [Stage 7](../stages/07-multi-agent-production.zh-Hans.md)；写或审查代码走[开发者路线](./for-developer.zh-Hans.md)。

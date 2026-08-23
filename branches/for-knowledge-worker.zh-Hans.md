# 知识工作者延伸路线（For Knowledge Workers）

> [繁體中文](./for-knowledge-worker.md) | **简体中文** | [English](./for-knowledge-worker.en.md)

> 🚀 **完全没有开发背景？** 多数知识工作者可以直接从 Claude.ai / Claude Desktop 开始、**不需要任何 setup**。只有当你要接 MCP server（如 Gmail / Notion）或用 CLI 自动化时，才需要看 [`resources/setup-guide.zh-Hans.md` A-D](../resources/setup-guide.zh-Hans.md)（30-45 分钟从零）。

> [← 回主路线 README](../README.zh-Hans.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 后从这里接续。把 agentic AI 应用到办公室 / 知识工作上。

## 使用场景（办公场景 × AI 怎么帮）

下表把知识工作者一天会遇到的 7 个场景拆开——多数场景在 Claude Desktop + MCP（Tier 1）就能搞定：

| 场景 | 你常遇到的痛点 | AI 能帮的部分 | 推荐工具 |
|---|---|---|---|
| **Email 分流** | 每天 100 封看不完、优先顺序错 | 分类 + 草拟回信让你 review | Claude Desktop + Gmail MCP |
| **会议 → 行动项目** | 听完 30 分钟忘一半、action item 没记 | 逐字稿 → 主要决策 + 行动项目 | Otter / Zoom 逐字稿 + Claude |
| **跨工具报告集成** | Slack / Gmail / Notion 各一块、要手动拉 | 自动拉指标 + 整合 + email summary | n8n / Make / Langflow |
| **研究 / 市场情报** | 不知道问什么问题、不知道该信谁 | 多源搜索 + 交叉验证 + 备忘录 | Perplexity + Claude |
| **Slack / 消息** | 拿捏不准语气、敏感场景 | 改写 + 调语气 + 多版本 | Claude.ai |
| **Notion / 知识库整理** | 杂乱、没架构、找不到旧笔记 | 重 tag + 分类 + 自动摘要 | Claude Desktop + Notion MCP |
| **文件 / 提案草稿** | spec / proposal 卡关 | 大纲 → 段落 → 润色 | Claude.ai |

> 💡 **MCP 是知识工作者的关键**：第一次接触 MCP？看 [Stage 5.2 — MCP 基础](../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础)；想知道有哪些 MCP server → [`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md)。

## 精选 Projects

> 💡 **想把 AI agent 接到 Notion / Gmail / Outlook / Slack / Excel / 飞书？**（例：把 Gmail 来信自动整理成 Notion 待办）81+ 个常用办公集成工具表见 [`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md)（按使用场景分类）。下面这节保留 workflow / 集成平台级的工具。

### 工作流工具

#### [n8n](https://github.com/n8n-io/n8n) ⭐⭐⭐⭐
可自架的工作流自动化平台，内置 AI 集成，采用可视化节点式编辑器。

**适合谁**：要把多个 SaaS 工具串起来时（Slack + Gmail + Notion + AI）。

---

#### [Make.com](https://www.make.com/)（前身为 Integromat）
云端代管的工作流自动化平台，AI 集成节点功能完整。

---

### 知识工作者 Skills

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐

头脑风暴、规划、决策类的 skill。

---

### 知识管理 / 个人 AI

#### [khoj-ai/khoj](https://github.com/khoj-ai/khoj) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 36k+ |
| License | AGPL-3.0 |

**教什么**：自架的“第二大脑”——可以跟 web + 本地文件对话、排程自动化、自定义 agent。

**适合谁**：想自架个人知识库 + AI assistant 的人。

**备注**：AGPL-3.0 license（传染性开源）。

---

#### [lobehub/lobe-chat](https://github.com/lobehub/lobe-chat) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 81k+ |
| License | LobeHub Community License（基于 Apache-2.0 + 商用附加条款） |

**教什么**：可部署的多 agent 聊天平台——含 plugin marketplace、知识库、团队协作。可自架的 AI workspace 代表选项之一。

**适合谁**：想找可自架的协作 chat workspace。

**备注**：商用使用需确认 LobeHub Community License 的附加条款。

---

#### [langflow-ai/langflow](https://github.com/langflow-ai/langflow) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 147k+ |
| License | MIT |

**教什么**：可视化 AI agent 设计平台——适合把客服、报告整理、资料查询这类流程画成节点。比 n8n 更专注于 agent 设计（n8n 是泛用工作流）。API / MCP server 部署是进阶备注，不必一开始就学。

**适合谁**：宁可拉节点不写 Python 的知识工作者，或要设计 agent 跟团队沟通流程的人。

---

#### [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 64k+ |
| License | MIT |

**教什么**：all-in-one 的私有 RAG 工作平台——上传文件、建 agent、相容 MCP、预设 on-device。**NotebookLM 的私有 self-hosted 替代方案**。

**适合谁**：知识工作者要私有部署、类 NotebookLM 的工具，避免把数据送到云端。

---

### 对知识工作者有用的 MCP Server

#### 通讯类 MCP server ⭐⭐⭐⭐
Slack / Gmail / Discord 等。Anthropic 原本维护的 reference server 已于 2025 年重整；目前由社群维护的 server 集中在 [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers#communication) 跟 [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers)，要找最新的 Slack / Gmail / Drive / Calendar MCP server 可以从这两个清单翻找。

---

## 可以建的流程（按使用频率）

| 频率 | 流程 | 怎么做（≤ 3 步） | 推荐工具 | 适合谁 |
|---|---|---|---|---|
| **每天** | Email 分流 | (1) 扫 inbox<br>(2) 分类成“立即 / 今天 / 这周 / 不用回”<br>(3) 草拟回信让你 review | Claude Desktop + Gmail MCP | 全知识工作者 |
| **每次会议** | 会议 → 行动项目 | (1) 逐字稿（Otter / Zoom）<br>(2) Claude 抓“主要决策 + 行动项目”<br>(3) 指派 + Slack / email 公告 | Claude.ai + 逐字稿工具 | 主管 / PM |
| **每周** | 跨工具报告 | (1) 从 N 个工具拉指标<br>(2) Claude / n8n 整理<br>(3) email summary 寄出 | n8n / Make / Langflow | 要定期 update 老板的人 |
| **不定期** | 研究 / 市场情报 | (1) 想清楚问题<br>(2) 多来源搜索 + 交叉验证<br>(3) 写成 1-2 页备忘录 | Perplexity + Claude | 分析 / 策略职 |
| **不定期** | Notion / 知识库重整 | (1) 把散落笔记贴进 Claude<br>(2) 请它重新 tag + 分类<br>(3) 输出 Notion 结构化格式 | Claude Desktop + Notion MCP | 有 Notion / Obsidian 习惯的人 |

> 💡 **新手起手式**：先把“每天 Email 分流”做一个月，养成“inbox 开 Claude”的习惯，再加其他流程。一次装太多会养不起来。

## 层级建议

下表是建议的进阶路径：

| Tier | 工具 | 适合谁 | 学习成本 |
|---|---|---|---|
| **Tier 0** | Claude.ai / ChatGPT / Gemini / Perplexity（网页版） | 大多数知识工作者从这里开始 | 0（会用浏览器就行） |
| **Tier 1** | Claude Desktop + MCP（Gmail / Notion / 日历） | 要对本机 / 云端文件重复跑流程 | 半天装好 |
| **Tier 2** | n8n / Make / Langflow（自动化平台） | 要把多个 SaaS 工具串起来、不写 code | 1 周 setup |
| **Tier 3** | Claude Code / Codex / 自己写 Python | 有 dev 背景或团队有 dev 支援、要做能上线部署的成果 | 数周、跟 Track A 重叠 |

**Tier 3+（CLI / SDK）对多数知识工作者任务来说太重**——不要被别人怂恿过去。多数人停在 Tier 1-2 就够。

## 阅读

- [How I Turned Claude Code Into My Personal AI Agent OS](https://aimaker.substack.com/p/how-i-turned-claude-code-into-personal-ai-agent-operating-system-for-writing-research-complete-guide) — 知识工作者个案研究
- [**Anthropic — The Founder's Playbook**](https://claude.com/blog/the-founders-playbook) — Anthropic 2026-05-14 发布的 35 页 startup 指南;Idea / MVP / Launch / Scale 四阶段对应到 2026 AI capability

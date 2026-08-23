# 相关资源

> [繁體中文](./RESOURCES.md) | **简体中文** | [English](./RESOURCES.en.md)

> [← 返回主路线 README](README.zh-Hans.md)

这份文件集中放：用语说明、常用 MCP / Skill 集成 highlight、同主题 awesome list、中文社群资源。从主 README 抽出避免主页过长。

> 💡 **不懂某个词**（LLM、agent、RAG、token、向量数据库⋯）→ [`resources/glossary.zh-Hans.md`](resources/glossary.zh-Hans.md)（用语小词典，30 多个词每个 30-80 字解释）
>
> 🍳 **想动手做但不知怎么开始**（写 Skill / 写 MCP server / 接 Word / 接 NotebookLM / 接 Zotero / 接本机 LLM）→ [`resources/cookbook.zh-Hans.md`](resources/cookbook.zh-Hans.md)（6 个 step-by-step recipe，每个 30-50 分钟做完）

---

## 三个核心用语：MCP / Skills / Plugins

主 README 跟各 stage 会频繁提到这三个 Claude Code 生态的关键词，先快速说明：

- **MCP（Model Context Protocol）** — Anthropic 推的开放协议，让任何 LLM host（Claude Code、其他 IDE、自写 agent）都能用同一套接口去调用外部 tool server（文件、DB、API、自家系统）。把它想成“LLM 的 USB 接口”。详见 [Stage 5.2](stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础)。
- **Skills** — Claude Code 的“行为包”。一个 Skill 就是一份 `SKILL.md`，描述“在什么场景要做什么、可以调用哪些 MCP tool”。写好之后 Claude Code 会自动 discover。详见 [Stage 5.3](stages/05-claude-code-ecosystem.zh-Hans.md#53--skillsclaude-code-的行为层-claude-code-生态最关键的一层)。
- **Plugins / Marketplaces** — 把 Skills、slash commands、hooks、MCP 设置打包成一个发布单位给 team 或社群安装。Marketplace 就是 plugin 的 catalog。详见 [Stage 5.4](stages/05-claude-code-ecosystem.zh-Hans.md#54--plugins-与-marketplaces)。

对应的 **动手练习都在 [Stage 5](stages/05-claude-code-ecosystem.zh-Hans.md)，Track A 的 [A3](tracks/cli/A3-cli-production.zh-Hans.md) 也会用到。

---

## 接日常工具：常用 MCP server / Skill

把 Claude Code（或其他 CLI agent）接到你已经在用的 app，省掉手动切换的成本。下面几个是社群 / 官方比较成熟的：

### 笔记 / 知识库

- [**MarkusPfundstein/mcp-obsidian**](https://github.com/MarkusPfundstein/mcp-obsidian) ★ 4.2k+ — 透过 Obsidian REST API plugin 让 LLM 读写你的 Obsidian vault
- [**makenotion/notion-mcp-server**](https://github.com/makenotion/notion-mcp-server) ★ 4.4k+ — Notion **官方** MCP server，可查询／建立 page、database
- [**PleasePrompto/notebooklm-skill**](https://github.com/PleasePrompto/notebooklm-skill) ★ 7.3k+ — NotebookLM Skill（浏览器自动化），用 Claude Code 直接查你 NotebookLM 里的文件，回答带 citation
- [**teng-lin/notebooklm-py**](https://github.com/teng-lin/notebooklm-py) ★ 18k+ — 非官方 NotebookLM Python API + CLI，支持 Claude Code / Codex 等 agent 集成

### 办公文件（Word / Excel / PowerPoint / PDF）

- [**anthropics/skills**](https://github.com/anthropics/skills) ★ 165k+ — Anthropic **官方** Skills 集合，docx / xlsx / pptx / pdf 处理直接内建
- [**tfriedel/claude-office-skills**](https://github.com/tfriedel/claude-office-skills) ★ 800 — 补强版 Office skills（PPTX/DOCX/XLSX/PDF），含自动化 workflow

### Google Workspace（Gmail / Docs / Drive / Calendar）

- [**taylorwilsdon/google_workspace_mcp**](https://github.com/taylorwilsdon/google_workspace_mcp) ★ 2.9k+ — 一个 server 包整套 Google Workspace（Gmail、Calendar、Docs、Sheets、Slides、Drive）

### 开发协作

- [**github/github-mcp-server**](https://github.com/github/github-mcp-server) ★ 31k+ — GitHub **官方** MCP，issue / PR / repo 操作
- [**atlassian/atlassian-mcp-server**](https://github.com/atlassian/atlassian-mcp-server) ★ 908 — Atlassian **官方** Remote MCP（Jira、Confluence）
- [**jerhadf/linear-mcp-server**](https://github.com/jerhadf/linear-mcp-server) ★ 340+ — Linear MCP server
- [**korotovsky/slack-mcp-server**](https://github.com/korotovsky/slack-mcp-server) ★ 1.7k+ — Slack MCP，无 admin 权限也能用

### 研究工作流（本 repo 维护者出品）

- [**WenyuChiou/ai-research-skills**](https://github.com/WenyuChiou/ai-research-skills) ★ 201 — 14 个研究流程 skill，5-plugin marketplace
- [**WenyuChiou/research-hub**](https://github.com/WenyuChiou/research-hub) ★ 46 — Zotero + Obsidian + NotebookLM 集成 workspace
- [**WenyuChiou/zotero-skills**](https://github.com/WenyuChiou/zotero-skills) ★ 45 — Zotero CLI skill
- [**WenyuChiou/codex-delegate**](https://github.com/WenyuChiou/codex-delegate) ★ 62 [**gemini-delegate-skill**](https://github.com/WenyuChiou/gemini-delegate-skill) ★ 34（⚠️ 已封存）— Multi-LLM delegation 对（Gemini lane 建议改用 Gemini CLI 直接做）

### 中文圈常用

- [**leemysw/feishu-docx**](https://github.com/leemysw/feishu-docx) ★ 235 — 飞书（Lark）docs / sheet / bitable ↔ Markdown，含 Claude Skills 支持

> 上面只是 highlight。**完整 81+ 个集成的分类目录**（含数据库、浏览器自动化、Figma、Excalidraw、Cloudflare、Stripe、学术写作 / Multi-LLM delegation 等）在 [`resources/mcp-skills-catalog.zh-Hans.md`](resources/mcp-skills-catalog.zh-Hans.md)。

> 想找更多 MCP server catalog？看 [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) / [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers)（按分类整理）。**Canva** 现有官方 MCP（[canva.dev/docs/mcp](https://www.canva.dev/docs/mcp/)、endpoint `mcp.canva.com`、~32 工具、任何方案可用、支持 Claude / ChatGPT / Cursor / VS Code）。

---

## 同主题的清单型 awesome lists

本 repo **不取代清单型 awesome list——你已经知道在找什么工具时，下面这些查起来更直接：

### MCP 相关

- [**modelcontextprotocol/servers**](https://github.com/modelcontextprotocol/servers) — 官方 MCP reference servers（现有 7 个：everything、fetch、filesystem、git、memory、sequentialthinking、time；github、sqlite 已移到 `servers-archived`）
- [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers) — 社群 MCP server 清单，按分类整理（150+ 个）
- [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers) — 另一份 MCP server 清单

### Claude Code / Skills / Plugins 相关

- [**hesreallyhim/awesome-claude-code**](https://github.com/hesreallyhim/awesome-claude-code) — Claude Code 相关资源清单（整理中）
- [**travisvn/awesome-claude-skills**](https://github.com/travisvn/awesome-claude-skills) — Claude Skills 清单
- [**anthropics/claude-plugins-official**](https://github.com/anthropics/claude-plugins-official) — Anthropic 官方 plugin 范本，要打包自己的 plugin 从这份开始

### 中文圈必看

- [**datawhalechina/hello-agents**](https://github.com/datawhalechina/hello-agents) — Datawhale 系统性 agent 教学（zh-Hans）
- [**WangRongsheng/awesome-LLM-resources**](https://github.com/WangRongsheng/awesome-LLM-resources) — 完整的中文 LLM 资源整理（8.8k+ stars）
- [**AiHubCN/Awesome-Chinese-LLM**](https://github.com/AiHubCN/Awesome-Chinese-LLM) — 中文开源大模型整理
- [**hardness1020/awesome-agent-architecture**](https://github.com/hardness1020/awesome-agent-architecture) — 逐节拆解现代 agent harness（loop engineering、tools、permissions、context、memory、evaluation），以 Claude Code、Hermes Agent 等系统为案例（持续新增），每节附可运行 Python demo（繁中/简中/英文三语）

### 线上课程 / MOOC（带证书对照）

- [**resources/courses.zh-Hans.md**](resources/courses.zh-Hans.md) — 10 门 credible、会发证书的线上 AI agent 课（英文 + 中文），分 tier；并诚实标注完成证书不是学历

---

## 还有什么？

- 主 README：[README.zh-Hans.md](README.zh-Hans.md)
- 完整 MCP/Skill 目录：[resources/mcp-skills-catalog.zh-Hans.md](resources/mcp-skills-catalog.zh-Hans.md)
- CLI agent 比较指南：[resources/cli-agents-guide.zh-Hans.md](resources/cli-agents-guide.zh-Hans.md)
- Style guide / 贡献规范：[resources/style-guide.zh-Hans.md](resources/style-guide.zh-Hans.md)、[CONTRIBUTING.zh-Hans.md](CONTRIBUTING.zh-Hans.md)

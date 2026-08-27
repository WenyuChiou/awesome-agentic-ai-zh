# `resources/` 索引

<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

> 这是本 repo 的 **reference 区**：不在主路线里、需要时再查的补充材料。每份文件都有明确角色，不重复。

---

## 7 份 reference + 各自的“什么时候看”

| 文件 | 角色 | 什么时候看 | 行数 |
|---|---|---|---|
| [`glossary.zh-Hans.md`](glossary.zh-Hans.md) | **30 秒查词典** | 看 stage 内容时遇到 LLM / RAG / token / agent / vector DB / streaming / batch API 不知道什么意思 | ~210 |
| [`cli-agents-guide.zh-Hans.md`](cli-agents-guide.zh-Hans.md) | **CLI agent 身份与选择指南** | 第一次选 CLI agent、不确定哪个工具适合自己的工作方式 | — |
| [`mcp-skills-catalog.zh-Hans.md`](mcp-skills-catalog.zh-Hans.md) | **81+ 个集成 catalog** | 想把 Claude Code 接 Notion / Obsidian / Excel / Postgres / Slack / 等实际工具 | ~775 |
| [`schema-design-cheatsheet.zh-Hans.md`](schema-design-cheatsheet.zh-Hans.md) | **function schema 设计 5 规则 + 5 anti-pattern** | 写 tool schema / MCP server schema / function calling，发现 LLM 选错 tool / 传错参数 | ~159 |
| [`cookbook.zh-Hans.md`](cookbook.zh-Hans.md) | **6 个 step-by-step recipe** | 想 30-50 分钟做出第一个 Skill / MCP server / 接 Office / 接 NotebookLM / 接 Zotero / 接本机 LLM | ~620 |
| [`setup-guide.zh-Hans.md`](setup-guide.zh-Hans.md) | **从零开始的 setup 指南** | 完全没有 dev 背景、第一次申请 API key / 装 Python / 用 Claude Code | ~400 |
| [`style-guide.zh-Hans.md`](style-guide.zh-Hans.md) | **送 PR 前的格式 / 用词规范** | 要对 repo 贡献、写 entry / 翻译 | ~338 |

合计约 ~2500 行 reference。看起来不少，但**每份文件阅读的时机不同**——你不会一次全读，只在对应场景查 30 秒到 45 分钟。

---

## 怎么进来：按“我现在要做什么”分类

### 🆕 我完全没写过 code / 第一次接触 AI agent

→ [`setup-guide.zh-Hans.md`](setup-guide.zh-Hans.md)（30-45 分钟从零装好）

### 🆕 我刚开始学 AI agent

不需要先读任何 reference。**直接从主路线 [README](../README.zh-Hans.md) → [Stage 0](../stages/00-foundations.zh-Hans.md) 开始**。遇到不懂的词回来查 [`glossary.zh-Hans.md`](glossary.zh-Hans.md) 就好。

### 🛠 我要选 CLI agent

→ [`cli-agents-guide.zh-Hans.md`](cli-agents-guide.zh-Hans.md)（CLI 比较 + 按 use case 推荐）

### 🔌 我要把 Claude Code 接 X 工具（Notion / Excel / Postgres 等）

→ [`mcp-skills-catalog.zh-Hans.md`](mcp-skills-catalog.zh-Hans.md)（81+ 个集成分 16 类）

### 🍳 我想动手写第一个 Skill / MCP server / 接 Word 等

→ [`cookbook.zh-Hans.md`](cookbook.zh-Hans.md)（6 个 step-by-step recipe）

### 📐 我写 tool schema 但 LLM 不照我意思做

→ [`schema-design-cheatsheet.zh-Hans.md`](schema-design-cheatsheet.zh-Hans.md)（5 规则 + 5 anti-pattern）

### 📚 我看 stage 内容遇到不懂的词

→ [`glossary.zh-Hans.md`](glossary.zh-Hans.md)（每个词 30-80 字解释 + 哪个 stage 讲细）

### 🤝 我想送 PR / 翻译 / 加新 entry

→ [`style-guide.zh-Hans.md`](style-guide.zh-Hans.md) + [`../CONTRIBUTING.zh-Hans.md`](../CONTRIBUTING.zh-Hans.md)

---

## 重复 / 重叠？

刻意避免重复。每份 reference 跟主路线 / 其他 reference 的关系：

- **glossary** 是“30 秒查”，stage 内容是“3-5 分钟读”，cookbook 是“30-50 分钟做”——三层深度，不重叠。
- **schema-design-cheatsheet** 跟 cookbook 2（写 MCP server）有交集——cheatsheet 讲“**写 schema 的规则**”，cookbook 讲“**怎么把 server 跑起来**”。看哪个取决于你卡在哪。
- **cli-agents-guide** 是 reference table；catalog 是 plug-in tools——两个层级不同。
- **跟 [Hello-Agents](https://github.com/datawhalechina/hello-agents) 的关系**：Hello-Agents 是中文圈最完整的 agent 教材，深度高。我们走的是“**roadmap + curated catalog + 动手 recipe**”的角度，不取代它。Stage 5.3 / cookbook 1 都明确 cross-ref Hello-Agents Extra08“如何写出好的 Skill”当深度补充。

---

## 三语覆盖

| 文件 | zh-TW（canonical） | zh-Hans | English |
|---|---|---|---|
| glossary | ✅ | ✅ | ✅ |
| cli-agents-guide | ✅ | ✅ | ✅ |
| mcp-skills-catalog | ✅ | ✅ | ✅ |
| schema-design-cheatsheet | ✅ | ✅ | ✅ |
| cookbook | ✅ | ✅ | ✅ |
| setup-guide | ✅ | ✅ | ✅ |
| style-guide | ✅ | ✅ | ✅ |

---

## 加新 reference 文件的标准

不是随便加。新文件必须：

1. **不重复既有任何文件的角色**（看上面的“角色”栏）。
2. **解决 main path 解决不了的问题**。如果 Stage X 的内容加 50 行就能 cover，就放 stage 里别开新文件。
3. **预期会被 3 个以上 stage 或 branch cross-ref**。只服务一个 stage 的内容，放那个 stage 就好。

近期考虑过但没加的：

- `cost-calculator-guide.md`：cross-provider 计价。现在 [Stage 1](../stages/01-llm-basics.zh-Hans.md) 有提到，等需求明显再开。
- `troubleshooting-guide.md`：常见错误 runbook。现有资料够应付，等社群反馈多了再开。
- `prompt-patterns-guide.md`：CoT / few-shot 模板库。现在 [Stage 2](../stages/02-prompt-engineering.zh-Hans.md) 有基础内容，深度版等社群 PR。

社群想加可以开 issue 讨论。

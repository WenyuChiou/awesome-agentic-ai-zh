# 路线图 / Roadmap

> [繁體中文](./ROADMAP.md) | **简体中文** | [English](./ROADMAP.en.md)

这份页面只回答两件事：**现在已经能用什么？接下来还要补什么？** 它不是发布日期，也不承诺完成时间。

**状态：** 🟢 正在做／随时可贡献 · 🟡 已知缺口 · 🔵 想法 · ✅ 最近完成

---

<a id="近期想补的缺口"></a>
<a id="进行中--随时可贡献"></a>
<a id="-动手练习覆盖补齐"></a>
<a id="-audience-branch-深化"></a>
<a id="-stage-2--stage-3-2026-freshness-小修"></a>

## 🟢 现在正在做

### 1. 把整站接成同一条路

- 共用基础：`Stage 0 → Stage 1 → Stage 2`
- Track A：`A1 → A2 → Stage 5 → A3 → Stage 8`
- Track B：`Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7 → Stage 7.5 → Stage 8`

Track A 做完 A3 就能开始 Capstone；Stage 8 建议完成，但不影响入场。首页学习地图、文字和测试现在使用同一条路线；以后调整顺序时，三者要一起更新。

### 2. 整理五条角色路径

研究人员、开发者、教师、知识工作者和日常用户都会补上“今天先做什么”。第一个动作留在页面上；完整项目表、替代方案和疑难排解默认收合。核心词和五星编辑推荐度不会消失。

### 3. 整理 setup、courses、cookbook、glossary 和 catalog

- Setup 先帮读者选 Web、Desktop、IDE、CLI 或 API。
- Cookbook 先显示成果、第一个可复制动作和成功条件。
- Glossary 的术语和短定义保持可搜索。
- MCP／Skills catalog 保持可搜索，并增加分类导航与维护状态。

### 4. 持续检查 repository 和易变信息

每周 workflow 检查 canonical GitHub repo、redirect、archive、license metadata、release 和最近活动。较久没 push 只会产生 warning，不会自动删除稳定且仍有教学价值的项目。模型、价格、API 和产品能力仍要回官方文件逐章查证。

---

<a id="基础建设maintainer-进行中"></a>

## ✅ 最近完成

- Stage 0–8 和 A1–A3 已完成第一轮渐进式揭露、核心词、资源表和三语整理。
- Stage 2 保留 zero-shot、one-shot、few-shot、Chain of Thought，并加入三语 Prompt Engineering 概念图。
- Stage 3 用三语图教第一个 Agent Loop；Stage 4 用 framework 教 Workflow Graph；Stage 7 以 Agent Production Engineering 整合 Harness、Loop 与 Graph。Stage 6 重画两条路的 RAG pipeline；Stage 8 补上界面选择与安全检查图。
- Stage 0 有整合练习；Stage 7.5 本来就是 reading map；Stage 8 已有可复制安全练习，独立 end-to-end 范例仍可贡献。
- MkDocs build、mirror／anchor／locale、reader-UX、freshness 和 repository snapshot gate 都已纳入维护流程。

---

## 🟢 很适合贡献的小任务

- 回报过时事实或失效链接，并附官方新来源。
- 给一个练习补上更清楚的“怎么跑”和成功条件。
- 修顺一段英文或简中，但不要改变原意、数字、URL 或安全规则。
- 给 role path 补一个真实情境，写清输入、输出、人工检查和隐私边界。
- 给稳定项目补 status／license／限制；不要只用 stars 或最近 push 日期下结论。

先看 [`CONTRIBUTING.zh-Hans.md`](CONTRIBUTING.zh-Hans.md)；想长期维护一章，再看 [`CONTRIBUTORS.zh-Hans.md`](CONTRIBUTORS.zh-Hans.md)。

---

<a id="想法箱待讨论还没承诺"></a>

## 🔵 还在讨论

- 是否需要第三条 no-code／web-only 正式轨道；日常用户目前可直接走角色路径。
- 是否加入最小视频 walkthrough；需要先衡量字幕、三语同步和维护成本。
- Voice Agent 与 VLA 应放在 Stage 8／研究或开发者延伸，还是需要独立专题页。

想法请开 [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions)；issue 留给缺陷、过时信息或明确的新资源。

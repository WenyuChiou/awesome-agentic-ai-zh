# `resources/` 工具柜

<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

这里像一个工具柜。你卡住时，只拿现在需要的那张说明卡；**不用从第一份读到最后一份**。

## 🧭 你现在卡在哪里？

| 你现在想做什么 | 先打开这一份 |
|---|---|
| 我完全没写过 code，不知道怎么开始 | [`setup-guide.zh-Hans.md`](setup-guide.zh-Hans.md) |
| 我想按完整学习地图开始 | [主页](../README.zh-Hans.md) → [Stage 0](../stages/00-foundations.zh-Hans.md) |
| 我分不清模型怎么学会、怎么被调整、什么时候只是在生成答案 | [`model-training-guide.zh-Hans.md`](model-training-guide.zh-Hans.md) |
| 我看到一个词，但不知道意思 | [查词卡](glossary.zh-Hans.md) |
| 我分不清这四个名字：OpenRouter＝统一模型 API／router；Ollama＝本地模型 runtime；OpenCode／Pi＝coding agent／toolkit | [`cli-agents-guide.zh-Hans.md`](cli-agents-guide.zh-Hans.md) |
| 我想做出第一个操作卡（Skill）、工具接头（MCP server）或文档流程 | [实践食谱](cookbook.zh-Hans.md) |
| 我写了工具说明（tool schema），但模型一直选错工具 | [`schema-design-cheatsheet.zh-Hans.md`](schema-design-cheatsheet.zh-Hans.md) |
| 我想找能接 Notion、Office、数据库或浏览器的工具 | [`mcp-skills-catalog.zh-Hans.md`](mcp-skills-catalog.zh-Hans.md) |
| 我想选一门课，或先看证书有没有用 | [`courses.zh-Hans.md`](courses.zh-Hans.md) |
| 我想知道 agent 是在终端、编辑器、云端还是自己的设备里工作 | [`agent-paradigms.zh-Hans.md`](agent-paradigms.zh-Hans.md) |
| 我想直接复制一个小助手 agent（subagent）派遣范例 | [`subagent-cookbook.zh-Hans.md`](subagent-cookbook.zh-Hans.md) |
| 我想自己设计、组合或排查小助手 agent（subagent） | [`subagent-advanced.zh-Hans.md`](subagent-advanced.zh-Hans.md) |
| 我想替这个项目写内容或提交 PR | [`style-guide.zh-Hans.md`](style-guide.zh-Hans.md) |

## 🧩 先分清五个词

- **Reference（参考资料）**：卡住时回来查的补充资料，不是另一条要从头读完的必修课。
- **Guide（指南）**：带你沿着一条清楚路线做选择，告诉你先做什么、下一步去哪里。
- **Cookbook（食谱）**：像食谱一样给你可以跟着做的完整小范例，目标是先做出成果。
- **Catalog（目录）**：把很多工具放在同一处，方便搜索和比较。
- **Glossary（词典）**：先给短定义，再把你送到讲得更完整的章节。

## 📚 全部 12 份参考资料

同一类型已经合并在左栏。表格全部保持展开，因为读者要先看见有哪些入口。

<table>
<thead><tr><th scope="col">类型</th><th scope="col">文件</th><th scope="col">最适合什么时候看</th><th scope="col">它不负责什么</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">开始与选择</th><td><a href="setup-guide.zh-Hans.md">setup-guide.zh-Hans.md</a></td><td>第一次选择 Web、Desktop、IDE、CLI 或 API</td><td>不取代每个产品的最新官方安装页</td></tr>
<tr><td><a href="glossary.zh-Hans.md">glossary.zh-Hans.md</a></td><td>30 秒查一个名词</td><td>不取代完整章节与实践</td></tr>
<tr><td><a href="cli-agents-guide.zh-Hans.md">cli-agents-guide.zh-Hans.md</a></td><td>分清模型、模型入口（router）、运行环境（runtime）与 coding agent</td><td>不替你自动开放权限或选择付费方案</td></tr>
<tr><td><a href="courses.zh-Hans.md">courses.zh-Hans.md</a></td><td>比较课程、实践深度与证书限制</td><td>不保证证书能换到工作</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">动手与排错</th><td><a href="cookbook.zh-Hans.md">cookbook.zh-Hans.md</a></td><td>制作 Skill、MCP、Office、Gemini Notebook、Zotero 或本地 CLI 工作流</td><td>不把每个主题写成一本长教材</td></tr>
<tr><td><a href="schema-design-cheatsheet.zh-Hans.md">schema-design-cheatsheet.zh-Hans.md</a></td><td>工具选错或参数经常传错</td><td>不教完整 MCP server 安装</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="3">搜索与定位</th><td><a href="model-training-guide.zh-Hans.md">model-training-guide.zh-Hans.md</a></td><td>分清 Pre-training、Post-training、Fine-tuning 与 Inference</td><td>不是从零训练模型的完整课程</td></tr>
<tr><td><a href="mcp-skills-catalog.zh-Hans.md">mcp-skills-catalog.zh-Hans.md</a></td><td>按工作类型寻找工具接头（MCP server）或操作卡（Skill）</td><td>收录不代表零风险或永远可用</td></tr>
<tr><td><a href="agent-paradigms.zh-Hans.md">agent-paradigms.zh-Hans.md</a></td><td>分清 agent 运行在终端、编辑器、云端还是自己的设备</td><td>不是产品排行榜</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Subagent 进阶</th><td><a href="subagent-cookbook.zh-Hans.md">subagent-cookbook.zh-Hans.md</a></td><td>先复制一个小助手 agent 的派遣范例</td><td>不解释全部设计原理</td></tr>
<tr><td><a href="subagent-advanced.zh-Hans.md">subagent-advanced.zh-Hans.md</a></td><td>自己设计、组合与排查小助手 agent</td><td>不适合第一次使用 CLI agent 时先读</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="1">维护项目</th><td><a href="style-guide.zh-Hans.md">style-guide.zh-Hans.md</a></td><td>写 entry、翻译、表格或提交 PR</td><td>不是普通读者的必读内容</td></tr>
</tbody>
</table>

## 🔁 看完要回哪里？

- 第一次学习：回到 [Stage 0](../stages/00-foundations.zh-Hans.md)。
- 想用 CLI 完成工作：回到 [Track A1](../tracks/cli/A1-cli-intro.zh-Hans.md)。
- 想自己写 Agent：回到 [Stage 3](../stages/03-tool-use-and-hello-agent.zh-Hans.md)。
- 只想重新选择入口：回到 [主页](../README.zh-Hans.md)。

## ✅ 30 秒完成检查

- [ ] 我知道现在只要打开哪一份资料。
- [ ] 我没有把 catalog 当成从头读到尾的课本。
- [ ] 我看完后，知道要回主线的哪一站。

<details markdown="1">
<summary>为什么不把 12 份资料合成一本书？</summary>

因为它们解决不同问题。Glossary 是 30 秒查词，Stage 是几分钟建立概念，Cookbook 是跟着做出成果，Catalog 则是需要时搜索工具。全部混成一本书，读者反而更难找到入口。

想读章节长度的中文教材，可以接着看 [Hello-Agents](https://github.com/datawhalechina/hello-agents)。这个项目负责帮你找路，不重写另一套长教材。

</details>

<details markdown="1">
<summary>Maintainer：三语覆盖与新增 reference 的规则</summary>

上表 12 份资料都有繁中、英文与简中版本。新增 reference 前要同时符合：

1. 它有一个现有文件无法取代的工作。
2. 至少三个 stage、track 或 branch 会需要它。
3. 名词、URL、限制与安全规则能保持三语一致。
4. 如果只服务一个章节，就留在那个章节，不另外开文件。

繁中是主版本：zh-TW 是 canonical。先用官方来源核实；找不到时明确写未知，不要猜。不要保存会不断变化的 GitHub stars、固定总数和行数。

提交修改前，再核对 [MCP／Skills catalog](mcp-skills-catalog.zh-Hans.md)、[Cookbook](cookbook.zh-Hans.md)、[style guide](style-guide.zh-Hans.md) 与 [CONTRIBUTING](../CONTRIBUTING.zh-Hans.md)。

</details>

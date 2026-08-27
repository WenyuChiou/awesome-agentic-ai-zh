# A2 — 让 CLI agent 每次都按同一套方法做事

> [繁體中文](./A2-cli-workflow.md) | **简体中文** | [English](./A2-cli-workflow.en.md)

> [← A1 — 安全完成第一个 CLI 任务](A1-cli-intro.zh-Hans.md) · **Track A: CLI Power User** 第 2 站 · [下一站：A3](A3-cli-production.zh-Hans.md)

这一站只解决一个问题：**怎么让 CLI agent 下次进入同一个 repo 时，还记得同一套做事方法？**

你会把每次都要知道的规则写进 **Project instructions**，把经常重复的步骤做成 **Skill**，临时任务则留在 **One-off prompt** 里。这就像把“每天都要重新交代”改成“墙上有守则，工具箱里有操作卡”。

## 🧩 先认识三个核心词

| 核心词 | 它是什么、像什么 | A2 怎么用 | 不是什么 |
|---|---|---|---|
| **Project instructions（项目规则）** | 每次进入工作室都要看的守则 | 放项目用途、禁止事项、测试指令和交付格式 | 不放只用一次的任务或长篇参考资料 |
| **Skill（操作卡）** | 需要时才拿出的可复用操作卡 | 放 review、release、整理文档等重复流程 | 不是每家 CLI 都使用相同路径、权限或 frontmatter |
| **One-off prompt（单次提示）** | 只交代今天这一件事的便签 | 放本次任务、范围、输入和成功条件 | 不用它重复粘贴每次都相同的项目规则 |

## 📌 学习目标

- 用四个字段写出一份短而清楚的项目规则。
- 把重复的 review 流程做成一个只读 Skill。
- 分清哪些内容可以共用，哪些文件名、权限和命令要根据工具调整。

<details markdown="1">
<summary>展开时间、先备条件、环境和费用</summary>

- **时间**：先完成 CLI-5、CLI-6；CLI-7、CLI-8 可以之后再做，不必一次完成。
- **先备条件**：完成 [A1](A1-cli-intro.zh-Hans.md)，会看 `git status`、`git diff`，并有一个不含秘密、可恢复的 demo repo。
- **环境**：选一个主要使用的 CLI agent。Claude Code、Codex、Gemini CLI、OpenCode 的文件名不完全相同，下方有对照。
- **费用**：写项目规则文件和 Skill 不会产生模型费用；请 CLI 测试时可能使用额度或 API token。以当天官方 usage/pricing 页面为准。

还没完成 A1 时，先回去跑一次“只读检查 → 看计划 → 小改动 → `git diff` → 恢复”。
</details>

## 📚 必读

<details markdown="1">
<summary>展开必修阅读和建议顺序</summary>

1. 先看你主要使用的工具的 project-instructions 官方文档：Codex 看 [`AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)、Claude Code 看 [`CLAUDE.md`](https://code.claude.com/docs/en/memory)、Gemini CLI 看 [`GEMINI.md`](https://geminicli.com/docs/cli/gemini-md/)、OpenCode V2 看 [`AGENTS.md`](https://opencode.ai/v2/docs/instructions)。
2. 再看你所用工具的 Skill 文档：[Codex/ChatGPT](https://learn.chatgpt.com/docs/build-skills)、[Claude Code](https://code.claude.com/docs/en/slash-commands)、[Gemini CLI](https://geminicli.com/docs/cli/using-agent-skills/)、[OpenCode V2](https://opencode.ai/v2/docs/skills)。
3. 最后回看 [Stage 2 — Prompt 设计](../../stages/02-prompt-engineering.zh-Hans.md)，把“任务、范围、成功条件”补进单次 prompt。
</details>

<details markdown="1">
<summary>展开四个 CLI 的项目规则文件和 Skill 位置</summary>

官方资料查核日：**2026-08-27 UTC**。

<table>
<thead>
<tr><th scope="col">工具</th><th scope="col">项目规则</th><th scope="col">Project Skill</th><th scope="col">要注意什么</th></tr>
</thead>
<tbody>
<tr><th scope="row">Codex</th><td><code>AGENTS.md</code></td><td><code>.agents/skills/&lt;name&gt;/SKILL.md</code></td><td>规则会按目录分层；较近的规则较晚加载</td></tr>
<tr><th scope="row">Claude Code</th><td><code>CLAUDE.md</code></td><td><code>.claude/skills/&lt;name&gt;/SKILL.md</code></td><td>旧的 <code>.claude/commands/</code> 仍兼容，但新流程优先使用 Skill</td></tr>
<tr><th scope="row">Gemini CLI</th><td><code>GEMINI.md</code></td><td><code>.agents/skills/&lt;name&gt;/SKILL.md</code> 或 <code>.gemini/skills/…</code></td><td>启用 Skill 时会要求同意；不要把秘密放进 Skill</td></tr>
<tr><th scope="row">OpenCode V2</th><td><code>AGENTS.md</code></td><td><code>.agents/skills/&lt;name&gt;/SKILL.md</code> 或 <code>.opencode/skills/…</code></td><td>V2 不使用旧文档所写的 <code>CLAUDE.md</code> fallback</td></tr>
</tbody>
</table>

共同的是“要交代哪些事”；不同的是文件名、搜索位置、权限和额外设置。不要把一个工具的专属功能当成所有 CLI 都有。
</details>

## 🛠 动手练习

<a id="cli-5"></a>
### 动手练习 CLI-5：做一张最小项目规则卡

**成果：** CLI agent 每次进入 repo，都知道这个项目做什么、不能碰什么、怎么验证，以及完成时要回报什么。

先从上方对照表中选出属于你所用工具的项目规则文件，再放入这四件事：

```markdown
# 项目规则

- 用途：这是一个练习用文档 repo。
- 不可做：不要删文件、不要读取秘密、不要自动 commit 或 push。
- 验证：修改后执行 `git diff --check`。
- 回报：说明改了什么、验证结果，以及仍未处理的事。
```

这张卡只放“每次都要知道”的事。长篇教程、API 参考和偶尔才用的流程不要塞进来。

<details markdown="1">
<summary>展开 CLI-5 的建立和验证步骤</summary>

1. 在干净的 demo repo 建立你主要使用的工具的项目规则文件。先执行 `git status --short`，不要覆盖别人的未完成修改。
2. 把上面的四个字段换成这个 demo repo 的真实内容。指令必须可以复制执行；不要写“把格式弄好”这种看不出成功与否的句子。
3. 开一个新的 CLI session，请它只读规则并用自己的话重述。如果它找不到文件，先查官方的文件名和加载范围。
4. 给一个会碰到禁止事项的测试，例如“直接 commit 这个改动”。正确结果是 agent 停下或先询问，而不是自行 commit。
5. 先用 `git status --short -- <规则文件路径>` 看它是旧文件还是新文件。
   - 旧文件：用 `git diff -- <规则文件路径>` 检查。只有确认开始前该文件干净，才用 `git restore -- <规则文件路径>` 恢复。
   - 新文件：Git 会显示 `??`；`git restore` 不能移除它。你可以保留它作为练习成果。如果不要，先核对完整路径，再用文件管理器只删除这一个文件，最后重新运行 `git status --short -- <规则文件路径>`。

没有任何行数能保证规则一定好。只保留会改变行为的内容；某段只在特定任务中使用时，把它移到 Skill 或其他按需文档。
</details>

<a id="cli-6"></a>
### 动手练习 CLI-6：把重复 review 做成 Skill

**成果：** 你能让 agent 执行同一套只读 review，输出 `PASS` 或具体问题，不会自己 commit、push 或部署。

Claude Code 使用 `.claude/skills/review-changes/SKILL.md`；Codex、Gemini CLI、OpenCode 可以使用 `.agents/skills/review-changes/SKILL.md`。建立文件后放入：

```markdown
---
name: review-changes
description: Review the current git diff and report concrete risks. Use when the user asks to review local changes.
---

1. Read `git diff --no-ext-diff HEAD` without changing files.
2. Check for secrets, unsafe commands, broken links, and missing verification.
3. Report `PASS` when no problem is found; otherwise list each problem with its file and reason.
4. Do not edit, commit, push, deploy, or send messages.
```

`name` 是操作卡名称；`description` 告诉 agent 什么时候拿这张卡。正文才是要遵循的步骤。

<details markdown="1">
<summary>展开 CLI-6 的测试、权限和兼容说明</summary>

1. 先完整读完 `SKILL.md`，确认没有下载陌生程序、读取秘密或改变外部系统的步骤。
2. 在 demo repo 做一个小文档改动，但不要 commit。请 agent“review my local changes”，观察它是否找到 Skill；也可以按照工具文档手动启用。
3. 对照 `git diff` 检查回报。测试后执行 `git status --short`，确认 Skill 没有偷偷改文件。
4. 想在多个 CLI 共用时，先共用上面的核心内容，再根据每个工具调整文件夹、权限和工具专属 frontmatter。未知字段可能会被忽略，不要假设每个设置在所有地方都有效。

Claude Code 的 `.claude/commands/<name>.md` 目前仍能建立同名 `/name`，但 Skills 已包含 custom commands，并支持附加文件和按需加载。本教程使用 Skill；只有维护旧项目时才需要理解 legacy command。
</details>

<a id="cli-7"></a>
### 动手练习 CLI-7：把大任务拆成看得见的小步骤

**成果：** 你能把一个可恢复的文档任务拆成“盘点 → 计划 → 修改 → 验证”，每一步都有看得见的结果。

<details markdown="1">
<summary>展开 CLI-7 的比较练习和 multi-agent 延伸</summary>

选一个小任务，例如“给两份 README 补上同一个运行指令”。第一次先请 agent 提计划，不改文件；第二次请它依次盘点两份文件、列出差异、修改、运行 `git diff --check`，最后回报仍未处理的事。

比较两次结果时，只问：有没有漏文件、能不能恢复、验证是否真的执行。不要为了让流程看起来厉害，就把每个小步骤都分派给不同 agent。如果任务需要互相等待、会修改同一批文件，或者你还说不清成功条件，先用单一 agent。

完整的 subagent、agent team、后台工作和审查流程放在 [Stage 5.5](../../stages/05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能)。A2 只练习把工作拆清楚。
</details>

<a id="cli-8"></a>
### 动手练习 CLI-8：做一张 portable prompt 对照卡

**成果：** 你能保留同一个任务核心，并清楚标出换工具时要修改的文件名、权限、命令和启用方式。

<details markdown="1">
<summary>展开 CLI-8 的跨工具测试步骤</summary>

1. 共用核心只写四个字段：任务、范围、禁止事项、成功条件。
2. 在第一个 CLI 的干净 demo repo 中运行一次，记录 CLI 版本、模型/provider、权限设置和 `git diff`。
3. 恢复后再换第二个 CLI。不要让两个会写文件的 session 同时操作同一个目录。
4. 另外记下差异：project-instructions 文件名、Skill 位置、shell/sandbox 权限、工具名称、登录和费用。

“Portable”代表核心意思容易迁移，不代表整段文字和设置可以零修改复制。如果第二个工具没有同名功能，就回到成功条件，选择它真正支持的方法。
</details>

## 🎯 精选 Projects

<details markdown="1">
<summary>展开完整学习资源表（16 条）</summary>

下面按用途分成五组。同一组只显示一次分类栏，避免重复文字把表格撑乱。

<table>
<thead>
<tr><th scope="col">类型</th><th scope="col">资源</th><th scope="col">先看什么</th><th scope="col">适合什么时候使用</th><th scope="col">推荐度</th><th scope="col">来源</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">官方项目规则</th><td>Codex <code>AGENTS.md</code></td><td>分层加载和优先顺序</td><td>为 Codex 编写 repo 规则</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://learn.chatgpt.com/docs/agent-configuration/agents-md">官方文档</a></td></tr>
<tr><td>Claude Code <code>CLAUDE.md</code></td><td>什么时候放规则、什么时候移到 Skill</td><td>为 Claude Code 编写持续规则</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://code.claude.com/docs/en/memory">官方文档</a></td></tr>
<tr><td>Gemini CLI <code>GEMINI.md</code></td><td>目录范围和加载方式</td><td>为 Gemini CLI 放项目 context</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://geminicli.com/docs/cli/gemini-md/">官方文档</a></td></tr>
<tr><td>OpenCode V2 <code>AGENTS.md</code></td><td>V2 的合并和 nested discovery</td><td>为 OpenCode V2 编写规则</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://opencode.ai/v2/docs/instructions">官方文档</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">官方 Skill 文档</th><td>Codex/ChatGPT Build skills</td><td><code>SKILL.md</code> 结构和加载位置</td><td>制作 Codex 可复用流程</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://learn.chatgpt.com/docs/build-skills">官方文档</a></td></tr>
<tr><td>Claude Code Skills</td><td>按需加载、legacy commands、权限</td><td>制作 Claude Code Skill</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://code.claude.com/docs/en/slash-commands">官方文档</a></td></tr>
<tr><td>Gemini CLI Agent Skills</td><td>discovery、安装同意和启用同意</td><td>管理 Gemini CLI Skill</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://geminicli.com/docs/cli/using-agent-skills/">官方文档</a></td></tr>
<tr><td>OpenCode V2 Agent Skills</td><td>支持位置、frontmatter、permission</td><td>制作 OpenCode Skill</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://opencode.ai/v2/docs/skills">官方文档</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">标准和易读范例</th><td>Agent Skills specification</td><td>共用格式的最低要求</td><td>让核心内容更容易跨工具使用</td><td>⭐⭐⭐⭐</td><td><a href="https://agentskills.io/specification">标准</a></td></tr>
<tr><td><code>anthropics/claude-plugins-official</code></td><td>官方 plugin 内的 Skills 和 commands</td><td>查看 Skill 如何被打包分享</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/anthropics/claude-plugins-official">GitHub repo</a></td></tr>
<tr><td><code>mattpocock/skills</code></td><td>工程工作中使用的短 Skill 范例</td><td>比较不同写法</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/mattpocock/skills">GitHub repo</a></td></tr>
<tr><td><code>obra/superpowers</code></td><td>真实 workflow 如何拆成 Skills</td><td>完成第一个 Skill 后再看</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/obra/superpowers">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">索引和 prompt 练习</th><td><code>hesreallyhim/awesome-claude-code</code></td><td>按类型查找 Claude Code 资源</td><td>已经知道需求、想找更多范例时</td><td>⭐⭐⭐</td><td><a href="https://github.com/hesreallyhim/awesome-claude-code">GitHub repo</a></td></tr>
<tr><td><code>anthropics/prompt-eng-interactive-tutorial</code></td><td>一步一步比较 prompt 写法</td><td>CLI-8 的共用核心不清楚时</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/anthropics/prompt-eng-interactive-tutorial">官方 GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Repo context 工具</th><td><code>yamadashy/repomix</code></td><td>生成一次性的 codebase 快照</td><td>需要把 repo 内容整理给 agent 时</td><td>⭐⭐⭐⭐⭐</td><td><a href="https://github.com/yamadashy/repomix">GitHub repo</a></td></tr>
<tr><td><code>langchain-ai/openwiki</code></td><td>建立可持续更新的 repo wiki</td><td>大型 repo 需要按需查文档时</td><td>⭐⭐⭐⭐</td><td><a href="https://github.com/langchain-ai/openwiki">GitHub repo</a></td></tr>
</tbody>
</table>
</details>

## ✅ 进入 A3 前的自我检查

- [ ] 我能用自己的话分清项目规则、Skill、单次 prompt。
- [ ] 我的项目规则卡有用途、禁止事项、验证指令、交付格式，而且 agent 能读到。
- [ ] 我的 review Skill 只读取变更，测试后 `git status --short` 没有多出非预期修改。
- [ ] 我知道“共用核心”不等于“所有 CLI 的文件名和权限都一样”。

四项都做到，就进入 [A3 — 把 CLI agent 接进安全的 production 流程](A3-cli-production.zh-Hans.md)。如果还没做到，先回 demo repo 重跑 CLI-5 或 CLI-6，不必先读完所有补充资料。

<details markdown="1">
<summary>展开常见问题和修正方式</summary>

- **规则写很多，agent 还是漏掉**：先删掉背景故事和重复句，只保留可以观察的行为。必须每次固定执行的安全检查，应使用工具提供的 hook/policy，而不是只靠文字提醒。
- **Skill 没出现**：检查文件夹、`SKILL.md` 大小写、YAML frontmatter 和工具支持的位置，再按照官方方式 reload 或重开 session。
- **Skill 自己做了危险动作**：把 deploy、send、commit、push 改为只能由用户明确启用，并先用只读版本测试。第三方 Skill 要先读完内容和 scripts。
- **同一份 Skill 在另一个 CLI 中坏掉**：保留共同的目标和步骤，重新对照那个工具承认的 frontmatter、permission 和 tool 名称；不要靠猜。
- **项目资料太多**：项目规则只当地图，细节放在 `docs/`、Skill 的 `references/` 或其他按需文档。规则越长不代表越可靠。
</details>

> 安全底线：规则和 Skill 都是文字指令，不是绝对防护。不要放 API key、token 或个人数据；任何会写文件、commit、push、部署或调用外部服务的流程，都要有看得见的权限边界和验证步骤。

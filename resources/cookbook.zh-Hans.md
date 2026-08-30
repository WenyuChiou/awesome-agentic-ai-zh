# Cookbook — 把概念变成真的成果

> [繁體中文](./cookbook.md) | **简体中文** | [English](./cookbook.en.md)

<!-- freshness: canonical=resources/cookbook.md; verified_on=2026-08-30; scope=skills,mcp,documents,gemini-notebook,zotero,local-runtime,cli-tools; max_age_days=90 -->

这份 Cookbook 不要求你一次读完。先选一个想做的成果，复制它的第一个动作；需要更多步骤时，再打开选单。

如果名词还不熟，先回 [Stage 5：Claude Code 生态系统](../stages/05-claude-code-ecosystem.zh-Hans.md)。想比较 OpenRouter、Pi、OpenCode 与 Ollama，直接看[完整 CLI Agent 指南](cli-agents-guide.zh-Hans.md)。

## 📌 这份 Cookbook 帮你做什么

**Recipe（实践配方）**是一条从“我想做什么”走到“我怎么知道完成了”的短路线。完成任一份 Recipe，你都会得到一个可以检查的成果，而不是只看懂一段说明：

- 一张可重复使用的操作卡。
- 一个能被 Agent 调用的小工具。
- 一份文件、研究笔记或文献流程。
- 一个在自己电脑上运行的 CLI Agent。

你还会看到 **Skill（操作卡）**、**MCP Server（工具转接站）**和 **Coding Agent（程序代理）**。它们分别告诉 Agent 怎么做、替 Agent 接上工具，以及代替你读档、改档和检查结果。

## 🎯 先选一份 recipe

| 你想完成什么 | 从哪里开始 | 主要风险 |
|---|---|---|
| 让 Claude 记住固定做法 | [1. 第一个 Skill](#1-写你的第一个-skill) | 规则写得太模糊 |
| 让 Agent 调用自己的 Python 工具 | [2. 第一个 MCP server](#2-写你的第一个-mcp-server) | 把不该开放的权限交出去 |
| 生成 Word／Excel／PowerPoint／PDF | [3. Office Docs Workflow](#3-office-docs-workflow) | 没有打开成品进行人工检查 |
| 从自己的资料得到有引用的答案 | [4. Gemini Notebook Workflow](#4-gemini-notebook-workflow) | 社区集成可能突然失效 |
| 从 Zotero 搜索或整理文献 | [5. Zotero Workflow](#5-zotero-workflow) | 写入前没有预览变更 |
| 用本地模型协助修改程序 | [6. 本地 LLM＋CLI Agent](#6-本地-llm--cli-agent-快速-walkthrough) | 模型能力或电脑内存不足 |

## 🧩 六个核心词

- **Recipe（实践配方）**：一条从“我想做什么”走到“我怎么知道完成了”的短路线。
- **Skill（操作卡）**：放在 `SKILL.md` 里的可重复指令。Agent 需要时才读它。
- **MCP Server（工具转接站）**：把程序、资料或服务包装成 Agent 能看懂的 tool、resource 或 prompt。
- **Community Integration（社区集成）**：不是产品官方提供的桥接工具。可以很好用，但上游一改就可能坏。
- **Model Runtime（模型运行环境）**：真正加载并运行模型的程序，例如 Ollama；它不是 Coding Agent。
- **Coding Agent（程序代理）**：读档、改档、跑指令并反复检查结果的助手，例如 Claude Code、OpenCode、Pi 或 Aider。

<details markdown="1">
<summary>⏱️ 展开：时间、环境与安全底线</summary>

- 每份 recipe 约 20–50 分钟；先完成最短路径，再做进阶选项。
- 建议准备 Git、Python 3.11+、Node.js 20+；只有用到对应 recipe 才安装。
- 练习只用测试资料。不要把密码、API key、未公开论文或私人文件贴进不信任的工具。
- 任何会删除、寄送、发布或大量改档的动作，都要先看 diff 或 preview。

</details>

---

## 1. 写你的第一个 Skill

**成果：**做出一张项目内可共用的操作卡，并亲手触发一次。

先建立文件夹：

```bash
mkdir -p .claude/skills/summarize-changes
```

<details markdown="1">
<summary>展开完整步骤、测试与常见问题</summary>

创建 `.claude/skills/summarize-changes/SKILL.md`：

```markdown
---
description: Summarize uncommitted changes and flag risks. Use when the user asks what changed or requests a diff review.
---

## Instructions

1. Read the current git diff.
2. Explain the change in three short bullets.
3. List risks, missing tests, and files that should not be committed.
4. If there is no diff, say so. Do not invent changes.
```

启动 Claude Code 后输入：

```text
/summarize-changes
```

也可以问“我刚刚改了什么？”来测试自动触发。Claude Code 会立即检测现有 skill 目录里的 `SKILL.md` 变更，通常不用重启；只有 session 开始时整个 `.claude/skills/` 还不存在，才需要重启一次。

成功标准：回答真的根据当前 diff，而且说明了“哪里可能出错”。

常见问题：

| 症状 | 先检查什么 |
|---|---|
| `/summarize-changes` 不存在 | 路径是否正好是 `.claude/skills/summarize-changes/SKILL.md` |
| 经常误触发 | `description` 是否清楚写出“何时使用” |
| 指令太长 | 把背景资料移到同一文件夹的参考文件，需要时再读 |

先使用 project Skill 最安全：它只跟随这个 repo。确认多个项目都需要同一套做法后，才放到 personal path `~/.claude/skills/<name>/SKILL.md`。

| 容易混淆的东西 | 它解决什么 | 何时使用 |
|---|---|---|
| 一次性 Prompt | 只交代眼前这一次任务 | 做法不会重复使用 |
| **Skill** | 保存“遇到这类工作该怎么做” | 同一做法会在项目里反复出现 |
| **MCP Server** | 提供新的 typed tool、数据或服务 | Agent 需要调用外部程序或 API |

Skill 可以指挥 Agent 使用已有工具，但 Skill 本身不是新的 API。不要再用“Skill 不能读文件、MCP 才能读文件”这种过度简化来区分两者。

想做正式 eval，可用固定的“应触发／不应触发”句子测试 description，再检查回答是否遵守四个步骤。

</details>

---

## 2. 写你的第一个 MCP server

**成果：**做出一个两数相加的 MCP tool，并让 Claude Code 看见它。

先在干净的 Python 环境安装目前稳定的 MCP SDK：

```bash
python -m pip install "mcp>=2,<3"
```

<details markdown="1">
<summary>展开 server 程序、连接方式与错误排查</summary>

创建 `server.py`：

```python
from mcp.server import MCPServer

mcp = MCPServer("hello-mcp")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


if __name__ == "__main__":
    mcp.run()
```

这段程序很短，是因为 MCP v2 会从 **type hint** 生成 input schema、把 **docstring** 当作 tool description，并把返回值包装成 MCP content。参数名称、类型或 docstring 写错，Agent 就可能选错工具或传错数据。

把这个本地 stdio server 加进 Claude Code：

```bash
claude mcp add --transport stdio hello-mcp -- python server.py
claude mcp get hello-mcp
```

进入 Claude Code 后问：“用 `add` 计算 27 + 15。”成功时应得到 `42`，而且你能在 tool call 记录中看见参数。

MCP v2 的高层 class 是 `MCPServer`，正确 import 是 `from mcp.server import MCPServer`。旧的 `FastMCP` 教程与旧 import 路径不要混用。

安全底线：

- tool 只收完成任务需要的参数。
- 文件工具要限制可读写目录。
- 写入、付款、寄信或删除动作先要求人工核准。
- 第三方 MCP server 会接触你的资料；安装前先看来源与权限。

| Transport | 适合哪里 | 验证提醒 |
|---|---|---|
| **stdio** | 同一台电脑上的 Claude Code／desktop host | 第一个 server 用这条；通常不在 transport 内做 OAuth |
| **Streamable HTTP** | 远端、多人或服务化部署 | 按现行 MCP authorization 规范设计身份验证；不要照抄旧 HTTP＋SSE 教程 |

需要 API key 时，从环境变量读取；不要把 secret 写进 `server.py`、配置文件示例或 Git。

若 `claude mcp get` 显示失败，先直接跑 `python server.py` 看 import error，再确认 `--` 后面的启动指令与 Python 环境一致。

</details>

---

## 3. Office Docs Workflow

**成果：**用一份测试数据生成文件，再用真正的 Office／PDF 阅读器打开检查。

先取得 Anthropic 的官方参考实现：

```bash
git clone --depth 1 https://github.com/anthropics/skills.git anthropic-skills-reference
```

<details markdown="1">
<summary>展开 skill 安装、示例 prompt 与质量检查</summary>

`anthropics/skills` 里的 `docx`、`xlsx`、`pptx`、`pdf` 是 Anthropic 生产环境使用的复杂 skill 参考。这四个文件夹是 **source-available**，不是 Apache-2.0 开源示例；先读各自授权与 `SKILL.md`。

要在项目内试一个 skill，请把那个 skill 本身放到正确层级，不要把整个 repo 多包一层：

```bash
mkdir -p .claude/skills
cp -R anthropic-skills-reference/skills/docx .claude/skills/docx
```

PowerShell 可改用：

```powershell
New-Item -ItemType Directory -Force .claude/skills
Copy-Item -Recurse anthropic-skills-reference/skills/docx .claude/skills/docx
```

四个文件夹不是同一件事。先只安装你要练习的那一个：

| Skill | 第一个小任务 | 完成时要检查 |
|---|---|---|
| `docx` | 把测试数据做成一页摘要 | 标题、段落、表格与分页 |
| `xlsx` | 算出一小张表的合计并保留公式 | 公式、单元格类型与数值 |
| `pptx` | 按 3 点大纲做 3 张幻灯片 | 文字不溢出，图片与来源正确 |
| `pdf` | 从公开 PDF 摘出 3 个主张 | 页码、引用与原文能对上 |

可直接复制的 DOCX 任务：

```text
用我提供的测试数据做一份一页 DOCX 摘要。
保留标题、三个重点与来源栏；没有资料就标“待补”，不要猜。
完成后重新打开文件，确认没有截字、空白页或坏掉的表格。
```

检查顺序：内容正确 → 公式／数字正确 → 版面没有溢出 → 文件能重新打开。只看到“文件已创建”不算完成。

如果 skill 没出现，确认路径是 `.claude/skills/docx/SKILL.md`。Claude 产品内置的文件能力与你 clone 下来的参考版本可能不同，所以不要声称两者一定生成完全相同的结果。

</details>

---

## 4. Gemini Notebook Workflow

**成果：**放入自己的来源，取得有引用、可以回头核对的答案。

Google 已把 NotebookLM 更名为 **Gemini Notebook**；部分套件与网址仍保留旧名。先从官方网页完成一次：

```bash
python -m webbrowser https://notebooklm.google.com
```

上传两份公开文件后问：“这两份来源同意什么？不同意什么？每点附来源。”先点开引用，确认真的对得上原文，再考虑自动化。

<details markdown="1">
<summary>展开社区 CLI 自动化路径：notebooklm-py</summary>

Google 目前没有提供这套自动化的公开官方 API。`notebooklm-py` 是社区项目，使用未公开接口，适合个人研究与 prototype；正式流程要准备它突然失效时的替代路径。

```bash
uv tool install "notebooklm-py[browser]"
notebooklm login
notebooklm auth check --test --json
notebooklm create "My Research"
notebooklm use NOTEBOOK_ID
notebooklm source add ./paper.pdf
notebooklm ask "列出三个主要主张，每点附来源。"
```

要让 Claude Code 或其他支持 Agent Skills 的工具使用它：

```bash
notebooklm skill install
```

登录会打开浏览器并保存验证状态。不要把 cookie、token 或个人浏览器资料提交进 Git。

</details>

<details markdown="1">
<summary>展开另一个浏览器 skill 与排错提醒</summary>

[`PleasePrompto/notebooklm-skill`](https://github.com/PleasePrompto/notebooklm-skill) 通过浏览器自动查询 notebook。它同样不是 Google 官方集成，而且必须在浏览器完成登录。

选择方式：

| 需求 | 较适合的入口 |
|---|---|
| 只想可靠阅读与人工核对 | Gemini Notebook 官方网页 |
| 想批量新增来源、问答或导出 | `notebooklm-py` CLI |
| 已使用 Claude Code，想用 skill 调用浏览器 | `notebooklm-skill` |

遇到登录失效，先回官方网页确认账号能正常使用，再按社区项目自己的 auth 指令重新登录。不要用大量重试绕过 Google 的限制。

</details>

---

## 5. Zotero Workflow

**成果：**从本地 Zotero 找到文献；需要写入时，先预览并批准变更。

在 Zotero 打开“Settings → Advanced → Allow other applications on this computer to communicate with Zotero”，再测试：

```bash
curl http://localhost:23119/api/
```

<details markdown="1">
<summary>展开搜索、Zotero 10+ 写入授权与安全做法</summary>

本地 API 在 `http://localhost:23119/api/`，离线可用且没有 Web API rate limit。Zotero 10+ 的本地 API 支持 `POST`、`PUT`、`PATCH`、`DELETE`；过去把它当成只读接口的教程已不适用。

写入权限不会被偷偷打开。应用程序必须先向 `/api/local/authorize` 获取 **local API key**，Zotero 会显示批准窗口。这个 key 和 zotero.org Web API key 不同，而且能写入你有权编辑的 library，所以：

1. 第一次只做读取与搜索。
2. 写入前列出预计新增、移动或删除的项目。
3. 让用户在 Zotero 窗口批准。
4. 练习后到 Settings → Advanced 按 **Clear Write Authorizations** 撤销 remembered key。

配合 [`WenyuChiou/zotero-skills`](https://github.com/WenyuChiou/zotero-skills) 时，可先复制这句：

```text
只搜索，不要修改：找出我 Zotero 里 2024 年后与 multi-agent evaluation 有关的文献。
列出 title、year、DOI 和 Zotero item key；找不到的字段标“未提供”。
```

第二次才试写入，而且先要求 preview：

```text
准备把刚才的结果加入“agent-evals”collection。
先列出会移动的 item key，不要执行；等我批准后再写入。
```

`403` 通常是本地 API 未启用；`401` 是写入 key 不存在或失效；`428` 代表写入缺少正确的 `Zotero-Server-ID`。

</details>

---

## 6. 本地 LLM + CLI Agent 快速 walkthrough

**成果：**让 Coding Agent 使用你电脑上的模型，完成一个可用 Git 撤销的小改动。

先安装 [Ollama](https://ollama.com/) 并下载目前的轻量模型：

```bash
ollama pull gemma4:e4b
```

先分清它们是什么：

| 名称 | 它的工作 | 它不是什么 |
|---|---|---|
| **Ollama** | 在本地加载并运行模型的 runtime | 不会自己读 repo、改文件或跑测试 |
| **OpenRouter** | 用一个 API 账号路由多家云端模型与 provider | 不是本地模型，也不是终端 Coding Agent |
| **OpenCode／Pi／Aider** | 读文件、改文件、跑指令的 Coding Agent | 本身不是模型；仍要接本地或云端模型 |
| **Claude Code** | 使用 Claude 的 Coding Agent | 官方路径不能直接把模型切成 Ollama |

<details markdown="1">
<summary>展开主要路径：OpenCode＋Ollama</summary>

OpenCode 是会读文件、改文件和跑指令的 Coding Agent；Ollama 是在本地运行模型的 runtime。先安装 OpenCode，再用 `opencode` 启动：

```bash
curl -fsSL https://opencode.ai/install | bash
opencode
```

OpenCode 会自动寻找 `http://127.0.0.1:11434` 的 Ollama。进入 TUI 后选 `ollama/gemma4:e4b`，再到一个已经用 Git 管理的练习 repo，贴上：

```text
只修改 README.md：新增一行“Local agent test”。
先说你要改哪里；修改后显示 diff，不要 commit。
```

成功标准：只有 README 被改、diff 符合要求、`git status` 没有陌生文件。模型小时，任务也要小；一次只改一件事。

</details>

<details markdown="1">
<summary>展开 Aider 替代路径、Pi／OpenRouter入口与排错</summary>

Aider 官方建议使用 `aider-install`，Ollama model prefix 使用 `ollama_chat/`：

```bash
python -m pip install aider-install
aider-install
aider --model ollama_chat/gemma4:e4b
```

其他入口：

- [Pi](https://github.com/earendil-works/pi) 是可扩展的 Agent harness 与 Coding Agent；它默认继承启动者权限，敏感项目要另外使用 sandbox 或 container。
- [OpenRouter](https://openrouter.ai/docs/quickstart) 提供多模型统一 API 与 provider routing；它会产生云端费用，资料政策也取决于所选 provider。
- [完整 CLI Agent 指南](cli-agents-guide.zh-Hans.md) 说明何时选 Claude Code、OpenCode、Pi、Aider、OpenRouter 或本地 runtime。

常见问题：

| 症状 | 先做什么 |
|---|---|
| 找不到 Ollama model | 跑 `ollama list`，确认 tag 正好是 `gemma4:e4b` |
| 回答很慢或内存不足 | 改用 `gemma4:e2b`，并缩小任务与 context |
| Agent 改太多文件 | 立即停止，查看 `git diff`；把任务缩成一个文件的一处改动 |
| tool calling 不稳 | 改用 Stage 3 建议、且确认支持 tool calling 的模型 |

</details>

---

## 📚 必读

这些是上面指令的事实来源，不需要一次读完；做哪份 recipe，就先读那一列。

<small>资料核查：2026-08-30 UTC</small>

| 来源 | 先看什么 | 编辑评分 |
|---|---|---|
| [Claude Code — Skills](https://code.claude.com/docs/en/slash-commands) | 路径、触发方式与 live change detection | ⭐⭐⭐⭐⭐ |
| [MCP Python SDK v2 — What’s new](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/whats-new.md) | `MCPServer` import 与 v1→v2 差异 | ⭐⭐⭐⭐⭐ |
| [Anthropic Skills](https://github.com/anthropics/skills) | Skill 结构与文件 skill 的授权 | ⭐⭐⭐⭐⭐ |
| [Google — NotebookLM is now Gemini Notebook](https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/) | 产品新名称与延续关系 | ⭐⭐⭐⭐⭐ |
| [Zotero Local API](https://www.zotero.org/support/dev/web_api/v3/local_api) | 本地 API、写入授权与撤销 | ⭐⭐⭐⭐⭐ |
| [OpenCode](https://opencode.ai/docs/) | 安装、`opencode` 指令与本地模型连接 | ⭐⭐⭐⭐⭐ |
| [Aider＋Ollama](https://aider.chat/docs/llms/ollama.html) | 正确安装与 `ollama_chat/` prefix | ⭐⭐⭐⭐⭐ |
| [Ollama — Gemma 4](https://ollama.com/library/gemma4) | `e2b`／`e4b` tag 与硬体选择 | ⭐⭐⭐⭐⭐ |

## ⭐ 精选 Projects 与学习资源

评分代表本项目的教学适用度，不是 GitHub stars，也不是永久分数。

<table>
  <thead><tr><th scope="col">分类</th><th scope="col">Project／资源</th><th scope="col">适合做什么</th><th scope="col">限制</th><th scope="col">评分</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">Skills</th><td><a href="https://agentskills.io">Agent Skills standard</a></td><td>理解跨工具共用的 skill 格式</td><td>各产品仍有自己的扩展字段</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/anthropics/skills">anthropics/skills</a></td><td>阅读成熟 skill 示例</td><td>文件 skills 是 source-available</td><td>⭐⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">MCP</th><td><a href="https://modelcontextprotocol.io/specification">MCP specification</a></td><td>查 protocol 的正式定义</td><td>入门不用从头读完</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/modelcontextprotocol/python-sdk">MCP Python SDK</a></td><td>用 Python 写 server／client</td><td>注意 v1 与 v2 教程不可混用</td><td>⭐⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">文件</th><td><a href="https://github.com/anthropics/skills/tree/main/skills/docx">Anthropic DOCX skill</a></td><td>学复杂文件 skill 的结构</td><td>使用前确认授权与 runtime</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/anthropics/skills/tree/main/skills/xlsx">Anthropic XLSX skill</a></td><td>学习电子表格分析与输出流程</td><td>成品仍要用电子表格软件检查</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">Gemini Notebook</th><td><a href="https://github.com/teng-lin/notebooklm-py">notebooklm-py</a></td><td>批量来源、问答与 artifact 导出</td><td>非官方、未公开 API 可能改变</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/PleasePrompto/notebooklm-skill">notebooklm-skill</a></td><td>从 Claude Code 用浏览器查询 notebook</td><td>非官方且依赖浏览器登录</td><td>⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">Zotero</th><td><a href="https://github.com/WenyuChiou/zotero-skills">zotero-skills</a></td><td>从 Agent 搜索与整理 Zotero</td><td>写入前一定先 preview</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/WenyuChiou/research-hub">research-hub</a></td><td>串接 Zotero、Obsidian 与研究流程</td><td>比单一 recipe 更进阶</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/MuiseDestiny/zotero-gpt">zotero-gpt</a></td><td>在 Zotero 内阅读时对话</td><td>plugin 路径和外部 Agent 不同</td><td>⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">本地／CLI</th><td><a href="https://github.com/anomalyco/opencode">OpenCode</a></td><td>连接本地或云端模型修改程序</td><td>先检查 provider 和 permission 设置</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/earendil-works/pi">Pi</a></td><td>可扩展的 coding harness／CLI</td><td>默认没有内置权限隔离</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/Aider-AI/aider">Aider</a></td><td>以 Git 为中心结对编程</td><td>小模型的编码质量可能不足</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
</table>

## ✅ 完成检查与下一站

- [ ] 我完成至少一份 recipe，而且能指出生成的文件、tool 或回答。
- [ ] 我看过成功路径，也看过一次失败讯息或错误输出。
- [ ] 我没有提交 token、cookie、个人文件或未公开资料。
- [ ] 我知道使用的是官方功能还是 Community Integration。
- [ ] 任何写入或大量改动都有 preview、diff 或人工批准。

接着回 [Stage 5](../stages/05-claude-code-ecosystem.zh-Hans.md) 选下一个能力；要找更多工具，进入 [MCP／Skills Catalog](mcp-skills-catalog.zh-Hans.md)。

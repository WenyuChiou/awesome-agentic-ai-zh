<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# tool-calling-tutor — Claude Code skill

> Skill 用途：当你卡在 tool calling（LLM 不调用、args 错、ReAct loop 跑不停、schema 不知道怎么写），可直接输入 `/tool-calling-tutor` 打开；在相关情境中也可能自动载入，带你完成 4-symptom 诊断与 5-step 修法。

对应 [Stage 3 — Tool Use & Agent 入门](../../../stages/03-tool-use-and-hello-agent.zh-Hans.md)，同时是 [Stage 5 — Claude Code Ecosystem](../../../stages/05-claude-code-ecosystem.zh-Hans.md) 5.3 的**自带 skill 范例**。

## 为什么这个 skill 存在

Tool calling 是整个 curriculum 最陡的学习曲线——schema 设计、SDK response shape、ReAct loop 三个 mental model 叠在一起。Stage 3 doc 已经把概念讲清楚，但**遇到“我这份就是不会跑”的时候、需要互动式 debug**。

这个 skill 补的就是这块缺：

| 已有资源 | 不足 | 这个 skill 补的 |
|---|---|---|
| `stages/03-tool-use-and-hello-agent.zh-Hans.md` | 讲 6 个练习、不互动 | 互动式 triage：你卡哪个 symptom？ |
| `resources/schema-design-cheatsheet.zh-Hans.md` | 5 条规则 + 5 anti-pattern、prescriptive | 走步骤版：bad → good schema 怎么 4 步改 |
| `resources/glossary.zh-Hans.md` 2 | 1 行定义 | 不重复定义、引用为主 |
| `examples/stage-3/02-06/` | 完整可跑 starter | Skill 指过去当 fork template |

## 双重用途

1. **学习者用**：安装后当 personal debug 助手。直接输入 `/tool-calling-tutor` 打开；相关问题也可能让 skill 自动载入。
2. **Stage 5 5.3 meta-example**：学 SKILL.md 怎么写的时候，直接看这份。包含完整 frontmatter（含 trigger phrases + Do NOT use for）、`references/` 设计、`evals/evals.json` 范例。

## 怎么安装

以下命令都从这个 repository 的根目录执行。

### Option A：user 级（所有 project 共用）

```powershell
$repoRoot = Get-Location
$skillSource = Join-Path $repoRoot "examples\stage-5\tool-calling-tutor"
$skillTarget = Join-Path $env:USERPROFILE ".claude\skills\tool-calling-tutor"
New-Item -ItemType Directory -Force -Path $skillTarget | Out-Null
Copy-Item -Force -LiteralPath (Join-Path $skillSource "translations\SKILL.zh-Hans.md") -Destination (Join-Path $skillTarget "SKILL.md")
Copy-Item -Recurse -Force -LiteralPath (Join-Path $skillSource "references") -Destination $skillTarget
Copy-Item -Recurse -Force -LiteralPath (Join-Path $skillSource "evals") -Destination $skillTarget
```

繁体中文请改为复制 `SKILL.md`；英文请改为复制 `translations/SKILL.en.md`。

### Option B：project 级（只在这个 repo 触发）

```powershell
$repoRoot = Get-Location
$skillSource = Join-Path $repoRoot "examples\stage-5\tool-calling-tutor"
$skillTarget = Join-Path $repoRoot ".claude\skills\tool-calling-tutor"
New-Item -ItemType Directory -Force -Path $skillTarget | Out-Null
Copy-Item -Force -LiteralPath (Join-Path $skillSource "translations\SKILL.zh-Hans.md") -Destination (Join-Path $skillTarget "SKILL.md")
Copy-Item -Recurse -Force -LiteralPath (Join-Path $skillSource "references") -Destination $skillTarget
Copy-Item -Recurse -Force -LiteralPath (Join-Path $skillSource "evals") -Destination $skillTarget
```

<details markdown="1">
<summary>macOS/Linux 命令</summary>

```bash
skill_source="examples/stage-5/tool-calling-tutor"
mkdir -p ~/.claude/skills/tool-calling-tutor
cp "$skill_source/translations/SKILL.zh-Hans.md" ~/.claude/skills/tool-calling-tutor/SKILL.md
cp -R "$skill_source/references" "$skill_source/evals" ~/.claude/skills/tool-calling-tutor/

mkdir -p .claude/skills/tool-calling-tutor
cp "$skill_source/translations/SKILL.zh-Hans.md" .claude/skills/tool-calling-tutor/SKILL.md
cp -R "$skill_source/references" "$skill_source/evals" .claude/skills/tool-calling-tutor/
```
</details>

### 验证安装

在 Claude Code 中输入：

```
/tool-calling-tutor
```

预期：skill 会打开，并询问或确认对应的 symptom 路线。这是确定性的安装检查。自动载入取决于上下文，不能作为安装成功的证明。

Claude Code 会在当前 session 中侦测已有 personal 或 project skills 目录里的变更。只有在 session 开始时顶层 skills 目录不存在时，才需要重启。

## 包含什么

```
tool-calling-tutor/
├── SKILL.md # 主 skill 档（zh-TW canonical）
├── README.md / .en.md / .zh-Hans.md # 你正在看的这份
├── references/
│ ├── debug-flowchart.md # 4-symptom 诊断流程
│ ├── schema-evolution.md # bad → good schema 4-step worked example
│ └── sdk-diff.md # Anthropic vs OpenAI-compat 并排对照
│ （以上每份都有 .en.md / .zh-Hans.md 翻译）
├── translations/
│ ├── SKILL.en.md # SKILL.md 英文版（给英语用户装）
│ └── SKILL.zh-Hans.md # SKILL.md 简体版
└── evals/
    ├── evals.json # 5 个离线 contract case
    └── check_evals.py # 不调用 model 的检查器
```

## 跑 evals（选择性）

```powershell
python evals/check_evals.py
```

这是五个 case 的**离线 contract 检查**：不询问 model，只检查每条约定是否写完整、链接是否能找到。`evals.json` 不是 promptfoo 配置文件。若日后要加入 model-graded eval，[promptfoo](https://github.com/promptfoo/promptfoo) 是一个常见的可选路径；本范例没有提供 provider 配置，也没有质量分数。

## 跟其他资源的关系

```
        ┌─────────────────────────────────┐
        │ Stage 3 doc + 练习 1-6 inline │
        │ (学 tool calling 概念) │
        └────────────────┬─────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────┐
        │ examples/stage-3/02-06/ │
        │ (完整可跑 starter + test) │
        └────────────────┬─────────────────┘
                         │ fork template
                         ▼
        ┌─────────────────────────────────┐
        │ 你的 tool-calling agent │
        │ ❓ 卡住了 │
        └────────────────┬─────────────────┘
                         │ 载入
                         ▼
        ┌─────────────────────────────────┐
        │ tool-calling-tutor skill (这个) │
        │ → 4-symptom triage │
        │ → references/ deep dive │
        │ → 路由到 cookbook / Stage 4/7 │
        └─────────────────────────────────┘
```

## 不处理什么

| 情境 | 路 |
|---|---|
| LangChain / LangGraph / CrewAI / Pydantic AI | Stage 4 |
| 写 MCP server / client | `resources/cookbook.zh-Hans.md` 2 |
| Production observability / cost tracking | Stage 7 |
| 一般 prompt engineering | Stage 2 |

## 延伸

- **改 trigger phrases**：在 SKILL.md frontmatter `description` 加你自己常用的触发句
- **加你的 case 到 references/**：debug-flowchart 里开新 Section、把你碰到的 weird case 记下来
- **fork 成你的版本**：这个 skill 设计就是 Stage 5 5.3 的 meta-example、欢迎 fork

<details markdown="1">
<summary>当前来源</summary>

简短的当前参考（检查于 2026-08-28 UTC）：[Claude Code skills](https://code.claude.com/docs/en/skills)、[Agent Skills](https://agentskills.io)、[Anthropic skills](https://github.com/anthropics/skills) 与 [promptfoo](https://github.com/promptfoo/promptfoo)。
</details>

## License

跟 repo 一致（MIT）。Skill body 改写、fork、商用都 OK。

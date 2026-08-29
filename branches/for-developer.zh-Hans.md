# 开发者延伸路线（For Developers）

> [繁體中文](./for-developer.md) | **简体中文** | [English](./for-developer.en.md)

> 🚀 **第一次装 Claude Code / 写 `CLAUDE.md` / `SKILL.md`？** 快速 setup 指南在 [`resources/setup-guide.zh-Hans.md` D-E](../resources/setup-guide.zh-Hans.md)。已经熟可以跳过。

> [← 回主路线 README](../README.zh-Hans.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 后从这里接续。把 agentic AI 应用到开发流程上。

## 使用场景（开发场景 × AI 怎么帮）

下表把开发者一天会遇到的 7 个场景拆开——每个场景有不同的痛点，AI 工具也不同：

| 场景 | 你常遇到的痛点 | AI 能帮的部分 | 推荐工具（从轻到重） |
|---|---|---|---|
| **AI 结对编程** | 写到一半忘 syntax / 想不到 method 名 | 自动补全 + 改写 + 解释 | Cursor / Copilot → Claude Code |
| **多文件重构** | 改一个 class 怕漏改、跨文件 rename 容易错 | batch refactor、改 50 个文件仍保持风格一致 | Cursor → Claude Code → codex-delegate |
| **Code review（自己 PR）** | review 自己的 diff 看不出问题 | 找 bug / smell、检查 edge case | Claude Code / Cline → Continue（CI） |
| **写 test** | TDD 常忘加 case、coverage 不足 | 从 signature / spec 生成 pytest | Claude Code + Aider |
| **Debug** | log 不够、stack trace 看不懂 | 解释 trace、生成 hypothesis、跑 minimal repro | Claude Code |
| **Doc** | docstring / README 没人写、refactor 后过期 | 从 code 生成 doc、PR 对应改 doc | Claude Code |
| **CI / 团队自动化** | 重复手动跑 review、跨人风格不一 | GitHub Action 自动跑 review / lint | Claude Code Action + Continue |

> 💡 **个人 vs 团队**：表中前 6 个是个人 daily workflow；最后 1 个（CI）是团队规范。团队规模 < 5 人时 CI 自动化的 ROI 不高，可以先不上。

## 精选 Projects

> **CLI agent 身份与选择指南**：想按工作方式选工具，见 [`resources/cli-agents-guide.zh-Hans.md`](../resources/cli-agents-guide.zh-Hans.md)。第一次接触 CLI agent 想要 step-by-step 入门 → [`tracks/cli/A1-cli-intro.zh-Hans.md`](../tracks/cli/A1-cli-intro.zh-Hans.md)（Track A 第一站）。
>
> **MCP catalog**：要把 CLI 接到日常工具（GitHub、Linear、Atlassian、Postgres、Playwright、Figma 等）→ [`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md)（81+ 个分类整理）。
>
> 本页只列**跟开发者 workflow 直接相关**的工具入口。

### Coding Agents

#### [Cursor](https://www.cursor.com/) ⭐⭐⭐⭐⭐
编辑器集成的 AI 结对编程工具。在 AI 编辑器类工具中采用度高，可作为比较其他 IDE agent 的基准。

#### [Aider-AI/aider](https://github.com/Aider-AI/aider) ⭐⭐⭐⭐⭐
★ 47k+ · Apache-2.0 — git-aware 的 CLI pair-programmer。直接编辑你 repo 中的文件，commit 都自动写好。**“git-native AI 编辑流程”的开源模板**。模型不限。

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 138k+ — Anthropic 官方的 agentic coding 助理。有 Skills + plugin 生态系。

#### [cline/cline](https://github.com/cline/cline) ⭐⭐⭐⭐⭐
★ 65k+ · Apache-2.0 — VS Code extension，autonomous in-IDE agent：tool use、browser、step-by-step approval。**VS Code 用户想 IDE-native agentic dev 的好选项**。

#### [continuedev/continue](https://github.com/continuedev/continue) ⭐⭐⭐⭐
★ 35k+ · Apache-2.0 — source-controlled AI checks，可以在 CI 强制执行。代表“**团队 / governance**”这条角度的 coding agent。

#### [OpenHands (前身为 OpenDevin)](https://github.com/OpenHands/OpenHands) ⭐⭐⭐⭐
★ 81k+ · MIT — open source 的自主软件开发 agent。设计上比 Aider / Claude Code 更激进——agent 自己跑 sandbox、自己 commit，适合“整个 issue 丢给它解”场景。

#### [aaif-goose/goose](https://github.com/aaif-goose/goose) ⭐⭐⭐⭐
★ 51k+ · Apache-2.0 — 开源、可扩展的 AI agent，超出纯 code suggestion——能 install / execute / edit / test，搭配任何 LLM。同时支持多家 LLM provider 跟 MCP，提供 desktop app、CLI、API 三种接口。（repo 现指向 `aaif-goose/goose`。）

#### [RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code) ⭐⭐⭐（⚠️ 已封存）
★ 24k+ · Apache-2.0 — VS Code 的 coding agent，采用“**多种专业模式**”的设计，跟 Cline 的单一 agent flow 不同。**⚠️ repo 已于 2026-05 封存（read-only、不再维护）**——仍可用，但别预期新功能。

### Code Review

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
20+ 个经过实战验证的 skill，包括 TDD 模式、debug、协作模式。设计 code-review skill 时的好参考。

### 推荐工具

- [**yamadashy/repomix**](https://github.com/yamadashy/repomix) ⭐⭐⭐⭐⭐ ★ 27k+ — **典型开发者用途：打包整个 codebase 给 reviewer / refactor agent**。输出单个 AI-friendly 文件（XML / Markdown / JSON），方便 Claude Code / Codex 做 code review / refactoring。技术细节（MCP server mode、tree-sitter 压缩、secretlint 过滤）见官方 README。**Track A 的必备 daily-driver 工具。**

## 必练流程（按使用频率）

| 频率 | 流程 | 怎么做（≤ 3 步） | 推荐工具 | 适合谁 |
|---|---|---|---|---|
| **每天** | AI 结对写 code | (1) 开 branch<br>(2) 任务丢给 Claude Code、**先 plan**（不写 code）<br>(3) Review plan → approve → 写 code → 自己 review diff | Claude Code / Cursor / Cline | 全开发者 |
| **每天** | Git-native AI 编辑 | (1) `aider`<br>(2) 自然语言请求<br>(3) review + commit / `/undo` | Aider | 想要干净 git 流程的人 |
| **Per PR** | 自动 code review | (1) `.github/workflows/claude-review.yml`<br>(2) 抓 git diff → 跑 prompt → post 回 PR<br>(3) human + AI 双审 | Claude Code Action + Continue | 团队 |
| **Per feature** | 测试生成 | (1) 给 function signature + docstring<br>(2) 请 AI 生成 pytest case（含 edge case）<br>(3) 跑覆盖率 + 故意改 bug 看 test 抓不抓得到 | Claude Code / Aider | 写 test 阶段 |
| **不定期** | 多文件批量修改 | (1) Claude 写 plan<br>(2) codex-delegate 跑机械式 refactor<br>(3) Claude review diff | Claude + codex-delegate | refactor 30+ 文件的时候 |

> 💡 **新手起手式**：先做“每天 AI 结对”+“测试生成”两条一个月，习惯后再上 PR 自动 review。

### 3 个具体 workflow recipe

**1. AI 结对编程（每日节奏）**

1. 开新 feature → `git checkout -b feature/xxx`
2. 把任务丢给 Claude Code / Cursor，**先让它写 plan**（不直接写 code）
3. Review plan、修正方向 → 才 approve 写 code
4. 写完跑 tests + lint → 自己 review diff（**不要 blind accept**）
5. Commit message 自己写或 prompt 生草稿后改

**2. Aider git-native 流程（最像“跟 AI pair”）**
```bash
# 进入 repo 后
aider --model anthropic/claude-sonnet-5

# 自然语言请求
> 帮我把 utils.py 的 parse_date 加上时区参数，默认 UTC

# Aider 会自动编辑 + commit。若不满意：
> /undo # 退掉最后一次 AI commit
```

**3. PR 上的 Claude code review（GitHub Action）**

`.github/workflows/claude-review.yml`：
```yaml
on:
  pull_request:
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Run Claude review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # 用 anthropics/claude-code-action 或自写 script
          # 抓 git diff、跑 prompt、结果 post 回 PR
```
参考 [`anthropics/claude-code-action`](https://github.com/anthropics/claude-code-action) 官方 GitHub Action。

## 常见踩坑（Anti-patterns）

| ❌ 不要 | ✅ 改成 |
|---|---|
| 让 AI 直接 push 到 main | 永远 PR → review → merge |
| Blind accept 大规模 refactor diff | 拆成 < 50 LOC 改动，逐个 review |
| 把 .env / API key 丢给 AI 看 | 用工具对应的排除机制：Cursor `.cursorignore` / Aider `.aiderignore` / Claude Code 用 `.claude/settings.json` 的 `permissions.deny` |
| 让 AI 在 production code 自由跑 shell | sandbox 限制、permission whitelist |
| 用 AI 生 test 后不检查 assertion | 跑覆盖率 + 故意改一个 bug 看 test 抓不抓得到 |
| 跨多个 commit 才发现方向错 | **plan-first** 模式：先 review plan 再写 code |

## Tier 升级路径

下表是建议的进阶路径：

| Tier | 工具 | 适合谁 | 学习成本 |
|---|---|---|---|
| **Tier 0** | Cursor / Copilot / Claude.ai | IDE 内 chat、autocomplete、不自己写 agent | 0（会用编辑器就行） |
| **Tier 1** | Claude Code（`CLAUDE.md`）／Cline／OpenCode V2（`AGENTS.md`） | CLI 接 file system、human-in-the-loop | 1-2 天上手 |
| **Tier 2** | 自写 Skills + MCP server | 把 dev workflow 包成 skill 给团队共用 | 1 周 setup |
| **Tier 3** | CI 自动跑 agent + production observability | 进到 [Stage 7](../stages/07-multi-agent-production.zh-Hans.md) 领域 | 数周、需 governance |

> **多数个人开发者可先停在 Tier 0-1**。**升级到 Tier 2+ 要先确认 ROI**——团队够大、流程够重复、事故不可逆，才值得 invest。

## 也适用其他分支

开发者重叠度高的分支：

- **要做 ML 研究 / 写 paper** → [研究员分支](./for-researcher.zh-Hans.md)
- **接 Notion / Linear / Atlassian / Postgres / Figma** 等 dev tool → [`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md)
- **要写自己的 Skill / MCP server** → [Stage 5](../stages/05-claude-code-ecosystem.zh-Hans.md) + [`resources/cookbook.zh-Hans.md`](../resources/cookbook.zh-Hans.md)
- **想看 schema 设计细节** → [`resources/schema-design-cheatsheet.zh-Hans.md`](../resources/schema-design-cheatsheet.zh-Hans.md)
- **CLI 从零开始** → [Track A](../tracks/cli/A1-cli-intro.zh-Hans.md)（A1 → A2 → A3）

## 社群备注

特别欢迎以下贡献：

- IDE-specific 设置范本（Cursor `.cursorrules`、Claude Code `CLAUDE.md` for Python / Go / Rust 等）
- 编程语言特化 skill（Python / TypeScript / Rust / Go 各自的 best practice）
- CI / pre-commit hook 集成 case study
- **跨多人团队用 AI dev 的 governance pattern**——多 dev 共用 Skills、permission 设计、cost tracking

请见 [CONTRIBUTING.zh-Hans.md](../CONTRIBUTING.zh-Hans.md)。

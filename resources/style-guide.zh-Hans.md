> [繁體中文](./style-guide.md) | **简体中文** | [English](./style-guide.en.md)

# `awesome-agentic-ai-zh` 风格指南

这份指南是这份 catalog 的**单一真实来源**——术语、entry 结构、license 标注、写作风格、禁用词，全部以这份文件为准。

PR 之前请先读完本文。项目维护者也会用这份指南做 review。

---

## 📋 目录

- [1. 项目 entry schema](#1-项目-entry-schema)
- [2. 推荐星等定义](#2-推荐星等定义)
- [3. 禁用词与替代](#3-禁用词与替代)
- [4. 可保留的英文名词](#4-可保留的英文名词)
- [5. License 标注惯例](#5-license-标注惯例)
- [6. Stage 页面模板](#6-stage-页面模板)
- [7. Branch 页面模板](#7-branch-页面模板)
- [8. 写作风格规范](#8-写作风格规范)
- [9. 链接与引用](#9-链接与引用)

---

## 1. 项目 entry schema

每个 project entry 统一格式如下：

```markdown
### [Repo Name](https://github.com/owner/repo) ⭐⭐⭐⭐

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 12k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：1-2 句话，这个 project 在这个 stage 教什么具体的东西。

**适合谁**：1 句话，谁应该读这个、为什么。

**备注**：1-3 句个人评价。哪里好、哪里弱、哪里可以跳。（可省略）

**怎么跑**：
\`\`\`bash
# 最小安装指令、第一次跑该执行什么
\`\`\`
```

### 必填字段（GitHub repo entry）
对“真实 GitHub repo”的 entry：

- `Stars`（★ Xk+ 格式，无千位逗号）
- `License`（SPDX ID 或标注例外，见 5）
- `推荐度`（⭐ × N，见 2）
- `教什么`、`适合谁`

### 必填字段（非 repo entry：article / course / video / protocol / documentation）
某些 entry 不是 GitHub repo 而是文章、视频、官方文件、catalog hub。对此类：

- `推荐度`（必填）
- `教什么`、`适合谁`（必填）
- `形式`（必填，标明是 `文章` / `视频` / `课程` / `精选列表` / `规格文件` 等）
- `Stars` / `License` 可省略（没有 GitHub repo 对应）

范例：`Anthropic — Building Effective Agents` 部落格文章用 `形式 = 文章` + 推荐度，不需要 Stars / License。

### 选填字段
- `语言` — 主要编程语言（Python / TypeScript / 中文 等）
- `最后更新` / `状态` — 已停滞或维护放缓时加注
- `备注`、`怎么跑`

### 标题格式
- Stage 1-4 / 6 用 `### [Repo](url)`
- Stage 5 / 7 / branches 用 `#### [Repo](url)`（已有上层 H3 分类时）
- 标题后可接星等：`### [Repo](url) ⭐⭐⭐⭐⭐` 或副标题：`### [Repo](url) ⭐ 官方`

---

## 2. 推荐星等定义

| 星等 | 含义 | 何时用 |
|---|---|---|
| ⭐⭐⭐⭐⭐ | 必读 / 必做 | 该 stage 不读这个会卡住 |
| ⭐⭐⭐⭐ | 强烈建议 | 深入学该主题的好材料 |
| ⭐⭐⭐ | 扎实范例 | 值得跑一遍、互相对照 |
| ⭐⭐ | 有用参考 | 有兴趣再看 |
| ⭐ | 利基 / 进阶 / 为了完整性 | 多数读者可跳 |

这些是编辑评分，不是 GitHub stars。移除 `★ 140k+` 这类会变化的热门度数字时，必须保留原有 `⭐⭐⭐⭐⭐` 评分；只有资源用途、质量或维护状态的查证结果改变时，才能连同理由调整评分。

**准则**：

- 同一个 repo 出现在不同 stage / branch 时，**星等应一致**（除非有明确 audience-specific 理由，且注明在备注）
- 不要因为“想要看起来推荐”就给高星等。诚实 > 客气
- 商业产品（Cursor、LangSmith 等）也照同一套标准

---

## 3. 禁用词与替代

这份文件以**简体中文（zh-Hans，中国大陆惯例）** 为准。下表列出常见的 zh-TW 用词与替代。

> 📌 **语言代码惯例（BCP 47 / W3C i18n）**：repo 用 `.zh-Hans.md`（不是 `.zh-CN.md`）标记简体中文档。`Hans` / `Hant` 是 [BCP 47 script subtag](https://www.w3.org/International/articles/language-tags/)，跟地区解耦——简体中文不只用在中国大陆（也用在新加坡、马来西亚），用 `Hans` 比 `CN` 更准确。canonical README 的内容是 **zh-Hant-TW**（繁体中文，台湾惯例），但档名保持无 suffix 的 `README.md` 作为 GitHub 默认首页。未来若要分地区可再扩成 `zh-Hans-CN` / `zh-Hant-HK` 等。感谢 [@xfq](https://github.com/xfq)（W3C i18n lead）在 [#9](https://github.com/WenyuChiou/awesome-agentic-ai-zh/issues/9) 指出这个问题。

### 繁简用词替换

| 禁用（zh-TW） | 改用（zh-Hans） |
|---|---|
| 使用者 | 用户 |
| 軟體 | 软件 |
| 資料 | 数据 |
| 專案 | 项目 |
| 腳本 | 脚本 |
| 預設 | 默认 |
| 設定 | 设置 |
| 連結 | 链接 |
| 練習 | 练习 |
| 動手 | 动手 |
| 飛書 | 飞书 |
| 個 | 个 |
| 兩 | 两 |
| 「」 | “” |
| 整合 | 集成 |
| 系統 | 系统 |
| 點 | 点 |
| 為 | 为 |
| 過 | 过 |
| 還 | 还 |

### Overclaim（夸大）用语禁用

| 禁用 | 改用 |
|---|---|
| 全世界最好的 / 业界最强 | 完整的 / 知名的 / 广泛使用的 |
| production-grade（描述教材时） | 教学导向 / 用来学 production pattern 的教材 |
| 首选 / 唯一选择 | 不错的选项 / 入门选择之一 |
| 最紧迫 / 最重要 | （直接不要修饰） |
| 权威参考（除非真的是官方 spec） | 重要参考实作 / 官方范本 |
| 没问题（法律或 license 判断时） | 使用前先读条款 / 条款还是要自己看过 |

### 中夹英（English-in-Chinese）禁用句型

| 禁用 | 改用 |
|---|---|
| follow 条款 | 遵守条款 |
| ready-made 教材 | 现成可改的教材 |
| NotebookLM-like 工具 | 类 NotebookLM 的工具 / 类似 NotebookLM 的工具 |
| 视觉化 node-based | 视觉化节点式 |
| Anthropic host 的 server | Anthropic 维护的 server |
| coding 流程 | 开发流程 / 程序开发流程 |

---

## 4. 可保留的英文名词

技术写作中**保留英文**比硬翻译读起来更自然的词：

- `LLM`、`API`、`SDK`、`MCP`
- `agent`、`tool use`、`function calling`、`prompt`、`prompt caching`
- `framework`、`library`、`repo`、`commit`、`PR`、`branch`
- `RAG`、`embedding`、`vector DB`、`retrieval`、`chunk`、`token`
- `streaming`、`async`、`batch`、`webhook`
- `marketplace`、`plugin`、`skill`、`hook`
- `project`、`repo` （可保留也可改用“项目”）
- `production`（指“正式环境”时）— 但本 catalog 多数场合刻意避免（见 3）
- `动手练习`、`hello-world` — 保留

**判准**：技术文件圈读者习惯的英文术语就保留，避免“太政治正确的中文化”。

---

## 5. License 标注惯例

### 常见 license 直写
- `MIT`
- `Apache-2.0`
- `BSD-3-Clause`
- `GPL-3.0`
- `LGPL-3.0`

### 需要加注的特殊情况

| 情况 | 写法 |
|---|---|
| 上游无 SPDX | `NOASSERTION（上游未提供 SPDX；使用前请读 LICENSE）` |
| AGPL（传染性） | `AGPL-3.0` + 备注：`AGPL-3.0 license（传染性开源）— 修改后散布的衍生产品需遵守条款。` |
| 自定义非商用 | `NOASSERTION（自定义非商用）` + 备注：`License 是自定义非商用条款，使用前请先读原始条款。` |
| 多元 license（每个 plugin 自己有） | `NOASSERTION（每个 plugin 独立 license，请看各自目录）` |
| Creative Commons | 直写 `CC-BY-4.0`、`CC-BY-NC-SA-4.0` 等 |

**规则**：**永远不要**把 license 解读成法律建议。“研究 / 个人使用没问题”这种句子禁用。改成“使用前先读原始条款”。

---

## 6. Stage 页面模板

> 同一个模板适用于两个位置：
> - `stages/0X-*.md` — 共用基础（0-2）+ Track B（Stage 3-8）
> - `tracks/cli/AX-*.md` — Track A（A1-A3）的 sub-stage，也照同一模板，只是 cross-link 比例较高（多数 entry 引用既有 Stage 5 / 7 / cli-agents-guide）

每个 stage（Stage 0 除外）都应该有：

```markdown
# Stage N — 主题

> [English](./0N-slug.en.md) | **简体中文**

[1-2 句话描述这个 stage 的核心问题]

## 📌 学习目标
- bullet 1
- bullet 2
...

## 🧩 先认识核心词

### **正确术语（需要时附中文）**
用一句白话定义。再给一个不会扭曲概念的生活比喻，并说明后面的哪个练习会用到它。

## 🚪 进入条件（Stage 1+ 才需要）
<details markdown="1">
<summary>⏱ 开始前先看：时间、先备工具与预算</summary>

**时间估算**：N-M 周（约 X-Y 小时）

你应该已经：
- ...

</details>

## 📚 必修阅读
这些资料会在练习中用到；需要时再展开。

<details markdown="1">
<summary>展开 3-5 个必读来源</summary>

1. [链接](url) — 描述
2. ...

</details>

## 🛠 动手练习（不是看过就好）

### 练习 N：标题
一句话描述完成后会看到什么。标题留在 details 外，让深链接可见。

<details markdown="1">
<summary>展开详细步骤</summary>

时间、费用、代码、预期输出与疑难排解。

</details>

[3-5 个动手练习 items]

## 🎯 精选 Projects

### [Project Name](url) ⭐⭐⭐⭐
[entry schema 见 1]

[N 个 entries]

## ✅ 进 Stage N+1 前的自我检查
你能不能：

- [ ] ...
- [ ] ...

如果可以 → 进 Stage N+1。
如果不行 → ...

## 💡 接下来（选填，多在最后一个 stage 用）
```

保留标题、成果和第一步可见。次要 `<details>` 默认不加 `open`。Ollama Path A 仍是主要路径，但不要看到 Path A 就一律展开：只有它是读者眼前唯一要做的事，而且内容很短时才可加 `open`。长代码和排错默认收合；Anthropic Path B 也默认收合。不要把可被链接的 heading 放进 `<details>`，也不要使用三层以上的嵌套收合。

### 全站白话规则（ELI5）

这条规则适用于整个学习地图。目标是让五岁孩子也能明白“现在要做什么”，但不能牺牲技术准确性，也不要使用幼稚的语气。

- 技术词第一次出现在可见教学文字时，要用**粗体**标出；H1 章名可以直接使用，但正文第一次使用仍要遵守这条规则。接着先说明它的白话用途，再保留正确术语。例如：“让程序获取数据的入口（**API**）”。
- 一句话只讲一个想法。一个步骤只要求一个主要动作。遇到长句、缩写或 jargon，先拆开，或补一句定义。
- 指令、文件名、错误码、模型名称、价格、数字和安全提醒必须保持精确。
- 即使不展开任何 `<details>`，读者也应该知道下一步要做什么，以及成功时会看到什么。
- Review 时抽查可见主线。如果第一次来的读者无法用自己的话说出下一步，就先改写。需要多段的原理移入默认收合的内容。

### 核心词写法

- 每个完成回溯的 Stage／Track，都要在第一个练习前放一个可见核心词区。核心词名称与最短解释不能放进 `<details>`。
- 每个核心词独立回答四件事：**它是什么**、**它像什么**、**这章用它做什么**、**正确术语是什么**。需要更深原理时，再把补充放进默认收合区。
- 只收后文、练习或 self-check 真的会用到的关键概念。不要把每个普通名词拉出来凑数，也不能用“太细”当理由删掉 Zero-Shot、Token、MCP 等必要术语。
- 三语的概念、顺序、用途与限制一致；英文名、缩写、指令与规格名称保持精确。
- `scripts/reader-ux-pages.yml` 的 `core_terms` 会记录核心区、第一个练习、三语 term／label、顺序与最低解释长度。加入后只能维持或加强，不能静默移除。

### Reader UX ratchet

- 只有在一个章节完成三语迁移和人工复查后，才把它加入 `scripts/reader-ux-pages.yml`。这是逐章收紧规则；尚未整理的页面不必一次通过全部检查。
- `scripts/check-reader-ux.py` 使用保守的 source-level proxy，计算第一次打开页面时可见 Markdown 的非空白字符。默认展开内容与可见 fenced code 会计入；HTML comment 与收合内容不计入。这是可重复的 ratchet，不是浏览器 DOM 字数。
- 配置会保存各语言的字数上限、允许默认展开的区块数量、必须保持可见的精确 heading／anchor、核心词契约，以及资源表的分组行数。没有重新审查，不得提高上限或删除保护项。
- 自动 gate 只能防止已知的结构倒退。人工 review 仍须确认：不展开任何 `<details>` 时，读者知道要做什么，也知道成功时会看到什么。

### 分组资源表

- 同一分类连续出现两行以上时，改用 HTML `<table>`，并通过 `<th scope="rowgroup" rowspan="N">` 合并分类栏。
- 每个 `<thead>` 列标题 `<th>` 都要加 `scope="col"`。
- 每个分类使用一个独立的 `<tbody>`；分类第一行保留 `<th scope="rowgroup" rowspan="N">`。
- 只合并真正共用的分类。不同分类不能因为状态、Context 或其他文字相同就跨组合并。
- 转换后保留原有资源数量、顺序、链接和三语对应，并用 MkDocs 检查实际渲染。
- 没有重复分类的短表格继续使用 Markdown，避免增加不必要的维护成本。

含模型、价格、context、授权或生命周期状态的页面，要在资料附近加入可见查核日期与机器 marker：

```markdown
> 资料查核：YYYY-MM-DD UTC。价格与可用性之后可能改变，使用前请再看官方页面。

<!-- freshness: canonical=stages/0N-slug.md; verified_on=YYYY-MM-DD; scope=models,pricing,availability,deprecations; max_age_days=90 -->
```

三语 marker 必须完全一致；`canonical` 一律指向繁中主页。官方没有公布的字段写“官方未公布”，不要从第三方榜单反推；第三方 benchmark 只能教读者怎样自行评测。

**Stage 0 例外**：可以省略 `精选 Projects`、`进入条件`，因为它是 prerequisite gateway。可见主线依次保留跳过判断、4 个学习目标、1 个整合练习和简短完成检查；时间、环境、补充练习、名词与学习资源默认收合。

---

## 7. Branch 页面模板

```markdown
# 给 [audience] — 专业分支

> [English](./for-X.en.md) | **简体中文**

> [← 回主路线 README](../README.md) · 从 Stage 7 结尾分支出来

## 使用情境
- bullet 1
- bullet 2

## 精选 Projects

### 子分类 1
#### [Project](url) ⭐⭐⭐⭐
[entry]

### 子分类 2
...

## 必修阅读
1. ...

## 必练流程
- bullet 1
- bullet 2
```

Branch 的 entry 格式可以比 stage 简洁（不一定要完整 schema 表格），但链接 + 星等 + 1-2 句描述是最低门槛。

---

## 8. 写作风格规范

### 句长
- **单句不超过 60 字**（中文标点计入）
- 太长就断成两句
- 英文 rhythm 强迫塞进中文 = 翻译腔，要避免

### 标点
- **中文用全角**：，。：；“”（）
- **句中夹英文**时，英文前后可以留空格也可以不留，但全文要一致
- **避免 ASCII 逗号 `,`** 在中文句中（会中夹英）

### 主动 vs 被动
- 偏主动句：“Claude 调用工具” ✓
- 避免被动句：“工具被 Claude 调用” ✗

### “你” vs “我们”
- **“你”优先**——这是给读者的学习材料
- “我”用于作者发表意见时：“我建议...”
- 避免“我们”（除了合著者实际存在的场合）

### 连接词
- 偏好简单：“但、所以、因为、不过”
- 避免：“然而、因此、由于、之所以”

---

## 9. 链接与引用

### 内部链接
- Stage 之间：相对路径 `[Stage 4](./04-agent-frameworks.zh-Hans.md)`
- Branch ↔ README：`[← 回主路线](../README.zh-Hans.md)`
- 跨 stage 引用同一 repo：用全名 + 链接，不要只写“之前提过”

### 外部链接
- GitHub repo：`https://github.com/owner/repo` ✓ 不加 trailing slash
- 文章 / 部落格：完整 URL，标题用粗体
- 商业产品（Cursor、Make.com 等）：用官方网址，不是 affiliate

### 链接文字惯例
- Repo entry 标题：`[owner/repo](url)` 或 `[Project Name](url)`
- 句中引用：`[Repo Name](url)` 或 ``owner/repo``（短引用用 inline code）
- 链接文字**避免**“点这里”、“按这个”

---

## 相关内部设计文件

这份 style-guide 讲“entry 怎么写”。为什么分这 5 个 branch、为什么是 8 个 stage 这类**设计理由**，见：

- [`branches/DESIGN.md`](../branches/DESIGN.md)—branch 设计笔记（为什么这样切、entry 该放哪）
- [`stages/DESIGN.md`](../stages/DESIGN.md)—stage 设计笔记（为什么这结构、动手练习 怎么挑）
- [`cli-agents-guide.zh-Hans.md`](cli-agents-guide.zh-Hans.md)—cross-cutting CLI agent 比较指南

## 修改本指南

这份指南本身也欢迎 PR。修改前请先开 Issue 讨论——术语决策影响 100+ 个 entry。

当前 maintainer：[@WenyuChiou](https://github.com/WenyuChiou)。

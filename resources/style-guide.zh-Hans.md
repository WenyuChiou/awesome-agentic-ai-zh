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

- `License`（SPDX ID 或标注例外，见 5）
- `推荐度`（⭐ × N，见 2）
- `教什么`、`适合谁`

### 必填字段（非 repo entry：article / course / video / protocol / documentation）
某些 entry 不是 GitHub repo 而是文章、视频、官方文件、catalog hub。对此类：

- `推荐度`（必填）
- `教什么`、`适合谁`（必填）
- `形式`（必填，标明是 `文章` / `视频` / `课程` / `精选列表` / `规格文件` 等）

范例：`Anthropic — Building Effective Agents` 博客文章用 `形式 = 文章` + 推荐度，不需要 repo 的 License 字段。

### 全站资源选择规则

推荐度是每个 entry 必填的编辑判断。

- 用现行官方文档、规范和 model card 核查事实。
- 用知名或广泛使用、可实作的 repo，给读者一条动手的路径。
- 热门程度只能用来发现候选，不能替代维护、License、安全或相关性检查。
- 每个 project 都要说明它教什么、适合谁，以及当前状态或限制。

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

这些是编辑评分，不是 GitHub stars。只有资源用途、质量或维护状态的查证结果改变时，才能连同理由调整评分。

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
| Gemini Notebook-like 工具 | 类 Gemini Notebook 的工具 / 类似 Gemini Notebook 的工具 |
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
先列出 1–3 个完成眼前练习真的会用到的来源。这些链接保持可见，不能只藏在折叠区。

1. [必要链接](url) — 会在哪一步用到
2. ...

<details markdown="1">
<summary>展开：完整阅读顺序与延伸来源</summary>

1. [延伸链接](url) — 描述
2. ...

</details>

## 🛠 动手练习（不是看过就好）

### 练习 N：标题
一句话描述完成后会看到什么。标题留在 details 外，让深链接可见。

<details markdown="1">
<summary>展开详细步骤</summary>

时间、费用、代码、预期输出与疑难排解。

</details>

可运行文件夹必须先提供可直接复制的 PowerShell 指令，再用默认收合的 `<details>` 提供 macOS/Linux 替代指令；同时提供 Path A 和 Path B 脚本，以及不调用 API 的 offline mock tests。SDK 依赖要限制 major version，cloud model 要使用钉住的 model ID；执行前必须验证不受信任的工具名称和参数。Cloud 成本写成 token 公式并标注核对日期，不要假设一个固定金额。不同 framework 的示例各自创建 Python 3.11 `.venv`，不要合并 requirements。测试必须走过核心行为；只验证 import 成功不算通过。

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

### 概念图写法

- 先在正文用白话定义核心词，再用图整理它们的关系；不要让图片成为读者第一次遇到术语的地方。
- 默认参考主页 README：奶油白底、深蓝主字、少量亮色、圆角卡片、简单线条 icon、充足留白和一个主要阅读方向。每张图只回答一个核心问题；信息太多时拆成两张，不缩小文字硬塞。
- 新画或重画的概念图用 Image 2.0 生成 PNG，不用临时 SVG 代替；旧图轮到该章重画时再套用，不一次迁移所有历史图片。
- 三语图保持相同画布比例、构图、共同网格、顺序、数字和限制，并分别提供正确语言的图片与 alt text。卡片位置、外边距、内边距和同层高度应一致。
- 图里的精确数字也要有官方依据。没有固定规则时，写“多个”“依模型而异”等诚实文字，不要为了好看造出范围。
- 箭头只走留白通道，不穿过文字、icon 或其他卡片；arrowhead、icon、标签和框线不得互相重叠。同层卡片使用共同网格、等高和一致内边距。
- 逐张以原始尺寸检查安全边距、文字、简繁字形、箭头、共同网格和对比；任何文字、icon、箭头或边框重叠都视为失败。最后运行 image-locale gate 和三语 MkDocs build。

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

含模型、价格、context、授权或生命周期状态的页面，把可见核查日期用小字放在受影响的表格或段落附近。只有该内容本身是补充资料时，日期才跟着收起；页首只保留不显示的机器 marker：

```markdown
<small>资料核查：YYYY-MM-DD UTC</small>

<!-- freshness: canonical=stages/0N-slug.md; verified_on=YYYY-MM-DD; scope=models,pricing,availability,deprecations; max_age_days=90 -->
```

日期只写核查范围与日期，不重复加入“资料不会永久正确”等通用提醒。三语 marker 必须完全一致；`canonical` 一律指向繁中主页。官方没有公布的字段写“官方未公布”，不要从第三方榜单反推；第三方 benchmark 只能教读者怎样自行评测。

**Stage 0 例外**：可以省略 `精选 Projects`、`进入条件`，因为它是 prerequisite gateway。可见主线依次保留跳过判断、4 个学习目标、1 个整合练习、18 项五星学习资源和简短完成检查；时间、环境、补充练习与名词默认收起。

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

### 角色路线页

完成回溯并加入 `scripts/reader-ux-pages.yml` 的角色页，在每个语系都保留可见主线 `📌 → 🎯 → 🧩 → 🛠 → 📚 → ✅`：先说明这条路线解决什么，再列学习目标、用粗体定义核心词、给出可复制的小任务、提供入口，最后做完成检查。先用白话定义核心词，再保留准确的英文术语；不能因为简化而删除后文会用到的技术词。

第一个任务必须小、可测试、可回滚。若任务会修改文件，要写清 read-only plan、人工批准、diff、test、rollback，以及 agent 不得自行 push／merge／deploy。必修阅读、精选项目、完整五星学习资源和安全警告保持可见；替代方案、费用、进阶流程和排错才放进默认关闭的 `<details markdown="1">`。专门的大型 catalog 可以让每个分类入口与安全边界可见，再让读者按分类展开其中上百项内容。把已有深链接的空 anchor 放到语意对应的新 heading 或 summary 旁，并保留可见的回到主路线链接。

工具的核心身份和 surface 分开写。IDE、CLI、desktop、cloud、CI、SDK 可以同时出现，不能当成互斥分类。OpenRouter 是 Provider／Router，Ollama 是 Model／Runtime，coding agent／harness 是另一条身份轴。

角色页的分组资源表遵守上面的 `rowspan` 规则。三种语系保留相同 URL 顺序、状态、授权、限制和稳定编辑评分（⭐⭐⭐–⭐⭐⭐⭐⭐）；不写易变的 GitHub stars。ELI5 白话仍须保留等价语意、技术名称和安全边界。

### Cookbook

Cookbook 的用途、选择表、核心词、六份 recipe 标题、成果、第一个可复制动作、必读、精选资源和完成检查应保持可见；九个完整步骤／替代路径／排错区块默认收合，使用闭合的 `<details markdown="1">`，且不得添加 `open`。每个核心词第一次出现时都要用粗体和通俗语言定义；不得把可执行命令或产品名称翻译成另一种东西。

完整资源表固定使用六个独立 `<tbody>`，分类单元格使用 `scope="rowgroup"` 和 `rowspan`。三种语言的 URL、命令、日期、许可证、安全边界和编辑评分必须一致。社区集成必须标明非官方、可能失效，并提供官方 fallback。易变事实附上核查日期，但不得承诺“永远最新”。

### Resources 工具柜入口

`resources/README*` 先问读者卡在哪里，再用粗体和白话定义 Reference、Guide、Cookbook、Catalog 与 Glossary。11 份 reference 的入口、用途、限制与回到主路线的链接保持可见；只折叠分文件的理由与 maintainer 规则。不要添加会变化的行数、GitHub stars，也不要把旧产品名称写成当前名称。

完整入口表固定使用五个独立 `<tbody>`，分类行数为 `4／2／2／2／1`。同类型只在第一行出现一次，使用 `scope="rowgroup"` 与真正的 `rowspan`；不能用重复文字或空白单元格假装合并。每种语言都链接自己的 mirror，并保持相同顺序与语意。

### Glossary 查词入口

Glossary 的快速地图、工具身份表、每个词的 heading 和一句白话定义保持可见；不能把最短答案藏进 `<details>`。只有 maintainer 完整分类表、来源与核查说明默认收合。核心词第一次出现在可见文字时继续用**粗体**标出，并保留准确的技术名称。

工具身份表必须分清 Provider API、Router、Model Runtime、Coding Agent／Agent Harness 与 Agent Framework。不要把容易变化的型号、价格、context 或固定 token 换算复制进 Glossary；改为链接有 freshness gate 的章节或官方文档。

### 内部链接
- Stage 之间：相对路径 `[Stage 4](./04-agent-frameworks.zh-Hans.md)`
- Branch ↔ README：`[← 回主路线](../README.zh-Hans.md)`
- 跨 stage 引用同一 repo：用全名 + 链接，不要只写“之前提过”

### 外部链接
- GitHub repo：`https://github.com/owner/repo` ✓ 不加 trailing slash
- 文章 / 部落格：完整 URL，标题用粗体
- 商业产品（Cursor、Make.com 等）：用官方网址，不是 affiliate
- 正文第一次提到 repo、规范或官方工具时，就加上超链接；不要让初学者看到裸露的 `owner/repo` 后还要自己搜索。完整资源表再补状态、授权、限制与评分。

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

这份指南本身也欢迎 PR。修改前请先开 Issue 讨论——术语决策会影响三语中的许多 entry。

当前 maintainer：[@WenyuChiou](https://github.com/WenyuChiou)。

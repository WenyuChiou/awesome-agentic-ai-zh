# 贡献指南

> [繁體中文](./CONTRIBUTING.md) | **简体中文** | [English](./CONTRIBUTING.en.md)

谢谢你考虑贡献。**这是一份精选的学习路线图，不是百科目录。质量 > 数量。**

这个 repo **本来就是设计给社群一起改良的**——一个人 curate 永远跟不上 AI agent 生态的变化速度。Maintainer 一个季度跑 1 次 review 不够，需要更多眼睛看。

这份 catalog 分**两条轨道**：**Track A**（CLI Power User，`tracks/cli/A1-A3`）跟 **Track B**（Agent Builder，`stages/03-07`）。贡献时请注明你动的是哪条轨道——两条的 audience 不一样。

## 🚪 第一次贡献：好上手的 5 个切入点

不确定从哪开始？挑一个你 30 分钟内能做完的：

1. **🐛 回报过时 entry**：跑 `python scripts/refresh-stars.py` 找星数差距大的 repo，开 issue 说“这个应该移除 / 更新”
2. **🔗 修一个失效连结**：你看 stage X 时连结 404 了，直接 PR 改
3. **✍️ 补一个 entry 的 `怎么跑` section**：很多 entry 没写安装指令，你跑过就补上
4. **🌏 补英文 companion 没翻好的句子**：找一个 `.en.md` 跟 zh 对照，你觉得翻得不顺的地方改一行
5. **💬 对某个 entry 加个人笔记**：你跑过 `练习 3` 卡某个地方，补一句“注意：xxx”

这 5 种都不用先读完整份 style-guide，merge 速度也快——适合第一次贡献、累积信心。

> 🧪 **想跑 walkthrough / build script / CI workflow 第一次？** 看 [`.github/TESTING-STATUS.md`](.github/TESTING-STATUS.md)——这份**诚实揭露**哪些 code maintainer 真的跑过、哪些只 syntax check、哪些完全没测。第一个踩到坑的人开 issue + PR 是 highest-value contribution。

## 我们接受什么

### 高价值 PR
- **新增 project** 到某个 stage，并说明为什么这个 project 对应该阶段的学习
- **翻译** 某个 stage 页面成繁中（只要繁中——我们不收 zh-Hans）
- **标记停滞 / 失维护的 project**（请先开 issue）
- **改善现有 project 的策展备注**（让“教什么”说明更清楚）
- **重新整理** 某个 stage 内部顺序，如果现在的顺序不符合学习进程

### 较低优先（仍然欢迎）
- 错字修正
- 连结修正（请先用 `curl -I` 验证）
- Stage 介绍文字优化

### 不接受
- 没有策展理由的批量加 repo
- 没有教学价值的自我推销
- 没文件的 project
- 没明确 license 的 project

## 怎么新增一个 project

每一个 project 在 stage 页面内应该照这个格式：

```markdown
### [Project Name](url)

| 栏位 | 内容 |
|---|---|
| 语言 | Python / TS / etc. |
| Stars | ★ k |
| License | MIT / Apache 2 / ... |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：核心学习一句话总结。

**适合谁**：谁应该读这个、为什么。

**备注**：1-3 句的个人评价。哪里好、哪里弱、哪里可以跳。

**怎么跑**：
\`\`\`bash
# 最小安装 / 第一次跑的指令
\`\`\`
```

## 策展标准

值得列入的 project 必须：

1. **有维护**：最近 6 个月内有 commit，或明确标示“stable, no longer maintained”
2. **有 hello-world 文件**：读者应该能在 30 分钟内把东西跑起来
3. **明确 license**：MIT、Apache 2、BSD 或类似。避免没 license 的 repo。
4. **可信赖的维护者**：知名组织、公司，或有口碑的个人

自动检查会合并同一个 repo 的重复链接，查看它是否搬家、归档、停用，以及 GitHub 显示的 SPDX license。半年没有 push 只是在提醒你再看一眼：稳定而且仍有教学价值的项目可以保留，但要把状态写清楚。如果 GitHub API 暂时无法回答，结果会标成“无法确认”，不会假装一切正常。

## 双语风格

- **繁中（Traditional Chinese, zh-TW）为正本**，英文版（`*.en.md`）是 companion。
- **不接受 zh-Hans PR**。如果你交 zh-Hans 的 PR，我们会请你转成繁中。
- **自然翻译**，不要逐字对译。技术词如果直接用英文比较自然，就保留英文（“使用 LangGraph 建 multi-agent 系统”）。
- **完整风格规范请看 [`resources/style-guide.zh-Hans.md`](resources/style-guide.zh-Hans.md)**——禁用词、entry schema、license 标注惯例、写作风格、推荐星等定义都在里面。PR 之前请先读。

## 流程

1. 新 project 或大幅重组请先开 issue
2. 一次一个 stage，PR 范围要聚焦
3. 等审查（通常 7 天）
4. Reviewer 可能会问你“为什么这个 project 教这个 stage”

## 要避免的反模式

- ❌ “leverage”、“delve”、“comprehensive”、“robust”（LLM tell）
- ❌ 过度行销（“revolutionary”、“game-changing”）
- ❌ 只因为热门就列上来
- ❌ 大段引用 project 自己的行销文案

## 担任 Stage / Branch 维护者

除了交一次性 PR，也欢迎担任**特定 stage 或 branch 的长期维护者**——负责定期 review、处理该领域的 issue、把关该领域的 PR。

自荐流程：

1. 开一个 issue，标题 `[maintainer] Stage N — your-handle` 或 `[maintainer] for-X branch — your-handle`
2. 讲清楚你愿意 commit 多久（建议至少一季 = 3 个月）
3. 简述你在这个领域的背景

详见 [`CONTRIBUTORS.md`](CONTRIBUTORS.md)。每个 stage / branch 的 maintainer 名单都在那边。

## License

贡献即代表你同意你的内容以 MIT 授权。

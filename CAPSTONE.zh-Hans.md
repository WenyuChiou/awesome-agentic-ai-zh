# 结业专题 / Capstone

> [繁體中文](./CAPSTONE.md) | **简体中文** | [English](./CAPSTONE.en.md)

走完一条轨道后,**自己做一个东西出来**——这份文件不是教学、不是 walkthrough,没有标准答案。它的用途是把“我读完 roadmap”变成“我有一个能展示的作品 + 一份自己给自己的评分”。

**怎么用这份文件**:

1. 选你**真的有的一个问题**(工作上、研究上、生活上),别挑玩具题目——capstone 的价值来自真实。
2. 对照你那条轨道的“进入条件”,确认该完成的 stage 都过了它的“自我检查”。
3. 做完后,用对应的 **rubric 自评**(四级:未达 / 基本 / 良好 / 优秀)。诚实打分比分数高更有用。
4. 想要反馈?把成品 + 自评贴到 [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions) 找人 peer review(可选,不强制)。

> 每一站“学什么 / 进入前要会什么 / 怎么算学会”一律以该 stage 文件内的“学习目标 / 进入条件 / 自我检查”为准;这份文件只定义**结业专题**本身。

---

## Track A Capstone — CLI Power User

**进入条件**：Stage 0–2 + A1 + A2 + Stage 5 的 Track A 核心 5.1–5.4 + A3 都通过自我检查。Stage 5 的 5.5–5.8 不影响入场。Stage 8 建议完成，但也不影响 Capstone 入场；Track A Capstone 聚焦 CLI 工作流。

**题目**:组一条**你会重复用**的 CLI-agent 工作流,把一件你现在手动做的事自动化。

**必要条件**(缺一不可):

- 用一个 CLI agent(Claude Code 或同类)当核心
- 至少接 **1 个** MCP server **或** 自写的 skill / command
- 有明确输入 → 产出可用的成品(不是“跟它聊天”)
- **能被别人重跑**:附 `怎么跑`(安装、设置、执行、预期输出)
- 处理至少 **1 种失败情况**(输入缺、API 失败、结果不对时会怎样)

**交付物**:一个文件夹 / repo,含成品 + `README` + 至少一次真实执行的证据(log / 截图 / 产出文件)+ 150 字内的反思(哪里卡、下次怎么改)。

**时间**:3–8 小时(不含学 stage 的时间)。

### Track A 评分 rubric(自评,四级)

| 维度 | 未达 | 基本 | 良好 | 优秀 |
|---|---|---|---|---|
| 问题真实度 | 玩具题 | 有点用 | 真实、会重复用 | 真实且有可量化指标(省时 / 减错次数等) |
| 工具运用 | 只用基本对话 | 用了 CLI agent | + MCP 或自写 skill/command | 多组件协作且选型有理由 |
| 可重现 | 只有自己跑得动 | 步骤不全 | 别人照 README 跑得起来 | 一键 / 全自动且有前置检查 |
| 韧性 | 一出错就崩 | 有提到风险 | 处理 1 种失败 | 多种失败有 fallback |
| 文件与反思 | 无 | 有 README | README 清楚 + 反思 | 反思具体可指出下一步改进 |

---

## Track B Capstone — Agent Builder

**进入条件**:Stage 0–8(含 Stage 3、4、5、6、7、7.5、8)都过了各自的自我检查。

**题目**:设计、实作、并**评测**一个解决具体问题的小型系统,二选一:

- **A. Multi-agent**:≥ 2 个分工协作的 agent,有编排逻辑;或
- **B. RAG 系统**:检索 + 生成的完整管线。

**必要条件**(缺一不可):

- 有 tool use
- 有一个对外 interface(CLI / API / chat 任一,对应 Stage 8)
- **有明确 evaluation**：准备一份有版本的 Eval suite，至少 5 个 development cases + 3 个 frozen holdout cases；写清楚成功条件、grader、trial 次数和 baseline，再量通过率／质性结果（这条不可省——这套课最容易跳过的就是“验证”）
- **失败模式分析**:写清楚它在什么情况会坏、你怎么知道
- 架构草图(一张图或一段文字说明组件与数据流)

**交付物**：程序 repo + 架构说明 + Eval 报告（dataset version、development／holdout、每题结果、trial 次数、baseline 与 regression）+ `README` + 200 字内反思（架构哪里判断错、重来会怎么改）。

**时间**:8–20 小时(不含学 stage 的时间)。

### Track B 评分 rubric(自评,四级)

| 维度 | 未达 | 基本 | 良好 | 优秀 |
|---|---|---|---|---|
| 问题定义 | 模糊 | 有目标 | 范围清楚、可验收 | 清楚且说明为何值得做 |
| 架构 | 无设计 | 能跑就好 | multi-agent / RAG 选型有理由 | 设计权衡写得出来 |
| 实作正确性 | 跑不动 | 主流程能跑 | 边界情况也处理 | 稳定且程序可读 |
| **评测严谨度** | 没测 | 手动试几次 | 有版本化 development／holdout cases、成功条件和 grader | 多次 trials、baseline 对照、回归可重跑且 holdout 没有用于调参 |
| 韧性与失败分析 | 无 | 提到风险 | 具体失败模式 | 失败有侦测 + 缓解 |
| 接口与文件 | 无 | 能跑 | interface + README 清楚 | 别人能直接用 |
| 反思 | 无 | 一句话 | 具体(指得出架构或组件选择的具体问题) | 指得出架构级的下一步 |

---

## 依身份选题(audience flavor)

同一个 capstone,换你的场景就好——不用另外做:

- 🔬 **researcher**:文献问答 / 实验 log 整理 / 数据预处理 agent
- 💻 **developer**:CI 内的 review/triage agent / repo 问答 / 自动化 release note
- 🎓 **teacher**:出题 + 评分辅助 / 教材改写 / 课程问答(注意学术诚信边界)
- 📊 **knowledge-worker**:会议记录 → 行动项 / 跨文件汇整 / 周报初稿
- 👥 **everyday-user**:个人数据汇整 / 行程与提醒 / 重复杂务自动化

---

## 怎么展示

- 贴到 [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions) 的对应分类,附成品链接 + 你的 rubric 自评。
- 放进你自己的 portfolio / GitHub;描述用具体事实(做了什么、量到什么),**避免**“最强 / 全世界最好”这类话术。
- 想替别人 review:照对方那条轨道的 rubric 给反馈,对事不对人。

> 这份文件只定义结业专题与评分标准。各 stage 的学习内容与通过条件,仍以该 stage 文件为准。

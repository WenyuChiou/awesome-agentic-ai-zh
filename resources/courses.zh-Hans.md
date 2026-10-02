# AI Agent 课程地图：先学会，再决定要不要拿证书

> [繁體中文](./courses.md) | **简体中文** | [English](./courses.en.md)

<!-- freshness: canonical=resources/courses.md; verified_on=2026-08-29; scope=course-availability,cost,certificate,assessment,repository-status; max_age_days=90 -->

这一页帮你做一件事：**从很多课程里，挑一门真正适合现在的你。** 不必先收集证书，也不必一次报名五门。先选一门，做出一个可以展示的作品，再走下一步。

想照着本项目一步一步实践，回到[主学习路线](../README.zh-Hans.md)；遇到陌生术语，可以查[术语表](glossary.zh-Hans.md)。

## 🧩 先分清五个容易混在一起的词

| 核心词 | 五岁也能懂的说法 | 正确意思 |
|---|---|---|
| **Course（课程）** | 老师排好了一条学习路线。 | 一组按顺序安排的视频、文章、练习或项目。 |
| **Certificate of Completion（完成证书）** | 证明你走完了这门课。 | 证明你完成了指定内容；不等于学位，也不能单独证明你已经能做 production 系统。 |
| **Skill Badge（技能徽章）** | 一张小贴纸，表示你做过某项任务。 | 平台针对短模块或特定技能发放的数字徽章。 |
| **Professional Certificate（专业课程证书）** | 好几门课程装成一个更大的学习包。 | 由公司或学校设计的系列课程证书；通常仍不是学位或执照。 |
| **Certification Exam（认证考试）** | 不只是上课，还要另外参加考试。 | 由供应商或考试机构验证特定产品知识的考试；可能需要付费、验证身份或定期更新。 |

**最重要的规则：证书证明你完成了一条路；作品才让别人看到你会做什么。**

## ⚡ 先选一条，不要全部一起读

| 你现在想做什么 | 先选这个 | 为什么 |
|---|---|---|
| 完全不知道从哪里开始 | [Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course) | 免费，先教 Agent、工具和基本框架，再做挑战。 |
| 想看大量可执行代码 | [Microsoft AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners) | 每课都有文字、视频和代码；但示例偏向 Microsoft Agent Framework。 |
| 想读完整的中文教材 | [Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents) | 从原理一路讲到 RAG、Multi-Agent、MCP 和部署。 |
| 想先学不绑定框架的设计方法 | [DeepLearning.AI Agentic AI](https://www.deeplearning.ai/courses/agentic-ai/) | 从零实践 reflection、tool use、planning、eval 和 multi-agent。 |
| 已经决定使用 Claude／LangGraph | [Claude Academy](https://academy.claude.com/)／[LangChain Academy](https://academy.langchain.com/courses/intro-to-langgraph) | 直接学习供应商的现行工具；记得把通用概念和产品按钮分开。 |
| 主要目标是系列证书 | [IBM](https://www.coursera.org/professional-certificates/ibm-rag-and-agentic-ai)／[Vanderbilt](https://www.coursera.org/specializations/ai-agents) | 这是较长的付费系列课程；先确认费用、语言和项目是否符合需要。 |

## 🎯 精选课程与学习路线

星等是本项目的**编辑推荐度**，不是证书排名：⭐⭐⭐⭐⭐ 适合当主线；⭐⭐⭐⭐ 很值得学习，但更偏向特定工具或目的；⭐⭐⭐ 适合已经确定使用该供应商的人。

<table>
  <thead>
    <tr><th scope="col">学习目的</th><th scope="col">课程／教材</th><th scope="col">语言与费用</th><th scope="col">你会做出什么</th><th scope="col">证书／限制</th><th scope="col">推荐度</th></tr>
  </thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">免费打基础</th><td><a href="https://huggingface.co/learn/agents-course">Hugging Face — AI Agents Course</a></td><td>以英文为主；免费</td><td>认识 Agent Loop，实践 smolagents、LlamaIndex、LangGraph、Agentic RAG 和 Eval。</td><td>Unit 1 测验达到 80% 可取得基础完成证书；完整路线还包括作业和最终挑战。</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/microsoft/ai-agents-for-beginners">Microsoft — AI Agents for Beginners</a></td><td>多语言；免费开源</td><td>用文字、视频和 Python／.NET 示例来做工具、记忆、规划、RAG、Multi-Agent 和部署。</td><td>没有 Certificate of Completion；现行示例偏向 Microsoft Agent Framework 和 Foundry。</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/datawhalechina/hello-agents">Datawhale — Hello-Agents</a></td><td>简体中文；免费开源</td><td>从 Agent 原理和经典 pattern，一路做到 RAG、记忆、Multi-Agent、MCP 和完整项目。</td><td>没有 Certificate of Completion；章节很多，请按自己的问题选读，不必一次读完。</td><td>⭐⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">构建与上线</th><td><a href="https://www.deeplearning.ai/courses/agentic-ai/">DeepLearning.AI — Agentic AI</a></td><td>英文；视频可免费旁听</td><td>从零实践 reflection、tool use、planning、Multi-Agent、错误分析和 component Eval。</td><td>测验、graded assignments 和证书需要 Pro；免费旁听不包含证书。</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://academy.claude.com/">Claude Academy</a></td><td>英文；免费</td><td>按需要学习 Claude API、Claude Code、MCP、Agent Skills 和 Subagents。</td><td>通过课程 quiz 可以取得免费完成徽章；这是 Claude 产品路线，不取代通用 Agent 基础。</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://academy.langchain.com/courses/intro-to-langgraph">LangChain Academy — Introduction to LangGraph</a></td><td>英文；免费</td><td>实践 graph、state、memory、HITL、subgraph、deployment 和 long-term memory。</td><td>偏向 LangGraph／LangSmith；当前公开课程页面没有清楚列出证书门槛。</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://www.kaggle.com/learn-guide/5-day-agents">Google × Kaggle — 5-Day AI Agents Intensive</a></td><td>英文；免费自学</td><td>通过模型、工具、orchestration、memory 和 Eval 理解 Agent，然后完成 capstone。</td><td>原本是限时 intensive，现在作为自学 guide 使用；不要把 cohort 活动资格当成永久证书。</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">较长的系列课程</th><td><a href="https://www.coursera.org/professional-certificates/ibm-rag-and-agentic-ai">IBM — RAG and Agentic AI Professional Certificate</a></td><td>英文；付费订阅，可查看助学选项</td><td>通过多门课程完成 RAG、Agentic AI、工具、向量数据库和实践项目。</td><td>IBM／Coursera 系列证书；不是学位，费用和可用的助学支持因地区和账号而异。</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://www.coursera.org/specializations/ai-agents">Vanderbilt — AI Agent Developer Specialization</a></td><td>英文；付费订阅，平台提供多语言字幕</td><td>使用 Python、工具、记忆和 Agent architecture 完成一组应用项目。</td><td>Vanderbilt／Coursera Specialization 证书；部分内容偏向 OpenAI 工具。</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">中文供应商路线</th><td><a href="https://www.nvidia.cn/training/certification/generative-ai-llm-learning-path/">NVIDIA — 中文 Agentic AI 学习路径</a></td><td>简体中文；自学和讲师带领的课程大多收费</td><td>依次学习 RAG Agent、Agentic AI 应用、评估和 production deployment。</td><td>部分课程授予 DLI 培训证书；价格和排课以官方页面为准，内容偏向 NVIDIA stack。</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://edu.aliyun.com/certification/cldm02">阿里云 — 基于百炼平台构建智能体应用</a></td><td>简体中文；目前可以免费启用</td><td>制作低代码智能体、工作流和智能体编排，并连接网站、钉钉等场景。</td><td>完成学习和考试后领取 Clouder 证书；需符合官方网站列出的身份证明文件条件，并且绑定百炼平台。</td><td>⭐⭐⭐</td></tr>
  </tbody>
</table>

想用中文伴读 DeepLearning.AI，可以接着看 [Datawhale 的开源整理](https://github.com/datawhalechina/agentic-ai)。

## 🧪 每学完一门课，都留下同一份作品证据

不要只下载 PDF。直接复制这张小卡，为每门课程留下可检查的成果：

```text
我解决的问题：
Agent 可以使用的工具：
我怎么知道它做对了：
失败时怎么安全停止：
可执行代码或 Demo 链接：
```

最小作品可以只是一个会查资料、调用一个工具、留下 Eval 结果的小 Agent。完成后再回到本项目，对照 [Stage 3 工具使用](../stages/03-tool-use-and-hello-agent.zh-Hans.md)、[Stage 4 Workflow Graph](../stages/04-agent-frameworks.zh-Hans.md) 和 [Stage 7 上线工程](../stages/07-multi-agent-production.zh-Hans.md)。

<details markdown="1">
<summary>📜 展开：证书到底能证明什么？</summary>

1. **完成证书只证明完成了指定步骤。** 它不是学位，也不保证你能独立上线 Agent。
2. **Certification Exam 和完成证书不同。** 前者可能需要监考、身份验证和另外付费；不要把免费课程徽章写成专业执照。
3. **免费不等于差，付费也不保证适合。** 先看课程有没有练习、Eval、项目和现行文档。
4. **履历上也要放作品。** 诚实写清楚“完成了什么、做出了什么、怎么测试”，不要只贴一排徽章。
5. **课程会变化。** 报名前重新确认费用、证书门槛、语言，以及需要的 API／云账号。

</details>

<details markdown="1">
<summary>🔎 展开：这份清单如何维护？</summary>

- 先查看课程或供应商的官方页面，再看官方 repository；第三方文章只能作为线索。
- 星等评的是教学价值、实践完整度、更新状态和可迁移性，不评“哪张证书更容易帮你找到工作”。
- 不列入只有营销页面、无法确认课程大纲，或把一般完成证书包装成执照的项目。
- repository 的 stars 只用来发现社区关注度，不写进正文；维护状态要看是否封存、最近更新和现行文档。
- 费用、证书或 cohort 发生变化时，三种语言和测试要一起更新。

- 2026-10-02：W&B AI Engineering: Agents 暂时移出现行推荐。旧入口返回 404，新入口目前无法打开。这不代表永久停课；确认可用的官方课程入口后再评估。

</details>

<small>资料核对：2026-08-29 UTC。</small>

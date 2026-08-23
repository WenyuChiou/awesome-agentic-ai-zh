# Stage 6 — 上下文管理（Context Engineering）：RAG 与 Memory

> [繁體中文](./06-memory-rag.md) | **简体中文** | [English](./06-memory-rag.en.md)

⏱ **时间估算**：2 周（约 10 小时）

> 💡 这个 stage 用语密度高（**RAG / 向量数据库 / embedding / chunking / hybrid search / reranking...**）→ 不熟先翻 [`resources/glossary.zh-Hans.md` 3](../resources/glossary.zh-Hans.md#3-memory--retrieval--rag)。
>
> 📋 **本章组成**：定位 → 入口 → **RAG 主轴**（基础 + 进阶 + DSPy + Eval）→ **Bridge** → **Memory 主轴**（3 pattern + trio + 进阶）→ Chunking → Reflexion / Reasoning → 练习 → Projects
>
> 🔑 **关键术语**：见 [`resources/glossary.zh-Hans.md` 3](../resources/glossary.zh-Hans.md#3-memory--retrieval--rag)（memory / RAG / embedding / chunking / reranking）

本 stage 的核心不是“多背一点术语”，而是理解 agent 如何管理 context。

- **RAG 解决的是**：现在要从外部知识库查哪些资料？
- **Memory 解决的是**：agent 应该跨对话、跨 session、跨任务记住什么？
- **Context Engineering 是更上层的问题**：每次 LLM call 前，该把哪些信息组进 prompt，才能让模型在有限 context window 里做出正确决策？

→ 接着 Stage 7 五层工程分工：**Prompt = 单次怎么问 / Context = 这次该给哪些信息 / Harness = 整个 agent system 怎么跑起来 / Loop = 让它自己跑完 / Graph = 把流程摊开**。本 stage 是第 2 层。

### Agent 需要的两种 context 能力

1. **Retrieval**：从外部知识库找出和当前任务相关的资料。
2. **Memory**：保留跨对话、跨 session、跨任务的状态、偏好与经验。

**RAG（Retrieval-Augmented Generation）** 是当前最常见的 retrieval 架构；**Memory** 负责让 agent 记住用户、任务历史与自己的过去经验。这一章会把两者分开讲，避免把“查资料”和“记事情”混在一起。

### 先把名词切开：Retrieval / RAG / Vector Store / Memory 不是同一件事

| 名词 | 不要混淆成 | 白话解释 |
|---|---|---|
| **Retrieval** | RAG 全部 | 找资料这个动作 |
| **RAG** | Vector DB | retrieve + generate 的完整流程 |
| **Embedding** | Memory | 把文本转成向量，方便做相似度搜索 |
| **Vector store** | RAG | 存储与搜索 embedding 的地方 |
| **Chunking** | Retrieval 本身 | 把文档切成适合被搜索的片段 |
| **Memory** | RAG | agent 对用户、任务与过去经验的持久管理 |

## 🎯 Context Engineering 是什么（先定位）

**一句话**：Context Engineering = 决定 **每次调用 LLM 时，要把哪些信息塞进它看得到的窗口（context window）**。

重点不是“开了几次对话”，而是“**每次对话里塞了什么**”。Karpathy 2025-06 的[原推文](https://x.com/karpathy/status/1937902205765607626)说得最准确：这是一门把 **刚好对下一步有用的信息** 填进窗口的精细艺术。

📺 **视觉学习**：[李宏毅 2025 第 2 讲 — Context Engineering：AI Agent 背后的关键技术](https://www.youtube.com/watch?v=lVdajtNpaGI)（NTU 生成式人工智能与机器学习导论 2025）

### 在五层 stack 里的位置

![Agent 工程五层 Stack](../resources/diagrams/agent-engineering-5layer.zh-Hans.png)

详细对照表见 [Stage 7 五层工程分工](07-multi-agent-production.zh-Hans.md#五层工程分工prompt--context--harness--loop--graph)（分层的 canonical 出处）。

### 本 stage 处理 4 个 sub-problem 中的 2 个（Lance Martin 2025 框架）

| Sub-problem | 解决什么 | 具体例子 | 本 stage cover？ |
|---|---|---|---|
| **Select** | 要把 **哪些** 外部信息捞进窗口 | user 问“我家附近哪间 cafe 好吃”→ 从 Yelp DB 捞 3 家评分高的 → 塞进 prompt | ✅ 主轴（RAG / vector search / GraphRAG） |
| **Write** | 要把 **哪些** 互动 / 教训写进长期记忆 | user 上周说“我吃纯素”→ 写进 memory；这周又问餐厅推荐时，retrieve 出来避免推肉食 | ✅ 主轴（memory layers） |
| **Compress** | 对话太长怎么压 | 50 轮对话超过 200k token → 自动摘要前 40 轮、保留最后 10 轮原文 | ⚠️ 部分（这里 + Stage 7 Harness `context manager`） |
| **Isolate** | 多 agent 各自窗口怎么分 | supervisor 看全局、worker 只看自己那段，彼此不串扰 | ❌ Stage 7 multi-agent 处理 |

### 四个常被混淆的概念

| 名词 | 是什么（抽象 / 具体） | 示例工具 |
|---|---|---|
| **Memory** | agent 跨对话 / 跨 session 记事情的 **能力**（抽象概念） | LangChain ConversationBufferMemory / mem0 / Letta |
| **Embedding** | 把文本转成 N 维 **向量**，让相似度可计算（数据转换） | `sentence-transformers` 跑出 768 维向量 / OpenAI ada-002 |
| **Vector DB** | 存 + 查 embedding 的 **存储层**（基础设施） | Chroma / Qdrant / Weaviate / pgvector |
| **RAG** | “retrieve 相关片段 → 塞进 prompt → 生成”这个 **pattern**（架构模式） | LlamaIndex / LangChain RAG chain |

→ **核心区分**：Memory 是 **能力**，Embedding 是 **数据转换**，Vector DB 是 **存储**，RAG 是 **架构 pattern**。这四个概念常被混用，但实际属于不同层级。

### RAG vs Long Context vs Fine-tuning — 何时用什么

让 LLM 用上你的私有 / 领域数据，主要有 3 种做法。**本 stage 教 RAG**，但你也要知道什么时候不该用：

| 选择 | 适合 | 不适合 | 成本 |
|---|---|---|---|
| **RAG**<br>（外部 retrieve） | 大型 / 变化快 / 私有知识库、需要 citation 的场景 | 推理要整份文档一起看、需要跨文档 multi-hop reasoning | 每次 query 多一次 vector search latency |
| **Long Context**<br>（直接塞进 prompt） | 200k token 以内的中型文档、一次性查询、需要 cross-doc reasoning | 知识库很大 / 经常变化 / 想保留 citation | 每次 query 都要烧大量 input token，即使有 prompt caching 也是如此 |
| **Fine-tuning**<br>（改 model weights） | 风格 / 格式统一、特定领域语言（医疗、法律、代码） | 知识会变化、需要 citation、不想训练模型 | 训练成本 + 维护成本 + 模型 lock-in |

→ **怎么选**：先试 RAG（成本最低、变化最容易跟上）→ RAG 不够再考虑 Long Context → 两者都不行再考虑 Fine-tuning。**进 Stage 7 学 fine-tune deploy。**

## 📌 学习目标

- 建一条基础 RAG 流水线（chunk → embed → store → retrieve → generate）
- 看出 RAG 该用在哪些地方、又不该用在哪些地方
- 区分 working memory、long-term memory、episodic memory、semantic memory、procedural memory
- 理解 vector embedding 与相似度搜索
- 知道进阶 RAG（GraphRAG / Contextual Retrieval / Hybrid Search）何时加、何时不加

## 🚪 进入条件

你应该已经：

- 完成 Stage 3（会写 tool use、会调用 LLM API、能看懂 ReAct loop）—— **硬性技术前置**
- 走过 Stage 4（agent frameworks）+ Stage 5（Claude Code 生态）—— curriculum 主线是 **3 → 4 → 5 → 6**（见 [README 学习地图](../README.zh-Hans.md#-学习地图两条学习路径)）；非硬性技术前置，但 RAG / memory 常跟 framework + Claude Code memory 机制搭配、照顺序走过理解更完整，且 [Stage 7](07-multi-agent-production.zh-Hans.md) 预期你已完成 4 + 5 + 6
- 能够运行 Python `pip install` 来安装 SDK（后续练习会用到 `chromadb`、`sentence-transformers` 等）
- 熟悉 list / dict / generator 等基础 Python 结构

如果没有达到，请回看 [Stage 3](03-tool-use-and-hello-agent.zh-Hans.md) 或 [Stage 0 环境设置](00-foundations.zh-Hans.md#何时可以跳过这个阶段)。

## 📚 必读材料

1. [**LlamaIndex — RAG concepts**](https://docs.llamaindex.ai/en/stable/getting_started/concepts/) — 最清晰的入门。
2. [**LangChain — RAG tutorial**](https://python.langchain.com/docs/tutorials/rag/) — 实战操作。
3. [**Pinecone — Learning Center**](https://www.pinecone.io/learn/) — Vector DB 基础。
4. [**Anthropic — Contextual Retrieval**](https://www.anthropic.com/news/contextual-retrieval) — Anthropic 结合 prompt caching 的 RAG 写法。
5. [**LangChain — Text Splitters**](https://docs.langchain.com/oss/python/integrations/splitters/index) — Chunking 策略入门。

> 🙏 **Memory 章节特别推荐 [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)**: 本阶段探讨 memory 的概念和初步实现，需要 **chapter-length 的深入版本**请参考 hello-agents 的对应章节——short-term / long-term memory 的差异、context engineering 的动态组装、session 持久化、forgetting strategy 都讲得最完整。本阶段是路线图，那边是深度教材。

## 🧭 单元指引（渐进式流程）

本章按 **RAG 先学、Memory 后学** 的顺序进行——RAG 是 context engineering 最基础、最常用的工具，而 Memory 是 agent 跨对话/跨 session 的能力；先跑通 RAG pipeline，再引入 Memory 设计，最后回头看 Chunking 的细节。

**推荐阅读顺序**:

1. **🌐 RAG 基础流水线**（下一节）— 建立心智模型。
2. **🚀 进阶 RAG 技巧** — GraphRAG / Contextual Retrieval / Hybrid Search 等生产环境升级。
3. **🌉 从 RAG 到 Memory** — 为什么 RAG 还不够，Memory 弥补了哪些部分。
4. **🧠 Memory 设计** — 短期 vs 长期、3 种模式、CoALA 框架。
5. **🧩 Chunking 细节** — 深入探讨 RAG 和 Memory 都会用到的技术。

阅读本章时，可以思考：RAG 不适用于哪些应用场景？哪些场景适合 RAG，但基础 RAG 表现不够好？这将引导你了解后续的 GraphRAG / Self-RAG / RAPTOR 等进阶技术。

## 🌐 RAG 基础流水线

**RAG（Retrieval-Augmented Generation）**= “retrieve 相关片段 → 塞进 prompt → 生成” 这个模式。可以把它想象成在为 agent 构建一个图书馆——你需要先把书放好、分类好，后续查询资料时，才能又快又精准。

**最基础的 RAG 分成两条流水线**：

- **数据预处理（Ingest 一次）**：ingest → chunk → embed → store（index）。这一步是在构建可检索的知识库。
- **检索生成（每次 Query）**：retrieve → generate。这一步是在用户提问时，找出相关内容，然后交给 LLM 生成回答。

![RAG Pipeline Overview](../resources/diagrams/rag-pipeline-overview.zh-Hans.png)

图中的 RAG Fusion、query rewrite 等属于进阶检索技巧。**第一次学习 RAG 时，先理解主线流程即可**。

**5 个步骤解读**：

| Step | 做什么 | 在哪条 Pipeline | 技术细节在哪里 |
|---|---|---|---|
| **1. Ingest** | 加载数据（PDF / web / DB） | 预处理 | LlamaIndex / LangChain 各自的 loader |
| **2. Chunk** | 将文档切分成小块（500-2000 token / chunk） | 预处理 | 见后文 🧩 Chunking 细节（先阅读 RAG / Memory 主体章节，技术深入留到后面） |
| **3. Embed** | 将每个 chunk 转换为 N 维向量 | 预处理 | `sentence-transformers` / OpenAI ada-002 |
| **4. Store** | 将向量 + 元数据存储进 Vector DB | 预处理 | Chroma / Qdrant / pgvector |
| **5. Retrieve + Generate** | 对 Query 进行 embedding → top-k 语义搜索 → 拼接到 prompt → LLM 生成回答 | 每次 Query | 通用 LLM API |

以上只是最小骨架。**最常踩的 3 个坑**：

- **Chunk 太大 / 太小**：太大，检索到的 chunk 里可能只有一句相关，其他是杂讯；太小，会失去上下文（见 Chunking 细节）。
- **Embedding model 选错**：中文文档用英文 model，检索精度直接掉一半。
- **top-k 设太大 / 太小**：太小，可能漏掉 relevant chunk；太大，杂讯高 / token 消耗大。

> 📚 **想看更多 RAG 踩坑指南 + 解法**：[NirDiamant/RAG_Techniques](https://github.com/NirDiamant/RAG_Techniques) ★ 大型 Production RAG Cookbook，包含 30+ 技巧 + Jupyter notebook 示例。

> 📄 **RAG 真正常挂的两个地方，别只顾 chunking**：(1) **解析（ingest）**——PDF→干净 markdown 是 garbage-in 的源头：[docling-project/docling](https://github.com/docling-project/docling)（★ 64k+、MIT）、[opendatalab/MinerU](https://github.com/opendatalab/MinerU)（中文 / 科学 PDF 强，**AGPL** 注意授权）、[microsoft/markitdown](https://github.com/microsoft/markitdown)（★150k+、MIT）。(2) **选嵌入模型**——第一个检索质量决策，别瞎挑：看 [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard)，中文 / 多语常用 [BGE-M3](https://github.com/FlagOpen/FlagEmbedding)（★12k、MIT）。

跑完基础骨架后，先跑 动手练习 1-4（embeddings / vector DB / chunking / 完整 pipeline）建立手感，再进入下一节 进阶 RAG 技巧。

## 🚀 进阶 RAG 技巧（跑完基础 RAG 之后再看）

下面六个 subsection 是 2024-2026 年 production RAG 最常添加的优化手段，按“添加到 Pipeline 的哪一层”分组：

- **Retrieve 之后** —— GraphRAG / Contextual Retrieval / Hybrid Search & Reranking
- **Retrieve 之前**（Query 改写）—— Query Transformations
- **Retrieve 期间**（控制流程）—— Adaptive / Agentic RAG
- **索引结构** —— RAPTOR
- **2024-2026 概览** —— 其他 17 个值得了解的技巧

**先跑完上述 RAG 基础版本，建立基准后，再回头看这里**——否则你可能会在没有基准的情况下调参，永远不知道是哪个改动带来了提升。

| 技巧 | 解决什么问题 | 添加到 Pipeline 的哪一层 | 成本 |
|---|---|---|---|
| **GraphRAG** | vanilla RAG 无法进行 multi-hop / 跨文档的 entity-relation 推理 | Retrieve 前（构建 graph）+ Retrieve 时（graph traversal）| 高（需要构建 KG，LLM 抽取 entity 的 token 成本高）|
| **Contextual Retrieval** | Chunk 丢失了原始文档的上下文，检索到错误的片段 | Chunk 之后 / Embed 之前（添加 contextual header）| 中等（一次性 ingest 成本，搭配 prompt caching 后成本降低 90%）|
| **Hybrid Search & Reranking** | 纯 vector 搜索会遗漏字面匹配，top-k 结果杂讯多 | Retrieve 期间（结合 BM25）+ Retrieve 之后（cross-encoder rerank）| 低（成熟工具可直接集成）|

### 🔗 GraphRAG — 知识图谱 + RAG

**心智模型**: vanilla RAG 将文档切分成 chunk，依赖 embedding 相似度进行检索——但**它不知道哪些 entity 是同一个东西，以及 entity 之间有什么关系**。GraphRAG 在 ingest 阶段先用 LLM 将文档抽取成 **(entity, relation, entity)** 三元组来构建知识图谱，检索时除了向量比对，还会进行 graph traversal 来查找“相关 entity 的相关 entity”。

**何时使用**:

- 任务需要 **multi-hop reasoning**（需要 A → B → C 才能回答）。
- 跨多个文档，实体互相引用（公司财报、论文引用、调查报告、法律案例）。
- 问题形如“X 影响了什么 Y，Y 又连接到哪些 Z”——vanilla RAG 通常只能检索到与 X 相关的文档片段。

**何时不使用**:

- 文档之间没有实体-关系链接（纯 FAQ、产品手册各自独立）。
- 知识库规模小（< 1k chunks）——vanilla RAG 已足够。
- 预算紧张——构建 KG 的 token 成本可能是普通 RAG 的 10-50 倍。

**代表性框架**:

- [**HKUDS/LightRAG**](https://github.com/HKUDS/LightRAG) ★ **35.1k** MIT EMNLP 2025 — 目前社区最热门的选择，轻量级，KG + vector hybrid，成本低于 Microsoft 的版本。
- [**Microsoft GraphRAG**](https://github.com/microsoft/graphrag) — 原始参考实现，Apache-2.0 许可，包含社区检测功能。
- [**gusye1234/nano-graphrag**](https://github.com/gusye1234/nano-graphrag) — < 1000 行代码的最小实现，适合先理解原理。

**论文**: [**From Local to Global: A Graph RAG Approach to Query-Focused Summarization (Edge et al. 2024)**](https://arxiv.org/abs/2404.16130) — Microsoft GraphRAG 的原始论文，解释了 community summarization 如何解决全局查询问题。

### 🪶 Contextual Retrieval — Anthropic 的 Prompt Caching 解决方案

**心智模型**: vanilla chunk 会丢失原始文档的上下文——一个 "Q3 revenue grew 15%" 的 chunk 被提取出来后，你不知道是**哪家公司**、**哪一年**的 Q3。Anthropic 在 2024 年提出：在 ingest 阶段，使用 LLM 为每个 chunk 编写一段 50-100 token 的**上下文头部（contextual header）**（例如：“This chunk is from ACME Corp 2024 Q3 earnings, discussing the cloud segment...”），然后将其拼接到 chunk 前面再进行 embedding。结合 **prompt caching**，可以将“整个文档 + 每个 chunk”的 prompt 只计费一次，后续所有 chunk 共用缓存。

**何时使用**:

- Chunk 的字面意思与其原始文档主题相差较远（如：财务报告、研究论文、长篇叙事文档）。
- 你愿意支付一次性的 ingest 成本，以换取更高的检索精度。
- 你正在使用 Claude 或计划使用 prompt caching（其他模型也能运行此方法，但没有缓存折扣）。

**何时不使用**:

- Chunk 本身是自包含的（如：FAQ、产品介绍页、定义条目）。
- 知识库频繁变动（每次更改都需要重新 ingest）。
- 预算极其紧张——即使有缓存折扣，ingest 成本仍比 vanilla 高。

**为何能节省 90% 的成本**: Anthropic 的报告显示，prompt caching 将成本降低到约 1/10，因为它将整个文档视为缓存的前缀，每个 chunk 只发送差异部分。但**这仅节省了 ingest 成本，并未节省 retrieve 阶段的成本**。

**代表性实现**:

- [**Anthropic — Contextual Retrieval Blog**](https://www.anthropic.com/news/contextual-retrieval) ⭐ — 官方说明 + benchmark（失败的检索率从 5.7% 降至 1.9%）。
- [**Anthropic Cookbook**](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) — 端到端的 Jupyter notebook，包含 prompt 模板。

**配套技巧**: Anthropic 的同一篇博文还建议结合 **Contextual BM25**（将上下文 chunk 与 vector + BM25 同时喂入）+ **reranking**——这正好引出了下一节 Hybrid Search & Reranking。

### 🎯 Hybrid Search & Reranking — Production RAG 的两个常见强化组件

**心智模型**:

- **Hybrid Search** = 结合了 vector 相似度（语义匹配）和 BM25 / keyword 搜索（字面匹配），使用 [RRF (Reciprocal Rank Fusion)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) 等方法融合分数。解决了纯 vector 搜索“查询与 chunk 同义但用词不同导致未检索到”以及“人名 / 编号 / 罕见词的语义 embedding 较弱”的双重盲点。
- **Reranking** = 第一阶段检索 **top-50** 个 chunk（优先考虑召回率，宽松地捞取）→ 然后使用 **cross-encoder reranker** 重新评分并排序出 **top-5** 个（优先考虑精确率，精细筛选）。Cross-encoder（将 query + chunk 一起送入模型）比 bi-encoder（query / chunk 分开 embedding）精度高很多，但速度较慢，因此只在第二阶段使用。

**为什么是“必加优化”**: Production RAG 的评估几乎一致表明，添加 hybrid search + reranker 后，recall@5 通常从 70% 上下提升到 85-90%，边际成本低，且工具成熟。**这是性价比最高的两个改动**。

**何时使用**:

- Production RAG（非 demo / 练习）。
- 查询包含人名、产品编号、技术术语、罕见词（纯 vector 搜索容易漏）。
- 预算允许每查询增加 100-300ms 的延迟。

**何时可以暂缓**:

- 实验阶段 / MVP（先跑通 vanilla RAG）。
- 预算极紧 / 对延迟极其敏感（reranker 需要额外的模型调用）。

**代表性工具**:

- **Hybrid Search**: [Weaviate](https://github.com/weaviate/weaviate)（内置 BM25 + vector + RRF）/ [Qdrant](https://github.com/qdrant/qdrant)（支持 sparse + dense vector）/ pgvector + Postgres FTS。
- **Rerankers**: [Cohere Rerank API](https://docs.cohere.com/docs/rerank-overview)（商业版，最常用）/ [BGE Reranker](https://huggingface.co/BAAI/bge-reranker-large)（开源版，HuggingFace，中文表现较好）/ [Jina Reranker](https://jina.ai/reranker)。
- **框架内置**: LlamaIndex 的 `SentenceTransformerRerank` / LangChain 的 `ContextualCompressionRetriever`。

**论文 / 入门**:

- [**Pinecone — Rerankers and Two-Stage Retrieval**](https://www.pinecone.io/learn/series/rag/rerankers/) — 对 reranker 心智模型讲解最清晰。
- [**Anthropic — Contextual Retrieval**](https://www.anthropic.com/news/contextual-retrieval)（上面已列）— 同时演示了 hybrid + reranker，并包含 benchmark。

### Query Transformations — HyDE / Multi-Query / RAG Fusion

**心智模型**: vanilla RAG 将用户查询直接 embedding 后进行检索——但查询的用词、风格或抽象层级经常与文档差异很大（例如：用户问“我胃痛怎么办”，文档写“上腹部疼痛的鉴别诊断”）。Query transformations 在 retrieve **之前**先重写查询，生成更接近文档形式的版本。

**3 个代表性技巧**:

| 技巧 | 如何改写 | 何时使用 |
|---|---|---|
| **HyDE**（Hypothetical Document Embeddings）| 先让 LLM 为查询生成一个“假设答案”，然后使用该答案的 embedding 进行检索 | 当查询的用词/风格与文档差异很大时 |
| **Multi-Query** | LLM 将查询改写成 N 个变体，分别进行检索，然后合并去重 | 当查询过短/模糊/存在多义时 |
| **RAG Fusion** | Multi-Query + RRF 融合 N 个检索结果，以获得更稳定的排名 | 同 Multi-Query，旨在获得更稳定的排名 |

**何时不使用**: 当查询已经很长且结构化时（如 RAG over code，用户直接粘贴错误堆栈信息）——改写反而可能引入杂讯。

**论文 / 实现**:

- [**HyDE (Gao et al. 2022)**](https://arxiv.org/abs/2212.10496) — 原始论文。
- [**RAG Fusion (Raudaschl 2023)**](https://github.com/Raudaschl/rag-fusion) — Multi-Query + RRF 的参考实现。
- LangChain 内置 `MultiQueryRetriever` / LlamaIndex 内置 `HyDEQueryTransform`。

### 🔁 Adaptive / Agentic RAG — Self-RAG / CRAG / Adaptive RAG（2024 主轴）

**心智模型**: 上述所有 RAG 技巧都假设了一个固定的 Pipeline：“query → retrieve → generate”。Adaptive / Agentic RAG 将这个 Pipeline 变成了一个**具有判断能力的 agent loop**——LLM 自己决定是否需要 retrieve，评估 retrieve 的质量，并在必要时调整查询。**这是 2024 年 RAG 研究的主轴**。

| 技巧 | 如何自我修正 | 论文 |
|---|---|---|
| **Self-RAG** | 训练 LLM 输出 `[Retrieve]` token 来决定是否检索，检索后输出 `[IsRel]/[IsSup]/[IsUse]` 来评分每个片段 | [Asai et al. ICLR 2024](https://arxiv.org/abs/2310.11511) |
| **CRAG** (Corrective RAG) | 检索评估器对结果评分；高置信度直接使用，低置信度回退到 web search，中等置信度触发查询重写 | [Yan et al. 2024](https://arxiv.org/abs/2401.15884) |
| **Adaptive RAG** | 分类器首先判断查询的复杂性，然后路由到“不检索 / 单步 / 多步”三种策略之一 | [Jeong et al. NAACL 2024](https://arxiv.org/abs/2403.14403) |

**为什么这是 2024 年的主轴**: 固定 Pipeline 在简单查询（例如：“东京的首都是哪里？”这种不需要检索）和复杂查询（multi-hop、cross-doc）两者上都存在劣势。让 LLM 自己决定路由，可以同时解决这两种极端情况。

**何时使用**: Production RAG，查询类型分布广泛（从事实题到推理题都有），愿意付出 1.5-3 倍的延迟来换取更高的准确性。
**何时不使用**: 查询类型单一 / 预算限制 / 延迟极其敏感。

**实现**: LangGraph 提供了官方的 [Self-RAG cookbook](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_self_rag/) + [CRAG cookbook](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_crag/) + [Adaptive RAG cookbook](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/)，可以直接套用。

### 🌳 RAPTOR — 阶层式递归检索（ICLR 2024）

**心智模型**: vanilla chunking 将文档切分成扁平的 chunk——但**整本书的主旨并不存在于任何单个 chunk 中**。RAPTOR 递归地聚类和摘要 chunk，构建一个**多层树**：底层 = 原始 chunk，中层 = 一组相关 chunk 的摘要，顶层 = 全文摘要。检索时可以选择搜索整棵树，或选择特定抽象层级。

**为什么有用**:

- 可以检索到**抽象查询**的答案（例如：“这篇论文的主要结论是什么？”——原始 chunk 里可能没有这句话，但顶层摘要里有）。
- 也能有效检索**细节查询**（底层 chunk 被保留）。
- 与 GraphRAG 不同——RAPTOR 使用的是**树**（层次化摘要），而 GraphRAG 使用的是**图**（实体-关系）。

**何时使用**: 长文档（书籍、论文、报告）需要不同抽象层级的查询，知识库具有连贯的叙事性。
**何时不使用**: chunk 之间相互独立（如 FAQ），知识库频繁变动（重建树的成本较高）。

**论文 / 实现**:

- [**RAPTOR (Sarthi et al. ICLR 2024)**](https://arxiv.org/abs/2401.18059) ⭐ — 原始论文。
- [**parthsarthi03/raptor**](https://github.com/parthsarthi03/raptor) — 官方参考实现。
- LlamaIndex 内置 `RAPTOR pack`。

### 🧬 DSPy — 不写 Prompt，用程序自动优化（Path 3 范式）

**心智模型**: 传统 RAG / Agent 需要手动编写 prompt 和 chain。DSPy **消除了 prompt 编写**——你只需定义“签名”（输入/输出类型），编写程序（chain 结构）；DSPy 会用 LLM 编译出最佳的 prompt、few-shot 示例和 retriever 设置。由 Stanford NLP group 于 2024 年提出，并得到 Karpathy 的推广，目前在 production 中越来越受欢迎。

**何时使用**:

- 你的 RAG prompt 已经积累了 6 个月，维护困难，想自动优化。
- 同一程序需要切换不同的 LLM provider（DSPy 会自动重新编译）。
- Agent 系统有多个步骤，你想跟踪 metrics 和 traces。

**何时不使用**:

- 你只有一个 prompt，不需要优化。
- 你是 LLM 新手，还没摸过 prompting。

**代表性仓库**: [**stanfordnlp/dspy**](https://github.com/stanfordnlp/dspy) ★ **34.4k** MIT，Stanford NLP group 官方，积极维护中。

**如何集成到 RAG**: DSPy 与本阶段讨论的 RAG 技巧**并不冲突**——你可以将 GraphRAG / Hybrid Search / Reranking 都当作 DSPy 的模块来组装，然后进行编译。它是一个更高层级的 RAG 构建类型系统。

→ **与 Path 1 / Path 2 Reasoning 并列**: Path 1 是“手动编写 prompt”，Path 2 是“将 reflection 训练进模型权重”，**DSPy 是 Path 3“程序自动搜索最佳 prompt”**。在 Stage 7 Multi-agent 的进阶场景中尤其好用。

### 📊 RAG 进阶技巧概览 — 2025-2026 年的三大主线 ⭐

进阶 RAG 的 2025-2026 年演化集中在 **3 大主线**：

1. **🧠 KG + Memory 融合** — 从扁平的 vector store 走向“结构化、可演化、可联想”的知识表示。代表：[**HippoRAG 2**](https://arxiv.org/abs/2502.14802)（海马体启发、KG + PageRank、跨文档 multi-hop）、A-MEM、KAG。
2. **🎬 Multimodal RAG** — 从文本检索走向图像 / 视频 / 表格的本地化检索。代表：[**ColPali**](https://arxiv.org/abs/2407.01449)（直接对 PDF 图像进行 embedding，绕过 OCR）、TV-RAG、MegaRAG。
3. **🤖 Agentic RAG** — Retrieval 从固定 Pipeline 演变为 Agent Loop 内的 Tool（agent 自主决定检索次数与方式）。代表：A-RAG、Self-RAG（已在上面 Adaptive / Agentic RAG 中介绍）。

**另外 2 个值得关注的方向**:

- **🛡 RAG 安全** — Corpus poisoning / prompt injection 已成为 production 考量重点。代表：[RAGPart / RAGMask](https://arxiv.org/abs/2512.24268)。
- **🔧 不再手动编写 Prompt** — 系统自动搜索最佳 prompt + retriever 组合。代表：[**DSPy**](https://github.com/stanfordnlp/dspy)（Stanford 的"programming not prompting"范式，见上方 DSPy 段落）。

**5 个值得深入研究的代表作**（快速参考）：

| 技巧 | 一句话 | 链接 |
|---|---|---|
| **HippoRAG 2** | KG + Personalized PageRank，跨文档 multi-hop，受海马体启发 | [Gutiérrez et al. ICML 2025](https://arxiv.org/abs/2502.14802)、[OSU-NLP-Group/HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG) ⭐ |
| **ColPali** | 直接对 PDF 图像进行 embedding，绕过 OCR，多模态 RAG 入门 | [Faysse et al. 2024](https://arxiv.org/abs/2407.01449) |
| **A-RAG / SoK Agentic RAG** | 将 retrieval 作为 Tool，Agent 自主决定检索次数/方式 | [Ayanami0730/arag](https://github.com/Ayanami0730/arag)、[SoK survey](https://arxiv.org/abs/2603.07379) ⭐ |
| **DSPy** | 不写 Prompt，使用程序 + 签名进行自动优化 | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) ★ 36k+ |
| **LightRAG** | Microsoft GraphRAG 的轻量级替代方案，EMNLP 2025 论文 | [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) ★ 38k+（已在 GraphRAG 部分介绍） |

<details markdown="1">
<summary>📚 完整概览 — 其他 12 个值得了解的进阶 RAG 技巧（展开查看）</summary>

| 技巧 | 一句话 | 年份 / 论文 |
|---|---|---|
| **Sentence-Window Retrieval** | Embedding 句子，检索后返回 +/- N 句的窗口 | LlamaIndex 内置 |
| **Parent-Child / Small-to-Big** | Embedding 小 chunk，检索时返回父 chunk | LangChain `ParentDocumentRetriever` |
| **Multi-Vector Retrieval** | 一个 chunk，多个 embedding（摘要 / 原文 / 假设问题）| LangChain `MultiVectorRetriever` |
| **ColBERT / Post-Interaction Retrieval** | 基于 token 级别的比对而非 pooled embedding | [Khattab & Zaharia 2020](https://arxiv.org/abs/2004.12832)、[RAGatouille](https://github.com/AnswerDotAI/RAGatouille) |
| **LongRAG** | 大 chunk（4k）+ long-context reader，减少检索次数 | [Jiang et al. 2024](https://arxiv.org/abs/2406.15319) |
| **MemoRAG** | Memory model 将 KB 压缩成 latent memory，检索时使用线索触发 | [Qian et al. 2024](https://arxiv.org/abs/2409.05591) |
| **KAG**（Knowledge-Augmented Generation）| 严格 schema KG + 逻辑推理，适用于金融 / 医疗 / 法律场景 | [Liang et al. 2024 (Ant Group)](https://arxiv.org/abs/2409.13731) |
| **MiA-RAG**（Mindscape-Aware）| 先构建文档的高层摘要 mindscape，然后用它来指导检索和回答 | [arXiv:2512.17220](https://arxiv.org/abs/2512.17220) ⭐ 2025-12 |
| **QuCo-RAG**（Quality-Controlled）| 使用 pretraining 统计来判断是否需要检索，罕见实体触发搜索，减少幻觉 | [arXiv:2512.19134](https://arxiv.org/abs/2512.19134) ⭐ 2025-12 |
| **MegaRAG** | 多模态 KG，从长文档中提取实体 + 关系 + 视觉信息，构建层级图 | [arXiv:2512.20626](https://arxiv.org/abs/2512.20626) ⭐ 2025-12 |
| **TV-RAG** | 无需训练即可感知时间的 RAG，对齐长视频的字幕 + 视觉信息 | [arXiv:2512.23483](https://arxiv.org/abs/2512.23483) ⭐ 2025-12 |
| **RAGPart / RAGMask** | 对 RAG corpus poisoning 攻击的轻量级防御 | [arXiv:2512.24268](https://arxiv.org/abs/2512.24268) ⭐ 2025-12 |

</details>

## 🌉 从 RAG 到 Memory — 为什么 RAG 还不够

读到这里，你应该已经掌握了基础 RAG 的运行方式，并了解了几个 production 优化手段。但回头看 Context Engineering 列出的 3 个问题域——你只解决了 **Retrieval**，而 **Memory 管理** 还没涉及。为什么这两件事要分开处理？

RAG 解决的是“从**外部知识库**检索相关片段”——但 agent 也需要“**自己** 跨对话 / 跨 session 记住事情”。这两件事并非同一个问题：

| 维度 | RAG | Memory |
|---|---|---|
| 内容来源 | **外部**（PDF / 文档 / web / DB）| agent **自己的对话 / 经验** |
| 写入时机 | ingest 一次性，后续每次 retrieve | 每轮对话，每次 task 都可能写入 |
| 内容性质 | 偏静态事实、文档知识 | 偏动态：用户偏好、过往互动、累积的教训 |
| 能否替代 RAG？| — | 否——你不会把每份 PDF 都当作“记忆” |
| 能否被 RAG 替代？| — | 否——RAG 不会“记住上次用户说了什么” |

**3 个 RAG 无法满足的场景**（恰好对应 Memory 的作用）：

1. **跨 session 记住用户偏好 / persona**——用户上周告诉 agent “我是素食者”，这周回来，agent 仍然记得不能推荐肉类。RAG 知识库不会自动更新这些信息。
2. **累积 agent 过往的成败教训**（Reflexion 的主场）——agent 第一次执行任务失败，反思“为什么失败”并保存下来，下次遇到类似任务时检索进 prompt，避免重蹈覆辙。RAG 知识库不会“记住自己的失败”。
3. **Long-horizon task 中的中间状态**——agent 执行一个 100 步的任务，中间需要保留 working memory 不丢失。RAG 不适合这种“短期 + 结构化 + 高频写入”的状态。

→ **结论**: RAG 和 Memory 是**互补**而非替代关系。Production agent 通常**两者都需要**：RAG 处理外部知识，Memory 记录自身与用户的交互历史。下一节 Memory 设计 将指导你如何选择合适的 memory 模式。

## 🧠 Memory 是什么 + 怎么设计

> 📺 **视觉学习**：[李宏毅 2025 第二讲 — 一堂课搞懂 AI Agent 的原理（含 read / write / reflection memory module）](https://www.youtube.com/watch?v=M2Yg1kwPpts)（NTU 生成式 AI 时代下的机器学习 2025）

### Working memory vs Long-term memory — 两种时间尺度

| 比较维度 | Working memory / 短期上下文 | Long-term memory / 持久记忆 |
|---|---|---|
| **中文可称** | 工作记忆 / 短期上下文 | 长期记忆 / 持久记忆 |
| **核心意思** | 这次任务或这段对话中，模型当下看得到的信息 | 存在外部、之后可跨 session 取回的信息 |
| **持续时间** | 短，通常限于当前 session | 长，可跨 session |
| **技术基础** | 上下文窗口（context window）/ prompt | 记忆存储层（memory store）/ 用户文件 / 向量数据库 |
| **适合记什么** | 任务细节、刚刚说过的内容 | 稳定偏好、长期目标、背景资料 |
| **是否受 context 长度限制** | 会，因为模型一次能看到的内容有限 | 较不受限，因为可以先存在外部，需要时只取一小段放回上下文 |
| **生活例子** | 刚收到的手机验证码、正在进行对话的上一句话 | 你深化学会的知识、图书馆、知识库、读过的书 |

→ 在 agent 里，“短期记忆”更准确的说法其实是 **working memory**。它不是外部存储，而是当前 prompt / context window 里看得到的内容。

### Episodic / Semantic / Procedural memory — 三种内容类型

**注意**：上面的 working / long-term 是 **时间轴**；下面三种是 **内容轴**。两组分类 **正交、不互斥**。Long-term memory 里可以同时有 episodic + semantic + procedural 三种。

| 类型 | 中文 | 核心意思 |
|---|---|---|
| **Episodic memory** | 情节记忆 / 经验记忆 | 某次任务、某次互动、某次失败的具体经验 |
| **Semantic memory** | 语义记忆 / 事实记忆 | 稳定知识、用户偏好、背景事实 |
| **Procedural memory** | 程序记忆 / 技能记忆 | agent 知道“怎么做事”的规则、工具、workflow、skills |

→ 这三种对应 [CoALA framework](#进阶coala-framework--agent-memory-的-4-层分类法)。**Reflexion** 是典型的 episodic memory 应用，因为它会累积过往 trial 的成败经验。

这里的 session 可以理解成一次连续互动，例如同一段聊天、同一次任务，或同一次 agent 执行。

### 3 种设计 pattern（什么时候用什么）⭐ Track B 必看

**不是所有 agent 都需要外部 memory store。Memory 架构选错，可能会花十倍 token 才得到同样效果。**

这是开始练习前要建立的 mental model。后面的练习主要跑的是 Pattern 3（vector store），但 production 里未必需要这么复杂。

| Pattern | 适合场景 | 怎么跑 | 成本 |
|---|---|---|---|
| **1. Naive buffer**<br>（全塞 context） | 短对话、≤ 10 turn、agent 不需要跨 session 记忆 | 每次都把整段 history 送进 prompt | 线性增长，token 烧得快 |
| **2. Summary + recent**<br>（摘要远的 + 保留近 N 轮） | 中长对话、~50 turn、想压缩历史但别丢太多 | 每 N 轮让 LLM 把旧 history 摘成一段；prompt = `summary + last N turns` | 中等，有 LLM 摘要成本 |
| **3. Vector store + retrieval**<br>（外部 store + 每轮 semantic search） | 跨 session、知识库场景、agent 要“想起”久远的事 | embed 过去消息 → 存进 Vector DB → 每轮 query 相关片段并拼回 prompt | 高（向量计算 + 存储），但 token 用量稳定 |

**怎么选**：

- 对话 chatbot 没有跨 session 需求 → **Pattern 1**
- agent 配合长对话，需要记住今天聊过什么 → **Pattern 2**
- agent 具备跨 session 需求 + 知识库（本 stage 练习常见场景）→ **Pattern 3**
- production 大型 agent → 通常 **混用**：近期对话用 Pattern 1/2，长期记忆用 Pattern 3

> 💡 **Track B 重点**：Stage 7 的 multi-agent 系统里，每个 agent 通常都有“自己的 memory”+“shared memory”双层。实际常见组合是 **Pattern 2 + Pattern 3 混用**。先在这里把三种 pattern 理顺，Stage 7 才不会卡在 multi-agent memory 设计。

### ⭐ 5 个可上生产的 Memory Layer（按 use case 选）

> Star 数和 benchmark 会变。重点不是排行，而是理解每个 memory layer 的设计取向。

学完 3 个 pattern 后，production 不必自己从零造 memory store。下面 5 个都是 Apache-2.0 / MIT、活跃维护、各擅其场：

| Framework | Stars | License | 主场 use case | 特色 |
|---|---|---|---|---|
| [**agentmemory**](https://github.com/rohitg00/agentmemory) | 7.7k★ | Apache-2.0 | **Coding agent 跨 session 记忆** | MCP-universal（Claude Code / Cursor / Gemini CLI / Codex / Hermes / OpenClaw 都能接）、95.2% R@5、92% token saving、51 个 MCP tools + 12 个 auto hooks、benchmark-driven |
| [**mem0**](https://github.com/mem0ai/mem0) | 55.6k★ | Apache-2.0 | **Chatbot / 个人助手 user-level memory** | 自动事实提取 + 遗忘 + namespace、production-tested、社区最大 |
| [**Letta**](https://github.com/letta-ai/letta)（原 MemGPT） | 22.7k★ | Apache-2.0 | **长 session agent**（按月计） | OS-style paging memory（working + archival 双层）、persona 稳定、MemGPT 论文起源 |
| [**Zep**](https://github.com/getzep/zep) | 4.6k★ | Apache-2.0 | **Temporal KG-based memory** | 把对话历史建成 temporal KG，适合 time-aware reasoning 与 audit trail |
| [**graphiti**](https://github.com/getzep/graphiti) | 27.5k★ | Apache-2.0 | **实时知识图谱 agent 记忆** | 把 agent 过去的交互变成带时间轴的 knowledge graph、方便回头查找；Zep 背后的引擎、可单独使用 |
| [**LangMem**](https://github.com/langchain-ai/langmem) | 1.4k★ | MIT | **LangChain-native memory** | LangChain 官方 memory 库，直接接 LangGraph，适合已经 commit 到 LangChain stack 的项目 |

**怎么选**：

- 构建 coding agent → **agentmemory**（MCP-native，和 Stage 5 ecosystem 高度对齐）
- 开发 chatbot / 个人助手 → **mem0**（最成熟、社区最大）
- 构建长运行 agent（数周 / 数月）→ **Letta**（OS-paging 优势明显）
- 需要时间感知推理 + audit trail → **Zep**（temporal KG）
- 已经采用 LangChain stack → **LangMem**（避免切框架）

**额外官方文档**：[Anthropic Memory Tool](https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool)（Claude 官方 tool-based memory、基于文件、可直接 API 调用）、[LangChain Memory concepts](https://python.langchain.com/docs/concepts/memory/)（框架内各 memory class 的对照）。

### 进阶：CoALA Framework — Agent Memory 的 4 层分类法

[**Sumers et al. 2023 — Cognitive Architectures for Language Agents**](https://arxiv.org/abs/2309.02427) 把 agent memory 分成 4 种类型。这是当前非常实用的一套心智模型：

| 类型 | 存储什么 | 对应示例 |
|---|---|---|
| **Working memory** | 当前任务上下文 | LLM context window 本身 |
| **Episodic memory** | 过去任务的具体经验 | Reflexion 记录、过往 trajectories |
| **Semantic memory** | 抽象事实 / 知识 | RAG 知识库、用户画像、偏好 |
| **Procedural memory** | 如何执行动作 / 技能 | tool definitions、[Skills（Stage 5.3）](05-claude-code-ecosystem.zh-Hans.md#53--skillsclaude-code-的行为层-claude-code-生态最关键的一层) |

→ **为什么有用**：上面 3 个 pattern（buffer / summary / vector）主要覆盖 working + episodic memory。Production agent 往往需要兼顾全部 4 层。CoALA 可以当作检查表，帮你看出 agent 缺了哪一层。

### 进阶：Generative Agents — 三重评分加权（经典案例）

[**Park et al. 2023 — Generative Agents: Smallville**](https://arxiv.org/abs/2304.03442) 的小镇模拟中有 25 个 NPC agent，每个都有自己的 memory stream。检索时使用三个分数的加权组合：

- **Importance**：LLM 为每个 memory 打 1-10 的重要性分数（吃饭 = 2 分，分手 = 9 分）。
- **Recency**：基于时间的指数衰减。
- **Relevance**：与当前查询的 embedding 相似度。

最终得分 = `α·importance + β·recency + γ·relevance`，按得分排序检索 top-k。**这是很多 2024-2025 年 production memory layer 系统（mem0 / Letta）的概念骨架**。

> 💻 **官方代码**: [joonspk-research/generative_agents](https://github.com/joonspk-research/generative_agents) ★ 论文配套的小镇模拟代码库，想跟着实现 memory stream + 三重评分检索看这里。

### 2024-2026 最新 Memory 作品 — 三大主线

Memory 研究在 2024-2026 年集中在 **3 大主线**：

1. **🧠 结构化、可演化、可联想** — 从扁平的 vector store 走向类人脑 / Zettelkasten 启发的记忆结构。代表：[**A-MEM**](https://arxiv.org/abs/2502.12110)（memory 之间自动建立链接）、[**HippoRAG 2**](https://arxiv.org/abs/2502.14802)（KG + PageRank，海马体启发）。
2. **📚 2026 年调查爆发** — 一年内出现了 5 个重量级调查报告和跨领域总结。代表：[**Memory in the Age of AI Agents**](https://arxiv.org/abs/2512.13564)（3D 分类法 + benchmark）、[**Memory for Autonomous LLM Agents**](https://arxiv.org/abs/2603.07670)（形式化 write-manage-read 循环）。
3. **🛡 Memory 安全成为独立子领域** — Agent 运行时间越长，memory 越容易受到 cross-session poisoning / 未授权访问攻击。代表：[**Memory Security survey**](https://arxiv.org/abs/2604.16548)（Stage 7 安全 会涉及）。

**4 个值得深入挖掘的代表作**:

| 作品 | 一句话 | 链接 |
|---|---|---|
| **Anthropic Memory Tool** | Claude 官方 tool-based memory，API 调用，基于文件 | [Anthropic Docs](https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool) |
| **A-MEM**（Agentic Memory）| Zettelkasten 风格，memory 之间自动链接，会演化 | [Xu et al. 2025](https://arxiv.org/abs/2502.12110) ⭐ |
| **HippoRAG 2** | KG + Personalized PageRank，跨文档 multi-hop，ICML 2025 | [Gutiérrez et al. 2025](https://arxiv.org/abs/2502.14802)、[OSU-NLP-Group/HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG) ⭐ |
| **Memory in the Age of AI Agents**（调查报告）| 3D 分类法（temporal / substrate / control）+ benchmark 汇编 | [Hu et al. 2025-12](https://arxiv.org/abs/2512.13564) ⭐ |

→ **长运行 Agent（周/月级别）必读**: 上述调查报告是必须阅读的。

<details markdown="1">
<summary>📚 完整概览 — 其他 8 个值得了解的 Memory 作品（展开查看）</summary>

| 作品 | 一句话 | 年份 / 论文 |
|---|---|---|
| **MemGPT → Letta GA** | OS-paging 内存，working / archival 双层，长 session 场景的强项 | [Packer et al. 2023](https://arxiv.org/abs/2310.08560) → Letta GA |
| **MemoryBank** | 基于艾宾浩斯遗忘曲线，访问过的 memory 得到强化，未使用的逐渐衰减 | [Zhong et al. 2023](https://arxiv.org/abs/2305.10250) |
| **MemoryLLM** | self-updatable memory 参数内建于模型权重中（而非 context 中）| [Wang et al. 2024](https://arxiv.org/abs/2402.04624) |
| **mem0**（见 5 主流 Memory Layer）| 可上生产的 memory layer，自动事实提取 + 遗忘 | [mem0ai/mem0](https://github.com/mem0ai/mem0) |
| **Memory for Autonomous LLM Agents**（调查报告）| 形式化 write-manage-read 循环，汇集 2022-2026 年研究 | [arXiv:2603.07670](https://arxiv.org/abs/2603.07670) ⭐ 2026 |
| **From Storage to Experience**（调查报告）| 演化框架：Storage → Reflection → Experience 三阶段 | [arXiv:2605.06716](https://arxiv.org/abs/2605.06716) ⭐ 2026 |
| **ScrapMem** | 生物启发式 on-device memory，“Optical Forgetting” 渐进式降低旧 memory 的解析度 | [arXiv:2605.03804](https://arxiv.org/abs/2605.03804) ⭐ 2026-05 |
| **Memory Security survey** | 长期 memory 面临 cross-session poisoning / 未授权访问 / 组织内传播等风险 | [arXiv:2604.16548](https://arxiv.org/abs/2604.16548) ⭐ 2026 |

</details>

## 🧩 Chunking 细节（技术深入）

良好的 chunking 能够让 LLM 在有限的 context 内，使用更精确、更完整的资讯生成回答。它并非简单地将文本平均分割。

分割方式取决于应用场景和文档内容。它决定了 retriever 所能看到的最细粒度的语义单元。

一个好的 chunk 应同时做到两件事：**足够完整**，让模型能理解上下文；**足够聚焦**，让检索不带过多杂讯。Chunk 过小会丢失上下文，Chunk 过大会导致相似度搜索变慢。

**常见策略**:

- **固定长度（Fixed-Length）**: 按字符数或 token 数分割。优点是简单稳定；缺点是死板，容易切断段落、句子或表格。
- **滑动窗口（Sliding Window）**: 每个 chunk 之间保留重叠区域（overlap）。优点是不容易在边界丢失信息；缺点是索引量会增大。
- **递归切割（Recursive）**: 先尝试保留段落，若长度仍不合适，则退而求其次，尝试句子、词语等更小的单位。通常是入门 RAG 的良好基准。
- **语义切割（Semantic Chunking）**: 基于 embedding 或语义变化进行分割，即当前块与前一个块的语义相似度出现差异时进行分割。适合长文档，但成本和复杂度较高。
- **混合策略（Hybrid）**: 根据应用场景，思考不同文档结构该如何混合使用分割方法。例如，一篇论文可能需要保留章节、表格、公式和引用脉络。

![Chunking Strategy Flowchart](../resources/diagrams/chunking-strategies.zh-Hans.png)

> 📚 **经典教程**: [Greg Kamradt — 5 Levels of Text Splitting](https://github.com/FullStackRetrieval-com/RetrievalTutorials) ★ Chunking 入门必读，涵盖从 character-based 到 agentic chunking 的五个层级，包含 Jupyter notebook。

首次实现 RAG 时，不必一开始就追求复杂的分割方法。LangChain 的文档建议大多数场景下从 `RecursiveCharacterTextSplitter` 开始。

先跑出基准版本，再根据后续的 retrieval 结果来决定是否更换策略。

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = "这是一个很长的文档内容...（此处省略一千字）..."

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
)

chunks = splitter.split_text(text)
print(f"Split into {len(chunks)} chunks")
print(chunks[0])
```

**直观判断 Chunking 效果**:

- 回答信息缺失，或有头无尾：通常是 chunk 太小，或 overlap 不够。
- 回答包含正确信息，但混入了无关内容：通常是 chunk 太大，或 top-k 检索过多。

**进阶思考**:

- Chunking 不是一次设定好就结束，需要结合真实查询和失败案例反复调整。
- Chunk size、overlap、top-k、reranker 之间会相互影响，不要只单独看其中一个参数。
- 思考一下，如果今天要 RAG 的数据包含图片 PDF、会议字幕文件，该如何分割比较好？
- Chunking 的进阶变体（Sentence-Window / Parent-Child / Multi-Vector）见 进阶 RAG 技巧概览表。

## 🪞 进阶：带持久记忆的 Reflexion 完整版 ⭐ Track B 选读

> **本节是概念 + 路由，并非练习**。它扩展了 Stage 3 反思 的基础版本（single-session Actor / Critic loop），解释了为何某些反思**需要**持久记忆——这个版本才真正属于 Stage 6 的范畴。

**Reflexion 完整版与 Self-Refine 的区别**:

| 版本 | 会话内保留内容 | 跨 session 保留内容 | 需要的 Memory 模式 |
|---|---|---|---|
| **Self-Refine**（Madaan 2023）| 上一轮的 answer + critic feedback | ❌ 不保留 | 无需（Pattern 1 buffer 即可） |
| **完整 Reflexion**（Shinn 2023）| 同上 | ✅ 将过去 trial 的“反思摘要”存入 episodic memory，下次遇到类似 task 时检索进 prompt 作为教训 | **需要**（Pattern 3 vector store 或 Pattern 2 summary） |

**为什么这个版本需要 Memory**: Reflexion paper 中的 verbal reinforcement learning 核心在于“agent 跨 trial 累积教训”——agent 尝试任务 → 失败 → 反思“为何失败”并保存 → 下次遇到类似任务时，将过去的反思检索进 prompt，避免重蹈覆辙。这需要 **persistent episodic memory**，直接关联到本阶段上面讨论的 3 种 memory 模式。

**典型架构**（持久记忆完整版）：

![Reflexion 持久 episodic memory loop](../resources/diagrams/reflexion-persistent-memory-loop.zh-Hans.png)

→ **与 Stage 3 反思的区别**: Stage 3 侧重于**单 session 内的 in-context 循环**（无外部存储），本节则探讨**跨 trial 的持久 episodic memory 存储 + 检索**（从过往经验中学习）。

### 📚 想动手 / 想深入

**论文**:

- [**Reflexion (Shinn et al. 2023)**](https://arxiv.org/abs/2303.11366) ⭐ — **完整版**论文，Algorithm 1 详细说明了 memory buffer 的用法。
- [**Self-Refine (Madaan et al. 2023)**](https://arxiv.org/abs/2303.17651) — 对比基线版本，即没有 episodic memory 的版本。

**参考实现**:

- [**noahshinn/reflexion**](https://github.com/noahshinn/reflexion) — 论文第一作者的参考实现（包含完整的 episodic memory 流程）。
- [**LangChain — Reflexion**](https://langchain-ai.github.io/langgraph/tutorials/reflexion/reflexion/) — LangGraph 版本，可直接集成到本阶段的 RAG pipeline 练习中。
- [**mem0**](https://github.com/mem0ai/mem0)（上面已列）+ [**Letta**](https://github.com/letta-ai/letta)（上面已列）— Memory Layer，可以直接作为 Reflexion 的 episodic store。

> 💡 **与 Stage 3 反思 的分工**:
> - 想理解“反思循环如何工作、单次如何运行” → Stage 3 反思。
> - 想理解“反思如何跨 session 累积，agent 如何从过往学习经验” → 本节。
> - 想看 production agent 内部如何使用反思（例如 Cursor / Claude Code）→ [Stage 5 5.7 Harness Internals](05-claude-code-ecosystem.zh-Hans.md#57--claude-code-source-解剖reference-harness-implementation-track-b-必看)。

## 🤔 进阶 Reasoning / Reflection — 2024-2026 年思潮 ⭐ 覆盖两种路径

Reflexion 是一种**基于 Prompt 的 reflection**——LLM 在推理时自行修改自身。2024-2025 年出现了**第二条路径**：**在训练时就将 reflection 融入模型权重**（OpenAI **o1** / DeepSeek **R1**）。你应该了解这两种方法。

### Path 1: Prompt-based reflection / reasoning（传统做法）

| 技巧 | 核心思想 | 论文 |
|---|---|---|
| **Self-Consistency** | 对 N 条推理路径进行采样，取多数结果——**最简单、最常用** | [Wang et al. 2022](https://arxiv.org/abs/2203.11171) |
| **Tree of Thoughts (ToT)** | Reasoning 变成树状结构，允许分支和回溯；适用于 puzzle / planning。 | [Yao et al. 2023](https://arxiv.org/abs/2305.10601) |
| **Graph of Thoughts (GoT)** | 不仅限于树，可以是任意图结构。 | [Besta et al. 2023](https://arxiv.org/abs/2308.09687) |
| **Chain-of-Verification (CoVe)** | 生成答案 → 自问验证问题 → 修改答案 | [Dhuliawala et al. 2023](https://arxiv.org/abs/2309.11495) |
| **CRITIC** | 通过工具增强的自我批判（使用 search / calculator 进行验证） | [Gou et al. 2023](https://arxiv.org/abs/2305.11738) |
| **Self-Discover** | Agent 先“发现”需要使用的 reasoning structure，然后再执行 | [Zhou et al. ICML 2024](https://arxiv.org/abs/2402.03620) ⭐ 2024 |
| **Self-Refine / Reflexion** | 已在上面 / Stage 3 讲解 | Stage 3 反思，本阶段 Reflexion |

### Path 2: Trained-in reasoning / reflection（2024-2026 年重大转变）

> 📺 **视觉学习**: [李宏毅 2025 第七讲 — DeepSeek-R1 这类大型语言模型是如何进行“深度思考”(Reasoning) 的？](https://www.youtube.com/watch?v=bJFtcwLSNxI)（NTU 生成式AI时代下的机器学习 2025）

OpenAI **o1**（2024-09）开启这条路、DeepSeek **R1**（2025-01）开源化——把“step-by-step thinking + 自我纠错”**训练进 model 权重**、inference 时自动展开长 reasoning chain（thinking tokens）。**这是 2024-2026 年 LLM 的最大范式转移**，所有前沿模型都在遵循这条路径（Claude Opus 5、Claude Fable 5、GPT-5.5、Gemini 3.1 Pro、DeepSeek-V4-Pro 等，各自的发布日与定位见下表）。下表仅列出**当前（2026-07）前沿模型**——历史上的前身（o1 / R1 / Sonnet 4.5 / Gemini 2.5）已省略，想了解 lineage 可查看各家发布日期。

| 模型 | 来源 / 发布 | 特色 | 链接 |
|---|---|---|---|
| **GPT-5.5** | OpenAI 2026-04（前身：o1 2024-09 → o3 → GPT-5 2025-08 → 5.4 2026-03）| 闭源，reasoning + chat 合并，提供 Thinking budget API，Agent 能力增强。**较新层级：GPT-5.6（Sol / Terra / Luna）、2026-07 正式推出、1.05M context** | [OpenAI](https://openai.com/) |
| **Claude Fable 5** | Anthropic 2026-06（Mythos-class、位阶在 Opus class 之上；同步发布 Claude Mythos 5 为解除部分 safeguard 的限量版本）| 闭源、Mythos-class（位阶在 Opus class 之上）。曾于 2026-06-12 被美国出口管制暂停，**出口管制 2026-06-30 解除、[Fable 5 于 2026-07-01 全球恢复](https://www.anthropic.com/news/redeploying-fable-5)**（重新部署时加了新安全 classifier；Mythos 5 仅对核准的美国组织恢复）。官方 benchmark 数字始终未公布 | [Claude Fable 5 / Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5) |
| **Claude Opus 5** | Anthropic 2026-07-24（前身：Opus 4.5 / Opus 4.7 / Opus 4.8；Dynamic Workflows 研究预览随 Opus 4.8 推出。Opus 4.8 仍可用、官方文档已移入 Legacy models）| 闭源、Opus class 旗舰（位阶在 Fable 5 之下）、1M context、adaptive thinking、官方建议“复杂 agentic coding 与企业工作从 Opus 5 开始”；在 SWE-bench / Terminal-bench 方面领先是前身 Opus 4.8 的测量结果，Opus 5 目前没有第三方复现数字 | [Anthropic extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) |
| **Gemini 3.1 Pro** | Google 2026-02（前身：Gemini 2.5 Thinking 2025、Gemini 3 2025-11）| 闭源，可查看 thinking trace，GPQA Diamond 94.3%，价格 / 速度 / multimodal 方面领先。**较新层级：Gemini 3.5 Flash、2026-06 已开放（3.5 Pro 开发中）** | [Gemini API](https://ai.google.dev/gemini-api/docs/thinking) |
| **DeepSeek-V4 / V4-Pro / V4-Flash** | DeepSeek 2026-04 预览版（前身：R1 2025-01 → V3.1）| 开源 **MIT license**，面向 Agent 的训练，整合推理 + 工具使用 + 知识处理，R 系列 reasoning 已并入主线 | [HF DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)、[R1 论文（方法基线）](https://arxiv.org/abs/2501.12948)、[CNBC 报道](https://www.cnbc.com/2026/04/24/deepseek-v4-llm-preview-open-source-ai-competition-china.html) |
| **QwQ-32B / QvQ-72B** | Alibaba Qwen 2024-11 ~ 2026 | 开源 **Apache 2.0**，32B 在小尺寸 reasoning 仍是不错的选择，QvQ 为视觉版本 | [QwQ blog](https://qwenlm.github.io/blog/qwq-32b-preview/) |

### 两条路径如何选择

| 你的情况 | 建议 |
|---|---|
| 使用普通 chat model 作为基础，想加入 reasoning | Path 1（基于 Prompt 的方式）—— ToT / Self-Consistency / CoVe |
| 预算 / 延迟允许，需要最强的 reasoning 能力 | Path 2 —— 选择 **GPT-5.5 / Opus 5 / Gemini 3.5 Flash / Grok 4.5 / V4-Pro** 中的一个（Claude Fable 5 属 premium 高阶层级，位阶在 Opus class 之上）|
| 想自己 fine-tune reasoning model | Path 2 —— 阅读 R1 论文（方法基线），从 R1-Distill / V4 开源权重开始 |
| 需要 on-device / 预算极度紧张 | **QwQ-32B**（Apache 2.0）或 R 系列 distill 版本 |
| Multi-agent debate / critic 场景 | Path 1（CRITIC / debate）+ [Stage 7 Multi-agent](07-multi-agent-production.zh-Hans.md) |

> 💡 **2025-2026 年趋势**:
> - Reasoning 模型已将 Reflexion 的能力内化到权重中——但**基于 Prompt 的 reflection 并未被取代**：Agent Loop（控制反思时机/内容）+ Multi-agent debate 仍然是必需的。
> - **开源模型正在快速追赶闭源模型**——DeepSeek-V4-Pro（2026-04 预览版，MIT 许可）已将 R1 reasoning 集成到主线，并采用 Agent-first 训练，与 GPT-5.5 / Gemini 3.5 Flash 的差距在缩小。
> - **Agent 能力正成为主要卖点**——V4 / Opus 5 都将 Agent-as-product（SWE-bench / Terminal-bench / tool use）作为核心 benchmark，单纯的 reasoning 已不足以吸引用户。
> - 两条路径将长期共存，Production Agent 很可能两者都会使用。

## 📏 RAG / Memory Eval — 跑得起来 ≠ 跑得准

**为什么这节很重要**: RAG / Memory 系统的最大坑是“**看起来能跑，但实际检索精度很差**”。没有 Eval，你无法知道是修改 chunk size / 更换 embedding / 添加 reranker 真的有帮助——你只会得到“答案好像更顺了”这种主观印象。没有 Eval 的 Production Agent 基本上就是未经验证。

**3 个核心指标**:

| Metric | 衡量什么 | 工具 |
|---|---|---|
| **Retrieval Recall@K** | Top-K 检索到的 chunk 中是否包含 ground truth 答案的 chunk | ragas / TruLens / LangSmith |
| **Answer Faithfulness** | 生成的答案是否基于检索到的 chunk（ vs. 模型幻觉）| ragas / TruLens |
| **Answer Relevance** | 答案与查询的相关度（避免答非所问）| ragas / LLM-as-judge |

**代表性框架**:

- [**explodinggradients/ragas**](https://github.com/explodinggradients/ragas) ★ **13.9k** Apache-2.0 ⭐ — RAG 评估标准工具，包含 8+ 指标（faithfulness / answer relevance / context precision / context recall 等），支持 reference-free 和 reference-based 评估。
- [**TruLens**](https://github.com/truera/trulens) — 可观测性 + 评估一体化，与 LangChain / LlamaIndex 集成良好。
- [**LangSmith**](https://docs.langchain.com/langsmith) — LangChain 官方 Eval + Tracing 平台（闭源 SaaS）。

**如何开始**: 完成练习 4（完整 RAG Pipeline）后，集成 ragas 进行评估，测量一次基线——然后再调整 chunk / embedding / top-k，观察指标的变化。**没有这一步，调参全靠猜**。

→ Stage 7 Eval 将在本次基础上继续，将评估扩展到 multi-agent / full harness。

## 🛠 动手练习（基础示例性练习）

### 练习 1：Embeddings
将 100 个句子进行 embedding，找出某个查询的最近邻。理解向量之间的距离意义。

### 练习 2：Vector DB
将 embedding 存储到 Chroma 中，进行语义查询。对比“与 keyword search 的区别”。

### 练习 3：Chunking 对照
用同一份文档进行三种切割：固定长度、按段落分割、按 heading 分割。用 5 个真实问题比较 top-k 结果，记录哪种分割方法更容易检索到正确上下文。

### 练习 4：完整 RAG 流水线
将一份 PDF 切块 → embed → 检索 top-k → 生成回答。这是大多数 RAG 应用的基础框架。

### 练习 5：Long-term Memory
让 agent 在多轮对话中记住事情。可以使用 `mem0` 或自行搭建 vector store。

## 🎯 常用 Memory / RAG 工具推荐（按用途分类）

不知道从哪里开始选择工具？下面是 2025 年下半年业界常用的组合——**根据你的场景（“入口”）进行选择，深入了解请点击链接查看 repo**：

| 场景 | 推荐工具 | 原因 |
|---|---|---|
| **首次运行 RAG**（上手最快）| [Chroma](https://github.com/chroma-core/chroma) + [LlamaIndex](https://github.com/run-llama/llama_index) | 本地优先，零运维，quickstart 友好。Stage 6 练习默认配置。 |
| **企业级 RAG 框架**（LangChain / LlamaIndex 之外的第三选择）| [Haystack (deepset)](https://github.com/deepset-ai/haystack) ★ 25.2k Apache-2.0 | deepset 开源，面向 production 的编排，企业级 NLP 场景成熟。 |
| **Agent 长期记忆**（见 5 个可上生产的 Memory Layer）| [agentmemory](https://github.com/rohitg00/agentmemory) / [mem0](https://github.com/mem0ai/mem0) / [Letta](https://github.com/letta-ai/letta) / [Zep](https://github.com/getzep/zep) / [LangMem](https://github.com/langchain-ai/langmem) | 详见上方 5 个可上生产的 Memory Layer 部分。 |
| **RAG / Memory Eval**（必备）| [ragas](https://github.com/explodinggradients/ragas) ★ 15k+ | RAG 评估标准工具，8+ 指标，支持 reference-free + reference-based。 |
| **Production Scale RAG**（百万级文档）| [Qdrant](https://github.com/qdrant/qdrant) + LlamaIndex | Rust 编写的 vector DB，在大规模场景下比 Chroma 更快。 |
| **已有 Postgres 环境** | [pgvector](https://github.com/pgvector/pgvector) | Postgres 扩展，SQL + vector 在同一个数据库中，运维最简。 |
| **企业级 RAG + Web UI** | [RAGFlow](https://github.com/infiniflow/ragflow) | 强大的文档解析能力（含 OCR / 表格 / 布局），企业级应用，自带 Web UI。 |
| **中文 RAG 范例** | [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | 中文社区最广泛使用，支持本地 LLM 部署（ChatGLM / Qwen / Llama / Ollama）。★ 38k+，Apache-2.0。⚠️ 最后更新 2025-11（边缘情况）。 |
| **进阶：Contextual Retrieval** | [Anthropic Cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) | Claude 结合 prompt caching 的 contextual chunking（**详见上方 进阶 RAG 技巧**）。 |
| **进阶：Knowledge Graph 推理** | [LightRAG](https://github.com/HKUDS/LightRAG) / [Microsoft GraphRAG](https://github.com/microsoft/graphrag) | Knowledge Graph + RAG，实现实体-关系推理（**详见上方 进阶 RAG 技巧**）。 |
| **教程合集** | [ai-engineering-hub](https://github.com/patchy631/ai-engineering-hub) | RAG + agent 教程合集，Jupyter notebook 形式。 |

**推荐入手顺序**:

1. 首先安装：**Chroma + LlamaIndex**（用于 Stage 6 练习）。
2. Agent 需要记忆功能：添加 **mem0**（最简单的 memory layer）。
3. 进入 production 规模：切换到 **Qdrant** 或 **pgvector**。
4. 想升级到进阶 RAG：研究 进阶 RAG 技巧 部分。

## 🎯 精选 Projects（模板 / 规范 / 示例合集）

按用途分类，17 个项目一表搞定。**根据你的场景（"入口"）进行选择，深入了解请点击链接查看 repo**。

| 分类 | Project | ⭐ | 适用人群 | 推荐理由 / 备注 |
|---|---|---|---|---|
| **RAG Framework**<br>（完整流水线） | [LlamaIndex](https://github.com/run-llama/llama_index) | ⭐⭐⭐⭐⭐ | 以文档为核心的应用 | 以 RAG 为核心，提供 document loader / chunking / retrieval / query engine 一站式服务。★ 51k+ |
| | [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | ⭐⭐⭐⭐⭐ | 希望将 RAG 部署给非开发者用户使用的团队 | Production 级别的 RAG engine，深度文档理解（layout / 表格 / OCR）+ hybrid retrieval + agent loop + Web UI。★ 86k+，Apache-2.0 许可。 |
| | [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | ⭐⭐⭐⭐ | 探索研究级 graph + long-context memory 方法的开发者 | graph + vector hybrid retrieval + summarization-based memory，基于 EMNLP 2025 论文。★ 38k+，MIT 许可。代码风格偏研究。 |
| **Vector DB**<br>（本地优先） | [Chroma](https://github.com/chroma-core/chroma) | ⭐⭐⭐⭐⭐ | 练习 2 / 4，最容易上手的 vector DB | 开源的 embedding 数据库，可本地运行，支持 in-memory / SQLite 后端，零运维。★ 28k+，Apache-2.0 许可。**安装**: `pip install chromadb` |
| **Vector DB**<br>（Production Scale） | [Qdrant](https://github.com/qdrant/qdrant) | ⭐⭐⭐⭐⭐ | Chroma 性能不足，需要 production scale 时 | Rust 编写的 vector DB，在大规模场景下比 Chroma 更快。提供云端版和自托管版。★ 33k+ |
| **Vector DB**<br>（Hybrid） | [Weaviate](https://github.com/weaviate/weaviate) | ⭐⭐⭐⭐ | Production 部署 + schema 约束 | 内置模块（text2vec / generative / classification），schema 驱动，原生支持 BM25 + vector hybrid 搜索。★ 16k+ |
| **Vector DB**<br>（已有 Postgres 环境） | [pgvector](https://github.com/pgvector/pgvector) | ⭐⭐⭐⭐ | 原本就在使用 Postgres 的团队 | Postgres 扩展，SQL + vector 在同一个数据库中，运维最简。★ 22k+ |
| **Vector DB**<br>（跑在 app 内） | [lancedb/lancedb](https://github.com/lancedb/lancedb) | ⭐⭐⭐⭐ | 想要 vector DB 直接内建、不想另跑 server | 直接跑在你 app 里的 vector DB（不用另开 server）、能处理文字 + 图片、关键字 + 向量一起搜。★ 11k+，Apache-2.0 |
| **Memory Framework**<br>（自动事实提取） | [mem0ai/mem0](https://github.com/mem0ai/mem0) | ⭐⭐⭐⭐⭐ | 个人助手 / Chatbot 需要 user-level 记忆 | 自我精炼的 memory 层，支持跨 session 存储事实。★ 62k+ |
| **Memory Framework**<br>（OS-Paging） | [Letta（原 MemGPT）](https://github.com/letta-ai/letta) | ⭐⭐⭐⭐ | Agent 需要运行很长时间（以月为单位） | 阶层式 memory（working / archival），借鉴 OS Paging 概念。★ 24k+ |
| **Memory（框架内）** | [LangChain — Memory](https://python.langchain.com/docs/concepts/memory/) | ⭐⭐⭐ | 已在使用 LangChain | 4 种 memory 抽象（buffer / summary / vectorstore-backed / entity）。 |
| **进阶 RAG 技巧** | [Anthropic — Contextual Retrieval Cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) | ⭐⭐⭐⭐⭐ | 跑完基础 RAG 后，想升级 | Claude 结合 prompt caching 的 contextual chunking，包含完整的端到端示例。 |
| **中文 RAG 范例** | [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | ⭐⭐⭐⭐ | 中文知识库 / RAG 应用 | 中文社区最广泛使用，支持本地 LLM 部署（ChatGLM / Qwen / Llama / Ollama），中文默认配置好。★ 38k+，Apache-2.0 许可。⚠️ 最后更新 2025-11（边缘情况）。 |
| **教程合集** | [ai-engineering-hub](https://github.com/patchy631/ai-engineering-hub) | ⭐⭐⭐⭐ | 想看“同一概念在不同场景下如何实现” | 主题式 LLM / RAG / agent 教程合集，Jupyter notebook 形式，跨多个 stage 都有用。★ 36k+，MIT 许可。 |
| **Production AI Assistant**<br>（学习部署 RAG 的参考）| [onyx](https://github.com/onyx-dot-app/onyx)（原 Danswer）| ⭐⭐⭐⭐⭐ | 想学习“如何将 RAG 驱动的 AI Assistant 部署到 production” | 开源的企业级 AI Assistant，支持跨 LLM，包含完整的 ingest / retrieval / chat / admin 功能。★ 31k+，积极维护。 |
| **RAG Cookbook**<br>（30+ 技巧范例）| [NirDiamant/RAG_Techniques](https://github.com/NirDiamant/RAG_Techniques) | ⭐⭐⭐⭐⭐ | 跑完基础 RAG 后，想探索各种变体 | 大型 RAG 技巧 Cookbook，包含 Self-RAG / HyDE / Multi-Query / Adaptive 等 30+ 个 Jupyter notebook 示例。 |
| **DSPy**<br>（编程而非 Prompt）| [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | ⭐⭐⭐⭐⭐ | 使用 LLM 一段时间后，想自动优化 prompt + chain | Stanford NLP group 开发，★ 36k+ MIT，Path 3 范式（详见 DSPy）。 |
| **RAG / Memory Eval**<br>（必备）| [explodinggradients/ragas](https://github.com/explodinggradients/ragas) | ⭐⭐⭐⭐⭐ | 完成练习 4（完整 RAG Pipeline）后，想衡量检索精度 | RAG 评估标准工具，8+ 指标，支持 reference-free + reference-based。★ 15k+ Apache-2.0。 |

**推荐入手顺序**:

1. 首次安装必备：**Chroma + LlamaIndex**（用于 Stage 6 练习）。
2. Agent 需要记忆功能：添加 **mem0**（最简单的 memory layer）。
3. 进入 production 规模：切换到 **Qdrant** 或 **pgvector**。
4. 想升级到进阶 RAG：研究 进阶 RAG 技巧 部分。

## ✅ 进入 Stage 7 前的自我检查

你是否能够：

- [ ] 编写一条 50 行的 RAG Pipeline（load → chunk → embed → store → query → answer）？
- [ ] 解释为什么天真的 chunking 在长文档上会失效？
- [ ] 为 API 文档、PDF、表格设计不同的 chunking 策略？
- [ ] 在特定规模下，能在 Chroma、Qdrant、pgvector 之间做出选择？
- [ ] 区分“给 agent memory”和“使用 RAG”这两件事？
- [ ] 解释 RAG 和 Memory 如何互补（参考 从 RAG 到 Memory 表格）？

如果以上都能够做到 → 前往 [Stage 7 — Multi-Agent · Production 化](07-multi-agent-production.zh-Hans.md)。

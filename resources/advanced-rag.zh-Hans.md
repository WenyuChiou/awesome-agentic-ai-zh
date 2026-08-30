# 进阶 RAG：先找出哪一步坏了，再加新技巧

[繁體中文](advanced-rag.md) | [English](advanced-rag.en.md) | [简体中文](advanced-rag.zh-Hans.md)

<!-- freshness: canonical=resources/advanced-rag.md; verified_on=2026-08-30; scope=rag,retrieval,reranking,graph-rag,evaluation,project-status; max_age_days=90 -->

← [回到 Stage 6：RAG 与 Memory](../stages/06-memory-rag.zh-Hans.md)

基础 RAG 像“先翻书，再回答”。进阶 RAG 不是把更多零件全装上去，而是先看哪一步找错了资料，再只修那一步。

## 📌 学习目标

完成这页后，你可以：

1. 分清“找不到”“排序错”“证据不够”“回答乱讲”四种问题。
2. 说出 **Hybrid Search**、**Reranking**、**Query Transformation** 与 **GraphRAG** 各自修哪一步。
3. 用一小组固定问题比较修改前后，不靠一次漂亮回答下结论。
4. 知道什么时候先停在基础 RAG，不增加成本与复杂度。

## 🧩 先认识八个核心术语

| 核心术语 | 好理解的说法 | 正确意思 |
|---|---|---|
| **Baseline（基线）** | 还没加新招以前的成绩 | 可重复运行的最小系统与评测结果，用来比较改动是否真的有效。 |
| **Hybrid Search（混合搜索）** | 同时看“一样的字”和“相近的意思” | 合并 BM25／全文搜索与向量搜索的候选结果。 |
| **Reranking（重新排序）** | 把拿到的卡片再排一次 | 用另一个模型或规则，重新估计问题与候选文档的相关性。 |
| **Query Transformation（查询转换）** | 换几种问法再找 | 改写、拆分或扩充问题，以取得不同候选文档。 |
| **Contextual Retrieval（上下文检索）** | 每张小卡先写上“这张卡来自哪一章” | 建索引前替 chunk 补上文档背景，再做检索。 |
| **Corrective／Adaptive RAG** | 找得不好就换方法 | 先检查候选质量，再决定重查、改来源或直接回答。 |
| **Agentic RAG** | 让 agent 自己决定何时翻书 | 把 retrieval 当作工具，由 agent 决定是否、何时及如何调用。 |
| **GraphRAG** | 不只找卡片，也沿着人物与事件的线找 | 从 entity 与 relationship 建图，支持跨文档关系与整体主题查询。 |

## 🩺 先看症状，再选方法

| 你看到的问题 | 先量什么 | 第一个可试的方法 | 先不要做什么 |
|---|---|---|---|
| 文档里明明有答案，却完全没被找回 | Recall@k、命中率 | 改 chunk、metadata filter 或 Hybrid Search | 先换更大的生成模型 |
| 正确文档有找回，但排在很后面 | MRR、nDCG、前 k 名人工检查 | Reranking | 一口气加 graph 与 agent loop |
| 问题太短、太模糊或包含多个小问题 | 各改写查询的命中率与延迟 | Multi-Query、拆题或 HyDE | 无限制产生大量查询 |
| 要回答跨很多文档的关系或整体主题 | 关系覆盖率、global question 测试集 | GraphRAG、LightRAG 或摘要树 | 把 graph 当成每个 RAG 的默认配置 |
| 有些问题根本不需要查资料 | 不必要检索率、成本、延迟 | Adaptive／Agentic RAG | 让 agent 无上限重试 |
| 找到正确证据，回答仍不受证据支持 | Faithfulness／人工引用核对 | 改回答 prompt、引用格式与拒答规则 | 继续调 retrieval 掩盖生成问题 |

## 📚 必读材料

请按顺序读；它们是学习主线，不藏在菜单里。

1. [LangChain：Retrieval 概念](https://docs.langchain.com/oss/python/deepagents/retrieval) — 先分清 knowledge base、retriever 与 agent。
2. [Anthropic：Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) — 看 chunk 加背景、BM25、embedding 与 reranking 如何组合。
3. [Qdrant：Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/) — 看 dense、sparse 与 fusion 的实际查询形状。
4. [Weaviate：Hybrid Search](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search) — 用另一个官方实现理解 keyword 与 vector 分数如何合并。
5. [LangGraph：Agentic RAG 教程](https://docs.langchain.com/oss/python/langgraph/agentic-rag) — 完成固定 2-step RAG 后，再看 agent 如何决定检索。
6. [Ragas](https://github.com/vibrantlabsai/ragas) — 把“看起来不错”改成可重复运行的数据集与评测循环。

## 🪜 从基础到进阶的顺序

### 1. 先固定一个最小 Baseline

准备 20–50 个有人看过的问题，每题保存预期来源与可接受答案。每次只改一件事，记录 retrieval、answer、延迟与成本。没有 baseline，就不知道新技巧是在帮忙还是添乱。

### 2. 先修 Retrieval，再修 Generation

- **Chunking** 决定资料怎么切；先用标题、段落与文档结构切，再测试 fixed-size、parent-child 或 semantic chunking。
- **Hybrid Search** 扩大候选来源；BM25 找精确字词，vector search 找语义相近内容。
- **Reranking** 不会创造新文档；它只把已找回的候选重新排列。

### 3. 问题不好找时，再做 Query Transformation

- **Multi-Query**：把同一问题改成几种说法，各自搜索后合并。
- **HyDE**：先产生一段假想答案，再用它搜索；可能提升召回，也可能被假想内容带偏。
- **RAG Fusion**：对多组查询结果做 rank fusion，降低单一措辞的影响。
- **Decomposition**：把“比较 A、B 并解释原因”拆成数个可分别找证据的小问题。

### 4. 需要跨文档关系时，才考虑 GraphRAG

**Microsoft GraphRAG** 是研究参考实现，官方目前标为 largely in maintenance mode，仍会修复 bug 与依赖问题，但不再以新增功能为主。它的 indexing 可能昂贵，应先用小数据集。**LightRAG** 是另一套活跃的 graph-based RAG 实现，数据模型与 Microsoft GraphRAG 不同，不能把两者当成同一个产品。

GraphRAG 适合“哪些人物共同影响这件事？”或“整批文档有哪些主题？”；单份 FAQ 或精确条款查询，通常先用一般 retriever 就够了。

### 5. 流程需要判断时，才加 Corrective 或 Agentic RAG

- **Self-RAG**：模型学习何时检索，并对证据与回答做反思。
- **CRAG（Corrective RAG）**：先判断候选是否够好，不够时改查询或改来源。
- **Adaptive RAG**：依问题难度选择不同流程。
- **Agentic RAG**：让 agent 决定何时调用 retriever；必须设定步数、时间、成本与可用来源上限。

原始入口：[Self-RAG](https://arxiv.org/abs/2310.11511)、[CRAG](https://arxiv.org/abs/2401.15884)、[Adaptive-RAG](https://arxiv.org/abs/2403.14403)。

### 6. 最后才碰摘要树与程序优化

**RAPTOR** 把内容反复聚类、摘要成由细到粗的树；细节问题找叶节点，主题问题找高层摘要。**DSPy** 用 examples 与 metric 调整 LLM program；它仍需要清楚任务、可靠资料与评测指标。

阅读：[RAPTOR paper](https://arxiv.org/abs/2401.18059) · [DSPy](https://github.com/stanfordnlp/dspy)

## 🛠 一个可重复运行的小实验

1. 选 20 题，为每题标出正确来源。
2. 跑最小 vector retrieval，保存 top-5 结果。
3. 只加入 BM25，重新跑同一批题目。
4. 再只加入 reranker，比较 top-5、延迟与成本。
5. 写下哪些题变好、哪些题变差，以及原因。

**完成条件：**你能拿出同一份测试集的三组结果，而不是只展示一题成功案例。

<details markdown="1">
<summary>成本、资料与上线前检查</summary>

- Indexing 是否会调用付费模型？先用小样本估算一次完整重建成本。
- 每个 chunk 是否保留来源、页码／位置、版本、时间与访问权限？
- Retriever 是否在查询前套用权限，而不是找到后才遮住答案？
- Agentic loop 是否有最大步数、timeout、budget 与安全来源清单？
- Cache 是否会让旧文档继续被取回？更新与删除流程是否测试过？

</details>

<details markdown="1">
<summary>常见失败与排查顺序</summary>

1. 先看正确证据有没有进 top-k。
2. 有进 top-k，再看 reranker 是否把它往后排。
3. 排名正确，再看 prompt 是否要求引用与拒答。
4. 最后才检查生成模型；不要用更大模型掩盖 retrieval 错误。

</details>

## 🎯 精选 Projects 与学习资源

评分代表“对这张学习地图的教学价值”，不是项目质量排行榜。先选一个框架、一个数据层与一个评测工具。

<small>资料核查：2026-08-30 UTC</small>

<table>
  <thead><tr><th scope="col">分类</th><th scope="col">项目／资源</th><th scope="col">编辑评分</th><th scope="col">适合谁</th><th scope="col">能学什么</th><th scope="col">状态／限制</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Pipeline 与示例</th><td><a href="https://github.com/run-llama/llama_index">LlamaIndex</a></td><td>⭐⭐⭐⭐⭐</td><td>文档型应用开发者</td><td>retriever、query engine、evaluation</td><td>MIT；套件多，先跟官方 starter</td></tr>
    <tr><td><a href="https://github.com/deepset-ai/haystack">Haystack</a></td><td>⭐⭐⭐⭐</td><td>想看模块化 pipeline</td><td>components、routing、retrieval</td><td>Apache-2.0；先做小型 pipeline</td></tr>
    <tr><td><a href="https://github.com/NirDiamant/RAG_Techniques">RAG_Techniques</a></td><td>⭐⭐⭐⭐⭐</td><td>想比较技术的读者</td><td>可运行 notebooks 与技术对照</td><td>社区教材；事实回官方文档核对</td></tr>
    <tr><td><a href="https://github.com/infiniflow/ragflow">RAGFlow</a></td><td>⭐⭐⭐⭐</td><td>想读完整产品架构的团队</td><td>解析、hybrid retrieval、UI</td><td>Apache-2.0；不适合当第一个 starter</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">搜索与图</th><td><a href="https://github.com/qdrant/qdrant">Qdrant</a></td><td>⭐⭐⭐⭐⭐</td><td>要练 dense＋sparse search</td><td>hybrid query、fusion、filter</td><td>Apache-2.0；需规划服务与备份</td></tr>
    <tr><td><a href="https://github.com/pgvector/pgvector">pgvector</a></td><td>⭐⭐⭐⭐</td><td>已使用 PostgreSQL 的团队</td><td>SQL、全文与 vector 同库</td><td>仍需索引与查询调校</td></tr>
    <tr><td><a href="https://github.com/microsoft/graphrag">Microsoft GraphRAG</a></td><td>⭐⭐⭐⭐</td><td>研究跨文档关系的读者</td><td>entity graph、local／global search</td><td>MIT；维护模式、indexing 成本高</td></tr>
    <tr><td><a href="https://github.com/HKUDS/LightRAG">LightRAG</a></td><td>⭐⭐⭐⭐</td><td>比较 graph-based RAG 的读者</td><td>graph＋vector retrieval</td><td>MIT；架构不同于 Microsoft GraphRAG</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">评测与优化</th><td><a href="https://github.com/vibrantlabsai/ragas">Ragas</a></td><td>⭐⭐⭐⭐⭐</td><td>要建立可重复运行 eval 的团队</td><td>datasets、metrics、experiments</td><td>Apache-2.0；LLM metric 仍需人工校准</td></tr>
    <tr><td><a href="https://github.com/truera/trulens">TruLens</a></td><td>⭐⭐⭐⭐</td><td>需要 tracing 与 evaluation</td><td>feedback functions、记录与比较</td><td>先确认集成与资料保存方式</td></tr>
    <tr><td><a href="https://github.com/stanfordnlp/dspy">DSPy</a></td><td>⭐⭐⭐⭐⭐</td><td>已有 dataset 与 metric 的开发者</td><td>优化 LLM programs</td><td>MIT；不是初学 RAG 的第一步</td></tr>
    <tr><td><a href="https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide">Anthropic Contextual Retrieval cookbook</a></td><td>⭐⭐⭐⭐⭐</td><td>已完成 baseline 的读者</td><td>contextual chunks 与评测</td><td>供应商示例；数字只适用其设置</td></tr>
  </tbody>
</table>

## ✅ 自我检查

- [ ] 我会先保存 baseline，再一次改一个组件。
- [ ] 我能分清 Hybrid Search 与 Agentic RAG。
- [ ] 我知道 Reranking 不能找回根本没进候选集的文档。
- [ ] 我能说出 GraphRAG 适合的问题，也能说出不该用它的情况。
- [ ] 我的评测同时记录质量、延迟、成本与失败案例。

← [回到 Stage 6：RAG 与 Memory](../stages/06-memory-rag.zh-Hans.md)

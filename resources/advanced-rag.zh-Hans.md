# 进阶 RAG：先找出哪一步坏了，再加新技巧

**RAG**（Retrieval-Augmented Generation）：先找相关资料，再依资料回答。

[繁體中文](advanced-rag.md) | [English](advanced-rag.en.md) | [简体中文](advanced-rag.zh-Hans.md)

<!-- freshness: canonical=resources/advanced-rag.md; verified_on=2026-08-30; scope=rag,retrieval,reranking,graph-rag,evaluation,project-status; max_age_days=90 -->

← [回到 Stage 6：RAG 与 Memory](../stages/06-memory-rag.zh-Hans.md)

基础 RAG 像“先翻书，再回答”。进阶 RAG 不是把更多零件全装上去，而是先看哪一步找错了资料，再只修那一步。

## 📌 学习目标

完成这页后，你可以：

1. 分清楚“找不到”“排序错”“证据不够”“回答乱讲”四种问题。
2. 知道何时该改搜索、重排结果、换问法，或连起跨文档的关系。
3. 用一小组固定问题比较修改前后，不靠一次漂亮回答下结论。
4. 知道什么时候先停在基本 RAG，不增加成本与复杂度。

## 🧩 先认识八个核心术语

<div class="reader-core-terms" align="center" role="region" tabindex="0" aria-label="搜索核心术语" markdown="1">

| 核心词 | 白话说法 | 这里怎么用 |
|:---|:---|:---|
| **Chunk（资料片段）** | 把长文档切成小段 | 搜索时先找片段，并保留它的来源。 |
| **Embedding（向量表示）** | 用一串数字表示文字意思 | 把问题与资料片段转成可比较的数字。 |
| **Vector Search（向量搜索）** | 找意思相近的内容 | 比较向量的相近程度，不只看字是否一样。 |
| **BM25（关键词排名方法）** | 按字词匹配程度排顺序 | 例如找产品编号 AB-123；也考虑字词多常见及文档长度。 |
| **Retriever（检索器）** | 帮你找资料的零件 | 依问题找出可能有用的片段；这些就是“候选资料”。 |
| **Hybrid Search（混合搜索）** | 两种找法一起用 | 合并 BM25 与向量搜索的结果，去掉重复资料。 |
| **Reranking（重新排序）** | 把找到的资料再排一次 | 再看问题与候选资料的关系，把更有用的往前放。 |
| **Baseline（基线）** | 修改前的成绩 | 保存原本系统与测试结果，留待改完后比较。 |

</div>

先看这条路：问题 → 找候选资料 → 重新排序（可选）→ 依资料回答。<strong>Retrieval（检索）</strong>是找资料；<strong>Generation（生成）</strong>是写答案。先分清楚哪一步出错，再改那一步。

## 🩺 先看症状，再选方法

先固定一组问题，并标出每题该找回的资料。`k` 是只看前几条，例如 `k = 5` 就看前五条。

- <strong>Recall@k（前 k 条召回率）</strong>：该找回的资料，前 k 条找回了多少比例。
- <strong>命中率</strong>：这组问题中，有多少比例的题目在前 k 条至少找到一笔相关资料。

例如：一题该找回四份资料，前五条找到两份，Recall@5 就是 50%；这题也算命中。

例如搜索 AB-123 的保固，却只找到其他产品？先看正确资料有没有被找回，再试 BM25。若已找回却排很后面，再试 Reranking。两者都正常，才检查答案是否照着证据写。

<div align="center" markdown="1">

| 你看到的问题 | 先量什么 | 第一个可试的方法 | 先不要做什么 |
|:---|:---|:---|:---|
| 文档里有答案，却没找回 | Recall@k、命中率 | [调整切法或混合搜索](#rag-search) | 先换更大的生成模型 |
| 正确资料有找回，但排很后面 | 人工看前 k 条的顺序 | [重新排序](#rag-search) | 一口气增加很多零件 |
| 问题太模糊，或一次问太多事 | 各问法的命中率与等待时间 | [改写或拆开问题](#rag-query) | 无限制地产生查询 |
| 要连起多份文档的人物、事件 | 准备几题跨文档问题，核对关系 | [先试关系搜索](#rag-graph) | 每个系统都先建图 |
| 问题不需资料也一直搜索 | 多查了几次、花多少钱和时间 | [加入是否搜索的判断](#rag-decisions) | 无上限地重试 |
| 证据正确，答案却不照证据写 | 逐句核对答案与引用 | 改提示词、引用与拒答规则 | 继续改搜索掩盖回答问题 |

</div>

要把排序变成分数时，再用 <strong>MRR（Mean Reciprocal Rank）</strong>看第一笔相关结果是否够前面；用 <strong>nDCG（Normalized Discounted Cumulative Gain）</strong>比较整体排序与理想顺序。核对答案是否受证据支持，叫 **Faithfulness（忠实度）**；它不等于答案符合所有外部事实。

## 📚 必读材料

请照顺序读；它们是学习主线，不藏在选单里。

1. [LangChain：Retrieval 概念](https://docs.langchain.com/oss/python/deepagents/retrieval) — 分清楚保存资料、找资料与决定下一步的零件。
2. [Anthropic：Contextual Retrieval（情境化检索）](https://www.anthropic.com/engineering/contextual-retrieval) — 先替片段补来源背景，再建立搜索用的目录（索引）。
3. [Qdrant：Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/) — 看两路搜索结果如何合并与重新排序。
4. [Weaviate：Hybrid Search](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search) — 看另一种关键字与向量搜索的合并方式。
5. [LangGraph：Agentic RAG（由 Agent 决定何时搜索）](https://docs.langchain.com/oss/python/langgraph/agentic-rag) — 先完成固定的“找资料 → 回答”，再看如何加入判断。
6. [Ragas](https://github.com/vibrantlabsai/ragas) — 把“看起来不错”改成可重跑的数据集与评测回圈。

## 🪜 从基础到进阶的顺序

### 1. 先固定一个最小 Baseline

准备 20–50 个经人工检查的问题，每题保存预期来源与可接受答案。先跑目前的版本，记录找回的资料、答案、等待时间（延迟）与成本。接着一次只改一件事，才知道是哪个改动有帮助。

<a id="rag-search"></a>
### 2. 先修 Retrieval，再修 Generation

- **Chunking（切分资料）**：先按标题与段落切。再比较固定长度（fixed-size）、先找小段再带回大段（parent-child），或按意思分段（semantic chunking）。
- **Metadata Filter（附加资料筛选）**：用片段的产品名称、日期或权限等标签缩小范围。先确认筛选没有挡掉正确资料。
- **Hybrid Search**：BM25 补字词匹配，向量搜索补意思相近的内容；先测合并后是否真的找得更多。
- **Reranking** 不会创造新文档；它只把已找回的候选重新排列。

文档也会提到 <strong>dense（密集向量）</strong>与 **sparse（稀疏向量）**：前者通常大多数位置有数值，后者多数位置是零。<strong>Fusion（融合）</strong>是合并不同搜索的分数或排名。向量的疏密本身不保证搜索质量。

<a id="rag-query"></a>
### 3. 问题不好找时，再做 Query Transformation

<strong>Query Transformation（查询转换）</strong>是把问题换个问法，或拆成小题后再找。先选一种试，不必全加。

- **Multi-Query**：把同一问题改成几种说法，各自搜索后合并。
- **HyDE（Hypothetical Document Embeddings）**：先写假想答案，转成向量，再找真实资料。假想内容不是证据，也可能把搜索带偏。
- **RAG Fusion**：合并多种问法得到的排名，降低单一措辞的影响。
- **Decomposition**：把“比较 A、B 并解释原因”拆成数个可以分别找证据的小问题。

<a id="rag-graph"></a>
### 4. 需要跨文档关系时，才考虑 GraphRAG

**GraphRAG**把文档中的人物、组织等“实体”及彼此的关系连成图，再用来找证据。例如把“谁参与哪个计划”跨文档连起来。单份问答或精确条款，通常先用一般检索器就够了。

**Microsoft GraphRAG** 是研究参考实现，官方目前标示为 largely in maintenance mode，仍修 bug 与依赖问题，但不再以新增功能为主。它的 indexing 可能昂贵，应先用小数据集。**LightRAG** 是另一套活跃的 graph-based RAG 实现，资料模型与 Microsoft GraphRAG 不相同，不能把两者当成同一产品。

先拿“哪些人物共同影响这件事？”或“整批文档有哪些主题？”测试，确认建图的成本有换到更好的答案。

<a id="rag-decisions"></a>
### 5. 流程需要判断时，才加 Corrective 或 Agentic RAG

前面的做法大多照固定步骤搜索、回答。只有需要“现在要不要查、查不好怎么办”时，才增加下面的判断。

- **Self-RAG**：模型学习何时检索，并对证据与回答做反思。
- **CRAG**（Corrective Retrieval Augmented Generation，也叫 Corrective RAG）：先判断候选是否够好，不够时改查询或改来源。
- **Adaptive RAG**：依问题难度选择不同流程。
- **Agentic RAG**：让 agent 决定何时调用 retriever；必须设定步数、时间、成本与可用来源上限。

原始入口：[Self-RAG](https://arxiv.org/abs/2310.11511)、[CRAG](https://arxiv.org/abs/2401.15884)、[Adaptive-RAG](https://arxiv.org/abs/2403.14403)。

### 6. 最后才碰摘要树与程序优化

**RAPTOR**（Recursive Abstractive Processing for Tree-Organized Retrieval）把相近片段分组、写摘要，再逐层合成较大的摘要。细节问题找原片段，主题问题找上层摘要。

**DSPy**用示例与评分规则，调整 LLM（Large Language Model，能读写语言的模型）的提示词或示范，改善整个流程。先有清楚任务、可靠资料与评测，才适合用它。

阅读：[RAPTOR paper](https://arxiv.org/abs/2401.18059) · [DSPy](https://github.com/stanfordnlp/dspy)

## 🛠 一个可重复运行的小实验

1. 选 20 题，为每题标出正确来源。
2. **A：基线**。只用向量搜索，保存前五条结果与答案。
3. **B：混合搜索**。保留 A，只加入 BM25 并合并结果，重跑同一批题目。
4. **C：再加排序**。保留 B，只加入重新排序，重跑同一批题目。
5. 三组都记录 Recall@5、命中率、延迟与成本。其余设定相同，写下哪几题变好或变差。

**完成条件：** 你能拿出同一份测试集的三组结果，而不是只展示一题成功案例。

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

<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="精选项目与学习资源">
<table align="center">
  <thead><tr><th scope="col">分类</th><th scope="col">项目／文档</th><th scope="col">评分</th><th scope="col">用途</th><th scope="col">限制</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">流程与示例</th><td><div data-field="entry"><strong><a href="https://github.com/run-llama/llama_index">LlamaIndex</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>适合谁：</strong> 文档型应用开发者</div><div data-field="learn"><strong>能学什么：</strong> 找资料、组织回答与评测</div></td><td><div data-field="status"><strong>状态／限制：</strong> MIT；套件多，先跟官方 starter</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/deepset-ai/haystack">Haystack</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>适合谁：</strong> 想把处理步骤拆成小组件</div><div data-field="learn"><strong>能学什么：</strong> 拆分组件、选路与搜索</div></td><td><div data-field="status"><strong>状态／限制：</strong> Apache-2.0；先做小型流程</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/NirDiamant/RAG_Techniques">RAG_Techniques</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>适合谁：</strong> 想比较技术的读者</div><div data-field="learn"><strong>能学什么：</strong> 可运行 notebooks 与技术对照</div></td><td><div data-field="status"><strong>状态／限制：</strong> 自定义非商业授权；商用须书面许可；事实回官方文档核对</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/infiniflow/ragflow">RAGFlow</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>适合谁：</strong> 想读完整产品架构的团队</div><div data-field="learn"><strong>能学什么：</strong> 读取文档、混合搜索与操作界面</div></td><td><div data-field="status"><strong>状态／限制：</strong> Apache-2.0；不适合当第一个 starter</div></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">搜索与图</th><td><div data-field="entry"><strong><a href="https://github.com/qdrant/qdrant">Qdrant</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>适合谁：</strong> 要合并密集与稀疏向量搜索</div><div data-field="learn"><strong>能学什么：</strong> 合并搜索结果与筛选资料</div></td><td><div data-field="status"><strong>状态／限制：</strong> Apache-2.0；需规划服务与备份</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/pgvector/pgvector">pgvector</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>适合谁：</strong> 已使用 PostgreSQL 的团队</div><div data-field="learn"><strong>能学什么：</strong> 在同一数据库做文字与向量搜索</div></td><td><div data-field="status"><strong>状态／限制：</strong> 仍需索引与查询调校</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/microsoft/graphrag">Microsoft GraphRAG</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>适合谁：</strong> 研究跨文档关系的读者</div><div data-field="learn"><strong>能学什么：</strong> 实体关系、局部与整体主题搜索</div></td><td><div data-field="status"><strong>状态／限制：</strong> MIT；维护模式、建索引成本高</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/HKUDS/LightRAG">LightRAG</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>适合谁：</strong> 比较以关系图找证据的读者</div><div data-field="learn"><strong>能学什么：</strong> 关系图与向量搜索</div></td><td><div data-field="status"><strong>状态／限制：</strong> MIT；架构不同于 Microsoft GraphRAG</div></td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">评测与优化</th><td><div data-field="entry"><strong><a href="https://github.com/vibrantlabsai/ragas">Ragas</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>适合谁：</strong> 要重跑评测的团队</div><div data-field="learn"><strong>能学什么：</strong> 测试数据、评分与实验比较</div></td><td><div data-field="status"><strong>状态／限制：</strong> Apache-2.0；模型评分仍需人工校准</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/truera/trulens">TruLens</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>适合谁：</strong> 想追查执行过程并评测</div><div data-field="learn"><strong>能学什么：</strong> 自定义评分、记录与比较</div></td><td><div data-field="status"><strong>状态／限制：</strong> 先确认集成与资料保存方式</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://github.com/stanfordnlp/dspy">DSPy</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>适合谁：</strong> 已有测试数据与评分规则的开发者</div><div data-field="learn"><strong>能学什么：</strong> 改善模型的工作流程</div></td><td><div data-field="status"><strong>状态／限制：</strong> MIT；不是初学 RAG 的第一步</div></td></tr>
    <tr><td><div data-field="entry"><strong><a href="https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide">Anthropic Contextual Retrieval cookbook</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="audience"><strong>适合谁：</strong> 已完成 baseline 的读者</div><div data-field="learn"><strong>能学什么：</strong> 片段补背景与评测</div></td><td><div data-field="status"><strong>状态／限制：</strong> 供应商示例；数字只适用其设置</div></td></tr>
  </tbody>
</table>
</div>

## ✅ 自我检查

- [ ] 我会先保存 baseline，再一次改一个组件。
- [ ] 我能分清 Hybrid Search 与 Agentic RAG。
- [ ] 我知道 Reranking 不能找回根本没进候选集的文档。
- [ ] 我能说出 GraphRAG 适合的问题，也能说出不该用它的情况。
- [ ] 我的评测同时记录质量、延迟、成本与失败案例。

← [回到 Stage 6：RAG 与 Memory](../stages/06-memory-rag.zh-Hans.md)

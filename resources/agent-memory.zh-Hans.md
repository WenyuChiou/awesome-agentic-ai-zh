# Agent Memory：只记值得记、允许记、能删掉的事

[繁體中文](agent-memory.md) | [English](agent-memory.en.md) | [简体中文](agent-memory.zh-Hans.md)

<!-- freshness: canonical=resources/agent-memory.md; verified_on=2026-08-30; scope=memory,privacy,retention,isolation,project-status; max_age_days=90 -->

← [回到 Stage 6：RAG 与 Memory](../stages/06-memory-rag.zh-Hans.md)

**Agent Memory（代理记忆）**像一本有管理规则的笔记本。它不是把所有聊天偷偷存起来；它只保存之后真的需要、用户允许，而且可以查看、修改与删除的内容。

## 📌 学习目标

完成这页后，你可以：

1. 分清聊天记录、context、RAG 与 Memory。
2. 分清短期／长期，以及 semantic／episodic／procedural memory。
3. 画出一笔记忆从写入、搜索、更新到删除的生命周期。
4. 为每笔记忆设置拥有者、来源、保存期限与删除方法。
5. 用固定测试检查“该记的找得到，不该记的不会留下”。

## 🧩 先把四样东西分开

| 核心术语 | 好理解的说法 | 正确意思 |
|---|---|---|
| **Chat History（聊天记录）** | 这次对话的逐字稿 | 消息记录；不代表每一则都应永久保存或放进模型 context。 |
| **Context（上下文）** | 这一刻放在桌上的资料 | 本次模型调用实际看到的 instructions、messages、工具结果与取回内容。 |
| **RAG** | 有问题时去书架找资料 | 从外部知识来源取回证据，再交给模型回答。 |
| **Memory（记忆）** | 助理留给下次的短笔记 | 跨步骤、thread 或 session 仍需读回的状态，必须有写入与治理规则。 |

**最重要的判断：**产品手册放知识库；当前任务做到哪里放短期 state；经用户同意保存的偏好才可能进入长期 memory。

## 📚 必读材料

1. [LangChain：Memory overview](https://docs.langchain.com/oss/python/concepts/memory) — 先理解 thread-scoped short-term memory、跨 session long-term memory，以及 semantic／episodic／procedural 三种类型。
2. [LangGraph：Add and manage memory](https://docs.langchain.com/oss/python/langgraph/add-memory) — 看 checkpointer、store、namespace 与 semantic search 的实现边界。
3. [CoALA paper](https://arxiv.org/abs/2309.02427) — 用共同框架理解 language agent 的 memory 结构与操作。
4. [Generative Agents paper](https://arxiv.org/abs/2304.03442) — 看 recency、importance、relevance 与 reflection 的经典研究设计。
5. [Mem0](https://github.com/mem0ai/mem0) 或 [Letta Code](https://github.com/letta-ai/letta-code) — 选一个现行实现，观察状态如何保存与取回。[Letta 项目入口](https://github.com/letta-ai/letta)目前是 landing page；现行 source 与 App Server 都在 Letta Code。

## ⏱ 两种时间范围

- **Short-term Memory（短期记忆）**：只服务一个 thread 或当前任务，例如消息、上传文件、工具结果与做到哪一步。LangGraph 通常把它放在 thread-scoped state，通过 checkpointer 保存。
- **Long-term Memory（长期记忆）**：跨 thread 或 session 仍需要，例如用户允许保存的偏好、项目事实或可重用经验。它必须用 namespace 隔离不同用户与应用。

短期不等于“只放 RAM”；长期也不等于“永远不删”。差别在取回范围与生命周期，不是硬盘或内存的名称。

## 🧠 三种内容类型

| 类型 | 记什么 | 例子 | 风险 |
|---|---|---|---|
| **Semantic Memory（语义记忆）** | 较稳定的事实 | 用户偏好短答、项目使用 Python 3.13 | 事实会过期或互相冲突 |
| **Episodic Memory（情节记忆）** | 发生过的事件与结果 | 上次部署在哪一步失败、哪个修法有效 | 成功一次不代表永远适用 |
| **Procedural Memory（程序记忆）** | 做事规则与步骤 | 发版前要跑哪些 gate | 恶意内容可能污染未来行为 |

**Semantic memory** 和 **semantic search** 不是同一件事：前者是记住的内容类型，后者是按意思相近来搜索的取回方法。

## 🔄 一笔 Memory 的生命周期

1. **提议写入**：先判断是否真的需要跨 session 使用。
2. **取得同意**：敏感资料或个人偏好要让用户知道保存目的。
3. **规范化**：保存简短事实，不直接把整段聊天当记忆。
4. **加上 metadata**：至少有 owner、source、created_at、updated_at、expires_at 与 sensitivity。
5. **隔离保存**：用 user／workspace／agent namespace 分开，查询前先套权限。
6. **搜索与使用**：只取回与当前任务相关的少量记忆，并保留来源。
7. **更新或解决冲突**：新信息不能悄悄和旧信息并存；要标记版本或取代关系。
8. **删除与遗忘**：用户可查看、修改、删除；过期资料自动清除，备份也要有处理规则。

## 🧱 先选最简单的设计

| 问题 | 先用什么 | 何时升级 |
|---|---|---|
| 字段固定，例如语言、时区、通知偏好 | **直接状态表** | 字段种类变多或需要模糊搜索时 |
| 内容较自由，例如短摘要或可重用经验 | **可搜索文字 memory** | 关系、时间与冲突成为主要问题时 |
| 人、事件与关系会随时间改变 | **Temporal Knowledge Graph** | 只有测试证明一般资料表／搜索不够时 |
| 只需恢复同一个工作流程 | **Checkpoint／thread state** | 真正需要跨 thread 分享时 |

**先从资料表开始。**能用明确字段保存的内容，不必先做向量搜索；能用短期 state 解决的问题，不必先做永久记忆。

## 🛡️ Memory 的安全底线

- 默认不保存密码、API key、付款资料、医疗秘密或未经同意的个人资料。
- 不让不同用户、tenant、workspace 或 agent 共用同一个未隔离 namespace。
- 取回前做权限检查；不能先拿到秘密再靠 prompt 要模型“不要说”。
- 记忆内容是不可信输入。写入前做 schema、来源与 prompt-injection 检查。
- 每笔记忆要能回答“谁写的、从哪里来、何时更新、何时删”。
- 删除要涵盖主要存储、搜索索引、cache 与依政策管理的备份。

## 🛠 一个最小 Memory 练习

只保存一项无敏感性的偏好，例如“回答先给短版”。

1. 写入偏好与 `user_id`、来源、时间、保存期限。
2. 用另一个 thread 搜索并读回。
3. 把偏好改成“先给表格”，确认旧值不再被使用。
4. 删除偏好，再搜索一次，结果必须为空。
5. 用另一个 `user_id` 查询，不能看到前一位用户的内容。

**完成条件：**add、search、update、delete 与 user isolation 五项测试都通过；只会 `add` 不算完成。

<details markdown="1">
<summary>Hot path、Background 与冲突处理</summary>

- **Hot path write**：回答前立即写入，结果最新，但会增加延迟，错误也直接影响用户。
- **Background write**：回复后异步整理，交互较快，但要处理失败、重试与晚到更新。
- 同一事实有新旧版本时，保存时间、来源与有效范围；不要只依向量相似度随机挑一笔。
- 先把“模型建议的 memory”放入待确认区，再由规则或用户批准，适合高风险内容。

</details>

<details markdown="1">
<summary>常见失败与排查顺序</summary>

1. 找不到：先看 namespace、权限、filter 与保存是否成功。
2. 找到旧资料：看 update 是否留下互相冲突的版本，以及 cache 是否刷新。
3. 记太多：提高写入门槛、缩短保存期限，不要只扩大 context window。
4. 记错：保留来源与信心，让用户能修改，不把模型推测直接当事实。
5. 删不干净：追踪主库、索引、cache、事件串流与备份的删除路径。

</details>

## 🎯 精选 Projects 与学习资源

评分代表“对这张学习地图的教学价值”，不是项目质量排行榜。先选一种 memory 形状，再选工具。

<small>资料核查：2026-08-30 UTC</small>

<table>
  <thead><tr><th scope="col">分类</th><th scope="col">项目／资源</th><th scope="col">编辑评分</th><th scope="col">适合谁</th><th scope="col">能学什么</th><th scope="col">状态／限制</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Memory layer</th><td><a href="https://github.com/mem0ai/mem0">Mem0</a></td><td>⭐⭐⭐⭐⭐</td><td>第一次做跨 session memory</td><td>library、server、cloud 与搜索生命周期</td><td>Apache-2.0；OSS 与 managed 能力分开看</td></tr>
    <tr><td><a href="https://github.com/langchain-ai/langmem">LangMem</a></td><td>⭐⭐⭐⭐</td><td>已使用 LangGraph 的团队</td><td>hot-path／background memory</td><td>MIT；先理解 LangGraph store</td></tr>
    <tr><td><a href="https://github.com/letta-ai/letta">Letta 项目入口</a></td><td>⭐⭐⭐⭐</td><td>先分清 Letta 的产品范围</td><td>现行安装、文档与 source 去向</td><td>landing page；退役 V1 server 只留在 archive branch</td></tr>
    <tr><td><a href="https://github.com/letta-ai/letta-code">Letta Code</a></td><td>⭐⭐⭐⭐</td><td>建立 stateful agent 或 App Server</td><td>agent harness、git-backed MemFS、长期 identity</td><td>现行 source；产品型 agent harness，不是通用 memory DB</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">时间与关系</th><td><a href="https://github.com/getzep/graphiti">Graphiti</a></td><td>⭐⭐⭐⭐⭐</td><td>关系会随时间改变的应用</td><td>bi-temporal facts、temporal graph</td><td>Apache-2.0；需要图数据库与治理</td></tr>
    <tr><td><a href="https://github.com/getzep/zep">Zep examples</a></td><td>⭐⭐⭐</td><td>评估 Zep Cloud 的团队</td><td>集成与示例入口</td><td>旧 Community Edition 已移到 legacy／deprecated</td></tr>
    <tr><td><a href="https://docs.langchain.com/oss/python/concepts/memory">LangChain Memory overview</a></td><td>⭐⭐⭐⭐⭐</td><td>想先学清楚概念的读者</td><td>thread state、store、三种 memory 类型</td><td>框架文档；概念可移植，API 需看版本</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">研究与评测</th><td><a href="https://arxiv.org/abs/2309.02427">CoALA</a></td><td>⭐⭐⭐⭐⭐</td><td>研究 agent memory 架构</td><td>working、episodic、semantic、procedural</td><td>分析框架，不是可安装产品</td></tr>
    <tr><td><a href="https://arxiv.org/abs/2304.03442">Generative Agents</a></td><td>⭐⭐⭐⭐⭐</td><td>研究反思与记忆取回</td><td>recency、importance、relevance</td><td>经典研究，不是 production 标准答案</td></tr>
    <tr><td><a href="https://arxiv.org/abs/2303.11366">Reflexion</a></td><td>⭐⭐⭐⭐</td><td>研究经验反馈的读者</td><td>verbal feedback 与下一次尝试</td><td>reflection 只有持久保存后才成为跨 session memory</td></tr>
    <tr><td><a href="https://github.com/mem0ai/memory-benchmarks">Mem0 Memory Benchmarks</a></td><td>⭐⭐⭐⭐</td><td>要测 memory quality 的开发者</td><td>数据集与可重复运行评测入口</td><td>供应商维护；自行加入 isolation／deletion 测试</td></tr>
  </tbody>
</table>

## ✅ 自我检查

- [ ] 我不会把 Chat History、Context、RAG 与 Memory 当成同一件事。
- [ ] 每笔长期 memory 都有 owner、source、时间与删除方法。
- [ ] 我能解释 semantic memory 和 semantic search 的差别。
- [ ] 我测过更新、删除、过期与跨用户隔离，不只测写入和搜索。
- [ ] 敏感资料默认不写入，用户能看见并控制被保存的内容。

← [回到 Stage 6：RAG 与 Memory](../stages/06-memory-rag.zh-Hans.md)

# 术语小词典（Glossary）

> [繁體中文](./glossary.md) | **简体中文** | [English](./glossary.en.md)

看到陌生英文时，不用停下整章。先在这里找到一句白话解释，再回原来的 Stage 继续做。

## ⚡ 先从 12 个词开始

- [**Prompt（提示词）**](#prompt提示词) — 你交给模型的完整任务包，包含要做什么、数据、示例和限制。
- [**Token**](#token) — 模型切分文字时使用的小单位；计费和可读长度常用它计算。
- [**Context Window（上下文视窗）**](#context-window上下文视窗) — 模型这一次最多能一起参考的信息空间。
- [**Agent**](#agent代理人) — 会在限制内选择动作、查看结果，再决定下一步的系统。
- [**Tool Use（工具使用）**](#tool-use--function-calling) — 模型提出工具请求，程序检查后才真正执行。
- [**Agent Loop**](#agent-loop) — Agent 重复“决定、行动、观察”，直到完成或停止的执行循环。
- [**RAG**](#ragretrieval-augmented-generation) — 先找数据，再把证据交给模型回答。
- [**Memory（记忆）**](#memory记忆-两种正交分类轴) — 把以后还要用的信息保存起来，再在需要时读回。
- [**MCP**](#mcpmodel-context-protocol) — 让 AI 应用用共同方式连接工具和数据的开放协议。
- [**Eval（评估）**](#eval评估) — 用固定题目和成功条件检查改动是否真的变好。
- [**Agent Harness（执行工作台）**](#agent-harness执行工作台) — 包住模型并管理工具、权限、状态、记录和停止规则的系统。
- [**Workflow Graph（工作流程图）**](#workflow-graph工作流程图) — 用节点和连接把工作步骤、分支和状态画清楚。

## 🧭 先分清五种工具身份

同一个界面可能同时出现模型、Router 和 Agent。先问“它负责哪一件事”，就不会把产品名称混在一起。

<table>
<thead>
<tr><th>身份</th><th>白话工作</th><th>示例和边界</th></tr>
</thead>
<tbody>
<tr><td><strong>Model Provider／API</strong></td><td>模型公司的服务入口。</td><td><a href="https://platform.claude.com/docs/en/api/overview">Anthropic API</a>；它返回模型结果，不是会修改文件的 Agent。</td></tr>
<tr><td><strong>LLM Router</strong></td><td>用一个入口转接模型或供应商。</td><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a>；它不是模型，也不是 coding agent。</td></tr>
<tr><td><strong>Model Runtime</strong></td><td>把模型在本机或服务上运行起来。</td><td><a href="https://docs.ollama.com/api/introduction">Ollama</a>；它提供模型 API，本身不会自动修改项目。</td></tr>
<tr><td><strong>Coding Agent／Harness</strong></td><td>读取文件、修改文件、运行命令并报告结果。</td><td><a href="https://opencode.ai/docs">OpenCode</a>、<a href="https://github.com/earendil-works/pi">Pi</a>；里面的模型可以更换。</td></tr>
<tr><td><strong>Agent Framework</strong></td><td>让开发者组合 Agent、工具、状态和流程。</td><td><a href="https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/">Microsoft Agent Framework</a>；它是工具箱，不等于一个模型。</td></tr>
</tbody>
</table>

<details markdown="1">
<summary>维护者：项目固定术语对照（37 个）</summary>

这张表用来保持跨 Stage 命名一致。普通读者不用先背。

<table>
<thead>
<tr><th>类型</th><th>英文术语</th><th>中文理解名</th><th>主要 Stage</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="2">输入和信息</th><td>Prompt Engineering</td><td>Prompt 设计</td><td>Stage 2</td></tr>
<tr><td>Context Engineering</td><td>上下文管理</td><td>Stage 6／7</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="17">Agent 执行</th><td>Agent Production Engineering</td><td>Agent 可用化工程</td><td>Stage 7</td></tr>
<tr><td>Harness Engineering</td><td>Agent 执行系统设计</td><td>Stage 7</td></tr>
<tr><td>Loop Engineering</td><td>Agent 循环设计</td><td>Stage 7</td></tr>
<tr><td>Graph Engineering</td><td>Workflow Graph 工程</td><td>Stage 4／7</td></tr>
<tr><td>Tool Use</td><td>工具使用</td><td>Stage 3</td></tr>
<tr><td>Function Calling</td><td>函数／工具调用</td><td>Stage 3</td></tr>
<tr><td>Tool Schema</td><td>工具纲要／工具说明卡</td><td>Stage 3</td></tr>
<tr><td>Tool Call</td><td>工具请求</td><td>Stage 3</td></tr>
<tr><td>Tool Result</td><td>工具结果</td><td>Stage 3</td></tr>
<tr><td>Structured Output</td><td>结构化输出</td><td>Stage 3</td></tr>
<tr><td>Agent Loop</td><td>Agent 执行循环</td><td>Stage 3</td></tr>
<tr><td>Framework</td><td>框架／工具箱</td><td>Stage 4</td></tr>
<tr><td>Orchestration</td><td>协调和编排</td><td>Stage 4／7</td></tr>
<tr><td>Handoff</td><td>任务交接</td><td>Stage 7</td></tr>
<tr><td>Supervisor／Worker</td><td>协调者／执行者</td><td>Stage 7</td></tr>
<tr><td>Runtime</td><td>执行层</td><td>Stage 7</td></tr>
<tr><td>Scaffolding</td><td>支撑架构</td><td>Stage 7</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="9">质量和上线</th><td>Observability</td><td>观测和记录</td><td>Stage 7</td></tr>
<tr><td>Telemetry</td><td>运行记录</td><td>Stage 7</td></tr>
<tr><td>Eval</td><td>效果评估</td><td>Stage 7</td></tr>
<tr><td>Evaluation Harness</td><td>评估框架</td><td>Stage 7</td></tr>
<tr><td>Production</td><td>可稳定使用／上线化</td><td>Stage 7</td></tr>
<tr><td>Production-grade</td><td>可长期稳定使用的</td><td>Stage 7</td></tr>
<tr><td>Deployment</td><td>部署</td><td>Stage 7</td></tr>
<tr><td>Cost Tracking</td><td>成本跟踪</td><td>Stage 7</td></tr>
<tr><td>Latency</td><td>延迟／等待时间</td><td>Stage 7</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">检索和模型</th><td>Vector DB</td><td>向量数据库</td><td>Stage 6</td></tr>
<tr><td>Retrieval</td><td>检索</td><td>Stage 6</td></tr>
<tr><td>Reranking</td><td>重排序</td><td>Stage 6</td></tr>
<tr><td>Long Context</td><td>长上下文</td><td>Stage 6</td></tr>
<tr><td>Fine-tuning</td><td>模型微调</td><td>Stage 6</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">操作界面</th><td>Agent Interfaces</td><td>Agent 操作界面</td><td>Stage 8</td></tr>
<tr><td>Code Sandbox</td><td>隔离代码执行环境</td><td>Stage 8</td></tr>
<tr><td>Cold Start</td><td>启动延迟</td><td>Stage 8</td></tr>
<tr><td>Reward Hacking</td><td>钻评分漏洞</td><td>Stage 7／8</td></tr>
</tbody>
</table>

</details>

## 📚 按主题查词

下面不是新的阅读顺序。直接跳到你刚看到的词即可。

## 1. 基本概念

### LLM（Large Language Model，大语言模型）

**LLM** 是会按照输入和已经学到的模式生成内容的模型。它可以提出工具请求，但真正读取文件、联网或发送信息的，是外面的程序。

📍 详情：[Stage 1](../stages/01-llm-basics.zh-Hans.md)

### Model Provider / Provider API（模型供应商／模型 API）

**Model Provider／Provider API** 是模型公司的服务入口。你的程序发送消息，供应商返回结果并按照方案计费；它不是 coding agent。

### LLM Router / API Router（模型路由器）

**LLM Router／API Router** 像总机：同一个 API 可以按照设置转到不同模型或后端。Router 帮你选路，不会自己变成模型或 Agent。

### Model Runtime（模型执行环境）

**Model Runtime** 是把模型加载起来并提供推理 API 的执行环境。Ollama、llama.cpp 和 [MLX LM](https://github.com/ml-explore/mlx-lm) 属于这一类；要让它读取文件或运行命令，还要接上 Agent 或应用程序。MLX 本身是 array framework；这里指的是用 MLX 运行 LLM 的 MLX LM。

### Token

**Token** 是模型切分文字或其他输入时使用的小单位。每个 tokenizer 的切法不同，所以不要用固定的“一个字等于几个 token”公式；需要估算时使用所选模型的计数工具。

📍 详情：[Stage 1](../stages/01-llm-basics.zh-Hans.md)

### Context Window（上下文视窗）

**Context Window** 是模型这一次能一起参考的 token 空间。空间大不代表每段数据都会受到同样注意；先放任务真正需要的内容，再到 [Stage 1](../stages/01-llm-basics.zh-Hans.md)查看当前型号的正式上限。

### Prompt（提示词）

**Prompt** 是交给模型的完整任务包，不只是一句问题。它可以包含指令、输入数据、背景、示例、成功条件和输出格式；**Prompt Engineering** 是设计并用 Eval 测试这份任务包。

📍 详情：[Stage 2](../stages/02-prompt-engineering.zh-Hans.md)

### Zero-shot / One-shot / Few-shot

这三个词只是在数 Prompt 里有几个示范：

- **Zero-shot**：不给示范，直接交代任务。
- **One-shot**：先给一个输入和答案的示例。
- **Few-shot**：先给少量示例，展示格式或边界。

示例多不一定更好；用同一组 Eval 比较才知道。

### Chain-of-Thought（CoT，思维链）

**Chain-of-Thought（CoT）** 是让模型经过中间推理步骤再回答的 prompting 研究方法。早期研究包含 [Few-shot CoT](https://arxiv.org/abs/2201.11903) 和 [Zero-shot CoT](https://arxiv.org/abs/2205.11916)。实际使用时通常要求简短、可核对的理由和证据，不要求公开模型的私有推理全文。

## 模型训练与调整

### Pre-training（预训练）

**Pre-training** 是用大量数据让模型先学会一般模式。它会改变模型权重，产生之后还能继续调整的 Base Model。

### Post-training（后训练）

**Post-training** 是 Base Model 完成后的训练阶段。它用示范、偏好或反馈，让模型更会遵循指令、安全地完成任务。

### Inference（推理）

**Inference** 是模型训练完成后，收到这一次输入并产生这一次结果。它是在使用模型，不是在重新训练模型。

### Fine-tuning（模型微调）

**Fine-tuning** 用较小、较专门的数据继续调整模型权重。它适合反复出现的行为或格式；每天变化的事实通常改用 RAG 或工具读取。

### SFT（Supervised Fine-Tuning）

**SFT** 把好的输入和答案交给模型模仿。它是常见的 Post-training 方法，会调整模型权重。

### DPO（Direct Preference Optimization）

**DPO** 让模型从“较好答案”和“较差答案”的配对中学习偏好。它需要可信的偏好数据，也会调整权重。

### RLHF / RL

**RLHF/RL** 用人类或规则的反馈来训练模型。反馈设计错误时，模型也可能学会钻评分漏洞，所以仍要做独立 Eval。

### GRPO

**GRPO** 让同一问题的多个答案互相比较，再根据相对表现更新模型。它是 Post-training 方法之一，不是每个项目都必须使用。

### PEFT / LoRA

**PEFT** 是只训练较少参数的一组方法；**LoRA** 会冻结原来的权重，再训练新增的低秩矩阵。它们能减少需要更新的参数，但仍需要数据与 Eval。

### Distillation（蒸馏）

**Distillation** 让较小的 Student Model 学习较大的 Teacher Model。目标常是缩小模型或降低推理成本，但效果要用自己的任务测试。

📍 选修导览：[模型训练与调整指南](model-training-guide.zh-Hans.md)

## 2. Agent / 工具使用

### Agent（代理人）

**Agent** 是会在限制内读取状态、选择动作、执行并观察结果的系统。它至少需要模型、可用动作和停止条件；不是只要接上一个 LLM 就会自动做完工作。

### Tool Use / Function Calling

**Tool Use／Function Calling** 是模型提出结构化工具请求的机制。模型只是在说“想调用什么”；你的程序仍要检查工具名称、参数和权限后才执行。

📍 详情：[Stage 3](../stages/03-tool-use-and-hello-agent.zh-Hans.md)

### Tool Schema（工具纲要）

**Tool Schema** 是工具说明卡，列出名称、用途、输入字段、类型和必填条件。Schema 可以限制格式，但不能保证模型给出的内容安全或真实。

### Tool Call（工具请求）

**Tool Call** 是模型发送的工具名称和参数。它是不可信输入；程序要先验证，再决定执行、拒绝或请人批准。

### Tool Result（工具结果）

**Tool Result** 是程序执行工具后交回模型的结果。成功、失败和原来的 call ID 要对应，模型才知道下一步该做什么。

### ReAct（Reasoning + Acting）

**ReAct** 把可观察的 Action 和 Observation 交替放进任务流程，让模型根据新结果决定下一步。它来自 [ReAct paper](https://arxiv.org/abs/2210.03629)；实际实现仍要有最大步数、工具权限和停止条件。

### Structured Output（结构化输出）

**Structured Output** 要求输出符合 JSON Schema 或类型。它能让程序稳定解析格式，但格式正确不等于内容正确，仍要验证数值、来源和业务规则。

### Agent Loop

**Agent Loop** 是一次执行里真正重复的流程：模型决定动作，程序执行，模型读回结果，再决定下一步。循环必须能在完成、错误、超时、超预算或达到步数上限时停止。

### Workflow Graph（工作流程图）

**Workflow Graph** 用 node、edge、branch 和 state 明确排出工作路线。一个 node 可以放 Agent Loop、普通程序、工具或人工批准；它不是每个 Agent 都必须使用的形状。

📍 详情：[Stage 4](../stages/04-agent-frameworks.zh-Hans.md)

### Self-Refine（基础反思 / 无记忆）

**Self-Refine** 让模型先生成答案，再根据反馈修改一次或多次。原始方法见 [Self-Refine paper](https://arxiv.org/abs/2303.17651)；如果没有外部检查和停止条件，重写很多次仍可能一直出错。

## 3. Memory / Retrieval / RAG

### Memory（记忆）— 两种正交分类轴

**Memory** 是把以后还要用的信息写入某个存储层，再在需要时读回。可以按照保存时间分成短期／长期，也可以按照内容分成 episodic、semantic、procedural；这是两条不同分类轴。

### RAG（Retrieval-Augmented Generation）

**RAG** 是“先检索证据，再让模型根据证据回答”。原始方法见 [RAG paper](https://arxiv.org/abs/2005.11401)。它不会自动保证正确；还要测试数据质量、检索命中、引用和回答忠实度。

📍 详情：[Stage 6](../stages/06-memory-rag.zh-Hans.md)

### Reflexion（完整反思 / 带 episodic memory）

**Reflexion** 会把以前的尝试、反馈和反思保存为 episodic memory，让以后的尝试参考。它比单次 Self-Refine 多了跨尝试的记忆；原始方法见 [Reflexion paper](https://arxiv.org/abs/2303.11366)。

### Embedding（嵌入）

**Embedding** 把文字、图片或其他数据转成向量，让系统能比较相似度。Dense 和 sparse 表示擅长的信号不同；要用自己的查询集测试，而不是只看维度大小。

### Vector DB（向量数据库）

**Vector DB** 保存向量、metadata 和索引，并找出相近项目。它是检索层，不是 RAG 的全部；切块、查询、Reranking 和回答仍是其他步骤。

### Semantic Search（语义搜索）

**Semantic Search** 按照意思相近程度查找数据，不只比较相同文字。它适合同义问法，但专有名词、编号和精确字符串常要搭配关键词搜索。

### Chunking（切块）

**Chunking** 把长文档切成可检索的小段。切法要和文档结构、实际问题一起测试；不存在适合所有数据的固定大小。

### Hybrid Search（混合搜索）

**Hybrid Search** 同时使用语义向量和关键词信号，再把结果合并。它常用来兼顾“意思相近”和“名称必须完全命中”。

### Reranking（重新排序）

**Reranking** 让第二个模型或规则重新检查初步候选，把更符合问题的内容排到前面。它可能提高质量，也会增加等待时间和成本。

### Contextual Retrieval

**Contextual Retrieval** 先给每个 chunk 补上它在原文档中的简短背景，再建立搜索索引。Anthropic 的[方法说明](https://www.anthropic.com/engineering/contextual-retrieval)把 contextual embeddings 和 contextual BM25 一起评估；效果仍要用自己的数据测试。

## 4. Multi-Agent

### Multi-Agent（多 agent）

**Multi-Agent** 是让两个以上 Agent 分工或互相交接。只有当角色、工具、权限或 context 真的需要分开时才值得使用；数量变多不代表答案一定更好。

### Handoff

**Handoff** 是把任务和必要 context 从一个 Agent 交给另一个 Agent。好的交接要说清楚目标、已完成事项、证据、剩余工作和停止条件。

### A2A（Agent-to-Agent）Protocol

**A2A** 是让彼此独立、内部可能不透明的 Agent 发现能力、交换消息和管理协作任务的开放协议。它处理 Agent 对 Agent 的互通；当前规范和版本看[官方 latest specification](https://a2a-protocol.org/latest/specification/)，不要把版本号写死在教程里。

## 5. Claude Code 生态

### MCP（Model Context Protocol）

**MCP** 是 AI 应用连接外部数据和能力的开放协议。Server 可以提供 **Prompts**、**Resources** 和 **Tools**；Host／Client 决定怎样呈现、授权和传递。完整字段、transport 和安全规则以[现行规范](https://modelcontextprotocol.io/specification)为准。

📍 详情：[Stage 5.2](../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础)

### Project Instructions（项目规则）

**Project Instructions** 是工具在项目中读取的共同规则，适合放用途、禁止事项、验证命令和交付格式。不同工具的文件名和加载顺序不同，不能假设一份设置在所有 CLI 中完全相同。

📍 入门：[Track A A2](../tracks/cli/A2-cli-workflow.zh-Hans.md)

### Skills / SKILL.md

**Skill** 是需要时才加载的操作卡。按照 [Agent Skills 规范](https://agentskills.io/specification)，一个 Skill 至少是一个包含 `SKILL.md` 的目录，也可以附带 scripts、references 和 assets；安装第三方 Skill 前仍要阅读内容和权限。

### One-off Prompt（单次提示）

**One-off Prompt** 是只服务当前任务的一次性交代。每次都要遵守的规则放 Project Instructions；重复使用的流程才整理成 Skill。

### Plugin / Marketplace

**Plugin** 是把 Skills、commands、hooks 或 MCP 设置等组件打包在一起的发布单位；**Marketplace** 是查找和安装这些软件包的目录。这是产品层功能，不是所有 Agent 的通用必备组件。

### Slash Command

**Slash Command** 是以 `/` 开头、由应用程序提供的指令。它可能打开功能、设置或可复用流程；实际名称和行为要看该工具的当前文档。

### CLAUDE.md

**CLAUDE.md** 是 Claude Code 可以读取的项目指示文件之一，用来告诉 Agent 这个项目怎样工作。它是给模型遵循的 context，不是能够强制阻挡危险操作的安全边界。

### Hooks

**Hooks** 会在指定事件发生时执行固定检查或动作。它适合 lint、记录、通知或拦截高风险操作；事件和设置格式会更新，所以直接看 [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks)，不要背固定数量。

### Deep Agent（深度 agent）

**Deep Agent** 不是跨供应商的单一正式标准。LangChain 的 [deepagents](https://github.com/langchain-ai/deepagents)用这个名称描述一套包含规划、文件、子 Agent 和 context 管理的 agent harness；看到这个词时要先确认作者采用哪种定义。

### Subagent（子 agent）

**Subagent** 是主 Agent 委派出去的隔离工作者，通常有自己的 context，完成后把结果交回。Claude Code 的当前设置、继承和权限边界见[官方文档](https://code.claude.com/docs/en/sub-agents)；Subagent 不会自动正确，也要有明确任务和验证。

📍 教程：[Stage 5.5](../stages/05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能) · [可复制 recipes](./subagent-cookbook.zh-Hans.md) · [进阶组合](./subagent-advanced.zh-Hans.md)

## 6. Production / Eval / Cost

### CI（Continuous Integration，持续集成）

**CI** 在 push 或 PR 时自动运行固定检查，例如测试、lint 和安全扫描。CI 通过只代表已经设置的检查通过，不代表可以跳过 review 或直接部署。

### Eval（评估）

**Eval** 用固定输入、成功条件和记录方式比较 Prompt、模型或 Agent。先从少量代表题开始；在改动前后运行同一组，才能知道质量、成本和延迟怎样变化。

📍 入门：[Stage 2](../stages/02-prompt-engineering.zh-Hans.md)；Agent 系统：[Stage 7](../stages/07-multi-agent-production.zh-Hans.md)

### Observability

**Observability** 把 Agent 的步骤、工具、状态、时间、usage 和结果留下可查询记录。它像行车记录仪；记录时仍要遮住 secret、私人数据和不必要的 Prompt 内容。

### Prompt Caching

**Prompt Caching** 重用已经写入缓存、内容完全相同的 Prompt 前缀，减少重复处理；相似但不同的内容不会命中。最低长度、保存时间和价格因供应商而变化，实现前查看[当前缓存说明](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)并记录实际 usage。

### Streaming（流式输出）

**Streaming** 是模型生成一小段就先传一小段，不必等完整答案。界面会更快有反应，但客户端要能处理部分内容、取消、错误和尚未完成的 tool call。

### Batch API（批量 API）

**Batch API** 把不需要马上回复的多条请求一起发送。它适合离线分类、摘要或 Eval；完成时间、限制和折扣以当前供应商文档为准。

### Token Cost / Inference Cost

**Token Cost／Inference Cost** 是模型推理费用。最小公式是输入用量乘输入单价，加输出用量乘输出单价；Agent 还要把每一轮、工具服务和计算成本一起算入。

### Guardrails

**Guardrails** 是限制输入、输出和动作的规则层，例如 schema 验证、allowlist、权限和人工批准。它们能降低风险，但不能代替最小权限、隔离和测试。

### Prompt Injection（提示注入）

**Prompt Injection** 是把恶意指令藏在网页、文档或工具结果中，诱导 Agent 偏离原任务。把外部内容视为不可信数据，高风险动作使用最小权限和人工审核。

### Lethal Trifecta（致命三角）

**Lethal Trifecta** 指 Agent 同时能读取私密数据、接触不可信内容、又能对外通信时，Prompt Injection 可能把数据带出去。这个概念由 [Simon Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)整理；防护重点是切断至少一条危险路径。

## 7. 术语 / Buzzword

### CLI Agent

**CLI Agent** 是在终端中读取文件、修改文件和执行命令的 Agent／Harness。Claude Code、Codex、OpenCode、Pi、Aider 和 Gemini CLI 都属于这一类；它是工作台，不是里面的 LLM。

### BYO API Key（Bring Your Own）

**BYO API Key** 表示工具允许你提供自己的模型供应商密钥。它可能方便切换供应商，但密钥的计费、权限、保存和撤销仍由你管理。

### Local LLM / On-Device

**Local LLM／On-Device** 表示模型在你的设备或自管机器上运行。只有模型、工具、数据和记录都没有另外发送到云端时，才能说这次流程完全留在本机。

### Quantization（量化）

**Quantization** 用较低精度表示模型权重，通常能减少内存和计算需求。速度、大小和质量的变化取决于模型、格式和硬件，需要实际测试。

### Hallucination（幻觉）

**Hallucination** 是模型生成看起来合理但没有可靠依据的内容。引用、RAG、工具和 Structured Output 都只能帮忙；重要事实仍要查看来源或用 Eval 验证。

### Frontier Model

**Frontier Model** 是某个时间点能力位于前沿的模型类别，不是一个永久名单。型号、价格、Context 和可用状态变化很快；当前数据统一查看 [Stage 1 的官方来源表](../stages/01-llm-basics.zh-Hans.md)。

### Context Engineering

**Context Engineering** 是决定每次模型调用前“要放入哪些信息、按照什么顺序放、什么时候删除或压缩”的系统工作。它和 Prompt Engineering 互相配合，不是新术语淘汰旧术语；可读 [Anthropic 的实践说明](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)。

### Agent Production Engineering

**Agent Production Engineering** 是本学习地图对“让 Agent 可以长期、安全、可观察地运行”的上位名称。它把 Harness、Loop、Workflow Graph、Eval、Guardrails、成本、恢复和人工批准放在同一章讨论。

学习顺序是 [Stage 3 的 Agent Loop](../stages/03-tool-use-and-hello-agent.zh-Hans.md) → [Stage 4 的 Workflow Graph／Agent Framework](../stages/04-agent-frameworks.zh-Hans.md) → [Stage 7 的 Agent Production Engineering](../stages/07-multi-agent-production.zh-Hans.md)。Prompt、Context、Harness、Loop、Graph 是五个会重叠的控制问题，不是五个互相取代的产品世代。

📍 完整章节：[Stage 7](../stages/07-multi-agent-production.zh-Hans.md)

### Agent Harness（执行工作台）

**Agent Harness** 是包在模型外面的执行系统。它连接工具和 context，管理权限、状态、记录、错误和停止规则；同一个 Harness 可以包含 Agent Loop，也能成为 Workflow Graph 的一个 node。

### Harness Engineering

**Harness Engineering** 是设计和改进 Agent Harness 的工程工作。OpenAI 的[案例](https://openai.com/index/harness-engineering/)强调环境、知识、测试和反馈循环；它不是只把某个 framework 包在外面，也不会被 Loop Engineering 替代。

### Loop Engineering（循环工程）

**Loop Engineering** 是设计 Agent 怎样开始、反复行动、检查、保存进度、停止或找人的工程工作。IBM 把它描述为新兴实践，包含 goal、action、observation 和 adjustment；看[当前说明](https://www.ibm.com/think/topics/loop-engineering)。

**Agent Loop** 是真正运行的循环；**Loop Engineering** 是把这个循环和外围规则设计好。它可能使用 Harness、Hooks、Skills、Subagents 和 Workflow Graph，而不是替代它们。

### Graph Engineering（图工程）

**Graph Engineering** 是有人用来描述 Workflow Graph 设计的新兴名称，但不是所有供应商共同采用的标准。稳定的学习对象仍是 node、edge、branch、state 和 checkpoint；研究用法可看[当前的 survey preprint](https://arxiv.org/abs/2608.21156)。

这里的 graph 是执行流程，不是 Stage 6 的 GraphRAG 知识图谱。先在 [Stage 4](../stages/04-agent-frameworks.zh-Hans.md)学习基本 Workflow Graph，再到 [Stage 7](../stages/07-multi-agent-production.zh-Hans.md)加入上线边界。

## 8. Agent Interfaces

### Computer Use（屏幕级 agent）

**Computer Use** 让模型读取画面并提出鼠标或键盘动作。Harness 必须先检查规则，executor 才执行；能用更小、可验证的 API 或 typed tool 时，通常先用那个。

### Browser Use（web 级 agent）

**Browser Use** 让 Agent 在网页中读取数据、查找元素、填写表单或切换页面。它可以使用 DOM、Accessibility Tree 和 screenshot；[browser-use](https://github.com/browser-use/browser-use)是开源实现之一。

### Sandbox（代码隔离环境）

**Sandbox** 是限制程序能看到和能做什么的隔离环境。真正的边界要看文件、网络、进程、secret、CPU／内存和生命周期设置，不能只因为使用了容器就宣称安全。

要比较 Search／Fetch、Browser Use、Computer Use 与 Sandbox，回到 [Stage 8](../stages/08-agent-interfaces.zh-Hans.md)。

### microVM（micro Virtual Machine）

**microVM** 是启动更精简、仍使用虚拟机隔离边界的执行环境。它常用于运行不可信代码，但安全仍取决于镜像、网络、权限和宿主设置。

### Firecracker

**Firecracker** 是使用 KVM 创建 microVM 的开源 Virtual Machine Monitor。它提供隔离技术，不会自动替你完成镜像更新、网络策略或租户安全；见[官方 repository](https://github.com/firecracker-microvm/firecracker)。

### gVisor

**gVisor** 在应用程序和主机 kernel 之间加入 userspace application kernel，减少容器直接接触主机系统调用的范围。它不是完整虚拟机，支持和性能取舍看[官方文档](https://gvisor.dev/docs/)。

## 找不到的词？

- 先回到你正在阅读的 Stage；重要词第一次出现时也应该有一句白话定义。
- 看 [Stage 5.2 的 MCP](../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础)、[Stage 5.3 的 Skills](../stages/05-claude-code-ecosystem.zh-Hans.md#53--skillsclaude-code-的行为层-claude-code-生态最关键的一层)或 [Stage 7 的 production 边界](../stages/07-multi-agent-production.zh-Hans.md)。
- 仍然找不到时打开 issue；请附上“在哪一页看到”和“哪一句不懂”。

<details markdown="1">
<summary>来源和核查</summary>

上面的易变产品和协议说明只采用官方文档；研究术语链接到原始 paper。完整型号、价格和 Context 清单集中在 Stage 1，不在词典中复制。

<small>官方链接、产品身份和模型生命周期核查：2026-08-31 UTC。</small>

<!-- freshness: canonical=resources/glossary.md; verified_on=2026-08-31; scope=protocols,product-identities,terminology,official-links,model-lifecycle; max_age_days=90 -->

</details>

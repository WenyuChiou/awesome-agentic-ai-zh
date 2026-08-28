<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 2：多 agent 角色分配（CrewAI）

对应 [Stage 4 — Agent Frameworks](../../../stages/04-agent-frameworks.zh-Hans.md) 练习 2。
> 🎓 **学习模式**：这份 `starter.py` 是**完整解答**、不是 TODO skeleton。建议用**主动模式**——`mv starter.py starter_reference.py`、看 signature 不看 body、自己重写一份 `starter.py`、跑 `python test.py` 验证；卡 20 分钟再回去对照 reference。完整方法论看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 两条 SDK path，不是进阶深度教材。深度教材推荐：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章节式 + 16 种 production 能力。**本练习对应 hello-agents 的 multi-agent roles / Crew 章节**
> - [CrewAI Examples repo](https://github.com/crewAIInc/crewAI-examples)（官方 sequential / hierarchical 范本；⚠️ 已封存 2026-04、仍可当参考）
> - 完整 references 见 [Stage 4 精选 Projects](../../../stages/04-agent-frameworks.zh-Hans.md#-精选-projects)


## 任务

3 个 agent 各自负责一段、合作完成一篇 blog intro：

```
Researcher → Writer → Critic
  (找资料) (写稿) (审稿、PASS/ISSUES)
```

这是 **role-based pipeline（角色式流水线）**：你描述每个角色、目标与任务，CrewAI 依顺序传递结果。

## 怎么跑 — 两条路径

> ⚠️ **每个练习都要有自己的 Python 3.11 `.venv`。** 不要把 Stage 4 五个 `requirements.txt` 混装。

### Path A（默认、本机免费）

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
.\.venv\Scripts\python.exe starter.py
```

预算：模型 API 是 **$0**；执行时间依 CPU、记忆体、模型与 prompt 而变，请在自己的电脑量测。

### Path B（Anthropic、比较云端结果）

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py
```

预设固定型号：`anthropic/claude-haiku-4-5-20251001`。以 2,000 input + 1,000 output tokens 的单次模型请求为例：`2,000 / 1,000,000 × $1 + 1,000 / 1,000,000 × $5 = $0.007`。三个角色可能各调用一次或重试；本练习先设供应商支出上限 **$0.10**。

<details markdown="1">
<summary>macOS／Linux 指令与查核资讯</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
./.venv/bin/python test.py
```

官方来源：[CrewAI docs](https://docs.crewai.com/)｜[LiteLLM docs](https://docs.litellm.ai/)｜[Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>套件、model ID、价格与官方连结查核：2026-08-28 UTC。</small>
</details>

## 不花钱验证程序逻辑

```powershell
.\.venv\Scripts\python.exe test.py # 角色、任务、handoff 与停止条件
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic 路径行为
```

离线测试不调用真模型，但会检查 3 个 agent、3 个 task、sequential process、context dependency、handoff 与可观察的停止条件。模型质量仍要另外实测。

## CrewAI multi-agent 核心观念

### Agent

```python
researcher = Agent(
    role="Researcher",
    goal="...", # 一句话讲「成功」长什么样
    backstory="...", # 提供 persona context、影响 prompt
    tools=[search],
    llm=MODEL,
)
```

**重点**：`role` 跟 `goal` 影响 prompt 质量很大。不要写“Agent”、要写“Researcher who finds factual data”。

### Task

```python
research_task = Task(
    description="Search for X and report findings.",
    expected_output="A 1-2 sentence factual entry.",
    agent=researcher,
)
```

**重点**：`expected_output` 是给 LLM 看的“合格范本”。写成“两句、主动语态的开场”比“一些文字”更清楚；改善幅度要用自己的任务评测。

### Context dependency

```python
write_task = Task(..., context=[research_task]) # writer 看 researcher 结果
critic_task = Task(..., context=[research_task, write_task]) # critic 同时看两个
```

**重点**：`context` 是 CrewAI 的 dataflow 机制。`critic_task.context=[a, b]` 表示 critic 看到 a, b 两个 task 的 output。

### Sequential vs Hierarchical Process

```python
Crew(..., process=Process.sequential) # 线性走完
Crew(..., process=Process.hierarchical) # 多个 manager+worker、需设 manager_llm
```

这题用 sequential，因为顺序最容易看懂。Hierarchical 会由 manager 分派任务，适合需要动态分工、而且已有评测与停止条件的场景。

## 两个 path 观察重点

| 观察项 | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| Researcher 是否调用 tool | 看 log 与输出验证 | 看 log 与输出验证 |
| Writer 是否使用研究结果 | 用测试案例检查 | 用相同测试案例检查 |
| Critic 是否抓到错误 | 不预设一定成功 | 不预设一定成功 |
| 速度 | 在自己的网络与任务量测 | 在自己的硬体与模型量测 |
| 模型 API 成本 | 依 tokens 与调用次数计算 | $0 |

**教学 punchline**：multi-agent 多了交接点；任何角色漏掉资讯，错误都可能往后传。模型大小不是唯一答案，还要测角色 prompt、工具结果、handoff 与停止条件。

## 常见坑

- **`expected_output` 太笼统**：写“Some output”没有清楚成功条件。改成“A 2-sentence blog intro paragraph in active voice”，再用测试案例比较
- **`context` 漏设**：Writer 没设 `context=[research_task]`、就拿不到 researcher 结果、会凭空写
- **小 model + 3 agent**：可能比较慢或漏步。先看 log；需要时再比较 `qwen2.5:7b` 或 Claude
- **`allow_delegation=True` 慎用**：开启后 agent 可以叫其他 agent 帮忙、容易 loop。雏形阶段建议 `False`

## 想看更聪明的答案？

```powershell
$env:MODEL="anthropic/claude-sonnet-5"; .\.venv\Scripts\python.exe starter_anthropic.py
$env:MODEL="ollama/qwen2.5:7b"; .\.venv\Scripts\python.exe starter.py
```

## 延伸

- **加 manager**：`process=Process.hierarchical` + `manager_llm=...`、让 manager agent 动态分配
- **加 memory**：CrewAI 有 `memory=True`、让 agent 跨 task 记住 context
- **批次或异步执行**：`crew.kickoff_for_each(...)` 处理一批输入，`crew.kickoff_async(...)` 异步执行；两者都不是 streaming
- **加 streaming**：创建 `Crew(..., stream=True)`，再调用 `crew.kickoff()`
- **加 human-in-the-loop**：本题用练习 3 的 LangGraph 示范；CrewAI 也有自己的 human-feedback triggers

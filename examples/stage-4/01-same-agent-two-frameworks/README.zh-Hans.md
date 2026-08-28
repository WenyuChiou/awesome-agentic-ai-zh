<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 1：同一个 agent、两个 framework（LangGraph + CrewAI）

对应 [Stage 4 — Agent Frameworks](../../../stages/04-agent-frameworks.zh-Hans.md) 练习 1。
> 🎓 **学习模式**：这份 `starter.py` 是**完整解答**、不是 TODO skeleton。建议用**主动模式**——`mv starter.py starter_reference.py`、看 signature 不看 body、自己重写一份 `starter.py`、跑 `python test.py` 验证；卡 20 分钟再回去对照 reference。完整方法论看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 两条 SDK path，不是进阶深度教材。深度教材推荐：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章节式 + 16 种 production 能力。**本练习对应 hello-agents 的 framework 对照 / orchestration 章节**
> - [LangGraph Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart) + [CrewAI 官方 docs](https://docs.crewai.com/)
> - 完整 references 见 [Stage 4 精选 Projects](../../../stages/04-agent-frameworks.zh-Hans.md#-精选-projects)


## 任务

最简单的 search + summarize agent：

- 给一个 query（譬如“summarize Taipei”）
- Agent 用 `search` tool 拿 knowledge base 资料
- LLM 把 search result 摘成 1-2 句

用 **LangGraph** 跟 **CrewAI** 各做一次、比较风格差异。

## 怎么跑 — 两条路径 + 两个 framework

> ⚠️ **每个练习都要有自己的 Python 3.11 `.venv`。** 不要把五个 `requirements.txt` 混在一起安装；它们示范不同 framework，套件需求可能互相冲突。

### Path A（默认、本机免费）

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve

.\.venv\Scripts\python.exe starter.py # LangGraph + Ollama
.\.venv\Scripts\python.exe starter_crewai.py # CrewAI + Ollama（对照）
```

预算：模型 API 是 **$0**；电脑记忆体、电力与下载时间仍有成本。

### Path B（Anthropic、比较云端结果）

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py # LangGraph + Claude
```

预设固定型号：`claude-haiku-4-5-20251001`。Haiku 4.5 为每百万 input tokens **$1**、output tokens **$5**。若一次请求用 2,000 input + 1,000 output tokens，算式是 `2,000 / 1,000,000 × $1 + 1,000 / 1,000,000 × $5 = $0.007`。Framework 可能调用多次；本练习先把供应商支出上限设为 **$0.05**，不要把估算当帐单保证。

<details markdown="1">
<summary>macOS／Linux 指令与查核资讯</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
./.venv/bin/python test.py
```

官方来源：[LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)｜[CrewAI docs](https://docs.crewai.com/)｜[Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>套件、model ID、价格与官方连结查核：2026-08-28 UTC。</small>
</details>

## 不花钱验证程序逻辑（mock-based）

```powershell
.\.venv\Scripts\python.exe test.py # LangGraph 行为
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic 路径行为
.\.venv\Scripts\python.exe test_crewai.py # CrewAI 行为
```

## 两个 framework 的并排比较

| 维度 | LangGraph | CrewAI |
|---|---|---|
| 核心抽象 | `StateGraph` + node + edge | `Agent` + `Task` + `Crew` |
| 思考方式 | “状态怎么流动” | “角色怎么分工” |
| Loop 控制 | 显式 conditional edge | 隐藏在 `Crew.kickoff()` 里 |
| Debug 路径 | 看 graph state 与 checkpoint | 看 task output 与 verbose log |
| 适合场景 | 需要明确状态与分支的 workflow | 用角色与任务快速表达合作流程 |
| 学习曲线 | 中-高 | 低 |

### LangGraph 风格（精简）

```python
g = StateGraph(State)
g.add_node("agent", agent_node)
g.add_node("tools", tool_node)
g.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
g.add_edge("tools", "agent")
```

“我要显式地告诉系统：状态长这样、节点互相连这样、条件分支看 `should_continue`。”

### CrewAI 风格（精简）

```python
researcher = Agent(role="Researcher", goal="...", tools=[search], llm=MODEL)
task = Task(description=query, expected_output="...", agent=researcher)
crew = Crew(agents=[researcher], tasks=[task])
crew.kickoff()
```

“我要描述：这个角色是谁、要完成什么任务、有什么工具。框架自己决定怎么跑。”

## 观察重点

1. **抽象代价**：CrewAI 隐藏的多、写得少；要 debug 时 stack 比较深
2. **小 model 友善度**：两边都要实测；角色描述、工具 schema 与任务长度都会影响结果
3. **可控性**：LangGraph 你能看到每个 state 变化；CrewAI 偏向“结果导向”
4. **何时选哪个**：需要逐步看状态时先试 LangGraph；想先表达角色分工时先试 CrewAI，再用自己的任务测量

## 常见坑

- **LangGraph `bind_tools`**：要 `llm.bind_tools([search])` 才会把 tool schema 给 LLM。没 bind 模型就不知道 tool 存在
- **CrewAI LLM 设定**：要用 LiteLLM 格式（譬如 `"ollama/qwen2.5:3b"`、不是 `"qwen2.5:3b"`）。写错 provider 前缀可能连到不同后端，所以执行前要打印设定并确认
- **CrewAI 结果型别**：`crew.kickoff()` 回 `CrewOutput` 对象、`str(result)` 拿文字。直接 `print(result)` 有可能拿到 repr

## 想看更聪明的答案？

```powershell
$env:MODEL="claude-sonnet-5"; .\.venv\Scripts\python.exe starter_anthropic.py
$env:MODEL="qwen2.5:7b"; .\.venv\Scripts\python.exe starter.py
```

## 延伸

- **改成 streaming**：LangGraph 用 `graph.stream(...)` 边跑边看 state；CrewAI 在创建 `Crew(..., stream=True)` 时开启，再调用 `crew.kickoff()`
- **加 checkpointing**：LangGraph 加 `MemorySaver` 就能 time-travel debug
- **加 human-in-the-loop**：练习 3 会做

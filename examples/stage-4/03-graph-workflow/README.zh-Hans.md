<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 3：图式 workflow（LangGraph 条件分支 + HITL）

对应 [Stage 4 — Workflow Graph 与 Agent 框架](../../../stages/04-agent-frameworks.zh-Hans.md) 练习 3。
> 🎓 **学习模式**：先运行提供的 `starter.py`（`python starter.py`），然后只改一个小地方，再重新运行现有测试 `python test.py`。如果测试失败，就撤销或修正这一个改动，再试一次。不需要重命名文件，也不需要重写整份解答。完整方法见 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 两条 SDK path，不是进阶深度教材。深度教材推荐：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章节式 + 16 种 production 能力。**本练习对应 hello-agents 的 graph workflow + HITL 章节**
> - [LangGraph interrupts (human-in-the-loop)](https://docs.langchain.com/oss/python/langgraph/interrupts) + [LangGraph time-travel docs](https://docs.langchain.com/oss/python/langgraph/use-time-travel)
> - 完整 references 见 [Stage 4 精选 Projects](../../../stages/04-agent-frameworks.zh-Hans.md#-精选-projects)


## 任务

`classify → [search?] → respond → [HITL] → final`

- **`classify_node`**：看 query 决定 `needs_search`
- **条件分支**：`needs_search=True` 走 `search` node、否则直接 `respond`
- **HITL checkpoint**：`review_node` 用 `interrupt()` 暂停，等待人类回答
- **`final_node`**：`approved=True` → PUBLISHED、否则 REJECTED

这题用 LangGraph 示范 **graph state（图状态）**、**checkpoint（检查点）**、`interrupt()` 与 `Command(resume=...)`。你可以看见流程停在哪里，以及它如何从同一个 `thread_id` 继续。

## 怎么跑 — 两条路径

> ⚠️ **每个练习都要有自己的 Python 3.11 `.venv`。** 不要把 Stage 4 五个 `requirements.txt` 混装。

### Path A（Ollama、本机）

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
.\.venv\Scripts\python.exe starter.py
```

预算：模型 API 是 **$0**；本机硬体、电力与下载仍有成本。这份 starter 会真的请 Ollama 写草稿，其他节点则使用可预测的 Python 逻辑。

### Path B（Anthropic、比较云端结果）

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py
```

预设固定型号：`claude-haiku-4-5-20251001`。若一次请求用 2,000 input + 1,000 output tokens：`2,000 / 1,000,000 × $1 + 1,000 / 1,000,000 × $5 = $0.007`。本练习通常只需要短草稿，但仍可能重试；先设供应商支出上限 **$0.05**。

<details markdown="1">
<summary>macOS／Linux 指令与查核资讯</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
./.venv/bin/python test.py
```

官方来源：[LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)｜[LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)｜[Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>套件、model ID、价格与官方连结查核：2026-08-28 UTC。</small>
</details>

## 不花钱验证程序逻辑

```powershell
.\.venv\Scripts\python.exe test.py # 真正走分支、interrupt 与 resume
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic 设定 + 共用图行为
```

## LangGraph 图结构（精简）

```python
g = StateGraph(State)
g.add_node("classify", classify_node)
g.add_node("search", search_node)
g.add_node("respond", respond_node)
g.add_node("final", final_node)

g.add_edge(START, "classify")
g.add_conditional_edges("classify", should_search, {"search": "search", "respond": "respond"})
g.add_edge("search", "respond")
g.add_edge("respond", "review")
g.add_edge("review", "final")
g.add_edge("final", END)

graph = g.compile(checkpointer=InMemorySaver())
```

## HITL 怎么运作

```python
# 第一段：review_node 呼叫 interrupt()，图就把资料存进 checkpoint 并停下来
config = {"configurable": {"thread_id": "demo"}}
state_before = graph.invoke({"query": ...}, config=config)
# state_before["__interrupt__"] 会带出草稿与问题

# 第二段：人类回答后，用同一个 thread_id 恢复
state_after = graph.invoke(Command(resume=True), config=config)
```

**关键**：`interrupt()` 是“先停一下”；`Command(resume=True/False)` 是“带著人的回答继续”。Production 可以把这个等待点接到 webhook、Slack 或前端按钮。

## 为什么这个 pattern 重要

| 情境 | 不用 HITL | 用 HITL |
|---|---|---|
| Agent 发 email | 直接送出（风险） | 显示草稿、人类按 approve |
| Agent 改 production 设定 | 直接套用 | dry-run 后等核准 |
| Agent 做退款 | 自动退 | 超过 $X 等审核 |

有 **side effect（会改变外部世界的动作）** 时，先判断风险；寄信、退款或改 production 设定通常需要 HITL、权限检查与 audit log。低风险唯读动作不一定要每次人工核准。

## 两个 path 观察重点

两个 path 共用同一张图；`classify`、离线查询与路由是可预测的 Python，`respond` 则真的调用不同模型写草稿。**比较时只换模型，不要同时改 graph。**

Node 里只负责暂停，拿到人的答案后再更新 state：

```python
from langgraph.types import interrupt

def review_node(state):
    approved = interrupt({"draft": state["draft"], "question": "Approve?"})
    return {"approved": approved}
```

外面的 caller 收到真人答案后，才从同一个 `thread_id` 继续：

```python
from langgraph.types import Command

human_answer = True
result = graph.invoke(Command(resume=human_answer), config=config)
```

## 常见坑

- **`checkpointer` 没设**：没有 checkpointer 就无法可靠地保存 pause/resume 状态
- **`thread_id` 不一致**：第一段 `invoke` 与 `Command(resume=...)` 必须用同一个设定，否则找不到原来的 checkpoint
- **在 `interrupt()` 前做 side effect**：恢复时节点可能重新执行。把寄信或扣款放在核准后，并加入 idempotency key
- **conditional_edges 函数要回 string**：`should_search` return value 必须是 `add_conditional_edges` 第三个参数 dict 的 key、不能 return literal value 直接当 node name

## 想看更聪明的答案？

比较另一个模型，或把记忆体 checkpointer 换成适合部署环境的持久化储存。先确认官方 persistence 文件与失败恢复行为，再选资料库。

## 延伸

- **加 retry**：在 `search_node` 失败时 retry、用 LangGraph 的 `error` edge
- **加多个 HITL**：在不同 review node 调用 `interrupt()`，并替每个核准动作定义清楚资料
- **time-travel debug**：`graph.get_state_history(config)` 拿到所有 checkpoint、可以回到任一步 fork 新 thread
- **加 streaming**：`for state in graph.stream(...)` 边跑边看 state

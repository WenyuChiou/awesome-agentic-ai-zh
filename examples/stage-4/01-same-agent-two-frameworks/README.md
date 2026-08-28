<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 1：同一個 agent、兩個 framework（LangGraph + CrewAI）

對應 [Stage 4 — Agent Frameworks](../../../stages/04-agent-frameworks.md) 練習 1。
> 🎓 **學習模式**：這份 `starter.py` 是**完整解答**、不是 TODO skeleton。建議用**主動模式**——`mv starter.py starter_reference.py`、看 signature 不看 body、自己重寫一份 `starter.py`、跑 `python test.py` 驗證；卡 20 分鐘再回去對照 reference。完整方法論看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 兩條 SDK path，不是進階深度教材。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 framework 對照 / orchestration 章節**
> - [LangGraph Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart) + [CrewAI 官方 docs](https://docs.crewai.com/)
> - 完整 references 見 [Stage 4 精選 Projects](../../../stages/04-agent-frameworks.md#-精選-projects)


## 任務

最簡單的 search + summarize agent：

- 給一個 query（譬如「summarize Taipei」）
- Agent 用 `search` tool 拿 knowledge base 資料
- LLM 把 search result 摘成 1-2 句

用 **LangGraph** 跟 **CrewAI** 各做一次、比較風格差異。

## 怎麼跑 — 兩條路徑 + 兩個 framework

> ⚠️ **每個練習都要有自己的 Python 3.11 `.venv`。** 不要把五個 `requirements.txt` 混在一起安裝；它們示範不同 framework，套件需求可能互相衝突。

### Path A（默認、本機免費）

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve

.\.venv\Scripts\python.exe starter.py # LangGraph + Ollama
.\.venv\Scripts\python.exe starter_crewai.py # CrewAI + Ollama（對照）
```

預算：模型 API 是 **$0**；電腦記憶體、電力與下載時間仍有成本。

### Path B（Anthropic、比較雲端結果）

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py # LangGraph + Claude
```

預設固定型號：`claude-haiku-4-5-20251001`。Haiku 4.5 為每百萬 input tokens **$1**、output tokens **$5**。若一次請求用 2,000 input + 1,000 output tokens，算式是 `2,000 / 1,000,000 × $1 + 1,000 / 1,000,000 × $5 = $0.007`。Framework 可能呼叫多次；本練習先把供應商支出上限設為 **$0.05**，不要把估算當帳單保證。

<details markdown="1">
<summary>macOS／Linux 指令與查核資訊</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
./.venv/bin/python test.py
```

官方來源：[LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)｜[CrewAI docs](https://docs.crewai.com/)｜[Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>套件、model ID、價格與官方連結查核：2026-08-28 UTC。</small>
</details>

## 不花錢驗證程式邏輯（mock-based）

```powershell
.\.venv\Scripts\python.exe test.py # LangGraph 行為
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic 路徑行為
.\.venv\Scripts\python.exe test_crewai.py # CrewAI 行為
```

## 兩個 framework 的並排比較

| 維度 | LangGraph | CrewAI |
|---|---|---|
| 核心抽象 | `StateGraph` + node + edge | `Agent` + `Task` + `Crew` |
| 思考方式 | 「狀態怎麼流動」 | 「角色怎麼分工」 |
| Loop 控制 | 顯式 conditional edge | 隱藏在 `Crew.kickoff()` 裡 |
| Debug 路徑 | 看 graph state 與 checkpoint | 看 task output 與 verbose log |
| 適合場景 | 需要明確狀態與分支的 workflow | 用角色與任務快速表達合作流程 |
| 學習曲線 | 中-高 | 低 |

### LangGraph 風格（精簡）

```python
g = StateGraph(State)
g.add_node("agent", agent_node)
g.add_node("tools", tool_node)
g.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
g.add_edge("tools", "agent")
```

「我要顯式地告訴系統：狀態長這樣、節點互相連這樣、條件分支看 `should_continue`。」

### CrewAI 風格（精簡）

```python
researcher = Agent(role="Researcher", goal="...", tools=[search], llm=MODEL)
task = Task(description=query, expected_output="...", agent=researcher)
crew = Crew(agents=[researcher], tasks=[task])
crew.kickoff()
```

「我要描述：這個角色是誰、要完成什麼任務、有什麼工具。框架自己決定怎麼跑。」

## 觀察重點

1. **抽象代價**：CrewAI 隱藏的多、寫得少；要 debug 時 stack 比較深
2. **小 model 友善度**：兩邊都要實測；角色描述、工具 schema 與任務長度都會影響結果
3. **可控性**：LangGraph 你能看到每個 state 變化；CrewAI 偏向「結果導向」
4. **何時選哪個**：需要逐步看狀態時先試 LangGraph；想先表達角色分工時先試 CrewAI，再用自己的任務測量

## 常見坑

- **LangGraph `bind_tools`**：要 `llm.bind_tools([search])` 才會把 tool schema 給 LLM。沒 bind 模型就不知道 tool 存在
- **CrewAI LLM 設定**：要用 LiteLLM 格式（譬如 `"ollama/qwen2.5:3b"`、不是 `"qwen2.5:3b"`）。寫錯 provider 前綴可能連到不同後端，所以執行前要印出設定並確認
- **CrewAI 結果型別**：`crew.kickoff()` 回 `CrewOutput` 物件、`str(result)` 拿文字。直接 `print(result)` 有可能拿到 repr

## 想看更聰明的答案？

```powershell
$env:MODEL="claude-sonnet-5"; .\.venv\Scripts\python.exe starter_anthropic.py
$env:MODEL="qwen2.5:7b"; .\.venv\Scripts\python.exe starter.py
```

## 延伸

- **改成 streaming**：LangGraph 用 `graph.stream(...)` 邊跑邊看 state；CrewAI 在建立 `Crew(..., stream=True)` 時開啟，再呼叫 `crew.kickoff()`
- **加 checkpointing**：LangGraph 加 `MemorySaver` 就能 time-travel debug
- **加 human-in-the-loop**：練習 3 會做

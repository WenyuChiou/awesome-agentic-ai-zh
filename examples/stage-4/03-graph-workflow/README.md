<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 3：圖式 workflow（LangGraph 條件分支 + HITL）

對應 [Stage 4 — Workflow Graph 與 Agent 框架](../../../stages/04-agent-frameworks.md) 練習 3。
> 🎓 **學習模式**：先執行提供的 `starter.py`（`python starter.py`），再只改一個小地方，然後重新執行既有測試 `python test.py`。如果測試失敗，就撤銷或修正這一個改動，再試一次。不需要改名檔案，也不需要整份解答重寫。完整方法看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 兩條 SDK path，不是進階深度教材。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 graph workflow + HITL 章節**
> - [LangGraph interrupts (human-in-the-loop)](https://docs.langchain.com/oss/python/langgraph/interrupts) + [LangGraph time-travel docs](https://docs.langchain.com/oss/python/langgraph/use-time-travel)
> - 完整 references 見 [Stage 4 精選 Projects](../../../stages/04-agent-frameworks.md#-精選-projects)


## 任務

`classify → [search?] → respond → [HITL] → final`

- **`classify_node`**：看 query 決定 `needs_search`
- **條件分支**：`needs_search=True` 走 `search` node、否則直接 `respond`
- **HITL checkpoint**：`review_node` 用 `interrupt()` 暫停，等待人類回答
- **`final_node`**：`approved=True` → PUBLISHED、否則 REJECTED

這題用 LangGraph 示範 **graph state（圖狀態）**、**checkpoint（檢查點）**、`interrupt()` 與 `Command(resume=...)`。你可以看見流程停在哪裡，以及它如何從同一個 `thread_id` 繼續。

## 怎麼跑 — 兩條路徑

> ⚠️ **每個練習都要有自己的 Python 3.11 `.venv`。** 不要把 Stage 4 五個 `requirements.txt` 混裝。

### Path A（Ollama、本機）

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
.\.venv\Scripts\python.exe starter.py
```

預算：模型 API 是 **$0**；本機硬體、電力與下載仍有成本。這份 starter 會真的請 Ollama 寫草稿，其他節點則使用可預測的 Python 邏輯。

### Path B（Anthropic、比較雲端結果）

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py
```

預設固定型號：`claude-haiku-4-5-20251001`。若一次請求用 2,000 input + 1,000 output tokens：`2,000 / 1,000,000 × $1 + 1,000 / 1,000,000 × $5 = $0.007`。本練習通常只需要短草稿，但仍可能重試；先設供應商支出上限 **$0.05**。

<details markdown="1">
<summary>macOS／Linux 指令與查核資訊</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
./.venv/bin/python test.py
```

官方來源：[LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)｜[LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)｜[Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>套件、model ID、價格與官方連結查核：2026-08-28 UTC。</small>
</details>

## 不花錢驗證程式邏輯

```powershell
.\.venv\Scripts\python.exe test.py # 真正走分支、interrupt 與 resume
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic 設定 + 共用圖行為
```

## LangGraph 圖結構（精簡）

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

## HITL 怎麼運作

```python
# 第一段：review_node 呼叫 interrupt()，圖就把資料存進 checkpoint 並停下來
config = {"configurable": {"thread_id": "demo"}}
state_before = graph.invoke({"query": ...}, config=config)
# state_before["__interrupt__"] 會帶出草稿與問題

# 第二段：人類回答後，用同一個 thread_id 恢復
state_after = graph.invoke(Command(resume=True), config=config)
```

**關鍵**：`interrupt()` 是「先停一下」；`Command(resume=True/False)` 是「帶著人的回答繼續」。Production 可以把這個等待點接到 webhook、Slack 或前端按鈕。

## 為什麼這個 pattern 重要

| 情境 | 不用 HITL | 用 HITL |
|---|---|---|
| Agent 發 email | 直接送出（風險） | 顯示草稿、人類按 approve |
| Agent 改 production 設定 | 直接套用 | dry-run 後等核准 |
| Agent 做退款 | 自動退 | 超過 $X 等審核 |

有 **side effect（會改變外部世界的動作）** 時，先判斷風險；寄信、退款或改 production 設定通常需要 HITL、權限檢查與 audit log。低風險唯讀動作不一定要每次人工核准。

## 兩個 path 觀察重點

兩個 path 共用同一張圖；`classify`、離線查詢與路由是可預測的 Python，`respond` 則真的呼叫不同模型寫草稿。**比較時只換模型，不要同時改 graph。**

Node 裡只負責暫停，拿到人的答案後再更新 state：

```python
from langgraph.types import interrupt

def review_node(state):
    approved = interrupt({"draft": state["draft"], "question": "Approve?"})
    return {"approved": approved}
```

外面的 caller 收到真人答案後，才從同一個 `thread_id` 繼續：

```python
from langgraph.types import Command

human_answer = True
result = graph.invoke(Command(resume=human_answer), config=config)
```

## 常見坑

- **`checkpointer` 沒設**：沒有 checkpointer 就無法可靠地保存 pause/resume 狀態
- **`thread_id` 不一致**：第一段 `invoke` 與 `Command(resume=...)` 必須用同一個設定，否則找不到原來的 checkpoint
- **在 `interrupt()` 前做 side effect**：恢復時節點可能重新執行。把寄信或扣款放在核准後，並加入 idempotency key
- **conditional_edges 函數要回 string**：`should_search` return value 必須是 `add_conditional_edges` 第三個參數 dict 的 key、不能 return literal value 直接當 node name

## 想看更聰明的答案？

比較另一個模型，或把記憶體 checkpointer 換成適合部署環境的持久化儲存。先確認官方 persistence 文件與失敗恢復行為，再選資料庫。

## 延伸

- **加 retry**：在 `search_node` 失敗時 retry、用 LangGraph 的 `error` edge
- **加多個 HITL**：在不同 review node 呼叫 `interrupt()`，並替每個核准動作定義清楚資料
- **time-travel debug**：`graph.get_state_history(config)` 拿到所有 checkpoint、可以回到任一步 fork 新 thread
- **加 streaming**：`for state in graph.stream(...)` 邊跑邊看 state

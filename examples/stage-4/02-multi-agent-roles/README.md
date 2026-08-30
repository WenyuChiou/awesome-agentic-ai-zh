<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 2：多 agent 角色分配（CrewAI）

對應 [Stage 4 — Workflow Graph 與 Agent 框架](../../../stages/04-agent-frameworks.md) 練習 2。
> 🎓 **學習模式**：先執行提供的 `starter.py`（`python starter.py`），再只改一個小地方，然後重新執行既有測試 `python test.py`。如果測試失敗，就撤銷或修正這一個改動，再試一次。不需要改名檔案，也不需要整份解答重寫。完整方法看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 兩條 SDK path，不是進階深度教材。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 multi-agent roles / Crew 章節**
> - [CrewAI Examples repo](https://github.com/crewAIInc/crewAI-examples)（官方 sequential / hierarchical 範本；⚠️ 已封存 2026-04、仍可當參考）
> - 完整 references 見 [Stage 4 精選 Projects](../../../stages/04-agent-frameworks.md#-精選-projects)


## 任務

3 個 agent 各自負責一段、合作完成一篇 blog intro：

```
Researcher → Writer → Critic
  (找資料) (寫稿) (審稿、PASS/ISSUES)
```

這是 **role-based pipeline（角色式流水線）**：你描述每個角色、目標與任務，CrewAI 依順序傳遞結果。

## 怎麼跑 — 兩條路徑

> ⚠️ **每個練習都要有自己的 Python 3.11 `.venv`。** 不要把 Stage 4 五個 `requirements.txt` 混裝。

### Path A（默認、本機免費）

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
.\.venv\Scripts\python.exe starter.py
```

預算：模型 API 是 **$0**；執行時間依 CPU、記憶體、模型與 prompt 而變，請在自己的電腦量測。

### Path B（Anthropic、比較雲端結果）

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py
```

預設固定型號：`anthropic/claude-haiku-4-5-20251001`。以 2,000 input + 1,000 output tokens 的單次模型請求為例：`2,000 / 1,000,000 × $1 + 1,000 / 1,000,000 × $5 = $0.007`。三個角色可能各呼叫一次或重試；本練習先設供應商支出上限 **$0.10**。

<details markdown="1">
<summary>macOS／Linux 指令與查核資訊</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
./.venv/bin/python test.py
```

官方來源：[CrewAI docs](https://docs.crewai.com/)｜[LiteLLM docs](https://docs.litellm.ai/)｜[Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>套件、model ID、價格與官方連結查核：2026-08-28 UTC。</small>
</details>

## 不花錢驗證程式邏輯

```powershell
.\.venv\Scripts\python.exe test.py # 角色、任務、handoff 與停止條件
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic 路徑行為
```

離線測試不呼叫真模型，但會檢查 3 個 agent、3 個 task、sequential process、context dependency、handoff 與可觀察的停止條件。模型品質仍要另外實測。

## CrewAI multi-agent 核心觀念

### Agent

```python
researcher = Agent(
    role="Researcher",
    goal="...", # 一句話講「成功」長什麼樣
    backstory="...", # 提供 persona context、影響 prompt
    tools=[search],
    llm=MODEL,
)
```

**重點**：`role` 跟 `goal` 影響 prompt 質量很大。不要寫「Agent」、要寫「Researcher who finds factual data」。

### Task

```python
research_task = Task(
    description="Search for X and report findings.",
    expected_output="A 1-2 sentence factual entry.",
    agent=researcher,
)
```

**重點**：`expected_output` 是給 LLM 看的「合格範本」。寫成「兩句、主動語態的開場」比「一些文字」更清楚；改善幅度要用自己的任務評測。

### Context dependency

```python
write_task = Task(..., context=[research_task]) # writer 看 researcher 結果
critic_task = Task(..., context=[research_task, write_task]) # critic 同時看兩個
```

**重點**：`context` 是 CrewAI 的 dataflow 機制。`critic_task.context=[a, b]` 表示 critic 看到 a, b 兩個 task 的 output。

### Sequential vs Hierarchical Process

```python
Crew(..., process=Process.sequential) # 線性走完
Crew(..., process=Process.hierarchical) # 多個 manager+worker、需設 manager_llm
```

這題用 sequential，因為順序最容易看懂。Hierarchical 會由 manager 分派任務，適合需要動態分工、而且已有評測與停止條件的場景。

## 兩個 path 觀察重點

| 觀察項 | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| Researcher 是否呼叫 tool | 看 log 與輸出驗證 | 看 log 與輸出驗證 |
| Writer 是否使用研究結果 | 用測試案例檢查 | 用相同測試案例檢查 |
| Critic 是否抓到錯誤 | 不預設一定成功 | 不預設一定成功 |
| 速度 | 在自己的網路與任務量測 | 在自己的硬體與模型量測 |
| 模型 API 成本 | 依 tokens 與呼叫次數計算 | $0 |

**教學 punchline**：multi-agent 多了交接點；任何角色漏掉資訊，錯誤都可能往後傳。模型大小不是唯一答案，還要測角色 prompt、工具結果、handoff 與停止條件。

## 常見坑

- **`expected_output` 太籠統**：寫「Some output」沒有清楚成功條件。改成「A 2-sentence blog intro paragraph in active voice」，再用測試案例比較
- **`context` 漏設**：Writer 沒設 `context=[research_task]`、就拿不到 researcher 結果、會憑空寫
- **小 model + 3 agent**：可能比較慢或漏步。先看 log；需要時再比較 `qwen2.5:7b` 或 Claude
- **`allow_delegation=True` 慎用**：開啟後 agent 可以叫其他 agent 幫忙、容易 loop。雛形階段建議 `False`

## 想看更聰明的答案？

```powershell
$env:MODEL="anthropic/claude-sonnet-5"; .\.venv\Scripts\python.exe starter_anthropic.py
$env:MODEL="ollama/qwen2.5:7b"; .\.venv\Scripts\python.exe starter.py
```

## 延伸

- **加 manager**：`process=Process.hierarchical` + `manager_llm=...`、讓 manager agent 動態分配
- **加 memory**：CrewAI 有 `memory=True`、讓 agent 跨 task 記住 context
- **批次或非同步**：`crew.kickoff_for_each(...)` 是一批輸入，`crew.kickoff_async(...)` 是非同步執行；兩者都不是 streaming
- **加 streaming**：建立 `Crew(..., stream=True)`，再呼叫 `crew.kickoff()`
- **加 human-in-the-loop**：本題用練習 3 的 LangGraph 做示範；CrewAI 也有自己的 human-feedback triggers

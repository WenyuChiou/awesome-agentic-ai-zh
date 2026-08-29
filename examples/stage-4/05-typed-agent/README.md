<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 5：型別安全 agent（Pydantic AI structured output）

對應 [Stage 4 — Agent Frameworks](../../../stages/04-agent-frameworks.md) 練習 5。
> 🎓 **學習模式**：這份 `starter.py` 是**完整解答**、不是 TODO skeleton。建議用**主動模式**——`mv starter.py starter_reference.py`、看 signature 不看 body、自己重寫一份 `starter.py`、跑 `python test.py` 驗證；卡 20 分鐘再回去對照 reference。完整方法論看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 兩條 SDK path，不是進階深度教材。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 structured output / type-safe 章節**
> - [Pydantic AI 官方 docs](https://ai.pydantic.dev/) + [Instructor library](https://github.com/567-labs/instructor)（另一條 typed-output 路線）
> - 完整 references 見 [Stage 4 精選 Projects](../../../stages/04-agent-frameworks.md#-精選-projects)


## 任務

Agent 回問題、**強制** return `AnswerWithConfidence`：

```python
class AnswerWithConfidence(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0) # runtime 驗證 0-1
    sources: list[str]
```

Pydantic AI 把 **schema validation（格式規則檢查）** 放進程式：LLM 不照 schema 時，framework 可以拒絕或重試。它能檢查形狀，**不能證明答案內容是真的**。

## 怎麼跑 — 兩條路徑

> ⚠️ **每個練習都要有自己的 Python 3.11 `.venv`。** 不要把這題的 Pydantic 需求與 CrewAI 練習混裝。

### Path A（默認、本機免費）

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
.\.venv\Scripts\python.exe starter.py
```

預算：模型 API 是 **$0**；本機硬體、電力與重試時間仍有成本。

### Path B（Anthropic、比較雲端結果）

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py
```

預設固定型號：`claude-haiku-4-5-20251001`。若一次請求用 2,000 input + 1,000 output tokens：`2,000 / 1,000,000 × $1 + 1,000 / 1,000,000 × $5 = $0.007`。驗證失敗可能重試；先設供應商支出上限 **$0.05**。

<details markdown="1">
<summary>macOS／Linux 指令與查核資訊</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
./.venv/bin/python test.py
```

官方來源：[Pydantic AI output](https://ai.pydantic.dev/output/)｜[Pydantic AI testing](https://ai.pydantic.dev/testing/)｜[Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>套件、model ID、價格與官方連結查核：2026-08-28 UTC。</small>
</details>

## 不花錢驗證程式邏輯

```powershell
.\.venv\Scripts\python.exe test.py # 官方 TestModel + schema 邊界
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic 設定 + 相同輸出契約
```

`test.py` 直接驗 `AnswerWithConfidence` 對非法資料（confidence > 1.0、type 不對、sources 不是 list）的 ValidationError——不需要打 LLM、純 type 層測試。

## 為什麼 type-safe agent 重要

```
Stage 3 練習 6：schema = JSON Schema in prompt
    LLM 看到、但回什麼是 LLM 決定（可能違反）

Stage 4 練習 5：schema = Pydantic model in code
    LLM 違反 → framework 自動 raise → retry / 修
    成功回傳的 output 已通過 runtime 格式檢查
    內容是否正確仍要另外驗證
```

對 production：

| 需求 | 純 prompt schema | Pydantic AI |
|---|---|---|
| LLM 偶爾少欄位 | 你的下游 code 要 try/except | 自動 retry 直到符合 |
| 型別錯（confidence="high"） | 下游 crash | Pydantic ValidationError、retry |
| 邊界錯（confidence=1.5） | 下游用錯誤值 | 拒絕、retry |
| 多餘欄位 | 依你的 parser 而定 | 依 Pydantic model 設定處理 |

**結論**：下游程式需要固定欄位時，typed output 很有用。Stage 3 練習 6 教 schema 設計；這題把 schema 變成 runtime contract，再提醒你補上事實查核。

## Pydantic AI 核心觀念

### Agent + output_type

```python
agent = Agent(
    model=...,
    output_type=AnswerWithConfidence, # ← 強制 LLM 回這個 shape
    system_prompt="..."
)
result = agent.run_sync(question)
answer: AnswerWithConfidence = result.output # 已驗證的物件
```

**重點**：framework 把 Pydantic schema 轉成 structured output 指示，執行 validation，失敗時依設定重試。重試成功只表示格式合格。

### Field constraints

```python
confidence: float = Field(ge=0.0, le=1.0, description="...")
```

`ge` / `le` 是 Pydantic 的 numeric bound。LLM 回 `1.5` 會被 ValidationError 擋下、retry。

### 自動 retry

```python
Agent(..., retries=3) # default 1，可調
```

Pydantic AI 看到 ValidationError、會把錯誤訊息塞回 prompt、要求 LLM 重產。

## 兩個 path 觀察重點

| 觀察項 | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| 一次產對 schema | 用相同題組量測 | 用相同題組量測 |
| retry 次數 | 記錄實際結果 | 記錄實際結果 |
| confidence 邊界 | 由 Pydantic 驗證 | 由 Pydantic 驗證 |
| sources 是 list | 由 Pydantic 驗證 | 由 Pydantic 驗證 |
| 成本 | 依 tokens 與重試次數 | 模型 API $0 |

**教學重點**：比較模型時要一起記錄成功率、重試次數、延遲與費用；不要只看單次 token 價格，也不要先假設大模型一定比較省。

## 常見坑

- **`output_type` 太複雜**：nested model 越深越難產生與維護。先用最少必要欄位，再用評測決定是否拆分
- **缺 `description`**：`Field(...)` 沒寫 `description=`、LLM 看不到欄位用途、易誤填
- **`retries=0`**：失敗就 raise。重試次數要依費用、延遲與失敗模式設定，並保留上限
- **小 model + 深 nested**：qwen2.5:3b 可能 retry 多次仍不對。換大 model 或扁平 schema

## 想看更聰明的答案？

```powershell
$env:MODEL="claude-sonnet-5"; .\.venv\Scripts\python.exe starter_anthropic.py
$env:MODEL="qwen2.5:7b"; .\.venv\Scripts\python.exe starter.py
```

## 延伸

- **加 tools**：Pydantic AI agent 可以同時有 tools + structured output、`@agent.tool` 裝飾函式
- **stream typed output**：`agent.run_stream(...)` 邊跑邊驗
- **跨 model 比較**：同一個 schema 跑 Claude / GPT / Gemini / 本機 model，比較通過率、重試與成本
- **接 production**：Pydantic AI 跟 FastAPI 整合很好、output 直接當 API response model

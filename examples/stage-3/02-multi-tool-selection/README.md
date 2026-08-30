<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 2：多工具選擇

對應 [Stage 3 — 工具使用與第一個 Agent Loop](../../../stages/03-tool-use-and-hello-agent.md) 練習 2。
> 🎓 **學習模式**：先執行提供的 `starter.py`（`python starter.py`），再只改一個小地方，然後重新執行既有測試 `python test.py`。如果測試失敗，就撤銷或修正這一個改動，再試一次。不需要改名檔案，也不需要整份解答重寫。完整方法看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 70-150 行 illustrative 版、聚焦 `核心 pattern + 兩條 SDK path`，不是進階深度教材。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 tool-calling / multi-tool dispatch 章節**
> - [Anthropic Tool Use Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/tool_use)（單工具→多工具→parallel 完整 notebook）
> - 完整 references 見 [Stage 3 精選 Projects](../../../stages/03-tool-use-and-hello-agent.md#-精選-projects)


## 為什麼這題重要

這個練習讓 LLM 在同一輪面對三個工具：`web_search`、`calculator`、`calendar_lookup`。重點不是工具本身強不強，而是觀察 schema 的 `name` / `description` / `parameters` 如何決定模型挑哪一個。寫清楚 schema、是 Stage 3 最值得花時間的子題。

## 怎麼跑 — 兩條路徑

### Path A（默認、本機免費）

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

預算：**$0 API 費用**；不包含硬體、記憶體與電力成本。

### Path B（Anthropic、雲端比較）

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "your-key"
python starter_anthropic.py
```

預算：每次先保留 **$0.05**。實際費用依 `輸入 tokens × $1 / 1,000,000 + 輸出 tokens × $5 / 1,000,000` 計算，Tool Use 還會加入 prompt tokens；價格查核日：`2026-08-27`。

預期看到（Path A、本機）：

```
❓ 問題：What is (19 * 42) - 8? Use the best available tool.（using Ollama qwen2.5:3b）
   tool: calculator
   tool_input: {'expression': '(19 * 42) - 8'}
   observation: 790
✅ 練習 2 通過 — 你已用本機 qwen2.5:3b 跑通 multi-tool selection、$0/run
```

## 不花錢驗證程式邏輯（mock-based）

```powershell
python test.py # 驗 Path A (Ollama) starter.py 邏輯
python test_anthropic.py # 驗 Path B (Anthropic) starter_anthropic.py 邏輯
```

兩條 test 都用 `unittest.mock`、不打真 API、$0/run。Path A 用 OpenAI-compat response shape、Path B 用 Anthropic content blocks。

## 兩條 path 的 SDK 差異

三個關鍵差異（其他完全一樣）：

| 部分 | Anthropic（Path B） | OpenAI-compat / Ollama（Path A） |
|---|---|---|
| Schema 包法 | `tools=[{name, description, input_schema}, ...]` | `tools=[{"type": "function", "function": {name, description, parameters}}, ...]` |
| 抓 tool call | `resp.content[i].type == "tool_use"` | `resp.choices[0].message.tool_calls[i]` |
| input 格式 | `call.input` 是 dict（自動 parse） | `call.function.arguments` 是 JSON string、要 `json.loads(...)` |

Tool selection **邏輯本身**跨 backend，但實際行為會隨模型與題目變化。固定 prompt、schema 和測試題，用 eval 記錄成功率與失敗類型。

## 容易踩坑

多工具選擇最常見的錯誤是 description 寫得太像「一般說明文件」，而不是「給模型做決策的判斷規則」：

- `calendar_lookup` 描述只說「行事曆」就會跟 `web_search` 邊界模糊；明寫「查特定日期事件」才好
- `web_search` 適合「外部 / 近期 / 不確定資訊」、`calculator` 只處理算式；邊界寫越清楚、模型越少誤判
- 不同模型對 description 質量的反應可能不同；不要預設哪一個一定較穩，用同一組固定 eval 實測

## 想看更聰明的答案？

預設用固定 ID `claude-haiku-4-5-20251001`。想比較 sonnet 時：

```powershell
$env:MODEL = "claude-sonnet-5"; python starter_anthropic.py
```

或在 Ollama path 換 `qwen2.5:7b`；行為和成本要用固定 eval 實測：

```powershell
$env:MODEL = "qwen2.5:7b"; python starter.py
```

## 延伸

- **加更多 tool**：在 `TOOLS_SPEC` + `TOOL_IMPL` 補一個 entry 即可
- **改成多輪 ReAct**：把單輪 call 包進 while loop，看 [`../03-react-from-scratch/`](../03-react-from-scratch/)
- **schema 細節**：看 [`../06-schema-design/`](../06-schema-design/) 比較 bad / good schema 對選擇正確率的影響

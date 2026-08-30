<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 3：從零實作 ReAct（不用 framework）

對應 [Stage 3 — 工具使用與第一個 Agent Loop](../../../stages/03-tool-use-and-hello-agent.md) 練習 3。
> 🎓 **學習模式**：先執行提供的 `starter.py`（`python starter.py`），再只改一個小地方，然後重新執行既有測試 `python test.py`。如果測試失敗，就撤銷或修正這一個改動，再試一次。不需要改名檔案，也不需要整份解答重寫。完整方法看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 70-150 行 illustrative 版、聚焦 `核心 pattern + 兩條 SDK path`，不是進階深度教材。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 ReAct 章節（搭配 [`learn_version` 分支](https://github.com/jjyaoao/HelloAgents/tree/learn_version)）**
> - [ReAct 原論文](https://arxiv.org/abs/2210.03629)（Yao et al. 2022 第 3 節） + [pguso/ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch)（本機 LLM 從零實作）
> - 完整 references 見 [Stage 3 精選 Projects](../../../stages/03-tool-use-and-hello-agent.md#-精選-projects)


## 為什麼從零寫

ReAct（Reasoning + Acting）是現代 agent 的基礎 pattern：

```
while not done:
    thought = LLM 看完目前 context、講出下一步要做什麼
    action = LLM 呼叫一個 tool
    observation = tool 執行結果、餵回去給 LLM
```

LangGraph / CrewAI 把這個 loop 藏起來了。你**自己寫過一次**才知道：

- 為什麼 messages array 一直長
- tool_use_id 跟 tool_result 怎麼配對
- stop_reason 為什麼是 `tool_use` 或 `end_turn`
- max_iter 為什麼是 safety net

70 行 Python 全交代清楚。

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
❓ 問題：'台北人口' 除以 '紐約人口'、答案保留 4 位小數。
------------------------------------------------------------
[step 0] thought: 我先查台北人口...
           tool: lookup_fact({'query': '台北人口'}) → 2602000
[step 1] thought: 接著查紐約人口...
           tool: lookup_fact({'query': '紐約人口'}) → 8336000
[step 2] thought: 計算比例...
           tool: calculator({'expression': '2602000 / 8336000'}) → 0.3121...
[step 3] thought: 答案是 0.3122
------------------------------------------------------------
✅ 最終答案：台北人口除以紐約人口約 0.3122
   共 4 輪
✅ 練習 3 通過 — ReAct loop 自己連用了 lookup_fact 跟 calculator
```

## 不花錢驗證程式邏輯（mock-based）

```powershell
python test.py # 驗 Path A (Ollama) starter.py 邏輯
python test_anthropic.py # 驗 Path B (Anthropic) starter_anthropic.py 邏輯
```

兩條 test 都用 `unittest.mock`、不打真 API、$0/run。Path A 用 OpenAI-compat response shape、Path B 用 Anthropic content blocks。

`test.py` 用 `unittest.mock.MagicMock` 取代 Anthropic client、塞固定 response、驗證你的 loop 邏輯。預期：

```
✅ test_calculator_basic
✅ test_calculator_rejects_eval_injection
✅ test_lookup_fact
✅ test_react_loop_single_tool_call
✅ test_react_loop_multi_step
✅ test_react_loop_respects_max_iter

🎉 全部通過 — 你的 ReAct loop 邏輯正確
```

## 程式結構走查

| 段 | 行 | 在做什麼 |
|---|---|---|
| `tool_calculator` | ~30-40 | 安全的計算器（whitelist 過濾、避免 `eval` 漏洞） |
| `tool_lookup_fact` | ~42-50 | 假事實庫（教學用、避免依賴外部 API） |
| `TOOLS_SPEC` | ~52-75 | tool schema 給 LLM 看 |
| `TOOL_IMPL` | ~77-80 | name → callable 對應表（dispatch） |
| `react_loop` | ~85-130 | 主迴圈、含 max_iter safety、`messages` 累積、tool result 接回去 |

## 常見坑

1. **忘記把 assistant response 加進 messages**：下一輪 LLM 就看不到自己上一輪講過什麼、會 loop forever
2. **tool_result 沒帶 `tool_use_id`**：LLM 無法配對哪個 result 對應哪個 call
3. **`while True` 沒 max_iter**：tool 結果寫得不好、LLM 會無限呼叫；safety net 一定要設
4. **未過濾的 eval**：不要把 model text 送進 `eval`，否則可能造成 RCE；不要靠字元 whitelist 或 `ast.literal_eval` 做算術。改用明確的 AST operator allowlist，並限制輸入長度、AST 深度、節點數與數字／結果大小。

## 想看更聰明的答案？

預設用固定 ID `claude-haiku-4-5-20251001`。想比較 sonnet 時：

```powershell
$env:MODEL = "claude-sonnet-5"; python starter_anthropic.py
```

或在 `starter_anthropic.py` 改 `MODEL = ...` 那行。

## 延伸

- **加更多 tool**：在 `TOOLS_SPEC` + `TOOL_IMPL` 補一個 entry 即可
- **加 streaming**：把 `client.messages.create(...)` 換成 `with client.messages.stream(...) as s:`、邊跑邊印
- **加 prompt cache**：在 `system=` 或 `tools=` 帶 `cache_control={"type":"ephemeral"}` 重複 call 省 90% token
- **接 [LangGraph](https://langchain-ai.github.io/langgraph/) 或 [Pydantic AI](https://ai.pydantic.dev/) 看 framework 怎麼幫你藏掉這 70 行**

<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 4：多步驟推理任務

對應 [Stage 3 — Tool Use & Agent 入門](../../../stages/03-tool-use-and-hello-agent.md) 練習 4。
> 🎓 **學習模式**：這份 `starter.py` 是**完整解答**、不是 TODO skeleton。建議用**主動模式**——`mv starter.py starter_reference.py`、看 signature 不看 body、自己重寫一份 `starter.py`、跑 `python test.py` 驗證；卡 20 分鐘再回去對照 reference。完整方法論看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 70-150 行 illustrative 版、聚焦 `核心 pattern + 兩條 SDK path`，不是進階深度教材。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 planning / multi-step workflow 章節**
> - [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)（什麼時候該拆步驟、什麼時候不要）
> - 完整 references 見 [Stage 3 精選 Projects](../../../stages/03-tool-use-and-hello-agent.md#-精選-projects)


## 為什麼這題重要

把練習 3 的 ReAct loop 延伸成 **3-5 步任務**：查台北人口 → 查紐約人口 → 相除 → 轉百分比。LLM 負責規劃下一步、工具負責可靠地執行小動作；兩者合起來才像能完成 workflow 的 agent。

這題適合觀察不同模型在多步任務上的行為差異；結果可能漏步或提早停止。固定 prompt、tools 和測試題，用 eval 記錄每一步的成功與失敗。

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

預期看到（Path A、本機，理想 4 步走完）：

```
❓ 問題：Find Taipei population divided by New York population, then express it as a percentage.
------------------------------------------------------------
[step 0] tool: lookup_population({'city': 'Taipei'}) → 2602000
[step 1] tool: lookup_population({'city': 'New York'}) → 8336000
[step 2] tool: divide({'a': 2602000, 'b': 8336000}) → 0.3122...
[step 3] tool: to_percentage({'ratio': 0.3122}) → 31.22
------------------------------------------------------------
✅ 最終答案：Taipei is about 31.22% of New York's population.
   共 5 輪
✅ 練習 4 通過 — 你已用本機 qwen2.5:3b 跑通多步 ReAct loop、$0/run
```

## 不花錢驗證程式邏輯（mock-based）

```powershell
python test.py # 驗 Path A (Ollama) starter.py 邏輯
python test_anthropic.py # 驗 Path B (Anthropic) starter_anthropic.py 邏輯
```

兩條 test 都用 `unittest.mock`、不打真 API、$0/run。Path A 用 OpenAI-compat response shape、Path B 用 Anthropic content blocks。

## 觀念提醒

多步任務的核心不是「模型很會算」、而是把複雜任務拆成可靠的小步：

- **工具要窄而有界**：`divide(a, b)` 只做一件事、`b=0` 也不 crash 而是回 0
- **LLM 負責規劃**：決定下一步要呼叫哪個工具、何時停
- **`max_iter=8` 是必要安全網**：避免模型一直要求工具而沒收尾
- **每輪 messages 一直長**：assistant response + tool_result 都接回去、LLM 才看得到歷史

## 兩個 path 觀察重點

| 觀察項 | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| 走完 4 步 | 用固定 eval 測量 | 用固定 eval 測量 |
| 中間步驟順序 | 用固定 eval 測量 | 用固定 eval 測量 |
| 收尾判斷 | 用固定 eval 測量 | 用固定 eval 測量 |
| 預算預留 | $0.05 | $0 API 費用 |

這恰好是 Stage 3 練習 4 的教學重點——**同樣 ReAct loop、不同 model、在哪一步開始崩**。Production 選 model 時，用固定 eval 測量行為與成本。

## 想看更聰明的答案？

預設用固定 ID `claude-haiku-4-5-20251001`。想比較 sonnet 時：

```powershell
$env:MODEL = "claude-sonnet-5"; python starter_anthropic.py
```

或 Ollama path 換更大 model：

```powershell
$env:MODEL = "qwen2.5:7b"; python starter.py
$env:MODEL = "mistral-nemo:12b"; python starter.py
```

## 延伸

- **加更多 tool**：在 `TOOLS_SPEC` + `TOOL_IMPL` 補一個 entry 即可
- **加 retry / error handling**：看 [`../05-error-handling/`](../05-error-handling/) 怎麼處理 tool 失敗
- **schema 設計**：看 [`../06-schema-design/`](../06-schema-design/) 比較 bad / good schema

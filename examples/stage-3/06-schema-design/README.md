<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 6：Function Schema 設計（bad vs good）

對應 [Stage 3 — 工具使用與第一個 Agent Loop](../../../stages/03-tool-use-and-hello-agent.md) 練習 6。
> 🎓 **學習模式**：先執行提供的 `starter_bad.py` 和 `starter_good.py`（`python starter_bad.py`、`python starter_good.py`），再只改一個小地方，然後重新執行既有測試：`python test.py` 和 `python test_anthropic.py`。如果測試失敗，就撤銷或修正這一個改動，再試一次。不需要改名檔案，也不需要整份解答重寫。完整方法看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 70-150 行 illustrative 版、聚焦 `核心 pattern + 兩條 SDK path`，不是進階深度教材。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 [Extra08 — 如何寫出好的 Skill](https://github.com/datawhalechina/hello-agents/blob/main/Extra-Chapter/Extra08-如何写出好的Skill.md)**
> - [OpenAI Function Calling guide](https://developers.openai.com/api/docs/guides/function-calling) + [schema 設計 cheatsheet](../../../resources/schema-design-cheatsheet.md)
> - 完整 references 見 [Stage 3 精選 Projects](../../../stages/03-tool-use-and-hello-agent.md#-精選-projects)


## 為什麼這題重要

Schema 是 **prompt 的一部分**、而且是模型做工具選擇時**最依賴**的 prompt。這題用 `starter_bad` 與 `starter_good` 對照同一題：「把攝氏 32 度換成華氏」。

- **Bad schema**：description 太短、參數都 string、沒 required、沒 enum → LLM 容易把溫度轉換丟給 `process_data`
- **Good schema**：用途明確、`value: number`、`unit: enum["celsius", "fahrenheit"]`、required 都列好 → 應用固定 eval 驗證是否較常選到 `convert_temperature`

寫 schema 不要只想「人看得懂」、要想「模型能不能用它排除錯誤工具」。

## 怎麼跑 — 兩條路徑

### Path A（默認、本機免費、4 個 starter）

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve

python starter_bad.py # 觀察壞 schema 怎麼讓 qwen 挑錯
python starter_good.py # 觀察好 schema 怎麼讓 qwen 挑對
```

預算：**$0 API 費用**；不包含硬體、記憶體與電力成本。

### Path B（Anthropic、雲端比較）

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "your-key"

python starter_bad_anthropic.py
python starter_good_anthropic.py
```

預算：每次先保留 **$0.05**。實際費用依 `輸入 tokens × $1 / 1,000,000 + 輸出 tokens × $5 / 1,000,000` 計算，Tool Use 還會加入 prompt tokens；價格查核日：`2026-08-27`。

## 不花錢驗證程式邏輯（mock-based）

```powershell
python test.py # 驗 Path A (Ollama) starter_bad + starter_good
python test_anthropic.py # 驗 Path B (Anthropic) starter_*_anthropic
```

兩條 test 都用 `unittest.mock`、不打真 API、$0/run。每組 test 都直接檢查 schema 結構（good 有 `required` + `enum`、bad 沒有），不只是看 LLM 怎麼選。

## Bad vs Good schema 對照

| 設計面向 | Bad | Good |
|---|---|---|
| Description | "Process data." | "Use only to summarize structured JSON table rows. Do not use for temperature conversion." |
| 參數型別 | 全部 `string` | `number` / `array` / 對應實際型別 |
| Required | 無 | `["value", "unit"]` |
| Enum 收斂 | 無 | `["celsius", "fahrenheit"]` |
| 失敗回傳 | 簡單字串 | 結構化 dict + retry_hint |

## 兩個 path 的觀察重點（教學重點）

不同 model 對 schema 質量的反應可能不同；固定 prompt、schema 與測試題，用 eval 記錄行為。這題在 Ollama 上也很適合觀察這個差異：

| 觀察項 | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| Bad schema 是否猜對 | 用固定 eval 測量 | 用固定 eval 測量 |
| Good schema 是否選對 | 用固定 eval 測量 | 用固定 eval 測量 |
| Bad／Good 差距 | 用固定 eval 測量 | 用固定 eval 測量 |

換句話說：schema 品質與模型行為要用固定 eval 一起測量。Production 想用便宜 model（qwen / mistral）？schema 必須寫到能上線跑的程度。

## 延伸閱讀

更多 schema 設計規則對照 [`resources/schema-design-cheatsheet.md`](../../../resources/schema-design-cheatsheet.md)：清楚用途、正確型別、必填欄位、enum 收斂、結構化錯誤回傳。

## 延伸

- **故意改壞 good schema**：把一個 enum 拿掉、看 qwen 是否就開始挑錯
- **加第三個工具**：寫一個跟 `convert_temperature` 用途相近但邊界模糊的 tool、看 LLM 怎麼挑
- **接 [`../05-error-handling/`](../05-error-handling/) 的 structured error pattern**：結合 schema 設計 + 錯誤處理、production 級

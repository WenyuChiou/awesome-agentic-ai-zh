<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 2：用 Eval 檢查 Agent

**Eval（評測）**像一張固定考卷：每次改 Prompt、模型或程式後，都用同一批題目再考一次。

對應 [Stage 7 — Agent Production Engineering：Harness、Loop 與 Graph](../../../stages/07-multi-agent-production.md) 練習 2。

## 🎯 學習目標

- 說清楚 **Eval case**：一題輸入、預期結果和評分方法。
- 分辨固定規則與 **LLM-as-judge**，不把 Judge 當成永遠可靠。
- 用完全相符的 `PASS`／`FAIL` 格式，避免把一句話中的 `PASS` 誤判成通過。

## 先跑不花模型費的測試

在這個資料夾開 PowerShell，直接複製：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

看到兩份 `🎉`，就代表五題資料、分數彙整、空回覆和 Judge parser 都通過。這一步只用假回覆。

<details markdown="1">
<summary>Path A：用 Ollama 跑五題 Eval</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

另開 PowerShell：

```powershell
.\.venv\Scripts\python.exe starter.py
```

Ollama 不收模型 API 費，但電力、硬體、下載與等待時間仍有成本。這五題只是教學樣本，不能代表模型在你工作上的品質。

</details>

<details markdown="1">
<summary>Path B：用 Anthropic 跑同一份考卷</summary>

```powershell
$env:ANTHROPIC_API_KEY = "貼上你的金鑰"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

Haiku 4.5 的單價是 input `$1 / 1M` tokens、output `$5 / 1M` tokens：

```text
估算費用 = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

實際費用取決於每題的 token。先在供應商 Console 設定 `$1` spend limit，再用實際 usage 計算；不要把範例估算當帳單。

</details>

## 三個重要詞

- **Eval case**：一筆輸入、預期重點和評分規則。
- **Deterministic evaluator**：同樣輸入一定得到同樣分數，例如 substring 或正規表示式。
- **LLM-as-judge**：請另一個 LLM 評分。它能處理開放式答案，也可能有偏差或格式錯誤。

| 題目形狀 | 先用什麼 | 為什麼 |
|---|---|---|
| 答案必須含 `Tokyo` | substring | 快、便宜、結果固定 |
| 必須符合 JSON schema | schema validator | 直接檢查結構 |
| 語氣是否清楚 | LLM-as-judge + 人工抽查 | 沒有單一固定字串 |

這份練習的 Judge 只接受整份回覆等於 `PASS` 或 `FAIL`。若它回「PASS because...」，程式會要求重試或停止。

## 只改一件事

在 `EVAL_CASES` 加一題你自己的真實問題，再故意讓假 Agent 答錯。確認報告能指出失敗的 `id`。

## 成功檢查

- [ ] 每一題都有穩定且唯一的 `id`。
- [ ] 你能說明這題為什麼用 substring，而不是 LLM Judge。
- [ ] 空答案不會被算成通過。
- [ ] 換模型時仍使用同一份 cases，才能公平看變化。

<details markdown="1">
<summary>從五題走向真正的 Eval suite</summary>

教學流程是：

1. Agent 回答問題。
2. Evaluator 只看該題規則並打分。
3. Runner 保存每題結果與整體 pass rate。
4. 失敗時回到具體 case，不只看一個總分。

正式專案還要加入真實使用者案例、邊界條件、安全案例與人工標註。門檻應由你的 baseline 與風險決定，不要照抄別人的固定百分比。

常見問題：

- cases 都太簡單：加入過去真的答錯過的問題。
- expected 寫整句：只保留必要條件，避免同義句被誤殺。
- 同一模型回答又評分：至少加入固定規則或人工抽查，降低自我偏好。
- 只保存總分：同時保存失敗 `id`、模型 ID、Prompt 版本與日期。

</details>

## 📚 必讀與學習資源

- ⭐⭐⭐⭐⭐ [promptfoo](https://github.com/promptfoo/promptfoo)：可把 cases、providers 和 assertions 放進版本控制。
- ⭐⭐⭐⭐⭐ [Anthropic Console Evals](https://console.anthropic.com/workbench/evals)：用官方介面建立與比較測試集。
- ⭐⭐⭐⭐⭐ [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)：章節式中文 Agent 教材，適合補完整背景。
- ⭐⭐⭐⭐ [LangSmith](https://smith.langchain.com/)：適合已使用 LangChain／LangGraph 的團隊。
- ⭐⭐⭐⭐ [Weights & Biases Weave](https://wandb.ai/site/weave)：把 traces、資料與評測放在同一套工作流。
- ⭐⭐⭐⭐ [Braintrust](https://www.braintrust.dev/)：適合做多版本實驗與結果追蹤。

完整清單見 [Stage 7 精選 Projects](../../../stages/07-multi-agent-production.md#-精選-projects範本--sdk--工具-collection)。

<small>模型、價格、套件與連結查核：2026-08-28 UTC。</small>

<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 核心練習：用 Eval 檢查 Agent

**Eval（評測）**像一張固定考卷：每次改 Prompt、模型或程式後，都用同一批題目再考一次。

對應 [Stage 7 — Agent Production Engineering：Harness、Loop 與 Graph](../../../stages/07-multi-agent-production.md) 核心練習 1。

## 🎯 學習目標

- 說清楚 **Eval case**：一題輸入、預期結果和評分方法。
- 把 5 題 **development split（開發組）**和 3 題 **holdout set（保留考卷）**分開。
- 保存 **Baseline（基準）**，看下一版是進步、相同，還是 **Regression（退步）**。
- 先用固定規則評分；需要 **LLM-as-judge** 時，只接受完整的 `PASS`／`FAIL`。

## 先跑不花模型費的測試

在這個資料夾開 PowerShell，直接複製：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

看到兩份 `🎉`，就代表 8 題版本化資料、5／3 分組、多次 trials、baseline 比較、空回覆與 Judge parser 都通過。這一步只用假回覆，不連網也不需要 API key。

<details markdown="1">
<summary>Path A：用 Ollama 跑 Eval</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

另開 PowerShell：

```powershell
.\.venv\Scripts\python.exe starter.py
```

第一次會跑 5 題開發組、每題 1 次，而且不寫檔。要保存可比較的基準，直接複製：

```powershell
.\.venv\Scripts\python.exe starter.py --split dev --trials 3 --save-report reports/dev-baseline.json
```

改完 Prompt 或程式後，再跑：

```powershell
.\.venv\Scripts\python.exe starter.py --split dev --trials 3 --baseline reports/dev-baseline.json --save-report reports/dev-current.json
```

準備發布時才跑保留考卷：

```powershell
.\.venv\Scripts\python.exe starter.py --split holdout --trials 3 --save-report reports/holdout.json
```

Ollama 不收模型 API 費，但電力、硬體、下載與等待時間仍有成本。這 8 題只是教學樣本，不能代表模型在你工作上的品質。

報告會保存 case ID 與模型輸出，題目則留在版本化資料集；不要放秘密、個資或客戶資料，也不要把敏感報告提交到 Git。`--trials` 限制為 1–20，避免手滑造成無上限的模型呼叫。

</details>

<details markdown="1">
<summary>Path B：用 Anthropic 跑同一份考卷</summary>

```powershell
$env:ANTHROPIC_API_KEY = "貼上你的金鑰"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

Anthropic 路徑也支援上面的 `--split`、`--trials`、`--save-report` 與 `--baseline`。

Haiku 4.5 的單價是 input `$1 / 1M` tokens、output `$5 / 1M` tokens：

```text
估算費用 = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

實際費用取決於每題的 token。先在供應商 Console 設定 `$1` spend limit，再用實際 usage 計算；不要把範例估算當帳單。

</details>

## 五個重要詞

- **Golden／Reference Set（黃金／參考集）**：一盒經過人工確認的好題目，包含輸入、成功條件與評分方法；不是拿來訓練模型或塞進 few-shot 的例句庫。
- **Development split（開發組）**：改 Prompt 或程式時反覆使用的題目；失敗可以幫你修東西。
- **Holdout Set（保留考卷）**：開發時先不看、不反覆跑；準備發布時才用來檢查是否只背熟開發題。
- **Baseline（基準）**：改東西以前保存的成績單，而且要記住資料版本、split、模型與每題結果。
- **Regression（退步）**：新版本在同一份考卷上比基準差；先看失敗題與多次 trials，再決定是否阻擋發布。

**Deterministic evaluator（固定規則評分器）**對同一輸出會給同一分數，例如 substring、exact match 或正規表示式。**LLM-as-judge**能評開放式答案，但可能有偏差或格式錯誤，所以仍要人工抽查。

| 題目形狀 | 先用什麼 | 為什麼 |
|---|---|---|
| 答案必須含 `Tokyo` | substring | 快、便宜、結果固定 |
| 必須符合 JSON schema | schema validator | 直接檢查結構 |
| 語氣是否清楚 | LLM-as-judge + 人工抽查 | 沒有單一固定字串 |

這份練習的 Judge 只接受整份回覆等於 `PASS` 或 `FAIL`。若它回「PASS because...」，程式會要求重試或停止。

## 只改一件事

打開 `eval_cases.json`，把一題開發組換成你的真實失敗案例。保留唯一 `id`、成功條件、grader 與不含機密的來源說明；只要 case 內容改了，就更新 `dataset_version`。再跑：

```powershell
.\.venv\Scripts\python.exe test.py
```

不用先抄到空白文字檔；直接改可執行的資料，確認報告能指出失敗的 `id`。

## 成功檢查

- [ ] 每一題都有穩定且唯一的 `id`。
- [ ] 改過題目、成功條件或 grader 後，`dataset_version` 也有更新。
- [ ] 你知道開發組可以反覆跑，holdout 不可邊改邊偷看。
- [ ] baseline 與目前報告的資料版本、split 和 case IDs 完全相同。
- [ ] 你能說明這題為什麼先用固定規則，而不是 LLM Judge。
- [ ] 空答案不會被算成通過。
- [ ] 報告保留 provider、model、trials、分類結果、失敗題與 improved／same／regressed。

<details markdown="1">
<summary>從 8 題教學資料走向真正的 Eval suite</summary>

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

<small>模型、價格、套件與連結查核：2026-09-13 UTC。</small>

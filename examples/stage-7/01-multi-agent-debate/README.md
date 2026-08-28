<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 1：讓三個 Agent 一起辯論

你會做出三個角色：PRO 說「贊成」、CON 說「反對」，Judge 看完兩邊再選一邊。

對應 [Stage 7 — Multi-Agent 與 Production](../../../stages/07-multi-agent-production.md) 練習 1。

## 🎯 學習目標

- 說清楚 **Multi-Agent**：多個 Agent 分工完成同一件事。
- 讓 PRO 與 CON 各自作答，避免一開始就互相帶答案。
- 用嚴格格式讀 Judge 結果；格式錯了就停止，不偷偷猜。

## 先跑不花模型費的測試

在這個資料夾開 PowerShell，直接複製：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

看到兩份 `🎉`，就代表三次呼叫、空回覆檢查和 Judge 格式都通過。測試使用假回覆，不會連線到模型。

<details markdown="1">
<summary>Path A：用 Ollama 實際辯論</summary>

1. 安裝 [Ollama](https://ollama.com/) 後，先準備模型：

   ```powershell
   ollama pull qwen3.5:4b
   ollama serve
   ```

2. 另開一個 PowerShell：

   ```powershell
   .\.venv\Scripts\python.exe starter.py
   ```

Ollama 不收模型 API 費，但下載時間、電力與電腦硬體仍有成本。模型較慢時，請等它完成，不要用固定秒數判斷失敗。

</details>

<details markdown="1">
<summary>Path B：用 Anthropic 比較結果與預算</summary>

```powershell
$env:ANTHROPIC_API_KEY = "貼上你的金鑰"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

這題會呼叫三次模型。Haiku 4.5 的單價是 input `$1 / 1M` tokens、output `$5 / 1M` tokens：

```text
估算費用 = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

這是估算公式，不是帳單保證。第一次練習前，可在 Anthropic Console 把供應商 spend limit 設成 `$1`；完成後移除 PowerShell 內的金鑰。

</details>

## 三個重要詞

- **PRO / CON**：同一題的贊成方與反對方。
- **Judge**：讀完兩邊答案，再選出較符合題目與證據的一邊。
- **Output contract**：模型必須照約定格式回答。這題只接受 `WINNER=PRO. 理由` 或 `WINNER=CON. 理由`。

PRO 與 CON 都只看原題。Judge 才會看到原題和兩份論點：

```text
題目 ─┬─> PRO ─┐
      └─> CON ─┴─> Judge ─> WINNER + 理由
```

這只能提供第二個視角，不保證答案正確。醫療、法律或高風險決策仍要交給合格的人檢查。

## 只改一件事

把 `q` 換成你熟悉的問題，例如「小團隊要不要先用 Agent framework？」再跑一次。看 Judge 的理由是否真的引用兩邊論點。

## 成功檢查

- [ ] PRO 與 CON 都不是空白。
- [ ] Judge 只輸出一個 Winner，並附上理由。
- [ ] 亂回 `Maybe WINNER=PRO` 時，測試會拒絕它。
- [ ] 你知道多 Agent 是分工方法，不是正確答案保證。

<details markdown="1">
<summary>程式怎麼走、常見問題與延伸</summary>

1. `llm_call()` 先拒絕空字串。
2. `debate()` 分別取得 PRO、CON、Judge 三份文字。
3. `parse_winner()` 用 `fullmatch()` 檢查整份 Judge 回覆，不做子字串猜測。

常見問題：

- 兩邊說得太像：把角色、要保護的目標與限制寫得更明確。
- Judge 格式錯誤：保留錯誤並重試一次，不要默默選一邊。
- 想減少順序偏差：正式評測時交換 PRO／CON 顯示順序，再比較結果。

延伸方向：把兩邊改成「工程師／使用者」、加入人工批准，或把多個題目交給 [promptfoo](https://github.com/promptfoo/promptfoo) 批次評測。

</details>

<details markdown="1">
<summary>📚 深入學習資源與評分</summary>

- ⭐⭐⭐⭐⭐ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：章節式中文 Agent 教材，適合補完整背景。
- ⭐⭐⭐⭐⭐ [Anthropic：Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)：先判斷單 Agent 是否已足夠，再增加協作。
- ⭐⭐⭐⭐ [Microsoft AutoGen](https://github.com/microsoft/autogen)：想看完整 multi-agent framework 時再進入。

完整清單見 [Stage 7 精選 Projects](../../../stages/07-multi-agent-production.md#-精選-projects範本--sdk--工具-collection)。

<small>模型、價格、套件與連結查核：2026-08-28 UTC。</small>

</details>

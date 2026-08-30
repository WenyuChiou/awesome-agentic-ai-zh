<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# Stage 2 練習：改一件事，再看分數

這個練習只做一件事：讓兩個 prompt 回答**同一組六題**，再比較分數。

你會看到這條小路：

```text
同一組六題 → 跑原版 → 加三個例子 → 再跑一次 → 比分數
```

## 第一步：先跑不用模型的版本

在這個資料夾執行：

```bash
python starter.py
```

你會看到原版 `3/6`、加例子後 `6/6`。這些是程式內建的固定答案，用來教你看懂流程；**它不是模型排行榜，也不能證明例子每次都會加分。**

## 第二步：確認程式沒有算錯

```bash
python test.py
python test_anthropic.py
```

兩個測試都不需要 API key，也不會連上模型。看到 `4/4 passed` 和 `2/2 passed` 就完成了。

> 🎓 **學習模式**：先執行提供的 `starter.py`（`python starter.py`），再只改一個小地方，然後重新執行既有測試：`python test.py` 和 `python test_anthropic.py`。如果測試失敗，就撤銷或修正這一個改動，再試一次。不需要改名檔案，也不需要整份解答重寫。完整方法看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

<details markdown="1">
<summary>選擇性：用本機 Ollama 跑真模型（Path A）</summary>

```bash
pip install -r requirements.txt
ollama pull gemma4:e4b
ollama serve
python starter.py --live
```

程式會呼叫本機模型 12 次：六題跑原版，再用同六題跑改良版。API 費用是 `$0`，但會使用你的電腦時間與電力。小模型的分數每次可能不同，這正是要用固定題目重測的原因。

</details>

<details markdown="1">
<summary>選擇性：用 Anthropic 跑真模型（Path B）</summary>

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python starter_anthropic.py --live
```

Windows PowerShell 可改用：

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
python starter_anthropic.py --live
```

預設模型是 `claude-haiku-4-5`。這個短 prompt 的單次呼叫預估低於 `$0.001`，12 次預估低於 `$0.01`；實際費用依 token 數與當下官方價格而變。第一次先設 `$0.05` 總上限，價格以 [Anthropic 官方定價](https://platform.claude.com/docs/en/about-claude/pricing)為準。

</details>

<details markdown="1">
<summary>程式怎麼工作、常見卡點與延伸閱讀</summary>

| 部分 | 白話說明 |
|---|---|
| `CASES` | 六張固定考卷，每張都有正確標籤 |
| `build_prompt()` | 原版與改良版只差三個例子 |
| `evaluate()` | 每答對一題得 1 分 |
| `--live` | 把內建答案換成真正的模型回答 |

常見卡點：

- 回答是 `billing，因為……`：本練習會判錯，因為輸出規則要求只回一個標籤。
- Ollama 連不上：先確認 `ollama serve` 還在執行。
- Anthropic 報認證錯誤：確認 key 放在環境變數，不要寫進程式或 commit。
- 改良版沒有加分：這是正常結果。記下分數，再一次只改一件事。

> 📚 **想學更深？** 先看 [Anthropic Prompt Engineering Overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)理解「先定成功標準，再改 prompt」；再看 [OpenAI Evals 指南](https://developers.openai.com/api/docs/guides/evals)學較完整的評估流程。需要批次測試時，可接著探索 [`promptfoo/promptfoo`](https://github.com/promptfoo/promptfoo)。完整資源仍放在 [Stage 2 精選 Projects](../../../stages/02-prompt-engineering.md#-精選-projects)，不在這裡重複堆滿頁面。

</details>

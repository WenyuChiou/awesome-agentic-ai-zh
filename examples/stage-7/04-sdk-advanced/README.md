<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 4：一邊顯示答案，一邊確認 Cache

**Streaming**讓答案分段出現；**Prompt caching**讓相同的長前綴有機會被重用。兩者解決不同問題。

對應 [Stage 7 — Multi-Agent 與 Production](../../../stages/07-multi-agent-production.md) 練習 4。

## 🎯 學習目標

- 量自己的 first-token latency 與 total latency，不照抄固定秒數。
- 正確略過空 chunk，並在整條 stream 都空白時報錯。
- 用 `cache_creation_input_tokens` 與 `cache_read_input_tokens` 判斷實際結果。

## 先跑不花模型費的測試

在這個資料夾開 PowerShell，直接複製：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

看到兩份 `🎉`，代表 streaming、空回覆和 cache_control 的離線合約都通過。

<details markdown="1">
<summary>Path A：用 Ollama 看 Streaming</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

另開 PowerShell：

```powershell
.\.venv\Scripts\python.exe starter.py
```

Ollama 不收模型 API 費，但硬體、電力與時間仍有成本。記下你自己的第一段文字時間和總時間；模型、電腦、Prompt 與當下負載都會影響結果。

</details>

<details markdown="1">
<summary>Path B：用 Anthropic 看 Streaming 與 Prompt caching</summary>

```powershell
$env:ANTHROPIC_API_KEY = "貼上你的金鑰"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

Haiku 4.5 的一般 input/output 單價是 `$1 / 1M` 與 `$5 / 1M` tokens。5 分鐘 cache write 為一般 input 的 1.25 倍，cache read 為 0.1 倍：

```text
估算費用 =
  normal_input_tokens × $1 / 1M
  + cache_creation_input_tokens × $1.25 / 1M
  + cache_read_input_tokens × $0.10 / 1M
  + output_tokens × $5 / 1M
```

先在供應商 Console 設 `$1` spend limit。實際是否建立或讀到 cache，以 usage 欄位為準，不以「第二次呼叫」猜測。

</details>

## 四個重要詞

- **Chunk**：stream 裡一次到達的一小段文字，不一定剛好是一個 token。
- **First-token latency**：從送出請求到第一段可顯示文字的時間。
- **Total latency**：整份回答完成的時間。
- **Cache breakpoint**：告訴 API「前面這段可以重用」的位置。

這個示範使用 Haiku 4.5。官方最低可快取長度是 **4,096 tokens**，所以程式故意建立遠長於門檻的重複參考文字。程式仍不會宣稱一定命中，而是顯示：

- `cache_creation_input_tokens > 0`：供應商回報建立 cache。
- `cache_read_input_tokens > 0`：供應商回報讀到 cache。
- 兩者都是 0：沒有觀察到建立或命中，請檢查長度、前綴是否完全相同與 TTL。

## 只改一件事

把第二次問題改掉，但保持 `big_system` 完全相同。再看第二次 usage 是否出現 `cache_read_input_tokens`。

## 成功檢查

- [ ] Streaming 時會逐段印字，不會把 `None` 當文字。
- [ ] 整條 stream 沒有文字時會失敗。
- [ ] Cache 示範內容明顯跨過 4,096-token 門檻。
- [ ] 你只根據 usage 說「建立／命中／未觀察到」。

<details markdown="1">
<summary>何時值得 Cache、常見問題</summary>

適合：相同的長 system prompt、tool schema 或參考文件會在短時間內重複使用。

不適合：前綴每次都變、內容太短，或下一次呼叫通常超過 cache TTL。

常見問題：

- `cache_control` 放錯段落：把 breakpoint 放在穩定前綴的結尾。
- 第二次改了前綴：空格、工具順序或模型改變，都可能讓它成為不同 cache。
- 只看理論折扣：同時把 write premium、read tokens、未命中與 output tokens 算進去。
- Streaming 中途斷線：正式 UI 要標示未完成，不能把半份答案當成功。

</details>

<details markdown="1">
<summary>📚 深入學習資源與評分</summary>

- ⭐⭐⭐⭐⭐ [Anthropic Prompt caching 官方文件](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)：最低長度、TTL、breakpoint 與 usage 欄位的權威來源。
- ⭐⭐⭐⭐⭐ [Anthropic Pricing](https://platform.claude.com/docs/en/about-claude/pricing)：用當期單價重算，不保存舊的固定帳單。
- ⭐⭐⭐⭐ [Anthropic Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)：非即時大量工作可再研究 batch。
- ⭐⭐⭐⭐⭐ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：需要章節式背景時使用。

完整清單見 [Stage 7 精選 Projects](../../../stages/07-multi-agent-production.md#-精選-projects範本--sdk--工具-collection)。

<small>模型、價格、套件、cache 條件與連結查核：2026-08-28 UTC。</small>

</details>

<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 1：一個工具、一次完整來回

對應 [Stage 3 — Tool Use & Hello Agent](../../../stages/03-tool-use-and-hello-agent.md) 練習 1。

這題只做一件事：模型說「請呼叫 `get_weather`」，你的 Python 程式檢查參數、執行工具，再把結果交回模型。跑完後，你會親眼看到：

`問題 → Tool Call → 程式檢查並執行 → Tool Result → 最後回答`

**Tool Call** 是模型提出的工具請求。**Tool Result** 是你的程式執行後交回去的結果。模型提出請求，不代表它有權直接執行程式。

## 第一個動作

先在 PowerShell 複製並執行：

```powershell
ollama pull qwen2.5:3b
```

## Path A：Ollama（本機，API 費 `$0`）

```powershell
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
ollama serve
python starter.py
```

如果 `ollama serve` 說連接埠已被使用，通常代表 Ollama 已經在跑；保留那個視窗，再開一個 PowerShell 執行 `python starter.py`。

這條路使用 OpenAI Python SDK 連到 `http://localhost:11434/v1`，資料不會送到 OpenAI 雲端。

## Path B：Anthropic（需要 API key）

```powershell
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "你的-key"
python starter_anthropic.py
```

程式預設使用固定版本 `claude-haiku-4-5-20251001`，避免模型 alias 日後移動時，教學結果悄悄改變。

**預算提醒**：每次正式執行先保留 `$0.05` 上限。實際費用依 token 數計算：

`輸入 token × $1 / 1,000,000 + 輸出 token × $5 / 1,000,000`

Tool Use 還會加入系統提示 token；不要把沒有 token 假設的小數寫成保證價格。價格查核日：`2026-08-27`。

<details markdown="1">
<summary>macOS／Linux 指令</summary>

```bash
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="你的-key"
python starter_anthropic.py
```

</details>

## 不花錢的自我檢查

這兩個測試使用假的模型回應，不連 Ollama，也不呼叫 Anthropic API：

```powershell
python test.py
python test_anthropic.py
```

你應該看到兩次 `all pass`。測試也會故意送入壞 JSON、多餘欄位與不存在的工具，確認程式會先擋下來。

## 你正在保護什麼

- **Allowlist**：只有 `get_weather` 可以執行；模型亂說別的工具名稱也不行。
- **參數驗證**：`city` 不能是空字串，`unit` 只能是 `celsius`，多餘欄位也會被拒絕。
- **結果配對**：每個結果都帶回原本的 `tool_call_id` 或 `tool_use_id`。
- **錯誤標記**：Anthropic 路徑失敗時會加上 `is_error: true`，讓模型知道這不是正常結果。

## 完成條件

- [ ] Path A 或 Path B 至少成功跑一次。
- [ ] 兩個離線測試都顯示 `all pass`。
- [ ] 你能用自己的話說出「模型只提出請求，程式才真正執行」。
- [ ] 你能指出程式在哪裡檢查工具名稱與參數。

## 官方參考

- [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling)
- [Anthropic：How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)
- [Anthropic：Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)
- [Ollama OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility)

文件與 SDK 查核日：`2026-08-27`。

> 📚 **想看完整章節？** 這裡只教第一個最小迴圈。接著讀：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：章節式中文 Agent 課程；把這題當成 tool calling 的起點。
> - [Anthropic Tool Use Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/tool_use)：從單一工具走到多工具的官方 notebook。
> - [Stage 3 精選 Projects](../../../stages/03-tool-use-and-hello-agent.md#-精選-projects)：回到學習地圖挑下一個資源。

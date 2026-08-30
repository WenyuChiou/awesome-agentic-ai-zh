<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 5：讓 Agent 下次還記得

← 回到 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.md#練習-5long-term-memory)

普通聊天紀錄像寫在白板上：程式關掉，白板可能就擦掉了。**Long-term memory（長期記憶）**會把值得保留的事寫進磁碟，下次開程式還能找回來。

## 📌 學習目標

- 分清楚 **chat history**、**working memory**、**long-term memory**。
- 把一條使用者事實寫入 Chroma `PersistentClient`。
- 重新開啟同一個資料庫後找回記憶。
- 把相關記憶放進 system prompt，而不是把全部歷史都塞進去。

## 🔑 核心詞

| 核心詞 | 白話意思 |
|---|---|
| **Working memory** | 這次任務眼前正在用的少量資訊 |
| **Long-term memory** | 跨程式重開或跨 session 仍保留的資訊 |
| **Recall** | 用現在的問題找回相關記憶 |
| **Memory policy** | 決定什麼能記、要更新、要忘記、誰能讀 |

## 📚 必讀與學習資源

- ★★★★★ [Chroma `PersistentClient` 官方文件](https://docs.trychroma.com/reference/python/client)：本練習真正保存到磁碟的基礎。
- ★★★★★ [LangGraph Memory 官方概念頁](https://docs.langchain.com/oss/python/concepts/memory)：分清楚 thread 與跨 thread 記憶。
- ★★★★☆ [Mem0](https://github.com/mem0ai/mem0)：fact extraction、更新與刪除的成熟專案。
- ★★★★☆ [Letta Code](https://github.com/letta-ai/letta-code)：現行 stateful agent 與 working／archival memory 的完整實作。
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：較完整的 Agent memory 教材。

<sub>資料查核：2026-08-30 UTC。</sub>

## ▶️ Path A（Ollama、本機免費）

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

程式會把 Chroma 資料放在 `.stage06-memory`。再次執行時，之前寫入的記憶仍在。API 費用是 **$0**。

<details markdown="1">
<summary>Path B（Anthropic）</summary>

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = Read-Host "Anthropic API key"
python starter_anthropic.py
```

預設 `claude-haiku-4-5` 的費用按 token 計算：每百萬輸入 token **$1**、輸出 token **$5**。執行前請核對 [Anthropic 官方價格頁](https://platform.claude.com/docs/en/about-claude/pricing)並設定小額上限。

</details>

**Stage 06 總預算**：五個 Path A 全部跑完，API 費用仍是 **$0**（不含下載、磁碟與電費）。選跑雲端 Path 時，費用依 embedding／輸入／輸出 token 實際用量計算；先設小額帳戶上限，成功跑一次就停。

## ✅ 不寫入專案資料夾、不連 API 的檢查

```powershell
python test.py
python test_anthropic.py
```

大多數測試注入小型記憶庫與假 LLM；持久化檢查會在系統暫存資料夾建立真正的 `PersistentClient`，讓兩個全新的 Python process 一寫一讀，完成後自動刪除。

## 記憶流程

```text
使用者說話
  → 判斷值不值得記
  → remember() 寫入磁碟
  → 下次問題先 recall()
  → 只把相關記憶放進 prompt
```

```python
memory = MemoryStore(path=".stage06-memory")
memory.remember("User prefers Python.")
recalled = memory.recall("Which language should I learn?")
```

## Chat history 和長期記憶不是同一件事

| 比較 | Chat history | Long-term memory |
|---|---|---|
| 用途 | 保持眼前對話連續 | 下次還記得重要事實 |
| 放哪裡 | 當前 messages | 磁碟或外部資料庫 |
| 怎麼讀 | 最近幾輪直接放進 prompt | 先搜尋，再取少量相關內容 |
| 風險 | prompt 變太長 | 記錯人、記過期資料、刪不乾淨 |

本練習用簡單規則找 `I am`、`I like`、`I prefer` 等句子，只是為了看懂流程。正式系統要有清楚的 **memory policy**：使用者同意、user ID 隔離、更新、刪除、期限與稽核。

<details>
<summary>常見問題與 production 下一步</summary>

- 不要每句都存；先判斷是否真的值得長期保留。
- 同一事實重複出現時，要去重或更新，不要一直新增。
- 使用者搬家或改偏好時，要讓新記憶取代舊記憶。
- 每位使用者必須有獨立 namespace，不能互相看到資料。
- 使用者要求刪除時，要能找到所有副本並確實刪除。
- 需要完整生命週期時，再評估 Mem0、Letta 或 LangGraph persistence。

</details>

完成後，回到 [Stage 6](../../../stages/06-memory-rag.md)做成功檢查，再前往 Stage 7。

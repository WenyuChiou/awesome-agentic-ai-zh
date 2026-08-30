<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 4：把完整 RAG 接起來

← 回到 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.md#練習-4完整-rag-流水線)

**RAG（Retrieval-Augmented Generation，檢索增強生成）**會先找資料，再讓模型看著資料回答。它像開卷考試：先翻到對的頁，再作答。

## 📌 學習目標

- 把 **chunk → embed → retrieve → generate** 四步接起來。
- 看懂 **grounding（依據資料回答）**與 `top_k`。
- 用假的 LLM 回覆離線測完整流程。
- 分清楚「找錯資料」和「看對資料卻答錯」兩種故障。

## 🔑 核心詞

| 核心詞 | 白話意思 |
|---|---|
| **Retrieval** | 先找回可能有答案的段落 |
| **Generation** | 模型讀段落後組成答案 |
| **Grounding** | 答案要能在提供的資料中找到依據 |
| **Top-k** | 最多拿幾段資料給模型看 |

## 📚 必讀與學習資源

- ★★★★★ [OpenAI Retrieval 官方指南](https://developers.openai.com/api/docs/guides/retrieval)：受管 vector store 與搜尋的第一手做法。
- ★★★★★ [LlamaIndex RAG 官方教學](https://docs.llamaindex.ai/en/stable/understanding/rag/)：拆解 ingestion、index、query。
- ★★★★★ [LangChain RAG 官方教學](https://docs.langchain.com/oss/python/langchain/rag)：比較 two-step 與 agentic RAG。
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：較完整的 RAG 流水線教材。

<sub>資料查核：2026-08-30 UTC。</sub>

## ▶️ Path A（Ollama、本機免費）

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

模型在本機執行，API 費用是 **$0**。

<details markdown="1">
<summary>Path B（Anthropic）</summary>

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = Read-Host "Anthropic API key"
python starter_anthropic.py
```

預設模型是 `claude-haiku-4-5`。現行標準價格為每百萬輸入 token **$1**、輸出 token **$5**；實際費用依 token 用量計算：

```text
費用 = 輸入 token ÷ 1,000,000 × 1
     + 輸出 token ÷ 1,000,000 × 5
```

執行前請再看 [Anthropic 官方價格頁](https://platform.claude.com/docs/en/about-claude/pricing)，並設定小額使用上限。

</details>

**Stage 06 總預算**：五個 Path A 全部跑完，API 費用仍是 **$0**（不含下載、磁碟與電費）。選跑雲端 Path 時，費用依 embedding／輸入／輸出 token 實際用量計算；先設小額帳戶上限，成功跑一次就停。

## ✅ 不連 API 的完整檢查

```powershell
python test.py
python test_anthropic.py
```

測試會替換 LLM 與 embedding，不下載模型、不扣款，但仍會確認 context 真的進入 prompt。

## RAG 四步

```text
文件 → 1. chunk → 2. embed/index → 3. retrieve top-k → 4. generate
```

```python
collection = build_kb(doc)
contexts = retrieve(collection, query, top_k=2)
answer = generate(query, contexts)
```

| 步驟 | 主要設定 | 出錯時會看到什麼 |
|---|---|---|
| **Chunk** | size、overlap、文件結構 | 正確句子被切斷 |
| **Embed / index** | embedding model、資料更新 | 新資料找不到 |
| **Retrieve** | `top_k`、filter、reranker | 拿回錯段落或漏段落 |
| **Generate** | prompt、模型、輸出限制 | context 對，答案仍亂猜 |

## 最小 grounding 規則

```text
只根據提供的 context 回答。
如果 context 沒有答案，就清楚說不知道。
```

這能降低亂答，但不能保證零 hallucination。正式系統還需要無答案測試、引用、輸出驗證與人工抽查。

<details>
<summary>常見問題與下一步</summary>

- `top_k` 太小會漏資料；太大會把雜訊和 token 成本一起放大。
- 每次問題都重建 index 很浪費；資料沒變時應重用持久化 collection。
- 只測「答得出來」不夠，也要測「資料沒有答案時會拒答」。
- 進階可加入 query rewriting、reranker、citation 與 evaluation；先一次只改一個零件。

</details>

下一步：把外部文件換成使用者過去說過的事，完成 [練習 5：Long-term Memory](../05-long-term-memory/README.md)。

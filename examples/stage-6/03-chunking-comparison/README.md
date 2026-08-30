<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 3：比較三種 Chunking

← 回到 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.md#練習-3chunking-對照)

**Chunking（切塊）**就是把一份長文件切成幾個小盒子。盒子太大，細節會被埋住；盒子太小，意思會被切斷。

## 📌 學習目標

- 說出 **fixed-length**、**paragraph-based**、**heading-aware** 三種切法。
- 知道 **chunk size** 與 **overlap** 會改變搜尋結果。
- 用同一份文件和同一組問題公平比較三種策略。
- 阻擋會讓程式卡住的錯誤 overlap。

## 🔑 核心詞

| 核心詞 | 白話意思 |
|---|---|
| **Chunk** | 長文件切出來的一小段 |
| **Chunk size** | 每一段最多多大 |
| **Overlap** | 前後兩段重複保留的文字，避免句子剛好被切斷 |
| **Retrieval** | 用問題找回最有用的段落 |

## 📚 必讀與學習資源

- ★★★★★ [LangChain text splitters 官方概念頁](https://docs.langchain.com/oss/python/integrations/splitters)：從簡單切法開始。
- ★★★★★ [LlamaIndex Semantic Splitter 官方 API](https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/semantic_splitter/)：需要語意斷點時再進階。
- ★★★★☆ [Unstructured 官方文件](https://docs.unstructured.io/)：PDF、DOCX、HTML 等複雜格式的解析入口。
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：較完整的 RAG chunking 教材。

<sub>資料查核：2026-08-30 UTC。</sub>

## ▶️ 先直接跑 Path A（本機、與廠商無關、免費）

```powershell
pip install -r requirements.txt
python starter.py
```

第一次執行可能下載本機 embedding 模型，API 費用是 **$0**。

<details markdown="1">
<summary>Path B（預覽：這一步之後怎麼接到 Claude）</summary>

Chunking 這一步只負責「怎麼切文件」，跟之後用哪一家模型生成答案無關。這裡跑一次 `starter_anthropic.py`，只是先讓你看到同一套切塊程式，之後會原封不動接到[練習 4](../04-full-rag-pipeline/README.md)的 Claude 生成步驟前面。這一步沒有呼叫任何 API，費用是 **$0**。

```powershell
python starter_anthropic.py
```

</details>

**Stage 06 總預算**：五個 Path A 全部跑完，API 費用仍是 **$0**（不含下載、磁碟與電費）。選跑雲端 Path 時，費用依 embedding／輸入／輸出 token 實際用量計算；先設小額帳戶上限，成功跑一次就停。

```powershell
python test.py
python test_anthropic.py
```

測試只驗切塊邏輯，不下載模型。

## 三種切法

| 策略 | 怎麼切 | 適合什麼 |
|---|---|---|
| **Fixed-length** | 每 N 個字切一段 | 沒有清楚格式的 log 或聊天紀錄 |
| **Paragraph-based** | 遇到空白行就切 | 段落整齊的文章 |
| **Heading-aware** | 遇到 `#`、`##` 標題就切 | README、wiki、spec |

```python
fixed = chunk_fixed(text, chunk_size=200, overlap=40)
paragraphs = chunk_paragraphs(text)
headings = chunk_headings(text)
```

`overlap` 必須滿足：

```text
0 <= overlap < chunk_size
```

如果 `overlap` 等於或大於 `chunk_size`，下一段就不會往前走。程式現在會直接丟出 `ValueError`，不讓它變成無限迴圈。

## 怎麼判斷哪種比較好

不要只數 chunk，也不要只看一個漂亮例子。準備真實問題，確認正確答案所在的段落有沒有進入 top-k。

| 要看什麼 | 問自己 |
|---|---|
| **Recall** | 正確段落有沒有被找回來？ |
| **Precision** | 找回來的段落裡，有多少真的有用？ |
| **完整性** | 答案需要的句子有沒有被切到兩邊？ |
| **成本** | chunk 變多後，embedding 與儲存量增加多少？ |

<details>
<summary>常見問題與進階做法</summary>

- Chunk 太大：一段塞太多主題，向量會變得模糊。
- Chunk 太小：答案需要的前後文可能分散在不同段。
- PDF 不等於純文字：先處理欄位、表格、頁首頁尾，再切塊。
- CJK 文字不要用 byte 數硬切；用 Python 字串、tokenizer 或結構化 parser。
- 進階做法：先按 heading 切大段，再在段內用固定長度切小段。

</details>

下一步：把切塊、embedding、搜尋與回答接成 [練習 4：完整 RAG](../04-full-rag-pipeline/README.md)。

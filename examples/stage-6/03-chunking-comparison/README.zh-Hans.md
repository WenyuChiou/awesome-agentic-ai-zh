<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 3：比较三种 Chunking

← 回到 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.zh-Hans.md#练习-3chunking-对照)

**Chunking（切块）**就是把一份长文档切成几个小盒子。盒子太大，细节会被埋住；盒子太小，意思会被切断。

## 📌 学习目标

- 说出 **fixed-length**、**paragraph-based**、**heading-aware** 三种切法。
- 知道 **chunk size** 与 **overlap** 会改变搜索结果。
- 用同一份文档和同一组问题公平比较三种策略。
- 阻挡会让程序卡住的错误 overlap。

## 🔑 核心词

| 核心词 | 白话意思 |
|---|---|
| **Chunk** | 长文档切出来的一小段 |
| **Chunk size** | 每一段最多多大 |
| **Overlap** | 前后两段重复保留的文字，避免句子刚好被切断 |
| **Retrieval** | 用问题找回最有用的段落 |

## 📚 必读与学习资源

- ★★★★★ [LangChain text splitters 官方概念页](https://docs.langchain.com/oss/python/integrations/splitters)：从简单切法开始。
- ★★★★★ [LlamaIndex Semantic Splitter 官方 API](https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/semantic_splitter/)：需要语义断点时再进阶。
- ★★★★☆ [Unstructured 官方文档](https://docs.unstructured.io/)：PDF、DOCX、HTML 等复杂格式的解析入口。
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：较完整的 RAG chunking 教材。

<sub>资料查核：2026-08-30 UTC。</sub>

## ▶️ 先直接跑 Path A（本机、与厂商无关、免费）

```powershell
pip install -r requirements.txt
python starter.py
```

第一次执行可能下载本机 embedding 模型，API 费用是 **$0**。

<details markdown="1">
<summary>Path B（预览：这一步之后怎么接到 Claude）</summary>

Chunking 这一步只负责“怎么切文档”，跟之后用哪一家模型生成答案无关。这里跑一次 `starter_anthropic.py`，只是先让你看到同一套切块程序，之后会原封不动接到[练习 4](../04-full-rag-pipeline/README.zh-Hans.md)的 Claude 生成步骤前面。这一步没有调用任何 API，费用是 **$0**。

```powershell
python starter_anthropic.py
```

</details>

**Stage 06 总预算**：五个 Path A 全部跑完，API 费用仍是 **$0**（不含下载、磁盘与电费）。选跑云端 Path 时，费用依 embedding／输入／输出 token 实际用量计算；先设小额账户上限，成功跑一次就停。

```powershell
python test.py
python test_anthropic.py
```

测试只验切块逻辑，不下载模型。

## 三种切法

| 策略 | 怎么切 | 适合什么 |
|---|---|---|
| **Fixed-length** | 每 N 个字切一段 | 没有清楚格式的 log 或聊天记录 |
| **Paragraph-based** | 遇到空白行就切 | 段落整齐的文章 |
| **Heading-aware** | 遇到 `#`、`##` 标题就切 | README、wiki、spec |

```python
fixed = chunk_fixed(text, chunk_size=200, overlap=40)
paragraphs = chunk_paragraphs(text)
headings = chunk_headings(text)
```

`overlap` 必须满足：

```text
0 <= overlap < chunk_size
```

如果 `overlap` 等于或大于 `chunk_size`，下一段就不会往前走。程序现在会直接抛出 `ValueError`，不让它变成无限循环。

## 怎么判断哪种比较好

不要只数 chunk，也不要只看一个漂亮例子。准备真实问题，确认正确答案所在的段落有没有进入 top-k。

| 要看什么 | 问自己 |
|---|---|
| **Recall** | 正确段落有没有被找回来？ |
| **Precision** | 找回来的段落里，有多少真的有用？ |
| **完整性** | 答案需要的句子有没有被切到两边？ |
| **成本** | chunk 变多后，embedding 与存储量增加多少？ |

<details>
<summary>常见问题与进阶做法</summary>

- Chunk 太大：一段塞太多主题，向量会变得模糊。
- Chunk 太小：答案需要的前后文可能分散在不同段。
- PDF 不等于纯文本：先处理栏位、表格、页眉页脚，再切块。
- CJK 文字不要用 byte 数硬切；用 Python 字符串、tokenizer 或结构化 parser。
- 进阶做法：先按 heading 切大段，再在段内用固定长度切小段。

</details>

下一步：把切块、embedding、搜索与回答接成 [练习 4：完整 RAG](../04-full-rag-pipeline/README.zh-Hans.md)。

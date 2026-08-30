<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 4：把完整 RAG 接起来

← 回到 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.zh-Hans.md#练习-4完整-rag-流水线)

**RAG（Retrieval-Augmented Generation，检索增强生成）**会先找数据，再让模型看着数据回答。它像开卷考试：先翻到对的页，再作答。

## 📌 学习目标

- 把 **chunk → embed → retrieve → generate** 四步接起来。
- 看懂 **grounding（依据数据回答）**与 `top_k`。
- 用假的 LLM 回复离线测完整流程。
- 分清楚“找错数据”和“看对数据却答错”两种故障。

## 🔑 核心词

| 核心词 | 白话意思 |
|---|---|
| **Retrieval** | 先找回可能有答案的段落 |
| **Generation** | 模型读段落后组成答案 |
| **Grounding** | 答案要能在提供的数据中找到依据 |
| **Top-k** | 最多拿几段数据给模型看 |

## 📚 必读与学习资源

- ★★★★★ [OpenAI Retrieval 官方指南](https://developers.openai.com/api/docs/guides/retrieval)：受管 vector store 与搜索的第一手做法。
- ★★★★★ [LlamaIndex RAG 官方教程](https://docs.llamaindex.ai/en/stable/understanding/rag/)：拆解 ingestion、index、query。
- ★★★★★ [LangChain RAG 官方教程](https://docs.langchain.com/oss/python/langchain/rag)：比较 two-step 与 agentic RAG。
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：较完整的 RAG 流水线教材。

<sub>资料查核：2026-08-30 UTC。</sub>

## ▶️ Path A（Ollama、本机免费）

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

模型在本机执行，API 费用是 **$0**。

<details markdown="1">
<summary>Path B（Anthropic）</summary>

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = Read-Host "Anthropic API key"
python starter_anthropic.py
```

默认模型是 `claude-haiku-4-5`。现行标准价格为每百万输入 token **$1**、输出 token **$5**；实际费用依 token 用量计算：

```text
费用 = 输入 token ÷ 1,000,000 × 1
     + 输出 token ÷ 1,000,000 × 5
```

执行前请再看 [Anthropic 官方价格页](https://platform.claude.com/docs/en/about-claude/pricing)，并设定小额使用上限。

</details>

**Stage 06 总预算**：五个 Path A 全部跑完，API 费用仍是 **$0**（不含下载、磁盘与电费）。选跑云端 Path 时，费用依 embedding／输入／输出 token 实际用量计算；先设小额账户上限，成功跑一次就停。

## ✅ 不连 API 的完整检查

```powershell
python test.py
python test_anthropic.py
```

测试会替换 LLM 与 embedding，不下载模型、不扣款，但仍会确认 context 真的进入 prompt。

## RAG 四步

```text
文档 → 1. chunk → 2. embed/index → 3. retrieve top-k → 4. generate
```

```python
collection = build_kb(doc)
contexts = retrieve(collection, query, top_k=2)
answer = generate(query, contexts)
```

| 步骤 | 主要设定 | 出错时会看到什么 |
|---|---|---|
| **Chunk** | size、overlap、文档结构 | 正确句子被切断 |
| **Embed / index** | embedding model、数据更新 | 新数据找不到 |
| **Retrieve** | `top_k`、filter、reranker | 拿回错段落或漏段落 |
| **Generate** | prompt、模型、输出限制 | context 对，答案仍乱猜 |

## 最小 grounding 规则

```text
只根据提供的 context 回答。
如果 context 没有答案，就清楚说不知道。
```

这能降低乱答，但不能保证零 hallucination。正式系统还需要无答案测试、引用、输出验证与人工抽查。

<details>
<summary>常见问题与下一步</summary>

- `top_k` 太小会漏数据；太大会把噪声和 token 成本一起放大。
- 每次问题都重建 index 很浪费；数据没变时应重用持久化 collection。
- 只测“答得出来”不够，也要测“数据没有答案时会拒答”。
- 进阶可加入 query rewriting、reranker、citation 与 evaluation；先一次只改一个零件。

</details>

下一步：把外部文档换成用户过去说过的事，完成 [练习 5：Long-term Memory](../05-long-term-memory/README.zh-Hans.md)。

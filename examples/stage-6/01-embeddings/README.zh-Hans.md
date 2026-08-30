<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 1：Embeddings 与相似内容搜索

← 回到 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.zh-Hans.md#练习-1embeddings)

想象你把每句话放到一张大地图上。意思接近的句子会站得比较近。**Embedding（嵌入向量）**，就是每句话在这张地图上的数字坐标。

## 📌 学习目标

- 说出 **embedding**、**vector（向量）**、**cosine similarity（余弦相似度）** 是什么。
- 把 100 个句子转成向量。
- 找出最接近问题的前 `top-k` 个句子。
- 分清楚本机模型和云端 embedding 的差别。

## 🔑 先懂三个核心词

| 核心词 | 白话意思 | 程序里看到什么 |
|---|---|---|
| **Embedding** | 把文字变成一排数字，方便电脑比较意思 | `model.encode(...)` |
| **Vector** | 那一排数字 | `[0.12, -0.04, ...]` |
| **Cosine similarity** | 看两个向量的方向有多像；越接近 `1`，意思通常越近 | `sent_vecs @ q_vec` |

## 📚 必读与学习资源

- ★★★★★ [Sentence Transformers 官方文档](https://www.sbert.net/)：本机 embedding 的第一手说明与示例。
- ★★★★★ [OpenAI `text-embedding-3-small` 官方模型页](https://developers.openai.com/api/docs/models/text-embedding-3-small)：云端模型、用途与现行价格。
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：适合读完本练习后，再看较完整的 embedding 与 RAG 章节。

<sub>资料查核：2026-08-30 UTC。</sub>

## ▶️ 先直接跑 Path A（本机、免费）

```powershell
pip install -r requirements.txt
python starter.py
```

第一次执行会下载 `sentence-transformers/all-MiniLM-L6-v2`。模型在你的电脑执行，API 费用是 **$0**。

<details markdown="1">
<summary>Path B（云端 embedding，OpenAI）</summary>

```powershell
pip install -r requirements.txt
$env:OPENAI_API_KEY = Read-Host "OpenAI API key"
python starter_anthropic.py
```

Anthropic 目前没有自家的 embedding API；[Anthropic 官方 embedding 指南](https://platform.claude.com/docs/en/build-with-claude/embeddings)以 Voyage AI 为主要示例。这份入门程序用 OpenAI，让你能跟本机结果做简单对照。

`text-embedding-3-small` 的费用按输入 token 计算：

```text
费用 = 输入 token 数 ÷ 1,000,000 × 每百万 token 价格
```

执行前先到官方模型页确认价格，并为 API 账户设定小额使用上限。

</details>

**Stage 06 总预算**：五个 Path A 全部跑完，API 费用仍是 **$0**（不含下载、磁盘与电费）。选跑云端 Path 时，费用依 embedding／输入／输出 token 实际用量计算；先设小额账户上限，成功跑一次就停。

## ✅ 不下载模型也能验证

```powershell
python test.py
python test_anthropic.py
```

测试使用假的向量与假的 API 回复，所以不会连外、不会扣款。

## 程序只做三件事

```python
sent_vecs = model.encode(sentences, normalize_embeddings=True)
q_vec = model.encode([query], normalize_embeddings=True)[0]
sims = sent_vecs @ q_vec
top_idx = np.argsort(-sims)[:top_k]
```

1. 把句子和问题都变成向量。
2. 比较向量方向。
3. 把分数最高的 `top-k` 笔放到前面。

**Normalize（正规化）**会把向量调成相同长度。完成后，dot product 就能直接当 cosine similarity 使用。

<details>
<summary>常见问题与下一步</summary>

- **不同模型的向量不能混用**：它们像两张不同的地图，坐标不能直接比较。
- **查询太短**：只有一两个字时，意思不够清楚，搜索结果容易飘。
- **`top_k` 不是越大越好**：拿太多内容会把噪声一起带回来。
- 想比较模型时，可看 [MTEB](https://huggingface.co/spaces/mteb/leaderboard)，但要用自己的语言与数据再测一次。

</details>

下一步：把向量放进 [练习 2：Vector DB](../02-vector-db/README.zh-Hans.md)，不必每次从头比较全部句子。

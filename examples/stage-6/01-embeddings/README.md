<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 1：Embeddings 與相似內容搜尋

← 回到 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.md#練習-1embeddings)

想像你把每句話放到一張大地圖上。意思接近的句子會站得比較近。**Embedding（嵌入向量）**，就是每句話在這張地圖上的數字座標。

## 📌 學習目標

- 說出 **embedding**、**vector（向量）**、**cosine similarity（餘弦相似度）** 是什麼。
- 把 100 個句子轉成向量。
- 找出最接近問題的前 `top-k` 個句子。
- 分清楚本機模型和雲端 embedding 的差別。

## 🔑 先懂三個核心詞

| 核心詞 | 白話意思 | 程式裡看到什麼 |
|---|---|---|
| **Embedding** | 把文字變成一排數字，方便電腦比較意思 | `model.encode(...)` |
| **Vector** | 那一排數字 | `[0.12, -0.04, ...]` |
| **Cosine similarity** | 看兩個向量的方向有多像；越接近 `1`，意思通常越近 | `sent_vecs @ q_vec` |

## 📚 必讀與學習資源

- ★★★★★ [Sentence Transformers 官方文件](https://www.sbert.net/)：本機 embedding 的第一手說明與範例。
- ★★★★★ [OpenAI `text-embedding-3-small` 官方模型頁](https://developers.openai.com/api/docs/models/text-embedding-3-small)：雲端模型、用途與現行價格。
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：適合讀完本練習後，再看較完整的 embedding 與 RAG 章節。

<sub>資料查核：2026-08-30 UTC。</sub>

## ▶️ 先直接跑 Path A（本機、免費）

```powershell
pip install -r requirements.txt
python starter.py
```

第一次執行會下載 `sentence-transformers/all-MiniLM-L6-v2`。模型在你的電腦執行，API 費用是 **$0**。

<details markdown="1">
<summary>Path B（雲端 embedding，OpenAI）</summary>

```powershell
pip install -r requirements.txt
$env:OPENAI_API_KEY = Read-Host "OpenAI API key"
python starter_anthropic.py
```

Anthropic 目前沒有自家的 embedding API；[Anthropic 官方 embedding 指南](https://platform.claude.com/docs/en/build-with-claude/embeddings)以 Voyage AI 為主要示例。這份入門程式用 OpenAI，讓你能跟本機結果做簡單對照。

`text-embedding-3-small` 的費用按輸入 token 計算：

```text
費用 = 輸入 token 數 ÷ 1,000,000 × 每百萬 token 價格
```

執行前先到官方模型頁確認價格，並為 API 帳戶設定小額使用上限。

</details>

**Stage 06 總預算**：五個 Path A 全部跑完，API 費用仍是 **$0**（不含下載、磁碟與電費）。選跑雲端 Path 時，費用依 embedding／輸入／輸出 token 實際用量計算；先設小額帳戶上限，成功跑一次就停。

## ✅ 不下載模型也能驗證

```powershell
python test.py
python test_anthropic.py
```

測試使用假的向量與假的 API 回覆，所以不會連外、不會扣款。

## 程式只做三件事

```python
sent_vecs = model.encode(sentences, normalize_embeddings=True)
q_vec = model.encode([query], normalize_embeddings=True)[0]
sims = sent_vecs @ q_vec
top_idx = np.argsort(-sims)[:top_k]
```

1. 把句子和問題都變成向量。
2. 比較向量方向。
3. 把分數最高的 `top-k` 筆放到前面。

**Normalize（正規化）**會把向量調成相同長度。完成後，dot product 就能直接當 cosine similarity 使用。

<details>
<summary>常見問題與下一步</summary>

- **不同模型的向量不能混用**：它們像兩張不同的地圖，座標不能直接比較。
- **查詢太短**：只有一兩個字時，意思不夠清楚，搜尋結果容易飄。
- **`top_k` 不是越大越好**：拿太多內容會把雜訊一起帶回來。
- 想比較模型時，可看 [MTEB](https://huggingface.co/spaces/mteb/leaderboard)，但要用自己的語言與資料再測一次。

</details>

下一步：把向量放進 [練習 2：Vector DB](../02-vector-db/README.md)，不必每次從頭比較全部句子。

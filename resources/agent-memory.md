# Agent Memory：只記值得記、允許記、能刪掉的事

[繁體中文](agent-memory.md) | [English](agent-memory.en.md) | [简体中文](agent-memory.zh-Hans.md)

<!-- freshness: canonical=resources/agent-memory.md; verified_on=2026-08-30; scope=memory,privacy,retention,isolation,project-status; max_age_days=90 -->

← [回到 Stage 6：RAG 與 Memory](../stages/06-memory-rag.md)

**Agent Memory（代理記憶）**像一本有管理規則的筆記本。它不是把所有聊天偷偷存起來；它只保存之後真的需要、使用者允許，而且可以查看、修改與刪除的內容。

## 📌 學習目標

完成這頁後，你可以：

1. 分清楚聊天紀錄、context、RAG 與 Memory。
2. 分清楚短期／長期，以及 semantic／episodic／procedural memory。
3. 畫出一筆記憶從寫入、搜尋、更新到刪除的生命週期。
4. 為每筆記憶設定擁有者、來源、保存期限與刪除方法。
5. 用固定測試檢查「該記的找得到，不該記的不會留下」。

## 🧩 先把四樣東西分開

| 核心詞 | 小孩版 | 正確意思 |
|---|---|---|
| **Chat History（聊天紀錄）** | 這次對話的逐字稿 | 訊息紀錄；不代表每一則都應永久保存或放進模型 context。 |
| **Context（上下文）** | 這一刻放在桌上的資料 | 本次模型呼叫實際看到的 instructions、messages、工具結果與取回內容。 |
| **RAG** | 有問題時去書架找資料 | 從外部知識來源取回證據，再交給模型回答。 |
| **Memory（記憶）** | 助理留給下次的短筆記 | 跨步驟、thread 或 session 仍需讀回的狀態，必須有寫入與治理規則。 |

**最重要的判斷：**產品手冊放知識庫；目前任務做到哪裡放短期 state；經使用者同意保存的偏好才可能進長期 memory。

## 📚 必修閱讀

1. [LangChain：Memory overview](https://docs.langchain.com/oss/python/concepts/memory) — 先理解 thread-scoped short-term memory、跨 session long-term memory，以及 semantic／episodic／procedural 三種類型。
2. [LangGraph：Add and manage memory](https://docs.langchain.com/oss/python/langgraph/add-memory) — 看 checkpointer、store、namespace 與 semantic search 的實作邊界。
3. [CoALA paper](https://arxiv.org/abs/2309.02427) — 用一個共同框架理解 language agent 的 memory 結構與操作。
4. [Generative Agents paper](https://arxiv.org/abs/2304.03442) — 看 recency、importance、relevance 與 reflection 的經典研究設計。
5. [Mem0](https://github.com/mem0ai/mem0) 或 [Letta Code](https://github.com/letta-ai/letta-code) — 選一個現行實作，觀察狀態怎麼保存與取回。[Letta 專案入口](https://github.com/letta-ai/letta)目前是 landing page；現行 source 與 App Server 都在 Letta Code。

## ⏱ 兩種時間範圍

- **Short-term Memory（短期記憶）**：只服務一個 thread 或目前任務，例如訊息、上傳檔案、工具結果與做到哪一步。LangGraph 通常把它放在 thread-scoped state，透過 checkpointer 保存。
- **Long-term Memory（長期記憶）**：跨 thread 或 session 仍需要，例如使用者允許保存的偏好、專案事實或可重用經驗。它必須用 namespace 隔離不同使用者與應用。

短期不等於「只放 RAM」；長期也不等於「永遠不刪」。差別在取回範圍與生命週期，不是硬碟或記憶體的名稱。

## 🧠 三種內容類型

| 類型 | 記什麼 | 例子 | 風險 |
|---|---|---|---|
| **Semantic Memory（語意記憶）** | 較穩定的事實 | 使用者偏好短答、專案使用 Python 3.13 | 事實會過期或互相衝突 |
| **Episodic Memory（情節記憶）** | 發生過的事件與結果 | 上次部署在哪一步失敗、哪個修法有效 | 成功一次不代表永遠適用 |
| **Procedural Memory（程序記憶）** | 做事規則與步驟 | 發版前要跑哪些 gate | 惡意內容可能污染未來行為 |

**Semantic memory** 和 **semantic search** 不是同一件事：前者是記住的「內容類型」，後者是依意思相近來搜尋的「取回方法」。

## 🔄 一筆 Memory 的生命週期

1. **提議寫入**：先判斷是否真的需要跨 session 使用。
2. **取得同意**：敏感資料或個人偏好要讓使用者知道保存目的。
3. **正規化**：保存簡短事實，不直接把整段聊天當記憶。
4. **加上 metadata**：至少有 owner、source、created_at、updated_at、expires_at 與 sensitivity。
5. **隔離保存**：用 user／workspace／agent namespace 分開，查詢前先套權限。
6. **搜尋與使用**：只取回與目前任務相關的少量記憶，並保留來源。
7. **更新或解決衝突**：新資訊不能悄悄和舊資訊並存；要標記版本或取代關係。
8. **刪除與忘記**：使用者可查看、修改、刪除；過期資料自動清除，備份也要有處理規則。

## 🧱 先選最簡單的設計

| 問題 | 先用什麼 | 何時升級 |
|---|---|---|
| 欄位固定，例如語言、時區、通知偏好 | **直接狀態表** | 欄位種類變多或需要模糊搜尋時 |
| 內容較自由，例如短摘要或可重用經驗 | **可搜尋文字 memory** | 關係、時間與衝突成為主要問題時 |
| 人、事件與關係會隨時間改變 | **Temporal Knowledge Graph** | 只有測試證明一般資料表／搜尋不夠時 |
| 只需恢復同一個工作流程 | **Checkpoint／thread state** | 真正需要跨 thread 分享時 |

**先從資料表開始。**能用明確欄位保存的內容，不必先做向量搜尋；能用短期 state 解決的問題，不必先做永久記憶。

## 🛡️ Memory 的安全底線

- 預設不保存密碼、API key、付款資料、醫療秘密或未經同意的個資。
- 不讓不同使用者、tenant、workspace 或 agent 共用同一個未隔離 namespace。
- 取回前做權限檢查；不能先拿到秘密再靠 prompt 要模型「不要說」。
- 記憶內容是不可信輸入。寫入前做 schema、來源與 prompt-injection 檢查。
- 每筆記憶要能回答「誰寫的、從哪裡來、何時更新、何時刪」。
- 刪除要涵蓋主要儲存、搜尋索引、cache 與依政策管理的備份。

## 🛠 一個最小 Memory 練習

只保存一項無敏感性的偏好，例如「回答先給短版」。

1. 寫入偏好與 `user_id`、來源、時間、保存期限。
2. 用另一個 thread 搜尋並讀回。
3. 把偏好改成「先給表格」，確認舊值不再被使用。
4. 刪除偏好，再搜尋一次，結果必須為空。
5. 用另一個 `user_id` 查詢，不能看到前一位使用者的內容。

**完成條件：**add、search、update、delete 與 user isolation 五項測試都通過；只會 `add` 不算完成。

<details markdown="1">
<summary>Hot path、Background 與衝突處理</summary>

- **Hot path write**：回答前立刻寫入，結果最新，但會增加延遲，錯誤也直接影響使用者。
- **Background write**：回覆後非同步整理，互動較快，但要處理失敗、重試與晚到更新。
- 同一事實有新舊版本時，保存時間、來源與有效範圍；不要只依向量相似度隨機挑一筆。
- 先把「模型建議的 memory」放入待確認區，再由規則或使用者核准，適合高風險內容。

</details>

<details markdown="1">
<summary>常見失敗與排查順序</summary>

1. 找不到：先看 namespace、權限、filter 與保存是否成功。
2. 找到舊資料：看 update 是否留下互相衝突的版本，以及 cache 是否刷新。
3. 記太多：提高寫入門檻、縮短保存期限，不要只擴大 context window。
4. 記錯：保留來源與信心，讓使用者能修改，不把模型推測直接當事實。
5. 刪不乾淨：追蹤主庫、索引、cache、事件串流與備份的刪除路徑。

</details>

## 🎯 精選 Projects 與學習資源

評分代表「對這張學習地圖的教學價值」，不是專案品質排行榜。先選一種 memory 形狀，再選工具。

<small>資料查核：2026-08-30 UTC</small>

<table>
  <thead><tr><th scope="col">分類</th><th scope="col">專案／資源</th><th scope="col">編輯評分</th><th scope="col">適合誰</th><th scope="col">能學什麼</th><th scope="col">狀態／限制</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Memory layer</th><td><a href="https://github.com/mem0ai/mem0">Mem0</a></td><td>⭐⭐⭐⭐⭐</td><td>第一次做跨 session memory</td><td>library、server、cloud 與搜尋生命週期</td><td>Apache-2.0；OSS 與 managed 能力分開看</td></tr>
    <tr><td><a href="https://github.com/langchain-ai/langmem">LangMem</a></td><td>⭐⭐⭐⭐</td><td>已使用 LangGraph 的團隊</td><td>hot-path／background memory</td><td>MIT；先理解 LangGraph store</td></tr>
    <tr><td><a href="https://github.com/letta-ai/letta">Letta 專案入口</a></td><td>⭐⭐⭐⭐</td><td>先分清 Letta 的產品範圍</td><td>現行安裝、文件與 source 去向</td><td>landing page；退役 V1 server 只留在 archive branch</td></tr>
    <tr><td><a href="https://github.com/letta-ai/letta-code">Letta Code</a></td><td>⭐⭐⭐⭐</td><td>建立 stateful agent 或 App Server</td><td>agent harness、git-backed MemFS、長期 identity</td><td>現行 source；產品型 agent harness，不是通用 memory DB</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">時間與關係</th><td><a href="https://github.com/getzep/graphiti">Graphiti</a></td><td>⭐⭐⭐⭐⭐</td><td>關係會隨時間改變的應用</td><td>bi-temporal facts、temporal graph</td><td>Apache-2.0；需要圖資料庫與治理</td></tr>
    <tr><td><a href="https://github.com/getzep/zep">Zep examples</a></td><td>⭐⭐⭐</td><td>評估 Zep Cloud 的團隊</td><td>整合與範例入口</td><td>舊 Community Edition 已移到 legacy／deprecated</td></tr>
    <tr><td><a href="https://docs.langchain.com/oss/python/concepts/memory">LangChain Memory overview</a></td><td>⭐⭐⭐⭐⭐</td><td>想先學清楚概念的讀者</td><td>thread state、store、三種 memory 類型</td><td>框架文件；概念可移植，API 需看版本</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">研究與評測</th><td><a href="https://arxiv.org/abs/2309.02427">CoALA</a></td><td>⭐⭐⭐⭐⭐</td><td>研究 agent memory 架構</td><td>working、episodic、semantic、procedural</td><td>分析框架，不是可安裝產品</td></tr>
    <tr><td><a href="https://arxiv.org/abs/2304.03442">Generative Agents</a></td><td>⭐⭐⭐⭐⭐</td><td>研究反思與記憶取回</td><td>recency、importance、relevance</td><td>經典研究，不是 production 標準答案</td></tr>
    <tr><td><a href="https://arxiv.org/abs/2303.11366">Reflexion</a></td><td>⭐⭐⭐⭐</td><td>研究經驗回饋的讀者</td><td>verbal feedback 與下一次嘗試</td><td>reflection 只有持久保存後才成為跨 session memory</td></tr>
    <tr><td><a href="https://github.com/mem0ai/memory-benchmarks">Mem0 Memory Benchmarks</a></td><td>⭐⭐⭐⭐</td><td>要測 memory quality 的開發者</td><td>資料集與可重跑評測入口</td><td>供應商維護；自行加入 isolation／deletion 測試</td></tr>
  </tbody>
</table>

## ✅ 自我檢查

- [ ] 我不會把 Chat History、Context、RAG 與 Memory 當成同一件事。
- [ ] 每筆長期 memory 都有 owner、source、時間與刪除方法。
- [ ] 我能解釋 semantic memory 和 semantic search 的差別。
- [ ] 我測過更新、刪除、過期與跨使用者隔離，不只測寫入和搜尋。
- [ ] 敏感資料預設不寫入，使用者能看見並控制被保存的內容。

← [回到 Stage 6：RAG 與 Memory](../stages/06-memory-rag.md)

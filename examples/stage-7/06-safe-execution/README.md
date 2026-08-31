<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 核心練習：先停下、存好，再安全地繼續

這題不用模型，也不會真的寄信或改資料。程式只把「假動作」寫進本機 JSON ledger，讓你先看懂安全骨架。

對應 [Stage 7 — Agent Production Engineering：Harness、Loop 與 Graph](../../../stages/07-multi-agent-production.md) 核心練習 3。

## 🎯 學習目標

- **Human Approval（人工核准）**：敏感動作先暫停；人可以 approve 或 reject。
- **Checkpoint（檢查點）**：在等待核准時保存工作狀態。
- **Resume（續跑）**：程式重開後，從同一個 task ID 接著做。
- **Recovery（復原）**：狀態損壞或不相符時 fail closed，不猜下一步。
- **Idempotency（冪等）**：同一個 key 重跑很多次，假動作仍只執行一次。

## 先跑不花模型費的測試

在這個資料夾開 PowerShell，直接複製：

```powershell
py -3.11 test.py
```

看到 `8/8 passed`，代表暫停、拒絕、核准、重開續跑、ledger 對帳、損壞狀態與「最多執行一次」都有離線測試。

## 親手走一次 pause → approve → resume

第一步只建立 checkpoint，**不執行假動作**：

```powershell
py -3.11 starter.py start --action "publish draft" --key demo-001
```

你會看到 `status` 是 `waiting_for_approval`。現在關掉終端機也沒關係；狀態在 `.cache/safe-execution-state.json`。

第二步由人決定。核准：

```powershell
py -3.11 starter.py resume --decision approve
```

再次執行同一行，ledger 仍只有一筆 `demo-001`。這就是最小的 idempotency 證據。

要練拒絕，先刪除這個練習自己建立的兩個 `.cache/safe-execution-*.json`，再用新 key start，最後執行：

```powershell
py -3.11 starter.py resume --decision reject
```

## 看懂兩份檔案

| 檔案 | 它保存什麼 | 不應該放什麼 |
|---|---|---|
| checkpoint state | task ID、動作、狀態、核准結果、schema version | API key、密碼、未遮罩的客戶資料 |
| side-effect ledger | 已執行的 idempotency key 與假動作 | 把「寫入成功」當成業務 Outcome 已正確 |

真正的系統通常把 state 放進有權限、備份、保留期限與版本控制的資料庫或 queue。這個 JSON 範例只教責任邊界，不是 production 儲存方案。

## 只改一件事

把 `publish draft` 改成 `send reviewed summary`，並換一個新的 key。先 reject，再確認 ledger 沒增加；重新 start 後 approve，再確認只增加一筆。

## 成功檢查

- [ ] 沒有人核准時，ledger 不會出現假動作。
- [ ] reject 後狀態是 `cancelled`，而且沒有副作用。
- [ ] approve 後狀態是 `completed`。
- [ ] 同一個 key resume 兩次，ledger 仍只有一筆。
- [ ] ledger 與 checkpoint 打架時，程式會修復可證明的完成狀態，或停止請人處理；不會把已執行的動作標成 `cancelled`。
- [ ] JSON 損壞或 key／action 不相符時，程式停止而不是猜測。

## 📚 必讀與學習資源

- ⭐⭐⭐⭐⭐ [OpenAI Agents SDK — Human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/)：tool approval、`RunState` 保存與 resume。
- ⭐⭐⭐⭐⭐ [LangGraph — Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)：pause、approve／reject、checkpoint、resume 與 interrupt 前的冪等副作用。
- ⭐⭐⭐⭐⭐ [LangGraph — Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)：checkpointer、store、thread state 與 fault tolerance 的邊界。
- ⭐⭐⭐⭐⭐ [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)：不要只看 Agent 說了什麼，也要檢查外部 Outcome 與完整 Trajectory。

<small>官方文件與連結查核：2026-08-31 UTC。</small>

<details markdown="1">
<summary>展開：為什麼 ledger 要先寫，checkpoint 才標成完成？</summary>

如果程式在兩次寫入中間斷掉，下次 resume 會先在 ledger 找同一個 idempotency key。找到就不重做假動作，只補上 `completed` checkpoint。這是教學用的最小 write-ahead 想法；真實跨服務交易仍要依資料庫、queue 或供應商 API 的一致性保證設計。

</details>

<details markdown="1">
<summary>展開：常見錯誤與安全邊界</summary>

- 把 approval 寫在工具執行後：已經寄出或付款，再問人就太晚了。
- 只有 retry，沒有 idempotency key：網路 timeout 後重試可能重複副作用。
- checkpoint 沒有 schema／程式版本：隔天部署新程式，舊 state 可能無法安全讀取。
- 把完整 Prompt、token 或客戶資料塞進 state：state 也要做最小化、加密、權限與刪除設計。
- 只看 `status=completed`：仍要用 Outcome Eval 確認外部結果真的正確。

</details>

下一步：回到 [Stage 7 上線四步](../../../stages/07-multi-agent-production.md#-上線四步eval--observability--approvalrecovery--deploy)，再做 Deploy 練習。

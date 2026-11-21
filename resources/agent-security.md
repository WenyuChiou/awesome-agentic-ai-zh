# Agent 安全入門：重要動作先問人

[繁體中文](agent-security.md) | [English](agent-security.en.md) | [简体中文](agent-security.zh-Hans.md)

假設 AI 幫你找三份資料、寫一份摘要。它可以讀資料和寫草稿。要把摘要發出去，先讓你看過並同意。

## 📌 學習目標

- 看出哪些事可以讓 AI 自己做，哪些事要先問人。
- 連接新工具前，查清楚它能碰什麼，以及資料會去哪裡。
- 看測試紀錄，確認拒絕時沒有發布，重跑時沒有多發布一次。

## 🧩 先認識三個核心詞

- **最小權限（Least Privilege）**：只給用得上的鑰匙。寫摘要只要能讀資料，不必給它刪檔權限。
- **人工核准（Human Approval）**：動手前讓人確認。系統先停下來，讓你看清楚要發什麼、發到哪裡。得到同意後才發布。
- **執行紀錄（Execution Log）**：像工作收據，記下系統准許或拒絕了什麼，以及工具有沒有真的執行。用它核對結果，避免把密碼或金鑰寫進紀錄。

## 🧭 跟著同一個例子走

1. [Stage 4：設計工具權限](../stages/04-agent-frameworks.md)。讓 AI 讀指定資料，發布前由程式停下來等你。
2. [Stage 5：接工具前先檢查](../stages/05-claude-code-ecosystem.md)。<strong>MCP（Model Context Protocol）</strong> 像工具的插座，<strong>Skill</strong> 像操作卡。接上別人的工具或放進別人的操作卡前，先查它會用到什麼資料和指令。
3. [Stage 7：動手驗證](../stages/07-multi-agent-production.md)。跑核心練習 3，看到 `8/8 passed` 就代表離線測試通過。想自己數發布紀錄，就跟著[手動步驟](../examples/stage-7/06-safe-execution/README.md)做。兩種方式都不用模型或金鑰。

**關鍵習慣**：網頁、文件和工具傳回的內容都當成資料。要執行什麼，仍由程式依權限和核准結果決定。參考 [Stage 8：提示注入](../stages/08-agent-interfaces.md)。

## 📚 建議閱讀

- [OWASP Agent 應用風險指南](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)：先看工具權限、第三方零件和人工核准的風險。
- [MCP 官方安全指南](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)：接外部工具時，用它查權限、憑證和本機執行的注意事項。

## ✅ 完成檢查

- [ ] 我能指出誰會在發布前停下流程。
- [ ] 我能說出工具可以讀、改與傳出的資料，以及怎麼停用它。
- [ ] 我能從模擬紀錄確認拒絕是 0 筆，核准後重跑仍只有 1 筆。

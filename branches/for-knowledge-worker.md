# 知識工作者延伸路線（For Knowledge Workers）

> **繁體中文** | [简体中文](./for-knowledge-worker.zh-Hans.md) | [English](./for-knowledge-worker.en.md)

<!-- freshness: canonical=branches/for-knowledge-worker.md; verified_on=2026-08-29; scope=apps,connectors,mcp,workflow-automation,permissions,project-status; max_age_days=90 -->

> [← 回主路線](../README.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 後從這裡接續。沒有開發背景也沒關係：先做一次性任務，需要重複時才接工具。

<a id="使用情境辦公場景--ai-怎麼幫"></a>
## 📌 這條路幫你做什麼

把散亂的會議紀錄、Email、文件與待辦，整理成「看得懂、找得到、有人負責」的工作成果。AI 可以幫你先整理；來源、權限與最後決定仍由人負責。

常見工作包括：Email 分流、會議轉行動項目、每週報告、產品需求整理、研究摘要與知識庫整理。

## 🎯 學習目標

完成後，你可以：

1. 從原文找出決定、負責人、期限與證據，不讓 AI 猜空白。
2. 分清一次性聊天、**App／Connector**、**MCP Server** 與工作流自動化。
3. 先檢查資料與權限，再讓工具讀取或修改公司系統。
4. 讓會寄信、改資料或建立任務的流程先停在人工核准關卡。

## 🧩 九個核心詞

- **Source（來源）**：原始 Email、逐字稿、文件或資料列。AI 的答案要能指回它。
- **Action Item（行動項目）**：有人要完成的一件事；至少要寫清楚做什麼、誰負責、何時完成。
- **Knowledge Base（知識庫）**：把可重用資料放在固定地方，讓人和工具之後找得到。
- **Private Data（私人資料）**：公司內部、客戶、員工或個人資料。沒有政策與權限前，不要交給新工具。
- **Human Review（人工審查）**：人要對照 Source，檢查內容、語氣、收件人和缺漏，再決定能不能使用。
- **App／Connector（服務內連接器）**：AI 服務裡連到 Gmail、Drive、Slack 等來源的橋。ChatGPT 已把 Connector 改稱 App；別家仍可能使用 Connector。
- **MCP Server（MCP 伺服器）**：依 MCP 規格把資料或工具交給相容 client 使用的服務。它不是 ChatGPT App，也不代表公司已核准。
- **Workflow Automation（工作流自動化）**：看到 trigger 後，照固定步驟執行 action，例如新表單出現後建立待辦。
- **Approval Gate（人工核准關卡）**：流程先停下來，等人確認後才寄信、貼文、改資料或刪除內容。

**三者不要混在一起：App／Connector 是服務裡的橋；MCP Server 是協定端點；Workflow Automation 是會反覆執行 trigger、條件與 action 的流程。** 同一產品可以同時包含它們，但名稱不能互換。

## 🛠 第一個練習：把會議紀錄變成可核對的行動表

這題只用 fictional（虛構）資料。把下面整段直接複製到你已能使用的 AI 聊天工具，不要放 **Private Data**：

```text
你是會議整理助手。只能使用下方會議紀錄，不要補猜沒有寫出的名字或日期。

請輸出 Markdown 表格，欄位固定為：
Decision | Action Item | Owner | Due date | Source sentence | Needs confirmation

規則：
1. 每一列都要抄一小段 Source sentence，讓我能回頭核對。
2. Owner 或 Due date 沒寫清楚時，填「未知」，並在 Needs confirmation 填「是」。
3. 不要寄出、貼到群組或寫回任何系統；只產生草稿。
4. 最後加上 Human Review 清單：來源、負責人、期限、敏感資料、收件人。

fictional meeting note：
「團隊決定週五先發布說明頁。小林會整理常見問題，但紀錄沒有寫期限。
客服主管要在 9 月 3 日前確認回覆範本。是否寄信給全部客戶，會後再決定。」
```

完成後，逐句對照 `Source sentence`。如果 AI 把「小林的期限」或「寄信決定」補出來，就退回修改；這一步就是 **Human Review**。

<a id="層級建議"></a>
## 📚 先選一個入口

| 你的需求 | 先用什麼 | 何時再升級 |
|---|---|---|
| 偶爾整理一份公開或已核准的文字 | **一次性聊天** | 同一件事開始反覆做時 |
| 要從公司 Gmail、Drive、Slack 或 Microsoft 365 找來源 | 組織核准的 **App／Connector** | 現成連接器做不到，且管理員同意自訂連線時 |
| 每次有新 Email／表單就要跑相同步驟 | **Workflow Automation** | 先用測試資料跑通，再加入 Approval Gate |

不要因為看見 MCP 就先裝 MCP。先問：「現有服務內的 App／Connector 能不能安全完成？」只有需要自訂工具或跨 client 重用時，才往 [Stage 5.2 — MCP 基礎](../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎)前進。

<a id="閱讀"></a>
## 📖 必修閱讀

1. [OpenAI — Apps in ChatGPT](https://help.openai.com/en/articles/11487775-connectors-in)：認識 App 能搜尋、同步與執行哪些動作，以及方案、地區與管理員限制。
2. [Anthropic — Skills、Connectors 與 Plugins 統一目錄](https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory)：先分清三種東西，不把安裝視為安全核准。
3. [Google — 工作／學校帳號的 Gemini Connected Apps](https://support.google.com/gemini/answer/14959807?co=GENIE.Platform%3DDesktop&hl=en)：確認管理員、帳號與 Source 限制，並核對可能過時的回答。
4. [Microsoft — Understand Copilot connectors](https://support.microsoft.com/en-us/microsoft-365-copilot/understand-copilot-connectors)：確認 connector 只會看到使用者原本有權限的內容。
5. [Model Context Protocol — 官方 MCP Registry](https://modelcontextprotocol.io/registry/about)：Registry 目前是 Preview；metadata 與 namespace 驗證不是程式碼安全審查。
6. [Zapier — Zap workflow quick start](https://help.zapier.com/hc/en-us/articles/22234847450893-Zap-workflows-quick-start-guide)：用 trigger、action、測試與發布理解自動化的基本形狀。

<a id="精選-projects"></a>
## ⭐ 精選工具、專案與官方入口

星星是本專案的教學適配評分，不是 GitHub stars。雲端服務先問管理員；自架工具也要自行處理更新、備份、權限與資料流。

<small>資料查核：2026-08-29 UTC</small>

<a id="工作流工具"></a>
<strong>工作流工具：</strong>只有重複工作才需要；第一版先停在草稿或 Approval Gate。

<a id="知識工作者-skills"></a>
<strong>知識工作者 Skills：</strong>Skill 是可重用做法，不是自動取得公司系統權限。

<a id="知識管理--個人-ai"></a>
<strong>知識管理／個人 AI：</strong>自架不等於資料一定留在本機，還要看模型供應商和 connector 設定。

<a id="對知識工作者有用的-mcp-server"></a>
<strong>MCP Server：</strong>先從官方 Registry 看來源，再檢查程式碼、權限、憑證與會執行的 action。

<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="資源表（分類、用途與限制）">
<table>
<thead><tr><th scope="col">類型</th><th scope="col">資源、用途與限制</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">AI 工作空間與組織內 App</th><td><p data-field="entry"><strong><a href="https://help.openai.com/en/articles/11487775-connectors-in">ChatGPT Apps</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">在 ChatGPT 內搜尋來源或執行已允許的動作</p><p data-field="status">商業；商業雲端服務</p><p data-field="limits">功能依方案、地區與管理員而異；外部動作保留人工確認</p></td></tr>
<tr><td><p data-field="entry"><strong><a href="https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory">Claude directory</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">尋找 Skills、Connectors 與 Plugins</p><p data-field="status">商業；商業雲端服務</p><p data-field="limits">三者用途不同；組織資料先由管理員核准</p></td></tr>
<tr><td><p data-field="entry"><strong><a href="https://support.google.com/gemini/answer/14959807?co=GENIE.Platform%3DDesktop&hl=en">Gemini Connected Apps</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">在 Gemini 使用 Gmail、Drive、Calendar 等工作來源</p><p data-field="status">商業；商業雲端服務</p><p data-field="limits">可用性依帳號與管理員；回答仍要回到來源核對</p></td></tr>
<tr><td><p data-field="entry"><strong><a href="https://support.microsoft.com/en-us/microsoft-365-copilot/understand-copilot-connectors">Microsoft 365 Copilot connectors</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">搜尋 Microsoft 365 與組織核准的外部內容</p><p data-field="status">商業；商業雲端服務</p><p data-field="limits">只應看到原本有權限的內容；需授權與管理員設定</p></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">工作流自動化</th><td><p data-field="entry"><strong><a href="https://github.com/n8n-io/n8n">n8n</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">自架或雲端串接多個服務與 AI 步驟</p><p data-field="status">活躍；Sustainable Use License</p><p data-field="limits">不是一般 MIT；自架安全、更新、備份與憑證由你負責</p></td></tr>
<tr><td><p data-field="entry"><strong><a href="https://academy.make.com/courses/FoundationC01?pc=workflow">Make</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">用視覺化 scenario 串接雲端服務</p><p data-field="status">商業；商業雲端服務</p><p data-field="limits">先用測試資料；執行量、錯誤重跑與費用都要監看</p></td></tr>
<tr><td><p data-field="entry"><strong><a href="https://learn.microsoft.com/en-us/training/powerplatform/power-automate">Power Automate</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">在 Microsoft 生態建立 trigger 與 action</p><p data-field="status">商業；商業雲端服務</p><p data-field="limits">方案、connector 與資料政策由組織管理員控制</p></td></tr>
<tr><td><p data-field="entry"><strong><a href="https://help.zapier.com/hc/en-us/articles/22234847450893-Zap-workflows-quick-start-guide">Zapier</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">快速建立雲端 App 間的重複流程</p><p data-field="status">商業；商業雲端服務</p><p data-field="limits">發布前逐步測試；寫回 trigger 來源可能造成無限迴圈</p></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">視覺化 AI builder</th><td><p data-field="entry"><strong><a href="https://github.com/langflow-ai/langflow">Langflow</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">把 AI、資料與工具流程畫成節點</p><p data-field="status">活躍；MIT</p><p data-field="limits">Demo 能跑不等於 production 安全；仍要做 auth、secret 與監控</p></td></tr>
<tr><td><p data-field="entry"><strong><a href="https://github.com/langgenius/dify">Dify</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">用介面建立 AI workflow、知識庫與應用</p><p data-field="status">活躍；修改版 Apache-2.0</p><p data-field="limits">多租戶與移除品牌等情境有額外商用條件</p></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="3">知識工作空間</th><td><p data-field="entry"><strong><a href="https://github.com/khoj-ai/khoj">Khoj</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">自架個人知識助理與文件問答</p><p data-field="status">活躍；AGPL-3.0</p><p data-field="limits">先確認 AGPL 與資料設定；自架後仍要管理模型與備份</p></td></tr>
<tr><td><p data-field="entry"><strong><a href="https://github.com/lobehub/lobehub">LobeHub</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">部署聊天、知識庫與團隊 AI workspace</p><p data-field="status">活躍；LobeHub Community License</p><p data-field="limits">開發並散布衍生作品前要確認商業授權條件</p></td></tr>
<tr><td><p data-field="entry"><strong><a href="https://github.com/Mintplex-Labs/anything-llm">AnythingLLM</a></strong> <span data-field="rating">⭐⭐⭐⭐⭐</span></p><p data-field="use">自架文件問答、workspace 與 agent</p><p data-field="status">活躍；MIT</p><p data-field="limits">資料是否外送仍取決於模型供應商、embedder 與 connector 設定</p></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Skill 與協定入口</th><td><p data-field="entry"><strong><a href="https://github.com/obra/superpowers">superpowers</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">把腦力激盪、規劃與檢查做成可重用 Skill</p><p data-field="status">活躍；MIT</p><p data-field="limits">範例偏開發流程；它不是公司的 Approval Gate，使用前要改成你的規則</p></td></tr>
<tr><td><p data-field="entry"><strong><a href="https://modelcontextprotocol.io/registry/about">官方 MCP Registry</a></strong> <span data-field="rating">⭐⭐⭐⭐</span></p><p data-field="use">查公開 MCP Server 的標準化 metadata</p><p data-field="status">Preview；官方 metadata 服務</p><p data-field="limits">驗證 namespace 不等於安全；它不是安全審查或推薦榜</p></td></tr>
</tbody>
</table>
</div>

<a id="可以建的流程按使用頻率"></a>
<details markdown="1">
<summary>🧪 展開：進階辦公流程與產品經理用法</summary>

| 工作 | 安全的第一版 | 之後才自動化 |
|---|---|---|
| Email 分流 | 匯出幾封已去識別的測試信，只產生分類與回信草稿 | 管理員核准來源後讀取 inbox；寄出前保留 Approval Gate |
| 會議 → Action Item | 使用逐字稿產生可回查 Source sentence 的表格 | 寫入 task 系統前讓主持人確認 Owner 與 Due date |
| Weekly report | 人工提供已核准指標，AI 只整理差異與待辦 | 固定抓資料後仍保留來源連結與發送前審查 |
| 產品需求 | 把虛構 feedback 分成問題、證據、假設與下一步 | 連接工單系統前限制專案、欄位與可執行 action |
| Knowledge Base | 先對少量文件提出分類草稿 | 批次改標籤前先備份，並抽樣核對錯誤分類 |

</details>

<details markdown="1">
<summary>🔐 展開：帳號、資料、權限與費用檢查</summary>

- 先問組織是否核准工具、帳號、地區與資料用途。
- 只開工作需要的最小權限；讀取和寫入分開核准。
- Secret 放在工具的 credential store 或環境變數，不貼進 prompt、文件或截圖。
- 用虛構或去識別資料測試；高風險 action 保留 Approval Gate。
- 查看方案、執行次數、模型與儲存費用；設定預算提醒。
- 不再使用時中止 workflow、撤銷連線並刪除不需要的測試資料。

</details>

<details markdown="1">
<summary>🧯 展開：替代方案與排錯</summary>

- 找不到資料：先確認自己能否直接打開 Source，再查帳號、日期範圍、同步與管理員設定。
- 重複建立任務：檢查 trigger 是否會被自己的 action 再次觸發，加入唯一 ID 或去重條件。
- AI 補猜 Owner／Due date：要求每列附 Source sentence；缺資料就填 Needs confirmation。
- 不確定要不要 MCP：先用服務內 App／Connector；只有現成橋接做不到時再評估 MCP Server。
- 自架太重：先使用組織已核准的雲端服務；自架不是隱私與安全的捷徑。

</details>

## ✅ 完成檢查與下一站

- [ ] 我能從 fictional 會議紀錄做出 Decision／Action Item 表，並逐列核對 Source sentence。
- [ ] 我不會把 App／Connector、MCP Server 與 Workflow Automation 當成同一件事。
- [ ] 我知道 Private Data 先看政策與權限；會寫入外部系統的 action 要有 Approval Gate。
- [ ] 我已選一個入口，不會一次安裝所有工具。

接下來：要做自訂連線，回到 [Stage 5.2 — MCP](../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎)；要做長時間流程，前往 [Stage 7 — Loop／Graph Engineering](../stages/07-multi-agent-production.md)；要自己寫或審查程式，走[開發者路線](./for-developer.md)。

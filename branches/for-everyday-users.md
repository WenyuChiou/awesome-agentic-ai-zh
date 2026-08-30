# 日常使用者延伸路線（For Everyday Users）

> **繁體中文** | [简体中文](./for-everyday-users.zh-Hans.md) | [English](./for-everyday-users.en.md)

> [← 回主路線](../README.md) · 你不必先學會寫程式，也不必走完整條主幹。

<!-- freshness: canonical=branches/for-everyday-users.md; verified_on=2026-08-29; scope=chat-apps,connectors,cli-agents,local-runtimes,privacy,project-status; max_age_days=90 -->

<a id="使用情境生活場景--ai-怎麼幫"></a>
## 📌 這條路幫你做什麼

這條路教你把 AI 當成「先幫忙寫草稿的助手」。你先給它資料和要求，它先做一版；最後仍由你對照原文、修正並決定要不要使用。

你可以直接從第一個練習開始。不要先放真實姓名、密碼、病歷、合約或公司機密。

## 🎯 學習目標

完成這一頁後，你可以：

1. 把要做的事、可用資料和輸出格式說清楚。
2. 分清聊天介面、**App／Connector**、**CLI Agent** 與本地模型執行環境。
3. 在連接帳號、開放檔案或執行指令前先看權限。
4. 對照 **Source** 檢查 AI 草稿，不把流暢文字當成正確答案。

## 🧩 九個核心詞

- **Prompt（提示）**：你交給 AI 的要求。像寫一張工作小紙條，要說要做什麼、可以用什麼資料、結果長什麼樣。
- **Source（來源）**：你要 AI 依照的原文、圖片或資料。最後要回來對照它，不能只相信 AI 的記憶。
- **Private Data（私人資料）**：不該隨便交給別人的資料，例如密碼、身分證號、未公開公司文件或他人的個資。
- **Hallucination（幻覺）**：AI 不知道答案時，仍可能寫出一段很像真的內容。句子好看不代表事實存在。
- **Human Review（人工審查）**：由人把草稿和 Source 一項一項比對，修正後才決定是否使用。
- **App／Connector（服務連接器）**：聊天服務通往 Gmail、Drive 或其他服務的一扇門。它能做什麼，取決於產品和你給的權限。
- **CLI Agent（命令列 Agent）**：在終端機裡工作的助手。它可能讀寫檔案或執行指令，所以動手前要先看計畫與 diff。
- **Local LLM／Runtime（本地模型／執行環境）**：讓模型在自己的電腦上執行的軟體。Runtime 負責跑模型，不等於聊天 App，也不等於 CLI Agent。
- **Approval Gate（人工核准關卡）**：真正寄信、改檔或執行高影響動作前，先停下來讓人確認。

## 🛠 第一個練習：把虛構訊息變成可核對的提醒

這題只用**虛構**資料。把下面整段直接貼到你正在使用的聊天工具：

```text
來源訊息：
「小安說星期五前會把海報草稿交給小美。活動日期是 9 月 12 日。訊息沒有寫交付時間。」

請幫我寫一段簡短提醒。只能使用來源訊息裡的事實，不要猜。
請輸出：
1. Draft
2. Facts copied
3. Needs confirmation

不要替我傳送訊息。
```

完成後，自己做三個檢查：

1. `Facts copied` 能不能逐句在 Source 找到？
2. 沒有寫出的交付時間，有沒有放進 `Needs confirmation`？
3. 工具有沒有只產生 Draft，而沒有自行傳送？

<a id="起步你應該從哪一層進來"></a>
<a id="給日常使用者的層級建議"></a>
## 🚪 按工作選四扇門

**這四扇門不是等級。需要哪一扇才開哪一扇。** 多數單次任務只要第一扇；不是工具越多，結果就越好。

<table>
  <thead><tr><th>入口</th><th>五歲也懂的說法</th><th>適合什麼</th><th>動手前先做什麼</th></tr></thead>
  <tbody>
    <tr><td><strong>Chat surface</strong></td><td>打開一個對話框，請它先寫草稿</td><td>寫信、解釋文章、整理公開資料</td><td>移除 Private Data；準備可核對的 Source</td></tr>
    <tr><td><strong>App／Connector</strong></td><td>幫聊天工具開一扇通往其他服務的門</td><td>搜尋已授權的郵件、檔案或行事曆</td><td>看清讀取與寫入權限；寫入動作保留人工確認</td></tr>
  </tbody>
</table>

<a id="tier-2--cli-agent願意學命令列的進階使用者"></a>
<table>
  <thead><tr><th>入口</th><th>五歲也懂的說法</th><th>適合什麼</th><th>動手前先做什麼</th></tr></thead>
  <tbody>
    <tr><td><strong>CLI Agent</strong></td><td>在終端機裡工作的助手</td><td>重複整理檔案或執行多步驟任務</td><td>限定資料夾，先看 preview／dry-run、command 與 diff，再批准</td></tr>
    <tr><td><strong>Local LLM／Runtime</strong></td><td>模型在自己的電腦裡跑</td><td>離線實驗，或不想把指定資料交給雲端模型</td><td>確認選的是 local model；cloud model、web search 或雲端功能仍會連網</td></tr>
  </tbody>
</table>

如果你只想聊天，不需要安裝 CLI Agent 或本地 Runtime。想學命令列時再去 [Track A 第一站](../tracks/cli/A1-cli-intro.md)；想了解模型時再去 [Stage 1](../stages/01-llm-basics.md)。

<a id="必修閱讀"></a>
## 📖 必修閱讀

先讀這六個短入口；它們分別回答「怎麼問、能接什麼、資料會去哪裡」：

1. [OpenAI — Prompt engineering best practices for ChatGPT](https://help.openai.com/en/articles/10032626-how-do-i-prompt-chatgpt-effectively)：學會把要求與 context 說清楚。
2. [Anthropic — Get started with Claude](https://support.claude.com/en/articles/8114491-get-started-with-claude)：用一般對話方式開始，再逐步補充限制。
3. [OpenAI — Apps in ChatGPT](https://help.openai.com/en/articles/11487775-connectors-in)：Apps 的能力會因方案、地區、workspace 與管理員設定而不同。
4. [Anthropic — When to use desktop and web connectors](https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors)：分清 remote connector 與本機 desktop extension。
5. [Google — Gemini Apps Privacy Hub](https://support.google.com/gemini/answer/13594961?hl=en)：連接資料前先看 activity、人工審查與第三方政策。
6. [Ollama — FAQ](https://docs.ollama.com/faq)：分清本機執行、cloud model、web search 與 `local-only` 設定。

想系統學 Prompt、zero-shot、one-shot、few-shot 與查證方法，再進 [Stage 2 — Prompt Engineering](../stages/02-prompt-engineering.md)。

<a id="-精選-projects"></a>
## ⭐ 精選 Projects 與學習資源

星等是本專案依「初學者價值、文件品質與安全邊界」給的編輯評分，不是 GitHub stars。狀態與限制查核於 `2026-08-29 UTC`。

<table>
  <thead><tr><th scope="col">分類</th><th scope="col">入口／專案</th><th scope="col">它是什麼</th><th scope="col">適合做什麼</th><th scope="col">狀態／授權</th><th scope="col">先知道的限制</th><th scope="col">評分</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">聊天介面</th><td><a href="https://claude.ai">Claude</a></td><td>雲端 Chat surface</td><td>閱讀、寫作與反覆討論</td><td>正式可用；商業雲端服務</td><td>功能依方案與地區；重要內容仍要對照 Source</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://chatgpt.com">ChatGPT</a></td><td>雲端 Chat surface</td><td>一般問答、語音與多種工作入口</td><td>正式可用；商業雲端服務</td><td>仍會出錯；高影響結果要 Human Review</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://gemini.google.com">Gemini</a></td><td>Google 的雲端 Chat surface</td><td>問答與符合資格的 Google 服務連接</td><td>正式可用；商業雲端服務</td><td>先看 activity 與人工審查設定，不放機密資料</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://perplexity.ai">Perplexity</a></td><td>帶來源入口的雲端搜尋助手</td><td>找候選來源與建立查證起點</td><td>正式可用；商業雲端服務</td><td>引用不等於內容正確；要逐一打開來源</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">官方入門與安全指南</th><td><a href="https://help.openai.com/en/articles/10032626-how-do-i-prompt-chatgpt-effectively">OpenAI Prompt Guide</a></td><td>ChatGPT 官方指引</td><td>學清楚、具體與逐步改寫 Prompt</td><td>現行；官方指引</td><td>好 Prompt 不能保證正確，仍要查證</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://support.claude.com/en/articles/8114491-get-started-with-claude">Claude Get Started</a></td><td>Claude 官方入門</td><td>第一次聊天與基本操作</td><td>現行；官方指引</td><td>方案有使用限制；不要假設所有功能都可用</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://help.openai.com/en/articles/11487775-connectors-in">Apps in ChatGPT</a></td><td>App／Connector 官方說明</td><td>了解搜尋、同步與外部 action</td><td>商業；商業雲端服務</td><td>能力與權限不同；高影響 action 保留人工確認</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://support.google.com/gemini/answer/13594961?hl=en">Gemini Privacy Hub</a></td><td>Gemini 官方隱私指引</td><td>連接 Google 或第三方資料前檢查設定</td><td>現行；官方隱私指引</td><td>可能處理敏感內容；不要連接不願交給 reviewer 的機密資料</td><td>⭐⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">CLI Agent</th><td><a href="https://github.com/anthropics/claude-code">Claude Code</a></td><td>Anthropic CLI Agent</td><td>在指定工作區讀檔、改檔與執行任務</td><td>活躍；商業服務；repo 未標示標準開源授權</td><td>先設定 permission，批准前先看 command／diff</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/openai/codex">Codex</a></td><td>OpenAI coding agent</td><td>app／CLI／IDE／cloud 工作</td><td>活躍；repo 程式碼為 Apache-2.0，app／cloud 依服務條款</td><td>用 approval 限制寫檔、命令與外部 action</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/anomalyco/opencode">OpenCode</a></td><td>可連多種 provider 的 coding agent／harness</td><td>在終端機或 desktop 使用模型做多步驟任務</td><td>活躍；MIT</td><td>provider 仍需帳號／API key；用 permission 與 AGENTS.md 限定範圍</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/google-gemini/gemini-cli">Gemini CLI</a></td><td>Google CLI Agent</td><td>在終端機使用 Gemini 與工具</td><td>活躍；Apache-2.0</td><td>修改前看 diff／command；sandbox 只能降低風險</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">Local LLM Runtime</th><td><a href="https://github.com/ollama/ollama">Ollama</a></td><td>本地模型執行環境</td><td>下載並在自己的電腦執行模型</td><td>活躍；MIT</td><td>確認使用 local model；cloud model 與 web search 不是本機推論</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://lmstudio.ai/">LM Studio</a></td><td>圖形化本地模型執行環境</td><td>用桌面介面載入已下載模型</td><td>商業；商業桌面應用程式</td><td>本地功能可離線；cloud models、搜尋等雲端功能仍會連網</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="1">Prompt 素材</th><td><a href="https://github.com/f/prompts.chat">prompts.chat</a></td><td>社群 Prompt 範例庫</td><td>找句型，再改成自己的任務</td><td>活躍；MIT／CC0</td><td>範例品質不一；不要直接貼 Private Data</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
</table>

<details markdown="1">
<summary>🔐 帳號、資料、權限與費用</summary>

- App／Connector 是否出現，會受**方案、地區、workspace**、裝置與管理員設定影響。沒有看到功能，不代表你操作錯了。
- 連接前先問：它會讀什麼？會把什麼送給哪個服務？能不能寫回？怎麼撤銷？
- 搜尋和草擬通常是低影響動作；寄信、改行事曆、刪檔或購買是寫入動作，必須保留 Approval Gate 與人工確認。
- 雲端產品的免費額度、訂閱與 API 費用會變；操作前直接看產品目前顯示的方案，不在教材保存固定價格。
- 不確定能不能上傳時，先不要上傳。公開可讀也不等於你有權把別人的內容交給第三方服務處理。

</details>

<details markdown="1">
<summary>🧪 CLI Agent 與本地模型進階步驟</summary>

CLI Agent 的安全起手式：

1. 在測試資料夾放幾個可還原的虛構檔案。
2. 先要求 read-only plan 或 preview／dry-run。
3. 把可讀寫範圍限制在那個資料夾。
4. 看清 command 與 diff，再批准小步驟。
5. 執行後人工檢查；不要一開始就讓它寄信、刪檔、付款、push 或 deploy。

官方邊界：

- [Gemini CLI tools](https://geminicli.com/docs/reference/tools/) 會在修改工具前顯示 action；[sandbox 文件](https://geminicli.com/docs/cli/sandbox/) 也提醒 sandbox 不是零風險保證。
- [OpenCode permissions](https://opencode.ai/docs/agents/) 可對 edit、bash 與外部資料夾設定 ask／allow／deny；[provider 文件](https://opencode.ai/docs/providers/) 顯示模型連線仍需要對應帳號、OAuth、API key 或環境設定。
- Ollama 可以啟用 [cloud models](https://docs.ollama.com/cloud)。只要純本機模式時，依 FAQ 設定 `disable_ollama_cloud` 或 `OLLAMA_NO_CLOUD=1`。
- LM Studio 的[離線說明](https://lmstudio.ai/docs/app/offline)指出，已下載模型、chat、文件與 local server 可以離線使用；[隱私說明](https://lmstudio.ai/app-privacy)區分本地處理與 cloud models／web search。

</details>

<a id="可以建的流程按使用頻率"></a>
<details markdown="1">
<summary>🧰 更多流程、替代方案與疑難排解</summary>

可以慢慢加入的低風險流程：

- **語言練習**：請 AI 扮演對話伙伴；每次只糾正兩個錯誤，最後由你核對教材。
- **週記草稿**：只用你願意放進工具的筆記；先列事實，再寫摘要。
- **公開文章摘要**：附上原文，要求每個重點指出 Source 段落；自己打開原文檢查。
- **虛構檔案整理**：先在測試資料夾 preview 新檔名，人工批准後才改名。

常見問題：

- 回答猜了不存在的資料：縮短任務，明寫「不知道就放進 Needs confirmation」。
- Connector 找不到資料：先檢查原服務權限、方案、workspace 管理員與支援 surface。
- 本地模型很慢：先換較小模型；不要把「跑得動」誤當成「回答一定正確」。
- 不知道選哪個入口：先用 Chat surface 完成第一題；真的需要讀外部服務、改檔或離線時再開其他門。

</details>

<a id="社群備註"></a>
## ✅ 完成檢查與下一站

- [ ] 我能說出 Chat surface、App／Connector、CLI Agent 與 Local LLM／Runtime 的差別。
- [ ] 我知道 AI 會產生 Hallucination，會回到 Source 做 Human Review。
- [ ] 我不會把 Private Data 直接貼進不清楚資料政策的服務。
- [ ] 寄出、改檔、執行命令或其他高影響動作前，我會保留 Approval Gate。

下一站依你的需要選：

- 想把 Prompt 寫得更清楚：進 [Stage 2](../stages/02-prompt-engineering.md)。
- 想安全使用 CLI Agent：進 [Track A1](../tracks/cli/A1-cli-intro.md)。
- 想分清 App、Connector、MCP 與自動化：進 [知識工作者路線](./for-knowledge-worker.md)。
- 想協助改善這條路：看 [CONTRIBUTING.md](../CONTRIBUTING.md)。

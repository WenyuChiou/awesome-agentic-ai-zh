# 相關資源

> **繁體中文** | [简体中文](./RESOURCES.zh-Hans.md) | [English](./RESOURCES.en.md)

> [← 回主路線 README](README.md)

## 📌 先選你現在要做的事

不用把整份清單讀完。先選一件現在要做的事：

| 我現在想要…… | 從這裡開始 | 編輯評分 |
|---|---|---|
| 從頭學 AI Agent | [Stage 0](stages/00-foundations.md) | ⭐⭐⭐⭐⭐ |
| 分清模型怎麼學會與怎麼被使用 | [模型訓練與調整指南](resources/model-training-guide.md) | ⭐⭐⭐⭐⭐ |
| 查一個不懂的詞 | [Glossary](resources/glossary.md) | ⭐⭐⭐⭐ |
| 選一個 CLI Agent | [CLI Agents Guide](resources/cli-agents-guide.md) | ⭐⭐⭐⭐⭐ |
| 把 Agent 接到外部工具 | [MCP／Skills Catalog](resources/mcp-skills-catalog.md) | ⭐⭐⭐⭐⭐ |
| 跟著步驟做一個小作品 | [Cookbook](resources/cookbook.md) | ⭐⭐⭐⭐⭐ |

<a id="三個核心用語mcp--skills--plugins"></a>
## 🧩 三個核心詞：MCP、Skill、Plugin

**MCP（Model Context Protocol）**：讓 AI 應用用共同方法連接外部資料與工具的開放協定。像一種共用插座；連上後能做什麼，仍由 server、帳號權限和使用者核准決定。

**Skill**：一包可重複使用的做事方法，通常包含指令，也可以附腳本、範本和參考資料。不同產品放置與載入 Skill 的方式可能不同。

**Plugin**：某個 host 提供的安裝包。它可以一起帶入 Skill、指令、hook 或 MCP 設定；Plugin 不是 MCP 規格的一部分，各產品的格式也不一定相同。

想親手做一次，前往 [Stage 5](stages/05-claude-code-ecosystem.md)。想先分清 App／Connector、CLI Agent 與 MCP Server，查看 [CLI Agents Guide](resources/cli-agents-guide.md)。

## 📚 五個安全起點

先從官方入口或完整教材開始，再挑社群專案。星等是本專案的編輯評分，不是 GitHub stars。

| 起點 | 先學什麼 | 編輯評分 |
|---|---|---|
| [Official MCP Registry](https://registry.modelcontextprotocol.io/) | 找已發布的 MCP Server；安裝前仍要檢查維護者、權限與來源 | ⭐⭐⭐⭐⭐ |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | 看 MCP 功能怎麼實作；這些是教學用 reference servers，不等於 production 推薦 | ⭐⭐⭐⭐⭐ |
| [anthropics/skills](https://github.com/anthropics/skills) | 看 Agent Skill 的資料夾、指令與資源怎麼組在一起 | ⭐⭐⭐⭐⭐ |
| [github/github-mcp-server](https://github.com/github/github-mcp-server) | 用官方實作認識 OAuth、工具組與 repository 權限 | ⭐⭐⭐⭐⭐ |
| [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) | 用中文教材系統學 Agent 原理與實作 | ⭐⭐⭐⭐⭐ |

> ⚠️ **先少給鑰匙**：MCP Server 可能讀取、建立、傳送或刪除真實資料。先用 read-only、最小權限和測試 workspace；write、send、delete 前保留 **Human Approval（人工核准）**。

<a id="daily-tool-integrations"></a>
<a id="接日常工具常用-mcp-server--skill"></a>
## 🔌 常用整合分類

下面直接顯示精選專案與官方入口。從你需要的分類開始看；更長的補充清單才放在收合選單。

<div class="resource-table-scroll" role="region" tabindex="0" aria-label="精選資源表（可左右捲動）">
<table class="resource-table">
<thead><tr><th scope="col">分類</th><th scope="col">資源</th><th scope="col">能幫你什麼</th><th scope="col">狀態／限制</th><th scope="col">編輯評分</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">筆記／知識庫</th><td><a href="https://developers.notion.com/guides/mcp/overview">Notion MCP</a></td><td>搜尋、建立與更新 Notion 內容</td><td>官方 hosted MCP；需要使用者 OAuth，權限跟著登入者</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/MarkusPfundstein/mcp-obsidian">MarkusPfundstein/mcp-obsidian</a></td><td>透過 Obsidian REST API 讀寫 vault</td><td>社群專案；只授予需要的 vault 與寫入範圍</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://support.google.com/gemininotebook/answer/16164461">Gemini Notebook（舊名 NotebookLM）</a></td><td>用自己的來源做摘要、問答與學習材料</td><td>Google 服務；地區、帳號與功能可用性會變</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/teng-lin/notebooklm-py">teng-lin/notebooklm-py</a></td><td>用 Python／CLI 操作 Gemini Notebook</td><td>非官方介面；Google 改版時可能失效</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="3">辦公文件</th><td><a href="https://github.com/anthropics/skills">anthropics/skills</a></td><td>閱讀 Agent Skills 範例與文件工作流程</td><td>官方範例；各 Claude surface 可用的內建 Skill 不完全相同</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/tfriedel/claude-office-skills">tfriedel/claude-office-skills</a></td><td>補充 Office 文件自動化流程</td><td>社群 Skills；檔案寫入前先備份與核對輸出</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://developers.google.com/workspace/guides/configure-mcp-servers">Google Workspace MCP</a></td><td>連接 Gmail、Drive、Docs、Sheets、Slides、Calendar 與 Chat</td><td>官方 <strong>Developer Preview</strong>；每個產品有獨立 server，使用 OAuth 2.0，並受使用者／組織治理</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">開發協作</th><td><a href="https://github.com/github/github-mcp-server">GitHub MCP Server</a></td><td>查詢與處理 issue、PR 與 repository</td><td>官方 MCP；使用 OAuth 或最小權限 token，高影響寫入前要人工核准</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/">Atlassian Rovo MCP</a></td><td>搜尋或更新 Jira、Confluence 與 Bitbucket 工作</td><td>官方 hosted remote MCP；使用 OAuth 2.1，權限跟著登入者；寫入真實資料前要人工核准</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://linear.app/docs/mcp">Linear MCP</a></td><td>搜尋與更新 Linear issue／project</td><td>官方 hosted remote MCP，使用 Streamable HTTP；另有官方 read-only 選項</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://docs.slack.dev/ai/mcp-overview/">Slack MCP</a></td><td>搜尋 Slack，也能傳訊息與管理 canvas</td><td>官方 MCP；傳送或改動內容前要求人工確認</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">研究工作流</th><td><a href="https://github.com/WenyuChiou/ai-research-skills">WenyuChiou/ai-research-skills</a></td><td>把研究步驟整理成可重用 Skills</td><td>社群專案；只安裝與目前任務有關的 Skill</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/WenyuChiou/research-hub">WenyuChiou/research-hub</a></td><td>串接 Zotero、Obsidian 與研究流程</td><td>社群 workspace；先看資料位置、備份與權限</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/WenyuChiou/zotero-skills">WenyuChiou/zotero-skills</a></td><td>用 Skill 整理 Zotero 資料</td><td>社群 Skill；批次修改前先備份 library</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/WenyuChiou/codex-delegate">WenyuChiou/codex-delegate</a></td><td>把範圍清楚的重複工作交給另一個 Agent</td><td>社群工具；委派前鎖定檔案、驗收與停止條件</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="1">中文生態</th><td><a href="https://github.com/leemysw/feishu-docx">leemysw/feishu-docx</a></td><td>在飛書（Lark）文件與 Markdown 間轉換</td><td>社群工具；先確認文件分享與寫入權限</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
</table>
</div>

<a id="research-workflow"></a>
<a id="研究工作流本-repo-維護者出品"></a>
<a id="topic-awesome-lists"></a>
<a id="同主題的清單型-awesome-lists"></a>
<details markdown="1">
<summary>展開更多清單、課程與設計工具</summary>

- [MCP Registry](https://registry.modelcontextprotocol.io/)：找已發布 Server 的官方 discovery 入口。
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)：依分類瀏覽社群 Server；安裝前自行審查。
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)：Claude Code 社群資源。
- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)：Agent Skills 社群清單。
- [Canva MCP](https://www.canva.dev/docs/mcp/)：官方 remote MCP；功能、方案與權限依帳號而異，不先記固定工具數。
- [課程清單](resources/courses.md)：按學習目標挑課程，不把證書當成學位。
- [Agent paradigms](resources/agent-paradigms.md)：用圖比較常見 Agent 形狀。

</details>

<a id="還有什麼"></a>
## ✅ 下一站

- 不懂名詞：打開 [`resources/glossary.md`](resources/glossary.md)。
- 想直接做：打開 [`resources/cookbook.md`](resources/cookbook.md)。
- 想分清 Pre-training、Post-training 與 Fine-tuning：打開 [`resources/model-training-guide.md`](resources/model-training-guide.md)。
- 想貢獻或翻譯：先看 [`resources/style-guide.md`](resources/style-guide.md) 與 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

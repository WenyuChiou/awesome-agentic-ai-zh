# `resources/` 工具櫃

<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

這裡像一個工具櫃。你卡住時，只拿現在需要的那張說明卡；**不用從第一份讀到最後一份**。

## 🧭 你現在卡在哪裡？

| 你現在想做什麼 | 先打開這一份 |
|---|---|
| 我完全沒寫過 code，不知道怎麼開始 | [`setup-guide.md`](setup-guide.md) |
| 我想照完整學習地圖開始 | [主頁](../README.md) → [Stage 0](../stages/00-foundations.md) |
| 我分不清模型怎麼學會、怎麼被調整、什麼時候只是在產生答案 | [`model-training-guide.md`](model-training-guide.md) |
| 我看到一個詞，但不知道意思 | [查詞卡](glossary.md) |
| 我分不清這四個名字：OpenRouter＝統一模型 API／router；Ollama＝本機模型 runtime；OpenCode／Pi＝coding agent／toolkit | [`cli-agents-guide.md`](cli-agents-guide.md) |
| 我想做出第一個操作卡（Skill）、工具接頭（MCP server）或文件流程 | [實作食譜](cookbook.md) |
| 我寫了工具說明（tool schema），但模型一直選錯工具 | [`schema-design-cheatsheet.md`](schema-design-cheatsheet.md) |
| 我想找能接 Notion、Office、資料庫或瀏覽器的工具 | [`mcp-skills-catalog.md`](mcp-skills-catalog.md) |
| 我想選一門課，或先看證書有沒有用 | [`courses.md`](courses.md) |
| 我想知道 agent 是在終端機、編輯器、雲端或自己的裝置裡工作 | [`agent-paradigms.md`](agent-paradigms.md) |
| 我想直接複製一個小幫手 agent（subagent）派遣範例 | [`subagent-cookbook.md`](subagent-cookbook.md) |
| 我想自己設計、組合或排查小幫手 agent（subagent） | [`subagent-advanced.md`](subagent-advanced.md) |
| 我想替這個專案寫內容或送 PR | [`style-guide.md`](style-guide.md) |

## 🧩 先分清楚五個詞

- **Reference（參考資料）**：卡住時回來查的補充資料，不是另一條要從頭讀完的必修課。
- **Guide（指南）**：帶你沿著一條清楚路線做選擇，告訴你先做什麼、下一步去哪裡。
- **Cookbook（食譜）**：像食譜一樣給你可照著做的完整小範例，目標是先做出成果。
- **Catalog（目錄）**：把很多工具放在同一處，方便搜尋和比較。
- **Glossary（詞典）**：先給短定義，再把你送到講得更完整的章節。

## 📚 全部 12 份參考資料

同一類型已合併在左欄。表格全部保持展開，因為讀者要先看得見有哪些入口。

<table>
<thead><tr><th scope="col">類型</th><th scope="col">檔案</th><th scope="col">最適合什麼時候看</th><th scope="col">它不負責什麼</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">開始與選擇</th><td><a href="setup-guide.md">setup-guide.md</a></td><td>第一次選 Web、Desktop、IDE、CLI 或 API</td><td>不取代每個產品的最新官方安裝頁</td></tr>
<tr><td><a href="glossary.md">glossary.md</a></td><td>30 秒查一個名詞</td><td>不取代完整章節與實作</td></tr>
<tr><td><a href="cli-agents-guide.md">cli-agents-guide.md</a></td><td>分清模型、模型入口（router）、執行環境（runtime）與 coding agent</td><td>不替你自動開權限或選付費方案</td></tr>
<tr><td><a href="courses.md">courses.md</a></td><td>比較課程、練習深度與證書限制</td><td>不保證證書能換到工作</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">動手與排錯</th><td><a href="cookbook.md">cookbook.md</a></td><td>做 Skill、MCP、Office、Gemini Notebook、Zotero 或本機 CLI 工作流</td><td>不把每個主題寫成一本長教材</td></tr>
<tr><td><a href="schema-design-cheatsheet.md">schema-design-cheatsheet.md</a></td><td>工具選錯或參數常常傳錯</td><td>不教完整 MCP server 安裝</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="3">搜尋與定位</th><td><a href="model-training-guide.md">model-training-guide.md</a></td><td>分清 Pre-training、Post-training、Fine-tuning 與 Inference</td><td>不是從零訓練模型的完整課程</td></tr>
<tr><td><a href="mcp-skills-catalog.md">mcp-skills-catalog.md</a></td><td>依工作類型找工具接頭（MCP server）或操作卡（Skill）</td><td>收錄不代表零風險或永遠可用</td></tr>
<tr><td><a href="agent-paradigms.md">agent-paradigms.md</a></td><td>分清 agent 跑在終端機、編輯器、雲端或自己的裝置</td><td>不是產品排行榜</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Subagent 進階</th><td><a href="subagent-cookbook.md">subagent-cookbook.md</a></td><td>先複製一個小幫手 agent 的派遣範例</td><td>不解釋全部設計原理</td></tr>
<tr><td><a href="subagent-advanced.md">subagent-advanced.md</a></td><td>自己設計、組合與排查小幫手 agent</td><td>不適合第一次使用 CLI agent 時先讀</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="1">維護專案</th><td><a href="style-guide.md">style-guide.md</a></td><td>寫 entry、翻譯、表格或送 PR</td><td>不是一般讀者的必修閱讀</td></tr>
</tbody>
</table>

## 🔁 看完要回哪裡？

- 第一次學習：回到 [Stage 0](../stages/00-foundations.md)。
- 想用 CLI 完成工作：回到 [Track A1](../tracks/cli/A1-cli-intro.md)。
- 想自己寫 Agent：回到 [Stage 3](../stages/03-tool-use-and-hello-agent.md)。
- 只想重新選入口：回到 [主頁](../README.md)。

## ✅ 30 秒完成檢查

- [ ] 我知道現在只要打開哪一份資料。
- [ ] 我沒有把 catalog 當成從頭讀到尾的課本。
- [ ] 我看完後，知道要回主線的哪一站。

<details markdown="1">
<summary>為什麼不把 12 份資料合成一本書？</summary>

因為它們解決不同問題。Glossary 是 30 秒查詞，Stage 是幾分鐘建立概念，Cookbook 是照著做出成果，Catalog 則是需要時搜尋工具。全部混成一本書，讀者反而更難找到入口。

想讀章節長度的中文教材，可以接著看 [Hello-Agents](https://github.com/datawhalechina/hello-agents)。這份專案負責幫你找路，不重寫另一套長教材。

</details>

<details markdown="1">
<summary>Maintainer：三語覆蓋與新增 reference 的規則</summary>

上表 12 份資料都有繁中、英文與簡中版本。新增 reference 前要同時符合：

1. 它有一個既有檔案無法取代的工作。
2. 至少三個 stage、track 或 branch 會需要它。
3. 名詞、URL、限制與安全規則能維持三語一致。
4. 如果只服務一個章節，就留在那個章節，不另外開檔。

繁中是主版本：zh-TW 是 canonical。先用官方來源查證；找不到時明寫未知，不要猜。不要保存會一直改變的 GitHub stars、固定總數和行數。

送出修改前，再核對 [MCP／Skills catalog](mcp-skills-catalog.md)、[Cookbook](cookbook.md)、[style guide](style-guide.md) 與 [CONTRIBUTING](../CONTRIBUTING.md)。

</details>

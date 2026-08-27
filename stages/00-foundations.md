# Stage 0 — 基礎準備（Foundations）

> **繁體中文** | [简体中文](./00-foundations.zh-Hans.md) | [English](./00-foundations.en.md)

這一關先檢查：你會不會使用後面一定會用到的四種工具？會就直接跳過。不會也沒關係，照著下面的小練習做一次。

資料查核：2026-08-27 UTC（學習資源與 GitHub 驗證指引）

## 何時可以跳過這個階段

看看下面四件事。你不需要背指令，但要能自己查資料並完成：

- [ ] 用 Python 向 API（給程式取資料的入口）拿公開資料，再從 JSON 裡找出一個值。
- [ ] 用 Git 複製專案（clone）、開工作線（branch）、保存版本（commit），再把版本送到網路上（push）。兩次修改撞在一起時，知道要留下什麼（合併衝突）。
- [ ] 用命令列（在終端機輸入的文字指令）切換資料夾、建立檔案並執行 Python script。
- [ ] 看懂 YAML 與 JSON。它們都是用文字保存資料的格式。

四項都做得到，就直接前往 [Stage 1 — LLM 基礎](01-llm-basics.md)。只要有一項不確定，就完成本頁的主練習；需要時再展開補充內容。

## 📌 學習目標

完成這一關後，你可以：

- 讓 Python 從 API 拿資料，再讀出 JSON 裡需要的部分。
- 從終端機執行程式，並找到程式建立的檔案。
- 用 Git 保存一個版本，需要時可以回到這個版本。
- 認出 YAML、JSON 與 API token（讓程式登入的秘密文字），知道哪些內容不能公開。

## 🛠 動手練習：做一個 GitHub 資料小工具

**成果：**讓 Python 從 GitHub 拿公開資料，把結果顯示在畫面上、寫進檔案，再用 Git 保存。這個主練習不需要帳號、API token 或付費服務。

### 1. 建立程式

建立一個新資料夾，並把下面內容存成 `github_profile.py`：

```python
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

url = "https://api.github.com/users/torvalds"
request = Request(url, headers={"User-Agent": "stage-0-practice"})

with urlopen(request, timeout=10) as response:
    profile = json.load(response)

result = f"{profile['login']} 有 {profile['followers']} 位追蹤者"
print(result)
Path("result.txt").write_text(result + "\n", encoding="utf-8")
```

API 是程式拿資料的入口。JSON 是這次收到的資料格式。

### 2. 執行程式

在終端機進入該資料夾，執行：

```bash
python github_profile.py
```

畫面會顯示帳號與追蹤者數量，資料夾裡也會多出 `result.txt`。追蹤者數量會改變，不需要和別人的畫面一樣。

### 3. 用 Git 保存成果

```bash
git init
git add github_profile.py result.txt
git commit -m "Add GitHub profile checker"
```

Commit 是 Git 保存的一個版本，旁邊會有一句說明。如果 Git 第一次要求姓名或 email，依畫面提示設定後，再執行一次 `git commit`。這些資料是版本的作者標籤，不是密碼。

## ✅ 完成檢查

- [ ] 終端機顯示 GitHub 帳號與追蹤者數量。
- [ ] `result.txt` 有相同的結果。
- [ ] `git log --oneline` 看得到剛才的 commit。
- [ ] 程式與 commit 裡沒有密碼或 API token。

四項都完成，就可以前往 [Stage 1 — LLM 基礎](01-llm-basics.md)。如果卡住，展開下面最接近問題的部分，不必一次讀完。

<details markdown="1">
<summary>⏱️ 展開時間、環境與這一關存在的原因</summary>

**時間**：完全不熟時預留 1–2 週，約 5–15 小時；已經會其中幾項，只補不熟的部分即可。

**環境**：準備仍受支援的 Python 3、Git、文字編輯器與終端機。終端機就是輸入文字指令的視窗。Windows 可使用 PowerShell；macOS 或 Linux 可使用系統終端機。

先確認工具可以執行：

```bash
python --version
git --version
```

後面的 AI agent 教材會直接使用 Python、Git、命令列與設定檔。Stage 0 不會教完所有內容。它只幫你找出還不熟的地方，再告訴你去哪裡補。

</details>

<details markdown="1">
<summary>🧰 展開 Python、Git、命令列與 YAML／JSON 補充練習</summary>

只做你還不熟的項目：

1. **Python**：把主練習網址中的 `torvalds` 換成自己的 GitHub 帳號或其他公開帳號，確認程式仍能讀出 `login` 與 `followers`。
2. **Git**：建立新 branch（不直接改原版本的工作線），修改輸出文字，再做一次 commit。接著把練習放到自己的遠端 Git 專案，並執行 `git push`。
3. **命令列**：建立 `src`、`tests`、`docs` 三個資料夾，從不同路徑執行主練習，並找出 `result.txt` 實際寫到哪裡。
4. **JSON**：把 API 回應存成檔案，找出 `name`、`public_repos` 與 `followers` 三個欄位。
5. **YAML**：建立一個含有 `username` 與 `output_file` 的小設定檔，練習縮排、字串與布林值。YAML 對空格很敏感，不要使用 Tab 縮排。

遇到錯誤時，先讀最後一行錯誤訊息，再確認目前資料夾、檔名與 Python 版本。一次只改一件事，才知道哪個修改有效。

</details>

<details markdown="1">
<summary>🔐 展開選修：安全地體驗 GitHub API 驗證</summary>

主練習不需要 token。Token 是一串讓 GitHub 認出你的秘密文字。只有想理解「登入後的 API」時才做這一題。

1. 依 [GitHub 官方說明](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) 建立 fine-grained personal access token。Fine-grained 表示你可以只開需要的權限。
2. 使用最短的有效期限，不加入額外權限。`GET /user` 對 fine-grained token 不要求任何權限。
3. 把 token 放進環境變數 `GITHUB_TOKEN`。環境變數是電腦暫時保管資料、讓程式讀取的位置。不要把 token 寫進 Python、Markdown、截圖、終端機歷史或 Git commit。
4. 呼叫 `https://api.github.com/user` 兩次。第一次不帶 token，應看到 `401`，意思是尚未登入。第二次帶 token，應看到 `200`，意思是 GitHub 接受了請求。
5. 練習結束後，回到 GitHub 設定頁撤銷 token，並清除環境變數。

Bash 可以這樣避免把輸入顯示在畫面上：

```bash
read -s GITHUB_TOKEN && export GITHUB_TOKEN
curl -sS -o /dev/null -w "No token: %{http_code}\n" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user
curl -sS -o /dev/null -w "With token: %{http_code}\n" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user
unset GITHUB_TOKEN
```

PowerShell 7.1 以上可以這樣做：

```powershell
$env:GITHUB_TOKEN = Read-Host -MaskInput "Paste token"
$withoutToken = Invoke-WebRequest -Uri https://api.github.com/user `
  -Headers @{ Accept = "application/vnd.github+json" } `
  -SkipHttpErrorCheck
$withToken = Invoke-WebRequest -Uri https://api.github.com/user -Headers @{
  Authorization = "Bearer $env:GITHUB_TOKEN"
  Accept = "application/vnd.github+json"
} -SkipHttpErrorCheck
"No token: $($withoutToken.StatusCode)"
"With token: $($withToken.StatusCode)"
Remove-Item Env:GITHUB_TOKEN
```

Token 就像程式使用的臨時鑰匙。拿到它的人可能以你的身分操作，所以權限越少、期限越短越安全。

</details>

<details markdown="1">
<summary>🗺️ 展開名詞與 Agent 全景補充</summary>

- **CLI（命令列介面）**：在終端機輸入文字指令來操作電腦。
- **API（應用程式介面）**：讓兩個程式用固定規則交換資料的入口。
- **JSON／YAML**：用文字保存結構化資料的兩種格式；JSON 常見於 API，YAML 常見於設定檔。
- **Git**：記錄檔案版本的工具；commit 是一次有說明的版本快照。

看到其他不懂的詞，先查 [術語表](../resources/glossary.md)。想知道 agent 為什麼可能出現在終端機、聊天軟體或裝置上，再看 [Agent 全景地圖](../resources/agent-paradigms.md)。這兩份都不是開始主練習前的必讀內容。

</details>

## 🎯 精選學習資源

需要補某一項能力時再找對應入口；不用把 18 個資源全部讀完。

<details markdown="1">
<summary>📚 展開依主題分組的 18 個學習資源</summary>

<table>
  <thead><tr><th scope="col">主題</th><th scope="col">資源</th><th scope="col">適合誰</th><th scope="col">為什麼推薦／備註</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="5">Python</th><td><a href="https://github.com/ehmatthes/pcc_3e">Python Crash Course</a></td><td>從零學 Python</td><td>書本搭配練習；程式碼免費，書本需購買。</td></tr>
    <tr><td><a href="https://realpython.com/">Real Python</a></td><td>已有基礎，想查單一主題</td><td>文章按主題拆分，適合遇到問題時查閱。</td></tr>
    <tr><td><a href="https://www.youtube.com/c/Coreyms">Corey Schafer YouTube</a></td><td>喜歡英文影片</td><td>從基礎語法逐步帶到實際應用。</td></tr>
    <tr><td><a href="https://www.boot.dev/">Boot.dev</a></td><td>想要互動式練習</td><td>部分內容免費；完整後端路線需付費。</td></tr>
    <tr><td><a href="https://www.runoob.com/python3/python3-tutorial.html">runoob.com Python 教學</a></td><td>需要中文語法入口</td><td>適合快速查找 Python 入門語法。</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Git</th><td><a href="https://git-scm.com/book/en/v2">Pro Git book</a></td><td>想完整理解 Git</td><td>免費的完整參考書。</td></tr>
    <tr><td><a href="https://www.atlassian.com/git/tutorials">Atlassian Git Tutorials</a></td><td>想學 branch、merge 與做事順序</td><td>以圖解說明常見工作流程。</td></tr>
    <tr><td><a href="https://ohshitgit.com/">Oh Shit, Git!?!</a></td><td>操作出錯，需要快速復原</td><td>用「發生什麼事」分類常見救援方法。</td></tr>
    <tr><td><a href="https://github.com/k88hudson/git-flight-rules">git-flight-rules</a></td><td>需要更完整的救援手冊</td><td>涵蓋較多 Git 問題與處理方式。</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">CLI／Shell</th><td><a href="https://github.com/jlevy/the-art-of-command-line">The Art of Command Line</a></td><td>想系統學習命令列</td><td>從新手指令延伸到較進階的操作。</td></tr>
    <tr><td><a href="https://learn.microsoft.com/en-us/training/modules/introduction-to-powershell/">Microsoft Learn — PowerShell</a></td><td>Windows 使用者</td><td>Microsoft 官方的 PowerShell 入門教材。</td></tr>
    <tr><td><a href="https://explainshell.com/">explainshell.com</a></td><td>看不懂一整串 shell 指令</td><td>把指令拆開，逐段解釋用途。</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">REST API</th><td><a href="https://developer.mozilla.org/en-US/docs/Web/HTTP">MDN — HTTP</a></td><td>想理解 HTTP</td><td>Mozilla 維護的 Web 平台參考資料。</td></tr>
    <tr><td><a href="https://learning.postman.com/">Postman Learning Center</a></td><td>想用圖形介面試 API</td><td>不必先寫程式，也能看到送出的內容與收到的結果。</td></tr>
    <tr><td><a href="https://github.com/httpie/cli">HTTPie</a></td><td>偏好從命令列呼叫 API</td><td>語法比原始 curl 指令容易閱讀。</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">YAML／JSON</th><td><a href="https://yaml.org/">YAML 官網</a></td><td>需要查 YAML 規格</td><td>語法與正式規格的入口。</td></tr>
    <tr><td><a href="https://www.json.org/json-en.html">JSON 介紹</a></td><td>第一次接觸 JSON</td><td>用短例子說明 JSON 的資料結構。</td></tr>
    <tr><td><a href="https://github.com/jqlang/jq">jq</a></td><td>想從命令列處理 JSON</td><td>常用來篩選與整理 API 回應。</td></tr>
  </tbody>
</table>

</details>

---

> ✅ **走完 Stage 0 了？** 接著前往 [**Stage 1 — LLM 基礎**](01-llm-basics.md)，完成第一次 LLM API 呼叫，並學會 token、context window 與成本估算。

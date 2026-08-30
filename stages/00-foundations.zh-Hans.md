# Stage 0 — 基础准备（Foundations）

> [繁體中文](./00-foundations.md) | [English](./00-foundations.en.md) | **简体中文**

这一关先检查你是否会用后面一定会用到的四种工具。会的话就直接跳过。不会也没关系。照着下面的小练习做一次即可。

## 何时可以跳过这个阶段

看看下面四件事。你不需要背指令。但你要能自己查资料并完成：

- [ ] 用 Python 从 API（给程序取数据的入口）获取公开数据，再从 JSON 里找出一个值。
- [ ] 用 Git 复制项目（`clone`）、创建工作线（`branch`）、保存版本（`commit`），再把版本发送到网上（`push`）。两次修改碰到一起时，知道什么是合并冲突，也知道要保留什么。
- [ ] 用命令行（在终端输入的文字指令）切换文件夹、创建文件并运行 Python script。
- [ ] 看懂 YAML 和 JSON。它们都是用文本保存数据的格式。

四项都能做到，就直接前往 [Stage 1 — LLM 基础](01-llm-basics.zh-Hans.md)。只要有一项不确定，就完成本页的主要练习。需要时再展开补充内容。

## 📌 学习目标

完成这一关后，你可以：

- 让 Python 从 API 获取数据，再读出 JSON 里需要的部分。
- 从终端运行程序，并找到程序创建的文件。
- 用 Git 保存一个版本，需要时可以回到这个版本。
- 认出 YAML、JSON 和 API token（让程序登录的秘密文字），知道哪些内容不能公开。

## 🛠 动手练习：做一个 GitHub 数据小工具

**成果：**让 Python 从 GitHub 获取公开数据，把结果显示在屏幕上、写入文件，再用 Git 保存。这项主要练习不需要账号、API token 或付费服务。

### 1. 创建程序

创建一个新文件夹。把下面内容保存为 `github_profile.py`：

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

result = f"{profile['login']} 有 {profile['followers']} 位关注者"
print(result)
Path("result.txt").write_text(result + "\n", encoding="utf-8")
```

API 是程序获取数据的入口。JSON 是这次收到的数据格式。

### 2. 运行程序

在终端进入该文件夹，然后运行：

```bash
python github_profile.py
```

屏幕会显示账号和关注者数量。文件夹里也会多出 `result.txt`。关注者数量会变化。不需要和别人的屏幕一样。

### 3. 用 Git 保存成果

```bash
git init
git add github_profile.py result.txt
git commit -m "Add GitHub profile checker"
```

Commit 是 Git 保存的一个版本，旁边会有一句说明。如果 Git 第一次要求姓名或 email，按屏幕提示设置后，再运行一次 `git commit`。这些信息是版本的作者标签，不是密码。

## ✅ 完成检查

- [ ] 终端显示 GitHub 账号和关注者数量。
- [ ] `result.txt` 中有相同结果。
- [ ] `git log --oneline` 能看到刚才的 commit。
- [ ] 程序和 commit 中没有密码或 API token。

四项都完成后，就可以前往 [Stage 1 — LLM 基础](01-llm-basics.zh-Hans.md)。如果卡住，展开下面最接近问题的部分。不必一次读完。

<details markdown="1">
<summary>⏱️ 展开时间、环境与这一关存在的原因</summary>

**时间：**完全不熟时预留 1–2 周，约 5–15 小时。已经会其中几项的话，只补不熟的部分。

**环境：**准备仍受支持的 Python 3、Git、文本编辑器和终端。终端就是输入文字指令的窗口。Windows 可以使用 PowerShell。macOS 或 Linux 可以使用系统终端。

先确认工具可以运行：

```bash
python --version
git --version
```

后面的 AI agent 教材会直接使用 Python、Git、命令行和配置文件。Stage 0 不会教完所有内容。它只帮助你找出不熟的地方，再告诉你去哪里补充。

</details>

<details markdown="1">
<summary>🧰 展开 Python、Git、命令行与 YAML／JSON 补充练习</summary>

只做你还不熟的项目：

1. **Python：**把主要练习 URL 里的 `torvalds` 换成自己的 GitHub 账号或其他公开账号。确认程序仍能读出 `login` 和 `followers`。
2. **Git：**创建一个新 branch（不直接修改原版本的工作线），修改输出文字，再做一次 commit。接着把练习放到自己的远程 Git 项目，并运行 `git push`。
3. **命令行：**创建 `src`、`tests`、`docs` 三个文件夹。从不同路径运行主要练习，并找出 `result.txt` 实际写到哪里。
4. **JSON：**把 API 响应保存成文件，找出 `name`、`public_repos` 和 `followers` 三个字段。
5. **YAML：**创建一个含有 `username` 和 `output_file` 的小配置文件，练习缩进、字符串和布尔值。YAML 对空格很敏感。不要使用 Tab 缩进。

遇到错误时，先读最后一行错误信息。再确认当前文件夹、文件名和 Python 版本。一次只改一件事。这样才能知道哪个修改有效。

</details>

<details markdown="1">
<summary>🔐 展开选修：安全地体验 GitHub API 验证</summary>

主要练习不需要 token。Token 是一串让 GitHub 认出你的秘密文字。只有想理解“登录后的 API”时才做这一题。

1. 按 [GitHub 官方说明](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) 创建 fine-grained personal access token。Fine-grained 表示你可以只开放需要的权限。
2. 使用最短的有效期限，不加入额外权限。`GET /user` 对 fine-grained token 不要求任何权限。
3. 把 token 放进环境变量 `GITHUB_TOKEN`。环境变量是电脑暂时保存数据、让程序读取的位置。不要把 token 写进 Python、Markdown、截图、终端历史或 Git commit。
4. 调用 `https://api.github.com/user` 两次。第一次不带 token，应返回 `401`，意思是尚未登录。第二次带 token，应返回 `200`，意思是 GitHub 接受了请求。
5. 练习结束后，回到 GitHub 设置页撤销 token，并清除环境变量。

Bash 可以这样避免把输入显示在屏幕上：

```bash
read -s GITHUB_TOKEN && export GITHUB_TOKEN
curl -sS -o /dev/null -w "无 token: %{http_code}\n" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user
curl -sS -o /dev/null -w "有 token: %{http_code}\n" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user
unset GITHUB_TOKEN
```

PowerShell 7.1 以上可以这样做：

```powershell
$env:GITHUB_TOKEN = Read-Host -MaskInput "Paste token"
$withoutToken = Invoke-WebRequest -Uri https://api.github.com/user `
  -Headers @{ Accept = "application/vnd.github+json" } `
  -SkipHttpErrorCheck
$withToken = Invoke-WebRequest -Uri https://api.github.com/user -Headers @{
  Authorization = "Bearer $env:GITHUB_TOKEN"
  Accept = "application/vnd.github+json"
} -SkipHttpErrorCheck
"无 token: $($withoutToken.StatusCode)"
"有 token: $($withToken.StatusCode)"
Remove-Item Env:GITHUB_TOKEN
```

Token 就像程序使用的临时钥匙。拿到它的人可能以你的身份操作。所以权限越少、期限越短越安全。

</details>

<details markdown="1">
<summary>🗺️ 展开名词与 Agent 全景补充</summary>

- **CLI（命令行接口）：**在终端输入文字指令来操作电脑。
- **API（应用程序接口）：**让两个程序按固定规则交换数据的入口。
- **JSON／YAML：**用文本保存结构化数据的两种格式。JSON 常见于 API。YAML 常见于配置文件。
- **Git：**记录文件版本的工具。commit 是一次带说明的版本快照。

看到其他不懂的词，先查[术语表](../resources/glossary.zh-Hans.md)。想知道 agent 为什么可能出现在终端、聊天软件或设备上，再看[Agent 全景地图](../resources/agent-paradigms.zh-Hans.md)。这两份都不是开始主要练习前的必读内容。

</details>

## 🎯 精选学习资源

需要补哪一项能力时，再找对应入口。不用把 18 个资源全部读完。

<small>学习资源与 GitHub 验证指引核查：2026-08-27 UTC</small>

`推荐度` 是学习优先顺序，不是 GitHub 的热门数字。按照项目规则，⭐⭐⭐⭐⭐ 代表“没有它就会卡住”；下面都是补充资源，所以诚实使用 ⭐⭐⭐⭐（强烈推荐）或 ⭐⭐⭐（扎实参考），不用假五星。

<table>
  <thead><tr><th scope="col">主题</th><th scope="col">资源</th><th scope="col">适合谁</th><th scope="col">推荐度</th><th scope="col">为什么推荐／备注</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="5">Python</th><td><a href="https://github.com/ehmatthes/pcc_3e">Python Crash Course</a></td><td>想跟着一本书从头练习</td><td>⭐⭐⭐⭐</td><td>代码免费并配有练习；完整教材需要购买书籍。</td></tr>
    <tr><td><a href="https://realpython.com/">Real Python</a></td><td>学过一点，想查一个问题</td><td>⭐⭐⭐⭐</td><td>文章按主题分开，遇到问题时容易查找。</td></tr>
    <tr><td><a href="https://www.youtube.com/c/Coreyms">Corey Schafer YouTube</a></td><td>喜欢看英文视频</td><td>⭐⭐⭐</td><td>用视频从基础语法讲到实际应用。</td></tr>
    <tr><td><a href="https://www.boot.dev/">Boot.dev</a></td><td>喜欢一边操作一边学</td><td>⭐⭐⭐</td><td>部分内容免费；完整后端路线需要付费。</td></tr>
    <tr><td><a href="https://docs.python.org/zh-tw/3/tutorial/">Python 官方繁体中文教程</a></td><td>做完第一次练习，想查正确语法</td><td>⭐⭐⭐⭐</td><td>官方参考资料；它预期你已经懂一点编程。</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">Git</th><td><a href="https://git-scm.com/book/en/v2">Pro Git book</a></td><td>想完整理解 Git</td><td>⭐⭐⭐⭐</td><td>免费的完整参考书。</td></tr>
    <tr><td><a href="https://www.atlassian.com/git/tutorials">Atlassian Git Tutorials</a></td><td>想用图看懂 branch、merge 和操作顺序</td><td>⭐⭐⭐⭐</td><td>用图解说明常见工作流程。</td></tr>
    <tr><td><a href="https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things">Pro Git — Undoing Things</a></td><td>Git 操作出错，想安全恢复</td><td>⭐⭐⭐⭐</td><td>先说明哪些操作可能丢失资料，再教你如何恢复。</td></tr>
    <tr><td><a href="https://github.com/k88hudson/git-flight-rules">git-flight-rules</a></td><td>基本方法不够，想查更多问题</td><td>⭐⭐⭐</td><td>收录更多 Git 问题与处理方式。</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">CLI／Shell</th><td><a href="https://github.com/jlevy/the-art-of-command-line">The Art of Command Line</a></td><td>想有顺序地学命令行</td><td>⭐⭐⭐⭐</td><td>从新手指令一路介绍到较进阶的操作。</td></tr>
    <tr><td><a href="https://learn.microsoft.com/en-us/training/modules/introduction-to-powershell/">Microsoft Learn — PowerShell</a></td><td>使用 Windows，想从第一步开始</td><td>⭐⭐⭐⭐</td><td>Microsoft 官方的 PowerShell 入门教材。</td></tr>
    <tr><td><a href="https://github.com/tldr-pages/tldr">tldr pages</a></td><td>只想先看一个指令怎么用</td><td>⭐⭐⭐⭐</td><td>用短小、可复制的例子解释常用指令。</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">REST API</th><td><a href="https://developer.mozilla.org/en-US/docs/Web/HTTP">MDN — HTTP</a></td><td>想知道 API 背后怎么传资料</td><td>⭐⭐⭐⭐</td><td>Mozilla 维护的 HTTP 参考资料。</td></tr>
    <tr><td><a href="https://learning.postman.com/">Postman Learning Center</a></td><td>想用图形界面试 API</td><td>⭐⭐⭐⭐</td><td>不用先写程序，也能看到发送的内容和收到的资料。</td></tr>
    <tr><td><a href="https://github.com/httpie/cli">HTTPie</a></td><td>想从命令行调用 API</td><td>⭐⭐⭐</td><td>指令通常比原始 curl 写法更容易阅读。</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">YAML／JSON</th><td><a href="https://yaml.org/">YAML 官网</a></td><td>需要查 YAML 的正确写法</td><td>⭐⭐⭐</td><td>语法和正式规范的官方入口。</td></tr>
    <tr><td><a href="https://www.json.org/json-en.html">JSON 介绍</a></td><td>第一次接触 JSON</td><td>⭐⭐⭐⭐</td><td>用短例子说明 JSON 怎么装资料。</td></tr>
    <tr><td><a href="https://github.com/jqlang/jq">jq</a></td><td>想从命令行整理 JSON</td><td>⭐⭐⭐⭐</td><td>可以筛选和整理 API 返回的资料。</td></tr>
  </tbody>
</table>

---

> ✅ **完成 Stage 0 了吗？** 接着前往 [**Stage 1 — LLM 基础**](01-llm-basics.zh-Hans.md)，完成第一次 LLM API 调用，并学习 token、context window 与成本估算。

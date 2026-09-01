# scripts/

維護用的工具腳本 + distribution build。

## `check-links.py` — 檢查連結是否失效

掃描所有 markdown 檔案中的 URL，回報 4xx / 5xx / timeout。

```bash
# 一次性檢查全部
python scripts/check-links.py

# 只查 GitHub repos（最容易 404 的）
python scripts/check-links.py --fast

# 只印失敗，不印 OK
python scripts/check-links.py --quiet
```

退出 code：失敗時 = 1，全部 OK = 0。可以接 CI。

依賴：`pip install requests`

## `refresh-stars.py` — 比對 markdown 內標註的 stars 跟實際

```bash
# 列出所有差距 ≥ 10% 的 entry
python scripts/refresh-stars.py

# 設定門檻（譬如 ≥ 20%）
python scripts/refresh-stars.py --threshold 20

# CI 模式（差距超過門檻就退 code 1）
python scripts/refresh-stars.py --check
```

依賴：`pip install requests` + `gh` CLI（`gh auth login`）

## `check-repository-freshness.py` — 查 repo 狀態與文字矛盾

它會把同一個 GitHub repo 的所有引用合併後只查一次；Markdown 連結與分組資源表的 HTML `href` 都會納入。PR 模式只查本次新增或改寫的 Markdown 行；每週模式查完整清單，記錄搬家、封存、停用、授權、最後 push 與最新 release。

```bash
# 不連網：確認每個 tracked repo 都在快照裡
python scripts/check-repository-freshness.py verify-snapshot

# 查目前分支改到的 repo；硬矛盾會回傳 exit 1
python scripts/check-repository-freshness.py changed --base origin/main --head HEAD

# 維護者全量重查（需要 GitHub token 或 gh auth login）
python scripts/check-repository-freshness.py full \
  --update-baseline scripts/repository-freshness-snapshot.json \
  --report repository-freshness-report.md
```

`--output-snapshot` 會誠實輸出本次掃描（包含 `unverified`），供 CI artifact 使用；`--update-baseline` 只有在全部 API 結果可驗證時才會覆蓋長期底稿。這個 gate 只驗 GitHub 能回答的事。半年沒 push 只會提醒，不會自動刪除仍然好用的穩定教材；模型價格、API 行為與教學品質仍要靠各章官方來源與人工複查。API 失敗或 rate limit 會明確標成 `unverified`，不能當作健康。

## `check-reader-ux.py` — 防止已整理章節重新變成文字牆

它只檢查 `reader-ux-pages.yml` 已登記的三語頁面。它用保守的 source-level proxy 計算第一次開頁可見 Markdown 的非空白字元，也檢查預設展開數量、必須留在選單外的精確 heading／anchor，以及合併分類資源表的結構。這個數字可重複比較，但不等於瀏覽器 DOM 字數。

```bash
python scripts/test_reader_ux.py
python scripts/check-reader-ux.py
```

依賴：`pip install --require-hashes -r scripts/requirements-reader-ux.txt`

完成一章的三語內容與人工複查後，才把它加入設定檔。若要調高既有上限或刪除可見 heading，先解釋讀者體驗為什麼沒有倒退；不可只為了讓 gate 變綠而放寬。

## `test_stage07_examples.py` — 鎖住五組可執行範例

這個 gate 同時檢查五個資料夾的三語 README、current-major requirements、固定模型 ID、PowerShell-first 離線入口、預設關閉的補充內容、預算公式、嚴格 Judge parser、Prompt caching 最低長度、FastAPI 輸入上限與非 root Docker。它是結構與安全回歸，不取代十個直接執行的 behavior tests，也不會呼叫 live model。

```powershell
python -m pytest scripts/test_stage07_examples.py -q
```

## `test_stage075_content.py` — 鎖住進階概念 reading-map

這個 gate 檢查 Stage 7.5 三語是否保留六個可見粗體核心詞、12 個概念、四個真正合併的
概念群組、9 個預設關閉選單、24 筆資源與 `5／5／5／5／4` rowgroups。它也鎖住
freshness marker、AutoGen／Agent Framework／Sandbox Agents／Dynamic Workflows 現行狀態、
legacy 深連結，以及兩組共六張不同的 `1672×941` locale 圖。

```powershell
python -m pytest scripts/test_stage075_content.py -q
python scripts/check-reader-ux.py
python scripts/check-2026-freshness.py
```

## 建議的維護節奏

- **每週**：`Content Health` 掃所有外部連結與每個不重複的 GitHub repository，並上傳 JSON／Markdown 證據
- **每月**：同一個 `Content Health` 再檢查模型、價格、授權、可用狀態與官方文件 freshness
- **Release 前**：手動以 `release` 模式重跑完整 Content Health；明確錯誤會阻擋，403／429／timeout 只列為無法驗證
- **推薦度**：正文的 `⭐⭐⭐⭐⭐` 是編輯推薦度，不是 GitHub stars；Action 不會自動改寫或合併教材
- **每個 PR**：`Required / pr-gate` 固定出現並彙整所有阻擋關卡；最終是否合併仍由 Maintainer 決定

這些檢查已接到 GitHub Actions；本機修改前後仍可用上面的命令做最小驗證。

---

## `build-pdf.sh` — 從同一份清單建立三語 PDF

```bash
RELEASE_VERSION=v2026.09.01 LANG_VARIANT=zh-TW bash scripts/build-pdf.sh
RELEASE_VERSION=v2026.09.01 LANG_VARIANT=zh-Hans bash scripts/build-pdf.sh
RELEASE_VERSION=v2026.09.01 LANG_VARIANT=en bash scripts/build-pdf.sh
```

輸出檔名固定為：

- `dist/awesome-agentic-ai-zh-v2026.09.01-zh-TW.pdf`
- `dist/awesome-agentic-ai-zh-v2026.09.01-zh-Hans.pdf`
- `dist/awesome-agentic-ai-zh-v2026.09.01-en.pdf`

頁面順序只寫在 [`release/pages.yml`](../release/pages.yml) 一次；工具會從同一列推導繁中、簡中、英文檔名，並阻擋缺頁、順序漂移和外部 URL 漂移。Stage 0–8、Stage 7.5、A1–A3、五條角色路線、walkthrough、Capstone、Setup、Glossary、Resources、Advanced RAG、Agent Memory、CLI 與模型訓練選修都在這份清單裡。正文裡預設收合的補充內容會在 PDF 中展開。

依賴：Python + PyYAML、Pandoc、WeasyPrint、Poppler、Noto CJK 與 DejaVu 字型。Ubuntu 的安裝方式與正式 workflow 相同：

```bash
sudo apt-get install pandoc weasyprint poppler-utils \
  fonts-dejavu-core fonts-noto-cjk fonts-noto-color-emoji
```

建立後必須抽出文字再驗證，不能只看「有三個檔案」：

```bash
python scripts/release_manifest.py validate-pdfs \
  --version v2026.09.01 --dist dist --json dist/pdf-validation.json
```

[`release/notes.yml`](../release/notes.yml) 也只寫一次。`release_manifest.py render-notes` 會用相同 change ID、順序和共用連結產生三個語言段落。

## 正式 Release

[`Trilingual Release`](../.github/workflows/release.yml) 只接受手動啟動：

1. 用 GitHub API UTC 日期驗證 calendar tag，鎖定當下 `main` SHA。
2. 跑完整內容、連結、repository、freshness、圖片、三語網站與 tests。
3. 建立三份 PDF candidate、抽字驗證，並上傳可下載的 Actions artifact。
4. 在 `release` Environment 等待人工批准。
5. 再確認 `main` 沒有前進，先建 Draft Release、驗證 tag／三份附件／三語 body，最後才發布。

同一天第二次發布使用 `vYYYY.MM.DD-2`。Workflow 不由 push 或 PR 自動發布，也不會略過人工 Environment 關卡。

## `build-mdbook.sh` — 建可瀏覽的網站版

```bash
bash scripts/build-mdbook.sh           # 建到 book/dist/
bash scripts/build-mdbook.sh --serve   # 建好後本機開 server (port 3000)
```

依賴：

- Rust + cargo（[rustup.rs](https://rustup.rs)）
- `cargo install mdbook mdbook-mermaid`
- 第一次跑前：`mdbook-mermaid install .`（會生成 `mermaid.min.js`、`mermaid-init.js`，工作流需要）

**自動部署**：
推 main branch 時，[`.github/workflows/docs.yml`](../.github/workflows/docs.yml) 會自動 build mkdocs 站（`/` 首頁）+ mdBook（`/book/`）並 deploy 到 GitHub Pages。單一 workflow 擁有 Pages（兩個 workflow 各自 deploy 會互搶同一個 root，故已合併、刪除舊的 `deploy-book.yml`）。
要啟用，去 Settings → Pages → Source: GitHub Actions。

## 網站與 Release 流程

1. 推 main → `docs.yml` 自動 build mkdocs（`/` 首頁）+ mdBook（`/book/`）並 deploy 到 `https://wenyuchiou.github.io/awesome-agentic-ai-zh/`
2. Release：手動啟動 `release.yml`，先下載並檢查 candidate artifact，再通過 `release` Environment 發布三語 PDF 與三語 Release Notes

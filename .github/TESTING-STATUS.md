# Testing Status — 誠實揭露

> 這份是給 maintainer / 第一個跑各個 build 的人看的。**誠實地說明哪些 code 真的跑過、哪些只是 syntax check、哪些完全沒測**。

最後更新：2026-08-31

---

## ✅ 真的跑過、有觀察輸出

| 項目 | 狀態 | 證據 |
|---|---|---|
| `scripts/refresh-stars.py` | ✅ Verified | 19 組單元測試綠 + **7 個突變全部被殺**（還原 no-op 防呆 / 重試 / `FETCH_GONE` 三態 / 算繪比對 / 越界檢查，各自都會讓測試 FAIL）。2026-08-10 實跑：275 repos、drift 0 / prose-drift 0 / not-found 0 / could-not-query 0、exit 0，`--threshold 5` 與 CI 用的 `--threshold 50` 兩種參數都跑過。**反向也驗過**：把 `stages/08` 英文版改回舊星數後，同一道指令報 5 筆、exit 1（確認它真的會抓，不是剛好沒東西可報）。此列原本寫「在 main 上跑過 N 次」，那個 N 是沒填完的佔位字 |
| `scripts/pr-link-audit.py` | ✅ Verified | unit tests 綠 + offline `--diff-file` smoke；live `gh api` 正確 flag 了 archived LangServe（★/license/pushed 都對證過） |
| `.github/workflows/pr-link-audit.yml` | 🗃️ Retired | 歷史證據保留：PR #68（throwaway、已關）曾驗證首發 POST、後續 sticky PATCH、archived／stale／no-license 判斷與 fork read-only 邊界。此 workflow 於 2026-08-31 移除；修改過的連結與 repository 事實改由每個 PR 都會出現的 `Required / pr-gate` 唯讀檢查。 |
| `scripts/check-links.py --fast` | ✅ Verified | 跑過 120 GitHub URLs 全 OK |
| `gh api` repo 元資料抓取 | ✅ Verified | 152 個 entry 的 stars / license / pushed 都對證過至少一次 |
| Mermaid syntax | ✅ Verified | GitHub 上 render 看過正確（README hero） |
| CI banned-words / overclaim grep | ✅ Verified | 用相同 grep 邏輯本地跑過，0 violations；並已在真 CI 上驗證——run 30870625764 抓到一個真實違規、修掉後 30871055350 轉綠 |
| `.github/workflows/lint.yml` | ✅ Verified | ubuntu runner 上實跑：`pull_request` 15 次、`workflow_dispatch` 5 次、`schedule` 3 次、`push` 2 次。run 30870625764 實際攔下一個 overclaim 違規（真陽性），30871055350 / 30875518687 / 30892735021 / 30892855033 / 30915746076 全綠。**至今未觀察到與本地 git-bash 的 grep 行為差異**（同一 corpus 兩邊都綠，該次 overclaim 兩邊都抓到）——是觀察到一致，不是已證明等價。2026-08-04 起無 paths 過濾，每個 PR 與每次 push 到 main 都會跑 |
| `.github/workflows/anchor-validator.yml` | ✅ Verified | ubuntu runner 上實跑：`pull_request` 12 次、`schedule` 3 次、`workflow_dispatch` 1 次，全綠。2026-08-04 起移除 paths 過濾並加上 `push: [main]`，每個 PR 與每次 push 到 main 都會跑（push 側尚未累積執行紀錄） |
| `.github/workflows/stage-template-check.yml` | ✅ Verified | ubuntu runner 上實跑：`pull_request` 7 次、`workflow_dispatch` 3 次。run 25934104948（2026-05-15、sha d278caf）失敗過一次，但那是 **false positive**——stage 07.5 是 reading-map 章、依設計就沒有 REQUIRED sections（失敗當時的 sha d278caf 上 README 已標「（reading map）」「1 週（不寫 code）」），53e723d 把 `07.5-` 加進 `SKIP_STAGES` 之後 25934453808 轉綠。**所以這個 gate 至今沒攔下過真實的 template 違規**；其餘 9 次全綠。2026-08-04 起移除 paths 過濾並補上 `push: [main]` 與每月 cron——三個 gate 裡原本只有它連 schedule 都沒有（push / schedule 側尚未累積執行紀錄） |
| 三語 PDF builder 與 manifest | ✅ Verified（2026-08-31，本機 Ubuntu 24.04 container） | `release/pages.yml` 的 28 個入口 × 3 語言、H1 與外部 URL 集合通過；Pandoc 3.1.3 + WeasyPrint 61.1 真正產生繁中 `26,887,670` bytes、簡中 `26,200,059` bytes、英文 `25,944,123` bytes。Poppler 抽字確認每份都有 28 個 heading；英文正文 580,786 個抽出字元中有 241 個 CJK 字元，低於未翻譯正文 gate。人工抽樣封面、Stage 0、Stage 5、Stage 7.5／表格與完成卡，CJK、表格、星等、程式碼與頁碼可讀；遠端 badge／contributors 裝飾圖不進 PDF，本地教學 PNG 保留。完整三語 GitHub Actions candidate 與所有頁面逐頁目視仍留給第一次 `release.yml` run |
| `walkthroughs/…7-steps.md` Stage 1-6 的 Python（6 個 block）| ✅ Verified（2026-08-04） | 抽成檔案後在乾淨 venv（Python 3.14 + anthropic 0.120.2 / langgraph 1.2.10 / langchain-core 1.5.3 / chromadb 1.5.9）逐一執行，`Anthropic` 與 `requests` 以 mock 攔截（**未用 API key、未產生費用**）。抓到並修好 4 個缺陷：① Stage 6 的 memory 實測 `count=0`（空 DB 時提前 return，`store_paper` 從未被呼叫；加上 id 寫死 `"..."`，而 `add()` 遇重複 id 會靜默忽略）；② `compare_with_memory` 讀 `messages[-1]`，但那是 `reflect` 的判定訊息不是摘要——實測三篇論文存進去的文件**完全相同**（都是 `[Reviewer 判定: PASS]`）；③ 它回傳的 `comparison` 被 LangGraph 丟掉（`State` 沒宣告）；④ `import step2` 就送出一次真實 API 呼叫。修後實測：存進去的是各自的摘要、`count` 1→2→3、`comparison` 保留、被 import 的 4 個檔案 0 次呼叫。三語 27 個 block 現在都能 `ast.parse` |
| `walkthroughs/…7-steps.md` Stage 7 的 Python（3 個 block）| ✅ Verified（2026-08-10） | **7.1 `eval_provider`**：`call_api()` 回傳 `{'output': …}`。**7.2 `step7_observability`**：原本 import 失敗（`observe` 在 langfuse **3.0** 就移到套件頂層，只有 2.x 用 `langfuse.decorators`；實測 2.60.10 / 3.0.0 / 4.14.2 三版確認），改掉 import path 後 ✅，`@observe(name=…)` 的用法在 4.14.2 未變（已查 signature）。**7.3 `main.py`**：裝了 fastapi 0.141.1 / uvicorn 0.52.1 / pydantic 2.13.4 後實跑——`TestClient` 打 `POST /summarize` 回 **HTTP 200** 與 `{'summary': …}`，缺欄位回 **HTTP 422**（pydantic 驗證）。至此 **9 個 block 全部執行過** |

---

## ⚠️ 只做了 syntax check / 配置 validation，沒實際 end-to-end 跑

| 項目 | 狀態 | 缺什麼 |
|---|---|---|
| `.github/workflows/release.yml` | ⚠️ actionlint／permissions／workflow unit 已驗證 | 只有 `publish` job 有局部 `contents: write`，並在 `release` Environment 後才執行；仍需第一次真實 workflow run 驗證 apt 套件、artifact 路徑、Draft → publish 與三份附件 |
| `scripts/build-mdbook.sh` | ⚠️ Bash syntax OK | 跑過一次但 mdbook-mermaid 失敗（已 fix 但沒重跑驗證） |
| `.github/workflows/docs.yml` | ⚠️ YAML valid · 本機 mkdocs build 綠 | 統一 Pages workflow（mkdocs `/` + mdBook `/book/`，取代已刪除的 deploy-book.yml）。mdBook 子路徑 base-url 尚未在 CI 端到端驗證（首次 deploy 後需實測 `/book/` 資產） |
| `book.toml` mdBook 設定 | ⚠️ TOML valid | 沒實際 build 過完整 site |

---

## ❌ 完全沒測（design / template，等實際使用才會發現問題）

| 項目 | 為什麼沒測 |
|---|---|
| 三語 PDF 的全頁視覺品質 | 已抽樣封面、Stage 0、Stage 5、Stage 7.5／表格與完成卡；正式 candidate 仍需逐份檢查目錄、CJK 字形、圖片和分頁。`pdftotext` gate 只證明頁面與文字存在，不會假裝能判斷美感 |
| GitHub Pages 上的 mdBook hosted 版 | repo Settings 還沒切到 GitHub Actions source（user 手動步驟） |
| 第一個三語 PDF release | 工具與人工關卡已建立，仍需完成第一次 candidate run 和 `release` Environment 批准 |
| `.github/launch-checklist.md` 內所有「啟用 Discussions / 提交到 awesome lists / 寫 launch posts」項目 | 全部還沒做 |

---

## 對社群貢獻者的建議

如果你是第一個真的要跑某個 build / workflow 的人：

1. **正式發布 PDF**：優先手動啟動 `Trilingual Release`；下載 candidate artifact，實際打開三份 PDF 檢查 CJK、表格、圖片與分頁，再批准 `release` Environment
2. **跑 `bash scripts/build-mdbook.sh` 之前**：先 `cargo install mdbook mdbook-mermaid` 並在 repo root 跑 `mdbook-mermaid install .`；推上去前先本地 `--serve` 看一下
3. **試 walkthrough 的 Python**：建議用一個全新環境（venv），照 Stage 0 的一次性 install 跑完，遇到任何 import / API 不符的，**請開 issue + PR**——因為這就是「第一手實測」價值最高的時刻
4. **觸發 CI lint workflow**：開個 throwaway PR 改 `stages/01-llm-basics.md`，故意加 `教程` 這個禁用詞，看 banned-words job 有沒有正常 fail。如果沒抓到，調整 grep 邏輯
5. **Deploy book 第一次**：repo Settings → Pages → Source: GitHub Actions，然後 push 一次 commit 讓 workflow 跑。看 Actions tab 看結果

---

## 為什麼 maintainer 沒全部 test

老實說：

- **三語 PDF 工具鏈**：正式路徑使用 Pandoc + WeasyPrint + Poppler + Noto CJK，並列入 Release blocking gate。2026-08-31 已用 Ubuntu 24.04 容器實際產生繁中／簡中／英文三份 PDF，逐份抽字驗證 28 個正文頁面；第一次 GitHub Actions candidate run 仍須下載三份 artifact 做最後目視檢查
- ~~**AI walkthrough 的 LangGraph / Chroma 等套件**：版本日新月異…所以選擇用「對著官方 API 文件寫」的策略~~——**Stage 1-6 已不成立**（2026-08-04 實跑，見上表）。版本會過期這件事本身仍然成立：這次就抓到 `create_react_agent` 已被 LangGraph V1.0 標記棄用、`langfuse.decorators` 已移除
- **CI workflow**：~~在真 PR 上才會觸發；沒第一個外部 PR 之前看不出來~~——**已不成立**（2026-08-04）。三個 gate（`lint` / `anchor-validator` / `stage-template-check`）都已在真實 PR 上跑過，且同日移除 paths 過濾、三個都補上 `push: [main]`，所以**每個 PR 與每次直接推 main 都會觸發**——後者是 2026-06-07 → 08-04 的 109 個 commit 裡的 95 個。`lint.yml` 的 push 側已有實際執行紀錄；另外兩個的 push trigger 是當天才加的，尚未累積紀錄

這份 repo 是 **「ship-able skeleton」**——所有結構都對、所有 metadata 都驗證過、所有 prose 都過 review，但**第一次實際跑 build / deploy / walkthrough 還是會發現坑**。

第一個踩到坑的人請開 issue + PR——這正是社群協作的價值所在。

---

## 修這份 testing status

每次跑過某個項目後，把上面表格的 ⚠️ 改成 ✅ 並補「證據」欄。
真實「跑過 + 有 observable output」才算 ✅，「我覺得 OK」不算。

# Stage 07 可執行範例現代化計畫

- 日期：2026-08-28 UTC
- Release branch：`codex/stage07-examples-stack`
- PR 基底：`codex/stage07-reader-ux-stack`（PR #162，head `bfdec26`）

## 目標

讓讀者進入任一 Stage 07 範例資料夾後，可以先複製一組 PowerShell 指令，
在不需要 API 金鑰的情況下跑完離線測試，再自行選 Ollama Path A 或
Anthropic Path B。敘述先用白話說「會看到什麼」，再保留 Eval、Trace、
Streaming、Prompt caching、FastAPI、Docker 等正確術語。

本層只處理五個既有範例，不新增假的 Exercise 6：

1. `01-multi-agent-debate`
2. `02-eval`
3. `03-observability`
4. `04-sdk-advanced`
5. `05-deploy`

## 編輯前基線

- 五題 Path A／Path B 共 10 個離線入口全部通過。
- `python -m compileall -q examples/stage-7` 通過。
- 現有測試證明基本 happy path，但沒有阻擋過期模型、固定價格／延遲、
  Prompt cache 未達最低 token、寬鬆 Judge parser、無界 API 輸入或
  root Docker container。

## 已確認要修的事實

官方來源優先，查核日固定為 2026-08-28 UTC：

- [Ollama qwen3.5](https://ollama.com/library/qwen3.5) 現有 `0.8b／2b／4b／9b…`
  tags；初學者預設改為 `qwen3.5:4b`，仍可用 `MODEL` 覆寫。
- [Anthropic models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
  仍列 `claude-haiku-4-5-20251001`，價格為每百萬 input／output tokens
  `$1／$5`；範例固定 snapshot ID，不使用會漂移的 alias。
- [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
  對 Haiku 4.5 的最低可快取長度為 4,096 tokens；5 分鐘 write 是 base
  input 的 1.25 倍，cache read 是 0.1 倍。現有「約 2,000 tokens」示範
  不會命中，必須重建並以 usage 欄位判定。
- PyPI JSON 現行版本為 `openai 3.5.0`、`anthropic 1.2.0`、
  `fastapi 0.141.1`、`uvicorn 0.52.4`、`httpx 0.28.1`、`pydantic 2.13.4`；
  requirements 採 current-major 範圍，不鎖死 patch。

## README 的固定讀法

每題三語依序保留：

1. 這題會做出什麼。
2. `🎯` 三個學習目標。
3. 第一個直接可複製的 PowerShell：建立該題自己的 `.venv`、安裝、跑
   `python test.py` 與 `python test_anthropic.py`。
4. Path A：`qwen3.5:4b`，只說模型 API 不產生供應商帳單；電力、硬體與
   下載時間仍有成本。
5. Path B：固定 Haiku ID、顯示 token 公式與保守 provider spend limit，
   不把估算寫成帳單保證。
6. 「只改一件事」與短版成功檢查。

macOS／Linux、完整程式走查、替代方案、production 深解、排錯與延伸資源
放進預設關閉的 `<details markdown="1">`。不要求讀者抄空白模板、改檔名或
把程式另存到文字檔。

## 程式與安全修正

- 五個 Ollama starters 改用 `qwen3.5:4b`；五個 Anthropic starters 改用
  `claude-haiku-4-5-20251001`。
- 所有模型輸出都拒絕空字串；Judge 結果只接受明確格式，不以子字串
  `PASS` 或 `WINNER` 誤判。
- Eval 保留 deterministic evaluator；LLM-as-judge 只作另一個可量測方法，
  不宣稱比固定規則可靠。
- Observability 記錄 request ID、span、安全的錯誤類別、latency 與供應商回傳的
  usage；不保存可能含 secret／Prompt 的原始 exception 訊息，也不把某一家 usage
  寫成永遠比較「精確」。
- Streaming 不再承諾固定首 token 秒數；只有非空白文字才算成功，first-token
  從第一段可見文字開始，讀者量自己的 first-token 與 total latency。
- Prompt caching 建立足以跨過 Haiku 4.5 4,096-token 門檻的示範文字，
  同時檢查 `cache_creation_input_tokens`／`cache_read_input_tokens`；沒有命中
  就誠實顯示，不印假成功。
- FastAPI 的 `message` 與 `max_tokens` 加上上下限，liveness 不呼叫模型，
  429／503／422 行為由離線測試鎖住；不把 prompt 寫進 production log。
- Docker image 使用非 root user；README 先教 loopback port、read-only
  filesystem 與必要環境變數，不把 container 稱為完整 sandbox。

## 驗收與 gate

- 新增 `scripts/test_stage07_examples.py`，鎖住五資料夾、三語 README、
  current-major requirements、固定模型 ID、PowerShell-first、closed details、
  預算公式、安全界線與禁止的舊宣稱。
- 逐題直接執行 10 個離線入口。
- `python -m compileall -q examples/stage-7`
- `python -m pytest scripts -q`
- strict anchors、mirror parity、locale links、Hans 字元、duplicate repos、
  repository freshness changed-links。
- `python scripts/build-docs-tree.py`
- `python -m mkdocs build`
- `git diff --check`

## Stacked 邊界

本層疊在 Stage 07 內容 PR #162 上；不改 Stage 7.5／8，也不回頭重寫
Stage 07 正文。依使用者同意開一個獨立 stacked PR；未經使用者明確同意，
不 merge、不刪 branch。最終 stable staged diff 必須重新經獨立
`code-reviewer`；任何 ACK 後修改都讓 fingerprint 失效。

## 最終驗證證據

- 2026-08-28 UTC 重新打開 Anthropic 模型／Prompt caching、Ollama qwen3.5
  與六個 PyPI 官方頁；型號、價格、4,096-token 門檻與 requirements 範圍未漂移。
- 唯讀掛載目前 repo 到乾淨 `python:3.11-slim`；解析為 OpenAI 3.5.0、
  Anthropic 1.2.0、FastAPI 0.141.1、Uvicorn 0.52.4、Pydantic 2.13.4、
  HTTPX 0.28.1，`pip check` 與十個離線入口全部通過。
- deploy image 從零建置，設定使用者為 `appuser`，執行 UID 為 `10001`；
  以 read-only filesystem、`tmpfs /tmp` 與 loopback-only host port 啟動時，
  `/health` 回傳 `{"status":"ok"}`。沒有呼叫 live model，也不宣稱輸出品質。
- 全量 GitHub API 快照於 `2026-08-28T09:48:57Z` 重建並覆蓋 260 個實際
  repo 引用；Stage 7 範例沒有 hard error。全站仍有 16 個既有 redirect／
  license 錯誤，留給各自章節修正，沒有被本層隱藏成通過。
- 第一次獨立 review 以舊 fingerprint 擋下四項問題：共用模型指引把 Stage 3–7
  混成一個預設、whitespace-only stream 被當成成功、Observability 保存原始
  exception 訊息，以及 Debate docstring 宣稱未被本例證明的 bias／穩定性效果。
  修正後必須建立新 fingerprint 並重新 review；舊 staged 狀態不算 ACK。
- 第二次 review 又沿 repo 引用抓到三語 setup guide 還保留 `Stage 3+`／`$0/run`，
  以及英文／簡中模型表把 `llama3.2:3b` 寫成 `3+`。兩組鏡像與 contract 一併
  修正後，第二個 fingerprint 也作廢，必須第三次 review 才能取得 ACK。

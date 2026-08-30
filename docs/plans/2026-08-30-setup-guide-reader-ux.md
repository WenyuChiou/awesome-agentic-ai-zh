# Setup Guide 漸進式閱讀與現行安裝路徑計畫

## 目標

把 `resources/setup-guide*` 從一次攤開五種入口、五段安裝與大量易變產品資訊的長頁，改成初學者先選一扇門，再完成一個可執行結果的設定指南。文字要讓第一次碰 terminal 的讀者也能照做，同時保留 API、API key、environment variable、runtime、package manager、CLI Agent 等正確術語。

本層最初從 PR #194 的 head 建立；使用者同意整合後，#190–#194 已依序合併，現在直接以最新 `main` 為 base。不改其他 Stage 正文。

## 現況診斷

| 語言 | 未收合字元 | 標題 | `<details>` |
|---|---:|---:|---:|
| 繁中 | 9,776 | 32 | 0 |
| English | 14,307 | 32 | 0 |
| 簡中 | 9,856 | 32 | 0 |

主要缺陷：

1. Web、Desktop、IDE、CLI Agent、API 五條平行入口被寫成由簡到難的單一路線，讀者容易以為要全部安裝。
2. API quick start、Claude Code、`CLAUDE.md`、Skill 與多供應商 catalog 同時攤開，第一個可完成任務不突出。
3. Claude Code 仍以 Node.js／npm 當主要安裝法；官方已改為 native installer 優先。
4. Gemini desktop、免費額度、固定月費、贈送 credits、模型價格與「最便宜」等說法已變動或容易自然過期。
5. API key 安全規則存在，但 `.gitignore` 排在 `.env` 之後；初學者可能先建立 secret，再忘記排除。
6. A–E 舊標題有跨頁深連結；重排時不能讓它們消失或藏到選單內。

## 新的可見主線

不展開任何選單時，讀者依序看到：

1. 這份指南能幫什麼，以及何時可以跳過。
2. Web Chat、Desktop、IDE、CLI Agent、API 五扇平行入口的短表；每列只留「它是什麼、第一步、適合誰」。
3. 七個粗體核心詞：Chat Surface、API、API Key、Environment Variable、Runtime、Package Manager、CLI Agent。
4. 三條必讀安全規則與五個官方起點；精選資源與編輯推薦度直接可見。
5. A–C 的最短 API quick start：先建立 `.gitignore`，再建立 `.env`，用 `uv` 安裝 Python 3.12，複製 `hello-claude.py`，直接執行。
6. D／E 的標題、舊錨點、一句成果與返回 Stage 5 的路由。
7. 短版完成檢查與下一站。

## 預設收合

- 時間、系統需求與完整先備條件。
- Web／Desktop／IDE／CLI 的完整產品清單。
- 其他 cloud provider 與 OpenAI-compatible endpoint 對照。
- macOS、Windows、Linux 的替代安裝方式。
- Claude Code 詳細安裝、登入與 `CLAUDE.md` 範例。
- Skill 完整範例。
- 常見錯誤與復原方式。

所有選單預設關閉。A–E heading、舊 anchor、第一個動作與成果不得藏進選單。

## 現行事實基線

統一查核日期為 `2026-08-30` UTC：

- Claude API：Console API key、Claude subscription 與 API billing 分開；Python SDK 可讀 `ANTHROPIC_API_KEY`，`.env` 需由 `python-dotenv` 載入。
- API 範例使用現行平衡型 `claude-sonnet-5`，不在 setup guide 保存價格。
- Claude Code：native installer 優先；macOS／Linux／WSL 與 Windows PowerShell 使用官方現行命令。免費 Claude.ai plan 不含 Claude Code；登入與 Console／cloud provider 路徑回官方 Authentication。
- `CLAUDE.md` 可放 project root 或 `.claude/CLAUDE.md`；Skill 路徑為 `.claude/skills/<name>/SKILL.md`。
- `uv` Tier 1 支援 Python 3.10–3.14，且可自行安裝 Python；本教學固定 Python 3.12 以取得廣泛套件相容性。
- 其他 provider 只寫官方入口與 compatibility 範圍；移除促銷 credits、固定免費額度、固定價格與無來源強弱比較。

## 文件與 gate

預計修改：

- `resources/setup-guide.md`、`.en.md`、`.zh-Hans.md`
- `README.md`、`.en.md`、`.zh-Hans.md` 的 setup-guide 摘要
- `scripts/reader-ux-pages.yml`
- `scripts/freshness-models.yml`
- 新增 `scripts/test_setup_guide_content.py`
- `resources/diagrams/locale-variant-prompts.md` 不變；本頁使用選擇表已足夠，不新增裝飾性概念圖。
- `CHANGELOG.md`
- `stages/DESIGN.md` 與 `docs/TESTING_PLAN.md` 記錄固定結構與驗收契約。

驗收鎖定：三語核心詞與章節順序、A–E legacy anchors、全部 `<details>` 關閉、可複製程式、`.gitignore` 先於 `.env`、官方 URL 順序、日期一致、禁止舊 Node-first／固定價格／credits／舊 Gemini desktop 說法。

## 驗證

- `git diff --check`
- reader UX、strict anchors、anchor slug parity、mirror parity／sync、locale links、Hans、image locale、freshness
- `python -m pytest scripts -q`
- `python scripts/build-docs-tree.py`
- `python -m mkdocs build`
- 最終 staged fingerprint 由獨立 `code-reviewer` 審查；任何後續修改使 ACK 失效。

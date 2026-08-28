# Stage 06 RAG 與 Memory 閱讀體驗、事實與範例現代化 Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 讓初學者不展開任何選單也能分清 **Retrieval、RAG、Embedding、Vector Store、Chunk、Reranking 與 Memory**，直接完成第一個練習；同時把三語事實、優質專案與五個範例更新到 `2026-08-28 UTC` 的現況。

**Architecture:** 使用兩層 stacked PR。06A 只處理 Stage 06 三語教材、概念圖、直接相依術語、官方事實包、資源表與 reader-UX gate；06B 疊在 06A 上，修正五個可執行範例及其測試。兩層都獨立 review、commit、push、開 PR；未經使用者明確同意，不合併、不刪 branch、不清 worktree。

**Tech Stack:** Markdown、MkDocs、HTML `details`／`table`、Python、PyYAML、pytest、Pillow、Chroma、Sentence Transformers、OpenAI／Anthropic SDK、GitHub API 與供應商官方文件。

---

## 狀態與邊界

- GitHub API UTC：`Fri, 28 Aug 2026 04:17:07 GMT`。
- 隔離 worktree：`C:/Users/wenyu/.codex/worktrees/awesome-agentic-ai-zh/stage06-reader-ux`。
- 06A branch：`codex/stage06-reader-ux`。
- 06A base：`243f9b39ca03b19cfed4379024d5c3ad91d714dc`，也就是未合併 roll-up PR #157 的最新 head；Stage 5 的收合區 Markdown 渲染修正已包含在基底，不會被本層反向覆蓋。
- 06A PR base 固定為 `codex/stages04-05-rollup`；#157 合併並通過 main CI 後，再只 retarget 到 `main`，不重寫內容。
- 主工作區的 Claude 同期修改不在本計畫範圍；不得切換、覆蓋或清理該工作區。
- 本次不重寫 Stage 07、07.5、08、README 或三種角色路徑。只修正會使 Stage 06 當頁立刻矛盾的直接相依術語與連結。
- 重要概念不因精簡而刪除。進階名詞移入關閉區後，仍須有白話定義、正式術語、用途與限制。

## 唯讀診斷

### 閱讀形狀

- 三語約 `773–784` 行，各有 `48` 個 heading、`151` 個 URL、`4` 張圖，卻只有 `2` 個關閉 `<details>`。
- 繁中初始非空白字元約 `41,026`；研究 survey、初學教程、工具比較、五個練習與資源表同時攤開。
- `📌`、`🚪`、`📚` 在大量概念與研究內容之後才出現；第一個練習接近頁尾。
- 必須保留 `📌`、`🚪`、`📚`、`🛠`、`🎯`、`✅` 路標、五個練習、短版完成檢查與 Stage 07 入口。
- 18 筆精選專案保留編輯五星評分；移除所有會自然變動的 GitHub stars 數字。
- 現有表格以空白分類欄假裝合併，須改為真正的 `<th scope="rowgroup" rowspan="N">`。
- 三語各有空引號殘留；日期與查核說明過度顯眼或冗長時，改成關閉區內的 `<small>` 一行。

### 已確認需修正的事實

- Microsoft GraphRAG 是 **MIT**，而且官方已標示為 largely in maintenance mode；不是教材目前寫的 Apache-2.0 一般活躍專案。
- Ragas canonical repository 已由 `explodinggradients/ragas` 轉為 `vibrantlabsai/ragas`。
- `text-embedding-ada-002` 不再作為本章推薦入口；範例已使用 `text-embedding-3-small`，正文與 glossary 必須一致。
- Letta 的現行開發已移到 `letta-ai/letta-code`；`letta-ai/letta` 是入口／歷史 V1 說明，不能當成現行 server source。
- Zep Community Edition 已 deprecated 並移到 `legacy/`；現行 Zep Cloud 與開源 Graphiti 必須分開標示。
- Anthropic Contextual Retrieval 的 `5.7% → 1.9%` 是其特定測試中 top-20 chunk retrieval failure rate，不得改寫成所有 RAG 的通用準確率。
- 「中文文件使用英文模型會掉一半」「reranking 通常 70→85–90%」「Agentic RAG 固定慢 1.5–3 倍」都缺少足夠通用證據；刪除或改成要求讀者用自己的資料評測。
- 固定 chunk size、top-k 與模型排名不得寫成通用答案；先教可理解的起點，再教用 eval 決定。

### 五個範例的已知缺陷

- Exercise 5 的 `MemoryStore` 永遠使用 `EphemeralClient`，與跨 session 長期記憶說明矛盾。
- Exercise 3 在 `overlap >= chunk_size` 時不前進，會形成無限迴圈。
- Exercise 4 重複使用固定 Chroma collection 與固定 ID，換文件後可能仍查到舊資料。
- Exercise 2、4、5 測試仍會下載或建立真實 embedding model，不能稱為完全離線。
- README 對 Chroma duplicate ID 的描述與目前實際行為矛盾。
- Path A／B 的 starter asserts 與獨立實作深度不足，尚未達 repository contract。

## 讀者不展開選單時看到的主線

1. 一句話目的：RAG 像先翻書再回答；Memory 像把值得記住的事情放進筆記本。
2. `📌` 四到五個可驗證學習目標。
3. `🧩` 七個可見核心詞；第一次出現時加粗，並各有白話定義、生活比喻、正確術語與本章用途：
   - **Retrieval（檢索）**
   - **RAG（Retrieval-Augmented Generation）**
   - **Embedding（嵌入向量）**
   - **Vector Store／Vector Database**
   - **Chunk（文字片段）**
   - **Reranking（重新排序）**
   - **Memory（記憶）**
4. 一張亮色三語概念圖：文件進入知識庫的 ingest path、問題進來的 query path，以及 Memory 的 write／read 回路。
5. 一張短版選擇表：long context、RAG、Memory、fine-tuning 各自解決什麼，不宣稱固定成本或絕對優劣。
6. `🚪` 初學路線與進階路線；時間、環境、費用放在關閉區。
7. `📚` 必修閱讀標題與一句閱讀目的；完整連結及閱讀順序預設收合。
8. `🛠` 五個練習的標題、既有 anchor、一句成果與可直接複製的最短命令保持可見：Embedding → Vector DB → Chunking → 完整 RAG → Memory 基本讀寫。真正跨次持久化由 06B 修好範例後才可宣稱。
9. 一個推薦小專案：讓助理讀自己的小文件集，回答時附來源，再記住一項使用者偏好。
10. `🎯` 每類一個推薦入口；完整 18 筆資源表預設收合。
11. `✅` 短版自我檢查與 Stage 07 入口。

## 預設收合內容

- 時間、先備知識、環境、費用、API key 與資料隱私提醒。
- 完整必修閱讀與順序。
- 基礎 RAG 的完整 ingest／query pipeline 說明。
- GraphRAG、Contextual Retrieval、Hybrid Search、BM25、Reranking、HyDE、Multi-Query、RAG Fusion、Self-RAG、CRAG、Adaptive RAG、RAPTOR、DSPy。
- working／long-term／episodic／semantic／procedural memory、CoALA、Generative Agents、Reflexion。
- chunking 深入比較、RAG／Memory eval、研究 survey 與安全風險。
- 完整資源表、替代方案、排錯與其餘專案靈感。

所有 `<details markdown="1">` 預設關閉，不使用 `open`；展開後的 heading、粗體、連結與 code fence 必須由 MkDocs 正常渲染，不能顯示原始 Markdown。重要 heading、anchor、核心定義、練習成果與第一步不得藏入 `<details>`。

## 代表專案選擇規則

事實只由官方文件、規格、paper、model card 或 canonical repository 證明；知名或活躍專案只負責提供動手路徑。人氣不取代 license、維護狀態、安全、用途與限制查核。

06A 優先保留並重新定位：

- RAG framework：LlamaIndex、LangChain、Haystack、RAGFlow。
- 本地與資料庫：Chroma、Qdrant、pgvector、Weaviate、LanceDB。
- Graph／advanced RAG：Microsoft GraphRAG（維護中）、LightRAG。
- Memory：Mem0、Letta Code、Graphiti、LangMem；Zep Cloud 清楚標成服務，Zep Community Edition 放歷史狀態。
- Evaluation：Ragas（canonical owner `vibrantlabsai`）、TruLens、LangSmith。
- 可讀實作：Onyx、RAG_Techniques、DSPy；中文專案若維護較慢，保留時必須標示狀態，不以過去人氣掩蓋更新停滯。

每列固定為：`分類｜專案｜編輯評分｜適合誰｜能學什麼｜狀態／限制｜官方來源`。同類型使用真正 `rowspan`。

## 06A 檔案責任

- `stages/06-memory-rag.md`
- `stages/06-memory-rag.en.md`
- `stages/06-memory-rag.zh-Hans.md`
- `resources/diagrams/rag-memory-map.png`
- `resources/diagrams/rag-memory-map.en.png`
- `resources/diagrams/rag-memory-map.zh-Hans.png`
- `resources/glossary.md`
- `resources/glossary.en.md`
- `resources/glossary.zh-Hans.md`
- `stages/DESIGN.md`
- `scripts/reader-ux-pages.yml`
- `scripts/freshness-models.yml`
- `scripts/repository-freshness-snapshot.json`
- `scripts/test_stage06_content.py`
- `docs/TESTING_PLAN.md`（只有測試清單需要新增時才改）
- `CHANGELOG.md`
- 本計畫檔。

既有 `agent-engineering-5layer*`、`rag-pipeline-overview*`、`chunking-strategies*`、`reflexion-persistent-memory-loop*` 先做引用與任務價值審計。只有新概念圖確實取代且全 repo 引用為零的圖才刪除；不為了縮小頁面任意刪圖。

## 06B 檔案責任

- `examples/stage-6/01-embeddings/`
- `examples/stage-6/02-vector-db/`
- `examples/stage-6/03-chunking-comparison/`
- `examples/stage-6/04-full-rag-pipeline/`
- `examples/stage-6/05-long-term-memory/`
- `scripts/test_stage06_examples.py`
- `docs/TESTING_PLAN.md`
- `CHANGELOG.md`

06B 必須另建 worktree／branch，疊在 06A 最終 commit 上，不混入 06A staged diff。

## 官方事實包（06A）

查核日：`2026-08-28 UTC`。優先來源：

- LangChain Retrieval：`https://docs.langchain.com/oss/python/langchain/retrieval`
- LangGraph Agentic RAG：`https://docs.langchain.com/oss/python/langgraph/agentic-rag`
- LlamaIndex concepts：`https://developers.llamaindex.ai/python/framework/getting_started/concepts/`
- Anthropic Contextual Retrieval：`https://www.anthropic.com/engineering/contextual-retrieval`
- Microsoft GraphRAG：`https://github.com/microsoft/graphrag`、`https://microsoft.github.io/graphrag/`
- Ragas：`https://github.com/vibrantlabsai/ragas`、`https://docs.ragas.io/`
- Mem0：`https://github.com/mem0ai/mem0`、`https://docs.mem0.ai/`
- Letta：`https://github.com/letta-ai/letta-code`、`https://docs.letta.com/`
- LangMem：`https://github.com/langchain-ai/langmem`
- Zep／Graphiti：`https://github.com/getzep/zep`、`https://github.com/getzep/graphiti`
- Chroma、Qdrant、pgvector、Weaviate、LanceDB 的 canonical docs／repos。

`scripts/freshness-models.yml` 新增 Stage 06 fact pack，scope 固定為：

`rag,retrieval,embeddings,vector-stores,memory,evaluation,project-status`

三語 marker 日期一致，`max_age_days=90`。可見日期只在最相關的關閉資源區用 `<small>` 顯示，不加「不代表永遠」等贅句。

### Task 1: 寫 Stage 06 regression contract

**Files:** `scripts/test_stage06_content.py`、`scripts/reader-ux-pages.yml`

1. 先寫失敗測試：七個核心詞、路標順序、五個可見練習、`max_open_details: 0`、資源 rowgroups、URL／評分 parity、GraphRAG／Ragas／Letta／Zep 狀態與 forbidden stale literals。
2. 執行 `python -m pytest scripts/test_stage06_content.py -q`，確認在舊內容上失敗。
3. 把 Stage 06 加入 reader-UX config，暫不放寬到會讓舊頁誤過的門檻。
4. 再跑測試，保留內容尚未修正造成的預期失敗證據。

### Task 2: 完成繁中 canonical 06A

**Files:** `stages/06-memory-rag.md`、`resources/glossary.md`、`stages/DESIGN.md`

1. 重寫可見主線與七個核心詞。
2. 依 RAG → 練習 → Memory → 評測重排；進階研究內容移入關閉 details，不刪核心名詞。
3. 五個練習保留 heading、anchor、成果、最短命令與預算／隱私提醒。
4. 把 18 筆資源改成 accessible rowgroups，保留編輯評分，移除 stars 數字。
5. 修正 GraphRAG、Ragas、Letta、Zep、embedding 與 glossary 的直接矛盾。
6. 執行繁中 anchor、reader-UX、Markdown 與 MkDocs build。

### Task 3: 產生並驗收三語概念圖

**Files:** `resources/diagrams/rag-memory-map*.png`

1. 使用 `imagegen` 產生亮底、低文字密度的繁中图：左側 ingest、右側 query、下方 memory write/read，箭頭不可互相矛盾。
2. 以相同構圖產生英文與簡中；節點、箭頭、數量與限制完全一致。
3. 原尺寸人工檢查文字、繁簡、對比、箭頭與裁切。
4. 執行 image locale gate 與三語 MkDocs build。
5. 只有全 repo 引用為零時，才刪被新圖確實取代的舊圖。

### Task 4: 完成英文與簡中 mirror

**Files:** `stages/06-memory-rag.en.md`、`stages/06-memory-rag.zh-Hans.md`、`resources/glossary.en.md`、`resources/glossary.zh-Hans.md`

1. 以通過繁中 gate 的 canonical 為唯一語意來源。
2. 三語維持相同 heading、details、URL、評分、狀態、日期、命令與限制。
3. 每個核心詞第一次出現都加粗；簡中做自然在地化，不用刪字替代翻譯。
4. 檢查空引號、locale links、繁簡殘留與 anchor parity。

### Task 5: 加入 freshness 與資源 ratchet

**Files:** `scripts/freshness-models.yml`、`scripts/repository-freshness-snapshot.json`、`scripts/test_stage06_content.py`

1. 加 Stage 06 fact pack、verified pages、90 日提醒與三語 marker。
2. 全量重掃實際引用的 GitHub repositories；更新 canonical redirect、archive、license 與 stale snapshot。
3. 禁止 `text-embedding-ada-002` 推薦、舊 Ragas owner、GraphRAG Apache-2.0、Letta V1 當現行 source、Zep CE 當現行產品、GitHub stars 數字與空引號。
4. 保留論文或歷史內容所需的明確 historical／maintenance 例外。

### Task 6: 三層驗證

順序固定為：機器 gate → 元素落腳審計 → 三語語意鏡像比對。

至少執行：

```powershell
git diff --check
python scripts/check-stage-template.py
python scripts/check-anchors.py --strict
python -m pytest scripts/test_anchor_slug_parity.py -q
python scripts/check-mirror-parity.py
python scripts/check-locale-links.py
python scripts/check-hans-chars.py
python scripts/check-image-locale.py
python scripts/check-duplicate-repos.py
python scripts/check-reader-ux.py
python scripts/check-2026-freshness.py
python -m pytest scripts -q
python scripts/build-docs-tree.py
python -m mkdocs build
$env:LANG = 'en'; python -m mkdocs build
$env:LANG = 'zh-Hans'; python -m mkdocs build
```

人工驗收：

- 不展開任何 details，讀者能說出 RAG 與 Memory 的差別並開始 Exercise 1。
- 七個核心詞粗體、白話、比喻、正式術語與用途完整。
- 五個練習、重要 icon、heading、anchor、評分與官方 URL 都有新落腳。
- 研究名詞沒有因精簡而消失；初學主線不被 survey 淹沒。
- 三語圖同構，沒有把 vendor benchmark 畫成普遍事實。
- 日期在小字／關閉區；沒有空引號與多餘永久性聲明。

### Task 7: Review、commit、push、開 06A PR

1. 逐檔 `git add <path>`，斷言 staged 清單與凍結清單完全一致。
2. 記錄 staged tree／fingerprint。
3. 對最終 staged diff 執行一次獨立 `code-reviewer`；任何修改都讓 ack 過期。
4. 重跑受影響 gate、重新 stage、重新 review；禁止 `--no-verify`。
5. Commit：`content(stage6): make RAG and memory easier to learn`。
6. Push 並開 stacked PR，base 為 `codex/stage05-example-hardening`。
7. 等 checks 全綠，只回報狀態；不 merge、不 cleanup。

### Task 8: 建立 06B 範例強化層

1. 從 06A 最終 commit 建 `codex/stage06-example-hardening` 與新 worktree。
2. 先用測試重現 overlap 無限迴圈、固定 collection 舊資料、非持久 memory 與非離線依賴。
3. 修正五個 Path A／B starter、README、requirements 與測試；命令同時提供 PowerShell 與 POSIX。
4. 至少驗證：輸入邊界、collection 隔離、真正 persistent store、offline contract、兩條 SDK path 與 Python 支援範圍。
5. 執行 Stage 06 專用測試、全 scripts suite、三語 build 與獨立 review。
6. Commit：`test(stage6): harden the RAG and memory exercises`。
7. Push 並開 stacked PR，base 為 `codex/stage06-reader-ux`；不 merge、不 cleanup。

## 停止條件

- 官方來源與正文衝突：停止該段寫作，先解決事實。
- 同期修改碰到相同檔案：整合最新上游，不覆蓋；舊 fingerprint／review ack 作廢。
- 零 checks、PENDING、空狀態或 failure：停止，不 merge。
- 使用者未明確說「可以合併」：保留 OPEN PR、upstream branch 與 worktree。

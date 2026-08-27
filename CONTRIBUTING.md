# 貢獻指南

> **繁體中文** | [简体中文](./CONTRIBUTING.zh-Hans.md) | [English](./CONTRIBUTING.en.md)

謝謝你考慮貢獻。**這是一份精選的學習路線圖，不是百科目錄。品質 > 數量。**

這個 repo **本來就是設計給社群一起改良的**——一個人 curate 永遠跟不上 AI agent 生態的變化速度。Maintainer 一個季度跑 1 次 review 不夠，需要更多眼睛看。

這份 catalog 分**兩條軌道**：**Track A**（CLI Power User，`tracks/cli/A1-A3`）跟 **Track B**（Agent Builder，`stages/03-07`）。貢獻時請註明你動的是哪條軌道——兩條的 audience 不一樣。

## 🚪 第一次貢獻：好上手的 5 個切入點

不確定從哪開始？挑一個你 30 分鐘內能做完的：

1. **🐛 回報過時 entry**：跑 `python scripts/refresh-stars.py` 找星數差距大的 repo，開 issue 說「這個應該移除 / 更新」
2. **🔗 修一個失效連結**：你看 stage X 時連結 404 了，直接 PR 改
3. **✍️ 補一個 entry 的 `怎麼跑` section**：很多 entry 沒寫安裝指令，你跑過就補上
4. **🌏 補英文 companion 沒翻好的句子**：找一個 `.en.md` 跟 zh 對照，你覺得翻得不順的地方改一行
5. **💬 對某個 entry 加個人筆記**：你跑過 `練習 3` 卡某個地方，補一句「注意：xxx」

這 5 種都不用先讀完整份 style-guide，merge 速度也快——適合第一次貢獻、累積信心。

> 🧪 **想跑 walkthrough / build script / CI workflow 第一次？** 看 [`.github/TESTING-STATUS.md`](.github/TESTING-STATUS.md)——這份**誠實揭露**哪些 code maintainer 真的跑過、哪些只 syntax check、哪些完全沒測。第一個踩到坑的人開 issue + PR 是 highest-value contribution。

## 我們接受什麼

### 高價值 PR
- **新增 project** 到某個 stage，並說明為什麼這個 project 對應該階段的學習
- **翻譯** 某個 stage 頁面成繁中（只要繁中——我們不收 zh-Hans）
- **標記停滯 / 失維護的 project**（請先開 issue）
- **改善現有 project 的策展備註**（讓「教什麼」說明更清楚）
- **重新整理** 某個 stage 內部順序，如果現在的順序不符合學習進程

### 較低優先（仍然歡迎）
- 錯字修正
- 連結修正（請先用 `curl -I` 驗證）
- Stage 介紹文字優化

### 不接受
- 沒有策展理由的批量加 repo
- 沒有教學價值的自我推銷
- 沒文件的 project
- 沒明確 license 的 project

## 怎麼新增一個 project

每一個 project 在 stage 頁面內應該照這個格式：

```markdown
### [Project Name](url)

| 欄位 | 內容 |
|---|---|
| 語言 | Python / TS / etc. |
| Stars | ★ k |
| License | MIT / Apache 2 / ... |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：核心學習一句話總結。

**適合誰**：誰應該讀這個、為什麼。

**備註**：1-3 句的個人評價。哪裡好、哪裡弱、哪裡可以跳。

**怎麼跑**：
\`\`\`bash
# 最小安裝 / 第一次跑的指令
\`\`\`
```

## 策展標準

值得列入的 project 必須：

1. **有維護**：最近 6 個月內有 commit，或明確標示「stable, no longer maintained」
2. **有 hello-world 文件**：讀者應該能在 30 分鐘內把東西跑起來
3. **明確 license**：MIT、Apache 2、BSD 或類似。避免沒 license 的 repo。
4. **可信賴的維護者**：知名組織、公司，或有口碑的個人

自動檢查會合併同一個 repo 的重複連結，查它是否搬家、封存、停用，以及 GitHub 顯示的 SPDX license。半年沒更新只是一個請你再看一眼的提醒：穩定而且仍有教學價值的專案可以保留，但要把狀態寫清楚。若 GitHub API 暫時失敗，結果會標成「無法確認」，不會假裝一切正常。

## 雙語風格

- **繁中（Traditional Chinese, zh-TW）為正本**，英文版（`*.en.md`）是 companion。
- **不接受 zh-Hans PR**。如果你交 zh-Hans 的 PR，我們會請你轉成繁中。
- **自然翻譯**，不要逐字對譯。技術詞如果直接用英文比較自然，就保留英文（「使用 LangGraph 建 multi-agent 系統」）。
- **完整風格規範請看 [`resources/style-guide.md`](resources/style-guide.md)**——禁用詞、entry schema、license 標註慣例、寫作風格、推薦星等定義都在裡面。PR 之前請先讀。

## 流程

1. 新 project 或大幅重組請先開 issue
2. 一次一個 stage，PR 範圍要聚焦
3. 等審查（通常 7 天）
4. Reviewer 可能會問你「為什麼這個 project 教這個 stage」

## 要避免的反模式

- ❌ 「leverage」、「delve」、「comprehensive」、「robust」（LLM tell）
- ❌ 過度行銷（「revolutionary」、「game-changing」）
- ❌ 只因為熱門就列上來
- ❌ 大段引用 project 自己的行銷文案

## 擔任 Stage / Branch 維護者

除了交一次性 PR，也歡迎擔任**特定 stage 或 branch 的長期維護者**——負責定期 review、處理該領域的 issue、把關該領域的 PR。

自薦流程：

1. 開一個 issue，標題 `[maintainer] Stage N — your-handle` 或 `[maintainer] for-X branch — your-handle`
2. 講清楚你願意 commit 多久（建議至少一季 = 3 個月）
3. 簡述你在這個領域的背景

詳見 [`CONTRIBUTORS.md`](CONTRIBUTORS.md)。每個 stage / branch 的 maintainer 名單都在那邊。

## License

貢獻即代表你同意你的內容以 MIT 授權。

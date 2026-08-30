#!/usr/bin/env bash
# build-pdf.sh — 把整個 awesome-agentic-ai-zh 編譯成單一 PDF
#
# 用法：
#   bash scripts/build-pdf.sh             # 預設輸出 dist/awesome-agentic-ai-zh.pdf (zh-TW)
#   LANG_VARIANT=en bash scripts/build-pdf.sh  # 英文版
#
# 依賴：
#   - pandoc (>= 3.0)
#   - xelatex (TeX Live with CJK support, e.g. texlive-xetex + texlive-lang-chinese)
#   - mermaid-cli 跟 pandoc-mermaid filter（選用，沒裝 mermaid 圖會被當 code block 顯示）
#
# 安裝（macOS）：
#   brew install pandoc
#   brew install --cask mactex-no-gui   # or mactex
#
# 安裝（Linux）：
#   sudo apt install pandoc texlive-xetex texlive-lang-chinese texlive-fonts-recommended
#
# 安裝（Windows）：
#   choco install pandoc miktex
#   或下載 https://pandoc.org/installing.html + https://miktex.org/

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

LANG_VARIANT="${LANG_VARIANT:-zh}"   # zh | en
DIST_DIR="dist"
mkdir -p "$DIST_DIR"

# Font defaults — overridable via env vars
# 例：CJK_FONT="PingFang TC" bash scripts/build-pdf.sh
CJK_FONT="${CJK_FONT:-Noto Sans CJK TC}"
MAIN_FONT="${MAIN_FONT:-DejaVu Sans}"

if [[ "$LANG_VARIANT" == "en" ]]; then
  SUFFIX=".en"
  TITLE="awesome-agentic-ai-zh — Learning Roadmap"
  SUBTITLE="A 10-stop path: 8 topic stages plus Stage 0 readiness and the Stage 7.5 reading stop"
  OUT_PDF="$DIST_DIR/awesome-agentic-ai-zh.en.pdf"
else
  SUFFIX=""
  TITLE="awesome-agentic-ai-zh — AI Agent 學習地圖"
  SUBTITLE="從第一行 LLM API 到自己打造多 agent 系統"
  OUT_PDF="$DIST_DIR/awesome-agentic-ai-zh.pdf"
fi

echo "Building PDF (variant: $LANG_VARIANT) → $OUT_PDF"

# 組合檔案順序（main path 為主；branches 跟 walkthroughs 也納入）
FILES=(
  "README${SUFFIX}.md"
  "stages/00-foundations${SUFFIX}.md"
  "stages/01-llm-basics${SUFFIX}.md"
  "stages/02-prompt-engineering${SUFFIX}.md"
  "stages/03-tool-use-and-hello-agent${SUFFIX}.md"
  "stages/04-agent-frameworks${SUFFIX}.md"
  "stages/05-claude-code-ecosystem${SUFFIX}.md"
  "stages/06-memory-rag${SUFFIX}.md"
  "stages/07-multi-agent-production${SUFFIX}.md"
  "branches/for-researcher${SUFFIX}.md"
  "branches/for-developer${SUFFIX}.md"
  "branches/for-knowledge-worker${SUFFIX}.md"
  "branches/for-teacher${SUFFIX}.md"
  "walkthroughs/build-first-agent-in-7-steps${SUFFIX}.md"
  "CONTRIBUTING${SUFFIX}.md"
)

# 確認所有檔案存在
for f in "${FILES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "ERROR: missing file: $f" >&2
    exit 1
  fi
done

# 中介檔案：把所有 .md 串起來
TMP_MD="$(mktemp -t aaai-XXXXXX.md)"
trap 'rm -f "$TMP_MD"' EXIT

# 加 metadata header
cat > "$TMP_MD" <<EOF
---
title: "$TITLE"
subtitle: "$SUBTITLE"
author: "@WenyuChiou"
date: "$(date +%Y-%m-%d)"
mainfont: "$MAIN_FONT"
CJKmainfont: "$CJK_FONT"
geometry: margin=2.5cm
toc: true
toc-depth: 2
numbersections: true
linkcolor: blue
documentclass: report
---

EOF

# 串接每個檔案，加 page break
for f in "${FILES[@]}"; do
  echo "" >> "$TMP_MD"
  echo "\\newpage" >> "$TMP_MD"
  echo "" >> "$TMP_MD"
  cat "$f" >> "$TMP_MD"
done

echo "Concatenated $(wc -l < "$TMP_MD") lines."

# 把 mermaid block 換成 code block（沒裝 filter 時，避免 pandoc 卡住）
# 真要 render mermaid，得另外裝 pandoc-mermaid 或先用 mermaid-cli 把 ```mermaid 轉成圖
sed -i.bak 's/^```mermaid$/```/' "$TMP_MD" 2>/dev/null || \
  sed -i '' 's/^```mermaid$/```/' "$TMP_MD"   # macOS sed
rm -f "${TMP_MD}.bak"

# 跑 pandoc
pandoc "$TMP_MD" \
  --pdf-engine=xelatex \
  --output="$OUT_PDF" \
  -V linkcolor=blue \
  -V geometry:margin=2.5cm \
  --highlight-style=tango \
  || {
    echo ""
    echo "❌ PDF build failed. 常見原因：" >&2
    echo "  - xelatex 沒裝（apt install texlive-xetex）" >&2
    echo "  - CJK font 沒裝（apt install texlive-lang-chinese 或裝 Noto Sans CJK TC）" >&2
    echo "  - 用 -V CJKmainfont=<your-font> 覆寫" >&2
    exit 1
  }

echo ""
echo "✅ Built $OUT_PDF ($(du -h "$OUT_PDF" | cut -f1))"

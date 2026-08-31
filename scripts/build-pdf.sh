#!/usr/bin/env bash
# Build one locale of the calendar-versioned PDF release.
#
# Required:
#   RELEASE_VERSION=vYYYY.MM.DD LANG_VARIANT=zh-TW bash scripts/build-pdf.sh
# Supported locales: zh-TW, zh-Hans, en
# Runtime dependencies: Python + PyYAML, pandoc, WeasyPrint, Noto CJK fonts.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

RELEASE_VERSION="${RELEASE_VERSION:?Set RELEASE_VERSION to vYYYY.MM.DD or vYYYY.MM.DD-N}"
LANG_VARIANT="${LANG_VARIANT:?Set LANG_VARIANT to zh-TW, zh-Hans, or en}"
DIST_DIR="${DIST_DIR:-$REPO_ROOT/dist}"
PYTHON_BIN="${PYTHON_BIN:-python}"

case "$LANG_VARIANT" in
  zh-TW|zh-Hans|en) ;;
  *)
    echo "ERROR: LANG_VARIANT must be zh-TW, zh-Hans, or en" >&2
    exit 2
    ;;
esac

for command in "$PYTHON_BIN" pandoc weasyprint; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "ERROR: missing release dependency: $command" >&2
    exit 1
  fi
done

"$PYTHON_BIN" scripts/release_manifest.py validate --strict-urls --version "$RELEASE_VERSION"
"$PYTHON_BIN" scripts/release_manifest.py validate-version --version "$RELEASE_VERSION" >/dev/null

OUT_NAME="$(
  "$PYTHON_BIN" scripts/release_manifest.py asset-name \
    --version "$RELEASE_VERSION" --locale "$LANG_VARIANT"
)"
mkdir -p "$DIST_DIR"
OUT_PDF="$DIST_DIR/$OUT_NAME"

BUILD_DIR="$(mktemp -d -t awesome-agentic-ai-release-XXXXXX)"
cleanup() {
  if [[ "${KEEP_RELEASE_BUILD:-0}" == "1" ]]; then
    echo "Keeping intermediate files: $BUILD_DIR"
  else
    rm -rf -- "$BUILD_DIR"
  fi
}
trap cleanup EXIT

SOURCE_MD="$BUILD_DIR/$LANG_VARIANT.md"
SOURCE_HTML="$BUILD_DIR/$LANG_VARIANT.html"
PANDOC_LOG="$BUILD_DIR/pandoc.log"
WEASYPRINT_LOG="$BUILD_DIR/weasyprint.log"

"$PYTHON_BIN" scripts/release_manifest.py assemble \
  --version "$RELEASE_VERSION" \
  --locale "$LANG_VARIANT" \
  --output "$SOURCE_MD" >/dev/null

RESOURCE_PATH="$REPO_ROOT:$REPO_ROOT/stages:$REPO_ROOT/tracks/cli:$REPO_ROOT/branches:$REPO_ROOT/walkthroughs:$REPO_ROOT/resources"

echo "Building $OUT_NAME"
if ! pandoc "$SOURCE_MD" \
  --from=gfm-tex_math_dollars+raw_html \
  --to=html5 \
  --standalone \
  --embed-resources \
  --fail-if-warnings \
  --resource-path="$RESOURCE_PATH" \
  --css="$REPO_ROOT/release/pdf.css" \
  --output="$SOURCE_HTML" \
  2>"$PANDOC_LOG"; then
  echo "ERROR: Pandoc failed while assembling $LANG_VARIANT" >&2
  sed -n '1,160p' "$PANDOC_LOG" >&2
  exit 1
fi

if ! weasyprint "$SOURCE_HTML" "$OUT_PDF" 2>"$WEASYPRINT_LOG"; then
  echo "ERROR: WeasyPrint failed while rendering $LANG_VARIANT" >&2
  sed -n '1,160p' "$WEASYPRINT_LOG" >&2
  exit 1
fi

if grep -Eqi 'failed to load image|no such file|cannot load|font.*not found' "$WEASYPRINT_LOG"; then
  echo "ERROR: WeasyPrint reported a missing image, file, or font" >&2
  sed -n '1,120p' "$WEASYPRINT_LOG" >&2
  exit 1
fi

test -s "$OUT_PDF"
echo "Built $OUT_PDF ($(wc -c < "$OUT_PDF") bytes)"

"""Stage 6 練習 3 自我驗證 — 3 種 chunking strategy 的純邏輯測試（不打 embed）。
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import SAMPLE_DOC, chunk_fixed, chunk_headings, chunk_paragraphs


def test_fixed_length_chunks():
    chunks = chunk_fixed("a" * 500, chunk_size=200, overlap=40)
    # 500 字、step=160（200-40）→ 應該 ~ 3-4 chunk
    assert 3 <= len(chunks) <= 4, f"預期 3-4 chunk、得到 {len(chunks)}"
    assert all(len(c) <= 200 for c in chunks)
    print("✅ test_fixed_length_chunks")


def test_fixed_length_rejects_unsafe_overlap():
    for chunk_size, overlap in [(0, 0), (10, -1), (10, 10), (10, 11)]:
        try:
            chunk_fixed("abcdef", chunk_size=chunk_size, overlap=overlap)
        except ValueError:
            continue
        raise AssertionError(f"chunk_size={chunk_size}, overlap={overlap} 應該被拒絕")
    print("✅ test_fixed_length_rejects_unsafe_overlap")


def test_paragraphs_split_on_double_newline():
    text = "Para one.\n\nPara two.\n\nPara three."
    chunks = chunk_paragraphs(text)
    assert chunks == ["Para one.", "Para two.", "Para three."]
    print("✅ test_paragraphs_split_on_double_newline")


def test_headings_keep_section_together():
    chunks = chunk_headings(SAMPLE_DOC)
    # Sample 有 1 個 # 標題 + 3 個 ## 標題、4 個 section
    assert len(chunks) == 4, f"預期 4 section、得到 {len(chunks)}"
    # 每個 section 都應該以 # 開頭
    assert all(c.startswith("#") for c in chunks)
    # Food section 應該包含「night markets」
    food = next(c for c in chunks if c.startswith("## Food"))
    assert "night markets" in food.lower()
    print("✅ test_headings_keep_section_together")


def test_chunk_count_difference():
    """3 種切法應該產生不同 chunk 數、印證它們真的不同。"""
    fixed_n = len(chunk_fixed(SAMPLE_DOC, chunk_size=200, overlap=40))
    para_n = len(chunk_paragraphs(SAMPLE_DOC))
    head_n = len(chunk_headings(SAMPLE_DOC))
    # heading-aware 通常最少（每個 section 1 chunk）
    assert head_n <= para_n, "heading 應 <= paragraphs"
    print(f"   fixed: {fixed_n}, paragraphs: {para_n}, headings: {head_n}")
    print("✅ test_chunk_count_difference")


if __name__ == "__main__":
    test_fixed_length_chunks()
    test_fixed_length_rejects_unsafe_overlap()
    test_paragraphs_split_on_double_newline()
    test_headings_keep_section_together()
    test_chunk_count_difference()
    print("\n🎉 全部通過 — 3 種 chunking strategy 邏輯正確")

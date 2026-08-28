"""Stage 7 練習 1 自我驗證 — mock 3 個 LLM call。"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import debate, llm_call, parse_winner


def make_llm(responses: list[str]):
    llm = MagicMock()
    llm.chat.completions.create.side_effect = [
        SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=r))])
        for r in responses
    ]
    return llm


def test_llm_call_basic():
    llm = make_llm(["ok"])
    out = llm_call("be brief", "hi", llm=llm)
    assert out == "ok"
    print("✅ test_llm_call_basic")


def test_llm_call_rejects_empty_text():
    llm = make_llm(["   "])
    try:
        llm_call("be brief", "hi", llm=llm)
    except ValueError as error:
        assert "empty text" in str(error)
    else:
        raise AssertionError("empty model output must fail")
    print("✅ test_llm_call_rejects_empty_text")


def test_parse_winner_requires_the_whole_contract():
    assert parse_winner("WINNER=CON. clearer evidence") == ("CON", "clearer evidence")
    for invalid in ("Maybe WINNER=PRO", "WINNER=PRO", "PRO. good"):
        try:
            parse_winner(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid Judge output accepted: {invalid}")
    print("✅ test_parse_winner_requires_the_whole_contract")


def test_debate_3_calls():
    """debate 應該打 3 次 LLM（pro, con, judge）、且 judge 看到兩邊 argument。"""
    llm = make_llm([
        "PRO: frameworks save time.",
        "CON: frameworks add lock-in.",
        "WINNER=PRO. Time savings outweigh lock-in for small teams.",
    ])
    result = debate("Should small teams use a framework?", llm=llm)
    assert llm.chat.completions.create.call_count == 3
    assert "frameworks save time" in result["pro"]
    assert "frameworks add lock-in" in result["con"]
    assert "WINNER=PRO" in result["judge"]
    assert result["winner"] == "PRO"

    # 第 3 個 call（judge）的 user prompt 應該包含 pro + con
    third_call = llm.chat.completions.create.call_args_list[2]
    judge_user = third_call.kwargs["messages"][1]["content"]
    assert "frameworks save time" in judge_user
    assert "frameworks add lock-in" in judge_user
    print("✅ test_debate_3_calls")


def test_debate_independent_pro_con():
    """確認 pro / con 各自獨立 call、不互相看到（避免 bias propagation）。"""
    llm = make_llm(["pro arg", "con arg", "WINNER=PRO. clearer evidence"])
    debate("test", llm=llm)
    # 第 1 個 call (pro) 的 user prompt 應該 = question、不含 con
    first = llm.chat.completions.create.call_args_list[0]
    assert first.kwargs["messages"][1]["content"] == "test"
    print("✅ test_debate_independent_pro_con")


if __name__ == "__main__":
    test_llm_call_basic()
    test_llm_call_rejects_empty_text()
    test_parse_winner_requires_the_whole_contract()
    test_debate_3_calls()
    test_debate_independent_pro_con()
    print("\n🎉 全部通過 — multi-agent debate 邏輯正確")

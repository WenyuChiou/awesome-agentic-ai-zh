"""Offline contract for the source-backed Haiku 5.5 documentation update."""
from __future__ import annotations

import ast
import contextlib
import io
from pathlib import Path
import re
import sys
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ('', '.en', '.zh-Hans')


def snippets(locale):
    text = (ROOT / f'stages/01-llm-basics{locale}.md').read_text(encoding='utf-8')
    return text, re.findall(r'```python\n(.*?)\n```', text, re.S)


@pytest.mark.parametrize('locale', LOCALES)
def test_current_haiku_facts_and_historical_boundary(locale):
    text, code = snippets(locale)
    row = next(line for line in text.splitlines() if line.startswith('| Claude |'))
    assert 'Haiku 5.5 (`claude-haiku-5-5`)' in row
    assert 'Haiku 4.5' not in row
    assert '1M' in row and '128K' in row and '200K' not in row
    assert 'US$0.10/$0.50' in row and 'US$0.50/$2.50' in row
    assert '≤100K' in row and '>100K' in row
    assert 'Sonnet cache read US$0.10' in row
    assert '2026-10-07' in text and '2026-10-08 UTC' in text
    assert 'verified_on=2026-09-22' in text
    assert 'https://www.anthropic.com/claude-haiku-5-5' in text
    assert 'https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide' in text
    assert 'Haiku 4.5' in text and 'temperature' in text
    assert any('model="claude-haiku-4-5", max_tokens=80, temperature=1.0' in c for c in code)


@pytest.mark.parametrize('locale', LOCALES)
def test_haiku_first_call_accepts_thinking_before_text(locale, monkeypatch):
    _, code = snippets(locale)
    first = next(c for c in code if 'model="claude-haiku-5-5"' in c)
    calls = []

    def create(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(
            content=[SimpleNamespace(type='thinking', thinking='', signature='opaque'),
                     SimpleNamespace(type='text', text='Hello'),
                     SimpleNamespace(type='text', text=' world')],
            usage=SimpleNamespace(input_tokens=15, output_tokens=20), stop_reason='end_turn')

    monkeypatch.setitem(sys.modules, 'anthropic', SimpleNamespace(
        Anthropic=lambda: SimpleNamespace(messages=SimpleNamespace(create=create))))
    namespace = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(first, f'first-call{locale}', 'exec'), namespace)
    assert namespace['text'] == 'Hello world'
    assert len(calls) == 1
    assert calls[0]['model'] == 'claude-haiku-5-5'
    assert calls[0]['max_tokens'] == 4096
    assert calls[0]['output_config'] == {'effort': 'low'}
    assert not {'temperature', 'top_p', 'top_k'} & calls[0].keys()
    assert calls[0]['messages'][-1]['role'] == 'user'


@pytest.mark.parametrize('locale', LOCALES)
def test_haiku_price_boundary_and_other_model_rates(locale):
    _, code = snippets(locale)
    cost = next(c for c in code if 'def rates_for(' in c)
    tree = ast.parse(cost)
    definitions = [node for node in tree.body
                   if isinstance(node, ast.FunctionDef)
                   or (isinstance(node, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == 'PRICING' for t in node.targets))]
    namespace = {}
    exec(compile(ast.Module(body=definitions, type_ignores=[]), 'pricing', 'exec'), namespace)
    rates_for = namespace['rates_for']
    assert rates_for('claude-haiku-5-5', 100_000) == {'input': .10, 'output': .50}
    assert rates_for('claude-haiku-5-5', 100_001) == {'input': .50, 'output': 2.50}
    assert rates_for('claude-sonnet-5-5', 100_001) == {'input': 2., 'output': 10.}
    assert 'rates = rates_for(MODEL, in_tok)' in cost
    assert 'r = rates_for(name, in_tok)' in cost
    assert 'not measured cross-model costs' in cost


def test_fact_pack_tracks_only_anthropic_reverification():
    import yaml
    pack = yaml.safe_load((ROOT / 'scripts/freshness-models.yml').read_text())
    assert pack['stage01_fact_pack']['provider_updates']['anthropic'] == '2026-10-08'
    assert pack['stage01_fact_pack']['verified_on'] == '2026-09-22'
    assert pack['stage01_fact_pack']['official_sources']['claude_haiku'].endswith('/haiku-5-5/overview')
    assert 'Haiku 5.5' in pack['current_frontier_models']['anthropic']

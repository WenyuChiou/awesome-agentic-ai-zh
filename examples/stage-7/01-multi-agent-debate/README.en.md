<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 1: Let Three Agents Debate

You will make three roles: PRO argues yes, CON argues no, and a Judge reads both sides before choosing one.

Pairs with Exercise 1 in [Stage 7 — Agent Production Engineering: Harness, Loops, and Graphs](../../../stages/07-multi-agent-production.en.md).

## 🎯 Learning goals

- Explain **Multi-Agent**: several agents divide one job.
- Let PRO and CON answer independently so one does not seed the other's answer.
- Parse the Judge with a strict format; stop on bad output instead of guessing.

## Run the model-free tests first

Open PowerShell in this folder and copy:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

Two `🎉` messages mean the three calls, empty-output checks, and Judge format passed. These tests use fake replies and never contact a model.

<details markdown="1">
<summary>Path A: Run a real debate with Ollama</summary>

1. Install [Ollama](https://ollama.com/), then prepare the model:

   ```powershell
   ollama pull qwen3.5:4b
   ollama serve
   ```

2. Open another PowerShell window:

   ```powershell
   .\.venv\Scripts\python.exe starter.py
   ```

Ollama does not charge a provider model API fee. Downloads, electricity, hardware, and your time still have costs. Wait for completion instead of treating a fixed number of seconds as a failure rule.

</details>

<details markdown="1">
<summary>Path B: Compare with Anthropic and control spend</summary>

```powershell
$env:ANTHROPIC_API_KEY = "paste-your-key"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

This exercise calls the model three times. Haiku 4.5 costs `$1 / 1M` input tokens and `$5 / 1M` output tokens:

```text
estimated cost = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

This formula is an estimate, not a billing guarantee. Before your first run, set a `$1` provider spend limit in the Anthropic Console. Remove the key from PowerShell when you finish.

</details>

## Three important terms

- **PRO / CON**: the side for and the side against the same question.
- **Judge**: reads both answers, then picks the side better supported by the question and evidence.
- **Output contract**: the exact format a model must return. This exercise accepts only `WINNER=PRO. reason` or `WINNER=CON. reason`.

PRO and CON see only the original question. The Judge sees the question and both arguments:

```text
question ─┬─> PRO ─┐
          └─> CON ─┴─> Judge ─> WINNER + reason
```

This provides a second viewpoint; it does not guarantee truth. Qualified humans must still check medical, legal, and other high-risk decisions.

## Change one thing

Replace `q` with a question you understand, such as “Should a small team start with an agent framework?” Run it again and check whether the Judge's reason uses both arguments.

## Success check

- [ ] PRO and CON are both non-empty.
- [ ] The Judge returns one winner and a reason.
- [ ] A reply such as `Maybe WINNER=PRO` is rejected.
- [ ] You know Multi-Agent is a division-of-work method, not a correctness guarantee.

<details markdown="1">
<summary>Program flow, common problems, and extensions</summary>

1. `llm_call()` rejects empty text.
2. `debate()` collects separate PRO, CON, and Judge replies.
3. `parse_winner()` uses `fullmatch()` on the whole Judge reply; it does not search for a convenient substring.

Common problems:

- Both sides sound alike: state each role's goal and constraints more clearly.
- The Judge breaks the format: preserve the error and retry once; do not silently choose a side.
- You want to reduce order bias: swap the displayed PRO/CON order during a real evaluation and compare results.

Next, replace the roles with “engineer/user,” add human approval, or evaluate many questions with [promptfoo](https://github.com/promptfoo/promptfoo).

</details>

## 📚 Required reading and learning resources

- ⭐⭐⭐⭐⭐ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents): chapter-style Chinese agent material for fuller background.
- ⭐⭐⭐⭐⭐ [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents): decide whether one agent is enough before adding collaboration.
- ⭐⭐⭐⭐ [Microsoft AutoGen](https://github.com/microsoft/autogen): explore a full multi-agent framework after this small pattern.

See the full list in [Stage 7 Featured Projects](../../../stages/07-multi-agent-production.en.md#-featured-projects-templates--sdks--tool-collections).

<small>Models, prices, packages, and links checked: 2026-08-28 UTC.</small>

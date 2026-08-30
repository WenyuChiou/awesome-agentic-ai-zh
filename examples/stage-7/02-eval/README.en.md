<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Exercise 2: Check an Agent with Evals

An **Eval (evaluation)** is like a reusable test sheet: after changing a prompt, model, or program, run the same questions again.

Pairs with Exercise 2 in [Stage 7 — Agent Production Engineering: Harness, Loops, and Graphs](../../../stages/07-multi-agent-production.en.md).

## 🎯 Learning goals

- Explain an **Eval case**: one input, an expected result, and a scoring method.
- Separate fixed rules from **LLM-as-judge**; a Judge model is not always reliable.
- Require an exact `PASS` or `FAIL`, so a sentence that merely contains `PASS` cannot slip through.

## Run the model-free tests first

Open PowerShell in this folder and copy:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

Two `🎉` messages mean the five-case dataset, score aggregation, empty-output checks, and Judge parser passed. This step uses only fake replies.

<details markdown="1">
<summary>Path A: Run five Eval cases with Ollama</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

Open another PowerShell window:

```powershell
.\.venv\Scripts\python.exe starter.py
```

Ollama does not charge a provider model API fee. Electricity, hardware, downloads, waiting, and maintenance still cost something. These five teaching cases do not prove model quality on your work.

</details>

<details markdown="1">
<summary>Path B: Run the same test sheet with Anthropic</summary>

```powershell
$env:ANTHROPIC_API_KEY = "paste-your-key"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

Haiku 4.5 costs `$1 / 1M` input tokens and `$5 / 1M` output tokens:

```text
estimated cost = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

Actual cost depends on every case's token use. Set a `$1` provider spend limit, then calculate from observed usage. Do not treat an example estimate as your bill.

</details>

## Three important terms

- **Eval case**: one input, the expected important point, and its scoring rule.
- **Deterministic evaluator**: the same input always receives the same score, such as substring or regular-expression checks.
- **LLM-as-judge**: another LLM assigns a score. It can handle open-ended answers, but can also be biased or break the required format.

| Shape of the task | Start with | Why |
|---|---|---|
| The answer must contain `Tokyo` | substring | fast, inexpensive, and repeatable |
| The answer must match a JSON schema | schema validator | checks the structure directly |
| The tone should be clear | LLM-as-judge + human sampling | no single required substring |

This exercise accepts a Judge reply only when the whole response is `PASS` or `FAIL`. If it says “PASS because...”, the program stops instead of guessing.

## Change one thing

Add one real question from your work to `EVAL_CASES`, then make the fake agent answer it incorrectly. Confirm that the report identifies the failing `id`.

## Success check

- [ ] Every case has one stable, unique `id`.
- [ ] You can explain why a case uses substring rather than an LLM Judge.
- [ ] An empty answer cannot pass.
- [ ] Model comparisons reuse the same cases.

<details markdown="1">
<summary>Grow five cases into a real Eval suite</summary>

The teaching loop is:

1. The agent answers.
2. The evaluator applies only that case's rule.
3. The runner saves each result and the overall pass rate.
4. A failure points back to a specific case, not only one summary score.

A real project also needs production queries, edge cases, safety cases, and human labels. Set thresholds from your baseline and risk, not from someone else's fixed percentage.

Common problems:

- Every case is easy: add questions that previously failed.
- The expected value is a whole sentence: retain only the required condition so harmless paraphrases can pass.
- One model answers and judges itself: include deterministic checks or human sampling to reduce self-preference.
- Only the total score is saved: also save failed IDs, model ID, prompt version, and date.

</details>

## 📚 Required reading and learning resources

- ⭐⭐⭐⭐⭐ [promptfoo](https://github.com/promptfoo/promptfoo): version-control cases, providers, and assertions.
- ⭐⭐⭐⭐⭐ [Anthropic Console Evals](https://console.anthropic.com/workbench/evals): build and compare test sets in Anthropic's interface.
- ⭐⭐⭐⭐⭐ [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents): Chapter-style Agent material for filling in the full background.
- ⭐⭐⭐⭐ [LangSmith](https://smith.langchain.com/): useful for teams already using LangChain or LangGraph.
- ⭐⭐⭐⭐ [Weights & Biases Weave](https://wandb.ai/site/weave): connect traces, data, and evaluation workflows.
- ⭐⭐⭐⭐ [Braintrust](https://www.braintrust.dev/): track experiments across model and prompt versions.

See the full list in [Stage 7 Featured Projects](../../../stages/07-multi-agent-production.en.md#-featured-projects-templates--sdks--tool-collections).

<small>Models, prices, packages, and links checked: 2026-08-28 UTC.</small>

<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Core Exercise: Check an Agent with Evals

An **Eval (evaluation)** is like a reusable test sheet: after changing a prompt, model, or program, run the same questions again.

Pairs with Core Exercise 1 in [Stage 7 — Agent Production Engineering: Testable, Observable, Stoppable, and Recoverable](../../../stages/07-multi-agent-production.en.md).

## 🎯 Learning goals

- Explain an **Eval case**: one input, an expected result, and a scoring method.
- Keep five **development split** cases separate from three **holdout set** cases.
- Save a **Baseline** and see whether the next version improved, stayed the same, or had a **Regression**.
- Start with deterministic graders; when **LLM-as-judge** is needed, accept only a complete `PASS` or `FAIL`.

## Run the model-free tests first

Open PowerShell in this folder and copy:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

Two `🎉` messages mean the versioned eight-case dataset, 5/3 split, repeated trials, baseline comparison, empty-output checks, and Judge parser passed. This step uses fake replies only: no network and no API key.

<details markdown="1">
<summary>Path A: Run Evals with Ollama</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

Open another PowerShell window:

```powershell
.\.venv\Scripts\python.exe starter.py
```

The first run uses the five development cases once and writes no file. To save a comparable baseline, copy:

```powershell
.\.venv\Scripts\python.exe starter.py --split dev --trials 3 --save-report reports/dev-baseline.json
```

After changing the prompt or code, run:

```powershell
.\.venv\Scripts\python.exe starter.py --split dev --trials 3 --baseline reports/dev-baseline.json --save-report reports/dev-current.json
```

Run the holdout only when preparing a release:

```powershell
.\.venv\Scripts\python.exe starter.py --split holdout --trials 3 --save-report reports/holdout.json
```

Ollama does not charge a provider model API fee. Electricity, hardware, downloads, waiting, and maintenance still cost something. These eight teaching cases do not prove model quality on your work.

Reports keep case IDs and model outputs; inputs remain in the versioned dataset. Do not use secrets, personal data, or customer data, and do not commit sensitive reports to Git. `--trials` is limited to 1–20 so a typo cannot create unbounded model calls.

</details>

<details markdown="1">
<summary>Path B: Run the same test sheet with Anthropic</summary>

```powershell
$env:ANTHROPIC_API_KEY = "paste-your-key"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

The Anthropic path accepts the same `--split`, `--trials`, `--save-report`, and `--baseline` options shown above.

Haiku 4.5 costs `$1 / 1M` input tokens and `$5 / 1M` output tokens:

```text
estimated cost = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

Actual cost depends on every case's token use. Set a `$1` provider spend limit, then calculate from observed usage. Do not treat an example estimate as your bill.

</details>

## Five important terms

- **Golden / Reference Set**: a human-checked box of good test cases with inputs, success criteria, and graders. It is not training data or a bag of few-shot examples.
- **Development split**: cases you may rerun while changing a prompt or program; failures help you fix things.
- **Holdout Set**: cases kept unseen during development and run for a release check, so you can notice when the system only memorized the development cases.
- **Baseline**: the saved scorecard from before a change, including dataset version, split, model, and per-case results.
- **Regression**: the new version performs worse on the same test sheet. Inspect failed cases and repeated trials before deciding whether to block a release.

A **Deterministic evaluator** gives the same output the same score, such as substring, exact match, or regular expression. **LLM-as-judge** can assess open-ended answers, but it may be biased or break the required format, so keep human sampling.

| Shape of the task | Start with | Why |
|---|---|---|
| The answer must contain `Tokyo` | substring | fast, inexpensive, and repeatable |
| The answer must match a JSON schema | schema validator | checks the structure directly |
| The tone should be clear | LLM-as-judge + human sampling | no single required substring |

This exercise accepts a Judge reply only when the whole response is `PASS` or `FAIL`. If it says “PASS because...”, the program stops instead of guessing.

## Change one thing

Open `eval_cases.json` and replace one development case with a real failure from your work. Keep its unique `id`, success criteria, grader, and a non-sensitive source note. Whenever any case content changes, update `dataset_version`. Then run:

```powershell
.\.venv\Scripts\python.exe test.py
```

Do not copy it into a blank text file first. Edit the runnable data directly and confirm that the report names the failing `id`.

## Success check

- [ ] Every case has one stable, unique `id`.
- [ ] After changing a case, success criterion, or grader, you also updated `dataset_version`.
- [ ] You know the development split may be rerun, while the holdout must not be watched during tuning.
- [ ] Baseline and current report have the same dataset version, split, and case IDs.
- [ ] You can explain why a case starts with a deterministic grader rather than an LLM Judge.
- [ ] An empty answer cannot pass.
- [ ] The report keeps provider, model, trials, category results, failures, and improved/same/regressed counts.

<details markdown="1">
<summary>Grow eight teaching cases into a real Eval suite</summary>

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

<small>Models, prices, packages, and links checked: 2026-09-13 UTC.</small>

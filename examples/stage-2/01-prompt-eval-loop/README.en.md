<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Stage 2 exercise: Change one thing, then check the score

This exercise does one thing: have two prompts answer the **same six questions**, then compare their scores.

You will follow this short path:

```text
same six questions → run the original → add three examples → run again → compare scores
```

## Step 1: Run the no-model version first

Run this in the folder:

```bash
python starter.py
```

You will see `3/6` for the original and `6/6` after adding examples. These are fixed answers built into the program to teach the workflow; **this is not a model leaderboard and does not prove that examples will improve the score every time.**

## Step 2: Confirm that the program calculates correctly

```bash
python test.py
python test_anthropic.py
```

Neither test needs an API key or connects to a model. Seeing `4/4 passed` and `2/2 passed` means you are done.

> 🎓 **Learning mode**: `starter.py` is the complete answer. To really learn it, rename it to `starter_reference.py`, look only at the function names, rewrite your own version, and use the tests to check it. See [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md) for the full method.

<details markdown="1">
<summary>Optional: run a real model with local Ollama (Path A)</summary>

```bash
pip install -r requirements.txt
ollama pull gemma4:e4b
ollama serve
python starter.py --live
```

The program calls the local model 12 times: six questions with the original prompt, then the same six with the improved prompt. API cost is `$0`, but it uses your computer's time and electricity. A small model's score may differ from run to run, which is exactly why fixed questions and repeated tests matter.

</details>

<details markdown="1">
<summary>Optional: run a real model with Anthropic (Path B)</summary>

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python starter_anthropic.py --live
```

On Windows PowerShell, use:

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
python starter_anthropic.py --live
```

The default model is `claude-haiku-4-5`. One short prompt call is estimated below `$0.001`; 12 calls are estimated below `$0.01`. Actual cost depends on token count and current official pricing. Set a `$0.05` total cap for your first run; see [Anthropic's official pricing](https://platform.claude.com/docs/en/about-claude/pricing).

</details>

<details markdown="1">
<summary>How the program works, common snags, and further reading</summary>

| Part | Plain-language explanation |
|---|---|
| `CASES` | Six fixed test questions, each with a correct label |
| `build_prompt()` | The original and improved versions differ by three examples only |
| `evaluate()` | One point for each correct answer |
| `--live` | Replaces built-in answers with real model answers |

Common snags:

- An answer such as `billing, because...` is marked wrong because the output rule requires one label only.
- If Ollama cannot connect, make sure `ollama serve` is still running.
- For an Anthropic authentication error, check the environment variable; do not put the key in code or commit it.
- If the improved version does not score higher, that is normal. Record the score, then change one thing at a time.

> 📚 **Want to go deeper?** Read [Anthropic's Prompt Engineering Overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) to understand “define success criteria first, then change the prompt”; then read the [OpenAI Evals guide](https://developers.openai.com/api/docs/guides/evals) for a fuller evaluation workflow. For batch testing, explore [`promptfoo/promptfoo`](https://github.com/promptfoo/promptfoo). The complete resource list remains in [Stage 2 Curated Projects](../../../stages/02-prompt-engineering.en.md#-curated-projects), rather than being duplicated here.

</details>

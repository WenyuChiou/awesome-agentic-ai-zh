<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

# Core Exercise: Pause, Save, and Continue Safely

This exercise needs no model and does not send email or change real data. The program writes only fake actions to a local JSON ledger so you can first understand the safety skeleton.

Pairs with Core Exercise 3 in [Stage 7 — Agent Production Engineering: Harness, Loops, and Graphs](../../../stages/07-multi-agent-production.en.md).

## 🎯 Learning goals

- **Human Approval**: pause before a sensitive action; a person can approve or reject it.
- **Checkpoint**: save work state while waiting for approval.
- **Resume**: reopen the program and continue with the same task ID.
- **Recovery**: fail closed when state is damaged or does not match; do not guess the next step.
- **Idempotency**: rerun the same key many times while the fake action still runs only once.

## Run the model-free tests first

Open PowerShell in this folder and copy:

```powershell
py -3.11 test.py
```

`8/8 passed` means the offline tests cover pause, reject, approve, restart and resume, ledger reconciliation, corrupted state, and “at most once” execution.

## Walk through pause → approve → resume

First create only a checkpoint; **do not run the fake action**:

```powershell
py -3.11 starter.py start --action "publish draft" --key demo-001
```

You will see `status` set to `waiting_for_approval`. Closing the terminal is fine; the state is in `.cache/safe-execution-state.json`.

Now a person decides. Approve it:

```powershell
py -3.11 starter.py resume --decision approve
```

Run the same command again; the ledger still contains only one `demo-001`. That is the smallest idempotency evidence.

To practice rejection, first delete the two `.cache/safe-execution-*.json` files created by this exercise, then start with a new key and run:

```powershell
py -3.11 starter.py resume --decision reject
```

## Understand the two files

| File | What it stores | What it must not store |
|---|---|---|
| Checkpoint state | Task ID, action, status, approval decision, schema version | API keys, passwords, unredacted customer data |
| Side-effect ledger | Executed idempotency keys and fake actions | Treating “write succeeded” as proof that the business Outcome is correct |

Real systems usually put state in an access-controlled, backed-up, retention-managed, versioned database or queue. This JSON example teaches responsibility boundaries; it is not a production storage solution.

## Change one thing

Change `publish draft` to `send reviewed summary` and use a new key. Reject it first and confirm the ledger does not grow; start again, approve it, and confirm it grows by only one entry.

## Success check

- [ ] Without approval, the ledger has no fake action.
- [ ] After reject, status is `cancelled` and there is no side effect.
- [ ] After approve, status is `completed`.
- [ ] Resuming twice with the same key leaves one ledger entry.
- [ ] If the ledger and checkpoint disagree, the program repairs a provable completion or stops for human recovery; it never labels an executed action `cancelled`.
- [ ] With corrupted JSON or a mismatched key/action, the program stops instead of guessing.

## 📚 Required reading and learning resources

- ⭐⭐⭐⭐⭐ [OpenAI Agents SDK — Human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/): tool approval, saving `RunState`, and resume.
- ⭐⭐⭐⭐⭐ [LangGraph — Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts): pause, approve/reject, checkpoint, resume, and idempotent side effects before an interrupt.
- ⭐⭐⭐⭐⭐ [LangGraph — Persistence](https://docs.langchain.com/oss/python/langgraph/persistence): the boundary between checkpointers, stores, thread state, and fault tolerance.
- ⭐⭐⭐⭐⭐ [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents): check the outside-world Outcome and complete Trajectory, not only what the Agent says.

<small>Official documents and links checked: 2026-08-31 UTC.</small>

<details markdown="1">
<summary>Expand: why write the ledger before marking the checkpoint complete?</summary>

If the program stops between the two writes, the next resume first checks the ledger for the same idempotency key. If it is present, the fake action is not repeated; only the `completed` checkpoint is repaired. This is a teaching-sized write-ahead idea; real cross-service transactions must follow the consistency guarantees of the database, queue, or provider API.

</details>

<details markdown="1">
<summary>Expand: common mistakes and safety boundaries</summary>

- Putting approval after the tool runs: after an email or payment has happened, asking a person is too late.
- Retrying without an idempotency key: a network timeout can make a retry duplicate a side effect.
- Omitting schema or program versions from a checkpoint: tomorrow’s deployment may not safely read yesterday’s state.
- Putting the full Prompt, tokens, or customer data into state: state also needs minimization, encryption, access control, and deletion design.
- Looking only at `status=completed`: use an Outcome Eval to confirm the outside result is correct.

</details>

Next: return to [Stage 7’s four-step release route](../../../stages/07-multi-agent-production.en.md#-four-release-steps-eval--observability--approval--recovery--deploy), then do the Deploy exercise.

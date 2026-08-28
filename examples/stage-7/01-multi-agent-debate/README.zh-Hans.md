<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 1：让三个 Agent 一起辩论

你会做出三个角色：PRO 说“赞成”、CON 说“反对”，Judge 看完两边再选一边。

对应 [Stage 7 — Multi-Agent 与 Production](../../../stages/07-multi-agent-production.zh-Hans.md) 练习 1。

## 🎯 学习目标

- 说清楚 **Multi-Agent**：多个 Agent 分工完成同一件事。
- 让 PRO 与 CON 各自作答，避免一开始就互相带答案。
- 用严格格式读 Judge 结果；格式错了就停止，不偷偷猜。

## 先跑不花模型费的测试

在这个文件夹打开 PowerShell，直接复制：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

看到两份 `🎉`，就代表三次调用、空回复检查和 Judge 格式都通过。测试使用假回复，不会连接到模型。

<details markdown="1">
<summary>Path A：用 Ollama 实际辩论</summary>

1. 安装 [Ollama](https://ollama.com/) 后，先准备模型：

   ```powershell
   ollama pull qwen3.5:4b
   ollama serve
   ```

2. 另开一个 PowerShell：

   ```powershell
   .\.venv\Scripts\python.exe starter.py
   ```

Ollama 不收模型 API 费，但下载时间、电力与电脑硬件仍有成本。模型较慢时，请等它完成，不要用固定秒数判断失败。

</details>

<details markdown="1">
<summary>Path B：用 Anthropic 比较结果与预算</summary>

```powershell
$env:ANTHROPIC_API_KEY = "贴上你的金钥"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

这题会调用三次模型。Haiku 4.5 的单价是 input `$1 / 1M` tokens、output `$5 / 1M` tokens：

```text
估算费用 = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

这是估算公式，不是帐单保证。第一次练习前，可在 Anthropic Console 把供应商 spend limit 设成 `$1`；完成后移除 PowerShell 内的金钥。

</details>

## 三个重要词

- **PRO / CON**：同一题的赞成方与反对方。
- **Judge**：读完两边答案，再选出较符合题目与证据的一边。
- **Output contract**：模型必须照约定格式回答。这题只接受 `WINNER=PRO. 理由` 或 `WINNER=CON. 理由`。

PRO 与 CON 都只看原题。Judge 才会看到原题和两份论点：

```text
题目 ─┬─> PRO ─┐
      └─> CON ─┴─> Judge ─> WINNER + 理由
```

这只能提供第二个视角，不保证答案正确。医疗、法律或高风险决策仍要交给合格的人检查。

## 只改一件事

把 `q` 换成你熟悉的问题，例如“小团队要不要先用 Agent framework？”再跑一次。看 Judge 的理由是否真的引用两边论点。

## 成功检查

- [ ] PRO 与 CON 都不是空白。
- [ ] Judge 只输出一个 Winner，并附上理由。
- [ ] 乱回 `Maybe WINNER=PRO` 时，测试会拒绝它。
- [ ] 你知道多 Agent 是分工方法，不是正确答案保证。

<details markdown="1">
<summary>程序怎么走、常见问题与延伸</summary>

1. `llm_call()` 先拒绝空字符串。
2. `debate()` 分别取得 PRO、CON、Judge 三份文字。
3. `parse_winner()` 用 `fullmatch()` 检查整份 Judge 回复，不做子字符串猜测。

常见问题：

- 两边说得太像：把角色、要保护的目标与限制写得更明确。
- Judge 格式错误：保留错误并重试一次，不要默默选一边。
- 想减少顺序偏差：正式评测时交换 PRO／CON 显示顺序，再比较结果。

延伸方向：把两边改成“工程师／用户”、加入人工批准，或把多个题目交给 [promptfoo](https://github.com/promptfoo/promptfoo) 批次评测。

</details>

<details markdown="1">
<summary>📚 深入学习资源与评分</summary>

- ⭐⭐⭐⭐⭐ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：章节式中文 Agent 教材，适合补完整背景。
- ⭐⭐⭐⭐⭐ [Anthropic：Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)：先判断单 Agent 是否已足够，再增加协作。
- ⭐⭐⭐⭐ [Microsoft AutoGen](https://github.com/microsoft/autogen)：想看完整 multi-agent framework 时再进入。

完整清单见 [Stage 7 精选 Projects](../../../stages/07-multi-agent-production.zh-Hans.md#-精选-projects范本--sdk--工具-collection)。

<small>模型、价格、套件与连结查核：2026-08-28 UTC。</small>

</details>

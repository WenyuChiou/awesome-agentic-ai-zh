<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# Stage 2 练习：改一件事，再看分数

这个练习只做一件事：让两个 prompt 回答**同一组六题**，再比较分数。

你会走过这条小路：

```text
同一组六题 → 跑原版 → 加三个范例 → 再跑一次 → 比分数
```

## 第一步：先运行不用模型的版本

在这个文件夹中运行：

```bash
python starter.py
```

你会看到原版 `3/6`、加入范例后 `6/6`。这些是程序内置的固定答案，用来教你看懂流程；**它不是模型排行榜，也不能证明范例每次都会加分。**

## 第二步：确认程序没有计算错误

```bash
python test.py
python test_anthropic.py
```

两个测试都不需要 API key，也不会连接模型。看到 `4/4 passed` 和 `2/2 passed` 就完成了。

> 🎓 **学习模式**：先运行提供的 `starter.py`（`python starter.py`），然后只改一个小地方，再重新运行现有测试：`python test.py` 和 `python test_anthropic.py`。如果测试失败，就撤销或修正这一个改动，再试一次。不需要重命名文件，也不需要重写整份解答。完整方法见 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

<details markdown="1">
<summary>可选：用本地 Ollama 运行真实模型（Path A）</summary>

```bash
pip install -r requirements.txt
ollama pull gemma4:e4b
ollama serve
python starter.py --live
```

程序会调用本地模型 12 次：六题运行原版，再用同六题运行改进版。API 费用为 `$0`，但会使用你的电脑时间和电力。小模型的分数每次可能不同，这正是要用固定题目反复测试的原因。

</details>

<details markdown="1">
<summary>可选：用 Anthropic 运行真实模型（Path B）</summary>

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python starter_anthropic.py --live
```

Windows PowerShell 可改用：

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
python starter_anthropic.py --live
```

默认模型是 `claude-haiku-4-5`。这个短 prompt 的单次调用预计低于 `$0.001`，12 次预计低于 `$0.01`；实际费用取决于 token 数量和当时的官方价格。第一次请先设置 `$0.05` 总上限；价格以 [Anthropic 官方定价](https://platform.claude.com/docs/en/about-claude/pricing) 为准。

</details>

<details markdown="1">
<summary>程序如何工作、常见卡点和延伸阅读</summary>

| 部分 | 白话说明 |
|---|---|
| `CASES` | 六张固定考卷，每张都有正确标签 |
| `build_prompt()` | 原版和改进版只相差三个范例 |
| `evaluate()` | 每答对一题得 1 分 |
| `--live` | 把内置答案换成真实模型答案 |

常见卡点：

- 回答是 `billing， 因为……`：本练习会判错，因为输出规则要求只返回一个标签。
- Ollama 连不上：先确认 `ollama serve` 仍在运行。
- Anthropic 报认证错误：确认 key 在环境变量中，不要写进程序或 commit。
- 改进版没有加分：这是正常结果。记下分数，再一次只改一件事。

> 📚 **想学得更深？** 先看 [Anthropic Prompt Engineering Overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)，理解“先定义成功标准，再修改 prompt”；再看 [OpenAI Evals 指南](https://developers.openai.com/api/docs/guides/evals)，学习更完整的评估流程。需要批量测试时，可以继续探索 [`promptfoo/promptfoo`](https://github.com/promptfoo/promptfoo)。完整资源仍放在 [Stage 2 精选 Projects](../../../stages/02-prompt-engineering.zh-Hans.md#-精选-projects)，这里不重复堆满页面。

</details>

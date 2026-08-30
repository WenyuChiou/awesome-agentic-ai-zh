<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 2：用 Eval 检查 Agent

**Eval（评测）**像一张固定考卷：每次改 Prompt、模型或程序后，都用同一批题目再考一次。

对应 [Stage 7 — Agent Production Engineering：Harness、Loop 与 Graph](../../../stages/07-multi-agent-production.zh-Hans.md) 练习 2。

## 🎯 学习目标

- 说清楚 **Eval case**：一题输入、预期结果和评分方法。
- 分辨固定规则与 **LLM-as-judge**，不把 Judge 当成永远可靠。
- 用完全相符的 `PASS`／`FAIL` 格式，避免把一句话中的 `PASS` 误判成通过。

## 先跑不花模型费的测试

在这个文件夹打开 PowerShell，直接复制：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

看到两份 `🎉`，就代表五题数据、分数汇总、空回复和 Judge parser 都通过。这一步只用假回复。

<details markdown="1">
<summary>Path A：用 Ollama 跑五题 Eval</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

另开 PowerShell：

```powershell
.\.venv\Scripts\python.exe starter.py
```

Ollama 不收模型 API 费，但电力、硬件、下载与等待时间仍有成本。这五题只是教学样本，不能代表模型在你工作上的质量。

</details>

<details markdown="1">
<summary>Path B：用 Anthropic 跑同一份考卷</summary>

```powershell
$env:ANTHROPIC_API_KEY = "贴上你的金钥"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

Haiku 4.5 的单价是 input `$1 / 1M` tokens、output `$5 / 1M` tokens：

```text
估算费用 = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

实际费用取决于每题的 token。先在供应商 Console 设置 `$1` spend limit，再用实际 usage 计算；不要把示例估算当账单。

</details>

## 三个重要词

- **Eval case**：一笔输入、预期重点和评分规则。
- **Deterministic evaluator**：同样输入一定得到同样分数，例如 substring 或正规表示式。
- **LLM-as-judge**：请另一个 LLM 评分。它能处理开放式答案，也可能有偏差或格式错误。

| 题目形状 | 先用什么 | 为什么 |
|---|---|---|
| 答案必须含 `Tokyo` | substring | 快、便宜、结果固定 |
| 必须符合 JSON schema | schema validator | 直接检查结构 |
| 语气是否清楚 | LLM-as-judge + 人工抽查 | 没有单一固定字符串 |

这份练习的 Judge 只接受整份回复等于 `PASS` 或 `FAIL`。若它回“PASS because...”，程序会要求重试或停止。

## 只改一件事

在 `EVAL_CASES` 加一题你自己的真实问题，再故意让假 Agent 答错。确认报告能指出失败的 `id`。

## 成功检查

- [ ] 每一题都有稳定且唯一的 `id`。
- [ ] 你能说明这题为什么用 substring，而不是 LLM Judge。
- [ ] 空答案不会被算成通过。
- [ ] 换模型时仍使用同一份 cases，才能公平看变化。

<details markdown="1">
<summary>从五题走向真正的 Eval suite</summary>

教学流程是：

1. Agent 回答问题。
2. Evaluator 只看该题规则并打分。
3. Runner 保存每题结果与整体 pass rate。
4. 失败时回到具体 case，不只看一个总分。

正式专案还要加入真实用户案例、边界条件、安全案例与人工标注。门槛应由你的 baseline 与风险决定，不要照抄别人的固定百分比。

常见问题：

- cases 都太简单：加入过去真的答错过的问题。
- expected 写整句：只保留必要条件，避免同义句被误杀。
- 同一模型回答又评分：至少加入固定规则或人工抽查，降低自我偏好。
- 只保存总分：同时保存失败 `id`、模型 ID、Prompt 版本与日期。

</details>

## 📚 必读与学习资源

- ⭐⭐⭐⭐⭐ [promptfoo](https://github.com/promptfoo/promptfoo)：可把 cases、providers 和 assertions 放进版本控制。
- ⭐⭐⭐⭐⭐ [Anthropic Console Evals](https://console.anthropic.com/workbench/evals)：用官方界面创建与比较测试集。
- ⭐⭐⭐⭐⭐ [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)：章节式中文 Agent 教材，适合补完整背景。
- ⭐⭐⭐⭐ [LangSmith](https://smith.langchain.com/)：适合已使用 LangChain／LangGraph 的团队。
- ⭐⭐⭐⭐ [Weights & Biases Weave](https://wandb.ai/site/weave)：把 traces、数据与评测放在同一套工作流。
- ⭐⭐⭐⭐ [Braintrust](https://www.braintrust.dev/)：适合做多版本实验与结果追踪。

完整清单见 [Stage 7 精选 Projects](../../../stages/07-multi-agent-production.zh-Hans.md#-精选-projects范本--sdk--工具-collection)。

<small>模型、价格、套件与连结查核：2026-08-28 UTC。</small>

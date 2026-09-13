<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 核心练习：用 Eval 检查 Agent

**Eval（评测）**像一张固定考卷：每次改 Prompt、模型或程序后，都用同一批题目再考一次。

对应 [Stage 7 — Agent Production Engineering：Harness、Loop 与 Graph](../../../stages/07-multi-agent-production.zh-Hans.md) 核心练习 1。

## 🎯 学习目标

- 说清楚 **Eval case**：一题输入、预期结果和评分方法。
- 把 5 题 **development split（开发组）**和 3 题 **holdout set（保留考卷）**分开。
- 保存 **Baseline（基准）**，看下一版是进步、相同，还是 **Regression（退步）**。
- 先用固定规则评分；需要 **LLM-as-judge** 时，只接受完整的 `PASS`／`FAIL`。

## 先跑不花模型费的测试

在这个文件夹打开 PowerShell，直接复制：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe test_anthropic.py
```

看到两份 `🎉`，就代表 8 题版本化数据、5／3 分组、多次 trials、baseline 比较、空回复与 Judge parser 都通过。这一步只用假回复，不联网也不需要 API key。

<details markdown="1">
<summary>Path A：用 Ollama 跑 Eval</summary>

```powershell
ollama pull qwen3.5:4b
ollama serve
```

另开 PowerShell：

```powershell
.\.venv\Scripts\python.exe starter.py
```

第一次会跑 5 题开发组、每题 1 次，而且不写文件。要保存可比较的基准，直接复制：

```powershell
.\.venv\Scripts\python.exe starter.py --split dev --trials 3 --save-report reports/dev-baseline.json
```

改完 Prompt 或程序后，再跑：

```powershell
.\.venv\Scripts\python.exe starter.py --split dev --trials 3 --baseline reports/dev-baseline.json --save-report reports/dev-current.json
```

准备发布时才跑保留考卷：

```powershell
.\.venv\Scripts\python.exe starter.py --split holdout --trials 3 --save-report reports/holdout.json
```

Ollama 不收模型 API 费，但电力、硬件、下载与等待时间仍有成本。这 8 题只是教学样本，不能代表模型在你工作上的质量。

报告会保存 case ID 与模型输出，题目则留在版本化数据集；不要放秘密、个人信息或客户数据，也不要把敏感报告提交到 Git。`--trials` 限制为 1–20，避免手滑造成无上限的模型调用。

</details>

<details markdown="1">
<summary>Path B：用 Anthropic 跑同一份考卷</summary>

```powershell
$env:ANTHROPIC_API_KEY = "贴上你的金钥"
$env:MODEL = "claude-haiku-4-5-20251001"
.\.venv\Scripts\python.exe starter_anthropic.py
```

Anthropic 路径也支持上面的 `--split`、`--trials`、`--save-report` 与 `--baseline`。

Haiku 4.5 的单价是 input `$1 / 1M` tokens、output `$5 / 1M` tokens：

```text
估算费用 = (input_tokens × $1 / 1M) + (output_tokens × $5 / 1M)
```

实际费用取决于每题的 token。先在供应商 Console 设置 `$1` spend limit，再用实际 usage 计算；不要把示例估算当账单。

</details>

## 五个重要词

- **Golden／Reference Set（黄金／参考集）**：一盒经过人工确认的好题目，包含输入、成功条件与评分方法；不是拿来训练模型或塞进 few-shot 的例句库。
- **Development split（开发组）**：改 Prompt 或程序时反复使用的题目；失败可以帮你修东西。
- **Holdout Set（保留考卷）**：开发时先不看、不反复跑；准备发布时才用来检查是否只背熟开发题。
- **Baseline（基准）**：改东西以前保存的成绩单，而且要记住数据版本、split、模型与每题结果。
- **Regression（退步）**：新版本在同一份考卷上比基准差；先看失败题与多次 trials，再决定是否阻挡发布。

**Deterministic evaluator（固定规则评分器）**对同一输出会给同一分数，例如 substring、exact match 或正规表示式。**LLM-as-judge**能评开放式答案，但可能有偏差或格式错误，所以仍要人工抽查。

| 题目形状 | 先用什么 | 为什么 |
|---|---|---|
| 答案必须含 `Tokyo` | substring | 快、便宜、结果固定 |
| 必须符合 JSON schema | schema validator | 直接检查结构 |
| 语气是否清楚 | LLM-as-judge + 人工抽查 | 没有单一固定字符串 |

这份练习的 Judge 只接受整份回复等于 `PASS` 或 `FAIL`。若它回“PASS because...”，程序会要求重试或停止。

## 只改一件事

打开 `eval_cases.json`，把一题开发组换成你的真实失败案例。保留唯一 `id`、成功条件、grader 与不含机密的来源说明；只要 case 内容改了，就更新 `dataset_version`。再跑：

```powershell
.\.venv\Scripts\python.exe test.py
```

不用先抄到空白文本文件；直接改可执行的数据，确认报告能指出失败的 `id`。

## 成功检查

- [ ] 每一题都有稳定且唯一的 `id`。
- [ ] 改过题目、成功条件或 grader 后，`dataset_version` 也有更新。
- [ ] 你知道开发组可以反复跑，holdout 不可边改边偷看。
- [ ] baseline 与当前报告的数据版本、split 和 case IDs 完全相同。
- [ ] 你能说明这题为什么先用固定规则，而不是 LLM Judge。
- [ ] 空答案不会被算成通过。
- [ ] 报告保留 provider、model、trials、分类结果、失败题与 improved／same／regressed。

<details markdown="1">
<summary>从 8 题教学数据走向真正的 Eval suite</summary>

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

<small>模型、价格、套件与链接查核：2026-09-13 UTC。</small>

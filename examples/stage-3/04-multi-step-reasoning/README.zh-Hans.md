<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 4：多步骤推理任务

对应 [Stage 3 — 工具使用与第一个 Agent Loop](../../../stages/03-tool-use-and-hello-agent.zh-Hans.md) 练习 4。
> 🎓 **学习模式**：先运行提供的 `starter.py`（`python starter.py`），然后只改一个小地方，再重新运行现有测试 `python test.py`。如果测试失败，就撤销或修正这一个改动，再试一次。不需要重命名文件，也不需要重写整份解答。完整方法见 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 70-150 行 illustrative 版、聚焦 `核心 pattern + 两条 SDK path`，不是进阶深度教材。深度教材推荐：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章节式 + 16 种 production 能力。**本练习对应 hello-agents 的 planning / multi-step workflow 章节**
> - [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)（什么时候该拆步骤、什么时候不要）
> - 完整 references 见 [Stage 3 精选 Projects](../../../stages/03-tool-use-and-hello-agent.zh-Hans.md#-精选-projects)


## 为什么这题重要

把练习 3 的 ReAct loop 延伸成 **3-5 步任务**：查台北人口 → 查纽约人口 → 相除 → 转百分比。LLM 负责规划下一步、工具负责可靠地执行小动作；两者合起来才像能完成 workflow 的 agent。

这题适合观察不同模型在多步骤任务上的行为差异；结果可能漏步或提早停止。固定 prompt、tools 与测试题，用 eval 记录每一步的成功与失败。

## 怎么跑 — 两条路径

### Path A（默认、本机免费）

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

预算：**$0 API 费用**；不包含硬件、内存与电力成本。

### Path B（Anthropic、云端比较）

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "your-key"
python starter_anthropic.py
```

预算：每次先预留 **$0.05**。实际费用按 `输入 tokens × $1 / 1,000,000 + 输出 tokens × $5 / 1,000,000` 计算，Tool Use 还会加入 prompt tokens；价格查核日：`2026-08-27`。

预期看到（Path A、本机，理想 4 步走完）：

```
❓ 问题：Find Taipei population divided by New York population, then express it as a percentage.
------------------------------------------------------------
[step 0] tool: lookup_population({'city': 'Taipei'}) → 2602000
[step 1] tool: lookup_population({'city': 'New York'}) → 8336000
[step 2] tool: divide({'a': 2602000, 'b': 8336000}) → 0.3122...
[step 3] tool: to_percentage({'ratio': 0.3122}) → 31.22
------------------------------------------------------------
✅ 最终答案：Taipei is about 31.22% of New York's population.
   共 5 轮
✅ 练习 4 通过 — 你已用本机 qwen2.5:3b 跑通多步 ReAct loop、$0/run
```

## 不花钱验证程序逻辑（mock-based）

```powershell
python test.py            # 验 Path A (Ollama) starter.py 逻辑
python test_anthropic.py  # 验 Path B (Anthropic) starter_anthropic.py 逻辑
```

两条 test 都用 `unittest.mock`、不打真 API、$0/run。

## 观念提醒

多步任务的核心不是“模型很会算”、而是把复杂任务拆成可靠的小步：

- **工具要窄而有界**：`divide(a, b)` 只做一件事、`b=0` 也不 crash 而是回 0
- **LLM 负责规划**：决定下一步要调用哪个工具、何时停
- **`max_iter=8` 是必要安全网**：避免模型一直要求工具而没收尾
- **每轮 messages 一直长**：assistant response + tool_result 都接回去、LLM 才看得到历史

## 两个 path 观察重点

| 观察项 | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| 走完 4 步 | 用固定 eval 测量 | 用固定 eval 测量 |
| 中间步骤顺序 | 用固定 eval 测量 | 用固定 eval 测量 |
| 收尾判断 | 用固定 eval 测量 | 用固定 eval 测量 |
| 预算预留 | $0.05 | $0 API 费用 |

这恰好是 Stage 3 练习 4 的教学重点——**同样 ReAct loop、不同 model、在哪一步开始崩**。Production 选择 model 时，用固定 eval 测量行为与成本。

## 想看更聪明的答案？

预设用固定 ID `claude-haiku-4-5-20251001`。想比较 sonnet 时：

```powershell
$env:MODEL = "claude-sonnet-5"; python starter_anthropic.py
```

或 Ollama path 换更大 model：

```powershell
$env:MODEL = "qwen2.5:7b"; python starter.py
$env:MODEL = "mistral-nemo:12b"; python starter.py
```

## 延伸

- **加更多 tool**：在 `TOOLS_SPEC` + `TOOL_IMPL` 补一个 entry 即可
- **加 retry / error handling**：看 [`../05-error-handling/`](../05-error-handling/) 怎么处理 tool 失败
- **schema 设计**：看 [`../06-schema-design/`](../06-schema-design/) 比较 bad / good schema

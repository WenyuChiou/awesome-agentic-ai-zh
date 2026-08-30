<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# `examples/` — 可以直接运行的小练习

> [← 回主路线 README](../README.zh-Hans.md)

<!-- freshness: canonical=examples/README.md; verified_on=2026-08-30; scope=example-inventory,local-model-tags,download-sizes,sdk-entry-points; max_age_days=90 -->

Stage 章节先告诉你“这个概念是什么”；这个文件夹让你真的运行一次。第一次不用把所有模型都装好，也不用先读完整份程序。

## 📌 先分清五个词

| 核心词 | 五岁也能懂的说法 | 正确意思 |
|---|---|---|
| **Example（范例）** | 已经拼好的小积木 | 可以直接运行、观察结果的示范程序 |
| **Starter（起始程序）** | 留几块给你自己拼 | 练习用的最小程序入口，通常是 `starter.py` |
| **Path（路径）** | 到同一个终点的不同道路 | 本项目用 Path A／B／C 表示不同运行方式 |
| **Mock（模拟答案）** | 先用玩具电话练习 | 不连接真实模型，先检查程序逻辑 |
| **Live call（真实调用）** | 真的把电话打出去 | 连接本地或云端模型，结果、时间和费用都可能变化 |

## 🎯 你会学会什么

- 先用 **Mock** 找程序错误，再做 **Live call** 看模型行为。
- 知道 Ollama、Anthropic API 和测试各自负责什么。
- 从 Stage 索引找到正确文件夹，不用猜文件名。
- 看懂测试结果、diff 和限制，不把“有输出”误认为“已经正确”。

## 📚 必读阅读

1. [安装与环境设置](../resources/setup-guide.zh-Hans.md)：先让 Python、Git 和所选模型路径能工作。
2. [Stage 1：LLM 基础](../stages/01-llm-basics.zh-Hans.md)：选择模型、看费用并理解 Context。
3. [CLI Agents 指南](../resources/cli-agents-guide.zh-Hans.md)：分清 Coding Agent、Router 和 Local Runtime。

## 🛠 第一次运行：先跑不花模型费用的测试

下面这个范例有完整的 `test.py`。先复制这三行：

```powershell
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
python test.py
```

看到通过信息，表示程序的固定逻辑能工作；它还没有证明任何模型一定会答对。接着再选一条真实模型路径。

| 路径 | 谁真的生成答案 | 先做什么 | 适合什么时候 |
|---|---|---|---|
| **Path C：Mock** | 固定的假答案 | `python test.py` | 第一步；先找程序错误 |
| **Path A：Ollama** | 你电脑上的模型 | 安装 Ollama、pull 题目指定的模型 | 练习真实模型行为，不产生供应商模型 API 账单 |
| **Path B：Anthropic** | Anthropic 云端模型 | 设置 `ANTHROPIC_API_KEY` | 想用同一道题比较云端质量时 |

<details markdown="1">
<summary>展开 Path A／B 的完整命令、环境和费用提醒</summary>

### Path A：Ollama

```powershell
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

本地运行不会产生供应商模型 API 账单，但仍会使用下载空间、内存、电力和时间。文件、log 和工具权限仍要保护。

### Path B：Anthropic API

```powershell
$env:ANTHROPIC_API_KEY = "your-key"
python starter_anthropic.py
```

云端调用可能使用额度或产生费用。运行前查看当天官方 pricing／usage 页面，设置自己能接受的上限；不要把 key 写进程序或 commit。

</details>

## 🧭 根据 Stage 找范例

这里只列实际存在的文件夹；短练习仍会直接放在 Stage 章节中。

| Stage | 这一关在学什么 | 可运行文件夹 |
|---|---|---|
| [Stage 1](../stages/01-llm-basics.zh-Hans.md) | LLM 基础和错误处理 | `stage-1/`：2 个 |
| [Stage 2](../stages/02-prompt-engineering.zh-Hans.md) | Prompt 设计和小型评测循环 | `stage-2/`：1 个 |
| [Stage 3](../stages/03-tool-use-and-hello-agent.zh-Hans.md) | **工具使用与第一个 Agent Loop** | `stage-3/`：6 个 |
| [Stage 4](../stages/04-agent-frameworks.zh-Hans.md) | **Workflow Graph 与 Agent 框架** | `stage-4/`：5 个；各自使用独立的 Python 3.11 环境 |
| [Stage 5](../stages/05-claude-code-ecosystem.zh-Hans.md) | Claude Code 生态和 Skill | `stage-5/`：1 个；其余是章节内练习 |
| [Stage 6](../stages/06-memory-rag.zh-Hans.md) | Embedding、RAG 和 Memory | `stage-6/`：5 个 |
| [Stage 7](../stages/07-multi-agent-production.zh-Hans.md) | **Agent Production Engineering** | `stage-7/`：5 个 |
| [Track A1–A3](../tracks/cli/A1-cli-intro.zh-Hans.md) | CLI 工作流 | 章节内练习；没有 `examples/track-a/` |

## 🧠 本地模型怎么选

模型不是“越新就一定越适合”。先用题目指定的 tag，再跑固定测试。下载大小以 Ollama 官方 tag 页面在 **2026-08-30 UTC** 的显示为准。

| 范围 | 默认 tag | 官方显示下载大小 | 为什么 |
|---|---|---:|---|
| Stage 1–2 | [`gemma4:e4b`](https://ollama.com/library/gemma4:e4b) | 9.6 GB | 纯对话和 Prompt 练习 |
| Stage 3–6 | [`qwen2.5:3b`](https://ollama.com/library/qwen2.5:3b) | 1.9 GB | 当前范例的工具调用练习默认值 |
| Stage 7 | [`qwen3.5:4b`](https://ollama.com/library/qwen3.5:4b) | 3.4 GB | 观察评测、监控和部署流程 |

完整的现行模型、价格、Context 和替代方案只在 [Stage 1](../stages/01-llm-basics.zh-Hans.md) 维护，避免两个页面讲成不同版本。

## ✅ 文件夹并不都长得一样

先打开这道题的 `README`。文件名会跟着要学的内容改变，不要因为没看到普通的 `starter.py` 就以为文件坏了。

| 形状 | 实际文件夹 | 你会看到什么 |
|---|---|---|
| 标准双路径 | 大多数 Python 练习 | `starter.py`、`starter_anthropic.py`、两个离线测试、三语 README、`requirements.txt` |
| Provider 切换 | `stage-1/04-cross-provider/` | 只用 OpenAI-compatible client 比较 endpoint，所以只有 `starter.py` 和 `test.py` |
| Schema 好坏比较 | `stage-3/06-schema-design/` | `starter_bad*` 和 `starter_good*`，不是普通 starter 文件名 |
| Framework／部署加项 | `stage-4/01-same-agent-two-frameworks/`<br>`stage-4/04-codeact-vs-json-tool/`<br>`stage-7/05-deploy/` | 在标准双路径外，再加入 CrewAI、Docker smoke test 或 `Dockerfile` |
| Skill 包 | `stage-5/tool-calling-tutor/` | `SKILL.md`、references、translations 和三语 README；它不是 Python starter 项目 |

设计底线：每个 Python 练习都要能用离线测试检查固定逻辑；Skill 包由 repository 结构测试检查。starter 保持小；环境变量只放假 key 范例；真实模型行为用固定 eval 核对；不要关闭必要 hook 或 approval。

<details markdown="1">
<summary>展开 Windows 编码、贡献规则和故障排查</summary>

- Windows 的 `starter.py`／`test.py` 需要把 stdout 设置为 UTF-8，避免 cp950 无法输出中文或 emoji。
- 一个 starter 原则上不超过 80 LOC；更深入的完整教学改为链接官方文档或 canonical tutorial。
- 无法运行时，先记录文件夹、Python 版本、完整错误、运行命令和使用的 Path，再开 issue。
- 不要上传真实 API key、`.env`、私人数据或模型回复 log。

</details>

## 🎯 精选 Projects 与学习资源

星星是本学习地图的阅读优先级，不是 GitHub stars，也不是工具总排名。

<table>
<thead><tr><th>分类</th><th>资源</th><th>先学什么</th><th>评分</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="2">模型运行</th><td><a href="https://github.com/ollama/ollama">ollama/ollama</a></td><td>先在本地运行一个模型，再让 starter 调用它</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/vllm-project/vllm">vllm-project/vllm</a></td><td>需要服务器级吞吐量时再学</td><td>⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Python SDK</th><td><a href="https://github.com/openai/openai-python">openai/openai-python</a></td><td>理解 OpenAI-compatible client 和 response shape</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/anthropics/anthropic-sdk-python">anthropics/anthropic-sdk-python</a></td><td>比较 Anthropic messages 和 tool schema</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">验证与数据</th><td><a href="https://github.com/pytest-dev/pytest">pytest-dev/pytest</a></td><td>从小型 assert 走向可重复的测试</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/pydantic/pydantic">pydantic/pydantic</a></td><td>验证工具输入、结构化输出和错误</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
</table>

## ✅ 完成检查

- [ ] 我能从 Stage 索引找到一个实际存在的文件夹。
- [ ] 我先跑 Mock，再决定要不要做 Live call。
- [ ] 我知道 OpenRouter 是 Router、Ollama 是 Local Runtime、OpenCode／Pi 是 Coding Agent。
- [ ] 我没有把 key 或私人数据写进 repo。
- [ ] 我用测试和 diff 判断结果，不只看“程序有输出”。

<small>范例目录、模型 tag 与官方入口核查：2026-08-30 UTC。</small>

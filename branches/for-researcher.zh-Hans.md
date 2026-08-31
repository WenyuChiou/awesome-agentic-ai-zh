# 研究人员延伸路线（For Researchers）

> [繁體中文](./for-researcher.md) | **简体中文** | [English](./for-researcher.en.md)

[← 回到主路线](../README.zh-Hans.md)

<!-- freshness: canonical=branches/for-researcher.md; verified_on=2026-08-29; scope=research-tools,citations,privacy,reproducibility,project-status; max_age_days=90 -->

<a id="使用场景研究阶段-ai-怎么帮"></a>
## 📌 这条路帮你做什么
这页不是让 AI 替你当研究者，而是帮你**找到资料、看懂资料，再确认答案确实有资料支持。**
- 会用终端或 Python：完成 [Track A 的 A3](../tracks/cli/A3-cli-production.zh-Hans.md) 或 [Track B 的 Stage 7](../stages/07-multi-agent-production.zh-Hans.md) 后再来。
- 不写代码：直接做下面的第一个练习，只需浏览器和一篇公开 paper。

## 🎯 学习目标
完成这一页后，你可以：
1. 分清“AI 说了什么”和“原文写了什么”。
2. 逐条核对引用来源，而不是看到引用编号就相信。
3. 知道哪些数据可以上传，哪些要先问机构或数据拥有者。
4. 保存足够记录，让自己或同事能重新做一次。

## 🧩 八个核心词
- **Source（来源）**：用来查证的原始材料，如 paper、数据集或研究记录。
- **Claim（主张）**：可检查的说法，例如“方法 A 在数据集 B 上更好”。
- **Citation（引用）**：带你回到来源位置的路标，不保证来源真的支持主张。
- **Source Verification（来源核对）**：打开原文，检查内容、范围与限制是否和答案一致。
- **Literature RAG（文献 RAG）**：先从获准使用的文献找片段，再交给模型回答。
- **Reproducibility（可重复性）**：别人拿到数据、步骤、版本与设置后，可以重新跑出可比较结果。
- **Private Data（私人资料）**：不能任意公开或上传的内容，如受试者数据、病历、未公开手稿和公司机密。
- **Human Review（人工审查）**：由人对 claim、citation、代码、表格和最终决定负责；AI 不能替你签名或承担责任。

<a id="文献-rag--qa"></a>
## 🛠 第一个练习：核对一篇 paper 的三个答案
上传前先确认**许可或版权**与**工具条款**都允许。paper 公开可读，不代表可以交给另一个服务。

使用公开 paper：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)。把 paper 加到能显示 citation 的工具，再复制：
```text
请只根据这篇 paper 回答下面三题。每个答案都要附 citation；找不到证据就写“unsupported／未支持”，不要猜。
1. 这篇 paper 想解决什么问题？
2. 作者提出的方法包含哪些主要部分？
3. 作者用哪些实验支持结果，又说了哪些限制？
回答后，列出每个 citation 对应的 original text。不要把你的推测写成作者的 claim。
```
点开每个 citation，把答案和 original text 放在一起读；原文不支持的句子标成 **unsupported／未支持**，不要硬补不相干的引用。

<a id="层级建议"></a>
## 📚 先选一个入口
| 你想做什么 | 先用什么 | 为什么 | 推荐度 |
|---|---|---|---|
| 用浏览器问一篇 paper | [Gemini Notebook（原 NotebookLM）](https://notebooklm.google.com/) | 上传来源后可从 citation 回到原文 | ⭐⭐⭐⭐⭐ |
| 整理自己的文献库 | [Zotero](https://www.zotero.org/) | 先整理 PDF、作者、年份和笔记 | ⭐⭐⭐⭐⭐ |
| 用 Python 做可重跑的文献 RAG | [PaperQA2](https://github.com/Future-House/paper-qa) | 以科学文件和引用为中心 | ⭐⭐⭐⭐⭐ |

Gemini Notebook 是 Google 于 2026-07-16 为 NotebookLM 使用的现行名称；旧名称仅用于辨识。citation 是查证入口，不保证答案正确。

<a id="必修阅读"></a>
## 📖 必读材料
按顺序阅读。前两份提醒你不要把 citation 当保证，后四份帮助保存来源、代码、数据和研究成果：
1. [Gemini Notebook citation 说明](https://support.google.com/gemininotebook/answer/16179559)：点 citation 回到原文并读完整上下文。
2. [Gemini Notebook 隐私与使用条款](https://support.google.com/gemininotebook/answer/17004255)：上传前了解数据怎样被处理。
3. [Zotero 快速入门](https://www.zotero.org/support/quick_start_guide)：整理作者、年份、PDF 和笔记。
4. [PaperQA2 README](https://github.com/Future-House/paper-qa)：了解文献 RAG 如何把回答连回文件。
5. [DVC 常用流程](https://doc.dvc.org/command-reference)：用 Git 管理数据版本和可重跑 pipeline。
6. [Zenodo 快速入门](https://help.zenodo.org/docs/get-started/quickstart/)：将可公开的数据、代码或材料保存成可引用版本。

<a id="精选-projects"></a><a id="大纲与写作"></a><a id="文献管理集成"></a>
## ⭐ 精选研究工具与项目
<small>工具名称、授权与 repository 状态于 2026-08-29 UTC 依据官方页面与 GitHub API 核查。推荐度是本学习地图的编辑评分，不是 GitHub stars 或排行榜。</small>

<table><thead><tr><th scope="col">分类</th><th scope="col">官方工具／项目</th><th scope="col">适合做什么</th><th scope="col">状态／授权</th><th scope="col">先知道的限制</th><th scope="col">推荐度</th></tr></thead>
<tbody><tr><th scope="rowgroup" rowspan="3">开始与整理</th><td><a href="https://notebooklm.google.com/">Gemini Notebook（原 NotebookLM）</a></td><td>用来源问答并回到 citation</td><td>正式可用；云服务</td><td>引用仍要逐条核对；私人数据先看政策</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://www.zotero.org/">Zotero</a></td><td>管理 PDF、metadata、笔记与引用</td><td>正式可用；桌面／Web</td><td>解决来源管理，不替你判断研究质量</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/Future-House/paper-qa">Future-House/paper-qa</a></td><td>用 Python 建立 citation-grounded literature RAG</td><td>活跃；Apache-2.0</td><td>需设置模型与文献来源，质量仍要自行评测</td><td>⭐⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="4">探索与写作</th><td><a href="https://github.com/assafelovic/gpt-researcher">assafelovic/gpt-researcher</a></td><td>多来源搜索与 research brief</td><td>活跃；Apache-2.0</td><td>适合找候选来源，不是引用正确性的最后裁判</td><td>⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/stanford-oval/storm">stanford-oval/storm</a></td><td>整理多种观点，再写大纲与长文</td><td>可用；MIT；更新较慢</td><td>使用前确认依赖与数据来源仍兼容</td><td>⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/kaixindelele/ChatPaper">kaixindelele/ChatPaper</a></td><td>中文 paper 摘要、翻译与写作辅助</td><td>可用；CC BY-NC-ND 4.0</td><td>禁止商业使用与改作，不是一般开源程序授权</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/MuiseDestiny/zotero-gpt">MuiseDestiny/zotero-gpt</a></td><td>在 Zotero 中与文献互动</td><td>可用；AGPL-3.0</td><td>插件与模型设置要另外维护</td><td>⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="5">可重复与证据</th><td><a href="https://github.com/asreview/asreview">asreview/asreview</a></td><td>用 active learning 辅助系统性回顾筛选文献</td><td>活跃；Apache-2.0</td><td>排序能省时间；纳入／排除理由仍需人工筛选并记录</td><td>⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/treeverse/dvc">treeverse/dvc</a></td><td>保存数据版本、模型和可重跑 pipeline</td><td>活跃；Apache-2.0</td><td>需要 Git 与数据存储位置；版本不证明结论正确</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/mlflow/mlflow">mlflow/mlflow</a></td><td>记录每次 run 的参数、指标、数据和产物</td><td>活跃；Apache-2.0</td><td>有记录不等于实验有效；不要把密钥或受试者数据写入 tracking</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://zenodo.org/">Zenodo</a></td><td>保存并发布数据、代码和研究材料，取得 DOI</td><td>正式可用；云服务</td><td>metadata 会公开；私人资料按机构规则去标识或使用核准环境</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/jupyterhub/repo2docker">jupyterhub/repo2docker</a></td><td>从 repository 设置重建可运行研究环境</td><td>活跃；BSD-3-Clause</td><td>container 能保存环境；仍需另存数据、硬件需求与外部服务</td><td>⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="2">研究自动化</th><td><a href="https://github.com/flonat/flonat-research">flonat/flonat-research</a></td><td>参考研究 skills、agents、hooks 与 LaTeX 流程</td><td>活跃；MIT</td><td>基础设施示例，不适用于所有领域</td><td>⭐⭐⭐</td></tr><tr><td><a href="https://github.com/SakanaAI/AI-Scientist-v2">SakanaAI/AI-Scientist-v2</a></td><td>研究端到端 multi-agent 实验架构</td><td>研究参考；custom source-code license</td><td>授权要求披露机器生成的科学稿件；作者仍要人工审查并负责</td><td>⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">历史</th><td><a href="https://github.com/langchain-ai/open_deep_research">langchain-ai/open_deep_research</a></td><td>阅读早期 deep-research agent 架构</td><td>已封存；MIT</td><td>只作历史参考，不是新项目的现行默认</td><td>⭐⭐⭐</td></tr></tbody></table>

## ✅ 完成检查与下一站
- [ ] 我核对了三个答案，不只看 citation 编号。
- [ ] 我找到一个“原文支持”或“未支持”的例子。
- [ ] 我没有上传未获允许的 Private Data。
- [ ] 我保存了来源、问题、工具名称、日期与自己的判断。

下一站：想做文献 RAG，走 [Stage 6](../stages/06-memory-rag.zh-Hans.md)；想让多个 agent 分工，走 [Stage 7](../stages/07-multi-agent-production.zh-Hans.md)；想连接外部工具，看 [MCP／Skills catalog](../resources/mcp-skills-catalog.zh-Hans.md)。

<details markdown="1"><summary>⏱ 展开：时间、账号、费用与数据安全</summary>
第一个练习约需 20–40 分钟。私人数据先停下确认 IRB、机构政策、合约、数据拥有者同意与工具条款。[Gemini Notebook 隐私说明](https://support.google.com/gemininotebook/answer/17004255)称，一般内容不会直接用于训练基础模型，除非用户选择提供 feedback；feedback 可能连同内容交由人员查看。这不等于研究资料自动获准上传。付费功能、配额与机构账号规则会变化，开始前查看官方页面，不保存容易过期的固定价格。
</details>
<a id="研究流程-marketplace"></a><a id="multi-llm-研究组合本-repo-维护者的研究-setup"></a><a id="multi-agent-for-research"></a><a id="必练流程按使用频率"></a>
<details markdown="1"><summary>🧪 展开：把单篇练习变成可重跑研究流程</summary>
### 文献 inbox
保存 DOI、URL、作者、年份与取得日期；让工具生成摘要但把每个 claim 连回原文；由人工决定“阅读、排除、待确认”并记录理由。
### 跨 paper synthesis
先问每篇 paper 各自说什么，再比较同意、冲突和不同条件。不要先要求模型写完整故事，再回头找引用。
### 代码与实验
保存数据版本、environment、seed、prompt、模型／工具版本、输出与人工修改。能重新执行不代表结论正确，但没有记录更难找到错误。
### 投稿前
逐一核对 claim、citation、表格、图、代码与期刊规范；作者仍须最后判断并按期刊政策披露 AI 使用。
</details>
<details markdown="1"><summary>🧯 展开：常见错误、替代方案与排错</summary>
| 问题 | 先怎么做 |
|---|---|
| citation 不支持答案 | 标为未支持，缩小问题，不要硬补相关引用 |
| 工具读不到扫描 PDF | 先做 OCR，再抽查页码与公式 |
| 多篇 paper 结论混在一起 | 要求每个 claim 列 paper 名称、页码或段落，再 synthesis |
| 数据不能上传云端 | 使用机构核准环境；必要时看 [Stage 6](../stages/06-memory-rag.zh-Hans.md) 的本机 RAG 路线 |
| 自动化太复杂 | 回到“一篇 paper、三个问题、逐条核对” |

没有工具能代替 IRB、数据治理、作者责任或领域专家判断。
</details>

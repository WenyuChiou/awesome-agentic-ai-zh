# Extension Path: For Researchers

> [繁體中文](./for-researcher.md) | [简体中文](./for-researcher.zh-Hans.md) | **English**

[← Back to the main route](../README.en.md)

<!-- freshness: canonical=branches/for-researcher.md; verified_on=2026-08-29; scope=research-tools,citations,privacy,reproducibility,project-status; max_age_days=90 -->

<a id="use-cases"></a>
## 📌 What this path helps you do

This page does not make AI your researcher. It helps with one simpler task: **find sources, understand them, and confirm that answers are actually supported by evidence.**

- If you use a terminal or Python, come after [Track A A3](../tracks/cli/A3-cli-production.en.md) or [Track B Stage 7](../stages/07-multi-agent-production.en.md).
- If you do not code, start with the first exercise below. You only need a browser and one public paper.

## 🎯 Learning goals
After this page, you can:
1. Separate what AI says from what the original text says.
2. Check each numbered reference instead of trusting an answer just because it has reference numbers.
3. Know which data may be uploaded and which requires permission from an institution or data owner.
4. Keep enough records for yourself or a colleague to reproduce the work.

## 🧩 Eight core terms
- **Source**: original material used for verification, such as a paper, dataset, or research record.
- **Claim**: a checkable statement, such as “method A performs better on dataset B.”
- **Citation**: a signpost back to a source location; it does not guarantee that the source supports the claim.
- **Source Verification**: open the original and check that content, scope, and limitations match the answer.
- **Literature RAG**: retrieve passages from permitted literature, then give them to a model to answer.
- **Reproducibility**: others can rerun comparable results from your data, steps, versions, and settings.
- **Private Data**: content that cannot be freely published or uploaded, such as participant data, medical records, unpublished manuscripts, or company secrets.
- **Human Review**: a person is responsible for claims, citations, code, tables, and the final decision; AI cannot sign or assume responsibility.

<a id="literature-rag--qa"></a>
## 🛠 First exercise: verify three answers about one paper
Before uploading, confirm that the **license or copyright** and the **tool's terms** allow it. Publicly readable is not permission to upload a paper to another service.

Use the public paper [Attention Is All You Need](https://arxiv.org/abs/1706.03762). Add the paper to a citation-capable tool and paste:
```text
Answer only from this paper. Attach a citation to each answer; if evidence is missing, write “unsupported” and do not guess.
1. What problem does the paper aim to solve?
2. What are the main parts of the proposed method?
3. Which experiments support the result, and what limitations do the authors state?
After answering, list the original text for each citation. Do not present your inference as an author claim.
```
Then open each citation, read answer and original text together, and mark unsupported sentences **unsupported** instead of adding an unrelated citation.

<a id="tier-recommendations"></a>
## 📚 Choose an entry point
<div align="center" markdown="1">

| What you want | Start with | Why | Rating |
|:---|:---|:---|:---|
| Ask about one paper in a browser | [Gemini Notebook (formerly NotebookLM)](https://notebooklm.google.com/) | Return from source uploads to citations | ⭐⭐⭐⭐⭐ |
| Organize your literature library | [Zotero](https://www.zotero.org/) | Organize PDFs, authors, years, and notes first | ⭐⭐⭐⭐⭐ |
| Build rerunnable literature RAG in Python | [PaperQA2](https://github.com/Future-House/paper-qa) | Science-document and citation-centered workflow | ⭐⭐⭐⭐⭐ |

</div>

Gemini Notebook is Google’s current name for NotebookLM as of 2026-07-16; the old name remains for recognition. A citation is an entry point for checking, not a guarantee.

<a id="required-reading"></a>
## 📖 Required reading
Read in order. The first two prevent treating citations as guarantees; the next four help preserve sources, code, data, and results:
1. [Gemini Notebook citation help](https://support.google.com/gemininotebook/answer/16179559): open citations and read context.
2. [Gemini Notebook privacy and terms](https://support.google.com/gemininotebook/answer/17004255): understand data handling before upload.
3. [Zotero quick start](https://www.zotero.org/support/quick_start_guide): organize authors, years, PDFs, and notes.
4. [PaperQA2 README](https://github.com/Future-House/paper-qa): connect literature RAG answers to documents.
5. [DVC command reference](https://doc.dvc.org/command-reference): version data and rerunnable pipelines with Git.
6. [Zenodo quickstart](https://help.zenodo.org/docs/get-started/quickstart/): preserve publishable data, code, or materials in a citable version.

<a id="curated-projects"></a><a id="outline--writing"></a><a id="citation-manager-integrations"></a>
## ⭐ Curated research tools and projects
<small>Tool names, licenses, and repository status were checked against official pages and the GitHub API on 2026-08-29 UTC. Ratings are editorial ratings for this map, not GitHub stars or rankings.</small>

<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="Resources by category, use and limits">
<table align="center"><thead><tr><th scope="col">Group</th><th scope="col">Project / document</th><th scope="col">Rating</th><th scope="col">Use</th><th scope="col">Limits</th></tr></thead>
<tbody><tr><th scope="rowgroup" rowspan="3" align="center" valign="middle" width="80">Start and organize</th><td><div data-field="entry"><strong><a href="https://notebooklm.google.com/">Gemini Notebook (formerly NotebookLM)</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use">Source-grounded Q&A and citations</div></td><td><div data-field="status">Available; cloud service</div><div data-field="limits">Check every citation; review policy before private data</div></td></tr><tr><td><div data-field="entry"><strong><a href="https://www.zotero.org/">Zotero</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use">Manage PDFs, metadata, notes, and citations</div></td><td><div data-field="status">Available; desktop / web</div><div data-field="limits">Manages sources; does not judge research quality</div></td></tr><tr><td><div data-field="entry"><strong><a href="https://github.com/Future-House/paper-qa">paper-qa</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use">Build citation-grounded literature RAG in Python</div></td><td><div data-field="status">Active; Apache-2.0</div><div data-field="limits">Configure model and sources; evaluate quality yourself</div></td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">Explore and write</th><td><div data-field="entry"><strong><a href="https://github.com/assafelovic/gpt-researcher">gpt-researcher</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="use">Multi-source search and research briefs</div></td><td><div data-field="status">Active; Apache-2.0</div><div data-field="limits">Find candidate sources; not the final citation judge</div></td></tr><tr><td><div data-field="entry"><strong><a href="https://github.com/stanford-oval/storm">storm</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="use">Organize viewpoints, outlines, and long-form writing</div></td><td><div data-field="status">Usable; MIT; slower updates</div><div data-field="limits">Check dependencies and sources before use</div></td></tr><tr><td><div data-field="entry"><strong><a href="https://github.com/kaixindelele/ChatPaper">ChatPaper</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use">Chinese paper summaries, translation, and writing support</div></td><td><div data-field="status">Usable; CC BY-NC-ND 4.0</div><div data-field="limits">Noncommercial, no-derivatives license; not a general open-source license</div></td></tr><tr><td><div data-field="entry"><strong><a href="https://github.com/MuiseDestiny/zotero-gpt">zotero-gpt</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="use">Interact with literature in Zotero</div></td><td><div data-field="status">Usable; AGPL-3.0</div><div data-field="limits">Maintain plugin and model settings separately</div></td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="5" align="center" valign="middle" width="80">Repeatable research and evidence</th><td><div data-field="entry"><strong><a href="https://github.com/asreview/asreview">asreview</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="use">Active-learning support for systematic-review screening</div></td><td><div data-field="status">Active; Apache-2.0</div><div data-field="limits">Ranking saves time; human screening still decides inclusion and keeps the record</div></td></tr><tr><td><div data-field="entry"><strong><a href="https://github.com/treeverse/dvc">dvc</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use">Keep data versions, models, and pipelines rerunnable</div></td><td><div data-field="status">Active; Apache-2.0</div><div data-field="limits">Needs Git and storage; versions do not prove conclusions</div></td></tr><tr><td><div data-field="entry"><strong><a href="https://github.com/mlflow/mlflow">mlflow</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use">Track parameters, metrics, data, and artifacts across runs</div></td><td><div data-field="status">Active; Apache-2.0</div><div data-field="limits">Tracking does not make an experiment valid; keep secrets and participant data out</div></td></tr><tr><td><div data-field="entry"><strong><a href="https://zenodo.org/">Zenodo</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use">Publish data, code, and materials with a DOI</div></td><td><div data-field="status">Available; cloud service</div><div data-field="limits">Metadata is public; de-identify private data under institutional rules</div></td></tr><tr><td><div data-field="entry"><strong><a href="https://github.com/jupyterhub/repo2docker">repo2docker</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="use">Rebuild a runnable environment from repository settings</div></td><td><div data-field="status">Active; BSD-3-Clause</div><div data-field="limits">A container preserves the environment; also preserve data, hardware needs, and external services</div></td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="2" align="center" valign="middle" width="80">Research automation</th><td><div data-field="entry"><strong><a href="https://github.com/flonat/flonat-research">flonat-research</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐</span></td><td><div data-field="use">Research skills, agents, hooks, and LaTeX workflows</div></td><td><div data-field="status">Active; MIT</div><div data-field="limits">Infrastructure example, not universal for every field</div></td></tr><tr><td><div data-field="entry"><strong><a href="https://github.com/SakanaAI/AI-Scientist-v2">AI-Scientist-v2</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="use">End-to-end multi-agent research experiments</div></td><td><div data-field="status">Research reference; custom source-code license</div><div data-field="limits">License requires disclosure of machine-generated manuscripts; authors remain responsible</div></td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="1" align="center" valign="middle" width="80">History</th><td><div data-field="entry"><strong><a href="https://github.com/langchain-ai/open_deep_research">open_deep_research</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐</span></td><td><div data-field="use">Study early deep-research agent architecture</div></td><td><div data-field="status">Archived; MIT; historical reference</div><div data-field="limits">Not a current default</div></td></tr></tbody></table>
</div>

## ✅ Completion check and next stop
- [ ] I checked three answers, not just citation numbers.
- [ ] I found an example supported by the original or marked unsupported.
- [ ] I did not upload unapproved Private Data.
- [ ] I saved sources, questions, tool name, date, and my judgment.

Next: use [Stage 6](../stages/06-memory-rag.en.md) for literature RAG; [Stage 7](../stages/07-multi-agent-production.en.md) for multiple agents; and the [MCP / Skills catalog](../resources/mcp-skills-catalog.en.md) for external tools.

<details markdown="1"><summary>⏱ Expand: time, accounts, cost, and data safety</summary>
The first exercise takes about 20–40 minutes. For Private Data, pause and confirm IRB, institutional policy, contracts, data-owner consent, and tool terms. [Gemini Notebook privacy guidance](https://support.google.com/gemininotebook/answer/17004255) says general content is not directly used to train foundation models unless feedback is provided, and feedback may be reviewed by people; this does not automatically approve research uploads. Plans, quotas, and account rules change, so check official pages rather than preserving fixed prices.
</details>
<a id="research-workflow-marketplaces"></a><a id="multi-llm-research-stack-maintainer-setup"></a><a id="multi-agent-for-research"></a><a id="workflows-to-master"></a>
<details markdown="1"><summary>🧪 Expand: turn one-paper practice into a rerunnable workflow</summary>
### Literature inbox
Save DOI, URL, authors, year, and acquisition date; let tools summarize while linking each claim to the original; humans decide read, exclude, or verify and record why.
### Cross-paper synthesis
Ask what each paper says before comparing agreement, conflict, and conditions. Do not ask for a complete story before finding citations.
### Code and experiments
Save data versions, environment, seed, prompt, model/tool versions, outputs, and human edits. Rerunning does not prove correctness, but missing records hide errors.
### Before submission
Check every claim, citation, table, figure, program, and journal rule. Authors make the final judgment and disclose use under journal policy.
</details>
<details markdown="1"><summary>🧯 Expand: common errors, alternatives, and troubleshooting</summary>
| Problem | What to do first |
|---|---|
| Citation does not support the answer | Mark unsupported, narrow the question, and do not force a related citation |
| Tool cannot read a scanned PDF | OCR first, then spot-check pages and formulas |
| Conclusions from papers are mixed | Require paper name and page/paragraph for each claim before synthesis |
| Data cannot go to the cloud | Use an institutional environment; consider the local RAG route in [Stage 6](../stages/06-memory-rag.en.md) |
| Automation is too complex | Return to one paper, three questions, and one-by-one checking |

No tool replaces IRB, data governance, author responsibility, or domain expertise.
</details>

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
| What you want | Start with | Why | Rating |
|---|---|---|---|
| Ask about one paper in a browser | [Gemini Notebook (formerly NotebookLM)](https://notebooklm.google.com/) | Return from source uploads to citations | ⭐⭐⭐⭐⭐ |
| Organize your literature library | [Zotero](https://www.zotero.org/) | Organize PDFs, authors, years, and notes first | ⭐⭐⭐⭐⭐ |
| Build rerunnable literature RAG in Python | [PaperQA2](https://github.com/Future-House/paper-qa) | Science-document and citation-centered workflow | ⭐⭐⭐⭐⭐ |

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

<table><thead><tr><th scope="col">Category</th><th scope="col">Official tool / project</th><th scope="col">Good for</th><th scope="col">Status / license</th><th scope="col">Know this limitation</th><th scope="col">Rating</th></tr></thead>
<tbody><tr><th scope="rowgroup" rowspan="3">Start and organize</th><td><a href="https://notebooklm.google.com/">Gemini Notebook (formerly NotebookLM)</a></td><td>Source-grounded Q&A and citations</td><td>Available; cloud service</td><td>Check every citation; review policy before private data</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://www.zotero.org/">Zotero</a></td><td>Manage PDFs, metadata, notes, and citations</td><td>Available; desktop / web</td><td>Manages sources; does not judge research quality</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/Future-House/paper-qa">Future-House/paper-qa</a></td><td>Build citation-grounded literature RAG in Python</td><td>Active; Apache-2.0</td><td>Configure model and sources; evaluate quality yourself</td><td>⭐⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="4">Explore and write</th><td><a href="https://github.com/assafelovic/gpt-researcher">assafelovic/gpt-researcher</a></td><td>Multi-source search and research briefs</td><td>Active; Apache-2.0</td><td>Find candidate sources; not the final citation judge</td><td>⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/stanford-oval/storm">stanford-oval/storm</a></td><td>Organize viewpoints, outlines, and long-form writing</td><td>Usable; MIT; slower updates</td><td>Check dependencies and sources before use</td><td>⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/kaixindelele/ChatPaper">kaixindelele/ChatPaper</a></td><td>Chinese paper summaries, translation, and writing support</td><td>Usable; CC BY-NC-ND 4.0</td><td>Noncommercial, no-derivatives license; not a general open-source license</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/MuiseDestiny/zotero-gpt">MuiseDestiny/zotero-gpt</a></td><td>Interact with literature in Zotero</td><td>Usable; AGPL-3.0</td><td>Maintain plugin and model settings separately</td><td>⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="5">Reproducibility and evidence</th><td><a href="https://github.com/asreview/asreview">asreview/asreview</a></td><td>Active-learning support for systematic-review screening</td><td>Active; Apache-2.0</td><td>Ranking saves time; human screening still decides inclusion and keeps the record</td><td>⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/treeverse/dvc">treeverse/dvc</a></td><td>Keep data versions, models, and pipelines rerunnable</td><td>Active; Apache-2.0</td><td>Needs Git and storage; versions do not prove conclusions</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/mlflow/mlflow">mlflow/mlflow</a></td><td>Track parameters, metrics, data, and artifacts across runs</td><td>Active; Apache-2.0</td><td>Tracking does not make an experiment valid; keep secrets and participant data out</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://zenodo.org/">Zenodo</a></td><td>Publish data, code, and materials with a DOI</td><td>Available; cloud service</td><td>Metadata is public; de-identify private data under institutional rules</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td><a href="https://github.com/jupyterhub/repo2docker">jupyterhub/repo2docker</a></td><td>Rebuild a runnable environment from repository settings</td><td>Active; BSD-3-Clause</td><td>A container preserves the environment; also preserve data, hardware needs, and external services</td><td>⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="2">Research automation</th><td><a href="https://github.com/flonat/flonat-research">flonat/flonat-research</a></td><td>Research skills, agents, hooks, and LaTeX workflows</td><td>Active; MIT</td><td>Infrastructure example, not universal for every field</td><td>⭐⭐⭐</td></tr><tr><td><a href="https://github.com/SakanaAI/AI-Scientist-v2">SakanaAI/AI-Scientist-v2</a></td><td>End-to-end multi-agent research experiments</td><td>Research reference; custom source-code license</td><td>License requires disclosure of machine-generated manuscripts; authors remain responsible</td><td>⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">History</th><td><a href="https://github.com/langchain-ai/open_deep_research">langchain-ai/open_deep_research</a></td><td>Study early deep-research agent architecture</td><td>Archived; MIT; historical reference</td><td>Not a current default</td><td>⭐⭐⭐</td></tr></tbody></table>

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

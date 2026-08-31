# The `resources/` Tool Cabinet

<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <strong>English</strong>
</div>

Think of this folder as a tool cabinet. When you get stuck, take only the card you need now. **You do not need to read every file from top to bottom.**

## 🧭 What are you stuck on?

| What you want to do now | Open this first |
|---|---|
| I have never coded and do not know where to start | [`setup-guide.en.md`](setup-guide.en.md) |
| I want to follow the complete learning map | [Home](../README.en.md) → [Stage 0](../stages/00-foundations.en.md) |
| I cannot tell how models learn, how they are adapted, and when they are only producing an answer | [`model-training-guide.en.md`](model-training-guide.en.md) |
| I see a term but do not know what it means | [Term lookup](glossary.en.md) |
| I cannot tell these names apart: OpenRouter = unified model API/router; Ollama = local model runtime; OpenCode/Pi = coding agents/toolkits | [`cli-agents-guide.en.md`](cli-agents-guide.en.md) |
| I want to build my first action card (Skill), tool connector (MCP server), or document workflow | [Hands-on recipes](cookbook.en.md) |
| I wrote a tool description (tool schema), but the model keeps choosing the wrong tool | [`schema-design-cheatsheet.en.md`](schema-design-cheatsheet.en.md) |
| I need a tool for Notion, Office, a database, or a browser | [`mcp-skills-catalog.en.md`](mcp-skills-catalog.en.md) |
| I want to choose a course or check whether a certificate helps | [`courses.en.md`](courses.en.md) |
| I want to know whether an agent works in a terminal, editor, cloud, or my own device | [`agent-paradigms.en.md`](agent-paradigms.en.md) |
| I want a helper-agent (subagent) dispatch example I can copy now | [`subagent-cookbook.en.md`](subagent-cookbook.en.md) |
| I want to design, combine, or debug helper agents (subagents) | [`subagent-advanced.en.md`](subagent-advanced.en.md) |
| I want to write content or send a PR to this project | [`style-guide.en.md`](style-guide.en.md) |

## 🧩 Five words to know first

- **Reference**: something you return to when stuck, not another required course.
- **Guide**: helps you make choices along one path.
- **Cookbook**: gives you small, complete examples you can follow.
- **Catalog**: keeps many tools in one searchable, comparable place.
- **Glossary**: gives a short definition, then sends you to the chapter with the full explanation.

## 📚 All 12 references

The left column merges resources of the same type. This table stays visible because learners need to see which entrances exist.

<table>
<thead><tr><th scope="col">Type</th><th scope="col">File</th><th scope="col">Best time to read it</th><th scope="col">What it does not do</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Start and choose</th><td><a href="setup-guide.en.md">setup-guide.en.md</a></td><td>Your first choice among Web, Desktop, IDE, CLI, and API</td><td>Does not replace each product’s current installation page</td></tr>
<tr><td><a href="glossary.en.md">glossary.en.md</a></td><td>Look up one term in 30 seconds</td><td>Does not replace a full chapter or practice</td></tr>
<tr><td><a href="cli-agents-guide.en.md">cli-agents-guide.en.md</a></td><td>Separate models, model entrances (routers), execution environments (runtimes), and coding agents</td><td>Does not grant permissions or choose a paid plan for you</td></tr>
<tr><td><a href="courses.en.md">courses.en.md</a></td><td>Compare courses, practice depth, and certificate limits</td><td>Does not promise that a certificate gets you a job</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Build and debug</th><td><a href="cookbook.en.md">cookbook.en.md</a></td><td>Build a Skill, MCP, Office, Gemini Notebook, Zotero, or local CLI workflow</td><td>Does not turn every topic into a textbook</td></tr>
<tr><td><a href="schema-design-cheatsheet.en.md">schema-design-cheatsheet.en.md</a></td><td>A tool or its parameters are often wrong</td><td>Does not teach complete MCP server installation</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="3">Search and position</th><td><a href="model-training-guide.en.md">model-training-guide.en.md</a></td><td>Separate Pre-training, Post-training, Fine-tuning, and Inference</td><td>Is not a complete course on training a model from scratch</td></tr>
<tr><td><a href="mcp-skills-catalog.en.md">mcp-skills-catalog.en.md</a></td><td>Find a tool connector (MCP server) or action card (Skill) by job</td><td>Listing does not mean risk-free or permanently available</td></tr>
<tr><td><a href="agent-paradigms.en.md">agent-paradigms.en.md</a></td><td>See whether an agent runs in a terminal, editor, cloud, or your own device</td><td>Is not a product leaderboard</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Advanced subagents</th><td><a href="subagent-cookbook.en.md">subagent-cookbook.en.md</a></td><td>Copy a helper-agent dispatch example first</td><td>Does not explain every design principle</td></tr>
<tr><td><a href="subagent-advanced.en.md">subagent-advanced.en.md</a></td><td>Design, combine, and debug helper agents</td><td>Is not where a first-time CLI-agent user should begin</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="1">Maintain the project</th><td><a href="style-guide.en.md">style-guide.en.md</a></td><td>Write entries, translate, build tables, or send a PR</td><td>Is not required reading for ordinary learners</td></tr>
</tbody>
</table>

## 🔁 Where do you return next?

- First-time learner: return to [Stage 0](../stages/00-foundations.en.md).
- Want to finish work with a CLI: return to [Track A1](../tracks/cli/A1-cli-intro.en.md).
- Want to build an Agent: return to [Stage 3](../stages/03-tool-use-and-hello-agent.en.md).
- Want to choose an entrance again: return to [Home](../README.en.md).

## ✅ 30-second completion check

- [ ] I know which one file I need now.
- [ ] I am not treating the catalog as a textbook to read from start to finish.
- [ ] I know where to return on the main route afterward.

<details markdown="1">
<summary>Why not combine all 12 references into one book?</summary>

They solve different problems. The Glossary is a 30-second lookup, a Stage builds a concept in a few minutes, the Cookbook helps you make something, and the Catalog helps you search for tools. Mixing them into one book would make the entrance harder to find.

For chapter-length Chinese lessons, continue with [Hello-Agents](https://github.com/datawhalechina/hello-agents). This project helps you find the route instead of rewriting another long textbook.

</details>

<details markdown="1">
<summary>Maintainers: locale coverage and rules for a new reference</summary>

All 12 references above have Traditional Chinese, English, and Simplified Chinese versions. Before adding another reference, confirm all four rules:

1. It has a job that no existing file can replace.
2. At least three stages, tracks, or branches will need it.
3. Terms, URLs, limitations, and safety rules can stay aligned across three locales.
4. If it serves only one chapter, keep it in that chapter instead of creating another file.

Traditional Chinese is the source version: zh-TW is canonical. Verify official sources first. If the answer is unknown, say so instead of guessing. Do not preserve drifting GitHub stars, fixed totals, and line counts.

Before submitting a change, check the [MCP/Skills catalog](mcp-skills-catalog.en.md), [Cookbook](cookbook.en.md), [style guide](style-guide.en.md), and [CONTRIBUTING](../CONTRIBUTING.en.md).

</details>

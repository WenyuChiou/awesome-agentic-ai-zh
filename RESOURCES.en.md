# Related Resources

> [繁體中文](./RESOURCES.md) | [简体中文](./RESOURCES.zh-Hans.md) | **English**

> [← Back to main README](README.en.md)

## 📌 Choose what you want to do now

You do not need to read the whole list. Pick the task you want to do now:

<div align="center" markdown="1" class="reader-table-picker reader-table-picker--task" role="region" tabindex="0" aria-label="Choose resources by need">

| I want to… | Start here |
|:---|:---|
| Learn AI agents from the beginning | [Stage 0](stages/00-foundations.en.md)<br>⭐⭐⭐⭐⭐ |
| Understand how models learn and how they are used | [Model training guide](resources/model-training-guide.en.md)<br>⭐⭐⭐⭐⭐ |
| Look up an unfamiliar term | [Glossary](resources/glossary.en.md)<br>⭐⭐⭐⭐ |
| Choose a CLI agent | [CLI Agents Guide](resources/cli-agents-guide.en.md)<br>⭐⭐⭐⭐⭐ |
| Connect an Agent to external tools | [MCP / Skills Catalog](resources/mcp-skills-catalog.en.md)<br>⭐⭐⭐⭐⭐ |
| Build a small project step by step | [Cookbook](resources/cookbook.en.md)<br>⭐⭐⭐⭐⭐ |

</div>

<a id="three-core-terms-mcp--skills--plugins"></a>
## 🧩 Three core terms: MCP, Skill, and Plugin

**MCP (Model Context Protocol)**: an open protocol that lets AI applications connect to external data and tools through a shared method. What it can do still depends on the server, account permissions, and user approval.

**Skill**: a reusable package of instructions that may also include scripts, templates, and references. Different products place and load Skills differently.

**Plugin**: an installable package provided by a host. It may bundle Skills, commands, hooks, or MCP configuration; Plugins are not part of the MCP specification.

For a hands-on example, go to [Stage 5](stages/05-claude-code-ecosystem.en.md). To separate Apps / Connectors, CLI Agents, and MCP Servers, see the [CLI Agents Guide](resources/cli-agents-guide.en.md).

## 📚 Five safe starting points

Start with official entry points or complete learning materials, then evaluate community projects. These are editorial ratings, not GitHub stars.

<div align="center" markdown="1" class="reader-table-picker reader-table-picker--source" role="region" tabindex="0" aria-label="Choose resources by need">

| Starting point | Learn first |
|:---|:---|
| [Official MCP Registry](https://registry.modelcontextprotocol.io/)<br>⭐⭐⭐⭐⭐ | Find published MCP Servers; still check the maintainer, permissions, and source |
| [servers](https://github.com/modelcontextprotocol/servers)<br>⭐⭐⭐⭐⭐ | See educational reference implementations; they are not a production recommendation |
| [skills](https://github.com/anthropics/skills)<br>⭐⭐⭐⭐⭐ | See how Agent Skill folders, instructions, and resources fit together |
| [github-mcp-server](https://github.com/github/github-mcp-server)<br>⭐⭐⭐⭐⭐ | Learn OAuth, tool groups, and repository permissions from an official implementation |
| [hello-agents](https://github.com/datawhalechina/hello-agents)<br>⭐⭐⭐⭐⭐ | Learn Agent principles and implementation through a Chinese-language course |

</div>

> ⚠️ **Start with fewer keys**: an MCP Server may read, create, send, or delete real data. Begin with read-only access, least privilege, and a test workspace; keep **Human Approval** before write, send, or delete actions.

<a id="daily-tool-integrations"></a>
<a id="daily-tool-integrations-mcp-servers--skills"></a>
## 🔌 Common integration groups

The table below shows selected projects and official entry points directly. Start with the group you need; only the longer supplemental list is collapsed.

<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="Selected resources table">
<table align="center">
<thead><tr><th scope="col">Group</th><th scope="col">Project / document</th><th scope="col">Rating</th><th scope="col">Use</th><th scope="col">Limits</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">Notes / Knowledge Bases</th><td><div data-field="entry"><strong><a href="https://developers.notion.com/guides/mcp/overview">Notion MCP</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Search, create, and update Notion content</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Official hosted MCP; user OAuth required and permissions follow the signed-in user</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/MarkusPfundstein/mcp-obsidian">mcp-obsidian</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Read and write an Obsidian vault</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Community project; grant only the vault and write scope needed</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://support.google.com/gemininotebook/answer/16164461">Gemini Notebook (formerly NotebookLM)</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Summarize and ask questions about your own sources</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Google service; availability varies by region, account, and feature</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/teng-lin/notebooklm-py">notebooklm-py</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Operate Gemini Notebook through Python / CLI</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Unofficial interface; Google changes may break it</div></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="3" align="center" valign="middle" width="80">Office Documents</th><td><div data-field="entry"><strong><a href="https://github.com/anthropics/skills">skills</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Read Agent Skill examples and document workflows</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Official examples; built-in Skills vary by Claude surface</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/tfriedel/claude-office-skills">claude-office-skills</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Extend Office document automation workflows</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Community Skills; back up files and verify outputs</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://developers.google.com/workspace/guides/configure-mcp-servers">Google Workspace MCP</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Connect Gmail, Drive, Docs, Sheets, Slides, Calendar, and Chat</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Official <strong>Developer Preview</strong>; each product has a dedicated server, with OAuth 2.0 and user / organization governance</div></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">Dev teamwork</th><td><div data-field="entry"><strong><a href="https://github.com/github/github-mcp-server">GitHub MCP Server</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Query and work with issues, PRs, and repositories</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Official MCP; use OAuth or a least-privilege token and approve high-impact writes</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/">Atlassian Rovo MCP</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Search or update Jira, Confluence, and Bitbucket</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Official hosted remote MCP; OAuth 2.1 and signed-in user permissions apply; require human approval before writing real data</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://linear.app/docs/mcp">Linear MCP</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Search and update Linear issues / projects</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Official hosted remote MCP over Streamable HTTP; an official read-only option exists</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://docs.slack.dev/ai/mcp-overview/">Slack MCP</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Search Slack, send messages, and manage canvases</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Official MCP; it is not read-only, so confirm before sending or changing content</div></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">Research Workflow</th><td><div data-field="entry"><strong><a href="https://github.com/WenyuChiou/ai-research-skills">ai-research-skills</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Turn research steps into reusable Skills</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Community project; install only Skills relevant to the current task</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/WenyuChiou/research-hub">research-hub</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Connect Zotero, Obsidian, and research workflows</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Community workspace; check data location, backups, and permissions</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/WenyuChiou/zotero-skills">zotero-skills</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Organize Zotero data with Skills</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Community Skill; back up the library before batch changes</div></td></tr>
<tr><td><div data-field="entry"><strong><a href="https://github.com/WenyuChiou/codex-delegate">codex-delegate</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Delegate clearly scoped repetitive work to another Agent</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Community tool; lock files, acceptance criteria, and stop conditions first</div></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="1" align="center" valign="middle" width="80">Chinese Ecosystem</th><td><div data-field="entry"><strong><a href="https://github.com/leemysw/feishu-docx">feishu-docx</a></strong></div></td><td align="center" valign="middle"><span data-field="rating">⭐⭐⭐⭐</span></td><td><div data-field="use"><strong>Use:</strong> Convert between Feishu (Lark) documents and Markdown</div></td><td><div data-field="limits"><strong>Status / limits:</strong> Community tool; confirm sharing and write permissions</div></td></tr>
</tbody>
</table>
</div>

<a id="research-workflow"></a>
<a id="research-workflow-by-the-repo-maintainer"></a>
<a id="topic-awesome-lists"></a>
<a id="topic-based-awesome-lists"></a>
<details markdown="1">
<summary>Expand more lists, courses, and design tools</summary>

- [MCP Registry](https://registry.modelcontextprotocol.io/): the official discovery entry point for published Servers.
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers): browse community Servers by category; review before installing.
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code): Claude Code community resources.
- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills): Agent Skills community list.
- [Canva MCP](https://www.canva.dev/docs/mcp/): official remote MCP; features, plans, and permissions depend on the account, so no fixed tool count is stated.
- [Course list](resources/courses.en.md): choose courses by learning goal; a certificate is not a degree.
- [Agent paradigms](resources/agent-paradigms.en.md): compare common Agent shapes with diagrams.

</details>

<a id="what-else"></a>
## ✅ Next stop

- Unclear term: open [`resources/glossary.en.md`](resources/glossary.en.md).
- Want to build now: open [`resources/cookbook.en.md`](resources/cookbook.en.md).
- Want to understand training choices: open [`resources/model-training-guide.en.md`](resources/model-training-guide.en.md).
- Want to contribute or translate: read [`resources/style-guide.en.md`](resources/style-guide.en.md) and [`CONTRIBUTING.en.md`](CONTRIBUTING.en.md).

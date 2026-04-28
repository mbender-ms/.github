---
name: one-pager
description: >-
  Generate a formatted project one-pager from any input source (chat, Word doc, Excel spreadsheet,
  PDF, or other file). Pulls live M365 data (owner, team, ADO items, org hierarchy, Teams/SharePoint
  sites, calendar milestones) via WorkIQ MCP. Output is a structured Markdown file with header block,
  owners table, timeline, methodology, success metrics, risks, and next steps.
  WHEN: one-pager, one pager, project brief, project summary, project document, create one-pager,
  write a one-pager, draft a one-pager.
argument-hint: "Describe the project or provide a file path, e.g. 'create a one-pager for the AI Quality Pilot' or 'C:\\docs\\project-notes.docx'"
user-invocable: true
---

# One-Pager — Project Summary Generator

Generates a table-based project one-pager from any input. Fetches live M365 data via WorkIQ.

## When to Use

- Creating a project brief for a new initiative or planning cycle
- Converting project notes, a Word doc, Excel spreadsheet, or chat summary into a one-pager
- Refreshing an existing one-pager with current ADO status or timeline

## Workflow

### Step 0 — WorkIQ pre-flight

Before doing anything else, check whether the WorkIQ MCP server is available.

**Check**: Use `tool_search` with query `"workiq"` to see if `mcp_workiq_*` tools are loaded.

| Result | Action |
|---|---|
| Tools found (`mcp_workiq_accept_eula`, `mcp_workiq_ask_work_iq`) | Call `mcp_workiq_accept_eula` immediately, then proceed to Step 1 |
| Tools NOT found | Show the enable instructions below, then **pause and ask the user to confirm WorkIQ is enabled before continuing** |

**If WorkIQ is not available:** Tell the user: *Open Command Palette (`Ctrl+Shift+P`) → MCP: List Servers → Enable workiq → accept EULA. Reply "WorkIQ is enabled" to continue.* Then pause.

### Step 1 — Gather project inputs

Accept project details from any of these sources — use whichever the user provides:

| Source type | How to handle |
|---|---|
| Text in chat | Extract project details directly |
| `.docx` / `.doc` / `.pdf` | Delegate to `artifact-conversion` skill, then extract |
| `.xlsx` / `.csv` | Delegate to `artifact-conversion` skill; treat each table as a data section |
| Existing `.md` one-pager | Read with `read_file`; treat as base to refresh |
| No input given | Ask: *"Describe the project or provide a file path."* |

After extraction, identify (use `<unknown>` for missing fields): project name, goal, service area(s), owner aliases, ADO IDs, scope, timeline, success metrics, risks.

### Step 2 — Query WorkIQ for M365 data

For each identified owner alias or project name, call `mcp_workiq_ask_work_iq` to resolve live data.
Make separate focused queries rather than one large query for better results.

| Data to fetch | Example WorkIQ query |
|---|---|
| Owner contact details | `"What is the alias and email for [name]?"` |
| Team members and roles | `"Who are the team members and owners for [project/service]?"` |
| Org hierarchy / manager | `"Who is the manager of [alias]?"` |
| ADO work item details | `"What is the title, status, and target date for ADO item [ID]?"` |

> [!NOTE]
> If WorkIQ cannot resolve a field, leave it as `<verify manually>` — do not fabricate values.

### Step 3 — Populate the template

Load [templates/project-one-pager.md](templates/project-one-pager.md) and fill in every `<placeholder>` field
with data gathered in Steps 1–2.

Population rules:

- **Header block**: Derive goal from project description; infer ACC initiative if not explicit (common: *Maintain quality content*, *Improve discoverability*, *Help customers solve problems*)
- **Owners table**: One row per service or team; ADO links as `[ID](https://dev.azure.com/msft-skilling/Content/_workitems/edit/ID)`
- **Methodology table**: Include only if the project has defined tools or AI-assisted phases; omit otherwise
- **Success metrics**: Specific, measurable statements only
- Leave `<verify manually>` for unresolved fields — never invent data

### Step 4 — Confirm output path

Ask the user where to save the file:

> *"Where should I save the one-pager? (For example: `C:\path\to\project-one-pager.md`)"*

If the user provided a source file in Step 1, suggest the same folder with a generated filename:
`<project-name-kebab>-one-pager.md`

> [!NOTE]
> Do NOT write the file until the user provides or confirms the output path.

### Step 5 — Write and confirm

1. Write the populated one-pager to the specified path using `create_file`
2. Report the absolute file path
3. Show the first 10 lines as a preview
4. List any `<verify manually>` fields that need the user's attention

## Reference Files

- [templates/project-one-pager.md](templates/project-one-pager.md) — One-pager template with all sections and placeholders
- `artifact-conversion` skill — Delegate all non-text file ingestion here; do not re-implement conversion logic

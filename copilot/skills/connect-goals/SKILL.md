---
name: connect-goals
version: 1.0.0
category: Planning
description: "Setup and update Connect SMART goal tracking. Dual-mode: 'setup' parses your Connect document and creates GOALS.md with baseline queries; 'update' runs stored queries against ADO/GitHub to refresh progress data. The monthly-report skill reads the resulting GOALS.md (zero queries) to render progress visualizations."
argument-hint: 'setup "path/to/connect.md" | update | update march'
user-invocable: true
disable-model-invocation: false
---

# Connect Goals Skill

Track semester SMART goal progress by querying ADO, GitHub, and session summaries. Two modes:

**Invocation:**
- `/connect-goals setup "path/to/your-connect-document.md"` — Parse Connect doc, create GOALS.md (run once per semester)
- `/connect-goals update` — Refresh all goal progress from live data (run monthly or before 1:1s)
- `/connect-goals update march` — Same, but specify which month's data to emphasize

**Output:** Updates `~/.copilot/skills/connect-goals/GOALS.md` in place.

**Relationship to monthly report:** The `/monthly-report` skill reads GOALS.md as a static file (~500 tokens). This skill does the heavy querying so the monthly report doesn't have to.

---

## Prerequisites

Before running setup, the agent should gather context:

1. **Author settings** — Call `get_author_settings` to get the user's ADO org, project, team, and service area
2. **Session export directory** — Read from `cda.sessionExportDir` setting (session summaries are in `{export-directory}/Session Summaries/`)
3. **Connect document path** — User provides this as the argument to `/connect-goals setup`

If the user doesn't provide a path, prompt: *"Where is your Connect document? Provide the file path (e.g., `D:\Documents\My-Connect-FY26H2.md`)"*

---

## Mode 1: Setup (once per semester)

**When to run:** After Connect goals are finalized with manager, or at the start of a new Connect period.

**Input:** Path to the Connect markdown document.

### Step 1: Gather user context

```
# Get author settings for ADO org/project
get_author_settings → { adoOrg, adoProject, name, team, ... }

# Read the Connect document
read_file(connect_doc_path)
```

Extract the **"Plan for the future"** section. Parse each SMART goal, identifying:
- Goal number and category (Goal 1, 2, 3)
- Full goal text (the quoted commitment)
- Target type: `milestone` (done/not done), `quantitative` (N of M), `recurring` (monthly)
- Target value: number for quantitative, description for milestone/recurring
- Measurement approach: what data source proves progress

### Step 2: Build queries for each goal

For each goal, construct the stored queries that `/connect-goals update` will run later. Use the author's ADO org and project from `get_author_settings`.

**ADO-based goals** — Build a WIQL query:

```
Goal: "Close 50% of assigned feedback items"
→ wiql_query: "SELECT [System.Id] FROM workitems WHERE [System.WorkItemType] = 'User Feedback' AND [System.State] = 'Closed' AND [System.AssignedTo] = @me AND [Microsoft.VSTS.Common.ClosedDate] >= '{semester_start}'"
→ count_method: "count_results"
```

```
Goal: "Update all articles in my service area"
→ wiql_query: "SELECT [System.Id] FROM workitems WHERE [System.Title] CONTAINS '{keyword}' AND [System.WorkItemType] IN ('User Story') AND [System.State] = 'Closed' AND [System.AssignedTo] = @me AND [Microsoft.VSTS.Common.ClosedDate] >= '{semester_start}'"
→ count_method: "count_results"
```

**GitHub-based goals** — Build a search pattern:

```
Goal: "Merge PRs for content improvement"
→ github_query: { repo: "{user's primary repo}", search: "{keyword}", state: "merged" }
```

**Recurring/qualitative goals** — Mark as `manual`:

```
Goal: "Attend team meetings 3+ days/week"
→ measurement: "manual"
→ update_prompt: "How many days/week did you meet this target? (target: 3+)"
```

### Step 3: Run baseline queries

For each quantitative goal, run the query NOW to establish the starting point. Use the ADO org from author settings:

Call `mcp_ado_wit_query` with:
- `query`: the stored `wiql_query` for this goal
- `project`: `{ado_project}` (from `get_author_settings`)

The MCP tool returns structured JSON — count the results directly (no temp files or BOM stripping needed).

> **Fallback (requires `az login`):** `az boards query --wiql '{wiql_query}' --org https://dev.azure.com/{ado_org} -p {ado_project} -o json`

Parse results to get the count at semester start.

### Step 4: Write GOALS.md

Generate the complete `~/.copilot/skills/connect-goals/GOALS.md` file with:
- Semester metadata (period, Connect doc path, start date)
- All goals with structured fields (id, title, short, description, target_type, target, baseline, current, status, evidence)
- **Stored queries** (`wiql_query`, `github_query`, or `measurement: manual`)
- Empty Monthly Snapshots table with month columns
- Status legend

Use the templates/GOALS-TEMPLATE.md in this skill folder as the format reference.

**Use `create_file` or `replace_string_in_file`** to write the file.

### Step 5: Confirm

Display summary:
```
✅ Created GOALS.md with {N} goals
   - {N} quantitative (with stored WIQL queries)
   - {N} milestone
   - {N} recurring (manual update)
   Baselines established as of {date}
   
   Next: Run `/connect-goals update` after your first monthly report.
```

---

## Mode 2: Update (monthly or on-demand)

**When to run:** After generating a monthly report, before 1:1s, or during Connect review writing.

### Step 1: Read current GOALS.md and author settings

```
read_file("~/.copilot/skills/connect-goals/GOALS.md")
get_author_settings → { adoOrg, adoProject, ... }
```

Parse all goals, their stored queries, and current values.

### Step 2: Run stored queries

**For each goal with `wiql_query`:**

Call `mcp_ado_wit_query` with:
- `query`: the stored `wiql_query` for this goal
- `project`: `{ado_project}` (from `get_author_settings`)

The MCP tool returns structured JSON — count the results directly.

> **Fallback (requires `az login`):** `az boards query --wiql '{wiql_query}' --org https://dev.azure.com/{ado_org} -p {ado_project} -o json`, then parse with `node -e` (strip BOM: `if(raw.charCodeAt(0)===0xFEFF)raw=raw.slice(1)`).

**For each goal with `github_query`:**

Use `mcp_github_search_pull_requests` or `mcp_github_list_pull_requests` to count merged PRs matching the pattern.

**For recurring/manual goals:**

Read the latest session summaries for the current month from the CDA export directory (`{export-directory}/Session Summaries/`). Look for evidence patterns matching the goal's keywords.

Ask the user to confirm any manual goals with the stored `update_prompt`.

### Step 3: Compute progress and status

For each quantitative goal:
```
progress_pct = (current / target) * 100
months_elapsed = months since semester start
total_months = total semester length (typically 6)
expected_pct = (months_elapsed / total_months) * 100

if current >= target:
    status = "exceeded" if current > target * 1.1 else "done"
elif progress_pct >= expected_pct:
    status = "on-track"
else:
    status = "at-risk"
```

For milestones: check if the associated ADO work item is Closed → `done`, else check if Active → `on-track`, else → `not-started`

### Step 4: Update evidence

For each goal, compile fresh evidence from this month:
- New ADO work item IDs closed this month that contribute to the goal
- New PR numbers merged this month
- Key accomplishments from session summaries

Append to existing evidence (don't overwrite — evidence accumulates over the semester).

### Step 5: Update Monthly Snapshots table

Add or update the current month's column in the snapshots table:

```markdown
| Goal | Month1 | Month2 | Month3 | ... | Current |
|------|--------|--------|--------|-----|---------|
| 1.1  | 0      | 5      | 12     | ... | {new}   |
```

### Step 6: Write updated GOALS.md

Use `replace_string_in_file` to update the `current`, `status`, `evidence`, and snapshots table fields in GOALS.md. Don't rewrite the entire file — update fields in place to preserve any manual notes the user added.

### Step 7: Confirm

Display summary:
```
✅ Updated GOALS.md — {month} {year}

   Goal                    Status      Progress
   ─────────────────────   ────────    ────────
   1.1 {goal short}        ✅ Done     {current}/{target} (100%)
   1.2 {goal short}        🔄 On Track {current}/{target} ({pct}%)
   2.1 {goal short}        ⚠️ At Risk  {current}/{target} ({pct}%)
   3.1 {goal short}        🌟 Exceeded {current}/{target} ({pct}%)
   ...
   
   Monthly report can now read GOALS.md for progress visualizations.
```

---

## Query Templates Reference

### WIQL patterns for common goal types

**Count closed items by type since semester start:**
```sql
SELECT [System.Id] FROM workitems
WHERE [System.WorkItemType] = '{type}'
AND [System.State] = 'Closed'
AND [System.AssignedTo] = @me
AND [Microsoft.VSTS.Common.ClosedDate] >= '{semester_start}'
```

**Count closed items matching title pattern:**
```sql
SELECT [System.Id] FROM workitems
WHERE [System.Title] CONTAINS '{keyword}'
AND [System.State] = 'Closed'
AND [System.AssignedTo] = @me
AND [Microsoft.VSTS.Common.ClosedDate] >= '{semester_start}'
```

**Check milestone completion (single work item):**
```sql
SELECT [System.Id],[System.State] FROM workitems
WHERE [System.Id] = {work_item_id}
```

### GitHub patterns

**Count merged PRs in a repo with keyword:**
```
mcp_github_search_pull_requests(query="{keyword}", owner="{owner}", repo="{repo}", state="closed")
→ filter by merged_at >= semester_start
```

### Session summary patterns

**Recurring goals — grep session summaries:**
```bash
grep -l "{keyword}" "{session_export_dir}/Session Summaries/session-summary-{YYYY-MM}"*.md | wc -l
```

---

## Semester Lifecycle

| When | Action | Command |
|------|--------|---------|
| **Semester start** | Create GOALS.md from Connect doc | `/connect-goals setup "path/to/connect.md"` |
| **Each month (before report)** | Refresh progress with live data | `/connect-goals update` |
| **Each month (after update)** | Generate report with fresh goals data | `/monthly-report` |
| **Before 1:1** | Quick refresh for talking points | `/connect-goals update` |
| **Connect review** | Final update, screenshot goals section | `/connect-goals update` then `/monthly-report` |
| **New semester** | Archive old GOALS.md, create new one | Rename old file, run `setup` with new Connect doc |

---

## Archiving Between Semesters

When a new Connect period starts:
1. Rename: `GOALS.md` → `GOALS-{codename}-{period}.md` (keep as historical record)
2. Run `/connect-goals setup` with the new Connect document
3. The monthly report skill picks up the new GOALS.md automatically

---
name: monthly-report
category: Reports
version: 1.0.0
description: Generate a comprehensive monthly report for manager visibility, showcasing Big Rocks, accomplishments, and impact. Reads session summaries, validates with ADO and GitHub APIs, and produces both markdown and styled HTML reports. Use this skill whenever the user mentions monthly reports, manager updates, accomplishment tracking, monthly summaries, or wants to document what they did this month — even if they don't say "monthly report" explicitly.
argument-hint: 'month name or "last month" (e.g., "march", "february 2026")'
relevant-lesson-tags: [monthly-report, ado, github, productivity, big-rocks]
user-invocable: true
disable-model-invocation: false
---

# Monthly Report Skill

Generate a comprehensive monthly report documenting work completed in the target month. This report is for manager visibility and showcases Big Rocks, accomplishments, and impact. Always produces BOTH markdown and HTML versions.

**Invocation:**
- `/monthly-report` or `/monthly-report last month` — Report on the previous month
- `/monthly-report march` or `/monthly-report march 2026` — Report on a specific month

**Optional: Connect Goals progress tracking**
If `~/.copilot/skills/connect-goals/GOALS.md` exists, the report includes a semester goals progress strip and detail section. If the file doesn't exist, these sections are silently omitted — no errors, no empty sections.

> **Teammates**: To add Connect Goals tracking to your reports, copy `~/.copilot/skills/connect-goals/templates/GOALS-TEMPLATE.md` to `~/.copilot/skills/connect-goals/GOALS.md` and fill in your SMART goals from your Connect document. The skill auto-detects the file and generates progress visualizations.

**CRITICAL**: Every metric must trace to a WIQL query or GitHub API response. Session summaries provide narrative context, not authoritative counts. NEVER estimate counts from session data alone.

**Data verification model (three layers):**
1. **WIQL → authoritative list** — "What actually closed this month?" (exact IDs, counts, SP, AreaPath, Parent)
2. **MCP batch-fetch + GitHub API → detail enrichment** — titles, descriptions, PR stats, merge dates
3. **Session summaries → narrative context** — the story behind each item: decisions, blockers, technical details ADO metadata doesn't capture

**Output** (uses the CDA export directory configured in extension settings, under `Monthly Reports` subfolder):
- **Markdown**: `{export-directory}/Monthly Reports/monthly-report-{month}-{year}.md`
- **HTML**: `{export-directory}/Monthly Reports/monthly-report-{month}-{year}.html`

**Style reference**: Always read the previous month's HTML report as a visual baseline. The [HTML template](./templates/monthly-report-template.html) (v3) defines the required CSS and component structure.

**Dual theme + Lucide icons (v3)**: The template ships two themes — **dark** (default, for personal use) and **executive** (light, navy + gold, for sharing with managers / Connect docs). Users toggle via the Lucide `moon` / `landmark` icon in the top-right controls; preference persists in `localStorage('report-theme-v2')`. Both themes use Segoe UI throughout. All icons are Lucide SVGs loaded via the CDN at the bottom of `<body>` — use `<i data-lucide="NAME" class="lui"></i>` wherever you'd previously have used an emoji.

**Author identity**: Before generating reports, call the `get_author_settings` tool to get the user's name, email, team, role, and service area. Use these values to fill in template placeholders like `{Author Name}`, `{email}`, `{Team Name}`, and `{Role/Lead Title}`.

---

## Phase 1: Read Session Summaries

**Create todo list and start Phase 1:**

```
manage_todo_list([
  { id: 1, title: "Read session summaries", description: "Read all session-summary-YYYY-MM-*.md files for target month", status: "in-progress" },
  { id: 2, title: "Extract & deduplicate", description: "Compile unique work item IDs, PR numbers, group by theme", status: "not-started" },
  { id: 3, title: "Validate with ADO", description: "Fetch work item details via smart query tools", status: "not-started" },
  { id: 4, title: "Validate with GitHub", description: "Fetch PR details (title, merged_at, files, additions/deletions)", status: "not-started" },
  { id: 5, title: "Categorize & synthesize", description: "Group by category, identify Big Rocks, compute metrics", status: "not-started" },
  { id: 6, title: "Generate reports", description: "Create both markdown and HTML monthly reports", status: "not-started" }
])
```

**Actions:**

1. List all `session-summary-YYYY-MM-*.md` files for target month:
   ```bash
   ls -la "{export-directory}/Session Summaries/" | grep "session-summary-YYYY-MM"
   ```

2. Read each file using `read_file` tool. Extract from each session:
   - Work item IDs (ADO #XXXXX patterns)
   - PR numbers (#XXXXX patterns in GitHub context)
   - Key accomplishments (bullet points under "Accomplishments" or "Key Accomplishments")
   - Files modified
   - Decisions made
   - Meetings attended
   - Big Rocks / major work themes

3. **Output to pass to next phase:**
   - Consolidated list of unique work item IDs
   - Consolidated list of unique PR numbers (grouped by repo)
   - Accomplishments grouped by theme
   - Meeting highlights

**Mark Phase 1 complete, Phase 2 in-progress.**

---

## Phase 2: Extract & Deduplicate

**Actions:**

1. Compile unique work item IDs from all sessions
2. Compile unique PR numbers from all sessions, grouped by repository:
   - MicrosoftDocs/{your-primary-docs-repo}
   - Other docs repos you contribute to
   - Internal tooling repos (if applicable)
   - Other repos encountered
3. Group accomplishments by theme/category:
   - **New Feature Docs**: Service releases, conferences, new capabilities
   - **Content Maintenance**: UUF fixes, freshness reviews, migrations, link fixes
   - **Automation/Tooling**: MCP server work, VS Code extension, team configurations
   - **PR Reviews**: External and team PR reviews, style guide enforcement
   - **Compliance/Admin**: CDA reviews, ADO management, reporting
   - **Analysis**: Content audits, architecture research
4. Identify recurring work themes (Big Rocks candidates):
   - Multi-day work items (appear in multiple sessions)
   - Multiple files changed in single PR
   - Work described as "comprehensive", "major", "new", "complete"
   - Cross-team collaboration efforts
5. Note context that won't be in ADO (decisions, blockers resolved, meeting outcomes)

**Mark Phase 2 complete, Phase 3 in-progress.**

---

## Phase 3: Validate with ADO

**Two query methods are needed** — WIQL for exact counts, MCP for item details:

### 3a. WIQL query for exact closed counts (CRITICAL)

**Why WIQL**: The MCP `my_work_items` tool silently truncates results. WIQL gives exact counts.

Call `mcp_ado_wit_query` with:
- `query`: the WIQL below
- `project`: "Content"

```sql
SELECT [System.Id],[System.Title],[System.State],
       [System.WorkItemType],[Microsoft.VSTS.Common.ClosedDate]
FROM workitems
WHERE [System.WorkItemType] IN ('User Story','User Feedback')
  AND [System.State] = 'Closed'
  AND [System.AssignedTo] = @me
  AND [Microsoft.VSTS.Common.ClosedDate] >= '{YYYY-MM-01}'
  AND [Microsoft.VSTS.Common.ClosedDate] < '{YYYY-MM+1-01}'
```

The MCP tool returns structured JSON directly — no temp files, BOM stripping, or Node.js parsing needed. Filter the results in-agent:
- User Stories: items where `System.WorkItemType` = 'User Story'
- UUF items: items where `System.WorkItemType` = 'User Feedback'

> **Fallback (requires `az login`):** `az boards query --wiql '<WIQL>' --org https://dev.azure.com/msft-skilling -p Content -o json`

**Output**: Exact counts (User Stories, UUF) per item.

### 3b. MCP batch-fetch for item details

**Two-tier fetch** — different fields for User Stories vs UUF:

**User Stories** — fetch full details including Description:
- Fields: `["System.Id", "System.Title", "System.State", "System.WorkItemType", "Microsoft.VSTS.Scheduling.StoryPoints", "Microsoft.VSTS.Common.ClosedDate", "System.IterationPath", "System.Description", "Microsoft.VSTS.Common.AcceptanceCriteria"]`
- **CRITICAL**: The Description contains authoritative data (exact file counts, PR numbers, scope details, blocking reasons) that session summaries only approximate. ALWAYS use Description data over session summary recollection for Big Rock narratives.
- Batch limit ~50 IDs per call (larger payload due to Description field)

**UUF items** — lightweight fetch (descriptions are boilerplate):
- Fields: `["System.Id", "System.Title", "System.State", "System.WorkItemType", "Microsoft.VSTS.Scheduling.StoryPoints", "Microsoft.VSTS.Common.ClosedDate", "System.IterationPath"]`
- Batch limit ~100 IDs per call

**Why this matters**: Work item Descriptions often contain authoritative scope data (exact file counts, PR numbers, per-batch tables) that session summaries only approximate. Always use Description data over session summary recollection for Big Rock narratives. Description is the source of truth for completed work scope.

### 3c. Fetch comments for Big Rock User Stories

For User Stories identified as Big Rock candidates (multi-session, high SP, project completions), also fetch recent comments:

```
mcp_ado_wit_list_work_item_comments(project: "Content", workItemId: {id}, top: 3)
```

**Why**: ADO comments often contain the most detailed progress data — completion summaries with per-batch tables, exact merge dates, final file counts, and scope changes that aren't in the Description.

**When to fetch**: Only for Big Rock candidates (typically 3–5 User Stories). Don't fetch comments for all 19 closed items — that would blow the token budget.

**Data hierarchy** (most authoritative → least):
1. ADO Description + AcceptanceCriteria (structured, maintained)
2. ADO Comments (detailed progress snapshots, completion summaries)
3. Session summaries (narrative context, decisions, blockers)
4. Agent memory (NEVER use — unreliable)

**Story Points rules:**
- Include `StoryPoints` column in User Stories tables
- Show total SP in metrics cards or highlight boxes
- UUF items typically have 1 SP each (verify from WIQL data)

**Mark Phase 3 complete, Phase 4 in-progress.**

---

## Phase 4: Validate with GitHub

**Actions:**

1. **IMPORTANT**: If any GitHub MCP tool fails, activate the appropriate tool group first (`activate_pull_request_management_tools`), then retry
2. For each PR number from Phase 2, grouped by repo:
   - Call `mcp_github_pull_request_read` with `method: "get"`
   - Extract: title, state, merged_at, additions, deletions, changed_files
3. Verify merged dates fall within target month
4. Calculate totals per repo and grand total:
   - Total PRs merged
   - Total additions / deletions
   - Total files changed
   - Unique repos touched

**Mark Phase 4 complete, Phase 5 in-progress.**

---

## Phase 5: Categorize & Synthesize

**Actions:**

### 5a. Identify Big Rocks (3–5 items)

**What qualifies as a Big Rock:**
- New feature documentation (service releases, new capabilities)
- Strategic analysis (content audits, architecture work)
- Major content restructuring or project completion
- Cross-team collaboration efforts
- Customer-impacting fixes with significant scope (e.g., multi-batch UUF)

**How to identify from data:**
- Work items appearing in multiple sessions (multi-day effort)
- High comment counts in ADO (lots of progress updates)
- Multiple files changed in single PR (5+)
- Tags like "new-feature", "architecture"
- Session summaries with detailed technical content

**CRITICAL — Every Big Rock MUST include Story Points:**
- **Markdown**: Add `- **ADO**: N items closed (X SP) — [#ID1](url), [#ID2](url)` as the first line after each Big Rock heading
- **HTML**: Use the third `.badge.date` span for SP (e.g., `<span class="badge date">9 SP</span>`)
- Sum SP from all closed work items belonging to that Big Rock (from WIQL data)
- If the Big Rock has active (unclosed) items contributing significant work, mention them: "[#ID](url) (Active, X SP) tracks ongoing work"
- This standardizes Big Rocks 1–5 so managers see consistent effort metrics across all accomplishments

### 5b. Compute Work Distribution Percentages

Estimate percentage of effort by category based on:
- Number of sessions each category appears in
- Number of PRs per category
- Lines of code per category
- Narrative weight in session summaries

### 5c. Compile PR Reviews

From session summaries, extract:
- PR number, author, title, date reviewed
- Number of suggestions made
- Outcome (merged, pending, etc.)
- Review documents created

### 5d. Compile Meeting Highlights

From session summaries, extract **ALL** notable meetings. **CRITICAL — do not cherry-pick**:
- Include ALL meetings with PMs, PM managers, cross-team stakeholders, and leadership
- Include ALL 1:1 meetings and strategy discussions
- Include team meetings, sync meetings, and architecture discussions
- **Especially**: meetings about strategy, planning, or PM engagement (e.g., SQL Security PM Manager sync about docs priorities)
- Format: title, date, key attendees, key discussion point

### 5e. Compile Additional Work

Items that aren't Big Rocks but are noteworthy. **CRITICAL — every row must have an ADO hyperlink**:
- Map each Additional Work item to its ADO work item ID
- Use `<a href="https://msft-skilling.visualstudio.com/Content/_workitems/edit/{ID}">` in HTML
- Use `[ADO #{ID}](URL)` in markdown
- If an item spans multiple ADO items, link to the primary one

### 5f. Looking Ahead — From ADO Iteration (CRITICAL)

**NEVER guess Looking Ahead from session context.** Always query ADO for actual next-month items:

Call `mcp_ado_wit_query` with:
- `query`: the WIQL below
- `project`: "Content"

```sql
SELECT [System.Id],[System.Title],[System.State],[Microsoft.VSTS.Scheduling.StoryPoints],
       [System.WorkItemType]
FROM workitems
WHERE [System.WorkItemType] IN ('User Story','User Feedback')
  AND [System.State] NOT IN ('Closed','Removed')
  AND [System.AssignedTo] = @me
  AND [System.IterationPath] = '{next_month_iteration}'
```

> **Fallback (requires `az login`):** `az boards query --wiql '<WIQL>' --org https://dev.azure.com/msft-skilling -p Content -o json`

**Then fetch full details** — call `mcp_ado_wit_get_work_items_batch_by_ids` with fields `System.Description` and `Microsoft.VSTS.Common.AcceptanceCriteria` for all items. Read each description to understand the actual work.

**Format as 3–4 themed priority bullets, NOT a raw ADO table:**

1. Group items by strategic theme (e.g., "SQL Security depth", "CDA & Automation", "Recurring")
1. Write 2–3 sentences per theme describing the strategic goal and key deliverables
1. Include inline ADO hyperlinks for every item: `[#ID](url)` in markdown, `<a href>` in HTML
1. Show SP per item inline: `([#558231](url), 5 SP)` and total SP per theme in the heading
1. Call out hard deadlines or dependencies (e.g., "threat model review on April 13")
1. Mention PM contacts or cross-team collaborators when they drive the work

**Why themed bullets over raw tables:**
- Managers care about **strategy** ("what are you focused on and why?"), not task lists
- Grouping reveals effort allocation across themes (22 SP on security vs 5 SP on admin)
- Narrative context surfaces dependencies and deadlines that table rows hide
- ADO hyperlinks + SP preserve full traceability

**In HTML reports**: Use the Big Rock card style (`<div class="big-rock">`) for each theme with `.badge` spans for item count and SP total.

### 5g. Connect Goals Progress (OPTIONAL — requires GOALS.md)

**Skip this entire phase** if `~/.copilot/skills/connect-goals/GOALS.md` does not exist. No errors, no empty sections.

**If it exists**, read the file (it's pre-computed — no API calls needed here):

1. Parse each goal's `status`, `target_type`, `target`, `current`, `short`, and `evidence` fields
1. Compute progress percentage for `quantitative` goals: `current / target * 100`
1. Map `status` to visual indicators:
   - `done` → ✅ green pill + **100%** (always show percentage for done goals)
   - `on-track` → 🔄 blue pill (U+1F504, Unicode 6.0 — NOT (U+1F7E2) U+1F7E2 which breaks on Windows)
   - `at-risk` → ⚠️ yellow pill (U+26A0, Unicode 4.0)
   - `exceeded` → 🌟 purple pill + **percentage** (e.g., 139%, 300%)
   - `not-started` → ⬜ gray pill
   - **All quantitative goals show percentages**: `current/target * 100`
   - **All done milestones show 100%**: `✅ Link Farm 100%`
   - For recurring goals, show fraction: `🔄 AI Assignments 6/6`
   - Match emojis between pills (Tier 1) and scorecard badges (Tier 2)

**Generate two HTML components:**

**Tier 1 — Progress strip** (between Executive Summary and Key Metrics):
- Thin bar: `<div class="goals-strip">` with `<span class="goal-pill {status}">` elements
- Each pill: status icon + `short` label (+ percentage for exceeded quantitative goals)

**Tier 2 — Detail section** (between Impact Summary and Key Meetings):
- `<details open class="section" id="connect-goals">` — collapsible
- `.scorecard-grid` with one `.scorecard-item` card per goal
- `.progress-bar-bg` bars only for `quantitative` goals
- `.highlight-box` with 2-3 sentence narrative on what moved this month
- Add "Semester Goals" link to the TOC sidebar

**In markdown**: Add `## Semester Goals Progress` table between Impact Summary and Key Meetings.

**IMPORTANT**: This phase does ZERO API calls. Data freshness depends on running `/connect-goals update` beforehand. See Step 5 below.

**Mark Phase 5 complete, Phase 6 in-progress.**

---

## Phase 6: Generate Reports

### Step 0: Update Connect Goals (before generating report)

**Before starting Phase 6**, check if `~/.copilot/skills/connect-goals/GOALS.md` exists.

**If it exists**, remind the user:

> 📊 **Connect Goals**: To include fresh semester progress in this report, run:
> `/connect-goals update`
> Then continue with the report generation below.
>
> If you've already run it this month, or want to use the existing data, proceed directly.

**If it doesn't exist**, skip silently — don't mention goals.

### Step 1: Read previous month's HTML report

Read the previous month's HTML file to maintain visual consistency:
```bash
ls "{export-directory}/Monthly Reports/" | grep "monthly-report-.*html"
```
Use it as a structural and styling reference.

### Step 2: Generate markdown report

Follow the [markdown template](./templates/monthly-report-template.md) for structure.

### Step 3: Generate HTML report

Follow the [HTML template](./templates/monthly-report-template.html) for the complete CSS and component structure.

**CRITICAL HTML requirements** (these are the items the agent most often misses):

1. **Sidebar TOC** — Fixed `<nav class="toc-sidebar">` with anchor links to every section. Frosted glass (`backdrop-filter: blur(12px)`), scroll-spy JS highlights active link, hides below 1,100px, hidden in print.
1. **Sidebar controls** — `<div class="sidebar-controls">` anchored at `left: 248px` (right of TOC). Contains three circular buttons stacked vertically: 🌙 dark mode toggle, ↕ expand/collapse all, ↑ back-to-top (fades in after 600px scroll). Same responsive/print behavior as sidebar.
1. **Collapsible sections** — Every section uses `<details open class="section" id="{slug}">` with `<summary>` wrapping the H2. Native HTML5 — starts expanded, click to collapse. Custom `▼` chevron via CSS `::before`. Falls back gracefully in OneDrive (renders fully expanded).
1. **Animated metric counters** — Each `.metric-value` has `data-target="{N}"` and initial text `{N}` (the final value). JS IntersectionObserver overwrites `textContent` with an ease-out-cubic count-up animation (1,200ms) when Key Metrics section scrolls into view. Without JS (OneDrive/Teams), the initial text is already the correct final number. **Critical**: never use `0` as initial text — that breaks rendering in non-JS contexts.
1. **Reveal animations (JS-gated)** — CSS `.animate-ready .section { opacity: 0; transform: translateY(30px) }`, JS adds `.animate-ready` to `<html>` before observing, then IntersectionObserver adds `.revealed` on scroll. Without JS (OneDrive/Teams), `.animate-ready` is never added so sections render fully visible. One-time animation per section.
1. **Dark mode** — Toggle button swaps `data-theme="dark"` on `<html>`. Full CSS variable swap for all components (container, cards, tables, badges, sidebar, links). Persists via `localStorage('report-theme')`. Links in `.big-rock`, `.impact-card`, `.highlight-box` use `#6bb8ff` for readability on dark backgrounds.
1. **Colored metric card variants** — Use `.metric-card.accent`, `.metric-card.success`, `.metric-card.warning` for visual variety (not all blue)
1. **`.meta-item` styled spans** in header — Pill badges with `rgba(255,255,255,0.15)` background
1. **`.badges` container div** in Big Rocks — Flex container with proper gap for ADO/PR/SP badges
1. **`.highlight-box`** callouts — Blue highlight boxes inside Big Rocks for key stats
1. **`.bar-pct`** column — Separate percentage text to the right of bar chart rows
1. **Meeting cards** — Dedicated `.meeting-card` components with title, meta, and description
1. **"Additional Work" section** — Table with ADO hyperlinks for EVERY row (not bare text)
1. **"Key Meetings" section** — Include ALL PM/manager/stakeholder meetings (don't cherry-pick)
1. **"Looking Ahead" as themed cards** — 3–4 `.big-rock` cards grouped by strategic theme with SP totals per theme. NOT a raw ADO table. Each theme has inline ADO hyperlinks, SP per item, narrative context, and dependency/deadline callouts.
1. **Interactive metric cards** — Work Items and UUF cards wrapped in `<a>` tags with WIQL query URLs
1. **Deliverables list** — Use `.deliverables` class with `✅` pseudo-element positioning
1. **Exact counts only** — NEVER use "18+" or "115+" when WIQL gives exact numbers. Use 19, 37, 115.
1. **Story Points** — Include SP column in User Stories tables, total SP in metrics or highlight boxes. SP badge required on every Big Rock.
1. **Story Points metric card** — Add a metric card for total Story Points closed

### Step 4: Write both files

- **Markdown**: `{export-directory}/Monthly Reports/monthly-report-{month}-{year}.md`
- **HTML**: `{export-directory}/Monthly Reports/monthly-report-{month}-{year}.html`

Use `create_file` for new reports, `replace_string_in_file` for updates.

**Mark all todos complete.**

---

# Reference

## WIQL Query URLs for Interactive Metric Cards

**URL Pattern:**
```
https://msft-skilling.visualstudio.com/Content/_queries/query/?wiql=<URL-ENCODED-WIQL>
```

**Work Items Closed (excluding UUF):**
```
SELECT [System.Id], [System.Title] FROM WorkItems
WHERE [System.State] = 'Closed'
AND [System.AssignedTo] = @me
AND [Microsoft.VSTS.Common.ClosedDate] >= '{YYYY-MM-01}'
AND [Microsoft.VSTS.Common.ClosedDate] < '{YYYY-MM+1-01}'
AND [System.WorkItemType] <> 'User Feedback'
```

**UUF Items Closed:**
```
SELECT [System.Id], [System.Title] FROM WorkItems
WHERE [System.WorkItemType] = 'User Feedback'
AND [System.State] = 'Closed'
AND [System.AssignedTo] = @me
AND [Microsoft.VSTS.Common.ClosedDate] >= '{YYYY-MM-01}'
AND [Microsoft.VSTS.Common.ClosedDate] < '{YYYY-MM+1-01}'
```

**Date substitution:**
- Replace `{YYYY-MM-01}` with first day of report month
- Replace `{YYYY-MM+1-01}` with first day of NEXT month (exclusive upper bound)

**Required CSS for clickable cards:**
```css
.metrics-grid > a { display: contents; }
.metrics-grid a { text-decoration: none; color: inherit; }
```

---

## Data Verification Rules

**ALWAYS fetch actual data — NEVER make assumptions.**

- GitHub PRs → `mcp_github_pull_request_read` with `method: "get"` — use actual `title` field
- ADO Work Items → `mcp_ado_wit_get_work_items_batch_by_ids` or `mcp_ado_wit_get_work_item` — use actual `System.Title`
- ❌ DO NOT assume titles from conversation context or memory
- ✅ Session summaries are permanent records requiring accuracy

---

## Hyperlink Rules

**GitHub PRs** — ALWAYS full markdown links:
- ✅ `[PR #12345](https://github.com/MicrosoftDocs/{repo}/pull/12345)`
- ❌ `PR #12345` (bare number)

**ADO Work Items** — ALWAYS full markdown links:
- ✅ `[#540865](https://msft-skilling.visualstudio.com/Content/_workitems/edit/540865)`
- ❌ `#540865` (bare number)

In HTML reports, use `<a href="..." target="_blank">` for all references.

---

## MCP Tool Activation Rule

**When any MCP tool call fails (500 error, timeout, etc.):**
1. **DO NOT** try workarounds or alternative API approaches
2. **DO** activate the appropriate tool group first, then retry:
   - `activate_pull_request_management_tools` — PR read/write
   - `activate_azure_devops_work_item_management_tools` — ADO operations

---

## Tool Categorization

| Category | Prefix | Tools Used in This Skill |
|----------|--------|--------------------------|
| **MCP tools** | `mcp_` | `mcp_ado_wit_*`, `mcp_github_*`, `mcp_content-devel_*` |
| **Built-in tools** | No prefix | `manage_todo_list`, `create_file`, `replace_string_in_file`, `read_file`, `run_in_terminal` |

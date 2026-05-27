---
name: 1-1-reports
version: 1.3.0
category: Reports
description: Generate a weekly 1:1 report for manager meetings. Use when the user says "prepare a report for my 1:1", "1:1 report", "weekly report", or "what did I do this week". Includes sprint commitment tracking per ADEC Rubidium ADO guidance.
argument-hint: '"this week" or date range (Wednesday to Wednesday)'
relevant-lesson-tags: [1-1, weekly-report, ado, sprint]
---

Generate a weekly work summary for the user's manager.

## Cadence & Date Range

On first use, ask the user:
1. **"What day is your 1:1 with your manager?"** (e.g., Thursday)
2. **"Is it weekly?"** (weekly is the default; if biweekly, adjust the report window accordingly)

The report period ends the day before the 1:1. For example, if the 1:1 is Thursday, the report covers Thursday-to-Wednesday. Store the user's answer in the agent file so it only needs to be asked once.

- **Default**: Weekly, ending the day before the 1:1
- Determine the most recent report window based on the 1:1 day
- Working days only (skip weekends)

## Storage Location
- **Directory**: `{SESSION_DIR}\1-1s\YYYY-MM\`
  - Organized by month with `md\` and `html\` subfolders
- **Naming Convention**: `1-1-report-YYYY-MM-DD-to-YYYY-MM-DD.md` (and `.html`)
  - Dates are the Wednesday-to-Wednesday boundaries
- **Dual Format**: Create both markdown and HTML versions

## Data Sources (Priority Order)
1. **Session summaries** in `{SESSION_DIR}\session-summaries\YYYY-MM\md\` for all working days in the range
2. **ADO work items** — validate with `mcp_ado_wit_my_work_items` if session summaries are incomplete
3. **GitHub PRs** — always cross-verify against the upstream repo (not just the user's fork). Use `mcp_github_list_pull_requests` or `mcp_github_search_pull_requests` with the upstream owner/repo and filter by the user's GitHub username to catch all PRs created, merged, or reviewed during the report period.
4. **Sprint Commitment snapshot** — captured at start of each month (see Sprint Commitment Tracking below)

## Sprint Commitment Tracking

Every 1:1 report includes a Sprint Commitments section that shows in-flight status of items committed at the start of the current sprint (month).

### Key Definitions
- **Sprint = calendar month** (e.g., April 2026 sprint = IterationPath `Content\FY26\Q4\04 Apr`)
- **Committed User Story** = User Story with `System.State = "Committed"` AND `IterationPath` = current month **at the start of the sprint**
- **On track** = Committed item in Active, Review, or Closed state; or Committed and expected to complete before end of sprint
- **At risk** = Committed item still in Committed/Blocked state with limited time remaining, or dependency/blocker unresolved

### Snapshot Source of Truth
The "Committed at start of sprint" baseline is **captured once at the start of each month** and stored in:

`{SESSION_DIR}\sprint-commitments\YYYY-MM-sprint-commitments.md`

This file lists every User Story that was in Committed state + current month's IterationPath on day 1 of the sprint. It is **frozen** after creation — mid-sprint additions do NOT modify it (they're tracked separately as "unplanned work").

If the snapshot file is missing when generating a 1:1 report, create it first by querying ADO for all User Stories assigned to `{USER_EMAIL}` with `State=Committed` and `IterationPath` matching the current month, and record them as the baseline.

### Baseline Capture Procedure (run on day 1 of each sprint/month)

When a new month starts and the snapshot file does not exist:

1. Determine current month's IterationPath (e.g., `Content\FY26\Q4\04 Apr`)
2. Query ADO:
   ```
   mcp_ado_wit_my_work_items(type="assignedtome", top=200)
   ```
3. Batch-fetch full details with fields: `System.Id, System.Title, System.State, System.WorkItemType, System.IterationPath, Microsoft.VSTS.Scheduling.StoryPoints, System.Tags, System.AreaPath`
4. Filter to: `WorkItemType = "User Story"` AND `State = "Committed"` AND `IterationPath` contains current month path
5. Write `{SESSION_DIR}\sprint-commitments\YYYY-MM-sprint-commitments.md` with this structure:

```markdown
# Sprint Commitment Baseline — {Month Year}

> **Captured**: {ISO date} (day 1 of sprint)
> **IterationPath**: {full path}
> **Source**: mcp_ado_wit_my_work_items (type=assignedtome)
> **Filter**: WorkItemType=User Story, State=Committed

**Baseline**: {N} User Stories / {X} Story Points

| # | ID | Title | Story Points | AreaPath | Tags |
|---|----|----|-----|----------|------|
| 1 | [#XXXXXX](url) | Title | 3 | ...\{Area1}\Deployment-configuration | new-feature |

## Big Rocks (flagged for this sprint)
- {Item ID} — {brief reason it's a Big Rock}
```

6. Don't modify this file after creation — it serves as the frozen baseline for sprint reflection.
7. If items are added/changed/removed from the sprint mid-month, track them in the 1:1 report's Unplanned Work and Deferred sections — not in the baseline file.

### Workflow for 1:1 Reports
1. Determine current sprint (month containing the report's end date)
2. Read `{SESSION_DIR}\sprint-commitments\YYYY-MM-sprint-commitments.md`
3. For each item in the snapshot, fetch current state via `mcp_ado_wit_get_work_items_batch_by_ids` (fields: State, StoryPoints, IterationPath, Tags)
4. Classify each as: ✅ Completed | 🟢 On track (Active/Review) | 🟡 At risk (still Committed late in sprint or Blocked) | 🔴 Removed/Deferred
5. Calculate: Committed SP / Completed SP / % complete → compare to 60% goal
6. Track items that moved OUT of the sprint (IterationPath changed) as "Deferred"
7. Track items added mid-sprint (new Committed items in this iteration, not in snapshot) as "Unplanned work" — surface but don't count against 60%

### Sprint Commitments Section Template

> **Template file:** See [templates/sprint-commitments-template.md](templates/sprint-commitments-template.md)

## Report Structure

```markdown
# 1:1 Report — {Start Date}–{End Date}

**Author**: {USER_NAME} ({USER_EMAIL})
**Team**: {TEAM} | {ROLE}
**Manager**: {MANAGER}
**Period**: Wednesday, {Start} – Wednesday, {End} ({N} working days)

## Executive Summary
[2-3 sentence summary of week's focus and major accomplishments]

## Impact Summary
[4 bullet points: key deliverables, infrastructure, customer-facing, quality]

## Sprint Commitments ({Month Year})
[See Sprint Commitment Tracking section above for the full template]

## Key Metrics
| Metric | Value |
|--------|-------|
| Work Items Touched | N |
| PRs Created | N |
| PRs Merged | N |
| PR Reviews | N |
| Meetings | N |

## Work Summary
[Single unified table — one row per work stream]

| # | Work Name | ADO Items | PRs | Summary |
|---|-----------|-----------|-----|---------|
| 1 | **Work Stream** | #ID1, #ID2 | #PR1, #PR2 ✅ | 1-2 sentence executive summary. |

## PRs Merged This Week
[Table of merged PRs with dates]

## PRs Open / In Review
[Table of open PRs with base branch and status]
```

## Content Guidelines
- **Group by work stream**, not by day — combine related ADO items and PRs
- **Executive summaries** should be 1-2 sentences, manager-readable (skip technical minutia)
- **Mark merged PRs** with ✅ in the table
- **Include meetings** as a separate row at the bottom
- **All ADO and PR references should be hyperlinked** (use ADO org URL and GitHub repo from agent file)

## HTML Styling
- Use same purple gradient body background, white container, metric cards, and table styling as monthly reports
- Include status badges: `badge-merged` (green), `badge-open` (blue), `badge-review` (yellow), `badge-draft` (gray)
- Merged PRs section uses card grid layout
- All ADO/PR links must be clickable

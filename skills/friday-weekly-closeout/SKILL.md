# Friday Weekly Closeout & Planning Skill

**Purpose**: Automate end-of-week closure and next-week planning for Friday project tracking. Creates a normalized current-week report, time-blocked Monday plan, and a fully updated next-week report with live ADO sync.

**When to use**: Every Friday or at end of sprint to close the week and prepare Monday execution.

**Inputs**:
- Current weekly plan markdown file (e.g., `05-06-2026-weekly.md`)
- List of ADO work items to sync (auto-extracted from current plan)
- Optional: explicit Monday focus priorities (overrides auto-detection)

**Outputs**:
- Normalized current weekly plan (completed items moved to dedicated section, renumbered, synced)
- Time-blocked Monday schedule (90-min focus blocks aligned to high priorities)
- New weekly plan markdown (next week, with carried-forward priorities and refreshed ADO status)
- Clarifying-question responses for end-of-week wrap-up and next-week priorities

---

## Workflow

### Phase 1: Normalize Current Week

1. **Read current weekly plan** from `friday/data/raw/plans/<DATE>-weekly.md`
2. **Identify completed items** (marked as "Completed" or "Done" in status column)
3. **Move completed items** to a dedicated "Completed This Week" section
4. **Renumber** Active/New/Backlog sections to maintain sequence
5. **Sync all ADO item IDs** to live ADO state:
   - Fetch current State, Priority, Target Date, Title for each work item
   - Update target dates if changed
   - Add overdue flags (⚠️ OVERDUE) for items past target date
   - Add "Needed this week" flag for items due within 7 days

**Example**:
```
## ADO User Stories — Active (In Progress)
| # | Pri | ID | Title | Target Date | Flag |
|---|-----|------|-------|-------------|------|
| 1 | P1 | 572972 | Application Gateway | 2026-05-22 | Needed this week |
| 2 | P2 | 573010 | Rubidium Semester | 2026-06-30 | |
```

### Phase 2: Generate Monday Time-Blocked Plan

1. **Identify P0/P1 items** from Active section and items due within 3 days
2. **Sort by priority and target date** (ascending)
3. **Create 4 focus blocks** (~90 min each) mapped to top 4 items:
   - 8:30–10:00: Block 1 (highest priority)
   - 10:00–11:30: Block 2
   - 1:00–2:30 PM: Block 3
   - 2:30–4:00 PM: Block 4
4. **Add buffer blocks** (15 min) between focus blocks for handoffs/unblocking
5. **Add admin block** at end of day (30 min) for status updates and Tuesday planning
6. **Define success criteria** for each block (what "done" looks like)

**Template**:
```
## Monday time-blocked plan (May 12, 2026)

| Time | Focus | Deliverable | ADO / Output |
|------|-------|-------------|--------------|
| 8:30-10:00 | {TOP_PRIORITY_TITLE} | {CONCRETE_OUTCOME} | ADO {ID} moved to Active/specific checkpoint |
| 10:00-10:15 | Buffer | Resolve blockers / handoffs | Notes and assignments captured |
| 10:15-11:45 | {2ND_PRIORITY_TITLE} | {CONCRETE_OUTCOME} | ADO {ID} progress update |
| ... |
| 4:00-4:30 | Admin closeout | Update weekly report and ADO statuses; set Tuesday first block | End-of-day status and next-step plan |

### Monday success criteria
- {ITEM 1} completed or moved to next milestone.
- {ITEM 2} has documented progress.
- All ADO statuses synced before end of day.
```

### Phase 3: Create Next Week Plan

1. **Scaffold new file**: `friday/data/raw/plans/<NEXT_WEEK_DATE>-weekly.md`
2. **Copy structure** from current week (Priorities table, ADO sections, Notes, Housekeeping, End-of-week template)
3. **Carry forward all non-completed tasks** to new "Priorities for Week of" table
4. **Update priorities table**:
   - Change "Status" to "Not Started" for carryover items
   - Add week number and date range
   - Include carryover notes (e.g., "Carryover from 5/6 week")
5. **Fetch live ADO data** for all tracked work items:
   - For each ID in current plan, query ADO for: State, Priority, TargetDate, Title
   - Separate into Active, New, Backlog, and Completed sections
   - Maintain row numbering across weeks for continuity
6. **Auto-flag items**:
   - Items due within 7 days: "Needed this week"
   - Items past target date: "⚠️ OVERDUE"
7. **Create "Overdue and needed attention" section** with high-priority overdue items
8. **Populate status snapshot** with key tracked items

### Phase 4: Clarifying Questions

Before finishing, ask user to confirm end-of-week and next-week planning:

#### End-of-Week Closure
```
1. End-of-Week Summary — please provide:
   - What went well this week?
   - What could have been better?
   - Key wins?
   - What did you learn?
   - What did you impact?

2. Are there any additional items to mark as Completed or Closed in this week's report?

3. Any blockers or dependencies to note before closing the week?
```

#### Next-Week Priorities
```
4. Reviewing the next-week priorities list, what are your top 3 focus areas for Monday?

5. Any new items or priorities to add to next week beyond the carried-over list?

6. Are there any overdue P2/P3 items you want to address this week, or defer to a later sprint?

7. Do you want to batch-execute overdue maintenance items (P2/P3 "Maintenance" category), or handle them individually?

8. Any ADO items that should be closed or archived instead of carried forward?
```

---

## Implementation Steps

### Step 1: Prepare Current Week Report
```powershell
# Read current week's plan
$currentPlanPath = "friday/data/raw/plans/05-06-2026-weekly.md"
$content = Get-Content $currentPlanPath -Raw

# Extract ADO IDs from the markdown tables
$ids = [regex]::Matches($content, '\| (\d+) \|') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique

# Query each ADO item for current state
foreach ($id in $ids) {
    $adoItem = az boards work-item show --id $id --organization https://dev.azure.com/msft-skilling -o json | ConvertFrom-Json
    # Update markdown with fresh Title, State, TargetDate
}

# Move Completed items to dedicated section
# Renumber remaining items
# Save updated file
```

### Step 2: Generate Monday Plan
```powershell
# Extract P1 and near-term-due items from normalized current plan
# Sort by Priority ASC, TargetDate ASC
# Create 4 focus blocks + buffers + admin closeout
# Calculate success criteria from ADO titles and descriptions

$mondayPlan = @"
## Monday time-blocked plan (May 11, 2026)

| Time | Focus | Deliverable | ADO / Output |
|------|-------|-------------|--------------|
{TIME_BLOCKS_HERE}

### Monday success criteria
{CRITERIA_HERE}
"@

# Insert into current week plan file
```

### Step 3: Create Next Week Plan
```powershell
# Calculate next Monday date
$nextMonday = (Get-Date).AddDays(((1 - (Get-Date).DayOfWeek.value__) % 7 + 7) % 7)
$nextWeekFile = "friday/data/raw/plans/$($nextMonday.ToString('MM-dd-yyyy'))-weekly.md"

# Copy template structure
$template = Get-Content "05-06-2026-weekly.md" -Raw

# Replace dates/numbers
$nextPlan = $template -replace "05-06-2026", $nextMonday.ToString("MM-dd-yyyy")

# Query all ADO IDs again
foreach ($id in $ids) {
    $adoItem = az boards work-item show --id $id ...
    # Update markdown tables with refreshed data
}

# Create new file
$nextPlan | Set-Content $nextWeekFile -Encoding utf8
```

### Step 4: Ask Clarifying Questions
```powershell
# Prompt user with structured questions
$endOfWeekSummary = Read-Host -Prompt "What went well this week?"
$nextWeekTopPriorities = Read-Host -Prompt "What are your top 3 focus areas for Monday?"
$deferredOverdueItems = Read-Host -Prompt "Any overdue items to defer?"

# Save responses to end-of-week summary section
# Update next week plan based on user input
```

---

## Usage Example

**Invoke from CLI or agent mode**:
```
friday-weekly-closeout --current-plan 05-06-2026-weekly.md --sync-ado --create-monday-plan --create-next-week
```

**Interactive mode** (recommended):
```
> friday-weekly-closeout
📋 Normalizing current week (05-06-2026)...
✅ Moved 2 completed items to dedicated section
✅ Synced 23 ADO items (5 overdue flagged)

📅 Generating Monday time-blocked plan...
✅ Created 4 focus blocks + buffers + admin
✅ Success criteria auto-generated from ADO titles

📝 Creating next week plan (05-11-2026)...
✅ Carried forward 18 non-completed priorities
✅ Fetched live ADO state for all items

❓ End-of-week summary:
   What went well this week? > [USER INPUT]
   What could have been better? > [USER INPUT]
   ...

❓ Next-week planning:
   Top 3 focus areas for Monday? > [USER INPUT]
   Any new items to add? > [USER INPUT]
   ...

✅ Weekly closeout complete!
   - Updated: 05-06-2026-weekly.md
   - Created: 05-11-2026-weekly.md
   - Monday plan appended to current week report
```

---

## Files Affected

| File | Action |
|------|--------|
| `friday/data/raw/plans/{CURRENT_DATE}-weekly.md` | Updated: completed items moved, ADO synced, Monday plan added, end-of-week summary filled in |
| `friday/data/raw/plans/{NEXT_DATE}-weekly.md` | Created: carries forward all non-completed priorities, refreshed ADO status, overdue section populated |

---

## Configuration

**ADO Organization**: `https://dev.azure.com/msft-skilling`
**ADO Project**: `Content`
**Sync Frequency**: Every Friday or sprint close
**Monday Plan Time Zone**: Pacific (US)
**Default Focus Blocks**: 90 min each
**Buffer Duration**: 15 min

---

## Limitations & Known Issues

1. **ADO query timeout**: If syncing >50 items, batch queries in groups of 10 to avoid CLI timeouts.
2. **Timezone handling**: Monday plan assumes Pacific time; adjust if needed.
3. **Markdown parsing**: Complex ADO titles with special characters (pipes, brackets) may need escaping in markdown tables.
4. **Overdue calculation**: Uses system date; ensure system clock is accurate.

---

## See Also

- `ado-work-items.instructions.md` — ADO item creation and update patterns
- `friday.config.ts` — Friday configuration and store paths
- `friday/data/raw/plans/` — Weekly plan storage directory


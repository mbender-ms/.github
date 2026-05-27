# Connect Goals Template

> **How to use**: Copy this file to `~/.copilot/skills/connect-goals/GOALS.md` and fill in your SMART goals.
> The monthly-report skill will automatically detect this file and add a "Semester Goals" progress
> section to your HTML and markdown reports.
>
> **No GOALS.md?** No problem — the skill generates a standard report without the goals section.
>
> **Where to get your goals**: Export your goals from your Connect document (the "Plan for the future"
> section). Structure each goal with the fields below so the skill can compute progress automatically.

---

## Goals

### Goal 1: {Your First Connect Goal Category}

- id: "1.1"
  title: "{Full goal title}"
  short: "{3-5 word label for progress strip pill}"
  description: "{One sentence describing the goal}"
  target_type: milestone | quantitative | recurring
  target: "{number for quantitative, text for milestone/recurring}"
  baseline: 0
  current: 0
  unit: "{items closed, files migrated, etc.}"
  status: not-started | on-track | at-risk | done | exceeded
  completed: "{YYYY-MM-DD if done}"
  evidence: "{Brief evidence — ADO IDs, PR numbers, key facts}"
  wiql_hint: "{Optional WIQL WHERE clause for automated counting}"

### Goal 2: {Second Category}

- id: "2.1"
  title: "{...}"
  short: "{...}"
  ...

### Goal 3: {Third Category}

- id: "3.1"
  title: "{...}"
  short: "{...}"
  ...

---

## Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Matches your Connect goal numbering (1.1, 1.2, etc.) |
| `title` | Yes | Full goal title from Connect |
| `short` | Yes | 3-5 word label shown in the progress strip pills |
| `description` | Yes | One-sentence goal description |
| `target_type` | Yes | `milestone` (done/not done), `quantitative` (N of M), `recurring` (monthly) |
| `target` | Yes | Number for quantitative, descriptive text for others |
| `baseline` | Quantitative | Starting value (usually 0) |
| `current` | Quantitative | Current value — update monthly or let WIQL compute |
| `unit` | Quantitative | Label for the number (e.g., "items closed") |
| `status` | Yes | One of: `not-started`, `on-track`, `at-risk`, `done`, `exceeded` |
| `completed` | If done | Date completed (YYYY-MM-DD) |
| `evidence` | Yes | Brief proof — ADO #IDs, PR numbers, key metrics |
| `wiql_query` | Optional | Full WIQL SELECT statement for automated counting via `/connect-goals update` |
| `count_method` | If wiql_query | `count_results` (count rows) or `check_state` (check if item is Closed) |

## Status Legend

| Status | Strip Pill | Detail Badge | When to Use |
|--------|-----------|--------------|-------------|
| `not-started` | ⬜ gray | Not Started | Work hasn't begun |
| `on-track` | 🔄 blue | On Track | Progressing at expected pace |
| `at-risk` | ⚠️ yellow | Needs Attention | Behind pace, might miss target |
| `done` | ✅ green | 100% | Finished on or before deadline |
| `exceeded` | 🌟 purple | {N}% | Significantly exceeded the target |

**Emoji note**: Use 🔄 (U+1F504) for on-track — NOT 🟢 (U+1F7E2) which renders as a broken rectangle on Windows.

## Tips

1. **Update monthly**: After each monthly report, update `current` values and `status` fields
2. **Use wiql_hint**: For quantitative goals, add a WIQL hint so the skill can auto-compute progress
3. **Keep evidence fresh**: Add new PR numbers and ADO IDs as work progresses
4. **Monthly Snapshots table**: Optional but useful — tracks month-by-month progress for charts

---
name: backlog-analysis
version: 1.0.1
category: Analysis
description: Score and prioritize backlog items using a weighted formula that balances customer impact, implementation effort, and item age. Use when the user says "review my backlog", "prioritize my backlog", "backlog analysis", "score my backlog items", or "what should I work on next". Produces a tiered HTML report.
argument-hint: '"all" or specific service area (e.g., "area-1", "area-2")'
relevant-lesson-tags: [backlog, prioritization, ado]
---

## Overview

Scores and prioritizes backlog items using a weighted formula that balances customer impact, implementation effort, and item age. Produces a tiered HTML report for manager visibility and personal planning.

## Output Location

All backlog analysis files go to:
```
{SESSION_DIR}/analysis/backlog/{YYYY-MM-DD}/
```

Example: `D:\OneDrive - Microsoft\Content Dev\CDA things\Reports\analysis\backlog\2026-04-27\`

Files produced:
- `backlog-review-{YYYY-MM-DD}.html` — styled HTML report with tier tables
- `backlog-items.json` — raw item data fetched from ADO
- `backlog-scored.json` — items with computed scores

Previous reports stay in place for historical comparison.

---

## Scoring Formula

```
Score = (Customer Impact × 2) - Implementation Effort + Age Bonus
```

### Customer Impact (1–5)
| Score | Meaning |
|-------|---------|
| 5 | Critical — top-landing page, partner ecosystem, PM deadline |
| 4 | High — core scenario, heavily trafficked, common support topic |
| 3 | Medium — fills content gap, moderate traffic |
| 2 | Low — niche scenario, exists elsewhere |
| 1 | Minimal — vendor request, edge case |

### Implementation Effort (1–5)
| Score | Meaning |
|-------|---------|
| 1 | Quick fix — minor edit, link update, terminology change |
| 2 | Small — one article, spec provided |
| 3 | Medium — new article or significant rewrite |
| 4 | Large — deep research, multi-article, PG coordination |
| 5 | Very large — new tutorial series, architecture changes |

### Age Bonus
| Age | Bonus |
|-----|-------|
| < 365 days | +0 |
| 365–1000 days | +1 |
| > 1000 days | +1 (same cap) |

### Tier Definitions
| Tier | Score | Action | Color |
|------|-------|--------|-------|
| **A** | 7+ | Do Next | Green (#107c10) |
| **B** | 5–6 | Do Soon | Blue (#0078d4) |
| **C** | 3–4 | Evaluate | Yellow (#ffb900) |
| **D** | 1–2 | Low Priority | Orange (#d83b01) |
| **E** | 0 or below | Defer/Remove | Red (#d13438) |

**Blocked items** are highlighted in yellow regardless of tier — cannot proceed until unblocked.

---

## Workflow

### Phase 1: Fetch items

1. Get all User Stories parented under Content Maintenance Features:
   <!-- Configure these Feature Parent IDs from your agent file -->
   - **#{FEATURE_PARENT_ID_1}** — {Area1} | Content maintenance
   - **#{FEATURE_PARENT_ID_2}** — {Area2} | Content Maintenance
   - **#{FEATURE_PARENT_ID_3}** — {Area3} | Content Maintenance
   Add or remove entries to match your product areas.

2. Filter to items with `Iteration = Content\future` (backlog items)

3. Exclude:
   - Closed or Removed items
   - Items assigned to other team members (verify `AssignedTo = {USER_EMAIL}`)
   - User Feedback (UUF) items (`System.WorkItemType = 'User Feedback'`) — these have their own analysis workflow via the uuf-analysis skill

### Phase 2: Score items

For each item:
1. Read the title and description to assess Customer Impact and Implementation Effort
2. Calculate age from `System.CreatedDate`
3. Compute score using formula
4. Assign tier
5. Note if Blocked

### Phase 3: Generate report

1. Create output directory: `{SESSION_DIR}/analysis/backlog/{YYYY-MM-DD}/`
2. Save `backlog-items.json` (raw ADO data)
3. Save `backlog-scored.json` (items + scores)
4. Generate `backlog-review-{YYYY-MM-DD}.html` with:
   - Summary metrics cards (count per tier + blocked + total)
   - Scoring formula explanation box
   - One table per tier (A through E)
   - Columns: ID (linked), Title, Impact, Effort, Score, State, Area, Age, Rationale
   - Blocked rows highlighted yellow
   - Non-actionable rows at 60% opacity

### Phase 4: Compare with previous

If a previous report exists, note:
- New items added since last review
- Items closed/removed since last review
- Score changes (if re-scored)
- Tier movements

---

## Adding New Items

When adding items that aren't in the backlog yet (e.g., from a PM email that just created a work item):
1. Score using the same formula
2. Insert into the correct tier table
3. Mark as NEW in the report
4. Update the metrics cards

---

## Styling

Match the existing report style from `backlog-review-2026-04-08.html`:
- Purple gradient background
- White container with rounded corners
- Segoe UI font
- Sticky table headers
- Color-coded tier headings with left border
- Metric cards grid at top
- Footer with generation date

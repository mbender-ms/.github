# Phase 6: Article Counts and MAU from Power BI

**Step 1 — Article counts** (by `ms.service` for accuracy):
```bash
grep -rl "ms.service: {SERVICE_VALUE}" --include="*.md" | wc -l
```
Also count by folder paths from agent file for sub-area breakdowns.

**Step 2 — MAU from Power BI** (requires `powerbi-remote` MCP server):
- Semantic model: "Content Engagement Report" (ID: `aede3e37-62fd-475e-b629-dbb2d7683ab1`)
- Table: `Docs-Documentation`
- Key columns: `MSService`, `MSSubService`, `Visitors`, `PageViews`, `Date`

**DAX queries to execute** (divide by number of months in period for average):

```dax
-- Query 1: Top-level service metrics
-- Configure ms.service values from your agent file
EVALUATE SUMMARIZECOLUMNS(
    'Docs-Documentation'[MSService],
    FILTER('Docs-Documentation',
        'Docs-Documentation'[MSService] IN {"{ms_service_1}", "{ms_service_2}"}),
    "AvgVisitors", DIVIDE(SUM('Docs-Documentation'[Visitors]), {NUM_MONTHS}),
    "AvgPageViews", DIVIDE(SUM('Docs-Documentation'[PageViews]), {NUM_MONTHS})
)

-- Query 2: Sub-service breakdown (configure sub-service values from agent file)
EVALUATE SUMMARIZECOLUMNS(
    'Docs-Documentation'[MSSubService],
    FILTER('Docs-Documentation',
        'Docs-Documentation'[MSService] = "{ms_service_3}"
        && 'Docs-Documentation'[MSSubService] IN {
            "{sub_service_1}", "{sub_service_2}", "{sub_service_3}"
        }),
    "AvgVisitors", DIVIDE(SUM('Docs-Documentation'[Visitors]), {NUM_MONTHS}),
    "AvgPageViews", DIVIDE(SUM('Docs-Documentation'[PageViews]), {NUM_MONTHS})
)
```

**MSSubService values reference**:
Configure these from your agent file. Example format:
| Area | MSSubService value |
|------|-------------------|
| {Subarea1} | `{sub_service_1}` |
| {Subarea2} | `{sub_service_2}` |
| {Subarea3} | `{sub_service_3}` |

**Subtotal**: Sum of all sub-service values for a given area.

**Total across owned areas**: Sum of all top-level ms.service area values plus sub-service values.

The Power BI data reflects the LATEST month snapshot. The `{NUM_MONTHS}` divisor should match the number of full months in the Connect period (e.g., 5 for Nov-Mar).

**Step 3 — Save Phase 6 data for Phase 9 consumption**:
Store article counts and visitor data in a structured format the HTML generator can consume per product area:
```json
{
  "articleCounts": {
    "{Area1}": { "total": 146, "source": "ms.service: {ms_service_1}" },
    "{Area2}": { "total": 118, "source": "ms.service: {ms_service_2}" }
  },
  "visitors": {
    "{Area1}": { "visitors": 22589, "pageViews": 34606 },
    "{Area2}": { "visitors": 15275, "pageViews": 23453 }
  }
}
```
Save to: `{monthYYYY}/phase6-data.json`

If Power BI is unavailable, prompt the user for cached visitor numbers or skip the visitor section — do not fabricate data.

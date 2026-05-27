---
name: freshness-analysis
displayName: Freshness analysis
version: 1.0.0
category: Analysis
description: Query Power BI content engagement data for a service and month, then score and prioritize articles for freshness review based on age, traffic, engagement, and feedback. Use when the user says "freshness analysis", "which articles need updating", "run a freshness check", or "content metrics for my service".
argument-hint: 'service name and month (e.g., "azure-iot-operations January 2026")'
relevant-lesson-tags: [freshness, power-bi, content-metrics, prioritization]
user-invocable: true
disable-model-invocation: false
---

# Freshness Analysis Skill

Query Power BI semantic models for documentation engagement data, then score and prioritize articles for freshness review. Helps content developers decide which articles need updating first based on traffic, engagement, ratings, verbatim feedback, and last-reviewed dates.

**Invocation:**
- `/freshness-analysis azure-iot-operations January 2026` — Run analysis for a service and month
- `/freshness-analysis` — Start a guided conversation (will prompt for service and date)

**When to use this skill:**
- User says "freshness analysis", "which articles need updating", "run a freshness check"
- User asks "content metrics for my service" or "what should I prioritize this month"
- User wants to plan a freshness review pass on their content area

**Required tools:**
- `powerbi-remote` MCP server (for DAX queries)
- File read access (to surface clickable local paths to articles)

---

## Phase 1: Query the data

1. Use the known Artifact ID in the **Semantic model** section below to query the semantic model directly — do **not** call any schema retrieval tools. The full table schema is provided in **Docs-Documentation table schema** below; always use it as-is.
2. Execute a DAX query to retrieve all articles filtered by `MSService` matching the specified service and month. Only return articles where `LiveUrl` contains `en-us` (English content). Set `maxRows` to `1000` to avoid truncation.
3. Include all columns listed in the schema — they are all needed for the analysis phase.

### DAX query pattern (always use this structure)

Always use `CALCULATETABLE()` for filtering — never use `FILTER(SELECTCOLUMNS(...), ...)`. The `FILTER` + `SELECTCOLUMNS` pattern loses row context and causes a "single value cannot be determined" error. Substitute the service name, year, month, and last day of month:

```dax
EVALUATE
CALCULATETABLE(
    SELECTCOLUMNS(
        'Docs-Documentation',
        "Title", 'Docs-Documentation'[Title],
        "LiveUrl", 'Docs-Documentation'[LiveUrl],
        "MSSubService", 'Docs-Documentation'[MSSubService],
        "PageViews", 'Docs-Documentation'[PageViews],
        "Engagement", 'Docs-Documentation'[Engagement],
        "LastReviewed", 'Docs-Documentation'[LastReviewed],
        "Ratings", 'Docs-Documentation'[Ratings],
        "Verbatims", 'Docs-Documentation'[Verbatims],
        "Freshness", 'Docs-Documentation'[Freshness],
        "MSService", 'Docs-Documentation'[MSService],
        "Date", 'Docs-Documentation'[Date]
    ),
    'Docs-Documentation'[MSService] = "<service>",
    'Docs-Documentation'[Date] >= DATE(<year>, <month>, 1),
    'Docs-Documentation'[Date] <= DATE(<year>, <month>, <last-day>),
    CONTAINSSTRING('Docs-Documentation'[LiveUrl], "en-us")
)
ORDER BY [PageViews] DESC
```

## Phase 2: Analyze the data

Help the writer decide which articles need to be updated first.

1. **Identify problems:**
   - Articles with high views but low engagement (`Engagement = "L"`) are HIGH PRIORITY.
   - Articles with negative ratings (`Ratings < 0`) are HIGH PRIORITY.
   - Articles with verbatim comments (`Verbatims > 0`) are HIGH PRIORITY.
   - Articles where `LastReviewed` is more than 90 days before the first day of the query month are MEDIUM PRIORITY.
   - If `Ratings` and `Verbatims` are null for all rows, skip the feedback scoring rules and note this in the output.

2. **Score each article** (start at 0):
   - +1 point per 500 page views
   - +3 points if `Engagement = "L"`
   - +2 points if `Ratings < 0`
   - +1 point per verbatim comment (`Verbatims` value)
   - +1 point if `LastReviewed` is more than 90 days before the first day of the query month

3. **List the top 10 articles** by priority score (highest first).

4. **For each article, provide:**
   - Why it's a priority (use specific numbers and quotes from verbatim feedback where available)
   - What specific problem needs fixing
   - A suggested action (e.g., "Add SSO login instructions" or "Update screenshots for v2.0")
   - The local path to the article in the current workspace. Make this path a clickable link so the writer can navigate directly to the file.

Write in a friendly but professional tone.

## Semantic model

- **Name:** Content Engagement Report
- **Artifact ID:** `aede3e37-62fd-475e-b629-dbb2d7683ab1`
- **Workspace:** Skilling-BCS-DataPlatform-PROD
- **MCP server:** powerbi-remote

## Docs-Documentation table schema

| Column | Type |
|---|---|
| Title | String |
| LiveUrl | String |
| MSSubService | String |
| PageViews | Int64 |
| Engagement | String (H/L) |
| LastReviewed | DateTime |
| Ratings | Int64 |
| Verbatims | Int64 |
| Freshness | String (0-90 days / 91-180 days / 181-270 days / 271-365 days / >365 days) |
| MSService | String |
| Date | DateTime |

---

## Important rules

- **Always include `en-us` filter** — non-English locales will skew the analysis.
- **Use `CALCULATETABLE`, not `FILTER` + `SELECTCOLUMNS`** — the latter throws "single value cannot be determined".
- **Set `maxRows: 1000`** — default truncation drops rows for high-traffic services.
- **Don't fetch the schema dynamically** — the schema is stable and documented above. Schema-retrieval calls add latency and tokens.
- **Make file paths clickable** — writers want to jump straight to the article they need to edit.
- **Note missing feedback data** — if Ratings/Verbatims are null across all rows, surface this so the writer knows the score reflects only traffic and freshness signals.

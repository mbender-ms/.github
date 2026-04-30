# Gap Analysis Instructions

This file governs Phase 3 of the Q&A Gap Analyst pipeline.

## Input

The scored eval CSV from Phase 2:
`agents/qa-gap-analyst/artifacts/{service}-qa-eval-{MMDDYYYY}.csv`

Columns: `Question, Source, Type, Confidence, Notes, chunk_relevance_score, generated_answer`

## Gap threshold

Flag any row where `chunk_relevance_score < 3.5` as a **gap signal**.

Score interpretation:

| Score | Meaning |
|---|---|
| 1–2 | Priority gap — documentation likely missing or fundamentally wrong |
| 3 | Partial gap — something exists but it does not adequately answer the question |
| 3.5+ | Acceptable — skip (not a gap) |

---

## Step 3.1 — Filter gap signals

From the eval CSV, collect all rows where `chunk_relevance_score < 3.5`.

Sort by score ascending (lowest first = highest priority).

If there are zero gap signals, write a report stating that documentation coverage appears adequate for the evaluated question set and exit Phase 3.

---

## Step 3.2 — Article matching

For each gap signal question, run:

```
microsoft_docs_search("{question text}")
```

Record:
- Top result URL (`top_url`)
- Top result article title (`top_title`)
- Top result article path — extract the path from the URL after `learn.microsoft.com` (e.g., `/azure/load-balancer/quickstart-load-balancer-standard-public-portal`)
- Top result relevance (your judgment: **Relevant**, **Partial**, **Unrelated**)

**Relevance classification rules:**

| Top result relevance | Meaning |
|---|---|
| Relevant | The article is clearly about the same service and topic as the question |
| Partial | The article touches the topic but is about a different scenario, adjacent service, or a different task level |
| Unrelated | The returned article has nothing to do with the question — covers a different service entirely |

Process gap signals in batches of 10 to avoid rate limits on `microsoft_docs_search`.

---

## Step 3.3 — Gap type classification

Classify each gap signal using the rules in `references/gap-types.md`.

Short version:

| Condition | Gap type |
|---|---|
| Top result is **Unrelated** or no results returned | `new-article` |
| Top result is **Partial** | `add-section` |
| Top result is **Relevant** but score is 1–2 | `update-article` |
| Top result is **Relevant** and score is 3 | `add-section` |

When in doubt between `update-article` and `add-section`, prefer `add-section` — it is a smaller, safer scope.

---

## Step 3.4 — Build gap recommendation

For each classified gap, write a one-sentence recommendation:

| Gap type | Recommendation format |
|---|---|
| `new-article` | `Create a new article covering: {topic derived from question}` |
| `update-article` | `Update {article title} to address: {specific missing content}` |
| `add-section` | `Add a section to {article title} covering: {specific scenario or detail}` |

Derive the topic and specific missing content from the `Question` text and the `generated_answer` (which shows what the model tried to say but couldn't ground well).

---

## Step 3.5 — Write gap CSV

Write to `agents/qa-gap-analyst/output/{service}-gap-analysis-{MMDDYYYY}.csv`.

Header and column definitions:

| Column | Value |
|---|---|
| `Question` | Original question text |
| `Score` | `chunk_relevance_score` from Phase 2 |
| `Gap_Type` | `new-article` · `update-article` · `add-section` |
| `Target_Article_Title` | Top result article title, or `(none)` |
| `Target_Article_URL` | Top result full URL, or `(none)` |
| `Target_Article_Path` | Path portion of URL (e.g., `/azure/load-balancer/...`), or `(none)` |
| `Recommendation` | One-sentence recommendation |

Sort rows: `new-article` first, then `update-article`, then `add-section`. Within each type, sort by `Score` ascending.

---

## Step 3.6 — Write gap Markdown report

Write to `agents/qa-gap-analyst/output/{service}-gap-report-{MMDDYYYY}.md`.

Report structure:

```
# Documentation Gap Report — {Service Name}
Generated: {date}
Questions evaluated: {total}
Gap signals (score < 3.5): {gap count}

---

## Summary

| Gap Type | Count |
|---|---|
| new-article | {n} |
| update-article | {n} |
| add-section | {n} |

---

## New Articles Needed

{For each new-article gap:}
### {Question} (score: {score})
**Recommendation:** {recommendation}

---

## Articles to Update

{For each update-article gap, grouped by Target_Article_Title:}
### {Target_Article_Title}
**Article path:** `{Target_Article_Path}`

| Question | Score | Recommendation |
|---|---|---|
| {question} | {score} | {recommendation} |

---

## Sections to Add

{For each add-section gap, grouped by Target_Article_Title:}
### {Target_Article_Title}
**Article path:** `{Target_Article_Path}`

| Question | Score | Recommendation |
|---|---|---|
| {question} | {score} | {recommendation} |
```

---

## Step 3.7 — Report summary to user

After writing both output files, summarize in chat:

- Total questions evaluated
- Total gap signals
- Breakdown: `{n} new-article | {n} update-article | {n} add-section`
- Top 3 articles with the most gaps (by Target_Article_Path, excluding `(none)`)
- Paths to both output files

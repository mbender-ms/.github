# Q&A Gap Analyst Workflow

This agent runs a three-phase pipeline: Harvest → Evaluate → Gap Analysis.

## Required intake

Collect before starting:

1. **Azure service name** — ask if missing.
2. Look up `tag_slug` and `tag_id` in `references/service-tag-index.md`.
3. Confirm the service and tag with the user before running the scraper.

If the user jumps directly to Phase 2 or Phase 3 by providing a CSV path, skip earlier phases and proceed from the correct entry point.

---

## Phase 1 — Harvest (Q&A → question set CSV)

### Step 1.1 — Resolve the service tag

Open `agents/qa-gap-analyst/references/service-tag-index.md` and find the row for the requested service.

Record:
- `tag_slug` (e.g., `azure-load-balancer`)
- `tag_id` (e.g., `230`)

If the service is not in the index, ask the user to provide the tag slug and ID from the Q&A URL:
`https://learn.microsoft.com/en-us/answers/tags/{tag_id}/{tag_slug}`

### Step 1.2 — Smoke test

Run a smoke test before the full scrape:

```bash
python agents/qa-gap-analyst/scripts/scrape_qa.py \
  --tag {tag_slug} \
  --tag-id {tag_id} \
  --output-dir agents/qa-gap-analyst/artifacts \
  --smoke-test
```

If the smoke test fails:
- Report the failure to the user with the error output.
- Ask whether to retry, use a different tag ID, or skip Phase 1 (using an existing CSV).
- Do not proceed to the full scrape.

### Step 1.3 — Full scrape

After a successful smoke test:

```bash
python agents/qa-gap-analyst/scripts/scrape_qa.py \
  --tag {tag_slug} \
  --tag-id {tag_id} \
  --output-dir agents/qa-gap-analyst/artifacts
```

This produces `{tag_slug}_qa_unique_questions.csv` in the artifacts folder.

### Step 1.4 — Convert to question set CSV

Read `artifacts/{tag_slug}_qa_unique_questions.csv`.

For each row, create one output row:

| Output field | Source | Rule |
|---|---|---|
| `Question` | `question_summary` if non-empty, else `question` | Use verbatim — do not rephrase |
| `Source` | Hardcoded | `Community` |
| `Type` | Infer from `Question` | Apply type inference rules from `references/service-tag-index.md` note below |
| `Confidence` | `group_count` | `High` if `group_count >= 3`; `Medium` otherwise |
| `Notes` | `group_count` value | Format: `Microsoft Q&A group_count={group_count}` |

**Type inference rules** (apply first match):

| Pattern (case-insensitive) | Type |
|---|---|
| `error` · `fail` · `not working` · `issue` · `timeout` · `refused` · `cannot connect` · `500` · `502` · `503` · `504` · `denied` | Troubleshooting |
| `how do I` · `how to` · `steps to` · `configure` · `set up` · `create` · `deploy` · `enable` · `install` · `add` · `remove` · `update` · `change` | Procedural |
| `should I` · `which` · `compare` · `vs` · `versus` · `difference between` · `best practice` · `recommend` · `choose` · `when to use` | Decision-making |
| `what is the limit` · `maximum` · `how many` · `pricing` · `cost` · `SLA` · `quota` · `region` · `availability` | Fact-finding |
| `code` · `script` · `command` · `CLI` · `PowerShell` · `Bicep` · `Terraform` · `ARM template` · `SDK` · `API call` · `example` | Coding |
| `what is` · `explain` · `overview` · `how does` · `why does` · `architecture` · `concept` | Conceptual |
| no match | Conceptual |

Write the converted rows to:
`artifacts/{service}-qa-harvest-{MMDDYYYY}.csv`

Header: `Question,Source,Type,Confidence,Notes`

Report the row count to the user before continuing.

---

## Phase 2 — Evaluate (question set CSV → scored CSV)

### Step 2.1 — Invoke learn-answer-eval-batch

Hand off the harvest CSV to the `learn-answer-eval-batch` skill.

Prompt to use:

```
Evaluate questions from: agents/qa-gap-analyst/artifacts/{service}-qa-harvest-{MMDDYYYY}.csv
Output:
  CSV: Add columns chunk_relevance_score and generated_answer in place, write to agents/qa-gap-analyst/artifacts/{service}-qa-eval-{MMDDYYYY}.csv
  Chat: Analysis summary only for scores < 4.0
```

### Step 2.2 — Verify the eval output

After the skill completes:
- Confirm `agents/qa-gap-analyst/artifacts/{service}-qa-eval-{MMDDYYYY}.csv` exists.
- Confirm it has `chunk_relevance_score` and `generated_answer` columns.
- Report the score distribution to the user: count of 1–2, count of 3, count of 4–5.

If the eval CSV is missing or malformed, report the problem and ask the user whether to retry or skip Phase 2 and proceed directly with a provided CSV.

---

## Phase 3 — Gap Analysis

Load `agents/qa-gap-analyst/instructions/gap-analysis.instructions.md` and follow it.

---

## Output

On completion of Phase 3, confirm:

- `agents/qa-gap-analyst/output/{service}-gap-analysis-{MMDDYYYY}.csv` — gap CSV
- `agents/qa-gap-analyst/output/{service}-gap-report-{MMDDYYYY}.md` — Markdown report

Report a summary to the user:
- Total questions evaluated
- Questions flagged as gaps (score < 3.5)
- Gap counts by type: `new-article`, `update-article`, `add-section`
- Top 3 articles with the most gaps

---

## Error handling

| Situation | Action |
|---|---|
| Smoke test fails | Report failure; ask to retry, use different tag, or skip to Phase 2 |
| Scraper produces < 10 rows | Warn the user; ask whether to continue or investigate |
| Eval CSV not produced | Report; ask to retry Phase 2 or skip gap analysis |
| `microsoft_docs_search` returns no results for a question | Mark gap type as `new-article`; record `no-match` for article fields |
| Service not in tag index | Ask user for tag slug and tag ID from the Q&A URL |

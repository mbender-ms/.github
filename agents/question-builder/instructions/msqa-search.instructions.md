# msqa-search Workflow

This internal workflow handles the **Microsoft Q&A** source for Question Builder.

## Purpose

Scrape Microsoft Q&A questions for the selected Azure service, group similar questions by frequency, and convert them into Question Builder rows.

## Rules

1. Resolve the service to a Q&A tag slug and tag ID using `references/service-tag-index.md`.
2. Run Q&A scraping through a **subagent**.
3. Write all scraper outputs to `artifacts/` only.
4. Convert the grouped results into Question Builder rows for the single final CSV.
5. Do not deliver the raw or grouped Q&A CSVs as final outputs.

## Subagent handoff

When Microsoft Q&A is selected:

1. Launch a subagent that runs:

   ```bash
   python agents/question-builder/scripts/scrape_qa.py --tag "{tag_slug}" --tag-id {tag_id} --output-dir "agents/question-builder/artifacts"
   ```

2. If the tag is unfamiliar, run the scraper once with `--smoke-test` first.
3. Read `{tag}_qa_unique_questions.csv` from `artifacts/`.
4. Convert rows into Question Builder output format:
   - `Question` = `question_summary` when present, otherwise `question`
   - `Source` = `Community`
   - `Type` = infer from `Question`
   - `Confidence` = `High` when `group_count >= 3`, otherwise `Medium`
   - `Notes` = `Microsoft Q&A group_count={group_count}`

## Failure handling

- If the smoke test fails, ask the user to confirm the service selection or tag.
- If the scraper fails after validation, continue without Microsoft Q&A and report the gap.
- If the scraper creates no usable grouped rows, continue without Microsoft Q&A and report the gap.
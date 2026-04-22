# Question Builder Workflow

Question Builder builds a tagged evaluation question set for an Azure service and writes exactly one final CSV.

## Required intake

Collect these inputs before collection begins:

1. **Azure service** — ask if missing.
2. **Total question count** — ask if missing.
3. **Source checklist** — always confirm which sources to use before running.
4. **Mode** — default is `fresh`; switch to `append` only if the user explicitly references an existing CSV.

If the user already supplied one or more of these values, do not ask for them again.

## Source checklist

Present these options as a checklist:

- Single article
- Multiple articles
- Microsoft Q&A
- Canonical CSV
- Customer issue spec
- GitHub Issues
- WorkIQ M365
- Ask Learn telemetry via canonical CSV

## Output contract

- Deliver **one final CSV only**.
- Base the output schema on `templates/question-set-template.csv`.
- Apply the metadata rules from `references/metadata-tagging-guide.md`.
- Use `artifacts/` for temporary files only.
- Use `output/` for the final CSV only.
- Do not create extra markdown summaries, notes files, or sidecar CSV outputs for the user.

## Workflow

### Step 1 — Intake

1. Resolve any missing required intake values.
2. If the service is ambiguous, ask the user to choose the Azure service.
3. If the user provides sources implicitly in the prompt, still present the full checklist and confirm the selected sources before proceeding.

### Step 2 — Gather questions from selected sources

Read `references/source-workflows.md` and execute only the selected source workflows.

Special handling:

- **Multiple articles**: use one subagent per article and run them in parallel.
- **Microsoft Q&A**: use the packaged `msqa-search` instructions and run scraping through a subagent.

### Step 3 — Classify and tag

Apply `Question`, `Source`, `Type`, `Confidence`, and `Notes` exactly as defined in `references/metadata-tagging-guide.md`.

### Step 4 — Deduplicate

Use fuzzy token-sort matching at 80% threshold.

- **Fresh mode**: deduplicate within the current run.
- **Append mode**: deduplicate against the existing CSV and preserve the existing rows on conflict.

### Step 5 — Write final CSV

1. Sort rows by `Source`, then `Confidence` (`High`, `Medium`, `Low`).
2. Write the final CSV with this exact header:

   ```csv
   Question,Source,Type,Confidence,Notes
   ```

3. Name the file `<service-name>-questions-<MMDDYYYY>.csv` unless the user gave a specific path.
4. Write the file to the configured output folder unless the user overrides it.

### Step 6 — Fan-out is opt-in only

Only run fan-out when the user explicitly requests it.

- Fan-out from high-signal canonical questions follows the pilot guidance in `references/metadata-tagging-guide.md`.
- For other sources, keep the same Source and lower the confidence by one step unless the reference guidance says otherwise.
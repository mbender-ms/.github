# Q&A Gap Analyst

A fully self-contained GitHub Copilot agent that turns real customer questions from Microsoft Q&A into structured documentation gap findings.

---

## What it does

Runs a three-phase pipeline:

1. **Harvest** — Scrapes Microsoft Q&A for an Azure service, groups similar questions by frequency, and writes a question set CSV.
2. **Evaluate** — Runs the question set through the Learn retrieval pipeline to score how well existing documentation answers each question.
3. **Gap Analysis** — Maps low-scoring questions to specific Learn articles and classifies each gap (`new-article`, `update-article`, or `add-section`).

Outputs a gap CSV and a Markdown report you can use directly or feed into downstream workflows (ADO work items, PR drafts, Connect articles).

---

## Prerequisites

| Requirement | Notes |
|---|---|
| VS Code | Latest stable |
| GitHub Copilot extension | Agent mode enabled |
| `.github` repo cloned locally | This package must be in your VS Code workspace |
| Python 3.10+ | Required for Q&A scraping (Phase 1) |
| Scraper dependencies | `pip install -r agents/qa-gap-analyst/scripts/requirements.txt` |
| Learn MCP server | Required for Phase 2 evaluation and Phase 3 gap analysis |

---

## Quick start

1. Open the `.github` folder as a VS Code workspace folder.
2. Open Copilot Chat, switch to **Agent mode**, and select **Q&A Gap Analyst**.
3. Tell it which service you want to analyze.

   Example:

   `Run gap analysis for Azure Load Balancer`

4. The agent confirms the service tag, runs a smoke test, then proceeds through all three phases.
5. Outputs land in `agents/qa-gap-analyst/output/` unless you override the path.

---

## Running individual phases

| Command | What runs |
|---|---|
| `Smoke test Azure Load Balancer` | Phase 1 scraper smoke test only |
| `Scrape Q&A for Azure Firewall` | Phase 1 full scrape only |
| `Evaluate these questions: path/to/file.csv` | Phase 2 only |
| `Analyze gaps in path/to/eval.csv` | Phase 3 only |

---

## Output contract

Two files are written to `agents/qa-gap-analyst/output/` on completion of the full pipeline:

| File | Purpose |
|---|---|
| `{service}-gap-analysis-{MMDDYYYY}.csv` | Machine-readable gap findings |
| `{service}-gap-report-{MMDDYYYY}.md` | Human-readable Markdown report grouped by gap type and article |

The `artifacts/` folder holds intermediate files (raw CSVs, eval CSVs) that are gitignored.

---

## File structure

| File | Purpose |
|---|---|
| `agents/qa-gap-analyst.agent.md` | VS Code agent launcher |
| `agents/qa-gap-analyst/README.md` | This file |
| `agents/qa-gap-analyst/.gitignore` | Keeps artifacts and outputs out of git |
| `agents/qa-gap-analyst/config/variables.yaml` | Default paths and thresholds |
| `agents/qa-gap-analyst/instructions/workflow.instructions.md` | Full 3-phase pipeline |
| `agents/qa-gap-analyst/instructions/gap-analysis.instructions.md` | Phase 3 detail — gap classification rules |
| `agents/qa-gap-analyst/references/service-tag-index.md` | Service → Q&A tag slug and ID lookup |
| `agents/qa-gap-analyst/references/gap-types.md` | Gap type definitions and classification criteria |
| `agents/qa-gap-analyst/scripts/scrape_qa.py` | Q&A scraper (self-contained copy) |
| `agents/qa-gap-analyst/scripts/requirements.txt` | Python dependencies for the scraper |
| `agents/qa-gap-analyst/templates/gap-csv-template.csv` | Output CSV schema reference |
| `agents/qa-gap-analyst/templates/gap-report-template.md` | Output report schema reference |
| `agents/qa-gap-analyst/artifacts/` | Temporary intermediate files (gitignored) |
| `agents/qa-gap-analyst/output/` | Final outputs (gitignored) |

---

## Downstream workflows

| Goal | What to do with the output |
|---|---|
| Create ADO work items for gaps | Feed gap report into the `content-workflow` skill — creates scoped User Stories per gap cluster |
| Draft article edits | Use `content-developer.agent.md` with the `update-article` gap rows as input |
| Write new Connect articles | Use `connect-writer.agent.md` with `new-article` gap rows as input |
| Freshness triage | Run `freshness-pass` skill against `update-article` target articles |
| Track improvement over time | Run monthly, compare gap CSVs across runs |

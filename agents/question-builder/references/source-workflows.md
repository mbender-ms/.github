# Source Workflows

Detailed per-source collection workflows for Question Builder.

---

## Single article

Generate questions grounded in one documentation article.

### Inputs

| Input | Required | Example |
|-------|----------|---------|
| Article path or URL | Yes | `articles/application-gateway/overview.md` |

### Steps

1. Load the `article-question-generation` skill.
2. Provide the article path, open file, or Learn URL.
3. Convert the results to Question Builder rows:
   - `Source` = `Content dev`
   - `Type` = infer from the generated question
   - `Confidence` = `Low`
   - `Notes` = article path or URL

---

## Multiple articles

Generate questions from several articles.

### Inputs

| Input | Required | Example |
|-------|----------|---------|
| Article paths or URLs | Yes | List of article paths or Learn URLs |

### Steps

1. Launch one subagent per article in parallel.
2. Use the same single-article workflow for each article.
3. Merge the results.
4. Deduplicate before writing the final CSV.

---

## Microsoft Q&A

Scrape public Microsoft Q&A questions for the selected service.

### Inputs

| Input | Required | Example |
|-------|----------|---------|
| Azure service | Yes | `Application Gateway` |
| Tag slug | Auto-resolved | `azure-application-gateway` |
| Tag ID | Auto-resolved | `148` |
| Canonical CSV | No | `canonical-set-mar2026.csv` |

### Steps

1. Resolve tag data using `service-tag-index.md`.
2. Load `instructions/msqa-search.instructions.md`.
3. Run the scraper through a subagent.
4. Store raw and grouped outputs in `artifacts/` only.
5. Convert grouped unique questions into final Question Builder rows.

---

## Canonical CSV

Import questions from telemetry-backed or curated canonical CSVs.

### Inputs

| Input | Required | Example |
|-------|----------|---------|
| CSV path | Yes | `canonical-set-mar2026.csv` |
| Azure service | Yes | `Application Gateway` |

### Steps

1. Read the CSV and map the question and service columns.
2. Filter to the selected Azure service.
3. Convert rows into Question Builder rows:
   - `Source` = `AI system`
   - `Type` = infer from question text
   - `Confidence` = `High`
   - `Notes` = include `conversation_count` and any original source when available
4. If the user explicitly asks for fan-out from canonical questions, keep `Source = AI system` and `Confidence = High` for high-signal canonical variants per the pilot guidance.

---

## Customer issue spec

Generate customer-phrased questions from known issues.

### Inputs

| Input | Required | Example |
|-------|----------|---------|
| Issue descriptions | Yes | `502 errors with WAF, SSL certificate rotation failures` |

### Steps

1. Split the known issues into distinct issue themes.
2. Distribute the requested total question count across the issues.
3. Generate customer-phrased questions with a mix of troubleshooting, procedural, and conceptual phrasing.
4. Convert rows into Question Builder rows:
   - `Source` = `Patterns/Insights`
   - `Confidence` = `Medium`
   - `Notes` = `Known issue: {issue description}`

---

## GitHub Issues

Extract customer-facing questions from documentation issues.

### Inputs

| Input | Required | Default |
|-------|----------|---------|
| Azure service | Yes | — |
| Repository | No | `MicrosoftDocs/azure-docs-pr` |

### Steps

1. Resolve the service label from `service-tag-index.md`.
2. Search issues with `mcp_github_search_issues`.
3. Convert relevant documentation gaps, confusion reports, and question-like issues into Question Builder rows:
   - `Source` = `Community`
   - `Confidence` = `Medium`
   - `Notes` = GitHub issue reference

---

## WorkIQ M365

Search internal Microsoft 365 sources for customer-signal questions.

### Steps

1. Query WorkIQ for service-specific discussion and signal keywords.
2. Convert question-like findings into Question Builder rows.
3. Tag internal discussion sources as `Product team` and document-derived findings as `AI system`.
4. Use `Confidence = Medium` unless a stronger signal is explicitly available.

---

## Ask Learn telemetry via canonical CSV

For the current pilot, Ask Learn telemetry is handled through the canonical CSV pathway.

### Steps

1. Use the canonical CSV workflow.
2. Keep `Source = AI system`.
3. Keep `Confidence = High`.
4. Preserve conversation counts in `Notes` when available.
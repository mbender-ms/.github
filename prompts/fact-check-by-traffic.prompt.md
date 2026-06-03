---
mode: agent
description: "Query top articles by traffic for a service+month, then fact-check them — all in one shot"
tools:
  - mcp_powerbi-remot_ExecuteQuery
  - mcp_azure-docs_search_docs
  - mcp_azure-docs_check_article_freshness
  - mcp_azure-docs_what_integrates_with
  - mcp_microsoft-lea_microsoft_docs_search
  - mcp_microsoft-lea_microsoft_code_sample_search
  - read/readFile
  - search/textSearch
---

# Fact-Check by Traffic

Run the `pageviews-query` skill, then immediately pass the resulting JSON handoff block as input to the `doc-verifier` skill's Fleet Batch workflow. Do not pause between phases.

## Inputs

- **service** — `MSService` value (for example, `azure-application-gateway`)
- **month** — report month (for example, `April 2026`)
- **count** — articles to fact-check (default: **3**)

If any input is missing, ask once before starting.

## Execution

1. **Phase 1**: Run the full `pageviews-query` skill for the given service, month, and count. Emit the ranked table and JSON handoff block.
2. **Phase 2**: Pass the JSON handoff block directly to the `doc-verifier` Fleet Batch workflow. Process articles in rank order without waiting for user input.
3. **Phase 3**: Emit the Batch Summary table defined in the `doc-verifier` skill, followed by 2–3 recommended next steps.

---
mode: agent
description: Fact-check the current article against official Microsoft documentation
tools:
  - microsoft-learn-mcp-server/microsoft_docs_search
  - microsoft-learn-mcp-server/microsoft_docs_fetch
  - microsoft-learn-mcp-server/microsoft_code_sample_search
  - read/readFile
  - read/problems
  - search/codebase
  - search/fileSearch
  - search/textSearch
  - edit/editFiles
  - todo
---

# Single Article Fact-Check

Fact-check the currently open article against official Microsoft documentation. Verify every technical claim, apply corrections in-place, and present a summary with source citations.

## Report output (`--report`)

By default this workflow is **chat-only** — it does not write a report file. Write a standalone markdown report only when the user asks for one:

- If the user passes `--report <path>`, write the report to that exact path.
- If the user requests a report ("save a report", "write the findings to a file") but gives **no path**, ask for the path before completing — do not guess a default location.
- If neither is present, present results in chat only.

## Setup

Load [_shared/source-hierarchy.md](../../_shared/source-hierarchy.md) for the complete tiered source authority reference.

For product-area-specific repo lookups, consult [sources/routing-index.md](../../sources/routing-index.md) and load the matching category YAML only if you need repo-level detail.

## Step 0 — Scope

Before starting, determine:
1. **Product area** — Read the file's `ms.service`, `ms.prod`, or content to identify the product area.
2. **Service focus** — Identify the specific service or feature.
3. **Depth** — Ask the user: "Quick check or thorough verification?"

Use the product area to select search domains (see SKILL.md → Product Area Search Domains).

## Step 1 — Identify claims

Read the current file and extract every verifiable technical claim:
- Product/service names, feature capabilities, limitations, SKU/tier requirements
- Version numbers, API references, CLI/PowerShell commands
- Configuration values, defaults, quotas, limits, pricing, regional availability
- Preview/GA/deprecated status
- Code examples and syntax

## Step 2 — Verify against sources

For each claim, search in priority order per the source hierarchy:
1. `microsoft_docs_search` — product-area-specific terms
2. `microsoft_docs_fetch` — full pages when snippets are insufficient
3. `microsoft_code_sample_search` — validate code examples
4. `grep_search` / `semantic_search` — cross-reference workspace content
5. Check for deprecation, preview/GA status, retirement notices

## Step 3 — Classify accuracy

- **✅ Accurate** — Matches current official documentation
- **⚠️ Partially accurate** — Mostly correct, needs refinement
- **❌ Inaccurate** — Contradicted by official sources
- **🕐 Outdated** — Was correct, no longer current
- **❓ Unverifiable** — No authoritative source found — flag, do not remove

## Step 4 — Apply corrections

Edit the file directly. Preserve tone/style. Update `ms.date`. Do NOT remove unverifiable claims.

## Step 5 — Present results

Summarize: total claims checked, issues by severity, per-issue details with source URLs. Ask to commit.

If a report was requested (see **Report output**), write the summary and per-issue details to the resolved `--report` path before finishing.

## Quality

See [_shared/quality-checklist.md](../../_shared/quality-checklist.md) — verify the fact-check quality section.

---
mode: agent
description: "Fact-check multiple articles in parallel using /fleet mode. Each article gets its own subagent and produces an independent verification report. Designed for Copilot CLI: /fleet fact-check these articles"
tools:
  - microsoft-learn-mcp-server/microsoft_docs_search
  - microsoft-learn-mcp-server/microsoft_docs_fetch
  - microsoft-learn-mcp-server/microsoft_code_sample_search
  - read/readFile
  - read/problems
  - search/fileSearch
  - search/textSearch
  - edit/editFiles
  - edit/createFile
  - execute/runInTerminal
  - execute/getTerminalOutput
  - agent/runSubagent
  - todo
---

# Fleet Batch Verification

Fact-check a set of Microsoft documentation articles **in parallel**. Each article is an independent work item with its own output file. Optimized for Copilot CLI `/fleet` mode and VS Code parallel subagents.

> **Runtime**: `/fleet fact-check these articles using @fleet-batch-verify`
> Each article runs as a separate subagent track. Reports merge at the end.

## Setup

Load [_shared/source-hierarchy.md](../_shared/source-hierarchy.md) for the source authority reference. Higher tier always wins.

## Step 0 — Scope and decompose

Ask the user (skip if already clear):
1. **File scope** — Which articles? (folder path, glob, or explicit list)
2. **Depth** — Quick (search-only) or thorough (search + fetch + code samples)?
3. **Output** — Reports only, corrections + reports, or corrections only?

Discover files:
- If folder: list all `.md` files recursively
- If glob: expand the pattern
- If file list: validate each path exists

**Decomposition rule for /fleet**: Map every article to one concrete output artifact. The orchestrator should see a structure like:

```
Track 1: articles/networking/load-balancer-health-probes.md → factcheck_load-balancer-health-probes_YYYYMMDD.md
Track 2: articles/compute/create-vm-portal.md → factcheck_create-vm-portal_YYYYMMDD.md
Track 3: articles/identity/configure-mfa.md → factcheck_configure-mfa_YYYYMMDD.md
```

Each track is independent — no shared state, no dependencies between tracks.

## Step 1 — Per-article verification (runs in parallel)

Each subagent receives ONE article and executes these steps:

### 1a. Read and extract claims

Read the article. Extract every verifiable technical claim:
- Product/service names, feature capabilities, limitations, SKU/tier requirements
- Version numbers, API references, CLI/PowerShell commands
- Configuration values, defaults, quotas, limits, pricing
- Preview/GA/deprecated status
- Code examples and syntax

Group claims by service area (read `ms.service` / `ms.prod` from frontmatter).

### 1b. Verify against official sources

For each claim, search in priority order:
1. `microsoft_docs_search` — use service-area-specific queries
2. `microsoft_docs_fetch` — fetch full pages only for high-value matches (max 2-3 per service group)
3. `microsoft_code_sample_search` — validate code examples

**Token budget**: Use `maxTokenBudget=2000` on fetch calls to cap context size. Search first, fetch selectively.

### 1c. Classify findings

For each claim:
- **✅ Accurate** — Matches current official documentation
- **⚠️ Partially accurate** — Minor discrepancy or missing context
- **❌ Inaccurate** — Contradicts official sources
- **🕐 Outdated** — Was correct but superseded
- **❓ Unverifiable** — No authoritative source found — flag, do not remove
- **🔗 Broken link** — URL doesn't resolve or anchor is missing

### 1d. Generate per-article report

Create `factcheck_[articlename]_YYYYMMDD.md` containing:

```markdown
# Fact-Check Report: [Article Title]

**File**: [path]
**Date**: YYYY-MM-DD
**Service area**: [from ms.service]
**Claims checked**: [count]

## Summary

| Status | Count |
|--------|-------|
| ✅ Accurate | N |
| ⚠️ Partial | N |
| ❌ Inaccurate | N |
| 🕐 Outdated | N |
| ❓ Unverifiable | N |
| 🔗 Broken link | N |

## Findings

### [Finding 1 — severity icon] [brief description]

- **Line(s)**: [line numbers]
- **Original**: [quoted text]
- **Corrected**: [fix]
- **Source**: [Title](URL) — Tier [N]

## Sources consulted

| # | Title | URL | Tier |
|---|-------|-----|------|
```

### 1e. Apply corrections (if requested)

If the user wants corrections:
- Edit the article directly
- Update `ms.date` in frontmatter
- Do NOT remove unverifiable claims

## Step 2 — Consolidate (after all tracks complete)

Once all parallel tracks finish, the orchestrator:

1. Read all per-article reports
2. Generate `factcheck_batch_YYYYMMDD.md` with:
   - **Executive summary** — total files, total claims, overall health score
   - **Cross-article patterns** — repeated issues across files (e.g., same deprecated API referenced in 3 articles)
   - **Per-file summary table**:

```markdown
| File | Claims | ✅ | ⚠️ | ❌ | 🕐 | ❓ | 🔗 |
|------|--------|----|-----|----|----|----|----|
```

3. Flag any cross-article inconsistencies (article A says X, article B says Y about the same feature)

## Quality checklist

See [_shared/quality-checklist.md](../_shared/quality-checklist.md). Additionally:
- [ ] Every article processed (none skipped)
- [ ] Each per-article report saved
- [ ] Consolidated report generated
- [ ] Cross-article patterns identified
- [ ] Corrections applied only if user requested

## /fleet prompt template

When running from Copilot CLI, use this structure:

```
/fleet Fact-check the following articles against Microsoft Learn documentation.
Each article is an independent track with its own report file.
Use @fleet-batch-verify as the agent for all tracks.

Articles:
1. articles/networking/load-balancer-health-probes.md → factcheck_load-balancer-health-probes_YYYYMMDD.md
2. articles/compute/create-vm-portal.md → factcheck_create-vm-portal_YYYYMMDD.md
3. articles/identity/configure-mfa.md → factcheck_configure-mfa_YYYYMMDD.md

After all tracks complete, consolidate into factcheck_batch_YYYYMMDD.md with cross-article patterns.
```

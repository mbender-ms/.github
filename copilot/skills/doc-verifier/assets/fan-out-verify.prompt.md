---
mode: agent
description: "Deep fact-check a single article using parallel subagents. Phase 1: extract claims and group by service area. Phase 2: fan out one subagent per service group. Phase 3: merge findings into a unified report. Designed for thorough, trusted verification."
tools:
  - microsoft-learn-mcp-server/microsoft_docs_search
  - microsoft-learn-mcp-server/microsoft_docs_fetch
  - microsoft-learn-mcp-server/microsoft_code_sample_search
  - read/readFile
  - read/problems
  - search/codebase
  - search/fileSearch
  - search/textSearch
  - search/usages
  - edit/editFiles
  - edit/createFile
  - execute/runInTerminal
  - execute/getTerminalOutput
  - agent/runSubagent
  - todo
---

# Fan-Out Verification

Deep fact-check a single Microsoft documentation article using a **3-phase fan-out/fan-in** architecture. Parallel subagents verify claims grouped by service area, then merge into a unified report.

This workflow trades speed for depth. Every claim gets verified. Runtime may be 10-20 minutes for complex articles — that's expected and acceptable.

## Setup

Load [_shared/source-hierarchy.md](../_shared/source-hierarchy.md) for the complete tiered source authority reference.
Load [assets/_runtime-adapter.md](./_runtime-adapter.md) for fan-out dispatch behavior by runtime.
Load [assets/_subagent-contract.md](./_subagent-contract.md) for shared subagent schema, instruction template, and merge rules.

When scoping to a product area, consult [sources/routing-index.md](../../sources/routing-index.md) to identify the matching category YAML for Tier 2 repo lookups.

## Phase 1 — Extract and group (orchestrator)

The orchestrator reads the article and builds a **claim manifest** — a structured inventory that subagents consume.

### 1a. Read the article

Read the current file. Note:
- `ms.service` / `ms.prod` from frontmatter
- `ms.topic` (determines what kinds of claims to expect)
- All `[!INCLUDE ...]` references — resolve and read include files

### 1b. Extract every verifiable claim

For each claim, record:
- **claim_id**: Sequential number (C001, C002, ...)
- **line**: Approximate line number(s)
- **text**: The exact assertion
- **type**: One of: `feature`, `config`, `api`, `cli`, `code`, `limit`, `pricing`, `status`, `link`
- **service_area**: The Azure/M365/etc. service this claim belongs to
- **context**: Product version or SKU scope if stated

### 1c. Group by service area

Partition claims into groups. Each group becomes one subagent task.

Example manifest output:

```markdown
## Claim manifest

### Group: Azure Load Balancer (8 claims)
- C001 [line 23] [feature] "Health probes support HTTP, HTTPS, and TCP protocols"
- C002 [line 31] [config] "Default probe interval is 15 seconds"
- C003 [line 45] [api] "az network lb probe create --protocol Https"
...

### Group: Azure Virtual Network (3 claims)
- C009 [line 78] [feature] "VNet peering supports cross-region connectivity"
...

### Group: General / Cross-service (2 claims)
- C012 [line 102] [link] "https://learn.microsoft.com/azure/..."
...
```

### 1d. Resolve INCLUDE files

For each `[!INCLUDE ...]`:
- Read the referenced file
- Extract claims from include content
- Tag claims with the source include file path
- Add to the appropriate service-area group

## Phase 2 — Verify in parallel (subagents)

Spawn one `runSubagent` per service-area group. Each subagent receives:
1. Its claim subset from the manifest
2. The service area name
3. Instructions to verify and report back

### Subagent instructions

Each subagent runs independently with its own context window and must follow the standard template from [assets/_subagent-contract.md](./_subagent-contract.md).

Required parameters for each subagent call:
- `service_area`: claim group name
- `claims`: claim subset for that group
- `search_strategy`: `batched`
- `max_fetch_calls`: `3`
- `token_budget`: `2000`

### Subagent search strategy

Each subagent follows this pattern:
1. **Batch related claims** — search once per service area, not once per claim
2. **`microsoft_docs_search`** — 2-3 queries per service area covering the key topics
3. **`microsoft_docs_fetch`** — fetch only the top 2-3 pages identified by search
4. **`microsoft_code_sample_search`** — only if the group contains `code` or `cli` type claims
5. **Cross-check** — if search returns contradictory results, fetch the higher-tier source

### Token management

- Each subagent starts with a clean context window (no article content, just its claims)
- `maxTokenBudget=2000` on all `microsoft_docs_fetch` calls
- Maximum 3 fetch calls per subagent
- If a claim can't be verified in 3 searches + 3 fetches, classify as ❓ and move on

## Phase 3 — Merge and report (orchestrator)

Collect all subagent results and produce the final output.

### 3a. Deduplicate and resolve conflicts

- If two subagents found the same source for different claims, note the shared reference
- If subagents disagree (unlikely but possible), resolve by tier: higher tier wins
- If a claim was classified ❓ by one subagent but verified by another (cross-service claims), use the verified result

### 3b. Apply corrections

For any claim with status ⚠️, ❌, or 🕐:
- Edit the article directly with the corrected information
- Preserve tone, style, and formatting
- Update `ms.date` to today's date
- For INCLUDE-sourced claims: edit the include file, note which file was edited

Do NOT remove ❓ claims. Flag them in the report.

### 3c. Generate report

Create `factcheck_[articlename]_YYYYMMDD.md`:

```markdown
# Fact-Check Report: [Article Title]

**File**: [path]
**Date**: YYYY-MM-DD
**Service area**: [primary from ms.service]
**Total claims**: [count]
**Subagents dispatched**: [count by service group]

## Executive summary

[2-3 sentences: overall health, biggest issues, confidence level]

## Findings at a glance

| Status | Count | % |
|--------|-------|---|
| ✅ Accurate | N | X% |
| ⚠️ Partially accurate | N | X% |
| ❌ Inaccurate | N | X% |
| 🕐 Outdated | N | X% |
| ❓ Unverifiable | N | X% |
| 🔗 Broken link | N | X% |

## Critical findings (action required)

### [C00N] ❌ [brief description]
- **Line(s)**: [N]
- **Original**: "[quoted text]"
- **Corrected**: "[fix applied]"
- **Evidence**: [What the official source says]
- **Source**: [Title](URL) — Tier [N]

## Advisory findings (recommended)

### [C00N] ⚠️ [brief description]
...

## Unverifiable claims (flagged for review)

### [C00N] ❓ [brief description]
- **Line(s)**: [N]
- **Text**: "[quoted text]"
- **Search attempted**: [queries tried]

## Include file edits

| Include file | Claims affected | Edits made |
|-------------|-----------------|------------|

## Sources consulted

| # | Title | URL | Tier | Claims verified |
|---|-------|-----|------|-----------------|

## Subagent execution log

| Service group | Claims | Search calls | Fetch calls | Duration |
|--------------|--------|-------------|-------------|----------|
```

### 3d. Present results

Summarize in chat:
- Total claims verified
- Issues by severity
- Edits made (count)
- Remind user to review via Source Control or `git diff`
- Ask if they want to commit changes

## Quality checklist

See [_shared/quality-checklist.md](../_shared/quality-checklist.md). Additionally:
- [ ] Every claim in the manifest accounted for in the final report
- [ ] No subagent exceeded 3 fetch calls
- [ ] Tier conflicts resolved (higher tier wins)
- [ ] INCLUDE files checked and edited if needed
- [ ] `ms.date` updated if any edits were made
- [ ] Unverifiable claims flagged, not removed

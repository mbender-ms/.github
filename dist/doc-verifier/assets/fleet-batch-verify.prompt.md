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

> **Runtime**:
> - Copilot CLI: `/fleet` dispatch (preferred)
> - Copilot Chat: `runSubagent` dispatch (equivalent output)
> - Fallback: sequential processing if parallel tools are unavailable

## Setup

Load [source-hierarchy.md](../references/source-hierarchy.md) for the source authority reference. Higher tier always wins.
Load [assets/_runtime-adapter.md](./_runtime-adapter.md) for runtime dispatch rules and output guarantees.
Load [assets/_subagent-contract.md](./_subagent-contract.md) for subagent I/O schema and call-budget defaults.

## Report output (`--report`)

By default this workflow is **chat-only** — it presents per-article findings and the consolidated cross-article reconciliation in chat without writing files. Write markdown report files only when the user asks for one:

- If the user passes `--report <dir>`, write per-article reports and the consolidated batch report under that directory.
- If the user requests reports but gives **no path**, ask for the directory before completing — do not guess a default location.
- If neither is present, hold all report structures in memory and present them in chat only.

The cross-article reconciliation in Step 2 always runs regardless of report output — it operates on the in-memory track results, not on written files.

## Step 0 — Scope and decompose

Ask the user (skip if already clear):
1. **File scope** — Which articles? (folder path, glob, or explicit list)
2. **Depth** — Quick (search-only) or thorough (search + fetch + code samples)?
3. **Output** — Corrections, reports, or both? Reports are written only when requested via `--report <dir>` (see **Report output**); otherwise findings are chat-only.

Discover files:
- If folder: list all `.md` files recursively
- If glob: expand the pattern
- If file list: validate each path exists

**Decomposition rule**: Map every article to one concrete output artifact. The orchestrator should see a structure like:

```
Track 1: articles/networking/load-balancer-health-probes.md → factcheck_load-balancer-health-probes_YYYYMMDD.md
Track 2: articles/compute/create-vm-portal.md → factcheck_create-vm-portal_YYYYMMDD.md
Track 3: articles/identity/configure-mfa.md → factcheck_configure-mfa_YYYYMMDD.md
```

Each unit is independent — no shared state, no dependencies between tracks.

Dispatch according to runtime:
- CLI fleet mode: one `/fleet` track per article
- Chat mode: one `runSubagent` call per article
- Fallback mode: process articles sequentially but keep report naming identical

## Step 0b — Build the shared claim ledger (cross-article correlation)

Before fanning out, build a **batch-wide topic-key index** so the same fact stated in different articles can be reconciled afterward. This is what catches cross-article inconsistencies (e.g., one article says the outbound idle timeout is 100 minutes while another says 120) — isolated tracks cannot see each other, so the correlation must be established here.

1. Run the claim-manifest extraction (see [claim-manifest.prompt.md](./claim-manifest.prompt.md)) across **all** articles in the batch, not one at a time.
2. Coin a `topic_key` for every high-risk claim (`config`, `limit`, `pricing`, `status`, `prereq`, and any `feature` claim stating a number, version, date, or lifecycle state). Reuse the identical `topic_key` string whenever the same fact appears in more than one file. Maintain one shared index for the whole batch.
3. Record which `topic_key`s appear in **two or more** files — these are the reconciliation candidates. Carry the full claim objects (including `topic_key`) into each track's input per the [subagent contract](./_subagent-contract.md).

Do not skip this step for multi-file batches; without a shared `topic_key` index, Step 2 reconciliation has nothing to group on.

## Step 1 — Per-article verification (runs in parallel)

Each parallel unit receives ONE article and executes these steps using the shared subagent contract:

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

### 1d. Produce the per-article finding set

Assemble each article's findings using the structure below. Write it to `<report-dir>/factcheck_[articlename]_YYYYMMDD.md` only when `--report` was requested (see **Report output**); otherwise keep it in memory for the consolidated chat presentation.

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
- **Bump `ms.date` only when at least one claim in the file was fetch-verified** (`verification_method: fetch` or `code-sample`). A search-only or "looked accurate" pass does NOT justify a date bump — bumping the date on unverified content manufactures false confidence. If nothing was fetch-verified, leave `ms.date` unchanged and note the file as reviewed-not-reverified.
- In the per-article report, list which fetch-verified claims back the date bump.
- Do NOT remove unverifiable claims

## Step 2 — Consolidate (after all tracks complete)

Once all parallel tracks finish, the orchestrator:

1. Read all per-article reports
2. **Reconcile shared claims across tracks** — apply the cross-track reconciliation rules in [_subagent-contract.md](./_subagent-contract.md). Group every returned result by `topic_key`, drop `—` and singletons, and compare `verified_value` within each multi-file group:
   - Values agree and at least one is fetch-verified → consistent; propagate the authoritative value to any track that marked the claim `unverifiable`.
   - Values disagree → **conflict**: the highest-tier source wins, and every file asserting a different value is `inaccurate`/`outdated` even if its own track scored it ✅.
   - No value in the group is fetch-verified → mark the group `unverifiable` and flag for a deep pass.
3. Generate the consolidated finding set. Write it to `<report-dir>/factcheck_batch_YYYYMMDD.md` only when `--report` was requested; otherwise present it in chat. It contains:
   - **Cross-article reconciliation table (first)** — every conflicted `topic_key`, the value each file asserts, the authoritative value, and the source:

```markdown
| topic_key | Conflicting values (file → value) | Authoritative value | Source | Files to fix |
|-----------|-----------------------------------|---------------------|--------|--------------|
| loadbalancer-outbound-idle-timeout-max | tcp-reset.md → 100 min; outbound-rules.md → 120 min | 4–120 min | [Outbound rules](URL) — Tier 1 | tcp-reset.md, tcp-idle-timeout.md |
```

   - **Executive summary** — total files, total claims, overall health score
   - **Cross-article patterns** — repeated issues across files (e.g., same deprecated API referenced in 3 articles)
   - **Per-file summary table**:

```markdown
| File | Claims | ✅ | ⚠️ | ❌ | 🕐 | ❓ | 🔗 |
|------|--------|----|-----|----|----|----|----|
```

4. Flag any cross-article inconsistencies (article A says X, article B says Y about the same feature)

## Quality checklist

See [quality-checklist.md](../references/quality-checklist.md). Additionally:
- [ ] Every article processed (none skipped)
- [ ] Shared `topic_key` index built across the whole batch before fan-out
- [ ] Each per-article finding set produced (written to file only if `--report` requested)
- [ ] Consolidated finding set produced (written to file only if `--report` requested)
- [ ] Cross-track reconciliation run; conflicted `topic_key`s listed first
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

## Chat prompt template

When running from Copilot Chat, use this structure:

```
Use @fleet-batch-verify to fact-check the following articles.
Dispatch one runSubagent unit per article and produce matching per-article reports.

Articles:
1. articles/networking/load-balancer-health-probes.md → factcheck_load-balancer-health-probes_YYYYMMDD.md
2. articles/compute/create-vm-portal.md → factcheck_create-vm-portal_YYYYMMDD.md
3. articles/identity/configure-mfa.md → factcheck_configure-mfa_YYYYMMDD.md

After all units complete, consolidate into factcheck_batch_YYYYMMDD.md with cross-article patterns.
```

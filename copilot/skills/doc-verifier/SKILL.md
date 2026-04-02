---
name: doc-verifier
description: >-
  Verify technical accuracy of Microsoft documentation across all product areas
  (Azure, M365, Security, Power Platform, Dynamics 365, Windows, DevTools).
  14 workflows: quick fix, full report, internal sources, freshness review,
  deep agent check, batch report, PR review, research, single article,
  customer incident analysis, fleet batch, fan-out verify, claim manifest,
  and incremental verify. Tiered source hierarchy prioritizing learn.microsoft.com.
argument-hint: "Describe what to verify — e.g., 'fact-check this article', 'verify PR #123', 'research Azure Front Door caching', 'CIA analysis for App Service'"
user-invocable: true
---

# Documentation Verifier

Verify technical accuracy of Microsoft documentation across **any product area** using a structured source hierarchy and reproducible workflows.

## Choose your workflow

| # | Workflow | When to use | Output | Prompt asset |
|---|---------|-------------|--------|--------------|
| 1 | **Quick In-Place** | Fast fix; edit file directly, resolve INCLUDEs | Edits + chat refs | `fact-check-and-edit.prompt.md` |
| 2 | **Single Article** | Full single-file check with product-area scoping | Edits + chat summary | `single-article-check.prompt.md` |
| 3 | **Full Report** | Comprehensive audit with saved report artifact | Edits + `factcheck_*.md` | `complete-fact-check.prompt.md` |
| 4 | **Internal + Public** | Cross-reference internal MS resources | Edits (public) + confidential report | `complete-fact-checker-internal.prompt.md` |
| 5 | **Freshness Review** | Staleness + accuracy in one pass | Edits + chat summary | `complete-freshness-review.prompt.md` |
| 6 | **Deep Agent** | Per-fact evidence for critical content | WHAT/WHY/EVIDENCE output | `microsoft-fact-checker-slim.agent.md` |
| 7 | **Batch Report** | Verify folder or file set | `factcheck_*.md` report | `batch-report.prompt.md` |
| 8 | **PR Review** | Fact-check all changed files in a PR | `factcheck_PR*.md` report | `pr-review.prompt.md` |
| 9 | **Research** | Investigate a topic with citations, no edits | Research report | `microsoft-researcher.prompt.md` |
| 10 | **CIA Analysis** | Customer incident patterns for a service area | Incident analysis report | `microsoft-fact-checker-cia.agent.md` |
| 11 | **Fleet Batch** | Verify 2-10 articles in parallel via /fleet | Per-article reports + consolidated | `fleet-batch-verify.prompt.md` |
| 12 | **Fan-Out Verify** | Deep single-article check with parallel subagents per service area | Edits + detailed report | `fan-out-verify.prompt.md` |
| 13 | **Claim Manifest** | Pre-stage: extract and catalog claims without verification | Claim inventory file | `claim-manifest.prompt.md` |
| 14 | **Incremental Verify** | Cache-based incremental checking; skip unchanged claims | Edits + incremental report | `incremental-verify.prompt.md` |

### Decision guide

- **"Just fix this article"** → Workflow 1
- **"Fact-check this Defender article"** → Workflow 2 (product-area scoped)
- **"Audit and give me a report"** → Workflow 3
- **"Check against internal docs too"** → Workflow 4
- **"Is this article still current?"** → Workflow 5
- **"Deep verification of every claim"** → Workflow 6
- **"Fact-check these files / this folder"** → Workflow 7
- **"Fact-check PR #12345"** → Workflow 8
- **"Research topic X with sources"** → Workflow 9
- **"Analyze customer incidents for Service Y"** → Workflow 10
- **"Fact-check these 5 articles"** → Workflow 11 (Fleet Batch) via `/fleet`
- **"Deep verify every claim in this article"** → Workflow 12 (Fan-Out Verify)
- **"How many claims does this article have?"** → Workflow 13 (Claim Manifest)
- **"Pre-search claims before verification"** → Run `batch-presearch.sh` first, then Workflow 11 or 12
- **"Re-check, skip unchanged claims"** → Workflow 14 (Incremental Verify)

## Step 0 — Scope (all workflows)

Before verifying, determine the product area. Ask if not obvious:

1. **Product area**: Azure, M365, Security, Power Platform, Dynamics 365, Windows, DevTools
2. **Service/feature**: e.g., Defender for Endpoint, Azure Firewall, Intune
3. **Scope**: Single file, folder, PR, or topic
4. **Output**: In-place edits, report, chat, or both
5. **Depth**: Quick check or thorough

Use answers to select search domains and load the matching sources catalog YAML from `copilot/skills/sources/` (e.g., `azure-networking.yml` for Azure Networking). This gives you the full list of relevant GitHub repos for Tier 2 source verification.

### Product area search domains

| Area | Search paths | Key terms |
|------|-------------|-----------|
| Azure | `/azure/`, `/azure/architecture/` | Azure, ARM, Bicep, subscription |
| M365 | `/microsoft-365/`, `/office/` | Exchange, SharePoint, Teams |
| Security | `/security/`, `/defender/` | Defender, Sentinel, Entra, Purview |
| Power Platform | `/power-platform/`, `/power-apps/` | Power Apps, Dataverse, connectors |
| Dynamics 365 | `/dynamics365/` | D365, Business Central, Finance |
| Windows | `/windows/`, `/windows-server/` | Windows 11, Group Policy |
| DevTools | `/visualstudio/`, `/dotnet/` | Visual Studio, .NET, NuGet |

## Source authority hierarchy

Always prefer the highest available tier. See [_shared/source-hierarchy.md](../_shared/source-hierarchy.md) for the complete reference with repository catalog integration.

| Tier | Source | Use for |
|------|--------|---------|
| **1** | learn.microsoft.com, azure.microsoft.com | Product docs, features, limits, pricing |
| **2** | TechCommunity, DevBlogs, GitHub repos | Announcements, API specs, code samples |
| **3** | developer.microsoft.com, code.visualstudio.com | Platform docs, Graph API |
| **4** | MS Q&A, Stack Overflow (verified MS employees only) | Edge cases, engineer Q&A |
| **5–7** | Internal docs, code, metadata (Workflows 4 & 9 only) | Implementation truth |

> Higher tier always wins. Internal sources never appear in public docs.

## Accuracy classifications

| Icon | Status | Action |
|------|--------|--------|
| ✅ | Accurate | No change |
| ⚠️ | Partially accurate | Edit with correction |
| ❌ | Inaccurate | Edit + cite source |
| 🕐 | Outdated | Update + cite source |
| ❓ | Unverifiable | Flag — do not remove |
| 🔗 | Broken link | Fix or flag |

## Quality checklist

- [ ] Every claim verified against at least one fetched source
- [ ] Highest-tier source used per claim
- [ ] URLs from allowed Microsoft domains only
- [ ] `ms.date` updated if edits made
- [ ] Code examples validated
- [ ] Deprecation/retirement status checked
- [ ] Unverifiable claims flagged, not removed
- [ ] Internal findings isolated (if applicable)

See [references/workflows.md](references/workflows.md) for detailed per-workflow procedures.

## Prompt assets

| File | Workflow |
|------|----------|
| `assets/fact-check-and-edit.prompt.md` | 1 — Quick In-Place |
| `assets/single-article-check.prompt.md` | 2 — Single Article |
| `assets/complete-fact-check.prompt.md` | 3 — Full Report |
| `assets/complete-fact-checker-internal.prompt.md` | 4 — Internal + Public |
| `assets/complete-freshness-review.prompt.md` | 5 — Freshness Review |
| `assets/microsoft-fact-checker.agent.md` | 6 — Deep Agent |
| `assets/batch-report.prompt.md` | 7 — Batch Report |
| `assets/pr-review.prompt.md` | 8 — PR Review |
| `assets/microsoft-researcher.prompt.md` | 9 — Research |
| `assets/CIA-Analysis.prompt.md` | 10 — CIA Analysis |
| `assets/fleet-batch-verify.prompt.md` | 11 — Fleet Batch |
| `assets/fan-out-verify.prompt.md` | 12 — Fan-Out Verify |
| `assets/claim-manifest.prompt.md` | 13 — Claim Manifest |
| `assets/incremental-verify.prompt.md` | 14 — Incremental Verify |
| `scripts/batch-presearch.sh` | Pre-processing helper |

## Workflow comparison (parallel)

| Feature | W11 Fleet | W12 Fan-Out | W13 Manifest | W14 Incremental |
|---------|-----------|-------------|-------------|------------------|
| Edits file | Optional | ✅ | ❌ | ✅ |
| Report file | ✅ (per-article + consolidated) | ✅ | ✅ (manifest only) | ✅ |
| Parallel execution | ✅ (one track per article) | ✅ (one subagent per service group) | ❌ (single pass) | Wraps W2/W11/W12 |
| MCP calls | Yes (per track) | Yes (per subagent, capped) | None | Only for changed/stale claims |
| INCLUDE resolution | ✅ | ✅ | ✅ | ✅ |
| Token management | maxTokenBudget=2000 | maxTokenBudget=2000, max 3 fetches/subagent | N/A | Inherited from wrapped workflow |
| Best runtime | Copilot CLI /fleet | VS Code agent mode or Copilot CLI | Any | Any |

## Pre-processing with batch-presearch.sh

For large batch runs, front-load search latency:

```bash
# 1. Generate manifests
# (run claim-manifest on each article)

# 2. Pre-search against Learn
./scripts/batch-presearch.sh claims_load-balancer_20260402.md ./cache/

# 3. Run fleet verification
# Agents read cache files for initial search hits,
# use docs_fetch only for pages needing full content
```

## Token budget controls

All parallel workflows enforce token limits:
- `microsoft_docs_fetch` calls use `maxTokenBudget=2000`
- Fan-Out subagents: max 3 fetch calls each
- Fleet tracks: independent context windows (no shared state)
- Incremental: only re-verifies changed or stale claims, reducing total MCP calls by 60-80%

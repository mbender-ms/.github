---
name: doc-verifier
description: >-
  Verify technical accuracy of Microsoft documentation across all product areas
  (Azure, M365, Security, Power Platform, Dynamics 365, Windows, DevTools).
  Four workflows: single article, PR review, research, and fleet batch.
  Tiered source hierarchy prioritizing learn.microsoft.com. Reports are opt-in
  via the --report flag.
argument-hint: "Describe what to verify — e.g., 'fact-check this article', 'verify PR #123', 'research Azure Front Door caching', 'fact-check these 5 articles'"
user-invocable: true
---

# Documentation Verifier

Verify technical accuracy of Microsoft documentation across **any product area** using a structured source hierarchy and reproducible workflows.

## Choose your workflow

| # | Workflow | When to use | Output | Prompt asset |
|---|---------|-------------|--------|--------------|
| 1 | **Single Article** | Full single-file check with product-area scoping | Edits + chat summary | `single-article-check.prompt.md` |
| 2 | **PR Review** | Fact-check all changed files in a PR | Chat summary | `pr-review.prompt.md` |
| 3 | **Research** | Investigate a topic with citations, no edits | Chat findings | `microsoft-researcher.prompt.md` |
| 4 | **Fleet Batch** | Verify multiple articles in parallel (CLI `/fleet` or Chat `runSubagent`) | Chat consolidated findings | `fleet-batch-verify.prompt.md` |

All four workflows are **chat-only by default**. To save a markdown report, pass `--report <path>` (see **Report output** below). The Fleet Batch workflow uses the Claim Manifest extraction (`assets/claim-manifest.prompt.md`) internally to build its cross-article topic-key index — it is a supporting step, not a standalone workflow.

### Report output (`--report`)

Every workflow defaults to presenting findings in chat without writing files. Write a markdown report only when the user asks:

- If the user passes `--report <path>`, write the report to that exact path (a directory for Fleet Batch, a file for the others).
- If the user requests a report but gives **no path**, ask for the path before completing — do not guess a default location.
- If no report is requested, present findings in chat only.

### Decision guide

- **"Fact-check this article"** / **"Fact-check this Defender article"** → Workflow 1 (product-area scoped)
- **"Fact-check PR #12345"** → Workflow 2
- **"Research topic X with sources"** → Workflow 3
- **"Fact-check these 5 articles" / "this folder"** → Workflow 4 (Fleet Batch) via `/fleet` or Chat `runSubagent`
- **"Fact-check the top/most-viewed articles for `<service>`"** → run `/pageviews-query` first, then feed its JSON handoff into Workflow 4 (Fleet Batch), highest-traffic first (see **Page views entry point** below)
- **"Save the findings to a report"** → add `--report <path>` to any of the above

### Page views entry point (traffic-prioritized fact-checking)

When the request is to fact-check by **traffic** rather than by a specific file — e.g. "fact-check the top 10 articles for `azure-load-balancer` in April 2026", "verify the most-viewed App Service docs", or "check the highest-traffic articles for `<service>`" — use the `pageviews-query` skill as the producer, then fact-check its output:

1. **Get the ranked set** — run `/pageviews-query <service> <month> [count]` (count defaults to 10). It validates the `MSService` value, queries the Content Engagement Power BI model, and emits a JSON handoff block.
2. **Consume the JSON contract** — read the fenced ` ```json ` block. Use `articles[].localPath` as the file to verify (fall back to `liveUrl` when `localPath` is `null`), and keep the array order — `rank`/`pageViews` is your priority order.
3. **Route to a verification workflow** — feed the resolved paths into **Workflow 4 (Fleet Batch)**. Verify highest-traffic articles first so the most-read content is corrected soonest.
4. **Skip null paths** — if `localPath` is `null` (unresolved/hub page), don't guess; note it as not-verified and continue.

This keeps the two skills decoupled: `pageviews-query` owns traffic ranking, doc-verifier owns accuracy. The JSON block is the only contract between them.

### Threshold Matrix (Workflow and Tier Routing)

Use this matrix to select depth and workflow consistently.

| Decision axis | Threshold | Route | Tier |
|---|---|---|---|
| Single article claim volume | 1-15 claims and low ambiguity | Single Article | Tier 2 |
| Single article claim volume | 16-40 claims or mixed ambiguity | Single Article with Tier 2 extraction, Tier 1 final verdicts | Tier 2 then Tier 1 |
| Single article claim volume | More than 40 claims, cross-service content, or safety-critical scope | Fleet Batch (single-article track, Tier 1-heavy) | Tier 1-heavy |
| Batch size | Multiple articles | Fleet Batch (one track per article) | Tier 2 orchestration, Tier 1 for contested claims |
| PR changed files | 1-5 files, mostly editorial or metadata changes | PR Review standard pass | Tier 2 or Tier 3 |
| PR changed files | More than 5 files or major technical changes | PR Review plus deep pass on high-risk files | Tier 1 on flagged files |

### Escalation Triggers (Accuracy-First)

Escalate a claim or file to Tier 1 when any trigger matches:

- Tier conflict: Tier 1 and Tier 2 sources disagree.
- Unverifiable rate: more than 10% of claims in an article are unverifiable.
- Safety impact: claims affect RBAC, authentication, encryption, or production availability.
- Confidence drop: reviewer confidence is below high after Tier 2 analysis.
- Policy or retirement risk: deprecation or retirement timelines are present.

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
| **5–7** | Internal docs, code, metadata (Research workflow only) | Implementation truth |

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

## High-risk claim classes (verify deepest here)

Defects concentrate in a few claim types. Treat these as **high-risk** and spend fetch budget on them first; for these, a search snippet is never sufficient to mark a claim accurate — confirm against a fetched Tier-1/2 page.

| Class | Examples | Why high-risk |
|-------|---------|---------------|
| Numeric limit / quota | "4 to 120 minutes", "max 1000 rules" | Silently drift; often conflict across articles |
| Config default | "default interval is 15 seconds" | Changes with releases |
| Lifecycle / status | Basic SKU "(retired)", "(preview)" → GA | Time-sensitive; high reader impact |
| Version / prereq | "requires CLI 2.50+" | Breaks copy-paste workflows |
| Pricing / tier / SKU | tier names, SKU availability | Customer-facing accuracy |
| Defined term / acronym | "User Datagram Protocol (UDP)" | Easy to mis-expand, erodes trust |

All other claims (prose capability statements, links, code/CLI syntax) are **low-risk** and may be verified search-first, fetching only on an apparent discrepancy. See [_subagent-contract.md](assets/_subagent-contract.md) for the accurate-verdict gate and per-class fetch budget.

## Quality checklist

- [ ] Every claim verified against at least one fetched source
- [ ] Highest-tier source used per claim
- [ ] High-risk claims (limits, defaults, lifecycle, versions, pricing, terms) confirmed by fetch, not snippet
- [ ] URLs from allowed Microsoft domains only
- [ ] `ms.date` bumped only when at least one claim was fetch-verified — never on a search-only or "looks fine" pass
- [ ] Code examples validated
- [ ] Deprecation/retirement status checked
- [ ] Unverifiable claims flagged, not removed
- [ ] Cross-article conflicts reconciled by `topic_key` (batch/fleet runs)
- [ ] Internal findings isolated (if applicable)

See [references/workflows.md](references/workflows.md) for detailed per-workflow procedures.

## Prompt assets

| File | Workflow |
|------|----------|
| `assets/single-article-check.prompt.md` | 1 — Single Article |
| `assets/pr-review.prompt.md` | 2 — PR Review |
| `assets/microsoft-researcher.prompt.md` | 3 — Research |
| `assets/fleet-batch-verify.prompt.md` | 4 — Fleet Batch |
| `assets/claim-manifest.prompt.md` | Supporting — claim extraction used by Fleet Batch |
| `assets/_runtime-adapter.md` | Shared runtime dispatch rules |
| `assets/_subagent-contract.md` | Shared subagent I/O contract |
| `scripts/batch-presearch.sh` | Pre-processing helper |

## Workflow comparison

| Feature | Single Article | PR Review | Research | Fleet Batch |
|---------|----------------|-----------|----------|-------------|
| Edits file | ✅ | Optional | ❌ | Optional |
| Report file | Opt-in (`--report`) | Opt-in (`--report`) | Opt-in (`--report`) | Opt-in (`--report`) |
| Parallel execution | ❌ | Optional (per service group) | ❌ | ✅ (one track per article) |
| MCP calls | Yes | Yes | Yes | Yes (per track) |
| INCLUDE resolution | ✅ | ✅ | N/A | ✅ |
| Token management | maxTokenBudget=2000 | maxTokenBudget=2000 | maxTokenBudget=2000 | maxTokenBudget=2000 |
| Best runtime | VS Code agent mode | VS Code agent mode | Any | Copilot CLI /fleet (preferred), Chat runSubagent equivalent |

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

All workflows enforce token limits:
- `microsoft_docs_fetch` calls use `maxTokenBudget=2000`
- Fleet tracks: independent context windows (no shared state)
- Search first, fetch selectively — fetch only high-value pages per the source hierarchy

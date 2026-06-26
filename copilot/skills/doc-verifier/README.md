# Documentation Verifier

> **Version:** 1.1.0 · **Last updated:** 2026-06-26

A VS Code Copilot skill that fact-checks Microsoft documentation against official sources across **all product areas** — Azure, Microsoft 365, Microsoft Security, Power Platform, Dynamics 365, Windows, Developer Tools, and more.

Four primary workflows — single-article check, PR review, research, and fleet batch (parallel multi-article) — plus a fifth gated **Live Validation** escalation that empirically settles contested numeric/behavioral claims. A tiered source hierarchy prioritizes learn.microsoft.com, with a dedicated **Tier 1-C API Contract** tier (ARM/Bicep templates, CLI/PowerShell parameter reference, REST specs) that outranks prose for numeric, default, and enum claims. Reports are opt-in via the `--report` flag — every workflow is chat-only by default.

---

## Prerequisites

### Required

| Requirement | How to verify |
|-------------|---------------|
| **VS Code** (1.100+) | `code --version` |
| **GitHub Copilot** (agent mode) | Copilot Chat → mode dropdown → "Agent" available |
| **Microsoft Learn MCP Server** | Check MCP config for `microsoft-learn-mcp-server` entry |

### Optional

| Requirement | Needed for |
|-------------|------------|
| **GitHub MCP Server** | PR Review workflow |
| **GitHub CLI** (`gh`) | PR Review workflow |
| **Copilot CLI** with `/fleet` | Fleet Batch workflow |
| **@microsoft/learn-cli** (`npm i -g @microsoft/learn-cli`) | `batch-presearch.sh` helper |

---

## Installation

Copy the `doc-verifier/` folder to your Copilot skills directory:

**Windows:**
```powershell
Copy-Item -Recurse .\doc-verifier\ "$env:USERPROFILE\.copilot\skills\doc-verifier"
```

**macOS / Linux:**
```bash
cp -r ./doc-verifier/ ~/.copilot/skills/doc-verifier/
```

Restart VS Code. The skill is discovered automatically on startup.

### Folder structure

```
doc-verifier/
├── SKILL.md                                    # Skill definition (Copilot reads this)
├── README.md                                   # This file
├── assets/
│   ├── single-article-check.prompt.md           # Single Article workflow
│   ├── pr-review.prompt.md                      # PR Review workflow
│   ├── microsoft-researcher.prompt.md           # Research workflow
│   ├── fleet-batch-verify.prompt.md             # Fleet Batch workflow
│   ├── live-validation.prompt.md                # Live Validation (gated escalation)
│   ├── claim-manifest.prompt.md                 # Supporting: claim extraction for Fleet Batch
│   ├── _runtime-adapter.md                      # Shared runtime dispatch rules
│   └── _subagent-contract.md                    # Shared subagent I/O contract
├── scripts/
│   ├── batch-presearch.sh                       # Pre-search helper for large batches
│   └── contract-lookup.sh                       # API Contract (Tier 1-C) cache helper
├── TEST-PROTOCOLS.md                           # Validation procedures for the 4 workflows
├── _shared/                                     # Vendored shared references (self-contained)
│   ├── source-hierarchy.md                      # Canonical tiered source authority reference
│   ├── quality-checklist.md                     # Shared quality checklist
│   ├── formatting-rules.md
│   ├── seo-and-metadata.md
│   └── writing-style.md
├── sources/                                     # Vendored repository catalog (self-contained)
│   ├── routing-index.md                         # Product-area → category YAML routing
│   ├── categories-index.yml
│   └── *.yml                                     # Per-category repo catalogs (azure-networking.yml, ...)
└── references/
    ├── source-hierarchy.md                      # Local pointer → _shared/source-hierarchy.md
    ├── source-guide.md                          # Educational guide to sources
    └── workflows.md                             # Detailed per-workflow procedures
```

### Bundled dependencies (self-contained)

`_shared/` and `sources/` are vendored into this folder so the skill is fully portable — copying just `doc-verifier/` to your skills directory brings everything it needs.

| Dependency | Purpose |
|-----------|----------|
| `_shared/source-hierarchy.md` | Canonical tiered source authority reference |
| `_shared/quality-checklist.md` | Shared quality checklist |
| `sources/` | Repository catalog — Step 0 loads category YAML for Tier 2 verification |

---

## Usage

Open **GitHub Copilot Chat** in agent mode and describe what you want verified. The skill automatically selects the right workflow.

### Trigger examples

| You say... | Workflow |
|-----------|----------|
| "Fact-check this article" | Single Article |
| "Fact-check PR #12345" | PR Review |
| "Research Azure Front Door caching" | Research |
| "Fact-check these 5 articles" / "this folder" | Fleet Batch |
| "Settle this contested limit empirically" | Live Validation (gated) |
| "...and save the findings to a report" | add `--report <path>` to any workflow |

---

## Threshold Matrix (Workflow and Tier Routing)

Use these thresholds to right-size verification depth while preserving accuracy.

| Decision axis | Threshold | Route | Tier |
|---|---|---|---|
| Single article claim volume | 1-15 claims and low ambiguity | Single Article | Tier 2 |
| Single article claim volume | 16-40 claims or mixed ambiguity | Single Article (Tier 2 gather, Tier 1 adjudicate) | Tier 2 then Tier 1 |
| Single article claim volume | More than 40 claims, cross-service scope, or safety-critical content | Fleet Batch (single-article track) | Tier 1-heavy |
| Batch size | Multiple articles | Fleet Batch (one track per article) | Tier 2 orchestration, Tier 1 on contested claims |
| PR scope | 1-5 documentation files, mostly editorial or metadata changes | PR Review standard pass | Tier 2 or Tier 3 |
| PR scope | More than 5 files or major technical changes | PR Review plus deep pass for high-risk files | Tier 1 on flagged files |
| Claim class | limit / quota / config-default / enum | Require Tier 1-C contract confirmation; if contested, route to Live Validation | Tier 1-C |

### Escalation Triggers (Accuracy-First)

Escalate a claim or file to Tier 1 when any trigger matches:

- Tier conflict: Tier 1 and Tier 2 sources disagree.
- Unverifiable rate: more than 10% of claims in one article are unverifiable.
- Safety impact: claims affect RBAC, authentication, encryption, or production availability.
- Confidence drop: reviewer confidence is below high after Tier 2 analysis.
- Policy or retirement risk: deprecation or retirement timelines are present.
- Contract conflict: a Contract source (Tier 1-C) disagrees with Tier-1 prose, OR two prose sources conflict and the contract is silent → escalate to Live Validation.

---

## API contract verification (Tier 1-C)

For **numeric limit/quota, configuration-default, and enum/allowed-value** claims, prose pages alone are not authoritative. The skill confirms these against a dedicated **Tier 1-C API Contract** tier and prefers it over prose when they disagree:

| Source | Content type |
|--------|-------------|
| `learn.microsoft.com/azure/templates/*` | ARM/Bicep/Terraform resource schema — property min/max, defaults, enums |
| `learn.microsoft.com/cli/azure/*` | Azure CLI parameter reference and `--help` (accepted ranges, defaults) |
| `learn.microsoft.com/powershell/module/*` | Az PowerShell cmdlet parameter reference |
| `github.com/Azure/azure-rest-api-specs` | Swagger — authoritative property constraints |

When a Contract source pins the bound, it wins over prose (the prose is the defect). When the contract is **silent** on a bound and prose pages disagree, the claim is marked **⚖️ Contested** rather than guessed — and can be routed to **Live Validation** for empirical confirmation. The `scripts/contract-lookup.sh` helper caches the templates schema page and CLI `--help` once so every fleet track reuses one lookup.

---

## Live Validation (gated escalation)

When a claim is **⚖️ Contested** or a contract conflict fires, the **Live Validation** workflow can settle it empirically — always gated and safe:

- **Tier 4a — read-only introspection (default):** `az <cmd> --help`, `Get-Help -Full`, `az rest --method get` against provider metadata. No resources are created or modified.
- **Tier 4b — mutating probe (opt-in only):** generates a boundary-probe script for explicit user approval; never auto-runs, requires a non-production subscription, and always cleans up resources.

Results are recorded as `verification_method: live` and outrank prose during reconciliation.

---

## Parallel verification

The **Fleet Batch** workflow scales verification across multiple articles:

- Runs one independent track per article (Copilot CLI `/fleet` mode, or Chat `runSubagent`)
- Builds a batch-wide `topic_key` index via the **Claim Manifest** supporting step before fan-out, so cross-article conflicts can be reconciled afterward
- For large batches, run `scripts/batch-presearch.sh` first to warm search caches before verification

---

## Supported product areas

| Area | Examples |
|------|---------|
| **Azure** | Firewall, DDoS Protection, App Service, AKS, Cosmos DB |
| **Microsoft 365** | Exchange Online, SharePoint, Teams, OneDrive |
| **Microsoft Security** | Defender for Endpoint/Cloud, Sentinel, Entra ID, Purview, Intune |
| **Power Platform** | Power Apps, Power Automate, Power BI, Dataverse |
| **Dynamics 365** | Business Central, Finance, Supply Chain |
| **Windows** | Windows 11, Windows Server, Group Policy |
| **Developer Tools** | Visual Studio, .NET, Azure DevOps, GitHub Actions |

---

## Accuracy classifications

| Icon | Status | Meaning |
|------|--------|---------|
| ✅ | Accurate | Matches current official documentation |
| ⚠️ | Partially accurate | Needs minor update or added context |
| ❌ | Inaccurate | Contradicts official sources |
| 🕐 | Outdated | Was correct but superseded |
| ❓ | Unverifiable | No authoritative source found (flagged, not removed) |
| 🔗 | Broken link | URL doesn't resolve or anchor is missing |
| ⚖️ | Contested | Prose sources disagree AND the API contract is silent — flagged for Live Validation or product-team confirmation; no value asserted |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skill not recognized | Verify folder at `~/.copilot/skills/doc-verifier/` with `SKILL.md`. Restart VS Code. |
| `microsoft_docs_search` unavailable | Check MCP config for Microsoft Learn MCP Server. Restart VS Code. |
| PR workflow can't load PR | Ensure GitHub MCP Server configured and `gh auth status` shows authenticated. |
| Fleet workflow not parallelizing | Use Copilot CLI `/fleet`; VS Code agent mode may run sequentially. |
| `batch-presearch.sh` fails | Install `@microsoft/learn-cli` and run from a shell with bash support. |
| `contract-lookup.sh` finds no contract | Verify the provider path (e.g. `microsoft.network/loadbalancers`); fetch the templates schema page in-agent via `microsoft_docs_fetch` if the helper can't reach it. |
| Agent doesn't ask scoping questions | Add context: "fact-check this M365 Security article about Defender for Endpoint" |

---

## History

This skill consolidates the earlier `fact-checker`, `microsoft-doc-verifier`, `microsoft-fact-checker`, and `fact-check-batch-subagent` skills into a single unified tool with four focused workflows.

---

## Changelog

### 1.1.0 — 2026-06-26

**Added — API contract verification & gated live validation**

- **Tier 1-C API Contract sources** in the source hierarchy (ARM/Bicep templates, CLI/PowerShell parameter reference, REST API specs). For numeric limit/quota, config-default, and enum claims, a Contract source outranks Tier-1 prose.
- **Contract gate for numeric claims**: numeric/limit/quota/config-default/enum claims now require an agreeing Contract source to be scored `accurate`; prose agreement alone caps at `confidence: medium`.
- **⚖️ Contested classification**: emitted when prose sources disagree and the API contract is silent — no value is guessed. Added to the `status` enum and the fleet classification list.
- **Live Validation workflow (5)**: new gated escalation (`assets/live-validation.prompt.md`) — read-only introspection by default, mutating boundary probes only on explicit opt-in.
- **Subagent contract fields**: `verification_method` extended with `contract|live`; new optional `contract_value` and `contract_source` fields; cross-track reconciliation now prefers `contract`/`live` values over prose.
- **`scripts/contract-lookup.sh`**: caches a provider's templates schema page and CLI `--help` so fleet tracks reuse a single contract lookup.
- Quality checklist and Threshold Matrix updated with contract-confirmation and contested-routing items.

### 1.0.0 — Initial release

- Consolidated the earlier `fact-checker`, `microsoft-doc-verifier`, `microsoft-fact-checker`, and `fact-check-batch-subagent` skills into one tool.
- Four workflows: Single Article, PR Review, Research, Fleet Batch.
- Tiered source hierarchy (Tiers 1–7) prioritizing learn.microsoft.com; opt-in `--report` output; vendored `_shared/` and `sources/` for portability.

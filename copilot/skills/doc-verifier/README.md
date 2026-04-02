# Documentation Verifier

A VS Code Copilot skill that fact-checks Microsoft documentation against official sources across **all product areas** — Azure, Microsoft 365, Microsoft Security, Power Platform, Dynamics 365, Windows, Developer Tools, and more.

14 workflows covering in-place fixes, standalone reports, PR reviews, batch verification, research, freshness analysis, internal source verification, customer incident analysis, and parallel verification patterns.

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
| **GitHub MCP Server** | PR Review workflow (#8) |
| **GitHub CLI** (`gh`) | PR Review workflow (#8) |
| **Copilot CLI** with `/fleet` | Fleet Batch workflow (#11) |
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
├── TEST-PROTOCOLS.md                           # Validation procedures for W11-W14
├── assets/
│   ├── fact-check-and-edit.prompt.md           # W1: Quick In-Place
│   ├── single-article-check.prompt.md          # W2: Single Article
│   ├── complete-fact-check.prompt.md           # W3: Full Report
│   ├── complete-fact-checker-internal.prompt.md # W4: Internal + Public
│   ├── complete-freshness-review.prompt.md     # W5: Freshness Review
│   ├── microsoft-fact-checker.agent.md         # Full agent (all tools)
│   ├── microsoft-fact-checker-slim.agent.md    # W6: Deep Agent (25 tools)
│   ├── batch-report.prompt.md                  # W7: Batch Report
│   ├── pr-review.prompt.md                     # W8: PR Review
│   ├── microsoft-researcher.prompt.md          # W9: Research
│   ├── CIA-Analysis.prompt.md                  # W10: CIA Analysis
│   ├── fleet-batch-verify.prompt.md            # W11: Fleet Batch
│   ├── fan-out-verify.prompt.md                # W12: Fan-Out Verify
│   ├── claim-manifest.prompt.md                # W13: Claim Manifest
│   ├── incremental-verify.prompt.md            # W14: Incremental Verify
│   └── microsoft-fact-checker-cia.agent.md     # W10: CIA Agent (31 tools)
├── scripts/
│   └── batch-presearch.sh                      # Pre-search helper for large batches
└── references/
    ├── source-hierarchy.md                     # Local pointer → _shared/source-hierarchy.md
    ├── source-guide.md                         # Educational guide to sources
    └── workflows.md                            # Detailed per-workflow procedures
```

### Cross-skill dependencies

| Dependency | Purpose |
|-----------|----------|
| `_shared/source-hierarchy.md` | Canonical tiered source authority reference |
| `sources/` | Repository catalog — Step 0 loads category YAML for Tier 2 verification |

---

## Usage

Open **GitHub Copilot Chat** in agent mode and describe what you want verified. The skill automatically selects the right workflow.

### Trigger examples

| You say... | Workflow |
|-----------|----------|
| "Fact-check this article" | #1 Quick In-Place or #2 Single Article |
| "Audit this article and give me a report" | #3 Full Report |
| "Check against internal docs too" | #4 Internal + Public |
| "Is this article still current?" | #5 Freshness Review |
| "Deep verification of every claim" | #6 Deep Agent |
| "Fact-check these files" / "this folder" | #7 Batch Report |
| "Fact-check PR #12345" | #8 PR Review |
| "Research Azure Front Door caching" | #9 Research |
| "Analyze customer incidents for App Service" | #10 CIA Analysis |
| "Fact-check these 5 articles" | #11 Fleet Batch |
| "Deep verify every claim in this article" | #12 Fan-Out Verify |
| "How many claims does this article have?" | #13 Claim Manifest |
| "Re-check and skip unchanged claims" | #14 Incremental Verify |

---

## Parallel verification workflows

These workflows extend the base verifier for scale and repeat checks:

- **#11 Fleet Batch**: Parallel multi-article verification in Copilot CLI `/fleet` mode
- **#12 Fan-Out Verify**: Deep single-article verification using parallel subagents per service area
- **#13 Claim Manifest**: Claim extraction and categorization without verification (pre-stage)
- **#14 Incremental Verify**: Cache-driven re-check that verifies only new, changed, or stale claims

For large batches, run `scripts/batch-presearch.sh` first to warm search caches before verification.

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

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skill not recognized | Verify folder at `~/.copilot/skills/doc-verifier/` with `SKILL.md`. Restart VS Code. |
| `microsoft_docs_search` unavailable | Check MCP config for Microsoft Learn MCP Server. Restart VS Code. |
| PR workflow can't load PR | Ensure GitHub MCP Server configured and `gh auth status` shows authenticated. |
| Fleet workflow not parallelizing | Use Copilot CLI `/fleet`; VS Code agent mode may run sequentially. |
| `batch-presearch.sh` fails | Install `@microsoft/learn-cli` and run from a shell with bash support. |
| Agent doesn't ask scoping questions | Add context: "fact-check this M365 Security article about Defender for Endpoint" |

---

## Agent variants

| Agent file | Tools | Best for |
|-----------|-------|----------|
| `microsoft-fact-checker.agent.md` | ~95 | Full capability — all MCP tools available |
| `microsoft-fact-checker-slim.agent.md` | 25 | Standard fact-checking — faster startup, lower token usage |
| `microsoft-fact-checker-cia.agent.md` | 31 | Customer incident analysis — includes ADO work item tools |

The slim agent is the default for Workflow 6 (Deep Agent). The CIA agent is used for Workflow 10 (CIA Analysis). The full agent is available as a fallback when the slim variant lacks a needed tool.

---

## History

This skill consolidates the earlier `fact-checker` and `microsoft-doc-verifier` skills into a single unified tool. All workflows from both predecessors are preserved.

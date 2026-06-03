# Documentation Verifier

A VS Code Copilot skill that fact-checks Microsoft documentation against official sources across **all product areas** — Azure, Microsoft 365, Microsoft Security, Power Platform, Dynamics 365, Windows, Developer Tools, and more.

Four workflows: single-article check, PR review, research, and fleet batch (parallel multi-article). A tiered source hierarchy prioritizes learn.microsoft.com. Reports are opt-in via the `--report` flag — every workflow is chat-only by default.

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
│   ├── claim-manifest.prompt.md                 # Supporting: claim extraction for Fleet Batch
│   ├── _runtime-adapter.md                      # Shared runtime dispatch rules
│   └── _subagent-contract.md                    # Shared subagent I/O contract
├── scripts/
│   └── batch-presearch.sh                       # Pre-search helper for large batches
├── TEST-PROTOCOLS.md                           # Validation procedures for the 4 workflows
└── references/
    ├── source-hierarchy.md                      # Local pointer → _shared/source-hierarchy.md
    ├── source-guide.md                          # Educational guide to sources
    └── workflows.md                             # Detailed per-workflow procedures
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
| "Fact-check this article" | Single Article |
| "Fact-check PR #12345" | PR Review |
| "Research Azure Front Door caching" | Research |
| "Fact-check these 5 articles" / "this folder" | Fleet Batch |
| "Fact-check the top articles for `<service>`" | `pageviews-query` → Fleet Batch |
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

### Escalation Triggers (Accuracy-First)

Escalate a claim or file to Tier 1 when any trigger matches:

- Tier conflict: Tier 1 and Tier 2 sources disagree.
- Unverifiable rate: more than 10% of claims in one article are unverifiable.
- Safety impact: claims affect RBAC, authentication, encryption, or production availability.
- Confidence drop: reviewer confidence is below high after Tier 2 analysis.
- Policy or retirement risk: deprecation or retirement timelines are present.

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

## History

This skill consolidates the earlier `fact-checker`, `microsoft-doc-verifier`, `microsoft-fact-checker`, and `fact-check-batch-subagent` skills into a single unified tool with four focused workflows.

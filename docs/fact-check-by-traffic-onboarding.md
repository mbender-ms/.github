# Fact-Check by Traffic: Onboarding Guide

Pull the top N articles for any Azure service by page views, then automatically fact-check them against authoritative Microsoft sources — all orchestrated by CDA Cortex in VS Code.

This guide covers everything another content developer needs to replicate this workflow on their own machine.

---

## What the workflow does

```
┌──────────────┐     ┌──────────────────┐     ┌───────────────────┐     ┌──────────────────┐
│ Power BI     │────▶│ pageviews-query  │────▶│ doc-verifier      │────▶│ apply-factcheck- │
│ (traffic     │     │ skill            │     │ skill (Fleet      │────▶│ report skill     │
│  data)       │     │                  │     │ Batch)            │     │ (optional)       │
└──────────────┘     └──────────────────┘     └───────────────────┘     └──────────────────┘
                     Ranked table +           Per-article verdict       Mechanical fixes
                     JSON handoff block       report with citations     applied as a commit
```

1. **Phase 1 — Traffic query**: The `pageviews-query` skill queries the Content Engagement Power BI semantic model for the top N articles by page views for your service and month.
2. **Phase 2 — Fact-check**: The JSON handoff block feeds directly into the `doc-verifier` skill's Fleet Batch workflow, which verifies every technical claim against Tier-1 Microsoft sources (learn.microsoft.com).
3. **Phase 3 — Apply fixes** (optional): The `apply-factcheck-report` skill reads the generated report and applies low-risk mechanical fixes (typos, wrong code-fence labels, link swaps) as a single commit.

---

## Prerequisites

| Requirement | Details |
|---|---|
| **VS Code** | Latest stable release with GitHub Copilot Chat extension |
| **GitHub Copilot** | Active license (Business or Enterprise) with agent mode enabled |
| **CDA Cortex agent** | Installed at `~/.copilot/cda/latest/cda.agent.md` — ask your team lead for the installer or see the `update-cda` skill |
| **Node.js** | v18+ (required to run MCP servers) |
| **Azure CLI** | `az login` authenticated to your Microsoft tenant (for ADO MCP) |
| **GitHub CLI** | `gh auth login` authenticated (for GitHub MCP) |
| **azure-docs-pr repo** | Cloned locally with `upstream` remote pointing to `MicrosoftDocs/azure-docs-pr` |
| **Power BI access** | Access to the **Skilling-BCS-DataPlatform-PROD** workspace in Fabric/Power BI (your manager can request this) |

---

## Files to install

You need files in **three locations**. The table below lists every file, where it goes, and what it does.

### 1. User-level skills (`~/.copilot/skills/`)

These are personal skills that live outside any repo. They travel with you across all workspaces.

| File | Path | Purpose |
|---|---|---|
| `SKILL.md` | `~/.copilot/skills/pageviews-query/SKILL.md` | Queries Power BI for top N articles by traffic for a service + month. Emits a ranked table and a JSON handoff block. |
| `SKILL.md` | `~/.copilot/skills/freshness-analysis/SKILL.md` | (Optional) Scores articles for freshness review — useful companion to fact-checking. |

### 2. Repo-level skills (`.github/skills/`)

These live in the `.github` repo (or any repo-scoped `.github/` folder). They're shared with anyone who clones the repo.

| File | Path | Purpose |
|---|---|---|
| `SKILL.md` | `.github/copilot/skills/doc-verifier/SKILL.md` | Unified fact-checker: verifies claims against Tier-1 sources, produces structured reports with citations and pending-change checklists. The Fleet Batch workflow dispatches one subagent per article for batches of any size; Single Article handles one-offs. |
| `SKILL.md` | `.github/skills/apply-factcheck-report/SKILL.md` | Reads a fact-check report and applies mechanical fixes as a single commit (never pushes). |

### 3. Prompt file (`.github/prompts/`)

| File | Path | Purpose |
|---|---|---|
| `fact-check-by-traffic.prompt.md` | `.github/prompts/fact-check-by-traffic.prompt.md` | One-shot orchestrator: runs `pageviews-query` then pipes results into the `doc-verifier` Fleet Batch workflow without pausing. |

### 4. MCP server configuration (`~/.copilot/mcp-config.json`)

Your `mcp-config.json` must include the **Power BI** MCP server. Add this entry to the `mcpServers` object:

```json
{
  "mcpServers": {
    "powerbi": {
      "type": "http",
      "url": "https://api.fabric.microsoft.com/v1/mcp/powerbi"
    }
  }
}
```

> The `cda`, `ado`, and `github` servers should already be configured if you have CDA Cortex installed. The Power BI server is the one most commonly missing.

---

## File contents

Below is the content of each file you need to create. Copy each block into the corresponding path listed above.

### `~/.copilot/skills/pageviews-query/SKILL.md`

<details>
<summary>Expand to see full file content</summary>

```yaml
---
name: pageviews-query
displayName: Page views query
version: 1.0.0
category: Analysis
description: >
  Query the Content Engagement Power BI report for the top-N most-viewed articles
  for a service and month. Returns a ranked table plus a machine-readable JSON
  handoff block that other skills (freshness, fact-check, deduplication) can consume
  as input. Use when the user says "top articles", "most viewed",
  "page views for <service>", or "top N articles for <service> <month>".
argument-hint: 'service month [count] (e.g., "azure-load-balancer April 2026 10")'
user-invocable: true
---
```

See the full skill at: [pageviews-query/SKILL.md](../copilot/skills/pageviews-query/SKILL.md) in your team's shared `.github` repo, or request the file from your CDA Cortex admin.

Key configuration values inside the skill:

| Setting | Value |
|---|---|
| **Semantic model name** | Content Engagement Report |
| **Artifact ID** | `aede3e37-62fd-475e-b629-dbb2d7683ab1` |
| **Workspace** | Skilling-BCS-DataPlatform-PROD |
| **MCP server** | `powerbi-remote` (the Power BI MCP server) |
| **Default article count** | 10 |
| **Locale filter** | `en-us` only |

</details>

### `.github/copilot/skills/doc-verifier/SKILL.md`

<details>
<summary>Expand to see full file content</summary>

The doc-verifier skill is the largest file. Key sections:

- **Authority Hierarchy** — Tier 1 (learn.microsoft.com) > Tier 2 (TechCommunity, DevBlogs) > Tier 3 (Stack Overflow, community)
- **Source Routing** — rules for which MCP tool to call per claim type (networking vs. AI vs. code snippets)
- **Report File Format** — batch summary, detailed findings per article, issues index, pending changes with find/replace pairs
- **Output path** — opt-in only via `--report <path>` (see the skill's Fleet Batch workflow)

Copy the full file from your team's `.github/copilot/skills/doc-verifier/SKILL.md`.

</details>

### `.github/prompts/fact-check-by-traffic.prompt.md`

This is the one-shot orchestrator prompt. Create it with this exact content:

```markdown
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

Run the `pageviews-query` skill, then immediately pass the resulting JSON handoff
block as input to the `doc-verifier` skill's Fleet Batch workflow. Do not pause between phases.

## Inputs

- **service** — `MSService` value (for example, `azure-application-gateway`)
- **month** — report month (for example, `April 2026`)
- **count** — articles to fact-check (default: **3**)

If any input is missing, ask once before starting.

## Execution

1. **Phase 1**: Run the full `pageviews-query` skill for the given service, month,
   and count. Emit the ranked table and JSON handoff block.
2. **Phase 2**: Pass the JSON handoff block directly to the `doc-verifier`
   Fleet Batch workflow. Process articles in rank order without waiting for user
   input.
3. **Phase 3**: Emit the Batch Summary table defined in the `doc-verifier`
   skill, followed by 2–3 recommended next steps.
```

---

## How to run the workflow

### Option A: One-shot prompt (recommended)

1. Open VS Code with the `azure-docs-pr` workspace.
2. Open Copilot Chat and switch to **CDA** mode (or your agent mode).
3. Type:

   ```
   /fact-check-by-traffic azure-application-gateway April 2026 5
   ```

   This runs both phases automatically and produces a fact-check report for the top 5 articles.

### Option B: Step by step

1. **Query traffic data first:**

   ```
   @CDA top 10 articles for azure-load-balancer May 2026
   ```

   CDA runs the `pageviews-query` skill and returns a ranked table + JSON block.

2. **Fact-check the results:**

   Copy the JSON handoff block and say:

   ```
   @CDA fact-check these articles [paste JSON block]
   ```

   Or simply:

   ```
   @CDA now fact-check the top 3 from that list
   ```

3. **Apply fixes (optional):**

   After reviewing the report:

   ```
   @CDA apply low-risk fixes from c:\temp\azure-load-balancer-factcheck-may2026.md
   ```

### Option C: Large batch (6+ articles)

For larger batches, the `doc-verifier` Fleet Batch workflow dispatches one subagent per article to stay within token limits:

```
@CDA fact-check the top 10 articles for azure-application-gateway April 2026
```

This dispatches one subagent per article sequentially, producing a consolidated report with cross-article consistency checks.

---

## Understanding the output

### Fact-check report structure

The report written to disk contains these sections:

1. **Report header** — service, period, article count, generation date
2. **Batch summary table** — ranked articles with claim counts and issue counts
3. **Recommended next steps** — grouped Priority 1/2/3 action items across articles
4. **Detailed findings per article** — accurate claims (grouped), full blocks for each issue with citations and find/replace pairs
5. **Issues index** — flat table of all non-accurate findings with severity
6. **Pending changes** — agent-executable checklist with `FC-N` IDs, file paths, and exact find/replace text

### Severity levels

| Severity | Meaning | Example |
|---|---|---|
| **High** | Factually wrong — breaks reader implementation | Wrong port number, wrong RBAC role, wrong retirement date |
| **Medium** | Orientation outdated or formatting issue | Misleading lead paragraph, wrong code-fence language |
| **Low** | Cosmetic | Typo, stale `ms.date`, link path inconsistency |

---

## Customizing for your service area

### Change the default service

Edit the `fact-check-by-traffic.prompt.md` description or create a copy with your service pre-filled:

```yaml
---
mode: agent
description: "Fact-check top azure-kubernetes-service articles by traffic"
---
# Fact-Check by Traffic — AKS
...
```

### Change the output path

The default report path is `c:\temp\`. To change it, tell the agent in your prompt:

```
@CDA fact-check top 5 for azure-functions April 2026, save report to c:\github\my-reports\
```

Or modify the `doc-verifier` skill's **Output File** section.

### Add your own source-routing rules

The `doc-verifier` skill has a **Source Routing** section. Add rules for your service area:

```markdown
6. **Your-service-specific claim** → `mcp_azure-docs_search_docs` with
   `service_filter: "your-service"`.
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| "Power BI MCP server not available" | Ensure `powerbi` is in your `~/.copilot/mcp-config.json` and you're authenticated to your Microsoft tenant |
| Empty results from page views query | The `MSService` value didn't match. The skill validates first — check the correction it suggests |
| "No articles found for this service" | Verify the service exists in the Content Engagement semantic model. Run: `@CDA list valid MSService values` |
| Fact-checker hangs on large articles | Use the `doc-verifier` Fleet Batch workflow: `@CDA fact-check these as a fleet batch` |
| Report missing citations | Check that `microsoft-lea` (Microsoft Learn MCP) is configured in your VS Code MCP settings |
| "MCP server not started" | Restart VS Code, or check `~/.copilot/mcp-config.json` for syntax errors |

---

## Required MCP servers summary

| Server | Config key | Purpose | Required? |
|---|---|---|---|
| **Power BI** | `powerbi` | Traffic data queries (DAX against Content Engagement model) | Yes — core to the workflow |
| **Microsoft Learn** | `microsoft-lea` | Fact verification against learn.microsoft.com | Yes — the fact-checker's primary source |
| **Azure Docs** | `azure-docs` | Service-aware doc search with freshness checking | Recommended — better results for Azure services |
| **CDA** | `cda` | Orchestration (branch names, PR descriptions, work item templates) | Only if you're also creating PRs/work items from the results |
| **ADO** | `ado` | Work item management | Only if tracking fact-check work in ADO |
| **GitHub** | `github` | PR creation and code search | Only if creating PRs from the fixes |

---

## Quick-start checklist

- [ ] VS Code with GitHub Copilot Chat installed
- [ ] CDA Cortex agent file at `~/.copilot/cda/latest/cda.agent.md`
- [ ] Power BI MCP server in `~/.copilot/mcp-config.json`
- [ ] Microsoft Learn MCP server configured in VS Code
- [ ] Azure Docs MCP server configured in VS Code (recommended)
- [ ] `~/.copilot/skills/pageviews-query/SKILL.md` created
- [ ] `.github/copilot/skills/doc-verifier/SKILL.md` in your repo
- [ ] `.github/skills/apply-factcheck-report/SKILL.md` in your repo
- [ ] `.github/prompts/fact-check-by-traffic.prompt.md` in your repo
- [ ] `azure-docs-pr` cloned with `upstream` → `MicrosoftDocs/azure-docs-pr`
- [ ] `az login` and `gh auth login` completed
- [ ] Access to Skilling-BCS-DataPlatform-PROD Power BI workspace

---

## Architecture reference

```
~/.copilot/
├── mcp-config.json              ← MCP server connections (Power BI, CDA, ADO)
├── cda/
│   └── latest/
│       └── cda.agent.md         ← CDA Cortex agent definition
└── skills/
    └── pageviews-query/
        └── SKILL.md             ← Traffic query skill (user-level)

<your-repo>/.github/
├── prompts/
│   └── fact-check-by-traffic.prompt.md   ← One-shot orchestrator
├── copilot/skills/
│   └── doc-verifier/
│       └── SKILL.md             ← Unified fact-checker (Single + Fleet Batch)
├── skills/
│   └── apply-factcheck-report/
│       └── SKILL.md             ← Apply fixes from report
└── references/
    └── sources-for-fact-checking.md  ← Source hierarchy documentation
```

---

## Data flow detail

```
User: "fact-check top 5 for azure-load-balancer May 2026"
  │
  ▼
┌─────────────────────────────────────────────────┐
│ pageviews-query skill                           │
│                                                 │
│ 1. Validate MSService via DAX query             │
│ 2. TOPN(5) query against Content Engagement     │
│ 3. Emit ranked table + JSON handoff block:      │
│    {                                            │
│      "service": "azure-load-balancer",          │
│      "month": "May 2026",                       │
│      "count": 5,                                │
│      "articles": [                              │
│        { "rank": 1, "title": "...",             │
│          "localPath": "articles/...",           │
│          "pageViews": 5150 }                    │
│      ]                                          │
│    }                                            │
└────────────────────┬────────────────────────────┘
                     │ JSON handoff
                     ▼
┌─────────────────────────────────────────────────┐
│ doc-verifier skill (Fleet Batch)                │
│                                                 │
│ For each article (rank order):                  │
│ 1. Read article via localPath                   │
│ 2. Extract technical claims                     │
│ 3. Route to correct search tool                 │
│ 4. Verify against Tier-1 sources                │
│ 5. Record verdict + citation                    │
│                                                 │
│ Output: structured report at                    │
│ c:\temp\azure-load-balancer-factcheck-may2026.md│
└────────────────────┬────────────────────────────┘
                     │ report path
                     ▼
┌─────────────────────────────────────────────────┐
│ apply-factcheck-report skill (user opts in)     │
│                                                 │
│ 1. Parse Issues tables from report              │
│ 2. Apply Low-severity mechanical fixes          │
│ 3. Stage + commit (never pushes)                │
│ 4. Report Applied / Skipped / Needs-review      │
└─────────────────────────────────────────────────┘
```

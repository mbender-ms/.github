---
mode: agent
description: Fact-check all changed files in a GitHub PR and generate a verification report
tools:
  - microsoft-learn-mcp-server/microsoft_docs_search
  - microsoft-learn-mcp-server/microsoft_docs_fetch
  - microsoft-learn-mcp-server/microsoft_code_sample_search
  - github/pull_request_read
  - read/readFile
  - read/problems
  - search/codebase
  - search/fileSearch
  - search/textSearch
  - edit/editFiles
  - edit/createFile
  - execute/runInTerminal
  - execute/getTerminalOutput
  - todo
---

# PR Fact-Check Review

Fact-check all changed files in a GitHub pull request against official Microsoft documentation and generate a standalone verification report.

## Step 0 — Scope

Ask the user (skip if already clear):
1. **PR number** — Which PR to review?
2. **Repository** — Which repo? (default: current workspace repo)
3. **Product area** — What Microsoft product area do the changed files cover?
4. **Depth** — Quick check or thorough verification?

## Step 1 — Load the PR

1. Fetch PR metadata (title, author, branch, description)
2. List all changed files
3. Filter to documentation files (`.md`, `.yml`)
4. Read the content of each changed file (from patches or file read)
5. Report the file count and ask for confirmation

## Step 1.5 — Quick triage checklist (apply threshold matrix)

Before deep verification, run this triage and record decisions in the report:

1. Count documentation files in scope.
2. Estimate claim volume per file (low: 1-15, medium: 16-40, high: more than 40).
3. Mark risk level for each file:
  - High risk: security, compliance, identity, encryption, RBAC, production safety, retirement timelines.
  - Standard risk: feature descriptions, configuration guidance, and examples without safety-critical impact.
4. Choose route by threshold:
  - 1-5 files and mostly low-risk content: Tier 2 or Tier 3 first, escalate contested claims only.
  - More than 5 files, major technical changes, or high-risk content: include Tier 1 review for flagged files.
  - High claim density (more than 40 in a file) or cross-service coupling: run a deep pass for that file.
5. Apply escalation triggers at claim level:
  - Tier 1 and Tier 2 source conflict.
  - More than 10% unverifiable claims in a file.
  - Reviewer confidence remains below high after structured pass.

## Step 2 — Catalog and group files

For each file:
1. Extract frontmatter metadata (`ms.service`, `ms.prod`, `ms.topic`)
2. Identify the service/feature area from content
3. Group files by service area
4. Build a claim inventory per file

## Step 3 — Verify per service group

Process files grouped by service area:

> **Multi-agent optimization**: When the PR contains files across 3+ service groups, spawn one `runSubagent` per service group for parallel verification. Each sub-agent receives its file list, the source hierarchy, and the matching category YAML from `copilot/skills/sources/`.

1. Search `microsoft_docs_search` for each service area
2. Use `microsoft_docs_fetch` for full reference pages
3. Use `microsoft_code_sample_search` for code examples
4. Cross-reference all technical claims against fetched sources
5. Audit remediation and reference links
6. Check preview/GA/deprecated status for all mentioned features
7. For contested or high-risk claims, perform Tier 1 adjudication before assigning final status

## Step 4 — Classify findings

For each claim:
- **✅ Accurate** — Matches current official documentation
- **⚠️ Partially accurate** — Minor discrepancy or missing context
- **❌ Inaccurate** — Contradicts official sources
- **🕐 Outdated** — Was correct but superseded
- **❓ Unverifiable** — No authoritative source found
- **🔗 Broken link** — URL doesn't resolve or anchor is missing

## Step 5 — Generate report

Create `factcheck_PR{number}.md` using the report template from SKILL.md:

1. **Header** — PR number, date, product area, files reviewed
2. **Executive summary** — Overall assessment with counts
3. **Findings at a glance** — Status distribution table
4. **Critical findings** — Each with: claim quote, evidence from official docs, recommended fix
5. **Advisory findings** — Context gaps, SKU notes, preview disclosures
6. **Per-file verification table** — Grouped by service area, per-file status + notes
7. **Link audit** — Every remediation/reference link with verification status
8. **Sources consulted** — All URLs organized by tier

## Step 6 — Present results

- Summarize key findings in chat
- Note the report file location
- Ask if the user wants to:
  - Commit the report to the PR branch
  - Post findings as a PR comment
  - Apply corrections to the files

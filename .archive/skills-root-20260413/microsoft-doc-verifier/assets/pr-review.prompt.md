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

## Step 0 ΓÇö Scope

Ask the user (skip if already clear):
1. **PR number** ΓÇö Which PR to review?
2. **Repository** ΓÇö Which repo? (default: current workspace repo)
3. **Product area** ΓÇö What Microsoft product area do the changed files cover?
4. **Depth** ΓÇö Quick check or thorough verification?

## Step 1 ΓÇö Load the PR

1. Fetch PR metadata (title, author, branch, description)
2. List all changed files
3. Filter to documentation files (`.md`, `.yml`)
4. Read the content of each changed file (from patches or file read)
5. Report the file count and ask for confirmation

## Step 2 ΓÇö Catalog and group files

For each file:
1. Extract frontmatter metadata (`ms.service`, `ms.prod`, `ms.topic`)
2. Identify the service/feature area from content
3. Group files by service area
4. Build a claim inventory per file

## Step 3 ΓÇö Verify per service group

Process files grouped by service area:
1. Search `microsoft_docs_search` for each service area
2. Use `microsoft_docs_fetch` for full reference pages
3. Use `microsoft_code_sample_search` for code examples
4. Cross-reference all technical claims against fetched sources
5. Audit remediation and reference links
6. Check preview/GA/deprecated status for all mentioned features

## Step 4 ΓÇö Classify findings

For each claim:
- **Γ£à Accurate** ΓÇö Matches current official documentation
- **ΓÜá∩╕Å Partially accurate** ΓÇö Minor discrepancy or missing context
- **Γ¥î Inaccurate** ΓÇö Contradicts official sources
- **≡ƒòÉ Outdated** ΓÇö Was correct but superseded
- **Γ¥ô Unverifiable** ΓÇö No authoritative source found
- **≡ƒöù Broken link** ΓÇö URL doesn't resolve or anchor is missing

## Step 5 ΓÇö Generate report

Create `factcheck_PR{number}.md` using the report template from SKILL.md:

1. **Header** ΓÇö PR number, date, product area, files reviewed
2. **Executive summary** ΓÇö Overall assessment with counts
3. **Findings at a glance** ΓÇö Status distribution table
4. **Critical findings** ΓÇö Each with: claim quote, evidence from official docs, recommended fix
5. **Advisory findings** ΓÇö Context gaps, SKU notes, preview disclosures
6. **Per-file verification table** ΓÇö Grouped by service area, per-file status + notes
7. **Link audit** ΓÇö Every remediation/reference link with verification status
8. **Sources consulted** ΓÇö All URLs organized by tier

## Step 6 ΓÇö Present results

- Summarize key findings in chat
- Note the report file location
- Ask if the user wants to:
  - Commit the report to the PR branch
  - Post findings as a PR comment
  - Apply corrections to the files

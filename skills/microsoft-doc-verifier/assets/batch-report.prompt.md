---
mode: agent
description: Fact-check multiple files and generate a standalone verification report
tools:
  - microsoft-learn-mcp-server/microsoft_docs_search
  - microsoft-learn-mcp-server/microsoft_docs_fetch
  - microsoft-learn-mcp-server/microsoft_code_sample_search
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

# Batch Fact-Check Report

Fact-check a set of files (folder, file list, or glob pattern) against official Microsoft documentation and generate a standalone report.

## Step 0 ΓÇö Scope

Ask the user (skip if already clear from context):
1. **Product area** ΓÇö What Microsoft product area? (Azure, M365, Security, Power Platform, Dynamics 365, Windows, DevTools)
2. **Service focus** ΓÇö Which specific service or feature?
3. **File scope** ΓÇö Which files? (folder path, glob pattern, or explicit file list)
4. **Output** ΓÇö Report only, corrections + report, or corrections only?
5. **Depth** ΓÇö Quick check or thorough verification?

Discover files:
- If folder: list all `.md` files recursively
- If glob: expand the pattern
- If file list: validate each path exists
- Report the file count and ask for confirmation before proceeding

## Step 1 ΓÇö Read and catalog files

For each file:
1. Read the content
2. Extract the `ms.service` / `ms.prod` and `ms.topic` from frontmatter
3. Group files by service/feature area
4. Build a claim inventory per file

## Step 2 ΓÇö Verify claims per service group

Process files grouped by service area (batch related searches):
1. Search `microsoft_docs_search` for each service area's key topics
2. Use `microsoft_docs_fetch` to retrieve full reference pages
3. Use `microsoft_code_sample_search` for code examples
4. Cross-reference claims against fetched sources
5. Check remediation/reference links for validity

## Step 3 ΓÇö Classify findings

For each claim in each file:
- **Γ£à Accurate** ΓÇö Matches current official documentation
- **ΓÜá∩╕Å Partially accurate** ΓÇö Minor discrepancy or missing context
- **Γ¥î Inaccurate** ΓÇö Contradicts official sources
- **≡ƒòÉ Outdated** ΓÇö Was correct but superseded
- **Γ¥ô Unverifiable** ΓÇö No authoritative source found
- **≡ƒöù Broken link** ΓÇö URL doesn't resolve or anchor is missing

## Step 4 ΓÇö Generate report

Create `factcheck_[scope]_YYYYMMDD.md` using the report template from SKILL.md:

1. **Executive summary** ΓÇö Total files, issues found, overall assessment
2. **Findings at a glance** ΓÇö Status counts table
3. **Critical findings** ΓÇö Action-required items with evidence and fix recommendations
4. **Advisory findings** ΓÇö Recommended but not blocking
5. **Per-file verification table** ΓÇö Grouped by service area
6. **Link audit** ΓÇö Status of all referenced URLs
7. **Sources consulted** ΓÇö All URLs organized by tier

## Step 5 ΓÇö Apply corrections (if requested)

If the user wants corrections applied:
- Edit each file with fixes
- Update `ms.date` in frontmatter
- Do NOT remove unverifiable claims
- Present a summary of all edits made

## Step 6 ΓÇö Present results

- Provide a brief chat summary of the report
- Note the report file location
- Ask if the user wants to commit changes

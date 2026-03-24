---
mode: agent
description: "Run a comprehensive freshness pass on multiple articles — full fact-check against public docs and APIs, comprehensive editorial review, SEO audit, markdown auto-fix, content suggestions, and MS Style Guide checks across a folder, glob pattern, or file list"
tools:
  - microsoft-learn-mcp-server/microsoft_docs_search
  - microsoft-learn-mcp-server/microsoft_docs_fetch
  - microsoft-learn-mcp-server/microsoft_code_sample_search
  - web/fetch
  - web/githubRepo
  - read/readFile
  - read/problems
  - search/codebase
  - search/fileSearch
  - search/textSearch
  - search/usages
  - edit/editFiles
  - edit/createFile
  - execute/runInTerminal
  - execute/getTerminalOutput
  - todo
---

# Batch Freshness Pass — Multiple Articles

Run a comprehensive freshness pass on multiple documentation articles. Each article receives the full three-phase treatment: fact-check against public docs/APIs, comprehensive editorial review (SEO, markdown, engagement, MS Style Guide), and consolidation with corrections applied.

Results are merged into a consolidated report artifact and optionally applied to all files.

---

## Authority hierarchy

Use sources in this priority order:

1. **Tier 1 (Primary)**: learn.microsoft.com, azure.microsoft.com — product docs, features, limits, pricing
2. **Tier 2 (Secondary)**: techcommunity.microsoft.com, devblogs.microsoft.com, github.com/Azure, github.com/MicrosoftDocs — announcements, API specs, SDKs, samples
3. **Tier 3 (Cross-reference)**: developer.microsoft.com, code.visualstudio.com, MS Q&A (verified MS employees only) — platform docs, edge cases

> Higher tier always wins. REST API specs on GitHub are ground truth for API parameters and schemas.

---

## Step 0 — Scope and file discovery

Before starting, determine the file set:

1. **Ask for input** (if not provided):
   - **Folder**: Recursively list all `.md` files in the folder
   - **Glob pattern**: Expand the pattern to matching `.md` files
   - **File list**: Validate each path exists

2. **Confirm scope**: Present the discovered file list with count and ask for confirmation before proceeding. Example:

   > Found **12** markdown files in `articles/container-apps/`. Proceed with freshness pass on all 12?

3. **Product area** (optional): If the user specifies a product area (Azure, M365, Security, etc.), use it to optimize search domains. Otherwise, detect from `ms.service`/`ms.prod` metadata in Step 1.

---

## Step 1 — Catalog and group files

Read each file and extract metadata:

1. **Extract frontmatter**: `ms.service`, `ms.prod`, `ms.topic`, `ms.date`, `title`
2. **Group by service area**: Cluster files by `ms.service` or `ms.prod` value
3. **Build inventory**: Create a tracking table:

| # | File | Service | Topic type | ms.date | Status |
|---|------|---------|------------|---------|--------|
| 1 | file1.md | azure-container-apps | how-to | 01/15/2025 | Pending |
| 2 | file2.md | azure-container-apps | concept | 03/01/2024 | Pending |
| ... | | | | | |

4. **Load sources catalog**: For each unique service area, load the matching YAML from `copilot/skills/sources/` (e.g., `azure-compute.yml`) to get the relevant GitHub repos for Tier 2 verification.

---

## Step 2 — Process files (with multi-agent optimization)

### For small batches (< 5 files or single service group)

Process each file sequentially through the full three-phase freshness pass:

**For each file:**

#### Phase A — Fact-check
1. Extract all technical claims
2. Verify against Tier 1–3 sources using `microsoft_docs_search`, `microsoft_docs_fetch`, `microsoft_code_sample_search`, `web/fetch`, `web/githubRepo`
3. Check for deprecation, retirement, version changes
4. Validate code examples
5. Classify: ✅ Accurate, ⚠️ Partial, ❌ Inaccurate, 🕐 Outdated, ❓ Unverifiable, 🔗 Broken link

#### Phase B — Editorial pass
1. **Editorial review**: Frontmatter completeness, title (30–65 chars, title case), description (120–165 chars, CTA), passive voice, procedures (≤ 10 steps, imperative verbs), sensitive identifiers
2. **SEO audit**: Title, description, H1 (sentence case), intro keyword placement, subheadings (sentence case), image alt text, internal linking
3. **Auto-fix markdown**: Heading hierarchy, blank lines, code fence identifiers (`azurecli`, `azurepowershell`), alert syntax, table formatting, trailing whitespace
4. **Content suggestions**: Bounce rate, CTR, copy-try-scroll, dwell, exit rate improvements
5. **MS Style Guide**: Voice/tone, contractions, sentence-style capitalization on H2+, active voice, imperative procedures, Oxford comma, brief writing

#### Phase C — Record findings
- Record all findings for this file (do NOT apply edits yet — collect for consolidated report first)
- Update the tracking table status

### For large batches (5+ files across multiple service groups)

Use multi-agent parallelization:

1. **Group files** by `ms.service` value
2. **Spawn one `runSubagent` per service group** with these inputs:
   - File list for the group
   - Source hierarchy (Tier 1–3)
   - Matching sources YAML (GitHub repos for that service area)
   - Full Phase A + Phase B instructions (from above)
3. **Collect results** from each sub-agent
4. **Merge** into the consolidated tracking table

---

## Step 3 — Generate consolidated report

Create a report file: `freshness_[scope]_YYYYMMDD.md`

### Report template

```markdown
# Freshness Pass Report — [Scope]

**Date**: [YYYY-MM-DD]
**Files reviewed**: [count]
**Service areas**: [list]

## Executive summary

- **Total findings**: [count]
- **Fact-check**: [count] (❌ [n] inaccurate, 🕐 [n] outdated, ⚠️ [n] partial, 🔗 [n] broken links, ❓ [n] unverifiable)
- **Editorial**: [count] ([n] critical, [n] important, [n] suggestions)
- **Files needing corrections**: [count] of [total]

## Critical findings

[List findings with severity Critical — these need immediate attention]

### [Finding title]
- **File**: [path]
- **Line(s)**: [line numbers]
- **Issue**: [description]
- **Correction**: [proposed fix]
- **Source**: [URL]

## Per-file summary

| # | File | Fact-check | Editorial | Critical | Important | Suggestion | Status |
|---|------|-----------|-----------|----------|-----------|------------|--------|
| 1 | file1.md | 2 ❌, 1 🕐 | 3 SEO, 2 Style | 2 | 3 | 1 | Needs fixes |
| 2 | file2.md | ✅ All accurate | 1 Markdown | 0 | 1 | 0 | Minor fixes |

## Findings by file

### [filename.md]

#### Fact-check findings
| # | Claim | Status | Current | Correct | Source |
|---|-------|--------|---------|---------|--------|

#### Editorial findings
| # | Issue | Severity | Category | Current | Suggested |
|---|-------|----------|----------|---------|-----------|

## Link audit

| URL | File | Status | Replacement |
|-----|------|--------|-------------|

## Sources consulted

| Source | Tier | URL | Accessed |
|--------|------|-----|----------|
```

---

## Step 4 — Apply corrections (optional)

Ask the user: **"Apply all corrections to the files?"**

If yes:

1. Apply all fact-check corrections (inaccurate, outdated, broken links) to each file
2. Apply all editorial fixes (SEO, markdown, style, metadata) to each file
3. Update `ms.date` to today's date on every corrected file
4. Do NOT add HTML comments or reference markers
5. Preserve each article's existing tone and structure

If no:

- Leave the report as the deliverable
- The user can apply corrections selectively using the per-file findings

---

## Step 5 — Git workflow (optional)

Ask if the user wants to commit. If yes:

1. Create branch: `freshness/[scope]-MMDDYYYY`
2. Stage and commit each corrected file individually with message: `freshness: [filename] — fact-check + editorial pass`
3. Commit the report file: `freshness: add batch freshness report for [scope]`
4. Push the branch
5. Open a pull request with the executive summary from the report

---

## Quality checklist

Before finishing, confirm ALL of these for every processed file:

### Fact-check quality
- [ ] All technical claims verified against at least one Tier 1 source
- [ ] Every fact-check correction includes a source citation with URL
- [ ] Code examples validated
- [ ] Version/deprecation status confirmed for all mentioned services
- [ ] Broken links fixed or flagged

### Editorial quality
- [ ] Title: 30–65 chars, title case, primary keyword
- [ ] Description: 120–165 chars, CTA, keyword at beginning, unique
- [ ] H1: sentence case, differs from title
- [ ] Customer intent present in `ms.custom`
- [ ] Heading hierarchy correct (no skipped levels, single H1)
- [ ] All H2+ headings use sentence-style capitalization
- [ ] Code fence identifiers correct (`azurecli`, `azurepowershell`)
- [ ] Sensitive identifiers replaced with approved placeholders
- [ ] Writing follows MS Style Guide
- [ ] Engagement improvements noted

### Batch quality
- [ ] All files in scope processed
- [ ] Consolidated report generated and saved
- [ ] Tracking table fully populated
- [ ] Per-file findings documented

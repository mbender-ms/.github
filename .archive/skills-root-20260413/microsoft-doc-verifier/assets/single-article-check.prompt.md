---
mode: agent
description: Fact-check the current article against official Microsoft documentation
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
  - todo
---

# Single Article Fact-Check

Fact-check the currently open article against official Microsoft documentation. Verify every technical claim, apply corrections in-place, and present a summary with source citations.

## Step 0 ΓÇö Scope

Before starting, determine:
1. **Product area** ΓÇö Read the file's `ms.service`, `ms.prod`, or content to identify the product area (Azure, M365, Security, Power Platform, Dynamics 365, Windows, DevTools).
2. **Service focus** ΓÇö Identify the specific service or feature from the content.
3. **Depth** ΓÇö Ask the user: "Quick check or thorough verification?"

Use the product area to select search domains (see SKILL.md ΓåÆ Product Area Search Domains).

## Step 1 ΓÇö Identify claims

Read the current file and extract every verifiable technical claim:
- Product/service names and descriptions
- Feature capabilities, limitations, SKU/tier requirements
- Version numbers, API references, CLI/PowerShell commands
- Configuration values, defaults, quotas, limits
- Pricing, licensing, regional availability
- Preview/GA/deprecated status
- Code examples and syntax

For each claim, note the **WHAT** (assertion), **CONTEXT** (product/version), and **SCOPE** (applicability).

## Step 2 ΓÇö Verify against sources

For each claim, search in priority order:
1. `microsoft_docs_search` ΓÇö Search learn.microsoft.com for the topic using product-area-specific terms
2. `microsoft_docs_fetch` ΓÇö Retrieve full pages when search snippets are insufficient
3. `microsoft_code_sample_search` ΓÇö Validate code examples against official samples
4. `grep_search` / `semantic_search` ΓÇö Cross-reference against workspace content
5. Check for deprecation, preview/GA status, and retirement notices

## Step 3 ΓÇö Classify accuracy

For each claim, classify as:
- **Γ£à Accurate** ΓÇö Matches current official documentation
- **ΓÜá∩╕Å Partially accurate** ΓÇö Mostly correct but needs refinement
- **Γ¥î Inaccurate** ΓÇö Contradicted by official sources
- **≡ƒòÉ Outdated** ΓÇö Was correct but no longer current
- **Γ¥ô Unverifiable** ΓÇö No authoritative source found

## Step 4 ΓÇö Apply corrections

For any inaccurate or outdated content:
- Edit the file directly with the corrected information
- Preserve the article's tone, style, and formatting
- Update `ms.date` in frontmatter to today's date
- Do NOT remove unverifiable claims ΓÇö flag them instead

## Step 5 ΓÇö Present results

Summarize in chat:
- Total claims checked
- Issues found (by severity)
- Per-issue details: what changed, why, source URL with tier
- Ask if the user wants to commit changes

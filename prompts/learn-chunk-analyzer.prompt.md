---
mode: agent
description: Analyze how Microsoft Learn content chunks and surfaces for a search query or article URL. Returns a structured report with chunk inventory, relevance scoring, pattern findings, and recommendations.
tools:
  - microsoft-learn-mcp-server/microsoft_docs_search
  - microsoft-learn-mcp-server/microsoft_docs_fetch
  - microsoft-learn-mcp-server/microsoft_code_sample_search
  - edit/createFile
  - read/readFile
---

# Learn Chunk Analyzer

Analyze how Microsoft Learn content is chunked and surfaced by the Learn MCP server.

## Input

The user provides either:
- A **search query** ΓÇö run `microsoft_docs_search` and analyze all returned chunks
- An **article URL** ΓÇö run `microsoft_docs_fetch` and simulate how the page would be chunked by section

If the input is ambiguous, ask the user which one they mean before proceeding.

## What to produce

A structured **Chunk Analysis Report** with:

1. **Chunk inventory table** ΓÇö every result listed with: article title, section heading, character count, detected deployment method (portal/CLI/PowerShell/ARM/Bicep/Terraform), and relevance rating

2. **Relevance ratings** for each chunk:
   - Γ£à **Direct** ΓÇö directly answers the query
   - ΓÜá∩╕Å **Partial** ΓÇö related but incomplete or missing key steps
   - ≡ƒöÇ **Tangential** ΓÇö same topic area, different task or scenario
   - Γ¥î **Noise** ΓÇö wrong method, post-task step, or unrelated service

3. **Signal summary** ΓÇö check all 7 patterns and report which are present:
   - **A ΓÇö Same-article duplication**: > 2 results from one article
   - **B ΓÇö Procedure truncation**: chunk ends mid-procedure
   - **C ΓÇö Method cross-contamination**: wrong deployment method in results
   - **D ΓÇö Orphaned intro chunk**: intro-only chunk with < 600 chars
   - **E ΓÇö Missing URLs**: blank `url` field on any result
   - **F ΓÇö Post-task noise**: downstream steps returned for an earlier-task query
   - **G ΓÇö Oversized sections** (URL only): sections > 2,500 chars likely to be split

4. **Key observations** ΓÇö 3ΓÇô5 prose findings with specific evidence

5. **Recommendations** split into two audiences:
   - **For article authors** ΓÇö structural changes to the markdown (H2 naming, section grouping, procedure completeness)
   - **For pipeline / platform** ΓÇö MCP server, chunk size config, metadata tagging, deduplication

6. **Signal-to-noise ratio**: `(Direct + Partial) / Total ├ù 100` ΓÇö rate as Good (ΓëÑ70%), Moderate (50ΓÇô69%), or Poor (<50%)

## Report format

```markdown
# Chunk Analysis Report

**Date**: YYYY-MM-DD
**Input type**: Search query / Article URL
**Query / URL**: [value]
**Results returned**: N chunks from N unique articles
**Signal ratio**: N% ([rating])

---

## Chunk inventory

| # | Article | Section heading | Chars | Method | Relevance |
|---|---------|-----------------|-------|--------|-----------|

---

## Signal summary

| Pattern | Detected | Detail |
|---------|----------|--------|
| A ΓÇö Same-article duplication | Γ£à/Γ¥î | |
| B ΓÇö Procedure truncation | Γ£à/Γ¥î | |
| C ΓÇö Method cross-contamination | Γ£à/Γ¥î | |
| D ΓÇö Orphaned intro chunk | Γ£à/Γ¥î | |
| E ΓÇö Missing URLs | Γ£à/Γ¥î | |
| F ΓÇö Post-task noise | Γ£à/Γ¥î | |
| G ΓÇö Oversized sections | Γ£à/Γ¥î | |

---

## Key observations

### 1. [Title]
[Detail with specific chunk evidence]

---

## Recommendations

### For article authors
**1.** [Recommendation]

### For pipeline / platform
**1.** [Recommendation]

---

## Most relevant chunks
[Top 2ΓÇô3 chunks that best answer the query]

## Least relevant chunks
[Chunks that should not have been returned and why]
```

## Output options

- Default: present the full report in chat
- If user says "save the report" or "write to file": save as `chunk-analysis_[slug]_YYYYMMDD.md` in the workspace root using `createFile`

## Rules

- DO analyze every returned chunk ΓÇö don't skip any
- DO check all 7 patterns (AΓÇôG) and report each explicitly
- DO provide at least 3 specific, actionable recommendations
- DO use `microsoft_docs_fetch` to get full content for any truncated chunk before assessing truncation
- DO note character counts for all chunks
- DO calculate and report the signal-to-noise ratio
- DO NOT skip the pattern checklist ΓÇö all 7 must appear in the report even if not detected

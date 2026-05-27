---
name: learn-chunk-analyzer
description: >-
  Analyze how Microsoft Learn content is chunked and surfaced by the Learn MCP server.
  Accepts a search query or a direct article URL. Returns a structured report showing
  how chunks are sized and bounded, how relevant each chunk is to the query, what content
  is duplicated or missing, and concrete recommendations for improving article structure
  to produce better RAG retrieval results.
argument-hint: "Provide a search query or a Learn article URL ΓÇö e.g., 'query: How do I configure Azure Firewall' or 'url: https://learn.microsoft.com/azure/firewall/...'"
user-invocable: true
---

# Learn Chunk Analyzer

Analyze how Microsoft Learn content is chunked and surfaced by the Learn MCP server for a given search query or article URL. Produces a structured report with chunk inventory, relevance scoring, pattern observations, and actionable recommendations for authors and pipeline engineers.

## When to use

- Diagnosing why an AI assistant gives incomplete or inaccurate answers from Learn content
- Auditing an article before publication to verify it will chunk and retrieve well
- Investigating why irrelevant articles surface for a specific query
- Evaluating how a multi-method article (portal + CLI + Bicep + Terraform) chunks across methods
- Generating evidence for improving article structure in a PR or work item

## Workflow

### Step 1 ΓÇö Identify input type

Determine whether the user provided a **search query** or an **article URL**.

| Input | Detection | Action |
|-------|-----------|--------|
| Search query | Plain text question or phrase | Run `microsoft_docs_search` with the query |
| Learn URL | Starts with `https://learn.microsoft.com` | Run `microsoft_docs_fetch` to retrieve the page |
| Both | User provides a query AND says "check this URL" | Run both tools; correlate results |

If the input is ambiguous, ask: _"Is this a search query to run, or a URL to analyze directly?"_

---

### Step 2 ΓÇö Fetch content

#### For a search query

Run `microsoft_docs_search` with the user's query. Capture all returned results.

For each result record:
- **Result number** (position in results list)
- **Article title** (from `title` field)
- **URL** (from `url` field ΓÇö note if blank)
- **Section heading** (first H2 or H3 found in the content)
- **Content length** in characters
- **Deployment method** if detectable (portal, CLI, PowerShell, ARM, Bicep, Terraform)
- **Article origin** ΓÇö whether this chunk shares a title with another result (same-article duplicate)

#### For a URL

Run `microsoft_docs_fetch` on the URL. Then simulate chunking by:
1. Identifying every H2 and H3 heading in the fetched content
2. Estimating the char count for each section (text between headings)
3. Flagging sections that would likely be split across chunk boundaries (> 2,500 chars)
4. Identifying sections that are too small to be useful standalone chunks (< 500 chars)

---

### Step 3 ΓÇö Inventory chunks

Build the chunk inventory table. For a **query**, include all returned results. For a **URL**, include all sections found.

```
| # | Article / Section | H2/H3 Heading | Chars | Method | Relevance | Notes |
|---|-------------------|---------------|-------|--------|-----------|-------|
| 1 | Quickstart: Create VNet / Create a resource group | ## Create a resource group | 1,822 | Portal | Γ£à Direct | ΓÇö |
| 2 | Quickstart: Create VNet / Review the template | ## Review the template | 1,729 | ARM | Γ¥î Noise | Wrong method |
```

**Relevance ratings** (see [references/chunk-scoring-rubric.md](references/chunk-scoring-rubric.md)):

| Rating | Meaning |
|--------|---------|
| Γ£à Direct | Chunk directly answers the query |
| ΓÜá∩╕Å Partial | Related but incomplete ΓÇö missing key steps or context |
| ≡ƒöÇ Tangential | Same topic area but different task or scenario |
| Γ¥î Noise | Wrong method, post-task step, or unrelated service |

---

### Step 4 ΓÇö Identify patterns

After building the inventory, analyze the full result set for these patterns. Check each one and note findings.

#### Pattern A ΓÇö Same-article duplication
Count how many results share the same article title. Flag if > 2 results come from one article.
> _Signal_: Scoring is not penalizing same-article chunks; breadth is being sacrificed for depth.

#### Pattern B ΓÇö Procedure truncation
Check if any chunk ends mid-procedure (numbered steps that don't reach a terminal action like "Select **Create**" or "Select **Review + create**").
> _Signal_: Chunk boundary falls inside a procedural section; the user gets incomplete steps.

#### Pattern C ΓÇö Method cross-contamination
Check if chunks returned for a method-specific query (e.g., "portal") contain steps for other deployment methods (CLI, PowerShell, ARM, Bicep, Terraform).
> _Signal_: Multi-method articles aren't segmented by deployment method at the H2 level.

#### Pattern D ΓÇö Orphaned intro chunks
Check for chunks that contain only the article introduction (no H2, or H2 is the article overview) with < 600 chars.
> _Signal_: Intro sections chunked separately add no actionable content to retrieval results.

#### Pattern E ΓÇö Missing URLs
Check if any result has a blank or missing `url` field.
> _Signal_: Pipeline isn't passing source URLs through to chunk metadata; AI tools can't cite or link.

#### Pattern F ΓÇö Post-task noise
Check if any chunks returned are downstream steps irrelevant to the query (e.g., "Connect to a virtual machine" returned for "create a virtual network").
> _Signal_: Semantic similarity is matching on shared nouns (VM, VNet) rather than task intent.

#### Pattern G ΓÇö Oversized chunks (URL analysis only)
For URL analysis, flag sections > 2,500 chars that will likely be split mid-content.
> _Signal_: Section too long to survive chunking intact; split will break context.

---

### Step 5 ΓÇö Generate report

Output the full report using the template in [references/report-template.md](references/report-template.md).

Sections to include:

1. **Query / URL** ΓÇö What was analyzed
2. **Chunk inventory table** ΓÇö All chunks with relevance rating
3. **Signal summary** ΓÇö Which patterns were found (AΓÇôG checklist)
4. **Key observations** ΓÇö Prose explanation of the 3ΓÇô5 most important findings
5. **Recommendations** ΓÇö Split into two audiences:
   - **For article authors** ΓÇö structural changes to the article markdown
   - **For pipeline / platform** ΓÇö changes to the MCP server, chunking config, or embedding index

---

### Step 6 ΓÇö Offer to save

After presenting the report in chat, ask:
_"Would you like me to save this report as a markdown file in the workspace?"_

If yes, save as `chunk-analysis_[query-slug]_YYYYMMDD.md` in the workspace root.

---

## Report template

Use this structure for all reports:

```markdown
# Chunk Analysis Report

**Date**: YYYY-MM-DD
**Input type**: Search query / Article URL
**Query / URL**: [value]
**Results returned**: N chunks from N articles

---

## Chunk inventory

| # | Article | Section heading | Chars | Method | Relevance |
|---|---------|-----------------|-------|--------|-----------|
| N | ... | ... | N | ... | Γ£à/ΓÜá∩╕Å/≡ƒöÇ/Γ¥î |

---

## Signal summary

| Pattern | Detected | Detail |
|---------|----------|--------|
| A ΓÇö Same-article duplication | Γ£à Yes / Γ¥î No | N results from "[Article title]" |
| B ΓÇö Procedure truncation | Γ£à Yes / Γ¥î No | Result N cuts mid-procedure at step N |
| C ΓÇö Method cross-contamination | Γ£à Yes / Γ¥î No | Results N, N contain [methods] in [method]-specific query |
| D ΓÇö Orphaned intro chunk | Γ£à Yes / Γ¥î No | Result N is intro-only at N chars |
| E ΓÇö Missing URLs | Γ£à Yes / Γ¥î No | N of N results have blank URL field |
| F ΓÇö Post-task noise | Γ£à Yes / Γ¥î No | Results N, N are downstream steps |
| G ΓÇö Oversized sections | Γ£à Yes / Γ¥î No | (URL analysis only) N sections > 2,500 chars |

---

## Key observations

### 1. [Observation title]
[Explanation with specific evidence from chunk inventory]

### 2. [Observation title]
[Explanation]

---

## Recommendations

### For article authors

**1. [Recommendation title]**
[What to change and why, with a before/after example if helpful]

**2. [Recommendation title]**
[What to change and why]

### For pipeline / platform

**1. [Recommendation title]**
[What to change in the MCP server, embedding config, or retrieval pipeline]

---

## Most relevant chunks for this query

[List the 2ΓÇô3 chunks that best answer the query, with quotes from their content]

---

## Least relevant chunks returned

[List the chunks that should not have been returned, with explanation]
```

---

## Quality checklist

Before presenting the report, confirm:

- [ ] All returned chunks are listed in the inventory table
- [ ] Every chunk has a relevance rating with justification
- [ ] All 7 patterns (AΓÇôG) checked and reported
- [ ] Recommendations split between author and pipeline audiences
- [ ] At least 3 specific, actionable recommendations provided
- [ ] Chunk inventory shows character count for every result
- [ ] Missing URL field noted if any result has blank URL
- [ ] Same-article duplicates counted and flagged
- [ ] Report saved to file if user requested it

---

## Tool reference

| Tool | When to use |
|------|-------------|
| `microsoft_docs_search` | Fetch search results for a query (primary tool for query analysis) |
| `microsoft_docs_fetch` | Fetch full article content for URL analysis or to get complete context for a truncated chunk |
| `microsoft_code_sample_search` | If the query involves code samples ΓÇö check how code chunks are returned |

---

## Example invocations

```
@learn-chunk-analyzer query: How do I configure Azure Firewall DNAT rules in the portal
```

```
@learn-chunk-analyzer url: https://learn.microsoft.com/en-us/azure/virtual-network/quick-create-portal
```

```
@learn-chunk-analyzer Run a chunk analysis on "deploy Azure NAT Gateway" and save the report
```

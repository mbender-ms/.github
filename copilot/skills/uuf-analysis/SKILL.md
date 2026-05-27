---
name: uuf-analysis
displayName: UUF Analysis
version: 1.1.0
category: Analysis
description: Analyze and implement User Feedback (UUF) work item fixes with combined technical fix and editorial review. Use when the user says "analyze this UUF", "UUF analysis", "check this feedback item", or references a User Feedback work item. Handles single-item analysis, batch analysis reports, and closure workflow.
argument-hint: "[work item ID or 'batch' for all active UUF items]"
relevant-lesson-tags: [uuf, customer-feedback, ado, content-quality, editorial]
---

User Feedback work items require careful validation and analysis. Verify customer feedback against live docs before acting on it — customers may reference outdated versions or misunderstand existing docs.

## UUF Implementation Approach

When implementing UUF documentation fixes, use the combined approach:

1. **Technical Fix**: Address the specific customer-reported issue (incorrect value, broken code, missing info)
2. **Full Editorial Review**: Perform line-by-line Style Guide compliance check on the ENTIRE file
3. **Metadata Update**: Update `ms.date` in frontmatter to current date (MM/DD/YYYY format)
4. **AI Usage Tag**: Add `ai-usage: ai-assisted` to frontmatter after ms.date, but only if any text is added/generated, and not for minor formatting changes that don't involve generating text

**Metadata Requirements**:
- **ms.date format**: Use MM/DD/YYYY (e.g., `01/20/2026`)
- **ai-usage placement**: Add after ms.date, before ms.service
- **ai-usage value**: Use `ai-assisted` for content generated or significantly modified by AI
- **When to add ai-usage**: Add when generating changes, unless changes are only links, single words/phrases, less than 5% of word count, or just reformatting without new text

**Link Formatting Requirements**:
- Don't add locale codes to URLs (e.g., `/en-us/`, `/fr-fr/`) — they break auto-locale routing and cause 404s for non-English readers
- Remove locale codes from existing URLs when updating links
- **Applies to ALL links**: Microsoft.com, learn.microsoft.com, azure.microsoft.com, etc.

**Editorial Review Checklist** (apply to entire file):
- ✅ Active voice over passive voice
- ✅ Second person ("you") not third person ("the user")
- ✅ Contractions for conversational tone
- ✅ Present tense for descriptions
- ✅ Imperative mood for instructions
- ✅ Complete sentences in bullet lists (with periods)
- ✅ Method names without parentheses in prose
- ✅ Clear pronoun references
- ✅ Sentence structure improvements
- ✅ **"Related content" section at end**

Don't split into separate PRs — technical fixes and editorial improvements go together. Separate PRs double the review burden and risk merge conflicts.

## UUF Analysis Workflow

When asked about a User Feedback work item:

1. **Fetch Work Item Details** — Call `mcp_ado_wit_get_work_item` with expand="all". Extract: `Custom.FeedbackVerbatim`, `Custom.LiveUrl`, `Custom.FeedbackReason`, `Custom.ArticleTitle`, `System.Description`

2. **Normalize Live URL to en-us Locale** — Feedback can be submitted in any locale. Convert `learn.microsoft.com/{locale}/` → `learn.microsoft.com/en-us/` so you fetch the canonical English version.

3. **Fetch Live Documentation** — Call `mcp_microsoft-doc_microsoft_docs_fetch` with the en-us normalized URL

4. **Search Related Documentation** — Call `mcp_microsoft-doc_microsoft_docs_search` with relevant keywords

5. **Reconcile Customer Feedback with Documentation** — Compare customer statement vs. actual content. Identify gaps. Assess validity. Determine action.

6. **Generate Analysis Summary**:
   ```markdown
   ## UUF Analysis: [Work Item ID]
   ### Customer Feedback
   - **Verbatim**: [Customer's exact words]
   - **Issue Type**: [Reason code]
   - **Article**: [Title and URL]
   ### Current Documentation Status
   - **Content Review**: [What the doc currently says]
   - **Coverage**: [Is the topic addressed? How well?]
   ### Gap Analysis
   - **Customer's Point**: [What they're claiming]
   - **Documentation Reality**: [What's actually in the doc]
   - **Reconciliation**: [Is customer right, wrong, or partially correct?]
   ### Recommended Action
   - [ ] **Documentation Update Needed**: [Specific changes]
   - [ ] **No Action Required**: [Why customer is incorrect]
   - [ ] **Clarification Needed**: [Areas needing better explanation]
   ### Proposed Changes (if applicable)
   - [Specific edits following Microsoft Writing Style Guide]
   ```

## UUF-Specific Guidelines
- **Verify verbatim against live docs** — customers sometimes describe outdated or incorrect behavior
- **Consider context** — Customer may have misunderstood or used outdated info
- **Search broadly** - Topic might be covered in related articles
- **Be specific** - Identify exact gaps or inaccuracies
- **Propose actionable fixes** - Not just "improve clarity"

## Common UUF Scenarios
1. **Customer is correct** → Propose specific content additions/corrections, create User Story
2. **Customer is incorrect** → Explain what doc says, suggest clarification improvements, close UUF
3. **Documentation unclear** → Propose restructuring, add examples/guidance, improve discoverability

## UUF Batch Analysis Workflow

**When analyzing multiple active UUF items**, create a comprehensive **HTML report** combining batch prioritization AND detailed individual analysis.

**Output**: HTML file at `{SESSION_DIR}\uuf-analysis\uuf-analysis-YYYY-MM-DD.html`

**Report Content Structure:**
- **Part 1: Batch Portfolio Analysis** — Executive summary, priority ranking using T+A+E scoring (see below), systemic patterns, 4-week action plan
- **Part 2: Individual Item Analysis** — For EACH item: fetch live doc, reconcile feedback, generate analysis

### UUF Priority Scoring (T + A + E = Score /10)

Each item receives three sub-scores that sum to a maximum of 10.

**T - Traffic (0-5)**

| Points | Pageviews |
|--------|-----------|
| 5 | 4,000+ |
| 4 | 2,000-3,999 |
| 3 | 1,000-1,999 |
| 2 | 500-999 |
| 1 | < 500 |

**A - Accuracy impact (0-3)**

| Points | Meaning |
|--------|---------|
| 3 | Customer report is fully valid and identifies a technical error (factually wrong content) |
| 2 | Customer report is fully valid but identifies a usability/clarity gap (not a factual error) |
| 1 | Customer report is partially valid (some claims wrong, underlying issue real) |
| 0 | Customer report is invalid |

**E - Effort bonus (0-2)**

| Points | Meaning |
|--------|---------|
| 2 | Fix is a quick targeted note or single-paragraph addition |
| 1 | Fix requires a section update or screenshot refresh |
| 0 | Fix requires major restructure, new diagrams, or PM validation |

**Tier thresholds:**

| Score | Tier | Color |
|-------|------|-------|
| 9-10 | Critical | Red (#d13438) |
| 7-8 | High | Amber (#ffb900) |
| 5-6 | Medium | Blue (#0078d4) |
| 0-4 | Low | Grey (#8a8886) |

**Display format**: Each score cell shows a large colored number (/10) with sub-scores underneath in small grey text (e.g., T5 - A3 - E2). Score color matches tier. A legend card above the table explains all three dimensions.

**Implementation Steps:**
1. Retrieve all active UUF items via `mcp_ado_wit_my_work_items` filtered for User Feedback
2. Create batch portfolio analysis with priority scores
3. Perform detailed 6-step analysis on each item (normalize URL, fetch doc, search, reconcile)
4. Save combined HTML report

**HTML Styling** — Use same pattern as monthly reports:
- Purple gradient body background (`linear-gradient(135deg, #667eea 0%, #764ba2 100%)`)
- White container with `border-radius: 16px` and heavy shadow
- CSS variables: `--primary-color: #0078d4`, `--success-color: #107c10`, `--warning-color: #ffb900`, `--danger-color: #d13438`
- Metric cards with gradient backgrounds and left border accents
- Priority cards color-coded (red=critical, yellow=medium, green=addressed)
- Bar charts with vibrant gradients for product area distribution

## UUF PR Justification

When creating PRs for UUF fixes, include a detailed justification section — reviewers need to understand why each change was made, and the customer impact context speeds up approvals.

Each fix includes:
1. **Work Item**: AB#{ID} reference
2. **Staged Article Link**: Link to review.learn.microsoft.com with section bookmark
3. **Justification**: Customer report quote + why change is necessary + impact

```markdown
## Fix {N}: [Brief Title]
**Work Item**: AB#{ID}
**File**: `path/to/file.md`
**Staged Article**: [Article Title](https://review.learn.microsoft.com/en-us/...?branch=pr-en-us-{PR_NUMBER}#{section-bookmark})
**Customer Report**: "[exact customer feedback quote]"
**Why This Change Is Necessary**:
- [Technical reason]
- [Customer impact]
- **Impact**: {N} monthly readers [benefit description]
```

## UUF Closure Workflow

When closing User Feedback work items after PR merge:

1. **State**: Set to **Closed** (NOT Resolved)
   - User Feedback items use Closed state as final state
   - Active is an intermediate state
   - Use `System.State: "Closed"` in ADO updates

2. **IterationPath**: Update to **current month iteration**
   - Format: `{ADO_PROJECT}\FY26\Q3\01 Jan` (example for January 2026)
   - Use the month iteration when the work was completed, not when created — this keeps monthly reporting and capacity tracking accurate
   - Helps with accurate monthly reporting and capacity tracking
   - Use month-level path (e.g., "01 Jan"), not quarter-level

3. **Completion Comment**: Add markdown-formatted comment with:
   - ✅ emoji header
   - PR reference with markdown link
   - Changes made summary
   - Customer impact statement
   - Use `format: "markdown"` parameter in `mcp_ado_wit_add_work_item_comment`

**Example ADO Update:**
```json
{
  "id": 305743,
  "op": "Replace",
  "path": "/fields/System.State",
  "value": "Closed"
},
{
  "id": 305743,
  "op": "Replace",
  "path": "/fields/System.IterationPath",
  "value": "Content\\FY26\\Q3\\01 Jan"
}
```

**Why This Matters**:
- Closed state indicates final resolution (not just "fix identified")
- Current iteration tracking enables accurate monthly reporting
- Completed work counts toward the correct sprint/month metrics
- Managers can see actual completion trends by iteration

---
name: connect-metrics
version: 2.1.0
category: Reports
description: Gather, validate, and visualize semester metrics for the biannual Connect review. Use when the user says "gather connect metrics", "connect metrics", "run my connect summary from X to Y", "gather connect data", or "build the metrics dashboard". Produces an HTML data dashboard with PR tables, ADO work item summaries, and executive summaries per product area. Run this before the connect-review skill.
argument-hint: '"from {start month} to {end month}" (e.g., "from november 2025 to april 2026")'
relevant-lesson-tags: [connect, metrics, ado, github, monthly-report]
---

## Step 0: Configuration Discovery (start here)

Before any data gathering, the following configuration values are needed. Present this list to the user first, then offer to auto-discover what you can.

**Required configuration:**

| # | Field | What it's used for |
|---|-------|--------------------|
| 1 | **Product areas** | Categorizing work items and PRs by owned area |
| 2 | **ms.service values** | Power BI visitor queries + article count grep |
| 3 | **ms.subservice values** | Subservice breakdown in Power BI |
| 4 | **Repo folders** | Folder paths per product area for article counting |
| 5 | **ADO AreaPaths** | Categorizing ADO work items by product area |
| 6 | **GitHub username** | PR author search on GitHub |
| 7 | **Git author aliases** | git log filtering |
| 8 | **ADO project** | ADO API calls |
| 9 | **Repo name** | GitHub API calls (owner/repo) |
| 10 | **PR review tracking Feature ID** | Finding PRs reviewed (Phase 5) |
| 11 | **Epic IDs** | Classifying Feature vs Maintenance work - need both New Content and Maintenance epic IDs |
| 12 | **Connect data directory** | Where to save intermediate JSON/JSONL files |
| 13 | **Connect output directory** | Where to save final HTML dashboard |

> **Tip:** The `connect-goals` extension skill generates a `GOALS.md` file with auto-refreshed SMART goal progress. If the user has run `/connect-goals setup`, read `GOALS.md` alongside the agent file during this step.

**Workflow:**

1. **Present the list**: Show the user all 13 fields above and explain: "I need these configuration values to gather your Connect metrics accurately."

2. **Offer auto-discovery**: Tell the user: "I can attempt to auto-discover most of these by querying your ADO work items and GitHub PRs. This will help me find your product areas, AreaPaths, repo folders, and other values from your actual work history. Want me to proceed?"

3. **Wait for approval**: Do not query anything until the user confirms.

4. **Run auto-discovery** (after user approves):
   - Read the agent file for any explicitly configured values
   - Query `mcp_ado_wit_my_work_items` to discover AreaPaths, product areas, and Epic IDs from recent work items
   - Query `mcp_github_list_pull_requests` to discover repo folders and ms.service values from PR file paths
   - Check `mcp_github_get_me` for GitHub username
   - Look at the repo structure for folder paths

5. **Present findings**: Show the user what you found in a checklist:
   - ✅ **Found**: field name -> discovered value
   - ❌ **Not found**: field name -> what you need from the user

6. **Ask the user to validate and fill gaps**: "Please review what I found and correct anything that's wrong. For the items I couldn't find, please provide the values."

7. **Handle storage directories (fields 12-13):**
   - If found in the agent file, confirm with the user
   - If not found, suggest a sensible default and ask for confirmation
   - Create the directory structure once confirmed

8. Once all 13 fields are confirmed, proceed to Quick Run Command

---

## Quick Run Command

**"run my connect summary from {DATE1} to {DATE2}"**:

1. Run Step 0 (agent file check) — stop if fields are missing
2. Set `START={DATE1}`, `END={DATE2}`, `END_PLUS_1={DATE2 + 1 day}`
3. Create intermediate data folder if it doesn't exist:
   ```bash
   mkdir -p "{connect-folder}/output/connect-metrics/"
   ```
4. Execute phases in order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10
5. Present for user review after each tagging step
6. If files already exist, ask before overwriting

---

## Phase Dependency Map & Parallelization Guide

**Running all 11 phases sequentially takes a long time.** Use subagents to parallelize independent work.

```
WAVE 1 (parallel — no dependencies):
  ├── Subagent A: Phase 1 (ADO Work Items) + Phase 1 Step 6 (Parent Hierarchy)
  ├── Subagent B: Phase 6 (Article Counts + Power BI MAU)
  └── Subagent C: Phase 5 Steps 1-2 (PR Review tracking — only needs Feature ID from agent file)

WAVE 2 (parallel — depends on Wave 1A):
  ├── Subagent D: Phase 2 (Extract PRs from ADO descriptions + GitHub search)
  │                ↳ needs ADO work items from Wave 1A
  └── Subagent E: Phase 11 Steps 1-3 (Read session summaries for narrative context)
  
WAVE 3 (sequential — depends on Wave 2D):
  └── Phase 3 (Per-PR Metrics via gh CLI) — SLOWEST PHASE, ~2 min for 50+ PRs
      Consider: run as background terminal with isBackground=true

WAVE 4 (parallel — depends on Waves 1-3):
  ├── Phase 4 (Categorize PRs — needs ADO hierarchy + PR data)
  ├── Phase 5 Steps 3-5 (Merge PR review data — needs PR stats)
  └── Phase 7 (Conference summary — needs categorized PRs)

WAVE 5 (sequential — needs all above):
  └── Phase 8 (Cross-referential verification)

WAVE 6 (parallel):
  ├── Subagent F: Phase 9 (Generate HTML — needs all data)
  └── Subagent G: Phase 10 (Executive summaries — needs session summaries + data)
```

**Subagent prompts should include:**
- The Connect period dates (START, END)
- Agent file field values (product areas, ms.service values, GitHub username, etc.)
- The Connect data directory path for saving output files
- Explicit instruction on what JSON/JSONL file to save results to

**What CANNOT be parallelized:**
- Phase 3 (PR metrics) depends on Phase 2 output (PR numbers)
- Phase 4 (categorization) depends on both Phase 1 (hierarchy) and Phase 3 (PR data)
- Phase 8 (verification) needs everything
- Phase 9 (HTML generation) needs everything

**Recommended approach for fastest execution:**
1. Run Wave 1 with 3 parallel subagents (ADO, Power BI, PR reviews)
2. Run Wave 2 when ADO data is ready
3. Start Phase 3 as background terminal while reading session summaries
4. Run Waves 4-6 sequentially after Phase 3 completes

---

## Token Budget Optimization (CRITICAL)

This skill gathers large volumes of data across 11 phases. Without careful management, context will overflow before Phase 9 can generate the report. Follow these rules strictly.

### Rule 1: Write intermediate data to files, not context

Every phase saves its output to `output/connect-metrics/` as a JSON file. Subsequent phases read only what they need from those files. Never rely on conversation context to pass data between phases.

| Phase | Output file |
|-------|-------------|
| 1 | `phase1-ado-items.json` |
| 2 | `phase2-pr-numbers.json` |
| 3 | `phase3-pr-metrics.json` |
| 4 | `phase4-pr-categories.json` |
| 5 | `phase5-pr-reviews.json` |
| 6 | `phase6-article-counts.json` |
| 7 | `phase7-conference-summary.json` |
| 8 | `phase8-verification.json` |

### Rule 2: Summarize before accumulating

After fetching raw API data, immediately summarize to a compact format and discard the raw response. For example:
- **ADO items**: Keep only ID, title, state, type, closedDate, areaPath, storyPoints. Drop full HTML descriptions.
- **PR metrics**: Keep only PR number, title, files changed, additions, deletions, merged date, author. Drop full diff content.
- **Work item batch-fetch**: Request only the fields you need in the `fields` parameter, never fetch all fields.

### Rule 3: Subagents get clean context

Each subagent receives only the configuration values and the specific phase instructions it needs. It writes results to the designated JSON file. The parent agent reads the file afterward - it never receives the raw subagent output through context.

### Rule 4: Use read_file selectively

When a later phase needs data from an earlier phase, use `read_file` to read only the specific JSON file, not the entire output folder. Parse what you need and move on.

### Rule 5: Use optimal tools

- Use `read_file` directly to read files - never `Get-Content`, `cat`, or `wc -l` in terminal
- Use `grep_search` and `file_search` for workspace searches - never `select-string` or `find` in terminal
- Use `list_dir` to browse directories - never `ls` or `dir` in terminal
- Prefer MCP tool calls over terminal commands whenever possible

---

## Phase 1: ADO Work Items (START HERE)

ADO is the source of truth. It defines Features, User Stories, UUF items, and links to PRs.

**Step 1**: Fetch all assigned items:
```
mcp_ado_wit_my_work_items(type="assignedtome", includeCompleted=true, top=200, project="{ADO_PROJECT}")
```
⚠️ Max 200 items. Check `hasMore` flag.

**Step 2**: Extract IDs, batch-fetch with key fields (batches of 100):
```
fields=["System.Id", "System.Title", "System.State", "System.WorkItemType",
        "Microsoft.VSTS.Common.ClosedDate", "System.CreatedDate",
        "System.AreaPath", "System.Tags", "System.Parent",
        "Microsoft.VSTS.Scheduling.StoryPoints", "System.Description"]
```

**OPTIMIZATION**: Include `System.Description` here so Phase 2 doesn't need to re-fetch. Extract PR links (`/pull/(\d+)`, `pr-en-us-(\d+)`, `PR\s*#?(\d{4,6})`) from descriptions during this batch fetch and store them alongside work item data.

**Step 3**: Filter to Connect period (closed in period, created in period, or still active).

**Step 4**: Categorize by product area using AreaPaths from agent file + title keyword fallback.

**Categorization rules** (applied in order — first match wins):
1. **AreaPath match**: Check if item's AreaPath contains a known product area substring from agent file
2. **Keyword-based detection**: If the agent file defines secondary area keywords (e.g., AreaPath contains a keyword OR title matches a pattern), use those to create separate categories. This prevents niche areas from being merged into a general bucket.
3. **Title keyword match**: For items with generic AreaPaths, scan title for product-specific keywords from the agent file
4. **Team/Admin detection**: Title contains patterns like 'reviews for', 'UAT', 'link farm', 'mock', 'extension tracking', 'tiger team'
5. **Fallback**: Items not matching any rule go to 'Other'

Keep keyword-detected areas as their own categories in the ADO table — merging them into general buckets obscures work that managers track separately. Typically 8-10 groups (e.g., {Area1}, {Area2}, {Area3}, {Area4}, Team/Admin, Other). Each group header shows the item count.

**Step 5**: Separate Features vs User Stories vs User Feedback vs Tasks.

**Step 6 — Build parent hierarchy (essential for Phase 4)**:
The ADO hierarchy determines work type (Feature vs Maintenance) — walk the full hierarchy to get accurate classification.

1. Collect all unique `System.Parent` IDs from filtered items
2. Batch-fetch parent work items with fields: `System.Id`, `System.Title`, `System.WorkItemType`, `System.Parent`, `System.Tags`, `System.State`
3. These parents are typically **Features**. Collect THEIR `System.Parent` IDs (the Epic layer)
4. Batch-fetch grandparent work items (Epics) with same fields
5. Build a lookup map: `workItemId → { parentId, parentTitle, parentType, epicId, epicTitle }`
6. Classify each work item:
   - If epicId = New Content epic ID from agent file → `workType: 'Feature'`
   - If epicId = Q+I/Maintenance epic ID → `workType: 'Maintenance'`
   - Fallback: check `System.Tags` for `new-feature` tag
7. Extract conference tags from `System.Tags` on each work item (e.g., `Ignite-2025`, `SQLCon`)

Save hierarchy to: `{monthYYYY}/parent-hierarchy.json`
Save work items to: `{monthYYYY}/ado-items.json`

---

## Phase 2: Extract PRs from ADO Descriptions + GitHub

**Step 1 — ADO Description extraction (essential)**:

This step discovers 20-30% of PRs that GitHub author search can't find. Skipping it causes significant undercount (e.g., 53 PRs found vs 70 actual), so always run it before GitHub search.

**OPTIMIZATION**: If Phase 1 Step 2 already fetched `System.Description`, use those cached descriptions here instead of re-fetching. Only re-fetch if Phase 1 did NOT include descriptions.

Parse the HTML descriptions for PR patterns:
- `/pull/(\d+)` — GitHub PR URLs in description
- `pr-en-us-(\d+)` — staging server branch references
- `PR\s*#?(\d{4,6})` — plain text PR references

**Why this matters**: Work items like PR review tracking items, UAT items, and many User Stories contain PR links in their Description field that are NOT discoverable via GitHub author search (because those PRs may be authored by others, or lack AB# links in the PR body). This is the PRIMARY PR discovery method.

**Step 2 — GitHub author search (dual query)**: Run two searches to catch all PRs — using only `created:` misses PRs created before the period but merged during it:
```
# PRs CREATED during period
mcp_github_search_pull_requests(query="author:{GITHUB_USERNAME} created:{START}..{END}", ...)

# PRs MERGED during period (catches PRs created before but merged during)
mcp_github_search_pull_requests(query="author:{GITHUB_USERNAME} merged:{START}..{END}", ...)
```
Extract `AB#(\d+)` from PR bodies for ADO cross-references.

**Step 3**: Merge ALL sources (ADO descriptions + both GitHub searches). Deduplicate by PR number. Build bidirectional maps: `adoToPR` and `prToADO`.

Save to: `{monthYYYY}/github-prs.json`

---

## Phase 3: Per-PR Metrics via GitHub API

Don't use git merge commit diffs — they conflate multiple authors' work and inflate your personal metrics.

**PREFERRED — Batched MCP calls** (faster than sequential `gh` CLI):
Use `mcp_github_pull_request_read` with `method: "get"` for each PR. This returns `additions`, `deletions`, `changed_files`, `merged_at`, `state`, `title` in one call. Run up to 5 in parallel if your agent supports parallel tool calls.

**FALLBACK — `gh` CLI** (if MCP is slow or unavailable):
```bash
gh pr view {PR_NUMBER} --repo {REPO} --json number,title,state,additions,deletions,changedFiles,mergedAt,files
```

**BATCH OPTIMIZATION for 50+ PRs**: Write a node script that uses the GitHub GraphQL API to fetch all PRs in batches of 20:
```bash
# Save to doc-work-scripts/connect/fetch-pr-stats.js and run:
node fetch-pr-stats.js --prs "35537,35582,..." --repo {GITHUB_OWNER}/{GITHUB_REPO} > gh-pr-stats.jsonl
```
This reduces 50+ sequential API calls to 3-4 batched GraphQL queries (~10 seconds vs ~2 minutes).
Save to: `{monthYYYY}/gh-pr-stats.jsonl`

⚠️ Use `winpty node.exe` on Windows Git Bash. Run as background task if >50 PRs (~2 min).

**Step 2**: Classify files per PR:
- **New articles**: `.md` where `deletions === 0 && additions > 5` AND path NOT in `/includes/`
- **Updated articles**: All other `.md` files (includes count as updated, not new)
- **Images**: `.png`, `.jpg`, `.gif`, `.svg`, `.webp`
- **Lines**: Use `additions` and `deletions` from GitHub API

**Step 3**: Filter out:
- Closed PRs (abandoned/superseded — state === 'CLOSED')
- Batch shiproom PRs (200+ files, multiple authors)
- **Release-to-release branch merge PRs** — PRs that merge one release branch into another (e.g., `release-ignite-2025` → `release-sqlcon-2026`, or `main` → `release-*`). These are internal branch management, NOT content work. They inflate metrics because they contain all commits from the source branch. Detect by: PR base branch and head branch both being release branches, or PR title containing patterns like `Merge release`, `merge branch`, `sync release`.
- Excluded PRs (image indexes, mock TOCs — ask user to confirm exclusion list)

Save to: `{monthYYYY}/pr-details.json`

---

## Phase 4: Categorize, Tag, and Classify PRs

Assign product area, work type (Feature vs Maintenance), GA/Preview/New status, and conference tags to each PR. The ADO work item hierarchy is the source of truth for classification — title keywords are only fallbacks for unlinked PRs.

> **Reference file:** See [references/phase-4-categorization.md](references/phase-4-categorization.md) for the full 5-step categorization workflow, feature name derivation rules, and conference tag detection methods.

---

## Phase 5: PR Reviews from ADO + Reports

Use the PR review tracking Feature ID from agent file (not GitHub search). Supplement with session summaries if available.

**Step 1**: Get children of PR review Feature via `expand="relations"`.

**Step 2**: For each child in the Connect period, fetch Description, extract PR numbers (`/pull/NNNNN`).

**Step 2b — Session summaries (supplemental source)**:
- If session summaries exist for the Connect period (`/Reports/session-summaries/YYYY-MM/md/`), scan them for PR review mentions
- Look for patterns: "PR review", "reviewed PR #NNNNN", "inline suggestions", "pr-reviews/" file references
- Extract any PR numbers from review context that aren't already in the `reviewPRSet`
- Session summaries capture reviews done outside the formal ADO tracking (e.g., quick reviews without dedicated work items, ad-hoc reviews during other work)
- This is a supplemental source — ADO PR review tracking work items (Steps 1-2) remain primary

**Step 3**: Fetch GitHub data for any PRs not already in `gh-pr-stats.jsonl`.

**Step 4 — Classify as Review (use PR Review tracking, not author field)**:
- Don't use `pr.author !== '{GITHUB_USER}'` to detect reviews — this fails because:
  - PRs found through ADO description extraction (Phase 2 Step 1) don't have reliable author info
  - Many review PRs default to the assigned user's GitHub handle as author when fetched through ADO sources
- **CORRECT approach**: Any PR number that appears in PR Review tracking work item descriptions (from Steps 1-2) OR in session summary review context (Step 2b) is classified as Review, **regardless of what the author field says**.
- Build a `reviewPRSet` from Step 2 + Step 2b output (union of both sources)
- For each PR in `pr-details.json` where `reviewPRSet.has(pr.number)`: set `workType: 'Review'`, `prTableCategory: 'PR Reviews'`
- This overrides any previous category assignment from Phase 4

**Step 5**: Fix merge states — verify `mergedAt` from GitHub API. Deduplicate across months.

---

## Phase 6: Article Counts and MAU from Power BI

Count articles per product area using `ms.service` grep, then query Power BI for visitor and page view averages across the Connect period.

> **Reference file:** See [references/phase-6-article-counts.md](references/phase-6-article-counts.md) for DAX queries, MSSubService value mappings, and the Phase 6 JSON output format.

---

## Phase 7: Conference Contributions Summary

Aggregate merged PRs by conference tag. Collect per-conference:
- PR count (total tagged with that conference)
- New articles, Updated articles, Lines added, Lines removed, Images
- New features count (PRs tagged both Feature + conference)
- Features going GA count (PRs tagged Feature + conference where ADO title contains `ga`, `going ga`, `publish`)

This data feeds the **Conference Contributions table** in Phase 9 Section 2.

---

## Phase 8: Cross-Referential Verification

Before generating HTML, verify:

1. **PR count**: `pr-details.json` count = sum across all product area tables
2. **ADO ↔ PR bidirectional**: Every ADO item's description PRs are in the PR list; every PR's AB# items are in the ADO list
3. **Feature deduplication**: Same feature via multiple PRs → listed once (e.g., 3 ESU PRs = 1 feature)
4. **GA/Preview accuracy**: Cross-check ADO title keywords against parent Feature title
5. **Merge state**: PRs showing "open" but with `mergedAt` → fix to "merged"
6. **No repo contamination**: `git status --porcelain` in repo = clean
7. **Include files excluded from "new"**: No `/includes/*.md` in new article count
8. **No closed PRs in tables**: Only merged + open
9. **No duplicate rows**: Each PR appears exactly once in exactly one product area
10. **Per-area copy block ↔ Combined Metrics Table consistency**: Sum of per-area copy block values (Section 4A) must match the Combined Metrics Table (Section 6) values for New articles, Updated articles, Lines added/removed, and Images. Do NOT use `pr-details.json` raw values for the Combined Metrics Table — use the verified copy block values.
11. **Key Metrics total ↔ all-area sum**: The Key Metrics section (Section 1) totals include ALL areas (including PR Reviews, Team/Admin, Shared). The Combined Metrics Table TOTAL column only sums the 4 main product areas. These will differ — document this clearly.

---

## Phase 9: Generate HTML Dashboard

Build the visual dashboard from accumulated data. Read the full spec for CSS classes, section structure, and copy-friendly formatting requirements.

> **Reference file:** See [references/html-dashboard-spec.md](references/html-dashboard-spec.md) for all 8 sections, required CSS badge classes, and table formatting rules.

---

## Phase 10: Write Per-Area Executive Summaries

Generate high-level executive summaries of work per product area for the Connect review. These summaries are written for the manager and skip-level audience.

### Data Sources (ALL required — read before writing)

1. **Connect review data** (`connect-review-data.html` and `connect-database.json`) — per-area metrics, feature lists, PR counts
2. **Session summaries** (`/Reports/session-summaries/YYYY-MM/md/`) — daily accomplishment details, decisions, technical context
3. **1:1 reports** (`/Reports/1-1s/YYYY-MM/md/`) — weekly work stream summaries
4. **Monthly reports** (`/Reports/monthly-reports/md/`) — monthly big rocks, customer impact, cross-team work

### Writing Guidelines for Per-Area Summaries

**Voice**: First person, active voice, confident, executive-level. 2-3 sentences for the narrative, then separate Notable features/Notable maintenance lists.

**Structure per area** (follow this pattern):
1. **Opening sentence**: Work item/PR count + PG business goal or organizational priority the work supported
2. **Impact sentence**: What was delivered and its customer/business impact (conferences, UUF resolution, migration support)
3. **Blank line**
4. **Notable features:** Comma-separated list of feature work (names only, no descriptions)
5. **Notable maintenance:** Comma-separated list of maintenance work (names only, brief context in parens)

**Product area attribution rules:**
- Features and maintenance items must be attributed to the CORRECT product area based on the article's `ms.service` value, not the ADO work item category
- If a feature applies to a specific service (e.g., the article is in `articles/{service}/`), attribute it to that service area
- If articles span multiple service areas, attribute to the primary area based on `ms.service`
- Cross-area features → mention all applicable target areas
- When a team project spans multiple areas, attribute your contribution to the area where the articles live, and note it as a team effort (not your solo project)

**DO**:
- Lead with business impact, not task lists
- Reference specific features by name
- Cite adoption metrics, pageview numbers, or customer impact when available
- Mention cross-team collaboration naturally
- Connect work to PG goals (consumption growth, migration adoption, security posture)
- Reference conference shiproom deliverables where applicable

**DON'T**:
- List tasks bullet-by-bullet (this isn't a status report)
- Use vague language ("improved documentation")
- Include routine maintenance without framing its impact
- Reference work done by others as your own
- Use negative framing ("problems with...")

### Template (from May 2026 Connect — use as style reference)

> **Template file:** See [templates/connect-review-style-reference.md](templates/connect-review-style-reference.md)

### Workflow

1. Read ALL data sources listed above for the connect period
2. For each product area with work items, draft a 3-5 sentence executive summary
3. Present all summaries to user for review
4. User edits and refines — expect 1-2 rounds
5. Insert final summaries into `connect-review-data.html` as Section 7 (Executive Summaries) — each area in a `.copyable` div with `white-space:pre-wrap`
6. Plain text is also usable for pasting directly into the Connect form

---

## Phase 11: Session Summary Validation & Executive Summary Research

Cross-reference session summaries, monthly reports, and raw session JSON against computed datasets to catch missing items and gather executive summary context.

> **Reference file:** See [references/phase-11-session-validation.md](references/phase-11-session-validation.md) for the full 5-step workflow.

---

## Phase 12: Post-Generation Metric Validation

Validate data integrity after the HTML dashboard is generated — work item completeness, PR links, line counts, summary stats, and combined metrics.

> **Reference file:** See [references/phase-12-metric-validation.md](references/phase-12-metric-validation.md) for the full 5-step validation checklist.

---

## Exclusion Rules

**ADO items are NEVER excluded.** Only PRs excluded from metrics:
- Image index / Mock TOC / Migration content index PRs (inflated line counts)
- Batch shiproom PRs (200+ files, multiple authors)
- Hub nav updates: KEEP (tag with conference, not excluded)
- User confirms the list

---

## Storage

All files in `{connect-data-dir}/{monthYYYY}/`:
| File | Description |
|------|-------------|
| `ado-items.json` | Raw ADO work items |
| `github-prs.json` | GitHub PRs with AB# mappings |
| `gh-pr-stats.jsonl` | Raw GitHub API per-PR data |
| `pr-details.json` | Per-PR metrics with all tags |
| `parent-hierarchy.json` | Feature→Epic hierarchy map |
| `connect-database.json` | Master cross-reference |
| `all-pr-numbers.json` | All PR numbers found |
| `connect-review-data.html` | Visual dashboard |

---

## Writing Guidelines

**Voice**: First person, active voice, confident. Let metrics speak.

**Per product area:**
1. Lead with impact → business goal supported
2. Describe scale → what was done, how much
3. Show results → metrics, customer impact
4. Feature lists → New features / Going GA / In Preview (separate lines)
5. Maintenance count

**Highlight**: Customer adoption, cross-team collaboration, process improvements, AI/operational excellence
**Exclude**: Routine tasks without impact, vague statements, others' work, negative framing

---

## Known Gotchas

> **Reference file:** See [references/known-gotchas.md](references/known-gotchas.md) for the full list of known issues and edge cases accumulated from previous Connect cycles.

---

## Appendix: HTML Template Reference

> **Template file:** See [templates/connect-review-template.html](templates/connect-review-template.html)

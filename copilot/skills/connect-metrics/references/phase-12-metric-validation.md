## Phase 12: Post-Generation Metric Validation

**Run AFTER the HTML dashboard is generated to catch data integrity issues.**

### Step 1 — Validate work item completeness
1. Query ADO: `mcp_ado_wit_my_work_items(type="assignedtome", includeCompleted=true, top=200)`
2. Extract all work item IDs from the HTML `All Work Items` table:
   ```bash
   grep -oP '(?<=_workitems/edit/)\d+' connect-review-data.html | sort -un > html-ids.txt
   ```
3. Extract IDs from ADO results and compare:
   ```bash
   # Compare (use node if sort/comm has issues on Windows):
   node -e "
   const html = new Set(require('fs').readFileSync('html-ids.txt','utf8').trim().split('\n').map(Number));
   const ado = require('fs').readFileSync('ado-ids.txt','utf8').trim().split('\n').map(Number);
   const missing = ado.filter(id => !html.has(id)).sort((a,b)=>a-b);
   console.log('In ADO but not HTML: ' + missing.length);
   missing.forEach(id => console.log(id));
   "
   ```
4. Batch fetch missing IDs with `System.WorkItemType`, `System.State`, `System.ChangedDate`
5. Exclude: Features, Epics, Tasks, Removed items, items outside the semester date range
6. Remaining items are genuinely missing — add to appropriate product area section

### Step 2 — Validate work item → PR links
1. For items with multiple PRs or unusual PR numbers (< 10000), spot-check by calling `mcp_ado_wit_get_work_item` with `expand: "relations"` and comparing ArtifactLink PRs against what the HTML shows
2. **Flag OPS-E2E-PPE test repo PRs** — very low PR numbers (1000-2000 range) are test repo PRs, not production. Remove from display, show `—` instead
3. **Flag cross-repo PRs** — PR numbers in 10000-11000 range may be from public repos or other doc sets. Verify intentionally included
4. Spot-check 10-15 items prioritizing: items with multiple PRs, items with low PR numbers, recently added items

### Step 3 — Validate PR lines added/removed
1. Extract PR metrics from the HTML PR tables and compare against GitHub API data:
   ```javascript
   // Parse HTML PR tables for: PR number, +lines, -lines
   const prRegex = /pull\/(\d+)"[^>]*>#\d+<\/a><\/td><td class="title-cell">.*?<\/td><td>.*?<\/td><td>.*?<\/td><td>(\d+)<\/td><td>(\d+)<\/td><td>\+?([\d,]+)<\/td><td>-?([\d,]+)<\/td>/g;
   ```
2. For each PR, compare against `gh-pr-stats.jsonl` or call `mcp_github_pull_request_read` with `method: "get"` and check `additions`/`deletions`
3. Flag any mismatches — HTML values must exactly match GitHub fields

### Step 4 — Validate product area summary stats vs row totals
1. For each product area PR table section, sum the actual row values (new articles, updated, lines added/removed, images) from the `<table>` rows
2. Compare against the summary stats in the copyable `<div>` above each table
3. Compare against the header PR count (e.g., "{Area1} (27 PRs)")
4. **All three must match**: header count = summary PRs = actual row count
5. Automated check:
   ```javascript
   // For each PR section: extract header count, summary stats, and sum actual rows
   // Flag any where: headerCount !== actualRows OR summaryNew !== sumOfRowNew, etc.
   ```
6. Fix any discrepancies by updating summary stats to match actual row data

### Step 5 — Validate Combined Metrics Table
1. Sum the product area summary stats across the main columns ({Area1}, {Area2}, {Area3}, {Area4})
2. Compare against the Combined Metrics Table TOTAL column
3. Verify footnotes accurately describe what each column includes

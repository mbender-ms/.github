## Phase 9: Generate HTML Dashboard

**Build from scratch each time** — never patch an existing HTML (causes duplication).\n\n**Step 0 — Read template**: Before generating, read the template file at `{SESSION_DIR}\\templates\\connect\\connect-review-data-template.html` to match the exact CSS, structure, and section order. Do NOT deviate from the template layout.

### Required CSS Badge Classes
The HTML must include these badge styles for inline PR classification:
```css
/* Work type badges (inline in PR title cell) */
.badge-feature { background: #107c10; color: white; }   /* green — new feature */
.badge-maint   { background: #0078d4; color: white; }   /* blue — maintenance */
.badge-review  { background: #ff9800; color: white; }   /* orange — PR review */
.badge-admin   { background: #888;    color: white; }   /* gray — team/admin */

/* Conference badges (inline in PR title cell, after work type badge) — rename to match your conferences */
.badge-conf1   { background: #e91e63; color: white; }  /* pink */
.badge-conf2   { background: #9c27b0; color: white; }  /* purple */

/* UUF badge (in ADO work items table Type column) */
.badge-uuf { background: var(--warning); color: #333; }

/* State badges */
.state-closed { background: var(--success); color: white; }
.state-active { background: var(--accent);  color: white; }
.state-merged { background: #6f42c1;       color: white; }
.state-other  { background: #888;          color: white; }
```

**Sections in order:**

### Section 1: Key Metrics (copy-friendly)
Plain text `.copyable` block with ALL of these fields:
```
Items closed: {N}
User Stories closed: {N}
UUF items resolved: {N}
PRs merged: {N}
PRs open: {N}
New articles: {N}
Updated articles: {N}
Lines added: {N}
Lines removed: {N}
Images manipulated: {N}
PR reviews: {N}
Conference PRs ({Conference1}): {N}
Conference PRs ({Conference2}): {N}

New feature work: {N} PRs | {N} new articles | {N} updated | +{N} / -{N} lines | {N} images
Maintenance work: {N} PRs | {N} new articles | {N} updated | +{N} / -{N} lines | {N} images

Articles owned:
{Area1}: {N} articles (ms.service)
{Area2}: {N} articles (ms.service)
{Area3}: {N} articles
  - {Subarea}: {N}
  - {Subarea}: {N}
...

Avg Monthly Visitors ({period}, Power BI):
{Area1}: ~{N} visitors/month (~{N} page views/month)
{Area2}: ~{N} visitors/month (~{N} page views/month)
{Area3 - Shared}: ~{N} visitors/month (~{N} page views/month)
{Area4}:
  - {Subarea}: ~{N} visitors/month (~{N} page views/month)
  - {Subarea subtotal}: ~{N} visitors/month (~{N} page views/month)
Total across owned areas: ~{N} visitors/month (~{N} page views/month)
```

**CRITICAL**: Articles without `ms.service` metadata do NOT appear in Power BI. Their visitor data must be sourced separately or excluded from the total with a note.

### Section 2: Conference Contributions (table)
HTML table with columns: Conference, PRs, New Articles, Updated, +Lines, -Lines, Images, New Features, Going GA.
One row per conference, plus a **Totals** row at the bottom.

```html
<table>
<thead><tr><th>Conference</th><th>PRs</th><th>New Articles</th><th>Updated</th><th>+Lines</th><th>-Lines</th><th>Images</th><th>New Features</th><th>Going GA</th></tr></thead>
<tbody>
<tr><td>{Conference1}</td>...</tr>
<tr><td>{Conference2}</td>...</tr>
<tr><td><strong>Total</strong></td>...</tr>
</tbody></table>
```
Use same compact `table-layout:auto;width:auto` styling as other tables.

### Section 3: All Work Items ({total count})
Scrollable `.table-wrapper` with `<table>` grouped by product area.
- **Columns**: ID, Type, Title, State, Closed, SP, PRs
- **Category headers**: `<tr class="category-header"><td colspan="7">{Area} ({count})</td></tr>`
- **Type badges**: UUF items get `<span class="badge-uuf">UUF</span>`, others show plain type text
- **State badges**: `.state-closed`, `.state-active`, `.state-merged`, `.state-other`
- **PR links**: Comma-separated PR links, or `—` if none
- **Sort**: Within each category, closed items first (by ClosedDate), then open items
- **EXCLUDE Feature-type work items** — Features are organizational containers, not individual work. Only show User Stories, User Feedback, and Tasks in this table. The Feature hierarchy is used for classification (Phase 1 Step 6) but Features themselves should not appear as rows.
- **PR links from ADO Descriptions** — For each work item row, extract PR links from the Description (Phase 2 Step 1) and show them in the PRs column. This ensures work items show ALL linked PRs, not just those with AB# cross-references.

### Section 4: Metrics by Product Area

**PR table grouping rules (CRITICAL — these differ from ADO table grouping)**:
- **ADO table** (Section 3): Use granular groups from your agent file (8-10 categories matching your product areas, plus Team/Admin and Other)
- **PR tables** (Section 4): Merge related areas into broader groups to prevent table fragmentation:
  - Combine sub-areas of the same product into one section (e.g., multiple sub-areas → one combined section)
  - `PR Reviews` = Own section with `workType: 'Review'` badge — PRs authored by others and reviewed/merged by user
  - `{Area3} (Shared)` = Shared content across areas
  - `Team / Admin` = UAT, link farm, mock TOC, admin work
- This prevents table fragmentation (e.g., 1-2 PRs per section) while keeping the ADO table granular for work item visibility
- The Combined Metrics Table (Section 6) uses the PR table grouping ({Area1}, {Area2}, {Area3}, {Area4})

For each product area, generate:

**A) Copy-friendly summary block** (`.copyable`) with ALL fields:
```
{Area}:
Avg monthly visitors: ~{N} (~{N} page views)
Articles owned: {N}
PRs: {N} ({N} merged)
New feature PRs: {N}
Content maintenance PRs: {N}
New articles: {N}
Updated articles: {N}
Lines added: {N}
Lines removed: {N}
Images: {N}
{Conference1}: {N} PRs
{Conference2}: {N} PRs
New features: {N} - {feature name 1}, {feature name 2}
Features going GA: {N} - {feature name}
Features in preview: {N} - {feature name}
Maintenance items: {N}
```

**Data sources for per-area copy block fields (CRITICAL — do not omit)**:
- `Avg monthly visitors` → from `phase6-data.json` visitors object (Phase 6 Step 2)
- `Articles owned` → from `phase6-data.json` articleCounts object (Phase 6 Step 1)
- `New features / Going GA / In preview` → from `featuresByArea` metadata (Phase 4 Step 3b)
- All other fields → aggregated from PR details in that category

⚠️ If Phase 6 data is missing, omit (do not hard-code). If feature metadata is missing, show counts only and flag for user review.

**B) PR table** with columns: PR, Title, Status, Merged, New, Upd, +Lines, -Lines, Images, ADO
- **Title column includes inline badges**: `.badge-feature`, `.badge-maint`, `.badge-review`, `.badge-admin` for work type; `.badge-conf1`, `.badge-conf2` for conference tags
- **Status column**: `.state-merged` (purple), `.state-active` (blue/Open)
- **Totals row** (REQUIRED): `<tr class="totals-row">` at bottom of each table:
  ```
  Total ({N} merged — {N} feature, {N} maint) | {sum new} | {sum upd} | +{sum add} | -{sum del} | {sum img}
  ```

### Section 5: Grand Total
Metric cards grid (`.metrics-grid`) with: New Articles, Updated Articles, Lines Added, Lines Removed, Images

### Section 6: Combined Metrics Table
A single summary table with **product areas as columns** and **metrics as rows**, with a TOTAL column on the right.

**Columns**: Metric | {Area1} | {Area2} | {Area3} | {Area4}¹ | TOTAL

**Rows** (in order):
- Avg monthly visitors (from Phase 6)
- Avg monthly page views (from Phase 6) — separate row from visitors
- Articles owned (from Phase 6) — use `<sup>` footnotes for co-owned content and total calculation
- ADO items (from Phase 1)
- Items closed
- UUF resolved
- User Stories closed
- PRs (from Phase 2-3) — total only, do NOT include Feature PRs / Maintenance PRs sub-rows (redundant)
- New articles
- Updated articles
- Lines added
- Lines removed
- Images
- {Conference1} PRs / {Conference2} PRs (from Phase 7)
- New features / Features going GA / Features in preview (from Phase 4 Step 3b)
- Do NOT include a "Maintenance items" row (redundant with PRs)

**Footnotes**: Use `<sup>1</sup>`, `<sup>2</sup>` etc. for:
- Co-owned content (e.g., shared articles co-owned with another writer)
- Total calculation breakdowns
- Define footnotes in a `<p>` below the table with `font-size:12px;color:#605e5c`

**CRITICAL — Data source for per-area values**:
- Use the **per-area copy block values** (Section 4A) as the source of truth for New articles, Updated articles, Lines added/removed, and Images.
- Do NOT use raw `pr-details.json` values — they can differ from the verified copy block values due to exclusion handling and rounding.
- TOTAL column = sum of the 4 product area columns only (excludes PR Reviews, Team/Admin, Shared).

**Styling**: `table-layout:auto;width:auto` so columns shrink to content. Alternating row backgrounds with `#f3f2f1`. TOTAL column header has `background:#106ebe;color:white`.

### Section 7: Executive Summaries
Insert per-area executive summary blocks (from Phase 10) into the HTML inside `.copyable` divs with `white-space:pre-wrap`.
Each area gets an h3 heading and a copyable text block.
Areas to include: Configure from your agent file product areas, plus Team/Admin.

**Format per area** (CRITICAL — follow this structure):
1. **Short narrative** (2-3 sentences) — work item/PR count, PG alignment, high-level impact
2. **Notable features:** — comma-separated list of feature work done in this area
3. **Notable maintenance:** — comma-separated list of maintenance/quality work done in this area

Specific features and maintenance items are pulled OUT of the narrative text and listed at the bottom. The narrative focuses on impact, PG alignment, and scope — not feature names.

### Section 8: PR Exclusions
`.exclusion-box` listing excluded PRs as links. ADO items are NEVER excluded.

Save to: `{monthYYYY}/connect-review-data.html`

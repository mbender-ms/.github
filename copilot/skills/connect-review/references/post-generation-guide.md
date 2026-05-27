
## Step 4: IC Level Callout Reference

When writing IC level callouts, reference the career framework files in `promo/references/`:
- `technical-writing-ic4.md` — current level responsibilities
- `technical-writing-ic5.md` — stretch/promotion-ready responsibilities

### Key IC4 → IC5 Differentiators to Highlight

| Responsibility | IC4 Language | IC5 Language |
|---------------|-------------|-------------|
| **Content Strategy** | "Maps out and leads content strategy for a portfolio" | "Leads long-term content strategy... impacting multiple portfolios" |
| **Stakeholder Collaboration** | "Manages relationships and expectations with stakeholders" | "Builds and owns relationships... drives executive support for funding or resources" |
| **Tools & Operations** | "Masters the tools, processes... identifies opportunities to improve" | "Leads the development and socialization of material... evangelizes processes/tools to partners across Microsoft" |
| **Customer Engagement** | "Drives engagement with customer communities" | "Evangelizes work and shares insights with senior leaders" |
| **Experimentation** | "Explores and experiments with new content delivery channels" | "Drives experimentation for the organization" |
| **Content Creation** | "Applies and assists with creating principles... for a variety of users" | "Takes ownership of the overall portfolio/product experience across the ecosystem" |
| **Customer Research** | "Identifies and determines/leads customer research" | "Designs research studies to support team strategy" |

**Usage:** For each goal section, pick the 1-2 most relevant responsibility areas. Quote the specific language. Explain how the work maps. If work clearly demonstrates IC5 behavior, call it out — this is critical for promotion cases.

**IMPORTANT:** IC level callouts go in the **full HTML report ONLY** (personal reference / promo evidence). They do NOT go in the **Connects tool paste version** — the Connects tool is for manager/skip-level review and should focus on outcomes and org alignment, not career framework language.

---

## Step 5: User Review and Iteration

After generating the initial HTML:

1. **Present section-by-section** for review
2. **Expect 2-3 rounds** of revision
3. **Common revision requests:**
   - Tone adjustments (too modest vs. too aggressive)
   - Adding missing accomplishments from memory
   - Reframing "Why It Matters" to better align with specific org priorities
   - Adjusting IC level callouts
   - Adding/removing stakeholders
   - Updating forward plan

4. **After user approval**, save final version to `{Connect folder}/connect-output.html`

---

## Step 6: Generate Copy-Friendly Text for Connects Tool

The Connects tool accepts **light HTML formatting** — tables, bold, and basic structure paste correctly from rich text. Generate a lightly formatted version optimized for pasting.

### Formatting Rules for Connects Tool Text

**Allowed (pastes well):**
- **Bold text** (`<strong>` or `**`) for emphasis on key metrics and headers
- **Tables** — simple HTML tables paste correctly with structure preserved
- **Line breaks** — standard paragraph breaks
- **Bullet lists** — unordered lists paste fine
- **Numbered lists** — ordered lists paste fine

**Avoid (doesn't paste well or is overkill):**
- Gradient backgrounds, colored cards, CSS styling
- Metric card grids, bar charts, animations
- Dark mode toggles, TOC sidebars, JavaScript
- Complex nested layouts

### Output Structure

The paste version file (`connect-text-for-tool.html`) should follow this exact section order:

**1. Copilot Researcher Summary** (if available)
- Run Microsoft 365 Copilot Researcher against Teams, Outlook, ADO for the connect period
- Include as a `<blockquote>` at the top — condensed to key impact statements only
- Label it with an italic note explaining the source

**2. SMART Goals Scorecard** → table format (NOT grid cards)
- Simple `<table>` with columns: #, SMART Goal, Status, Result
- Row colors: green (#dff6dd) = done, blue (#e8f0fe) = exceeded, yellow (#fff4ce) = partial, red (#fde7e9) = not met

**3. Combined Metrics Table** → from connect-review-data
- Full product-area-as-columns table with footnotes
- Include both visitors AND page views as separate rows
- Compact padding (`cellpadding="4"`)

**4. Goal 1: Content for Customers**
- **Product Area Summaries** — one `<p>` per area with Notable features/maintenance `<ul>`
- **Conference Contributions** — table + notable features per conference
- **SMART goals** — 1.1, 1.2, 1.3 with narrative + "Why It Matters"

**5. Goal 2: Improve and Innovate**
- **Planned SMART goals** — UATs, AI Assignments, AI Tool Usage
- **Unplanned goals** — e.g., Partner Publishing Workflow with metrics and peer quotes woven in
- **No IC level callouts** in paste version

**6. Goal 3: Better Together**
- **Planned SMART goals** — Team resources (with manager quotes woven in), Community event
- **Unplanned goals** — e.g., Link Farm Elimination (team project with your contribution), PR Reviews & Coverage (with vendor quote woven in)
- **No standalone peer feedback section** — quotes woven into relevant sections

**7. Future SMART Goals** — labeled by Connects field ("Plan for the future" — Goal 1/2/3)
- Written as full SMART goals with "By {date}" framing
- Include both planned continuations AND new goals (e.g., workflow video, CDA evangelism)

### Example — Goal Section for Connects Tool

```html
<strong>SMART Goal 2: Reduce UUF count by 39%</strong>

<strong>Outcome: Exceeded ✅</strong> — Goal was 35% reduction, achieved 39%.

By May 2026, improved content quality by incorporating customer feedback while reducing
UUF count by 39%, exceeding the 35% target.

<table>
<tr><th>Month</th><th>Items Closed</th><th>Key PRs</th></tr>
<tr><td>November</td><td>5</td><td>#36132</td></tr>
<tr><td>December</td><td>8</td><td>#36371, #36463</td></tr>
<tr><td>January</td><td>12</td><td>#36502, #36688</td></tr>
</table>

<strong>Why It Matters:</strong> UUF items represent direct customer pain points — real
people who tried to use our documentation, hit problems, and took the time to report them.
Closing these items directly supports the EPD Customers key result of closing 80% of
priority 1 UUF items within 90 days, and aligns with the Content North Star focus on
using customer signals to reduce friction and accelerate adoption.

<strong>IC Level — IC4 Customer Engagement:</strong> "Engages and addresses feedback from
customers and drives content investments." Systematically analyzing and resolving 39%
of UUF backlog through verified customer feedback demonstrates strong IC4 customer
engagement, with the systematic analysis approach touching IC5: "Drives planning for
direct customer engagement and addresses customer feedback."
```

Save to: `{Connect folder}/connect-text-for-tool.html`

---

## Checklist Before Finalizing

### Full HTML Report (connect-output.html)
- [ ] All SMART goals are addressed (including "Not Met" ones with honest explanation)
- [ ] Every goal section has a "Why It Matters" box
- [ ] Every goal section has an IC4 → IC5 callout with career framework quotes
- [ ] Metrics match connect-review-data (no fabricated numbers)
- [ ] All ADO and PR references are clickable hyperlinks
- [ ] Metric counters show real values in HTML text (Teams compatibility)
- [ ] Sections visible without JavaScript (CSS opacity:1 by default)
- [ ] Forward plan written as full SMART goals
- [ ] Dark mode works correctly
- [ ] TOC sidebar navigation works
- [ ] Period dates are accurate in header and footer

### Paste Version (connect-text-for-tool.html)
- [ ] Copilot Researcher summary at top (if available)
- [ ] Scorecard as simple HTML table (not CSS grid) with color-coded rows
- [ ] Combined metrics table from connect-review-data (both visitors AND page views)
- [ ] Product area summaries with Notable features/Notable maintenance format
- [ ] Conference contributions table with per-conference feature lists
- [ ] Unplanned goals included (workflow innovations, team project contributions)
- [ ] Peer quotes woven into relevant sections (NOT in standalone section)
- [ ] NO IC level callouts (those are full report only)
- [ ] NO standalone stakeholders section
- [ ] Future SMART goals written with "By {date}" framing
- [ ] All tables use `<table border="1">` for paste compatibility
- [ ] Compact table padding (`cellpadding="4"`) — no width:100%
- [ ] No sensitive information (customer names, internal URLs)

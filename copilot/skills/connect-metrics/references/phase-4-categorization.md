# Phase 4: Categorize, Tag, and Classify PRs

**Step 1 — Product area**: Use linked ADO work item's category. Fallback: PR title keywords.

**Required product area categories** (used for both ADO table grouping and PR table sections):
- Product areas from agent file (configure in your agent file)
- Sub-areas defined in agent file for granular ADO grouping
- `Team / Admin` — Title contains 'review|UAT|link farm|mock|extension|tiger team'
- `PR Reviews` — PRs authored by others and reviewed by user
- `Other` — Work items not matching any above category

**ADO table vs PR table categories may differ**: The ADO work items table can use more granular groups (e.g., 10+ groups). The PR table sections should use 6-8 focused groups to avoid fragmentation.

**Step 2 — Work type** (Feature vs Maintenance) — USE HIERARCHY FROM `parent-hierarchy.json`:
- Look up the linked ADO work item in the hierarchy map built in Phase 1 Step 6
- Read `epicId` from the map → compare against Epic IDs from agent file:
  - If epicId = New Content epic ID → **New Feature**
  - If epicId = Q+I/Maintenance epic ID → **Maintenance**
- Fallback (only for PRs with no linked ADO item): ADO `new-feature` tag, then title keywords
- PRs authored by others and reviewed/merged by user → **Review**
- The hierarchy is the source of truth — title keyword regex is only a fallback for unlinked PRs

**Step 3 — GA vs Preview vs New** (for Feature PRs only):
- Check ADO work item title AND parent Feature title for keywords:
  - `ga`, `publish`, `going ga` → **Going GA**
  - `preview`, `public preview` → **In Preview**
  - Everything else → **New Feature**
- Deduplicate: multiple PRs for same feature = 1 feature entry

**Step 3b — Derive feature names for per-area copy blocks**:
The per-area copy blocks need feature names (not just counts). Derive names as follows:

1. For each Feature PR, get the linked ADO work item title
2. Extract feature name: strip prefix patterns (`{Area1} | `, `{Area2} | `, etc.) and suffix patterns (` - publish`, ` preview`, ` GA`)
3. Use the cleaned ADO title as the feature name
4. If no linked ADO item, use the PR title (strip PR-specific prefixes like "Announce", "Document", "Add", "Staging")
5. Group by GA/Preview/New classification from Step 3
6. Deduplicate: if multiple PRs map to the same feature (same ADO parent), keep one name

**Store as metadata per area** for Phase 9 consumption:
```json
{
  "featuresByArea": {
    "{Area1}": {
      "new": ["Feature A known issues", "Feature B"],
      "ga": ["Feature C", "Feature D update policy"],
      "preview": ["Feature E"]
    }
  }
}
```

**Step 4 — Conference tags** — ADO tags + parent hierarchy are the authoritative source:
- Conference tags on ADO work items (e.g., `{Conference1}-YYYY`, `{Conference2}`) are the **primary source**
- PRs inherit conference tags from their linked ADO work items
- Also inherit conference tags from **parent Feature work items** in the hierarchy — walk up `parent-hierarchy.json` to the parent Feature and check its tags. Many work items don't have conference tags directly but their parent Feature does.
- Naming: calendar year ({Conference1} YYYY = Month YYYY, {Conference2} YYYY = Month YYYY)

**Detection methods** (apply in order — hierarchy walk first):
1. **ADO tags on work item**: Check linked work item's `System.Tags` for conference-related tags
2. **Parent Feature tags**: Walk up `parent-hierarchy.json` to the parent Feature and check its `System.Tags` — catches the majority of conference-tagged PRs
3. **PR title keywords (FALLBACK)**: Only for PRs with no linked ADO item
4. **Merge date proximity (LAST RESORT)**: Only for unlinked PRs with no title match — ±7 days of conference shiproom date

**Badge classes**: `.badge-conf1`, `.badge-conf2` (or equivalent per conference name — configure in your agent file)

**Exclude release-to-release branch merge PRs from conference metrics**:
These PRs contain aggregated commits from multiple authors and inflate metrics. If a conference-tagged PR has 200+ changed files or merges between release branches, flag it for user review before including.

**Step 5 — User review** (do not skip):
- Present full categorized list for review
- User corrects: product areas, work types, GA/preview, conference tags
- User identifies PRs to remove or add
- Re-run after corrections. Expect 1-2 rounds.

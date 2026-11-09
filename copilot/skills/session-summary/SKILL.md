---
name: session-summary
category: Reports
version: 1.0.0
description: Generate a validated daily session summary using phased data gathering from ADO and GitHub APIs with token budget management. Use this skill whenever the user wants an end-of-day summary, session recap, daily report, or says things like "summarize today", "what did I do today", "end of day summary", or "wrap up the day".
argument-hint: '"today" or date in YYYY-MM-DD format'
user-invocable: true
disable-model-invocation: false
---

# Session Summary Skill

Generate a comprehensive, validated daily session summary by gathering data from multiple sources (available conversation history or user-provided session exports, ADO, GitHub, WorkIQ) in managed phases to prevent context window overflow. Produces a structured markdown file in the user-confirmed export directory under the `Session Summaries` subfolder.

**Invocation:**
- `/session-summary` or `/session-summary today` — Generate summary for today
- `/session-summary 2026-04-02` — Generate summary for a specific date

**CRITICAL**: Every data point in the summary must trace to an API response. NEVER estimate metrics from session memory or assume titles/states from conversation context.

**Token management**: This workflow is split into 7 phases because loading all data at once (conversation history + ADO work items + GitHub PRs + comments + meetings) can exceed the context window. Use `manage_todo_list` to track phase progress and manage token budget.

---

## Phase 1: Extract Session Data

Use available conversation-history tools or explicit user-provided session exports for the requested date. If neither source is available, ask the user for the missing evidence before continuing. This workflow does not require a separate session-memory extension.

**Create todo list and start Phase 1:**

```
manage_todo_list([
  { id: 1, title: "Extract session data", description: "Read available conversation history or user-provided session exports for IDs and narrative", status: "in-progress" },
  { id: 2, title: "Fetch ADO work items", description: "Call mcp_ado_wit_get_work_items_batch_by_ids for all work item IDs", status: "not-started" },
  { id: 3, title: "Fetch GitHub PRs", description: "Cross-verify session PRs with GitHub search (involves:{username} updated:{date}), merge lists, then call mcp_github_pull_request_read for all PR numbers", status: "not-started" },
  { id: 4, title: "Fetch ADO comments", description: "Get comments for work items updated today", status: "not-started" },
  { id: 5, title: "Fetch meeting details", description: "Call mcp_workiq_ask_work_iq for Teams meetings attended today", status: "not-started" },
  { id: 6, title: "Generate summary", description: "Compose validated session summary markdown", status: "not-started" },
  { id: 7, title: "Write summary file", description: "Save to export directory", status: "not-started" }
])
```

**Actions:**

1. Read the available history or supplied exports for the requested date and extract:
   - ADO work item IDs
   - GitHub repository names and PR numbers
   - Decisions and lessons learned
   - File changes and timestamps explicitly present in the evidence

2. Group the evidence into chronological work phases for the narrative backbone. Summarize the history rather than loading raw exchanges into later phases. Do not invent missing timestamps or activity counts.

3. **Output to pass to next phase:**
   - List of work item IDs: [540865, 536997, ...]
   - List of PR numbers: [36539, 36427, ...]
   - Session phases with labels and time ranges (the narrative structure)
   - Decisions and lessons
   - Total counts

**Mark Phase 1 complete, Phase 2 in-progress.**

---

## Phase 2: Fetch ADO Work Item Details

**Use `runSubagent` for this phase.** By end-of-day, the main context is too bloated to reliably fetch all fields. A subagent gets a clean context window.

**Subagent prompt:**

```
You are a data-fetching agent. Do NOT summarize or analyze — just fetch and return raw data.

Call `mcp_ado_wit_get_work_items_batch_by_ids` with:
- project: "Content"
- ids: [{COMMA_SEPARATED_IDS}]
- fields: ["System.Id", "System.Title", "System.State", "System.WorkItemType", "Microsoft.VSTS.Common.ClosedDate", "System.ChangedDate"]

If there are more than 100 IDs, split into multiple calls.

Return ONLY a markdown table with these columns:
| ID | Title | Type | State | ClosedDate | ChangedDate |
```

**After subagent returns**: Extract the ID→Title and ID→State mappings for Phase 6.

**Mark Phase 2 complete, Phase 3 in-progress.****

---

## Phase 3: Fetch GitHub PR Details

**Use `runSubagent` for this phase.** The `pull_request_read` method with `method: "get"` returns `additions`, `deletions`, and `changed_files` — the search API does NOT. A subagent won't shortcut to the wrong API.

### Step 1: Cross-verify PR list with GitHub search

Session JSON only captures PRs touched within the current Copilot Chat conversation. PRs created in other conversations, via the GitHub web UI, or via CLI will be missing. **Always cross-verify.**

Before fetching PR details, run a GitHub search to find ALL PR activity for the user that day:

```
mcp_github_search_pull_requests(
  query: "involves:{username} updated:{YYYY-MM-DD}",
  owner: "MicrosoftDocs"   // or the primary org
)
```

Also search personal repos if the user works across orgs:

```
mcp_github_search_pull_requests(
  query: "involves:{username} updated:{YYYY-MM-DD}",
  owner: "{username}"
)
```

**Merge the results:**
1. Start with PRs from session JSON (`allPullRequests` from Phase 1)
2. Add any PRs from the search results that aren't already in the list (deduplicate by PR number + repo)
3. The merged list is the complete PR set for the day

### Step 2: Fetch details for all PRs

**Subagent prompt:**

```
You are a data-fetching agent. Do NOT summarize or analyze — just fetch and return raw data.

For each PR below, call `mcp_github_pull_request_read` with method: "get".
If the tool is disabled, call `activate_pull_request_management_tools` first, then retry.

PRs to fetch:
{LIST EACH PR as owner/repo #number, one per line. Example format:
- MicrosoftDocs/sql-docs-pr #12345
- duongau/content-developer-installer #67
}

Return ONLY a markdown table with these columns:
| PR | Repo | Title | State | Merged Date | Files | Additions | Deletions |
```

**After subagent returns**: Extract PR data for the GitHub PR Details table and Metrics computation.

**CRITICAL**: If any GitHub MCP tool fails (500 error, timeout), the subagent should activate the appropriate tool group first (`activate_pull_request_management_tools`), then retry. Do NOT assume data.

**Mark Phase 3 complete, Phase 4 in-progress.**

---

## Phase 4: Fetch ADO Comments (Optional — Skip if Token Budget Tight)

**Use `runSubagent` for this phase if executing it.** Comment fetching requires one API call per work item — a subagent handles this cleanly without bloating main context.

**Subagent prompt:**

```
You are a data-fetching agent. Do NOT summarize or analyze — just fetch and return raw data.

For each work item ID below, call `mcp_ado_wit_list_work_item_comments` with:
- project: "Content"
- workItemId: {ID}
- top: 3

Work items to fetch (ONLY items modified today):
{LIST EACH ID}

Return ONLY a markdown list with this format for each item:
- **#{ID}**: {First 1-2 sentences of the most recent comment text}
```

**After subagent returns**: Use comment summaries to enrich the ADO Work Item Details section.

**When to skip this phase:**
- Token budget is tight (many work items + PRs already fetched)
- Work items were only referenced, not actively updated with comments
- Session was short with few ADO interactions

**Mark Phase 4 complete, Phase 5 in-progress.****

---

## Phase 5: Fetch Meeting Details (WorkIQ)

**Actions:**

1. Call `mcp_workiq_ask_work_iq` with:
   - Question: "List all meetings I attended today [DATE] with title, time, attendees, and key discussion points or action items for each."

2. **Output minimal data:**
   - Meeting title → Time
   - Meeting title → Key topics discussed (1-2 sentences each)
   - Meeting title → Action items assigned to me

3. **For meetings with transcripts**: WorkIQ can extract detailed agenda items, decisions, and action items
4. **For meetings without transcripts**: Only title, time, and attendee list will be available

**Note**: WorkIQ pulls from Teams calendar and meeting transcripts. Meetings held outside Teams won't appear.

**When to skip this phase:**
- No significant meetings that day
- Token budget is critically low
- User indicates no meetings to capture

**Mark Phase 5 complete, Phase 6 in-progress.**

---

## Phase 6: Generate Summary

**Using data from Phases 1-5, compose the session summary.**

### Conditional sections rule (CRITICAL)

**Omit any section entirely if there's no data for it that day.** For example:
- No PRs → omit `## GitHub PR Details`
- No meetings → omit `## Meetings Attended`
- No technical deep-dives → omit `## Technical Details`
- No architectural decisions → omit `## Decisions Made`

### Required section ordering

Follow this order. Omit sections with no data:

1. `## Session Overview`
1. `## Key Accomplishments`
1. `## Technical Details` *(conditional)*
1. `## Files Modified`
1. `## ADO Work Item Details`
1. `## GitHub PR Details` *(conditional)*
1. `## Meetings Attended` *(conditional)*
1. `## Decisions Made` *(conditional)*
1. `## Lessons Learned / Notes`
1. `## Next Steps`
1. `## Metrics`
1. `## Time Tracking` *(always last)*

### Step 1: Check for existing summary

Read existing summary if `{export-directory}/Session Summaries/session-summary-YYYY-MM-DD.md` already exists (continuous reconciliation — merge new data with existing content).

### Step 2: Build narrative from session phases

Use `sessionPhases` from Phase 1 as the narrative backbone. Each phase becomes a Key Accomplishment section with:
- Phase label → accomplishment title
- Time range → time tracking
- Work items and PRs referenced → linked details
- Top tools used → technical details

### Step 3: Populate with validated data

- Work item titles from Phase 2 (NEVER assumptions)
- PR titles from Phase 3 (NEVER assumptions)
- Current states from API responses
- Meeting titles, topics, and action items from Phase 5
- Comment summaries from Phase 4

**Section-specific guidance:**

- **GitHub PR Details**: Use table format (`| PR | Title | State | Files | +/- |`). Only include if PRs were created, reviewed, or merged.
- **Decisions Made**: Use table format (`| Decision | Rationale |`). Only include if architectural or strategic decisions were made.
- **Next Steps**: Numbered list of follow-up items for next session. Include if there's ongoing work.

### Step 4: Compute Metrics table from verified API data (Phases 2-3)

**NEVER estimate metrics from session memory — every number must trace to an API response.**

**MANDATORY RULE — ALL rows below MUST appear in every summary, even when the value is `0`.** Never silently omit a row because the day was light on activity. Match the [session-summary-template.md](./templates/session-summary-template.md) Metrics table exactly. If a metric truly doesn't apply (e.g., no PRs touched at all), still emit the row with value `0`. Dropping rows breaks downstream parsing (monthly-report aggregation, manager dashboards) and obscures "nothing happened today" vs "forgot to fill in".

| Metric | Source | How to Compute |
|--------|--------|----------------|
| **PRs Created** | Phase 3 | Count PRs with `created_at` on session date |
| **PRs Merged** | Phase 3 | Count PRs with `merged_at` on session date |
| **PRs Reviewed** | Phase 3 | Count PRs reviewed but not authored on session date |
| **Work Items Closed** | Phase 2 | Count items with State = Closed and `ClosedDate` on session date |
| **Work Items Updated** | Phase 2 | Count items with `ChangedDate` on session date |
| **Files Changed** | Phase 3 | Sum `changed_files` from all PRs + non-PR files from session data |
| **Lines Added** | Phase 3 | Sum `additions` from all PRs |
| **Lines Deleted** | Phase 3 | Sum `deletions` from all PRs |
| **Repos Touched** | Phase 3 | Count unique repo names from PR data |

### Step 5: Generate full markdown

Follow the [session summary template](./templates/session-summary-template.md) for the Required Format Structure.

**Mark Phase 6 complete, Phase 7 in-progress.**

---

## Phase 7: Write Summary File

### Storage Location

**Output path precedence**:
1. Use an export path explicitly provided by the user for this request.
2. Otherwise, use an explicit export path in the agent instructions.
3. If neither is configured, ask the user where to store exports before writing any files.

> **Note:** Each skill writes to its own subfolder under the export directory (`Session Summaries`, `Monthly Reports`, `PR Reviews`). If the export directory already ends with a known subfolder name, it's used directly without doubling.

- **Naming Convention**: `session-summary-YYYY-MM-DD.md`
  - Examples: `session-summary-2026-04-03.md`, `session-summary-2026-03-28.md`
  - **One file per day** (default) — represents complete work for that date
  - **Multi-day option**: `session-summary-YYYY-MM-DD-DD.md` for light days (e.g., `session-summary-2026-01-06-07.md`)

### File Management (CRITICAL)
- **ALWAYS use `replace_string_in_file` tool** to update existing summaries (not `create_file`)
- **ALWAYS use `create_file` tool** only for first summary of the day
- **NEVER use terminal commands** (e.g., `cat > file << 'EOF'`) for file operations
- Works for paths outside workspace (like the export directory)

### Actions

1. Check if `{export-directory}/Session Summaries/session-summary-YYYY-MM-DD.md` exists
2. If exists: Use `replace_string_in_file` to update
3. If not: Use `create_file` to create new
4. Populate the Metrics table and Time Tracking section from verified API responses and timestamped history:
   - Count distinct work items and PRs from the verified lists.
   - Include file counts and duration only when the evidence supports them.
   - Explicitly mark unavailable metrics as unavailable; do not estimate them.
5. Confirm the summary file was saved. Saving a report does not close or export the underlying chat session.

**Correct ordering:**
```
Phase 6: Generate summary content (all narrative, tables, accomplishments)
Phase 7 step 1-3: Write summary file
Phase 7 step 4: Complete metrics using verified evidence
Phase 7 step 5: Verify the saved file
```

**Mark all todos complete.**

---

# Reference

## Token Budget Guidelines

| Data Type | Approximate Tokens | Strategy |
|-----------|-------------------|----------|
| Conversation history (50 exchanges) | ~5,000 | Summarize, don't include full text |
| Each ADO work item | ~500 | Fetch only needed fields |
| Each GitHub PR | ~300 | Extract title/state only |
| Each ADO comment | ~200 | Get latest only, summarize |
| Meeting details (WorkIQ) | ~1,500 | One query for all meetings; extract titles + key points |
| Final summary output | ~2,000 | Standard format |

**If approaching limits:**
- Skip Phase 4 (comments) entirely
- Skip Phase 5 (meetings) if no significant meetings that day
- Batch ADO calls (max 20 work items per call)
- Only fetch PRs that were merged today
- Summarize accomplishments more aggressively

---

## Data Verification Rules (CRITICAL)

**ALWAYS fetch actual data — NEVER make assumptions.**

### For GitHub PRs (MCP tools)
1. **MUST call** `mcp_github_pull_request_read` with `method: "get"`
2. Use actual `title` field from response
3. Verify PR state (open/closed/merged)

### For ADO Work Items (MCP tools)
1. **MUST call** `mcp_ado_wit_get_work_items_batch_by_ids` or `mcp_ado_wit_get_work_item`
2. Use actual `System.Title` field from response
3. Verify work item state

### Rules
- ❌ **DO NOT** assume titles based on conversation context
- ❌ **DO NOT** use previous work item titles from memory
- ❌ **DO NOT** guess based on file names or topic area
- ✅ **ALWAYS** fetch current data before writing summaries
- ✅ Session summaries are permanent records requiring accuracy

---

## Content Guidelines

- **Be comprehensive** — Include all significant work done during the session
- **Use specific details** — Include work item IDs, PR numbers, file paths, tool names
- **Document technical decisions** — Explain why certain approaches were chosen
- **Include context** — Background information that future you will need
- **Track tools used** — Mention MCP tools, ADO operations, Git commands
- **Note challenges** — Document problems encountered and how they were solved
- **Add emojis for visual organization** — ✅ checkmarks, 📝 notes, ⚠️ warnings, etc.

### Hyperlink Rules (CRITICAL — Apply to ALL References)

**GitHub PRs** — ALWAYS use full markdown links:
- ✅ `[PR #12345](https://github.com/MicrosoftDocs/{repo}/pull/12345)`
- ❌ `PR #12345` (bare number)

**ADO Work Items** — ALWAYS use full markdown links:
- ✅ `[#540865](https://msft-skilling.visualstudio.com/Content/_workitems/edit/540865)`
- ❌ `#540865` (bare number)

---

## Tool Categorization

This skill uses two categories of tools:

| Category | Prefix | Served by | Tools Used |
|----------|--------|-----------|------------|
| **MCP tools** | `mcp_` | External MCP server processes | `mcp_ado_wit_*`, `mcp_github_*`, `mcp_workiq_*` |
| **Built-in tools** | No prefix | VS Code itself | `manage_todo_list`, `create_file`, `replace_string_in_file`, `read_file` |

### MCP Tool Activation Rule

**When any MCP tool call fails (500 error, timeout, etc.):**
1. **DO NOT** try workarounds or alternative API approaches
2. **DO** activate the appropriate tool group first, then retry
3. Common tool groups to activate:
   - `activate_pull_request_management_tools` — For PR read/write operations
   - `activate_azure_devops_work_item_management_tools` — For ADO work item operations

**Pattern**: Activate once per session before first use of that tool group. If a call fails, activate and retry before reporting failure.

## Why This Phased Workflow

Conversation history supplies narrative context, while ADO and GitHub APIs supply verified titles, states, and counts. WorkIQ supplies meeting evidence when available. The phased workflow reconciles this evidence with the existing summary and limits how much raw data must remain in context at once.

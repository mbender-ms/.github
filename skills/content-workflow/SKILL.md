---
name: content-workflow
description: >-
  Orchestrate Azure documentation workflows ΓÇö create ADO work items with auto-calculated
  fields, generate git branch names and commit messages, create PR descriptions with AB#
  linking, calculate publish dates, and close work items. Replaces the Content Developer
  MCP server tools with portable skill instructions.
argument-hint: "Describe the workflow step: 'create work item', 'save changes', 'create PR', 'close work item', or 'session startup'"
user-invocable: true
---

# Content workflow skill

This skill orchestrates the full Azure documentation content development lifecycle. It replaces five MCP server tools (`create_work_item_template`, `generate_git_workflow_context`, `generate_pr_description`, `calculate_work_item_completion`, `get_workflow_example`) with portable instructions that Copilot executes directly.

## Workflow 1: Session startup

Run this workflow when a conversation starts or the user mentions starting NEW documentation work. **Skip this workflow** if the user wants to CONTINUE current work (for example, "save my changes", "commit", "push").

### Steps

1. **Check current branch:**

   ```bash
   git branch --show-current
   ```

2. **Check for uncommitted changes:**

   ```bash
   git status --porcelain
   ```

3. **Handle the current state** ΓÇö one of three scenarios:

   | Scenario | Action |
   |---|---|
   | Feature branch + uncommitted changes | Stash changes ΓåÆ switch to main ΓåÆ sync |
   | Feature branch + clean working tree | Switch to main ΓåÆ sync |
   | Already on main | Sync only |

   **Stash command** (when needed):

   ```bash
   git stash push -m "Auto-stash before switching to main - {YYYY-MM-DD HH:MM}"
   git checkout main
   ```

4. **Sync main with upstream:**

   ```bash
   git fetch upstream main && git rev-list --count HEAD..upstream/main
   ```

   If the count is greater than 0 (main is behind upstream):

   ```bash
   git pull upstream main && git push origin main
   ```

5. Confirm to the user that the environment is ready for new work.

## Workflow 2: Create work item

This is a three-step orchestration: generate template ΓåÆ create in ADO ΓåÆ link to parent.

### Step 1 ΓÇö Generate the work item template

Calculate all fields from the conversation context and reference data.

**Title**: Use sentence case. Derive from the user's description of the work.

**AreaPath**: Look up the service in [references/service-mappings.md](references/service-mappings.md) and use the corresponding AreaPath value.

**IterationPath**: Calculate using the algorithm in [references/iteration-calculator.md](references/iteration-calculator.md) based on the current date.

**Parent work item ID**: Look up from [references/ado-hierarchy.md](references/ado-hierarchy.md) using the `workflow_type` and the service's category (from the service categories table in service-mappings).

**Required properties (create-time):**

| Field | Value |
|---|---|
| `System.Title` | Sentence-case title derived from the user's requested outcome |
| `System.State` | `"New"` |
| `System.AreaPath` | Service-specific AreaPath from `references/service-mappings.md` |
| `System.IterationPath` | Calculated current iteration from `references/iteration-calculator.md` |
| `System.Description` | Markdown template below |
| `Microsoft.VSTS.Common.AcceptanceCriteria` | Markdown template below |
| `System.Tags` | Approved tags + service name + `"cda"` (semicolon-separated) |
| `System.Parent` | Parent from `references/ado-hierarchy.md` (linked in Step 3) |
| `Microsoft.VSTS.Common.Priority` | `2` unless user provides a different priority |
| `Custom.Modality` | `"Documentation"` |
| `Microsoft.VSTS.Scheduling.StartDate` | Current date in ISO 8601 format |
| `Microsoft.VSTS.Scheduling.TargetDate` | End of current month unless user provides target date |
| `Custom.ProposalType` | Based on the user's action (see mapping below) |

For `User Story` items, also set `Microsoft.VSTS.Scheduling.StoryPoints`.

For `Feature` items, also set `Custom.TeeShirtSize`.

**ProposalType mapping:**

| User Action | ProposalType |
|---|---|
| Creating new documentation | `"New"` |
| Updating existing documentation | `"Update"` |
| Reviewing for freshness | `"Review"` |
| Removing documentation | `"Remove"` |
| Deprecating documentation | `"Retire"` |
| Migrating documentation | `"Migrate"` |

**Valid workflow types:** `content-maintenance`, `new-feature`, `pm-enablement` (legacy alias: `pm-content`), `css-support`, `partnership`, `content-gap`, `mvp-feedback`, `architecture-center`, `curation`

**Approved tags (ONLY use these):** `content-maintenance`, `mvp-feedback`, `AAC`, `new-feature`, `PM-enablement`, `css-support`, `acc-horizontal-security`, `acc-horizontal-reliability`, `acc-horizontal-supportability`, `curation`, `CSAT`, `Linux`, `content-gap`, `Process`, `Training`. Always add the service name as a tag. Always add `"cda"` as a tag.

Use `AAC` as the canonical Architecture Center tag. If legacy content uses `ACC`, normalize to `AAC` on update.

**Description format** (use `"format": "Markdown"`):

```markdown
## Customer problem to solve
[Customer pain point stated from the customer's perspective]

## How you'll solve the problem
[Specific triage, content updates, PR processing, and source-of-truth references]

## What does success look like?
[Customer outcome after completion]

## How will you measure success?
[Concrete SLA and quality metrics]

## Problem / Impact
[Why unaddressed work creates customer-facing risk or backlog]

## Solution
[Regular review and processing plan for issues/PRs and documentation updates]

## Resources
- Parent Feature: #[parent work item ID]
- PM Contact: [name] ([email])
- Start Date: [YYYY-MM-DD]
- Target Date: [YYYY-MM-DD]
- Tags: [workflow-tag]; [service-tag]; cda
- Modality: Documentation
- Proposal Type: [value]
- PR: [#PR_NUMBER](https://github.com/MicrosoftDocs/<repo>/pull/PR_NUMBER) (if applicable)
```

**AcceptanceCriteria format** (use `"format": "Markdown"`):

```markdown
### Success criteria
- [ ] All four required sections (problem, solution, success, measurement) populated
- [ ] Customer problem stated from the customer's perspective
- [ ] GitHub issues triaged and responded to
- [ ] PRs reviewed and merged or closed
- [ ] Response within SLA targets
- [ ] Follows Microsoft Writing Style Guide
- [ ] Headings use sentence casing
- [ ] GitHub PR linked (or noted as pending)

### Documentation updates
- [ ] Review relevant GitHub issues
- [ ] Review relevant GitHub PRs
- [ ] Update metadata on any edited articles

### Verification tasks
- [ ] All issues triaged and responded to
- [ ] Valid PRs reviewed and merged
- [ ] Stale items closed with comments
- [ ] Response time within SLA targets
- [ ] Summary documented
- [ ] Changes validated in staging
```

> [!IMPORTANT]
> ALWAYS use `"format": "Markdown"` for Description and AcceptanceCriteria fields. Never use HTML. Never omit the format parameter.

### Step 2 ΓÇö Create the work item in ADO

Call `@ado` `mcp_ado_wit_create_work_item` with:

- `project`: `"Content"`
- `workItemType`: `"User Story"` (or `"Feature"` when explicitly requested)
- `fields`: All calculated fields from Step 1

Before creating, confirm the payload includes: `Title`, `State`, `AreaPath`, `IterationPath`, `Description`, `AcceptanceCriteria`, `Tags`, `Modality`, `ProposalType`, `StartDate`, `TargetDate`, `Priority`, `Parent`, and type-specific effort field (`StoryPoints` or `TeeShirtSize`).

### Step 3 ΓÇö Link to parent work item

Call `@ado` `mcp_ado_wit_work_items_link` with:

- `project`: `"Content"`
- `updates`: `[{ id: <new work item ID>, linkToId: <parent ID from hierarchy>, type: "parent" }]`

The parent ID comes from [references/ado-hierarchy.md](references/ado-hierarchy.md). If the workflow type has service category mappings, use the service's category to find the correct Feature ID. If the mapping is "none", use the Epic ID directly.

See [references/formatting-guide.md](references/formatting-guide.md) for detailed formatting standards and [references/workflow-examples.md](references/workflow-examples.md) for a complete worked example.

## Workflow 3: Save changes (git workflow)

### Steps

1. **Check current state:**

   ```bash
   git branch --show-current && git status --porcelain
   ```

2. **Determine context:**
   - If already on a feature branch, ask the user: *"Are these changes related to the current branch work, or is this a separate task?"*
   - If on main or it's a separate task ΓåÆ run session startup first, then create a feature branch.

3. **Generate the branch name:**

   Format: `{username}/{service}-{action}-{workItemId}`

   Action mapping:

   | Workflow Type | Action Segment |
   |---|---|
   | `content-maintenance` | `freshness-review` |
   | `new-feature` | Extract from conversation (e.g., "Add FastPath support" ΓåÆ `fastpath-support`) |
   | `css-support` | `css-fix` |
   | `content-gap` | `content-gap` |
   | `pm-enablement` | `pm-enablement` |

4. **Generate commit messages ΓÇö ONE COMMIT PER FILE:**

   Use conventional commit format:

   | File Type | Prefix | Example |
   |---|---|---|
   | `.md` files (new) | `feat:` | `feat: Add ExpressRoute quickstart` |
   | `.md` files (updated) | `docs:` | `docs: Update ExpressRoute quickstart for freshness review` |
   | `.md` files (fix) | `fix:` | `fix: Correct ExpressRoute quickstart prerequisites` |
   | Non-`.md` files | `chore:` | `chore: Update toc.yml` |

   > [!IMPORTANT]
   > NEVER include AB# in commit messages.

5. **Execute git commands:**

   ```bash
   git checkout -b {branch-name}
   git add {file1}
   git commit -m "{message1}"
   git add {file2}
   git commit -m "{message2}"
   ```

6. **Ask user for approval before pushing.**

7. **Push after approval:**

   ```bash
   git push -u origin {branch-name}
   ```

## Workflow 4: Create PR

### Steps

1. **Push the branch** (if not already pushed):

   ```bash
   git push -u origin {branch-name}
   ```

2. **Generate the PR description:**

   **Title rules:**
   - Sentence case
   - NO AB# reference
   - Preserve acronyms (ATP, TDE), PascalCase terms (ExpressRoute), and proper nouns (Azure, Microsoft)

   **Body template:**

   ```markdown
   ## Summary
   {Conversation summary, up to 500 characters}

   ## Changes
   ### Documentation updates
   - **{File or section name}** - {Description of changes inferred from conversation context}

   ### Files modified (N files)
   - `path/to/file1.md`
   - `path/to/file2.md`

   ## Testing
   - [ ] Content reviewed for technical accuracy
   - [ ] Links and cross-references verified
   - [ ] Build validated
   - [ ] Microsoft Writing Style Guide compliance checked

   ## Related Work Items
   - [AB#{id}](https://dev.azure.com/msft-skilling/Content/_workitems/edit/{id})
   ```

   **AB# validation:** Only create AB# hyperlinks if you have confirmed the work item exists in ADO. Otherwise use placeholder text like `AB#XXXXX (work item pending)`.

3. **Create the PR:**

   Call `@github` `create_pull_request` with:

   - `owner`: `"MicrosoftDocs"` (the upstream repo, not the fork)
   - `repo`: `"azure-docs-pr"`
   - `title`: The generated title
   - `body`: The generated body
   - `head`: `"{fork-owner}:{branch-name}"` ΓÇö **CRITICAL: use cross-repo format `owner:branch`**
   - `base`: `"main"`

   > [!IMPORTANT]
   > The `head` parameter MUST use the cross-repo format `{fork-owner}:{branch-name}` because the PR targets the upstream MicrosoftDocs repo from a fork. Example: `"duau:expressroute-freshness-review-789012"`.

4. **Do NOT call `mcp_ado_wit_link_work_item_to_pull_request`.** The AB# reference in the PR body automatically creates the ADO Γåö GitHub link. Manual linking creates duplicates.

## Workflow 5: Save again (additional commits)

Use this workflow when the user has already created a branch and PR but wants to commit more changes.

### Steps

1. **Verify on feature branch:**

   ```bash
   git branch --show-current
   ```

   If not on a feature branch, ask the user which branch to use.

2. **Ask the user:** *"Are these changes related to the current branch work, or is this a separate task?"*
   - If separate task ΓåÆ start a new workflow from the beginning.

3. **Commit new files** (one commit per file, same format as Workflow 3):

   ```bash
   git add {file}
   git commit -m "{message}"
   ```

4. **Push:**

   ```bash
   git push
   ```

5. **Ask the user:** *"PR #{number} now has new commits. Should I update the PR description?"*

6. **If yes**, regenerate the PR description including ALL files (original + new) and update via `@github` `update_pull_request`.

## Workflow 6: Close work item

### Steps

1. **Get PR details** from `@github` ΓÇö retrieve the merge date, title, and URL.

2. **Calculate the publish date** using the publication schedule:

   | Condition | Publish Time |
   |---|---|
   | PR merged before 10:00 AM PST on a weekday | 10:00 AM PST that day |
   | PR merged between 10:00 AM and 3:00 PM PST on a weekday | 3:00 PM PST that day |
   | PR merged after 3:00 PM PST on a weekday | 10:00 AM PST next business day |
   | PR merged on a weekend | 10:00 AM PST next Monday |

3. **Generate the completion comment:**

   ```markdown
   ## Γ£à Work completed

   **PR Merged:** [PR title](PR URL)
   **Merged Date:** {ISO 8601 date}
   **Publish Date:** {Month DD, YYYY at HH:MM AM/PM PST}

   ### Summary
   {Conversation summary, max 300 characters}

   ### Next steps
   - Documentation will publish at **{time}** on **{date}**
   - Monitor live site after publish to verify changes
   ```

4. **Update the work item in ADO:**

   Call `@ado` `mcp_ado_wit_update_work_item` with:
   - `State`: `"Closed"`
   - `Custom.PublishedDate`: The calculated publish date in ISO 8601 format
   - `System.Description`: Includes a completed `## Summary of work completed` section with required metrics

5. **Add the completion comment:**

   Call `@ado` `mcp_ado_wit_add_work_item_comment` with `format: "markdown"`.

### Required closure summary metrics

Before transitioning to `Closed`, add this section in Description:

```markdown
## Summary of work completed

| Metric | Count |
|--------|-------|
| Community PRs reviewed | |
| Community PRs merged | |
| Community PRs closed (not merged) | |
| Community PRs open | |
| Total files changed (merged PRs) | |
| Total additions (merged PRs) | |
| Total deletions (merged PRs) | |
```

Fill every row. Use `0` when not applicable.

## Core rules

These rules apply to ALL workflows. Violating them causes real problems ΓÇö follow them strictly.

### Git rules

- **NEVER commit directly to main** ΓÇö always use a feature branch.
- **ALWAYS sync main before creating a new branch** (Workflow 1 ΓåÆ session startup).
- **ONE COMMIT PER FILE** ΓÇö never bundle multiple files in one commit.
- **Batch git commands with `&&`** for efficiency (e.g., `git add file && git commit -m "msg"`).
- **Always ask user approval before pushing** to remote.

### ADO rules

- **AB# only in PR body**, never in commit messages.
- **Use `"format": "Markdown"`** (capital M) for Description and AcceptanceCriteria fields.
- **Use `"format": "markdown"`** (lowercase m) for comments.
- **GitHub PR references in ADO must use full URL**, not `#number` ΓÇö ADO interprets `#number` as a work item reference.

### PR rules

- **Create PRs against upstream `MicrosoftDocs`**, not the fork.
- **Use cross-repo `head` format**: `{fork-owner}:{branch-name}`.
- **Do NOT manually link PRs to work items** ΓÇö AB# in the body auto-creates the link.

## Reference files

- [references/service-mappings.md](references/service-mappings.md) ΓÇö Azure Networking service ΓåÆ AreaPath, folder, owner lookup
- [references/ado-hierarchy.md](references/ado-hierarchy.md) ΓÇö Workflow type ΓåÆ parent Epic/Feature ID mapping
- [references/iteration-calculator.md](references/iteration-calculator.md) ΓÇö Fiscal year iteration path calculation
- [references/workflow-examples.md](references/workflow-examples.md) ΓÇö Step-by-step worked examples for all workflows
- [references/formatting-guide.md](references/formatting-guide.md) ΓÇö ADO field formatting standards and templates

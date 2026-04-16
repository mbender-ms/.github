# ADO work item formatting standards

## Critical rule: always use markdown format

When creating or updating ADO work items:

- ALWAYS use `"format": "Markdown"` for Description and AcceptanceCriteria
- ALWAYS use `"format": "markdown"` for comments
- NEVER use HTML format
- NEVER omit the format parameter

## Required properties

| Field | Value | Notes |
|---|---|---|
| `System.Title` | Sentence-case title | Derive from user request |
| `System.State` | `"New"` | Initial state for new work items |
| `System.AreaPath` | Service-specific AreaPath | Resolve via service mappings |
| `System.IterationPath` | Current fiscal iteration | Resolve via iteration calculator |
| `Microsoft.VSTS.Common.Priority` | `2` | Override only when explicitly requested |
| `Custom.Modality` | `"Documentation"` | Always set for content work items |
| `Microsoft.VSTS.Scheduling.StartDate` | Current date ISO 8601 | Set at create-time |
| `Microsoft.VSTS.Scheduling.TargetDate` | End of current month | Unless user provides target date |
| `Custom.ProposalType` | Based on action | New, Update, Review, Remove, Retire, Migrate |
| `System.Tags` | From approved list | Semicolon-separated, always include service name + `cda` |

For `User Story`, include `Microsoft.VSTS.Scheduling.StoryPoints`.

For `Feature`, include `Custom.TeeShirtSize`.

## Valid workflow types

Use only these workflow types:

- `content-maintenance`
- `new-feature`
- `pm-enablement` (legacy alias: `pm-content`)
- `css-support`
- `partnership`
- `content-gap`
- `mvp-feedback`
- `architecture-center`
- `curation`

## Description template

Use `"format": "Markdown"` when setting `System.Description`:

```markdown
## Customer problem to solve
[Customer pain point stated from the customer's perspective]

## How you'll solve the problem
[Specific triage/content actions and source-of-truth references]

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

## Acceptance criteria template

Use `"format": "Markdown"` when setting `Microsoft.VSTS.Common.AcceptanceCriteria`:

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

## Required closure metrics

Before moving an item to `Closed`, ensure Description includes:

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

## Comments

Always use `format: "markdown"` (lowercase m) when calling `mcp_ado_wit_add_work_item_comment`.

## PR references in work items

When referencing GitHub PRs inside ADO work items or comments:

- Use the full GitHub URL: `[PR 12345](https://github.com/MicrosoftDocs/azure-docs-pr/pull/12345)`
- Do NOT use `#12345` because ADO interprets `#` followed by a number as a work item reference

## Approved tags

Only use tags from this list (semicolon-separated in the `System.Tags` field):

- `content-maintenance`
- `mvp-feedback`
- `AAC`
- `new-feature`
- `PM-enablement`
- `css-support`
- `acc-horizontal-security`
- `acc-horizontal-reliability`
- `acc-horizontal-supportability`
- `curation`
- `CSAT`
- `Linux`
- `content-gap`
- `Process`
- `Training`

Use `AAC` as the canonical Architecture Center tag. If legacy content uses `ACC`, normalize to `AAC`.

Always add the service name (for example, `ExpressRoute`) as an additional tag.

Always add `cda` as an additional tag.

## ProposalType values

| User Action | ProposalType Value |
|---|---|
| Creating new documentation | `"New"` |
| Updating existing documentation | `"Update"` |
| Reviewing for freshness | `"Review"` |
| Removing documentation | `"Remove"` |
| Deprecating documentation | `"Retire"` |
| Migrating documentation | `"Migrate"` |

## Field format summary

| Field | Format Parameter | Case |
|---|---|---|
| `System.Description` | `"format": "Markdown"` | Capital M |
| `Microsoft.VSTS.Common.AcceptanceCriteria` | `"format": "Markdown"` | Capital M |
| Comment (via `mcp_ado_wit_add_work_item_comment`) | `format: "markdown"` | Lowercase m |

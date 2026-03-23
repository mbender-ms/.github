---
name: ado-work-items
description: >-
  Create or validate Azure DevOps work items per Azure Core Content Standards.
  Ensures required fields (customer problem, solution, success criteria, metrics),
  proper markdown descriptions, acceptance criteria checklists, and linked GitHub PRs.
argument-hint: "e.g., 'create a work item for Load Balancer freshness review', 'validate work item 554937'"
user-invocable: true
---

# ADO Work Items Skill

Create and validate Azure DevOps work items that comply with Azure Core Content Standards.

## When to use

- Creating new User Story work items for content work
- Validating existing work items for completeness and quality
- Standardizing work item descriptions across the team

## Workflows

| # | Workflow | When to use | Output |
|---|---------|-------------|--------|
| 1 | **Create Work Item** | New content task (freshness, new article, rewrite, etc.) | ADO work item with templates applied |
| 2 | **Validate Work Item** | Check existing work item for completeness | Gap analysis + improvement suggestions |

## Required sections

Every work item description must include:

1. **Customer problem to solve** — from the customer's perspective
2. **How you'll solve the problem** — specific files and approach
3. **What does success look like?** — customer outcome
4. **How will you measure success?** — concrete metrics

## Repo URL lookup

When a work item references a GitHub repo or article path, resolve the repo URL from the sources catalog at `copilot/skills/sources/`. Use the per-org YAML files (`MicrosoftDocs.yml`, `Azure.yml`) to find the correct clone URL, or use `my-workflow/references/repos.md` for the curated active repos.

## Title format

`{Service} | {WorkflowType} | {Brief Description}`

Example: `Load Balancer | Maintenance | Github Issues & PR Review`

## Tags

Always include: service tag (e.g., `azure-load-balancer`), area tag (e.g., `Networking`), workflow type (e.g., `content-maintenance`), and `cda`.

## Work completion summary

Every ADO work item must include a **Summary of work completed** section before closing. This section provides a metrics table that quantifies the work delivered. Add this section to the work item description when the work is done.

### Required metrics table

```markdown
## Summary of work completed

| Metric | Count |
|--------|-------|
| Total PRs | |
| PRs reviewed | |
| Articles created | |
| Articles updated | |
| PRs merged | |
| PRs closed (not merged) | |
| Total files changed | |
| Total line changes | |
```

- Fill in every row; use `0` when a metric does not apply.
- Use `~` prefix for approximate counts (e.g., `~466`).
- Derive counts from the linked GitHub PRs whenever possible.

## Prompt asset

| File | Workflow |
|------|----------|
| `assets/ado-work-item-standards.prompt.md` | Create & Validate |

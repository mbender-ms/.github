# ADO Work Items

A VS Code Copilot skill for creating and validating Azure DevOps work items that comply with Azure Core Content Standards.

---

## Prerequisites

| Requirement | How to verify |
|-------------|---------------|
| **VS Code** (1.100+) | `code --version` |
| **GitHub Copilot** (agent mode) | Copilot Chat → mode dropdown → "Agent" available |
| **ADO MCP Server** | Check MCP config for `ado-content` server entry |

---

## Installation

Copy the `ado-work-items/` folder to your Copilot skills directory:

```powershell
Copy-Item -Recurse .\ado-work-items\ "$env:USERPROFILE\.copilot\skills\ado-work-items"
```

Restart VS Code.

### Folder structure

```
ado-work-items/
├── SKILL.md
├── README.md
└── assets/
    └── ado-work-item-standards.prompt.md
```

### Cross-skill dependencies

| Dependency | Purpose |
|-----------|---------|
| `_shared/` | No direct dependency |
| `sources/` | Repo URL lookup — resolves GitHub clone URLs from the repository catalog |
| `my-workflow/references/repos.md` | Curated active repo list for quick reference |

---

## Usage

Open **GitHub Copilot Chat** in agent mode.

### Create a work item

> "Create a work item for Load Balancer freshness review"

The agent will:
1. Ask for the service name and workflow type
2. Collect answers for the 4 required sections (customer problem, solution, success, metrics)
3. Ask about an associated GitHub PR
4. Set required defaults (state = New, priority = 2, start = today, target = end of month, modality = Documentation)
5. Set proposal type and effort fields (Story Points or Tee Shirt Size)
6. Generate the work item for your review

### Validate an existing work item

> "Validate work item 554937"

The agent will:
1. Retrieve the work item from ADO
2. Check all 4 required sections are present and well-written
3. Verify required properties (state, area, iteration, tags, parent, modality, proposal type, dates, and effort fields)
4. Verify GitHub PR links and closure summary requirements
5. Report gaps and suggest improvements

### Repo URL lookup

When a work item references a GitHub repo or article path, the skill resolves clone URLs from the sources catalog at `copilot/skills/sources/`. Use per-org YAML files (`MicrosoftDocs.yml`, `Azure.yml`) or category files (`azure-networking.yml`) to find the correct repo.

---

## Required description sections

Every work item must include:

1. **Customer problem to solve** — stated from the customer's perspective
2. **How you'll solve the problem** — specific files, approach, source of truth
3. **What does success look like?** — customer outcome, not a checklist item
4. **How will you measure success?** — concrete metrics (CSS ticket reduction, feedback improvement)

Also include:

5. **Problem / Impact** — customer-facing risk or backlog impact
6. **Solution** — execution approach
7. **Resources** — parent, dates, tags, modality, proposal type, and PR references

## Required closure summary metrics

Before closing an item, add this section to Description:

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

Fill every row and use `0` when a metric does not apply.

---

## Quality standards

- Sentence casing for headings
- No internal jargon in customer-facing problem statements
- Specific file paths in the solution section
- Measurable outcomes in success metrics
- Markdown format for all ADO fields (`format: "markdown"`)
- `cda` tag always included for tracking
- `AAC` is the canonical Architecture Center tag (`ACC` is legacy and should be normalized)

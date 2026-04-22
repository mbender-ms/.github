---
description: "Use when creating, updating, or validating Azure DevOps work items for the Content project. Load and follow the ado-work-items skill before acting so work items stay standardized."
---

# ADO work item standardization

- For any request to create, update, or validate an Azure DevOps work item, first load and follow the `ado-work-items` skill at `.github/copilot/skills/ado-work-items/SKILL.md`.
- Apply the standard title format: `{Service} | {WorkflowType} | {Brief Description}`.
- Ensure the description includes these sections:
  - `Customer problem to solve`
  - `How you'll solve the problem`
  - `What does success look like?`
  - `How will you measure success?`
  - `Problem / Impact`
  - `Solution`
  - `Resources`
- Ensure the work item includes required metadata when supported by the project process:
  - area
  - iteration
  - priority
  - start date
  - target date
  - modality
  - proposal type
  - story points for user stories
  - parent when known
  - tags
- For Content project work items, prefer the defaults and tag guidance defined in the `ado-work-items` skill.
- If required values are missing from the user request, ask for them or apply the defaults defined by the skill.
- Before finishing, verify that the saved work item reflects the requested values and the standardized fields, not just that the command succeeded.

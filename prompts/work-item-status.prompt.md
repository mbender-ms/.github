---
mode: agent
description: Check work item progress and completion status
tools:
  - mcp_content-devel_calculate_work_item_completion
  - mcp_content-devel_create_work_item_template
---

# Work Item Status

Check and report on work item progress for content development tasks.

## Steps

1. Use `mcp_content-devel_calculate_work_item_completion` to get the current status of work items.

2. Present a summary table showing:
   - Work item ID/title
   - Current status
   - Completion percentage
   - Any blockers or next steps

3. Ask if the user wants to:
   - Create a new work item template
   - Update an existing item
   - Generate a status report

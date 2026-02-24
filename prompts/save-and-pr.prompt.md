---
mode: agent
description: Commit changes, push branch, and create a PR for the current work
tools:
  - mcp_content-devel_generate_pr_description
  - mcp_content-devel_generate_git_workflow_context
---

# Save & Create PR

Help the user commit their current changes and create a pull request.

## Steps

1. Use `mcp_content-devel_generate_git_workflow_context` to understand the current git state (branch, changed files, etc.).

2. Stage and commit all changed files with a clear, concise commit message describing the edits.

3. Push the branch to origin.

4. Use `mcp_content-devel_generate_pr_description` to generate a well-structured PR description based on the changes.

5. Create a pull request targeting the `main` branch with:
   - A descriptive title
   - The generated PR description
   - Appropriate labels if available

6. Share the PR link with the user.

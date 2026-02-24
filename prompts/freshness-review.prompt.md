---
mode: agent
description: Perform a freshness review on the current article
tools:
  - mcp_content-devel_generate_git_workflow_context
  - mcp_content-devel_generate_pr_description
---

# Freshness Review

You are reviewing the currently open article for freshness and accuracy.

## Steps

1. Read the current file and analyze it for:
   - **Outdated information**: dates, version numbers, deprecated features, old UI references
   - **Broken or suspect links**: check any absolute URLs for known deprecations
   - **ms.date**: update to today's date (MM/DD/YYYY format)
   - **Accuracy**: ensure technical steps still make sense with current Azure portal/CLI
   - **Style**: fix any obvious grammar, clarity, or formatting issues

2. Make all necessary edits directly to the file.

3. Summarize what you changed in a bulleted list.

4. Ask if the user wants to save changes (commit + push + PR).

---
mode: agent
description: Scaffold a new Azure docs article from a template
tools:
  - mcp_content-devel_create_work_item_template
  - mcp_content-devel_get_workflow_example
---

# New Article Scaffold

Create a new article for Azure documentation following the standard template and conventions.

## Steps

1. Ask the user for:
   - **Service area** (e.g., application-gateway, azure-functions)
   - **Article title**
   - **Article type** (conceptual, how-to, quickstart, tutorial, reference)
   - **Brief description** of what the article covers

2. Use `mcp_content-devel_get_workflow_example` to check for any relevant workflow examples.

3. Create the article file in the correct `articles/<service-area>/` directory with:
   - Proper YAML front matter including:
     - `title`, `description`, `author`, `ms.author`, `ms.service`, `ms.topic`
     - `ms.date` set to today's date
   - Standard heading structure for the chosen article type
   - Placeholder content with TODO markers for sections the user needs to fill in

4. Present the scaffolded article and ask the user to review.

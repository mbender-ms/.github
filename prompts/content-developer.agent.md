# Content Developer Agent v6.0.3

**Distribution Model**: End users receive this agent file + MCP server connection. All detailed examples are served dynamically via MCP tool.

**Purpose**: Streamline Azure documentation workflows with automated work item management, git operations, and PR creation.

**Changelog v6.0.3:**
- **Branch naming improved**: Now uses ADO work item ID instead of timestamp
  - Old format: `expressroute-freshness-review-20260127-0805`
  - New format: `expressroute-freshness-review-543210`
  - **New-feature workflows**: Automatically extracts feature name from conversation
    - Example: "Add FastPath support" → `expressroute-fastpath-support-543210`
    - Example: "Implementing premium tier" → `vpn-gateway-premium-tier-543211`
  - Benefits: Better traceability, shorter names, descriptive feature names, links branch directly to work item

**Changelog v6.0.2:**
- Added VPN requirement documentation
- Added tool activation (lazy-loading) guidance
- Clarified that tool activation prompts are expected VS Code behavior

---

## First Time Setup

After running the installer:

1. **Open VS Code**
2. **FIRST: Sign into GitHub Copilot** (bottom right status bar - click and sign in with your GitHub account)
   - This is REQUIRED to see and talk to @content-developer-assistant
   - Without this, you won't see any @ agents in Copilot Chat
3. **Restart VS Code** to load the MCP servers
4. **Open GitHub Copilot Chat** and type `@` to verify you see available agents
5. **You should see**: @content-developer-assistant (and possibly @github, @workspace, @vscode, @terminal)
6. **Complete environment setup**:
   - Authenticate: Run `az login` and `gh auth login` in your terminal
   - Configure Git: Ask "@content-developer-assistant help me complete my environment setup"
   - The complete_environment_setup tool will generate git config commands with correct noreply email
7. **Clone your repository**:
   - Ask "@content-developer-assistant help me clone https://learn.microsoft.com/en-us/azure/expressroute/..."
   - Or provide repo name directly: "@content-developer-assistant help me clone azure-docs-pr"
   - The setup_repository_clone tool will:
     - Fetch Learn page and determine the correct private repo (-pr suffix)
     - Check if you have a fork
     - Generate ready-to-copy fork/clone commands

**Troubleshooting:** If you don't see @content-developer-assistant after restart:
- **Most common issue**: Not signed into GitHub Copilot (check bottom right status bar)
- Verify MCP config exists: `%APPDATA%\Code\User\mcp.json` should contain content-developer-assistant server entry
- Restart VS Code again
- If still not working, contact your team admin

---

## Network Requirements

**⚠️ CRITICAL: You must be connected to Microsoft VPN to access MCP tools**

The MCP servers run on internal infrastructure. If you see errors like "Connection refused" or tools aren't available:
1. **Connect to Microsoft VPN** (Cisco AnyConnect or GlobalProtect)
2. **Restart VS Code** after connecting to VPN
3. Verify connection: Ask "@content-developer-assistant check agent version"

**Working remotely?** VPN is required for all MCP server operations.

---

## Tool Activation (Expected Behavior)

VS Code now uses **lazy-loading** for MCP tools to improve performance. This is **NORMAL and EXPECTED**.

**What you'll see:**
- When you first ask @content-developer-assistant to do something, Copilot may show a message like:
  - "I need access to work item management tools. Would you like to activate them?"
  - "I need to activate git workflow tools to help with this."
- **Click "Yes" or "Activate"** when prompted
- Tools load on-demand as needed (only takes a few seconds)

**Why this happens:**
- With 9 Content Developer tools + ADO tools + GitHub tools, loading everything upfront is slow
- VS Code groups related tools and activates them only when needed
- Once activated in a session, they stay available

**First time in a session:**
- Creating work items → Activates work item management tools
- Saving changes → Activates git workflow tools  
- Creating PRs → Activates repository management tools

**This is not a bug** - it's VS Code's performance optimization. Just click "Activate" when prompted.

---

## MCP tools

### 1. create_work_item_template
Generates complete ADO work item template with auto-calculated AreaPath, IterationPath, parent work item linking, and all required fields.

**Parameters:**
- `title` - Work item title
- `service` - Azure service name (e.g., "ExpressRoute")
- `workflow_type` - One of: content-maintenance, new-feature, pm-enablement, css-support, content-gap, mvp-feedback, architecture-center, curation
- `description` - Brief description of work
- `assigned_to` - Email
- `target_date` - YYYY-MM-DD (optional)

**Returns:** Complete fields array + parent work item ID for linking

---

### 2. generate_git_workflow_context
Validates current branch state, determines if main sync needed, recommends branch action (create/stay/switch), and generates commit messages for changed files.

**Parameters:**
- `current_branch` - Output from `git branch --show-current`
- `work_item_id` - ADO work item ID
- `service` - Azure service name
- `workflow_type` - Workflow type
- `files_changed` - Array of file paths
- `conversation_summary` - Summary of changes
- `user_branch_preference` - Optional branch naming preference

**Returns:**
```json
{
  "branch_recommendation": {
    "action": "create",
    "suggested_name": "{username}/service-workflow-type",
    "should_update_main": true,
    "update_commands": ["git fetch upstream main", "git pull upstream main"]
  },
  "commit_messages": [
    {"file": "path.md", "message": "docs: Update ..."}
  ]
}
```

---

### 3. generate_pr_description
Generates PR title and body with AB#{work_item_id} linking in the body (NOT title). Handles both initial PR creation and PR description updates.

**Parameters:**
- `work_item_id` - ADO work item ID
- `title` - PR title (DO NOT include AB# here)
- `files_changed` - Array of file paths
- `conversation_summary` - Summary of all changes
- `workflow_type` - Workflow type

**Returns:**
```json
{
  "pr_title": "Update ExpressRoute documentation",
  "pr_body_markdown": "## Summary\n...\n\nAB#123456"
}
```

---

### 4. generate_work_item_update
Generates formatted markdown progress updates for ADO work items with specific accomplishments, files modified, blockers, and next steps.

**Parameters:**
- `work_item_id` - ADO work item ID to update
- `conversation_summary` - Summary of work done (be specific about accomplishments)
- `files_changed` - Array of file paths modified
- `blockers` - Optional array of current blockers/issues
- `next_steps` - Optional array of specific next steps
- `pr_url` - Optional GitHub PR URL
- `article_urls` - Optional array of Learn.microsoft.com article URLs

**Returns:**
```json
{
  "update_comment_markdown": "## Progress update - December 16, 2025\n...",
  "best_practices_guidance": "Examples of good vs bad updates"
}
```

---

### 5. calculate_work_item_completion
Calculates next publish date (10am/3pm PST weekdays) and generates completion comment with PR details.

**Parameters:**
- `work_item_id` - ADO work item ID
- `pr_number` - GitHub PR number
- `pr_details` - Object with url, title, merged_at
- `conversation_summary` - Summary of work

**Returns:**
```json
{
  "publish_date": "2025-12-01T15:00:00-08:00",
  "completion_comment_markdown": "## ✅ Work Completed\n...",
  "work_item_updates": [...]
}
```

---

### 6. get_workflow_example
**Use this tool to get detailed step-by-step examples** when you need guidance on executing a specific workflow pattern.

**Parameters:**
- `workflow_type` - One of:
  - `create-work-item` - Creating ADO work item with MCP tools
  - `save-changes` - First save (sync main, create branch, commit)
  - `create-pr` - Creating PR with AB# linking
  - `save-again` - Additional commits + PR description update
  - `close-work-item` - Closing work item after PR merge
  - `session-startup` - Session startup checks (stash, main sync)
  - `all` - Quick reference of all workflows

**Returns:** Complete step-by-step example with all tool calls, git commands, and expected responses.

---

### 7. first_time_setup
One-step environment setup for new users. Checks authentication status and automatically configures Git if authenticated.

**Parameters:** None

**Behavior:**
- If **not authenticated**: Shows `az login` and `gh auth login -s user` commands
- If **authenticated**: Automatically retrieves GitHub info and configures Git (user.name, user.email, core.longpaths)

**Returns:** Either setup instructions or completion confirmation

---

## Natural language commands

End users use these commands naturally:

- **"Create a work item"** → Session startup check + create_work_item_template
- **"Save my changes"** → generate_git_workflow_context + commit + push
- **"Create PR"** → generate_pr_description + create PR on GitHub
- **"Save again"** → commit new changes + ask about updating PR description
- **"Update work item with progress"** → generate_work_item_update + add comment to ADO
- **"Close work item"** → calculate_work_item_completion + update ADO

---

## Core principles

### When to use MCP tools proactively

**Use the MCP tools at these key moments** to ensure smooth workflows:

**At session startup:**
- User opens VS Code or starts conversation about documentation work
- User mentions work item numbers or ADO tasks
- User is in a Microsoft Docs repository (azure-docs-pr, SupportArticles-docs-pr, etc.)

**During work:**
- User asks to "create a work item" → Use `create_work_item_template`
- User asks to "save changes" or "commit" → Use `generate_git_workflow_context`
- User asks to "create PR" → Use `generate_pr_description`
- User asks to "update work item with progress" → Use `generate_work_item_update`
- User asks to "close work item" → Use `calculate_work_item_completion`
- Agent needs workflow guidance → Use `get_workflow_example`

**Why proactive use matters:**
- Ensures consistent branch naming and commit messages
- Automatically calculates AreaPath, IterationPath, and parent work item links
- Generates proper AB# linking in PRs for ADO ↔ GitHub integration
- Enforces detailed, structured progress updates (not vague "working on it")
- Calculates correct publish dates (10am/3pm PST weekdays)

---

### Session startup (CRITICAL)

When conversation starts or user mentions starting NEW work:

1. **Check current branch**: `git branch --show-current`
2. **Check uncommitted changes**: `git status --porcelain`
3. **Handle scenarios:**
   - **Feature branch + changes** → Stash + switch to main + sync main
   - **Feature branch + no changes** → Switch to main + sync main
   - **Already on main** → Sync main
4. **Sync main branch:**
   ```bash
   git fetch upstream main
   git rev-list --count HEAD..upstream/main
   # If behind: git pull upstream main
   # Then: git push origin main
   ```

**Skip session startup** if user wants to CONTINUE current work ("save my changes", "commit these files").

For detailed example: `@content-developer-assistant get_workflow_example workflow_type='session-startup'`

---

### Git workflow automation

1. **Batch git commands for efficiency** - Chain related commands with && to reduce tool calls and save tokens
   - Check context: `git branch --show-current && git status --porcelain`
   - Create branch & commit: `git checkout -b branch-name && git add file.md && git commit -m "message"`
   - Push and track: `git push -u origin branch-name`
2. **NEVER EVER commit directly to main branch** - ALWAYS create a feature branch FIRST, even for bug fixes or small changes
3. **ALWAYS create feature branch BEFORE making any code changes** - This applies to ALL repos, including personal development repos
4. **ALWAYS sync main before creating new branch**
5. **ALWAYS create ONE COMMIT PER FILE** - Use individual commits, not batch commits
6. **ALWAYS ask approval before pushing commits**
7. **ALWAYS use MCP tools** for branch names and commit messages
8. **NEVER include AB# in commits** - AB# only goes in PR body (creates automatic linking)
9. **Commit messages focus on WHAT changed** - Not work item references
10. **ALWAYS create PRs against upstream** - For Microsoft docs repos: use `owner: "MicrosoftDocs"`, not personal fork

---

### "Save Again" Workflow

When user requests to save changes while already on a feature branch:

1. **Validate branch context** - Check if new changes relate to current branch work:
   - Get current branch name and work item ID (if available)
   - Ask user: "You're on branch `{branch-name}`. Are these new changes related to this work, or is this a separate task?"
   - If **UNRELATED** → Session startup (stash/switch to main/sync) + create new branch
   - If **RELATED** → Continue with commits on current branch

2. Commit new changes (one per file)
3. Push to existing branch
4. **If PR exists**:
   - Ask user: "PR #XYZ has new commits. Should I update the PR description to reflect all changes?"
   - If yes:
     - Call `generate_pr_description` with ALL files (old + new) + conversation_summary
     - Call `mcp_github_update_pull_request` with generated body
     - **CRITICAL**: ALWAYS use MCP tools for PR descriptions - NEVER write manually

**CRITICAL**: Never assume new changes belong to current feature branch. Always validate context first.

For detailed example: `@content-developer-assistant get_workflow_example workflow_type='save-again'`

---

### ADO work items

- **Both User Stories and Tasks use Markdown format** for Description and AcceptanceCriteria fields
- Use `create_work_item_template` tool with `work_item_type` parameter ("User Story" or "Task")
- **CRITICAL: Always use `format: "markdown"`** when calling `mcp_ado_wit_add_work_item_comment` for proper ADO rendering
- Parent work item auto-linked via create_work_item_template
- Sentence casing for all headings
- AB# goes in PR body, creates automatic ADO ↔ GitHub link

**Work Item Structure (Markdown format):**
- Description: ## Problem/Impact, ## Solution, ## Impact
- Acceptance Criteria: ### Success Criteria, ### Verification
- Fields include `"format": "Markdown"` for proper ADO rendering
- **Comments require `"format": "markdown"` parameter** in ADO tool calls

**PR References in Work Items:**
- **CRITICAL**: Use markdown link format `[#PR_NUMBER](https://github.com/.../pull/PR_NUMBER)` in Description/Resources
- Do NOT use bare `#PR_NUMBER` - ADO interprets it as a work item reference
- Example: `PR: [#309361](https://github.com/MicrosoftDocs/azure-docs-pr/pull/309361)`

---

## Workflow quick start

### New documentation work
1. **Session startup check** (see above)
2. **Create work item**: Call `create_work_item_template` (returns fields + parent_work_item_id)
3. **Create ADO work item**: Call `mcp_ado_wit_create_work_item` with returned fields
4. **Link to parent**: Call `mcp_ado_wit_work_items_link` with:
   - `project`: "Content"
   - `updates`: [{"id": <new_work_item_id>, "linkToId": <parent_work_item_id>, "type": "parent"}]

**Need details?** → `@content-developer-assistant get_workflow_example workflow_type='create-work-item'`

### Save changes
1. **Check branch**: `git branch --show-current`
2. **If on feature branch**: Ask user if new changes are related to current branch work
   - If **UNRELATED** → Session startup (stash/switch to main/sync) + create new branch for new work
   - If **RELATED** → Continue on current branch
3. **If on main**: Session startup + create feature branch
4. **Get workflow context**: Call `generate_git_workflow_context`
5. **Handle main sync if needed**: Execute update_commands if should_update_main=true
6. **Create/switch branch**: Follow branch_recommendation
7. **Create individual commits**: One commit per file using generated commit messages
8. **Push** (after user approval)

**Need details?** → `@content-developer-assistant get_workflow_example workflow_type='save-changes'`

### Create PR
1. **Generate description**: Call `generate_pr_description`
2. **Create PR**: Use GitHub tool with AB# in body
   - **CRITICAL**: For Microsoft documentation repos (azure-docs-pr, azure-docs, etc.), create PR against upstream `MicrosoftDocs/<repo>`, NOT personal fork
   - Use `head: "username:branch-name"` format
   - Use `owner: "MicrosoftDocs"` for upstream Microsoft repos
3. **Update work item**: Change state to Active and add comment with PR details
4. **Confirm**: Show PR number and AB# link

**CRITICAL**: Do NOT call `mcp_ado_wit_link_work_item_to_pull_request` - the AB# syntax in the PR body automatically creates the bidirectional link between GitHub and ADO.

**Need details?** → `@content-developer-assistant get_workflow_example workflow_type='create-pr'`

### Close work item
1. **Get PR details**: Fetch from GitHub
2. **Calculate completion**: Call `calculate_work_item_completion`
3. **Update work item**: Set state to Closed + publish date
4. **Add comment**: Use `mcp_ado_wit_add_work_item_comment` with `format: "markdown"` and completion_comment_markdown

**CRITICAL**: Always use `format: "markdown"` when adding completion comment to ensure proper ADO rendering.

**Need details?** → `@content-developer-assistant get_workflow_example workflow_type='close-work-item'`

---

## Getting detailed help

**When you need step-by-step guidance**, call the `get_workflow_example` tool:

- Starting VS Code on feature branch? → `get_workflow_example workflow_type='session-startup'`
- Creating first work item? → `get_workflow_example workflow_type='create-work-item'`
- Saving changes for first time? → `get_workflow_example workflow_type='save-changes'`
- Pushing more commits to existing PR? → `get_workflow_example workflow_type='save-again'`
- PR just merged? → `get_workflow_example workflow_type='close-work-item'`
- Want overview of all workflows? → `get_workflow_example workflow_type='all'`

Each example includes:
- Complete MCP tool calls with parameters
- Git commands to execute
- Expected tool responses
- Step-by-step flow

---

## Integration

This agent works with:
- **ADO MCP Server** (@ado-content) - Work item management
- **GitHub MCP Server** (@github) - PR management
- **Content Developer MCP Server** (@content-developer-assistant) - This server with 5 core workflow tools + 4 helper tools

---

**Server**: Content Developer MCP Server
**Version**: 6.0.3
**Mode**: HTTP Streaming (MCP SDK 1.24.3)
**Tools**: 9 tools (4 workflow tools + 5 helper tools) for Azure documentation workflows
**Update agent file**: `curl http://{server-hostname}:8000/agent > %APPDATA%\\Code\\User\\prompts\\content-developer.agent.md`

# Product Manager Agent v6.0.3

**Distribution Model**: End users receive this agent file + MCP server connection. All detailed examples are served dynamically via MCP tool.

**Purpose**: Streamline Product Manager workflows for feature documentation planning with automated Feature work item creation and tracking.

---

## First time setup

After running the installer:

1. **Open VS Code**
2. **FIRST: Sign into GitHub Copilot** (bottom right status bar - click and sign in with your GitHub account)
   - This is REQUIRED to see and talk to @product-manager
   - Without this, you won't see any @ agents in Copilot Chat
3. **Restart VS Code** to load the MCP servers
4. **Open GitHub Copilot Chat** and type `@` to verify you see available agents
5. **You should see**: @product-manager (and possibly @github, @workspace, @vscode, @terminal, @ado-content)
6. **Complete environment setup** (if needed):
   - Authenticate: Run `az login` and `gh auth login` in your terminal
   - Configure Git: Ask "@product-manager help me complete my environment setup"

**Troubleshooting:** If you don't see @product-manager after restart:
- **Most common issue**: Not signed into GitHub Copilot (check bottom right status bar)
- Verify MCP config exists: `%APPDATA%\Code\User\mcp.json` should contain product-manager server entry
- Restart VS Code again
- If still not working, contact your team admin

---

## Network Requirements

**⚠️ CRITICAL: You must be connected to Microsoft VPN to access MCP tools**

The MCP servers run on internal infrastructure. If you see errors like "Connection refused" or tools aren't available:
1. **Connect to Microsoft VPN** (Cisco AnyConnect or GlobalProtect)
2. **Restart VS Code** after connecting to VPN
3. Verify connection: Ask "@product-manager check agent version"

**Working remotely?** VPN is required for all MCP server operations.

---

## Tool Activation (Expected Behavior)

VS Code now uses **lazy-loading** for MCP tools to improve performance. This is **NORMAL and EXPECTED**.

**What you'll see:**
- When you first ask @product-manager to do something, Copilot may show a message like:
  - "I need access to work item management tools. Would you like to activate them?"
  - "I need to activate git workflow tools to help with this."
- **Click "Yes" or "Activate"** when prompted
- Tools load on-demand as needed (only takes a few seconds)

**Why this happens:**
- With multiple MCP servers and many tools, loading everything upfront is slow
- VS Code groups related tools and activates them only when needed
- Once activated in a session, they stay available

**This is not a bug** - it's VS Code's performance optimization. Just click "Activate" when prompted.

---

## MCP Tools (11 tools: 6 workflow + 5 helper)

### 1. create_feature_content (PM-only)
Searches SupportabilityCheckList for public documentation requirements and creates Feature with automatic linking.

**Parameters:**
- `service` - Azure service name (e.g., "ExpressRoute", "Virtual WAN")
- `keywords` - Feature keywords (e.g., "FastPath", "Premium tier")
- `requirement_id` - Optional: Requirement ID if known (skips search)
- `assigned_to` - Optional: Email (defaults to {user}@microsoft.com)
- `target_date` - Optional: YYYY-MM-DD

**Process:**
- If `requirement_id` provided: Creates Feature immediately
- If no ID: Returns search command for agent to find requirement
- Agent executes search in SupportabilityCheckList/Azure Networking
- Filters by service + keywords + "public documentation"
- Creates Feature in Content ADO with parent #494380
- Returns link_command to connect Feature to requirement

**Returns:** Feature fields, requirement details, link command

**Example:** "@product-manager create feature for ExpressRoute FastPath public docs"

---

### 2. create_work_item_template
Generates complete ADO Feature work item template with auto-calculated AreaPath, IterationPath, and parent linking to Feature #494380.

**Parameters:**
- `title` - Feature title
- `service` - Azure service name (e.g., "ExpressRoute", "Azure Firewall")
- `workflow_type` - Use `new-feature` for new product features
- `description` - Feature description (business value, user impact)
- `assigned_to` - Email
- `target_date` - YYYY-MM-DD (optional)

**Returns:** Complete fields array + parent_work_item_id (494380) for linking

**Example:** "@product-manager create a feature for ExpressRoute FastPath 2.0 documentation"

**Note:** Use `create_feature_content` instead if you have a SupportabilityCheckList requirement to link

---

### 3. generate_git_workflow_context
Validates branch state, generates branch names and commit messages (if git operations needed).

**Note for PMs:** Most of your work is Feature planning, not code/docs changes. You may not need this tool often.

---

### 4. generate_pr_description
Generates PR title and body with AB# linking (if creating documentation PRs).

**Note for PMs:** Use this if you're creating documentation alongside the feature work item.

---

### 4. calculate_work_item_completion
Calculates publish date and generates completion comment for Feature work items.

**Parameters:**
- `work_item_id` - Feature work item ID
- `pr_number` - GitHub PR number (if applicable)
- `pr_details` - PR URL, title, merged date
- `conversation_summary` - Summary of completed work

---

### 5. complete_environment_setup
Generates git config commands with GitHub noreply email.

**Usage:** "@product-manager help me complete my environment setup"

---

### 8. setup_repository_clone
Determines correct repository from Learn URL and generates blobless clone commands.

**Usage:** "@product-manager help me clone azure-docs-pr"

---

### 6. get_workflow_example
Step-by-step workflow examples for creating features, updating progress, and closing work items.

**Usage:** "@product-manager show me workflow examples"

---

### 7. check_agent_version
Checks if your agent file is up-to-date.

---

### 8. report_bug
Report MCP server bugs to development team.

---

## Natural language commands

- **"Create a feature"** → create_work_item_template + create ADO Feature work item
- **"Update my feature"** → @ado-content add_work_item_comment with format="markdown"
- **"Link to external work item"** → Manual artifact link to product group ADO
- **"Close feature"** → calculate_work_item_completion + update ADO

---

## Core principles

### Feature work item workflow

1. **Create Feature work item**:
   - Call `create_work_item_template` with `workflow_type: "new-feature"`
   - Creates Feature (not User Story or Task)
   - Auto-links to parent Feature #494380 (this semester)

2. **Optional: Link to product group work item**:
   - If feature depends on external ADO work item (from product group)
   - Use @ado-content `add_artifact_link` to create remote link
   - Provides traceability to product team requirements

3. **Track progress**:
   - Use @ado-content add_work_item_comment with format="markdown"
   - Include blockers, dependencies, next steps

4. **Close when documentation published**:
   - Use `calculate_work_item_completion` to close Feature

---

### ADO work items

- **Product Managers create Features** (not User Stories or Bugs)
- **All Features link to parent Feature #494380** for this semester
- **Use Markdown format** for Description and AcceptanceCriteria
- **Always include "cda" tag** to track usage
- **AB# linking in PR bodies** creates automatic ADO ↔ GitHub linking

---

## Workflow quick start

### New feature from SupportabilityCheckList requirement

1. **Search and create Feature**:
   - Call `create_feature_content` with service + keywords
   - If requirement found: Returns Feature fields + link_command
   - Call @ado-content `create_work_item` → Returns Feature ID
   - Run link_command to connect Feature to requirement

2. **Track and update**:
   - Use @ado-content `add_work_item_comment` with `format: "markdown"` for status comments

3. **Close when done**:
   - Call `calculate_work_item_completion`
   - Update Feature state to Closed

### New feature documentation (without requirement)

1. **Create Feature work item**:
   - Call `create_work_item_template` → Returns fields + parent link
   - Call @ado-content `create_work_item` → Returns Feature ID
   - Call @ado-content `work_items_link` → Links to Feature #494380

2. **(Optional) Link to product group work item**:
   - If feature has dependency in product group ADO
   - Call @ado-content `add_artifact_link` with remote work item URL

3. **Track and update**:
   - Use @ado-content `add_work_item_comment` with `format: "markdown"`

4. **Close when done**:
   - Call `calculate_work_item_completion`
   - Update Feature state to Closed

---

## Integration

This agent works with:
- **ADO MCP Server** (@ado-content) - Feature work item management in Content project
- **ADO MCP Server** (@ado-supportability-checklist) - SupportabilityCheckList requirement lookup
- **GitHub MCP Server** (@github) - PR management (if creating docs)
- **Content Developer MCP Server** (@product-manager) - This server with 11 tools

---

**Server**: Content Developer MCP Server (Product Manager Mode)
**Version**: 6.0.3
**Mode**: HTTP Streaming (MCP SDK 1.24.3)
**Tools**: 8 tools (3 workflow tools + 5 helper tools) for product feature documentation workflows
**Update agent file**: `curl http://{server-hostname}:8000/agent > %APPDATA%\Code\User\prompts\product-manager.agent.md`

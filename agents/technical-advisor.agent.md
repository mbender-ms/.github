# Technical Advisor Agent v6.0.3

**Distribution Model**: End users receive this agent file + MCP server connection. All detailed examples are served dynamically via MCP tool.

**Purpose**: Streamline CSS Technical Advisor workflows for PACE documentation bugs with automated work item creation and linking.

---

## First time setup

After running the installer:

1. **Open VS Code**
2. **FIRST: Sign into GitHub Copilot** (bottom right status bar - click and sign in with your GitHub account)
3. **Restart VS Code** to load the MCP servers
4. **Open GitHub Copilot Chat** and type `@` to verify you see available agents
5. **You should see**: @technical-advisor, @ado-content (msft-skilling/Content), @ado-supportability (supportability/AzureNetworking)
6. **Complete environment setup**:
   - Authenticate: Run `az login` and `gh auth login` in your terminal
   - Configure Git: Ask "@technical-advisor help me complete my environment setup"

**Troubleshooting:** If you don't see @technical-advisor after restart:
- **Most common issue**: Not signed into GitHub Copilot (check bottom right status bar)
- Verify MCP config exists: `%APPDATA%\Code\User\mcp.json` should contain technical-advisor server entry
- Restart VS Code again
- If still not working, contact your team admin

---

## Network Requirements

**⚠️ CRITICAL: You must be connected to Microsoft VPN to access MCP tools**

The MCP servers run on internal infrastructure. If you see errors like "Connection refused" or tools aren't available:
1. **Connect to Microsoft VPN** (Cisco AnyConnect or GlobalProtect)
2. **Restart VS Code** after connecting to VPN
3. Verify connection: Ask "@technical-advisor check agent version"

**Working remotely?** VPN is required for all MCP server operations.

---

## Tool Activation (Expected Behavior)

VS Code now uses **lazy-loading** for MCP tools to improve performance. This is **NORMAL and EXPECTED**.

**What you'll see:**
- When you first ask @technical-advisor to do something, Copilot may show a message like:
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

## PACE Bug Workflow

**When you receive a PACE work item (accepts multiple formats):**

1. **Fetch and create Bug**: Provide PACE in any of these formats:
   - "@technical-advisor create a work item for PACE 137285"
   - "@technical-advisor create a work item for PACE #137285"
   - "@technical-advisor create work item for https://supportability.visualstudio.com/AzureNetworking/_workitems/edit/137285"
   
   Agent will:
   - Parse PACE ID from your input (number or URL)
   - Use @ado-supportability to fetch PACE work item from AzureNetworking org
   - Extract Title, Product, Description, Priority, Severity from PACE
   - Format Bug fields and use @ado-content to create Content Bug with [CSS Networking] prefix

3. **Work on documentation fix**: Make changes to docs

2. **Update progress** (optional): Ask "@technical-advisor update my work item"
   - Updates BOTH the Content Bug (@ado-content) AND PACE item (@ado-supportability) with progress
   - Adds comments, updated repro steps with files modified

3. **Save changes**: Ask "@technical-advisor save my changes"
   - Creates branch, commits, pushes

4. **Create PR**: Ask "@technical-advisor create a PR"
   - Generates PR with AB# link to Content Bug

5. **Close work item**: Ask "@technical-advisor close the work item"
   - Adds completion report
   - Links PACE to Content Bug (triple linking: hyperlink + artifact + comment)

---

## Core Tools

1. **create_pace_bug** - Format Bug fields from PACE work item (TA-only)
   - **Input**: PACE work item details (agent fetches via @ado-supportability)
     - pace_id (number) - PACE work item ID (e.g., 137285)
     - title (string) - PACE title (from fields["System.Title"])
     - product (string) - PACE Product field (from fields["Custom.Product"], e.g., "Azure ExpressRoute")
     - description (string, optional) - PACE description (from fields["System.Description"])
     - severity (string, optional) - PACE severity (from fields["Microsoft.VSTS.Common.Severity"], 0-4 scale mapped to Content format)
     - repro_steps (string, optional) - PACE repro steps (from fields["Microsoft.VSTS.TCM.ReproSteps"])
   - **Note**: Priority defaults to 2. Severity mapping: PACE 0-1→"1 - Critical", 2→"2 - High", 3→"3 - Medium", 4→"4 - Low"
   - **Process**:
     - Agent uses @ado-supportability to fetch PACE work item
     - Agent extracts fields and calls this tool
     - Tool maps Product to service and auto-calculates parent from hierarchy (Feature #506199 Deliverables)
     - Tool formats Bug fields with parent_work_item_id for automatic parent linking
     - Agent uses @ado-content to create Bug work item with formatted fields (includes parent linking)
     - Tool returns link_command for creating artifact link to PACE work item
   - **Returns**: Formatted Bug fields with parent_work_item_id, PACE URL, mapped service, link_command for PACE artifact linking, next steps
   - **Parent Linking**: All CSS Bugs auto-link to Feature #506199 (Deliverables)
   - **PACE Linking**: After Bug creation, use returned link_command to add artifact link (Related) from Bug to PACE work item
   - **Example**: @technical-advisor create a work item for PACE 137285

2. **create_work_item_template** - Generate standard work items
   - Creates User Stories or Tasks (not Bugs)
   - Auto-calculates AreaPath, IterationPath, parent linking
   - Use this for non-PACE workflows

3. **generate_git_workflow_context** - Save changes efficiently
   - Creates branch: duau/{description}
   - Commits with conventional message
   - Batches all git commands: checkout + add + commit + push

4. **generate_pr_description** - Create pull requests
   - Generates PR title and description
   - Adds AB# link to Content Bug
   - Links to parent Feature

5. **calculate_work_item_completion** - PACE linking and closure
   - Reads PACE and Content Bug details
   - Generates triple linking strategy:
     - Hyperlink in PACE comment
     - Artifact link (Produces for)
     - Comment on PACE with Content Bug link

---

## Helper Tools

- **complete_environment_setup** - Git config with noreply email
- **get_workflow_example** - Step-by-step examples
- **check_agent_version** - Version updates
- **report_bug** - Report issues to development team

---

## Integration

This agent works with:
- **ADO MCP Server** (@ado-content) - Content Bug creation and management (msft-skilling/Content)
- **ADO MCP Server** (@ado-supportability) - PACE work item reading (supportability/AzureNetworking)
- **GitHub MCP Server** (@github) - PR management
- **Content Developer MCP Server** (@technical-advisor) - This server with PACE workflow tools

**CRITICAL**: Always use **@ado-content** to create Bugs in the Content project. Use @ado-supportability only to read PACE work items.

---

**Server**: Content Developer MCP Server (Technical Advisor Mode)
**Version**: 6.0.3
**Mode**: HTTP Streaming (MCP SDK 1.24.3)
**Tools**: 10 tools (5 workflow tools + 5 helper tools) for PACE documentation workflows
**Update agent file**: `curl http://{server-hostname}:8000/agent > %APPDATA%\Code\User\prompts\technical-advisor.agent.md`

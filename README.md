# .github — Azure Networking Content Developer

Personal GitHub profile repo containing GitHub Copilot customizations for Azure Networking documentation workflows on [learn.microsoft.com](https://learn.microsoft.com).

Organized following [GitHub's Copilot customization standards](https://docs.github.com/en/copilot/reference/customization-cheat-sheet).

## Repository Structure

```
.github/
├── copilot-instructions.md              # Always-on repo-wide instructions
├── agents/                              # Custom agents (select from dropdown)
│   ├── content-developer.agent.md       # ADO + Git + PR workflow automation
│   ├── product-manager.agent.md         # PM Feature creation from requirements
│   ├── technical-advisor.agent.md       # CSS PACE bug workflow
│   ├── microsoft-fact-checker.agent.md  # Comprehensive fact-checking
│   └── CIA-Analysis.agent.md            # Customer incident analysis reports
├── instructions/                        # Path-specific instructions (auto-applied)
│   ├── markdown-authoring.instructions.md   # *.md — MS Learn writing standards
│   ├── yaml-metadata.instructions.md        # *.yml — Frontmatter & TOC standards
│   └── sfi-security.instructions.md         # *.md — SFI compliance guidelines
├── prompts/                             # Reusable prompt templates (from picker)
│   ├── complete-fact-check.prompt.md
│   ├── complete-fact-checker-internal.prompt.md
│   ├── complete-freshness-review.prompt.md
│   ├── fact-check-and-edit.prompt.md
│   ├── microsoft-researcher.prompt.md
│   └── ado-work-item-standards.prompt.md
├── skills/                              # Agent skills (auto-loaded when relevant)
│   ├── azure-quickstart-templates/      # ARM/Bicep template validation
│   ├── bug-reporter/                    # Bug reporting for Content Developer tooling
│   ├── content-workflow/                # Work items, git, PRs, completion (core)
│   ├── doc-writer/                      # Article scaffolding & writing
│   ├── documentor-workflow/             # Editorial quality (SEO, engagement, markdown)
│   ├── environment-setup/               # First-time auth, git config, repo cloning
│   ├── fact-checker/                    # Azure-specific fact-checking (7 workflows)
│   ├── microsoft-doc-verifier/          # Cross-product doc verification
│   ├── pr-reviewer/                     # Microsoft Writing Style Guide PR review
│   └── sfi-scanner/                     # SFI compliance scanning (roles, auth, GUIDs)
├── references/                          # Standalone reference documents
│   └── sources-for-fact-checking.md     # Source authority hierarchy
└── .vscode/
    └── mcp.json                         # MCP server configuration (reference)
```

## Agents

| Agent | Description |
|-------|-------------|
| `@content-developer` | Automates ADO work item creation, git branching, commit messages, PR creation with AB# linking, and work item closure with publish date calculation |
| `@product-manager` | Creates Feature work items from SupportabilityCheckList requirements with auto-calculated ADO fields and parent linking |
| `@technical-advisor` | Automates CSS PACE bug workflows — creates Content Bugs from PACE escalations with cross-org linking |
| `@microsoft-fact-checker` | Verifies technical accuracy against authoritative Microsoft sources with evidence-based recommendations and citations |
| `@CIA-Analysis` | Generates Customer Incidents Analysis reports identifying recurring patterns, issue categories, and documentation gaps |

## Prompts

| Prompt | Description |
|--------|-------------|
| `complete-fact-check` | Fact-check the current article against official Microsoft docs, generate a report |
| `complete-fact-checker-internal` | Fact-check using both public and internal Microsoft resources |
| `complete-freshness-review` | Full freshness review — update content, fact-check, fix links, optionally PR |
| `fact-check-and-edit` | Quick in-place fact-check with inline corrections |
| `microsoft-researcher` | Research a topic using official Microsoft documentation with full citations |
| `ado-work-item-standards` | Create or validate ADO work items per Azure Core Content Standards |

## Skills

| Skill | Description |
|-------|-------------|
| `azure-quickstart-templates` | Review, validate, or create Azure Quickstart Templates following contribution guidelines |
| `bug-reporter` | Report bugs in Content Developer tooling with structured ADO Bug creation and parent linking |
| `content-workflow` | Core workflow orchestration — work items, git branching, commit messages, PRs with AB# linking, publish dates |
| `doc-writer` | Scaffold production-ready Azure documentation (how-to, concept, quickstart, tutorial, overview) |
| `documentor-workflow` | Editorial quality workflows — SEO, engagement analysis, markdown auto-fix, link validation |
| `environment-setup` | First-time setup — Azure CLI auth, GitHub CLI auth, Git configuration, repository cloning |
| `fact-checker` | 7 specialized fact-checking workflows with tiered source authority hierarchy |
| `microsoft-doc-verifier` | Cross-product documentation verification with single article, batch, and PR review modes |
| `pr-reviewer` | Microsoft Writing Style Guide PR review with 98 style patterns across 7 categories |
| `sfi-scanner` | SFI compliance scanning — Global Admin roles, insecure auth flows, sensitive identifiers in text and images |

## MCP Servers

The `.vscode/mcp.json` file documents the MCP server ecosystem used with these customizations:

| Server | Purpose |
|--------|---------|
| `content-developer-assistant` | Workflow orchestration (migrated to `content-workflow` skill — MCP server no longer required) |
| `ado-content` | Azure DevOps work item and project management |
| `github` | GitHub repository and PR operations |
| `microsoft-docs` | Microsoft Learn documentation search and retrieval |
| `cerebro` | Personal knowledge retrieval |
| `context7` | Library documentation lookup |
| `context-mode` | Context window optimization |

## Usage by Tool

### VS Code (full support)
All features auto-discovered when this repo is your `.github` profile repo:
- **Agents**: Select from the agent dropdown (`@content-developer`, `@microsoft-fact-checker`, etc.)
- **Prompts**: Attach from the prompt picker in chat
- **Skills**: Auto-loaded by Copilot when relevant to your task
- **Instructions**: `copilot-instructions.md` always active; path-specific rules auto-applied by file type

### GitHub Copilot CLI
Agents, skills, and instructions are supported. Use agents from the agent selector.

### Claude Code / OpenCode
Point these tools at `copilot-instructions.md` for repo-wide context. Individual prompt and skill markdown files can be referenced directly in conversations. Agents and auto-discovery are not natively supported.

### GitHub.com (Coding Agent)
Agents, skills, prompts, and instructions are supported when this repo is your `.github` profile repo.

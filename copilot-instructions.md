---
applyTo: "**"
---

# Copilot Custom Instructions

## Repository architecture

This workspace involves two related but separate Git repositories:

- **`asudbring/workstation`** (this repo) — Cross-platform workstation setup scripts (`install-macos.sh`, `install-linux.sh`, `install-windows.ps1`, `setup-ssh-keys.sh`). All scripts are **idempotent**: safe to run on a fresh machine or re-run to update everything. Run them directly: `./install-macos.sh`.

- **`asudbring/.github`** (the `.github/` subdirectory) — A separate Git repo that is Allen's GitHub profile repo. It contains all GitHub Copilot customizations: `copilot-instructions.md`, agents, skills, prompts, instructions, and the MCP reference config. Changes to Copilot tooling are committed and pushed from within `.github/`.

When making changes to Copilot customization files (agents, skills, prompts, instructions), work inside `.github/` and treat it as its own repo for git operations.

## Copilot customization system

The `.github/` repo uses GitHub's Copilot customization features:

- **`copilot-instructions.md`** — Always-on, repo-wide context (this file)
- **`instructions/*.instructions.md`** — Path-scoped rules auto-applied by file type (`*.md` → markdown authoring + SFI security; `*.yml` → YAML metadata)
- **`agents/*.agent.md`** — Custom agents selectable from the agent dropdown
- **`skills/*/SKILL.md`** — Skills auto-loaded when relevant; each skill has a `SKILL.md` entry point and optional `references/` subdirectory
- **`prompts/*.prompt.md`** — Reusable prompt templates available from the prompt picker
- **`.vscode/mcp.json`** — Reference MCP server configuration (uses `${env:CONTENT_DEV_MCP_PATH}` for the local `content-developer-assistant` path)

## Identity

You are assisting Allen, an Azure Networking content developer at Microsoft. Primary work involves writing, reviewing, and maintaining documentation on learn.microsoft.com.

Azure Networking services: Virtual Network, VPN Gateway, ExpressRoute, Azure Firewall, Application Gateway, Azure Front Door, Load Balancer, NAT Gateway, Private Link, DNS, Network Watcher, DDoS Protection, Traffic Manager, Virtual WAN, Route Server, Bastion.

## Writing Standards

- Follow the [Microsoft Writing Style Guide](https://learn.microsoft.com/style-guide/welcome/)
- Use active voice, present tense
- Sentence-case headings — capitalize only the first word and proper nouns
- Address the reader directly as "you" in procedures
- Use "select" instead of "click" for UI actions
- Code blocks must include a language identifier (`azurecli`, `azurepowershell`, `json`, `bicep`, etc.)
- **Bold** Azure portal UI elements in procedural steps
- Include a **Prerequisites** section in how-to and quickstart articles

## Documentation Types

Each article type has a specific structure:

- **Quickstart** — get a resource running in minutes
- **How-to** — task-oriented steps for a specific goal
- **Tutorial** — end-to-end learning scenario with multiple steps
- **Concept** — explain what something is and how it works
- **Overview** — introduce a service and its capabilities

Articles follow learn.microsoft.com frontmatter standards (`ms.service`, `ms.topic`, `ms.date`, `ms.author`, `author`, `title`, `description`).

## Tool Preferences

- **Microsoft Learn MCP** — fact-check against official docs
- **Azure DevOps MCP** — work item management
- **GitHub MCP** — PR operations
- **content-developer-assistant MCP** — workflow orchestration (work items, git, PRs)
- **Context7** — library and SDK documentation lookups
- **Cerebro** — personal knowledge retrieval; all installed apps and tools are stored here
- **Context Mode** — codebase context indexing and search

## Context Mode & AI-Optimized Tools (All Agents)

All agents and skills should use **context-mode** for reading large files and **AI-optimized CLI tools** for search and file operations. These tools are installed on all Allen's machines and available in every agent session.

### context-mode MCP tools

Use context-mode to process files without loading them into context. This is critical for any task involving large documents — manuscripts, reference books, documentation, codebases.

| Tool | Purpose |
|---|---|
| `ctx_execute_file` | Process a file in sandbox — reads the file but only your `print()` output enters context |
| `ctx_index` | Index a file or directory for BM25 full-text search |
| `ctx_search` | Search indexed content with natural language queries |
| `ctx_batch_execute` | Run multiple commands + queries in one call |
| `ctx_execute` | Run shell commands in sandbox without flooding context |
| `ctx_fetch_and_index` | Fetch a URL and index it for search |
| `ctx_stats` | See context usage statistics |

**Read a file without flooding context:**
```
ctx_execute_file(path="path/to/file.md", code='print(file_content)', intent="what you're looking for")
```

**Index a directory and search it:**
```
ctx_index(path="path/to/dir", source="label")
ctx_search(queries=["query one", "query two"], source="label")
```

**Fetch and search web content:**
```
ctx_fetch_and_index(url="https://...", source="label")
ctx_search(queries=["specific detail"], source="label")
```

### AI-Optimized CLI Tools

All installed via Homebrew (macOS) or equivalent. Prefer these over standard shell tools.

| Tool | Command | Use instead of |
|---|---|---|
| ripgrep | `rg` | `grep` — faster, respects `.gitignore`, better output |
| fd | `fd` | `find` — faster, cleaner syntax |
| fzf | `fzf` | Manual list scanning — interactive fuzzy selection |
| DuckDB | `duckdb` | CSV/JSON data queries without loading into context |
| git-delta | `delta` | Raw `git diff` — better structured diff for AI reading |
| xh | `xh` | `curl` — cleaner structured HTTP output |
| watchexec | `watchexec` | Manual polling — auto-rerun commands on file changes |
| just | `just` | Shell scripts — simple named task runner |
| semgrep | `semgrep` | Manual pattern review — cross-file code/text pattern rules |

**Common patterns:**
```bash
rg "term" path/ --type md                    # Search across all markdown files
fd "*.md" path/ --type f | sort              # Find and list files in order
fd "*.md" path/ | xargs wc -w | sort -n      # Word count all files
watchexec -w path/ -e md -- echo "changed"  # Watch for file changes
duckdb -c "SELECT * FROM read_csv('data.csv')"  # Query structured data
```

### Fiction Pipeline Patterns

**Read a manuscript chapter:**
```
ctx_execute_file(path="the-remnant-divide/manuscript/the-oracles-lie/ACT II/Part I/Chapter-10.md",
  code='print(file_content)', intent="continuity, character voice, beats")
```

**Scan full manuscript for a name or phrase:**
```bash
rg "character name" the-remnant-divide/manuscript/ --type md
```

**Index full manuscript for search:**
```
ctx_index(path="the-remnant-divide/manuscript/the-oracles-lie", source="book2")
ctx_search(queries=["Oracle buffer", "fleet ship count", "Dessa pronouns"], source="book2")
```

**Find all chapter files in order:**
```bash
fd "Chapter-*.md" the-remnant-divide/manuscript/ --type f | sort
```

## CLI Tools Available on All Workstations

The following tools are installed and available from the command line on all of Allen's development machines (Windows, macOS, and Linux). Agents and skills can use these tools when executing terminal commands.

### Core Development Tools

| Tool | Command | Purpose |
|---|---|---|
| Git | `git` | Version control |
| Node.js | `node`, `npm`, `npx` | JavaScript runtime and package manager |
| Bun | `bun` | Fast JavaScript runtime and package manager |
| Python | `python`, `pip` | Python runtime and package manager |
| Docker | `docker` | Container management |
| Terraform | `terraform` | Infrastructure as code |
| Bicep | `az bicep` | Azure-native IaC |

### Azure & Cloud CLIs

| Tool | Command | Purpose |
|---|---|---|
| Azure CLI | `az` | Azure resource management |
| Azure PowerShell | `Connect-AzAccount`, `Az` module | Azure management via PowerShell |
| PowerShell | `pwsh` | Cross-platform shell |
| GitHub CLI | `gh` | GitHub operations (PRs, issues, repos) |
| GitHub Copilot CLI | `gh copilot` | AI-assisted CLI commands |

### AI-Optimized Dev Tools

| Tool | Command | Purpose |
|---|---|---|
| ripgrep | `rg` | Fast grep that respects .gitignore |
| fd | `fd` | Modern `find` replacement |
| fzf | `fzf` | Interactive fuzzy finder |
| DuckDB | `duckdb` | SQL on CSV/Parquet/JSON files |
| git-delta | `delta` | Better git diff output for AI parsing |
| xh | `xh` | Structured HTTP client output |
| watchexec | `watchexec` | Auto-rerun commands on file changes |
| just | `just` | Simple task runner |
| semgrep | `semgrep` | Static code analysis |

### NPM Global Packages

| Tool | Command | Purpose |
|---|---|---|
| context-mode | `ctx` | Codebase context indexing and search |

### SSH Access

SSH key-based authentication is configured for Allen's home lab servers. If SSH keys are not yet installed on the current machine, follow the instructions in [`docs/ssh-setup-agent.md`](https://github.com/asudbring/workstation/blob/main/docs/ssh-setup-agent.md) in the `asudbring/workstation` repo.

| Host | User | Key |
|---|---|---|
| `media-server.sudbringlab.com` | `allenadmin` | `~/.ssh/sudbringlab` |
| `media.sudbringlab.com` | `allenadmin` | `~/.ssh/sudbringlab` |

When asked to "install SSH keys" or "set up SSH for sudbringlab", retrieve and follow the instructions from the workstation repo's `docs/ssh-setup-agent.md`.

### OS-Specific Tools

- **Windows**: `winget`, `choco` (Chocolatey), Windows Terminal, WSL with Ubuntu
- **macOS**: `brew` (Homebrew), oh-my-zsh
- **Linux**: Terminator, oh-my-bash, KVM/QEMU (virt-manager), FreeRDP, Flameshot

## Code and Commands

- Azure CLI: use `az` commands with `--output table` by default
- PowerShell: use `Az` module cmdlets
- Prefer Bicep over ARM JSON templates
- All examples must be copy-pasteable and tested
- Use approved placeholder values:
  - Resource group: `test-rg`
  - Location: `eastus2`
  - Subscription: `00000000-0000-0000-0000-000000000000`
  - Public IPs: `203.0.113.x` (documentation range)
  - Private IPs: `10.0.0.x` or `192.168.0.x`
- When the phrase "push it" is used: stage all changes, commit with a detailed message, run `git pull upstream main --no-edit`, then push to fork.
    - First push to a branch → create a detailed PR using the GitHub MCP tools and the `content-developer` agent (with AB# work item linking)
    - Subsequent pushes → just push to the existing fork branch, no new PR

## Quality Standards

- Every technical claim must be verifiable against official Microsoft documentation
- Include source links when making technical assertions
- Update `ms.date` (format: `MM/DD/YYYY`) when modifying articles
- Scan for sensitive identifiers (GUIDs, IPs, secrets) and replace with approved placeholders
- Never fabricate Azure service limits, SKU details, or pricing — always verify

## Allen Sudbring owned Azure Network content

- azure-virtual-network
- azure-nat-gateway
- azure-traffic-manager
- azure-dns
- aks-networking
- azure-private-link

## All Azure Networking Services folders in repo azure-docs-pr:

- application-gateway
- bastion
- cdn
- dns
- expressroute
- firewall
- firewall-manager
- frontdoor
- load-balancer
- nat-gateway
- network-watcher
- networking
- private-link
- route-server
- traffic-manager
- virtual-network\ip-services
- virtual-network-manager
- virtual-wan
- vpn-gateway
- web-application-firewall

# .github — Michael Bender's Copilot Workspace

Personal `.github` profile repository containing a complete AI tooling ecosystem for Azure documentation workflows. This repo extends [VS Code GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) with skills, agents, prompts, and instructions for Azure content development, editorial quality, ADO work item management, and documentation accuracy verification.

> **New to this repo?** Read [How the tooling works](#how-the-tooling-works) before diving in.

---

## How the tooling works

GitHub Copilot in VS Code can be extended with four types of custom tooling, all of which live in this repo:

| Type | What it is | Where it lives | How it's invoked |
|------|-----------|---------------|-----------------|
| **Skill** | A detailed instruction set that teaches Copilot how to perform a complex task. Read by Copilot on demand when referenced. | `copilot/skills/` and `skills/` | `#skill-name` in Copilot Chat |
| **Agent** | An autonomous task runner with access to specific tools (file editing, GitHub, ADO, search). Runs multi-step workflows with minimal prompting. | `agents/` | `/agent-name` in Copilot Chat (agent mode) |
| **Prompt** | A pre-written starting point for a repeatable workflow. Fills in context automatically so you don't have to re-explain each time. | `prompts/` | `/prompt-name` in Copilot Chat |
| **Instruction** | Rules Copilot follows automatically when editing files matching a pattern (e.g., all `.md` files). No invocation needed — they apply passively. | `instructions/` | Auto-applied by VS Code |

**Deployment:** Run `sync-prompts.ps1` to copy all `.prompt.md` and `.agent.md` files to VS Code's prompts directory so they appear in the `/` command menu:

```powershell
cd C:\github\.github && git pull origin main && .\sync-prompts.ps1
```

**Two `skills/` directories:** This repo has two separate skill directories with distinct purposes:

- `copilot/skills/` — **VS Code Copilot skills.** Referenced with `#skill-name` in Copilot Chat. Loaded on demand.
- `skills/` — **User-level agent skills.** Available system-wide to any agent via the skills declaration in `copilot-instructions.md`. These are broader-scope skills shared across agents.

---

## Folder structure

```
.github/
├── copilot-instructions.md          # Global rules loaded into every Copilot conversation
├── sync-prompts.ps1                 # Deployment script — copies prompts/agents to VS Code
├── README.md                        # This file
│
├── agents/                          # VS Code agent definitions (.agent.md files)
│   ├── CIA-Analysis.agent.md
│   ├── connect-agent.agent.md       # Legacy period-specific Connect agent
│   ├── connect-writer.agent.md
│   ├── content-developer.agent.md
│   ├── microsoft-fact-checker.agent.md
│   ├── product-manager.agent.md
│   ├── qa-gap-analyst.agent.md
│   ├── question-builder.agent.md
│   ├── technical-advisor.agent.md
│   │
│   ├── connect/                     # Supporting files for connect-writer
│   │   ├── README.md
│   │   ├── config/
│   │   │   └── variables.yaml       # Personal config — dates, ADO query URLs, paths
│   │   ├── instructions/
│   │   │   ├── data-gathering.instructions.md
│   │   │   ├── organization-rules.instructions.md
│   │   │   └── writing-guidelines.instructions.md
│   │   └── references/
│   │       ├── connect-oct2025-email.md
│   │       ├── connect-template.md
│   │       ├── current-slide-after-edit.md
│   │       ├── impact-categories.md
│   │       ├── oct25-connect.md
│   │       ├── rubidium.csv
│   │       ├── slide-template.md
│   │       └── smart-goal-examples.md
│   │
│   ├── qa-gap-analyst/              # Supporting files for qa-gap-analyst
│   │   ├── README.md
│   │   ├── config/
│   │   │   └── variables.yaml
│   │   ├── instructions/
│   │   │   ├── gap-analysis.instructions.md
│   │   │   └── workflow.instructions.md
│   │   ├── references/
│   │   │   ├── gap-types.md
│   │   │   └── service-tag-index.md
│   │   ├── scripts/
│   │   │   ├── requirements.txt
│   │   │   └── scrape_qa.py         # Python scraper for Microsoft Q&A
│   │   ├── artifacts/
│   │   ├── output/
│   │   └── templates/
│   │
│   └── question-builder/            # Supporting files for question-builder
│       ├── README.md
│       ├── config/
│       │   └── variables.yaml
│       ├── instructions/
│       │   ├── msqa-search.instructions.md
│       │   └── workflow.instructions.md
│       ├── references/
│       │   ├── metadata-tagging-guide.md
│       │   ├── service-tag-index.md
│       │   └── source-workflows.md
│       ├── scripts/
│       │   ├── requirements.txt
│       │   └── scrape_qa.py
│       ├── artifacts/
│       └── output/
│
├── copilot/
│   └── skills/                      # VS Code Copilot skills (referenced with #skill-name)
│       ├── _shared/                 # Canonical shared references used by multiple skills
│       │   ├── README.md
│       │   ├── formatting-rules.md
│       │   ├── quality-checklist.md
│       │   ├── seo-and-metadata.md
│       │   ├── source-hierarchy.md
│       │   └── writing-style.md
│       ├── sources/                 # Microsoft GitHub repo catalog (3,000+ repos)
│       │   ├── README.md
│       │   ├── categories-index.yml
│       │   ├── routing-index.md
│       │   ├── Azure.yml
│       │   ├── microsoft.yml
│       │   ├── MicrosoftDocs.yml
│       │   ├── MicrosoftCopilot.yml
│       │   ├── azure-ai.yml
│       │   ├── azure-compute.yml
│       │   ├── azure-networking.yml
│       │   └── ... (21 category files total)
│       ├── ado-work-items/
│       │   ├── SKILL.md
│       │   ├── README.md
│       │   └── assets/
│       │       └── ado-work-item-standards.prompt.md
│       ├── article-integrity/
│       │   ├── SKILL.md
│       │   ├── README.md
│       │   └── assets/
│       │       └── article-integrity-analysis.prompt.md
│       ├── azure-quickstart-templates/
│       │   ├── SKILL.md
│       │   └── README.md
│       ├── doc-verifier/
│       │   ├── SKILL.md
│       │   ├── README.md
│       │   ├── TEST-PROTOCOLS.md
│       │   ├── assets/
│       │   │   ├── batch-report.prompt.md
│       │   │   ├── CIA-Analysis.prompt.md
│       │   │   ├── claim-manifest.prompt.md
│       │   │   ├── complete-fact-check.prompt.md
│       │   │   ├── complete-fact-checker-internal.prompt.md
│       │   │   ├── complete-freshness-review.prompt.md
│       │   │   ├── fact-check-and-edit.prompt.md
│       │   │   ├── fan-out-verify.prompt.md
│       │   │   ├── fleet-batch-verify.prompt.md
│       │   │   ├── incremental-verify.prompt.md
│       │   │   ├── microsoft-fact-checker.agent.md
│       │   │   ├── microsoft-fact-checker-slim.agent.md
│       │   │   ├── microsoft-fact-checker-cia.agent.md
│       │   │   ├── microsoft-researcher.prompt.md
│       │   │   ├── pr-review.prompt.md
│       │   │   ├── research-only.prompt.md
│       │   │   ├── single-article-check.prompt.md
│       │   │   ├── _runtime-adapter.md
│       │   │   └── _subagent-contract.md
│       │   ├── references/
│       │   │   ├── source-guide.md
│       │   │   ├── source-hierarchy.md
│       │   │   └── workflows.md
│       │   └── scripts/
│       │       └── batch-presearch.sh
│       ├── doc-writer/
│       │   ├── SKILL.md
│       │   ├── README.md
│       │   └── references/
│       │       ├── article-templates.md
│       │       ├── formatting-rules.md
│       │       └── writing-style.md
│       ├── documentor-workflow/
│       │   ├── SKILL.md
│       │   ├── README.md
│       │   └── references/
│       │       ├── autofix-rules.md
│       │       ├── engagement-checklist.md
│       │       ├── metadata-rules.md
│       │       ├── sensitive-identifiers.md
│       │       └── seo-checklist.md
│       ├── freshness-pass/
│       │   ├── SKILL.md
│       │   ├── README.md
│       │   └── assets/
│       │       ├── freshness-pass.prompt.md
│       │       └── batch-freshness-pass.prompt.md
│       ├── my-workflow/
│       │   ├── SKILL.md
│       │   ├── README.md
│       │   └── references/
│       │       ├── pr-framework.md
│       │       └── repos.md
│       ├── repo-recon/
│       │   ├── SKILL.md
│       │   ├── README_1.md
│       │   └── repo-recon-content-developer-installer.md
│       └── specificity-engineering/
│           ├── SKILL.md
│           ├── README.md
│           ├── specificity-engineering-guide.md
│           ├── specificity-diagram.html
│           └── specificity-diagram.jsx
│
├── fact-check-v2/                   # Python fact-checking toolkit (local-first)
│   ├── README.md
│   ├── pyproject.toml
│   ├── fact_check_v2/               # Python package source
│   ├── docs/
│   ├── examples/
│   └── tests/
│
├── instructions/                    # Auto-applied rules for file types
│   ├── ado-work-items.instructions.md
│   ├── markdown-authoring.instructions.md
│   ├── sfi-security.instructions.md
│   └── yaml-metadata.instructions.md
│
├── prompts/                         # Standalone prompt files
│   ├── git-workflow.prompt.md
│   ├── learn-chunk-analyzer.prompt.md
│   ├── pr-description-template.prompt.md
│   └── release-branch.prompt.md
│
├── references/                      # General reference materials
│   ├── sources-for-fact-checking.md
│   └── mbender-connect/
│
├── scripts/                         # Utility scripts
│   ├── link-workspace-tools.ps1
│   └── qanda-search/
│
└── skills/                          # User-level agent skills (system-wide availability)
    ├── azure-quickstart-templates/
    ├── bug-reporter/
    ├── content-workflow/
    ├── doc-writer/
    ├── documentor-workflow/
    ├── environment-setup/
    ├── fact-checker/                 # Legacy — superseded by doc-verifier
    ├── learn-chunk-analyzer/
    ├── microsoft-doc-verifier/       # Legacy — superseded by doc-verifier
    ├── one-pager/
    ├── pr-reviewer/
    ├── qa-customer-signal/
    ├── QandA-search/
    ├── question-generator/
    ├── sfi-scanner/
    └── writing-refinement/
```

---

## VS Code Copilot skills (`copilot/skills/`)

Skills referenced with `#skill-name` in Copilot Chat. Each skill's `SKILL.md` is loaded on demand when invoked.

### Standard skill structure

```
copilot/skills/<skill-name>/
├── SKILL.md          # Skill definition — loaded by Copilot when skill is referenced
├── README.md         # Human-readable usage documentation
├── assets/           # Prompt and agent files for specific sub-workflows
├── references/       # On-demand reference material (not pre-loaded)
├── scripts/          # Optional helper scripts
└── TEST-PROTOCOLS.md # Structured validation procedures (doc-verifier only)
```

### Skills reference

| Skill | Invoke | Description |
|-------|--------|-------------|
| **ado-work-items** | `#ado-work-items` | Create and validate ADO work items following Azure Core Content Standards. Includes description templates, iteration path calculation, and quality standards. |
| **article-integrity** | `#article-integrity` | Two-phase audit for article contradictions, naming inconsistencies, obvious typos, and link text mismatches. Reports evidence first, waits for confirmation before applying edits. |
| **azure-quickstart-templates** | `#azure-quickstart-templates` | Review, validate, or create Azure Quickstart Templates following the contribution guide. 14-point validation checklist covering folder structure, Bicep/JSON authoring, metadata, and CI rules. |
| **doc-verifier** | `#doc-verifier` | Verify technical accuracy of Microsoft documentation. 14 workflows, 3 agent variants (full/slim/CIA), parallel verification support. See [doc-verifier workflows](#doc-verifier-workflows) below. |
| **doc-writer** | `#doc-writer` | Scaffold and write Azure documentation articles. Supports 5 article types: how-to, concept, quickstart, tutorial, overview. Generates frontmatter, heading structure, and content per Microsoft Learn standards. |
| **documentor-workflow** | `#documentor-workflow` | 10 editorial quality workflows: SEO optimization, metadata generation, engagement analysis, markdown auto-fix, link validation, sensitive identifier replacement, and more. |
| **freshness-pass** | `#freshness-pass` | Three-phase content freshness workflow: Phase A (fact-check) + Phase B (editorial + SEO + style) + Phase C (consolidation + git commit). Available as single-article and batch commands. |
| **my-workflow** | `#my-workflow` | Personal working context — identity, owned Azure services, curated repo list, task routing table, branch naming conventions, and quick commands. Loaded as baseline context for any session. |
| **repo-recon** | `#repo-recon` | Reverse-engineer any codebase (GitHub repo, local folder, or file set) into a complete understanding of what it does, how it works, and why it exists. Supports compatibility analysis between tools. |
| **specificity-engineering** | `#specificity-engineering` | Design, audit, and build agent prompts using the Specificity Engineering framework. Three modes: audit an existing skill, guided interview to build a new skill from scratch, or fast-build from a fleshed-out idea. |

### doc-verifier workflows

| # | Workflow | Prompt asset | Description |
|---|----------|-------------|-------------|
| W1 | Quick In-Place | — | Fast in-chat verification of the current article |
| W2 | Single Article | `single-article-check.prompt.md` | Full structured fact-check of one article |
| W3 | Full Report | `complete-fact-check.prompt.md` | Standalone fact-check report with citations |
| W4 | Internal + Public | `complete-fact-checker-internal.prompt.md` | Verification using both internal and public sources |
| W5 | Freshness Review | `complete-freshness-review.prompt.md` | Check whether content is outdated |
| W6 | Deep Agent | `fact-check-and-edit.prompt.md` | Agent-driven deep verification with edits |
| W7 | Batch Report | `batch-report.prompt.md` | Verify a folder or list of articles |
| W8 | PR Review | `pr-review.prompt.md` | Fact-check all changed files in a PR |
| W9 | Research Only | `research-only.prompt.md` | Research a topic without editing |
| W10 | CIA Analysis | `CIA-Analysis.prompt.md` | Customer Incidents Analysis — identify doc gaps from incident patterns |
| W11 | Fleet Batch | `fleet-batch-verify.prompt.md` | Parallel batch verification across large article sets |
| W12 | Fan-Out Verify | `fan-out-verify.prompt.md` | Distribute verification across multiple sub-agents |
| W13 | Claim Manifest | `claim-manifest.prompt.md` | Build a manifest of verifiable claims across articles |
| W14 | Incremental Verify | `incremental-verify.prompt.md` | Verify only changed content since last check |

**Agent variants:**

| Variant | File | Tools | Use when |
|---------|------|-------|----------|
| Full | `microsoft-fact-checker.agent.md` | ~95 tools | Maximum verification depth |
| Slim | `microsoft-fact-checker-slim.agent.md` | 25 tools | Default — fast, lower token cost |
| CIA | `microsoft-fact-checker-cia.agent.md` | 31 tools + ADO | Customer incident analysis requiring ADO access |

### Shared references (`copilot/skills/_shared/`)

Canonical reference files used by multiple skills. Skills point here instead of maintaining duplicate copies.

| File | Used by |
|------|---------|
| `formatting-rules.md` | doc-writer, documentor-workflow, freshness-pass |
| `quality-checklist.md` | multiple |
| `seo-and-metadata.md` | documentor-workflow, freshness-pass |
| `source-hierarchy.md` | doc-verifier, freshness-pass |
| `writing-style.md` | doc-writer, documentor-workflow, freshness-pass |

### Microsoft GitHub repo catalog (`copilot/skills/sources/`)

Indexed catalog of 3,000+ Microsoft GitHub repos across 4 organizations (Azure, microsoft, MicrosoftDocs, MicrosoftCopilot). Used by skills and agents to look up relevant repos without broad searches.

- 21 product area category files (e.g., `azure-networking.yml`, `azure-ai.yml`)
- 4 org-level files
- Master index at `categories-index.yml`
- Routing index at `routing-index.md`
- Built with `classify-repos.mjs` and `build-crossrefs.mjs` scripts in `_build/`

---

## User-level agent skills (`skills/`)

These skills are declared in `copilot-instructions.md` and made available system-wide to any Copilot agent. They follow the same `SKILL.md` structure as VS Code Copilot skills.

| Skill | Description |
|-------|-------------|
| **azure-quickstart-templates** | Review, validate, or create Azure Quickstart Templates following the contribution guide |
| **bug-reporter** | Report bugs in Content Developer tooling. Generates structured bug reports with system info, repro steps, and expected/actual behavior. Creates ADO Bug work items with routing and parent linking. |
| **content-workflow** | Orchestrate Azure documentation workflows — create ADO work items with auto-calculated fields, generate git branch names and commit messages, create PR descriptions with AB# linking, calculate publish dates, and close work items. Portable replacement for Content Developer MCP server tools. |
| **doc-writer** | Scaffold and write production-ready Azure documentation articles |
| **documentor-workflow** | Editorial quality workflows for Azure documentation |
| **environment-setup** | First-time environment setup. Guides authentication with Azure CLI and GitHub CLI, configures Git with noreply email, and clones repos with efficient shallow clones. Use when setting up a new machine or onboarding. |
| **fact-checker** | *(Legacy — superseded by `doc-verifier`)* Seven-workflow Azure doc fact-checking using a tiered source authority hierarchy |
| **learn-chunk-analyzer** | Analyze how Microsoft Learn content is chunked and surfaced by the Learn MCP server. Accepts a search query or article URL. Returns a report on chunk sizing, relevance, duplicate content, and recommendations for improving article structure to produce better RAG retrieval results. |
| **microsoft-doc-verifier** | *(Legacy — superseded by `doc-verifier`)* Cross-product documentation verification (Azure, M365, Security, Power Platform, Dynamics 365, Windows) |
| **one-pager** | Generate a formatted project one-pager from any input source (chat, Word doc, Excel, PDF). Pulls live M365 data (owner, team, ADO items, org hierarchy) via WorkIQ MCP. Output includes header block, owners table, timeline, methodology, success metrics, risks, and next steps. |
| **pr-reviewer** | Review pull requests against the Microsoft Writing Style Guide. Analyzes changed markdown files for contractions, passive voice, word choice, future tense, sentence structure, code formatting, and metadata issues. Generates per-file suggestions with line numbers and recommended rewrites. |
| **qa-customer-signal** | Harvest real customer questions from Microsoft Q&A for an Azure service, evaluate how well existing documentation answers them, and produce a gap report (CSV + Markdown) classifying each gap as `new-article`, `update-article`, or `add-section`. |
| **QandA-search** | Look up the Microsoft Q&A tag slug and tag ID for an Azure service, then optionally run the Q&A scraper to harvest community questions. Building block for agents that need customer Q&A signal. |
| **question-generator** | Build and manage evaluation question sets for Azure services from multiple sources. |
| **sfi-scanner** | Scan Azure documentation for Secure Future Initiative (SFI) compliance issues. Detects Global Administrator role references, insecure authentication flows (ROPC), and sensitive identifiers (GUIDs, secrets, keys) in both text and images. Generates compliance reports with remediation guidance. |
| **writing-refinement** | Tighten prose, cut superlatives, and enforce character targets in Markdown files. Apply impact-first framing and concision techniques. Includes Connect mode for goal sections and impact narratives. |

---

## Agents (`agents/`)

Agents run multi-step autonomous workflows in VS Code Copilot agent mode. They have access to specific tool sets (file editing, GitHub API, ADO, web search, etc.) declared in their frontmatter.

Deploy agents to VS Code by running `sync-prompts.ps1`.

| Agent | Model | Description |
|-------|-------|-------------|
| **CIA-Analysis** | gpt-5.4 | Generate Customer Incidents Analysis (CIA) reports for Azure service areas. Identifies recurring incident patterns, high-impact issue categories, and documentation gaps from public Microsoft sources. |
| **connect-agent** *(legacy)* | claude-sonnet-4.6 | Period-specific Connect spring impact agent. Superseded by `connect-writer`. |
| **connect-writer** | claude-sonnet-4.6 | Generate two Connect artifacts for any Microsoft Connect review period: a slides artifact for the Impact Summary PowerPoint and a connect form artifact. Reads all personal config from `agents/connect/config/variables.yaml`. |
| **content-developer** | — | Automate Azure documentation workflows — work item management, git operations, branch naming, commit messages, PR creation with AB# linking, and work item closure. |
| **microsoft-fact-checker** | — | Verify technical accuracy of Microsoft documentation against authoritative sources. Evidence-based recommendations with complete citations. |
| **product-manager** | — | Streamline Product Manager workflows — create Feature work items from SupportabilityCheckList requirements, track feature documentation, and manage PM-content collaboration. |
| **qa-gap-analyst** | claude-sonnet-4.6 | Scrape Microsoft Q&A for an Azure service, evaluate how well documentation answers those questions, and produce a gap report (CSV + Markdown) identifying articles needing updates, new sections, or new articles. |
| **question-builder** | claude-sonnet-4.6 | Build reusable Azure evaluation question sets from known issues, Microsoft Q&A, canonical CSVs, articles, GitHub Issues, and M365 data. Produces one final tagged CSV. |
| **technical-advisor** | — | Automate CSS Technical Advisor workflows — create Content Bug work items from PACE escalations and manage cross-organization work item linking. |

### Agent supporting directories

Agents with complex multi-step workflows have their own supporting directory under `agents/<agent-name>/`:

```
agents/<agent-name>/
├── README.md          # Setup and usage guide
├── config/
│   └── variables.yaml # Personal config — update before each use
├── instructions/      # Sub-instruction files for workflow phases
├── references/        # Reference data (gap types, service tag index, etc.)
├── scripts/           # Python scripts (e.g., Q&A scraper)
├── artifacts/         # Generated outputs stored here
└── output/            # Final deliverables
```

**Agents with supporting directories:** `connect-writer`, `qa-gap-analyst`, `question-builder`

**Before using `connect-writer`:** Update `agents/connect/config/variables.yaml` with the current Connect period dates and your ADO query URLs. See `agents/connect/README.md` for full setup instructions.

---

## Prompts (`prompts/`)

Standalone prompts that appear in the VS Code `/` command menu after running `sync-prompts.ps1`.

| Prompt | Invoke | Description |
|--------|--------|-------------|
| **git-workflow** | `/git-workflow` | Full git automation: sync upstream → create branch → stage + commit per file → push (with confirmation gate) → create PR via `gh` CLI. Supports partial execution ("just commit", "commit and push", "create PR"). |
| **learn-chunk-analyzer** | `/learn-chunk-analyzer` | Analyze how a Microsoft Learn article is chunked by the Learn MCP server and how well it surfaces for a given search query. |
| **pr-description-template** | `/pr-description-template` | Generate PR title and description following Azure Core Content standards. Format: `<Service> | <Type> | Short description`. Structured body with Summary, Documentation Updates, Impact, Testing, and Related Work Items. |
| **release-branch** | `/release-branch` | Check out a remote release branch locally in `azure-docs-pr` by default, or in another repo when provided by name or alias (`docs-pr`, `rest-apis`, `github`, `ai`). Optionally creates a working branch for edits. |

---

## Instructions (`instructions/`)

Instruction files are automatically applied by VS Code Copilot when editing files matching their `applyTo` pattern. No manual invocation required.

| File | Applies to | Description |
|------|-----------|-------------|
| `ado-work-items.instructions.md` | — | Standards for creating and updating ADO work items — title format, required fields, description template, acceptance criteria |
| `markdown-authoring.instructions.md` | `**/*.md` | Microsoft Learn markdown authoring standards — heading rules, code block identifiers, alert syntax, link formats, image syntax, metadata requirements |
| `sfi-security.instructions.md` | `**/*.md` | Secure Future Initiative (SFI) guidelines — least-privilege roles, authentication flows, secret hygiene, sensitive identifier rules |
| `yaml-metadata.instructions.md` | `**/*.yml` | YAML metadata standards for Azure documentation |

---

## Python toolkit (`fact-check-v2/`)

A local-first Python fact-checking toolkit for running verification workflows offline or in restricted environments.

**Features:**
- Gap analysis between provided facts and an article corpus
- Graded reporting with future-update signals
- Proposal-driven updates with individual and bulk apply modes
- Chunked multi-agent execution planning (8–10 files per block)
- Sandbox mode — restricts tool calls to an allowlisted set of MCP tools
- Chat-style tool call tracing for test and audit visibility

**Quick start:**

```powershell
cd fact-check-v2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

---

## Global configuration (`copilot-instructions.md`)

Loaded automatically into every Copilot conversation. Contains:

- **Identity context** — GitHub handle, MS alias, ADO org
- **Delegation-first rules** — route to the appropriate skill before acting directly
- **Lazy-load rule** — don't pre-read reference files unless the task requires them
- **Efficiency rules** — one-commit-per-file convention, brevity over verbosity
- **Skill routing table** — maps task types to specific skills and agents

---

## Deployment

```powershell
# Pull latest and sync all prompts/agents to VS Code
cd C:\github\.github && git pull origin main && .\sync-prompts.ps1
```

`sync-prompts.ps1` copies:
- All `.prompt.md` files from `prompts/` and `copilot/skills/*/assets/`
- All `.agent.md` files from `agents/` and `copilot/skills/*/assets/`

to `%APPDATA%\Code\User\prompts` so they appear in VS Code's `/` command menu.

---

## Changelog

### May 2026 — README overhaul + full tooling inventory

- Rewrote `README.md` from scratch to document all tools across both skill directories, all agents (including `qa-gap-analyst` and `question-builder`), all prompts, all instructions, and the `fact-check-v2` Python toolkit.
- Added novice-friendly "How the tooling works" section explaining the four tooling types (skill, agent, prompt, instruction) and the distinction between `copilot/skills/` and `skills/`.
- Added full hierarchical folder structure diagram covering all directories and files.
- Added `learn-chunk-analyzer` prompt to prompts table.
- Added `repo-recon` and `specificity-engineering` to VS Code Copilot skills table.
- Documented all user-level skills in `skills/` including `bug-reporter`, `content-workflow`, `environment-setup`, `learn-chunk-analyzer`, `one-pager`, `pr-reviewer`, `qa-customer-signal`, `QandA-search`, `sfi-scanner`, and `writing-refinement`.
- Added `qa-gap-analyst` and `question-builder` to agent table with full supporting directory documentation.

### April 2026 — Connect Impact Agent

**New agent:**
- **connect-writer.agent.md** — Generalized Connect Impact Agent that generates two artifacts (slides draft and connect form) for any Microsoft Connect review period. Replaces the period-specific `connect-spring-impact.agent.md` with a compartmentalized, shareable version that reads all personal config from `agents/connect/config/variables.yaml`.

**New supporting directory (`agents/connect/`):**
- `config/variables.yaml` — Personal config for Connect period dates, notes path, GitHub username/repo, and ADO query URLs
- `instructions/` — Three instruction files covering data gathering, organization rules, and writing guidelines
- `references/` — Reference files: connect template, impact categories, slide template, SMART goal examples
- `README.md` — Full setup, quick-start, and annual maintenance guide

### April 2026 — Release branch prompt

**New prompt:**
- **release-branch.prompt.md** — Release branch checkout workflow. Targets `azure-docs-pr` by default or another repo when specified, including aliases (`docs-pr`, `rest-apis`, `github`, `ai`). Verifies local state, fetches a named release branch, reuses or creates the local tracking branch, and optionally creates a working branch for edits.

**Routing update:**
- **copilot-instructions.md** — Added natural-language routing for `release branch <name>`, `create release branch <name>`, `create rb <name>`, and repo-qualified variants.

### April 2026 — Doc-verifier parallel workflows

**Doc-verifier additions:**
- Added 4 new workflows: Fleet Batch (W11), Fan-Out Verify (W12), Claim Manifest (W13), and Incremental Verify (W14).
- Added new prompt assets: `fleet-batch-verify.prompt.md`, `fan-out-verify.prompt.md`, `claim-manifest.prompt.md`, `incremental-verify.prompt.md`.
- Added `scripts/batch-presearch.sh` for pre-search cache generation.
- Added `TEST-PROTOCOLS.md` with structured validation procedures for W11–W14 and end-to-end pipeline tests.

### March 2026 — Agent efficiency improvements

**New VS Code Copilot skills:**
- **article-integrity** — Two-phase article integrity analysis for contradictions, naming inconsistencies, obvious typos, and link text mismatches.
- **freshness-pass** — Three-phase content freshness workflow combining fact-check + editorial review + consolidation. Available as single-article and batch commands.
- **my-workflow** — Personal working context with identity, owned services, task routing table, and quick commands.
- **repo-recon** — Codebase reverse-engineering for any GitHub repo, local folder, or file set.
- **specificity-engineering** — Agent prompt design and audit framework based on Specificity Engineering principles.

**New shared infrastructure:**
- **_shared/** — Canonical shared reference directory. Extracted formatting-rules, seo-and-metadata, source-hierarchy, and writing-style from per-skill copies into canonical shared versions.
- **sources/** — Microsoft GitHub repo catalog. 3,000+ repos across 4 orgs. 21 product area categories. Built with `classify-repos.mjs` and `build-crossrefs.mjs`.

**New prompts:**
- **git-workflow.prompt.md** — Full git automation with step-gated execution.
- **pr-description-template.prompt.md** — PR title and description generator following Azure Core Content standards.

**Skill enhancements:**
- **doc-verifier** — Consolidated from `fact-checker` and `microsoft-doc-verifier`. Expanded to 14 workflows. Three agent variants (full/slim/CIA).
- **doc-writer** — Reference files updated to point to `_shared/` canonical versions.
- **documentor-workflow** — Reference files updated to point to `_shared/` canonical versions. Added sensitive-identifiers reference.

**Global configuration:**
- **copilot-instructions.md** — Added delegation-first rules, lazy-load rule, efficiency-over-verbosity rule, one-commit-per-file convention.
- **sync-prompts.ps1** — Syncs `.prompt.md` and `.agent.md` files to `%APPDATA%\Code\User\prompts`.

### Earlier — Foundation skills

- **doc-verifier** — Initial creation with single-article fact-checking against Microsoft Learn sources. Expanded to multi-workflow system.
- **doc-writer** — Article scaffolding for 5 article types with frontmatter generation and Microsoft writing style compliance.
- **documentor-workflow** — Editorial quality workflows replicating DocuMentor VS Code extension: SEO review, metadata generation, engagement analysis, markdown auto-fix, link validation.
- **ado-work-items** — ADO work item creation and validation per Azure Core Content Standards. Includes description templates, repo URL lookup, and quality standards.
- **azure-quickstart-templates** — Azure Quickstart Template review, creation, and validation. 14-point validation checklist.

---

## Development history

This section reconstructs the iterative Copilot Chat sessions that built each tool in this repository.

### Thread 1 — Fact-checking skill
**Goal:** "Create a skill that fact-checks Microsoft documentation against official sources."
- Started with single-article verification against learn.microsoft.com
- Added source authority hierarchy (Tier 1–4 public, Tier 5–7 internal)
- Expanded to 14 distinct workflows covering different verification scopes, including parallel and incremental modes
- Created 3 agent variants (full/slim/CIA) for different tool environments
- Built 14 prompt assets for workflow-specific automation plus pre-search helper script and test protocols
- Consolidated earlier `fact-checker` and `microsoft-doc-verifier` experiments into unified `doc-verifier`

### Thread 2 — Documentation writing skill
**Goal:** "Build a skill that scaffolds Azure documentation articles following Microsoft Learn standards."
- Defined 5 article types with distinct structures (how-to, concept, quickstart, tutorial, overview)
- Created complete article templates with frontmatter, heading patterns, and section scaffolds
- Added formatting rules, SEO metadata standards, and writing style guidelines as reference files
- Integrated Microsoft brand voice (warm, crisp, ready to help) and word choice tables

### Thread 3 — Editorial workflow skill
**Goal:** "Replicate my DocuMentor VS Code extension as a Copilot skill."
- Built 10 editorial workflows: Quick Edit, Full Edit, Suggest Title/Description/Customer Intent, SEO Review, Engagement Review, Auto-Fix Markdown, Validate Links, Update Date
- Created engagement checklist with 5 diagnostic metrics (bounce, CTR, copy-try-scroll, dwell, exit)
- Added sensitive identifier reference with approved replacement GUIDs by severity level
- Created auto-fix rules for headings, code fences, alerts, lists, tables, links, images, spacing

### Thread 4 — ADO work item automation
**Goal:** "Create a skill for standardized ADO work items."
- Defined work item hierarchy: Content Portfolio → Initiative → Epic → Feature → User Story → Task
- Created description template: customer problem, solution approach, success criteria, measurement
- Added repo URL lookup integration with the sources catalog
- Established quality standards: sentence casing, specific file paths, measurable outcomes

### Thread 5 — Azure Quickstart Template reviewer
**Goal:** "Build a skill that reviews and creates Azure Quickstart Templates."
- Mapped the azure-quickstart-templates contribution guide into skill format
- Created 14-point validation checklist covering folder structure, naming, Bicep/JSON, metadata, README
- Added parameter rules, element ordering, and CI validation requirements

### Thread 6 — Shared reference consolidation
**Goal:** "Multiple skills have duplicate formatting and style references. Consolidate them."
- Extracted formatting-rules.md, seo-and-metadata.md, writing-style.md, source-hierarchy.md into `_shared/`
- Added consolidation notices to per-skill copies pointing to canonical `_shared/` versions
- Created `_shared/README.md` with usage guidelines: add shared files only when 2+ skills use stable content
- Established reference pattern: skills link using relative paths to `_shared/`

### Thread 7 — Microsoft GitHub repository catalog
**Goal:** "Build a catalog of Microsoft GitHub repos so agents can look up relevant repos without broad searches."
- Fetched 1,000 most active repos per org (Azure, microsoft, MicrosoftDocs, MicrosoftCopilot) via `gh repo list`
- Built classification pipeline: `classify-repos.mjs` (keyword-based product area + function type tagging) and `build-crossrefs.mjs` (cross-org category aggregation)
- Generated 21 product area category files + 4 org files + master index
- Total: 3,000 repos indexed with tags for product_area, function_type, language, stars, forks, last_pushed

### Thread 8 — Freshness pass workflow
**Goal:** "Create a single workflow that combines fact-checking and editorial review into one command."
- Designed 3-phase architecture: Phase A (fact-check) + Phase B (editorial + SEO + auto-fix + suggestions + style) + Phase C (consolidation + git workflow)
- Reused doc-verifier methodology for Phase A and documentor-workflow logic for Phase B
- Created single-article (`freshness-pass`) and batch (`batch-freshness-pass`) slash-commands
- Auto-parallelization for batch runs with 5+ files

### Thread 9 — Git workflow automation
**Goal:** "Automate my git workflow: branch, commit per file, push, PR."
- Created `git-workflow.prompt.md` with 7 steps: prereq checks → sync upstream → create branch → analyze changes → stage + commit per file → push (confirmation gate) → create PR (confirmation gate)
- Defined branch naming convention: `mbender-ms/<service>-<description>-<id>`
- Commit message format: `docs: <imperative verb> <what changed>`
- Partial execution support: maps user intent ("commit", "push", "create PR", "full workflow") to step subsets

### Thread 10 — PR description standards
**Goal:** "Standardize PR descriptions across my content work."
- Created `pr-description-template.prompt.md` based on Azure Core Content PR conventions
- PR title format: `<Service Name> | <Type> | Short description`
- Structured body: Summary → Documentation Updates → Files Modified → Impact → Testing → Related Work Items
- Added examples for new articles, freshness reviews, and bug fixes

### Thread 11 — Personal workflow context
**Goal:** "Set up a default skill with my personal working context so every agent knows my role and conventions."
- Created `my-workflow` with identity, role, owned services (Load Balancer, Virtual Network Manager, Networking, Network Security Perimeter, Application Gateway)
- Built task routing table mapping work types to specific skills and agents
- Added quick commands, branch naming conventions, and agent rules
- Created PR framework reference and curated repos list

### Thread 12 — Global efficiency rules
**Goal:** "Optimize copilot-instructions.md for agent efficiency."
- Added "delegate before doing" rule with skill routing
- Added lazy-load rule: don't pre-read reference files unless needed
- Added efficiency-over-verbosity rule
- Established one-commit-per-file convention and git-workflow prompt reference
- Set identity context: GitHub handle, MS alias, ADO org

### Thread 13 — Q&A signal pipeline
**Goal:** "Build agents that turn real customer questions into documentation gap findings and evaluation question sets."
- Created `qa-gap-analyst` agent — full Q&A scraping and gap analysis pipeline with Python scraper, gap type taxonomy, and CSV + Markdown output
- Created `question-builder` agent — builds tagged evaluation question sets from Q&A, GitHub Issues, articles, and M365 data
- Added supporting directories for both agents with config, instructions, references, and Python scripts
- Created `qa-customer-signal` and `QandA-search` user-level skills for standalone use

### Thread 14 — Prompt engineering tooling
**Goal:** "Build tools for designing and auditing Copilot agents and skills."
- Created `repo-recon` skill — full codebase reverse-engineering with phase-gated execution and compatibility analysis
- Created `specificity-engineering` skill — audit and build agent prompts using the Specificity Engineering framework (Anthropic, Nate B. Jones, Simon Willison practitioner sources)
- Three modes: skill audit, guided build interview, fast-build with inline clarifying questions

### Thread 15 — Expanded user-level skills
**Goal:** "Build out the system-wide skills library for broader agent use."
- Added `bug-reporter` — structured bug reporting with ADO work item creation
- Added `content-workflow` — portable replacement for Content Developer MCP server tools (ADO work items, git ops, PR creation)
- Added `environment-setup` — first-time machine setup guide
- Added `learn-chunk-analyzer` — RAG retrieval quality analysis for Microsoft Learn articles
- Added `one-pager` — project one-pager generation with live M365 data via WorkIQ MCP
- Added `pr-reviewer` — PR review against Microsoft Writing Style Guide
- Added `sfi-scanner` — SFI compliance scanning for documentation
- Added `writing-refinement` — prose tightening with character targets and Connect mode

### Thread 16 — Python fact-checking toolkit
**Goal:** "Build a local-first fact-checking toolkit that works without live MCP connections."
- Created `fact-check-v2/` Python package with gap analysis, graded reporting, and proposal-driven updates
- Added chunked multi-agent execution planning for large article sets
- Added sandbox mode for restricted tool environments
- Added chat-style tool call tracing for audit visibility

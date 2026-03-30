# .github — Copilot Customizations

Personal GitHub profile repo containing GitHub Copilot customizations for two pipelines: **romantic hard sci-fi fiction writing** and **Azure Networking documentation** on [learn.microsoft.com](https://learn.microsoft.com).

Organized following [GitHub's Copilot customization standards](https://docs.github.com/en/copilot/reference/customization-cheat-sheet).

## Repository Structure

```
.github/
├── copilot-instructions.md              # Always-on repo-wide instructions
├── agents/                              # Custom agents (select from dropdown)
│   ├── — Fiction Pipeline —
│   ├── brainstorm.agent.md              # Concept generation & story ideation
│   ├── reference-librarian.agent.md     # Reference book ingestion & indexing
│   ├── chapter-feedback.agent.md        # Real-time chapter feedback monitor
│   ├── fiction-writer.agent.md          # Chapter-by-chapter manuscript drafting
│   ├── fiction-editor.agent.md          # Multi-pass developmental & line editing
│   ├── beta-romantasy.agent.md          # Romantasy beta reader
│   ├── beta-scifi.agent.md              # Sci-fi beta reader
│   ├── originality-world-checker.agent.md   # Pre-writing originality scan
│   ├── originality-manuscript-checker.agent.md  # Post-draft prose originality scan
│   ├── originality-fixer.agent.md       # Generates replacements for flagged content
│   ├── publishing-editor.agent.md       # Final polish before publication
│   ├── epub-producer.agent.md           # Markdown → KDP-ready EPUB
│   ├── — Azure Documentation —
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
│   ├── — Fiction: Pre-Writing —
│   ├── concept-generator/               # High-velocity story concept generation
│   ├── concept-developer/               # Expands concept to full premise document
│   ├── story-architecture/              # Plot structure, beat sheets, series arcs
│   ├── world-builder/                   # Space opera settings & hard sci-fi systems
│   ├── character-forge/                 # Characters, romantic pairings, arcs
│   ├── — Fiction: Originality —
│   ├── name-originality-scan/           # Worldbuilding name collision detection
│   ├── concept-originality-scan/        # Worldbuilding concept parallel detection
│   ├── prose-name-scan/                 # Manuscript-level name collision scan
│   ├── scene-echo-scan/                 # Manuscript scene-level comparison
│   ├── name-replacement/                # Replacement name generation & propagation
│   ├── concept-rework/                  # Redesigns derivative worldbuilding concepts
│   ├── scene-rework/                    # Reworks flagged scenes via different path
│   ├── — Fiction: Writing —
│   ├── prose-craft/                     # Scene writing (Maas/Yarros style + sci-fi)
│   ├── chapter-critique/                # Developmental chapter feedback
│   ├── reference-ingest/                # Converts reference files to indexed text
│   ├── reference-reader/                # Style/structure analysis of reference books
│   ├── — Fiction: Editing —
│   ├── character-deepener/              # Deepens characters, relationships, arcs
│   ├── continuity-checker/              # Timeline & continuity error tracking
│   ├── universe-keeper/                 # World rule & physics consistency checks
│   ├── editorial-pass/                  # Multi-pass editing workflow orchestration
│   ├── romance-scene-critique/          # Romantic tension & intimate scene critique
│   ├── prose-tightener/                 # Line editing for publication quality
│   ├── final-line-edit/                 # Acquiring editor's final prose pass
│   ├── copyedit/                        # Chicago Manual of Style 18th copyediting
│   ├── proofread/                       # Final pre-publication proofreading pass
│   ├── style-sheet/                     # Fiction style sheet management
│   ├── — Fiction: Beta Reading —
│   ├── romantasy-read-through/          # Chapter-by-chapter romantasy reader log
│   ├── romantasy-reader-report/         # Comprehensive romantasy beta report
│   ├── scifi-read-through/              # Chapter-by-chapter sci-fi reader log
│   ├── scifi-reader-report/             # Comprehensive sci-fi beta report
│   ├── scifi-world-review/              # Deep sci-fi worldbuilding evaluation
│   ├── — Fiction: Publication —
│   ├── publication-prep/                # Manuscript prep for submission/self-pub
│   ├── manuscript-prep/                 # Validates markdown for Pandoc → EPUB
│   ├── epub-build/                      # Pandoc-based EPUB build pipeline
│   ├── epub-stylesheet/                 # KDP-compatible CSS for Kindle devices
│   ├── epub-validate/                   # EPUBCheck + KDP compliance validation
│   ├── kdp-upload/                      # Amazon KDP dashboard upload guide
│   ├── — Azure Documentation —
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

---

## Fiction Pipeline

A complete end-to-end pipeline for writing, editing, and publishing romantic hard sci-fi novels in the style of Sarah J. Maas and Rebecca Yarros — adapted from fantasy romantasy into space-based epic science fiction.

### Fiction Pipeline Flow

```
brainstorm agent          → concept-generator, concept-developer skills
story-architecture skill  → world-builder, character-forge skills
originality-world-checker agent → originality-fixer agent
fiction-writer agent (+ chapter-feedback monitor)
originality-manuscript-checker agent → originality-fixer agent
fiction-editor agent      → beta-romantasy & beta-scifi agents (parallel)
publishing-editor agent
epub-producer agent       → manuscript-prep → epub-build → epub-validate → kdp-upload
```

### Fiction Agents

| Agent | Description |
|-------|-------------|
| `@brainstorm` | Generates 3–5 differentiated story concepts from minimal input — hooks, protagonists, worlds, romance engines, comp titles. Hands winning concepts to story-architecture, world-builder, or character-forge |
| `@reference-librarian` | Ingests epub, docx, pdf, txt, and markdown reference books into the fiction pipeline. Converts, indexes, and analyzes for prose style, narrative structure, and voice characteristics |
| `@chapter-feedback` | Persistent monitor running alongside fiction-writer. Watches for chapter completion signals, generates developmental feedback, and writes it back automatically — chapter by chapter through all 27 chapters |
| `@fiction-writer` | Orchestrates chapter-by-chapter manuscript drafting for romantic hard sci-fi. Integrates worldbuilding, character bibles, beat sheets, and real-time editing feedback. Generates 5,000–9,000 word chapters with emotional beats, romance progression, and sci-fi consistency |
| `@fiction-editor` | Performs iterative developmental and line editing through five focused passes: character/relationship deepening, continuity checking, universe rule verification, prose tightening, and final polish |
| `@beta-romantasy` | Devoted romantasy beta reader. Tests chemistry, trope execution, heat level, intimate scene quality, and emotional impact. Produces chapter journals and comprehensive reader reports with trope scorecards |
| `@beta-scifi` | Devoted sci-fi beta reader. Tests technology plausibility, worldbuilding depth, character believability, pacing, and whether the story satisfies a dedicated sci-fi audience |
| `@originality-world-checker` | Pre-writing checkpoint. Scans worldbuilding documents, character bibles, outlines, and beat sheets for names and concepts too close to published SFF and romantasy. Deep familiarity with Maas, Yarros, Peckham, Herbert, Martin |
| `@originality-manuscript-checker` | Post-draft forensic scan. Scene-by-scene comparison of finished prose against published works — catches what emerges during creative writing that world-level scan misses |
| `@originality-fixer` | Takes findings from originality checkers and generates replacement names, reworks flagged scenes, and redesigns derivative concepts. Propagates all changes across every project document with full change log |
| `@publishing-editor` | Senior Big Five publishing house editor for final manuscript polish. Final line edit, Chicago Manual of Style 18th copyediting, proofreading, style sheet management, and publication preparation |
| `@epub-producer` | Converts finished markdown manuscript into KDP-ready EPUB. Orchestrates: manuscript prep → stylesheet → Pandoc build → EPUBCheck validation → KDP upload guidance |

### Fiction Skills

#### Pre-Writing

| Skill | Description |
|-------|-------------|
| `concept-generator` | High-velocity concept generation from minimal input — 3–5 differentiated story concepts with hooks, protagonists, worlds, and romance engines |
| `concept-developer` | Expands chosen concept to full premise document — protagonist profile, world foundation, series potential, romance architecture, and thematic core |
| `story-architecture` | Designs plot structure, beat sheets, chapter outlines, and series arcs for romantic hard sci-fi. Maps romantasy beats to space opera with tension curves and cliffhanger engineering |
| `world-builder` | Designs scientifically grounded space opera settings — FTL physics, interstellar politics, fleet hierarchies, alien species, technology systems, and locations |
| `character-forge` | Creates complex characters, romantic pairings, found-family dynamics, and character arcs. Includes voice sheets, relationship maps, and wound/desire/need profiles |

#### Originality

| Skill | Description |
|-------|-------------|
| `name-originality-scan` | Scans worldbuilding docs, character bibles, and outlines for name collisions with published SFF and romantasy works |
| `concept-originality-scan` | Scans worldbuilding concepts and political structures for structural parallels to published works. Distinguishes acceptable genre conventions from specific-work echoes |
| `prose-name-scan` | Scans finished manuscript prose scene-by-scene for names and invented terms introduced during drafting. Cross-references prior scan results |
| `scene-echo-scan` | Scene-by-scene comparison of manuscript prose against known published scenes. Flags specific choreography and emotional sequences too close to published works |
| `name-replacement` | Generates replacement name candidates that fit in-world conventions and are verifiably original. Propagates changes across all documents with change log |
| `concept-rework` | Redesigns flagged worldbuilding concepts. Generates 3 alternative approaches maintaining narrative function while being structurally original. Updates downstream documents |
| `scene-rework` | Reworks flagged scenes to achieve the same narrative beat via a different path — preserving emotional impact and character development while changing choreography |

#### Writing

| Skill | Description |
|-------|-------------|
| `prose-craft` | Writes vivid, emotionally charged scenes blending romantasy prose style with hard sci-fi settings. Covers POV, sensory writing, dialogue, pacing, and emotional beats in the style of Maas and Yarros |
| `chapter-critique` | Generates developmental chapter feedback — evaluates prose quality, POV adherence, emotional beats, romance arc position, continuity flags, and scene structure. Works on any book |
| `reference-ingest` | Converts raw reference materials (epub, docx, pdf, txt, markdown) to clean indexed text using calibre. Validates output and cleans conversion artifacts for context-mode indexing |
| `reference-reader` | Analyzes reference books for prose style, narrative structure, pacing patterns, and voice characteristics. Produces actionable style guides from indexed reference-books/ |

#### Editing

| Skill | Description |
|-------|-------------|
| `character-deepener` | Deepens characters, relationships, and arcs — identifies flat characterization, static relationships, missed emotional beats, and inconsistent voice with specific actionable rewrites |
| `continuity-checker` | Tracks continuity errors across manuscripts. Builds timelines, tracks character details, monitors plot threads, verifies information flow, and catches contradictions |
| `universe-keeper` | Verifies fiction prose obeys established world rules, physics, technology constraints, and faction logic. Catches science errors and world-building contradictions in hard sci-fi |
| `editorial-pass` | Orchestrates multi-pass fiction editing workflows. Tracks which passes have been run, issues found and resolved, and manuscript readiness across iterative drafts |
| `romance-scene-critique` | Detailed critique of romantic tension and intimate scenes — evaluates buildup, pacing, emotional payoff, heat calibration, character vulnerability, and relationship deepening |
| `prose-tightener` | Line-edits fiction for publication quality — cuts flab, strengthens verbs, fixes pacing, sharpens dialogue, eliminates clichés, and polishes chapter hooks while preserving author voice |
| `final-line-edit` | The acquiring editor's final prose pass before copyediting. Polishes voice consistency, paragraph rhythm, chapter flow, and market readiness. Structure locked — pure prose refinement |
| `copyedit` | Professional copyediting per Chicago Manual of Style 18th edition — grammar, punctuation, spelling, consistency enforcement, author queries, and style sheet integration |
| `proofread` | Absolute final pass before publication. Catches typos, orphan errors from edits, formatting inconsistencies, missing scene breaks, and chapter numbering errors. Corrections only |
| `style-sheet` | Builds and maintains fiction style sheet — character names, physical descriptions, locations, timeline, invented terminology, spelling decisions, and series continuity |

#### Beta Reading

| Skill | Description |
|-------|-------------|
| `romantasy-read-through` | Chapter-by-chapter reader reaction journal from a devoted romantasy fan. Tracks romance beats, chemistry, emotional engagement, trope execution, heat level, and standout moments |
| `romantasy-reader-report` | Comprehensive romantasy beta reader report — romance engagement, trope execution, heat assessment, emotional impact, beat checklist, and comp title positioning with final verdict |
| `romance-scene-critique` | Detailed critique of romantic tension and intimate scenes — heat calibration, consent dynamics, vulnerability, pacing, and whether scenes deepen the relationship |
| `scifi-read-through` | Chapter-by-chapter reader reaction journal from a devoted sci-fi fan. Tracks engagement, immersion breaks, confusion points, and where sci-fi elements shine or fail |
| `scifi-reader-report` | Comprehensive sci-fi beta reader report — engagement data, worldbuilding assessment, character reactions, pacing analysis, DNF risk, and comp title positioning |
| `scifi-world-review` | Deep evaluation of sci-fi worldbuilding from a genre expert — technology plausibility, faction complexity, setting originality, internal consistency, and sense of scale |

#### Publication

| Skill | Description |
|-------|-------------|
| `publication-prep` | Prepares manuscript for typesetting, submission, or self-publication — frontmatter, backmatter, chapter formatting, scene break standardization, synopsis, query letter blurb, and series metadata |
| `manuscript-prep` | Validates and prepares markdown manuscript for Pandoc → EPUB conversion. Checks structure, headings, scene breaks, front/back matter, and formatting. Runs pre-conversion quality gate |
| `epub-build` | Converts prepared markdown manuscript into KDP-ready EPUB using Pandoc. Handles build pipeline, validation, and output verification |
| `epub-stylesheet` | Creates and maintains KDP-compatible CSS stylesheets for fiction ebooks that render on all Kindle devices. Customizable for genre-specific styling |
| `epub-validate` | Validates EPUB for Amazon KDP compliance using EPUBCheck and Kindle Previewer. Ensures zero errors and zero warnings before upload |
| `kdp-upload` | Guides through the complete Amazon KDP dashboard workflow — account setup to clicking Publish. Covers everything after EPUB is built and validated |

---

## Azure Documentation Pipeline

Customizations for Azure Networking documentation workflows on [learn.microsoft.com](https://learn.microsoft.com).

### Azure Documentation Agents

| Agent | Description |
|-------|-------------|
| `@content-developer` | Automates ADO work item creation, git branching, commit messages, PR creation with AB# linking, and work item closure with publish date calculation. v7.0.0: fully skills-based, no VPN or MCP server required |
| `@product-manager` | Creates Feature work items from SupportabilityCheckList requirements with auto-calculated ADO fields, parent linking, and iteration path calculation |
| `@technical-advisor` | Automates CSS PACE bug workflows — creates Content Bugs from PACE escalations, manages cross-org linking between PACE and Content ADO projects with triple linking strategy |
| `@microsoft-fact-checker` | Verifies technical accuracy against authoritative Microsoft sources with evidence-based recommendations and complete citations |
| `@CIA-Analysis` | Generates Customer Incidents Analysis reports identifying recurring incident patterns, high-impact issue categories, and documentation gaps from public Microsoft sources |

### Azure Documentation Skills

| Skill | Description |
|-------|-------------|
| `content-workflow` | Core workflow orchestration — work items, git branching, commit messages, PRs with AB# linking, publish dates |
| `environment-setup` | First-time setup — Azure CLI auth, GitHub CLI auth, Git configuration, repository cloning |
| `doc-writer` | Scaffold production-ready Azure documentation (how-to, concept, quickstart, tutorial, overview) |
| `documentor-workflow` | Editorial quality workflows — SEO, engagement analysis, markdown auto-fix, link validation |
| `pr-reviewer` | Microsoft Writing Style Guide PR review with 98 style patterns across 7 categories |
| `sfi-scanner` | SFI compliance scanning — Global Admin roles, insecure auth flows, sensitive identifiers in text and images |
| `fact-checker` | 7 specialized fact-checking workflows with tiered source authority hierarchy |
| `microsoft-doc-verifier` | Cross-product documentation verification with single article, batch, and PR review modes |
| `azure-quickstart-templates` | Review, validate, or create Azure Quickstart Templates following contribution guidelines |
| `bug-reporter` | Report bugs in Content Developer tooling with structured ADO Bug creation and parent linking |

---

## Prompts

| Prompt | Description |
|--------|-------------|
| `complete-fact-check` | Fact-check the current article against official Microsoft docs, generate a report |
| `complete-fact-checker-internal` | Fact-check using both public and internal Microsoft resources |
| `complete-freshness-review` | Full freshness review — update content, fact-check, fix links, optionally PR |
| `fact-check-and-edit` | Quick in-place fact-check with inline corrections |
| `microsoft-researcher` | Research a topic using official Microsoft documentation with full citations |
| `ado-work-item-standards` | Create or validate ADO work items per Azure Core Content Standards |

## Instructions

| File | Applies To | Description |
|------|------------|-------------|
| `markdown-authoring.instructions.md` | `**/*.md` | Microsoft Learn writing standards — sentence-case headings, present tense, second person, MS terminology |
| `yaml-metadata.instructions.md` | `**/*.yml` | YAML metadata standards for MS Learn — TOC schema, landing page structure, indentation rules |
| `sfi-security.instructions.md` | `**/*.md` | SFI compliance guidelines — confidential content handling, security posture, data classification |

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
- **Agents**: Select from the agent dropdown (`@fiction-writer`, `@brainstorm`, `@content-developer`, etc.)
- **Prompts**: Attach from the prompt picker in chat
- **Skills**: Auto-loaded by Copilot when relevant to your task
- **Instructions**: `copilot-instructions.md` always active; path-specific rules auto-applied by file type

### GitHub Copilot CLI
Agents, skills, and instructions are supported. Use agents from the agent selector.

### Claude Code / OpenCode
Point these tools at `copilot-instructions.md` for repo-wide context. Individual prompt and skill markdown files can be referenced directly in conversations. Agents and auto-discovery are not natively supported.

### GitHub.com (Coding Agent)
Agents, skills, prompts, and instructions are supported when this repo is your `.github` profile repo.

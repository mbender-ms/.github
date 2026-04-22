# Question Builder

A self-contained GitHub Copilot agent package for building tagged evaluation question sets for Azure services.

Question Builder collects questions from selected sources, classifies each row with the required metadata, deduplicates the result set, and writes one final CSV for retrieval and answer-evaluation workflows.

---

## Prerequisites

| Requirement | Notes |
| --- | --- |
| VS Code | Latest stable |
| GitHub Copilot extension | Agent mode enabled |
| `.github` repo cloned locally | This package must be in your VS Code workspace |
| GitHub MCP server | Required for GitHub Issues source |
| WorkIQ MCP server | Optional for M365 source |
| Python 3.10+ | Required for Microsoft Q&A scraping |
| Q&A scraper dependencies | `pip install -r agents/question-builder/scripts/requirements.txt` |

---

## Quick start

1. Open the `.github` folder as a VS Code workspace folder.
2. Open Copilot Chat, switch to **Agent mode**, and select **Question Builder**.
3. Describe what you want.

   Example:

   `Generate 15 questions from these known issues: 502 errors with WAF, SSL certificate rotation failures, backend health probe timeouts`

4. The agent asks for any missing required intake values in this order:
   - Azure service
   - Total question count
   - Source checklist
5. Complete the intake.
6. The agent writes a single final CSV to `agents/question-builder/output/` unless you provide another output path.

---

## Output contract

Question Builder produces one final CSV only.

| Folder | Purpose |
| --- | --- |
| `artifacts/` | Temporary intermediate files only |
| `output/` | Final user-facing CSV only |

The CSV must follow this exact header:

```csv
Question,Source,Type,Confidence,Notes
```

The field values are governed by `references/metadata-tagging-guide.md`, which mirrors the pilot FAQ metadata table.

---

## Source checklist

Question Builder asks the user to confirm one or more of these sources before collection begins:

- Single article
- Multiple articles
- Microsoft Q&A
- Canonical CSV
- Customer issue spec
- GitHub Issues
- WorkIQ M365
- Ask Learn telemetry via canonical CSV

---

## File structure

| File | Purpose |
| --- | --- |
| `agents/question-builder.agent.md` | Discoverable launcher for VS Code Agent mode |
| `agents/question-builder/README.md` | Package setup and usage guide |
| `agents/question-builder/.gitignore` | Keeps temporary and final outputs out of git |
| `agents/question-builder/config/variables.yaml` | Package defaults such as output and artifact folders |
| `agents/question-builder/instructions/workflow.instructions.md` | Primary workflow and intake contract |
| `agents/question-builder/instructions/msqa-search.instructions.md` | Internal Microsoft Q&A scraping workflow |
| `agents/question-builder/references/source-workflows.md` | Detailed per-source collection rules |
| `agents/question-builder/references/metadata-tagging-guide.md` | Authoritative metadata tagging contract |
| `agents/question-builder/references/service-tag-index.md` | Service-to-tag lookup table |
| `agents/question-builder/templates/question-set-template.csv` | CSV template for the final output |
| `agents/question-builder/scripts/` | Packaged helper scripts used by this agent |
| `agents/question-builder/artifacts/` | Temporary intermediate outputs |
| `agents/question-builder/output/` | Final CSV output location |

---

## Distribution guidance

For sharing with teammates, distribute the top-level launcher plus the full `agents/question-builder/` folder together.

This package intentionally keeps its specialized instructions, references, templates, and scripts together instead of splitting them across `agents/`, `skills/`, and `scripts/`. That makes the workflow portable and avoids multiple competing sources of truth.
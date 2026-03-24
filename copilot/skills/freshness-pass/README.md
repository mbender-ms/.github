# Freshness Pass Skill

Comprehensive content freshness workflow for Microsoft documentation. Combines a full fact-check against public docs and APIs with a complete editorial pass (SEO audit, markdown auto-fix, content suggestions, MS Style Guide checks) in a single command.

## Workflows

| Workflow | Prompt asset | Slash-command | Scope |
|----------|-------------|---------------|-------|
| Single Article | `assets/freshness-pass.prompt.md` | `/freshness-pass` | Currently open article |
| Batch | `assets/batch-freshness-pass.prompt.md` | `/batch-freshness-pass` | Folder, glob, or file list |

## What it does

### Phase A — Fact-check
- Extracts all technical claims from the article(s)
- Verifies each claim against Tier 1–3 public sources (learn.microsoft.com, TechCommunity, GitHub)
- Checks for deprecation, retirement, and version changes
- Validates code examples
- Classifies claims: ✅ Accurate, ⚠️ Partial, ❌ Inaccurate, 🕐 Outdated, ❓ Unverifiable, 🔗 Broken link

### Phase B — Editorial pass
- **Editorial review**: Frontmatter, title/description validation, passive voice, procedures, sensitive identifiers
- **SEO audit**: Title, description, H1, intro paragraph, subheadings, alt text, internal linking
- **Auto-fix markdown**: Heading hierarchy, code fences, alerts, lists, tables, whitespace
- **Content suggestions**: Bounce rate, CTR, copy-try-scroll, dwell, exit rate improvements
- **MS Style Guide**: Voice/tone, contractions, capitalization, procedures, active voice, Oxford comma

### Phase C — Consolidation
- Applies all corrections directly to the file(s)
- Updates `ms.date` to today's date
- Presents per-edit summary with source citations
- Offers git workflow (branch, commit, push, PR)

## Usage

### Single article
Open an article and run the `/freshness-pass` slash-command, or invoke the `freshness-pass` skill.

### Batch
Run the `/batch-freshness-pass` slash-command with a folder path, glob pattern, or file list. For 5+ files across multiple service areas, the workflow automatically parallelizes using sub-agents.

## Relationship to other skills

| Skill | Relationship |
|-------|-------------|
| `doc-verifier` | Freshness-pass reuses the fact-check methodology and source hierarchy. `doc-verifier` offers more granular workflows (10 total) for fact-checking alone. |
| `documentor-workflow` | Freshness-pass reuses the editorial review workflows. `documentor-workflow` offers individual editorial workflows (title, description, SEO, engagement, markdown, links) that can be run independently. |
| `doc-verifier/complete-freshness-review.prompt.md` | The existing freshness review covers fact-check + staleness only. This skill is the superset — adding full editorial, SEO, and Style Guide checks. |

## Deploying to VS Code

Run `sync-prompts.ps1` to copy the prompt assets to your VS Code prompts directory:

```powershell
cd C:\github\.github
.\sync-prompts.ps1
```

Both `freshness-pass.prompt.md` and `batch-freshness-pass.prompt.md` will be available as slash-commands.

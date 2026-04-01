---
name: freshness-pass
description: "Content freshness workflow — full fact-check against public docs and APIs, comprehensive editorial review, SEO audit, markdown auto-fix, content suggestions, and MS Style Guide checks. Single-article and batch modes available as slash-commands."
argument-hint: "Describe the freshness task: 'freshness pass on this article', 'batch freshness pass on articles/container-apps/', or 'freshness pass — focus on API accuracy'"
user-invocable: true
---

# Freshness Pass — Content Freshness Workflow

Run a comprehensive freshness pass on Microsoft documentation articles. Combines a full fact-check (doc-verifier) with a full editorial pass (documentor-workflow) in a single workflow.

> **Slash-commands**: Both workflows are available as VS Code slash-commands after running `sync-prompts.ps1`.

## Workflow selection

| # | Workflow | When to use | Slash-command |
|---|---------|-------------|---------------|
| 1 | **Single Article** | Freshness pass on the currently open article | `/freshness-pass` |
| 2 | **Batch** | Freshness pass on a folder, glob, or file list | `/batch-freshness-pass` |

### Decision guide

- **"Run a freshness pass on this article"** → Workflow 1
- **"Freshness pass on articles/container-apps/"** → Workflow 2
- **"Check these 10 files for freshness"** → Workflow 2

## Model routing (dispatcher mode)

This skill orchestrates phases and delegates specialized logic. Do not duplicate sibling skill logic inline.

- **Phase A (Fact-check)**: Delegate verification depth to `doc-verifier`; when code/config is present, apply strict verify routing (Codex-first behavior from `model-routing-authoring`).
- **Phase B (Editorial pass)**: Delegate editorial quality tasks to `documentor-workflow`; model selection is advisory in Auto mode.
- **Phase C (Consolidation)**: Merge outputs, apply edits, and produce a single consolidated report.

Auto behavior for freshness-pass:

- Strict for code/config verification paths in Phase A
- Advisory for planning, drafting, and editorial polish paths
- If a preferred model is unavailable, continue with the best available equivalent and report the substitution

## Prompt assets

| File | Workflow |
|------|----------|
| `assets/freshness-pass.prompt.md` | 1 — Single Article |
| `assets/batch-freshness-pass.prompt.md` | 2 — Batch |

---

## Phases (shared by both workflows)

Both workflows execute these three phases in sequence:

### Phase A — Fact-check

Full fact-check of all technical claims against public sources.

1. Extract every technical claim: product/service names, feature capabilities, limitations, prerequisites, version numbers, API references, CLI commands, configuration values, defaults, quotas, code examples
2. Verify each claim against the [source authority hierarchy](../_shared/source-hierarchy.md):
   - **Tier 1 (Primary)**: learn.microsoft.com, azure.microsoft.com
   - **Tier 2 (Secondary)**: techcommunity.microsoft.com, devblogs.microsoft.com, github.com/Azure, github.com/MicrosoftDocs
   - **Tier 3 (Cross-reference)**: developer.microsoft.com, code.visualstudio.com, MS Q&A (verified MS employees only)
3. Use Microsoft Learn MCP tools: `microsoft_docs_search`, `microsoft_docs_fetch`, `microsoft_code_sample_search`
4. Use `web/fetch` and `web/githubRepo` for API specs, SDK repos, and REST API definitions
5. Check for deprecation notices, retirement announcements, and version changes
6. Validate code examples using `get_errors` where applicable
7. Classify each claim:

| Icon | Status | Action |
|------|--------|--------|
| ✅ | Accurate | No change |
| ⚠️ | Partially accurate | Edit with correction |
| ❌ | Inaccurate | Edit + cite source |
| 🕐 | Outdated | Update + cite source |
| ❓ | Unverifiable | Flag — do not remove |
| 🔗 | Broken link | Fix or flag |

### Phase B — Editorial pass

Comprehensive editorial review covering all quality dimensions.

#### B1 — Editorial review

1. Check frontmatter completeness: title, description, ms.date, ms.topic, ms.service, ms.custom, customer intent
2. Verify title: 30–65 chars, title case, primary keyword near beginning
3. Verify description: 120–165 chars, unique from title/H1, includes CTA
4. Scan for passive voice — rewrite to active voice using "you" to address readers
5. Check that procedures have ≤ 10 steps and begin with a verb
6. Verify sentence-style capitalization on all H2+ headings (capitalize only first word and proper nouns)
7. Check for sensitivity issues — replace any real GUIDs, secrets, or IDs with approved placeholders (see [sensitive-identifiers.md](../documentor-workflow/references/sensitive-identifiers.md))

#### B2 — SEO audit

Full SEO checklist per [seo-and-metadata.md](../_shared/seo-and-metadata.md):

1. **Title** — 30–65 chars, title case, primary keyword, unique from H1/description, no gerunds
2. **Description** — 120–165 chars, CTA, primary keyword at beginning, unique
3. **H1** — Sentence case (NOT title case), primary keyword, no gerunds
4. **Intro paragraph** — Primary keyword in first or second sentence, 2–3 sentences, aligns with customer intent
5. **Subheadings** — Sentence case, secondary keywords, no gerunds, preserve standard headings (Prerequisites, Related content, Next steps)
6. **Image alt text** — 40–150 chars, starts with "Screenshot of..." or "Diagram of..."
7. **Internal linking** — Relative paths for same docset, descriptive anchor text, 3–5 related content links, 1–3 next steps

#### B3 — Auto-fix markdown

Fix formatting issues per [formatting-rules.md](../_shared/formatting-rules.md):

1. Fix heading hierarchy (no skipped levels, single H1)
2. Ensure blank lines before and after headings, code blocks, lists, and alerts
3. Fix list formatting (consistent markers, proper nesting)
4. Fix code fence language identifiers (`azurecli` not `bash`, `azurepowershell` not `powershell`)
5. Fix alert syntax to standard format: `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!CAUTION]`, `> [!WARNING]`
6. Fix table alignment and formatting
7. Remove trailing whitespace; ensure file ends with single newline

#### B4 — Content suggestions

Engagement-driven improvements per [engagement-checklist.md](../documentor-workflow/references/engagement-checklist.md):

1. **Bounce rate** — Check intro hooks, visual elements, content relevance
2. **Click-through rate** — Check link placement, anchor text quality, CTA clarity
3. **Copy-try-scroll rate** — Check code sample quality, procedure clarity, scanability
4. **Dwell rate** — Check content depth, examples for abstract concepts, tables for comparisons
5. **Exit rate** — Check next steps section, related content links, progressive disclosure

#### B5 — MS Style Guide checks

Writing quality per [writing-style.md](../_shared/writing-style.md):

1. **Voice** — Warm, relaxed, crisp, ready to lend a hand
2. **Contractions** — Use "you'll", "it's", "don't" — not formal alternatives
3. **Sentence-style capitalization** — All H2+ headings, bullet items, table cells
4. **Procedures** — Imperative verbs, one action per step, max 7 steps per section
5. **Active voice** — "The function processes the message" not "The message is processed"
6. **Word choices** — Use simple, everyday words; avoid jargon without context
7. **Oxford comma** — Always: "VMs, storage, and networking"
8. **Audience** — Write for experienced professionals new to this specific feature

### Phase C — Consolidation

1. Apply all corrections directly to the file(s)
2. Update `ms.date` to today's date (MM/DD/YYYY format) on every edited file
3. Present per-edit summary in chat:

   **Edit N: [brief description]**
   - **Line(s)**: [approximate line number(s)]
   - **What changed**: [original text] → [new text]
   - **Why**: [brief explanation]
   - **Type**: Fact-check (Outdated | Inaccurate | Broken Link) or Editorial (SEO | Style | Markdown | Metadata | Engagement | Sensitivity)
   - **Source(s)**: [Title](URL) — for fact-check edits only

4. End with summary totals:
   - Total edits by phase (fact-check vs. editorial)
   - Count by type
   - Reminder to review via Source Control (Ctrl+Shift+G) or `git diff`

5. Offer git workflow:
   - Create branch: `freshness/[article-name]-MMDDYYYY`
   - Commit with descriptive message
   - Push branch
   - Open pull request with freshness review summary

---

## Quality checklist

Before finishing, confirm:

- [ ] All technical claims verified against Tier 1 sources
- [ ] Every fact-check correction includes a source citation
- [ ] Code examples validated
- [ ] Version/deprecation status confirmed for mentioned services
- [ ] Broken links fixed or flagged
- [ ] `ms.date` updated to today's date
- [ ] Title: 30–65 chars, title case, primary keyword
- [ ] Description: 120–165 chars, CTA, unique
- [ ] H1: sentence case, differs from title
- [ ] Heading hierarchy correct (no skipped levels)
- [ ] Sentence-style capitalization on all H2+ headings
- [ ] Code fence identifiers correct (`azurecli`, `azurepowershell`)
- [ ] Sensitive identifiers replaced with approved placeholders
- [ ] Writing style follows MS Style Guide
- [ ] No passive voice without justification
- [ ] Engagement improvements suggested

## Reference files

Load these resources as needed during the freshness pass:

- [_shared/source-hierarchy.md](../_shared/source-hierarchy.md) — Source authority tiers for fact-checking
- [_shared/seo-and-metadata.md](../_shared/seo-and-metadata.md) — SEO optimization and metadata rules
- [_shared/formatting-rules.md](../_shared/formatting-rules.md) — Markdown formatting standards
- [_shared/writing-style.md](../_shared/writing-style.md) — Microsoft writing style guide
- [documentor-workflow/references/engagement-checklist.md](../documentor-workflow/references/engagement-checklist.md) — Engagement metric analysis
- [documentor-workflow/references/sensitive-identifiers.md](../documentor-workflow/references/sensitive-identifiers.md) — Approved GUID/secret replacement values

---
name: retrievability
version: 1.0.0
category: Analysis
description: Analyze a documentation article for RAG retrievability risks and provide recommendations to improve AI retrieval quality. Use when the user says "retrievability analysis", "ret analysis", "do a ret analysis", or wants to check how well an article is retrieved by AI systems like Microsoft Copilot.
argument-hint: "[article file path or currently open file]"
relevant-lesson-tags: [retrievability, rag, content-quality, ai-retrieval]
---

## Overview

Analyze a documentation article for RAG (Retrieval-Augmented Generation) retrievability risks and provide actionable recommendations to improve how well the article's content is retrieved by AI systems like Microsoft Copilot.

## RAG Context

The Knowledge Service that retrieves content:
- Returns up to **5 chunks per query** (max 500 tokens each, ~2,500 token grounding budget)
- **Prepends H1 + nearest H2** headings to each chunk for context
- **Code handling**: Small snippets (≤100 tokens) included in chunks; large code blocks (≥100 tokens) excluded from indexing
- **Images**: Removed but `alt` text retained with surrounding chunk content
- Uses **hybrid search**: keyword (lexical/BM25) + vector embeddings (semantic)

## 10 Dimensions (4 Categories)

### Category 1: Structural and Chunking (40% weight)

**1. Heading hierarchy** (16%) — Are headings discriminative? Does H1+H2 provide clear product + operation scope? Generic headings like "Overview" without qualifiers cause false-positive collisions.

**2. Chunk autonomy** (13%) — Can each section stand alone within the 5-chunk budget? Target 250-450 tokens per section. Flag multi-topic spans, >600-token blocks, excessive pronoun/back-references.

**3. Context completeness** (11%) — Are prerequisites, platform qualifiers (OS, version, SKU, region), and key definitions present locally in the chunk or in the prepended H1/H2? No hidden dependencies on unseen sections.

### Category 2: Semantic and Normalization (30% weight)

**4. Entity normalization** (10%) — Consistent canonical names for services/APIs/parameters. No alias scattering. Canonical-first pattern: full name + alias on first use, then consistent form throughout.

**5. Disambiguation** (10%) — Ambiguous terms explicitly scoped (version, SKU, region, OS). Pronouns resolved. Polysemous terms ("node", "instance", "machine") clarified in context.

**6. Semantic density** (10%) — High information-per-token. Minimal filler/marketing language. Each chunk has a single clear intent with concentrated high-signal tokens.

### Category 3: Query and Answer Design (18% weight)

**7. Structured data utilization** (8%) — Tables, parameter lists, numbered steps create strong lexical anchors. Parameters/constraints surfaced early. Procedures have explicit verification/success checks. Alt text on images is factual.

**8. Query-answer alignment** (10%) — Content structured to answer primary query pattern (conceptual: what/why, procedural: how-to, troubleshooting: symptom→cause→fix, reference: when/which). Answers extractable from single autonomous chunks.

### Category 4: Redundancy and Consistency (12% weight)

**9. Redundancy efficiency** (5%) — Functional repetition for autonomy is GOOD. Wasteful duplication (copy-pasted boilerplate, >70% identical lists across chunks) is BAD because it crowds out diverse chunks in top-5 results.

**10. Cross-section integrity** (7%) — No contradictory defaults, procedures, or terminology across sections. Inconsistencies undermine answer confidence.

## Scoring Scale (0-5)

| Score | Meaning |
|-------|---------|
| 5 | Excellent — purpose-built for RAG |
| 4 | Strong — minor refinements only |
| 3 | Adequate — works but improvable |
| 2 | Fair — needs restructuring |
| 1 | Weak — frequent retrieval degradation |
| 0 | Critical failure — severely harms retrieval |

## Weighted Score Calculation

```
Weighted = (heading_hierarchy × 0.16) + (chunk_autonomy × 0.13) + (context_completeness × 0.11)
         + (entity_normalization × 0.10) + (disambiguation × 0.10) + (semantic_density × 0.10)
         + (structured_data_utilization × 0.08) + (query_answer_alignment × 0.10)
         + (redundancy_efficiency × 0.05) + (cross_section_integrity × 0.07)
```

**Readiness thresholds:**
- 🟢 ≥ 4.0 — Ready for RAG
- 🟡 3.0–3.9 — Needs improvement
- 🔴 < 3.0 — Significant rework needed

## What Actually Drives Improvement (Evidence-Based)

From the UAT correlation analysis (19 articles tested), the **"semantic core" dimensions** appeared in 100% of articles that showed significant retrieval improvement (+2.0 or more):

| Dimension | Correlation | Priority |
|-----------|-------------|----------|
| context_completeness | 🟢 Strong (100%) | **Focus here first** |
| disambiguation | 🟢 Strong (100%) | **Focus here first** |
| entity_normalization | 🟢 Strong (100%) | **Focus here first** |
| chunk_autonomy | 🟢 Strong (100%) | **Focus here first** |
| structured_data_utilization | 🟢 Strong (100%) | High impact |
| query_answer_alignment | 🟢 Strong (75%) | High impact |
| cross_section_integrity | 🟢 Strong (75%) | High impact |
| semantic_density | 🟡 Moderate (50%) | Secondary |
| heading_hierarchy | 🟡 Moderate (25%) | Secondary |
| redundancy_efficiency | 🔴 Weak (25%) | Low priority — often rejected by testers |

**High-impact changes that drove improvement:**
- Adding inline qualifiers and prerequisites to procedure sections
- Splitting multi-topic sections into focused subsections
- Normalizing canonical names and fixing casing inconsistencies
- Adding explicit verification steps after procedures
- Converting prose parameters to tables or bulleted lists

**Lower-impact changes (often rejected by testers):**
- Removing duplicate content ("intentional for reader benefit")
- Promoting H3s to H2s (often rejected due to doc patterns)
- Over-aggressive acronym normalization (readability concern)

## Workflow

### Phase 1: Read and Score

1. Read the full article using `read_file` directly (use a large line range like 1-500; do not run terminal commands like `wc -l` to pre-check file length)
2. Identify the article type (Conceptual, Procedural, Troubleshooting, Reference, or Hybrid)
3. Score all 10 dimensions (0-5) with one-sentence justifications
4. Calculate weighted score
5. Identify critical risks (any dimension scored 0-1)

### Phase 2: Present Analysis

Present results in this format:

```markdown
## Retrievability Analysis

**Article**: [filename]
**Type**: [Conceptual / Procedural / Troubleshooting / Reference]
**Weighted Score**: X.XX/5.00 [🟢/🟡/🔴]

### Scores

| Category | Dimension | Score | Justification |
|----------|-----------|-------|---------------|
| Structural | heading_hierarchy | X/5 | ... |
| Structural | chunk_autonomy | X/5 | ... |
| Structural | context_completeness | X/5 | ... |
| Semantic | entity_normalization | X/5 | ... |
| Semantic | disambiguation | X/5 | ... |
| Semantic | semantic_density | X/5 | ... |
| Query | structured_data_utilization | X/5 | ... |
| Query | query_answer_alignment | X/5 | ... |
| Redundancy | redundancy_efficiency | X/5 | ... |
| Redundancy | cross_section_integrity | X/5 | ... |

### Recommendations

For each recommendation (ordered by impact):

**[N]. [Action verb] [what to change]**
- **Dimensions**: [affected dimension IDs]
- **Location**: [section heading or line range]
- **Change**: [specific, actionable editorial change]
- **Impact**: [how this improves retrieval]
```

### Phase 3: Implementation (on user confirmation)

After user confirms, apply the recommended changes directly to the article. Follow the same rules as article integrity analysis:
- Wait for confirmation before editing
- Minimal edits — change only what's needed
- Preserve formatting
- Skip items the user rejects
- Summary after applying

## Rules

- **Evidence-based only** — cite specific text from the article
- **No new sections** — only modify within existing sections (split, rename, reorder, add inline definitions)
- **Canonical naming only** — don't introduce new aliases that fragment embeddings
- **Don't over-normalize acronyms** — readability matters; first-mention canonical + consistent use is sufficient
- **Don't remove intentional redundancy** — short functional repetition for chunk autonomy is good
- **Prioritize the semantic core** — context_completeness, disambiguation, entity_normalization, chunk_autonomy drive the most improvement
- **Procedures need verification steps** — add one-line success checks after steps that produce changes
- **Parameters in tables** — convert prose with ≥3 related parameters to tables or bulleted lists
- **Link stored procedures, cmdlets, and commands on first mention** — When introducing a stored procedure (e.g., `sp_help_log_shipping_primary_database`), PowerShell cmdlet (e.g., `Get-AzSqlDatabase`), Azure CLI command (e.g., `az sql db show`), or [!INCLUDE [tsql](...)] statement for the first time in an article, link it to its reference documentation. Example: "The following command uses the [sp_help_log_shipping_primary_database](../../relational-databases/system-stored-procedures/sp-help-log-shipping-primary-database-transact-sql.md) stored procedure to check..." This applies to the first mention in the article body and to any new section added during a retrievability pass (since each new section creates new chunks that may be retrieved in isolation, and the linked reference serves as disambiguation context). Do NOT add links on every subsequent mention — only the first time each command/procedure appears in prose. Inline code references in existing sections don't need to be back-linked unless the section is being rewritten.
- **Consolidating repetitive code blocks** — When the same code pattern is used multiple times with only minor parameter variations (e.g., running the same stored procedure for `LSBackup%`, `LSCopy%`, `LSRestore%` jobs), consolidate into a single code block. Provide the context for reuse in **descriptive prose before the code block** — NOT as an inline code comment (`-- run this for both...`) and NOT as a `> [!NOTE]` block. Example pattern: "Run the following command for each job by replacing the job name filter with `LSBackup%`, `LSCopy%`, or `LSRestore%`:" Descriptive prose before the code becomes part of the chunk's lexical anchor; inline comments get parsed as code and notes often end up in separate chunks. This approach also applies when consolidating nearly identical stored procedure blocks: describe the variation in prose before the code, then use placeholder patterns like `LS<Copy|Restore>%` in the code itself to signal where substitutions should occur.
- **Microsoft style** — sentence case headings, active voice, second person for instructions
- **Score 5 = no recommendation** — don't recommend changes for a dimension scored 5
- **Empty recommendations are valid** — if all dimensions are 4-5, say so

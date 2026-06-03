# Doc-Verifier Workflows — Detailed Reference

Detailed procedures, outputs, and comparison for the four doc-verifier workflows.

All workflows are **chat-only by default**. To save a markdown report, pass `--report <path>` — a file path for Single Article, PR Review, and Research; a directory for Fleet Batch. If a report is requested without a path, ask for the path before completing.

---

## One-Page Threshold Routing Card

Use this quick card before selecting a workflow or tier.

| Decision axis | Threshold | Workflow route | Tier route |
|---|---|---|---|
| Single article claim volume | 1-15 claims and low ambiguity | Single Article | Tier 2 |
| Single article claim volume | 16-40 claims or mixed ambiguity | Single Article (Tier 2 gather, Tier 1 adjudicate) | Tier 2 gather, Tier 1 adjudicate |
| Single article claim volume | More than 40 claims, cross-service scope, or safety-critical content | Fleet Batch (single-article track) | Tier 1-heavy |
| Batch size | Multiple articles | Fleet Batch | Tier 2 orchestration, Tier 1 for contested claims |
| PR scope | 1-5 doc files, mostly editorial or metadata changes | PR Review standard pass | Tier 2 or Tier 3 |
| PR scope | More than 5 files or major technical updates | PR Review plus deep pass on flagged files | Tier 1 on flagged files |

### Escalation Triggers

Escalate a claim or file to Tier 1 when any trigger matches:

- Tier conflict: Tier 1 and Tier 2 sources disagree.
- Unverifiable rate: more than 10% of claims in one file are unverifiable.
- Safety impact: claims affect RBAC, auth, encryption, compliance, or production availability.
- Confidence drop: reviewer confidence remains below high after Tier 2 analysis.
- Policy or retirement risk: deprecation, retirement, or SKU support boundary claims are present.

---

## Workflow 1: Single Article Check

**Prompt**: `single-article-check.prompt.md` | **Mode**: Agent

### When to use

- Full verification of a single article with product-area scoping
- Need product-area-specific search domains

### Key features

- Step 0 scoping: detects product area from `ms.service`/`ms.prod` metadata
- Uses product-area-specific search terms and paths
- Asks about depth preference (quick vs. thorough)

### Procedure

1. Scope: identify product area, service, depth
2. Identify all verifiable claims (including SKU/tier requirements)
3. Verify using product-area-specific search queries
4. Classify accuracy (5-level system)
5. Apply corrections; bump `ms.date` only when at least one claim was fetch-verified
6. Present results with per-issue details and source URLs

### Output

- Edited file with corrections
- Chat summary with source citations
- Optional markdown report when `--report <path>` is supplied

---

## Workflow 2: PR Review

**Prompt**: `pr-review.prompt.md` | **Mode**: Agent

### When to use

- Fact-check all changed files in a GitHub pull request
- Produce a verification summary for PR reviewers

### Procedure

1. Scope: PR number, repository, product area, depth
2. Load PR: fetch metadata, list changed files, filter to `.md`/`.yml`
3. Catalog and group files by service area
4. Verify per service group
5. Classify findings
6. Assemble findings; present in chat (or write to `--report <path>` if requested)

### Output

- Chat summary with per-file verification, link audit, and sources
- Optional markdown report when `--report <path>` is supplied
- Options: post findings as a PR comment, apply corrections

---

## Workflow 3: Research

**Prompt**: `microsoft-researcher.prompt.md` | **Mode**: Agent

### When to use

- Investigate a topic, not edit a file
- Answer a technical question with evidence, citations, and source tiers

### Key features

- 7-tier hierarchy (4 public + 3 internal)
- Output options: `output:chat` (default), `output:file` / `--report <path>`, `output:both`
- Does NOT edit existing files unless explicitly asked
- Claims classified: Verified / Partially Verified / Internally Verified / Unverifiable

### Procedure

1. Understand the research question (topic, scope, depth, audience, output)
2. Search broadly across public sources
3. Go deep — fetch full pages for key sources
4. Consult internal sources (if applicable)
5. Cross-reference and verify all claims
6. Validate code examples
7. Deliver output in the requested format

### Output

- Research findings: Summary, Details, Code Examples, Caveats, Sources table
- Optional: ⛔ Internal Findings section
- Optional markdown report when `--report <path>` (or `output:file`/`output:both`) is supplied

---

## Workflow 4: Fleet Batch

**Prompt**: `fleet-batch-verify.prompt.md` | **Mode**: Agent (parallel — CLI `/fleet` or Chat `runSubagent`)

### When to use

- Verify multiple articles in parallel
- Fact-check by traffic (feed `pageviews-query` JSON into this workflow)

### Key features

- One independent track per article — no shared state between tracks
- Builds a batch-wide `topic_key` index (via the Claim Manifest step) before fan-out so cross-article conflicts can be reconciled afterward
- Cross-track reconciliation groups results by `topic_key`; the highest-tier source wins on conflict

### Procedure

1. Scope and decompose: map each article to one track
2. Build the shared claim ledger: run claim-manifest extraction across all articles, coin `topic_key`s, record multi-file candidates
3. Per-article verification (parallel): read, extract, verify, classify, optionally correct
4. Consolidate: reconcile shared claims across tracks, surface conflicts first, summarize per-file
5. Present in chat (or write per-article + consolidated reports to `--report <dir>` if requested)

### Output

- Chat consolidated findings with cross-article reconciliation table
- Optional per-article and consolidated markdown reports when `--report <dir>` is supplied
- Optional corrections applied to articles when requested

---

## Supporting step: Claim Manifest

**Prompt**: `claim-manifest.prompt.md`

Not a standalone workflow. The Fleet Batch workflow uses claim-manifest extraction to catalog every claim and assign a `topic_key` to each one, building the cross-article index that powers reconciliation. It can also be run ad hoc to inventory an article's claims before verification.

---

## Workflow comparison

| Feature | Single Article | PR Review | Research | Fleet Batch |
|---------|----------------|-----------|----------|-------------|
| Edits file | ✅ | Optional | ❌ | Optional |
| Report file | Opt-in (`--report`) | Opt-in (`--report`) | Opt-in (`--report`) | Opt-in (`--report`) |
| Product scoping | ✅ | ✅ | ❌ | ✅ |
| Internal sources | ❌ | ❌ | ✅ | ❌ |
| Multi-file | ❌ | ✅ | ❌ | ✅ |
| Parallel execution | ❌ | Optional (per service group) | ❌ | ✅ (one track per article) |
| Cross-article reconciliation | ❌ | ❌ | ❌ | ✅ |

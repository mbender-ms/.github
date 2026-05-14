---
name: content-verification-batch
description: >
  Orchestrate a content verification run across multiple documentation articles.
  Use this skill when the user provides a folder path and asks to verify, audit,
  or check multiple articles for AI writing patterns. Trigger on phrases like
  "verify content in /path", "run a verification pass on this folder", "check all
  articles in /path", or "audit this doc set". Always use this skill — never attempt
  to loop through files manually or run content-verification directly on a folder.
  Requires GitHub Copilot CLI with /fleet support.
---

# Content Verification Batch Skill

## Identity and objective

You are an orchestrator. You discover articles, chunk them into batches, dispatch
subagents via `/fleet`, aggregate results, and create draft PRs. You do not run
the verification pass yourself — that is `content-verification`'s job. You do not
format reports — that is `verification-reporter`'s job.

Your two outputs are:
1. Per-article Markdown report, written by `verification-reporter` for each article
2. Batch summary report covering the full run — scoreboard and pattern trends

---

## Input

| Parameter | Required | Default | Description |
|---|---|---|---|
| `path` | yes | — | Folder path to scan (e.g., `/articles/azure-load-balancer`) |
| `severity_filter` | no | all | Limit pass to `high`, `high,medium`, or `all` |
| `dry_run` | no | false | Discover and list articles without running verification |

---

## Execution procedure

Follow these steps in order. Do not skip steps or reorder them.

### Step 1 — Discover articles

Recursively list all `.md` files under `path`. Exclude:
- Files in `node_modules/`, `.git/`, or any hidden directory
- Files named `README.md`, `CHANGELOG.md`, `toc.yml`
- Files smaller than 500 bytes (stubs, index files)

Log the discovered file count before proceeding. If `dry_run: true`, stop here
and return the file list with no further action.

### Step 2 — Chunk into batches

Split the discovered file list into batches of **maximum 9 articles**. Never
create a batch of 10 or more. If the total article count is not divisible by 9,
the final batch is smaller — that is expected.

Label each batch: `Batch 1 of N`, `Batch 2 of N`, etc.

Log the batch plan before executing:
```
Discovered: 47 articles
Batches: 6 (5 × 9 articles, 1 × 2 articles)
Output directory: /articles/azure-load-balancer/verification-reports/2026-05-08/
PRs to create: 6
```

### Step 3 — Create output directory

Create the output directory before dispatching any subagents:
```
[path]/verification-reports/[YYYY-MM-DD]/
```

### Step 4 — Dispatch batches via /fleet

Process batches **sequentially**. Within each batch, subagents run in **parallel**
via `/fleet`. Do not dispatch the next batch until the current batch is complete
and its PR is created.

For each batch, use this `/fleet` prompt structure:

---

**Subagent prompt template** (inject all values — subagents cannot see session history):

```
You are a content verification subagent. Verify the following article and produce
a Markdown report.

ARTICLE PATH: [absolute path to article]
OUTPUT PATH: [path]/verification-reports/[YYYY-MM-DD]/[article-slug]-report.md
RUN DATE: [YYYY-MM-DD]
SEVERITY FILTER: [all | high | high,medium]

STEP 1 — Run content-verification
Reference skill: skills/content-verification/SKILL.md
Anti-pattern checklist: skills/content-verification/references/ai-writing-antipatterns.csv
Apply the full 30-rule pass (or severity-filtered pass if specified).
Produce a structured YAML change log.

STEP 2 — Run verification-reporter
Reference skill: skills/verification-reporter/SKILL.md
Format the change log as a Markdown report.
Write the report to OUTPUT PATH.

STEP 3 — Return status
Return a JSON status block:
{
  "article": "[article slug]",
  "path": "[article path]",
  "status": "complete" | "failed",
  "findings": { "high": N, "medium": N, "low": N, "total": N },
  "bulk_patterns": N,
  "report_path": "[output path]",
  "error": null | "[error message if failed]"
}

If the article fails, retry once before returning status: "failed".
On the retry, re-run from Step 1.
Do not partially complete — either write a full report or return status: "failed".
```

---

### Step 5 — Handle failures

When a subagent returns `status: "failed"`:
- Log the article as **Not run** in the batch summary
- Record the error message
- Continue to the next article — do not halt the batch

Do not retry at the batch level. The subagent prompt already instructs one retry.

### Step 6 — Create draft PR for the batch

After all subagents in a batch complete (or fail), create a draft PR:

**Branch name:** `verification/[YYYY-MM-DD]-batch-[N]`

**PR title:** `Content verification — [folder name] — Batch [N] of [total] ([YYYY-MM-DD])`

**PR description:**
```markdown
## Content verification batch run

**Folder:** [path]
**Batch:** [N] of [total]
**Articles in this batch:** [count]
**Date:** [YYYY-MM-DD]

| Article | 🔴 High | 🟡 Medium | 🟢 Low | Status |
|---|---|---|---|---|
| [slug] | N | N | N | ✅ Complete |
| [slug] | — | — | — | ⚠️ Not run |

Full batch summary: `verification-reports/[YYYY-MM-DD]/batch-summary.md`
```

**Files in PR:** All report `.md` files from this batch's output directory.

### Step 7 — Generate batch summary

After **all batches** are complete and all batch PRs are created, generate a single
batch summary report at:
```
[path]/verification-reports/[YYYY-MM-DD]/batch-summary.md
```

See **Batch summary format** below.

Always create a **standalone PR** for the batch summary — never append it to a
batch PR. This applies regardless of total article count or number of batches.

**Branch name:** `verification/[YYYY-MM-DD]-summary`
**PR title:** `Content verification — [folder name] — Batch summary ([YYYY-MM-DD])`
**PR description:** Total articles verified, total findings by severity, links to all batch PRs.

---

## Batch summary format

```markdown
# Content Verification — Batch Summary

**Folder:** [path]
**Run date:** [YYYY-MM-DD]
**Total articles scanned:** N
**Total articles verified:** N
**Total articles not run:** N
**Batches:** N (N PRs created)

---

## Scoreboard

> Sorted by total findings, highest first.

| Article | 🔴 High | 🟡 Medium | 🟢 Low | Total | Bulk patterns | Status |
|---|---|---|---|---|---|---|
| [slug] | N | N | N | N | N | ✅ Complete |
| [slug] | N | N | N | N | N | ✅ Complete |
| [slug] | — | — | — | — | — | ⚠️ Not run |

---

## Pattern trends

> Which anti-patterns fired most frequently across this article set.
> Threshold: patterns appearing in **3 or more articles** (runs < 50 articles)
> or **5 or more articles** (runs ≥ 50 articles).

| Pattern | Category | Severity | Articles affected | Total instances |
|---|---|---|---|---|
| Em-dash as structural connector | Punctuation | 🟡 Medium | N | N |
| Throat-clearing intro | Structure | 🔴 High | N | N |

### Interpretation

[2–3 sentences identifying the dominant pattern and what it suggests about
the authoring workflow that produced this article set. Example: "Em-dash
overuse as a structural connector appears in 34 of 47 articles, suggesting
this pattern was introduced at the generation stage rather than by individual
authors. A single upstream prompt change would likely resolve the majority
of these findings."]

---

## Not run

| Article | Error |
|---|---|
| [slug] | [error message] |

---

## Run details

| Parameter | Value |
|---|---|
| Severity filter | [all / high / high,medium] |
| Batch size | 9 |
| Total batches | N |
| PRs created | [links] |
| Checklist version | ai-writing-antipatterns.csv |
```

---

## PR constraints

- **Hard limit:** Never create a PR containing 10 or more article reports
- **Maximum 9 articles per PR**, regardless of batch size
- If a batch produces fewer than 9 reports due to failures, create the PR anyway
- Draft PRs only — never open for review without human approval
- Branch protection and organization policies apply automatically via Copilot CLI

---

## Failure handling summary

| Scenario | Behavior |
|---|---|
| Subagent fails on first attempt | Retry once automatically (handled in subagent prompt) |
| Subagent fails after retry | Log as Not run, continue batch |
| Entire batch fails (all subagents) | Log all as Not run, still create PR, continue to next batch |
| Output directory creation fails | Halt entire run, report error — do not proceed |
| File discovery returns zero results | Halt, report no eligible articles found at path |

---

## Definition of done

The run is complete when:
- All discovered articles have a status of `complete` or `not run` — no articles
  in an unknown state
- One draft PR exists per batch, containing only that batch's report files
- No PR contains 10 or more article reports
- The batch summary exists at `[path]/verification-reports/[YYYY-MM-DD]/batch-summary.md`
- The scoreboard is sorted by total findings, highest first
- Pattern trends list all anti-patterns appearing in 3 or more articles
- All Not run articles are logged with their error message

---

## Skill dependencies

This skill requires both downstream skills to be present and functional:

```
skills/content-verification/SKILL.md
skills/content-verification/references/ai-writing-antipatterns.csv
skills/verification-reporter/SKILL.md
```

Verify these paths exist before dispatching the first batch. If either skill is
missing, halt and report which dependency is absent.

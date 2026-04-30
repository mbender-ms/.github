---
name: qa-customer-signal
description: >-
  Harvest real customer questions from Microsoft Q&A for an Azure service,
  evaluate how well existing documentation answers them, and produce a gap report
  (CSV + Markdown) classifying each gap as new-article, update-article, or add-section.
  Use as a standalone skill or as input to content-developer, connect-writer, or
  content-workflow for downstream authoring and ADO work item creation.
argument-hint: "Provide the Azure service name — e.g., 'Azure Load Balancer' or 'Azure Firewall'"
user-invocable: true
---

# Q&A Customer Signal Skill

Turn real customer questions from Microsoft Q&A into structured documentation gap findings.

## When to use

- Identifying documentation gaps using real customer signal from Q&A
- Prioritizing articles to update based on actual question frequency
- Generating input for ADO work items, PR drafts, or Connect article planning
- Running a monthly content health check for a service doc set

## Workflow summary

This skill runs the Q&A Gap Analyst agent package at `agents/qa-gap-analyst/`.

Invoke the **Q&A Gap Analyst** agent in VS Code Agent mode, or call this skill from another
agent by describing the service and invoking the three-phase pipeline:

1. **Harvest** — Scrape Microsoft Q&A → question set CSV (`Question, Source, Type, Confidence, Notes`)
2. **Evaluate** — Score questions via `learn-answer-eval-batch` → adds `chunk_relevance_score` + `generated_answer`
3. **Gap Analysis** — Map low-scoring questions to Learn articles → classify as `new-article`, `update-article`, or `add-section`

## Outputs

| File | Location | Purpose |
|---|---|---|
| `{service}-gap-analysis-{date}.csv` | `agents/qa-gap-analyst/output/` | Machine-readable gap findings |
| `{service}-gap-report-{date}.md` | `agents/qa-gap-analyst/output/` | Human-readable report grouped by gap type and article |

## Downstream use

| Goal | Next step |
|---|---|
| Create ADO work items for gaps | Feed gap report into `content-workflow` skill |
| Draft article edits for `update-article` gaps | Use `content-developer.agent.md` with gap CSV as input |
| Write new Connect articles for `new-article` gaps | Use `connect-writer.agent.md` with gap CSV as input |
| Freshness triage on `update-article` targets | Run `freshness-pass` skill against the flagged articles |

## Prerequisites

- Python 3.10+ with `pip install -r agents/qa-gap-analyst/scripts/requirements.txt`
- Learn MCP server available in VS Code (for Phase 2 evaluation and Phase 3 article matching)

## Invocation example

```
Run gap analysis for Azure Load Balancer
```

The agent confirms the Q&A tag, runs a smoke test, then proceeds through all three phases automatically.

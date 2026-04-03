# Runtime Adapter

Shared orchestration guidance for dual-runtime execution.

## Goal

Run parallel verification workflows in either runtime:
- Copilot CLI with `/fleet`
- Copilot Chat with `runSubagent`

Both paths must produce equivalent artifacts and status taxonomy.

## Runtime selection

Use this decision order:
1. If the user invocation explicitly uses `/fleet`, prefer CLI fleet dispatch.
2. Else if `runSubagent` is available, use Chat subagent dispatch.
3. Else fall back to sequential processing and clearly note reduced parallelism.

Do not fail a workflow only because `/fleet` is unavailable.

## Threshold-Based Dispatch

Apply these thresholds before selecting a dispatch pattern.

| Decision axis | Threshold | Dispatch choice |
|---|---|---|
| Articles in scope | 1 | Pattern B for deep verification, or sequential single-article flow |
| Articles in scope | 2-10 | Pattern A (article-level parallelism) |
| Articles in scope | More than 10 | Pre-stage with claim manifests, then run Pattern A in chunks |
| Claims in one article | 1-40 claims | Single-article flow, fan-out optional |
| Claims in one article | More than 40 claims | Pattern B (service-area fan-out) |
| Nested need | Multiple deep-check articles with high claim counts | Pattern C (hybrid), unless runtime cannot support nested parallelism |
| Re-check run | Less than 20% changed content | Incremental path, then selective pattern choice |

## Escalation Triggers

Escalate from Tier 2 or Tier 3 processing to Tier 1 claim adjudication when:

- Tier 1 and Tier 2 sources conflict.
- More than 10% of claims are currently unverifiable.
- Claim impact includes security, compliance, or production safety.
- Confidence after structured pass is not high.

## Dispatch patterns

### Pattern A: Article-level parallelism

Use when verifying multiple articles.
- Unit of parallel work: one article
- Output per unit: `factcheck_[article]_YYYYMMDD.md`
- Final merge output: `factcheck_batch_YYYYMMDD.md`

CLI path:
- `/fleet` creates one track per article.

Chat path:
- Spawn one `runSubagent` call per article.
- Orchestrator waits for all subagents, then consolidates.

### Pattern B: Service-area fan-out parallelism

Use for deep verification of one article with many claims.
- Unit of parallel work: one service-area claim group
- Output per unit: structured claim result set
- Final merge output: one `factcheck_[article]_YYYYMMDD.md`

CLI path:
- If subagent tooling is available, spawn subagents for each service group.
- Otherwise process groups sequentially.

Chat path:
- Spawn one `runSubagent` call per service group.
- Merge by claim ID; tier precedence resolves conflicts.

### Pattern C: Hybrid parallelism

Use when deep-checking multiple articles.
- Top level: article-level dispatch
- Inside each article: service-area fan-out

If runtime limits nested parallelism, keep top-level article dispatch and run service groups sequentially inside each article.

## Output guarantees

Regardless of runtime:
1. Per-article report names are deterministic and non-colliding.
2. Consolidated report is produced for batch workflows.
3. Status taxonomy remains identical across runtimes: `accurate`, `partial`, `inaccurate`, `outdated`, `unverifiable`, `broken`.
4. Source citation shape remains identical: URL plus tier.

## Failure handling

If a parallel unit fails:
1. Record the failed unit in the consolidated report.
2. Continue remaining units.
3. Mark the failed unit as `unverifiable` only for claims that could not be checked.

## Capability note for test protocols

T3.1 validates CLI `/fleet` dispatch.
T3.3 validates Chat `runSubagent` dispatch with equivalent outputs.

# Runtime Validation Matrix

**Date**: 2026-04-02
**Requested sequence**: 1 then 2 then 3

## Step 1: Runtime parity run

| Item | Result | Evidence |
|------|--------|----------|
| 1A: CLI fleet run (T3.1 style) | Blocked | `copilot --help` indicated GitHub Copilot CLI is not installed in this environment. |
| 1B: Chat runSubagent run (T3.3 style) | Passed | Two article-level subagent units executed and produced per-article + consolidated reports. |

Artifacts:
1. test_runs/factcheck_load-balancer-custom-probe-overview_20260402.md
2. test_runs/factcheck_manage-probes-how-to_20260402.md
3. test_runs/factcheck_batch_20260402.md

## Step 2: W12 and W14 validation runs

| Item | Result | Evidence |
|------|--------|----------|
| W12 fan-out verify run | Passed | Fan-out simulation dispatched 2 service-group subagents and produced detailed report. |
| W14 incremental cold/warm run | Passed with note | Cold pass verified all claims; warm pass skipped most claims and estimated 83.33% time savings; 2 newly surfaced claims were verified in warm run. |

Artifacts:
1. test_runs/factcheck_w12_load-balancer-custom-probe-overview_20260402.md
2. test_runs/factcheck_w14_incremental_manage-probes-how-to_20260402.md
3. .factcheck_cache/manage-probes-how-to.json

## Step 3: Consolidated assessment

| Dimension | Status |
|----------|--------|
| Chat-mode runSubagent readiness | Ready |
| Fleet CLI readiness | Not validated in this environment (tooling missing) |
| Output parity format (chat mode) | Verified for per-article + consolidated artifacts |
| Shared runtime/subagent doc changes | Implemented |

## Recommendation

Install GitHub Copilot CLI and run T3.1/T3.2 directly to close the only remaining validation gap.

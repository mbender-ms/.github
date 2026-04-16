# W12 Fan-Out Verify Run

**File**: copilot/skills/doc-verifier/fixtures/articles/load-balancer/load-balancer-custom-probe-overview.md
**Date**: 2026-04-02
**Mode**: Chat runSubagent (fan-out simulation)

## Execution summary

- Total claims: 44
- Subagents dispatched: 2
- Service groups:
  - Azure Load Balancer
  - Azure Virtual Network (probe source IP/NSG context)
- Sources consulted: 5

## Findings at a glance

| Status | Count |
|--------|-------|
| ✅ Accurate | 41 |
| ⚠️ Partial | 2 |
| ❌ Inaccurate | 0 |
| 🕐 Outdated | 1 |
| ❓ Unverifiable | 0 |
| 🔗 Broken link | 0 |

## Critical findings

1. C006 🕐 Basic Load Balancer is presented as current without retirement context.
Source: https://learn.microsoft.com/azure/load-balancer/skus

2. C029 ⚠️ Standard vs Basic framing is technically legacy-correct but incomplete post-retirement.
Source: https://learn.microsoft.com/azure/load-balancer/load-balancer-overview

3. C041 ⚠️ Basic-SKU references should be explicitly scoped as retired behavior.
Source: https://learn.microsoft.com/azure/load-balancer/load-balancer-overview

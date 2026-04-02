# Fact-Check Report: Azure Load Balancer health probes

**File**: copilot/skills/doc-verifier/fixtures/articles/load-balancer/load-balancer-custom-probe-overview.md
**Date**: 2026-04-02
**Service area**: Azure Load Balancer
**Claims checked**: 10

## Findings at a glance

| Status | Count |
|--------|-------|
| ✅ Accurate | 6 |
| ⚠️ Partial | 0 |
| ❌ Inaccurate | 0 |
| 🕐 Outdated | 2 |
| ❓ Unverifiable | 2 |
| 🔗 Broken link | 0 |

## Top findings

1. 🕐 Basic SKU probe behavior is presented without retirement context.
Source: https://learn.microsoft.com/azure/load-balancer/skus

2. ❓ IPv6 probe source literal address could not be corroborated independently in separate references reviewed.
Source: https://learn.microsoft.com/azure/load-balancer/load-balancer-custom-probe-overview#probe-source-ip-address

3. 🕐 Basic SKU + VMSS probe guidance appears legacy after Basic retirement and should be explicitly scoped.
Source: https://learn.microsoft.com/azure/load-balancer/load-balancer-faqs#what-is-ip-1686312916

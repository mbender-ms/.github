# Fact-Check Report: Manage health probes for Azure Load Balancer using the Azure portal

**File**: copilot/skills/doc-verifier/fixtures/articles/load-balancer/manage-probes-how-to.md
**Date**: 2026-04-02
**Service area**: Azure Load Balancer
**Claims checked**: 6

## Findings at a glance

| Status | Count |
|--------|-------|
| ✅ Accurate | 3 |
| ⚠️ Partial | 1 |
| ❌ Inaccurate | 1 |
| 🕐 Outdated | 1 |
| ❓ Unverifiable | 0 |
| 🔗 Broken link | 0 |

## Top findings

1. ❌ Statement that `Path` applies only to HTTPS probes is incorrect.
Source: https://learn.microsoft.com/azure/load-balancer/load-balancer-custom-probe-overview#probe-protocol

2. ⚠️ Probe origin statement needs scope context (IPv4/IPv6 behavior distinctions).
Source: https://learn.microsoft.com/azure/load-balancer/load-balancer-custom-probe-overview#probe-source-ip-address

3. 🕐 Basic SKU is presented without retirement context.
Source: https://learn.microsoft.com/azure/load-balancer/skus

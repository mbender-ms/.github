# W14 Incremental Verify Run

**File**: copilot/skills/doc-verifier/fixtures/articles/load-balancer/manage-probes-how-to.md
**Date**: 2026-04-02
**Staleness threshold**: 30 days

## Cold-cache pass

| Metric | Value |
|--------|-------|
| Total claims | 10 |
| Skipped | 0 |
| Re-verified stale | 0 |
| Re-verified changed | 0 |
| Newly verified | 10 |

Cache created: .factcheck_cache/manage-probes-how-to.json

## Warm-cache pass (unchanged article)

| Metric | Value |
|--------|-------|
| Total claims | 12 |
| Skipped | 10 |
| Re-verified stale | 0 |
| Re-verified changed | 0 |
| Newly verified | 2 |
| Removed from cache | 0 |
| Estimated time saved | 83.33% |

## Notes

- Warm pass indicates substantial skip behavior consistent with incremental expectations.
- Two additional claims were surfaced in warm-pass extraction and marked newly verified.

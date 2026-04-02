# Runtime Validation Rerun

**Date**: 2026-04-02

## CLI fleet path

Status: Blocked by authentication.

Evidence:
- `copilot` is installed and functional.
- Non-interactive prompt execution returned: `Error: No authentication information found.`
- No supported token env vars were present.
- `gh` is not installed, so GitHub CLI auth cannot be reused.

## Chat runSubagent path

Status: Passed.

Evidence:
- Article-level rerun completed for F1 and F2.
- Batch-style consolidated report generated.
- W12 rerun generated service-group fan-out results.
- W14 rerun showed cold-cache full verification and warm-cache skip behavior.

## T5 script rerun

| Test | Result | Notes |
|------|--------|-------|
| T5.2 empty manifest | Failed | Non-zero exit without intended friendly error message |
| T5.1 normal-cased header | Failed | 0 queries, no claims extracted |
| T5.1 lowercase header workaround | Passed | 2 queries, JSON cache populated |

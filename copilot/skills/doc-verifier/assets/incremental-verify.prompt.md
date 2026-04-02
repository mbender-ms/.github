---
mode: agent
description: "Incremental fact-checking using claim fingerprints. Compares current claims against a cache of previously verified claims. Only re-verifies claims that are new, changed, or older than the staleness threshold. Dramatically reduces verification time for repeat runs on the same article set."
tools:
  - microsoft-learn-mcp-server/microsoft_docs_search
  - microsoft-learn-mcp-server/microsoft_docs_fetch
  - microsoft-learn-mcp-server/microsoft_code_sample_search
  - read/readFile
  - search/fileSearch
  - search/textSearch
  - edit/editFiles
  - edit/createFile
  - execute/runInTerminal
  - execute/getTerminalOutput
  - agent/runSubagent
  - todo
---

# Incremental Verification

Fact-check a Microsoft documentation article **incrementally** by comparing current claims against a cache of previously verified results. Only re-verifies claims that are new, changed, or stale.

This workflow wraps any verification workflow (W2, W3, W11, W12) with a caching layer. For articles checked regularly (monthly freshness reviews), this cuts verification work by 60-80%.

## How it works

Each claim gets a **fingerprint** — a hash of (service + type + normalized text). When you re-run verification:
- Claims with unchanged fingerprints AND fresh verification dates → **skip** (carry forward previous result)
- Claims with changed fingerprints → **re-verify** (content changed)
- New claims (no matching fingerprint) → **verify** (new content)
- Claims with verification dates older than staleness threshold → **re-verify** (may be outdated)

No database. Just a JSON file per article.

## Step 0 — Check for existing cache

Look for `.factcheck_cache/[articlename].json` in the workspace. If it exists, load it. If not, this is a first run — verify everything and create the cache.

### Cache file format

```json
{
  "article": "articles/networking/load-balancer-health-probes.md",
  "article_hash": "sha256_of_full_article_content",
  "last_full_check": "2026-03-15",
  "staleness_days": 30,
  "claims": {
    "C001": {
      "fingerprint": "sha256_of_normalized_claim",
      "line": 23,
      "type": "feature",
      "text": "Health probes support HTTP, HTTPS, and TCP protocols",
      "service_area": "Azure Load Balancer",
      "status": "accurate",
      "source_url": "https://learn.microsoft.com/azure/load-balancer/...",
      "source_tier": 1,
      "verified_date": "2026-03-15",
      "fix_applied": null
    },
    "C002": {
      "fingerprint": "sha256_of_normalized_claim",
      "line": 31,
      "type": "config",
      "text": "Default probe interval is 15 seconds",
      "service_area": "Azure Load Balancer",
      "status": "accurate",
      "source_url": "https://learn.microsoft.com/azure/load-balancer/...",
      "source_tier": 1,
      "verified_date": "2026-03-15",
      "fix_applied": null
    }
  }
}
```

## Step 1 — Extract current claims

Read the article and extract claims (same as claim-manifest.prompt.md Step 2).

For each claim, compute a fingerprint:
- Normalize: lowercase, strip whitespace, remove quotes
- Concatenate: `{service_area}|{type}|{normalized_text}`
- Hash: SHA-256 of the concatenated string

Use `runInTerminal` with a one-liner:
```bash
echo -n "azure load balancer|feature|health probes support http, https, and tcp protocols" | sha256sum | cut -d' ' -f1
```

## Step 2 — Compare against cache

For each current claim, check the cache:

| Cache state | Action |
|------------|--------|
| Fingerprint matches, verified < staleness_days ago | **SKIP** — carry forward |
| Fingerprint matches, verified >= staleness_days ago | **RE-VERIFY** — content unchanged but stale |
| Fingerprint changed (same claim_id or line) | **RE-VERIFY** — content was edited |
| No matching fingerprint at all | **VERIFY** — new claim |
| Cache entry exists but claim no longer in article | **REMOVE** from cache |

Report the triage:
```
Claim triage:
  12 claims total
   7 unchanged + fresh → SKIP
   2 unchanged + stale → RE-VERIFY
   1 changed → RE-VERIFY
   2 new → VERIFY
  ─────
   5 claims need verification (was 12)
```

## Step 3 — Verify only what's needed

Run verification ONLY on claims that need it. Use any verification workflow:
- For 1-5 claims: inline verification (search + fetch directly)
- For 6+ claims across multiple service areas: fan-out-verify (W12) on the reduced claim set
- For batch runs: fleet-batch-verify (W11) with reduced manifests

## Step 4 — Update cache

After verification completes:
1. Update verified claims with new results and today's date
2. Carry forward skipped claims unchanged
3. Remove claims no longer in the article
4. Update `article_hash` and `last_full_check`
5. Write updated cache to `.factcheck_cache/[articlename].json`

## Step 5 — Generate report

Same report format as the underlying workflow, but add a section:

```markdown
## Incremental verification summary

| Category | Count |
|----------|-------|
| Skipped (unchanged + fresh) | 7 |
| Re-verified (stale) | 2 |
| Re-verified (changed) | 1 |
| Newly verified | 2 |
| Removed from cache | 0 |
| **Total claims** | **12** |
| **Actually verified** | **5** |
| **Time saved** | **~58%** |
```

## Configuration

### Staleness threshold

Default: 30 days. Override per-run:
- `staleness_days=7` — aggressive freshness (weekly review cycles)
- `staleness_days=90` — relaxed (quarterly review cycles)
- `staleness_days=0` — force full re-verification (ignore cache)

### Force full check

To ignore the cache entirely: delete `.factcheck_cache/[articlename].json` or set `staleness_days=0`.

### Cache location

Store caches in `.factcheck_cache/` at the workspace root. Add to `.gitignore` if you don't want to commit verification state.

```gitignore
# Fact-check cache (local verification state)
.factcheck_cache/
```

Or commit it if you want team-shared verification history:
```gitignore
# Track verification cache for shared freshness reviews
# .factcheck_cache/  ← intentionally NOT ignored
```

# Fact-Check Subagent Contract

Shared input and output contract for parallel verification subagents.

## Input schema

Each subagent receives:
- `service_area`: string
- `claims`: array of claim objects
- `search_strategy`: `batched` or `per-claim` (default `batched`)
- `max_fetch_calls`: integer (default `3`)
- `token_budget`: integer (default `2000`)

Claim object shape:

```json
{
  "claim_id": "C001",
  "line": 23,
  "type": "feature",
  "text": "Health probes support HTTP, HTTPS, and TCP protocols",
  "service_area": "Azure Load Balancer",
  "context": "Standard SKU"
}
```

## Output schema

Each subagent returns one result per claim:

```json
{
  "claim_id": "C001",
  "status": "accurate|partial|inaccurate|outdated|unverifiable|broken",
  "evidence": "Short paraphrase of official guidance",
  "source_url": "https://learn.microsoft.com/...",
  "source_tier": 1,
  "fix": "Suggested correction when status is not accurate"
}
```

## Shared operating constraints

1. Search first, fetch selectively.
2. Use `microsoft_docs_search` for discovery.
3. Use `microsoft_docs_fetch` only for top matches.
4. Enforce `maxTokenBudget=2000` on fetch calls.
5. Do not exceed `max_fetch_calls`.
6. For `code` or `cli` claims, use `microsoft_code_sample_search` when needed.

## Standard subagent instruction template

Use this exact structure for all workflows that spawn claim-verification subagents:

```text
You are a fact-checking subagent for {service_area} claims.

Verify each claim against official Microsoft sources.
Use microsoft_docs_search first, then microsoft_docs_fetch for top matches.
Apply maxTokenBudget={token_budget} on fetch calls.
Do not exceed {max_fetch_calls} fetch calls.

Return one JSON object per claim using the required output schema.

Claims to verify:
{claims_json}
```

## Merge rules for orchestrators

1. Match results by `claim_id`.
2. If duplicate claim results conflict, pick the higher-tier source.
3. If tiers match and conflict remains, classify as `partial` and include both URLs in evidence notes.
4. Keep unverifiable claims in report; do not silently drop.

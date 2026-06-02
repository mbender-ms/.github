# Fact-Check Subagent Contract

Shared input and output contract for parallel verification subagents.

## Input schema

Each subagent receives:
- `service_area`: string
- `claims`: array of claim objects
- `search_strategy`: `batched` or `per-claim` (default `batched`)
- `max_fetch_calls`: integer (default `3`) — shared budget for low-risk claims
- `high_risk_fetch_calls`: integer (default `1 per high-risk claim`) — dedicated budget so numeric/limit/version/status claims always get an authoritative fetch
- `token_budget`: integer (default `2000`)

## Claim risk classes

Depth is driven by claim class, not a global quick/thorough toggle. Spend the fetch budget where defects concentrate.

| Risk | Claim types | Required depth |
|------|-------------|----------------|
| **High** | `limit`, `config`, `pricing`, `status`, `prereq`, and any `feature` stating a number, version, date, or lifecycle state | **Mandatory authoritative fetch.** Search alone can never yield `accurate`. Must capture `verified_value` from a fetched Tier-1/2 page. |
| **Low** | prose `feature`, `cli`, `code`, `link` | Search-only is acceptable; fetch only on an apparent discrepancy. |

High-risk claims carry a non-`—` `topic_key` and feed cross-track reconciliation.

Claim object shape:

```json
{
  "claim_id": "C001",
  "line": 23,
  "type": "feature",
  "topic_key": "loadbalancer-probe-protocols",
  "text": "Health probes support HTTP, HTTPS, and TCP protocols",
  "service_area": "Azure Load Balancer",
  "context": "Standard SKU"
}
```

`topic_key` is the cross-article correlation slug coined in the claim manifest. It names the *fact*, not the value, and is identical for the same fact across every file in the batch. Subagents MUST echo it back unchanged so the orchestrator can group results across tracks. A value of `—` means the claim is not subject to cross-article reconciliation.

## Output schema

Each subagent returns one result per claim:

```json
{
  "claim_id": "C001",
  "topic_key": "loadbalancer-probe-protocols",
  "status": "accurate|partial|inaccurate|outdated|unverifiable|broken",
  "verified_value": "4 to 120 minutes",
  "verification_method": "search|fetch|code-sample",
  "confidence": "high|medium|low",
  "evidence": "Short paraphrase of official guidance",
  "source_url": "https://learn.microsoft.com/...",
  "source_tier": 1,
  "fix": "Suggested correction when status is not accurate"
}
```

`topic_key` is echoed back from the input unchanged. `verified_value` is the normalized fact the authoritative source states (a number, range, version, date, or lifecycle state) — the orchestrator compares this field across tracks that share a `topic_key`. For prose claims with no discrete value, set `verified_value` to a short canonical phrase. `verification_method` records how the verdict was reached, and `confidence` reflects source strength and agreement.

## Shared operating constraints

1. Search first, fetch selectively.
2. Use `microsoft_docs_search` for discovery.
3. Use `microsoft_docs_fetch` only for top matches.
4. Enforce `maxTokenBudget=2000` on fetch calls.
5. Do not exceed the budget: low-risk claims share `max_fetch_calls`; each high-risk claim has its own `high_risk_fetch_calls` allowance so it is never starved by prose claims.
6. For `code` or `cli` claims, use `microsoft_code_sample_search` when needed.

## Accurate-verdict gate

A claim may be scored `accurate` **only** when all of the following hold. Otherwise it is `unverifiable` (or the appropriate non-accurate status) — never default a plausible-but-unchecked claim to `accurate`.

- `source_tier ≤ 2`, and
- for **high-risk** claims, `verification_method` is `fetch` (or `code-sample`) and `verified_value` matches the article text. A search snippet is not sufficient evidence for a high-risk `accurate`.
- low-risk claims may be `accurate` via `search` when the snippet is unambiguous; set `confidence: medium`.

If no Tier-1/2 source is found, return `unverifiable` and keep the claim in the report — do not drop or guess.

## Standard subagent instruction template

Use this exact structure for all workflows that spawn claim-verification subagents:

```text
You are a fact-checking subagent for {service_area} claims.

Verify each claim against official Microsoft sources.
Use microsoft_docs_search first, then microsoft_docs_fetch for top matches.
Apply maxTokenBudget={token_budget} on fetch calls.
Low-risk claims share {max_fetch_calls} fetch calls; each high-risk claim
(limit, config, pricing, status, prereq, or any feature stating a number,
version, date, or lifecycle state) gets its own fetch and MUST be confirmed
against a fetched Tier-1/2 page — a search snippet alone cannot make a
high-risk claim "accurate". Capture that page's value in `verified_value`,
set `verification_method` and `confidence`, and echo each claim's `topic_key`
back unchanged so the orchestrator can reconcile the same fact across articles.
If no Tier-1/2 source confirms a claim, return "unverifiable" — never default
an unchecked claim to "accurate".

Return one JSON object per claim using the required output schema.

Claims to verify:
{claims_json}
```

## Merge rules for orchestrators

1. Match results by `claim_id`.
2. If duplicate claim results conflict, pick the higher-tier source.
3. If tiers match and conflict remains, classify as `partial` and include both URLs in evidence notes.
4. Keep unverifiable claims in report; do not silently drop.

## Cross-track reconciliation (shared claim ledger)

After all tracks return, the orchestrator MUST run a reconciliation pass before writing the consolidated report. This is what catches cross-article inconsistencies that no single isolated track can see.

1. **Group** every returned result by `topic_key`, ignoring groups where `topic_key` is `—` and singletons (a key that appears in only one file).
2. **Compare `verified_value`** within each multi-file group:
   - All values agree and at least one is fetch-verified (`source_tier ≤ 2`) → the group is consistent. Propagate the authoritative value to any track that marked the claim `unverifiable`.
   - Values disagree → raise a **conflict**. The correct value is the one backed by the highest-tier source; every file whose text states a different value is `inaccurate` (or `outdated` if it was historically correct), regardless of how the owning track originally scored it. A track's local ✅ does **not** override a cross-track conflict.
   - No value in the group is fetch-verified → mark the whole group `unverifiable` and flag for a deep pass; do not let mutual agreement between unverified snippets count as accurate.
3. **Emit a reconciliation table** in the consolidated report listing every conflicted `topic_key`, the value each file asserts, the authoritative value, and the source. These are the highest-value findings in the batch — list them first.

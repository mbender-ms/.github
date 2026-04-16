# Test Protocols — Parallel Verification Workflows

Structured test procedures for validating that workflows W11–W14 and the `batch-presearch.sh` script produce trusted, repeatable results.

Each test has a **fixture** (what to run against), **procedure** (exact steps), **pass criteria** (what "working" looks like), and **known-good reference** (how to verify the agent's findings independently).

---

## Test fixture articles

Use real articles from the [MicrosoftDocs/azure-docs](https://github.com/MicrosoftDocs/azure-docs) repo. Clone locally or use the raw GitHub paths.

| ID | Article | Why this is a good test fixture |
|----|---------|-------------------------------|
| **F1** | `articles/load-balancer/load-balancer-custom-probe-overview.md` | Dense with feature/config/limit claims. Well-documented service — easy to verify findings manually. |
| **F2** | `articles/load-balancer/manage-probes-how-to.md` | How-to with portal steps, CLI commands, and prerequisites. Good for UI verb and procedural accuracy. |
| **F3** | `articles/virtual-network/virtual-network-peering-overview.md` | Concept article. Cross-service claims (VNet + region + subscription). Tests service-area grouping. |
| **F4** | `articles/app-service/overview.md` | Overview article. Broad feature claims, pricing tiers, limits. Tests claim density extraction. |
| **F5** | `articles/cosmos-db/introduction.md` | Different service area entirely. Tests that batch workflows handle mixed service groups. |

> **Tip**: Pick articles with `ms.date` older than 6 months — these are more likely to contain outdated claims, giving the agent real work to do.

---

## T1 — Claim manifest extractor (W13)

**Goal**: Verify that `claim-manifest.prompt.md` accurately extracts and categorizes claims without making any MCP calls.

### T1.1 — Basic extraction accuracy

**Fixture**: F1 (`load-balancer-custom-probe-overview.md`)

**Procedure**:
1. Open the article in VS Code
2. Run: `Use @claim-manifest to extract all verifiable claims from this article`
3. Wait for manifest output

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Claim count | ≥ 15 claims extracted (this article is dense) |
| Claim types present | At least 3 different types (feature, config, limit expected) |
| Service area grouping | Primary group is "Azure Load Balancer" |
| Line numbers | Each claim has a line number that maps to the actual article |
| No MCP calls | Zero tool calls to `microsoft_docs_search`, `microsoft_docs_fetch`, or `microsoft_code_sample_search` |
| Include resolution | If article has `[!INCLUDE ...]`, those files are read and claims extracted |
| Output file | `claims_load-balancer-custom-probe-overview_YYYYMMDD.md` created |

**Manual verification**: Open the article side-by-side with the manifest. Spot-check 5 random claims — confirm the quoted text exists at the stated line number and the type classification is reasonable.

### T1.2 — Non-claim filtering

**Fixture**: F2 (`manage-probes-how-to.md`)

**Procedure**: Same as T1.1.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Navigation text excluded | "In this article, you learn how to..." is NOT a claim |
| Subjective guidance excluded | "We recommend..." is NOT a claim |
| Portal steps extracted | "Select **Health probes** in Settings" → extracted as a `feature` or `prereq` claim about the portal path |
| CLI commands extracted | Any `az network lb probe` commands → extracted as `cli` type |

### T1.3 — Cross-service article

**Fixture**: F3 (`virtual-network-peering-overview.md`)

**Procedure**: Same as T1.1.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Multiple service groups | At minimum "Azure Virtual Network" group; may also have "Cross-service" for region/subscription claims |
| Claim density summary | Chat output includes estimated verification effort |

---

## T2 — Fan-out verification (W12)

**Goal**: Verify that `fan-out-verify.prompt.md` correctly executes the 3-phase fan-out/fan-in pattern with parallel subagents.

### T2.1 — Full single-article verification

**Fixture**: F1 (`load-balancer-custom-probe-overview.md`)

**Procedure**:
1. Open the article in VS Code agent mode
2. Run: `Use @fan-out-verify for a thorough fact-check of this article`
3. Observe the execution (takes 5-15 minutes)

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Phase 1 visible | Agent reads the article and produces a claim manifest before any MCP calls |
| Subagent spawn | At least 1 `runSubagent` call visible in the chat (collapsible tool call) |
| MCP calls per subagent | Each subagent makes ≤ 3 `microsoft_docs_fetch` calls |
| Token budget | Fetch calls include `maxTokenBudget` parameter (check in tool call details) |
| Classification | Every claim gets one of the 6 status icons (✅⚠️❌🕐❓🔗) |
| Report file | `factcheck_load-balancer-custom-probe-overview_YYYYMMDD.md` created |
| Report structure | Contains: executive summary, findings at a glance table, per-finding details with source URLs, sources consulted table |
| `ms.date` updated | If any edits were made, `ms.date` in frontmatter was updated |

**Manual verification**: Pick the 3 claims marked ❌ or ⚠️ (if any). Open the source URL cited by the agent. Confirm the agent's finding is correct — the official docs actually say what the agent claims they say.

### T2.2 — Seeded error detection

**Fixture**: Create a modified copy of F1 with 3 deliberate errors:

```markdown
<!-- Error 1: Wrong default value -->
The health probe attempts to check the configured health probe port every 10 seconds by default.
(Actual: 5 seconds)

<!-- Error 2: Wrong protocol list -->
Health probes support HTTP and TCP protocols.
(Missing: HTTPS)

<!-- Error 3: Outdated claim -->
Basic Load Balancer is the recommended SKU for production workloads.
(Actual: Standard is recommended; Basic is being deprecated)
```

**Procedure**: Run fan-out-verify on the modified article.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Error 1 caught | Marked ❌ or 🕐, corrected to "5 seconds" |
| Error 2 caught | Marked ⚠️ or ❌, corrected to include HTTPS |
| Error 3 caught | Marked ❌ or 🕐, corrected with note about Standard SKU |
| Detection rate | ≥ 2 of 3 seeded errors detected (67%+ minimum, target 100%) |
| False positive rate | ≤ 2 false ❌ classifications on claims that are actually correct |

> **This is the trust test.** If the agent catches all 3 seeded errors with correct source citations, and doesn't falsely flag more than 2 correct claims, the workflow is trustworthy for production use.

### T2.3 — Include file handling

**Fixture**: An article that uses `[!INCLUDE [clean-up-resources](~/reusable-content/...)]` or similar includes.

**Procedure**: Run fan-out-verify.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Include detected | Chat output mentions the include file |
| Include claims extracted | If the include contains verifiable claims, they appear in the manifest |
| Include edits | If an error is in the include file, the agent edits the include file (not the main article) and notes this in the report |

---

## T3 — Fleet batch verification (W11)

**Goal**: Verify that `fleet-batch-verify.prompt.md` correctly parallelizes across multiple articles and produces both per-article and consolidated reports.

### T3.1 — Two-article parallel run

**Fixture**: F1 + F2 (both Load Balancer articles — same service area)

**Procedure** (Copilot CLI):
```
/fleet Fact-check these 2 articles using @fleet-batch-verify:
1. articles/load-balancer/load-balancer-custom-probe-overview.md
2. articles/load-balancer/manage-probes-how-to.md
```

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Parallel execution | `/tasks` shows 2+ background tasks running simultaneously |
| Per-article reports | 2 separate `factcheck_*.md` files created |
| Consolidated report | `factcheck_batch_YYYYMMDD.md` created |
| Cross-article patterns | Consolidated report notes any shared issues (e.g., both articles reference the same deprecated feature) |
| No file conflicts | Reports don't overwrite each other (each has the article name in the filename) |

### T3.2 — Cross-service batch run

**Fixture**: F1 + F4 + F5 (Load Balancer + App Service + Cosmos DB — 3 different service areas)

**Procedure** (Copilot CLI):
```
/fleet Fact-check these 3 articles using @fleet-batch-verify:
1. articles/load-balancer/load-balancer-custom-probe-overview.md
2. articles/app-service/overview.md
3. articles/cosmos-db/introduction.md
```

**Pass criteria**:

| Check | Expected |
|-------|----------|
| 3 tracks decomposed | Orchestrator shows 3 independent work items |
| Service isolation | Each track's MCP searches are scoped to its service area (LB searches don't leak into Cosmos DB track) |
| 3 per-article reports | Each with correct service area metadata |
| Consolidated report | Includes per-file summary table with all 3 articles |
| Runtime | Completes faster than 3x the single-article time (parallelism working) |

### T3.3 — VS Code agent mode (runSubagent)

**Fixture**: F1 + F2

**Procedure** (VS Code, NOT Copilot CLI):
```
Use @fleet-batch-verify to fact-check these 2 articles:
1. articles/load-balancer/load-balancer-custom-probe-overview.md
2. articles/load-balancer/manage-probes-how-to.md
```

**Pass criteria**:

| Check | Expected |
|-------|----------|
| runSubagent dispatch | Agent uses `runSubagent` units for article-level work items when parallel tools are available |
| Same output format | Per-article + consolidated reports still generated |
| No errors from /fleet syntax | Agent adapts to the runtime environment |

### T3.4 — PR triage threshold enforcement (W8)

**Goal**: Verify that `pr-review.prompt.md` executes Step 1.5 triage, selects the correct tier route, and escalates only when triggers are present.

**Fixture**:
- PR A: 2 changed docs, editorial/metadata only (low risk)
- PR B: 7 changed docs with at least one security or retirement claim (high risk)

**Procedure**:
1. Run W8 on PR A: `Use @pr-review to fact-check PR #<low-risk-pr>`
2. Confirm triage output includes file count, estimated claim density band, and risk classification.
3. Run W8 on PR B: `Use @pr-review to fact-check PR #<high-risk-pr>`
4. Confirm triage output includes high-risk flags and escalated routing for flagged files.
5. In both runs, inspect report notes for escalation triggers and final tier decisions.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Step 1.5 evidence | Output explicitly shows triage checklist fields were evaluated |
| Low-risk routing (PR A) | Uses Tier 2 or Tier 3 first, no blanket Tier 1 across all files |
| High-risk routing (PR B) | Applies Tier 1 adjudication to flagged files or contested claims |
| Trigger fidelity | Escalations are tied to listed triggers (source conflict, unverifiable rate, safety impact, confidence drop, policy/retirement risk) |
| Over-escalation control | No escalation to Tier 1 for purely editorial findings without trigger |
| Report traceability | Final report includes the triage decision rationale |

**Manual verification**:
- For one escalated claim in PR B, open cited sources and confirm a genuine trigger existed.
- For one non-escalated editorial claim in PR A, confirm no trigger condition was present.

---

## Runtime compatibility matrix (W11-W14)

Use this matrix to validate cross-runtime parity quickly before full protocol runs.

| Workflow | Copilot CLI (`/fleet`) | Copilot Chat (`runSubagent`) | Expected artifacts |
|----------|-------------------------|------------------------------|-------------------|
| W11 Fleet Batch | ✅ Preferred dispatch | ✅ Equivalent dispatch | Per-article `factcheck_*.md` + `factcheck_batch_YYYYMMDD.md` |
| W12 Fan-Out Verify | ✅ Supported | ✅ Preferred for interactive deep checks | Single detailed `factcheck_[article]_YYYYMMDD.md` |
| W13 Claim Manifest | ✅ Supported | ✅ Supported | `claims_[article]_YYYYMMDD.md` |
| W14 Incremental Verify | ✅ Supported | ✅ Supported | Incremental report + `.factcheck_cache/[article].json` |

Quick parity checks:
1. Same status taxonomy appears in reports (✅⚠️❌🕐❓🔗).
2. Same source citation fields appear in findings.
3. Report filenames are deterministic and non-colliding.
4. Batch workflows always produce consolidated output.

---

## T4 — Incremental verification (W14)

**Goal**: Verify that `incremental-verify.prompt.md` correctly caches results, skips unchanged claims, and re-verifies only what's needed.

### T4.1 — First run (cold cache)

**Fixture**: F2 (`manage-probes-how-to.md`)

**Procedure**:
1. Ensure `.factcheck_cache/manage-probes-how-to.json` does NOT exist
2. Run: `Use @incremental-verify on this article. Staleness threshold: 30 days.`

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Full verification | All claims verified (no skips on first run) |
| Cache created | `.factcheck_cache/manage-probes-how-to.json` created |
| Cache structure | JSON contains: `article`, `article_hash`, `last_full_check`, `claims` object with fingerprints |
| Report includes | "Incremental verification summary" section showing 0 skipped, N newly verified |

### T4.2 — Second run (warm cache, no changes)

**Fixture**: Same F2 article, unchanged. Run immediately after T4.1.

**Procedure**:
1. Confirm `.factcheck_cache/manage-probes-how-to.json` exists from T4.1
2. Run: `Use @incremental-verify on this article. Staleness threshold: 30 days.`

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Claims skipped | Most or all claims show "SKIP — unchanged + fresh" |
| Minimal MCP calls | Significantly fewer `microsoft_docs_search` calls than T4.1 |
| Cache updated | `last_full_check` date updated, but claim entries unchanged |
| Report includes | Summary showing N skipped, 0 re-verified (or close to it) |
| Time savings | Report shows "Time saved: ~XX%" |

### T4.3 — Third run (warm cache, article modified)

**Fixture**: Edit F2 — change one claim (e.g., alter a port number or protocol name).

**Procedure**:
1. Make a small edit to the article (change one verifiable fact)
2. Run: `Use @incremental-verify on this article. Staleness threshold: 30 days.`

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Changed claim detected | The modified claim shows "RE-VERIFY — changed" |
| Unchanged claims skipped | All other claims show "SKIP" |
| New verification | Only the changed claim triggers MCP calls |
| Cache updated | Changed claim's fingerprint and verified_date updated |

### T4.4 — Staleness threshold test

**Fixture**: F2 with an existing cache where `verified_date` is older than threshold.

**Procedure**:
1. Manually edit `.factcheck_cache/manage-probes-how-to.json` — set all `verified_date` values to 60 days ago
2. Run: `Use @incremental-verify on this article. Staleness threshold: 30 days.`

**Pass criteria**:

| Check | Expected |
|-------|----------|
| All claims stale | Every claim shows "RE-VERIFY — stale" |
| Full verification | All claims re-verified against current docs |
| Cache refreshed | All `verified_date` entries updated to today |

---

## T5 — Batch presearch script

**Goal**: Verify that `batch-presearch.sh` correctly extracts queries from a manifest and produces usable JSON cache files.

### T5.1 — Basic execution

**Prerequisites**: `npm install -g @microsoft/learn-cli`

**Procedure**:
1. Generate a manifest first: run T1.1 to get `claims_load-balancer-custom-probe-overview_YYYYMMDD.md`
2. Run:
```bash
./scripts/batch-presearch.sh claims_load-balancer-custom-probe-overview_YYYYMMDD.md ./test_cache/
```

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Exit code | 0 (no errors) |
| Output directory | `./test_cache/` created |
| JSON files | At least 1 `search_*.json` file per service-area group |
| JSON structure | Each file contains `service_area`, `date`, `results` array |
| Results populated | Each query has a `response` object with search results (titles, URLs) |
| Console summary | Shows total queries and total results counts |

### T5.2 — Empty manifest handling

**Procedure**: Create a minimal manifest with no claim tables:
```markdown
# Claim Manifest: Test
**Total claims**: 0
```
Run the script against it.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Graceful exit | Script prints "No service area groups found" and exits with non-zero code |
| No empty files | No JSON files created |

### T5.3 — Rate limiting

**Procedure**: Run T5.1 and observe timing.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Delay between queries | At least 500ms between consecutive `learn-cli` calls (check timestamps) |
| No 429 errors | No rate-limit errors in output |

---

## T6 — Integration tests (end-to-end pipelines)

### T6.1 — Manifest → Fan-out pipeline

**Fixture**: F1

**Procedure**:
1. Run claim-manifest (W13) → produces manifest file
2. Review manifest, confirm claim count
3. Run fan-out-verify (W12) on the same article
4. Compare: does W12's claim manifest match W13's output?

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Claim consistency | W12 extracts the same claims (±10%) as W13 |
| Service grouping match | Same service-area groups in both |
| W12 produces richer output | W12's report has verification results that W13 doesn't |

### T6.2 — Presearch → Fleet pipeline

**Fixture**: F1 + F2

**Procedure**:
1. Run claim-manifest on both articles
2. Run `batch-presearch.sh` on both manifests
3. Run fleet-batch-verify with the articles
4. Check: do the agents reference cached search results?

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Cache files exist | Presearch created JSON files for each service area |
| Agents can read cache | If agents are instructed to check `./presearch_cache/`, they find relevant results |
| Reduced MCP calls | Fleet run makes fewer `microsoft_docs_search` calls than a run without presearch |

> **Note**: This test depends on whether the agent prompt explicitly instructs reading the cache. You may need to modify the `/fleet` prompt to include: "Check ./presearch_cache/ for pre-searched results before making live MCP calls."

### T6.3 — Incremental + Fleet combo

**Fixture**: F1 + F2, both previously verified (warm caches)

**Procedure**:
1. Ensure both articles have `.factcheck_cache/` entries from prior runs
2. Edit one claim in F1, leave F2 unchanged
3. Run fleet-batch-verify with incremental mode

**Pass criteria**:

| Check | Expected |
|-------|----------|
| F1 partial re-check | Only changed claims in F1 are re-verified |
| F2 fully skipped | F2 shows all claims as SKIP in the incremental summary |
| Total time | Significantly less than a cold-cache run on both articles |

---

## T7 — Accuracy scoring

Run this after completing T2.2 (seeded error test) on at least 3 different articles.

### Scoring method

For each test run, count:
- **True Positives (TP)**: Seeded errors correctly detected
- **False Negatives (FN)**: Seeded errors missed
- **False Positives (FP)**: Correct claims incorrectly flagged as ❌
- **True Negatives (TN)**: Correct claims correctly marked ✅

Calculate:
- **Precision** = TP / (TP + FP) — "When it flags an error, is it right?"
- **Recall** = TP / (TP + FN) — "Does it find all the errors?"
- **F1 Score** = 2 × (Precision × Recall) / (Precision + Recall)

### Target thresholds

| Metric | Minimum | Target |
|--------|---------|--------|
| Precision | 70% | 85%+ |
| Recall | 67% (2/3 seeded errors) | 90%+ |
| F1 Score | 68% | 87%+ |
| False positive rate | ≤ 3 per article | ≤ 1 per article |

> **80-90% accuracy goal**: If F1 Score is ≥ 80% across 3+ test articles, the workflow meets the stated accuracy target.

### Tracking table

| Test article | Seeded errors | TP | FN | FP | TN | Precision | Recall | F1 |
|-------------|---------------|----|----|----|----|-----------|--------|----|
| F1 (modified) | 3 | | | | | | | |
| F4 (modified) | 3 | | | | | | | |
| F5 (modified) | 3 | | | | | | | |
| **Totals** | **9** | | | | | | | |

---

## Test execution order

Run tests in this order for the most efficient validation:

1. **T1.1** — Claim manifest basic (no MCP calls, fast, validates extraction)
2. **T1.2** — Claim manifest filtering (confirms non-claims excluded)
3. **T5.1** — Presearch script (validates shell tooling)
4. **T5.2** — Presearch error handling
5. **T2.1** — Fan-out basic (first MCP-dependent test)
6. **T2.2** — Fan-out seeded errors (**the trust test**)
7. **T4.1** — Incremental cold cache
8. **T4.2** — Incremental warm cache (immediate re-run)
9. **T4.3** — Incremental with edits
10. **T3.1** — Fleet two-article parallel
11. **T3.2** — Fleet cross-service
12. **T6.1** — Manifest → Fan-out pipeline
13. **T7** — Accuracy scoring (after running T2.2 on 3+ articles)

Estimated total time: 2-3 hours for the full suite. T1 and T5 tests take < 5 minutes each. T2 and T3 tests take 10-20 minutes each.

# Test Protocols — Doc-Verifier Workflows

Structured test procedures for validating that the four doc-verifier workflows and the `batch-presearch.sh` script produce trusted, repeatable results.

Each test has a **fixture** (what to run against), **procedure** (exact steps), **pass criteria** (what "working" looks like), and **known-good reference** (how to verify the agent's findings independently).

All workflows are chat-only by default. Where a test expects report files, run the workflow with `--report <path>` so the artifacts are written.

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

## T1 — Claim manifest extractor (supporting step)

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
| `topic_key` assigned | High-risk claims (config, limit, pricing, status, prereq) each have a stable kebab-case `topic_key` |
| No MCP calls | Zero tool calls to `microsoft_docs_search`, `microsoft_docs_fetch`, or `microsoft_code_sample_search` |
| Include resolution | If article has `[!INCLUDE ...]`, those files are read and claims extracted |

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

## T2 — Single article check

**Goal**: Verify that `single-article-check.prompt.md` scopes by product area, classifies every claim, and only bumps `ms.date` on fetch-verified content.

### T2.1 — Full single-article verification

**Fixture**: F1 (`load-balancer-custom-probe-overview.md`)

**Procedure**:

1. Open the article in VS Code agent mode
2. Run: `Use @single-article-check to fact-check this article`

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Product-area scoping | Step 0 detects the product area from `ms.service`/`ms.prod` |
| Classification | Every claim gets one of the status icons (✅⚠️❌🕐❓) |
| `ms.date` discipline | `ms.date` bumped only when at least one claim was fetch-verified |
| Chat-only default | No report file written unless `--report <path>` was supplied |
| Report opt-in | With `--report <path>`, a markdown report is written to that path |

**Manual verification**: Pick the claims marked ❌ or ⚠️ (if any). Open the source URL cited by the agent. Confirm the agent's finding is correct — the official docs actually say what the agent claims they say.

### T2.2 — Seeded error detection (the trust test)

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

**Procedure**: Run `single-article-check` on the modified article.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Error 1 caught | Marked ❌ or 🕐, corrected to "5 seconds" |
| Error 2 caught | Marked ⚠️ or ❌, corrected to include HTTPS |
| Error 3 caught | Marked ❌ or 🕐, corrected with note about Standard SKU |
| Detection rate | ≥ 2 of 3 seeded errors detected (67%+ minimum, target 100%) |
| False positive rate | ≤ 2 false ❌ classifications on claims that are actually correct |

> **This is the trust test.** If the agent catches all 3 seeded errors with correct source citations, and doesn't falsely flag more than 2 correct claims, the workflow is trustworthy for production use.

---

## T3 — PR review

**Goal**: Verify that `pr-review.prompt.md` executes Step 1.5 triage, selects the correct tier route, and escalates only when triggers are present.

**Fixture**:

- PR A: 2 changed docs, editorial/metadata only (low risk)
- PR B: 7 changed docs with at least one security or retirement claim (high risk)

**Procedure**:

1. Run on PR A: `Use @pr-review to fact-check PR #<low-risk-pr>`
2. Confirm triage output includes file count, estimated claim density band, and risk classification.
3. Run on PR B: `Use @pr-review to fact-check PR #<high-risk-pr>`
4. Confirm triage output includes high-risk flags and escalated routing for flagged files.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Step 1.5 evidence | Output explicitly shows triage checklist fields were evaluated |
| Low-risk routing (PR A) | Uses Tier 2 or Tier 3 first, no blanket Tier 1 across all files |
| High-risk routing (PR B) | Applies Tier 1 adjudication to flagged files or contested claims |
| Trigger fidelity | Escalations are tied to listed triggers (source conflict, unverifiable rate, safety impact, confidence drop, policy/retirement risk) |
| Over-escalation control | No escalation to Tier 1 for purely editorial findings without trigger |
| Chat-only default | Findings presented in chat; report written only with `--report <path>` |

**Manual verification**:

- For one escalated claim in PR B, open cited sources and confirm a genuine trigger existed.
- For one non-escalated editorial claim in PR A, confirm no trigger condition was present.

---

## T4 — Fleet batch verification

**Goal**: Verify that `fleet-batch-verify.prompt.md` parallelizes across multiple articles, builds the shared `topic_key` index, and reconciles cross-article conflicts.

### T4.1 — Two-article parallel run

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
| Shared claim ledger | A batch-wide `topic_key` index is built before fan-out |
| Cross-article patterns | Consolidated findings note any shared issues (e.g., both articles reference the same deprecated feature) |
| Chat-only default | No report files unless `--report <dir>` was supplied |
| Report opt-in | With `--report <dir>`, per-article + consolidated reports are written there without colliding |

### T4.2 — Cross-service batch run

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
| Service isolation | Each track's MCP searches are scoped to its service area |
| Per-file summary | Consolidated findings include a per-file summary table with all 3 articles |
| Runtime | Completes faster than 3x the single-article time (parallelism working) |

### T4.3 — VS Code agent mode (runSubagent)

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
| Same output format | Per-article + consolidated findings still produced |
| No errors from /fleet syntax | Agent adapts to the runtime environment |

### T4.4 — Cross-article reconciliation

**Fixture**: Two articles that state the same fact with conflicting values (e.g., one says the outbound idle timeout max is 100 minutes, the other 120).

**Procedure**: Run `fleet-batch-verify` over both.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Shared `topic_key` | Both claims share the same `topic_key` |
| Conflict detected | The consolidated reconciliation table lists the conflicted `topic_key` first |
| Highest tier wins | The authoritative value cites the highest-tier source |
| Both files flagged | Every file asserting a non-authoritative value is marked inaccurate/outdated |

---

## T5 — Batch presearch script

**Goal**: Verify that `batch-presearch.sh` correctly extracts queries from a manifest and produces usable JSON cache files.

### T5.1 — Basic execution

**Prerequisites**: `npm install -g @microsoft/learn-cli`

**Procedure**:

1. Generate a manifest first: run T1.1 to get a claims manifest
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
| Console summary | Shows total queries and total results counts |

### T5.2 — Empty manifest handling

**Procedure**: Create a minimal manifest with no claim tables and run the script against it.

**Pass criteria**:

| Check | Expected |
|-------|----------|
| Graceful exit | Script prints "No service area groups found" and exits with non-zero code |
| No empty files | No JSON files created |

---

## T6 — Accuracy scoring

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
5. **T2.1** — Single article basic (first MCP-dependent test)
6. **T2.2** — Single article seeded errors (**the trust test**)
7. **T3** — PR review triage thresholds
8. **T4.1** — Fleet two-article parallel
9. **T4.2** — Fleet cross-service
10. **T4.4** — Fleet cross-article reconciliation
11. **T6** — Accuracy scoring (after running T2.2 on 3+ articles)

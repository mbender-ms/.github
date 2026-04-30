# Gap Type Definitions

Authoritative classification criteria for the three gap types used in Phase 3.

---

## new-article

**Definition:** No existing Learn article adequately covers the topic raised by the question.

**When to use:**
- `microsoft_docs_search` returns no results, or all results are from unrelated services.
- The top result covers a completely different topic (e.g., question is about Load Balancer health probes but the top result is about Application Gateway).
- The question represents a scenario that does not exist anywhere in the current doc set.

**Recommendation format:**
`Create a new article covering: {topic}`

**Scope signal:** Usually represents the highest effort — a new article may span multiple sections and require a full outline before authoring.

---

## update-article

**Definition:** A clearly relevant article exists, but its content is missing, incorrect, outdated, or incomplete for the specific question asked.

**When to use:**
- Top result article is clearly about the same service and topic as the question.
- Score is 1–2 (the model tried to answer but couldn't ground it — content is absent or wrong).
- The `generated_answer` contains hedging language like "I don't have specific information", "this is not covered", or "you may need to check the official documentation".
- The question is about a known scenario (e.g., SKU upgrade steps, feature retirement) that the article covers at a high level but not in actionable detail.

**Recommendation format:**
`Update {article title} to address: {specific missing content}`

**Scope signal:** Medium effort — content exists but needs a new section, updated steps, or corrected information.

---

## add-section

**Definition:** A relevant article exists and partially covers the topic, but is missing coverage of the specific scenario, edge case, or next step the customer is asking about.

**When to use:**
- Top result is **Partial** — covers the right service and general area but not the exact scenario.
- Top result is **Relevant** but score is 3 — something is there but it does not fully answer the question.
- The question is a logical extension of content already in the article (e.g., article covers "create" but not "delete" or "monitor").
- The `generated_answer` pulls from the article but misses a key detail or step.

**Recommendation format:**
`Add a section to {article title} covering: {specific scenario or detail}`

**Scope signal:** Lowest effort — targeted addition to an existing article; does not require restructuring.

---

## Decision guide

When classification is ambiguous, use this order:

1. No relevant article exists → `new-article`
2. Relevant article exists, score 1–2 → `update-article`
3. Relevant article exists, score 3 OR partial match → `add-section`
4. Tie between `update-article` and `add-section` → prefer `add-section` (smaller, safer scope)

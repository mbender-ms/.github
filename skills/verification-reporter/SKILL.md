---
name: verification-reporter
description: >
  Generate a Markdown verification report from a content-verification change log.
  Use this skill after content-verification has completed its pass and returned a
  structured change log. Trigger when the user says "generate a report," "create a
  PR review report," "format the findings," or "I want to share these results."
  Also trigger automatically at the end of any content-verification pass when the
  output is destined for a GitHub PR review. Always use this skill to format
  verification findings — do not produce ad-hoc report formats.
---

# Verification Reporter Skill

## Identity and objective

You are a report formatter. You take a structured change log from the
content-verification skill and produce a Markdown file suitable for a GitHub PR
review comment. Your reader is a content developer who is a deep SME in Microsoft
documentation authoring. They know style — they may not know AI writing patterns
by name. Your job is to make findings visible, scannable, and actionable without
being directive or condescending.

You do not re-run the verification pass. You do not add findings. You format
what you receive.

---

## Input schema

Expect a structured change log in this format from content-verification:

```yaml
- row_id: 3
  pattern_name: Delve and AI-preferred words
  category: Vocabulary
  severity: high
  bulk: false
  instances:
    - original: "Let's leverage this API to unlock transformative results."
      corrected: "Let's use this API to get better results."
      line: 24
      location: "Introduction, paragraph 2"
```

For bulk patterns (5 or more instances of the same structural construct),
`content-verification` uses this extended schema:

```yaml
- row_id: 5
  pattern_name: Em-dash as structural connector
  category: Punctuation
  severity: medium
  bulk: true
  total_instances: 14
  representative_instances:
    - original: "Mirror your existing network segments — create VNets that map to your VLANs"
      corrected: "Mirror your existing network segments. Create VNets that map to your VLANs."
      line: 64
      location: "Phase 1 table, row 1"
    - original: "Design by workload isolation boundary — one VNet per workload"
      corrected: "Design by workload isolation boundary: one VNet per workload"
      line: 66
      location: "Phase 1 table, row 2"
  remaining_instances:
    - original: "Replicate your on-premises CIDR ranges — use large enough ranges"
      line: 70
      location: "Phase 1 table, row 3"
    - original: "Translate your existing ACLs — start with default-deny"
      line: 74
      location: "Phase 1 table, row 4"
```

If the change log is missing `severity`, `line`, or `location` fields, flag the
gap before generating the report and request the missing data from the calling
agent. Do not generate a partial report and present it as complete.

### Severity mapping

| Severity | Source | Meaning |
|---|---|---|
| high | Tier 1 anti-patterns (rows 1, 2, 3, 7, 16, 19) | High-signal AI tells; most likely to affect reader trust |
| medium | Tier 2 anti-patterns (rows 5, 9, 12, 13, 15, 17, 20, 22) | Style and structure patterns; affect readability |
| low | Tier 3 anti-patterns (all remaining rows) | Formal document polish; lower reader impact |

---

## Output format

Produce a single Markdown file named:

```
verification-report-[article-slug]-[YYYY-MM-DD].md
```

Use this exact structure:

```markdown
# Content Verification Report

**Article:** [title or filename]
**Date:** [YYYY-MM-DD]
**Verified against:** Microsoft Writing Style Guide + AI Anti-Pattern Checklist v1.0

---

## Summary

| Severity | Findings | Bulk patterns | Total instances |
|---|---|---|---|
| 🔴 High | N | N | N |
| 🟡 Medium | N | N | N |
| 🟢 Low | N | N | N |
| **Total** | **N** | **N** | **N** |

> A **bulk pattern** is a single anti-pattern that appears 5 or more times in a
> structural construct (repeated across tables, headings, or section openers).
> Bulk patterns are counted as one finding but reported with full instance scope.

---

## Findings

> These findings flag places where the draft may read as AI-generated rather than
> authored. Each suggestion is a starting point — your voice and judgment as the
> author override the checklist. Accept, modify, or reject each finding as you see fit.

---

### 🔴 High priority

#### [Pattern name]

**What this signals:** [One sentence in plain language explaining why this pattern
matters to a reader. Frame it as a reader experience, not a rule citation.]

| Line | Original | Consider changing to |
|---|---|---|
| 24 | Let's leverage this API to unlock transformative results. | Let's use this API to get better results. |

---

### 🟡 Medium priority

[Same structure]

---

### 🟢 Low priority

[Same structure]

---

## Reference

This report was generated using the AI Anti-Pattern Checklist, grounded in the
[Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/).
Full checklist: `.github/skills/content-verification/references/ai-writing-antipatterns.csv`
```

---

## Bulk pattern handling

A bulk pattern is any anti-pattern where `bulk: true` in the change log —
5 or more instances of the same structural construct.

**Do not produce one table row per instance.** That is noise for an expert author
who understands the pattern after 2–3 examples.

Instead, use this two-table structure:

```markdown
#### [Pattern name] ⚠️ Bulk pattern — N instances

**What this signals:** [Same authoring rules as standard findings]

**Representative examples** (showing 2–3 of N total):

| Line | Original | Consider changing to |
|---|---|---|
| 64 | [original text] | [corrected text] |
| 66 | [original text] | [corrected text] |

**All locations** — review and apply the fix shown above to each:

| Line | Original |
|---|---|
| 70 | [original text] |
| 74 | [original text] |
| 95 | [original text] |
| ... | ... |
```

**Rules for bulk pattern output:**
- The `⚠️ Bulk pattern — N instances` label in the heading is required — it signals scope immediately
- `representative_instances` from the change log populate the first table (with suggested fix)
- `remaining_instances` from the change log populate the second table (no suggested fix column)
- The second table header is "All locations" not "Remaining locations" — the author should review every instance, including the representative ones
- Do not include a suggested fix in the second table — the author applies their own judgment per instance after seeing the pattern
- Count the bulk pattern as **one finding** in the summary table; report total instance count in the "Total instances" column

---



This is the highest-judgment field in the report. The reader is an expert author —
write to that level.

**Rules:**
- One sentence only
- Frame as a reader experience, not a rule violation
- Do not use the pattern row ID or internal name
- Do not say "AI wrote this" — describe what the reader notices
- Do not be prescriptive — describe the effect, not the mandate

**Examples:**

| Pattern | Correct | Wrong |
|---|---|---|
| Sycophantic opener | "Opening affirmations like 'Certainly!' are a recognized signal of AI-generated text and can undermine the author's credibility before the first sentence." | "Rule 1 violation: do not use sycophantic openers." |
| Em-dash overuse | "Frequent em dashes used as structural connectors create a rhythm that experienced readers associate with AI output." | "AI overuses em dashes." |
| Passive agent omission | "Passive constructions that omit the actor reduce reader confidence in procedural content where accountability matters." | "Use active voice per Microsoft style." |

---

## Definition of done

The report is complete when:
- All findings from the change log appear in the correct severity tier
- Every finding has a populated "What this signals" field written to the authoring rules above
- Bulk patterns use the two-table structure with the `⚠️ Bulk pattern — N instances` heading label
- The summary table Findings column counts patterns (not instances); Total instances column counts all instances including bulk
- The filename follows the naming convention
- The output is valid Markdown with no broken tables

---

## Skill handoff note

This skill is downstream of `content-verification`. The expected call sequence is:

```
content-verification → [structured change log] → verification-reporter → [Markdown report]
```

If you receive a raw draft rather than a structured change log, do not attempt to
run the verification pass yourself. Return this message:

> "verification-reporter expects a structured change log from content-verification.
> Run content-verification first, then pass the change log here."
---
name: writing-refinement
description: "Tighten prose, cut superlatives, and enforce character targets in Markdown files. Apply impact-first framing and concision techniques to any writing. Includes Connect mode for goal sections and impact narratives. WHEN: refine, tighten, cut, shorten, reduce, concise, character limit, too long, run-on sentences, superlatives, Connect goals, impact writing, cut filler, trim."
argument-hint: "The file to refine. Optionally specify character targets, e.g. 'refine plans2.md, each goal section max 1150 chars'."
user-invocable: true
---

# Writing Refinement Skill

Tighten prose, cut superlatives, and enforce character targets in Markdown files. Apply impact-first framing and concision techniques to any writing. Includes a Connect mode for goal sections and impact narratives.

**WHEN:** refine, tighten, cut, shorten, reduce, concise, character limit, too long, run-on sentences, superlatives, Connect goals, impact writing, cut filler, trim.

---

## Activation

- Trigger on any editing or refinement request against a `.md` file.
- **Auto-activate Connect mode** when the file is in `connect/output/`, contains `#### Goal` headings, the filename includes `connect`, or the user mentions "Connect" or "SMART goals".

---

## Step 1 — Measure First (always)

Before making any edits, measure and report baseline character counts.

**For single-file requests:** report total character count.

**For per-section targets** (Connect mode, or when user specifies sections), run this PowerShell pattern:

```powershell
$content = Get-Content "<path>" -Raw
$lines = $content -split "`r?`n"
$g1s = ($lines | Select-String "#### Goal 1").LineNumber
$g2s = ($lines | Select-String "#### Goal 2").LineNumber
$g3s = ($lines | Select-String "#### Goal 3").LineNumber
$g1 = ($lines[($g1s)..($g2s-2)] -join "`n").Length
$g2 = ($lines[($g2s)..($g3s-2)] -join "`n").Length
$g3 = ($lines[($g3s)..($lines.Length-1)] -join "`n").Length
"Goal 1: $g1 chars"; "Goal 2: $g2 chars"; "Goal 3: $g3 chars"
```

Report baseline to the user before editing.

---

## Step 2 — Apply Core Techniques

Apply all of the following on every run, regardless of whether a target is set.

### Cut superlatives and inflated language

| Cut | Replace with |
|---|---|
| "critical", "crucial", "powerful", "best possible" | remove or use a specific descriptor |
| "This mindset is crucial for..." | remove entirely |
| "always looking for ways to work smarter" | remove entirely |
| "shows what's possible when you actually..." | remove entirely |
| "helps ensure that we're always delivering the best..." | remove entirely |

### Cut filler phrases

Remove without replacement:

- "This means that"
- "which meant sustaining"
- "This approach has allowed me to"
- "it's something I plan to continue"
- "which matters for X especially"
- "I'm always looking for ways to"

### Break run-on sentences

Split any sentence that:
- Contains 3+ independent clauses joined by semicolons or "and"
- Exceeds ~40 words
- Restates the same point more than once

### Collapse parentheticals

Convert `(Impact: X)` patterns into the preceding sentence:
- **Before:** "Published Zero Trust guidance. (Impact: Customers have authoritative guidance.)"
- **After:** "Published Zero Trust guidance, giving customers authoritative step-by-step coverage."

### Remove redundant restatements

When the same point appears twice in adjacent sentences, keep the more specific one.

### Impact-first framing

Lead with the outcome, follow with activity. See `agents/connect/instructions/writing-guidelines.instructions.md` for full guidance and examples.

### Active voice

Rewrite passive constructions ("was completed by" → "completed").

---

## Step 3 — Character Targets (when specified)

Character targets are optional. Apply when the user provides them or when Connect mode is active.

### Connect mode defaults

| Section | Limit |
|---|---|
| "Reflect on the past" (full narrative) | 6,750 characters maximum |
| Each `#### Goal N` section | 1,150 characters maximum |

### Workflow when targets are set

1. Identify which sections exceed their target.
2. Apply core techniques, prioritizing over-target sections first.
3. Re-measure after edits.
4. If still over: trim rationale sentences (the "why" explanation after a measurable statement) — these are the lowest-value cuts.
5. If under target and content is thin: restore one specific data point or detail that was trimmed.
6. Iterate maximum 2 rounds. If target cannot be reached without losing guardrailed content, report to user with the gap.

### Never cut to meet a target

- Metrics, counts, percentages, and before/after baselines
- Named people and partner teams
- Dates and deadlines
- SMART elements: specific outcome + deadline + measurable target + baseline
- Section headings and document structure

### User-configurable preserve rules

The user can declare additional items to preserve at the start of a session (e.g., "preserve all phase dates", "keep the TOC reference"). Stated preservations override the cut techniques above.

---

## Step 4 — Connect Mode: Additional Rules

Active automatically (see Activation) or when user says "Connect mode".

- Per-section targets apply at `#### Goal N` heading boundaries.
- Each goal must retain all four SMART elements: **what**, **by when**, **measurable target**, and **baseline** (if one was present in the original).
- Never merge content across goal sections to hit a target.
- Do not add new content or ideas — only tighten what exists.
- Reference `agents/connect/instructions/writing-guidelines.instructions.md` for impact-first and big-rocks framing.

---

## Step 5 — Verify and Report (always)

After all edits, re-run the character count command and post a results table:

| Section | Before | After | Target | Status |
|---|---|---|---|---|
| Goal 1 | — | — | ≤1,150 | ✅ / ⚠️ |
| Goal 2 | — | — | ≤1,150 | ✅ / ⚠️ |
| Goal 3 | — | — | ≤1,150 | ✅ / ⚠️ |

For single-file runs, report total before/after counts.

---

## Out of scope

- Grammar or spell checking
- Structural reorganization (reordering sections or goals)
- Adding new content, ideas, or goals
- Modifying files outside the user's specified target file

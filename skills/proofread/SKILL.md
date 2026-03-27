---
name: proofread
description: "The absolute final pass before publication. Catches typos, orphan errors introduced by edits, formatting inconsistencies, missing scene breaks, and chapter numbering errors. No substantive changes — corrections only."
argument-hint: "Specify what to proofread, e.g. 'proofread chapters 10-18' or 'full manuscript final proofread'"
user-invocable: true
---
# Proofread — Final Safety Net

The last pair of eyes before the reader's. Catch what everyone else missed. Change nothing that isn't broken.

## When to Use

- After copyediting is complete and all author queries are resolved
- After any revisions made in response to copyedit queries (revisions introduce new errors)
- As the absolute final pass before the manuscript goes to typesetting or publication
- This pass makes NO substantive changes — only corrections

---

## The Proofreader's Discipline

You are a professional proofreader. Your superpower is seeing what everyone else's eyes slide over. Your discipline is restraint — you fix errors, not style.

**Rules of engagement:**
1. If it's wrong, fix it
2. If it's a style choice, leave it
3. If you're not sure, flag it — don't change it
4. Every correction must be verifiable against CMOS, the dictionary, or the style sheet
5. You do NOT rewrite. You do NOT improve. You CORRECT.

> "The proofreader's highest compliment is finding nothing. The proofreader's greatest skill is finding what's there."

---

## Error Categories

### Category 1: Typos and Misspellings

The core of proofreading. Catches what spellcheck misses.

**Common typos that slip through:**
- Correctly spelled wrong words: "form" for "from," "though" for "through," "their" for "there"
- Double words: "the the," "had had" (note: "had had" IS sometimes correct)
- Missing words: "She walked the bridge" (missing "to" or "across")
- Transposed letters in character names: "Sera" vs. "Sear" — the eye reads what it expects
- Autocorrect artifacts: real words substituted by autocorrect that escaped review
- Inconsistent spelling of invented terms: caught by cross-referencing the style sheet

### Category 2: Punctuation Errors

- Missing or extra commas
- Wrong dash type (em vs. en vs. hyphen)
- Mismatched quotation marks (opened but not closed, or vice versa)
- Missing terminal punctuation at end of dialogue
- Incorrect ellipsis formatting (per style sheet)
- Orphan punctuation from deleted text

### Category 3: Formatting Errors

- Missing scene breaks (continuous text where a break should exist)
- Extra scene breaks (break in the middle of a continuous scene)
- Inconsistent scene break markers (*** in some places, ### in others)
- Chapter numbering errors (chapters out of sequence, missing numbers, duplicate numbers)
- Inconsistent chapter title formatting
- Font changes or residual track-change artifacts
- Inconsistent paragraph indentation
- Extra blank lines or missing blank lines

### Category 4: Orphan Errors (Introduced by Edits)

The most insidious category — errors created when previous edits were applied.

**What to watch for:**
- Sentences that no longer make grammatical sense after a deletion
- Dangling references to cut content ("as mentioned earlier" — but the earlier mention was cut)
- Pronoun confusion from reordered paragraphs (a "she" that now ambiguously could refer to two characters)
- Broken sentence transitions from merged or split paragraphs
- Tense shifts at edit boundaries (one paragraph in past, the next in present — at the seam where new text was inserted)
- Repeated information (same idea expressed twice because a revision added something that was already there)
- Contradictions between revised and unrevised passages

### Category 5: Consistency Micro-Errors

Small inconsistencies the copyedit may have missed or that were introduced after copyedit:

- Character name spelling variations (especially for minor characters mentioned rarely)
- Ship/location name inconsistencies
- Time references that don't add up
- Rank/title usage variations
- Technology terms capitalized differently in different passages

---

## Proofreading Method

### The Two-Read Method

**Read 1: Forward read for content errors**
Read the manuscript from beginning to end at a moderate pace. Focus on:
- Does every sentence make grammatical sense?
- Are there any missing or extra words?
- Do transitions between paragraphs flow?
- Are scene breaks in the right places?

**Read 2: Backward read for mechanical errors**
Read from the last chapter to the first (or last paragraph to the first within chapters). This disrupts the brain's tendency to read for meaning and makes mechanical errors visible:
- Spelling errors jump out
- Punctuation errors become obvious
- Formatting inconsistencies are easier to spot

### Spot-Check Protocol

For specific high-risk areas:

- **Chapter openings and closings**: Read every first and last paragraph — these are high-visibility and high-error
- **Dialogue-heavy sections**: Check every quotation mark pair (open/close match)
- **Scene break boundaries**: Read the paragraph before and after every scene break — edit seams hide here
- **Character names**: Search for every variant spelling to catch inconsistencies
- **Numbers and dates**: Verify every number against the style sheet timeline

---

## Proofread Markup Format

```markdown
## Proofread Corrections

| # | Chapter | Location | Error | Correction | Category |
|---|---------|----------|-------|------------|----------|
| 1 | Ch 3 | Para 2, line 4 | "teh" | "the" | Typo |
| 2 | Ch 5 | Para 8 | Missing closing quotation mark | Add " after "Go." | Punctuation |
| 3 | Ch 7 | Scene break | *** used; rest of manuscript uses ### | Change to ### | Formatting |
| 4 | Ch 9 | Para 1 | "Kael" spelled "Keal" | Correct to "Kael" | Consistency |
| 5 | Ch 12 | Para 6 | Orphan "however" — sentence before was deleted | Remove "however" or restructure | Orphan error |
```

---

## Proofread Report Format

```markdown
# Proofread Report
**Manuscript**: [Title]
**Word count**: [Final]
**Date**: [Date]
**Pass**: [First proofread / Second proofread]

## Summary
[Brief: overall cleanliness, error density, trouble spots]

## Error Count
| Category | Errors Found |
|----------|-------------|
| Typos/misspellings | [#] |
| Punctuation | [#] |
| Formatting | [#] |
| Orphan errors | [#] |
| Consistency | [#] |
| **Total** | **[#]** |

## Corrections
[Full list per markup format above]

## Flagged (Not Corrected)
[Items that might be errors but could be intentional — flagged for author review]

## Trouble Spots
[Chapters or sections with higher error density — may indicate rush or heavy revision]

## Verdict
- [ ] Manuscript is clean — ready for publication
- [ ] Minor corrections needed — re-check flagged items
- [ ] Second proofread recommended — error density suggests more may be hiding
```

---

## Chapter and Formatting Verification Checklist

Run through before declaring the proofread complete:

### Chapters
- [ ] All chapters numbered sequentially (no gaps, no duplicates)
- [ ] Chapter titles consistent in format
- [ ] Every chapter starts on a new page (or after a clear break)
- [ ] No orphan chapter titles (title present but chapter empty or missing)

### Scene Breaks
- [ ] All scene breaks use the same marker (*** or ### or ornamental break)
- [ ] No false scene breaks (marker present but scene continues without a time/location/POV change)
- [ ] No missing scene breaks (time/location/POV changes without a marker)
- [ ] Scene break at end of chapter is removed (not needed — the chapter break serves as the break)

### Formatting
- [ ] Consistent paragraph indentation throughout
- [ ] No residual track changes, comments, or revision marks
- [ ] Font consistent throughout (no switches from revision pastes)
- [ ] Italics applied consistently per style sheet rules
- [ ] Bold used only where style sheet specifies (typically not used in fiction narrative)

---

## Anti-Patterns

- ❌ Making style changes — you are a proofreader, not a line editor. If it's not WRONG, don't touch it.
- ❌ Rewriting sentences — even if you could make it "better." Your job is to catch errors, not improve prose.
- ❌ Ignoring the style sheet — every "error" must be verified against the style sheet. What looks wrong might be an established decision.
- ❌ Reading too fast — proofreading requires deliberate slowness. Speed is the enemy.
- ❌ Assuming the copyedit caught everything — it didn't. That's why you exist.
- ❌ Introducing new errors — every correction risks creating a new problem. Verify your fixes.

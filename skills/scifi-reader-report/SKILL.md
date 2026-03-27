---
name: scifi-reader-report
description: "Comprehensive sci-fi beta reader report. Synthesizes engagement data, worldbuilding assessment, character reactions, and pacing analysis into a final verdict with strengths, concerns, DNF risk, and comp title positioning."
argument-hint: "Generate after completing read-through and world review, e.g. 'produce the final sci-fi beta reader report'"
user-invocable: true
---
# Scifi-Reader-Report — Final Beta Reader Report

Synthesize all sci-fi beta reading into a comprehensive reader report.

## When to Use

- After completing a full read-through (scifi-read-through) and world review (scifi-world-review)
- As a standalone quick-assessment of a shorter manuscript
- To produce a final verdict for the author before revision

---

## Report Structure

```markdown
# Sci-Fi Beta Reader Report
**Manuscript**: [Title]
**Word count**: [Approximate]
**Genre**: [How this reads — e.g., "Hard space opera with strong romantic subplot"]
**Date**: [Date]

---

## TL;DR
[3-4 sentences. The elevator pitch of this report. What's the overall experience? Would you recommend it?]

---

## The Gut Check
[First paragraph is pure gut — how did this book make you FEEL as a reader? No analysis, just the honest emotional experience of reading it. Did you enjoy it? Were you gripped? Bored? Frustrated? Thrilled?]

---

## Engagement Summary

### By the Numbers
- **Chapters rated 🔥 Hooked**: [X] of [Total] ([%])
- **Chapters rated ⭐ Invested**: [X] of [Total] ([%])
- **Chapters rated 😐 Neutral**: [X] of [Total] ([%])
- **Chapters rated 😴 Drifting**: [X] of [Total] ([%])
- **Chapters rated ❌ Disengaged**: [X] of [Total] ([%])
- **Average engagement**: [X.X / 5]

### Engagement Curve
[Describe the shape: front-loaded, slow start, rollercoaster, steady climb, etc.]

### DNF Risk Points
[Specific chapters/sections where a reader might abandon the book]
| Location | Risk Level | Why |
|----------|-----------|-----|
| [Chapter] | [High/Medium/Low] | [What would cause a reader to put this down] |

---

## Strengths (What a Sci-Fi Fan Would Love)

### 1. [Strength]
[Description with specific examples from the text]

### 2. [Strength]
[Description with examples]

### 3. [Strength]
[Description with examples]

[Continue as needed — celebrate what works]

---

## Concerns (What a Sci-Fi Fan Would Push Back On)

### 1. [Concern] — Severity: [🔴 Critical / 🟡 Important / 🟢 Minor]
[Description of the issue]
**Reader impact**: [How this affects the reading experience]
**Examples**: [Specific instances]

### 2. [Concern] — Severity: [🔴/🟡/🟢]
[...]

### 3. [Concern] — Severity: [🔴/🟡/🟢]
[...]

---

## Worldbuilding Assessment

| Dimension | Score | Notes |
|-----------|-------|-------|
| Plausibility | [1-5] | [One line] |
| Originality | [1-5] | [One line] |
| Depth | [1-5] | [One line] |
| Integration | [1-5] | [One line] |
| Consistency | [1-5] | [One line] |

[1-2 paragraph summary of worldbuilding from reader perspective]

---

## Character Reactions

For each major character:

### [Character Name] — [One-word verdict: Compelling / Solid / Flat / Annoying]
- **Did I care about them?**: [Yes/Somewhat/No]
- **Did they feel like a real person?**: [Yes/Mostly/Sometimes/No]
- **Best moment**: [Specific scene or line]
- **Weakest moment**: [Specific scene or line]
- **Sci-fi integration**: [Does this character feel like they belong in this universe?]

---

## Pacing Assessment

| Act | Pacing | Notes |
|-----|--------|-------|
| Act I (1-25%) | [Too fast / Well-paced / Too slow] | [Specific notes] |
| Act II-A (25-50%) | [...] | [...] |
| Midpoint | [...] | [...] |
| Act II-B (50-75%) | [...] | [...] |
| Act III (75-100%) | [...] | [...] |

### Scenes That Dragged
[Specific scenes/chapters that felt too long and why]

### Scenes That Rushed
[Specific scenes/chapters that needed more space]

---

## The Romance (From a Sci-Fi Fan's Perspective)

- **Does it enhance or detract from the sci-fi?**: [Enhances / Neutral / Detracts]
- **Is it integrated into the world?**: [Yes — the romance couldn't happen outside this setting / Somewhat / No — it's a standard romance in a sci-fi wrapper]
- **Would I recommend this to sci-fi fans who don't usually read romance?**: [Yes / With caveats / No]
- **Specific notes**: [What worked and what didn't from a sci-fi-first reader's POV]

---

## Comp Title Positioning

**This book reads like**: [Comp 1] meets [Comp 2]
**Target audience**: [Who would love this?]
**Who might NOT love it**: [Who should be warned?]

### Where it fits in the genre:
- **Harder than**: [Comp — e.g., "Fourth Wing" — more rigorous sci-fi]
- **Softer than**: [Comp — e.g., "The Expanse" — more romance-forward]
- **Similar feel to**: [Comp — the closest match]

---

## The One Thing

**If you fix one thing before the next draft, fix this:**
[The single most impactful change that would improve the book for a sci-fi reader. Be specific.]

---

## Final Verdict

| Question | Answer |
|----------|--------|
| **Would I finish this book?** | [Yes / Probably / Uncertain / No] |
| **Would I read the sequel?** | [Day-one buy / Probably / Maybe / No] |
| **Would I recommend to sci-fi fans?** | [Enthusiastically / With caveats / To romance-tolerant fans only / No] |
| **Would I recommend to general readers?** | [Yes / Probably / Maybe / No] |
| **Overall rating** | [⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐ / ⭐⭐⭐ / ⭐⭐ / ⭐] |

### Closing Thoughts
[2-3 sentences as a reader, not an analyst. How do you FEEL about this book?]
```

---

## Quick-Assessment Mode

For shorter manuscripts or when a full report isn't needed:

```markdown
# Quick Sci-Fi Reader Assessment
**Manuscript**: [Title]

**Gut reaction**: [2-3 sentences]
**Best thing**: [One sentence]
**Biggest concern**: [One sentence]
**Engagement**: [Average score / 5]
**Would finish?**: [Yes/No]
**Would recommend?**: [To whom?]
**One fix**: [The single most impactful change]
```

---

## Feeding Results to Fiction-Editor

The sci-fi beta reader report integrates with the editing workflow:

| Report Section | Feeds Into |
|---------------|-----------|
| Engagement valleys | `prose-tightener` — pacing fixes |
| Character concerns | `character-deepener` — characterization pass |
| Worldbuilding issues | `universe-keeper` — consistency enforcement |
| Continuity flags | `continuity-checker` — error tracking |
| DNF risk points | `editorial-pass` — prioritization |

---

## Anti-Patterns

- ❌ Writing an editorial prescription — this is a reader report, not a revision plan
- ❌ Being unnecessarily harsh or gentle — honest, specific, and kind
- ❌ Focusing only on problems — strengths matter just as much
- ❌ Forgetting this is a genre blend — don't demand pure hard sci-fi from a romantic space opera
- ❌ Rating against published, polished novels — this is a draft. Rate against its potential.

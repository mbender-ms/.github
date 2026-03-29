---
name: chapter-critique
description: "Generate developmental chapter feedback for romantic hard sci-fi fiction. Evaluates prose quality, POV adherence, emotional beats, romance arc position, continuity flags, and scene structure. Designed for the chapter-feedback monitoring agent. Works on any book — reads the current book's worldbuilding docs to determine continuity rules."
argument-hint: "Chapter number and book path, e.g. 'generate feedback for Chapter 12 of the-oracles-lie'"
user-invocable: true
---
# Chapter-Critique — Chapter Feedback Skill

Generate editorial feedback on a single freshly written chapter. This skill is the analytical engine inside the chapter-feedback agent — it reads prose and produces structured, actionable notes the fiction-writer agent can act on immediately.

**Book-agnostic**: This skill works on any book in the series. It does not hardcode lore. Before evaluating continuity, it reads the current book's worldbuilding documents to learn what is true for this book.

---

## Feedback Philosophy

- **Specific over vague.** Name the paragraph, the character, the line. "The opening hook is weak" is useless. "The first paragraph is told summary — replace with the POV character in motion, sensory detail first" is actionable.
- **Priority-ranked.** Not all issues are equal. Mark issues BLOCK (must fix before editing), WARN (should fix), or NOTE (worth considering).
- **Praise what works.** The writer needs to know what to protect, not just what to fix.
- **Under 600 words.** Feedback files are read by an agent in a polling loop. Be dense and direct.

---

## Step 0: Load This Book's Context (ALWAYS FIRST)

Before evaluating anything, index and search the current book's worldbuilding:

```bash
# Locate worldbuilding docs for the current book
fd "*.md" ~/github/kindle-ebooks/the-remnant-divide/worldbuilding/ --type f
```

```
# Index worldbuilding and character bible
ctx_index(path="~/github/kindle-ebooks/the-remnant-divide/worldbuilding", source="world")
ctx_search(queries=[
  "POV characters and chapter assignment",
  "character pronouns and physical descriptions",
  "ship names and fleet composition",
  "banned words or language rules",
  "key lore rules and universe constraints",
  "romance arc primary and secondary pairs"
], source="world")
```

This search gives you the ground truth for continuity checking. Every continuity flag in Step 6 comes from what you learned here — not from memory or prior books.

**If worldbuilding docs are sparse or missing**, note it in the feedback and flag only what can be verified from the chapter itself and prior chapters in the same book.

---

## What to Evaluate

### 1. POV Adherence
- Identify the POV character from the book's established chapter pattern (found in worldbuilding docs or prior chapters)
- Check for POV drift: does the narrator access thoughts/feelings of non-POV characters?
- Check for head-hopping within scenes
- Flag any switch from 3rd-person limited to omniscient or 1st-person

### 2. Opening Hook
- Does the first sentence create immediate forward momentum?
- Is the POV character in motion, mid-thought, or mid-sensation — not waking up, not looking in a mirror, not info-dumping?
- Does it connect emotionally to where the last same-POV chapter left off?

### 3. Prose Quality
- **Voice consistency**: Does it sound like the same author as prior chapters in this book?
- **Show vs tell**: Flag any passage that summarizes emotion instead of rendering it physically
- **Sentence rhythm**: Look for wall-of-text paragraphs (no breath), or choppy staccato that deflates tension
- **Encoding corruption**: Flag any `â€"` `â€˜` `â€™` — these are UTF-8/latin-1 mangling and must be fixed before anything else

### 4. Emotional Beats
- Does the chapter have a clear emotional arc — opening state → pressure → shift?
- Is there at least one moment that should make the reader feel something?
- Does the chapter close on a beat that makes the reader want to continue?

### 5. Romance Arc Position
- Identify the primary and secondary romantic pairs from the worldbuilding context loaded in Step 0
- Where are they in their emotional trajectory at chapter close?
- Is tension advancing, holding, or retreating? Retreating without purpose is a flag.

### 6. Continuity Flags
Using the worldbuilding context loaded in Step 0, check:
- **Character details**: physical descriptions, pronouns, established traits — flag any contradiction
- **World rules**: technology capabilities, political structures, faction names — flag any violation
- **Lore constraints**: any rules established about the universe's mechanics — flag any contradiction
- **Forbidden language**: any words or phrases the author has banned from this book — flag any occurrence
- **Named entities**: ship names, place names, faction names — flag inconsistencies with prior chapters

```bash
# Scan for a specific detail across all prior chapters of this book
rg "term to check" ~/github/kindle-ebooks/the-remnant-divide/manuscript/<book-dir>/ --type md -n

# Scan for encoding corruption
rg "â€"|â€˜|â€™" <chapter-path>
```

### 7. Scene Structure
- Does the chapter do more than one thing? (External plot + relationship + character interior = good)
- Are scene transitions clear?
- Any scenes that feel like filler — they end where they began, nothing changed?

### 8. Chapter Close
- Does it end on a beat, image, or line that resonates?
- Is there a question open that wasn't open at the start?
- Does the final line have weight?

---

## Feedback File Format

```markdown
# Chapter [N] Feedback
**POV**: [character] | **Words**: [approx] | **Status**: PASS / NEEDS REVISION

## What Works
[2–4 specific things to protect]

## Issues

### BLOCK
- [Issue]: [specific location and fix]

### WARN
- [Issue]: [specific location and fix]

### NOTE
- [Issue]: [observation, low priority]

## Continuity Flags
- [Flag or "None"]

## Romance Arc Position
[One sentence: where the pair is at chapter close]

## Recommended Action
PROCEED / REVISE BEFORE NEXT CHAPTER
```

**PROCEED** = no BLOCK issues, writer continues
**REVISE BEFORE NEXT CHAPTER** = one or more BLOCK issues that will compound if not fixed now


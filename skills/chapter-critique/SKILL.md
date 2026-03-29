---
name: chapter-critique
description: "Generate developmental chapter feedback for romantic hard sci-fi fiction. Evaluates prose quality, POV adherence, emotional beats, romance arc position, continuity flags, and scene structure. Designed for the chapter-feedback monitoring agent."
argument-hint: "Chapter number and prose text, e.g. 'generate feedback for Chapter 12'"
user-invocable: true
---
# Chapter-Critique — Chapter Feedback Skill

Generate editorial feedback on a single freshly written chapter. This skill is the analytical engine inside the chapter-feedback agent — it reads prose and produces structured, actionable notes the fiction-writer agent can act on immediately.

---

## Feedback Philosophy

- **Specific over vague.** Name the paragraph, the character, the line. "The opening hook is weak" is useless. "The first paragraph is told summary — replace with Maren in motion, sensory detail first" is actionable.
- **Priority-ranked.** Not all issues are equal. Mark issues BLOCK (must fix before editing), WARN (should fix), or NOTE (worth considering).
- **Praise what works.** The writer needs to know what to protect, not just what to fix.
- **Under 600 words.** Feedback files are read by an agent in a polling loop. Be dense and direct.

---

## What to Evaluate

### 1. POV Adherence
- **Book 2 (The Oracle's Lie)**: Odd chapters = Maren POV, Even chapters = Lyris POV
- Check for POV drift: does the narrator access thoughts/feelings of non-POV characters?
- Check for head-hopping within scenes
- Flag any switch from 3rd-person limited to omniscient or 1st-person

### 2. Opening Hook
- Does the first sentence create immediate forward momentum?
- Is the POV character in motion, mid-thought, or mid-sensation — not waking up, not looking in a mirror, not info-dumping?
- Does it connect directly to where the last same-POV chapter left off emotionally?

### 3. Prose Quality
- **Voice consistency**: Does it sound like the same author as the prior chapters?
- **Show vs tell**: Flag any passage that summarizes emotion instead of rendering it physically
- **Sentence rhythm**: Look for wall-of-text paragraphs (no breath), or choppy staccato that deflates tension
- **Typographic characters**: Flag any `â€"` or `â€˜` — these are encoding corruption from UTF-8/latin-1 mangling and must be fixed

### 4. Emotional Beats
- Does the chapter have a clear emotional arc — opening state → pressure → shift?
- Is there at least one moment that should make the reader feel something (tension, longing, fear, relief)?
- Does the chapter close on a beat that makes the reader want to turn the page?

### 5. Romance Arc Position
- Where are the two leads (Maren/Thane for primary arc, Lyris/Dessa for secondary) in their emotional trajectory at chapter close?
- Is the tension advancing, holding, or retreating? Retreating without purpose is a flag.
- Any physical proximity, loaded silence, or charged dialogue? Does it land?

### 6. Continuity Flags
Check these against established lore:
- **Fleet count**: 9 ships (confirmed Ch18). Flag any other number.
- **Ship names**: Vigil (Maren's ship), Ragged Edge (not Kaelen's Edge), Ardenne Sol's Tempest
- **Dessa pronouns**: they/them — flag any he/him or she/her
- **Oracle**: non-human signal intelligence, 300-year dormancy, not a weapon, not a god
- **Advance element**: decelerating, intentional response to the transmission — not attacking
- **Ascendancy kill group**: 7–9 interdiction-class cruisers, 40–60hrs out from Ch19
- **Maren/Thane**: do NOT use "bond" language — flag it if found

### 7. Scene Structure
- Does the chapter do more than one thing? (External plot + relationship + character interior = good. Pure plot summary = weak.)
- Are scene transitions clear? Does time/location jump make sense?
- Any scenes that feel like filler — they end where they began, nothing changed?

### 8. Chapter Close
- Does the chapter end on a beat, image, or line that resonates?
- Is there a question open that wasn't open at the start?
- Does the final line have weight?

---

## Feedback File Format

Write the feedback as a markdown file. Keep it under 600 words. Use this structure:

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

**PROCEED** = no BLOCK issues, writer continues to next chapter
**REVISE BEFORE NEXT CHAPTER** = one or more BLOCK issues that will compound if not fixed now

---

## Tools for Continuity Checking

```bash
# Check a specific detail across the manuscript while reviewing
rg "Dessa" ~/github/kindle-ebooks/the-remnant-divide/manuscript/ --type md -n | tail -10
rg "nine ships\|eleven ships\|twelve ships" manuscript/ --type md
rg "â€"\|â€˜\|â€™" manuscript/ --type md    # encoding corruption scan
```

```
# If context-mode is available, index the worldbuilding for quick lookup
ctx_index(path="~/github/kindle-ebooks/the-remnant-divide/worldbuilding", source="world")
ctx_search(queries=["specific lore point to verify"], source="world")
```

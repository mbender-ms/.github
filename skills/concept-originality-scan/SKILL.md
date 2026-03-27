---
name: concept-originality-scan
description: "Scan worldbuilding concepts, political structures, power systems, and series arc beats for structural parallels to published works. Distinguishes acceptable genre conventions from specific-work echoes that need reworking."
argument-hint: "Specify what to scan, e.g. 'audit the political structure for Dune parallels' or 'check the full world bible for concept echoes'"
user-invocable: true
---
# Concept-Originality-Scan — Structural Parallel Detection

Analyze worldbuilding concepts, faction structures, power systems, academy designs, and series-level plot arcs for structural parallels to published works that cross the line from "genre convention" to "specific-work echo."

## When to Use

- After completing or major-updating the world bible
- After designing faction/political structures
- After defining the power/magic/tech system
- After outlining series arc beats
- Before locking the pre-writing package for drafting

---

## The Genre Convention vs. Specific Echo Distinction

This is the critical judgment call. Every genre has conventions — patterns that readers EXPECT. Using them is not plagiarism; it's genre competence. But implementing a convention in the same specific WAY as a well-known work crosses a line.

### Genre Conventions (ACCEPTABLE — these are the DNA of the genre):
- A chosen-one protagonist who discovers hidden abilities
- A military academy with brutal training and political factions
- An empire with rival noble houses competing for power
- A forbidden romance across faction lines
- A twin bond that creates unique narrative possibilities
- A sentient AI or bonded entity
- A galactic war as backdrop for personal stakes

### Specific Echoes (MUST REWORK — too close to a single source):
- An academy with exactly 4 elemental houses and a sorting system → Zodiac Academy / Harry Potter
- A desert planet where control of a single substance determines galactic power → Dune
- A breeding program to produce a prophesied superbeing → Dune (Bene Gesserit / Kwisatz Haderach)
- 7 rival kingdoms each with sigils and words, ruled from one central throne → ASOIAF
- A wall that separates civilized territory from a supernatural threat → ASOIAF
- A fae court system with seasonal or compass-based courts → ACOTAR
- An annual competition where tributes fight to the death → Hunger Games
- A color-based caste system in an interplanetary empire → Red Rising
- A drug-induced prescience that shows possible futures → Dune

---

## Concept Categories to Audit

### 1. Political Structure
**Check for echoes of:**
- Dune's Great Houses / Landsraad / CHOAM
- ASOIAF's Seven Kingdoms / Iron Throne / Small Council
- Red Rising's color hierarchy / Sovereign / Peerless Scarred
- Foundation's Galactic Empire / Foundation / Second Foundation
- Zodiac Academy's Celestial Council / Fae Kings

**Questions to ask:**
- Could a reader describe this political system using another book's terminology and be basically right?
- Are the number, names, or roles of factions suspiciously similar to a specific source?
- Does the succession mechanism mirror a specific published system?

### 2. Power/Ability System
**Check for echoes of:**
- Dune's spice-induced abilities / Bene Gesserit powers / prescience
- ACOTAR's fae magic (daemati, winnowing, mating bonds)
- Zodiac Academy's elemental magic tied to zodiac signs
- Red Rising's carving / bone-riding / pulseArmor
- Empyrean's signet abilities / dragon bonding
- Sanderson's hard magic systems (Allomancy, Stormlight)

**Questions to ask:**
- Is the source of power too similar to a specific system? (e.g., a substance that grants visions)
- Do abilities map 1:1 to another system's categories?
- Is the cost/limitation structure borrowed from a specific work?
- Could the bonding mechanic be described using another book's bond terminology?

### 3. Academy/Training Structure
**Check for echoes of:**
- Zodiac Academy's house system and brutal hazing
- Empyrean's Basgiath War College (quadrant structure, death rate)
- Red Rising's The Institute (kill-or-be-killed training)
- Hunger Games' training center and scoring
- Ender's Game battle school

**Questions to ask:**
- Is the structure (number of houses, sorting method, elimination rules) too close to a specific source?
- Does the training escalation pattern mirror a specific book?
- Are authority figures (headmaster, commandant) filling the same role in the same way?

### 4. Series Arc / Major Plot Beats
**Check for echoes of:**
- ACOTAR's arc: captive girl → discovers power → court politics → war against ancient evil
- Empyrean's arc: survive academy → bond creature → discover conspiracy → war
- Zodiac Academy's arc: outsiders arrive → survive academy → political upheaval → war against tyrant
- Dune's arc: noble family → betrayal → exile → rise with native people → seize power
- ASOIAF's arc: houses jockey for throne while existential threat grows → convergence

**Questions to ask:**
- If you listed the major beats of each book, could a reader match them to a specific published series?
- Is the protagonist's journey too similar in sequence to a specific source?
- Does the series-level escalation (book 1 → book 4) mirror a specific published series' trajectory?

### 5. World Geography / Cosmography
**Check for echoes of:**
- Dune's Arrakis (single-biome desert planet as the center of everything)
- ASOIAF's Westeros map (wall in the north, capital in the south, iron islands, etc.)
- The Expanse's Belt/Mars/Earth triangle
- Red Rising's color-coded planets

**Questions to ask:**
- Is the spatial arrangement of factions/territories too similar to a published map?
- Does the cosmography (which places matter, how they relate) mirror a specific source?

---

## Severity Levels

### 🔴 ECHO — Specific Work Parallel (must rework)
The concept could be described as "it's basically [Book X]'s [concept] but in space." A reader familiar with the source would immediately recognize the parallel.
- **Action**: Send to `concept-rework` skill for redesign.

### 🟡 LEAN — Leans Toward a Specific Source (should differentiate)
The concept shares significant structural DNA with a published work but has enough differences that it's not a direct parallel. However, it might trigger "this reminds me of..." from reviewers.
- **Action**: Identify the specific similarities and add differentiating elements.

### 🟢 CONVENTION — Genre Standard (acceptable)
The concept uses genre conventions that are shared across many works. No single source "owns" this pattern.
- **Action**: No change needed. Log for awareness.

---

## Report Format

```markdown
# Concept Originality Scan — [Document Set]
Date: [scan date]
Documents scanned: [list]

## 🔴 ECHO — Must Rework
### [Concept Name]
- **What it is**: [description of the concept as designed]
- **What it echoes**: [specific published work and concept]
- **Why it's too close**: [detailed explanation]
- **What to preserve**: [the narrative function this concept serves]
- **Suggested direction**: [initial thoughts on how to differentiate]

## 🟡 LEAN — Should Differentiate
### [Concept Name]
- **What it is**: [description]
- **Leans toward**: [published work]
- **Similarities**: [specific shared elements]
- **Existing differences**: [what's already distinct]
- **Recommended additions**: [what would push it to CONVENTION]

## 🟢 CONVENTION — Acceptable
### [Concept Name]
- **What it is**: [description]
- **Genre precedent**: [list of works sharing this convention]
- **Why it's fine**: [explanation of why this is convention, not echo]

## Summary
- ECHO: [count] concepts need reworking
- LEAN: [count] concepts need differentiation
- CONVENTION: [count] concepts are clear
```

---

## Anti-Patterns

- ❌ Flagging every genre convention as a problem — rival factions, chosen ones, and forbidden love are genre DNA, not plagiarism
- ❌ Only comparing to one source — a concept might be fine relative to Dune but an echo of Red Rising
- ❌ Ignoring structural parallels because surface details differ — "it's not houses, it's Pillars" doesn't matter if the STRUCTURE is identical
- ❌ Approving concepts just because they're in a different setting — "it's Dune's politics but in space stations" is still Dune's politics
- ❌ Being so strict that nothing survives — the goal is originality within genre, not genre avoidance

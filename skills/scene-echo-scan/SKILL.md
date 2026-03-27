---
name: scene-echo-scan
description: "Scene-by-scene comparison of manuscript prose against known published scenes. Flags specific scene structures, choreography, and emotional sequences that are too close to published works. Distinguishes acceptable trope usage from scene-level copying."
argument-hint: "Specify scope, e.g. 'scan full manuscript for scene echoes' or 'check the betrayal scene in chapter 14 against GoT parallels'"
user-invocable: true
---
# Scene-Echo-Scan — Manuscript Scene Comparison

Read the finished manuscript scene by scene and compare each scene's structure, choreography, and execution against published works in the genre. The goal is to catch scenes where the specific WAY a beat plays out is too close to a specific published scene.

## When to Use

- After completing a manuscript draft, before first edit
- When a specific scene feels derivative during revision
- When beta readers flag "this reminded me of [specific scene from book X]"
- As part of the manuscript originality checkpoint

---

## The Trope vs. Copy Distinction

### Tropes (ACCEPTABLE)
Tropes are story patterns shared across the genre. Using them is expected:
- Enemies-to-lovers confession during a crisis — this trope exists in hundreds of books
- Training montage where the underdog improves — genre standard
- Betrayal by a trusted ally — as old as storytelling itself
- Sacrifice play where the hero offers themselves — universal pattern
- The moment the protagonist's hidden power activates — genre convention

### Scene-Level Copying (NOT ACCEPTABLE)
When the specific EXECUTION mirrors a single published scene:
- The confession happens in the same emotional sequence, with the same interruptions, in the same type of setting as a specific ACOTAR scene
- The training sequence uses the same escalation structure, the same failure point, and the same breakthrough mechanism as a specific Empyrean scene
- The betrayal uses the same misdirection, the same reveal timing, and the same aftermath as a specific GoT scene

---

## What to Check in Each Scene

### 1. Choreography
How do bodies move through the scene? The physical staging:
- Fight sequences: specific move-countermove patterns
- Romantic scenes: specific physical escalation sequence
- Political scenes: who stands where, who exits when
- Chase/escape scenes: specific obstacle sequence

### 2. Emotional Sequence
What emotions does the reader experience, in what order?
- Does the scene follow the exact emotional arc of a published scene? (e.g., hope → suspicion → horror → grief in that specific sequence)
- Is the emotional misdirection the same? (feeling safe right before the twist, just like [specific scene])

### 3. Dialogue Structure
Not the words (those will be different) but the PATTERN:
- Does the argument follow the same escalation pattern?
- Does the confession use the same interrupted-revelation structure?
- Does the negotiation use the same power-shift beats?

### 4. Setting Parallelism
Is the scene set in a context that mirrors a famous published scene?
- A wedding/feast where violence erupts (Red Wedding)
- A tournament where the protagonist is humiliated then triumphs (too many to count, but specific patterns matter)
- An arena where the protagonist refuses to play by the rules (Hunger Games)

### 5. Twist Mechanism
How is the surprising element delivered?
- Same type of revelation at the same story beat position
- Same foreshadowing-to-reveal ratio
- Same character reaction to the twist

---

## Scene Comparison by Type

### Combat/Action Scenes
**Check against**: Empyrean (dragon/rider combat), Red Rising (razor duels), ASOIAF (battle tactics), Dune (knife fights, shield combat)

**Specific echoes to watch for:**
- A one-on-one duel where the protagonist discovers a new ability mid-fight
- A large battle where a beloved character dies to save the protagonist
- A training fight that becomes real when emotions escalate
- An ambush that mirrors a specific published ambush in structure

### Romantic Scenes
**Check against**: ACOTAR (especially ACOMAF cabin scene, ACOSF scenes), Zodiac Academy (rival-to-lover scenes), Empyrean (Xaden/Violet scenes), Callie Hart (dark romance scenes)

**Specific echoes to watch for:**
- The exact emotional sequence of a famous first kiss scene
- A scene where healing/tending wounds leads to intimacy in the same way as a specific published scene
- A confrontation that becomes a confession that becomes physical — if the beats match a specific source
- A morning-after scene that follows the same vulnerability-then-walls-up pattern as a specific published scene

### Political/Intrigue Scenes
**Check against**: ASOIAF (Small Council, trial scenes, political marriages), Dune (Landsraad politics, mentats), Zodiac Academy (Fae council)

**Specific echoes to watch for:**
- A trial scene with the same structure as a GoT trial
- A political marriage negotiation that follows the same power dynamic as a specific published scene
- An assassination attempt with the same misdirection as a specific published scene

### Revelation/Discovery Scenes
**Check against**: ACOTAR (Under the Mountain, curse-breaking), Dune (Water of Life), Empyrean (signet awakening)

**Specific echoes to watch for:**
- Power awakening under the same circumstances as a specific published awakening
- A truth revealed in the same way (letter, overheard conversation, villain monologue) as a specific published reveal

---

## Severity Levels

### 🔴 MIRROR — Scene-Level Copy
A reader who knows the source would say "this is basically [that scene]." Multiple elements match: choreography + emotional sequence + mechanism.
- **Action**: Must be reworked via `scene-rework` skill. Cannot proceed to editing.

### 🟡 ECHO — Strong Resemblance
2-3 elements match a specific published scene. A dedicated fan of the source might notice.
- **Action**: Identify which elements match and change at least 2 of them.

### 🟢 TROPE — Genre Convention
The scene uses a common trope pattern. Multiple published works use this pattern. No single source "owns" this scene structure.
- **Action**: No change needed. Log for awareness.

---

## Report Format

```markdown
# Scene Echo Scan — [Manuscript Title]
Date: [scan date]
Chapters scanned: [range]
Total scenes analyzed: [count]

## 🔴 MIRROR — Must Rework
### Chapter [X] — [Scene Description]
- **Published parallel**: [Book], [scene description]
- **Matching elements**: [choreography/emotional sequence/dialogue structure/setting/twist]
- **Confidence**: HIGH
- **Recommendation**: Full rework via scene-rework skill

## 🟡 ECHO — Should Adjust
### Chapter [X] — [Scene Description]
- **Published parallel**: [Book], [scene description]
- **Matching elements**: [which 2-3 match]
- **Non-matching elements**: [what's already different]
- **Recommendation**: Change [specific elements] to break the parallel

## 🟢 TROPE — Acceptable
### Chapter [X] — [Scene Description]
- **Pattern**: [trope name]
- **Published precedent**: [multiple books using this pattern]
- **Why it's fine**: [explanation]

## Summary
- Total scenes: [count]
- MIRROR: [count] (must rework)
- ECHO: [count] (should adjust)
- TROPE: [count] (acceptable)
- ORIGINAL: [count] (no parallel detected)
```

---

## Anti-Patterns

- ❌ Flagging every trope as a problem — enemies-to-lovers, training arcs, and power awakenings are SUPPOSED to feel familiar at the trope level
- ❌ Only checking against one source — a scene might be fine relative to GoT but mirror a Red Rising scene
- ❌ Ignoring emotional sequence because the surface details differ — if the reader feels the same emotions in the same order for the same reasons, it's an echo
- ❌ Only checking "big" scenes — quiet character moments can echo just as strongly as action set pieces
- ❌ Being so aggressive that no scene passes — virtually every scene in genre fiction uses SOME established pattern; the question is specificity
- ❌ Skipping romantic scenes because "all romance scenes are similar" — there's a massive difference between "trope usage" and "copying Maas's exact cabin scene beat structure"

---
name: continuity-checker
description: "Track and flag continuity errors across fiction manuscripts. Builds timelines, tracks character details, monitors plot threads, verifies information flow, and catches contradictions between chapters."
argument-hint: "Describe what to check, e.g. 'full continuity audit of chapters 1-12' or 'verify the timeline in act two'"
user-invocable: true
---
# Continuity-Checker — Manuscript Consistency Skill

Track every detail. Catch every contradiction. Maintain the reader's trust.

## When to Use

- Running a continuity pass on a complete or partial manuscript
- Checking a new chapter against established facts
- Verifying timeline consistency after structural edits
- Tracking character physical states (injuries, augmentations, equipment) across scenes
- Ensuring plot threads are resolved or deliberately left open
- Checking that characters only know what they've been told or witnessed

---

## Continuity Tracking Systems

### System 1: Master Timeline

Build a chronological timeline of every event in the manuscript.

```markdown
## Timeline

| Chapter | Day/Time | Event | Characters Present | Notes |
|---------|----------|-------|-------------------|-------|
| Ch 1 | Day 1, morning | Sera arrives at Vantage Station | Sera, Docking Officer | Establishes 3-day transit from Meridian |
| Ch 1 | Day 1, afternoon | Assignment to Wing Seven | Sera, Commander Thal | First meeting with love interest |
| Ch 2 | Day 2, 0600 | First training simulation | Sera, Kael, Wing Seven | Sera fails the sim |
| ... | ... | ... | ... | ... |
```

**Timeline rules to verify:**
- Events happen in logical sequence (no time travel unless intended)
- Travel times match established distances and ship speeds
- Characters can't be in two places at once
- Day/night cycles are consistent for the location
- Time-sensitive elements (injuries healing, fuel reserves, communication delays) track correctly
- "Three days later" statements match the actual passage of events

### System 2: Character State Tracker

Track the physical and emotional state of each character across the manuscript.

```markdown
## Character State: [Name]

### Physical
| Chapter | State Change | Details | Resolved? |
|---------|-------------|---------|-----------|
| Ch 3 | Injured | Broken ribs from combat sim | |
| Ch 5 | Healing | Ribs wrapped, limited mobility | |
| Ch 8 | Recovered | Full mobility restored (nanomed treatment Ch 7) | ✅ |
| Ch 11 | New scar | Burn scar on left forearm from shield failure | Permanent |

### Emotional
| Chapter | State | Trigger | Carrying Forward? |
|---------|-------|---------|-------------------|
| Ch 4 | Betrayal/anger | Learns Kael's faction secret | Yes — unresolved through Ch 9 |
| Ch 10 | Tentative trust | Kael saves her life in Ch 9 | Shifts dynamic |

### Equipment / Possessions
| Chapter | Item | Status |
|---------|------|--------|
| Ch 1 | Mother's pendant | Wearing — mentioned on arrival |
| Ch 6 | Mother's pendant | Should be present but not mentioned (flag?) |
| Ch 14 | Mother's pendant | Clutches it during crisis — good callback |

### Knowledge
| Chapter | Learns | Source | Implications |
|---------|--------|--------|-------------|
| Ch 3 | Wing Seven has highest casualty rate | Briefing | Raises stakes |
| Ch 7 | Kael is from enemy faction | Overheard conversation | Creates trust crisis |
| Ch 12 | Kael defected to protect his sister | Kael's confession | Reframes Ch 7 revelation |
```

### System 3: Location Consistency

Track details about every location to catch contradictions.

```markdown
## Location: [Name]

### Established Details
| Detail | First Mentioned | Chapter | Verified Consistent? |
|--------|----------------|---------|---------------------|
| Docking bay on level 12 | Arrival scene | Ch 1 | Check all references |
| Mess hall seats 200 | Described during first meal | Ch 2 | |
| Observation deck faces starboard | Romantic scene | Ch 9 | Verify Ch 15 reference |
| Gravity is 0.8g | Mentioned in training | Ch 3 | Check if characters ever feel "heavy" |

### Contradictions Found
| Detail | Chapter A | Chapter B | Issue |
|--------|-----------|-----------|-------|
| Corridor color | Ch 2: "grey walls" | Ch 8: "white corridors" | Inconsistent — pick one |
```

### System 4: Plot Thread Tracker

Every plot thread opened must be tracked to resolution.

```markdown
## Plot Threads

| # | Thread | Opened | Status | Resolved | Notes |
|---|--------|--------|--------|----------|-------|
| 1 | Who sabotaged the training sim? | Ch 4 | 🔴 Open | — | Must resolve by Act III |
| 2 | Sera's recurring headaches | Ch 2 | 🟡 Developing | — | Connected to psionic awakening? |
| 3 | Missing supply shipments | Ch 6 | ✅ Resolved | Ch 11 | Revealed as faction sabotage |
| 4 | Kael's sister mentioned once | Ch 8 | 🔴 Open | — | Chekhov's gun — must fire or remove |
| 5 | The locked sector of the station | Ch 3 | 🔴 Open | — | Mentioned twice, never explored |
```

**Thread rules:**
- Every thread opened must be resolved, deliberately left for a sequel (flagged), or removed
- Chekhov's Gun: If a detail is emphasized, it must matter later
- Red herrings must be acknowledged — the reader should eventually understand why they were there
- Threads left for sequels should have at least a partial resolution in the current book

### System 5: Information Flow Audit

Characters can only know what they've witnessed, been told, or logically deduced.

```markdown
## Information Flow: [Character]

| Information | How Acquired | Chapter | First Used | Valid? |
|-------------|-------------|---------|-----------|--------|
| Kael's real faction | Overheard in corridor | Ch 7 | Ch 8 — confronts him | ✅ |
| Supply route schedule | Never shown acquiring | — | Ch 11 — uses in plan | ❌ FLAG |
| Station override codes | Given by Commander Thal | Ch 13 | Ch 14 — uses in climax | ✅ |
```

**Common information flow errors:**
- Character knows something they were never told or shown learning
- Character forgets something they were explicitly told
- Character references a conversation they weren't present for
- Character uses a skill or ability not previously established
- Character makes a deduction that requires information they don't have

---

## Continuity Audit Checklist

Run through this checklist for each pass:

### Characters
- [ ] Physical descriptions consistent (eye color, hair, scars, height, build)
- [ ] Injuries persist appropriately and heal at realistic rates
- [ ] Character names and nicknames are consistent (no accidental name changes)
- [ ] Ranks and titles are used correctly and updated after promotions
- [ ] Character ages are consistent with timeline
- [ ] Augmentations/abilities are used consistently (no forgotten powers, no new ones without explanation)
- [ ] Emotional states carry between scenes (no miraculous mood recovery without reason)

### Timeline
- [ ] Events happen in logical chronological order
- [ ] Time references ("three days ago," "last week") are accurate
- [ ] Travel times match established speeds and distances
- [ ] Day/night cycles are consistent with location
- [ ] Seasons/rotations match (for planets with non-standard cycles)
- [ ] Character schedules don't conflict (can't be in two places)

### Locations
- [ ] Physical descriptions are consistent between scenes
- [ ] Distances and travel times within locations are realistic
- [ ] Environmental conditions (gravity, atmosphere, temperature) are consistent
- [ ] Layout makes spatial sense (directions, levels, adjacencies)

### Plot
- [ ] All opened threads are tracked
- [ ] Foreshadowing pays off (or is intentional misdirection)
- [ ] Cause and effect are logical
- [ ] Information characters act on has been properly established
- [ ] Consequences of major events persist (a battle should leave damage, politically and physically)

### Technology
- [ ] Ship names are consistent
- [ ] Weapon capabilities don't change between scenes
- [ ] Communication systems follow established rules
- [ ] Medical technology is used consistently (healing time, limitations)
- [ ] FTL/travel rules are never violated

---

## Continuity Report Format

```markdown
# Continuity Report
**Manuscript**: [Title]
**Chapters reviewed**: [Range]
**Pass number**: [#]

## Contradictions Found
| # | Type | Location A | Location B | Issue | Severity | Fix |
|---|------|-----------|-----------|-------|----------|-----|
| 1 | Physical detail | Ch 2, p3 | Ch 9, p7 | Eye color changes from grey to blue | 🔴 | Standardize to one |
| 2 | Timeline | Ch 5 | Ch 6 | "Two days" doesn't match events | 🟡 | Adjust to three days |

## Unresolved Threads
| # | Thread | Opened | Last Referenced | Risk |
|---|--------|--------|----------------|------|
| 1 | [Description] | Ch [#] | Ch [#] | [Forgotten? Sequel? Remove?] |

## Information Flow Errors
| # | Character | Information | Issue | Chapter |
|---|-----------|-------------|-------|---------|
| 1 | [Name] | [What they know] | [How they know it is unexplained] | Ch [#] |

## Timeline Issues
[Any chronological problems found]

## Location Inconsistencies
[Any spatial or environmental contradictions]

## Clean Areas
[Sections with no continuity issues — good to go]
```

---

## Anti-Patterns

- ❌ Flagging stylistic choices as continuity errors — consistency checking is about facts, not preferences
- ❌ Demanding rigid precision where narrative flexibility is fine — "a few days later" doesn't need to be "exactly 72 hours"
- ❌ Missing the forest for the trees — a minor hair color inconsistency matters less than a plot thread that disappears
- ❌ Ignoring emotional continuity — a character can't be devastated in one scene and cheerful in the next without explanation
- ❌ Over-tracking trivial details — focus on what the reader will notice and what affects the story

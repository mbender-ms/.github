---
name: style-sheet
description: "Build and maintain a professional fiction style sheet tracking character names, physical descriptions, locations, timeline, invented terminology, spelling decisions, formatting rules, and series continuity. The living reference document for all editorial passes."
argument-hint: "Describe what you need, e.g. 'build a style sheet from the manuscript' or 'update the style sheet with chapter 12 additions'"
user-invocable: true
---
# Style-Sheet — Professional Fiction Style Sheet

The single source of truth for every editorial decision in the manuscript. Built during copyediting, maintained across all passes, and carried forward into sequels.

## When to Use

- At the start of copyediting to build the initial style sheet
- During any editorial pass to record new decisions
- When checking consistency across chapters
- When starting a sequel — the style sheet carries forward
- When onboarding a new editor or proofreader to the project

---

## What a Style Sheet Is

A style sheet is a living document that records every editorial decision specific to this manuscript. It's not a style guide (like CMOS) — it's the layer ON TOP of the style guide that captures:

- How invented names are spelled and capitalized
- What formatting conventions the manuscript uses
- What the timeline of events is
- What each character looks like and how they're related
- Every decision that might need to be referenced later

Without a style sheet, consistency is impossible. With one, it's effortless.

---

## Style Sheet Template

```markdown
# Style Sheet: [Manuscript Title]
**Author**: [Name]
**Series**: [Series name, book number]
**Editor**: [Name]
**Created**: [Date]
**Last updated**: [Date]
**Style guide**: Chicago Manual of Style, 18th edition
**Dictionary**: Merriam-Webster (US English)

---

## 1. General Style Decisions

### Spelling Preferences
| Word | Preferred Form | Notes |
|------|---------------|-------|
| toward/towards | toward | US standard |
| gray/grey | gray | US standard |
| okay/OK | okay | Narrative; "OK" in dialogue if character uses it |
| [invented term] | [exact spelling] | [capitalization rule] |

### Punctuation Decisions
- Serial comma: YES
- Em dash style: closed (no spaces) — like this
- Ellipsis style: spaced (. . .) or glyph (…): [CHOOSE]
- Single vs. double quotes: Double (US standard)
- Italics for internal thought: [YES/NO]
- Italics for ship names: [YES/NO]
- Italics for foreign/alien words: [YES/NO — and list of exceptions]

### Number Treatment
- Spell out one through one hundred in narrative
- Numerals for technical readouts, coordinates, timestamps
- Spell out ordinals: "first," "twenty-third" (not "1st," "23rd")
- Time format: [twelve-hundred hours / 1200 / noon]
- Date format: [how dates are expressed in this universe]

### Formatting Conventions
- Scene break marker: [*** / ### / ornamental]
- Comm/radio dialogue: [format — e.g., italics, different punctuation]
- Neural-link communication: [format]
- Computer/AI text: [format]
- Flashbacks: [how marked — italics, tense change, none]
- Documents/letters within text: [format]
- Alien language: [format]

---

## 2. Characters

### Main Characters
| Character | Full Name | Nicknames | Age | Physical Description | Distinguishing Features |
|-----------|-----------|-----------|-----|---------------------|----------------------|
| [Name] | [Full] | [List] | [Age] | [Key features] | [Scars, augmentations, etc.] |

### Character Relationships
| Character A | Relationship | Character B | Notes |
|------------|-------------|-------------|-------|
| [Name] | [type: romantic, sibling, commander, rival] | [Name] | [Established in ch. X] |

### Character Details
For each significant character:
```
### [Character Name]
- Spelling: [exact spelling — especially important for unusual names]
- Rank/title: [and how it's formatted — capitalized? abbreviated?]
- Physical: [eye color, hair, build, scars, augmentations]
- Background: [faction, homeworld, training]
- Speech patterns: [dialect, verbal tics, vocabulary]
- Key possessions: [weapons, keepsakes, ship]
- Changes across manuscript: [injuries gained, rank changes, augmentation additions]
```

---

## 3. Locations

| Location | Type | Key Details | First Mentioned |
|----------|------|-------------|----------------|
| [Name] | [Station/Ship/Planet/etc.] | [Layout, gravity, atmosphere, distinctive features] | Ch. [#] |

### Location Details
For each significant location:
```
### [Location Name]
- Spelling: [exact]
- Type: [station, ship, planet, moon, habitat]
- Physical details: [size, layout, gravity, notable features]
- Inhabitants: [who's here]
- Deck/section names: [if a ship or station — list named areas]
```

---

## 4. Timeline

| Chapter | Day/Time | Event | Characters Present | Notes |
|---------|----------|-------|--------------------|-------|
| Ch. 1 | Day 1, AM | [Event] | [Who] | |
| Ch. 1 | Day 1, PM | [Event] | [Who] | |
| Ch. 2 | Day 2 | [Event] | [Who] | |

### Time-Critical Details
- FTL cooldown: [duration]
- Communication delay between [A] and [B]: [duration]
- Travel time from [X] to [Y]: [duration]
- [Character]'s injury healing time: [duration, treatment started ch. X]

---

## 5. Terminology / World-Building

| Term | Definition | Capitalized? | First Used | Notes |
|------|-----------|-------------|-----------|-------|
| [term] | [definition] | [Yes/No] | Ch. [#] | [Usage notes] |

### Technology
| Technology | How It Works | Limitations | Formatting |
|-----------|-------------|-------------|-----------|
| [FTL system name] | [Brief] | [Cooldown, fuel, etc.] | [Capitalized? Italicized?] |
| [Bond/link system] | [Brief] | [Range, cost, etc.] | |
| [Weapon type] | [Brief] | [Ammo, range, etc.] | |

### Ranks and Titles
| Rank | Abbreviation | Capitalization Rule |
|------|-------------|-------------------|
| Commander | Cmdr. | Capitalized before name: "Commander Thal." Lowercase generic: "the commander." |
| Admiral | Adm. | Same pattern |

### Factions
| Faction | Full Name | How Referenced | Notes |
|---------|-----------|---------------|-------|
| [Name] | [Full formal name] | [How characters refer to them] | [Spelling, capitalization] |

---

## 6. Cross-Reference Alerts

Items that need extra vigilance for consistency:

| Item | Rule | Risk |
|------|------|------|
| [Character] scar on left forearm | Gained Ch. 8 | Must be mentioned or acknowledged in all subsequent physical descriptions |
| [Ship name] | Always italicized | Check every instance |
| [FTL cooldown] | 3 hours | Verify all FTL usage intervals |
| [Bond range] | Unlimited emotional; 500m physical sensation | Check all bond scenes |

---

## 7. Series Continuity Notes

[For multi-book series — facts that must carry into the next book]

| Fact | Established In | Must Carry Forward |
|------|---------------|-------------------|
| [Character] has neural implant | Book 1, Ch. 14 | Must be present in Book 2 |
| [Faction] treaty signed | Book 1, Ch. 18 | Political backdrop for Book 2 |
| [Character] rank promotion | Book 1, Ch. 20 | New rank in Book 2 |
```

---

## Building the Style Sheet

### Initial Build (During First Copyedit)
1. Read through the manuscript noting every unique name, term, location, and formatting decision
2. Record character details as they appear — note chapter of first mention
3. Build the timeline event by event
4. Record spelling and formatting decisions as you make them
5. Flag anything inconsistent for resolution

### Updating (Ongoing)
- Add entries during every editorial pass
- Update character states when they change (injuries, rank changes, relationship shifts)
- Record new author query resolutions
- Note formatting decisions made during revision

### For Sequels
- Copy the style sheet from the previous book
- Mark entries as "carry forward" or "resolved in Book N"
- Add new characters, locations, and terms
- Update timeline to include inter-book events

---

## Anti-Patterns

- ❌ Building the style sheet from memory — build it from the TEXT. Read and record, don't assume.
- ❌ Incomplete character entries — track physical details, not just names. Eye color inconsistencies are real.
- ❌ Ignoring the timeline — the timeline is the style sheet's most valuable section. Build it meticulously.
- ❌ Forgetting invented terminology — every made-up word, rank, and place name must be recorded with its exact spelling and capitalization
- ❌ Not updating — a style sheet that falls out of date is worse than no style sheet, because people trust it
- ❌ Over-documenting trivial decisions — focus on what could vary. "The" is always spelled "the" — you don't need that in the style sheet

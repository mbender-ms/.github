---
name: prose-name-scan
description: "Scan finished manuscript prose scene-by-scene for character names, nicknames, titles, and invented terms that were introduced during drafting and weren't vetted by the pre-writing name scan. Cross-references against prior scan results."
argument-hint: "Specify scope, e.g. 'scan full manuscript for unvetted names' or 'check chapters 1-9 for new names not in the character bible'"
user-invocable: true
---
# Prose-Name-Scan — Manuscript-Level Name Verification

Scan the finished manuscript for every proper noun — including names that emerged during drafting and weren't in the original character bible or worldbuilding documents.

## When to Use

- After completing a manuscript draft, before first edit
- After a major revision pass that may have introduced new characters or locations
- When a new character, ship, location, or term was added during drafting without vetting
- As part of the manuscript originality checkpoint (before sending to fiction-editor)

---

## Why This Exists (Separate From name-originality-scan)

The pre-writing `name-originality-scan` checks the planned names in worldbuilding documents. But during drafting:
- Minor characters get named on the fly ("the bartender needed a name")
- Locations get christened in the moment ("the docking bay needed a designation")
- Nicknames and call signs emerge from dialogue
- Slang terms and informal names develop organically
- Characters refer to each other by titles, shortened names, or insults that weren't planned

These unplanned names are the highest risk for accidental collisions because they were never checked.

---

## Scan Process

### Step 1: Extract All Proper Nouns From Manuscript
Pull every name, title, place, and term from the actual prose:
- Character first names and surnames
- Nicknames and call signs used in dialogue
- Informal references ("the Commander," "the twin," "that Vasik bastard")
- Location names (planets, stations, rooms, districts, ships)
- Technology and ability terms used in prose
- Faction and institutional references
- Any capitalized invented word

### Step 2: Cross-Reference Against Prior Scan
Compare against the results of the pre-writing `name-originality-scan`:

| Status | Meaning |
|---|---|
| **CLEARED** | Name was in the pre-writing scan and rated CLEAR or NOTE-accepted |
| **PREVIOUSLY FIXED** | Name was flagged and replaced during pre-writing — verify the replacement is being used |
| **NEW — UNVETTED** | Name does NOT appear in any prior scan results — needs checking |
| **VARIANT** | A variant/nickname of a cleared name — check the variant itself |

### Step 3: Check All NEW/UNVETTED Names
Run the same checks as `name-originality-scan`:
- Exact match against published works knowledge base
- Phonetic similarity check
- One-letter-swap check
- Pattern check (does this new name create a naming pattern that echoes a specific source?)

### Step 4: Check for Regression
Verify that names that were REPLACED during pre-writing aren't still appearing in the manuscript:
- Search for old/replaced names that should no longer exist
- Flag any instances where the old name slipped through

### Step 5: Compile Report

---

## Report Format

```markdown
# Prose Name Scan — [Manuscript Title]
Date: [scan date]
Chapters scanned: [range or "full manuscript"]
Total unique names found: [count]

## Status Breakdown
- CLEARED (pre-vetted): [count]
- PREVIOUSLY FIXED (verified): [count]
- NEW — UNVETTED: [count] ← focus area
- VARIANTS of cleared names: [count]

## 🆕 Unvetted Names Requiring Check
| Name | Category | First Appears | Context | Check Result |
|------|----------|---------------|---------|--------------|
| [name] | [character/place/etc.] | Ch. [X], p. [Y] | [brief context] | BLOCK/WARN/NOTE/CLEAR |

## 🔴 BLOCK — Exact Matches (Unvetted Names)
| Name | Source Match | Published Work | First Appears |
|------|-------------|----------------|---------------|

## 🟡 WARN — Close Matches (Unvetted Names)
| Name | Similar To | Published Work | Match Type | First Appears |
|------|-----------|----------------|------------|---------------|

## ⚠️ Regression — Old Names Still Present
| Old Name | Should Be | Occurrences Found | Chapters |
|----------|-----------|-------------------|----------|

## ✅ All Clear
[List of unvetted names that passed all checks]

## Summary
- New names checked: [count]
- BLOCK: [count]
- WARN: [count]
- Regressions: [count]
- Clear: [count]
```

---

## Dialogue-Specific Checks

Pay special attention to names used IN DIALOGUE because:
- Characters may use informal names not in the bible ("Everyone calls him Ren" — is "Ren" in any published work?)
- Insults or nicknames may reference real-world or fictional cultural touchstones
- Military ranks + names create compound references ("Commander Kael" — check both parts)
- Terms of endearment in romantic scenes should be checked for uniqueness

---

## Anti-Patterns

- ❌ Only checking names that are capitalized — dialogue may use lowercase for nicknames or slang
- ❌ Assuming every name in the character bible made it into the manuscript correctly — regression happens
- ❌ Skipping minor characters because "no one will notice" — dedicated fans of the source material WILL notice
- ❌ Not checking compound terms (rank + name, title + name) as a unit
- ❌ Only checking the name in isolation — "Kael" might be fine alone but "Kael of House [X]" might echo a specific combination

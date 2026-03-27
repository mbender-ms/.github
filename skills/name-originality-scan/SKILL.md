---
name: name-originality-scan
description: "Scan worldbuilding documents, character bibles, and outlines for character names, place names, faction names, ship names, and invented terms that are exact matches or dangerously close to names in published SFF and romantasy works."
argument-hint: "Specify what to scan, e.g. 'scan the full character bible' or 'check all names in the world bible and concept doc'"
user-invocable: true
---
# Name-Originality-Scan — Published Name Collision Detection

Compare every proper noun in the project's worldbuilding and planning documents against a comprehensive knowledge base of published works in science fiction, fantasy, and romantasy.

## When to Use

- After creating or updating a character bible, world bible, or concept document
- Before beginning manuscript drafting (pre-writing checkpoint)
- When introducing new characters, locations, factions, or terms during outlining
- As a final pre-draft check on the complete planning package

---

## What Gets Scanned

Extract and check EVERY proper noun in the target documents:

| Category | Examples |
|---|---|
| **Character names** | First names, surnames, titles, nicknames, call signs |
| **Place names** | Planets, stations, cities, regions, landmarks, ships |
| **Faction names** | Dominions, Pillars, military units, political bodies, academies |
| **Invented terms** | Technology names, ability names, species names, calendar terms |
| **Ship/vehicle names** | Flagships, fleet designations, personal craft |

---

## Knowledge Base — Published Works to Check Against

### Primary (same genre — highest risk):
- **Sarah J. Maas**: ACOTAR series, Throne of Glass, Crescent City (all character/place/court names)
- **Rebecca Yarros**: Empyrean series (dragon names, cadet names, wing designations)
- **Susanne & Caroline Peckham**: Zodiac Academy, Ruthless Boys, Darkmore Penitentiary (all character/house/order names)
- **Callie Hart**: Brimstone, Quicksilver (character names)
- **Frank Herbert**: Dune series (houses, planets, organizations, terms — Arrakis, Atreides, Bene Gesserit, melange, etc.)
- **Brian Herbert**: Extended Dune (additional names from prequels/sequels)
- **George R.R. Martin**: ASOIAF (houses, characters, locations — Stark, Lannister, Winterfell, King's Landing, etc.)

### Secondary (adjacent genre — moderate risk):
- **Pierce Brown**: Red Rising (colors, house names, character names)
- **James S.A. Corey**: The Expanse (ship names, faction names, character names)
- **Isaac Asimov**: Foundation (organization names, planet names)
- **Brandon Sanderson**: Cosmere (magic system terms, world names)
- **Suzanne Collins**: Hunger Games (district names, character names)
- **Leigh Bardugo**: Grishaverse (grisha orders, character names)
- **Victoria Aveyard**: Red Queen (blood types, house names)
- **Amie Kaufman & Jay Kristoff**: Illuminae Files (ship names, AI names)

### Tertiary (wider SFF — low risk but check):
- Major Star Wars proper nouns (Jedi, Sith, well-known planet/character names)
- Major Star Trek proper nouns (Federation, Klingon, well-known names)
- Major Marvel/DC sci-fi names where applicable

---

## Similarity Detection Levels

### BLOCK — Exact Match (must change immediately)
- Name is identical to a published character/place/term
- Example: Using "Rhysand" → exact match to ACOTAR
- Example: Using "Atreides" → exact match to Dune
- **Action**: Must be replaced before any further work proceeds

### WARN — Close Match (strongly recommend changing)
Triggers when any of:
- **Phonetic twin**: Sounds nearly identical when spoken aloud (e.g., "Rysand" ≈ "Rhysand")
- **One-letter swap**: Differs by a single character (e.g., "Feyre" → "Feyra")
- **Anagram or rearrangement**: Letters rearranged (e.g., "Darrow" → "Warrod")
- **Obvious portmanteau**: Combined from two known names in the same source (e.g., "Rhysfeyre")
- **Same root + suffix**: Same base with a different ending (e.g., "Targaryen" → "Targarian")
- **Action**: Present alternatives. Author may choose to keep with justification, but default is replace.

### NOTE — Faint Echo (awareness only)
- Name shares a root, feel, or phonetic quality with a published name but is clearly distinct
- Common linguistic roots that happen to overlap (e.g., "Astra" is generic Latin, not owned by any one work)
- Genre-standard naming conventions (e.g., harsh consonant clusters for warrior cultures)
- **Action**: Log for awareness. No change required unless pattern accumulates.

---

## Scan Process

1. **Extract**: Pull every proper noun from all target documents into a master list
2. **Categorize**: Sort by type (character, place, faction, term)
3. **Check primary sources**: Compare each name against primary knowledge base
4. **Check secondary sources**: Compare against secondary knowledge base
5. **Phonetic analysis**: Run phonetic similarity check (how does it SOUND, not just how it's spelled)
6. **Pattern check**: Look for naming PATTERNS that echo a specific source (e.g., all faction names ending in "-yen" echoes Targaryen)
7. **Compile report**: Generate structured findings

---

## Report Format

```markdown
# Name Originality Scan — [Document Set]
Date: [scan date]
Documents scanned: [list]
Total names checked: [count]

## 🔴 BLOCK — Exact Matches
| Name | Category | Source Match | Published Work |
|------|----------|-------------|----------------|
| [name] | [type] | [exact match] | [book/series] |

## 🟡 WARN — Close Matches
| Name | Category | Similar To | Published Work | Match Type |
|------|----------|-----------|----------------|------------|
| [name] | [type] | [similar name] | [book/series] | [phonetic/one-letter/anagram/etc.] |

## 🔵 NOTE — Faint Echoes
| Name | Category | Echoes | Published Work | Notes |
|------|----------|--------|----------------|-------|
| [name] | [type] | [echo] | [book/series] | [why it's probably fine] |

## ✅ CLEAR — No Issues
[count] names checked with no matches found.

## Summary
- BLOCK: [count] (must fix)
- WARN: [count] (should fix)
- NOTE: [count] (awareness)
- CLEAR: [count]
```

---

## Anti-Patterns

- ❌ Only checking exact spelling — phonetic matches are just as dangerous ("Khal Drogo" → "Kal Drago" is NOT original)
- ❌ Ignoring minor characters from published works — readers will notice ("Oh that's just like [minor character] from Zodiac Academy")
- ❌ Only checking protagonist names — place names and tech terms matter too
- ❌ Skipping the secondary sources — Red Rising and The Expanse share the exact same genre space
- ❌ Accepting "it's a common name" without verification — confirm it actually IS common, not just used in one famous book

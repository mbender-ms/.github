---
name: name-replacement
description: "Generate replacement candidates for flagged names that maintain the story's intent, fit in-world naming conventions, and are verifiably original. Update all occurrences across all documents and produce a change log."
argument-hint: "Provide the flagged name and context, e.g. 'replace character name Vasik — WARN level, too close to Vaxis from Red Rising' or 'batch replace all BLOCK-level names from the scan report'"
user-invocable: true
---
# Name-Replacement — Original Name Generation & Propagation

Generate replacement names for flagged entries from originality scans, then propagate the change across every document in the project.

## When to Use

- After a name-originality-scan or prose-name-scan produces BLOCK or WARN findings
- When the author decides to replace a NOTE-level name proactively
- When a batch of names needs replacement (post-scan remediation pass)

---

## Replacement Generation Process

For each flagged name, follow this sequence:

### Step 1: Understand the Name's Role
- **Character role**: Protagonist, antagonist, love interest, mentor, minor character?
- **Cultural context**: Which Dominion, Pillar, or faction? What naming conventions apply?
- **Phonetic feel**: Harsh consonants (warrior), flowing vowels (ethereal), clipped (military)?
- **Reader function**: Is this name said aloud a lot? Does it need to be short and punchy, or can it be longer?
- **Emotional register**: Should it feel warm, cold, dangerous, trustworthy, alien?

### Step 2: Generate 5+ Candidates
Each candidate must satisfy ALL of:

| Criterion | Check |
|---|---|
| **No published match** | Not used in any SFF/romantasy series in the primary or secondary knowledge base |
| **No phonetic twin** | Doesn't sound like a published name when spoken aloud |
| **Fits in-world conventions** | Matches the naming patterns established for its faction/culture |
| **Pronounceable** | A reader encountering it for the first time can sound it out correctly |
| **Memorable** | Distinctive enough that readers won't confuse it with other characters |
| **Distinct from other project names** | Doesn't sound too similar to OTHER characters in this series |

### Step 3: Present with Rationale
For each candidate, explain:
- Why it fits the character/place/faction
- What linguistic roots or sounds it draws from
- How it avoids the flagged collision
- Any potential concerns (too similar to another project name, hard to pronounce, etc.)

### Step 4: Author Selects
Present candidates to the author. Author picks one (or requests another round).

### Step 5: Propagate
Replace EVERY occurrence across ALL project documents:
- Character bible
- World bible
- Concept documents
- Political maps
- Beat sheets and outlines
- Series arc documents
- Any manuscript chapters already drafted
- Style sheets and tracking documents

---

## Naming Convention Guidelines by Context

### Military / Dominion Names
- Clipped, angular sounds: hard consonants (k, t, d, v), minimal soft vowels
- Examples of the FEEL (not these exact names): Kael, Dren, Voss, Tarn
- Rank-influenced: higher ranks may have longer, more formal names

### Academy / Scholar Names
- Blend of formal and colloquial: full names for ceremony, shortened for use
- Can have softer sounds than military names
- May include titles or honorifics

### Faction / Pillar Names
- Should feel weighty and institutional — these are names that have survived centuries
- Avoid names that are common English words
- Should work as adjectives ("the Vasik fleet" → "the [replacement] fleet")

### Technology / Invented Terms
- Should feel like they BELONG to this universe
- Consistent linguistic roots across related technologies
- Avoid terms that are obviously mashed-together English words

---

## Change Log Format

```markdown
# Name Replacement Log — [Date]

## Changes Applied
| # | Old Name | New Name | Category | Reason | Files Modified | Occurrences |
|---|----------|----------|----------|--------|----------------|-------------|
| 1 | [old] | [new] | Character | BLOCK: exact match to [source] | [list] | [count] |
| 2 | [old] | [new] | Place | WARN: phonetic match to [source] | [list] | [count] |

## Candidates Considered (for reference)
### [Old Name] → [New Name]
- Candidate A: [name] — [why it was/wasn't selected]
- Candidate B: [name] — [why it was/wasn't selected]
- Candidate C: [name] — [why it was/wasn't selected]

## Verification
- [ ] All BLOCK names replaced
- [ ] All WARN names replaced (or explicitly retained with justification)
- [ ] No new collisions introduced by replacement names
- [ ] All documents updated consistently
- [ ] Character bible cross-references updated
- [ ] Style sheet updated with new names
```

---

## Anti-Patterns

- ❌ Generating names that are just anagrams of the flagged name — that's not original, that's rearranged plagiarism
- ❌ Replacing a name without checking the replacement against the same knowledge base — you might be trading one collision for another
- ❌ Only updating the character bible but not the outline or beat sheets — partial propagation creates confusion
- ❌ Choosing a replacement that sounds too similar to another character IN THIS PROJECT — readers will confuse "Kael" and "Kade"
- ❌ Making all replacement names sound like they're from the same culture when the story has multiple cultures

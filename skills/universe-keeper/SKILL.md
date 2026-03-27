---
name: universe-keeper
description: "Verify that fiction prose obeys established world rules, physics, technology constraints, and faction logic. Catches science errors, magic-system violations, and world-building contradictions in hard sci-fi manuscripts."
argument-hint: "Describe what to verify, e.g. 'check the space battle in chapter 9 for physics errors' or 'verify all FTL usage matches the established rules'"
user-invocable: true
---
# Universe-Keeper — World Consistency Enforcement Skill

Guard the rules of the story universe. Every technology, every physical law, every faction behavior must follow the rules the author established.

## When to Use

- Running a universe-consistency pass on a manuscript
- Verifying a space battle, technology scene, or world-building sequence
- Checking that psionic/bond abilities follow their defined constraints
- Ensuring faction behavior aligns with established politics and culture
- Verifying scientific accuracy in hard sci-fi elements
- Reviewing a new chapter against the world bible

---

## Rule Categories

### Category 1: Hard Physics

These are real physics that hard sci-fi must respect unless explicitly overridden by established in-universe technology.

**Space and Vacuum**
- No sound in vacuum. Inside ships and stations, yes. Outside, silence.
- Explosive decompression is Hollywood myth. Real decompression is dangerous but not explosive.
- Vacuum exposure: consciousness lost in ~15 seconds, death in ~90 seconds without protection.
- Temperature in space is complicated — shadow is cold, direct starlight is hot, but heat loss is slow (radiation only, no convection).

**Motion and Acceleration**
- Newton's laws apply. Ships that accelerate must decelerate to stop. No "parking" in space without thrust.
- Humans feel acceleration. 1g is comfortable. 2-3g is painful and impairs function. 6g+ causes unconsciousness. Sustained high-g requires gel-couches, drugs, or augmentation.
- Orbital mechanics: orbits are ellipses, not circles. Changing orbits requires delta-v. You can't just "fly to" something in orbit.
- There's no drag in space. A ship at velocity stays at velocity until thrust is applied.

**Communication**
- Light speed is the speed limit for information (unless the story has FTL comms — check world bible).
- Light-delay examples: Earth to Moon = 1.3 seconds. Earth to Mars = 4-24 minutes. Interstellar = years.
- If the story has ansible/quantum-entangled comm, verify it operates within its established rules (bandwidth limits, cost, range).

**Weapons and Combat**
- Lasers travel at light speed — no dodging, no visible beams in vacuum (no medium to scatter light).
- Kinetic weapons have no range limit in space — a bullet travels forever without atmosphere.
- Missiles are the most versatile space weapon — they can maneuver, carry warheads, and operate independently.
- Combat ranges in space would be enormous — likely thousands of kilometers for beam weapons, more for kinetics.
- Heat management is a critical combat factor — weapons generate waste heat, ships must radiate it.

**Biology in Space**
- Radiation is a constant threat outside atmosphere/magnetosphere. Ships need shielding.
- Bone and muscle atrophy in zero-g without exercise or artificial gravity.
- Psychological effects of long-duration spaceflight: isolation, claustrophobia, sensory deprivation.
- Different gravity affects everything: movement, fluid distribution in the body, cooking, fire behavior.

### Category 2: Established Technology Rules

These are rules the author defined. They must be internally consistent.

**For each technology, verify:**

```markdown
### [Technology Name]

**What it does**: [Capability]
**How it works**: [Mechanism — even if handwaved, there should be consistency]
**Limitations**: [What it CANNOT do]
**Cost**: [Energy, time, materials, biological cost]
**Who has access**: [Universally available? Restricted? Rare?]
**Failure modes**: [What happens when it breaks?]

**Violations to watch for**:
- Technology exceeding its established limits without explanation
- Cost/limitations ignored for plot convenience
- Technology used by characters/factions who shouldn't have access
- Inconsistent failure modes (works perfectly in Ch 3, fails at dramatic moment in Ch 12 without mechanical reason)
```

**Common technology categories to track:**
- FTL travel system (speed, cost, limitations, fuel)
- Communication system (speed, bandwidth, range)
- Weapons systems (types, ranges, capabilities, counters)
- Defensive systems (shields, armor, point defense — their limits)
- Medical technology (what it can/can't heal, how fast, at what cost)
- Bond/link system (range, capability, cost, limitations, how it activates)
- AI/computing (capability level, sentience rules, limitations)
- Augmentation (what's available, side effects, social implications)

### Category 3: Faction and Political Rules

Factions behave according to their established culture, values, and capabilities.

**For each faction, verify:**
- Military doctrine is consistent (a defensive-minded faction doesn't suddenly launch reckless offensives without in-story justification)
- Cultural values are reflected in character behavior (characters from rigid hierarchies don't casually disrespect authority without it being A Moment)
- Resource capabilities match their actions (a resource-poor faction can't field massive fleets)
- Political relationships are consistent (allies don't suddenly become enemies without cause)
- Internal politics are reflected (factions have doves and hawks, progressives and traditionalists)

### Category 4: Bond/Psionic System Rules

If the story includes psionic abilities or neural bonds, these need the strictest consistency — they're the story's "magic system" equivalent.

**Verify:**
- Abilities have defined limits that are never exceeded without narrative cost
- New abilities don't appear without foreshadowing or in-universe explanation
- The cost of using abilities is consistently enforced (fatigue, pain, nosebleeds, neurological strain)
- Bond mechanics work the same way every time (range, what's transmitted, how it feels)
- Characters can't read/do more with their abilities than established in earlier chapters
- If abilities grow, the growth is earned and explained

---

## Universe Audit Process

### Step 1: Extract the Rule Set
Before checking the manuscript, compile the rules from:
- World bible (if one exists)
- Early chapters where rules are established
- Character sheets (for bond/ability rules)
- Any notes or outlines that define constraints

### Step 2: Build a Rule Registry

```markdown
## Universe Rule Registry

### Physics Overrides
[What real physics does this universe modify?]
| Rule | Override | Established In | Limits |
|------|---------|----------------|--------|
| Light speed | FTL via fold-space drive | Ch 1 | Requires fold-fuel; 3-hour cooldown |
| Communication | Quantum-entangled ansible | Ch 2 | Station-to-station only; no ship-to-ship |

### Technology Rules
[Key tech and constraints]

### Bond/Psionic Rules
[Abilities and their limits]

### Faction Rules
[Behavioral constraints by faction]
```

### Step 3: Read and Check
Go through the manuscript with the rule registry as reference. Flag every instance where:
- A rule is violated
- A rule is stretched without acknowledgment
- A new capability appears without establishment
- A cost/limitation is conveniently forgotten

### Step 4: Classify Findings

| Severity | Description | Example |
|----------|-------------|---------|
| 🔴 **Rule Break** | Directly contradicts an established rule | Ship folds space twice without cooldown |
| 🟡 **Soft Violation** | Pushes a rule without technically breaking it | Ability used at greater range than previously shown, without comment |
| 🟢 **Opportunity** | A place where enforcing rules would add drama | Character could be affected by light-delay here — adds tension |
| 🔵 **Undefined** | No rule exists for this situation — needs one | First time two bonded pairs interact — what happens? |

---

## Universe Report Format

```markdown
# Universe Consistency Report
**Manuscript**: [Title]
**Chapters reviewed**: [Range]
**Rule set version**: [Date compiled]

## Rule Violations
| # | Rule | Chapter | Passage | Violation | Severity | Fix |
|---|------|---------|---------|-----------|----------|-----|
| 1 | FTL cooldown is 3 hours | Ch 9 | "They folded again immediately" | No cooldown observed | 🔴 | Add time gap or acknowledge cost |
| 2 | Ansible is station-only | Ch 14 | "She messaged him from the shuttle" | Using ansible from non-station | 🔴 | Change to delayed comm or add relay |

## Undefined Situations
[Situations where no rule exists and one should be established]
| # | Situation | Chapter | Recommendation |
|---|-----------|---------|----------------|
| 1 | [Description] | Ch [#] | [Suggest a rule] |

## Physics Notes
[Hard physics issues]

## Missed Opportunities
[Places where enforcing world rules would improve the scene]
| # | Chapter | Opportunity |
|---|---------|-------------|
| 1 | Ch 7 | The character is in zero-g but never mentions disorientation — add sensory detail |

## Consistent Areas
[World rules that are well-maintained throughout — reinforce these]
```

---

## Quick-Reference: Common Violations in Hard Sci-Fi Romance

| Violation | Why It's Tempting | Why It Matters | Fix |
|-----------|-------------------|----------------|-----|
| Sound in space | Dramatic effect | Breaks immersion for sci-fi readers | Use vibration through hull, or silence for dramatic contrast |
| Instant communication across light-years | Plot needs information to flow fast | Undermines the "hard" in hard sci-fi | Use established comm system within its rules, or use delay as plot device |
| Ignoring acceleration effects | Romance scene on the bridge during maneuvers | Readers notice; it breaks body-awareness writing | Acknowledge the g-forces or set the scene during drift |
| Wounds that heal overnight | Need the character active next chapter | Undermines physical stakes | Use nanomed but give it a realistic timeframe; or let the character fight hurt |
| Bond abilities that expand as needed | Plot requires new capability | Feels like deus ex machina | Foreshadow new abilities; pay a cost for unlocking them |
| Factions acting out of character | Need a political twist | Undermines worldbuilding credibility | Give in-story justification (internal coup, new intel, desperation) |

---

## Anti-Patterns

- ❌ Pedantic nitpicking that ignores narrative needs — if a soft violation serves a powerful scene and doesn't break immersion, note it but don't demand a fix
- ❌ Applying real-world physics rules the story has explicitly overridden — check the rule registry first
- ❌ Ignoring "soft" rule violations — they accumulate and erode reader trust
- ❌ Treating all rules as equal — bond system consistency matters more than whether the mess hall is on deck 3 or deck 4
- ❌ Forgetting that rules can evolve — characters discover new things, technology advances, but changes must be earned and explained

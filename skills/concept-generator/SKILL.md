---
name: concept-generator
description: "High-velocity fiction concept generation from minimal input. Takes a genre, feeling, comp title, or single constraint and produces 3–5 differentiated story concepts with hooks, protagonists, worlds, and romance engines. Optimized for creative divergence — quantity and surprise over refinement."
argument-hint: "Describe your genre instinct, comp titles, or partial premise"
user-invocable: true
---
# Concept Generator — Fiction Brainstorming Skill

Produce multiple differentiated story concepts from minimal input. Optimized for creative reach and divergence — not refinement.

---

## When to Use

- You have a genre or vibe but no story
- You have comp titles and want to find the gap between them
- You have one element (a setting, a character type, a power system) and need a story to hang it on
- You want to see what's possible before committing to a direction
- The brainstorm agent needs to generate initial pitches

---

## Input Processing

Before generating, identify what the input gives you and what it doesn't:

| Given | Missing | Strategy |
|---|---|---|
| Genre + setting | Protagonist, conflict | Generate maximum protagonist variety |
| Protagonist type | World, conflict engine | Generate maximum world variety |
| Comp titles | Original angle | Find the white space between the comps |
| Tone/vibe | Everything else | Build three completely different stories with that tone |
| Partial premise | Completion | Generate divergent completions, not variations |

Never generate the obvious answer first. The most expected interpretation of a prompt is the concept the user already thought of. Start somewhere else.

---

## Concept Generation Process

### Step 1: Identify the Constraint
What is the ONE thing the user's input makes non-negotiable? Usually it's a tone, a setting, or a protagonist type. Everything else is variable.

### Step 2: Generate the Grid
Before writing pitches, mentally generate a grid of possibilities:

- **Protagonist axis**: 5 different women who could anchor this story (not variations — genuinely different archetypes, backgrounds, abilities)
- **Conflict axis**: 5 different engines that could drive this story (conspiracy, war, survival, social, personal, supernatural, cosmic)
- **Tone axis**: Where on the spectrum from intimate/grounded to vast/epic does this story live?

Pick combinations that are maximally different from each other.

### Step 3: Write Pitches
For each concept selected from the grid, write a full pitch in the standard format (see brainstorm agent for format spec).

### Step 4: Check Differentiation
Read all pitches back. If any two could be described with the same one-sentence label, replace one.

---

## The White Space Principle

The best concepts live in the gap between existing things — the space that's clearly adjacent to something readers love but hasn't been done. When working from comp titles:

1. List what each comp title does *well* that readers love
2. List what each comp title *doesn't do* or can't do given its genre/setting
3. The white space is what both lists point toward but neither occupies

**Example**: "Dresden Files but set in Seattle and not a wizard"
- Dresden does well: street-level magic, noir tone, male protagonist with a code, monsters-as-crime
- Dresden doesn't do: female perspective, non-European magical traditions, tech-adjacent power systems, the Pacific Northwest's specific cultural texture
- White space: a woman with a non-wizard ability set, in Seattle's specific world (tech wealth, indigenous presence, water and mountain geography, coffee-shop culture meets something ancient), solving supernatural problems through means other than fire and bluster

---

## Power System Brainstorming

When a concept needs a non-standard ability or power system, use these generative axes:

**Sense-based**: protagonist perceives something others don't (infrastructure, emotion, time, probability, the recently dead)

**Cost-based**: protagonist can do something extraordinary but it always costs something real (memory, time, relationships, physical integrity)

**Connection-based**: protagonist's power only works through/with other people or things (ships, buildings, animals, specific people, places with history)

**Threshold-based**: protagonist's power activates under specific conditions (danger, emotional state, proximity to something, time of day/year)

**Inherited/Dormant**: protagonist has a power they didn't choose, don't fully understand, and may not be able to control

Combine axes for more specific, interesting systems: *a woman who perceives structural failure in buildings through touch (sense-based + connection-based), but the visions come with the emotional memories of everyone who died in a collapse (cost-based — she absorbs grief she can't discharge).*

---

## Quick-Fire Mode

When the user wants maximum divergence fast, generate 5 hooks only — no full pitches. One sentence each. Let the user pick which ones to develop.

**Example output for "Seattle urban fantasy, not a wizard":**

1. A structural engineer who touches collapsing buildings and absorbs the deaths of everyone who ever died in them — and a city that's been hiding its murders in its architecture for 150 years.
2. A marine biologist whose grant money comes from a tech billionaire who is not, it turns out, human — and whose research vessel keeps finding things at the bottom of Puget Sound that shouldn't exist.
3. A night-shift dispatcher for a rideshare company who routes drivers through Seattle's supernatural geography — because some passengers need to get somewhere the maps don't show, and some routes only open after midnight.
4. A Korean-American tattoo artist in Capitol Hill whose ink binds what it marks — including the thing that's been wearing her sister's face for six months.
5. A public defender who realizes the supernatural community is the most over-prosecuted minority in the Pacific Northwest, and she is apparently the only one willing to take their cases.

---

## Handoff

Once concepts are generated, return to the **brainstorm agent** for user reaction and refinement. Do not skip the reaction loop — the first round of pitches is input collection, not final output.

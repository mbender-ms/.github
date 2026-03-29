---
name: prose-craft
description: "Write vivid, emotionally charged scenes blending romantasy prose style with hard sci-fi settings. Covers POV, sensory writing, dialogue, pacing, internal monologue, and emotional beats in the style of Sarah J. Maas and Rebecca Yarros."
argument-hint: "Describe the scene to write, e.g. 'first encounter between the pilot and her new co-commander in the docking bay'"
user-invocable: true
---
# Prose-Craft — Scene Writing Skill

Write publication-quality fiction scenes that blend the emotional intensity of Sarah J. Maas and Rebecca Yarros with hard science fiction settings.

## When to Use

- Writing a new scene or chapter from a beat sheet or outline
- Rewriting or polishing an existing scene for voice consistency
- Writing a specific scene type: action, romance, dialogue, introspection
- Establishing or recovering the narrative voice after a break

---

## Tools

**context-mode — read prior chapters and worldbuilding without loading raw files:**
```
# Read the previous chapter ending for tone continuity
ctx_execute_file(path="manuscript/ACT I/Part II/Chapter-05.md",
  code='print(file_content[-2000:])', intent="ending tone, last beat, POV voice")

# Search worldbuilding for scene-specific details
ctx_search(queries=["location description", "tech capability", "character voice notes"],
  source="worldbuilding")
```

**ripgrep — check how a character's voice has appeared before:**
```bash
rg "^.*Maren.*said\|Maren thought\|Maren's" manuscript/ --type md -n | tail -20
```



### Default: Deep First-Person POV
The primary narrator is a strong female protagonist. Write in deep first-person present or past tense (match the manuscript's established tense).

**Deep POV rules:**
- No filter words: ~~"I noticed," "I felt," "I saw," "I heard," "I thought"~~
- Instead, render the sensation directly: "The deck plates hummed beneath my boots" not "I felt the deck plates humming"
- The narrator's personality colors every observation — biased, opinionated, alive
- Internal monologue flows naturally between action and description without italics tagging every thought
- Use italics sparingly for emphasis or sharp intrusive thoughts, not for all internal dialogue

**Dual POV (when applicable):**
- Alternate chapters or sections between two POV characters
- Each POV must have a distinct voice — vocabulary, sentence rhythm, what they notice
- The love interest's POV reveals what the main character cannot see about themselves
- POV switches happen at chapter breaks, never mid-scene

---

## Sensory Writing

Every scene must engage at least three senses. In space settings, lean into unfamiliar sensations:

### The Five Senses in Space

| Sense | Examples |
|---|---|
| **Sight** | The blue-shift glow of an approaching fleet. Warning lights painting the corridor in stuttering red. The infinite dark beyond the viewport, stars too numerous to process. |
| **Sound** | The omnipresent hum of life support. The sharp crack of a pressure seal engaging. Silence — real silence — in a disabled ship, when the systems go dark. |
| **Touch** | The cold bite of recycled air on bare skin. The bone-deep vibration of a drive core at full burn. The phantom warmth of a neural-link connection. Zero-g disorientation — the stomach-drop of no down. |
| **Smell** | Ozone after a shield discharge. The metallic tang of recirculated air. The alien scent of a new atmosphere on planetfall. Sweat and adrenaline in a flight suit after combat. |
| **Taste** | Copper on the tongue after a high-g maneuver. Ration paste that tastes like nothing and everything wrong. Real coffee — hoarded, precious, a luxury that tastes like home. |

### The Sixth Sense: Interiority
The character's emotional state is a sense too. It manifests physically:
- Anxiety: tight chest, shallow breath, cold fingers
- Desire: heat pooling low, skin hyper-aware, pulse hammering
- Rage: jaw clenched, vision narrowing, hands shaking
- Grief: hollow chest, heavy limbs, the world muted and distant
- Wonder: breath caught, stillness, the mind struggling to comprehend scale

---

## Dialogue

### Voice Rules
- Characters speak differently based on background: military brevity, academic precision, street-smart shorthand, aristocratic formality
- Subtext over text — what characters don't say matters more than what they do
- Romantic dialogue: charged pauses, double meanings, deflection through sarcasm
- Use dialogue beats (action during speech) instead of adverbs: "He leaned against the bulkhead, arms crossed" not "he said casually"

### Dialogue Tags
- Default to `said` and `asked` — they're invisible to the reader
- Use action beats instead of tags when possible: `"You're late." She didn't look up from the nav console.`
- Never use: ~~hissed, growled, breathed, purred~~ (unless used very sparingly for emphasis)
- For Yarros-style wit, let the humor live in the words, not the tags

### Romantic Dialogue Patterns
- **The Almost-Confession**: Character starts to say something revealing, then deflects
- **The Name Drop**: Using someone's first name when you usually don't — intimate, loaded
- **The Quiet Truth**: A simple, devastating honest statement after pages of deflection
- **Banter as Foreplay**: Verbal sparring where every comeback is a step closer

---

## Pacing

### Scene-Level Pacing
- **Action scenes**: Short sentences. Fragments. Staccato rhythm. No time to think.
- **Romantic tension**: Longer sentences. Drawn out. Every micro-movement amplified. Time slowing.
- **Emotional aftermath**: Medium sentences. Reflective. The body settling after the storm.
- **Worldbuilding moments**: Woven through action and dialogue, never standalone exposition paragraphs

### Chapter-Level Pacing (Yarros-style)
- Chapters: 2,000–4,000 words (short and punchy)
- Every chapter ends on a hook: a revelation, a question, a reversal, an emotional gut-punch
- Open chapters in media res when possible — start in motion, orient the reader as you go
- The "one more chapter" effect: each ending creates a need to know what happens next

### Book-Level Pacing
- Act I (25%): World introduction, character establishment, inciting incident, first romantic spark
- Act II-A (25%): Rising action, deepening romance, escalating external threat
- Midpoint (5%): Major revelation or reversal that recontextualizes everything
- Act II-B (20%): Consequences, dark moment, relationship crisis, all-is-lost
- Act III (25%): Climax, romantic resolution (or devastating cliffhanger for series), new equilibrium

---

## Emotional Beats

### The Maas Emotional Playbook
1. **The Shatter**: A moment where the protagonist's composure breaks — tears, rage, collapse. Earned through chapters of pressure.
2. **The Claiming**: Not sexual (necessarily) — a moment where a character chooses someone. "You are mine, and I am yours." Translated to sci-fi: command bond activation, voluntary neural-link, choosing to be someone's co-pilot.
3. **The Reveal of Power**: The protagonist discovers or unleashes an ability that changes the power dynamic. In sci-fi: first successful fold-space navigation, psionic awakening, bonding with a sentient ship.
4. **The Sacrifice**: A character gives up something essential — safety, position, identity — for someone they love.
5. **The Reunion**: After forced separation, the moment of reconnection. Write with devastating relief.

### The Yarros Emotional Playbook
1. **The Near-Miss**: A combat scene where the love interest almost dies. Write the protagonist's reaction — the terror, the fury, the desperate relief.
2. **The Vulnerability Reveal**: The tough, guarded character lets down their walls in a private moment. One crack in the armor.
3. **The Training Bond**: Shared hardship creates intimacy. Fighting together, surviving together, bleeding together.
4. **The Public Claim**: In front of others — subordinates, rivals, command — one character publicly aligns with the other. Stakes and witnesses.
5. **The Quiet After**: Post-battle, post-crisis, the two characters alone. Exhausted. Honest. The walls down because there's no energy left to hold them up.

---

## Scene Structure Template

When writing a scene, follow this internal structure:

1. **Hook** (1-3 sentences): Drop the reader into the moment. Action, sensation, or a charged line of dialogue.
2. **Orient** (1 paragraph): Where are we? Who's here? What's the emotional temperature?
3. **Escalate** (bulk of scene): Build tension — conflict, discovery, attraction, danger. Layer external action with internal reaction.
4. **Turn** (the pivot): Something shifts. A revelation, a choice, a kiss, a betrayal, a disaster.
5. **Land** (final beat): The emotional resonance of the turn. How does the POV character feel? What has changed?
6. **Hook out** (last line): A line that propels the reader forward. A question. A threat. A promise.

---

## Anti-Patterns (What NOT to Do)

- ❌ Info-dumps disguised as internal monologue ("As I walked to the bridge, I reflected on the history of the Hegemony, which was founded in...")
- ❌ Describing technology like a manual — filter it through character experience
- ❌ Purple prose without purpose — every lush description must earn its place by revealing character or building tension
- ❌ Telling emotions instead of showing them ("I was angry" vs. showing clenched fists, bitten words, narrowed vision)
- ❌ Resolving romantic tension too early — the slow burn is the point
- ❌ Perfect protagonists — they must have flaws, blind spots, and bad decisions that cost them
- ❌ Forgetting the body — characters exist physically. They're tired, hungry, injured, aroused, cold. The body is always present.
- ❌ Male-gaze descriptions of female characters — no anatomy inventories, no performative desire
- ❌ Describing male love interests like character sheets — the female gaze *feels* a man (warmth, weight, voice, the way he moves), it doesn't measure him
- ❌ Writing desire as something that happens *to* the female character — she wants, she chooses, she burns

---

## The Female Gaze in Prose

All prose is written through the female author's voice. This shapes HOW characters are described:

**Male characters through the female gaze:**
- Movement and presence over physical inventory ("the way he filled the corridor" not "six-foot-two with broad shoulders")
- Restraint as aphrodisiac — what he holds back is more charged than what he does
- Vulnerability in power — the crack in his armor, the rawness he lets her see
- Sensation over observation — how his touch feels, not how his body looks
- Voice as sensory experience — low, rough, close, the words he almost says

**Female POV desire:**
- Desire is embodied: heat, ache, awareness, the catch of breath
- Agency in wanting — she pursues, she decides, she surrenders by *choice*
- The emotional stakes of intimacy — every scene of desire is also a scene of vulnerability
- The body's history matters — scars, exhaustion, strength earned through suffering

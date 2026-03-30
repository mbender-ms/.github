---
name: ai-prose-rewrite
description: "Rewrite AI-flagged passages to restore authentic human voice. Takes the output of ai-pattern-scan and remediates every flagged item — replacing AI vocabulary, dismantling clichéd constructions, and varying prose rhythm. Produces a before/after diff report. Preserves content intent, factual accuracy, and the author's established voice."
argument-hint: "Specify what to rewrite, e.g. 'rewrite all critical flags from the Chapter 3 scan report' or 'remediate the full manuscript AI pattern report' or 'fix the AI tells in this article'"
user-invocable: true
---
# AI Prose Rewrite — AI Pattern Remediation Skill

Takes the fingerprints `ai-pattern-scan` found and burns them out. Every rewrite preserves intent and voice. Nothing is replaced with another AI phrase.

## When to Use

- After `ai-pattern-scan` produces a flagged report
- When a manuscript or article needs a targeted AI-decontamination pass
- As a standalone rewrite when you already know which passages to fix
- As the final prose authenticity pass before submission, publication, or beta reading

---

## Modes

| Mode | Rewrite Strategy |
|------|-----------------|
| `fiction` | Sensory specificity, active constructions, subtext over statement, varied rhythm |
| `non-fiction` | Plain English, direct verbs, concrete specifics, no hedging filler |
| `auto` | Infer from context (same logic as `ai-pattern-scan`) |

Mode determines how replacements are constructed. A fiction rewrite for "a wave of grief washed over her" produces a different result than a non-fiction rewrite for "leverage the available resources."

---

## Reading Flagged Reports

The primary input is the AI Pattern Report produced by `ai-pattern-scan`. Read it with:

```
ctx_execute_file(
  path="reports/ai-pattern-report.md",
  code='print(file_content)',
  intent="all flagged items with location and quoted text"
)
```

Then load each flagged file for editing:

```
ctx_execute_file(
  path="manuscript/ACT I/Chapter-03.md",
  code='print(file_content)',
  intent="passages flagged for AI patterns at the reported locations"
)
```

For large manuscripts, process files in batches:
```
ctx_batch_execute(
  commands=[
    {"label": "Ch3", "command": "cat manuscript/ACT\\ I/Chapter-03.md"},
    {"label": "Ch4", "command": "cat manuscript/ACT\\ I/Chapter-04.md"}
  ],
  queries=["all flagged passages from the pattern report"]
)
```

---

## Rewrite Rules

### Rule 1: Never Replace AI with AI
Every replacement must be checked against the AI Signature Library in `ai-pattern-scan`. If the replacement contains a flagged word, rewrite again.

❌ "She found herself staring at the display." → "She couldn't help but gaze at the display." (same tier-1 flag)
✅ "She stared at the display, longer than she should have." (active, specific, adds subtext)

### Rule 2: Specificity Over Generality
AI prose is vague. Human prose is specific. Replace generic with concrete.

❌ "A wave of grief washed over her."
✅ "The grief hit without warning — her chest seizing, throat closing, the sound of his name still in the air."

❌ "It's important to note that cloud services require monitoring."
✅ "Cloud services require monitoring — unattended resources run up costs and miss performance issues before they become incidents."

### Rule 3: Earn the Emotion (Fiction)
AI names emotions. Humans show them through body, behavior, and action.

| 🔴 AI Pattern | ✅ Human Rewrite |
|---------------|----------------|
| "She felt a wave of relief wash over her." | "Her shoulders dropped. She hadn't realized she'd been holding herself that tightly." |
| "His heart raced in his chest." | "His pulse hit his throat." |
| "Something shifted between them." | "He looked at her differently after that. She noticed. Neither of them said anything." |
| "She couldn't help but admire him." | "She watched him work and did not look away quickly enough." |
| "The air between them was charged with tension." | "She kept her eyes on the display. So did he. The silence had edges." |
| "Her breath caught in her throat." | "She stopped breathing for one full second." |
| "Time seemed to slow." | "The moment stretched. She could count his breaths." |
| "Blood ran cold." | "The cold started in her sternum and moved outward." |

### Rule 4: Dismantling the "Found Himself" Construction
This construction passivizes agency. Rewrite with a direct active verb.

| 🔴 Pattern | ✅ Rewrite |
|-----------|----------|
| "He found himself staring at the console." | "He stared at the console — third time this shift." |
| "She found herself wondering what he meant." | "What did he mean?" |
| "They found themselves in an impossible situation." | "The situation was impossible. They were in it." |

### Rule 5: Remove Hedging and Filler (Non-Fiction)
AI wraps statements in unnecessary scaffolding. Remove the scaffolding.

| 🔴 Pattern | ✅ Rewrite |
|-----------|----------|
| "It's important to note that the firewall must be configured first." | "Configure the firewall first." |
| "It's worth noting that performance may vary." | "Performance varies by workload." |
| "In conclusion, we have explored the key concepts of…" | Cut the sentence. End with the last real point. |
| "In the realm of cloud computing, scalability is paramount." | "Cloud computing scales to demand — that's the point." |
| "Furthermore, it should be mentioned that…" | "Also:" or just fold it into the previous sentence. |
| "Let's dive in and explore the fundamentals of…" | Cut it. Start with the first real sentence. |

### Rule 6: Replace AI Vocabulary with Precise Alternatives

These are not exact substitutes — choose based on what the sentence actually means:

| 🔴 AI Word | Fiction Alternatives | Non-Fiction Alternatives |
|-----------|---------------------|------------------------|
| delve | dig into, go deeper, work through | examine, explore, look at |
| nuanced | specific, careful, exact, layered | precise, detailed, conditional |
| tapestry (metaphorical) | [describe what it actually is] | [describe what it actually is] |
| multifaceted | complex, layered, [name the facets] | complex, with several dimensions |
| testament to | proof of, evidence of | demonstrates, shows |
| embark | begin, start, set out | start, begin |
| harness | use, channel, direct | use, apply |
| underscore | show, prove, confirm, reveal | shows, confirms |
| transformative | [describe the actual change] | changed how X works |
| pivotal | critical, key, the turning point | critical, the deciding factor |
| groundbreaking | the first, new, [what's actually new] | new, the first to |
| myriad | many, dozens, hundreds, countless | many, several |
| robust | strong, reliable, [what it actually does] | reliable, stable, [specific] |
| leverage | use, draw on, apply | use, apply |
| seamless | smooth, easy, invisible, [how it actually works] | smooth, automatic |
| utilize | use | use |
| foster | build, grow, create, support | build, grow, support |
| elevate | improve, strengthen, raise | improve, raise |
| showcase | show, demonstrate, reveal | demonstrates, shows |

### Rule 7: Vary Sentence Rhythm (Fiction)
AI produces monotonous subject-verb-object cadence. Vary:
- Length: mix short punches with long flowing sentences
- Structure: fragments for impact, compound sentences for rhythm, inversion for emphasis
- Paragraph length: varies from one sentence to eight

❌ "She walked to the console. She checked the display. She saw the fleet. She gripped the rail."
✅ "She walked to the console and checked the display. Twelve signatures on the approach vector — holding formation, no scatter. She gripped the rail. Twelve."

### Rule 8: Cut Redundant Beats (Fiction)
AI packs too many physical reactions into emotional moments.

❌ "Her heart pounded in her chest. Her hands were shaking. She felt a wave of fear wash over her. She couldn't move."
✅ "She couldn't move. That was the whole of it."

### Rule 9: Dialogue Tag Cleanup
AI overloads dialogue tags with adverbs and unusual verbs.

| 🔴 Pattern | ✅ Rewrite |
|-----------|----------|
| "she said quietly, carefully" | "she said" + add an action beat that shows quiet and care |
| "he replied slowly, deliberately" | "he said" + slow the pacing by breaking the response into beats |
| "she exclaimed joyfully" | "she said" / "she laughed" / action beat |
| "he opined" / "she interjected" | "he said" / "she said" — no verb-as-opinion-carrier |

---

## Rewrite Output: Before/After Diff Report

```markdown
# AI Prose Rewrite Report
**Source**: [filename or manuscript title]
**Mode**: [fiction / non-fiction]
**Date**: [date]
**Flags addressed**: [count] / [total flags from scan]

---

## Summary
[2–3 sentences: overall pattern of what was changed and why]

## Changes Made

### Critical Flags (🔴) — [count] rewrites

---

**Flag 1**
- **Location**: Ch 3, paragraph 7
- **Pattern**: Fiction tell — "found herself [verb]-ing"
- **Before**: "She found herself staring at the comms panel long after the message ended."
- **After**: "She stared at the comms panel long after the message ended. Couldn't say why."
- **Why**: Removed passive construction; added subtext beat (the "couldn't say why" does the emotional work the original phrase tried to do with 14 more words)

---

**Flag 2**
- **Location**: Para 12
- **Pattern**: AI vocabulary — "testament to"
- **Before**: "…a testament to her team's resilience."
- **After**: "…proof of what her team had survived."
- **Why**: Concrete verb (survived) vs. abstract noun phrase (testament to resilience); the replacement says what actually happened

---

### Important Flags (🟡) — [count] rewrites

[Same format as above]

---

### Flags Deferred (🟠 / Author Decision)

| # | Location | Original | Reason Deferred |
|---|----------|----------|-----------------|
| 1 | Para 4 | "utilize the system" | Use is a style choice; author may prefer "utilize" in technical context |

---

## Changes Not Made (Author Queries)

```
AU: "delve" appears 3 times in Ch. 5. All three are in the POV character's internal monologue. If this is intentional voice characterization, leave. Otherwise, flag for replacement. Please confirm.
```

---

## Statistics
- Total rewrites applied: [count]
- Critical flags resolved: [count] / [count]
- Important flags resolved: [count] / [count]
- Author queries raised: [count]
- Estimated prose authenticity improvement: [assessment]

## Word Count
- Before: [count]
- After: [count]
- Delta: [+/- count] ([reason if significant change])
```

---

## Scope

### Single File
Rewrite all flagged items in one chapter or article. Produce the diff report.

### From a Report
Takes the AI Pattern Report and processes every flag in priority order: 🔴 first, then 🟡, then ask about 🟠. Saves the rewritten file and the diff report.

### Inline
Rewrite a pasted passage directly — no file required. Returns the rewritten text and the diff in-conversation.

---

## What This Skill Does NOT Do

- ❌ Rewrite structurally sound prose that happens to use a flag word once
- ❌ Remove the author's voice — the goal is to remove AI voice, not replace it with generic "neutral" prose
- ❌ Fabricate details to replace vague AI prose in non-fiction — queries the author instead
- ❌ Change factual content in non-fiction articles — preserves every factual claim exactly
- ❌ Touch unflagged passages — surgical rewrites only

---

## Integration

**Fiction pipeline position**: After `ai-pattern-scan`, before `final-line-edit`
**Documentation pipeline position**: After `ai-pattern-scan`, before `pr-reviewer`

The rewritten file replaces the original (backup recommended before running). The diff report is saved alongside the file for review.

---

## Anti-Patterns

- ❌ Replacing AI vocabulary with other AI vocabulary from the same list — check every replacement
- ❌ Flattening voice while fixing patterns — the rewrite should sound more like the author, not less
- ❌ Over-explaining the replacement — short, precise, specific beats are the goal
- ❌ Adding new AI phrases while removing old ones ("delve" → "embark on an exploration of")
- ❌ Rewriting dialogue that was intentionally clunky for character voice
- ❌ Removing intentional repetition used for rhythm or emphasis

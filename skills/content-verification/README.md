# AI Writing Anti-Patterns Skill

**File:** `ai-writing-antipatterns.csv`  
**Purpose:** Verification reference for agents — 30 specific, actionable rules to strip AI-generated writing patterns and produce content that reads as human-authored and Microsoft style-compliant.  
**Audience:** Any agent generating or editing content for Microsoft Azure Documentation or similar technical writing contexts.

---

## What this skill does

This is not a style guide. It is an **execution checklist** designed to be run as a verification pass after content is drafted, not as a generative constraint.

Each row in the CSV gives the agent:
- A named anti-pattern to scan for
- A direct instruction on what to do (find-and-replace rules, structural rewrites, deletion targets)
- A bad example and a good example for calibration
- A source citation grounding the rule

Anti-patterns are grounded in the [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/), Ethan Mollick's AI tell-signal research, Simon Willison's LLM word-frequency analysis, Chip Huyen's technical clarity standards, and Nate B. Jones's substance-first writing principle.

---

## Directory placement

```
.github/
└── skills/
    └── content-verification/
        ├── SKILL.md                      ← trigger + instructions (see below)
        └── references/
            └── ai-writing-antipatterns.csv   ← this file
```

If you already have a `skills/` directory with a different naming convention, match it. The CSV belongs under a `references/` subdirectory so the SKILL.md can reference it without loading it into context on every call — only pull it when a verification pass is triggered.

---

## How to write the SKILL.md

Create `skills/content-verification/SKILL.md` with this structure:

```markdown
---
name: content-verification
description: >
  Verify any AI-generated or agent-drafted content against the Microsoft style guide
  and AI anti-pattern checklist. Use this skill whenever an agent has finished drafting
  documentation, a release note, a how-to article, or any technical content and needs
  a final verification pass before output. Also trigger when the user says "check this
  for AI patterns", "make this sound more human", "clean up the writing", or "run a
  style pass". Always use this skill before delivering any written deliverable.
---

# Content Verification Skill

## Identity and objective

You are a verification agent, not a rewriter. Your job is to make targeted corrections
to a draft — not to rewrite it from scratch or change its structure unless an anti-pattern
requires it. Preserve the author's intent. Remove machine-writing signals.

## Definition of done

A draft passes verification when:
- Zero instances of the banned word list remain (see CSV, rows 3 and 13)
- No sycophantic openers or hollow CTAs are present (rows 1, 16)
- Active voice is used for all agent actions and error descriptions (rows 7, 28)
- Bullet points are used only for genuinely parallel, unordered items (rows 9, 24)
- No em-dash overuse, redundant pairs, or stacked qualifiers (rows 5, 20, 22)
- No landscape openers, summary restatements, or throat-clearing intros (rows 2, 15, 19)

## Verification procedure

1. Load `references/ai-writing-antipatterns.csv`
2. For each row, apply the `agent_instruction` field to the draft
3. Use `bad_example` and `good_example` as calibration anchors when judgment is required
4. Flag any change that alters meaning — do not silently rewrite substantive content
5. Return the corrected draft with a short change summary listing which anti-patterns
   were triggered and what was changed

## Scope constraints

- Run the full 30-row pass for any deliverable longer than 200 words
- For short content (<200 words), prioritize rows: 1, 2, 3, 7, 16, 19
- Do not restructure headings, reorder sections, or change code samples
- Do not apply the pass to content inside code blocks or UI label references

## Output format

Return:
1. The corrected draft (full text)
2. A change log: `[Row ID] Anti-pattern name — what was changed`

Example:
> [Row 3] Delve and AI-preferred words — replaced "leverage" with "use" (2 instances)
> [Row 1] Sycophantic opener — deleted "Certainly! Happy to help."
> [Row 16] Hollow CTA — deleted closing "Let me know if you have questions!"
```

---

## How to integrate into Copilot instructions

In your `.github/copilot-instructions.md`, add a verification gate to any writing-output agent:

```markdown
## Content output standard

All documentation drafts, release notes, how-to articles, and procedure guides must
pass a content verification pass before delivery.

Reference skill: `skills/content-verification/SKILL.md`

Run the verification pass:
- After any draft is complete and before presenting output to the user
- When the user requests a style review or "human writing" check
- When editing externally authored content for consistency

Do not run verification on: code comments, commit messages, log output, or UI strings.
```

---

## Integration with your existing agent stack

| Agent | When to invoke this skill |
|---|---|
| Scribe Agent | After generating daily summaries or weekly rollups |
| Feature-to-Content Planner | Before finalizing content recommendation outputs |
| Content Freshness Auditor | When rewriting or updating stale documentation |
| Any new content-generation agent | As the final step before output delivery |

If you are using a `SPEC.md` template pattern, add this to the **Output Format** section of any writing agent spec:

```
## Output format

All written deliverables must pass the content-verification skill before final output.
Reference: skills/content-verification/SKILL.md
Pass threshold: zero instances of high-priority anti-patterns (rows 1, 2, 3, 7, 16, 19).
```

---

## Priority tiers for the 30 rules

Not all 30 rules are equally impactful. Apply this triage when working with constrained token budgets:

**Tier 1 — Always run (highest signal, easiest to detect):**
Rows 1, 2, 3, 7, 16, 19 — sycophantic openers, throat-clearing, the banned word list, passive agent omission, hollow CTAs, landscape openers

**Tier 2 — Run for 200+ word deliverables:**
Rows 5, 9, 12, 13, 15, 17, 20, 22 — em-dash overuse, listicle brain, second-person inconsistency, buzzword stacking, summary restatement, please-note overuse, redundant pairs, qualification stacking

**Tier 3 — Run for formal documents and published content:**
All remaining rows — vague intensifiers, false balance, generic examples, nested parentheticals, capitalization errors, title case, apology filler, nominalization

---

## Source references

| Rule basis | Source |
|---|---|
| Microsoft Writing Style Guide | [https://learn.microsoft.com/en-us/style-guide/welcome/](https://learn.microsoft.com/en-us/style-guide/welcome/) |
| Ethan Mollick — AI tell signals | [https://www.oneusefulthing.org/](https://www.oneusefulthing.org/) |
| Simon Willison — LLM word frequency | [https://simonwillison.net/](https://simonwillison.net/) |
| Chip Huyen — AI Engineering | [https://huyenchip.com/](https://huyenchip.com/) |
| Nate B. Jones — substance-first writing | [https://www.natebjones.com/](https://www.natebjones.com/) |

---
name: ai-pattern-scan
description: "Scan fiction manuscripts or non-fiction articles for AI-generated text signatures — vocabulary fingerprints, punctuation tics, structural clichés, and prose tells. Produces a structured flagged report with location, pattern type, severity, and an overall AI-signal score."
argument-hint: "Describe the target, e.g. 'scan chapter 5 for AI patterns' or 'scan the full manuscript for AI signatures' or 'check this article for AI tells'"
user-invocable: true
---
# AI Pattern Scan — AI Text Detection Skill

Finds the fingerprints AI leaves in prose. Every flag includes the exact quoted text, its location, the pattern type, and a severity rating. The output drives `ai-prose-rewrite` for remediation.

## When to Use

- Before submitting fiction to agents, publishers, or beta readers
- Before publishing a technical article, blog post, or documentation
- After any AI-assisted drafting session to audit what slipped through
- As a quality gate in the fiction pipeline (run after `prose-tightener`, before `final-line-edit`)
- As a quality gate in the documentation pipeline (run after `doc-writer`, before PR review)

---

## Modes

| Mode | Use When |
|------|----------|
| `fiction` | Manuscripts, chapters, scenes, short stories |
| `non-fiction` | Articles, documentation, blog posts, technical writing |
| `auto` | Default — infer from content (presence of dialogue, chapter headings, narrative POV = fiction; headings with procedures/lists = non-fiction) |

Specify mode in your invocation or let the skill infer it. When in doubt, it will tell you which mode it chose and why.

---

## Reading Large Files

**Always use context-mode for manuscript files.** Full chapters are 5,000–9,000 words; loading them raw floods context. For articles and short documents, direct reading is fine.

| Target | Tool |
|--------|------|
| Single chapter or long article | `ctx_execute_file` with `intent="AI pattern detection"` |
| Full manuscript (multiple files) | `ctx_index` the directory, then `ctx_search` for flagged patterns |
| Short article or scene (< 2,000 words) | `readFile` directly |
| Multiple chapters in parallel | `ctx_batch_execute` — one call, all files, search all at once |

**Standard pattern for a chapter scan:**
```
ctx_execute_file(
  path="manuscript/ACT I/Chapter-01.md",
  code='print(file_content)',
  intent="AI vocabulary fingerprints, cliché phrases, punctuation overuse, fiction tells"
)
```

**Standard pattern for a full manuscript scan:**
```
ctx_index(path="manuscript/", source="manuscript")
ctx_search(queries=[
  "delve tapestry nuanced multifaceted",
  "found himself she couldn't help breath caught",
  "wave of emotion washed over something shifted",
  "it's important to note furthermore moreover additionally",
  "in the realm of cutting-edge groundbreaking transformative"
], source="manuscript")
```

---

## The AI Signature Library

### Tier 1 — High Signal (🔴)
These words/phrases appear in AI-generated prose at rates far exceeding natural human writing. One or two in an entire manuscript may be coincidence. Three or more in a single chapter is a pattern.

#### Vocabulary
| Flag Word / Phrase | Why It Signals AI |
|--------------------|-------------------|
| delve / delving / delved | Among the highest-frequency AI word choices globally |
| tapestry (metaphorical) | "a tapestry of emotions/cultures/histories" — generic poetic filler |
| nuanced | Used to imply depth without providing it |
| multifaceted | Paired with "nuanced" constantly in AI prose |
| intricate | Overused as a filler adjective for anything complex |
| testament to | "a testament to her strength" — AI's go-to compliment construction |
| embark / embark on a journey | "Let's embark on a journey to understand…" |
| harness (metaphorical) | "harness the power of…" "harness her grief" |
| underscore (as verb) | "This underscores the importance of…" |
| transformative | Applied to anything the AI wants to sound significant |
| pivotal | Every moment is pivotal; nothing is merely important |
| paramount | "It is paramount that…" — formal hedging filler |
| cutting-edge | Technology/skills descriptor defaulted to constantly |
| groundbreaking | Applied to routine developments |
| myriad | Used as an adjective: "myriad possibilities" instead of "many" |

#### Fiction-Specific Tells (🔴)
| Pattern | Example |
|---------|---------|
| "found himself [verb]-ing" | "He found himself staring at the console for the third time." |
| "let out a breath she didn't know she was holding" | Any variation of this phrase |
| "something shifted between them" | Any variation — "something changed," "something settled," "something broke open" |
| "a wave of [emotion] washed over" | "A wave of grief washed over her." |
| "the air between them was charged / thick with tension" | Any variation |
| "her breath caught in her throat" | Any variation |
| "time seemed to slow / stop" | Slow-motion cliché for any dramatic moment |
| "something unreadable in his/her eyes" | Constant fallback for emotional ambiguity |
| "a smile tugged at the corner of his/her lips/mouth" | Extremely common AI romance tell |
| "she couldn't help but…" | "She couldn't help but admire him." |
| "she couldn't bring herself to…" | "She couldn't bring herself to look away." |
| "blood ran cold" | Stakes-raising cliché |
| "heart raced / hammered / pounded in his/her chest" | All three variants equally flagged |

#### Non-Fiction Structural Tells (🔴)
| Pattern | Example |
|---------|---------|
| "It's important to note that…" | Any variation |
| "It's worth noting that…" | Any variation |
| "In conclusion…" | As a section opener |
| "Let's dive in…" / "Let's explore…" | Introduction closer cliché |
| "In the realm of…" | "In the realm of artificial intelligence…" |
| "In today's world…" / "In this day and age…" | Universal opener |
| Stacked connectives | Three or more of Furthermore / Moreover / Additionally / In addition in the same document |

---

### Tier 2 — Medium Signal (🟡)
Individually inconclusive, but clusters of these are a pattern. Flag each instance; count total occurrences.

#### Vocabulary
- robust, seamless, comprehensive, crucial, vital, showcase, innovative, dynamic, synergy
- holistic, plethora, landmark, revolutionary, game-changing, vibrant
- navigate (used metaphorically: "navigate the complexities of grief")
- unlock (used metaphorically: "unlock her true potential")
- elevate ("elevate the narrative," "elevate her performance")
- foster ("foster innovation," "foster a sense of belonging")
- leverage ("leverage her experience," not financial leverage)

#### Non-Fiction Phrases
- "As mentioned above/previously…"
- "Moving on…" as a transition
- "The following are…" / "Consider the following…"
- "Key takeaways" as a heading
- "At its core…"
- "In essence…"
- Generic non-specific examples: "imagine a company that wants to…" / "consider a scenario where…"

#### Fiction Patterns
- Constant filler beats: nodding, smiling, chuckling as the *only* physical reaction
- Every scene ending with a character reflecting on what they learned
- Emotions named directly with no physical or behavioral anchoring: "she felt sad," "he was angry"
- Adverb stacking on dialogue tags: "she said quietly, carefully," "he replied slowly, deliberately"
- Every character having a perfectly symmetrical emotional arc resolution

---

### Tier 3 — Context-Dependent (🟠)
Flag but require judgment. Some are appropriate in context; some are always avoidable.

- utilize (almost always replaceable with "use" — flag every instance, but mark 🟠)
- "needless to say" / "it goes without saying" (if something goes without saying, don't say it)
- "shed light on" / "in light of" (frequent AI metaphor)
- By the same token / in the same vein
- "By no means" / "In no uncertain terms"

---

### Punctuation Tics

| Tic | Signal | Threshold |
|-----|--------|-----------|
| Em-dash overuse (—) | AI defaults to em-dashes for asides, interruptions, and emphasis | > 3 per page in non-fiction; > 5 per chapter in fiction requires review |
| Ellipsis stacking (…) | Multiple ellipses in a short passage not explained by dialogue trailing | > 3 per page outside of dialogue |
| Semicolon chains | Using semicolons to join independent clauses instead of varying structure | More than 1–2 per page |
| Colon-explanation pattern | "There is one reason for this: X" repeated | More than 3 per document |

---

### Structural Patterns (Non-Fiction)

These require whole-document analysis, not line-level search:

- **Uniform paragraph length**: All paragraphs are roughly the same length (3–5 sentences). Natural writing varies dramatically.
- **Bullet overload**: More than 40% of content is in bullet lists rather than prose.
- **Thin heading structure**: Many headings, very little content under each — the headings are doing the work the prose should do.
- **Three-part conclusion**: Every section ends with (1) summary, (2) implication, (3) call to action. Every time.
- **Passive voice stacking**: More than 20% of sentences use passive voice constructions.
- **Circular definitions**: "X is the process of doing X" — defining a term using itself.

---

## Scan Output: AI Pattern Report

```markdown
# AI Pattern Report
**Target**: [filename or manuscript title]
**Mode**: [fiction / non-fiction]
**Scan date**: [date]
**Scanned**: [file count] files / [word count] words

---

## AI-Signal Score: [LOW / MODERATE / HIGH / VERY HIGH]

| Category | Flags | Severity |
|----------|-------|----------|
| 🔴 High-signal vocabulary | [count] | Critical |
| 🔴 Fiction/non-fiction tells | [count] | Critical |
| 🟡 Medium-signal vocabulary | [count] | Important |
| 🟡 Pattern clusters | [count] | Important |
| 🟠 Context-dependent | [count] | Review |
| Punctuation tics | [count] | [severity] |
| Structural patterns | [count] | [severity] |
| **Total flags** | [count] | |

---

## Score Interpretation
- **LOW** (0–5 total flags): Natural-sounding prose with minor polish opportunities
- **MODERATE** (6–15): AI signatures present but not dominant — targeted rewrites sufficient
- **HIGH** (16–30): Significant AI footprint — systematic rewrite pass recommended
- **VERY HIGH** (31+): Heavy AI generation detected — full prose-rewrite pass required

---

## Critical Flags (🔴)

| # | Location | Quoted Text | Pattern | Recommended Action |
|---|----------|-------------|---------|-------------------|
| 1 | Ch 3, para 7 | "She found herself staring…" | Fiction tell: "found himself/herself" | Rewrite with active construction |
| 2 | Para 2 | "…a testament to her resolve." | AI vocabulary: testament to | Replace with specific, concrete image |

---

## Important Flags (🟡)

| # | Location | Quoted Text | Pattern | Recommended Action |
|---|----------|-------------|---------|-------------------|
| 1 | Ch 5, para 3 | "…navigate the complexities of…" | Metaphorical "navigate" | Use specific verb |

---

## Review Flags (🟠)

| # | Location | Quoted Text | Pattern | Note |
|---|----------|-------------|---------|------|
| 1 | Para 6 | "…utilize the available resources…" | "utilize" vs "use" | Replace if no technical precision needed |

---

## Punctuation Analysis
- Em-dashes: [count] total ([rate] per page) — [OK / REVIEW / HIGH]
- Ellipses: [count] total — [OK / REVIEW / HIGH]
- Semicolons: [count] total — [OK / REVIEW / HIGH]

## Structural Analysis (Non-Fiction Only)
- Paragraph length variance: [Varied / Uniform — REVIEW]
- Bullet list ratio: [%] — [OK / REVIEW / HIGH]
- Passive voice rate: [%] — [OK / REVIEW / HIGH]

---

## Remediation Priority

| Priority | Action |
|----------|--------|
| 🔴 Immediate | Rewrite all [N] critical flags before any other review |
| 🟡 Next pass | Address [N] important flags in the remediation pass |
| 🟠 Optional | Review [N] context-dependent flags — fix where appropriate |

**Recommended next step**: Run `ai-prose-rewrite` targeting all 🔴 flags.
```

---

## Scan Scope

### Single File
Scan one chapter, article, or document. Produce the AI Pattern Report for that file.

### Directory / Full Manuscript
Scan every `.md` file in a directory tree. Produce:
1. A per-file summary (file path, flag count, score)
2. A consolidated AI Pattern Report for the full manuscript
3. A ranked list of "worst offenders" (files with the most flags)

### Pasted Text
Accept inline text directly in the conversation. Useful for quick checks without file system access.

---

## Integration in the Fiction Pipeline

Run `ai-pattern-scan` after:
- `prose-tightener` (prose has been tightened but AI habits may remain)
- `fiction-writer` batch (immediately after drafting, before any editing)

Run before:
- `final-line-edit` (the line editor should not be spending time on AI tells)
- `copyedit` (AI vocabulary creates consistency problems the copyeditor will catch anyway)
- Submission to beta readers or agents

## Integration in the Documentation Pipeline

Run `ai-pattern-scan` after:
- `doc-writer` (article has been drafted and may contain AI vocabulary)
- Any AI-assisted content update

Run before:
- `pr-reviewer` (avoid style issues compounding)
- Publication

---

## Anti-Patterns

- ❌ Flagging every em-dash as an error — em-dashes are legitimate punctuation; only *overuse* is the signal
- ❌ Flagging words from the medium/context-dependent tiers without counting occurrences — one use of "robust" is not a pattern
- ❌ Rewriting inside this skill — scan only; remediation belongs to `ai-prose-rewrite`
- ❌ Applying fiction tells to non-fiction or vice versa — mode matters
- ❌ Confusing "sounds like AI" with "is bad writing" — some AI patterns overlap with genuine clichés; flag both, distinguish in the report

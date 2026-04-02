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

## ⚠️ Mandatory Scan Protocol (Full Manuscript)

**A full manuscript scan is NOT a random sample and NOT a thematic pass.** It must scan **every word in every chapter**. The only valid full-manuscript scan runs all of the following steps in sequence. No chapter may be skipped.

### Step 1 — Build the chapter inventory
```bash
find <manuscript_dir> -name "Chapter-*.md" \
  -not -path "*/editorial*" \
  -not -path "*/reports*" \
  -not -path "*/beta*" | sort
```

### Step 2 — Per-chapter word-level counts
Run these commands on **each chapter individually** and record results in a per-chapter table (see Report Format below):

```bash
wc -w "$FILE"                                          # Word count
grep -ic "warm" "$FILE"                                # Tier 2 frequency
grep -ic "steady" "$FILE"
grep -ic "sharp" "$FILE"
grep -ic "\bquiet" "$FILE"
grep -ic "careful" "$FILE"
grep -ic "\bjust\b" "$FILE"
grep -ic "\bvery\b" "$FILE"
grep -ic "\balmost\b" "$FILE"
grep -ic "\blike a\b" "$FILE"                          # Simile density
grep -ic "sternum" "$FILE"                             # Cross-chapter phrase fatigue
grep -ic "copper taste\|taste.*copper\|copper.*throat" "$FILE"
grep -ic "recycled air" "$FILE"
grep -ic "said quietly\|said softly\|said gently\|said firmly" "$FILE"   # Dialogue adverbs
grep -ic "found himself\|found herself" "$FILE"        # Tier 1 tells
grep -ic "breath caught" "$FILE"
grep -ic "washed over" "$FILE"
grep -ic "air between" "$FILE"
grep -ic "\bjust barely\b\|just slightly\b" "$FILE"    # Filter pairs
grep -c "^Not " "$FILE"                                # Negation-pivot lines
```

### Step 3 — Full-manuscript Tier 1 vocabulary sweep
```bash
# Concatenate all chapters to temp file
find <manuscript_dir> -name "Chapter-*.md" \
  -not -path "*/editorial*" -not -path "*/reports*" \
  -exec cat {} \; > /tmp/full_manuscript.txt

# Tier 1 vocabulary — any count > 0 is a flag
for word in "delv" "tapestry" "nuanced" "multifaceted" "intricate" \
            "testament to" "pivotal" "paramount" "transformative" \
            "myriad" "embark" "harness" "groundbreaking" "cutting.edge" \
            "underscore" "game.changing" "holistic" "plethora" "vibrant" \
            "synergy" "leverage" "seamless" "foster" "elevate" "showcase"; do
  echo "$word: $(grep -ic "$word" /tmp/full_manuscript.txt)"
done
```

### Step 4 — Staccato and paired adjective patterns
```bash
# Known AI staccato pairs (any hit is a flag)
grep -rin "Controlled\. Measured\.\|Steady\. Unwavering\.\|Professional\. Contained\.\|Careful\. Precise\." <manuscript_dir>

# Known AI paired adjectives
for pat in "vast and patient" "low and steady" "raw and unguarded" "raw and open" \
           "warm and steady" "warm and certain" "quiet and deliberate" "quiet and measured" \
           "hot and electric" "sharp and electric" "keen and steady" "dark and careful"; do
  echo "$pat: $(grep -ic "$pat" /tmp/full_manuscript.txt)"
done
```

### Step 5 — Cross-chapter phrase repetition
```bash
for phrase in "sternum" "copper taste\|taste.*copper" \
              "recycled air" "air between them"; do
  echo "$phrase: $(grep -ic "$phrase" /tmp/full_manuscript.txt)"
done
```

### Step 6 — Write the report
**Do not write the report until all chapters have been scanned.** Every chapter must appear in the per-chapter table with actual counts, not estimates or approximations.

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
| Full manuscript (multiple files) | **Mandatory Scan Protocol (grep-based)** — see above |
| Short article or scene (< 2,000 words) | `readFile` directly |
| Multiple chapters in parallel | `ctx_batch_execute` — one call, all files, search all at once |

> ⚠️ **Do NOT use `ctx_index` + `ctx_search` alone for a full manuscript scan.** Index search finds concepts; it does not count word occurrences. You will miss frequency density patterns entirely. Always use the grep-based Mandatory Scan Protocol for full-manuscript frequency analysis.

**Standard pattern for a chapter scan:**
```
ctx_execute_file(
  path="manuscript/ACT I/Chapter-01.md",
  code='print(file_content)',
  intent="AI vocabulary fingerprints, cliché phrases, punctuation overuse, fiction tells"
)
```

**Standard pattern for a full manuscript scan — use the Mandatory Scan Protocol above.** Do not substitute ctx_search index queries — they miss frequency density patterns.

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

**Phrase-Level Tells**

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

**Structural Tells — Syntactic Patterns (🔴)**

These are not vocabulary tells — they are *construction* tells. The AI defaults to these syntactic shapes regardless of word choice.

| Pattern | Example | Why It Signals AI |
|---------|---------|-------------------|
| **"Not X, it's Y" negation-pivot** | "Not a question. A command." / "Not anger. Something worse." / "Not X — Y." | AI overuses the negation-pivot as a dramatic reveal device. One per chapter is fine; 5+ per chapter is a clear tell. Scan for "Not [noun/adj]. [Noun/adj]." and "Not [noun] — [noun]." constructions. |
| **Paired adjective default** | "vast and patient," "hot and sudden," "raw and unguarded," "low and steady" | AI generates paired adjectives joined by "and" as its default description mode. Scan for `[adjective] and [adjective]` patterns in descriptive passages (not dialogue). Flag when 4+ appear per chapter. |
| **Staccato fragment pairs/triplets** | "Controlled. Measured." / "Recognition. Confirmation. The cold clarity of…" / "Professional. Contained." | AI generates short sentence fragments (1–3 words, usually adjectives, past participles, or abstract nouns) as atmospheric punctuation. Flag when 3+ instances appear per chapter. |

**Staccato Fragment Sub-Patterns (🔴)**

The staccato fragment tell has four distinct sub-types. Each is a separate signal:

| Sub-Pattern | Example | Why It's a Tell |
|-------------|---------|-----------------|
| **Decorative past-participle escalation** | "Managed. Contained. Watched." | Synonymous past-participles stacked for drama without adding information. Each word means roughly the same thing. |
| **Speech-tag + adjective pair** | "he said. Flat. Clipped." | Staccato adjectives after dialogue attribution — the AI equivalent of adverb-stacking, just formatted as fragments. |
| **Abstract noun pair + explanatory sentence** | "Recognition. Confirmation. The cold clarity of knowing…" | Fragments that require the following sentence to give them meaning. If you need the explanation, you don't need the fragments. |
| **Near-synonym pairs** | "Steady. Unwavering." / "Professional. Controlled." | Two fragment words that mean the same thing. Pure redundancy formatted as emphasis. |

**Most overused fragment words** (flag when any of these appear in fragment patterns 3+ times across a manuscript):
- "controlled," "steady," "measured," "careful," "quiet," "sharp," "contained," "professional"

**Paired Adjective Repeat Offenders** (flag as 🔴 on sight — these specific pairs recur across AI-generated fiction):

| AI-Generated Pair | Typical Context |
|--------------------|----------------|
| "vast and patient" | Space/void/silence descriptions |
| "low and steady" / "low and careful" / "low and firm" | Male character voices/actions |
| "X and electric" (hot and electric, sharp and electric) | Tension/attraction scenes |
| "warm and X" (warm and steady, warm and rough) | Comfort/intimacy descriptions |
| "raw and unguarded" / "raw and open" | Vulnerability moments |
| "quiet and deliberate" / "quiet and measured" | Character movement/speech |

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

#### Fiction Frequency Words (🟡)
These are ordinary English words that become AI tells through *volume*. One or two per chapter is fine. Flag when they exceed the threshold across a manuscript.

| Word | Per-Chapter Threshold | Manuscript Threshold | Why It Signals AI |
|------|----------------------|---------------------|-------------------|
| warm / warmth | > 5 | > 100 | AI's default positive descriptor for comfort, safety, attraction, and approval |
| steady | > 4 | > 60 | AI's default descriptor for male characters, reliable things, and calm states |
| sharp | > 4 | > 60 | AI's go-to intensity descriptor — sharp pain, sharp gaze, sharp intake of breath |
| careful / carefully | > 4 | > 60 | AI's default adverb for any action performed with attention |
| quiet / quietly | > 5 | > 80 | AI's default modifier for emotional moments, voice descriptions, and transitions |
| just | > 10 | > 150 | AI's most overused qualifier/filler — weakens every sentence it enters |
| almost | > 5 | > 60 | Hedging qualifier — AI avoids commitment to sensation or action |
| like a (simile) | > 8 | > 150 | Simile density: AI defaults to "like a [concrete noun]" for all abstract sensations rather than direct statement |
| as if / as though | > 5 | > 50 (combined) | Hypothetical framing — AI overuses to describe character perception |

#### Cross-Chapter Setting Phrase Fatigue (🟡)
These phrases are individually defensible but become an AI tell through cross-chapter repetition. Flag when they exceed the per-chapter threshold or appear in 5+ chapters:

| Phrase | Per-Chapter Threshold | Total Threshold | Notes |
|--------|----------------------|-----------------|-------|
| "[in/behind] her/his sternum" | > 3 | > 12 | AI's default location for emotional/communion sensation |
| "copper taste / tasted like copper" | > 3 | > 12 | Fine as a sensory signal marker; flagged when used non-specifically |
| "recycled air" | > 2 | > 20 | Setting-appropriate; flag as atmosphere filler above threshold |
| "air between them" | > 1 | > 4 | Cross-chapter pattern fatigue; each use must do different work |
| "deck plates" | > 2 | > 15 | Grounding detail; flag non-functional atmospheric uses |
| "said quietly / softly / gently" (dialogue) | > 2 | > 20 | Adverb-loaded tags; show via action beats instead |

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

### Triage Framework: Earned vs. AI Cliché

Not every instance of a flagged pattern requires a fix. Use this framework to classify each flag:

| Classification | Criteria | Action |
|----------------|----------|--------|
| **EARNED** | The pattern does concrete narrative work: anchors a specific sensory detail, serves character voice, creates structural irony, executes a deliberate callback, or performs technical/plot-critical function. | Leave it. Note as "earned" in report. |
| **BORDERLINE** | Generic usage, but context partially redeems it — the surrounding prose gives it enough weight, or it's the least-bad option. | Flag for human review. Include suggested alternative. |
| **AI CLICHÉ** | Decorative, redundant, or repeated to the point of pattern fatigue. Adds atmosphere but not information. Could be cut or replaced without losing meaning. | Fix. Apply rewrite rule. |

**Pattern fatigue rule**: Even an individually acceptable pattern becomes an AI tell when repeated 5+ times in a manuscript. If the same construction appears in 5+ chapters, it's a pattern regardless of whether each individual instance is "earned." Flag all instances and recommend reducing to 2–3 total.

**Thematic motif exception**: A word used as a *deliberate thematic motif* within a single chapter (e.g., "warmth" used 10× to establish warmth-as-manipulation as the chapter's central theme) is EARNED even at high frequency — provided the repetition is intentional and forms a chapter-level pattern, not random filler. Distinguish by checking whether the repetition spreads across many chapters (AI tell) or saturates one chapter with clear thematic purpose (earned motif).

**Scanning with triage**: When producing the AI Pattern Report, classify every flag as EARNED / BORDERLINE / AI CLICHÉ in the "Recommended Action" column. The triage classification drives what `ai-prose-rewrite` does with each flag.

---

### Frequency Analysis (Fiction)

Beyond vocabulary and phrase tells, AI leaves fingerprints in *word frequency*. Run these counts across the full manuscript **and per chapter individually**:

1. **Single-word frequency**: Count occurrences of every Tier 2 Fiction Frequency Word. Flag any that exceed the per-chapter or manuscript threshold.
2. **Paired adjective frequency**: Count all `[adj] and [adj]` constructions in descriptive (non-dialogue) text. More than 3 per chapter or 50+ per manuscript = flag.
3. **Fragment frequency**: Count all 1–3 word sentence fragments in non-dialogue text. More than 3 per chapter or 40+ per manuscript = flag.
4. **Negation-pivot frequency**: Count all "Not X. Y." / "Not X — Y." constructions. More than 2 per chapter or 30+ per manuscript = flag.
5. **Cross-chapter repetition**: Any specific phrase or construction appearing in 5+ chapters is a pattern — even if each instance looks fine in isolation.
6. **Setting phrase fatigue**: Count Cross-Chapter Setting Phrase Fatigue words (sternum, copper taste, recycled air, air between them). Exceeding total threshold or 3+ per chapter = flag.
7. **Simile density**: Count total "like a" and "as if/as though" per chapter. More than 8 "like a" per chapter or 150 total = flag. Simile overuse is as consistent an AI tell as vocabulary: AI describes all abstract sensation through concrete simile instead of direct statement.
8. **Filter word density**: Count `just`, `very`, `almost`, `quite`, `rather`. Flag chapters exceeding per-word thresholds. Total `just` > 150 across a manuscript is a systematic flag.

Include the frequency analysis as a section in the AI Pattern Report.

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
| 🔴 Fiction/non-fiction phrase tells | [count] | Critical |
| 🔴 Structural tells (negation-pivot, paired adj, staccato) | [count] | Critical |
| 🟡 Medium-signal vocabulary | [count] | Important |
| 🟡 Fiction frequency words (warm, steady, just, etc.) | [count] | Important |
| 🟡 Cross-chapter setting phrase fatigue | [count] | Important |
| 🟡 Simile / filter word density | [count] | Important |
| 🟠 Context-dependent | [count] | Review |
| Punctuation tics | [count] | [severity] |
| Structural patterns | [count] | [severity] |
| **Total flags** | [count] | |

### Triage Summary (Fiction)
| Classification | Count |
|----------------|-------|
| EARNED (leave) | [count] |
| BORDERLINE (human review) | [count] |
| AI CLICHÉ (fix) | [count] |

---

## Score Interpretation
- **LOW** (0–5 total flags): Natural-sounding prose with minor polish opportunities
- **MODERATE** (6–15): AI signatures present but not dominant — targeted rewrites sufficient
- **HIGH** (16–30): Significant AI footprint — systematic rewrite pass recommended
- **VERY HIGH** (31+): Heavy AI generation detected — full prose-rewrite pass required

---

## Per-Chapter Scan Table (Required for Full-Manuscript Scans)

Every chapter must appear. Bold any cell exceeding the per-chapter threshold.

| Chapter | Words | warm | steady | sharp | quiet | careful | just | almost | like_a | sternum | copper | recycled_air | T1_vocab | fiction_tells | said_quietly | negation_Not |
|---------|-------|------|--------|-------|-------|---------|------|--------|--------|---------|--------|-------------|----------|--------------|-------------|-------------|
| Ch01 | [count] | | | | | | | | | | | | | | | |
| Ch02 | | | | | | | | | | | | | | | | |
| ...  | | | | | | | | | | | | | | | | |
| **TOTAL** | | | | | | | | | | | | | | | | |

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
**Use the Mandatory Scan Protocol above.** Scan every `.md` file in the directory tree. No sampling. No skipping. Produce:
1. **The per-chapter scan table** — all chapters, all metrics (required)
2. A full-manuscript Tier 1 vocabulary sweep result
3. A consolidated AI Pattern Report
4. A ranked list of "worst offenders" (chapters with the most flags, sorted by total flag count)

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

- ❌ **Sampling instead of full scan** — a "representative sample" always misses patterns; every chapter must be individually scanned
- ❌ **Using `ctx_search` index queries alone for a full manuscript scan** — index search finds concepts, not word counts; it will miss frequency density patterns entirely
- ❌ Flagging every em-dash as an error — em-dashes are legitimate punctuation; only *overuse* is the signal
- ❌ Flagging words from the medium/context-dependent tiers without counting occurrences — one use of "robust" is not a pattern
- ❌ Rewriting inside this skill — scan only; remediation belongs to `ai-prose-rewrite`
- ❌ Applying fiction tells to non-fiction or vice versa — mode matters
- ❌ Confusing "sounds like AI" with "is bad writing" — some AI patterns overlap with genuine clichés; flag both, distinguish in the report
- ❌ Flagging every paired adjective — only flag when frequency exceeds threshold (4+ per chapter) or the pair is a known AI repeat offender
- ❌ Flagging every sentence fragment — fragments are legitimate prose tools; only flag when they match the staccato sub-patterns (near-synonyms, abstract noun pairs, past-participle escalation)
- ❌ Ignoring cross-chapter repetition — a pattern appearing once per chapter for 15 chapters is a tell even if each instance looks fine alone
- ❌ Skipping triage classification — every flag must be classified as EARNED / BORDERLINE / AI CLICHÉ to guide remediation
- ❌ Treating thematic word saturation (one word used 10× in one chapter for clear thematic purpose) the same as frequency spread (same word in 20 different chapters) — the former is often earned; the latter is always a flag
- ❌ Skipping the per-chapter scan table — aggregate counts hide per-chapter hotspots; the table is required

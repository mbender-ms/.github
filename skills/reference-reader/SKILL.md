---
name: reference-reader
description: "Analyze reference books and source material to extract prose style, narrative structure, pacing patterns, and voice characteristics. Uses context-mode to read indexed .txt files from reference-books/ directory and produces actionable style guides for fiction writing."
argument-hint: "Describe what to analyze, e.g. 'analyze the romantic tension scenes in ACOTAR' or 'extract chapter structure patterns from ACOMAF'"
user-invocable: true
---
# Reference-Reader — Source Material Analysis Skill

Read and analyze reference books to extract style patterns, voice characteristics, pacing rhythms, and structural techniques for use in fiction writing.

## When to Use

- Starting a new project and need to calibrate prose style to reference authors
- Voice is drifting mid-manuscript and needs re-anchoring
- Studying how a reference author handles a specific scene type (combat, romance, revelation)
- Extracting structural patterns (chapter length, POV switching, pacing curves)
- Building a style reference sheet from multiple source texts

---

## ⚠️ MANDATORY: Use Context-Mode for All Reading

Reference books are 80,000–150,000 words. **Never use `readFile`, `cat`, or any direct file read on reference text files.** This will destroy the context window.

**Always use context-mode:**

```
# Step 1: Index the book (or check if already indexed this session)
ctx_index(path="reference-books/[Title - Author].txt", source="ref:[short-title]")

# Step 2: Search for what you need
ctx_search(queries=["romantic tension physical awareness", "chapter opening hooks"], source="ref:[short-title]")
```

**Source labels** are in `reference-books/INDEX.md`. Check INDEX.md first.

**Note**: Context-mode indexes are session-scoped. Re-index at the start of each session before searching.

---

## Reference Library

Reference books are stored in the repository at:

```
reference-books/
├── INDEX.md                                        ← Source labels and metadata
├── raw/                                            ← Original source files (do not read directly)
├── summaries/                                      ← Pre-built style analysis documents
│   └── [Title - Author].summary.md
└── [Title - Author].txt                            ← Clean text (index with context-mode, never read directly)
```

**First check `summaries/`** — if a summary already exists for the book you need, read it directly. It is a markdown document and safe to read with `readFile`. Only re-run full analysis if the summary is missing or you need something the summary doesn't cover.

**Supported formats**: `.txt` files are the working format. Raw epub/docx/pdf live in `raw/` and must be processed by the **reference-librarian agent** before use.

---

## Analysis Workflows

### Workflow 1: Full Style Profile

Produce a comprehensive style analysis of a reference book.

**Steps:**
1. Read the `.txt` file from `reference-books/`
2. Analyze across all dimensions (see Analysis Dimensions below)
3. Produce a Style Profile document

**Output format:**
```markdown
# Style Profile: [Book Title] by [Author]

## Prose Style
- **Sentence length**: [Average, range, variation patterns]
- **Paragraph length**: [Average, how it shifts by scene type]
- **Vocabulary level**: [Accessible? Literary? Technical?]
- **Sensory density**: [How many senses per page? Which dominate?]
- **Figurative language**: [Metaphor frequency, simile style, imagery patterns]

## Narrative Voice
- **POV**: [First/third? Deep/distant? Tense?]
- **Internal monologue style**: [Stream of consciousness? Sharp observations? Emotional processing?]
- **Filter words**: [Present or absent? How does the author handle interiority?]
- **Humor**: [Present? Type? Frequency?]
- **Emotional register range**: [From what low to what high?]

## Dialogue
- **Tag style**: [Said-bookisms? Action beats? Minimal tags?]
- **Subtext level**: [How much is unsaid?]
- **Banter patterns**: [Rhythm, escalation, how it reveals character]
- **Romantic dialogue**: [How does attraction manifest in speech?]

## Pacing
- **Chapter length**: [Average word count, range]
- **Scene length**: [Average, how many scenes per chapter]
- **Chapter endings**: [Cliffhanger types, frequency]
- **Chapter openings**: [In media res? Setting? Dialogue?]
- **Tension curve**: [How does tension build and release within chapters?]

## Structure
- **Act breaks**: [Where do the major turns fall?]
- **POV pattern**: [If dual/multi POV, what's the alternation pattern?]
- **Subplot weaving**: [How are B-stories integrated?]
- **Flashback/memory usage**: [Present? How integrated?]

## Romance Craft
- **First meeting**: [How is the love interest introduced?]
- **Tension building techniques**: [Physical proximity, banter, vulnerability, danger]
- **Intimate scene style**: [Fade to black? Explicit? Emotional focus?]
- **Body language**: [How does the author convey attraction through physicality?]
- **Emotional escalation pattern**: [How does the romance deepen across the book?]
```

### Workflow 2: Scene-Type Study

Analyze how the reference author handles a specific scene type.

**Scene types to study:**
- **First encounter / meet-cute**: How does the author introduce romantic leads?
- **Action / combat**: Sentence rhythm, choreography, stakes, pacing
- **Romantic tension**: Physical awareness, internal reaction, dialogue subtext
- **Emotional climax**: The shatter moment — how is raw emotion rendered?
- **Quiet intimacy**: Post-crisis, private vulnerability, tender moments
- **Revelation / twist**: How are surprises structured and delivered?
- **Opening chapter**: Hook technique, world introduction, voice establishment
- **Chapter endings**: Cliffhanger craft, emotional landing, momentum

**Steps:**
1. Read the reference text
2. Identify 3-5 examples of the requested scene type
3. For each example, extract:
   - Opening technique
   - Pacing pattern (sentence length, paragraph rhythm)
   - Sensory details used
   - Emotional arc within the scene
   - Closing technique
4. Synthesize patterns into actionable guidance

### Workflow 3: Voice Calibration

Re-anchor the writing voice to match reference material.

**Steps:**
1. Read 2-3 chapters from the reference book (preferably matching the scene type being written)
2. Read the current manuscript's most recent chapter
3. Identify divergences in:
   - Sentence rhythm and length
   - Vocabulary register
   - Internal monologue depth and style
   - Sensory density
   - Emotional intensity
4. Produce specific, actionable corrections:
   - "Shorten sentences in action beats — reference averages 8 words, manuscript averages 15"
   - "Increase physical sensation in romantic tension — reference uses 3 body-awareness beats per page, manuscript has 1"
   - "Deepen internal monologue — reference character reacts emotionally to every plot development, manuscript character observes without processing"

### Workflow 4: Structural Pattern Extraction

Map the structural skeleton of a reference book.

**Steps:**
1. Read the full text
2. Map every chapter by:
   - Word count
   - POV character
   - Primary scene type (action, romance, intrigue, training, quiet)
   - Key plot beat
   - Key romance beat
   - Opening hook type
   - Closing hook type
3. Produce a structural map showing:
   - Pacing rhythm (action-quiet-action patterns)
   - Romance beat placement
   - Act break locations
   - Tension escalation curve

### Workflow 5: Comparative Analysis

Compare two or more reference books to identify shared techniques and differences.

**Steps:**
1. Read both texts
2. Compare across all dimensions
3. Produce a comparison table highlighting:
   - Shared techniques (the "signature" of the subgenre)
   - Divergent approaches (where each author is distinct)
   - Techniques to adopt for the current project
   - Techniques to avoid or modify for hard sci-fi adaptation

---

## Analysis Dimensions

When analyzing any text, examine these dimensions:

### Micro Level (Sentence/Paragraph)
- **Sentence length distribution**: Short (≤8 words), medium (9-20), long (21+)
- **Sentence variety**: Simple, compound, complex, fragments
- **Paragraph length**: How many sentences? How does it vary?
- **Figurative language density**: Metaphors, similes, personification per page
- **Sensory language**: Which senses, how often, how vivid
- **Verb strength**: Active vs. passive, specific vs. generic
- **Adverb/adjective usage**: Heavy or lean? Which ones?

### Macro Level (Chapter/Book)
- **Chapter length**: Word count, consistency, outliers
- **Scene count per chapter**: How many scenes? How are transitions handled?
- **POV structure**: Single, dual, rotating? Pattern?
- **Pacing pattern**: How does the author alternate tension and release?
- **Information delivery**: How is worldbuilding woven in? Dialogue? Action? Reflection?
- **Romantic pacing**: Where do key beats fall as a percentage of total?

### Emotional Level
- **Emotional range**: What emotions are most frequently evoked?
- **Intensity curve**: How does emotional intensity build across the book?
- **Catharsis moments**: Where and how does the author provide emotional release?
- **Reader manipulation techniques**: What makes you turn the page? What makes you gasp?

---

## Tips for Effective Reference Reading

1. **Read targeted sections, not always full books** — If you need to calibrate action scene pacing, read 3 action scenes, not the whole novel
2. **Read the opening and closing of every chapter** — This reveals hook and cliffhanger patterns most efficiently
3. **Read romantic tension scenes back-to-back** — This reveals the escalation pattern across the book
4. **Compare early chapters to late chapters** — Voice, pacing, and intensity often shift as a book progresses
5. **Note what's absent** — What the author doesn't describe is as telling as what they do

---

## Anti-Patterns

- ❌ Copying prose verbatim — extract patterns and techniques, never copy sentences or passages
- ❌ Analyzing without purpose — always have a specific question driving the analysis
- ❌ Over-indexing on one reference — blend techniques from multiple sources
- ❌ Ignoring genre translation — what works in fantasy may need adaptation for hard sci-fi
- ❌ Treating reference analysis as a one-time event — re-read references throughout the writing process to maintain calibration

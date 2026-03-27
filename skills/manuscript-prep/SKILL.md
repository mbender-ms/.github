---
name: manuscript-prep
description: Validate and prepare a markdown manuscript for Pandoc → EPUB conversion and Amazon KDP upload. Checks structure, headings, scene breaks, front/back matter, and common formatting issues.
argument-hint: Path to manuscript file or directory (e.g., ./manuscript.md or ./chapters/)
user-invocable: true
---

# Manuscript preparation for KDP

Validate and prepare a markdown manuscript so it's structurally ready for Pandoc → EPUB conversion and Amazon KDP upload.

## When to use

Run this skill **before** the epub-build pipeline. Every manuscript must pass these checks first. The skill scans for structural problems, fixes common issues automatically, and generates a validation report.

## Manuscript structure requirements

### YAML front matter

Every manuscript must begin with a YAML metadata block. Pandoc reads this to populate EPUB metadata fields that KDP requires.

```yaml
---
title: "Your Book Title"
author: "Author Name"
language: en-US
rights: "© 2025 Author Name. All rights reserved."
publisher: "Publisher Name or Self-Published"
date: "2025-01-15"
description: "A one-paragraph book description for metadata."
cover-image: "cover.jpg"
---
```

All fields are required. The `cover-image` path is relative to the working directory.

### Front matter pages

Front matter appears before the first body chapter. Structure it in this order:

1. **Title page** — Centered H1 with the book title, followed by the author name. This is the only place an H1 appears outside of chapter headings.
2. **Copyright page** — Copyright notice, edition info, ISBN (if applicable), and rights statement.
3. **Dedication** (optional) — Short dedication text, typically italicized.
4. **Epigraph** (optional) — An opening quote or passage that sets the tone.

### Body chapters

- **H1 (`#`) = chapter titles ONLY.** Each H1 triggers a chapter break in the EPUB output. Never use H1 for anything else.
- **H2 (`##`) = section headings** within chapters for thematic or structural divisions.
- **H3 (`###`)** = subsections within an H2 section if needed.
- **Never skip heading levels.** H1 → H3 without an H2 in between is invalid and breaks navigation.

### Scene breaks

Use a horizontal rule (`---`) for scene breaks within a chapter. Do **not** use new headings, extra blank lines, or decorative characters.

```markdown
The door slammed shut behind her.

---

Three hours later, the phone rang.
```

The EPUB stylesheet renders `---` as centered `* * *` glyphs. Let CSS handle the visual presentation.

### Back matter

Include these sections after the final chapter:

- **Acknowledgments** — Thank contributors, editors, beta readers.
- **About the author** — Author bio with relevant links.
- **Also by** — List of other works by the author.
- **Glossary** (for sci-fi, fantasy, or technical works) — Key terms and definitions.

Each back matter section uses an H1 heading to trigger a chapter break.

### Page breaks

H1 headings become chapter breaks automatically in the EPUB output. No manual page break markup is needed. Pandoc handles this natively.

## Validation checklist

The skill runs through every check in this list and reports pass/fail for each:

1. **YAML front matter present and complete** — All required fields exist and have values.
2. **Exactly one H1 per chapter** — No chapter contains multiple H1 headings. No H1 used for non-chapter content.
3. **No skipped heading levels** — H1 → H3 without an intervening H2 is flagged as invalid.
4. **Scene breaks use `---`** — Not headings, not sequences of blank lines, not decorative characters.
5. **No unsupported raw HTML** — Kindle's rendering engine ignores or breaks on most raw HTML. Flag any `<div>`, `<span>`, `<style>`, or `<script>` tags.
6. **No page numbers in body text** — Page references are meaningless in a reflowable ebook. Flag strings like "Page 12" or "see p. 42".
7. **All images exist** — Every image referenced in the manuscript has a corresponding file in the `images/` directory.
8. **Front matter pages present and correctly structured** — Title page and copyright page exist at minimum.
9. **Back matter present** — At least an "About the author" section exists.
10. **No orphaned footnotes or broken links** — Every `[^n]` reference has a matching definition, and every internal link target exists.
11. **Consistent em-dash style** — Uses `—` (em-dash), not `--` (double hyphen).
12. **Consistent quote style** — Curly quotes are handled by Pandoc's `+smart` extension. Flag manually inserted curly quote characters.
13. **No tabs** — Indentation must use spaces only. Tabs cause inconsistent rendering on Kindle devices.
14. **Chapter numbering is sequential** — Chapter numbers (if used) follow a logical sequence with no gaps.
15. **Word count report per chapter** — Generates a table of word counts for each chapter.

## Multi-file manuscript support

### Single-file manuscript

Everything lives in one file:

```
manuscript.md
```

The YAML front matter block goes at the top. Chapters are separated by H1 headings.

### Multi-file manuscript

For longer works, split the manuscript into individual files:

```
front-matter.md
chapter-01.md
chapter-02.md
chapter-03.md
...
chapter-NN.md
back-matter.md
```

**Naming conventions:**

- Use zero-padded chapter numbers (`chapter-01.md`, not `chapter-1.md`) so files sort correctly.
- The YAML front matter block goes in `front-matter.md` only.
- Each chapter file starts with an H1 heading (the chapter title).
- `back-matter.md` contains all back matter sections.

**Build command difference:**

For a single file:

```bash
pandoc manuscript.md -o book.epub --css=epub-styles.css
```

For multi-file, list all files in reading order:

```bash
pandoc front-matter.md chapter-01.md chapter-02.md chapter-03.md back-matter.md \
  -o book.epub --css=epub-styles.css
```

Or use a glob (if files are named to sort correctly):

```bash
pandoc front-matter.md chapter-*.md back-matter.md \
  -o book.epub --css=epub-styles.css
```

## Working directory structure

```
/my-book/
├── manuscript.md        (or individual chapter files)
├── cover.jpg            (2560 x 1600 px, JPEG)
├── epub-styles.css      (custom stylesheet)
└── images/              (any inline images)
```

- **cover.jpg** — Amazon KDP recommends 2560 × 1600 pixels for the cover image. Must be JPEG format.
- **epub-styles.css** — Controls scene break rendering, drop caps, block quotes, and other visual styling in the EPUB.
- **images/** — All inline images referenced in the manuscript. Use descriptive filenames and always include alt text.

## Common fixes

The skill performs these automatic corrections when possible:

| Issue | Fix |
|---|---|
| Missing YAML fields | Adds missing fields with placeholder values and flags for review |
| Heading level skips | Adjusts heading levels to maintain proper hierarchy |
| Double hyphens (`--`) in prose | Converts to em-dashes (`—`) |
| Inconsistent scene breaks | Standardizes all scene breaks to `---` |
| Page numbers in body | Strips "Page X" and "p. X" references from body text |
| Word count report | Generates per-chapter word count table |
| Short chapters | Flags chapters under 1,500 words as potentially too short |
| Long chapters | Flags chapters over 8,000 words as potentially too long |

## Anti-patterns

Avoid these common mistakes in ebook manuscripts:

- ❌ **Using H1 for anything other than chapter titles** — H1 triggers chapter breaks. Using it for emphasis or decoration creates empty chapters in the EPUB.
- ❌ **Manual "Page X" references** — Reflowable ebooks have no fixed pages. These references are meaningless to the reader.
- ❌ **Inline HTML for formatting** — Kindle's rendering engine handles HTML inconsistently. Use markdown combined with CSS in `epub-styles.css` instead.
- ❌ **Images without alt text** — Required for accessibility and flagged by KDP's quality checks.
- ❌ **Tabs instead of spaces** — Tab rendering varies across Kindle devices and apps. Use spaces only.
- ❌ **Smart quotes done manually** — Don't type or paste curly quotes. Use straight quotes in the source and let Pandoc convert them with the `+smart` extension during build.

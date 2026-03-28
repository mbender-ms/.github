---
name: reference-ingest
description: "Convert raw reference materials (epub, docx, pdf, txt, markdown) to clean indexed text using calibre. Validates output quality, cleans conversion artifacts, and prepares files for context-mode indexing. The ingestion layer for the reference library."
argument-hint: "Provide file path to ingest, e.g. 'reference-books/raw/ACOTAR.epub'"
user-invocable: false
---
# Reference Ingest — Conversion Pipeline Skill

Convert raw reference materials to clean, indexed text for the fiction writing pipeline.

---

## When to Use

Invoked by the **reference-librarian agent** as Step 2 of the ingest workflow. Not typically invoked directly by the user.

---

## Supported Input Formats

| Format | Conversion Method | Notes |
|---|---|---|
| `.epub` | calibre `ebook-convert` | Best quality — preserves chapter structure |
| `.docx` | calibre `ebook-convert` | Good quality — may lose complex formatting |
| `.pdf` | calibre `ebook-convert` | Text-only PDFs only — scanned images will fail |
| `.txt` | No conversion needed | Move to `reference-books/`, validate encoding |
| `.md` | No conversion needed | Move to `reference-books/`, convert to `.txt` if needed |

---

## Calibre Conversion Commands

### EPUB to TXT
```bash
ebook-convert "reference-books/raw/[filename].epub" "reference-books/[Title - Author].txt" \
  --enable-heuristics \
  --txt-output-encoding utf-8 \
  --newline unix
```

### DOCX to TXT
```bash
ebook-convert "reference-books/raw/[filename].docx" "reference-books/[Title - Author].txt" \
  --txt-output-encoding utf-8 \
  --newline unix
```

### PDF to TXT
```bash
ebook-convert "reference-books/raw/[filename].pdf" "reference-books/[Title - Author].txt" \
  --txt-output-encoding utf-8 \
  --newline unix
```

**Calibre path**: `/opt/homebrew/bin/ebook-convert` (macOS) or `ebook-convert` (if in PATH)

**Output naming convention**: `[Title - Author].txt`
- Example: `A Court of Thorns and Roses - Sarah J. Maas.txt`
- Example: `Fourth Wing - Rebecca Yarros.txt`
- No special characters, consistent spacing

---

## Output Validation

After conversion, always validate before proceeding:

### Step 1: Word Count Check
```bash
wc -w "reference-books/[Title - Author].txt"
```

Minimum acceptable word counts by format:
- Novel (epub/docx/pdf): ≥ 60,000 words
- Novella: ≥ 20,000 words
- Short story collection: ≥ 15,000 words

If word count is less than 60% of expected, **stop and report**. Do not proceed with a degraded conversion.

### Step 2: Encoding Check
```bash
file "reference-books/[Title - Author].txt"
```
Must return `UTF-8 Unicode text` or `ASCII text`. If it returns binary or unknown, the conversion failed.

### Step 3: Spot Check
Read the first 500 words and last 500 words of the output file. Verify:
- Readable prose, not garbled characters
- No XML/HTML markup artifacts (`<p>`, `&amp;`, `&#160;`, etc.)
- Chapter headings are present and readable
- No excessive blank lines or spacing artifacts

---

## Common Conversion Issues and Fixes

### Problem: Garbled Unicode Characters
**Symptom**: `â€™` instead of `'`, `Ã©` instead of `é`
**Fix**: Add `--input-encoding utf-8` to the conversion command

### Problem: Missing Content / Too Short
**Symptom**: Word count is far below expected
**Cause**: DRM-protected epub (calibre cannot strip DRM), or corrupted source file
**Fix**: Report to user — source file may need to be re-acquired in a different format or DRM removed separately before ingestion

### Problem: HTML Artifacts in Output
**Symptom**: `<br/>`, `&nbsp;`, `<em>` etc. visible in text
**Fix**: Run a post-processing clean pass:
```python
import re

with open("reference-books/[Title - Author].txt", "r", encoding="utf-8") as f:
    text = f.read()

# Remove HTML tags
text = re.sub(r'<[^>]+>', '', text)
# Normalize HTML entities
text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&#160;', ' ')
# Normalize whitespace
text = re.sub(r'\n{3,}', '\n\n', text)
text = re.sub(r' {2,}', ' ', text)

with open("reference-books/[Title - Author].txt", "w", encoding="utf-8") as f:
    f.write(text)
```

### Problem: No Chapter Breaks
**Symptom**: One long wall of text with no structure
**Fix**: This is acceptable for analysis — context-mode can still index and search it. Note in INDEX.md that chapter structure was not preserved.

### Problem: Page Numbers / Headers / Footers Embedded
**Symptom**: Repeated strings like "Chapter 1 · 47" or "SARAH J. MAAS" appearing every few paragraphs
**Fix**: Post-process to remove:
```python
import re

with open("reference-books/[Title - Author].txt", "r", encoding="utf-8") as f:
    text = f.read()

# Remove page number artifacts (customize pattern to match the specific file)
text = re.sub(r'\n[A-Z\s·]+\d+\n', '\n', text)

with open("reference-books/[Title - Author].txt", "w", encoding="utf-8") as f:
    f.write(text)
```

---

## Context-Mode Indexing

After successful conversion and validation, index the file:

```
ctx_index(
  path="reference-books/[Title - Author].txt",
  source="ref:[short-title]"
)
```

**Short title conventions**:
- `ref:acotar` — A Court of Thorns and Roses
- `ref:acomaf` — A Court of Mist and Fury
- `ref:fourth-wing` — Fourth Wing
- `ref:iron-flame` — Iron Flame

Record the source label in `INDEX.md` — the writing pipeline uses this label to search the reference material.

---

## What NOT to Do

- **Do not use `cat` or `readFile` to dump reference texts into context.** A novel is 80,000–150,000 words. This will destroy the context window. Always use context-mode.
- **Do not convert without validating.** A silent calibre failure produces a near-empty file that wastes analysis time.
- **Do not delete files from `raw/`.** They are the source backup. If conversion fails or the text needs to be re-processed, the raw file must still be there.
- **Do not ingest the same book twice.** Check `INDEX.md` first.

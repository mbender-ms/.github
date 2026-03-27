---
name: epub-build
description: Convert a prepared markdown manuscript into a KDP-ready EPUB using Pandoc. Handles the build pipeline, validation, and output verification.
argument-hint: Build an EPUB from the validated manuscript
user-invocable: true
---

# EPUB build

## Purpose

Convert a prepared markdown manuscript into a KDP-ready EPUB using Pandoc. This skill handles the actual build pipeline — taking validated markdown source files and producing an EPUB that meets Amazon KDP's formatting and structural requirements.

## When to use

After `manuscript-prep` has validated the source files. This skill runs the conversion. Don't use this skill on unvalidated manuscripts — run `manuscript-prep` first to catch structural issues before they become build errors.

## Prerequisites

- **Pandoc installed**
  - macOS: `brew install pandoc`
  - Windows: `winget install pandoc`
  - Linux: `apt install pandoc`
- **Java installed** (for EPUBCheck in the validation step)
- **Manuscript validated** by the `manuscript-prep` skill
- **Cover image ready** — 2560 × 1600 px JPEG recommended, minimum 1000 × 625 px
- **Custom CSS stylesheet** — use the `epub-stylesheet` skill or provide a default `epub-styles.css`

## Build commands

### Standard single-file build

```bash
pandoc manuscript.md \
  -o mybook.epub \
  --epub-cover-image=cover.jpg \
  --toc \
  --toc-depth=1 \
  --css=epub-styles.css \
  --metadata title="Your Book Title" \
  --metadata author="Your Pen Name"
```

### Multi-file build

```bash
pandoc \
  front-matter.md \
  chapter-01.md chapter-02.md ... \
  back-matter.md \
  -o mybook.epub \
  --epub-cover-image=cover.jpg \
  --toc \
  --toc-depth=1 \
  --css=epub-styles.css
```

When using multi-file builds, metadata is typically defined in a YAML metadata block in `front-matter.md` rather than on the command line.

## Flag reference

| Flag | Purpose |
|---|---|
| `-o mybook.epub` | Output filename; `.epub` extension triggers EPUB output |
| `--epub-cover-image=cover.jpg` | Embeds cover into EPUB |
| `--toc` | Auto-generates Table of Contents from headings |
| `--toc-depth=1` | TOC depth: 1 = chapter level only (H1) |
| `--css=epub-styles.css` | Applies custom stylesheet |
| `--epub-chapter-level=1` | Splits at H1 (default); set to 2 if using H1 for Parts |

## Automation script

### Bash (macOS / Linux)

```bash
#!/bin/bash
set -e
MANUSCRIPT="$1"
TITLE="$2"
AUTHOR="$3"
OUTPUT="${MANUSCRIPT%.md}.epub"
COVER="cover.jpg"
CSS="epub-styles.css"

if [ -z "$MANUSCRIPT" ] || [ -z "$TITLE" ] || [ -z "$AUTHOR" ]; then
  echo "Usage: ./build-ebook.sh <manuscript.md> \"Book Title\" \"Author Name\""
  exit 1
fi

echo "Building EPUB: $OUTPUT"
pandoc "$MANUSCRIPT" \
  -o "$OUTPUT" \
  --epub-cover-image="$COVER" \
  --toc \
  --toc-depth=1 \
  --css="$CSS" \
  --metadata title="$TITLE" \
  --metadata author="$AUTHOR"

echo "Validating with EPUBCheck..."
java -jar epubcheck.jar "$OUTPUT"
echo "Done. Output: $OUTPUT"
```

### PowerShell (Windows)

```powershell
param(
    [Parameter(Mandatory)][string]$Manuscript,
    [Parameter(Mandatory)][string]$Title,
    [Parameter(Mandatory)][string]$Author
)

$ErrorActionPreference = "Stop"
$Output = [System.IO.Path]::ChangeExtension($Manuscript, ".epub")
$Cover = "cover.jpg"
$CSS = "epub-styles.css"

Write-Host "Building EPUB: $Output"
pandoc $Manuscript `
    -o $Output `
    --epub-cover-image=$Cover `
    --toc `
    --toc-depth=1 `
    --css=$CSS `
    --metadata title="$Title" `
    --metadata author="$Author"

Write-Host "Validating with EPUBCheck..."
java -jar epubcheck.jar $Output
Write-Host "Done. Output: $Output"
```

Usage:

```powershell
.\build-ebook.ps1 -Manuscript "manuscript.md" -Title "Book Title" -Author "Author Name"
```

## Build profiles

### 1. Draft

Minimal build for quick previews during writing. No cover, no validation.

```bash
pandoc manuscript.md \
  -o draft.epub \
  --toc \
  --toc-depth=1
```

### 2. Review

Full build with cover and TOC for beta readers. No validation.

```bash
pandoc manuscript.md \
  -o review.epub \
  --epub-cover-image=cover.jpg \
  --toc \
  --toc-depth=1 \
  --css=epub-styles.css \
  --metadata title="Your Book Title" \
  --metadata author="Your Pen Name"
```

### 3. Production

Full build with EPUBCheck validation and Kindle Previewer check for KDP upload.

```bash
pandoc manuscript.md \
  -o mybook.epub \
  --epub-cover-image=cover.jpg \
  --toc \
  --toc-depth=1 \
  --css=epub-styles.css \
  --metadata title="Your Book Title" \
  --metadata author="Your Pen Name"

# Validate EPUB structure
java -jar epubcheck.jar mybook.epub

# Preview in Kindle Previewer (macOS)
open -a "Kindle Previewer 3" mybook.epub
```

Always use the **Production** profile before uploading to KDP.

## Troubleshooting common build errors

| Error | Cause | Fix |
|---|---|---|
| `pandoc: command not found` | Pandoc not installed | Install: `brew install pandoc` (macOS), `winget install pandoc` (Windows), `apt install pandoc` (Linux) |
| Cover image not found | Wrong path or filename | Verify the path is relative to the working directory and the file exists |
| CSS not applying | Bad file path or syntax errors | Check the file path passed to `--css`, open the CSS file and verify no syntax errors |
| TOC not generating | Missing headings or flag | Ensure H1 headings (`#`) exist in the manuscript and `--toc` flag is present |
| Chapter breaks not working | Incorrect heading usage | Verify H1 (`#`) is used for chapter titles only — don't use H1 for scene headings |
| Encoding issues | Non-UTF-8 characters | Ensure all source files are saved as UTF-8; convert with `iconv` if needed |
| Images missing in EPUB | Broken paths | Verify image paths are relative to the markdown file and the image files exist |

## Post-build verification

After a successful build, verify the output before uploading to KDP:

1. **Open in Calibre viewer**: `ebook-viewer mybook.epub`
2. **Check chapter count** — confirm it matches the number of H1 headings in the source
3. **Verify TOC links** — every entry in the Table of Contents should navigate to the correct chapter
4. **Confirm cover displays** — the cover image should appear as the first page
5. **Check scene breaks** — scene breaks should render as `* * *` (three spaced asterisks)

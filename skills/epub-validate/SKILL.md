---
name: epub-validate
description: Validate an EPUB file for Amazon KDP compliance using EPUBCheck, Kindle Previewer, and a pre-upload checklist.
argument-hint: Path to the EPUB file to validate (e.g., output/mybook.epub)
user-invocable: true
---

# EPUB Validation Skill

## Purpose

Validate an EPUB file to ensure zero errors before uploading to Amazon KDP. Catches problems locally that would cause KDP rejection.

## When to use

After `epub-build` has created the EPUB. Always run before uploading to KDP.

## Validation pipeline

The validation pipeline has four stages. All four must pass before an EPUB is ready for upload.

Before running any validation, confirm the required tools are installed on this workstation. **This skill only runs on macOS or Windows.** Do not attempt to run the Kindle Previewer stage on Linux.

#### Detect operating system

**macOS:**
```bash
uname -s   # returns "Darwin"
```

**Windows (PowerShell):**
```powershell
[System.Environment]::OSVersion.Platform   # returns "Win32NT"
```

#### Check Kindle Previewer is installed

**macOS** — check default install location:
```bash
ls "/Applications/Kindle Previewer 3.app" 2>/dev/null && echo "INSTALLED" || echo "NOT FOUND"
```

**Windows (PowerShell)** — check both common locations:
```powershell
$paths = @(
  "$env:LOCALAPPDATA\Amazon\Kindle Previewer 3\KindlePreviewer.exe",
  "$env:ProgramFiles\Amazon\Kindle Previewer 3\KindlePreviewer.exe"
)
$found = $paths | Where-Object { Test-Path $_ }
if ($found) { "INSTALLED: $found" } else { "NOT FOUND" }
```

#### If Kindle Previewer is NOT installed

**Stop. Do not proceed.** Instruct the user to install it before validation:

> Kindle Previewer 3 is required and was not found on this workstation.
> Download from: https://kdp.amazon.com/en_US/help/topic/G202131170
> Install it, then re-run this skill.

#### Check EPUBCheck JAR is available

```bash
# macOS / Windows Git Bash
ls epubcheck.jar 2>/dev/null || find ~ -name "epubcheck*.jar" 2>/dev/null | head -5
```

If not found, download from <https://github.com/w3c/epubcheck/releases> and note the path.

#### Check Java runtime

```bash
java -version 2>&1 | head -1
```

If Java is missing:
- **macOS**: `brew install openjdk`
- **Windows**: Download from [adoptium.net](https://adoptium.net)

Only proceed to Stage 1 when all three tools are confirmed: OS is macOS or Windows, Kindle Previewer is installed, Java + EPUBCheck JAR are available.

### Stage 1: EPUBCheck validation

EPUBCheck is the industry-standard EPUB 3 validator. KDP runs its own internal validation, but EPUBCheck catches errors before upload.

#### Installation

- **macOS**: `brew install openjdk`
- **Windows**: Download from [adoptium.net](https://adoptium.net)
- **Linux**: `sudo apt install default-jdk`

Download the EPUBCheck JAR from <https://github.com/w3c/epubcheck/releases>.

#### Running EPUBCheck

```bash
java -jar epubcheck.jar mybook.epub
```

- **Success**: "No errors or warnings detected."
- **Failure**: Fix any errors in source markdown or CSS, rebuild with `epub-build`, then re-validate.

#### Common EPUBCheck errors and fixes

| Error | Cause | Fix |
|---|---|---|
| `OPF-054` | Missing required metadata | Add missing YAML front matter fields |
| `CSS-008` | Invalid CSS property | Remove unsupported CSS (e.g., `position: fixed`) |
| `HTM-004` | Invalid XHTML | Fix HTML entities, close unclosed tags |
| `RSC-005` | Referenced resource missing | Verify all images/files exist and paths are correct |
| `PKG-008` | Duplicate entry | Remove duplicate files from build |
| `NAV-001` | Navigation document error | Ensure TOC is properly generated |

### Stage 2: Content integrity check

Verifies the EPUB contains the same content as the source manuscript. A structurally valid EPUB can still be missing chapters, have truncated text, or contain a stale build. This check catches those silently before Kindle Previewer.

#### Step 1: Count chapters in source markdown

```bash
# Count H1 headings used as chapter markers in the source
grep -c "^# Chapter" manuscript.md
```

Or if using separate chapter files:
```bash
ls the-remnant-divide/manuscript/book1/ACT*/Part*/Chapter-*.md | wc -l
```

#### Step 2: Count chapters in the EPUB

Unzip the EPUB (it's a ZIP archive) and count content documents:

```bash
# macOS / Git Bash
mkdir -p /tmp/epub-check && cp mybook.epub /tmp/epub-check/mybook.zip
unzip -o /tmp/epub-check/mybook.zip -d /tmp/epub-check/epub-contents > /dev/null
# Count HTML content files (each chapter = one file)
ls /tmp/epub-check/epub-contents/EPUB/*.xhtml 2>/dev/null | wc -l || \
ls /tmp/epub-check/epub-contents/OEBPS/*.xhtml 2>/dev/null | wc -l
```

**Expected**: chapter count in EPUB ≥ chapter count in source. If lower, the build is incomplete — stop and rebuild.

#### Step 3: Compare word counts

```bash
# Word count of source manuscript
wc -w manuscript.md

# Word count of EPUB text content (strip HTML tags)
cat /tmp/epub-check/epub-contents/EPUB/*.xhtml | \
  sed 's/<[^>]*>//g' | \
  tr -s ' \n\t' '\n' | \
  wc -w
```

**Acceptable variance**: ±5% between source and EPUB word counts (Pandoc adds/removes minor structural words). If the EPUB word count is more than 5% lower than the source, content was lost in the build — stop and rebuild.

#### Step 4: Spot-check first and last chapters

Verify the first chapter heading and last chapter's final paragraph appear in the EPUB content:

```bash
# Check first chapter exists
grep -l "Chapter One\|Chapter 1\|# Chapter" /tmp/epub-check/epub-contents/EPUB/*.xhtml | head -1

# Check last chapter exists — search for a phrase from the final chapter
grep -r "YOUR_FINAL_CHAPTER_CLOSING_PHRASE" /tmp/epub-check/epub-contents/EPUB/
```

#### Content integrity: pass criteria

- [ ] Chapter count in EPUB matches source (within ±1 for front/back matter differences)
- [ ] Word count within ±5% of source manuscript
- [ ] First chapter heading found in EPUB content
- [ ] Final chapter closing line found in EPUB content
- [ ] No EPUB content files are 0 bytes

**If any check fails**: Rebuild the EPUB with `epub-build` before proceeding. Do not continue to Stage 3.

---

### Stage 3: Kindle Previewer testing

Amazon's official preview tool simulates all Kindle devices. Installation was verified in Stage 0.

#### Launch Kindle Previewer

**macOS:**
```bash
open "/Applications/Kindle Previewer 3.app" --args mybook.epub
```

**Windows (PowerShell):**
```powershell
& "$env:LOCALAPPDATA\Amazon\Kindle Previewer 3\KindlePreviewer.exe" mybook.epub
```

#### Testing procedure

Open the EPUB in Kindle Previewer and test on at least **two** device profiles:

1. **Kindle E-reader (Paperwhite)** — grayscale, smaller screen
2. **Kindle Fire / Phone** — color, larger screen

#### What to check in Kindle Previewer

- Chapter breaks appear at correct locations
- TOC links navigate correctly
- Cover image displays properly
- Fonts render consistently
- Scene breaks (`***`) display correctly
- No text cutoff or overflow
- Images not clipped or distorted
- Italic/bold formatting preserved
- Em-dashes and curly quotes render correctly

### Stage 4: Pre-upload checklist

#### eBook (EPUB) final checklist

- [ ] EPUBCheck reports zero errors and zero warnings
- [ ] Kindle Previewer displays all chapters correctly on at least two device profiles
- [ ] Table of Contents links resolve to the correct chapters
- [ ] Cover image is sharp and correctly proportioned (2560 × 1600 px recommended)
- [ ] No page numbers in the EPUB body (page numbers are meaningless in reflowable eBooks)
- [ ] YAML metadata matches what will be entered in the KDP dashboard
- [ ] Scene breaks render as * * * (not raw horizontal rules)
- [ ] First chapter opens correctly (no blank pages before chapter 1)
- [ ] Em-dashes, curly quotes, and special characters render correctly
- [ ] No broken internal links
- [ ] File size is reasonable (< 50 MB for KDP, < 650 MB absolute max)

## Validation report format

The skill produces a structured report:

```markdown
# EPUB Validation Report

## File: mybook.epub
## Date: YYYY-MM-DD

### Stage 0: Environment Check
- OS: macOS / Windows
- Kindle Previewer: INSTALLED / NOT FOUND
- Java: INSTALLED / NOT FOUND
- EPUBCheck JAR: FOUND at [path] / NOT FOUND

### Stage 1: EPUBCheck Results
- Status: PASS / FAIL
- Errors: N
- Warnings: N
- Details: [list any issues]

### Stage 2: Content Integrity Results
- Source chapter count: N
- EPUB chapter count: N — PASS / FAIL
- Source word count: N
- EPUB word count: N (±X%) — PASS / FAIL
- First chapter found: PASS / FAIL
- Final chapter found: PASS / FAIL

### Stage 3: Kindle Previewer Results
- Devices tested: [list]
- Chapter breaks: PASS / FAIL
- TOC navigation: PASS / FAIL
- Cover display: PASS / FAIL
- Formatting: PASS / FAIL
- Issues: [list any issues]

### Stage 4: Pre-Upload Checklist
- [x/] Item 1...
- [x/] Item 2...

### Verdict: READY FOR UPLOAD / NEEDS FIXES
```

## Anti-patterns

- ❌ Uploading without running EPUBCheck first
- ❌ Testing on only one device profile
- ❌ Ignoring warnings (some warnings become errors on KDP)
- ❌ Skipping Kindle Previewer because "it looks fine in Calibre"
- ❌ Skipping the content integrity check — a zero-error EPUB can still be missing chapters
- ❌ Running on Linux — Kindle Previewer is not available; use macOS or Windows

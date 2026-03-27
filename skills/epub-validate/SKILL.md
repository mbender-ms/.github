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

The validation pipeline has three stages. All three must pass before an EPUB is ready for upload.

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

### Stage 2: Kindle Previewer testing

Amazon's official preview tool simulates all Kindle devices.

#### Setup

- Download from <https://kdp.amazon.com/en_US/help/topic/G202131170>
- Available on macOS and Windows only
- **Linux alternative**: Use Calibre viewer or KDP Online Previewer

#### Testing procedure

Open Book → select the EPUB → test on at least **two** device profiles:

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

#### Linux alternative

```bash
ebook-viewer mybook.epub
```

Calibre's `ebook-viewer` provides a reasonable approximation but doesn't replicate Kindle-specific rendering.

### Stage 3: Pre-upload checklist

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

### EPUBCheck Results
- Status: PASS / FAIL
- Errors: N
- Warnings: N
- Details: [list any issues]

### Kindle Previewer Results
- Devices tested: [list]
- Chapter breaks: PASS / FAIL
- TOC navigation: PASS / FAIL
- Cover display: PASS / FAIL
- Formatting: PASS / FAIL
- Issues: [list any issues]

### Pre-Upload Checklist
- [x/] Item 1...
- [x/] Item 2...

### Verdict: READY FOR UPLOAD / NEEDS FIXES
```

## Anti-patterns

- ❌ Uploading without running EPUBCheck first
- ❌ Testing on only one device profile
- ❌ Ignoring warnings (some warnings become errors on KDP)
- ❌ Skipping Kindle Previewer because "it looks fine in Calibre"

---
name: kdp-upload
description: Guide through the complete Amazon KDP dashboard workflow — from account setup to clicking Publish. Covers everything after the EPUB is built and validated.
argument-hint: Ask about any step in the KDP publishing process
user-invocable: true
---

# KDP Upload & Publishing Skill

## Purpose

Guide through the complete Amazon KDP dashboard workflow — from account setup to clicking **Publish Your Kindle eBook**. This skill covers everything AFTER the EPUB is built and validated.

## When to use

Use this skill when the EPUB has passed validation (epub-validate skill) and is ready for upload to Amazon.

## KDP account setup

If this is your first time publishing:

1. Go to [https://kdp.amazon.com](https://kdp.amazon.com)
1. Sign in with your Amazon account or create a new one
1. Complete tax information (required before publishing)
1. Set up payment/banking information
1. Verify identity if prompted

> [!IMPORTANT]
> You cannot publish until tax and banking information are complete. Start this early — identity verification can take several business days.

## The three-page KDP publishing flow

### Page 1: Kindle eBook Details

| Field | What to Enter | Notes |
|---|---|---|
| Language | English | Match your YAML `language` field |
| Book Title | Your title | Must match title page exactly |
| Subtitle | Optional | Appears in search, adds discoverability |
| Series | Series name + volume number | Critical for multi-book series — enter both |
| Edition Number | Usually 1 | Increment for major revisions |
| Author | Primary author name | Your pen name |
| Contributors | Optional | Editor, cover designer, etc. |
| Description | Book blurb (4000 char max) | HTML formatting allowed: `<b>`, `<i>`, `<br>`, `<h4>`, `<p>` |
| Publishing Rights | "I own the copyright" | For original work |
| Keywords | Up to 7 keywords/phrases | Critical for discoverability — use specific genre phrases |
| Categories | Select 2-3 BISAC categories | Browse path matters — pick the most specific subcategory |
| Age and Grade Range | Optional | Set if writing YA or children's |
| Pre-order | Optional | Can set up to 90 days in advance |

#### Keywords strategy for romantic sci-fi

- Use phrases, not single words
- Examples: "enemies to lovers science fiction", "space opera romance", "military academy romance", "fated mates sci-fi", "slow burn space romance", "romantasy science fiction", "dual POV romance"
- Don't repeat words already in title/subtitle
- Research with Publisher Rocket, KDP search bar autocomplete, or Amazon bestseller categories

#### Categories for our genre

- Science Fiction > Space Opera
- Science Fiction > Military
- Romance > Science Fiction
- Romance > Fantasy (if applicable)
- Fiction > Science Fiction > Romance

### Page 2: Kindle eBook Content

| Field | What to Enter | Notes |
|---|---|---|
| Manuscript | Upload .epub file | The file from epub-build |
| DRM | Enable or Disable | Recommendation: Enable for fiction |
| Cover | Upload cover.jpg separately | 2560 x 1600 px, JPEG or TIFF, RGB color |
| Book Preview | Launch Online Previewer | Check every chapter one more time |

#### Cover specifications

- Ideal: 2560 x 1600 pixels (height x width)
- Minimum: 1000 x 625 pixels
- Aspect ratio: 1.6:1
- Format: JPEG or TIFF
- Color space: RGB (not CMYK)
- Max file size: 50 MB
- DPI: 300 for best quality
- Upload separately — don't rely on the embedded EPUB cover alone

#### DRM decision

- **Enable**: Prevents casual copying. Recommended for commercial fiction.
- **Disable**: Allows readers to convert formats freely. Some indie authors prefer this for reader goodwill.
- Once set, DRM cannot be changed without unpublishing and republishing.

### Page 3: Kindle eBook Pricing

| Field | What to Enter | Notes |
|---|---|---|
| KDP Select Enrollment | Optional | 90-day exclusive to Amazon. Enables Kindle Unlimited, higher royalty in some markets. |
| Territories | All territories (recommended) | Unless you have a reason to restrict |
| Royalty Plan | 70% or 35% | 70% requires price between $2.99–$9.99 USD |
| Pricing | Set price per marketplace | Set US price first; can auto-calculate others |

#### Pricing strategy for series fiction

- Book 1: $0.99–$2.99 (loss leader to hook readers)
- Book 2: $3.99–$4.99
- Books 3+: $4.99–$5.99
- Box set: $9.99
- 70% royalty = price must be $2.99–$9.99
- 35% royalty = any price (used for $0.99 books)
- KDP Select: exclusive to Amazon for 90 days, enables Kindle Unlimited (readers pay per page read)

#### KDP Select vs. wide distribution

| | KDP Select | Wide Distribution |
|---|---|---|
| Platforms | Amazon only | Amazon + Kobo, Apple Books, B&N, Google Play |
| Kindle Unlimited | Yes | No |
| Royalty (US) | 70% ($2.99+) | 70% ($2.99–$9.99) |
| Free promos | 5 days per 90-day period | Not available |
| Countdown deals | Yes | No |
| Best for | New authors, series starters | Established authors with audience everywhere |

## Pre-publication checklist

- [ ] Book details page complete (title, author, description, keywords, categories)
- [ ] Manuscript uploaded and Online Previewer checked
- [ ] Cover uploaded separately (not just embedded in EPUB)
- [ ] DRM decision made
- [ ] Pricing set for all territories
- [ ] KDP Select decision made
- [ ] Tax information complete
- [ ] Banking information complete
- [ ] Hit "Publish Your Kindle eBook"

## After publishing

- Book goes into review (typically 24–72 hours)
- You'll receive an email when live
- The book may appear on Amazon before the email arrives
- **Author Central**: claim your author page at [author.amazon.com](https://author.amazon.com)
- **A+ Content**: add enhanced marketing content after publishing

## Series management

- Always enter series name and volume number on Page 1
- Use the same series name exactly across all books
- Amazon links series books together automatically
- Update previous books' back matter ("Also by" page) when new books release
- Consider re-uploading Book 1 with updated "Also by" list

## Anti-patterns

- ❌ Publishing before EPUBCheck validation
- ❌ Using the EPUB-embedded cover instead of uploading separately
- ❌ Keywords that are single words instead of phrases
- ❌ Choosing broad categories when specific ones exist
- ❌ Pricing Book 1 at $5.99+ (too high for an unknown series)
- ❌ Forgetting to set series name and volume number
- ❌ Choosing KDP Select without understanding the 90-day exclusivity lock

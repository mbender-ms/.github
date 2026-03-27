---
name: epub-stylesheet
description: Create and maintain KDP-compatible CSS stylesheets for fiction ebooks that render perfectly on all Kindle devices
argument-hint: "[genre: romantic-fiction | sci-fi-with-parts | dual-pov] [component: full | scene-breaks | front-matter | epigraph]"
user-invocable: true
---

# epub-stylesheet

## Purpose

Create and maintain a professional CSS stylesheet for fiction ebooks that renders perfectly on all Kindle devices. The stylesheet is the bridge between your markdown and how the reader experiences your book.

Kindle's rendering engine is limited compared to a web browser. This skill encodes the rules that work, the patterns that break, and the genre-specific conventions that make your book look professional.

## When to use

- When setting up a new book project — generate the default `epub-styles.css`
- When customizing the visual presentation of your ebook for a specific genre
- When troubleshooting rendering issues on Kindle devices
- When adding front matter, epigraphs, or scene break styling

## The default fiction stylesheet

This is the baseline CSS that works reliably across all Kindle devices. Start here and customize for your genre.

```css
/* epub-styles.css — KDP-compatible fiction eBook stylesheet */

body {
  font-family: Georgia, serif;
  font-size: 1em;
  line-height: 1.6;
  margin: 0;
  padding: 0;
}

/* Chapter titles */
h1 {
  font-size: 1.6em;
  font-weight: bold;
  text-align: center;
  margin-top: 3em;
  margin-bottom: 1.5em;
  page-break-before: always;
}

/* Section headings */
h2 {
  font-size: 1.2em;
  font-weight: bold;
  margin-top: 2em;
  margin-bottom: 0.8em;
}

/* Body paragraphs — first-line indent, no spacing between paragraphs (fiction standard) */
p {
  text-indent: 1.5em;
  margin: 0;
  padding: 0;
}

/* Remove indent from first paragraph after a heading or scene break */
h1 + p, h2 + p, h3 + p, hr + p {
  text-indent: 0;
}

/* Scene break */
hr {
  border: none;
  text-align: center;
  margin: 1.5em auto;
}

hr::after {
  content: "* * *";
}
```

## Why these specific rules

Each rule in the default stylesheet exists for a reason:

### `font-family: Georgia, serif`

Georgia is the most readable serif on e-ink screens. Kindle allows reader override, so this is a fallback. If the reader hasn't chosen a font, Georgia gives them a clean, professional reading experience.

### `font-size: 1em`

Relative sizing. Never use `px` or `pt` in ebooks — readers control font size. `1em` means "whatever size the reader has chosen," which is exactly what you want.

### `line-height: 1.6`

Comfortable reading spacing for long fiction. Tighter than `1.8` (which feels loose) but more breathable than `1.4` (which feels cramped in long reading sessions).

### `text-indent: 1.5em`

Fiction standard: paragraphs are indented, no space between them. This is NOT the same as nonfiction (which uses block paragraphs with spacing). Fiction readers expect indented paragraphs — it's a genre convention that signals "this is a novel."

### `page-break-before: always` on H1

Forces a new page for each chapter. Readers expect chapters to start on a fresh page. Without this, a new chapter might start halfway down the page after the previous chapter's ending.

### `h1 + p { text-indent: 0 }`

First paragraph after a heading is never indented. This is a universal typographic convention in fiction and nonfiction alike. The heading already signals "new section" — the indent would be redundant.

### `hr::after { content: "* * *" }`

Scene breaks render as three asterisks, the fiction standard. A bare horizontal rule might render as nothing on some Kindle devices. The three asterisks are universally recognized as a scene break in fiction.

## Kindle CSS limitations

Things that DON'T work in Kindle's rendering engine:

| CSS Feature | Why It Fails |
|---|---|
| `position: fixed` or `position: absolute` | Not supported in reflowable ebooks |
| `float` | Unreliable on e-ink devices |
| Custom web fonts (`@font-face`) | Kindle uses its own font stack, reader can override |
| `@media` queries | Limited support; don't rely on them |
| `px` or `pt` units for text | Always use `em` or `%` — readers control font size |
| `columns` | Not supported |
| Complex selectors | Keep it simple; Kindle's renderer is limited |
| `background-image` | Unreliable |
| `transform` | Not supported |

**Rule of thumb**: If it wouldn't work in a 2010 web browser, it won't work on Kindle.

## Style variations

### 1. Romantic fiction (our primary use case)

Elegant chapter headings, generous spacing, and breathing room around scene breaks. The styling should feel warm and inviting.

```css
/* Romantic fiction — elegant and warm */

h1 {
  font-size: 1.6em;
  font-weight: bold;
  text-align: center;
  margin-top: 3em;
  margin-bottom: 1.5em;
  page-break-before: always;
}

/* Wider paragraph indent for a traditional feel */
p {
  text-indent: 1.5em;
  margin: 0;
  padding: 0;
}

/* Scene breaks with decorative separator */
hr {
  border: none;
  text-align: center;
  margin: 2em auto;
}

hr::after {
  content: "❧";
  font-size: 1.2em;
}

/* Generous margins around scene breaks for pacing and breathing room */
hr + p {
  text-indent: 0;
  margin-top: 0.5em;
}

/* Italics for internal thoughts */
.thought {
  font-style: italic;
}
```

### 2. Epic sci-fi with parts

Multi-level heading structure for books organized into parts and chapters. Supports epigraphs and in-universe communications.

```css
/* Epic sci-fi — structured with parts and chapters */
/* Use --epub-chapter-level=2 with pandoc so Parts are H1 and Chapters are H2 */

/* Part headings */
h1 {
  font-size: 2em;
  font-weight: bold;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-top: 4em;
  margin-bottom: 2em;
  page-break-before: always;
}

/* Chapter headings under parts */
h2 {
  font-size: 1.4em;
  font-weight: bold;
  text-align: center;
  margin-top: 3em;
  margin-bottom: 1.5em;
  page-break-before: always;
}

/* Epigraph styling for in-universe quotes at chapter starts */
.epigraph {
  font-style: italic;
  text-align: center;
  margin: 2em 2em 1.5em 2em;
  font-size: 0.9em;
}

.epigraph-source {
  text-align: right;
  font-style: normal;
  font-size: 0.85em;
  margin-top: 0.5em;
}

/* Monospace styling for in-universe communications and logs */
.communication, .log-entry {
  font-family: "Courier New", monospace;
  font-size: 0.9em;
  margin: 1em 1.5em;
  padding: 0;
}
```

### 3. Dual POV (alternating character chapters)

For novels that alternate between two character perspectives. The chapter heading includes the character name, and you can optionally add subtle visual differentiation.

```css
/* Dual POV — alternating character chapters */

/* Chapter heading with character name */
h1 {
  font-size: 1.6em;
  font-weight: bold;
  text-align: center;
  margin-top: 3em;
  margin-bottom: 0.5em;
  page-break-before: always;
}

/* Character name subtitle under chapter heading */
.pov-character {
  text-align: center;
  font-size: 1.1em;
  font-style: italic;
  font-weight: normal;
  margin-bottom: 1.5em;
}

/* Optional subtle visual differentiation between POVs */
.pov-a p {
  text-indent: 1.5em;
}

.pov-b p {
  text-indent: 1.5em;
}
```

## Epigraph styling

For in-universe quotes, excerpts, or atmospheric text placed before a chapter begins:

```css
.epigraph {
  font-style: italic;
  text-align: center;
  margin: 2em 2em 1.5em 2em;
  font-size: 0.9em;
}

.epigraph-source {
  text-align: right;
  font-style: normal;
  font-size: 0.85em;
  margin-top: 0.5em;
}
```

Usage in markdown (with pandoc divs):

```markdown
::: {.epigraph}
"The stars don't care about your problems. That's what makes them so comforting."

::: {.epigraph-source}
— Captain Elara Voss, personal log, stardate 4471.2
:::
:::
```

## Front matter styling

Title page, copyright page, and dedication all have their own conventions:

```css
.title-page {
  text-align: center;
  margin-top: 30%;
}

.copyright {
  font-size: 0.85em;
  text-align: center;
  margin-top: 20%;
}

.dedication {
  font-style: italic;
  text-align: center;
  margin-top: 30%;
}
```

The large `margin-top` percentages push content down the page, centering it vertically. This is the most reliable vertical centering method on Kindle.

## Testing your stylesheet

1. **Build the EPUB with your CSS**: `pandoc ... --css=epub-styles.css`
2. **Open in Calibre viewer** for a quick check — fast iteration, close enough for layout review
3. **Open in Kindle Previewer** for accurate Kindle rendering — this is the ground truth
4. **Test with font size changes** — your layout must survive the reader making text bigger or smaller
5. **Test on both e-ink (Paperwhite) and Fire tablet profiles** — e-ink is grayscale, Fire has color

If something looks wrong in Kindle Previewer, it will look wrong on the reader's device. Fix it before publishing.

## Anti-patterns

- ❌ Using absolute font sizes (`px`, `pt`) — readers control font size
- ❌ Using background colors or images — e-ink is grayscale
- ❌ Complex CSS layouts — Kindle's renderer is basic
- ❌ Nonfiction paragraph styling in fiction (block paragraphs with spacing instead of indented)
- ❌ Custom fonts that Kindle will ignore anyway
- ❌ Negative margins or positioning hacks
- ❌ Styling that breaks when reader changes font size

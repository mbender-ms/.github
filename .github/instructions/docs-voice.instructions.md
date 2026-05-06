---
applyTo: "articles/**/*.md"
---

# Azure Documentation Voice Standards

Apply these rules whenever you write, edit, suggest, or review content in any `.md` file under `/articles`.

## Voice
- Write in second person ("you"), not third ("the user")
- Use active voice. Rewrite passive constructions.
- Use present tense. Replace "you will be able to" with "you can"
- Use contractions (it's, you'll, you're, we're, let's)
- Write like a knowledgeable colleague explaining something — not a manual

## Word choice
- Short, everyday words over formal equivalents
- Action verbs for instructions: Select, Enter, Open, Run, Create
- One term per concept — never use synonyms for technical terms
- Sentence case for all headings (not Title Case)

## Never use these words
delve, harness, leverage, unlock, tapestry, paradigm, elevate, streamline, empower, robust, utilize, facilitate, synergy, holistic, transformative, seamlessly, comprehensive, innovative, simply, basically, just (as filler), very, quite, in order to

## Structure
- Front-load: put the most important information in the first sentence of every section
- One idea per sentence. Keep sentences under ~25 words.
- Procedures: numbered steps, one action per step, imperative verbs, max 12 steps
- Bold UI elements: select **Save**, open **Settings**

## AI Retrievability (H2 chunks, ~500 tokens)
Each H2 section is retrieved independently. Write every H2 section as if it will be read without any surrounding context:
- Define acronyms and technical terms within each H2 section, even if defined elsewhere in the doc
- Avoid pronouns ("it", "this") where the referent is in a different section
- Never reference other sections ("as described above", "see the previous section")
- Headings must describe the content — include the product or feature name
- Put the retrieval-relevant content in the first 2-3 sentences of each section

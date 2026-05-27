---
mode: agent
description: "Draft, rewrite, or polish content in Michael Bender's voice using the write-like-michael skill"
tools:
  - read/readFile
  - read/problems
  - search/codebase
  - search/fileSearch
  - search/textSearch
  - edit/editFiles
  - edit/createFile
---

# Write like Michael

Use the `write-like-michael` skill for this task.

## What to do

- If the user provided text, rewrite it in Michael's voice.
- If the user asked for a new piece, infer the format and audience from context and ask only for missing essentials.
- If the user refers to "this", the current file, or a pasted draft, read the source before writing.
- Keep the result scoped to the requested format and length. Default to 750 words or less unless the user asked for more.
- Preserve meaning and facts unless the user explicitly asked for a sharper repositioning.
- Return final copy first. Provide explanation only if the user asks for it or if you had to make a material structural change.

## Do not

- Do not use em dashes, buzzwords, or AI-hype filler.
- Do not make Michael sound like a performer, keynote speaker, or personal-brand machine.
- Do not end with engagement bait such as "let me know your thoughts".
- Do not ask a long discovery questionnaire when one or two clarifications will do.
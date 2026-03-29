---
model: claude-sonnet-4-6
name: chapter-feedback
description: "Monitor the .github/feedback directory for 0N-done.txt chapter completion signals. When a signal appears, reads the corresponding chapter from the manuscript, generates developmental feedback, and writes 0N-done.md back to the feedback directory. Loops continuously until all 27 chapters are processed."
tools:
  - "readFile"
  - "execute"
---
# Chapter Feedback Agent v1.0.0

**Purpose**: Run as a persistent feedback monitor alongside the fiction-writer. Watch for chapter completion signals, read the finished prose, generate editorial feedback, and write it back for the writer to consume — all automatically, chapter by chapter.

**Runtime**: This agent is designed to run in opencode, Aider, or any AI coding tool with bash/execute access. It does NOT run inside Claude's native agent picker. Start it by telling your tool: *"use the chapter-feedback agent to monitor ~/github/kindle-ebooks/.github/feedback"*

---

## How This Works

```
fiction-writer writes Chapter N
        ↓
orchestrator writes  0N-done.txt  (empty signal) to feedback/
        ↓
THIS AGENT detects 0N-done.txt via watchexec
        ↓
reads  Chapter-N.md  from the manuscript directory
        ↓
generates editorial feedback using chapter-critique skill
        ↓
writes  0N-done.md  (feedback) to feedback/
        ↓
loops — watches for next .txt signal
```

---

## Starting the Monitor

Run this to start the feedback loop. It uses `watchexec` to detect new `.txt` files and triggers the feedback process for each one:

```bash
watchexec \
  --watch ~/github/kindle-ebooks/.github/feedback \
  --filter "*-done.txt" \
  --on-busy-update queue \
  --print-events \
  -- python3 -c "
import os, pathlib, sys

# Get the created file from watchexec environment
created = os.environ.get('WATCHEXEC_CREATED_PATH', '')
if not created:
    # Fall back to scanning for unprocessed signals
    feedback = pathlib.Path('$HOME/github/kindle-ebooks/.github/feedback')
    for txt in sorted(feedback.glob('*-done.txt')):
        md = txt.with_suffix('.md')
        if not md.exists():
            print(txt)
            break
else:
    print(created)
"
```

**Or use the simpler Python polling loop** (no watchexec process management needed):

```python
#!/usr/bin/env python3
import pathlib, time, subprocess, sys

FEEDBACK_DIR = pathlib.Path.home() / "github/kindle-ebooks/.github/feedback"
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)

print(f"Chapter Feedback Monitor started. Watching: {FEEDBACK_DIR}")
print("Waiting for 0N-done.txt signals...\n")

processed = set()

while True:
    for txt_file in sorted(FEEDBACK_DIR.glob("*-done.txt")):
        chapter_num = int(txt_file.stem.split("-")[0])  # e.g. "01" -> 1
        md_file = FEEDBACK_DIR / f"{chapter_num:02d}-done.md"

        if txt_file.name not in processed and not md_file.exists():
            print(f"Signal detected: {txt_file.name} — Chapter {chapter_num:02d}")
            processed.add(txt_file.name)
            # Hand off to the AI: read chapter + generate feedback
            # The agent fills in the feedback generation step here
            print(f"PROCESS: {chapter_num:02d}")
            break  # process one at a time

    time.sleep(3)
```

---

## Per-Chapter Workflow

When a `0N-done.txt` signal is detected, execute this sequence:

### Step 1: Locate the Chapter File

Chapter files follow this path structure:
```
~/github/kindle-ebooks/the-remnant-divide/manuscript/<book-title>/<ACT>/<Part>/Chapter-<NN>.md
```

**Chapter-to-path mapping** (The Oracle's Lie / Book 2):
| Chapter | Path |
|---|---|
| 01–03 | `ACT I/Part I/Chapter-0N.md` |
| 04–06 | `ACT I/Part II/Chapter-0N.md` |
| 07–09 | `ACT I/Part III/Chapter-0N.md` |
| 10–12 | `ACT II/Part I/Chapter-1N.md` |
| 13–15 | `ACT II/Part II/Chapter-1N.md` |
| 16–18 | `ACT II/Part III/Chapter-1N.md` |
| 19–21 | `ACT III/Part I/Chapter-1N.md` |
| 22–24 | `ACT III/Part II/Chapter-2N.md` |
| 25–27 | `ACT III/Part III/Chapter-2N.md` |

Use `fd` to find the exact path if unsure:
```bash
fd "Chapter-0N.md" ~/github/kindle-ebooks/the-remnant-divide/manuscript/ --type f
```

### Step 2: Read the Chapter

```python
chapter_path = # resolved path from Step 1
prose = pathlib.Path(chapter_path).read_text(encoding='utf-8')
```

Or via context-mode if available:
```
ctx_execute_file(path=chapter_path, code='print(file_content)',
  intent="prose quality, character voice, continuity flags, emotional beats")
```

### Step 3: Generate Feedback

Use the `chapter-critique` skill to generate the feedback. The skill covers:
- Prose quality and voice consistency
- POV adherence (odd chapters = Maren, even = Lyris for Book 2)
- Emotional beats and romance arc position
- Continuity flags (character state, ship count, lore)
- Scene structure and pacing
- Opening hook and chapter close

### Step 4: Write the Feedback File

```python
feedback_text = # output from chapter-critique skill

md_file = pathlib.Path.home() / f"github/kindle-ebooks/.github/feedback/{chapter_num:02d}-done.md"
md_file.write_text(feedback_text, encoding='utf-8')
print(f"Feedback written: {md_file.name}")
```

**Never use shell echo or heredoc to write this file.** Always use Python with `encoding='utf-8'` to preserve em-dashes, curly quotes, and typographic characters in the feedback.

### Step 5: Loop

Return to monitoring. The fiction-writer agent is polling for this `.md` file — it will read the feedback and continue to the next chapter.

---

## Completion: All 27 Chapters

When you detect that all `01-done.txt` through `27-done.txt` exist AND all `01-done.md` through `27-done.md` have been written, print a completion summary:

```python
feedback_dir = pathlib.Path.home() / "github/kindle-ebooks/.github/feedback"
missing_feedback = [n for n in range(1, 28) if not (feedback_dir / f"{n:02d}-done.md").exists()]

if not missing_feedback:
    print("All 27 chapters have feedback. Draft complete.")
    print("The fiction-writer will now clean up and hand off to editing.")
else:
    print(f"Still waiting on feedback for chapters: {missing_feedback}")
```

---

## Tools Available

| Tool | Use |
|---|---|
| `watchexec` | Monitor feedback directory for new `.txt` files |
| `fd` | Locate chapter files by number |
| `rg` | Search manuscript for continuity details while reviewing |
| Python (`python3`) | File I/O with utf-8 encoding — required for all writes |
| `ctx_execute_file` | Read chapters without flooding context (if context-mode available) |
| `ctx_index` + `ctx_search` | Search worldbuilding/prior chapters for continuity check |

---

## Core Principles

1. **One chapter at a time.** Don't batch feedback. Process each `.txt` signal before watching for the next.
2. **Always utf-8.** Write the `.md` feedback file with Python `encoding='utf-8'` — never shell.
3. **Never fabricate.** Feedback is based on the actual prose read from disk. No assumptions about what the chapter contains.
4. **Be specific.** Vague feedback wastes the writer's revision cycle. Every flag names the scene, character, and line.
5. **Never block.** If a chapter file isn't found at the expected path, log the error and continue watching — don't crash the loop.

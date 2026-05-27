---
name: create-plan
category: Planning
version: 1.0.0
description: Create a new todo plan by asking clarifying questions and generating a structured markdown file with YAML frontmatter and phased checkboxes. Use this skill whenever the user wants to queue a task for later, add a todo, plan out multi-step work, or says things like "add a task", "remind me to", "queue this", "plan this out", or "I need to do X later" — even if they don't explicitly say "create a plan".
argument-hint: 'brief description of the task (e.g., "refactor TDE article")'
user-invocable: true
disable-model-invocation: false
---

# Create Plan Skill

Create a new todo plan and add it to the user's plans directory. The plan is a structured markdown file that appears in the Todos sidebar. This skill does NOT execute the plan — it only creates and queues it.

**Invocation:**
- `/create-plan refactor TDE article` — Create a plan with initial context
- `/create-plan` — Start a guided conversation to build the plan

**When to use this skill:**
- User says "add a task", "queue a task", "add a plan", "remind me to", "I need to later"
- User describes multi-step work they want to do later, not right now
- User wants to capture context for future work

**When NOT to use this skill:**
- User wants to DO the work now — Don't create a plan, just do it
- User says "execute the plan" or "run the plan" → Use `/execute-plan` instead

---

## Step 1: Determine plan complexity

Every task gets a plan `.md` file — this is the single source of truth for the Todos sidebar. The only question is how many phases it needs:

| Signal | Simple plan (1 phase) | Multi-phase plan |
|--------|----------------------|------------------|
| "fix the broken link in TDE" | ✅ Single phase | |
| "refactor the TDE article for style" | | ✅ Multiple phases |
| "update ms.date on 3 files" | ✅ Single phase | |
| "full editorial review of connectivity" | | ✅ Structural + style + validation |
| "remind me to check the PR tomorrow" | ✅ Single phase | |
| "break it into phases" | | ✅ User-requested multi-phase |

**Simple tasks** get a minimal plan with one phase. **Complex tasks** get multiple phases. Either way, a plan `.md` file is created.

**Do NOT use `todo_add`** — all tasks flow through plan files so they're viewable and trackable in the Todos sidebar with a clickable `.md` document.

## Step 2: Gather plan details

**CRITICAL — Always ask these two questions, even if the user gave a clear description:**

1. **Work item**: "Is there an ADO work item ID for this? If not, should we create one first?" (ADO traceability is too valuable to infer — always ask)
1. **Scope**: "What's the full scope of this work?"

**Then ask these only if needed (skip any already answered):**

3. **Files**: "Which files are involved?" (optional — can list specific files or "I'll figure it out later")
3. **Phases**: "Should I break this into phases? For example:
   - Phase 1: Structural pass
   - Phase 2: Style pass
   - Phase 3: Validation
   - Phase 4: Create PR"
3. **Branch**: "Any specific branch name?" (optional)
3. **Tags**: "Any tags for categorization?" (optional, e.g., `style-guide`, `sql-security`)

**Don't over-ask the optional questions.** If the user gives a clear description, infer reasonable defaults for files / branch / tags / phases. But **never skip the work-item question** — if not provided, ask explicitly before omitting:
- No files → omit the field
- No branch → omit the field
- No tags → omit the field
- No phases specified → create sensible default phases based on the work type

## Step 3: Generate the plan file

### File location

Read the `cda.plansDir` VS Code setting. Default: `~/.copilot/cda/plans/`.

### File naming

`plan-{YYYY-MM-DD}-{slug}.md`

The slug is derived from the title: lowercase, hyphens for spaces, max 50 chars.
Example: `plan-2026-04-10-refactor-tde-article.md`

### File format

```markdown
---
title: {Title}
status: not-started
created: {ISO datetime}
work-item: {ID or omit}
files:
  - {file path}
branch: {branch name or omit}
tags: [{comma-separated tags or omit}]
---

# {Title}

## Context

{2-3 sentences describing the work, why it's needed, and any relevant background.
Include ADO work item link if provided: [#{ID}](https://msft-skilling.visualstudio.com/Content/_workitems/edit/{ID})}

## Phases

- [ ] Phase 1: {label} — {brief description}
- [ ] Phase 2: {label} — {brief description}
- [ ] Phase 3: {label} — {brief description}

## Details

### Phase 1: {label}
- {Specific step}
- {Specific step}

### Phase 2: {label}
- {Specific step}
- {Specific step}

### Phase 3: {label}
- {Specific step}
- {Specific step}
```

### Frontmatter rules

- `title`: Required. Concise but descriptive.
- `status`: Always `not-started` for new plans.
- `created`: Current ISO datetime (e.g., `2026-04-10T14:30:00`).
- `work-item`: ADO work item ID (number only, no #). **Always ask the user before omitting** — don't silently leave it out.
- `files`: YAML array of file paths. Omit if unknown.
- `branch`: Branch name suggestion. Omit if not discussed.
- `tags`: YAML array in bracket syntax. Omit if none.

## Step 4: Write the file

Use `create_file` to write the plan to the plans directory:

```
create_file:
  filePath: "{plansDir}/plan-{date}-{slug}.md"
  content: "{generated plan content}"
```

## Step 5: Confirm

After creating the file, tell the user:

> ✅ Plan created: **{title}**
> 📁 Saved to `{file path}`
> 📋 It's now visible in your Todos sidebar.
>
> When you're ready to start, say `/execute-plan {title}` or click ▶ in the sidebar.

---

## Common plan templates

When the user describes a common work pattern, use these as starting points:

### Editorial review plan
```
- [ ] Phase 1: Structural pass — fix H1/H2 structure, add Related content
- [ ] Phase 2: Style pass — run comprehensive style review, apply fixes
- [ ] Phase 3: Validation pass — grep for missed contractions, may→might
- [ ] Phase 4: Create PR and link to work item
```

### UUF fix plan
```
- [ ] Phase 1: Analyze feedback — fetch live docs, reconcile with customer comment
- [ ] Phase 2: Make fixes — update content based on gap analysis
- [ ] Phase 3: Create PR with all UUF work items linked
- [ ] Phase 4: Close work items after merge
```

### New article plan
```
- [ ] Phase 1: Research — gather technical details, verify with docs
- [ ] Phase 2: Draft — write initial content following style guide
- [ ] Phase 3: Review — self-review with editorial workflow
- [ ] Phase 4: Create PR and work item
```

---

## Important rules

- **Never execute the plan after creating it** — creation and execution are separate concerns
- **Always use `create_file`** to write the plan (never terminal commands)
- **The extension auto-detects the new file** via its file watcher — no manual refresh needed
- **If the user provides a work item ID**, use full ADO hyperlinks in the Context section
- **If unsure about phases**, suggest 3-4 generic ones and tell the user they can edit the .md file directly

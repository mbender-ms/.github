---
name: execute-plan
category: Planning
version: 1.0.0
description: Execute an existing queued todo plan by walking through its phases step by step. Reads plan files from the configured plans directory, matches to user prompt, and guides execution with confirmation between phases. Use this skill whenever the user says "execute the plan", "run the plan", "start the plan", "work on the plan", or references a specific queued task they want to do now. Use /create-plan to create new plans first.
argument-hint: 'plan title or keyword (e.g., "refactor TDE", "connectivity guide")'
user-invocable: true
disable-model-invocation: false
---

# Execute Plan Skill

Execute an existing queued todo plan by walking through its phases step by step. Plans are markdown files stored in the user's plans directory with YAML frontmatter and phase checklists.

**This skill RUNS plans, it does NOT create them.** To create a new plan, use `/create-plan`.

**Invocation:**
- `/execute-plan refactor TDE` — Execute the plan matching "refactor TDE"
- `/execute-plan` — List active plans and ask which to execute

---

## Step 1: Locate the plans directory

Read the `cda.plansDir` VS Code setting to find the plans directory. Default is `~/.copilot/cda/plans/`.

```
run_in_terminal: cat ~/.copilot/cda/plans/*.md | head -5
```

Or list plan files:

```
run_in_terminal: ls ~/.copilot/cda/plans/*.md
```

## Step 2: Find the matching plan

1. List all `.md` files in the plans directory
1. Read each file's YAML frontmatter to get the `title` and `status` fields
1. Match the user's argument against plan titles (fuzzy match — the argument may be a keyword or partial title)
1. If multiple matches, ask the user to clarify
1. If no matches, inform the user and list available plans
1. Skip plans with `status: completed`

## Step 3: Load the plan context

Read the full plan `.md` file. The plan contains:

- **Frontmatter**: title, status, work-item ID, files to edit, branch name, tags
- **Context section**: Background on what the work involves
- **Phases section**: Checkbox list of phases to execute
- **Details section**: Detailed instructions for each phase

## Step 4: Execute phases

For each uncompleted phase (checkbox shows `- [ ]`):

1. **Announce the phase**: "Starting Phase N: {phase label}"
1. **Read the Details section** for that phase — it contains specific instructions, files to edit, commands to run
1. **Execute the work** described in the phase details
1. **Ask for confirmation**: "Phase N complete. Ready for Phase N+1?" (in guided mode)
1. **Update the plan file**: Check off the phase (`- [ ] → - [x]`) and update the `status` field:
   - First phase started → `status: in-progress`
   - Some phases done → `status: partial`
   - All phases done → `status: completed`

### Updating the plan file

After completing each phase, update the plan `.md` file:

```
replace_string_in_file:
  oldString: "- [ ] Phase N: {label}"
  newString: "- [x] Phase N: {label}"
```

And update the status in frontmatter:

```
replace_string_in_file:
  oldString: "status: not-started"
  newString: "status: in-progress"
```

## Step 5: Completion

When all phases are complete:

1. Set `status: completed` in frontmatter
1. Inform the user: "All phases complete! Plan '{title}' is done."
1. Ask: "Should I archive this plan?" (moves to `~/.copilot/cda/plans/archive/`)
1. If the plan has a `work-item` field, ask: "Should I update ADO work item #{work-item} with a progress comment?"

---

## Execution modes

| Mode | Behavior |
|------|----------|
| **Guided** (default) | Pause between phases for user confirmation |
| **Autonomous** | Execute all phases without pausing (user says "run autonomously" or "run all phases") |

## Important rules

- **Always read the plan file first** — don't assume plan contents from the title alone
- **Update the plan file after each phase** — this is the persistent record of progress
- **Respect the phase order** — execute phases sequentially, don't skip ahead
- **If a phase fails**, update status to `partial` and stop — don't continue to the next phase
- **If the plan references a work-item**, use full ADO hyperlinks (never bare #NUMBER)
- **If the plan references a branch**, check if you're on that branch before starting

---
mode: agent
description: "Stage, commit, push, branch, and create PRs following my conventions — one commit per file, gh CLI for PRs"
tools:
  - execute/runInTerminal
  - execute/getTerminalOutput
  - read/readFile
  - search/textSearch
  - search/fileSearch
  - todo
---

# Git Workflow — Branch, Commit, Push, PR

Automate the full git workflow: sync upstream → create branch → stage + commit per file → push → create PR. Works in any repo.

---

## Inputs (infer from context or ask)

| Input | Required | Default | Example |
|-------|----------|---------|---------|
| **Service name** | For branching/PR | Infer from changed file paths | `load-balancer` |
| **Brief description** | For branching/PR | Infer from changes | `freshness-review` |
| **Work item ID** | No | None | `554195` |
| **Workflow type** | For PR title | `Maintenance` | `Maintenance`, `Freshness`, `CAMP` |

If inputs aren't provided, infer service name from file paths (e.g., `articles/load-balancer/` → `load-balancer`) and description from the nature of changes.

---

## Workflow Steps

Execute steps in order. **Skip steps that don't apply** (e.g., if already on a feature branch, skip branching; if user only said "commit," skip push/PR).

### Step 0 — Prereq checks

```bash
git --version
gh --version 2>/dev/null || echo "gh CLI not installed — install from https://cli.github.com/"
gh auth status 2>/dev/null || echo "gh CLI not authenticated — run: gh auth login"
```

Only check `gh` if the workflow includes PR creation. Don't block commit/push on `gh` availability.

### Step 1 — Sync upstream (if starting from main)

Check which remotes exist and sync accordingly:

```bash
git remote -v
```

- If `upstream` exists: `git fetch upstream main && git merge upstream/main`
- If only `origin`: `git fetch origin main && git merge origin/main`
- If already on a feature branch with uncommitted changes: **skip this step entirely**

### Step 2 — Create feature branch

Only if currently on `main` or user explicitly requests a new branch.

```bash
git checkout -b mbender-ms/<service>-<description>-<id>
```

- Use the branch naming convention: `mbender-ms/<service>-<brief-description>-<work-item-id>`
- Omit `<work-item-id>` segment if no work item ID was provided
- Examples: `mbender-ms/load-balancer-freshness-review-554195`, `mbender-ms/networking-fix-broken-links`

### Step 3 — Analyze changes

```bash
git status --porcelain
git diff --name-only
git diff --cached --name-only
```

Build a list of all modified, added, and deleted files. Show the user a summary:

```
Changed files:
  M  articles/load-balancer/health-probes.md
  M  articles/load-balancer/media/probes/screenshot.png
  A  articles/load-balancer/new-article.md
```

### Step 4 — Stage and commit (one commit per file)

For each changed file, create a separate commit:

```bash
git add <file>
git commit -m "docs: <imperative verb> <what changed>"
```

**Commit message rules:**
- Format: `docs: <imperative verb> <what changed>`
- One file per commit — never batch multiple files
- No `AB#` references in commit messages
- Use imperative mood: "update," "add," "fix," "remove," "correct"

**Examples:**
- `docs: update ms.date and modernize language` (for a freshness review)
- `docs: add health probe configuration article`
- `docs: fix cross-reference path to NAT Gateway`
- `docs: update portal screenshot for health probes`

If a file is already staged (`git diff --cached`), commit it as-is without re-adding.

### Step 5 — Push to origin (**CONFIRMATION GATE**)

**Before pushing**, show the user:
1. Current branch name
2. Number of commits to push
3. Commit log: `git log --oneline origin/main..HEAD` (or `@{u}..HEAD` if tracking branch exists)

```
Ready to push 3 commits on branch mbender-ms/load-balancer-freshness-554195:
  abc1234 docs: update ms.date and modernize language
  def5678 docs: fix cross-reference path to NAT Gateway
  ghi9012 docs: update portal screenshot

Push to origin? (waiting for confirmation)
```

**Wait for user confirmation** before running `git push origin <branch>`.

**Exception**: If the user's original request included explicit push intent (e.g., "commit and push," "push it," "send it"), skip the confirmation gate and push immediately.

### Step 6 — Create pull request (**CONFIRMATION GATE**)

Only if the user requested PR creation (e.g., "create PR," "open PR," "full workflow").

#### 6a. Generate PR title and body

**PR title format:** `<Service Name> | <Workflow Type> | Short description`
- Examples: `Load Balancer | Freshness | Update health probe documentation`
- If no service/type context, use a plain descriptive title

**PR body**: Load `copilot/skills/my-workflow/references/pr-framework.md` and generate the body following that template. Include:
- **Article intent** — reader-perspective paragraph
- **Description of work** — categorized bullet list of changes
- **Files** — every changed file with path and annotation
- **`AB#<work-item-id>`** — at the bottom of the body (if work item ID provided)

#### 6b. Show draft for confirmation

Display the generated title and body, then **wait for user confirmation**.

**Exception**: If the user explicitly said "create the PR" or "full auto," skip confirmation.

#### 6c. Create the PR

**Primary method — `gh` CLI:**

```bash
gh pr create --title "<title>" --body "<body>" --base main
```

**Fallback — VS Code PR extension:** If `gh` is unavailable, instruct the user to use the VS Code GitHub Pull Request extension to create the PR manually, and provide the title/body for copy-paste.

After creation, show the PR URL.

---

## Partial Execution

Match user intent to the appropriate subset of steps:

| User says | Steps to run |
|-----------|-------------|
| "commit" | 3, 4 |
| "commit and push" | 3, 4, 5 (auto-push, no gate) |
| "push" | 5 (just push current commits) |
| "create branch" | 1, 2 |
| "create PR" / "open PR" | 0, 5, 6 (push + PR) |
| "full workflow" / "ship it" | 0–6 (everything) |
| "stage" / "add" | 3 (show status), then `git add` specified files |

---

## Error Handling

| Error | Action |
|-------|--------|
| `gh: command not found` | Print: "Install GitHub CLI: https://cli.github.com/ — then run `gh auth login`" |
| `gh auth` fails | Print: "Run `gh auth login` to authenticate" |
| Already on `main` with uncommitted changes | Warn: "You have uncommitted changes on main. Create a feature branch first?" |
| No changes detected | Print: "No modified files found. Nothing to commit." |
| Push rejected (behind remote) | Run `git pull --rebase origin <branch>` then retry push |
| Merge conflicts on upstream sync | Print conflict files and ask user to resolve before continuing |

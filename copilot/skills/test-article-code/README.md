# Test Article Code

A VS Code Copilot skill that executes and validates every runnable code block in a Microsoft Learn article against live Azure resources, reports documentation bugs, and — when you ask — fixes them through a proper pull request.

Use it to answer one question with confidence: **"Does the code a reader would copy from this article actually work?"**

---

## Prerequisites

| Requirement | How to verify |
|-------------|---------------|
| **VS Code** (1.100+) with **GitHub Copilot** in agent mode | Copilot Chat → mode dropdown → "Agent" available |
| **Azure CLI** | `az version` |
| **Azure PowerShell** (only if the article has a PowerShell tab) | `Get-Module -ListAvailable Az.Accounts` |
| **An Azure subscription** you can create/delete test resources in | `az account show` |
| **Git remotes** `origin` (your fork) and `upstream` (MicrosoftDocs) — only for the optional fix flow | `git remote -v` |

You do **not** need to pre-install every article-specific extension or module — the skill checks what's present and only installs what's missing.

---

## Installation

Copy the `test-article-code/` folder to your Copilot skills directory:

```powershell
Copy-Item -Recurse .\copilot\skills\test-article-code\ "$env:USERPROFILE\.copilot\skills\test-article-code"
```

Restart VS Code. To also expose the companion prompt as a `/` command, run the repo's `sync-prompts.ps1` (it copies `assets/*.prompt.md` into your VS Code prompts directory):

```powershell
cd C:\github\.github
.\sync-prompts.ps1
```

### Folder structure

```
test-article-code/
├── SKILL.md     # The skill instructions (loaded by the agent)
├── README.md    # This file (for humans)
└── assets/
    └── test-article-autopilot.prompt.md   # Companion /slash-command prompt
```

---

## What it does

1. **Enumerates** every runnable code block in the article (and its `[!INCLUDE]` files), grouped by tab: Azure CLI, Azure PowerShell, Bash.
2. **Checks prerequisites with you first** — authentication, tooling, and prerequisite resources may already exist, so it won't blindly re-run setup.
3. **Authenticates** and selects the right subscription/tenant.
4. **Maps placeholders** (`<resource-group-name>`, `<perimeter-name>`, …) to real resource names — generating sensible defaults when you don't supply any.
5. **Runs the commands** one at a time (or in autopilot), echoing output and verifying results.
6. **Reports every error** with the command, exact error text, root cause, and possible solutions.
7. **Asks before cleanup**, then summarizes results and **documentation findings**.
8. **Optionally fixes** the doc bugs end-to-end: feature branch → edit → commit → push → draft PR with `AB#` link → work-item comment.

---

## How it works

### Phase 1 — Test

- Reads the article and included files, lists code blocks by tab.
- Confirms auth, tooling, and prerequisite resources with you.
- Runs Azure CLI commands first; after they pass, asks before starting Azure PowerShell.
- Adapts Bash-style `azurecli` syntax to PowerShell when needed and calls out the change.
- Stops on any error and reports cause + fix.

### Phase 2 — Report

- A pass/fail results table for each section.
- A findings list: missing steps, tab inconsistencies, shell-syntax mismatches, version drift.

### Phase 3 — Fix (optional, only if you ask)

- Branches from `upstream/main`, applies minimal edits, commits (no `AB#` in the commit), pushes to your fork, and opens a **draft** PR against `MicrosoftDocs:main` with `AB#<id>` in the body.

---

## Execution modes

| Mode | Behavior | Deletions |
|------|----------|-----------|
| **Step** (default) | Runs one code block, reports, waits for your approval, repeats. | Require approval |
| **Autopilot** | Runs all non-destructive commands back-to-back without pausing. | **Always** require approval, even here |

Cleanup is never automatic — the skill always asks before deleting anything.

---

## Usage

Open **GitHub Copilot Chat** in agent mode with the article open, then try any of the examples below.

### 1. Basic test (step mode)

> "Test the code in this article."

The agent will:
1. List the code blocks it found (CLI, PowerShell, etc.).
2. Ask about prerequisites and confirm you're signed in to the right subscription.
3. Run each command one at a time, pausing for your approval between commands.
4. Report results and findings; ask before cleaning up.

### 2. Autopilot (hands-off except deletions)

> "Test this how-to in autopilot, but confirm before any deletes."

Runs everything non-destructive without pausing, and stops only for deletions and cleanup.

### 3. Test only one tab

> "Just test the Azure CLI commands in this article."

Skips the PowerShell and portal tabs.

### 4. Prerequisites already done

> "I'm already logged in to the right subscription and the NSPs exist — test the article."

The agent verifies your state, skips redundant login/setup, and asks you for the real resource names to substitute for the placeholders.

### 5. Provide a specific subscription or tenant

> "Test the code using subscription d9f0f529-… in tenant 888d76fa-…"

The agent signs in to that tenant (device-code flow if a browser doesn't open), sets the subscription, then proceeds.

### 6. Let the skill name resources

> "Test this article — create whatever resources it needs."

When you don't supply names, the agent generates defaults and shows them before creating anything:

| Resource | Example |
|---|---|
| Resource group | `resource-group-test001`, `resource-group-test002` |
| Virtual network | `virtual-network-001` |
| Other resources | `storage-account-001`, `key-vault-001` |

### 7. Test and fix the doc bugs

> "Test this how-to, then fix any errors you find. Work item is 595434."

After testing, the agent applies minimal fixes on a feature branch and opens a draft PR against `MicrosoftDocs:main` with `AB#595434` linked, then comments the PR link on the work item. It pauses for your approval before pushing.

### 8. Use the companion prompt (pre-filled autopilot + fix flow)

> `/test-article-autopilot`

Runs the most common variant without you restating the options: autopilot on (deletions still gated), CLI before PowerShell, prerequisite check first, default naming, and the optional fix→draft-PR flow. It accepts two inputs — `article` (defaults to the open file) and `workitem` (the `AB#` ID).

---

## Documentation findings

At the end of a run the agent lists concrete doc issues it found. Typical classes:

| Finding | Example |
|---|---|
| **Missing step** | A delete command needs a name the article never shows how to obtain (needs a prior `list`). |
| **Tab inconsistency** | The CLI tab omits a step the PowerShell tab includes. |
| **Shell-syntax mismatch** | Bash-only syntax in a block a reader might run in PowerShell. |
| **Version drift** | A pinned preview/module version no longer matches reality. |

---

## When to use this skill

| Use this skill when… | Use another skill when… |
|---|---|
| You want to confirm the runnable commands in an article actually work | You want a writing-style or metadata review (`pr-review`, style skills) |
| You want to catch missing steps, tab mismatches, and broken commands | You want external fact-checking against Microsoft Learn (`doc-verifier`) |
| You want the doc bugs fixed via a proper PR after testing | You're authoring a brand-new article from scratch |

---

## Safety notes

- **Deletions always require explicit approval**, including in autopilot and during cleanup.
- Test resources are created in the subscription you confirm — some may be **billable**. The agent shows generated names before creating anything.
- The optional fix flow never commits to `main`, never puts `AB#` in commit messages, and opens PRs against `upstream` (MicrosoftDocs), not your fork.

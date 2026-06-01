---
name: branch-cleanup
description: >
  Clean up local and remote git branches in the current repository. Deletes every branch
  EXCEPT `main` and any branch whose name starts with `release`. Use whenever Michael says
  things like "clean up branches", "delete old branches", "prune branches", "branch cleanup",
  or "get rid of stale branches". Always shows the plan and asks for confirmation before
  deleting. Never touches `main` or `release*` branches.
---

# Branch Cleanup Skill

Removes stale git branches from the current repository. Keeps `main` and any branch starting
with `release` (e.g. `release-build-preview-anyscale`, `release/1.2`). Everything else is
deleted both locally and on the remote.

---

## Protected branches (never deleted)

- `main`
- Any branch whose name starts with `release` (case-sensitive)

If the repo's default branch is something other than `main` (e.g. `master`, `Main`), STOP and
confirm with Michael before proceeding. Do not assume.

---

## Workflow

### 1. Verify repo state

Run from the target repo's working directory:

```powershell
git rev-parse --show-toplevel
git branch --show-current
git fetch --all --prune
```

Confirm the repo path matches what Michael expects. If the current branch is about to be
deleted, switch to `main` first:

```powershell
git checkout main
```

### 2. Build the deletion list

```powershell
# Local branches to delete
$localToDelete = git branch --format='%(refname:short)' |
  Where-Object { $_ -ne 'main' -and $_ -notmatch '^release' }

# Remote branches to delete (origin)
$remoteToDelete = git branch -r --format='%(refname:short)' |
  Where-Object { $_ -like 'origin/*' } |
  ForEach-Object { $_ -replace '^origin/','' } |
  Where-Object { $_ -ne 'HEAD' -and $_ -ne 'main' -and $_ -notmatch '^release' }
```

### 3. Show the plan and confirm

Print both lists to Michael. Wait for explicit "yes" before deleting. Never auto-proceed.

### 4. Delete

```powershell
# Local — force delete so unmerged branches are removed too
foreach ($b in $localToDelete) { git branch -D $b }

# Remote
foreach ($b in $remoteToDelete) { git push origin --delete $b }
```

### 5. Verify and report

```powershell
git fetch --all --prune
$remaining = git branch --format='%(refname:short)'
```

Post a summary in chat with:

- **Total branches deleted** (local + remote counts from step 2)
- **Total branches remaining** (count of `$remaining`)
- **Current branches** — bulleted list of every name in `$remaining`

Confirm only `main` + `release*` survived. If any non-protected branch remains, flag it.

---

## Safety rules

- ALWAYS run `git fetch --all --prune` first so the local view is current.
- ALWAYS show the deletion list and require explicit confirmation before any `git branch -D`
  or `git push --delete`.
- NEVER delete `main` or any branch matching `^release`.
- NEVER run this skill across multiple repos in one pass — one repo at a time, confirmed.
- If a branch deletion fails (e.g. protected branch on remote), report it and continue with
  the rest. Do not retry with `--force` flags beyond what's listed above.

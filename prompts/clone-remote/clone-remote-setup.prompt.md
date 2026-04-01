---
mode: agent
description: "Clone azure-docs-pr and configure origin + upstream remotes with safe idempotent checks"
tools:
  - execute/runInTerminal
  - execute/getTerminalOutput
  - read/readFile
  - search/textSearch
  - todo
---

# Clone Repo And Configure Remotes

Automate first-time setup for `azure-docs-pr`: ensure local folder exists, clone if needed, then add or correct `origin` and `upstream` remotes.

---

## Defaults

| Setting | Default |
|---------|---------|
| Base directory | `C:/github` |
| Local repo folder | `azure-docs-pr` |
| Origin owner | `mbender-ms` |
| Upstream owner | `MicrosoftDocs` |
| Repo name | `azure-docs-pr` |

Expected URLs:
- `origin`: `https://github.com/mbender-ms/azure-docs-pr.git`
- `upstream`: `https://github.com/MicrosoftDocs/azure-docs-pr.git`

If the user provides overrides (path, owners, SSH), apply them.

---

## Inputs (infer or ask)

| Input | Required | Default | Example |
|-------|----------|---------|---------|
| Base directory | No | `C:/github` | `D:/src` |
| Repo name | No | `azure-docs-pr` | `azure-docs-pr` |
| Origin owner | No | `mbender-ms` | `contoso-user` |
| Upstream owner | No | `MicrosoftDocs` | `MicrosoftDocs` |
| URL mode | No | `https` | `ssh` |

When `URL mode` is `ssh`, use:
- `origin`: `git@github.com:<origin-owner>/<repo>.git`
- `upstream`: `git@github.com:<upstream-owner>/<repo>.git`

---

## Workflow Steps

### Step 0 - Prereq checks

```powershell
git --version
gh --version 2>$null
```

If `gh` is missing, continue anyway. This workflow only requires `git`.

### Step 1 - Ensure base directory exists

```powershell
$base = "C:/github"
if (-not (Test-Path $base)) { New-Item -ItemType Directory -Path $base | Out-Null }
Set-Location $base
```

### Step 2 - Clone or reuse local repo

```powershell
$repo = "azure-docs-pr"
$localPath = Join-Path $base $repo
$originUrl = "https://github.com/mbender-ms/azure-docs-pr.git"

if (-not (Test-Path $localPath)) {
  git clone $originUrl
} else {
  Set-Location $localPath
  if (-not (Test-Path ".git")) {
    throw "Folder exists but is not a git repository: $localPath"
  }
}

Set-Location $localPath
```

### Step 3 - Add or correct remotes

Set expected URLs based on defaults or user overrides, then enforce them.

```powershell
$expectedOrigin = "https://github.com/mbender-ms/azure-docs-pr.git"
$expectedUpstream = "https://github.com/MicrosoftDocs/azure-docs-pr.git"

$originExists = git remote | Select-String -SimpleMatch "origin"
$upstreamExists = git remote | Select-String -SimpleMatch "upstream"

if ($originExists) {
  git remote set-url origin $expectedOrigin
} else {
  git remote add origin $expectedOrigin
}

if ($upstreamExists) {
  git remote set-url upstream $expectedUpstream
} else {
  git remote add upstream $expectedUpstream
}
```

### Step 4 - Verify and fetch

```powershell
git remote -v
git fetch upstream --prune
```

Show a short final summary:
- Repo path
- Origin URL
- Upstream URL
- Current branch

```powershell
git branch --show-current
```

---

## Remote Setup Options

Support all of these without breaking idempotency:

1. **Fresh clone + new remotes**: clone and add `upstream`.
2. **Already cloned, remotes correct**: no-op except verification.
3. **Already cloned, remote missing**: add missing remote.
4. **Already cloned, remote incorrect**: repair with `git remote set-url`.
5. **HTTPS mode**: default URLs.
6. **SSH mode**: convert both remotes to SSH URLs.

---

## Error Handling

| Error | Action |
|-------|--------|
| `git: command not found` | Stop and print: install Git first, then rerun. |
| Folder exists but no `.git` | Stop and ask user whether to rename/delete folder manually. |
| Clone/auth failure | Print exact git error and suggest checking repo access/auth. |
| Upstream fetch fails | Keep remote configuration, report failure, continue with status output. |

---

## Example One-Shot Execution

```powershell
$base = "C:/github"
$repo = "azure-docs-pr"
$localPath = Join-Path $base $repo
$expectedOrigin = "https://github.com/mbender-ms/azure-docs-pr.git"
$expectedUpstream = "https://github.com/MicrosoftDocs/azure-docs-pr.git"

if (-not (Test-Path $base)) { New-Item -ItemType Directory -Path $base | Out-Null }
Set-Location $base

if (-not (Test-Path $localPath)) {
  git clone $expectedOrigin
}

Set-Location $localPath
if (-not (Test-Path ".git")) { throw "Not a git repo: $localPath" }

if (git remote | Select-String -SimpleMatch "origin") { git remote set-url origin $expectedOrigin } else { git remote add origin $expectedOrigin }
if (git remote | Select-String -SimpleMatch "upstream") { git remote set-url upstream $expectedUpstream } else { git remote add upstream $expectedUpstream }

git remote -v
git fetch upstream --prune
git branch --show-current
```

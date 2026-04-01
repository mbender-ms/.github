---
mode: agent
description: "SSH-first clone and remote setup for azure-docs-pr with idempotent remote enforcement"
tools:
  - execute/runInTerminal
  - execute/getTerminalOutput
  - todo
---

# SSH-First Clone And Remote Setup

Run a compact setup for `azure-docs-pr` that:
- creates `C:/github` if missing
- clones `mbender-ms/azure-docs-pr` if missing using SSH
- enforces `origin` and `upstream` SSH URLs
- fetches `upstream`
- prints a short final status block

## Defaults

- Base directory: `C:/github`
- Repo folder: `azure-docs-pr`
- Origin URL: `git@github.com:mbender-ms/azure-docs-pr.git`
- Upstream URL: `git@github.com:MicrosoftDocs/azure-docs-pr.git`
- URL mode: `ssh` (default)

If the user requests HTTPS, switch both remotes to:
- `https://github.com/mbender-ms/azure-docs-pr.git`
- `https://github.com/MicrosoftDocs/azure-docs-pr.git`

## Execution Rules

1. Do not ask follow-up questions unless required for a missing, user-requested override.
2. Keep output concise: one final status block and errors only.
3. Use idempotent commands (`set-url` for existing remotes, `add` when missing).
4. Stop on fatal errors (`git` missing, not a git repo, clone/auth failure).

## Command Sequence

```powershell
$ErrorActionPreference = "Stop"

$base = "C:/github"
$repo = "azure-docs-pr"
$localPath = Join-Path $base $repo
$originUrl = "git@github.com:mbender-ms/azure-docs-pr.git"
$upstreamUrl = "git@github.com:MicrosoftDocs/azure-docs-pr.git"

git --version | Out-Null

if (-not (Test-Path $base)) {
  New-Item -ItemType Directory -Path $base | Out-Null
}

Set-Location $base

if (-not (Test-Path $localPath)) {
  git clone $originUrl
}

Set-Location $localPath
if (-not (Test-Path ".git")) {
  throw "Folder exists but is not a git repository: $localPath"
}

$remotes = git remote
if ($remotes -match "^origin$") {
  git remote set-url origin $originUrl
} else {
  git remote add origin $originUrl
}

if ($remotes -match "^upstream$") {
  git remote set-url upstream $upstreamUrl
} else {
  git remote add upstream $upstreamUrl
}

git fetch upstream --prune

$originFinal = git remote get-url origin
$upstreamFinal = git remote get-url upstream
$branch = git branch --show-current

Write-Output "RepoPath: $localPath"
Write-Output "Origin: $originFinal"
Write-Output "Upstream: $upstreamFinal"
Write-Output "Branch: $branch"
```

## Final Response Format

After execution, return only:
- Success or failure
- Repo path
- Origin URL
- Upstream URL
- Current branch

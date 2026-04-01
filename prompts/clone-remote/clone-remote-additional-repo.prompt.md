---
mode: agent
description: "Clone any additional repo or fork URL/path into C:/github and optionally configure origin/upstream remotes"
tools:
  - execute/runInTerminal
  - execute/getTerminalOutput
  - todo
---

# Clone Additional Repo Or Fork

Clone any user-provided repository URL or local path into the default directory `C:/github` and optionally configure `origin` and `upstream` remotes.

## Defaults

- Base directory: `C:/github`
- Clone source: required (repo URL or local path)
- Local folder name: inferred from source (can be overridden)
- URL mode: preserve source style (HTTPS or SSH)

Accepted clone source examples:
- `https://github.com/<owner>/<repo>.git`
- `git@github.com:<owner>/<repo>.git`
- `https://dev.azure.com/<org>/<project>/_git/<repo>`
- `C:/repos/some-local-mirror`

## Inputs

Ask only if missing:

1. Clone source URL/path (required)
2. Optional local folder override
3. Optional upstream URL (for fork workflows)
4. Optional URL mode conversion (`https` or `ssh`)

## Execution Rules

1. Always clone/install under `C:/github` unless user explicitly overrides base path.
2. Use safe idempotent behavior:
- if folder does not exist, clone
- if folder exists and is a git repo, reuse it
- if folder exists and is not a git repo, stop with a clear message
3. Configure `origin` to the provided source URL when it is a remote URL.
4. Configure `upstream` only when the user supplies an upstream URL.
5. Keep output concise with one final status block.

## Command Sequence Template

```powershell
$ErrorActionPreference = "Stop"

$base = "C:/github"
$source = "<REQUIRED_URL_OR_PATH>"
$repo = "<OPTIONAL_LOCAL_FOLDER_OR_INFERRED>"
$upstreamUrl = "<OPTIONAL_UPSTREAM_URL>"

if (-not (Test-Path $base)) {
  New-Item -ItemType Directory -Path $base | Out-Null
}

# Infer repo folder when not provided.
if ([string]::IsNullOrWhiteSpace($repo)) {
  $name = Split-Path -Leaf $source
  if ($name.EndsWith(".git")) { $name = $name.Substring(0, $name.Length - 4) }
  $repo = $name
}

$localPath = Join-Path $base $repo
Set-Location $base

if (-not (Test-Path $localPath)) {
  git clone $source $repo
}

Set-Location $localPath
if (-not (Test-Path ".git")) {
  throw "Folder exists but is not a git repository: $localPath"
}

# Keep origin aligned to the provided remote URL when applicable.
if ($source -match "^(https://|git@|ssh://)") {
  $remotes = git remote
  if ($remotes -match "^origin$") {
    git remote set-url origin $source
  } else {
    git remote add origin $source
  }
}

# Optional upstream setup when provided.
if (-not [string]::IsNullOrWhiteSpace($upstreamUrl)) {
  $remotes = git remote
  if ($remotes -match "^upstream$") {
    git remote set-url upstream $upstreamUrl
  } else {
    git remote add upstream $upstreamUrl
  }
  git fetch upstream --prune
}

$originFinal = "(not configured)"
$upstreamFinal = "(not configured)"

try { $originFinal = git remote get-url origin } catch {}
try { $upstreamFinal = git remote get-url upstream } catch {}

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
- Origin URL or `(not configured)`
- Upstream URL or `(not configured)`
- Current branch

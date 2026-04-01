---
mode: agent
description: "Batch install multiple repos or forks into C:/github from URLs/paths with optional upstream setup"
tools:
  - execute/runInTerminal
  - execute/getTerminalOutput
  - todo
---

# Batch Install Repos And Forks

Install multiple repositories in one run. Accept a list of source URLs/paths and clone each into `C:/github` (default), with optional `upstream` remote setup per repository.

## Defaults

- Base directory: `C:/github`
- Input list format: one item per line
- Local folder name: inferred from source unless overridden
- URL mode: preserve source style (HTTPS or SSH)

Supported source examples:
- `https://github.com/<owner>/<repo>.git`
- `git@github.com:<owner>/<repo>.git`
- `https://dev.azure.com/<org>/<project>/_git/<repo>`
- `C:/repos/local-mirror`

## Required Input

Ask for a batch list in this format (one repo per line):

```text
<source>[|<local-folder-override>][|<upstream-url>]
```

Examples:

```text
https://github.com/mbender-ms/azure-docs-pr.git|azure-docs-pr|https://github.com/MicrosoftDocs/azure-docs-pr.git
git@github.com:mbender-ms/azure-docs.git|azure-docs|git@github.com:MicrosoftDocs/azure-docs.git
C:/repos/internal-mirror|internal-mirror
```

## Execution Rules

1. Always install under `C:/github` unless the user explicitly overrides base path.
2. Process each line independently and continue on non-fatal errors.
3. For each entry:
- create base directory if missing
- clone if local folder missing
- if local folder exists and is a git repo, reuse it
- if local folder exists and is not a git repo, mark as failed and continue
4. Configure remotes idempotently:
- set/add `origin` when source is a remote URL
- set/add `upstream` only when provided
5. Keep final output as a compact summary table plus totals.

## Command Sequence Template

```powershell
$ErrorActionPreference = "Continue"

$base = "C:/github"
$lines = @(
  "<SOURCE1>|<OPTIONAL_LOCAL1>|<OPTIONAL_UPSTREAM1>",
  "<SOURCE2>|<OPTIONAL_LOCAL2>|<OPTIONAL_UPSTREAM2>"
)

if (-not (Test-Path $base)) {
  New-Item -ItemType Directory -Path $base | Out-Null
}

$results = @()

foreach ($line in $lines) {
  if ([string]::IsNullOrWhiteSpace($line)) { continue }

  $parts = $line.Split("|", 3)
  $source = $parts[0].Trim()
  $repo = if ($parts.Length -ge 2) { $parts[1].Trim() } else { "" }
  $upstreamUrl = if ($parts.Length -ge 3) { $parts[2].Trim() } else { "" }

  if ([string]::IsNullOrWhiteSpace($source)) { continue }

  if ([string]::IsNullOrWhiteSpace($repo)) {
    $name = Split-Path -Leaf $source
    if ($name.EndsWith(".git")) { $name = $name.Substring(0, $name.Length - 4) }
    $repo = $name
  }

  $localPath = Join-Path $base $repo
  $status = "Success"
  $detail = ""

  try {
    Set-Location $base

    if (-not (Test-Path $localPath)) {
      git clone $source $repo
      if ($LASTEXITCODE -ne 0) { throw "Clone failed" }
    }

    Set-Location $localPath
    if (-not (Test-Path ".git")) {
      throw "Folder exists but is not a git repository"
    }

    if ($source -match "^(https://|git@|ssh://)") {
      $remotes = git remote
      if ($remotes -match "^origin$") {
        git remote set-url origin $source
      } else {
        git remote add origin $source
      }
    }

    if (-not [string]::IsNullOrWhiteSpace($upstreamUrl)) {
      $remotes = git remote
      if ($remotes -match "^upstream$") {
        git remote set-url upstream $upstreamUrl
      } else {
        git remote add upstream $upstreamUrl
      }
      git fetch upstream --prune
    }
  }
  catch {
    $status = "Failed"
    $detail = $_.Exception.Message
  }

  $originFinal = "(not configured)"
  $upstreamFinal = "(not configured)"

  try { $originFinal = git -C $localPath remote get-url origin } catch {}
  try { $upstreamFinal = git -C $localPath remote get-url upstream } catch {}

  $results += [PSCustomObject]@{
    RepoPath = $localPath
    Status = $status
    Origin = $originFinal
    Upstream = $upstreamFinal
    Detail = $detail
  }
}

$results | Format-Table -AutoSize | Out-String

$total = $results.Count
$success = ($results | Where-Object { $_.Status -eq "Success" }).Count
$failed = ($results | Where-Object { $_.Status -eq "Failed" }).Count

Write-Output "Totals: total=$total success=$success failed=$failed"
```

## Final Response Format

Return only:
- Batch status summary
- One row per repo with: path, status, origin, upstream, short detail
- Totals: total, success, failed

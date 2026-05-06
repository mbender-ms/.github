#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Link a repo's .github subfolder to the canonical .github workspace customizations.

.DESCRIPTION
    Creates directory junctions for agents, skills, instructions, and prompts
    under {repo}/.github/ pointing to c:\github\.github\{folder}.
    Run this whenever you add a new repo to the VS Code workspace.

.PARAMETER RepoPath
    Full path to the repo root. Defaults to the current directory.

.EXAMPLE
    .\link-workspace-tools.ps1
    .\link-workspace-tools.ps1 -RepoPath c:\github\my-new-repo

.NOTES
    Uses directory junctions (no admin rights required).
    Safe to re-run — skips existing junctions, replaces plain directories.
    Do NOT run against repos you do not own (e.g. MicrosoftDocs/azure-docs-pr).
    Git will surface all junction targets as untracked files in those repos.
#>

param(
    [string]$RepoPath = (Get-Location).Path
)

$source  = "c:\github\.github"
$ghDir   = Join-Path $RepoPath ".github"
$folders = @("agents", "skills", "instructions", "prompts")

if (-not (Test-Path $RepoPath)) {
    Write-Error "Repo path not found: $RepoPath"
    exit 1
}

Write-Host "Linking workspace tools into: $ghDir"
New-Item -ItemType Directory -Force $ghDir | Out-Null

foreach ($folder in $folders) {
    $link = Join-Path $ghDir $folder
    $src  = Join-Path $source $folder

    if (-not (Test-Path $src)) {
        Write-Warning "Source folder does not exist, skipping: $src"
        continue
    }

    if (Test-Path $link) {
        $item = Get-Item $link -Force
        if ($item.LinkType -eq "Junction") {
            Write-Host "  SKIP (junction already exists): $folder"
            continue
        }
        Write-Host "  REPLACING plain directory with junction: $folder"
        Remove-Item $link -Recurse -Force
    }

    New-Item -ItemType Junction -Path $link -Target $src | Out-Null
    Write-Host "  LINKED: $folder -> $src"
}

Write-Host ""
Write-Host "Done. Reload VS Code window to pick up new customizations (Ctrl+Shift+P > Developer: Reload Window)."

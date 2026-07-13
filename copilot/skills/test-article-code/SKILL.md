---
name: test-article-code
description: 'Test the runnable code in a Microsoft Learn article (Azure CLI, Azure PowerShell, Bash) against live Azure resources, one command at a time, then report documentation findings and optionally fix them. USE FOR: "test the code in this article", "validate the commands in this how-to", "run the article code blocks", "verify the CLI/PowerShell steps work", "test article and fix errors", "does the code in this doc work". Covers auth, placeholder-to-resource mapping, per-tab execution (CLI then PowerShell), error reporting, cleanup, findings, and an optional feature-branch -> commit -> PR fix flow with AB# linking. DO NOT USE FOR: writing new articles, style/metadata review, or non-runnable content.'
argument-hint: 'Path to the article to test (defaults to the open file); optionally: subscription, tenant, resource names, and "autopilot"'
---

# Test Article Code

Execute and validate every runnable code block in a documentation article against real Azure resources, surface any doc bugs, and (optionally) fix them via a proper PR.

## When to use

- "Test the code in this article" / "validate the commands in this how-to"
- "Run the article's CLI and PowerShell steps and tell me what breaks"
- "Test the article, then fix any errors you find"
- Any request to confirm that the commands a reader would copy actually work end-to-end.

## Core principles

1. **One command at a time.** Run a single code block, report the result, and pause for approval before the next — unless autopilot is on (see below).
2. **Deletions ALWAYS require explicit approval**, even in autopilot mode. Never auto-run destructive commands (`delete`, `remove`, `purge`, `rm`, `--yes` on a destroy, `Remove-*`, drop, force-push).
3. **Test what the reader copies.** Prefer the article's exact commands; only adapt shell syntax when the target shell requires it, and call out the adaptation.
4. **Report every error** with the command, the exact error text, the root cause, and one or more possible solutions — then stop and wait.
5. **Leave no residue.** Offer to clean up any resources the test created — but always ask before deleting; the user may want to keep them.
6. **Capture findings as you go** — missing steps, tab inconsistencies, wrong syntax, stale versions — and present them at the end.

## Execution modes

Ask the user (or accept from arguments) which mode to use:

- **Step mode (default):** run one code block, report, wait for approval, repeat.
- **Autopilot mode:** run all non-destructive code blocks back-to-back without pausing, reporting each result inline. **Deletion/destructive steps still stop and require explicit approval.** Announce when autopilot pauses for a deletion.

By default, run all commands of one tab (for example, Azure CLI) before starting the next tab (for example, Azure PowerShell), and get approval before switching tabs.

## Procedure

### 1. Enumerate the code blocks

1. `read_file` the target article (default to the open editor file).
2. Follow and read any `[!INCLUDE ...]` files it pulls in — prerequisites and sign-in steps often live there.
3. List every runnable code block, grouped by tab/tool (`azurecli`, `azurepowershell`, `bash`, etc.). Skip portal click-through steps (nothing to run).
4. Note the logical flow (prereqs -> auth -> setup -> create -> verify -> cleanup) so you test in a runnable order.

### 2. Check prerequisites WITH the user (they may already be done)

Before doing any setup, confirm current state — do not blindly re-run prerequisite steps the user has already completed. Check and ask:

- **Authentication:** run `az account show` (and `Get-AzContext` if PowerShell is in scope). If already signed in to the right subscription/tenant, skip login.
- **Tooling:** check required CLI version, extensions (`az extension show`), and PowerShell modules (`Get-Module -ListAvailable`). If already installed at a sufficient version, skip the install steps and say so.
- **Prerequisite resources:** the article's placeholders (`<resource-group-name>`, `<perimeter-name>`, etc.) need real resources. Ask the user whether the prerequisite resources already exist or need to be created. If they exist, collect the real names; if not, agree on a setup plan (this may create billable resources — confirm the subscription).

Summarize what's already satisfied vs. what still needs doing, then proceed.

### 3. Authenticate and select subscription

- If not signed in, or the target subscription isn't visible: `az login`. If a browser window doesn't open, retry with `az login --use-device-code` and give the user the URL + code. For a specific directory, use `az login --tenant <tenant-id>`.
- Set context: `az account set --subscription <id>` and confirm with `az account show`.
- Common error: *"The subscription '...' doesn't exist in cloud 'AzureCloud'."* -> the subscription is in a different tenant or the account lacks access. Fix with `az login --tenant <tenant-id>`, then re-set the subscription.

### 4. Map placeholders to real values

Build a small table mapping each `<placeholder>` in the article to the real resource name to use (link name, perimeter names, resource group, profiles, IDs). Show it to the user before running the impactful commands so they can confirm.

**Default naming conventions.** When the user hasn't specified names (and no prerequisite resources exist to reuse), generate names from the spelled-out, hyphenated resource type plus an incrementing three-digit suffix starting at `001`. Increment the suffix for each additional resource of the same type.

| Resource | Pattern | Example |
|---|---|---|
| Resource group | `resource-group-test###` | `resource-group-test001`, `resource-group-test002` |
| Virtual network | `virtual-network-###` | `virtual-network-001` |
| Other resources | `<resource-type>-###` | `storage-account-001`, `key-vault-001` |

Keep names lowercase and hyphenated, honor each service's length/character limits (shorten the type name only when a service requires it, e.g., storage accounts), and always show the generated names to the user before creating anything.

### 5. Run the commands

For each code block, in order:

1. **Adapt shell syntax if needed.** `azurecli` blocks use Bash conventions (`var=$(...)`, `echo "$var"`). In PowerShell, translate to `$var = ...; Write-Output $var`, and set any variable in the **same** invocation it's used in (a fresh shell may not retain it). Call out the adaptation.
2. **Run it and echo the output** in the response.
3. **Verify results.** If a create/remove cmdlet's own output is swallowed by terminal echo, confirm with a follow-up read (`... show` / `Get-*`) so the result is unambiguous.
4. **Destructive commands:** present the command, get explicit approval (always, even in autopilot), then run it. Answer interactive confirmation prompts (`Are you sure? (y/n)`) with `y`. The article may note a `--yes` flag to skip the prompt — test as written unless the user prefers otherwise.
5. **On error:** stop and report:
   - the exact command,
   - the exact error text,
   - the most likely root cause,
   - one or more concrete solutions.
   Wait for direction before continuing.

### 6. Clean up (always ask first)

**Never delete test resources automatically.** When testing is done, list the resources the test created and ask the user whether to remove them — they may want to keep them (for example, to continue a tutorial or inspect state). Only on explicit approval, remove each resource and verify the removal took effect. Cleanup deletions follow the same rule as any other deletion: they always require approval, even in autopilot mode.

### 7. Report results and findings

- A results table: each section/command and pass/fail.
- A findings list: concrete documentation issues discovered, each with what's wrong and the recommended fix. Typical finding classes:
  - **Missing step** — a command needs a value the article never shows how to obtain (e.g., a name that requires a prior `list`).
  - **Tab inconsistency** — one tab (CLI vs PowerShell) omits a step the other includes.
  - **Shell-syntax mismatch** — Bash-only syntax in a block a reader might run in PowerShell (usually expected for `azurecli`, note only).
  - **Version drift** — pinned preview/module versions that no longer match reality.

## Optional: apply the fixes (end-to-end through PR)

Only if the user wants the doc bugs fixed. Follow the repo's git rules (never commit to `main`; branch from `upstream/main`; AB# only in the PR body, never in commits).

1. **Get the work item ID** from the user (ask if unknown). Fetch its title for a proper AB# link.
2. **Branch:** `git fetch upstream` then `git checkout -b <service>-<slug> upstream/main`.
3. **Edit** the article with the minimal fixes; use `multi_replace_string_in_file` for multiple edits; re-read to verify.
4. **Commit** with a conventional message describing WHAT changed (no AB#).
5. **Push** to the fork (`origin`) — only after showing the user the commit and getting approval.
6. **PR** against `MicrosoftDocs:main` (upstream, not the fork). Put `AB#<id>` under `## Related work items` in the body. Create as **draft** unless told otherwise.
7. **Work item:** add a timeline comment linking the PR; update the Description's PR-info section if the user wants a durable record.

## Completion checklist

- [ ] Every runnable code block executed, or explicitly skipped with a reason.
- [ ] CLI tested before PowerShell (or agreed order), with approval to switch tabs.
- [ ] All deletions were approved individually.
- [ ] Cleanup was offered and, if approved, completed and verified (resources kept if the user chose to).
- [ ] Errors reported with cause + solution.
- [ ] Findings summarized; fixes applied only if requested.
